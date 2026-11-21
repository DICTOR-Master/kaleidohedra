# DICTO · dictospheres.com — the DICTO Ogdoecontahedron (OG, #31) beside the Fullerene Star on their shared 80 planes: the 20 hexagon planes of the
# truncated icosahedron (edge 1) and the 60 triangle planes of a pentakis dodecahedron. OG = polar of the truncated icosahedron in its midsphere (planes
# v.x <= r_mid^2, v the 60 corners) cut at the 20 hexagon planes; Fullerene Star = scenes.py's C1. Same frame, same viewpoint (renders/og.html: p0 OG, p1 Fullerene Star).
# Checks (printed, then FINAL ok, in floats; the exact check is studies/2026-11-21-fullerene-star-og): OG 102 corners, 60 kites + 20 hexagons, convex;
# Fullerene Star 72 corners, 60 triangles + 20 hexagons; the hexagon planes of the two are the same.
import os, sys, itertools
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0], os.path.join(H, 'data', 'resin.json')]
import scenes as S
from render3d import write, solid_part
TV, hexes = S.TV, S.hexes
E1 = [(i, j) for i in range(60) for j in range(i + 1, 60) if abs(np.linalg.norm(TV[i] - TV[j]) - 1) < 1e-9]; assert len(E1) == 90
rm2 = float(np.dot((TV[E1[0][0]] + TV[E1[0][1]]) / 2, (TV[E1[0][0]] + TV[E1[0][1]]) / 2))
assert all(abs(np.dot((TV[i] + TV[j]) / 2, (TV[i] + TV[j]) / 2) - rm2) < 1e-9 for i, j in E1)
planes = [(v / 1.0, rm2) for v in TV] + [(n * 1.0, d) for n, d, o in hexes]
A = np.array([p[0] for p in planes]); B = np.array([p[1] for p in planes]); found = []
for i, j, k in itertools.combinations(range(80), 3):
    M = A[[i, j, k]]
    if abs(np.linalg.det(M)) < 1e-9: continue
    x = np.linalg.solve(M, B[[i, j, k]])
    # hexagon-plane normals are unit; kite normals are the corners (scaled): compare on the plane values directly
    if np.all(A @ x <= B + 1e-7) and not any(np.linalg.norm(x - y) < 1e-6 for y in found): found.append(x)
OG = S.hull(np.array(found))
sz = sorted(len(o) for n, d, o in OG.F)
LOG = [f'OG: {len(OG.V)} corners, {sz.count(4)} kites + {sz.count(6)} hexagons, {len(OG.E)} edges']
assert len(OG.V) == 102 and sz.count(4) == 60 and sz.count(6) == 20 and len(OG.E) == 180
fs = S.C1; fsz = sorted(len(o) for n, d, o in fs.F)
assert len(fs.V) == 72 and fsz.count(3) == 60 and fsz.count(6) == 20 and len(fs.E) == 150
hpl = lambda Sx: sorted(tuple(np.round(np.append(n, d), 6)) for n, d, o in Sx.F if len(o) == 6)
assert hpl(OG) == hpl(fs), 'hexagon planes differ'
LOG.append('Fullerene Star: 72 corners, 60 triangles + 20 hexagons, 150 edges; the 20 hexagon planes of the two solids coincide')
SAND = '#d6b46a'
DIR = np.array([0.36, 0.30, 1.0])
po = [solid_part(OG, [S.PEARL if len(o) == 6 else SAND for n, d, o in OG.F], rad=0.0036, edge_col=S.EDGE)]
pf = [S.c1_whole(0.0036)]
E = max(S.ext(po, DIR), S.ext(pf, DIR))
write(os.path.join(S.OUT, 'og.html'), [{'E': E, 'dir': DIR.tolist(), 'parts': po}, {'E': E, 'dir': DIR.tolist(), 'parts': pf}])
LOG.append('og.html: p0 OG, p1 Fullerene Star, same viewpoint and scale')
open(os.path.join(H, 'scenes5.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
