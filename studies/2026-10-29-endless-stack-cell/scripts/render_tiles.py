# Picture of the two layer tiles (Endless Stack Cell, DICTO's idea 2026-10-29): the c-tile (from ABC) and the h-tile (from AB)
# at one weight; left whole, right drawn apart along z. Octahedral halves violet, tetrahedral pieces gold; the layer's ball as a dot.
import sys, numpy as np
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from tiles import tile
lam = Fr(sys.argv[1]) if len(sys.argv) > 1 else Fr(1, 10)
D = (2 / 3) ** 0.5
def cart(p): return np.array([float(p[0]) + float(p[1]) / 2, float(p[1]) * 3 ** 0.5 / 2, float(p[2]) * D])
def faces(P):
    h = ConvexHull(P); out = {}
    for s, eq in zip(h.simplices, h.equations):
        out.setdefault(tuple(np.round(eq, 6)), set()).update(s)
    F = []
    for eq, idx in out.items():
        Q = P[list(idx)]; c = Q.mean(0); n = np.array(eq[:3]); u = Q[0] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        F.append(Q[np.argsort(np.arctan2((Q - c) @ v, (Q - c) @ u))])
    return F
if __name__ == '__main__':
    COL = {('oct', True): '#8a5cc2', ('oct', False): '#b48ae0', ('tet', None): '#d9a521'}
    fig = plt.figure(figsize=(12, 10), facecolor='white')
    for row, (name, word, L) in enumerate([('c-tile (from the cubic stacking ABC)', 'ABC', 1), ('h-tile (from the hexagonal stacking AB)', 'AB', 0)]):
        P, tz = tile(word, L, lam)
        for col, gap in enumerate((0.0, 0.9)):
            ax = fig.add_subplot(2, 2, 2 * row + col + 1, projection='3d'); ax.set_proj_type('ortho')
            allp = []
            for k, up, s, pts, J in P:
                Q = np.array([cart(p) for p in pts])
                dz = {('oct', True): -1, ('oct', False): 1}.get((k, up), 0) * gap
                if k == 'tet': dz = gap * 0.35 * (1 if s[2] > 0 else -1)
                Q = Q + [0, 0, dz]; allp.append(Q)
                ax.add_collection3d(Poly3DCollection(faces(Q), facecolor=COL[(k, up)], edgecolor='#2b2b2b', linewidth=0.6, alpha=0.85))
            ax.scatter([0], [0], [0], color='black', s=30)
            A = np.vstack(allp); c = A.mean(0); r = (A.max(0) - A.min(0)).max() / 2
            ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
            ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=14, azim=-58); ax.set_axis_off()
            ax.set_title(name + (', drawn apart' if gap else ''), fontsize=11)
    fig.text(0.5, 0.02, f'Endless Stack Cell (DICTO): the two layer tiles at λ = {lam}. Violet: octahedral halves (top half from the gap below, '
             'bottom half from the gap above); gold: the two tetrahedral pieces of the layer. Dot: the layer\'s ball.', ha='center', fontsize=9, wrap=True)
    fig.text(0.98, 0.005, 'DICTO · dictospheres.com', ha='right', fontsize=8, color='#777')
    plt.subplots_adjust(left=0, right=1, top=0.95, bottom=0.06, wspace=0, hspace=0.08)
    plt.savefig(f'tiles_{str(lam).replace("/", "_").replace("-", "m")}.png', dpi=130)
    print('saved')

