# Star Cores names (2026-10-31): one sheet of the five shapes proposed for naming, render standard (solid, crisp edges), faces coloured
# by their number of sides, DICTO mark. Usage: ~/geom/bin/python sheet.py <data dir> <logo png> <out png>
import sys, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
D, LOGO, OUT = sys.argv[1:4]
COL = {3: '#e8c547', 4: '#5b97d8', 5: '#c0392b', 6: '#3fa66b', 8: '#8e5bd8', 9: '#e07b39', 10: '#d65fa0', 12: '#2b8c9e'}
LIGHT = np.array([0.45, -0.55, 0.7]); LIGHT /= np.linalg.norm(LIGHT)

def ordered(V, f):
    P = V[f]; c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0])
    if np.dot(n, c) < 0: n = -n
    n /= np.linalg.norm(n); a = P[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
    ang = np.arctan2((P - c) @ b, (P - c) @ a)
    return [f[i] for i in np.argsort(ang)], n

def faces_from_hull(V):
    ch = ConvexHull(V); groups = {}
    for eq, s in zip(ch.equations, ch.simplices):
        key = tuple(np.round(eq, 6)); groups.setdefault(key, set()).update(s)
    return [sorted(g) for g in groups.values()]

def draw(ax, V, F, title, sub):
    V = np.asarray(V, float); V /= np.linalg.norm(V, axis=1).max()
    polys, cols = [], []
    for f in F:
        f, n = ordered(V, list(f))
        shade = 0.55 + 0.45 * max(0.0, float(np.dot(n, LIGHT)))
        c = np.array(matplotlib.colors.to_rgb(COL.get(len(f), '#999999'))) * shade
        polys.append(V[f]); cols.append(np.clip(c, 0, 1))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors='#1a1a1a', linewidths=0.7))
    ax.set_xlim(-0.8, 0.8); ax.set_ylim(-0.8, 0.8); ax.set_zlim(-0.8, 0.8); ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=-58); ax.set_axis_off()
    ax.set_title(title, fontsize=13, fontweight='bold', pad=0)
    ax.text2D(0.5, -0.02, sub, transform=ax.transAxes, ha='center', va='top', fontsize=7.4, color='#444')

pearls = json.load(open(D + '/pearls.json')); og = json.load(open(D + '/og56-shapes.json'))
NAMES = {3: 'triangles', 4: 'squares', 5: 'pentagons', 6: 'hexagons', 8: 'octagons', 9: 'nonagons', 10: 'decagons', 12: 'dodecagons'}
def kinds(F):
    k = {}
    for f in F: k[len(f)] = k.get(len(f), 0) + 1
    return ', '.join('%d %s' % (n, NAMES[a]) for a, n in sorted(k.items()))
c, d, g = pearls
items = [
    (c['V'], c['faces'], 'Cube Pearl', '%d corners, all on one sphere (depth 3/5)\n%s' % (len(c['V']), kinds(c['faces']))),
    (g['V'], g['faces'], 'Golden Clasp', '%d corners; depths 1 : 1/φ : 3/4, its chain closes\n%s' % (len(g['V']), kinds(g['faces']))),
    (og['5']['V'], og['5']['F'], 'DICTO TSPNP', 'OG chain step 5: %d corners\n%s' % (len(og['5']['V']), kinds(og['5']['F']))),
    (og['6']['V'], og['6']['F'], 'DICTO SHDP', 'OG chain step 6: %d corners\n%s' % (len(og['6']['V']), kinds(og['6']['F']))),
]
fig = plt.figure(figsize=(12, 4.6), dpi=200)
for i, (V, F, t, s) in enumerate(items):
    draw(fig.add_subplot(1, 4, i + 1, projection='3d'), V, F, t, s)
fig.suptitle("Proposed names for four new Star Cores shapes", fontsize=15, y=0.99)
lg = plt.imread(LOGO); la = fig.add_axes([0.93, 0.86, 0.06, 0.12]); la.imshow(lg); la.set_axis_off()
fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.12, wspace=0.02)
fig.savefig(OUT, facecolor='white'); print('saved', OUT)
