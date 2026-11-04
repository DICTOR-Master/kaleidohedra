#!/usr/bin/env python3
"""Interlocking of the HexOct tiles (#75; DICTO 4 Nov: "run the interlocking check on the HexOct tiles"). c-tile (ABC, layer 1) and h-tile (AB, layer 0) at λ = 1/10, exact
from studies/2026-10-29-hexoct-cover/scripts/tiles.py; each tile = rigid union of its 4 convex pieces. One layer (a plate between z = ±1/2 layer) repeated over the
triangular lattice; inner tiles tested against slides and twists (interlock_rot.py), outer ring fixed. Also a plate of TWO layers (c over h)."""
import os, sys, math, json, itertools
import numpy as np
from fractions import Fraction as Fr
HEX = os.path.expanduser('~/kres-tmp/hexoct-scripts'); sys.path.insert(0, HEX); os.chdir(HEX)
import tiles as T
here = os.path.expanduser('~/kres-tmp/2026-11-04-hopf-interlock')
src = open(os.path.join(here, 'interlock_rot.py')).read()
g = {'__file__': os.path.join(here, 'interlock_rot.py')}; exec(src.split("# calibration: Dyskin tetrahedra")[0], g)
H = math.sqrt(2/3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*math.sqrt(3)/2, float(p[2])*H])
def tile_parts(word, L, lam):
    pieces, tz = T.tile(word, L, lam)
    return [np.unique(np.round(np.array([cart(p) for p in P]), 10), axis=0) for k, up, s, P, J in pieces]
def plate(parts_by_layer, R=3):
    bodies, kinds = [], []
    for zoff, kind, parts in parts_by_layer:
        for u in range(-R, R + 1):
            for v in range(-R, R + 1):
                sh = np.array([u + v/2, v*math.sqrt(3)/2, zoff*H]); bodies.append([p + sh for p in parts]); kinds.append(kind)
    return bodies, kinds
lam = Fr(1, 10)
C = tile_parts('ABC', 1, lam); Hh = tile_parts('AB', 0, lam)
print('c-tile parts', len(C), 'h-tile parts', len(Hh))
R = {}
for name, layers in (('c-tile plate', [(0, 'c-tile', C)]), ('h-tile plate', [(0, 'h-tile', Hh)])):
    bodies, kinds = plate(layers)
    cent = np.array([np.mean(np.vstack(b), 0) for b in bodies]); c0 = cent.mean(0)
    ids = [i for i, cc in enumerate(cent) if np.linalg.norm((cc - c0)[:2]) < 1.6]
    R[name] = g['run'](name, bodies, ids, kinds)
json.dump(R, open(os.path.join(here, 'interlock-hexoct.json'), 'w'), indent=1)
