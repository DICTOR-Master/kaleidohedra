# The icosahedron cut by the great dodecahedron's 12 pentagon planes (DICTO, 2026-10-14: the 20 Icosahedral Cleo look like the great
# dodecahedron in translucent view). The great dodecahedron shares the icosahedron's 12 corners and 30 edges; each of its pentagons
# lies in the plane through the five neighbours of one corner. Cut the same icosahedron (edge 2/sqrt5, as the Icosahedral Cleo
# kit) by those 12 planes and list the cells. Writes paper/figures/great-dodeca-cut.json (cells pulled apart) and the counts.
# DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
I = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
I *= (2 / 5 ** .5) / 2                                   # edge 2/sqrt5
H = ConvexHull(I); OUT = np.unique(np.round(H.equations, 9), axis=0)
planes = []
for v in I:
    nb = [w for w in I if abs(np.linalg.norm(w - v) - 2 / 5 ** .5) < 1e-9]; n = v / np.linalg.norm(v); d = float(np.mean([w @ n for w in nb]))
    planes.append((n, d))
cells = {}
for signs in itertools.product((1, -1), repeat=12):
    hs = [list(e[:3]) + [e[3]] for e in OUT] + [list(s * n) + [-s * d] for s, (n, d) in zip(signs, planes)]   # s*(n.x - d) <= 0
    hs = np.array(hs); A, b = hs[:, :3], -hs[:, 3]
    r = linprog(c=[0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if r.status != 0 or r.x[3] < 1e-6: continue
    X = np.unique(np.round(HalfspaceIntersection(hs, r.x[:3]).intersections, 9), axis=0)
    cells[signs] = X
def kind(X):
    h = ConvexHull(X); return (len(X), round(h.volume, 6))
groups = {}
for s, X in cells.items(): groups.setdefault(kind(X), []).append(X)
print('cells', len(cells), 'volume', round(sum(ConvexHull(X).volume for X in cells.values()), 9), 'icosahedron', round(H.volume, 9))
for k, L in sorted(groups.items(), key=lambda kv: -kv[0][1]): print(f'{len(L)} cells, {k[0]} corners, volume {k[1]}')
def TAGOF(X):
    v = ConvexHull(X).volume
    return 'w2' if len(X) >= 20 else ('w0' if abs(v - 0.031476) < 1e-4 else ('w3' if abs(v - 0.022776) < 1e-4 else 'w1'))
verts, faces, tags = [], [], []
for X in cells.values():
    c = X.mean(0); Y = X + c * 0.35; h = ConvexHull(Y); b0 = len(verts); verts += Y.tolist()
    for e in np.unique(np.round(h.equations, 9), axis=0):
        on = np.where(np.abs(Y @ e[:3] + e[3]) < 1e-7)[0]; cc = Y[on].mean(0); a = Y[on[0]] - cc; a /= np.linalg.norm(a); bb = np.cross(e[:3], a)
        faces.append([int(b0 + i) for i in on[np.argsort(np.arctan2((Y[on] - cc) @ bb, (Y[on] - cc) @ a))]]); tags.append(TAGOF(X))
json.dump({'gd_cut': dict(v=verts, f=faces, t=tags)}, open(os.path.join(ROOT, 'paper', 'figures', 'great-dodeca-cut.json'), 'w'))
json.dump({f'{len(L)} cells, {k[0]} corners': k[1] for k, L in groups.items()}, open(os.path.join(ROOT, 'great-dodeca-cut.json'), 'w'), indent=1)
# edge lengths of each kind (merged near-duplicate corners), scaled so the core dodecahedron's edge is 1
core = [X for X in cells.values() if len(X) >= 20][0]
ce = min(np.linalg.norm(a - b) for a, b in itertools.combinations(core, 2))
for k, L in sorted(groups.items(), key=lambda kv: -kv[0][1]):
    X = L[0]; Xm = []
    for p in X:
        if all(np.linalg.norm(p - q) > 1e-6 for q in Xm): Xm.append(p)
    E2 = sorted(round(float(np.linalg.norm(a - b)) / ce, 4) for a, b in itertools.combinations(Xm, 2))
    print(len(L), 'cells:', len(Xm), 'corners; distances / core edge:', sorted(set(E2))[:8], 'volume / core edge^3:', round(k[1] / ce ** 3, 6))
print('core edge', ce, 'icosahedron edge / core edge', (2 / 5 ** .5) / ce)
