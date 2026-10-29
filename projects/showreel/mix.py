"""Soundtrack for the reel: beat-aligned music + SFX placed on the on-screen events, muxed onto the render."""
import subprocess

import numpy as np
import soundfile as sf

SR, T = 48000, 15.0
n = int(SR * T)
BAR = 1.875
BEAT = BAR / 4
S = [i * BAR for i in range(8)]


def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", name, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def sfx(name):
    return load(f"assets/sfx/{name}.wav")


def peak_at(x):
    """Seconds into the clip where it is loudest, so hits land exactly on the cut."""
    env = np.abs(x).mean(1)
    return int(np.argmax(np.convolve(env, np.ones(480) / 480, mode="same"))) / SR


mix = np.zeros((n, 2), np.float32)


def place(x, t, gain, align_peak=False):
    t0 = t - (peak_at(x) if align_peak else 0.0)
    i = int(round(t0 * SR))
    a = max(0, -i)
    i = max(0, i)
    m = min(len(x) - a, n - i)
    if m > 0:
        mix[i:i + m] += x[a:a + m] * gain


place(load("build/music.wav"), 0.0, 0.62)

# 01 boot: keys while the command types, a glitch into the hit
for k in range(9):
    place(sfx("key-press"), 0.1 + k * 0.08, 0.35)
place(sfx("glitch-2")[: int(0.32 * SR)], 1.55, 0.35)
# every section change: whoosh peaking on the cut + a low impact
for t in S[1:]:
    place(sfx("whoosh"), t, 0.45, align_peak=True)
    place(sfx("impact-bass-1"), t, 0.5)
# 02 second word flip
place(sfx("whoosh-short"), S[1] + 2 * BEAT, 0.4, align_peak=True)
# 03 iris swells into the morph
place(sfx("whoosh-cinematic"), S[3] - 0.05, 0.4, align_peak=True)
# 04 one pop per morph
for k in (1, 2, 3):
    place(sfx("pop"), S[3] + k * BEAT, 0.45)
# 05 line drawing shimmer + fill flashes
place(sfx("sparkle"), S[4] + 0.15, 0.3)
for k in range(2):
    place(sfx("click"), S[4] + 3 * BEAT + k * 0.16, 0.35)
# 06 cube quarter turns
for k in (1, 2, 3):
    place(sfx("whoosh-short"), S[5] + k * BEAT, 0.35, align_peak=True)
# 07 bars tick up, then riser into the zoom-through
for k in range(14):
    place(sfx("click"), S[6] + 0.03 * k + 0.05, 0.12)
riser = sfx("riser")
place(riser[int((peak_at(riser) - 1.3) * SR): int(peak_at(riser) * SR)], S[7] - 1.3, 0.4)
place(sfx("impact-bass-2"), S[7], 0.55)
# 08 signature shimmer
place(sfx("sparkle"), S[7] + 0.4, 0.35)

fade = np.clip((T - np.arange(n) / SR) / 0.6, 0, 1)[:, None]
sf.write("build/soundtrack.wav", mix * fade, SR, subtype="FLOAT")
