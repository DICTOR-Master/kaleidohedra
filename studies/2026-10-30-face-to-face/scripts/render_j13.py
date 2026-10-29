# Face to face (#77, DICTO 2026-10-30): the one convex deltahedron beyond the tetrahedron that the six-piece search of
# DICTO's pieces reached: the pentagonal bipyramid (J13) from 4 M-S t1 and 2 Hound Tooth (M-S t2), i.e. two pentagonal
# pyramids t1 + t2 + t1 (Koca et al. 2020) base to base. Left: assembled; right: pulled apart along the axis and outwards.
# Run on dicto-big-brother from ~/kres-tmp/pyramids: DEEP=1 ~/geom/bin/python scripts/render_j13.py data/f2f-deep-L6-results.json out.png
import sys, os, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
res, out = sys.argv[1], sys.argv[2]
sys.argv = ['x', '1', '1']; sys.path.insert(0, 'scripts')
import enum_glue_f2f as g

GOLD, PURPLE, BG = '#d4af37', '#8e5bd6', '#0d0d12'
lib = g.library()
r = json.load(open(res))['results'][1]
pieces = []
for i, R, t in r['cl']:
    P = lib[i]; V = np.array(P['V']) @ np.array(R).T + np.array(t)
    pieces.append((P['name'], V, P['F']))
allV = np.vstack([V for _, V, _ in pieces]); c = allV.mean(0)
# the axis: through the two corners of degree 5 (the two apexes)
F = [np.array(Q) for Q in r['merged_faces']]; deg = {}
for Q in F:
    for p in Q: k = tuple(np.round(p, 7)); deg[k] = deg.get(k, 0) + 1
ap = np.array([k for k, v in deg.items() if v == 5]); ax_ = ap[0] - ap[1]; ax_ /= np.linalg.norm(ax_)
# turn the axis upright: frame (u, w, ax_) with u towards an equator corner
eqc = np.array([k for k, v in deg.items() if v == 4]); u = eqc[0] - c; u -= np.dot(u, ax_) * ax_; u /= np.linalg.norm(u)
Rf = np.array([u, np.cross(ax_, u), ax_])
pieces = [(n, (V - c) @ Rf.T, Fs) for n, V, Fs in pieces]; c = np.zeros(3); ax_ = np.array([0., 0., 1.])

def draw(ax, explode):
    for name, V, Fs in pieces:
        m = V.mean(0) - c; along = np.dot(m, ax_) * ax_; side = m - along
        d = explode * (0.9 * np.sign(np.dot(m, ax_)) * ax_ + 1.6 * side)
        col = PURPLE if 'Hound' in name else GOLD
        ax.add_collection3d(Poly3DCollection([V[f] + d for f in Fs], facecolor=col, edgecolor='#f5f0dc', linewidths=0.8, alpha=0.8))
    rr = 0.62 + 0.4 * explode
    for k in range(3): getattr(ax, 'set_%slim' % 'xyz'[k])(c[k] - rr, c[k] + rr)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG)
    ax.view_init(elev=18, azim=-62)

fig = plt.figure(figsize=(9, 4.6), facecolor=BG)
for k, (e, title) in enumerate([(0, 'assembled: the pentagonal bipyramid J13'), (0.45, 'pulled apart: 4 M-S t1 (gold), 2 Hound Tooth (purple)')]):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d'); draw(ax, e); ax.set_title(title, color='#e8e2cc', fontsize=10)
fig.text(0.985, 0.02, 'DICTO', color=GOLD, ha='right', va='bottom', fontsize=11, fontweight='bold', family='serif')
fig.savefig(out, dpi=200, facecolor=BG, bbox_inches='tight')
print('wrote', out)
