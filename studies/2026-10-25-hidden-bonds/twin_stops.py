# The gyrated (twinned) octet's own stops (census hcpholes): lam = 5/24 (oct piece a rhombohedron? + 16-corner tet piece) and
# lam = 3/8 (oct pieces vanish; 10-corner tet piece = twinned counterpart of the Delian cube). Measures shape (edges, face angles,
# volumes) and exports OBJs for render_twin_stops.py. Floats on the census sites (exact stop values from data/raw/hcpholes.json).
import itertools, numpy as np, trimesh
exec(open('keyed_gyrated.py').read().split('LAM = ')[0].replace('import os; ', ''))   # imports
import os
from scipy.spatial import ConvexHull
net = NETS['hcpholes']; G = np.array(net['G'], float); L = np.linalg.cholesky(G)
T = [np.array(t, float) for t in net['T']]; M = [(k, np.array(p, float)) for k, p in net['motif']]
sites = [(k, L.T @ (p + sum(c * t for c, t in zip(n, T)))) for n in itertools.product(range(-2, 3), repeat=3) for k, p in M]
def cellV(p, kp, lam):
    w = lambda k: lam if k == 'tet' else 0.0; H = []
    for k, q in sites:
        d = q - p
        if np.allclose(d, 0) or d @ d > 6: continue
        H.append(np.r_[2 * d, -(q @ q - p @ p - w(k) + w(kp))])
    H = np.array(H); A, b = H[:, :3], -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if r.x[3] < 1e-7: return None
    return np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0)
def faces(V):
    h = ConvexHull(V); F = {}
    for s, e in zip(h.simplices, np.round(h.equations, 7)): F.setdefault(tuple(e), set()).update(s)
    return h, list(F.values())
for lam, tag in ((5 / 24, '524'), (3 / 8, '38')):
    print(f'== lam = {tag[0]}/{tag[1:]}')
    for kind, idx in (('oct', 0), ('tet', 2)):
        V = cellV(L.T @ M[idx][1], kind, lam)
        if V is None: print(f'  {kind}: vanished'); continue
        h, F = faces(V); E = set()
        for a, b2 in itertools.combinations(range(len(F)), 2):
            s = F[a] & F[b2]
            if len(s) == 2: E.add(tuple(sorted(s)))
        lens = sorted({round(float(np.linalg.norm(V[i] - V[j])), 6) for i, j in E})
        angs = set()
        for f in F:
            P = V[sorted(f)]; c = P.mean(0)
            for i in sorted(f):
                nb = [j for j in sorted(f) if tuple(sorted((i, j))) in E]
                if len(nb) == 2:
                    u, v = V[nb[0]] - V[i], V[nb[1]] - V[i]
                    angs.add(round(float(np.degrees(np.arccos(u @ v / np.linalg.norm(u) / np.linalg.norm(v)))), 4))
        print(f'  {kind}: corners {len(V)}, faces {sorted(len(f) for f in F)}, volume {h.volume:.6f}, edge lengths {lens}, face angles {sorted(angs)}')
        c = V.mean(0); trimesh.Trimesh(V - c, h.simplices).export(f'ts-{tag}-{kind}.obj')
