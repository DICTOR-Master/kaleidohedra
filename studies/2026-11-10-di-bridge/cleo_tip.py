"""Is the Dogstar part below the (111) plane at level 0.467086, of volume 0.0515 (= CLEO), congruent to CLEO (base equilateral 1/phi,
side edges 1)? Selects the cells exactly as cuts.py; samples the part densely; its convex hull gives corners and edge lengths."""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1')); sys.path.insert(0, os.path.expanduser('~/mslide/free'))
from mixes3 import phi, CUBE, ROOF
from scipy.spatial import ConvexHull
import cuts as CT
n = CT.n; c = 0.467086; e = 1 / phi
for i, j, k in itertools.product(range(-2, 3), repeat=3):
    if (i + j + k) % 2 == 0: continue
    ctr = np.array([i, j, k]) * phi; C = CUBE + ctr
    if not ((C @ n).min() < c < (C @ n).max()): continue
    v = CT.cut_vol(C, c) - sum(CT.cut_vol(ROOF[(a, -sg)] + ctr + np.eye(3)[a] * sg * phi, c) for a in range(3) for sg in (1, -1))
    if abs(v - 0.0515) > 1e-3: continue
    low = C[np.argmin(C @ n)]
    rs = np.random.default_rng(1); X = low + (rs.uniform(-1, 1, (3000000, 3)) * 1.1)
    HC = ConvexHull(C); m = np.all(X @ HC.equations[:, :3].T + HC.equations[:, 3] < 0, axis=1) & (X @ n < c)
    for a in range(3):
        for sg in (1, -1):
            HR = ConvexHull(ROOF[(a, -sg)] + ctr + np.eye(3)[a] * sg * phi)
            m &= ~np.all(X @ HR.equations[:, :3].T + HR.equations[:, 3] < 0, axis=1)
    T = X[m]; hull = ConvexHull(T)
    found = abs(v - CT.cleo) < 1e-6
    print(f'cell {i,j,k}: part volume exact {v:.6f}, sampled hull {hull.volume:.5f}; CLEO {CT.cleo:.6f}')
    V = T[hull.vertices]
    apex = low; base = V[np.abs(V @ n - c) < 0.02]
    # three base corners: farthest-point selection
    far = [base[np.argmax(np.linalg.norm(base - base.mean(0), axis=1))]]
    for _ in range(2): far.append(base[np.argmax(np.min([np.linalg.norm(base - f, axis=1) for f in far], axis=0))])
    E = sorted(np.linalg.norm(far[a] - far[b]) for a, b in ((0, 1), (1, 2), (0, 2))); S = sorted(np.linalg.norm(f - apex) for f in far)
    print(f'   base edges ≈ {np.round(E, 3)} (CLEO 1/φ = {e:.3f}); side edges ≈ {np.round(S, 3)} (CLEO 1); height {c - apex @ n:.4f} (CLEO {np.sqrt(1 - e ** 2 / 3):.4f})')
    break
print('FINAL ok' if 'found' in dir() and found else 'FINAL FAIL: no CLEO-volume tip found')
