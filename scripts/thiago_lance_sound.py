"""Score and SFX for "A hora do lance" (ThiagoLance), synthesised from its timeline.

usage: python3 thiago_lance_sound.py timeline.json out_dir
Writes music.wav, sfx/*.wav and events.json for the motionmaxxing mix.py.
"""
import json
import os
import sys
import wave

import numpy as np

SR = 48000
FPS = 30
tl = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(f"{out}/sfx", exist_ok=True)
rng = np.random.default_rng(5)
DUR = tl["DURATION"] / FPS
N = int(DUR * SR)


def sec(frame):
    return frame / FPS


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


def add(buf, start_s, x, gain=1.0):
    i = int(start_s * SR)
    if 0 <= i < len(buf):
        x = x[: len(buf) - i]
        buf[i : i + len(x)] += gain * x


def pad(freqs, length, a=1.5, r=1.5):
    n = int(length * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for d in (-0.004, 0, 0.004):
            ph = rng.random() * 6.28
            for k in range(1, 7):
                x += np.sin(2 * np.pi * f * (1 + d) * k * t + ph * k) / k**1.4
    return band(x, 30, 900) * env(n, a, r) / (len(freqs) * 6)


def sub_hit(f0=50, length=0.5):
    n = int(length * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * (1 + 1.5 * np.exp(-t / 0.03))) / SR) * np.exp(-t / 0.16)


def pluck(freq, length=1.6):
    n = int(length * SR)
    t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * freq * k * t) * np.exp(-t * (2 + 1.5 * k)) / k for k in range(1, 6)) * env(n, 0.004, 0.3)


silence = tl["SILENCE"]
slam = tl["SLAM"]
card = tl["CARD"]

# --- music: D minor drone and a soft pulse, cut for the silence, D major after the stamp.
music = np.zeros(N)
add(music, 0, pad([73.42, 110.0, 174.61], sec(silence[0]) + 0.02, a=1.0, r=0.02), 0.9)
for f in range(120, silence[0] - 6, 18):
    add(music, sec(f), sub_hit(), 0.45 if f < 240 else 0.6)
music[int(sec(silence[0]) * SR) :] = 0
add(music, sec(slam + 24), pad([73.42, 146.83, 185.0, 220.0, 329.63], DUR - sec(slam + 24), a=2.0, r=1.5), 1.0)
for f in range(card[0], 726, 36):
    add(music, sec(f), sub_hit(44, 0.6), 0.3)
for f, hz in [(card[0] + 14, 440.0), (card[0] + 60, 554.37), (tl["CHECK"][0], 659.26)]:
    add(music, sec(f), pluck(hz), 0.35)
write(f"{out}/music.wav", music)


# --- sfx
def tick(freq, length=0.09):
    n = int(length * SR)
    t = np.arange(n) / SR
    return band(rng.normal(0, 1, n), 1500, 6000) * np.exp(-t / 0.006) + np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.018) * 0.6


def roll(length):
    n = int(length * SR)
    t = np.arange(n) / SR
    speed = 1 - t / t[-1]
    rate = 6 + 22 * speed  # bumps per second as it slows
    bumps = 0.65 + 0.35 * np.sin(2 * np.pi * np.cumsum(rate) / SR)
    return band(rng.normal(0, 1, n), 120, 1400) * bumps * (0.25 + 0.75 * speed) * env(n, 0.05, 0.05)


def scratch(length):
    n = int(length * SR)
    t = np.arange(n) / SR
    strokes = np.clip(np.sin(2 * np.pi * 7.5 * t + 2 * np.sin(2 * np.pi * 1.3 * t)), 0, 1) ** 1.5
    return band(rng.normal(0, 1, n), 1800, 6500) * strokes * env(n, 0.03, 0.05)


def thud(length=2.4):
    n = int(length * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(42 * (1 + 2.2 * np.exp(-t / 0.04))) / SR) * np.exp(-t / 0.55)
    x += band(rng.normal(0, 1, n), 150, 2500) * np.exp(-t / 0.03) * 0.9  # paper and wood slap
    x += np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.5  # wooden knock
    return x


def swish(length, lo=400, hi=5000):
    n = int(length * SR)
    t = np.arange(n) / SR
    return band(rng.normal(0, 1, n), lo, hi) * np.sin(np.pi * t / t[-1]) ** 2


events = []


def ev(name, x, t, gain):
    write(f"{out}/sfx/{name}.wav", x)
    events.append({"t": round(t, 3), "sfx": f"sfx/{name}.wav", "gain": gain})


write(f"{out}/sfx/tick.wav", tick(1900))
write(f"{out}/sfx/tock.wav", tick(1400))
for i, f in enumerate(range(8, tl["DURATION"] - 20, 30)):
    loud = silence[0] <= f < slam
    events.append({"t": round(sec(f), 3), "sfx": f"sfx/{'tick' if i % 2 == 0 else 'tock'}.wav", "gain": -14 if loud else -24})

ball = tl["BALL"]
ev("roll", roll(sec(ball[1] - ball[0])), sec(ball[0]), -12)
ev("ballstop", tick(900, 0.12), sec(ball[1]), -14)
feint = tl["FEINT"]
ev("feint_down", swish(0.5, 200, 2500), sec(feint[0]), -18)
ev("feint_up", swish(0.6, 200, 2500), sec(feint[0] + 30), -20)
for i, span in enumerate([tl["WRITE_1"], tl["WRITE_2"]]):
    ev(f"pen{i}", scratch(sec(span[1] - span[0]) + 0.05), sec(span[0]), -20)
ev("stamp_in", swish(0.8, 150, 2000), sec(tl["STAMP_IN"][0]), -18)
ev("thud", thud(), sec(slam), -2)
ev("lift", swish(0.7, 200, 3000), sec(tl["LIFT"][0]), -22)
ev("card", swish(sec(card[1] - card[0]), 600, 7000), sec(card[0]), -20)

json.dump(sorted(events, key=lambda e: e["t"]), open(f"{out}/events.json", "w"), indent=1)
print(len(events), "events")
