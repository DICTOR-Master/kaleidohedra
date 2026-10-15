# X-ray sections (DICTO, 2026-10-16): the OCD and its dual-nesting Hecatodihedron (scale 4/9) cut through the centre by planes
# perpendicular to a 5-fold, a 3-fold and a 2-fold axis. Each section of a convex solid is an exact polygon. Up = a 2-fold axis
# in the plane (the picture is left-right symmetric); other symmetry axes lying in the plane are drawn as lines. matplotlib.
import json, itertools, numpy as np, sys, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
sys.path.insert(0, '../_lib'); import geomcheck as gc
O = np.array(json.load(open('data/network.json'))['ocd']); r = np.linalg.norm(O, axis=1); ax = gc.icosa_axes(O[np.abs(r - r.max()) < 1e-9])
pl = []
for e in ConvexHull(O).equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
H = np.array([e[:3] / -e[3] for e in pl]) * (4 / 9)
def section(P, n):
    """polygon where the plane n.x = 0 cuts convex P, in plane coordinates (u, w)"""
    h = ConvexHull(P); pts = []
    for s in h.simplices:
        for a, b in itertools.combinations(s, 2):
            da, db = P[a] @ n, P[b] @ n
            if da * db < 0: t = da / (da - db); pts.append(P[a] + t * (P[b] - P[a]))
            elif abs(da) < 1e-12: pts.append(P[a])
    return np.unique(np.round(np.array(pts), 10), axis=0)
fig, axs = plt.subplots(1, 3, figsize=(15, 5.6), facecolor='#f4f1ea')
for A, (k, name) in zip(axs, [('5', 'five-fold'), ('3', 'three-fold'), ('2', 'two-fold')]):
    n = ax[k][0]; up = next(u for u in ax['2'] if abs(u @ n) < 1e-9); right = np.cross(up, n)
    A.set_facecolor('#f4f1ea'); A.set_aspect('equal'); A.axis('off')
    for P, fc, ec, z in [(H, '#c792ea', '#5e3a8c', 1), (O, '#ffc857', '#7a5a00', 2)]:
        S = section(P, n); uv = np.c_[S @ right, S @ up]; hh = ConvexHull(uv); poly = uv[hh.vertices]
        A.add_patch(Polygon(poly, closed=True, fc=fc, ec=ec, lw=1.6, zorder=z))
    # symmetry axes lying in the plane: draw as lines through the centre, labelled by order
    R = 0.85
    for kk, col in (('5', '#c0392b'), ('3', '#1f8fa6'), ('2', '#6d6556')):
        for d in ax[kk]:
            if abs(d @ n) < 1e-9:
                x, y = d @ right, d @ up; A.plot([-R * x, R * x], [-R * y, R * y], color=col, lw=0.9, ls='--', zorder=3)
                A.text(R * 1.06 * x, R * 1.06 * y, kk, color=col, ha='center', va='center', fontsize=10, fontweight='bold')
    A.plot([0], [0], 'o', color='#2b2620', ms=3, zorder=4)
    A.set_xlim(-0.95, 0.95); A.set_ylim(-0.95, 0.95)
    A.set_title(f'cut perpendicular to a {name} axis', fontsize=13, color='#2b2620', fontweight='bold')
fig.text(0.01, 0.02, 'X-ray sections through the centre. Gold: the DICTO Ogdoecontahedron. Violet: its dual Hecatodihedron (scale 4/9, all 102 faces through Ogdoecontahedron corners); '
         'the violet band is the shell between them. Dashed: symmetry axes lying in the cut (5 red, 3 blue, 2 grey); up is a two-fold axis.', fontsize=9, color='#5b5346', wrap=True)
fig.text(0.99, 0.065, 'DICTO · dictospheres.com', ha='right', fontsize=10, fontweight='bold', color='#5b5346')
fig.tight_layout(rect=(0, 0.06, 1, 0.94)); fig.savefig('renders/xray-sections.png', dpi=150, facecolor='#f4f1ea'); print('ok')
