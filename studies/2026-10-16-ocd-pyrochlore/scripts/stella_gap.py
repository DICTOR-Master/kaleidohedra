# The gap left by the stella-cut companion S in the OCD's bcc packing (DICTO: "could it have a partner to fill space?" / "if it fits with an
# icosahedron would be mindblowing"). Float, voxels over one periodic cell: label the gap's connected pieces, then each piece's corners
# (hull), faces, volume, convexity (piece volume / hull volume) and symmetry, and whether it is an icosahedron. -> data/stella-gap.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
R = {r['name']: r for r in json.load(open('data/companion-variants.json'))}
S = np.array(R['trimmed to its cell']['v']); hS = ConvexHull(S)
P = []
for e in hS.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
P = np.array(P)
N = json.load(open('data/network.json')); T = np.array(N['T']); B = np.array([T[0] + T[1], T[0] + T[2], T[0]]).T; Bi = np.linalg.inv(B)
n = 96                                                     # voxels per basis direction (fractional coordinates, periodic)
g = (np.arange(n) + 0.5) / n
F = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
X = F @ B.T
inside = np.zeros(len(X), bool)
for m in itertools.product((-1, 0, 1, 2), repeat=3):       # copies of S at nearby lattice sites
    c = B @ np.array(m, float); Y = X - c
    inside |= np.all(Y @ P[:, :3].T + P[:, 3] <= 1e-9, axis=1)
gap = (~inside).reshape(n, n, n)
lab, k = ndimage.label(gap)
# merge labels across the periodic boundary
par = list(range(k + 1))
def find(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for ax in range(3):
    a = np.take(lab, 0, axis=ax); b = np.take(lab, n - 1, axis=ax)
    for x, y in zip(a.ravel(), b.ravel()):
        if x and y: par[find(x)] = find(y)
roots = sorted({find(i) for i in range(1, k + 1)})
vox = abs(np.linalg.det(B)) / n ** 3
out = ['DICTO · dictospheres.com', 'Gap of the stella-cut companion in the OCD bcc packing (float, voxels)',
       f'  S fills {inside.mean():.4f} of space (exact run: see stella-cut-exact.txt); gap {1 - inside.mean():.4f}; gap pieces per cell (periodic): {len(roots)}']
L = lab.reshape(-1); tiny = []
for r in roots:
    sel = np.isin(L, [i for i in range(1, k + 1) if find(i) == r])
    if sel.sum() < 200: tiny.append(int(sel.sum())); continue      # voxel specks at touching faces
    pts = X[sel]; vol = sel.sum() * vox
    # unwrap a piece that crosses the cell boundary: shift points by lattice vectors toward the piece's first point
    f = F[sel]; f0 = f[0]; f = f - np.round(f - f0); pts = f @ B.T
    h = ConvexHull(pts); cen = pts.mean(0)
    out.append(f'  piece: volume {vol:.5f} ({vol / abs(np.linalg.det(B)):.4f} of the cell), hull volume {h.volume:.5f}, convex share {vol / h.volume:.3f}, centre {np.round(cen, 3)}')
out.append(f'  voxel specks ignored (< 200 voxels, at faces where copies touch): {len(tiny)}')
print('\n'.join(out)); open('data/stella-gap.txt', 'w').write('\n'.join(out) + '\n')
