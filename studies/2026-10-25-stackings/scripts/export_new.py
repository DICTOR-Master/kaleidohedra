# Export the three new interface pieces of ABAC (stackings-new.txt) as OBJ for render_new.py, picked by their face signature.
import itertools, numpy as np, trimesh
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
from stackings import net_for
net = net_for('ABAC'); G = np.array(net['G'], float); L = np.linalg.cholesky(G)
M = [(k, np.array([float(c) for c in p])) for k, p in net['motif']]
sites = [(k, L.T @ (p + np.array(n, float))) for n in itertools.product(range(-2, 3), repeat=3) for k, p in M]
def cell(i, lam):
    w = lambda k: lam if k == 'tet' else 0.0; kp, p = M[i][0], L.T @ M[i][1]; H = []
    for k, q in sites:
        d = q - p
        if np.allclose(d, 0) or d @ d > 6: continue
        H.append(np.r_[2 * d, -(q @ q - p @ p - w(k) + w(kp))])
    H = np.array(H); A, b = H[:, :3], -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if r.x[3] < 1e-7: return None
    V = np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0); V -= V.mean(0); return V
def sig(V):
    h = ConvexHull(V); F = {}
    for s, e in zip(h.simplices, np.round(h.equations, 7)): F.setdefault(tuple(e), set()).update(s)
    return len(V), sorted(len(f) for f in F.values()), h
want = [(-3 / 8, 'oct', (19, [3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 9]), 'n1'), (5 / 24, 'oct', (7, [3, 3, 3, 3, 4, 4, 4]), 'n2'),
        (5 / 24, 'tet', (16, [3, 3, 3, 3, 6, 6, 6, 6, 6, 6]), 'n3')]
for lam, kind, target, tag in want:
    for i, (k, _) in enumerate(M):
        if k != kind: continue
        V = cell(i, lam)
        if V is None: continue
        nv, fs, h = sig(V)
        if (nv, fs) == target:
            trimesh.Trimesh(V, h.simplices).export(f'../{tag}.obj'); print(tag, 'site', i, 'volume', round(h.volume, 9)); break
    else: print(tag, 'NOT FOUND')
