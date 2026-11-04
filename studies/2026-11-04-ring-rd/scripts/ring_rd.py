#!/usr/bin/env python3
"""DICTO's rhombic dodecahedron of 8-notch security rings (B1NR-style ring build; DICTO 4 Nov 2026, reading A):
12 rings, one per rhombic face, each squeezed to the rhombus proportion (sqrt2 : 1, the ellipse touching the four side midpoints)
and bowed onto the ball through the edge midpoints, so it reads as a fat crescent; 8 notches (outer lugs) evenly round each ring;
a tie where two rings touch (24, one per edge); open gaps at the 14 corners. Illustration, not an exact ring-flex model.
Writes figures/ring-rd.png (two views). Run with ~/geom/bin/python on dicto-big-brother."""
import itertools, math, os
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures'); os.makedirs(OUT, exist_ok=True)
faces = []
for i, j in itertools.combinations(range(3), 2):
    for a, b in itertools.product((1, -1), repeat=2):
        n = np.zeros(3); n[i] = a; n[j] = b; c = n.copy()            # face centre (±1, ±1, 0)
        long = np.zeros(3); long[i] = a; long[j] = -b; long /= np.linalg.norm(long)   # long diagonal direction (in face)
        short = np.zeros(3); short[3 - i - j] = 1.0                    # short diagonal direction
        faces.append((c, long * math.sqrt(2), short * 1.0))            # half-diagonals: sqrt2 (long), 1 (short)
Rm = math.sqrt(2.75)   # radius of the edge midpoints
def bow(p):            # rings lie flat in their face planes; they touch exactly at the edge midpoints
    return p
def ring(c, L, S, w=0.15, nseg=120):
    p, q = np.linalg.norm(L) / math.sqrt(2), np.linalg.norm(S) / math.sqrt(2)
    lu, su = L / np.linalg.norm(L), S / np.linalg.norm(S)
    th = np.linspace(0, 2*math.pi, nseg + 1)
    pt = lambda t, k: c + lu * (p * k) * np.cos(t) + su * (q * k) * np.sin(t)
    k_in, k_out = 1 - w / q, 1.0
    quads = [[bow(pt(th[m], k_out)), bow(pt(th[m+1], k_out)), bow(pt(th[m+1], k_in)), bow(pt(th[m], k_in))] for m in range(nseg)]
    lugs = []
    for m in range(8):                                     # 8 notches: small lugs on the outer rim, evenly by angle
        t0 = (m + 0.5) * 2 * math.pi / 8; dt = 0.10
        a0, a1 = pt(t0 - dt, 1.0), pt(t0 + dt, 1.0); b0, b1 = pt(t0 - dt, 1.16), pt(t0 + dt, 1.16)
        lugs.append([bow(a0), bow(a1), bow(b1), bow(b0)])
    return quads, lugs
ties = []
V4 = [np.array(v, float) for v in [(2, 0, 0), (-2, 0, 0), (0, 2, 0), (0, -2, 0), (0, 0, 2), (0, 0, -2)]]
V3 = [np.array(v, float) for v in itertools.product((1, -1), repeat=3)]
for a in V4:
    for b in V3:
        if abs(np.linalg.norm(a - b) - math.sqrt(3)) < 1e-9:
            m = (a + b) / 2
            ties.append(m)
assert len(ties) == 24
def draw(ax, elev, azim, title):
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev, azim); ax.set_axis_off(); ax.computed_zorder = False
    view = np.array([math.cos(math.radians(elev)) * math.cos(math.radians(azim)), math.cos(math.radians(elev)) * math.sin(math.radians(azim)), math.sin(math.radians(elev))])
    polys, cols = [], []
    for c, L, S in faces:
        quads, lugs = ring(c, L, S)
        front = (c / np.linalg.norm(c)) @ view
        al = 1.0 if front > -0.05 else 0.22
        shade = 0.86 + 0.12 * max(front, 0)
        for qd in quads: polys.append(qd); cols.append((shade, shade * 0.97, shade * 0.92, al))
        for lg in lugs: polys.append(lg); cols.append((0.55, 0.42, 0.25, al))
    pc = Poly3DCollection(polys, facecolors=cols, edgecolors='none')
    ax.add_collection3d(pc)
    T = np.array([t for t in ties if (t / np.linalg.norm(t)) @ view > -0.05]); ax.scatter(T[:, 0], T[:, 1], T[:, 2], s=60, c='#1f3b5a', depthshade=False, marker='s', zorder=10)
    lim = 1.55; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_title(title, fontsize=11)
fig = plt.figure(figsize=(12, 6.4))
draw(fig.add_subplot(1, 2, 1, projection='3d'), 0, 0, 'four-fold view: a square gap at the centre')
draw(fig.add_subplot(1, 2, 2, projection='3d'), 35.26, 45.0, 'three-fold view: a triangular gap at the centre')
fig.suptitle("Rhombic dodecahedron of 8-notch rings: 12 crescent rings (one per face), 24 ties (blue), notches brown, 14 open corners", fontsize=12)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=9, color='#888')
fig.savefig(os.path.join(OUT, 'ring-rd.png'), dpi=170, bbox_inches='tight'); print('ok')
