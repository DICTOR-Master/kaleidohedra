#!/usr/bin/env python3
"""Breadth-first search over all fine tilings of T reachable by flips (a flip re-tiles one 4-generator rhombic dodecahedron
made of 4 cells), from one regular tiling. Each tiling is checked exactly (surface = T, no two cells cross). Reports whether any
tiling holds all four corner cells of Inchbald's solid; if so writes the 16 other cells as tile_check input.
Usage: flips.py <k10 dir> <out dir>"""
import sys, json, itertools
import numpy as np
from collections import deque
K10, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, K10 + '/scripts')
from zsurf import *
G = Geo(6); n = 6
E = np.array([[zfloat(c) for c in e] for e in G.E]); T = zonotope(G)
d = json.load(open(OUT + '/inchbald.json'))
S = {(tuple(f[0]), f[1], f[2]): f[3] for f in d['candidates_rank_le_3'][0]['faces']}
REM = {((0,1,0,0,0,0),(0,2,5)), ((0,0,0,0,0,0),(0,3,4)), ((0,0,0,1,0,1),(1,2,4)), ((1,0,1,0,1,0),(1,3,5))}
h = np.random.default_rng(0).normal(size=n); W = np.hstack([E, h[:, None]])
start = []
for t in itertools.combinations(range(n), 3):
    d3 = np.linalg.det(E[list(t)]); q = [0]*n
    for l in range(n):
        if l not in t and np.sign(np.linalg.det(W[list(t) + [l]])) * np.sign(d3) > 0: q[l] = 1
    start.append((tuple(q), t))
if from_cells(G, start) != T: start = [(tuple(1 - x if i not in t else 0 for i, x in enumerate(q)), t) for q, t in start]
assert from_cells(G, start) == T
def valid(cells): return from_cells(G, cells) == T and not any(G.relation(a[0], a[1], b[0], b[1]) == 'cross' for a, b in itertools.combinations(cells, 2))
assert valid(start)
seen = {frozenset(start)}; Q = deque([frozenset(start)]); found = None
while Q:
    til = Q.popleft()
    if REM <= til: found = til; break
    bytype = {c[1]: c for c in til}
    for A in itertools.combinations(range(n), 4):
        cs = [bytype[tuple(x for x in A if x != l)] for l in A]
        base = [tuple(c[0][i] for i in range(n) if i not in A) for c in cs]
        if len(set(base)) != 1: continue
        new = set(til)
        for l, c in zip(A, cs):
            q = list(c[0]); q[l] = 1 - q[l]; new.discard(c); new.add((tuple(q), c[1]))
        key = frozenset(new)
        if key in seen: continue
        if not valid(list(key)): continue
        seen.add(key); Q.append(key)
print('tilings of T reached by flips:', len(seen))
if found:
    keep = [c for c in found if c not in REM]
    ok = from_cells(G, keep) == S and not any(G.relation(a[0], a[1], b[0], b[1]) == 'cross' for a, b in itertools.combinations(keep, 2))
    print('a tiling holds all four corner cells; solid reproduced exactly:', ok)
    if ok:
        d['candidates_rank_le_3'][0]['cells'] = [[list(c[0]), list(c[1]), 1] for c in keep]
        d['cell_types'] = sorted(''.join(map(str, c[1])) for c in keep)
        json.dump(d, open(OUT + '/inchbald.json', 'w')); print('cell types', d['cell_types'])
    print('FINAL ok' if ok else 'FINAL FAIL: tiling found but the solid is not reproduced')
else:
    cnt = {}
    for til in seen:
        k = len(REM & til); cnt[k] = cnt.get(k, 0) + 1
    print('no reached tiling holds all four; tilings by how many of the four they hold:', dict(sorted(cnt.items())))
    print('FINAL none')
