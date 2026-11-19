# The three Aequi whose views down a 3-fold axis look alike (TC-10, ORD-20, IRT-50): the same view (top row) and a side view
# (bottom row, the axis vertical, looking along a direction through the middle of one triangle side). One regular triangle face
# and its ring of three hexagons, plates from the centre to each edge: slate sloping, pale sand on a mirror (labels only).
import json, sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
PHI = (1 + 5 ** 0.5) / 2
def _u(v): v = np.array(v, float); return v / np.linalg.norm(v)
MIRRORS = [_u(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,-1,0),(1,0,1),(1,0,-1),(0,1,1),(0,1,-1)]] + \
          [_u(p) for s1 in (1,-1) for s2 in (1,-1) for p in ((1, s1*PHI, s2/PHI), (s2/PHI, 1, s1*PHI), (s1*PHI, s2/PHI, 1))]
CS, CM = '#5b6f8a', '#d9c7a3'
DICE = [('tc', 4, 'Aequus TC-10 (tetrahedron ∩ cube)'), ('or', 8, 'Aequus ORD-20 (octahedron ∩ rhombic dodecahedron)'),
        ('it', 20, 'Aequus IRT-50 (icosahedron ∩ rhombic triacontahedron)')]
fig, axs = plt.subplots(2, 3, figsize=(13.5, 9.2), dpi=200)
for col, (m, NA, name) in enumerate(DICE):
    D = json.load(open(sys.argv[1] + '/verts-%s.json' % m))
    F = {int(k): np.array([[float(c) for c in v] for v in vs]) for k, vs in D['faces'].items() if len(vs) >= 3}
    f0 = min(k for k in F if k < NA and len(F[k]) == 3); F0 = F[f0]
    z = F0.mean(0); z /= np.linalg.norm(z)
    mid = (F0[0] + F0[1]) / 2; x = mid - (mid @ z) * z; x /= np.linalg.norm(x); y = np.cross(z, x)
    ring = [P for k, P in F.items() if any(np.min(np.linalg.norm(F0 - p, axis=1)) < 1e-9 for p in P)]
    assert len(ring) == 4 and sorted(len(P) for P in ring) == [3, 6, 6, 6]
    E = {}
    for P in ring:
        c = P.mean(0); n = c / np.linalg.norm(c); e1 = _u(P[0] - c); e2 = np.cross(n, e1)
        P = P[np.argsort(np.arctan2((P - c) @ e2, (P - c) @ e1))]
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            key = tuple(sorted([tuple(np.round(a, 9)), tuple(np.round(b, 9))]))
            nrm = _u(np.cross(a, b)); E.setdefault(key, (a, b, not any(abs(abs(nrm @ q) - 1) < 1e-9 for q in MIRRORS)))
    for row, (h, v, d) in enumerate(((x, y, z), (x, z, y))):   # top: look down z; side: look along y (axis z up)
        ax = axs[row, col]
        for a, b, s in sorted(E.values(), key=lambda e: (e[0] @ d + e[1] @ d) / 3):
            ax.add_patch(plt.Polygon([[0, 0], [a @ h, a @ v], [b @ h, b @ v]], closed=True, facecolor=CS if s else CM,
                                     alpha=0.55 if s else 0.35, edgecolor=CS if s else 'none', linewidth=0.2))
        for a, b, s in E.values(): ax.plot([a @ h, b @ h], [a @ v, b @ v], color='#1a1a1a', lw=0.8)
        if row == 1: ax.plot([0, 0], [0, max(p @ z for P in ring for p in P) * 1.08], color='#888888', lw=0.6, ls='--')
        r = max(max(abs(a @ h), abs(a @ v)) for a, b, s in E.values()) * 1.08
        ax.set_xlim(-r, r); ax.set_ylim(-r * (0.15 if row else 1), r); ax.set_aspect('equal'); ax.set_axis_off()
        ax.set_title((name + '\nfrom above, down the 3-fold axis') if row == 0 else 'from the side (axis dashed, centre at the bottom)', fontsize=9)
plt.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.01, wspace=0.05, hspace=0.12)
plt.savefig(sys.argv[2], facecolor='white'); print('FINAL ok')
