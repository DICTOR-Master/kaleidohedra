# The finished RD cushion, rendered (DICTO 2026-11-02 "a finished image of the RD cushion"): every face carries its exact knitted
# slice of the cubic (3C) stacking, tetrahedral halves dark gold, octahedral halves light gold, from rd.py's exact sections.
# Usage (compute-host): LOGO=~/work/dicto-logo.png python3 rd_render.py [m]
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m = int(sys.argv[1]) if len(sys.argv) > 1 else 8   # n = 2 chart scale (m = 4n)
L = np.array([0.4, -0.6, 0.7]); L /= np.linalg.norm(L)
def to3(uv, N, b1, b2):
    N, b1, b2 = (np.array(x, float) for x in (N, b1, b2))
    return N * m / (N @ N) + uv[0] * b1 / (b1 @ b1) + uv[1] * b2 / (b2 @ b2)
items = []
for f in rd.faces(m):
    res, R2, b1, b2 = rd.face_sections(f, m)
    n = np.array(f['N'], float); n /= np.linalg.norm(n)
    for r in res:
        c = np.array(plt.matplotlib.colors.to_rgb(rd.GOLD_D if r['kind'].startswith('t') else rd.GOLD_L))
        items.append(([to3((float(p[0]), float(p[1])), f['N'], b1, b2) for p in r['poly']], c, n))
def view_dir(el, az):
    e, a = np.radians(el), np.radians(az); return np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
fig = plt.figure(figsize=(12, 6.4), facecolor='#f4f1ea')
for k, (el, az) in enumerate([(24, -52), (-18, 128)]):
    ax = fig.add_axes([0.0 + k * 0.5, 0.04, 0.5, 0.88], projection='3d'); ax.set_facecolor('#f4f1ea')
    vd = view_dir(el, az); key = vd + 0.35 * np.array([0, 0, 1.0]); key /= np.linalg.norm(key)
    vis = [(P, np.clip(c * (0.6 + 0.4 * max(0, n @ key)), 0, 1)) for P, c, n in items if n @ vd > 0]   # front faces only: no sorting faults
    ax.add_collection3d(Poly3DCollection([P for P, c in vis], facecolors=[c for P, c in vis], edgecolors='#6b5214', linewidths=0.35))
    for f in [f for f in rd.faces(m) if np.array(f['N'], float) @ vd > 0]:
        V = np.array([[float(x) for x in v] for v in f['V']]); ax.plot(*np.vstack([V, V[:1]]).T, color='#3a2a05', lw=1.6)
    lim = m * 0.95; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim); ax.set_box_aspect((1, 1, 1))
    ax.view_init(el, az); ax.set_axis_off()
fig.suptitle('The HexOct rhombic dodecahedron cushion, finished: twelve knitted faces, one chart, every seam matching', fontsize=13, color='#222', y=0.97)
fig.text(0.5, 0.02, 'Each face is the exact slice of the cubic close packing on that face plane: dark gold = tetrahedral halves, light gold = octahedral halves.', ha='center', fontsize=9, color='#444')
lg = plt.imread(os.path.expanduser(os.environ.get('LOGO', '~/work/dicto-logo.png'))); la = fig.add_axes([0.93, 0.02, 0.06, 0.11]); la.imshow(lg); la.axis('off')
fig.savefig(os.path.join(rd.OUT, 'rd-cushion-finished.png'), dpi=170, facecolor='#f4f1ea'); print('ok')
