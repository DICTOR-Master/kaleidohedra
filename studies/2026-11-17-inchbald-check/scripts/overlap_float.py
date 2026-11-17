#!/usr/bin/env python3
"""Floating-point (not exact) overlap volumes of Inchbald's solid P with its lattice translates P + l, |l| <= 2R + margin.
1_P = sum of 17 cells of a tiling of T that holds three of the four corner cells, minus the fourth corner cell (inside them).
vol(P n (P+l)) = sum over signed cell pairs of vol(a n b'), each a convex intersection (scipy HalfspaceIntersection + ConvexHull).
Usage: overlap_float.py <k10 dir> <out dir>"""
import sys, json, itertools
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog
from collections import deque
K10, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, K10 + '/scripts')
from zsurf import *
G = Geo(6); n = 6
E = np.array([[zfloat(c) for c in e] for e in G.E]); T = zonotope(G)
d = json.load(open(OUT + '/inchbald.json')); S = {(tuple(f[0]), f[1], f[2]): f[3] for f in d['candidates_rank_le_3'][0]['faces']}
REM = [((0,1,0,0,0,0),(0,2,5)), ((0,0,0,0,0,0),(0,3,4)), ((0,0,0,1,0,1),(1,2,4)), ((1,0,1,0,1,0),(1,3,5))]
info, _ = analyse(G, S); lam = face_pair_vectors(G, S, info); assert lam is not None
basis = int_rank_basis(list(lam.values())); print('face-pair lattice rank', len(basis), basis)
assert len(basis) == 3
# flip search again for a tiling holding three of the four
h = np.random.default_rng(0).normal(size=n); W = np.hstack([E, h[:, None]]); start = []
for t in itertools.combinations(range(n), 3):
    d3 = np.linalg.det(E[list(t)]); q = [0]*n
    for l in range(n):
        if l not in t and np.sign(np.linalg.det(W[list(t) + [l]])) * np.sign(d3) > 0: q[l] = 1
    start.append((tuple(q), t))
def valid(cells): return from_cells(G, cells) == T and not any(G.relation(a[0], a[1], b[0], b[1]) == 'cross' for a, b in itertools.combinations(cells, 2))
seen = {frozenset(start)}; Q = deque([frozenset(start)]); best = None
while Q and best is None:
    til = Q.popleft()
    for r4 in REM:
        if all(r in til for r in REM if r != r4): best = (til, r4); break
    bt = {c[1]: c for c in til}
    for A in itertools.combinations(range(n), 4):
        cs = [bt[tuple(x for x in A if x != l)] for l in A]
        if len({tuple(c[0][i] for i in range(n) if i not in A) for c in cs}) != 1: continue
        new = set(til)
        for l, c in zip(A, cs): q = list(c[0]); q[l] = 1 - q[l]; new.discard(c); new.add((tuple(q), c[1]))
        k = frozenset(new)
        if k not in seen and valid(list(k)): seen.add(k); Q.append(k)
til, r4 = best
signed = [(c, 1) for c in til if c not in REM] + [(r4, -1)]
print('signed cells', len(signed), '(17 plus, 1 minus)')
def box(c, shift=np.zeros(3)):
    p, t = c; o = np.array(p, float) @ E + shift; V = E[list(t)]
    H = []
    for a, b in ((0, 1), (0, 2), (1, 2)):
        nv = np.cross(V[a], V[b]); k = 3 - a - b
        if nv @ V[k] < 0: nv = -nv
        lo, hi = nv @ o, nv @ (o + V[k])
        H.append(np.r_[nv, -hi]); H.append(np.r_[-nv, lo])
    return np.array(H)
def vol_int(H):
    A, b = H[:, :3], -H[:, 3]; nrm = np.linalg.norm(A, axis=1)
    res = linprog(np.r_[np.zeros(3), -1], A_ub=np.c_[A, nrm], b_ub=b, bounds=[(None, None)]*3 + [(0, None)])
    if not res.success or res.x[3] < 1e-9: return 0.0
    hs = HalfspaceIntersection(H, res.x[:3]); return ConvexHull(hs.intersections).volume
vP = sum(s * ConvexHull(np.array([np.array(c[0], float) @ E + sum(E[i]*x for i, x in zip(c[1], bits)) for bits in itertools.product((0, 1), repeat=3)])).volume for c, s in signed)
B = np.array(basis, float) @ E; cov = abs(np.linalg.det(B))
print('volume of P', vP, 'covolume', cov)
pts = np.array([np.array(f[0], float) @ E for f in S]); R = np.linalg.norm(pts - pts.mean(0), axis=1).max() + 3
worst = 0; tested = 0
rng = range(-6, 7)
for c in itertools.product(rng, repeat=3):
    if c == (0, 0, 0): continue
    sh = np.array(c, float) @ B
    if np.linalg.norm(sh) > 2*R: continue
    tested += 1; v = 0.0
    for (a, sa), (b, sb) in itertools.product(signed, signed):
        v += sa * sb * vol_int(np.vstack([box(a), box(b, sh)]))
    worst = max(worst, abs(v))
    if abs(v) > 1e-6: print('OVERLAP', c, v)
print('translates tested', tested, 'largest |overlap volume|', worst)
print('FINAL', 'no overlap (float)' if worst < 1e-6 else 'overlap')
