# Star Cores book: the sharpest dihedral angle of D106-D109 (the number that decides growth by the valley law, Chapter 5).
# Usage: dihedral_new4.py <dataset-v7 dir> <star-cores scripts dir>
import sys, math, numpy as np
DS, SCR = sys.argv[1:3]; sys.argv = [sys.argv[0], DS, '/tmp']; sys.path.insert(0, SCR)
from star_core import faces_info, load
for D, fn in (('D106', 'dicto-cube-pearl'), ('D107', 'dicto-golden-clasp'), ('D108', 'dicto-hamlet'), ('D109', 'dicto-ophelia')):
    d, V, F = load('solids/' + fn + '.json'); V = V - V.mean(0); FI = faces_info(V, F); E = {}
    for i, (f, n, c) in enumerate(FI):
        for k in range(len(f)): E.setdefault(tuple(sorted((f[k], f[(k + 1) % len(f)]))), []).append(n)
    ang = sorted({round(180 - math.degrees(math.acos(np.clip(a @ b, -1, 1))), 3) for a, b in E.values()})
    print(D, fn, 'edges', len(E), 'dihedral kinds', len(ang), 'min', ang[0], 'max', ang[-1])
