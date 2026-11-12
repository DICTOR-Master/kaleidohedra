"""LEAD 5 exploration (float): the icosahedral two-family line S_lam = {a.x <= 1 (12 five-fold normals: dodecahedron faces),
b.x <= lam (20 three-fold normals: icosahedron faces)}, unit normals. Antipol: distances inverted, S_lam^v = S_{1/lam}; turn
lam -> 1/lam, fixed point lam = 1 (every face tangent to the unit sphere). t_min = max_{x in S, y in S^v} x.y (form (B)).
Prints t_min, the maximising corner pair, and the combinatorial type along lam in (1/rho, rho), rho = R/r of the dodecahedron."""
import itertools, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
phi = (1 + 5 ** .5) / 2
A = []
for s1 in (1, -1):
    for s2 in (1, -1):
        for p in ([0, s1, s2 * phi], [s1, s2 * phi, 0], [s2 * phi, 0, s1]): A.append(p)
A = np.array(A, float); A /= np.linalg.norm(A, axis=1)[:, None]                  # 12 five-fold axes
B = [list(v) for v in itertools.product([1, -1], repeat=3)]
for s1 in (1, -1):
    for s2 in (1, -1):
        for p in ([0, s1 * phi, s2 / phi], [s1 * phi, s2 / phi, 0], [s2 / phi, 0, s1 * phi]): B.append(p)
B = np.array(B, float); B /= np.linalg.norm(B, axis=1)[:, None]                  # 20 three-fold axes
assert len(A) == 12 and len(B) == 20
rho = np.sqrt(15 - 6 * 5 ** .5)
def corners(lam):
    H = np.vstack([np.hstack([A, -np.ones((12, 1))]), np.hstack([B, -lam * np.ones((20, 1))])])
    P = HalfspaceIntersection(H, np.zeros(3)).intersections
    return np.unique(np.round(P, 12), axis=0)
def tmin(lam):
    S, Sv = corners(lam), corners(1 / lam)
    G = S @ Sv.T; i, j = np.unravel_index(G.argmax(), G.shape)
    return G.max(), S[i], Sv[j], len(S)
print(f'rho = R/r(dodecahedron) = {rho:.12f}, 1/rho = {1/rho:.12f}')
rows = []
for lam in np.linspace(1 / rho + 1e-3, rho - 1e-3, 41):
    t, x, y, n = tmin(lam); s = lam + 1 / lam; rows.append((lam, t, n))
    print(f'lam {lam:.6f}  s {s:.6f}  t_min {t:.12f}  corners {n:3d}  |x|^2 {x @ x:.9f} |y|^2 {y @ y:.9f}  x.y/(|x||y|) {t / np.linalg.norm(x) / np.linalg.norm(y):.9f}')
# checks: t_min symmetric under the turn (B is symmetric in S, S^v), 60 corners off the walls, largest t_min next to lam = 1
sym = max(abs(t - tmin(1 / lam)[0]) for lam, t, _ in rows[::5])
top = max(rows, key=lambda r: r[1])[0]
ok = sym < 1e-9 and all(n == 60 for _, _, n in rows) and abs(top - 1) < 0.02
print(f'turn symmetry max |t(lam) - t(1/lam)| = {sym:.2e}; largest t_min at lam = {top:.4f}')
print('FINAL ok' if ok else 'FINAL FAIL')
