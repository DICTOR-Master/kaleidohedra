# Scoping a buildable great icosahedron (DICTO, 2026-10-14): cut space by the icosahedron's 20 face planes (inradius 1), find every bounded
# cell, keep those inside the great icosahedron (nonzero winding number of its 20 triangles, which lie in those same planes), and group
# them into congruent pieces. DICTO · dictospheres.com
import itertools, json, os
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
phi = (1 + 5 ** .5) / 2
V = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float) / 2
D = np.linalg.norm(V[:, None] - V[None], axis=2)
GI = [t for t in itertools.combinations(range(12), 3) if all(abs(D[a, b] - phi) < 1e-9 for a, b in itertools.combinations(t, 2))]
ICO = [t for t in itertools.combinations(range(12), 3) if all(abs(D[a, b] - 1) < 1e-9 for a, b in itertools.combinations(t, 2))]
N = np.array([V[list(t)].mean(0) for t in ICO]); N /= np.linalg.norm(N, axis=1)[:, None]          # the 20 face normals
d_gi = float(np.mean([abs(np.cross(V[b] - V[a], V[c] - V[a]) @ V[a]) / np.linalg.norm(np.cross(V[b] - V[a], V[c] - V[a])) for a, b, c in GI]))
P = V / d_gi                                                                                     # great icosahedron with its planes at distance 1
assert all(min(abs(abs(N @ np.cross(P[b] - P[a], P[c] - P[a]) / np.linalg.norm(np.cross(P[b] - P[a], P[c] - P[a]))).max() - 1), 1) < 1e-9 for a, b, c in GI)
def winding(X):
    w = np.zeros(len(X))
    for a, b, c in GI:
        A, B, C = P[a] - X, P[b] - X, P[c] - X; la, lb, lc = [np.linalg.norm(Y, axis=1) for Y in (A, B, C)]
        num = np.einsum('ij,ij->i', A, np.cross(B, C)); den = la * lb * lc + np.einsum('ij,ij->i', A, B) * lc + np.einsum('ij,ij->i', A, C) * lb + np.einsum('ij,ij->i', B, C) * la
        sgn = np.sign(np.dot(P[[a, b, c]].mean(0), np.cross(P[b] - P[a], P[c] - P[a])))
        w += sgn * 2 * np.arctan2(num, den)
    return np.round(w / (4 * np.pi)).astype(int)
R = np.linalg.norm(P[0]); rng = np.random.default_rng(7)
X = rng.uniform(-R, R, (1_500_000, 3)); X = X[np.linalg.norm(X, axis=1) < R]
inball = len(X); wn = winding(X); mc_volume = (wn != 0).mean() * inball / 1_500_000 * (2 * R) ** 3; print('mc volume', mc_volume); print("winding values", dict(zip(*np.unique(wn, return_counts=True)))); X = X[wn != 0]
S = (X @ N.T > 1).astype(np.int8)
keys, idx = np.unique(S, axis=0, return_index=True); print("sign keys", len(keys))
cells = []
for k in keys:
    sg = np.where(k == 1, -1.0, 1.0)                                   # inside: n.x <= 1; outside: n.x >= 1
    hs = np.c_[N * sg[:, None], -sg]
    r = linprog(c=[0, 0, 0, -1], A_ub=np.c_[hs[:, :3], np.ones(20)], b_ub=-hs[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if r.status != 0 or r.x[3] < 1e-7: print("skip", r.status, None if r.x is None else r.x[3]); continue
    Y = HalfspaceIntersection(hs, r.x[:3]).intersections; Y = Y[ConvexHull(Y).vertices]; Z = []
    for y in Y:
        if all(np.linalg.norm(y - z) > 1e-6 for z in Z): Z.append(y)
    cells.append(np.array(Z))
def sig(C):
    return (len(C), round(ConvexHull(C).volume, 6), tuple(sorted(round(float(np.linalg.norm(a - b)), 5) for a, b in itertools.combinations(C, 2))))
groups = {}
for C in cells: groups.setdefault(sig(C), []).append(C)
layer = lambda C: round(float(np.linalg.norm(C.mean(0))), 4)
tot = sum(ConvexHull(C).volume for C in cells)
out = dict(cells=len(cells), types=len(groups), volume=round(tot, 6),
           pieces=[dict(count=len(L), corners=k[0], volume=k[1], centre_radius=layer(L[0])) for k, L in sorted(groups.items(), key=lambda kv: layer(kv[1][0]))])
json.dump(out, open(os.path.join(ROOT, 'great-ico-cells.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
