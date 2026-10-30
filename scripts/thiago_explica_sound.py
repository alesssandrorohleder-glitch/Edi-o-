"""Score and SFX for the 40 s explainer (ThiagoExplica). Frame numbers mirror the events in
remotion-video/src/ThiagoExplica/ThiagoExplica.tsx.

usage: python3 thiago_explica_sound.py out_dir
Writes music.wav (105 BPM, light and modern), sfx/*.wav and events.json for mix.py.
"""
import json
import os
import sys
import wave

import numpy as np

SR = 48000
FPS = 30
DUR = 40.0
N = int(DUR * SR)
out = sys.argv[1]
os.makedirs(f"{out}/sfx", exist_ok=True)
rng = np.random.default_rng(9)

DROP_LAND = 42
SPREAD = 128
POOL_IN = 176
COIN_AT = 300
SWEEP1 = (462, 510)
CARD = 540
SWEEP2 = (640, 676)
LANCE = (684, 708)
STRIKE = 796
REST_GREEN = [round(880 + 50 * (k / 8) ** 0.5) for k in range(9)]
CTA = 1012
HANDLE = 1160


def sec(f):
    return f / FPS


def write(path, x):
    x = np.asarray(x, np.float32)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    x = x / (np.abs(x).max() or 1) * 0.89
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / hi) ** 4) / np.sqrt(1 + (lo / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def env(n, a, r):
    t = np.arange(n) / SR
    return np.clip(np.minimum(1, t / max(a, 1e-4)) * np.minimum(1, (n / SR - t) / max(r, 1e-4)), 0, 1)


def add(buf, s, x, g=1.0):
    i = int(s * SR)
    if 0 <= i < len(buf):
        x = x[: len(buf) - i]
        buf[i : i + len(x)] += g * x


def tone(freq, length, decay, harm=(1, 0.5, 0.25)):
    n = int(length * SR)
    t = np.arange(n) / SR
    return sum(a * np.sin(2 * np.pi * freq * (k + 1) * t) for k, a in enumerate(harm)) * np.exp(-t / decay) * env(n, 0.003, 0.05)


def rhodes(freqs, length):
    n = int(length * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.3)) for f in freqs)
    return x * np.exp(-t / 1.2) * (1 + 0.15 * np.sin(2 * np.pi * 5 * t)) * env(n, 0.005, 0.2) / len(freqs)


def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(55 * (1 + 2.5 * np.exp(-t / 0.025))) / SR) * np.exp(-t / 0.12)


def snap():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return band(rng.normal(0, 1, n), 1500, 7000) * np.exp(-t / 0.025)


def hat():
    n = int(0.05 * SR)
    return band(rng.normal(0, 1, n), 7000, 14000) * np.exp(-np.arange(n) / SR / 0.01)


# --- music: 105 BPM, Fmaj7 - Am7 - Dm9 - Bbmaj7, drums enter with the ring.
beat = 60 / 105
music = np.zeros(N)
chords = [[174.6, 220.0, 261.6, 329.6], [220.0, 261.6, 329.6, 392.0], [146.8, 220.0, 261.6, 329.6], [116.5, 174.6, 233.1, 293.7]]
bar = 0
t0 = 0.4
while t0 < DUR:
    c = chords[bar % 4]
    add(music, t0, rhodes(c, beat * 4), 0.55)
    add(music, t0, tone(c[0] / 2, beat * 4, 1.2, (1, 0.3)), 0.35)
    for b in range(4):
        tb = t0 + b * beat
        if tb > sec(SPREAD) and not (sec(CTA) + 2 < tb):
            if b in (0, 2):
                add(music, tb, kick(), 0.5)
            if b in (1, 3):
                add(music, tb, snap(), 0.22)
            add(music, tb + beat / 2, hat(), 0.12)
    t0 += beat * 4
    bar += 1
write(f"{out}/music.wav", music)

# --- sfx
events = []


def ev(name, x, t, gain):
    p = f"{out}/sfx/{name}.wav"
    if not os.path.exists(p):
        write(p, x)
    events.append({"t": round(t, 3), "sfx": f"sfx/{name}.wav", "gain": gain})


def pop(f0=520):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * (1 + 1.2 * np.exp(-t / 0.01))) / SR) * np.exp(-t / 0.03)


def coin():
    return tone(2400, 0.35, 0.08, (1, 0.0, 0.0)) + tone(3700, 0.35, 0.05, (0.6,))


def plim(f=1318.5):
    return tone(f, 1.2, 0.35, (1, 0.35, 0.12))


def swish(length, lo=300, hi=6000):
    n = int(length * SR)
    t = np.arange(n) / SR
    return band(rng.normal(0, 1, n), lo, hi) * np.sin(np.pi * t / t[-1]) ** 2


def thump():
    n = int(0.4 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(90 * (1 + 1.5 * np.exp(-t / 0.02))) / SR) * np.exp(-t / 0.08)


ev("thump", thump(), sec(DROP_LAND), -10)
for i in range(12):
    ev("pop", pop(), sec(SPREAD + 2 * i + 6), -22)
ev("pool", swish(0.7, 200, 3000), sec(POOL_IN), -24)
for i in range(12):
    ev("coin", coin(), sec(COIN_AT + 5 * i + 16), -22)
for s in (SWEEP1, SWEEP2):
    ev(f"sweep{s[0]}", swish(sec(s[1] - s[0]), 400, 5000), sec(s[0]), -24)
ev("plim", plim(), sec(SWEEP1[1]), -14)
ev("card", swish(0.9, 600, 7000), sec(CARD), -22)
ev("plim", plim(), sec(SWEEP2[1]), -14)
for j in range(3):
    ev("coin", coin(), sec(LANCE[1] - 6 + 2 * j), -20)
ev("plim", plim(), sec(LANCE[1]), -14)
ev("strike", swish(0.25, 1500, 7000), sec(STRIKE), -20)
scale = [1046.5, 1174.7, 1318.5, 1396.9, 1568.0, 1760.0, 1975.5, 2093.0, 2349.3]
for k, f in enumerate(REST_GREEN):
    ev(f"plim{k}", plim(scale[k]), sec(f), -18)
ev("reveal", swish(1.2, 200, 4000), sec(CTA + 8), -20)
ev("final", plim(1760.0) + plim(2217.5) * 0.6, sec(HANDLE), -16)

json.dump(sorted(events, key=lambda e: e["t"]), open(f"{out}/events.json", "w"), indent=1)
print(len(events), "events")
