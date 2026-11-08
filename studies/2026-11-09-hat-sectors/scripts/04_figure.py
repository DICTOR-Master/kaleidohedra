# Task 4: one RD hat piece (c-layer relief): top view over the hexagon/kite grid, and 3D views (as placed, turned over).
import sys, os
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from hatgrid import *
import importlib
sat = importlib.import_module('02_orientation_sat')
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = np.sqrt(6) / 6          # lattice units -> RD units (hexagon circumradius 2 -> sqrt6/3)
HU = np.sqrt(3) / 12        # height unit
def xy(p): return np.array([p[0] + p[1] / 2, p[1] * np.sqrt(3) / 2]) * S
REL = {'C': (6, -6), 'M': (3, -3), 0: (4, -2), 1: (2, -4)}   # c-layer: class0 tip high on top, class1 deep below

t, hk = kites_of_hat()
fig = plt.figure(figsize=(15, 5.6))
ax = fig.add_subplot(1, 3, 1)
hexes = {c for c, k in hk}
cs = [centre(i, j) for i in range(-6, 3) for j in range(-5, 3)]
for c in cs:
    for k in range(6):
        P = np.array([xy(p) for p in kite(c, k)])
        inhat = (c, k) in hk
        col = ('#d9a441' if k % 2 == 0 else '#4f7fbf') if inhat else 'none'
        ax.fill(P[:, 0], P[:, 1], facecolor=col, edgecolor='#bbbbbb', lw=0.5, alpha=0.9 if inhat else 1)
    H6 = np.array([xy(add(c, rot((2, 0), k))) for k in range(7)])
    ax.plot(H6[:, 0], H6[:, 1], color='#555555', lw=1.0)
Hp = np.array([xy(add(p, t)) for p in HAT + [HAT[0]]])
ax.plot(Hp[:, 0], Hp[:, 1], color='black', lw=2.2)
for c, k in hk:
    v = xy(kite(c, k)[2]); ax.plot(*v, 'o', ms=4, color='#d9a441' if k % 2 == 0 else '#4f7fbf', mec='k', mew=0.5)
cen = np.array([xy(c) for c in hexes]).mean(0)
ax.set_xlim(cen[0] - 1.9, cen[0] + 1.9); ax.set_ylim(cen[1] - 1.9, cen[1] + 1.9); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Top view: hat = 8 kites of 3 RD cells (hexagons)\ngold kite: tip high on top (octahedral hole above)\nblue kite: tip deep below', fontsize=9)

def sector_faces(c, k, flip=False):
    C, M1, V, M2 = kite(c, k)
    def P3(p, h): q = xy(p); return [q[0], q[1], (-h if flip else h) * HU]
    tv, bv = REL[k % 2]
    T = {'C': P3(C, 6), 'M1': P3(M1, 3), 'V': P3(V, tv), 'M2': P3(M2, 3)}
    B = {'C': P3(C, -6), 'M1': P3(M1, -3), 'V': P3(V, bv), 'M2': P3(M2, -3)}
    tops = [[T['C'], T['M1'], T['V']], [T['C'], T['V'], T['M2']]]
    bots = [[B['C'], B['M1'], B['V']], [B['C'], B['V'], B['M2']]]
    walls = []
    edges = [('C', 'M1'), ('M1', 'V'), ('V', 'M2'), ('M2', 'C')]
    pts = {'C': C, 'M1': M1, 'V': V, 'M2': M2}
    for a, b in edges:
        walls.append(((pts[a], pts[b]), [T[a], T[b], B[b], B[a]]))
    return tops, bots, walls

def draw_piece(ax, flip, title):
    from collections import Counter
    seg = Counter()
    allw = []
    for c, k in hk:
        tops, bots, walls = sector_faces(c, k, flip)
        ax.add_collection3d(Poly3DCollection(tops, facecolor='#d9a441' if (k % 2 == 0) != flip else '#4f7fbf', edgecolor='#333333', lw=0.4, alpha=0.95))
        ax.add_collection3d(Poly3DCollection(bots, facecolor='#999999', edgecolor='#333333', lw=0.3, alpha=0.5))
        for (a, b), q in walls:
            key = tuple(sorted([a, b])); seg[key] += 1; allw.append((key, q))
    outer = [q for key, q in allw if seg[key] == 1]     # walls on the hat boundary only
    ax.add_collection3d(Poly3DCollection(outer, facecolor='#e8e2d4', edgecolor='#333333', lw=0.4, alpha=0.55))
    pts = np.array([p for q in outer for p in q])
    mid = (pts.max(0) + pts.min(0)) / 2; r = (pts.max(0) - pts.min(0)).max() / 2
    ax.set_xlim(mid[0] - r, mid[0] + r); ax.set_ylim(mid[1] - r, mid[1] + r); ax.set_zlim(mid[2] - r, mid[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=28, azim=-62); ax.axis('off')
    ax.set_title(title, fontsize=9)

draw_piece(fig.add_subplot(1, 3, 2, projection='3d'), False,
           'RD hat piece in a c-layer (8 RD sectors, vertical walls,\nslanted top and bottom); stacking axis [111] up')
draw_piece(fig.add_subplot(1, 3, 3, projection='3d'), True,
           'Same piece turned over: fits the reflected hats in\ncentre-midpoint mirror lines; the 60-degree turned hats\nneed the mirror image (SAT: no layer patch without it)')
mark = os.path.join(HERE, 'figures', 'dicto-mark.png')
if os.path.exists(mark):
    im = plt.imread(mark); fax = fig.add_axes([0.905, 0.02, 0.08, 0.13]); fax.imshow(im); fax.axis('off')
fig.suptitle('Hat sectors on the rhombic dodecahedron layer (study 2026-11-09)', fontsize=11)
out = os.path.join(HERE, 'figures', 'hat-piece-rd.png')
fig.savefig(out, dpi=150, bbox_inches='tight')
print('wrote', out)
print('FINAL ok' if os.path.getsize(out) > 20000 and len(hk) == 8 else 'FINAL FAIL: figure')
