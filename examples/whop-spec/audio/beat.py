"""Original 90 BPM dark trap bed for the Whop spec ad.

Modelled on the measured groove of the Slash reference (tempo, 808 weight,
chromatic D/Eb/C/C# palette, hat rolls, two full drop-outs) without copying
its melody. Writes assets/audio/beat.wav (44.1 kHz stereo, 27 s).

Run: python audio/beat.py   (needs numpy + scipy)
"""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
import os

SR = 44100
BPM = 90.0
BEAT = 60.0 / BPM          # 0.6667 s
STEP = BEAT / 4            # 16th = 0.1667 s
BAR = BEAT * 4             # 2.6667 s
DUR = 27.0
N = int(DUR * SR)
rng = np.random.default_rng(7)

# Drop-outs: everything but the pad tail goes silent, then slams back.
DROPS = [(5.0, 5.3333), (16.8333, 17.3333)]
HITS = [5.3333, 17.3333, 23.3333, 24.6667]  # scene cuts that get an impact
END = 26.0                                  # last downbeat, then ring out


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def place(buf, sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= buf.shape[1]:
        return
    sig = sig[: buf.shape[1] - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[0, i : i + len(sig)] += sig * gain * l * 1.414
    buf[1, i : i + len(sig)] += sig * gain * r * 1.414


def in_drop(t):
    return any(a <= t < b for a, b in DROPS) or t >= END + 0.01


# ---------- instruments ----------
def kick():
    n = int(0.28 * SR); t = np.arange(n) / SR
    f = 48 + 190 * np.exp(-t * 38)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 14)
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t * 400) * 0.35
    return np.tanh(1.8 * (s + click))


def eight08(note, length, glide_from=None):
    n = int(length * SR); t = np.arange(n) / SR
    f = np.full(n, mtof(note))
    if glide_from is not None:
        g = np.minimum(t / 0.07, 1)
        f = mtof(glide_from) + (mtof(note) - mtof(glide_from)) * g
    f = f * (1 + 0.9 * np.exp(-t * 55))          # pitch punch
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.exp(-t * 1.1) * np.minimum(t / 0.004, 1)
    env *= np.minimum((length - t) / 0.03, 1).clip(0, 1)
    s = np.sin(ph) * env
    return np.tanh(2.6 * s) * 0.9                # saturation gives the growl


def clap():
    n = int(0.45 * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    env = np.zeros(n)
    for d in (0, 0.011, 0.022):                   # three-hand flam
        k = int(d * SR); env[k:] += np.exp(-(t[: n - k]) * 60)
    env += 0.5 * np.exp(-t * 9)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5
    return np.tanh(bp(noise, 900, 6500) * env * 0.8 + body)


def hat(open_=False):
    n = int((0.32 if open_ else 0.06) * SR); t = np.arange(n) / SR
    sq = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in (317, 457, 571, 683, 829, 997))
    s = hp(sq / 6 + 0.6 * rng.standard_normal(n), 7000, 4)
    return s * np.exp(-t * (9 if open_ else 75)) * 0.5


def bell(note, length=1.2):
    n = int(length * SR); t = np.arange(n) / SR
    f = mtof(note)
    mod = np.sin(2 * np.pi * f * 3.5 * t) * 2.2 * np.exp(-t * 5)
    s = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 3.2)
    return s * np.minimum(t / 0.002, 1)


def pad(notes, length):
    n = int(length * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notes:
        for det in (-0.12, 0.0, 0.11):
            f = mtof(m + det)
            s += 2 * ((t * f + rng.random()) % 1) - 1      # detuned saws
    s = lp(s / (3 * len(notes)), 1400, 2)
    env = np.minimum(t / 0.25, 1) * np.minimum((length - t) / 0.4, 1).clip(0, 1)
    return s * env


def riser(length):
    n = int(length * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n); seg = 2048
    for i in range(0, n, seg):                    # sweep a band upward
        c = 400 * (16 ** (i / n))
        out[i : i + seg] = bp(x[i : i + seg], c * 0.7, min(c * 1.6, 18000))[: len(out[i : i + seg])]
    return out * (t / length) ** 2.2 * 0.6


def impact():
    n = int(2.2 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (36 + 60 * np.exp(-t * 9)) * t) * np.exp(-t * 2.2)
    crash = hp(rng.standard_normal(n), 3500) * np.exp(-t * 2.6) * 0.35
    return np.tanh(1.5 * boom) + crash


def reverb(x, secs=1.6, wet=0.25):
    n = int(secs * SR); t = np.arange(n) / SR
    ir = rng.standard_normal((2, n)) * np.exp(-t * 6.0 / secs)
    ir = np.stack([lp(i, 6000) for i in ir])
    y = np.stack([fftconvolve(x[c], ir[c])[: x.shape[1]] for c in range(2)])
    y /= np.abs(y).max() + 1e-9
    return x + wet * y * np.abs(x).max()


# ---------- arrangement ----------
drums = np.zeros((2, N)); bass = np.zeros((2, N)); music = np.zeros((2, N)); fx = np.zeros((2, N))
K, CL, HC, HO = kick(), clap(), hat(), hat(True)

# 2-bar 808 riff (step, midi note, length in steps). D1 = 26.
RIFF = [(0, 26, 6), (6, 38, 3), (10, 39, 4), (16, 26, 5), (22, 36, 3), (26, 37, 4), (30, 38, 2)]
KICKS_A = [0, 6, 10]            # kick steps in bar A
KICKS_B = [0, 6, 7, 11, 14]     # bar B, busier
nbars = int(np.ceil(DUR / BAR))
EV = {"kick": [], "clap": [], "roll": [], "bass": []}
prev = None
for b in range(nbars):
    t0 = b * BAR
    intro = b == 0
    # 808 + kick
    for s, note, ln in RIFF:
        if (b % 2) * 16 > s or s >= (b % 2) * 16 + 16:
            continue
        t = t0 + (s - (b % 2) * 16) * STEP
        if in_drop(t) or t >= DUR:
            continue
        place(bass, eight08(note, ln * STEP + 0.02, glide_from=prev if s in (6, 30) else None), t, 0.85)
        prev = note
        EV["bass"].append(round(t, 4))
    for s in (KICKS_A if b % 2 == 0 else KICKS_B):
        t = t0 + s * STEP
        if not in_drop(t):
            place(drums, K, t, 0.75 if not intro else 0.55)
            EV["kick"].append(round(t, 4))
    # clap on 2 and 4 (bar 1: only the 4)
    for s in ((12,) if intro else (4, 12)):
        t = t0 + s * STEP
        if not in_drop(t):
            place(drums, CL, t, 0.7)
            EV["clap"].append(round(t, 4))
    # hats: 8ths from bar 2, with rolls on alternate bars
    if not intro:
        for s in range(0, 16, 2):
            t = t0 + s * STEP
            if in_drop(t):
                continue
            if b % 2 == 1 and s == 8:                     # 32nd roll then triplet roll
                for k in range(4):
                    place(drums, HC, t + k * STEP / 2, 0.22 + 0.05 * k, pan=0.25)
                    EV["roll"].append(round(t + k * STEP / 2, 4))
                continue
            if b % 4 == 3 and s == 12:
                for k in range(6):
                    place(drums, HC, t + k * (2 * STEP / 6), 0.18 + 0.04 * k, pan=-0.2)
                    EV["roll"].append(round(t + k * (2 * STEP / 6), 4))
                continue
            place(drums, HO if s == 14 and b % 2 == 0 else HC, t, 0.32 if s % 4 == 0 else 0.24, pan=0.2)
    else:
        place(drums, HC, t0 + 8 * STEP, 0.2); place(drums, HC, t0 + 14 * STEP, 0.2)

# Pad: dissonant D / Eb drone, opens up after the first drop.
for b in range(nbars):
    t0 = b * BAR
    chord = [50, 57, 63] if b % 2 == 0 else [49, 56, 62]   # D-A-Eb / C#-G#-D
    p = pad(chord, BAR + 0.3)
    place(music, p, t0, 0.20 if b > 1 else 0.13)

# Bell motif (original): D Eb D C# ... answered an octave up after the drop.
MOTIF = [(0, 74), (3, 75), (6, 74), (8, 73), (11, 70), (14, 69)]
for b in range(nbars):
    t0 = b * BAR
    up = 12 if b >= 6 else 0
    for s, m in MOTIF:
        t = t0 + s * STEP
        if in_drop(t) or t >= END:
            continue
        place(music, bell(m + up), t, 0.17, pan=0.35 if s % 2 else -0.35)

# Transitions: riser into each drop, impact on the hit.
for a, bnd in DROPS:
    r = riser(bnd - a + 0.9)
    place(fx, r, a - 0.9, 0.22)
for t in HITS:
    place(fx, impact(), t, 0.55)
# Final: one long 808 under the logo, ringing out.
place(bass, eight08(26, 0.9), END, 0.9)
place(fx, impact(), END, 0.4)

# Mute everything but the riser inside drop windows (tails included).
for a, bnd in DROPS:
    i, j = int(a * SR), int(bnd * SR)
    for buf in (drums, bass):
        buf[:, i:j] *= np.linspace(1, 0, j - i) ** 6
    music[:, i:j] *= 0.25

# ---------- mix ----------
music = reverb(music, 2.2, 0.45)
drums = reverb(drums, 0.9, 0.12)
fx = reverb(fx, 2.0, 0.3)
bass = np.stack([lp(c, 900) for c in bass])
mix = 0.72 * bass + 1.0 * drums + 1.35 * music + 0.8 * fx

# sidechain-style pump on music from kick+808
env = lp(np.abs(bass[0]) + np.abs(drums[0]), 12, 1)
env = env / (env.max() + 1e-9)
mix = mix  # pump kept subtle: music already sits low

fade = int(0.6 * SR)
mix[:, -fade:] *= np.linspace(1, 0, fade)
# glue + soft clip to reach a loud, flat master like the reference
mix /= np.abs(mix).max() + 1e-9
mix = np.tanh(mix * 2.2) / np.tanh(2.2)
mix *= 0.80

# ---------- SFX on the picture's own actions (times = visual events) ----------
import subprocess, json
def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"assets/audio/sfx/{name}.mp3", "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(float)
    return x / (np.abs(x).max() + 1e-9)
SMP = {n: load(n) for n in ["whoosh1", "whoosh2", "whoosh3", "whoosh4", "tick1", "tick2", "ui-snap", "ui-press",
                            "ui-receive", "ui-notification", "ui-purchase", "ui-success", "ui-open"]}
sfx = np.zeros((2, N))
def hit(name, t, g, pan=0.0, peak_on=False):
    x = SMP[name]
    if peak_on:                                   # land the loudest moment on t (whooshes)
        t -= np.argmax(np.abs(x)) / SR
    if t < 0:
        x = x[int(-t * SR):]; t = 0
    place(sfx, x, t, g, pan)
CUE = json.load(open("audio/visual_cues.json"))
for i, t in enumerate(CUE["whoosh"]):
    hit(["whoosh1", "whoosh2", "whoosh3", "whoosh4"][i % 4], t, 0.38, pan=0.4 if i % 2 else -0.4, peak_on=True)
# Text appearing: no per-letter clicks. One soft, short air swish as each caption pops in.
SW = hp(SMP["whoosh2"], 1800)
SW = SW[max(0, np.argmax(np.abs(SW)) - int(0.06 * SR)):][: int(0.22 * SR)]
SW = SW * np.linspace(1, 0, len(SW)) ** 1.5
for i, t in enumerate(CUE["pop"]):
    place(sfx, SW, max(0, t - 0.06), 0.16, 0.25 if i % 2 else -0.25)
for t in CUE["bubble"]:
    hit("ui-receive", t, 0.4)
for name, t, g in CUE["ui"]:
    hit(name, t, g)
sfx = reverb(sfx, 0.6, 0.08)
mix = mix + sfx
mix = np.tanh(mix * 1.15) / np.tanh(1.15) * 0.89
EV["drops"] = DROPS; EV["hits"] = HITS; EV["end"] = END
with open("assets/cues.js", "w") as f:
    f.write("// Generated by audio/beat.py: exact music event times (s).\nwindow.CUES = " + json.dumps(EV) + ";\n")

os.makedirs("assets/audio", exist_ok=True)
wavfile.write("assets/audio/beat.wav", SR, (mix.T * 32767).astype(np.int16))
print("wrote assets/audio/beat.wav", mix.shape[1] / SR, "s")
