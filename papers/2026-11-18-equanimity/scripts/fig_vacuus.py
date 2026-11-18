# Figure 2 (and, with argument 'axis', one picture per die looking down the axis of a regular A face, near half only): the Vacuus of the eight fair dice (plates = triangles from the centre to each edge), from the exact vertex dumps.
# See-through shell (edges only). Slate: the sloping plates (over the edges of the regular A faces, Theorem 6);
# pale sand: the plates on mirrors. Colours are labels only, as in Figure 1.
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
ORDER = [('tc', 10, 'tetrahedron ∩ cube', '7π/30'), ('co', 14, 'cube ∩ octahedron', '2π/7'),
         ('tr', 16, 'tetrahedron ∩ rhombic dodecahedron', '5π/24'), ('cr', 18, 'cube ∩ rhombic dodecahedron', '5π/18'),
         ('or', 20, 'octahedron ∩ rhombic dodecahedron', 'π/5'), ('di', 32, 'dodecahedron ∩ icosahedron', '5π/16'),
         ('dt', 42, 'dodecahedron ∩ rhombic triacontahedron', '13π/42'), ('it', 50, 'icosahedron ∩ rhombic triacontahedron', '9π/50')]
NA = {'tc': 4, 'co': 6, 'tr': 4, 'cr': 6, 'or': 8, 'di': 12, 'dt': 12, 'it': 20}
CS, CM = '#5b6f8a', '#d9c7a3'
import sys
AXIS = len(sys.argv) > 1 and sys.argv[1] == 'axis'
# axis views: one regular A face and the ring of faces sharing a corner with it (the far side only clutters)
fig = plt.figure(figsize=(12, 6.6), dpi=200)
nslope_all = []
for k, (m, N, name, th) in enumerate(ORDER):
    D = json.load(open('verts-%s.json' % m))
    edges = {}
    for f, vs in D['faces'].items():
        P = np.array([[float(c) for c in v] for v in vs]); c = P.mean(0); n = c / np.linalg.norm(c)
        u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        P = P[np.argsort(np.arctan2((P - c) @ w, (P - c) @ u))]
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            key = tuple(sorted([tuple(np.round(a, 9)), tuple(np.round(b, 9))]))
            edges.setdefault(key, [a, b, False])
            if int(f) < NA[m]: edges[key][2] = True      # edge of a regular A face -> sloping plate
    a0 = None
    for f, vs in D['faces'].items():
        if int(f) < NA[m] and len(vs) >= 3:
            a0 = np.array([[float(c) for c in v] for v in vs]).mean(0); a0 /= np.linalg.norm(a0); f0 = int(f); break
    if AXIS:   # 2D orthographic view down the face axis, painter's order by depth (matplotlib 3D sorting skewed the 50-face view)
        z = a0; x = np.cross([0.0, 0.0, 1.0] if abs(z[2]) < 0.9 else [1.0, 0.0, 0.0], z); x /= np.linalg.norm(x); y = np.cross(z, x)
        Rm = np.array([x, y, z])
        F0 = np.array([[float(c) for c in v] for v in D['faces'][str(f0)]])
        ring = [np.array([[float(c) for c in v] for v in vs]) for vs in D['faces'].values() if len(vs) >= 3 and
                any(np.min(np.linalg.norm(F0 - p, axis=1)) < 1e-9 for p in np.array([[float(c) for c in v] for v in vs]))]
        Vr = np.concatenate(ring)
        inring = lambda p: np.min(np.linalg.norm(Vr - p, axis=1)) < 1e-9
        E = [(Rm @ a, Rm @ b, s) for a, b, s in edges.values() if inring(a) and inring(b)]
        fig, ax = plt.subplots(figsize=(6, 6.4), dpi=220)
        items = sorted(E, key=lambda e: (e[0][2] + e[1][2]) / 3)
        for a, b, s in items:
            ax.add_patch(plt.Polygon([[0, 0], a[:2], b[:2]], closed=True, facecolor=CS if s else CM, alpha=0.55 if s else 0.35,
                                     edgecolor=CS if s else 'none', linewidth=0.2))
        for a, b, s in E: ax.plot([a[0], b[0]], [a[1], b[1]], color='#1a1a1a', lw=0.8)
        r = max(max(np.abs(a[:2]).max(), np.abs(b[:2]).max()) for a, b, s in E) * 1.05
        ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_aspect('equal'); ax.set_axis_off()
        ax.set_title('%d faces: θ = %s\n%s\none regular face and its ring, down its %d-fold axis' % (N, th, name, len(D['faces']['0'])), fontsize=11)
        fig.savefig('fig-vacuus-axis-%02d.png' % N, facecolor='white', bbox_inches='tight'); plt.close(fig)
        nslope_all.append((m, sum(1 for e in E if e[2]), len(edges)))
        continue
    else:
        ax = fig.add_subplot(2, 4, k + 1, projection='3d', computed_zorder=False)
    O = np.zeros(3)
    near = (lambda a, b: (a + b) @ a0 > 1e-9) if AXIS else (lambda a, b: True)
    if AXIS:   # rotate so the face axis a0 is +z, then look straight down (robust for every axis)
        z = a0; x = np.cross([0.0, 0.0, 1.0] if abs(z[2]) < 0.9 else [1.0, 0.0, 0.0], z); x /= np.linalg.norm(x); y = np.cross(z, x)
        Rm = np.array([x, y, z])
        edges = {k_: [Rm @ a, Rm @ b, s] for k_, (a, b, s) in edges.items()}; a0 = np.array([0.0, 0.0, 1.0])
    mir = [[O, a, b] for a, b, s in edges.values() if not s and near(a, b)]
    slo = [[O, a, b] for a, b, s in edges.values() if s and near(a, b)]
    nslope_all.append((m, len(slo), len(edges)))
    ax.add_collection3d(Poly3DCollection(mir, facecolors=CM, edgecolors='none', alpha=0.22))
    ax.add_collection3d(Poly3DCollection(slo, facecolors=CS, edgecolors=CS, linewidths=0.2, alpha=0.55))
    ax.add_collection3d(Line3DCollection([[a, b] for a, b, s in edges.values() if near(a, b)], colors='#1a1a1a', linewidths=0.7))
    r = max(np.abs(np.array([a for a, b, s in edges.values()])).max(), 1)
    for s in (ax.set_xlim, ax.set_ylim, ax.set_zlim): s(-r, r)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off()
    if AXIS:
        ax.set_proj_type('ortho')
        ax.view_init(elev=90, azim=-90)
        ax.set_title('%d faces: θ = %s\n%s\none regular face and its ring, down its %d-fold axis' % (N, th, name, len(D['faces'][str(min(int(f) for f in D['faces']))])), fontsize=11)
        plt.subplots_adjust(left=0, right=1, top=0.88, bottom=0)
        fig.savefig('fig-vacuus-axis-%02d.png' % N, facecolor='white'); plt.close(fig)
    else:
        ax.view_init(elev=22, azim=-58)
        ax.set_title('%d faces: θ = %s\n%s' % (N, th, name), fontsize=9)
if not AXIS:
    plt.subplots_adjust(left=0, right=1, top=0.93, bottom=0, wspace=0, hspace=0.14)
    plt.savefig('fig-vacuus.png', facecolor='white')
print('sloping/all plates:', nslope_all)
ok = all(0 < s < e for _, s, e in nslope_all)
print('FINAL ok' if ok else 'FINAL FAIL')
