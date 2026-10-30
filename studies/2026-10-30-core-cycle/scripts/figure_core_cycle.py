# Figure for #78 v2, Proposition 5 (golden version): TI with its spikes; the core C (the icosahedron truncated at 1/phi^3) with its own
# spikes; the core of C's turn, a uniform TI again. Each scaled to the same radius; body gold, spikes violet; DICTO mark.
import json, sys, numpy as np
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull, HalfspaceIntersection
GOLD, VIOLET, BG, PALE = '#d4af37', '#8e5bd6', '#0d0d12', '#e8e2cc'
phi = (1 + 5 ** .5) / 2; t = phi
raw = json.load(open(sys.argv[1])); out = sys.argv[2]
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def facelist(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; o = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in o: o[k] = (eq, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    return V, list(o.values())
def pl(Q):
    u = {}
    for eq in ConvexHull(Q).equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
def core_of(Q):
    V, F = facelist(Q); tips = [t * (-eq[3]) * eq[:3] for eq, _ in F]
    pen = np.array([tp for tp, (_, ids) in zip(tips, F) if len(ids) == 5]); hexa = np.array([tp for tp, (_, ids) in zip(tips, F) if len(ids) == 6])
    W = HalfspaceIntersection(np.vstack([pl(pen), pl(hexa)]), np.zeros(3)).intersections; return W[ConvexHull(W).vertices]
C = core_of(P); P2 = core_of(C)
L = np.array([-0.4, 0.5, 0.8]); L /= np.linalg.norm(L)
def order(V, ids, n):
    c = V[ids].mean(0); u = V[ids[0]] - c; w = np.cross(n, u); return [i for _, i in sorted((np.arctan2((V[i] - c) @ w, (V[i] - c) @ u), i) for i in ids)]
def shade(col, n): return np.clip(np.array(mc.to_rgb(col)) * (0.35 + 0.65 * max(0, n @ L)), 0, 1)
TEAL = '#2bb3a3'
panels = [(P, 'TI'), (C, 'its core\n(icosahedron truncated at 1/φ³)'), (P2, 'the core of the core\'s turn:\nTI again')]
fig = plt.figure(figsize=(12, 4.4), facecolor=BG)
for k, (Q, name) in enumerate(panels):
    V, F = facelist(Q); V = V / np.linalg.norm(V, axis=1).max()
    ax = fig.add_subplot(1, 3, k + 1, projection='3d'); polys, cols = [], []
    for eq, ids in F:
        n = eq[:3]; polys.append(V[order(V, ids, n)]); cols.append(shade(GOLD if len(ids) == 5 else TEAL, n))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors=(0, 0, 0, 0.6), linewidths=0.5))
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim): f(-0.72, 0.72)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(18, 32); ax.axis('off'); ax.set_facecolor(BG)
    ax.set_title(name, color=PALE, fontsize=10, pad=-4)
for x in (0.333, 0.667): fig.text(x, 0.5, '→', color=PALE, ha='center', va='center', fontsize=26)
fig.text(0.5, 0.03, 'Pentagons gold, hexagons teal. Each turn swaps the distances of the two kinds of face plane, so the cores alternate: period two (each drawn at the same radius)', color=PALE, ha='center', fontsize=8.5)
fig.text(0.985, 0.03, 'DICTO', color=GOLD, ha='right', fontsize=9, fontweight='bold')
plt.subplots_adjust(0, 0.08, 1, 0.88, 0.02, 0); plt.savefig(out, dpi=180, facecolor=BG)
