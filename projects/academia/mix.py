"""Places the narration lines and ducks the original audio around them.

Original speech in the kept clips stays fully audible; narration never overlaps it.
"""
import subprocess, numpy as np, soundfile as sf

SR = 48000
NARR = [("n3", 6.35), ("n4", 14.6), ("n5", 22.85), ("n6", 31.45), ("n7", 39.5)]
SPEECH = [(0.5, 6.0), (24.55, 27.6)]   # real speech found by Whisper in build/speech.json

def load(path, ch):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, ch).copy()

base = load("build/base_orig_audio.wav", 2)
n = len(base); t = np.arange(n) / SR
narr = np.zeros(n, dtype=np.float32)
windows = []
for name, start in NARR:
    x = load(f"assets/narr/{name}.wav", 1)[:, 0]
    i = int(start * SR); narr[i:i + len(x)] += x[: n - i]
    windows.append((start, start + len(x) / SR))
for a, b in windows:
    for s0, s1 in SPEECH:
        assert b <= s0 or a >= s1, f"narration {a:.2f}-{b:.2f} overlaps speech {s0}-{s1}"

def env(spans, level, ramp=0.15):
    g = np.zeros(n)
    for a, b in spans:
        g = np.maximum(g, np.clip(np.minimum((t - (a - ramp)) / ramp, ((b + ramp) - t) / ramp), 0, 1))
    return g
gain = 0.32 + (1.0 - 0.32) * env(SPEECH, 1.0)
gain = gain * (1 - (1 - 0.14 / 0.32) * env(windows, 1.0, 0.2))
sf.write("build/base_ducked.wav", (base * gain[:, None]).astype(np.float32), SR)
sf.write("assets/narration.wav", narr, SR)
print("narration windows:", [(round(a, 2), round(b, 2)) for a, b in windows])
