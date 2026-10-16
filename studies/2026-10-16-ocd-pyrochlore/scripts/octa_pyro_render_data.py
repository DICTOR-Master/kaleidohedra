# Render data for OCD Stella + octahedra on the pyrochlore networks (render_octa_pyro.html), in the network frame of crystal-render.json:
# OCD Stellas on network 1, regular octahedra (the cell's 8 joint planes) on network 2, and the 6 tips that nest in each Stella. Float.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
N = json.load(open('data/network.json')); T = np.array(N['T']); Lb = np.array(N['Lb']).T
R = json.load(open('data/crystal-render.json'))
sites = [Lb @ np.array(m, float) + k * T[0] for m in itertools.product(range(-2, 3), repeat=3) for k in range(4)]
nb = [s for s in sites if 1e-9 < np.linalg.norm(s) < 2.0]
Vc = HalfspaceIntersection(np.array([np.r_[s, -(s @ s) / 2] for s in nb]), np.zeros(3)).intersections
P = []
for e in ConvexHull(Vc).equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
P = np.array(P); on = lambda e: sum(abs(Vc @ e[:3] + e[3]) < 1e-7)
O = np.unique(np.round(HalfspaceIntersection(np.array([e for e in P if on(e) == 6]), np.zeros(3)).intersections, 10), axis=0)
def faces(X):
    h = ConvexHull(X); g = {}
    for s, e in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(e, 6)), set()).update(s)
    F = []
    for k, idx in g.items():
        idx = list(idx); n = np.array(k[:3]); c = X[idx].mean(0); u = X[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        F.append([int(i) for i in sorted(idx, key=lambda i: np.arctan2((X[i] - c) @ w, (X[i] - c) @ u))])
    return F
tips = []
for e in P:
    if on(e) != 4: continue
    n = e[:3] / np.linalg.norm(e[:3]); d = -e[3] / np.linalg.norm(e[:3]); X = O + 2 * d * n
    pts = np.array([p for p in X if p @ n < d - 1e-9] + [p for p in Vc if abs(p @ n - d) < 1e-7]); tips.append({'v': pts.tolist(), 'f': faces(pts)})
big = [(Lb @ np.array(m, float) + k * T[0], k) for m in itertools.product(range(-3, 4), repeat=3) for k in range(4)]
net1 = [s.tolist() for s, k in big if k < 2 and np.linalg.norm(s) < 3.0]; net2 = [s.tolist() for s, k in big if k >= 2 and np.linalg.norm(s) < 3.0]
json.dump({'stella': R['stella'], 'octa': {'v': O.tolist(), 'f': faces(O)}, 'net1': net1, 'net2': net2, 'axis': R['axis'], 'tips': tips},
          open('data/octa-pyro-render.json', 'w'))
print('octa', len(O), 'tips', len(tips), 'net1', len(net1), 'net2', len(net2))
