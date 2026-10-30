"""Textures for the ThiagoCall film: paper fibre tile, walnut desk, film grain tiles."""
import sys
import numpy as np
from PIL import Image, ImageFilter

out = sys.argv[1]
rng = np.random.default_rng(7)


def smooth_noise(h, w, cell_y, cell_x):
    """Value noise: random grid upsampled with bicubic."""
    g = rng.random((max(2, h // cell_y + 2), max(2, w // cell_x + 2))).astype(np.float32)
    img = Image.fromarray((g * 255).astype(np.uint8)).resize((w + 2 * cell_x, h + 2 * cell_y), Image.BICUBIC)
    return np.asarray(img, dtype=np.float32)[cell_y:cell_y + h, cell_x:cell_x + w] / 255.0


# Paper: fine fibres, seamless enough at 512 with low contrast.
n = 512
fib = sum(smooth_noise(n, n, cy, cx) * a for cy, cx, a in [(2, 18, 0.5), (3, 7, 0.3), (1, 1, 0.2)])
fib = (fib - fib.mean()) / fib.std()
alpha = np.clip(fib * 18 + 14, 0, 60).astype(np.uint8)
rgba = np.zeros((n, n, 4), np.uint8)
rgba[..., :3] = (90, 70, 45)
rgba[..., 3] = alpha
Image.fromarray(rgba, "RGBA").save(f"{out}/paper.png")

# Walnut desk: long horizontal grain, rings warped by low-frequency noise.
h, w = 2050, 1450  # rendered at 2x in the film (2900 x 4100)
warp = smooth_noise(h, w, 180, 260) * 40
y = np.arange(h, dtype=np.float32)[:, None] + warp
rings = 0.5 + 0.5 * np.sin(y / 9.0 + smooth_noise(h, w, 40, 400) * 6)
streak = smooth_noise(h, w, 2, 160)
fine = smooth_noise(h, w, 1, 30)
v = 0.45 * rings + 0.35 * streak + 0.2 * fine
v = (v - v.min()) / (v.max() - v.min())
dark = np.array([16, 10, 7], np.float32)
light = np.array([62, 38, 22], np.float32)
img = dark + (light - dark) * (v[..., None] ** 1.6)
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).save(f"{out}/desk.jpg", quality=92)

# Film grain: four tiles, cycled per frame.
for i in range(4):
    g = rng.normal(128, 38, (512, 512)).clip(0, 255).astype(np.uint8)
    Image.fromarray(g, "L").convert("RGB").save(f"{out}/grain{i}.png")
print("ok")
