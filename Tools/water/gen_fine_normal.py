import numpy as np
from PIL import Image
import math

S = 1024
rng = np.random.default_rng(20261119)

# periodic value noise (tileable): integer lattice wrapped at period
def pnoise(period, octaves, persistence, seed):
    r = np.random.default_rng(seed)
    out = np.zeros((S, S), dtype=np.float64)
    amp = 1.0; norm = 0.0; p = period
    for o in range(octaves):
        g = r.standard_normal((p, p))
        # bilinear upsample with wrap
        xs = np.linspace(0, p, S, endpoint=False)
        x0 = np.floor(xs).astype(int) % p; x1 = (x0 + 1) % p; fx = xs - np.floor(xs)
        ys = xs; y0 = x0; y1 = x1; fy = fx
        fx = fx[None, :]; fy = fy[:, None]
        sx = fx*fx*(3-2*fx); sy = fy*fy*(3-2*fy)
        top = g[y0][:, x0]*(1-sx) + g[y0][:, x1]*sx
        bot = g[y1][:, x0]*(1-sx) + g[y1][:, x1]*sx
        out += amp * (top*(1-sy) + bot*sy)
        norm += amp; amp *= persistence; p *= 2
    return out / norm

# fine anisotropic ripples: many integer wave vectors, elongated along X (flow)
h = np.zeros((S, S), dtype=np.float64)
xs = np.arange(S)[None, :] / S
ys = np.arange(S)[:, None] / S
N = 140
for i in range(N):
    # frequency grows across components; anisotropy: kx smaller than ky -> elongated along X
    f = 8.0 + (i / N) * 44.0
    kx = int(round(f * rng.uniform(0.35, 0.75)))
    ky = int(round(f * rng.uniform(0.8, 1.4)))
    if kx == 0: kx = 1
    if ky == 0: ky = 1
    phase = rng.uniform(0, 2*math.pi)
    amp = (1.0 / (f ** 0.85)) * rng.uniform(0.7, 1.3)
    h += amp * np.sin(2*math.pi*(kx*xs + ky*ys) + phase)

# organic irregularity: 3 octaves periodic noise
h += 0.35 * pnoise(8, 3, 0.55, 777)

# normalize height
h -= h.mean(); h /= (h.std() + 1e-9)

# gradient via periodic central difference
strength = 7.0
dhx = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)) * 0.5 * strength
dhy = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)) * 0.5 * strength
nz = np.ones_like(h)
ln = np.sqrt(dhx*dhx + dhy*dhy + nz*nz)
nx = -dhx/ln; ny = -dhy/ln; nz = nz/ln

rgb = np.stack([nx, ny, nz], axis=-1) * 0.5 + 0.5
rgb = np.clip(rgb, 0, 1)
img = (rgb * 255).astype(np.uint8)
Image.fromarray(img, "RGB").save(r"F:/CG/Projects/PICOUE/logs/water-assets/T_RiverFine_Normal.png")
print("FINE_OK", img.shape, "nz_range", float(nz.min()), float(nz.max()))
