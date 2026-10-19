# quick look at the grown bipyramid piece (dbt-fill-bip.json): faces after merging coplanar triangles, smallest dihedral angles, a render
import json, numpy as np, math, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
H = '/home/dicto/dbt-exact/2026-10-19-og-gyrated-octet/'; D = json.load(open(H + 'dbt-fill-bip.json')); P = np.array(D['v']); T = np.array(D['t'])
N = np.cross(P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]]); A = np.linalg.norm(N, axis=1); keep = A > 1e-12; N = N[keep] / A[keep, None]; T = T[keep]; A = A[keep]
d = np.einsum('ij,ij->i', N, P[T[:, 0]])
planes = []
for n, dd, a in zip(N, d, A):
    for p in planes:
        if np.allclose(n, p[0], atol=1e-5) and abs(dd - p[1]) < 1e-5: p[2] += a / 2; break
    else: planes.append([n, dd, a / 2])
print('faces', len(planes), 'areas', sorted(round(p[2], 4) for p in planes)[:10], '...')
c = P.mean(0); fig = plt.figure(figsize=(9, 4.5))
for k, (el, az) in enumerate([(20, 30), (70, 120)]):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d'); L = np.ones(3) / 3 ** .5
    cols = [plt.cm.Greens(0.35 + 0.55 * max(0, n @ np.array([0.3, -0.5, 0.8]))) for n in N]
    ax.add_collection3d(Poly3DCollection(P[T] - c, facecolors=cols, edgecolors='none'))
    r = np.abs(P - c).max(); ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.view_init(el, az); ax.set_axis_off(); ax.set_box_aspect((1, 1, 1))
fig.text(0.98, 0.02, 'DICTO · dictospheres.com', ha='right', fontsize=8, color='#6d6556'); fig.savefig(H + 'renders/dbt-fill-bip.png', dpi=110)
