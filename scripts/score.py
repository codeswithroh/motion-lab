#!/usr/bin/env python3
"""Write an original music bed + SFX for a film from one cue file, and export every music event
so the picture can ride it. Proven on the Whop spec ad (the person: "much better", "perfect").

usage: score.py score.json            (needs numpy + scipy; ffmpeg for SFX files)

score.json (all times in film seconds; see references/sync.md for a filled example):
{
  "duration": 27, "bpm": 90, "style": "trap" | "four",
  "root": 26,                       # MIDI note of the bass root (26 = D1). Pick the brand's mood:
                                    # dark/chromatic -> trap, root D/Eb; bright/tech -> four, root F/G
  "scale": [0, 1, -2, -1],          # bass riff intervals from the root (default: dark chromatic)
  "drops":  [[5.0, 5.3333]],        # music cuts out (a breath) ...
  "hits":   [5.3333, 23.3333],      # ... and slams back with an impact here: brand name, hero number, logo
  "end": 26.0,                      # last downbeat; one long 808 + impact rings out after it
  "sfx_dir": "assets/audio/sfx",
  "sfx": {                          # sounds on the picture's own actions
    "whoosh": [1.333, 2.667],       #   peak lands ON the cut (file's loudest sample is aligned)
    "pop": [0.12, 3.67],            #   a caption appears: one soft air swish, never per-letter clicks
    "ui": [["ui-press.mp3", 20.0, 0.45]]   # any file at a time and gain
  },
  "out": "assets/audio/score.wav", "cues": "assets/cues.js"
}

Writes the WAV (44.1 kHz stereo, about -9 LUFS like a mastered ad) and cues.js:
  window.CUES = {kick:[...], clap:[...], roll:[...], bass:[...], drops:[[a,b]], hits:[...], end:s}
Mux the WAV straight into the delivery MP4 (the renderer re-levels audio ~4 dB down):
  ffmpeg -i film.mp4 -i score.wav -map 0:v -map 1:a -c:v copy -af "aresample=192000,
  alimiter=limit=0.7:level=disabled,aresample=48000" -c:a aac -b:a 256k -shortest out.mp4
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
cfg = json.load(open(sys.argv[1]))
DUR = float(cfg["duration"])
BPM = float(cfg.get("bpm", 90))
STYLE = cfg.get("style", "trap")
ROOT = int(cfg.get("root", 26))
SCALE = cfg.get("scale", [0, 12, 13, 10, 11])
DROPS = [tuple(d) for d in cfg.get("drops", [])]
HITS = cfg.get("hits", [])
END = float(cfg.get("end", DUR - 1.0))
BEAT = 60.0 / BPM
STEP = BEAT / 4
BAR = BEAT * 4
N = int(DUR * SR)
rng = np.random.default_rng(int(cfg.get("seed", 7)))


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output="sos"), x)


def place(buf, sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= buf.shape[1] or i < 0:
        return
    sig = sig[: buf.shape[1] - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[0, i:i + len(sig)] += sig * gain * l * 1.414
    buf[1, i:i + len(sig)] += sig * gain * r * 1.414


def in_drop(t):
    return any(a <= t < b for a, b in DROPS) or t >= END + 0.01


def kick():
    n = int(0.28 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(48 + 190 * np.exp(-t * 38)) / SR) * np.exp(-t * 14)
    return np.tanh(1.8 * (s + filt(rng.standard_normal(n), "high", 2500) * np.exp(-t * 400) * 0.35))


def bass808(note, length, glide_from=None):
    n = int(length * SR); t = np.arange(n) / SR
    f = np.full(n, mtof(note))
    if glide_from is not None:
        f = mtof(glide_from) + (mtof(note) - mtof(glide_from)) * np.minimum(t / 0.07, 1)
    f = f * (1 + 0.9 * np.exp(-t * 55))
    env = np.exp(-t * 1.1) * np.minimum(t / 0.004, 1) * np.clip((length - t) / 0.03, 0, 1)
    return np.tanh(2.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env) * 0.9


def clap():
    n = int(0.45 * SR); t = np.arange(n) / SR
    env = np.zeros(n)
    for d in (0, 0.011, 0.022):
        k = int(d * SR); env[k:] += np.exp(-t[: n - k] * 60)
    env += 0.5 * np.exp(-t * 9)
    return np.tanh(filt(rng.standard_normal(n), "band", [900, 6500]) * env * 0.8 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5)


def hat(open_=False):
    n = int((0.32 if open_ else 0.06) * SR); t = np.arange(n) / SR
    sq = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in (317, 457, 571, 683, 829, 997))
    return filt(sq / 6 + 0.6 * rng.standard_normal(n), "high", 7000, 4) * np.exp(-t * (9 if open_ else 75)) * 0.5


def bell(note, length=1.2):
    n = int(length * SR); t = np.arange(n) / SR; f = mtof(note)
    return np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * f * 3.5 * t) * 2.2 * np.exp(-t * 5)) * np.exp(-t * 3.2) * np.minimum(t / 0.002, 1)


def pad(notes, length):
    n = int(length * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for m in notes:
        for det in (-0.12, 0.0, 0.11):
            s += 2 * ((t * mtof(m + det) + rng.random()) % 1) - 1
    return filt(s / (3 * len(notes)), "low", 1400) * np.minimum(t / 0.25, 1) * np.clip((length - t) / 0.4, 0, 1)


def riser(length):
    n = int(length * SR); t = np.arange(n) / SR; x = rng.standard_normal(n); out = np.zeros(n)
    for i in range(0, n, 2048):
        c = 400 * (16 ** (i / n)); seg = x[i:i + 2048]
        out[i:i + len(seg)] = filt(seg, "band", [c * 0.7, min(c * 1.6, 18000)])
    return out * (t / length) ** 2.2 * 0.6


def impact():
    n = int(2.2 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (36 + 60 * np.exp(-t * 9)) * t) * np.exp(-t * 2.2)
    return np.tanh(1.5 * boom) + filt(rng.standard_normal(n), "high", 3500) * np.exp(-t * 2.6) * 0.35


def reverb(x, secs, wet):
    n = int(secs * SR); t = np.arange(n) / SR
    ir = np.stack([filt(i, "low", 6000) for i in rng.standard_normal((2, n)) * np.exp(-t * 6.0 / secs)])
    y = np.stack([fftconvolve(x[c], ir[c])[: x.shape[1]] for c in range(2)])
    return x + wet * y / (np.abs(y).max() + 1e-9) * np.abs(x).max()


drums, bass, music, fx = (np.zeros((2, N)) for _ in range(4))
K, CL, HC, HO = kick(), clap(), hat(), hat(True)
EV = {"kick": [], "clap": [], "roll": [], "bass": []}
nbars = int(np.ceil(DUR / BAR))
# two-bar bass riff from the scale (step, interval, length in 16ths)
R = SCALE + [0] * (5 - len(SCALE))
RIFF = [(0, R[0], 6), (6, R[1], 3), (10, R[2], 4), (16, R[0], 5), (22, R[3], 3), (26, R[4], 4), (30, R[1], 2)]
prev = None
for b in range(nbars):
    t0, intro, half = b * BAR, b == 0, (b % 2) * 16
    for s, iv, ln in RIFF:
        if not (half <= s < half + 16):
            continue
        t = t0 + (s - half) * STEP
        if in_drop(t) or t >= DUR:
            continue
        note = ROOT + iv
        place(bass, bass808(note, ln * STEP + 0.02, prev if s in (6, 30) else None), t, 0.85)
        prev = note; EV["bass"].append(round(t, 4))
    kicks = ([0, 6, 10] if b % 2 == 0 else [0, 6, 7, 11, 14]) if STYLE == "trap" else [0, 4, 8, 12]
    for s in kicks:
        t = t0 + s * STEP
        if not in_drop(t):
            place(drums, K, t, 0.55 if intro else 0.75); EV["kick"].append(round(t, 4))
    for s in ((12,) if intro else (4, 12)):
        t = t0 + s * STEP
        if not in_drop(t):
            place(drums, CL, t, 0.7); EV["clap"].append(round(t, 4))
    if intro:
        continue
    for s in range(0, 16, 2 if STYLE == "trap" else 1):
        t = t0 + s * STEP
        if in_drop(t):
            continue
        if STYLE == "trap" and b % 2 == 1 and s == 8:
            for k in range(4):
                place(drums, HC, t + k * STEP / 2, 0.22 + 0.05 * k, 0.25); EV["roll"].append(round(t + k * STEP / 2, 4))
            continue
        if STYLE == "trap" and b % 4 == 3 and s == 12:
            for k in range(6):
                place(drums, HC, t + k * STEP / 3, 0.18 + 0.04 * k, -0.2); EV["roll"].append(round(t + k * STEP / 3, 4))
            continue
        open_ = (STYLE == "four" and s % 4 == 2) or (STYLE == "trap" and s == 14 and b % 2 == 0)
        place(drums, HO if open_ else HC, t, 0.32 if s % 4 == 0 else 0.22, 0.2)

for b in range(nbars):
    chord = [ROOT + 24, ROOT + 31, ROOT + 37] if b % 2 == 0 else [ROOT + 23, ROOT + 30, ROOT + 36]
    place(music, pad(chord, BAR + 0.3), b * BAR, 0.20 if b > 1 else 0.13)
    for s, iv in [(0, 48), (3, 49), (6, 48), (8, 47), (11, 44), (14, 43)]:
        t = b * BAR + s * STEP
        if not in_drop(t) and t < END:
            place(music, bell(ROOT + iv + (12 if b >= nbars * 0.6 else 0)), t, 0.17, 0.35 if s % 2 else -0.35)

for a, bnd in DROPS:
    place(fx, riser(bnd - a + 0.9), a - 0.9, 0.22)
for t in HITS:
    place(fx, impact(), t, 0.55)
place(bass, bass808(ROOT, 0.9), END, 0.9)
place(fx, impact(), END, 0.4)
for a, bnd in DROPS:
    i, j = int(a * SR), int(bnd * SR)
    for buf in (drums, bass):
        buf[:, i:j] *= np.linspace(1, 0, j - i) ** 6
    music[:, i:j] *= 0.25

mix = 0.72 * np.stack([filt(c, "low", 900) for c in bass]) + reverb(drums, 0.9, 0.12) + 1.35 * reverb(music, 2.2, 0.45) + 0.8 * reverb(fx, 2.0, 0.3)
fade = int(0.6 * SR); mix[:, -fade:] *= np.linspace(1, 0, fade)
mix /= np.abs(mix).max() + 1e-9
mix = np.tanh(mix * 2.2) / np.tanh(2.2) * 0.80

# ---------- SFX on the picture's actions ----------
SFX = cfg.get("sfx", {})
sdir = cfg.get("sfx_dir", "assets/audio/sfx")


def load(fn):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(sdir, fn), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(float)
    return x / (np.abs(x).max() + 1e-9)


sfx = np.zeros((2, N))
whooshes = sorted(f for f in os.listdir(sdir) if f.startswith("whoosh")) if os.path.isdir(sdir) else []
for i, t in enumerate(SFX.get("whoosh", [])):
    if whooshes:
        x = load(whooshes[i % len(whooshes)])
        place(sfx, x, max(0, t - np.argmax(np.abs(x)) / SR), 0.38, 0.4 if i % 2 else -0.4)
if SFX.get("pop") and whooshes:
    sw = filt(load(whooshes[min(1, len(whooshes) - 1)]), "high", 1800)
    sw = sw[max(0, np.argmax(np.abs(sw)) - int(0.06 * SR)):][: int(0.22 * SR)]
    sw = sw * np.linspace(1, 0, len(sw)) ** 1.5
    for i, t in enumerate(SFX["pop"]):
        place(sfx, sw, max(0, t - 0.06), 0.16, 0.25 if i % 2 else -0.25)
for fn, t, g in SFX.get("ui", []):
    place(sfx, load(fn), t, g)
mix = np.tanh((mix + reverb(sfx, 0.6, 0.08)) * 1.15) / np.tanh(1.15) * 0.89

out = cfg.get("out", "assets/audio/score.wav")
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
wavfile.write(out, SR, (mix.T * 32767).astype(np.int16))
EV.update({"drops": DROPS, "hits": HITS, "end": END, "bpm": BPM})
with open(cfg.get("cues", "assets/cues.js"), "w") as f:
    f.write("// Generated by score.py: exact music event times (s).\nwindow.CUES = " + json.dumps(EV) + ";\n")
print(f"wrote {out} ({DUR:.1f} s, {BPM} BPM, {STYLE}) and {cfg.get('cues', 'assets/cues.js')}: "
      f"{len(EV['kick'])} kicks, {len(EV['clap'])} claps, {len(HITS)} hits")
