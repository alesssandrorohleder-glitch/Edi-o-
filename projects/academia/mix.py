"""Keeps the real speech up front and the crowd/ambience low everywhere else.

Speech windows come from a Whisper pass over build/base_raw.mp4 (build/speech.json).
"""
import subprocess, numpy as np, soundfile as sf

SR = 48000
SPEECH = [(0.3, 12.85), (31.3, 34.4)]   # opener talk; "...falta só 16"
BED, VOICE, RAMP = 0.32, 1.0, 0.2

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "build/base_raw.mp4", "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
base = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
t = np.arange(len(base)) / SR
g = np.zeros(len(base))
for a, b in SPEECH:
    g = np.maximum(g, np.clip(np.minimum((t - (a - RAMP)) / RAMP, ((b + RAMP) - t) / RAMP), 0, 1))
sf.write("build/base_mixed.wav", (base * (BED + (VOICE - BED) * g)[:, None]).astype(np.float32), SR)
