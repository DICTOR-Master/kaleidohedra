#!/usr/bin/env python3
"""Search fine tilings of T (by lifting, random heights) that contain the four removed corner cells of Inchbald's solid;
then the solid is the union of the other 16 cells. Writes tile_check input. Usage: lifts.py <k10 dir> <out dir> <tries>"""
import sys, json, itertools, random
import numpy as np
K10, OUT, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, K10 + '/scripts')
from zsurf import *
G = Geo(6); n = 6
E = np.array([[zfloat(c) for c in e] for e in G.E]); T = zonotope(G)
d = json.load(open(OUT + '/inchbald.json'))
S = {(tuple(f[0]), f[1], f[2]): f[3] for f in d['candidates_rank_le_3'][0]['faces']}
REM = {((0,1,0,0,0,0),(0,2,5)), ((0,0,0,0,0,0),(0,3,4)), ((0,0,0,1,0,1),(1,2,4)), ((1,0,1,0,1,0),(1,3,5))}
assert from_cells(G, list(REM)) is not None
seen = set(); random.seed(1)
for trial in range(N):
    h = np.random.default_rng(trial).normal(size=n)
    W = np.hstack([E, h[:, None]])
    for s in (1, -1):
        cells = []
        for t in itertools.combinations(range(n), 3):
            d3 = np.linalg.det(E[list(t)]); q = [0]*n
            for l in range(n):
                if l not in t and np.sign(np.linalg.det(W[list(t) + [l]])) * np.sign(d3) * s > 0: q[l] = 1
            cells.append((tuple(q), t))
        key = frozenset(cells)
        if key in seen: continue
        if from_cells(G, cells) != T: continue
        seen.add(key)
        if REM <= key:
            keep = [c for c in cells if c not in REM]
            ok = from_cells(G, keep) == S and not any(G.relation(a[0], a[1], b[0], b[1]) == 'cross' for a, b in itertools.combinations(keep, 2))
            print('trial', trial, 'tiling of T holding all four corner cells; solid reproduced exactly:', ok)
            if ok:
                d['candidates_rank_le_3'][0]['cells'] = [[list(c[0]), list(c[1]), 1] for c in keep]
                d['cell_types'] = sorted(''.join(map(str, c[1])) for c in keep)
                json.dump(d, open(OUT + '/inchbald.json', 'w')); print('cell types', d['cell_types']); print('FINAL ok'); sys.exit()
print('distinct regular tilings of T seen', len(seen), '; none holds all four corner cells'); print('FINAL none')
