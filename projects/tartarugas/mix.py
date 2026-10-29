"""Mixes the soundtrack and muxes it onto the rendered picture.

music (MusicGen take, looped to 45 s, ducked under the voice) + ocean bed + soft SFX + narration.
"""
import subprocess

import numpy as np
import soundfile as sf

SR, T = 48000, 45.0
n = int(SR * T)


def load(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()


def place(dst, x, t, gain=1.0):
    i = int(t * SR)
    m = min(len(x), n - i)
    dst[i:i + m] += x[:m] * gain


# music: extend the 30 s take to 45 s by crossfading a second pass that re-enters at 8 s
m = load("build/music_take1_eq.wav")
xf = int(3 * SR)
seg2 = m[int(8 * SR):]
fade = np.linspace(0, 1, xf)[:, None]
music = np.concatenate([m[:-xf], m[-xf:] * (1 - fade) + seg2[:xf] * fade, seg2[xf:]])[:n]
music = np.pad(music, ((0, max(0, n - len(music))), (0, 0)))
t = np.arange(n) / SR
music *= (np.clip(t / 2.5, 0, 1) * np.clip((T - t) / 3.0, 0, 1))[:, None]

narr = load("assets/narration.wav")
# duck the music ~7 dB while the narrator speaks (smoothed envelope)
env = np.convolve(np.abs(narr[:, 0]), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
speak = np.clip(env / (env.max() * 0.08), 0, 1)
speak = np.convolve(speak, np.ones(int(0.35 * SR)) / int(0.35 * SR), mode="same")
music *= (1 - 0.55 * speak)[:, None]

mix = np.zeros((n, 2), np.float32)
mix += music * 0.55
mix += load("assets/ocean.wav")[:n] * 0.9
for tt in (6.6, 12.6, 31.3):
    place(mix, load("assets/sfx/whoosh-soft.wav"), tt, 0.35)
place(mix, load("assets/sfx/boom.wav"), 40.0, 0.5)
mix += narr
sf.write("build/soundtrack.wav", mix, SR, subtype="FLOAT")
