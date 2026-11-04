#!/usr/bin/env python3
"""Reversed-neighbour search for any centre pyramid whose lateral edges carry three pyramids at 120 deg (T: #92 Prop. 7; C6: #93 Thm D).
Generic convex pieces (vertex 0 = apex), separating-axis overlap from hull facets and all edge pairs. Usage: reversed_general.py T|C6 maxtiles"""
import itertools, math, sys
import numpy as np
from scipy.spatial import ConvexHull
EPS = 1e-9
def piece(kind):
    if kind == 'T':
        v = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)/(2*math.sqrt(2)); return np.array([np.zeros(3), *v[1:]])
    if kind == 'C6':
        return np.array([np.zeros(3), (.5, .5, .5), (.5, -.5, .5), (.5, -.5, -.5), (.5, .5, -.5)])
def axes_edges(t):
    h = ConvexHull(t); ax = [eq[:3] for eq in h.equations]
    ed = [t[j] - t[i] for s in h.simplices for i, j in itertools.combinations(s, 2)]
    return ax, ed
def overlap(a, b):
    aa, ea = axes_edges(a); ab, eb = axes_edges(b); cand = aa + ab
    for x in ea:
        for y in eb:
            c = np.cross(x, y); n = np.linalg.norm(c)
            if n > 1e-12: cand.append(c/n)
    best = 1e9
    for n in cand:
        pa, pb = a @ n, b @ n; d = min(pa.max() - pb.min(), pb.max() - pa.min())
        if d <= EPS: return 0.0
        best = min(best, d)
    return best
def same(a, b): return np.allclose(a[0], b[0], atol=1e-7) and len(a) == len(b) and all(np.min(np.linalg.norm(b[1:] - p, axis=1)) < 1e-7 for p in a[1:])
def rot(P, X, Y, ang):
    k = (Y - X)/np.linalg.norm(Y - X); c, s = math.cos(ang), math.sin(ang)
    return np.array([X + (p - X)*c + np.cross(k, p - X)*s + k*(k @ (p - X))*(1 - c) for p in P])
def refl(P, X, Y):
    m = (X + Y)/2; k = (Y - X)/np.linalg.norm(Y - X); return np.array([p - 2*((p - m) @ k)*k for p in P])
def cands(t, li):
    X, Y = t[0], t[li]; out = []
    for ang in (2*math.pi/3, -2*math.pi/3):
        n = rot(t, X, Y, ang); out.append([n, refl(n, X, Y)])
    return out
pens = []
def search(tiles, todo, maxd, st):
    st['nodes'] += 1
    if len(tiles) >= maxd: return True
    while todo:
        ti, li, si = todo[0]; cs = cands(tiles[ti], li)[si]
        if any(same(c, u) for c in cs for u in tiles): todo = todo[1:]; continue
        for c in cs:
            o = [overlap(c, u) for u in tiles]
            if max(o) > 0: pens.append(max(o)); continue
            k = len(tiles)
            if search(tiles + [c], todo[1:] + [(k, l, s) for l in range(1, len(c)) for s in (0, 1)], maxd, st): return True
        return False
    return True
kind, maxd = sys.argv[1], int(sys.argv[2])
P = piece(kind); nl = len(P) - 1
# sanity: normal pieces alone close the solid
tiles = [P]
for li in range(1, nl+1):
    for si in (0, 1):
        n = cands(P, li)[si][0]
        if not any(same(n, u) for u in tiles): tiles.append(n)
print(kind, 'normal pieces round P:', len(tiles), 'overlap-free:', all(overlap(a, b) == 0 for i, a in enumerate(tiles) for b in tiles[i+1:]))
Q = cands(P, 1)[0][1]
print('reversed Q overlaps P:', overlap(P, Q) > 0)
st = {'nodes': 0}
ok = search([P, Q], [(0, l, s) for l in range(1, nl+1) for s in (0, 1)] + [(1, l, s) for l in range(1, nl+1) for s in (0, 1)], maxd, st)
print(f'{kind}: some branch with a reversed neighbour survives to {maxd} pieces: {ok}; nodes {st["nodes"]}; rejections {len(pens)}; smallest penetration {min(pens) if pens else None}')
