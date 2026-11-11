"""Figure 5 (paper #89 lead strip): the tesseract (corners (+-1,+-1,+-1,+-1)) seen along its long diagonal (1,1,1,1),
with the vertex-first section x1+x2+x3+x4 = 2h drawn inside at h = 1/phi^2, 1/2, 1/phi, and the ladder of corner layers.
Same renderer and house colours as figs.py (gold = golden truncated triangle, teal = regular hexagon, lilac = corner
triangle); DICTO mark bottom right.
usage (compute-host): python fig5_tesseract.py <out dir> <logo png>
"""
import os, sys, itertools
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import gcb

OUT, LOGO = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
G = gcb.g
GOLD, TEAL, LILAC, EDGE, GREY = '#d4af37', '#2bb3a3', '#c4a6ee', '#1d1d24', '#c9ccd3'
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
logo = plt.imread(LOGO)


def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz


def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); k = 0.50 + 0.50 * max(0.0, float(n @ LIGHT))
    return tuple(np.clip(c * k + 0.06 * (1 - k), 0, 1))


def colour(P):
    L = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1)
    if len(P) < 6: return LILAC
    if np.ptp(L) < 1e-7 * L.max(): return TEAL
    return GOLD


V = np.array(list(itertools.product([1, -1], repeat=4)), float)
E = [(i, j) for i, j in itertools.combinations(range(16), 2) if np.abs(V[i] - V[j]).sum() == 2]
B = np.array([[1, -1, 0, 0], [1, 1, -2, 0], [1, 1, 1, -3]], float); B /= np.linalg.norm(B, axis=1)[:, None]
VIEW = (18, 30); M = rot(*VIEW)
P3 = V @ B.T; lay = V.sum(1) / 2          # layer height h of each corner: -2, -1, 0, 1, 2


def section(h):
    pts = []
    for i, j in E:
        a, b = V[i].sum() - 2 * h, V[j].sum() - 2 * h
        if a * b < 0: t = a / (a - b); pts.append((V[i] + t * (V[j] - V[i])) @ B.T)
    return np.array(pts)


def panel(ax, h, title):
    Q = P3 @ M.T
    for i, j in E:                                       # the tesseract's 32 edges, projected
        ax.plot(*np.c_[Q[i, :2], Q[j, :2]], '-', color='#9aa0ab', lw=0.6, zorder=1)
    for k in range(16):
        on = abs(lay[k]) in (0, 1)
        ax.plot(*Q[k, :2], 'o', ms=2.2 if on else 1.6, color='#5b5f6a', zorder=1)
    W = section(h); F = gcb.faces(W); items = []
    for f in F:
        P = W[f]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        if n @ (P.mean(0) - W.mean(0)) < 0: n = -n
        nn = M @ n
        if nn[2] <= 1e-9: continue
        R = P @ M.T; items.append((R[:, 2].mean(), R[:, :2], shade(colour(P), nn)))
    items.sort(key=lambda t: t[0])
    ax.add_collection(PolyCollection([t[1] for t in items], facecolors=[t[2] for t in items], edgecolors=EDGE,
                                     linewidths=0.5, zorder=2))
    lim = 1.05 * np.linalg.norm(P3, axis=1).max(); ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=8.5)


fig, axs = plt.subplots(1, 4, figsize=(10, 2.95), gridspec_kw=dict(wspace=0.04, width_ratios=[1, 1, 1, 0.8]))
for ax, h, t in zip(axs[:3], (1 / G ** 2, .5, 1 / G), ('h = 1/φ²: Greater Golden Cut\nTetrahedron', 'h = 1/2: Archimedean\ntruncated tetrahedron', 'h = 1/φ: Lesser Golden Cut\nTetrahedron')):
    panel(ax, h, t)
ax = axs[3]
for hh, t in ((0, 'h = 0: 6 corners'), (1, 'h = 1: 4 corners')):
    ax.plot([0, 1], [hh, hh], '-', color='#5b5f6a', lw=1.0); ax.text(1.06, hh, t, va='center', fontsize=7)
ax.text(0.5, 1.22, 'tip h = 2 (1 corner) above', ha='center', fontsize=6.5, color='#5b5f6a')
ax.text(0.5, -0.22, 'the layer h = 0 passes through the centre', ha='center', fontsize=6.5, color='#5b5f6a')
for hh, col, t in ((1 / G ** 2, GOLD, '1/φ² ≈ 0.382'), (.5, TEAL, '1/2'), (1 / G, GOLD, '1/φ ≈ 0.618')):
    ax.plot([0, 1], [hh, hh], '-', color=col, lw=2.2); ax.text(1.06, hh, t, va='center', fontsize=7)
ax.set_xlim(-0.1, 2.0); ax.set_ylim(-0.4, 1.4); ax.axis('off')
ax.set_title('one gap between corner layers\n(x1+x2+x3+x4 = 2h)', fontsize=8.5)
a = fig.add_axes([0.925, 0.008, 0.065, 0.065 * fig.get_figwidth() / fig.get_figheight()]); a.imshow(logo); a.axis('off')
fig.savefig(os.path.join(OUT, 'fig5-tesseract.png'), dpi=220, facecolor='white'); plt.close(fig)
print('written', os.path.join(OUT, 'fig5-tesseract.png'))
