#!/usr/bin/env python3
"""Find the biggest drops in a music track and where to start it so a drop lands on a film moment.

usage: find_drop.py <track> [--hero SECONDS] [--top N]

Prints a loudness map (0.5 s steps), the top N drops (jump from the 0.3 s before to the 0.3 s
after, plus how loud it lands, with a 10 ms onset), and, with --hero, the data-media-start that puts each drop's
onset on the hero time, snapped to a beat when `npx hyperframes beats` is available.
"""
import argparse
import json
import subprocess

import numpy as np

SR = 8000


def decode(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(float) / 32768


def rms_db(x, win):
    n = len(x) // win
    frames = x[: n * win].reshape(n, win)
    return 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)


def beats(path):
    try:
        out = subprocess.run(["npx", "hyperframes", "beats", path, "--json"], capture_output=True, text=True, timeout=300)
        return json.loads(out.stdout).get("beatTimes", [])
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("track")
    ap.add_argument("--hero", type=float, help="film time (s) the drop should land on")
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()

    x = decode(a.track)
    half = rms_db(x, SR // 2)
    print(f"duration {len(x) / SR:.1f} s\n\nloudness map (dBFS, 0.5 s steps)")
    for i in range(0, len(half), 8):
        print(f"{i / 2:6.1f}s " + " ".join(f"{v:6.1f}" for v in half[i : i + 8]))

    # a drop: a jump from the 0.3 s before to the 0.3 s after, counted more when it lands loud
    fine = rms_db(x, SR // 100)  # 10 ms
    median = np.median(fine[fine > -60])
    lo = int(a.hero * 100) + 30 if a.hero is not None else 30  # media-start must be >= 0
    cands = []
    for i in range(max(lo, 30), len(fine) - 30):
        before = fine[i - 30 : i].mean()
        after = fine[i : i + 30].mean()
        cands.append(((after - before) + 0.5 * (after - median), i))
    cands.sort(reverse=True)
    picked = []
    for jump, i in cands:
        if all(abs(i - j) > 400 for _, j in picked):  # 4 s apart
            picked.append((jump, i))
        if len(picked) == a.top:
            break

    bt = beats(a.track) if a.hero is not None else []
    print("\ndrops, best first (onset = first 10 ms window 6 dB over the 0.3 s before)")
    for jump, i in picked:
        base = fine[i - 30 : i].mean()
        onset = i
        for k in range(i - 20, min(i + 30, len(fine))):
            if fine[k] > base + 6:
                onset = k
                break
        t = onset / 100
        line = f"  {t:7.2f} s  score {jump:5.1f}"
        if a.hero is not None:
            start = t - a.hero
            line += f"   media-start {start:.3f}"
            if bt:
                nb = min(bt, key=lambda b: abs(b - start))
                line += f"  (nearest beat {nb:.3f}, drop then lands at {t - nb:.3f} s)"
        print(line)


if __name__ == "__main__":
    main()
