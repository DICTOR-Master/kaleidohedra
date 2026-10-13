# DESHI-style cuboctahedral test (DICTO, 2026-10-14). DESHI: 12 icosahedra on the 12 five-fold axes of a central one, parallel,
# slid in until they share whole edges. Cubic analogue: 12 unit cuboctahedra on the 12 vertex (two-fold) axes of a central
# cuboctahedron, parallel, slid in until first contact. Reports the contact distance and type, the hull, the gap, and the hull face
# on each three-fold axis compared with the flat-ended triangle of the cuboctahedral member r = (sqrt3 - 1)/2.
# DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
dirs = np.unique(np.array([p for s in itertools.product((1, -1), repeat=2) for p in set(itertools.permutations((s[0], s[1], 0)))], float), axis=0)
cubo = dirs / math.sqrt(2)                    # unit-edge cuboctahedron (circumradius 1)
U = dirs / np.linalg.norm(dirs, axis=1)[:, None]
H0 = ConvexHull(cubo); EQ = H0.equations
def overlap(c1, c2, eps=1e-9):
    # separating axis test for two translated copies of the same convex polytope: face normals + edge cross products
    d = c2 - c1
    axes = list(EQ[:, :3])
    E = {tuple(np.round(cubo[b] - cubo[a], 9)) for s in H0.simplices for a, b in itertools.combinations(s, 2)}
    E = [np.array(e) for e in E if np.linalg.norm(e) > 1e-9 and abs(np.linalg.norm(e) - 1) < 1e-6]
    for e1, e2 in itertools.combinations(E, 2):
        n = np.cross(e1, e2)
        if np.linalg.norm(n) > 1e-9: axes.append(n / np.linalg.norm(n))
    for n in axes:
        p1 = cubo @ n; p2 = (cubo + d) @ n
        if p1.max() <= p2.min() + eps or p2.max() <= p1.min() + eps: return False
    return True
# slide in: smallest t with no overlap between neighbouring outers (and with a unit centre)
def ok(t):
    C = U * t
    return not any(overlap(C[i], C[j]) for i, j in itertools.combinations(range(12), 2)) and not any(overlap(np.zeros(3), C[i]) for i in range(12))
lo, hi = 1.0, 3.0
for _ in range(60):
    mid = (lo + hi) / 2
    (hi := mid) if ok(mid) else (lo := mid)
t = hi; C = U * t
out = dict(contactDistance=t)
# contact type between neighbours: count shared vertices
def shared(c1, c2): return int(sum(np.min(np.linalg.norm((cubo + c2)[None] - (cubo + c1)[:, None], axis=2), axis=1) < 1e-6))
nb = [(i, j) for i, j in itertools.combinations(range(12), 2) if abs(np.dot(U[i], U[j]) - .5) < 1e-9]
out['neighbourPairs'] = len(nb); out['sharedVerticesPerNeighbourPair'] = sorted({shared(C[i], C[j]) for i, j in nb})
out['sharedWithCentre'] = sorted({shared(np.zeros(3), C[i]) for i in range(12)})
allv = np.vstack([cubo] + [cubo + c for c in C]); H = ConvexHull(allv)
out['hullVolume'] = H.volume; out['piecesVolume'] = 13 * H0.volume; out['fill'] = 13 * H0.volume / H.volume
eq = np.unique(np.round(H.equations, 6), axis=0); out['hullFaces'] = len(eq)
# hull face on the three-fold axis (1,1,1)
n3 = np.ones(3) / math.sqrt(3)
f = [e for e in eq if np.allclose(e[:3], n3, atol=1e-5)]
if f:
    e = f[0]; on = allv[np.abs(allv @ e[:3] + e[3]) < 1e-5]; on = np.unique(np.round(on, 9), axis=0)
    c = on.mean(0); a = on[0] - c; a /= np.linalg.norm(a); b = np.cross(n3, a)
    order = np.argsort(np.arctan2((on - c) @ b, (on - c) @ a)); poly = on[order]
    sides = [float(np.linalg.norm(poly[i] - poly[(i + 1) % len(poly)])) for i in range(len(poly))]
    out['threefoldHullFace'] = dict(corners=len(poly), sides=[round(x, 6) for x in sides])
out['cuboMember_r'] = (3 ** .5 - 1) / 2
json.dump(out, open(os.path.join(ROOT, 'cubo-deshi.json'), 'w'), indent=1)
for k, v in out.items(): print(k, v)
