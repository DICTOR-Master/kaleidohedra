"""Exact check of a surround witness (DICTO 10 Nov 2026: 'yes run the exact check'). The six icosahedral axes are taken unnormalised
as (0, 1, φ)-type vectors (all of one length, so the scale drops out); every tile corner is an integer combination, so every coordinate
lies in Z[φ] ⊂ Q(√5). For every pair of tiles: interiors overlap iff no separating axis (3 + 3 face normals, 9 edge cross products)
separates them; projections compared EXACTLY in Q(√5) (qf.py). Also exact: every face within the search radius is shared by exactly
two tiles (no gaps there). usage: python verify_exact.py witness.json"""
import sys, json, itertools, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qf import QF
from fractions import Fraction as Fr
import numpy as np
W = json.load(open(sys.argv[1])); tiles = W['tiles']; Ef = np.array(W['axes_float'])
half = QF(Fr(1, 2), Fr(1, 2), 5)                        # phi
one, zero = QF(1, 0, 5), QF(0, 0, 5)
# exact axes matching the float ones up to the common positive scale: each float axis is (x, y, z)/|v| with entries in {0, ±1, ±phi}
s = np.sqrt(1 + ((1 + 5 ** .5) / 2) ** 2)
def ex(x):
    v = x * s
    for cand, q in ((0, zero), (1, one), (-1, -one), ((1 + 5 ** .5) / 2, half), (-(1 + 5 ** .5) / 2, -half)):
        if abs(v - cand) < 1e-9: return q
    raise ValueError(v)
E = [[ex(x) for x in row] for row in Ef]
def vec(iv): return [sum((E[i][k] * iv[i] for i in range(6) if iv[i]), zero) for k in range(3)]
def sub(a, b): return [x - y for x, y in zip(a, b)]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def corners(t):
    p = t['p']; a, b, c = t['span']; out = []
    for i, j, k in itertools.product((0, 1), repeat=3):
        out.append(vec([p[m] + i * a[m] + j * b[m] + k * c[m] for m in range(6)]))
    return out
T = [(corners(t), [vec(x) for x in t['span']]) for t in tiles]
TF = [np.array([[float(x.a) + float(x.b) * 5 ** .5 for x in c] for c in cs]) for cs, _ in T]
def overlap(i, j):
    (c1, e1), (c2, e2) = T[i], T[j]
    axes = [cross(e1[0], e1[1]), cross(e1[0], e1[2]), cross(e1[1], e1[2]), cross(e2[0], e2[1]), cross(e2[0], e2[2]), cross(e2[1], e2[2])]
    axes += [cross(x, y) for x in e1 for y in e2]
    for ax in axes:
        if all(x == zero for x in ax): continue
        p1 = [dot(c, ax) for c in c1]; p2 = [dot(c, ax) for c in c2]
        if max(p1) <= min(p2) or max(p2) <= min(p1): return False
    return True
bad = 0; checked = 0
for i, j in itertools.combinations(range(len(T)), 2):
    if np.any(TF[i].max(0) < TF[j].min(0) - 1e-9) or np.any(TF[j].max(0) < TF[i].min(0) - 1e-9): continue
    checked += 1
    if overlap(i, j): bad += 1; print('OVERLAP', i, j)
# gap check (exact: faces are sets of integer corner keys): faces within the search radius shared by exactly two tiles
add = lambda p, q: tuple(x + y for x, y in zip(p, q))
cnt = {}
for t in tiles:
    p = tuple(t['p']); a, b, c = (tuple(x) for x in t['span'])
    for (u, w), base in (((a, b), [p, add(p, c)]), ((a, c), [p, add(p, b)]), ((b, c), [p, add(p, a)])):
        for q in base:
            f = frozenset([q, add(q, u), add(q, w), add(add(q, u), w)]); cnt[f] = cnt.get(f, 0) + 1
Ef_ = Ef
def cen(f): return np.mean([np.array(q) @ Ef_ for q in f], axis=0)
over2 = sum(1 for n in cnt.values() if n > 2)
open_in = sum(1 for f, n in cnt.items() if n == 1 and np.linalg.norm(cen(f)) <= W['rmax'] - 1e-6)
print(f'faces used by more than two tiles {over2}; open faces inside radius {W["rmax"]}: {open_in}')
bad += over2 + open_in
print(f'tiles {len(T)}; pairs tested exactly {checked}; overlapping pairs {bad}')
print('FINAL ok' if bad == 0 else 'FINAL FAIL: overlapping tiles')
