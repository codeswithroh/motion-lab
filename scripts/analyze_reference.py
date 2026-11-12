#!/usr/bin/env python3
"""Break a reference video down into numbers: shots, pacing, motion, palette, music, sync.

usage: analyze_reference.py <video> [--out DIR]   (needs ffmpeg; numpy; librosa for tempo/beats)

Writes DIR/report.md, DIR/report.json, DIR/shots.jpg (one tile per shot, in order) and
DIR/timeline.jpg (one tile per second, 6 per row: row r holds seconds 6r..6r+5).
Read report.md with both sheets: the numbers say when and how much, the tiles say what.
For a closer look at a stretch: ffmpeg -ss A -t 4 -i V -vf "fps=5,scale=320:-2,tile=5x4" -frames:v 1 out.jpg

What it measures
  shots     every hard cut (frame-difference spike), shot lengths, cuts per 2 s (the pacing curve)
  motion    mean absolute frame difference per frame (96x54 grey), share of still / moving frames,
            motion per second, cut frames excluded
  look      mean luma and the 6 dominant colours over the film, per-shot luma
  music     integrated LUFS, LRA, peak; tempo, beat grid, onsets; loudness and band balance
            per 0.5 s; drop-outs (>= 9 dB under the running level for >= 0.12 s) and the hit after each
  speech    whisper-cli transcript with times, when a ggml model is found
  sync      each cut's offset to the nearest beat and 8th note; share of cuts within one frame;
            share of motion peaks on the 8th grid; which cuts land on a drop-out's hit
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

import numpy as np

W, H = 96, 54


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def probe(path):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
              "-of", "json", path], text=True).stdout
    d = json.loads(out)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {"duration": float(d["format"]["duration"]), "width": v["width"], "height": v["height"],
            "fps": float(num) / float(den), "has_audio": any(s["codec_type"] == "audio" for s in d["streams"])}


def frames(path, fps, size=(W, H), pix="gray"):
    ch = 1 if pix == "gray" else 3
    raw = sh(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={size[0]}:{size[1]}",
              "-pix_fmt", pix, "-f", "rawvideo", "-"]).stdout
    a = np.frombuffer(raw, np.uint8)
    return a.reshape(-1, size[1], size[0], ch).astype(np.float32) if ch == 3 else a.reshape(-1, size[1], size[0]).astype(np.float32)


def find_cuts(rgb, fps):
    # colour-histogram distance + pixel difference; a cut is a spike well above its neighbourhood
    g = rgb.mean(-1)
    pix = np.abs(np.diff(g, axis=0)).mean((1, 2))
    hists = []
    for f in rgb:
        q = (f // 32).astype(int)
        idx = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
        hists.append(np.bincount(idx.ravel(), minlength=512) / idx.size)
    hists = np.array(hists)
    hd = 0.5 * np.abs(np.diff(hists, axis=0)).sum(1)
    score = hd * 100 + pix * 0.5
    cuts = []
    for i in range(len(score)):
        lo, hi = max(0, i - 6), min(len(score), i + 7)
        neigh = np.delete(score[lo:hi], i - lo)
        base = np.median(neigh) if len(neigh) else 0
        if score[i] > 18 and score[i] > 2.6 * base + 6:
            t = (i + 1) / fps
            if not cuts or t - cuts[-1] > 1.5 / fps:
                cuts.append(round(t, 3))
    return cuts, pix


def palette(rgb, k=6, seed=1):
    px = rgb[::3, ::3, ::3].reshape(-1, 3)
    rng = np.random.default_rng(seed)
    px = px[rng.choice(len(px), min(len(px), 40000), replace=False)]
    c = px[rng.choice(len(px), k, replace=False)]
    for _ in range(20):
        lab = ((px[:, None] - c[None]) ** 2).sum(-1).argmin(1)
        c = np.array([px[lab == j].mean(0) if (lab == j).any() else c[j] for j in range(k)])
    share = np.bincount(lab, minlength=k) / len(lab)
    order = np.argsort(share)[::-1]
    return [{"hex": "#%02x%02x%02x" % tuple(int(v) for v in c[j]), "share": round(float(share[j]), 3)} for j in order]


def lufs(path):
    err = sh(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], text=True).stderr
    tail = err[err.rfind("Summary:"):]
    get = lambda k: (re.search(k + r":\s+(-?[\d.]+)", tail) or [None, None])[1]
    return {"lufs": float(get("I") or 0), "lra": float(get("LRA") or 0), "true_peak_db": float(get("Peak") or 0)}


def audio(path):
    raw = sh(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "22050", "-f", "f32le", "-"]).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64), 22050


def music(y, sr):
    out = {}
    try:
        import librosa
    except ImportError:
        out["note"] = "pip install librosa for tempo, beats and onsets"
        librosa = None
    hop = 512
    S = np.abs(np.fft.rfft(np.lib.stride_tricks.sliding_window_view(np.pad(y, (0, 2048)), 2048)[::hop] * np.hanning(2048), axis=1)).T
    f = np.fft.rfftfreq(2048, 1 / sr)
    t = np.arange(S.shape[1]) * hop / sr
    rms = np.sqrt((np.lib.stride_tricks.sliding_window_view(np.pad(y, (0, 1024)), 1024)[::hop] ** 2).mean(1))[: S.shape[1]]
    db = 20 * np.log10(rms + 1e-9)
    bands = {"sub<120": (0, 120), "low120-500": (120, 500), "mid500-3k": (500, 3000), "high3k+": (3000, sr / 2)}
    prof = []
    for s in np.arange(0, len(y) / sr, 0.5):
        m = (t >= s) & (t < s + 0.5)
        if not m.any():
            continue
        tot = S[:, m].sum() + 1e-9
        prof.append({"t": round(float(s), 2), "db": round(float(db[m].mean()), 1),
                     **{k: round(float(S[(f >= a) & (f < b)][:, m].sum() / tot * 100)) for k, (a, b) in bands.items()}})
    out["profile"] = prof
    # drop-outs: >= 9 dB under the running 2 s median for >= 0.12 s
    win = int(2 * sr / hop)
    run = np.array([np.median(db[max(0, i - win): i + 1]) for i in range(len(db))])
    low = db < run - 9
    drops, i = [], 0
    while i < len(low):
        if low[i]:
            j = i
            while j < len(low) and low[j]:
                j += 1
            if (j - i) * hop / sr >= 0.12 and t[i] > 0.3 and t[min(j, len(t) - 1)] < len(y) / sr - 0.3:
                drops.append({"start": round(float(t[i]), 3), "end": round(float(t[min(j, len(t) - 1)]), 3),
                              "depth_db": round(float((run[i:j] - db[i:j]).mean()), 1)})
            i = j
        else:
            i += 1
    out["dropouts"] = drops
    if librosa:
        tempo, beats = librosa.beat.beat_track(y=y.astype(np.float32), sr=sr, units="time")
        tempo = float(np.atleast_1d(tempo)[0])
        # report the musical tempo in 70-140 (the tracker often doubles)
        while tempo > 140:
            tempo /= 2
        while tempo < 70:
            tempo *= 2
        onsets = librosa.onset.onset_detect(y=y.astype(np.float32), sr=sr, units="time")
        chroma = librosa.feature.chroma_cqt(y=y.astype(np.float32), sr=sr).mean(1)
        names = "C C# D D# E F F# G G# A A# B".split()
        out.update({"tempo_bpm": round(tempo, 1), "beat_s": round(60 / tempo, 4), "beats": [round(float(b), 3) for b in beats],
                    "onsets": [round(float(o), 3) for o in onsets],
                    "pitch_classes": [names[i] for i in np.argsort(chroma)[::-1][:4]]})
    return out


def grid_from(beats, beat_s, dur):
    # 8th-note grid from the tracked beats themselves (a fixed spacing drifts when the BPM estimate is off)
    if not beats or len(beats) < 2:
        return None
    b = np.array(beats)
    mids = (b[:-1] + b[1:]) / 2
    step = np.median(np.diff(b))
    head = np.arange(b[0] - step / 2, -1e-9, -step / 2)[::-1]
    tail = np.arange(b[-1] + step / 2, dur + step, step / 2)
    return np.sort(np.concatenate([head, b, mids, tail]))


def speech(path, outdir):
    models = glob.glob(os.path.expanduser("~/.cache/*/whisper/models/ggml-*.bin")) + glob.glob(os.path.expanduser("~/.cache/*/ggml-*.bin"))
    if not models or not sh(["which", "whisper-cli"]).stdout:
        return {"note": "no whisper-cli/ggml model found"}
    wav = os.path.join(outdir, "a16k.wav")
    sh(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", wav])
    txt = sh(["whisper-cli", "-m", sorted(models)[-1], "-f", wav, "-np"], text=True).stdout
    lines = [l.strip() for l in txt.splitlines() if l.strip().startswith("[")]
    return {"model": os.path.basename(sorted(models)[-1]), "lines": lines}


def shots_sheet(path, cuts, dur, outdir, cols=6):
    bounds = [0.0] + cuts + [dur]
    mids = [(a + b) / 2 for a, b in zip(bounds, bounds[1:])]
    files = []
    for i, m in enumerate(mids):
        fn = os.path.join(outdir, f"_s{i:03d}.jpg")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{m:.3f}", "-i", path, "-frames:v", "1", "-vf", "scale=320:-2", fn])
        files.append(fn)
    rows = (len(files) + cols - 1) // cols
    lst = os.path.join(outdir, "_list.txt")
    with open(lst, "w") as fh:
        for fn in files:
            fh.write(f"file '{fn}'\n")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf",
        f"tile={cols}x{rows}:padding=4:color=white", "-frames:v", "1", os.path.join(outdir, "shots.jpg")])
    for fn in files + [lst]:
        os.remove(fn)
    return [round(m, 2) for m in mids]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out")
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.video)[0] + "_analysis"
    os.makedirs(out, exist_ok=True)
    meta = probe(a.video)
    fps, dur = meta["fps"], meta["duration"]
    afps = min(fps, 30)
    rgb = frames(a.video, afps, pix="rgb24")
    cuts, pix = find_cuts(rgb, afps)
    shot_len = np.diff([0.0] + cuts + [dur])
    cutset = {int(round(c * afps)) - 1 for c in cuts}
    motion = np.array([v for i, v in enumerate(pix) if i not in cutset])
    per_sec = [round(float(pix[int(s * afps): int((s + 1) * afps)].mean()), 1) for s in range(int(dur))]
    pacing = [sum(1 for c in cuts if s <= c < s + 2) for s in range(0, int(np.ceil(dur)), 2)]
    rep = {"file": os.path.basename(a.video), **meta,
           "shots": {"count": len(shot_len), "cuts": cuts, "median_s": round(float(np.median(shot_len)), 2),
                     "mean_s": round(float(shot_len.mean()), 2), "min_s": round(float(shot_len.min()), 2),
                     "max_s": round(float(shot_len.max()), 2), "cuts_per_2s": pacing},
           "motion": {"mean": round(float(motion.mean()), 2), "still_share": round(float((motion < 0.5).mean()), 2),
                      "moving_share": round(float((motion > 2).mean()), 2), "per_second": per_sec},
           "look": {"mean_luma": round(float(rgb.mean()), 1), "palette": palette(rgb)}}
    if meta["has_audio"]:
        y, sr = audio(a.video)
        rep["loudness"] = lufs(a.video)
        rep["music"] = music(y, sr)
        rep["speech"] = speech(a.video, out)
        m = rep["music"]
        g = grid_from(m.get("beats"), m.get("beat_s"), dur) if m.get("beats") else None
        if g is not None:
            beat_grid = np.array(m["beats"])
            off8 = [float(c - g[np.argmin(abs(g - c))]) for c in cuts]
            offb = [float(c - beat_grid[np.argmin(abs(beat_grid - c))]) for c in cuts]
            thr = np.percentile(pix, 75)
            peaks = [(i + 1) / afps for i in range(1, len(pix) - 1) if pix[i] > thr and pix[i] >= pix[i - 1] and pix[i] >= pix[i + 1]]
            on8 = [min(abs(p - g)) <= 1.01 / afps for p in peaks]
            hits = [d["end"] for d in m["dropouts"]]
            rep["sync"] = {"cuts_within_1f_of_8th": round(float(np.mean(np.abs(off8) <= 1.01 / afps)), 2) if cuts else None,
                           "cuts_within_1f_of_beat": round(float(np.mean(np.abs(offb) <= 1.01 / afps)), 2) if cuts else None,
                           "median_cut_offset_to_8th_s": round(float(np.median(off8)), 3) if cuts else None,
                           "motion_peaks_on_8th": round(float(np.mean(on8)), 2) if peaks else None,
                           "cuts_on_dropout_hits": [c for c in cuts if any(abs(c - h) <= 0.12 for h in hits)]}
    shot_mids = shots_sheet(a.video, cuts, dur, out)
    rows = int(np.ceil(np.ceil(dur) / 6))
    sh(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", f"fps=1,scale=400:-2,tile=6x{rows}:padding=3:color=white",
        "-frames:v", "1", os.path.join(out, "timeline.jpg")])
    rep["shots"]["mid_times"] = shot_mids
    json.dump(rep, open(os.path.join(out, "report.json"), "w"), indent=1)

    L = [f"# {rep['file']}", "", f"{meta['width']}x{meta['height']} {fps:.2f} fps, {dur:.2f} s", ""]
    s = rep["shots"]
    L += ["## Shots", f"{s['count']} shots; median {s['median_s']} s, mean {s['mean_s']} s, min {s['min_s']}, max {s['max_s']}",
          f"cuts per 2 s: {s['cuts_per_2s']}", "cuts: " + " ".join(f"{c:.2f}" for c in s["cuts"]), ""]
    mo = rep["motion"]
    L += ["## Motion", f"mean {mo['mean']}, still {mo['still_share']:.0%}, moving {mo['moving_share']:.0%}",
          "per second: " + " ".join(str(v) for v in mo["per_second"]), ""]
    L += ["## Look", f"mean luma {rep['look']['mean_luma']}; palette " + ", ".join(f"{p['hex']} {p['share']:.0%}" for p in rep['look']['palette']), ""]
    if "music" in rep:
        m, ld = rep["music"], rep["loudness"]
        L += ["## Music", f"{ld['lufs']} LUFS, LRA {ld['lra']}, peak {ld['true_peak_db']} dBFS",
              f"tempo {m.get('tempo_bpm')} BPM (beat {m.get('beat_s')} s), pitch classes {m.get('pitch_classes')}",
              "drop-outs: " + (", ".join(f"{d['start']:.2f}-{d['end']:.2f} (-{d['depth_db']} dB)" for d in m["dropouts"]) or "none"),
              "", "| t | dB | sub | low | mid | high |", "|---|---|---|---|---|---|"]
        L += [f"| {p['t']} | {p['db']} | {p['sub<120']} | {p['low120-500']} | {p['mid500-3k']} | {p['high3k+']} |" for p in m["profile"]]
        L += ["", "## Speech"] + (rep["speech"].get("lines") or [rep["speech"].get("note", "none")]) + [""]
        if "sync" in rep:
            L += ["## Sync"] + [f"- {k}: {v}" for k, v in rep["sync"].items()]
    open(os.path.join(out, "report.md"), "w").write("\n".join(L) + "\n")
    print(os.path.join(out, "report.md"))


if __name__ == "__main__":
    sys.exit(main())
