"""Line-by-line Kokoro (ONNX) voice-over: one wav per script line plus durations.

usage: python3 kokoro_vo.py script.txt out_dir model.onnx voices.bin [voice] [speed]
"""
import json
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

script, out, model, voices = sys.argv[1:5]
voice = sys.argv[5] if len(sys.argv) > 5 else "pm_alex"
speed = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
k = Kokoro(model, voices)
lines = [l.strip() for l in open(script, encoding="utf-8") if l.strip()]
meta = []
for i, text in enumerate(lines, 1):
    audio, sr = k.create(text, voice=voice, speed=speed, lang="pt-br")
    # trim silence at both ends (-45 dB)
    a = np.abs(audio)
    on = np.where(a > 10 ** (-45 / 20) * a.max())[0]
    audio = audio[max(0, on[0] - int(0.02 * sr)) : on[-1] + int(0.06 * sr)]
    path = f"{out}/line{i:02d}.wav"
    sf.write(path, audio, sr)
    meta.append({"i": i, "text": text, "file": path, "dur": round(len(audio) / sr, 3)})
    print(f"{i:02d} {len(audio)/sr:5.2f}s  {text}")
json.dump(meta, open(f"{out}/lines.json", "w"), ensure_ascii=False, indent=1)
print("total", round(sum(m["dur"] for m in meta), 2))
