#!/usr/bin/env python3
"""Independent check of the N = 20 tiling found by tile_octet.py: rebuild the torus solution, take the two placed pieces as real polytopes (T(4) minus corners,
from half-spaces), repeat them by the period lattice L, and check (1) volume: 2 pieces = one period cell, (2) no overlap among all copies near the origin
(separating axes, methods.overlap), (3) coverage: random points in a box each lie in exactly one copy."""
import sys, os, json, itertools, numpy as np
sys.path.insert(0, 'scripts/_lib')
try: import methods as M; overlap = M.overlap
except Exception: M = None
sys.argv = [sys.argv[0]]; exec(open('scripts/tile_octet.py').read().split("if __name__")[0])
from scipy.spatial import ConvexHull, Delaunay
cl = PIECES['S2'](); kinds = [c[0] for c in cl]; pts = np.array([c[1] for c in cl])
H = np.array([[10, 1, 4], [0, 2, 1], [0, 0, 1]], float); L = B @ H
orients = []; seen = set()
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        Mx = np.zeros((3, 3))
        for i in range(3): Mx[i, perm[i]] = sg[i]
        k = frozenset((kd, tuple(np.round(q - (pts @ Mx.T).min(0), 6))) for kd, q in zip(kinds, pts @ Mx.T))
        if k not in seen: seen.add(k); orients.append(Mx)
# re-solve to get the placements
Li = np.linalg.inv(L)
def key(kind, x): z = Li @ np.asarray(x, float); return (kind, tuple(np.round(z - np.floor(z + 1e-9), 6) % 1))
reps = [B @ np.array(v, float) for v in itertools.product(*[range(int(H[k, k])) for k in range(3)])]
base = [('O', (1, 0, 0)), ('T', (.5, .5, .5)), ('T', (-.5, -.5, -.5))]
idx = {c: i for i, c in enumerate(sorted({key(k, np.array(p) + r) for r in reps for k, p in base}))}
rows, meta = [], []
for oi, Mx in enumerate(orients):
    for r in reps:
        ks = [idx.get(key(k, p + r)) for k, p in zip(kinds, pts @ Mx.T)]
        if None in ks or len(set(ks)) != len(ks): continue
        rows.append(tuple(sorted(ks))); meta.append((oi, r))
sol = solve(rows, len(idx)); place = [meta[i] for i in sol]
V0 = np.array([(0,0,0),(4,4,0),(4,0,4),(0,4,4)], float); C = V0.mean(0)
# S2 solid = T(4) ∩ {cut planes}: corners T(4) - corner T(1): take hull of T(4) vertices moved 1/4 along edges
corners = [v + (w - v)/4 for v in V0 for w in V0 if not np.array_equal(v, w)]
S = np.array(corners); hS = ConvexHull(S)
copies = []
for oi, r in place:
    for t in itertools.product(range(-7, 8), repeat=3):
        c = S @ orients[oi].T + r + L @ np.array(t, float)
        if np.linalg.norm(c.mean(0)) < 16: copies.append(c)
vol_piece = hS.volume; vol_cell = abs(np.linalg.det(L))
out = {'placements': [(int(o), [float(x) for x in r]) for o, r in place], 'piece_volume': vol_piece, 'period_volume': vol_cell, 'volume_ok': bool(abs(2*vol_piece - vol_cell) < 1e-9)}
cen = [c.mean(0) for c in copies]; near = [i for i, c in enumerate(cen) if np.linalg.norm(c) < 14]
bad = 0; pairs = 0
for i, j in itertools.combinations(near, 2):
    if np.linalg.norm(cen[i] - cen[j]) > 9: continue
    pairs += 1
    if M is not None and M.overlap(copies[i], copies[j]): bad += 1
out['overlap_pairs_tested'] = pairs; out['overlaps'] = bad
D = [Delaunay(c) for c in copies]; rng = np.random.default_rng(1); X = rng.uniform(-5, 5, (20000, 3))
cnt = np.zeros(len(X), int)
for d in D: cnt += d.find_simplex(X) >= 0
out['coverage_counts'] = {int(k): int(v) for k, v in zip(*np.unique(cnt, return_counts=True))}
# describe the piece: faces
from collections import Counter
fa = Counter(); 
for eq in np.unique(np.round(hS.equations, 4), axis=0):
    on = [p for p in S if abs(eq[:3] @ p + eq[3]) < 1e-6]; fa[len(on)] += 1
out['faces_by_corner_count'] = dict(fa); out['corners'] = len(S)
out['orientations_used'] = sorted({int(o) for o, r in place}); out['orient_matrices'] = [orients[o].tolist() for o in out['orientations_used']]
print(json.dumps(out, indent=1)); json.dump(out, open('data/tiling-N20.json', 'w'), indent=1)
