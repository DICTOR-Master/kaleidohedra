#!/usr/bin/env python3
"""The 3D build the crocheted cells must make: HexOct at the end of the walk (lambda = 3/8, paper #98), where every c layer is
filled by cubes and every h layer by Narcissus, two pieces per ball. For several stackings, on a periodic box:
  1. volume: the pieces' volumes add up to the box;  2. no gaps or overlaps: 20 000 random points each lie in exactly one piece;
  3. face to face: every face of every piece coincides with a whole face of exactly one other piece (the crochet seams);
  4. census: which faces meet which (hexagon-hexagon, square-square, triangle-triangle; within a layer or across layers).
Layer tiles from tiles.py of the keyed-hexoct study (the census engine of #53/#57, exact rationals). Run on a compute host:
  python3 tiling.py <path to keyed-hexoct scripts>"""
import os, sys, math, json, itertools, collections, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, Delaunay
HEX = os.path.abspath(sys.argv[1]); here = os.getcwd(); sys.path.insert(0, HEX); os.chdir(HEX)
import tiles as T
from stackings import POS
os.chdir(here)
H = math.sqrt(2/3); s3 = math.sqrt(3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*s3/2, float(p[2])*H])
LAM = Fr(3, 8); n = 3
WORDS = {'3C': 'ABC', '2H': 'AB', '4H': 'ABCB', '6H': 'ABCACB', '9R': 'ABACACBCB'}
def faces_of(X):
    h = ConvexHull(X); fs = {}
    for eq, s in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 7)), set()).update(s)
    return [sorted(v) for v in fs.values()]
out = {}
for name, w in WORDS.items():
    L_n = len(w); Lm = np.array([cart((n, 0, 0)), cart((0, n, 0)), cart((0, 0, L_n))]).T; Li = np.linalg.inv(Lm)
    def wrap(x): f = Li @ x; f -= np.floor(f + 1e-7); return Lm @ f
    pieces = []; types = T.types(w)
    for L in range(L_n):
        os.chdir(HEX); pcs, _ = T.tile(w, L, LAM); os.chdir(here)
        ball = cart((*POS[w[L]], L))
        for k, up, s_, P, J in pcs:
            X0 = np.unique(np.round(np.array([cart(p) for p in P]), 12), axis=0) + ball
            for i, j in itertools.product(range(n), repeat=2):
                pieces.append({'X': X0 + cart((i, j, 0)), 'layer': L, 'type': types[L], 'kind': 'Narcissus' if len(X0) == 10 else ('cube' if len(X0) == 8 else f'{len(X0)}-corner'),
                               'zrel': [round(float(X0[:, 2].min() - ball[2])/H, 4), round(float(X0[:, 2].max() - ball[2])/H, 4)]})
    vol_box = abs(np.linalg.det(Lm)); vol = sum(ConvexHull(p['X']).volume for p in pieces)
    imgs = [Lm @ np.array(t) for t in itertools.product((-1, 0, 1), repeat=3)]
    S = (Lm @ np.random.default_rng(7).random((3, 20000))).T; cnt = np.zeros(len(S), int)
    for p in pieces:
        D = Delaunay(p['X'])
        for sh in imgs: cnt += D.find_simplex(S - sh) >= 0
    # faces: canonical key = sorted wrapped corners of the face, translated so its first wrapped corner is fixed
    fkey = collections.defaultdict(list)
    for pi, p in enumerate(pieces):
        for f in faces_of(p['X']):
            V = p['X'][f]; c = wrap(V.mean(0)); key = (tuple(np.round(c, 5)), tuple(sorted(map(tuple, np.round(V - V.mean(0), 5)))))
            fkey[key].append((pi, len(f)))
    mult = collections.Counter(len(v) for v in fkey.values())
    census = collections.Counter()
    for key, v in fkey.items():
        if len(v) == 2:
            (a, na), (b, nb) = v; pa, pb = pieces[a], pieces[b]
            shape = {3: 'triangle', 4: 'square', 6: 'hexagon'}.get(na, f'{na}-gon')
            where = 'same layer' if pa['layer'] == pb['layer'] else 'next layer'
            census[f"{shape}: {'+'.join(sorted((pa['kind'], pb['kind'])))} ({where})"] += 1
    kinds = collections.Counter((p['type'], p['kind'], tuple(p['zrel'])) for p in pieces)
    out[name] = {'word': w, 'types': ''.join(types), 'pieces': len(pieces), 'volume_ok': bool(abs(vol - vol_box) < 1e-9),
                 'coverage': {int(k): int(v) for k, v in zip(*np.unique(cnt, return_counts=True))},
                 'faces_by_multiplicity': dict(mult), 'face_to_face': bool(set(mult) == {2}),
                 'contacts': dict(sorted(census.items())), 'pieces_by_layer_type': {f'{t} layer: {k}, z from {z[0]} to {z[1]} layers about its ball': c for (t, k, z), c in kinds.items()}}
    print(name, json.dumps(out[name], indent=1), flush=True)
json.dump(out, open('tiling.json', 'w'), indent=1)
print('FINAL', 'OK' if all(o['volume_ok'] and o['face_to_face'] and list(o['coverage']) == [1] for o in out.values()) else 'CHECK')
