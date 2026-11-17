"""Positive control with a known answer: a periodic Voronoi tiling of moving seeds, drawn as an image and sent through the SAME
segmentation, matching, logger and flicker filter as the Sun data (census.py), against the exact count of neighbour swaps.

Seeds move on smooth random paths in an L x L periodic box (L = 504 pixels, as the Bifrost grid). Image = minus the periodic distance
to the nearest seed (each seed is a peak, the Voronoi edges are the valleys), optionally with smooth noise added (texture). Exact
swaps: the periodic Delaunay neighbour sets are computed at 20 substeps per frame, and every pair lost between substeps is counted
(with N seeds fixed there are no births or deaths, so every change is a swap = one Delaunay edge flip).
Usage: control_voronoi.py OUTDIR N FRAMES SPEED NOISE SEED"""
import sys, os, json
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tiles as TL

out, N, NF, speed, noise, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6])
L = 504; SUB = 20
rng = np.random.default_rng(seed)
os.makedirs(out, exist_ok=True)
p0 = rng.uniform(0, L, (N, 2))
# smooth paths: sum of two random Fourier modes per seed and coordinate
A = rng.normal(0, 1, (N, 2, 2)); w = rng.uniform(0.002, 0.01, (N, 2, 2)); ph = rng.uniform(0, 2 * np.pi, (N, 2, 2))
def pos(t):
    return (p0 + speed * (A * np.sin(w * t + ph)).sum(2) / np.maximum(w.mean(2), 1e-9) * 0.01) % L
def pairs(P):
    nb = TL.periodic_voronoi_counts(P, L)
    return {(min(i, j), max(i, j)) for i in nb for j in nb[i]}
yy, xx = np.indices((L, L))
grid = np.stack([yy.ravel(), xx.ravel()], 1) + 0.5
name = f'voronoi_n{N}_v{speed}_z{noise}_s{seed}'
img = np.lib.format.open_memmap(f'{out}/{name}_img_dz0.0.npy', mode='w+', dtype=np.float32, shape=(NF, L, L))
exact_total, exact_per_frame, frame_changes = 0, [], []
prevP = pairs(pos(0.0))
frame_pairs = [sorted(prevP)]
for k in range(NF):
    t = 10.0 * k
    P = pos(t)
    d, _ = cKDTree(P, boxsize=L).query(grid % L)
    f = -d.reshape(L, L)
    if noise > 0:
        f = f + noise * ndi.gaussian_filter(rng.normal(0, 1, (L, L)), 3, mode='wrap') / 0.094
    img[k] = f
    if k < NF - 1:
        c = 0; Pk = prevP
        for sstep in range(1, SUB + 1):
            Q = pairs(pos(t + 10.0 * sstep / SUB))
            c += len(prevP - Q); prevP = Q
        exact_per_frame.append(c); exact_total += c; frame_changes.append(len(Pk - prevP)); frame_pairs.append(sorted(prevP))
    print(f'PROGRESS {(k + 1) / NF:.4f} frame {k + 1}/{NF}', flush=True)
img.flush()
np.save(f'{out}/{name}_times.npy', 10.0 * np.arange(NF))
json.dump(dict(run=name, dx_Mm=1.0, dtsnap_s=10.0, n=NF), open(f'{out}/{name}_meta.json', 'w'))
# exact swaps for coarser steps: flips between frames k and k+s that are not undone inside the interval are not separable from
# sampling; we record the exact fine count and the per-frame list so any step can be compared
json.dump(dict(name=name, N=N, frames=NF, exact_swaps_total=exact_total, exact_per_frame=exact_per_frame,
               exact_frame_to_frame_lost_pairs=sum(frame_changes), substeps=SUB, frame_pairs=frame_pairs),
          open(f'{out}/{name}_exact.json', 'w'))
print('EXACT', name, exact_total, flush=True)
print('CONTROL_DATA_OK', flush=True)
