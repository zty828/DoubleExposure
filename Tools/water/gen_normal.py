import numpy as np
from PIL import Image
import os
# Tileable multi-scale water normal map: sum of periodic sine waves (integer wave vectors => seamless)
rng = np.random.default_rng(42)
N = 512
x = np.arange(N) / N
X, Y = np.meshgrid(x, x, indexing='xy')
H = np.zeros((N, N), dtype=np.float64)
# (kx, ky, amplitude, phase) - integer k ensures tiling
waves = []
for i in range(14):
    kx = int(rng.integers(-7, 8)); ky = int(rng.integers(-7, 8))
    if kx == 0 and ky == 0: kx = 1
    k = (kx*kx + ky*ky) ** 0.5
    amp = 0.9 / (1.0 + k**1.6)   # spectral falloff: big swells + fine ripples
    waves.append((kx, ky, amp, rng.uniform(0, 2*np.pi)))
for kx, ky, amp, ph in waves:
    H += amp * np.sin(2*np.pi*(kx*X + ky*Y) + ph)
# slight sharpening of crests
H = H + 0.18 * np.sin(2*np.pi*(3*X + 5*Y) + 1.3) * np.sin(2*np.pi*(-4*X + 2*Y))
# gradients via periodic differences
strength = 8.0
dX = (np.roll(H, -1, axis=1) - np.roll(H, 1, axis=1)) * 0.5 * strength * N / (2*np.pi) * 0.02
dY = (np.roll(H, -1, axis=0) - np.roll(H, 1, axis=0)) * 0.5 * strength * N / (2*np.pi) * 0.02
nx, ny, nz = -dX, -dY, np.ones_like(H)
L = np.sqrt(nx*nx + ny*ny + nz*nz)
nx, ny, nz = nx/L, ny/L, nz/L
rgb = np.stack([(nx*0.5+0.5), (ny*0.5+0.5), (nz*0.5+0.5)], axis=-1)
img = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
out = r'F:\CG\Projects\PICOUE\logs\water-assets'
os.makedirs(out, exist_ok=True)
p = os.path.join(out, 'T_RiverNormal.png')
Image.fromarray(img).save(p)
print('SAVED', p, os.path.getsize(p), 'bytes; normal z range', float(nz.min()), float(nz.max()))
