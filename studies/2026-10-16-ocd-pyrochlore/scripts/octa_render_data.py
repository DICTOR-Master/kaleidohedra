# Render data for OCD Stella + octahedra (render_octa.html). Float. Sites of the OCD's bcc packing = simple cubic A (cube-axis vectors from
# the cell's square walls) + B = A + one joint vector. Octahedra on A with even coordinate sum, OCD Stellas elsewhere (A odd: notched by
# 6 octahedron tips; B: whole). -> data/octa-render.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
D = json.load(open('data/stella-cut-exact.json')); S = np.array(D['S']['v']); C = np.array(D['cell']['v'])
def faces(P):
    h = ConvexHull(P); g = {}
    for s, e in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(e, 6)), set()).update(s)
    F = []
    for k, idx in g.items():
        idx = list(idx); n = np.array(k[:3]); c = P[idx].mean(0); u = P[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        F.append([int(i) for i in sorted(idx, key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u))])
    return F
H = ConvexHull(C); P = []
for e in H.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
P = np.array(P); on = lambda e: sum(abs(C @ e[:3] + e[3]) < 1e-7)
hexw = np.array([e for e in P if on(e) == 6]); sqw = np.array([e for e in P if on(e) == 4])
O = np.unique(np.round(HalfspaceIntersection(hexw, np.zeros(3)).intersections, 10), axis=0)
vec = lambda e: 2 * (-e[3]) * e[:3] / (e[:3] @ e[:3])
cube = [vec(e) for e in sqw]; e1 = cube[0]; e2 = next(v for v in cube if abs(v @ e1) < 1e-9); e3 = np.cross(e1, e2); e3 *= np.linalg.norm(e1) / np.linalg.norm(e3)
t = vec(hexw[0])
sites = []
for i, j, k in itertools.product(range(-3, 4), repeat=3):
    a = i * e1 + j * e2 + k * e3
    sites.append([a.tolist(), 'octa' if (i + j + k) % 2 == 0 else 'notched']); sites.append([(a + t).tolist(), 'stella'])
tips = []   # the 6 tips entering a notched Stella's cell (at the origin): the octahedra at the 6 cube neighbours, cut to beyond each wall
for e in sqw:
    sh = vec(e); Osh = O + sh; n = e[:3] / np.linalg.norm(e[:3]); d = -e[3] / np.linalg.norm(e[:3])
    tip = [p for p in Osh if p @ n < d - 1e-9]; ring = [p for p in C if abs(p @ n - d) < 1e-7]
    T = np.array(tip + ring); tips.append({'v': T.tolist(), 'f': faces(T)})
json.dump({'stella': {'v': S.tolist(), 'f': faces(S)}, 'octa': {'v': O.tolist(), 'f': faces(O)}, 'sites': sites, 'tips': tips, 'dir': (e1 + 0.62 * e2 + 0.38 * e3).tolist(), 'up': e3.tolist()},
          open('data/octa-render.json', 'w'))
print('octa corners', len(O), 'tips', len(tips), [len(x['v']) for x in tips], 'sites', len(sites))
