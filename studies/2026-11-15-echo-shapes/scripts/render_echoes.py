#!/usr/bin/env python3
"""Figures for the echo-shapes study (render standard: solid shaded faces, crisp edges, see-through shells for nested sets, DICTO mark).
Panel set 1 (echoes-solids.png): one combinatorial type met three ways, and the chiral Goldberg echo:
  (a) icosahedral Goldberg GP(2,1) (polar of the geodesic points; 12 pentagons violet, 60 hexagons gold; chiral)
  (b) octahedral Goldberg GP(2,0) (polar; 6 squares, 12 hexagons; every dihedral angle 120 or 135 degrees, Dehn invariant 0)
  (c) the zonohedron of the cube's 3 + 4 axes (C4 + C3): the same 6 + 12 face type, grown by whole zones
Panel set 2 (echoes-shadows.png): shadows and sections
  (d) the 600-cell cut through its centre across a vertex axis: 30 corners of an icosidodecahedron + 12 edge midpoints = 80 triangles
      (the geodesic (2,0) type)
  (e) the S5 orbits C1 + C2 (40 corners) along the S4 axis: Oh image, cube + 24-corner shell + cube
  (f) the S5 orbit C1 of the 600-cell (20 corners) seen along the S4 axis: tetrahedron + truncated tetrahedron + tetrahedron
Usage: render_echoes.py figdir"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); FIG = sys.argv[1]
sys.argv = [sys.argv[0], '/dev/null']
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-13-paradigm-expansion', 'scripts'))
import numpy as np
import figlib as F
import matplotlib.pyplot as plt
from echo_lib import *
import gc_echoes as GC
import shadow_echoes as SH
import zono_growth as ZG

def polar_of(points):
    U = np.array([to_np(p) for p in points]); U = U/np.linalg.norm(U, axis=1)[:, None]
    H = hull3(U); V = []
    for n, d in zip(H['normals'], H['offsets']): V.append(n/d)
    return np.array(V)

def draw_solid(ax, P, title, colfn=None, az=28, el=20, glass_extra=()):
    R = F.rot(az, el); sc = F.Scene(R, byobject=True)
    P = np.asarray(P, float); P = P - P.mean(0)
    faces = F.hull_faces(P)
    cols = [colfn(len(f)) if colfn else F.GOLD for f, n in faces]
    for Q, col, lw in glass_extra: sc.solid(Q, color=col, glass=True, alpha=0.18, lw=lw, shell=True, z=1)
    sc.solid(P, faces=faces, facecolors=cols, lw=1.1)
    sc.draw(ax); F.blank(ax); ax.autoscale_view(); ax.set_title(title, fontsize=9.5)

def main():
    os.makedirs(FIG, exist_ok=True)
    # (a)
    pts, grp, T = GC.geodesic_points('icosahedron', 2, 1); A = polar_of(pts)
    # (b)
    pts2, _, _ = GC.geodesic_points('octahedron', 2, 0); B = polar_of(pts2)
    # (c)
    G = ZG.C4 + ZG.C3; Cv = np.array([to_np(p) for p in ZG.vertices(G)])
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.8))
    draw_solid(axs[0], A, 'Goldberg GP(2,1), icosahedral, chiral\n12 pentagons + 60 hexagons (T = 7)',
               colfn=lambda n: F.VIOLET if n == 5 else F.GOLD)
    draw_solid(axs[1], B, 'Goldberg GP(2,0), octahedral\n6 squares + 12 hexagons; Dehn invariant 0',
               colfn=lambda n: F.ELEM['I'] if n == 4 else F.GOLD)
    draw_solid(axs[2], Cv, 'grown: zones of the cube (3) + rhombic dodecahedron (4)\nthe same 6 + 12 face type, Dehn invariant 0',
               colfn=lambda n: F.ELEM['I'] if n == 4 else F.ELEM['C'])
    F.mark(fig); fig.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.07, wspace=0.04)
    fig.savefig(os.path.join(FIG, 'echoes-solids.png'), dpi=180, facecolor='white'); plt.close(fig)

    # shadows
    S600 = SH.cell600(); E = SH.edges4(S600)
    d = (Q5(1), Q5(0), Q5(0), Q5(0))
    sec = []
    s = [dot(x, d) for x in S600]
    for i, x in enumerate(S600):
        if s[i].iszero(): sec.append(x)
    for i, j in E:
        if s[i].sign()*s[j].sign() < 0:
            t = s[i]/(s[i] - s[j]); sec.append(tuple(a + t*(b - a) for a, b in zip(S600[i], S600[j])))
    sec = uniq(sec); D = np.array([[float(x) for x in p[1:]] for p in sec])
    r = np.linalg.norm(D, axis=1)
    # (e) cell-first: centre of one tetrahedral cell
    cents = SH.hull4_dirs(S600); c = cents[0]
    Pts, X = SH.image(S600, c)
    shells = {}
    for p, x in zip(Pts, X): shells.setdefault(round(float(np.linalg.norm(x)), 6), []).append(x)
    keys = sorted(shells)
    # (f) S5 orbit C1 along the S4 axis
    orb, _ = SH.s5_orbits()
    def cen(v): m = sum(v, Q5())/5; return tuple(x - m for x in v)
    axis = cen((Q5(0), Q5(0), Q5(0), Q5(0), Q5(1))); one = tuple(Q5(1) for _ in range(5))
    P1, X1 = SH.image(orb['C1'], axis, one)
    sh1 = {}
    for x in X1: sh1.setdefault(round(float(np.linalg.norm(x)), 6), []).append(x)
    k1 = sorted(sh1)
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.8))
    draw_solid(axs[0], D, '600-cell cut through its centre, across a vertex axis\n30 corners + 12 edge midpoints: 80 triangles',
               colfn=lambda n: F.VIOLET)
    # mark the 12 raised midpoints
    R = F.rot(28, 20); Dc = D - D.mean(0)
    for p, rr in zip(Dc, r):
        if rr < 0.99:
            q = R @ p
            if q[2] > 0: axs[0].scatter([q[0]], [q[1]], s=14, color=F.GOLD, zorder=200, edgecolors=F.INK, linewidths=0.6)
    P2_, X2 = SH.image(orb['C1'] + orb['C2'], axis, one)
    sh2 = {}
    for x in X2: sh2.setdefault(round(float(np.linalg.norm(x)), 6), []).append(x)
    k2 = sorted(sh2); mid = [np.array(sh2[k]) for k in k2 if len(sh2[k]) == 24][0]
    cubes = [np.array(sh2[k]) for k in k2 if len(sh2[k]) == 8]
    draw_solid(axs[1], mid, 'S5 orbits C1 + C2 (40 corners) along the S4 axis:\nOh shadow, cube + 24-corner shell + cube',
               colfn=lambda n: F.GOLD if n == 4 else F.VIOLET,
               glass_extra=[(Q, col, 0.8) for Q, col in zip(cubes, (F.ELEM['I'], F.ELEM['T']))])
    tt = np.array(sh1[k1[1]]) if len(sh1[k1[1]]) == 12 else np.array(sh1[k1[0]])
    tets = [np.array(sh1[k]) for k in k1 if len(sh1[k]) == 4]
    draw_solid(axs[2], tt, 'S5 orbit C1 of the 600-cell (20 corners) along the S4 axis:\ntetrahedron + truncated tetrahedron + tetrahedron',
               colfn=lambda n: F.GOLD if n == 6 else F.VIOLET,
               glass_extra=[(Q, col, 0.8) for Q, col in zip(tets, (F.ELEM['T'], F.ELEM['I']))])
    F.mark(fig); fig.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.07, wspace=0.04)
    fig.savefig(os.path.join(FIG, 'echoes-shadows.png'), dpi=180, facecolor='white'); plt.close(fig)
    print('wrote', FIG); print('FINAL ok')

main()
