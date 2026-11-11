#!/usr/bin/env python3
"""DICTO's ring cell for the TRD (trapezo-rhombic dodecahedron), the RD's twin on twisted (h) layers, next to the RD ring cell.
Ring = one per FACE (12: 6 rhombi, 6 trapezoids); tie = one per EDGE MIDPOINT (24); open gap = at each CORNER (14).
Each ring is drawn flat in its face through the 4 edge midpoints (ellipse with the Varignon half-diagonals as conjugate radii), 8 notches.
Cells from the hcp / fcc neighbour shells (the Voronoi cell = planes halfway to the 12 neighbours). Axis vertical (c-axis / three-fold axis).
Run on compute-host with python3. Writes figures/trd-ring.png and prints the corner degrees."""
import itertools, math, os
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import HalfspaceIntersection, ConvexHull
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
def shell(kind):
    P = [(math.cos(k*math.pi/3), math.sin(k*math.pi/3), 0.0) for k in range(6)]
    e = math.atan(math.sqrt(2))
    for k in range(3):
        a = math.pi/6 + k*2*math.pi/3; P.append((math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)))
        a2 = a if kind == 'h' else a + math.pi/3          # h: directly below (mirror); c: turned 60 deg
        P.append((math.cos(e)*math.cos(a2), math.cos(e)*math.sin(a2), -math.sin(e)))
    return np.array(P)
def cell(kind):
    N = shell(kind); H = np.array([[*n, -0.5] for n in N])
    V = np.unique(np.round(HalfspaceIntersection(H, np.zeros(3)).intersections, 10), axis=0)
    faces = []
    for n in N:
        F = [v for v in V if abs(v @ n - 0.5) < 1e-8]; c = np.mean(F, 0); u = F[0] - c; w = np.cross(n, u)
        F.sort(key=lambda p: math.atan2((p - c) @ w, (p - c) @ u)); faces.append((n, np.array(F)))
    deg = {}
    for v in V: d = sum(1 for _, F in faces if any(np.allclose(v, f) for f in F)); deg[d] = deg.get(d, 0) + 1
    return V, faces, deg
def ring(F, n, w=0.16):
    M = [(F[i] + F[(i+1) % 4])/2 for i in range(4)]; c = np.mean(M, 0)
    u = (M[0] - M[2])/2; v = (M[1] - M[3])/2
    th = np.linspace(0, 2*math.pi, 121)
    P = lambda t, k: c + k*(u*math.cos(t) + v*math.sin(t))
    quads = [[P(th[m], 1), P(th[m+1], 1), P(th[m+1], 1-w), P(th[m], 1-w)] for m in range(120)]
    lugs = []
    for m in range(8):
        t0 = (m + 0.5)*math.pi/4; dt = 0.10
        lugs.append([P(t0-dt, 1), P(t0+dt, 1), P(t0+dt, 1.15), P(t0-dt, 1.15)])
    return quads, lugs, M
fig = plt.figure(figsize=(13, 9.5))
for row, kind in enumerate(('c', 'h')):
    V, faces, deg = cell(kind)
    print(kind, 'corners', len(V), 'corner degrees', deg, 'faces', len(faces))
    for col, (elev, azim, ttl) in enumerate([(89, -90, 'from the top'), (10, -60, 'side, axis upright')]):
        ax = fig.add_subplot(2, 2, 2*row + col + 1, projection='3d'); ax.set_axis_off(); ax.set_box_aspect((1, 1, 1)); ax.view_init(elev, azim); ax.computed_zorder = False
        view = np.array([math.cos(math.radians(elev))*math.cos(math.radians(azim)), math.cos(math.radians(elev))*math.sin(math.radians(azim)), math.sin(math.radians(elev))])
        polys, cols, ties = [], [], []
        for n, F in faces:
            q, l, M = ring(F, n); front = n @ view; al = 1.0 if front > -0.05 else 0.18
            lens = sorted(round(np.linalg.norm(F[i] - F[(i+1) % 4]), 4) for i in range(4)); trap = len(set(lens)) > 1
            base = (0.86, 0.66, 0.28) if trap else (0.95, 0.93, 0.88)
            if kind == 'c' and abs(n[2]) < 1e-9: base = (0.86, 0.66, 0.28)
            for qq in q: polys.append(qq); cols.append((*base, al))
            for ll in l: polys.append(ll); cols.append((0.45, 0.35, 0.22, al))
            ties += [m for m in M if (m/np.linalg.norm(m)) @ view > -0.05]
        ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors=[(0.3, 0.3, 0.3, 0.2*c[3]) for c in cols], linewidths=0.2))
        T = np.unique(np.round(ties, 6), axis=0); ax.scatter(T[:, 0], T[:, 1], T[:, 2], s=45, c='#1f3b5a', marker='s', depthshade=False)
        L = 0.75; ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-L, L)
        name = 'RD ring cell (straight layer): band of 6 rhombi zigzags' if kind == 'c' else 'TRD ring cell (twisted layer): band of 6 trapezoids, mirror at the waist'
        ax.set_title(f'{name}\n{ttl}', fontsize=10)
fig.suptitle('Ring cells, 12 rings each (one per face), ties (blue) at the 24 edge midpoints, 14 open corners; band rings gold', fontsize=11)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=9, color='#888')
fig.savefig(os.path.join(OUT, 'trd-ring.png'), dpi=150, bbox_inches='tight'); print('ok')
