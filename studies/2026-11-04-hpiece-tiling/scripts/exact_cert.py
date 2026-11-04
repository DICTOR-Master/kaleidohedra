#!/usr/bin/env python3
"""Exact certificate for a periodic tiling found by any_tile.py. Lattice coordinates (u, v, z): x = u + v/2, y = v√3/2, z_cart = z√(2/3); every corner
snapped to a fraction (denominator <= 72, checked). Certificate: (1) every face of every piece, mod the box, is the exact corner set of a face of
another piece (face-to-face), (2) Σ volumes = box volume exactly (volume ratios are affine-invariant: computed in lattice coordinates). (1) gives a
covering of constant multiplicity; (2) makes it 1. Usage: exact_cert.py <piece> <n>"""
import sys, math, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
name, n = sys.argv[1], int(sys.argv[2])
ch = np.load(f'data/solution-{name}-n{n}.npy'); s3 = math.sqrt(3); Hh = math.sqrt(2/3)
def lat(p):
    u, v, z = p[0] - p[1]/s3, 2*p[1]/s3, p[2]/Hh; out = []
    for x in (u, v, z):
        f = Fr(x).limit_denominator(72); assert abs(float(f) - x) < 1e-7, x; out.append(f)
    return out
BOX = (Fr(n), Fr(n), Fr(6))
def wrapf(p): return tuple(x - (x // b)*b for x, b in zip(p, BOX))
def det3(a, b, c): return a[0]*(b[1]*c[2] - b[2]*c[1]) - a[1]*(b[0]*c[2] - b[2]*c[0]) + a[2]*(b[0]*c[1] - b[1]*c[0])
pieces = []; facekeys = {}; total = Fr(0)
for pi, P in enumerate(ch):
    L = [lat(p) for p in P]; h = ConvexHull(P); fs = {}
    for eq, sm in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 7)), set()).update(int(i) for i in sm)
    c = [sum(x[i] for x in L)/len(L) for i in range(3)]
    vol = Fr(0)
    for sm in h.simplices:
        a, b, d = (L[i] for i in sm); vol += abs(det3([a[k] - c[k] for k in range(3)], [b[k] - c[k] for k in range(3)], [d[k] - c[k] for k in range(3)]))/6
    total += vol
    for f in fs.values():
        pts = [L[i] for i in f]; base = min(pts)   # face identified by its corner set up to a box translation
        shift = [b_ - (b_ // B)*B - b_ for b_, B in zip(base, BOX)]
        key = frozenset(tuple(p[k] + shift[k] for k in range(3)) for p in pts)
        facekeys.setdefault(key, []).append(pi)
boxvol = BOX[0]*BOX[1]*BOX[2]
unmatched = [k for k, v in facekeys.items() if len(v) != 2]
print(f'{name} n={n}: pieces {len(ch)}, faces {len(facekeys)}, faces not shared by exactly two pieces: {len(unmatched)}, '
      f'Σ volume / box volume = {total/boxvol} (lattice units)', flush=True)
print('EXACT CERTIFICATE:', 'YES — a face-to-face tiling' if not unmatched and total == boxvol else 'NO (see counts)')
