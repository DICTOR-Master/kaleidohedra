# Independent check of swept9's lattices by random points: every point of one lattice cell is tested against all copies of K
# whose translate could reach it; coverage fraction must equal the density and no point may lie in two copies (beyond boundary specks).
import numpy as np, itertools, json
from scipy.spatial import ConvexHull
phi = (1 + 5**.5) / 2
D = np.array([(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]) * phi / 2
D = np.vstack([D] + [np.array([[0, a*.5, b*phi**2/2], [a*.5, b*phi**2/2, 0], [b*phi**2/2, 0, a*.5]]) for a in (1, -1) for b in (1, -1)])
s = np.array([phi, phi, 0.]); K = np.vstack([D, D + s]); E = ConvexHull(K).equations; VK = ConvexHull(K).volume
inside = lambda Q, tol: (Q @ E[:, :3].T + E[:, 3] <= tol).all(1)
res = json.load(open('swept-symmetric.json'))
rs = np.random.default_rng(7); F = rs.random((500000, 3))
for fam in ['general', 'C_ab', 'P']:
    B = np.array(res[fam]['basis']); X = F @ B; cnt = np.zeros(len(X), int); deep = np.zeros(len(X), int)
    R = int(np.ceil(np.abs(K).max() * 2 / min(np.linalg.norm(B, axis=1)))) + 2
    for c in itertools.product(range(-R, R+1), repeat=3):
        Y = X - np.array(c) @ B
        cnt += inside(Y, 1e-9); deep += inside(Y, -1e-3)
    print(f'{fam:8s} stated {res[fam]["density"]:.5f}  covered {np.mean(cnt > 0):.5f}  vol/det {VK / abs(np.linalg.det(B)):.5f}  points deep inside 2 copies: {(deep > 1).sum()}  lattice range ±{R}')
