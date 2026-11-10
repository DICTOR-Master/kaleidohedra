"""fig-orderings.png (DICTO 11 Nov: "refer to the underlying form of the permutohedron, not erase it"): the permutohedron as what it is.
Left: the 3D permutohedron of 1, 2, 3, 4 (the 1:1). Right: the permutohedron of 1, 2, 4, 5 (the DICTO 1:2 Truncated Octahedron, the heart of
the 4D Vacuus). Every corner labelled by its ordering; every edge coloured by the exchange it makes (which two neighbouring values swap).
Same view for both; near corners in bold, far corners faint. Exact corners mapped to ordinary space by the isometry of #105 Theorem 4."""
import itertools, sys, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
OUT = sys.argv[1] if len(sys.argv) > 1 else 'fig-orderings.png'
H = np.array([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]) / 2.0
EXC = ['#2f6fb3', '#3c9a5a', '#c0392b']          # exchange of the 1st/2nd, 2nd/3rd, 3rd/4th smallest values
def panel(ax, vals, title):
    m = sum(vals) / 4; P = list(itertools.permutations(vals)); X = np.array([[v - m for v in p] for p in P], float) @ H.T
    X /= np.abs(X).max()
    hh = ConvexHull(X); groups = {}
    for simp, eq in zip(hh.simplices, hh.equations): groups.setdefault(tuple(np.round(eq, 6)), (set(), eq))[0].update(simp)
    for idx, eq in groups.values():
        idx = list(idx); c = X[idx].mean(0); nrm = eq[:3]; u = X[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(nrm, u)
        idx.sort(key=lambda i: math.atan2((X[i] - c) @ w, (X[i] - c) @ u))
        ax.add_collection3d(Poly3DCollection([X[idx]], facecolors=(0.93, 0.88, 0.72, 0.16) if len(idx) == 6 else (0.93, 0.80, 0.35, 0.30), edgecolors='none'))
    elev, azim = 20, -60
    view = np.array([math.cos(math.radians(elev)) * math.cos(math.radians(azim)), math.cos(math.radians(elev)) * math.sin(math.radians(azim)), math.sin(math.radians(elev))])
    order = sorted(vals)
    for i, j in itertools.combinations(range(24), 2):
        d = [k for k in range(4) if P[i][k] != P[j][k]]
        if len(d) == 2 and P[i][d[0]] == P[j][d[1]] and abs(order.index(P[i][d[0]]) - order.index(P[i][d[1]])) == 1:
            k = min(order.index(P[i][d[0]]), order.index(P[i][d[1]]))
            near = (X[i] + X[j]) / 2 @ view > -0.15
            ax.plot(*zip(X[i], X[j]), color=EXC[k], lw=2.4 if near else 1.0, alpha=1.0 if near else 0.35, solid_capstyle='round')
    for i, p in enumerate(P):
        near = X[i] @ view > -0.1
        ax.text(*(X[i] * 1.13), ''.join(map(str, p)), ha='center', va='center', fontsize=8.2 if near else 6.5,
                fontweight='bold' if near else 'normal', color='#111' if near else '#999')
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1); ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.view_init(elev=elev, azim=azim)
    ax.set_title(title, fontsize=11)
    for k, c in enumerate(EXC): ax.plot([], [], color=c, lw=2.4, label=f'exchange {order[k]} ↔ {order[k + 1]}')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.06), ncol=3, fontsize=8, frameon=False)
fig = plt.figure(figsize=(13, 6.6), dpi=220)
panel(fig.add_subplot(1, 2, 1, projection='3d'), (1, 2, 3, 4), 'the 3D permutohedron: the 24 orderings of 1, 2, 3, 4')
panel(fig.add_subplot(1, 2, 2, projection='3d'), (1, 2, 4, 5), 'the 24 orderings of 1, 2, 4, 5: the DICTO 1:2 Truncated Octahedron')
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
plt.subplots_adjust(wspace=0.02, left=0.01, right=0.99, top=0.93, bottom=0.06)
fig.savefig(OUT, bbox_inches='tight'); plt.close(fig)
import os
print('FINAL ok' if os.path.getsize(OUT) > 50000 else 'FINAL FAIL')
