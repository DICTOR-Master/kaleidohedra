"""D–I bridge B, step 1 (DICTO 10 Nov: "both, A first" → "start B now while A runs"): the gap under a diagonal plane.
World 1 (#47: dodecahedra edge 1 = Euclid's cube of edge phi + 6 roofs, on the even cells of the cubic grid of edge phi; Dogstars in the
odd cells). The octet of edge phi*sqrt2 has its corners exactly at the even-cell centres (one shared lattice). Plane n.x = c,
n = (1,1,1)/sqrt3, c = L + phi*sqrt3/2: the dodecahedra of the diagonal layer at level L touch it with one corner each (points only).
Kept below: dodecahedra with centre level <= L, Dogstars with centre level <= L - phi/sqrt3. The GAP = points under the plane covered by
nothing kept. This measures it (sampling, exploration): volume per period, its connected pieces, their volumes and convexity.
Usage: python gap.py"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1'))
from mixes3 import planes, phi, CUBE, ROOF, DOD
from scipy.spatial import ConvexHull
from scipy import ndimage
n = np.ones(3) / 3 ** .5; L = 0.0; c = L + phi * 3 ** .5 / 2
pieces = []
for i, j, k in itertools.product(range(-6, 7), repeat=3):
    ctr = np.array([i, j, k]) * phi; lev = ctr @ n
    if (i + j + k) % 2 == 0 and lev <= L + 1e-9 and lev > L - 6:
        pieces.append(planes(DOD + ctr))
    elif (i + j + k) % 2 == 1 and lev <= L - phi / 3 ** .5 + 1e-9 and lev > L - 6:
        # Dogstar = cube minus the six roofs poking in from the dodecahedra around it
        pieces.append(('S', planes(CUBE + ctr), [planes(ROOF[(a, -sg)] + ctr + np.eye(3)[a] * sg * phi) for a in range(3) for sg in (1, -1)]))
def inside(X, pl): nrm, off = pl; return np.all(X @ nrm.T < off - 1e-12, axis=1)
def covered(X):
    cov = np.zeros(len(X), bool)
    for p in pieces:
        if isinstance(p, tuple) and len(p) == 3 and p[0] == 'S':
            m = inside(X, p[1])
            for r in p[2]: m &= ~inside(X, r)
            cov |= m
        else: cov |= inside(X, p)
    return cov
# in-plane period: hexagonal, vectors phi*(1,-1,0) and phi*(0,1,-1) (length phi*sqrt2); sample one period cell x depth 3
u = phi * np.array([1., -1, 0]); v = phi * np.array([0., 1, -1])
res = 96; dz = 3.0; nz = 120
A, B, Z = np.meshgrid(np.arange(res) / res, np.arange(res) / res, (np.arange(nz) + 0.5) / nz * dz, indexing='ij')
X = (A[..., None] * u + B[..., None] * v + (c - Z)[..., None] * n).reshape(-1, 3)
gap = ~covered(X)
cellvol = np.linalg.norm(np.cross(u, v)) * dz
print(f'period area {np.linalg.norm(np.cross(u, v)):.6f}; gap volume per period ≈ {gap.mean() * cellvol:.5f} (depth window {dz})')
G = gap.reshape(res, res, nz)
deepest = (G.any(axis=(0, 1)) * (np.arange(nz) + 0.5) / nz * dz).max()
print(f'gap reaches {deepest:.3f} below the plane (window {dz})')
# connected pieces with in-plane periodicity: tile 2x2 and label, count pieces fully inside the centre copy
G2 = np.concatenate([np.concatenate([G, G], 0)] * 2, 1)
lab, nlab = ndimage.label(G2)
sizes = ndimage.sum(np.ones_like(lab), lab, range(1, nlab + 1)) * cellvol / (res * res * nz)
print(f'connected pieces in a 2x2 patch: {nlab}; volumes (sampled): {sorted(set(np.round(sizes, 3)))}')
print('FINAL ok' if gap.any() else 'FINAL FAIL: no gap found (check the plane level)')
