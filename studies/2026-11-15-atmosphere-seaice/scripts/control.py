"""Controls built from one real frame: the frame is cut at an origin moving DY, DX pixels per step (a rigid drift, nothing
changes), with optional Gaussian noise of standard deviation NOISE (albedo units), redrawn each frame.
Expected: no noise -> no interior event at all (tests box tracking, the outside cell and matching);
noise -> elementary events from segmentation flicker, which the persistence rule should remove.
Usage: control.py SRC_DIR FRAME DY DX NOISE NFRAMES OUT_DIR"""
import sys, os, json
import numpy as np
src, k, dy, dx, noise, n, out = sys.argv[1:8]
k, dy, dx, noise, n = int(k), int(dy), int(dx), float(noise), int(n)
F = np.load(os.path.join(src, 'frames.npy'), mmap_mode='r'); t = np.load(os.path.join(src, 'times.npy'))
A = np.asarray(F[k]); H, W = A.shape
h, w = H - abs(dy) * n, W - abs(dx) * n
rng = np.random.default_rng(1)
fr = []
for q in range(n):
    r0 = (abs(dy) * n - dy * q) if dy > 0 else (-dy * q)
    c0 = (abs(dx) * n - dx * q) if dx > 0 else (-dx * q)
    r0 = min(max(r0, 0), H - h); c0 = min(max(c0, 0), W - w)
    a = A[r0:r0 + h, c0:c0 + w].copy()
    if noise > 0: a = a + rng.normal(0, noise, a.shape).astype(np.float32)
    fr.append(a)
os.makedirs(out, exist_ok=True)
np.save(os.path.join(out, 'frames.npy'), np.stack(fr).astype(np.float32))
np.save(os.path.join(out, 'times.npy'), (np.arange(n) * float(np.median(np.diff(t)))))
json.dump(dict(src=src, frame=k, dy=dy, dx=dx, noise=noise, n=n), open(os.path.join(out, 'meta.json'), 'w'))
print('CONTROL_DATA_OK', np.stack(fr).shape)
