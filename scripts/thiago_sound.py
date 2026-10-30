"""Score and SFX for the ThiagoCall film, synthesised from the film's own timeline.

usage: python3 thiago_sound.py timeline.json out_dir
Writes music.wav (25 s, 100 BPM, silence before the "?"), sfx/*.wav and events.json for mix.py.
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
rng = np.random.default_rng(3)
DUR = tl["DURATION"] / FPS
N = int(DUR * SR)


def sec(frame):
    return frame / FPS


def write(path, x):
    x = np.asarray(x, np.float32)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    peak = np.abs(x).max() or 1
    x = x / peak * 0.89
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def lowpass(x, hz):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / hz) ** 4)
    return np.fft.irfft(X, len(x))


def highpass(x, hz):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (hz / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def env(n, a, r):
    """Attack/release envelope in seconds over n samples."""
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.minimum(1, (n / SR - t) / max(r, 1e-4))
    return np.clip(e, 0, 1)


def add(buf, start_s, x, gain=1.0):
    i = int(start_s * SR)
    if i >= len(buf):
        return
    x = x[: len(buf) - i]
    buf[i : i + len(x)] += gain * x


def pad(freqs, length, a=1.5, r=1.5, detune=0.004):
    n = int(length * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for d in (-detune, 0, detune):
            ph = rng.random() * 2 * np.pi
            # soft saw from a few harmonics
            for k in range(1, 7):
                x += np.sin(2 * np.pi * f * (1 + d) * k * t + ph * k) / k**1.4
    x = lowpass(x, 900)
    return x * env(n, a, r) / (len(freqs) * 6)


def sub_hit(f0=52, length=0.5):
    n = int(length * SR)
    t = np.arange(n) / SR
    f = f0 * (1 + 1.6 * np.exp(-t / 0.03))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.16)


def hat(length=0.06):
    n = int(length * SR)
    x = highpass(rng.normal(0, 1, n), 7000)
    return x * np.exp(-np.arange(n) / SR / 0.012)


grid = 18  # frames per beat at 100 BPM
music = np.zeros(N)

# Act 1-2: low A minor drone, entering with the film.
add(music, 0, pad([55.0, 82.41, 110.0], sec(400) + 0.02, a=1.2, r=0.02), 0.9)
# Tension voice in act 2: a minor second above that creeps in.
add(music, sec(170), pad([116.54, 174.6], sec(400 - 170) + 0.02, a=2.5, r=0.02), 0.35)

# Sub pulse on the item grid (items print on 168 + 18k).
for f in range(114, 280, grid):
    add(music, sec(f), sub_hit(), 0.55)
# Stream: the pulse doubles and hats run on sixteenths, getting denser.
f = 280.0
while f < 398:
    add(music, sec(f), sub_hit(length=0.3), 0.5)
    f += grid / 2
f = 280.0
step = grid / 4
while f < 399:
    add(music, sec(f), hat(), 0.18 + 0.25 * (f - 280) / 118)
    f += step
    step = max(1.6, step * 0.985)
# Riser: filtered noise sweeping up into the stop.
n = int(sec(398 - 270) * SR)
t = np.arange(n) / SR
sweep = rng.normal(0, 1, n)
riser = np.zeros(n)
for lo, hi, g in [(300, 1200, 1.0), (1200, 5000, 0.6)]:
    riser += highpass(lowpass(sweep, hi), lo) * g
riser *= (t / t[-1]) ** 2.2
tone = np.sin(2 * np.pi * np.cumsum(110 * 2 ** (2 * t / t[-1])) / SR) * (t / t[-1]) ** 2
add(music, sec(270), riser * 0.5 + tone * 0.25)

# Hard stop at 400: everything above is cut there by construction (pads end at 400).
music[int(sec(400) * SR) :] = 0

# After the "?": a low held drone, then the resolve at the tear.
add(music, sec(QUESTION := tl["QUESTION"]), pad([55.0, 41.2], sec(tl["TEAR"] - QUESTION) + 0.3, a=0.05, r=0.3), 0.7)
# Resolve: A major add9, warm, from just after the tear to the end.
add(music, sec(tl["TEAR"] + 18), pad([110.0, 164.8, 220.0, 277.2, 329.6, 493.9], DUR - sec(tl["TEAR"] + 18), a=1.8, r=1.5), 1.0)
# Half-time pulse under the CTA.
for f in range(570, 726, grid * 2):
    add(music, sec(f), sub_hit(46, 0.6), 0.35)
# Soft plucks on the CTA lines.
def pluck(freq, length=1.6):
    n = int(length * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * freq * k * t) * np.exp(-t * (2 + k * 1.5)) / k for k in range(1, 6))
    return x * env(n, 0.004, 0.3)

for f, hz in [(576, 440.0), (644, 554.4), (680, 659.3)]:
    add(music, sec(f), pluck(hz), 0.35)

write(f"{out}/music.wav", music)


# --- SFX
def printer(length, rate=55):
    """Soft thermal-printer purr: muffled paper-feed noise with a gentle stepper flutter, no tonal whine."""
    n = int(length * SR)
    t = np.arange(n) / SR
    flutter = 0.75 + 0.25 * np.sin(2 * np.pi * rate * t)
    body = highpass(lowpass(rng.normal(0, 1, n), 1800), 250) * flutter
    motor = np.sin(2 * np.pi * 95 * t) * 0.25
    return (body + motor) * env(n, 0.04, 0.08)


def tear(length=0.55):
    n = int(length * SR)
    t = np.arange(n) / SR
    crackle = rng.normal(0, 1, n) * (rng.random(n) < 0.12)
    body = highpass(lowpass(rng.normal(0, 1, n), 6000), 900)
    x = (crackle * 1.4 + body * 0.6) * (1 - np.exp(-t / 0.01)) * np.exp(-t / 0.22)
    return x


def boom(length=2.5):
    n = int(length * SR)
    t = np.arange(n) / SR
    f = 38 * (1 + 2 * np.exp(-t / 0.05))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.7)
    x += lowpass(rng.normal(0, 1, n), 400) * np.exp(-t / 0.08) * 0.6
    return x


def key(length=0.12):
    n = int(length * SR)
    t = np.arange(n) / SR
    return highpass(rng.normal(0, 1, n), 1500) * np.exp(-t / 0.008) + np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.02) * 0.5


events = []
lengths = {}
for seg in ("A", "B"):
    for line in tl[seg]:
        if line["kind"] == "blank" or line["kind"] == "stream":
            continue
        d = round(line["dur"] / FPS + 0.08, 3)
        name = f"printer_{int(d * 1000)}.wav"
        if name not in lengths:
            write(f"{out}/sfx/{name}", printer(d))
            lengths[name] = d
        events.append({"t": round(sec(line["at"]), 3), "sfx": f"sfx/{name}", "gain": -24 if line["kind"] == "item" else -21})

# The stream: one continuous chatter that speeds up.
n = int(sec(398 - 280) * SR)
t = np.arange(n) / SR
# The stream: the same soft purr, brightening a little as the tape speeds up.
ramp = (t / t[-1]) ** 1.5
noise = rng.normal(0, 1, n)
chat = highpass(lowpass(noise, 1600), 250) * (1 - ramp) + highpass(lowpass(noise, 3200), 300) * ramp * 0.8
chat *= 0.8 + 0.2 * np.sin(2 * np.pi * np.cumsum(55 + 60 * ramp) / SR)
write(f"{out}/sfx/stream.wav", chat * env(n, 0.3, 0.004))
events.append({"t": sec(280), "sfx": "sfx/stream.wav", "gain": -19})

write(f"{out}/sfx/key.wav", key())
write(f"{out}/sfx/tear.wav", tear())
write(f"{out}/sfx/boom.wav", boom())
events += [
    {"t": sec(397), "sfx": "sfx/key.wav", "gain": -8},
    {"t": sec(QUESTION), "sfx": "sfx/boom.wav", "gain": -3},
    {"t": sec(tl["TEAR"] - 2), "sfx": "sfx/tear.wav", "gain": -6},
]
json.dump(sorted(events, key=lambda e: e["t"]), open(f"{out}/events.json", "w"), indent=1)
print(len(events), "events")
