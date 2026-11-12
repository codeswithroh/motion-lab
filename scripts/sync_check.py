#!/usr/bin/env python3
"""Measure picture-vs-sound sync on a rendered MP4.

usage: python3 sync_check.py <mp4> <hit_s> <hero_frame> <row_y> [fps]

  hit_s       where you expect the track's hit in film time (searches +-0.25 s around it)
  hero_frame  the frame you expect the two shapes to touch
  row_y       a pixel row through both shapes (e.g. the logo circles' vertical centre)

Prints the first 10 ms window that jumps >= 12 dB over the previous 100 ms (the hit), and, for
frames hero_frame-6 .. hero_frame+4, the count of ground-coloured pixels between the leftmost and
rightmost saturated pixels on row_y (0 = the shapes touch). Pass: the gap reaches 0 at most one
frame before the hit, never after.
"""
import math
import struct
import subprocess
import sys

mp4, hit_s, hero, row_y = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
fps = float(sys.argv[5]) if len(sys.argv) > 5 else 60.0

# ── audio: find the hit ──────────────────────────────────────
SR = 48000
t0 = max(0.0, hit_s - 0.35)
raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", "0.6", "-i", mp4, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
    capture_output=True, check=True,
).stdout
x = struct.unpack(f"{len(raw) // 4}f", raw)
W = SR // 100  # 10 ms
db = []
for i in range(0, len(x) - W, W):
    r = math.sqrt(sum(v * v for v in x[i:i + W]) / W)
    db.append(20 * math.log10(r + 1e-9))
hit = None
for k in range(10, len(db)):
    if db[k] - max(db[k - 10:k]) >= 12 or (db[k] - sum(db[k - 10:k]) / 10 >= 15):
        hit = t0 + k * 0.01
        break
if hit is None:
    k = max(range(10, len(db)), key=lambda k: db[k] - sum(db[k - 10:k]) / 10)
    hit = t0 + k * 0.01
    print("no clean 12 dB jump; biggest rise used")
# refine to 1 ms
lo = int((hit - t0 - 0.01) * SR)
for i in range(max(0, lo), min(len(x) - 48, lo + int(0.03 * SR)), 48):
    r = math.sqrt(sum(v * v for v in x[i:i + 48]) / 48)
    if 20 * math.log10(r + 1e-9) > db[int((hit - t0) / 0.01)] - 3:
        hit = t0 + i / SR
        break
print(f"audio hit  {hit:.4f} s = frame {hit * fps:.2f}")

# ── picture: gap between the shapes ──────────────────────────
WIDTH = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                            "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout.strip())
a, b = hero - 6, hero + 4
pix = subprocess.run(
    ["ffmpeg", "-v", "error", "-i", mp4, "-vf", f"select='between(n\\,{a}\\,{b})',crop=w={WIDTH}:h=2:x=0:y={row_y}",
     "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
    capture_output=True, check=True,
).stdout
F = WIDTH * 3 * 2
touch = None
for k in range(len(pix) // F):
    row = pix[k * F:k * F + WIDTH * 3]
    px = [row[i * 3:i * 3 + 3] for i in range(WIDTH)]
    sat = [i for i in range(WIDTH) if max(px[i]) - min(px[i]) > 60]  # coloured, not paper or ink
    gap = sum(1 for i in range(sat[0], sat[-1]) if max(px[i]) - min(px[i]) < 30 and min(px[i]) > 190) if sat else -1
    print(f"frame {a + k}  gap {gap} px")
    if gap == 0 and touch is None:
        touch = a + k
if touch is not None:
    d = hit * fps - touch
    ok = 0 <= d <= 1.0
    print(f"shapes touch on frame {touch}; sound is {d:+.2f} frames after the picture -> {'PASS' if ok else 'FIX: move the hero tween'}")
