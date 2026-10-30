# Figure 1 of #80 (The Gains of DICTO's Growth Rule): two steps of T(S) = {x : v·x <= v·v} for the Platonic pairs.
# Each corner of S lies on a face of T(S), and T(T(S)) is S scaled by the gain g = (R'/R)^2 (checked below).
# Usage: ~/geom/bin/python fig_paper_c.py <out png> <logo png>   (rendering helpers as in figs_paper_a.py, render standard: solid, crisp edges)
import sys, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scipy.spatial import ConvexHull, HalfspaceIntersection
from itertools import product
OUT, LOGO = sys.argv[1:3]; phi = (1 + 5 ** .5) / 2
GOLD, VIOLET, TEAL, EDGE = '#d4af37', '#8e5bd6', '#2bb3a3', '#1d1d24'
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz
def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); k = 0.50 + 0.50 * max(0.0, float(n @ LIGHT)); return tuple(np.clip(c * k + 0.06 * (1 - k), 0, 1))
def hull_faces(Q):
    h = ConvexHull(Q); out = {}
    for eq in h.equations:
        k = tuple(np.round(eq, 6))
        if k in out: continue
        ids = [i for i, p in enumerate(Q) if abs(eq[:3] @ p + eq[3]) < 1e-7 * (1 + np.abs(Q).max())]
        R = Q[ids]; c = R.mean(0); n = eq[:3]; a = R[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        out[k] = (R[np.argsort(np.arctan2((R - c) @ b, (R - c) @ a))], n)
    return list(out.values())
def T(V):
    hs = np.hstack([V, -(V * V).sum(1, keepdims=True)])
    P = HalfspaceIntersection(hs, np.zeros(3)).intersections
    P = P[ConvexHull(P).vertices]; keep = []
    for p in P:
        if all(np.linalg.norm(p - q) > 1e-9 for q in keep): keep.append(p)
    return np.array(keep)
def solid(items, Q, col, M, layer):
    for P, n in hull_faces(Q):
        nn = M @ n
        if nn[2] <= 1e-9: continue
        W = P @ M.T; items.append((layer, W[:, 2].mean(), W[:, :2], shade(col, nn), EDGE, 0.5))
def shell(items, Q, M):
    for P, n in hull_faces(Q):
        W = P @ M.T; front = (M @ n)[2] > 0
        items.append((2 if front else 0, W[:, 2].mean(), W[:, :2], (0.62, 0.68, 0.80, 0.16 if front else 0.10),
                      (0.25, 0.28, 0.38, 0.95 if front else 0.40), 0.5 if front else 0.3))
def draw(ax, items, lim):
    items.sort(key=lambda t: (t[0], t[1]))
    ax.add_collection(PolyCollection([t[2] for t in items], facecolors=[t[3] for t in items], edgecolors=[t[4] for t in items],
                                     linewidths=[t[5] for t in items], joinstyle='round', antialiased=True))
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal'); ax.axis('off')
tet = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
cube = np.array(list(product((-1, 1), repeat=3)), float)
dod = np.vstack([cube] + [np.array([np.roll((0, s * 1 / phi, t * phi), k) for s in (-1, 1) for t in (-1, 1)]) for k in range(3)])
rows = [(tet, 'tetrahedron', 'tetrahedron', '9', 9.0),
        (cube, 'cube', 'octahedron', '3', 3.0),
        (dod, 'dodecahedron', 'icosahedron', '15 − 6√5 ≈ 1.584', 15 - 6 * 5 ** .5)]
M = rot(18, 22)
fig, axs = plt.subplots(3, 3, figsize=(8, 8.4), gridspec_kw=dict(wspace=0.03, hspace=0.22))
for r, (S, a, b, gtxt, g) in enumerate(rows):
    S1 = T(S); S2 = T(S1)
    R = np.linalg.norm(S, axis=1); R1 = np.linalg.norm(S1, axis=1)
    assert np.ptp(R) < 1e-9 and np.ptp(R1) < 1e-9, a                       # both on one sphere: the theorem applies
    assert abs((R1[0] / R[0]) ** 2 - g) < 1e-9, (a, (R1[0] / R[0]) ** 2)    # gain = (R'/R)^2
    assert all(min(np.linalg.norm(g * p - q) for q in S2) < 1e-8 for p in S) and len(S2) == len(S), a   # T^2(S) = g S
    for v in S: assert abs((S1 @ v).max() - v @ v) < 1e-9                    # every corner of S lies on a face of T(S)
    it = []; solid(it, S, GOLD, M, 1); draw(axs[r, 0], it, 1.05 * R[0] * 1.02)
    it = []; solid(it, S, GOLD, M, 1); shell(it, S1, M); draw(axs[r, 1], it, 1.02 * R1[0])
    it = []; solid(it, S1, VIOLET, M, 1); shell(it, S2, M); draw(axs[r, 2], it, 1.02 * g * R[0])
    axs[r, 0].set_title(f'S: {a}', fontsize=8.5)
    axs[r, 1].set_title(f'T(S): {b}, round S\n(each corner of S on a face)', fontsize=8.5)
    axs[r, 2].set_title(f'T²(S) = g·S, round T(S)\ng = {gtxt}', fontsize=8.5)
fig.text(0.5, 0.025, "DICTO's rule T(S) = {x : v·x ≤ v·v}, each panel at its own scale; two steps give S back, g times larger", ha='center', fontsize=8.5)
logo = plt.imread(LOGO); la = fig.add_axes([0.925, 0.008, 0.065, 0.065 * 8 / 8.4]); la.imshow(logo); la.axis('off')
fig.savefig(OUT, dpi=300, facecolor='white'); print('ok', OUT)
