# The pockets of DICTO's six-ring ball (2026-10-14: "leaving regular or irregular CLEOs in each pocket"). The six ring planes
# (the cuboctahedron's four plus x = 0 and y = 0) cut the cuboctahedron (circumradius = edge = 1) into cones from the centre;
# each cone, closed by the cuboctahedron's face, is a triangular pyramid. Lists the pockets by shape, checks they fill the
# cuboctahedron exactly, and writes an exploded model. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
P = [np.array(v, float) / np.linalg.norm(v) for v in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (1, 0, 0), (0, 1, 0)]]
V = np.array(sorted({p for s in itertools.product((1, -1), repeat=2) for p in set(itertools.permutations((s[0], s[1], 0)))}), float) / math.sqrt(2)
H = ConvexHull(V); EQ = np.unique(np.round(H.equations, 9), axis=0)
pieces = []
for signs in itertools.product((1, -1), repeat=6):
    hs = [list(-s * p) + [0.0] for s, p in zip(signs, P)] + [list(e[:3]) + [e[3]] for e in EQ]   # s*p.x >= 0 and inside
    hs = np.array(hs)
    # find an interior point: try the cone's mean direction
    try:
        A = hs[:, :3]; b = -hs[:, 3]
        from scipy.optimize import linprog
        res = linprog(c=[0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
        if res.status != 0 or res.x[3] < 1e-7: continue
        X = HalfspaceIntersection(hs, res.x[:3]).intersections
        X = np.unique(np.round(X, 9), axis=0); pieces.append(X)
    except Exception as ex:
        continue
def kind(X):
    E = sorted(round(float(np.linalg.norm(a - b)), 4) for a, b in itertools.combinations(X, 2))
    return len(X), tuple(E)
groups = {}
for X in pieces: groups.setdefault(kind(X), []).append(X)
vol = sum(ConvexHull(X).volume for X in pieces)
print('pockets', len(pieces), 'volume sum', round(vol, 9), 'cuboctahedron', round(H.volume, 9))
for k, L in groups.items(): print(len(L), 'x', k[0], 'corners, edges', k[1], 'volume', round(ConvexHull(L[0]).volume, 6))
# exploded model
verts, faces, tags = [], [], []
def tagof(X):
    E = sorted(float(np.linalg.norm(a - b)) for a, b in itertools.combinations(np.unique(np.round(X, 6), axis=0), 2))
    if max(E) > 1.3: return 'w0'          # one edge sqrt2: half a square pyramid
    if min(E) < 0.8: return 'w1'          # quarter of the top and bottom square pyramids
    return 'w2'                          # regular tetrahedron
for gi, (k, L) in enumerate(sorted(groups.items(), key=lambda kv: -len(kv[1]))):
    for X in L:
        c = X.mean(0); X = np.unique(np.round(X, 9), axis=0); Y = X + c * 0.35; h = ConvexHull(Y); base = len(verts); verts += Y.tolist()
        for s, e in zip(h.simplices, h.equations):
            f = list(s); n = np.cross(Y[f[1]] - Y[f[0]], Y[f[2]] - Y[f[0]])
            if n @ e[:3] < 0: f = f[::-1]
            faces.append([int(base + i) for i in f]); tags.append(tagof(X))
json.dump({'ring_pockets': dict(v=verts, f=faces, t=tags)}, open(os.path.join(ROOT, 'paper', 'figures', 'ring-pockets.json'), 'w'))
json.dump({str(k): len(v) for k, v in groups.items()}, open(os.path.join(ROOT, 'ring-pockets.json'), 'w'), indent=1)
