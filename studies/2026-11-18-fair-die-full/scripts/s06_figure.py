#!/usr/bin/env python3
"""Fair 14-face die figure (render standard: solid faces, crisp edges; see-through shell and pull-apart view). DICTO · dictospheres.com
(a) the die, solid; (b) see-through shell with the 24 struts of its Vacuus (centre to corners); (c) pull-apart: the 14 centre pyramids,
each subtending 4pi/14, moved out along their face normals. Cube-family green #488e48 (as in God's Dice); one colour for the one solid.
Output figures/fair-die-full.png; FINAL line conditional on the geometry checks."""
import math, os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fdlib import corners, faces, solid_angle_face, MUF
FIG = os.path.join(HERE, '..', 'figures'); os.makedirs(FIG, exist_ok=True)
GREEN = '#488e48'; EDGE = '#1d3a1d'; INK = '#2b2b2b'; BG = '#fbfaf6'
V = corners(MUF); F, N, H = faces(V)
W = [solid_angle_face(V, f) for f in F]
ok = len(F) == 14 and max(abs(w - 4*math.pi/14) for w in W) < 1e-12
light = np.array([0.4, -0.55, 0.75]); light /= np.linalg.norm(light); base = np.array(matplotlib.colors.to_rgb(GREEN))
def shade(n): s = 0.6 + 0.4*max(0, float(n @ light)); return np.clip(base*s + (1 - s)*0.05, 0, 1)
ELEV, AZIM = 22, -58
e = np.radians(ELEV); a = np.radians(AZIM); view = np.array([math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)])
fig = plt.figure(figsize=(13.5, 4.9), facecolor=BG)
def axis(i, lim):
    ax = fig.add_subplot(1, 3, i, projection='3d', computed_zorder=False); ax.set_facecolor(BG)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim); ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=ELEV, azim=AZIM); ax.set_axis_off(); return ax
ax = axis(1, 1.15)
for f, n in sorted(zip(F, N), key=lambda t: float(np.array(t[1]) @ view)):
    ax.add_collection3d(Poly3DCollection([V[f]], facecolor=shade(np.array(n)), edgecolor=EDGE, linewidths=1.1))
ax.set_title('(a) the fair 14-face die, μ_f = 1.756582…\n6 squares, 8 hexagons: each face 1/14', fontsize=10, color=INK)
bx = axis(2, 1.15)
bx.add_collection3d(Line3DCollection([[np.zeros(3), v] for v in V], colors='#6f8f6f', linewidths=0.8))
for f, n in zip(F, N):
    bx.add_collection3d(Poly3DCollection([V[f]], facecolor=(*base, 0.10), edgecolor=EDGE, linewidths=1.0))
bx.set_title('(b) see-through shell with the Vacuus struts\n(one strut length 1.25396; 36 fins in 2 kinds)', fontsize=10, color=INK)
cx = axis(3, 1.75)
pieces = []
for f, n in zip(F, N):
    n = np.array(n); off = 0.45*n; P = V[f] + off; O = off
    tris = [[O, P[i], P[(i + 1) % len(P)]] for i in range(len(P))]
    pieces.append((float(n @ view), P, tris, n))
for d, P, tris, n in sorted(pieces, key=lambda t: t[0]):
    for t in sorted(tris, key=lambda t: float(np.mean(t, 0) @ view)):
        nn = np.cross(t[1] - t[0], t[2] - t[0]); nn /= np.linalg.norm(nn)
        cx.add_collection3d(Poly3DCollection([t], facecolor=shade(nn if nn @ (np.mean(t, 0) - t[0]*0) >= 0 else -nn), edgecolor=EDGE, linewidths=0.6))
    cx.add_collection3d(Poly3DCollection([P], facecolor=shade(n), edgecolor=EDGE, linewidths=1.0))
cx.set_title('(c) pulled apart: 14 centre pyramids,\neach subtending 4π/14 from the centre', fontsize=10, color=INK)
fig.text(0.995, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=8, color='#a08a3c')
plt.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.03, wspace=0.02)
out = os.path.join(FIG, 'fair-die-full.png'); fig.savefig(out, dpi=160, facecolor=BG)
print(f"wrote figures/fair-die-full.png; 14 faces, equal solid angles: {ok}")
print("FINAL ok" if ok and os.path.getsize(out) > 20000 else "FINAL FAIL")
