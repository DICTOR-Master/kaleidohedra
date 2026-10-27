"""Figure for the Red Queen paper (DICTO 2026-10-28): Aristotle's five pyramids as the shadow cores of the 4D solids, and the star
120-cell's spikes. Each panel: the regular solid cut from its centre into its face pyramids (one pyramid lifted out, gold).
Drawing only; the shapes are proved exactly in five_pyramids.py. usage: render_five_pyramids.py <out.png>"""
import sys, os, itertools
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.expanduser("~/kres-tmp/4d/scripts")); from render import BG, GOLD, mark
p = (1 + 5 ** .5) / 2
def perms_even(v):
    out = []
    for s in itertools.product(*[(1, -1) if x else (1,) for x in v]):
        w = [a * b for a, b in zip(v, s)]
        out += [(w[0], w[1], w[2]), (w[1], w[2], w[0]), (w[2], w[0], w[1])]
    return out
SOL = {
 'tetrahedron': np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float),
 'octahedron': np.array([v for i in range(3) for s in (1, -1) for v in [tuple(s if j == i else 0 for j in range(3))]], float),
 'cube': np.array(list(itertools.product((1, -1), repeat=3)), float),
 'icosahedron': np.array(perms_even((0, 1, p)), float),
 'dodecahedron': np.array(list(itertools.product((1, -1), repeat=3)) + perms_even((0, 1 / p, p)), float)}
def faces(V):
    h = ConvexHull(V); F = {}
    for s, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(s)
    out = []
    for f in F.values():
        f = list(f); c = V[f].mean(0); n = c / np.linalg.norm(c); a = V[f[0]] - c; b = np.cross(n, a)
        out.append([f[i] for i in np.argsort([np.arctan2((V[k] - c) @ b, (V[k] - c) @ a) for k in f])])
    return out
PANELS = [('tetrahedron', '5-cell, 16-cell, 600-cell', '4 pyramids'), ('octahedron', '16-cell (corner), 24-cell (cell)', '8 pyramids'),
          ('cube', 'tesseract (cell)', '6 pyramids'), ('icosahedron', '600-cell (corner)', '20 Cleo-Icos'),
          ('dodecahedron', '120-cell (cell)', '12 pentagonal pyramids'), ('dodecahedron', 'small stellated 120-cell (corner)', '12 spikes')]
plt.rcParams["figure.facecolor"] = BG
fig = plt.figure(figsize=(15, 7.2))
for k, (name, where, count) in enumerate(PANELS):
    ax = fig.add_subplot(2, 3, k + 1, projection="3d"); ax.set_facecolor(BG); ax.set_axis_off()
    V = SOL[name] / np.linalg.norm(SOL[name][0]); F = faces(V)
    side = np.array([-np.sin(np.radians(32)), np.cos(np.radians(32)), 0.25])
    i0 = int(np.argmax([V[f].mean(0) @ side for f in F]))   # the gold pyramid: a face seen from the side, so its height shows
    for i, f in enumerate(F):
        lift = 0.55 if i == i0 and k < 5 else 0
        off = V[f].mean(0) / np.linalg.norm(V[f].mean(0)) * lift
        tris = [np.array([np.zeros(3), V[f[j]], V[f[(j + 1) % len(f)]]]) + off for j in range(len(f))] + [V[f] + off]
        if k == 5 and i == i0:                     # the true spike: side edge = phi x base edge (golden), standing on the face
            c = V[f].mean(0); n = c / np.linalg.norm(c); a2 = np.sum((V[f[0]] - V[f[1]]) ** 2); r2 = np.sum((V[f[0]] - c) ** 2)
            apex = c + n * np.sqrt(p * p * a2 - r2)
            tris = [np.array([apex, V[f[j]], V[f[(j + 1) % len(f)]]]) for j in range(len(f))]
        ax.add_collection3d(Poly3DCollection(tris, facecolor=GOLD if i == i0 else "#5b7fa6", edgecolor="#f3ead2", linewidths=0.4, alpha=0.9 if i == i0 else 0.22))
    lim = 1.25 if k < 5 else 1.9
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim): f(-lim, lim)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(18, 32)
    ax.set_title(f"{name}: {count}\n{where}" + ("\ngold: one true spike (golden); blue: the shadows" if k == 5 else ""), color=GOLD if k == 5 else "white", fontsize=9)
fig.suptitle("Aristotle's five pyramids as the cores of the regular four-dimensional solids", color="white", fontsize=12)
mark(fig); fig.savefig(sys.argv[1], dpi=130, facecolor=BG); print("written", sys.argv[1])
