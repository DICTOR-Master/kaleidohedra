# DICTO Spheroid-13 RD, research batch 1 (2026-10-13): the block lattice, the symmetry of the tiling and of the rounded block, the
# roundest-tile benchmark (the block lattice's Voronoi cell), and how the centre pieces meet across blocks.
# Usage: python3 analysis.py rd13-round-m0.15.json [rd13-round-m0.35.json ...]
import sys, json, itertools, numpy as np
from scipy.spatial import Voronoi, ConvexHull
R0 = json.load(open(sys.argv[1]))
L = np.array(R0['L'], float)          # rows: three short block-lattice vectors
G = L @ L.T
print('block lattice basis (rows):', L.astype(int).tolist())
print('Gram matrix:', G.astype(int).tolist(), ' covolume', round(abs(np.linalg.det(L)), 6))
# reduced: all vectors of the lattice up to length^2 12, and the shortest ones
pts = [a * L[0] + b * L[1] + c * L[2] for a, b, c in itertools.product(range(-3, 4), repeat=3) if (a, b, c) != (0, 0, 0)]
lens = sorted({round(float(p @ p), 6) for p in pts})[:4]
print('shortest squared lengths:', lens, ' how many of each:', [sum(1 for p in pts if abs(p @ p - l) < 1e-6) for l in lens])
# point symmetry of the tiling: cube symmetries (about the centre) that map the block lattice to itself
ops = []
for perm in itertools.permutations(range(3)):
    for s in itertools.product([1, -1], repeat=3):
        M = np.zeros((3, 3)); [M.__setitem__((i, p), s[i]) for i, p in enumerate(perm)]; ops.append(M)
Li = np.linalg.inv(L.T)
stab = [M for M in ops if np.allclose(np.round(Li @ (M @ L.T)), Li @ (M @ L.T), atol=1e-9)]
proper = sum(1 for M in stab if np.linalg.det(M) > 0)
print('tiling point group: order', len(stab), '(turns', proper, ', with inversion' if any(np.allclose(M, -np.eye(3)) for M in stab) else '', ')')
# symmetry of each rounded block: which of those map its corner set to itself
for fn in sys.argv[1:]:
    R = json.load(open(fn)); V = np.array([p for c in R['cells'] for f in c for p in f])
    U = np.unique(np.round(V, 6), axis=0)
    # The optimiser may slide the whole honeycomb (it changes nothing), so test about the centre piece's own middle.
    mid = np.unique(np.round(np.array([p for f in R['cells'][0] for p in f]), 6), axis=0).mean(0); U = U - mid
    keep = [M for M in stab if all(np.min(np.linalg.norm(U - M @ u, axis=1)) < 1e-5 for u in U)]
    print(f"rounded block (thickness {R['margin']}): symmetry order {len(keep)} of {len(stab)}")
# benchmark: the Voronoi cell of the block lattice, the roundest tile with these translations (volume 26)
P = np.array([a * L[0] + b * L[1] + c * L[2] for a, b, c in itertools.product(range(-2, 3), repeat=3)])
vor = Voronoi(P); o = int(np.argmin(np.linalg.norm(P, axis=1))); reg = vor.regions[vor.point_region[o]]
cell = ConvexHull(vor.vertices[reg]); iq = 36 * np.pi * cell.volume ** 2 / cell.area ** 3
print('Voronoi cell of the block lattice: volume %.4f area %.4f roundness %.4f faces %d' % (cell.volume, cell.area, iq, len({tuple(np.round(e[:3], 5)) for e in cell.equations})))
# centres across blocks: does the centre piece meet its copies in the neighbouring blocks?
for fn in sys.argv[1:]:
    R = json.load(open(fn)); C = np.unique(np.round(np.array([p for f in R['cells'][0] for p in f]), 6), axis=0)
    touch = {}
    for t in pts:
        if t @ t > 40: continue
        shared = sum(1 for p in C if np.min(np.linalg.norm(C + t - p, axis=1)) < 1e-5)
        if shared: touch[round(float(t @ t), 3)] = touch.get(round(float(t @ t), 3), []) + [shared]
    print(f"thickness {R['margin']}: centre meets centres in other blocks: {touch if touch else 'never (each centre is wrapped by its twelve)'}")
