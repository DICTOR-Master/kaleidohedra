# The cut positions that make each stage uniform (every edge one length), built from the 600-cell's own corners, edges,
# triangles and cells, as the app builds them: truncated 600-cell, a point at s along each edge from each end; bitruncated, on each
# triangle a point at l of the way from each edge's middle to the triangle's centre; truncated 120-cell, a point at t along each
# 120-cell edge (centres of two cells sharing a triangle) from each end. Uniform = every corner's k nearest corners (k = its
# degree) at one distance. Solved numerically to 1e-12, then recognised in Q(sqrt5) and the recognised value checked.
import numpy as np, itertools, sympy as sp
from scipy.spatial import cKDTree
from scipy.optimize import minimize_scalar
exec(open(__file__.replace('cuts.py', 'stages.py')).read().split('keys = ')[0])   # V, D, e0, phi from stages.py
adj = {i: set(j for j in range(120) if abs(D[i, j] - e0) < 1e-9) for i in range(120)}
E = [(i, j) for i in range(120) for j in adj[i] if j > i]
T = [(i, j, k) for i, j in E for k in adj[i] & adj[j] if k > j]
C = [(i, j, k, l) for i, j, k in T for l in adj[i] & adj[j] & adj[k] if l > k]
face = {}
for ci, c in enumerate(C):
    for f in itertools.combinations(c, 3): face.setdefault(f, []).append(ci)
P = list(face.values()); cen = lambda q: V[list(q)].mean(0)
B = {'truncated 600-cell': (lambda s: np.array([(1 - s) * V[a] + s * V[b] for x, y in E for a, b in ((x, y), (y, x))]), 6, (0.2, 0.45)),
     'bitruncated': (lambda l: np.array([(1 - l) * (V[a] + V[b]) / 2 + l * cen(t) for t in T for a, b in itertools.combinations(t, 2)]), 4, (0.05, 0.95)),
     'truncated 120-cell': (lambda s: np.array([(1 - s) * cen(C[a]) + s * cen(C[b]) for x, y in P for a, b in ((x, y), (y, x))]), 4, (0.05, 0.45))}
def spread(X, k):
    d, _ = cKDTree(X).query(X, k + 2); d = d[:, 1:]
    return d[:, k - 1].max() - d[:, 0].min()   # the k nearest at one distance -> 0
for name, (f, k, (lo, hi)) in B.items():
    g = lambda s: spread(f(s), k)
    xs = np.linspace(lo, hi, 400); x0 = xs[np.argmin([g(x) for x in xs])]
    r = minimize_scalar(g, bounds=(x0 - (hi - lo) / 400, x0 + (hi - lo) / 400), method='bounded', options={'xatol': 1e-14})
    q = sp.nsimplify(r.x, [sp.sqrt(5)], tolerance=1e-9)
    print(f'{name}: {r.x:.12f}  spread {r.fun:.2e}  ->  {q}  (check spread {spread(f(float(q)), k):.1e})')
