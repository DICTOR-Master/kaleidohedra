"""Figure (paper #89, "where the cubes live"): sections x1 = h of the rectified tesseract {|x_i| <= 1, sum |x_i| <= 3}:
the cube (h = 0), the Lesser Golden Cut Cube (h = 2 x_L), the Greater Golden Cut Cube (h = 2 x_G), the cuboctahedron
(h = 1, a cell).
House colours as figs.py (gold = golden octagon, teal = regular square, lilac = corner triangle); DICTO mark.
usage (dicto-big-brother): python fig6_cubes.py <out dir> <logo png>
"""
import os, sys, itertools
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scipy.spatial import ConvexHull

OUT, LOGO = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
G = (1 + 5 ** .5) / 2
xG = G / (2 ** .5 + 2 * G); xL = 1 / (G * 2 ** .5 + 2)
GOLD, TEAL, LILAC, BLUE, EDGE = '#d4af37', '#2bb3a3', '#c4a6ee', '#8fb3e0', '#1d1d24'
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
logo = plt.imread(LOGO)


def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz
M = rot(22, 32)


def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); k = 0.50 + 0.50 * max(0.0, float(n @ LIGHT))
    return tuple(np.clip(c * k + 0.06 * (1 - k), 0, 1))


def section(h):
    """corners of {|y_j| <= 1, sum |y_j| <= 3 - h} (cube cut at x = h/2), h in [0, 1]"""
    pts = []
    for s in itertools.product((1, -1), repeat=3):
        for k in range(3):
            p = np.array(s, float); p[k] -= s[k] * h; pts.append(p)
    return np.unique(np.round(pts, 12), axis=0)


def faces(P, octa=False):
    hl = ConvexHull(P); groups = {}
    for eq, sx in zip(np.round(hl.equations, 8), hl.simplices): groups.setdefault(tuple(eq), set()).update(sx)
    out = []
    for eq, g in groups.items():
        g = list(g); c = P[g].mean(0); n = np.array(eq[:3])
        u = P[g[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        g.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u))
        col = BLUE if octa else {3: LILAC, 4: TEAL, 6: TEAL}.get(len(g), GOLD)
        out.append((P[g], n, col))
    return out


def draw(ax, F, lim, cull=True):
    items = []
    for P, n, col in F:
        nn = M @ n
        if cull and nn[2] <= 1e-9: continue
        R = P @ M.T; items.append((R[:, 2].mean() + (0 if cull else 0.02 * nn[2]), R[:, :2], shade(col, nn)))
    items.sort(key=lambda t: t[0])
    ax.add_collection(PolyCollection([t[1] for t in items], facecolors=[t[2] for t in items], edgecolors=EDGE, linewidths=0.5))
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal'); ax.axis('off')


fig, axs = plt.subplots(1, 4, figsize=(9, 2.75), gridspec_kw=dict(wspace=0.04))
for ax, h, t in zip(axs[:4], (0.0, 2 * xL, 2 * xG, 1.0),
                    ('h = 0: cube', f'h = 2x_L ≈ {2 * xL:.4f}:\nLesser Golden Cut Cube', f'h = 2x_G ≈ {2 * xG:.4f}:\nGreater Golden Cut Cube', 'h = 1: cuboctahedron\n(a cell)')):
    draw(ax, faces(section(h)), 1.75); ax.set_title(t, fontsize=8.5)
a = fig.add_axes([0.93, 0.01, 0.06, 0.06 * fig.get_figwidth() / fig.get_figheight()]); a.imshow(logo); a.axis('off')
fig.savefig(os.path.join(OUT, 'fig6-cubes.png'), dpi=220, facecolor='white'); plt.close(fig)
print('written', os.path.join(OUT, 'fig6-cubes.png'))
