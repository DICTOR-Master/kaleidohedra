"""Crossed nest (DICTO 11-06: "the stella octangula stood for the tetrahedron in EKP and the Kepler star; I wonder if there could be a
further refinement crossing further elements"). For each Platonic solid P: every compound of k congruent regular solids whose corners are
among P's corners / edge midpoints / face centres (k = 2..10, the classical ones), its UNION's hull and its common CORE (intersection of the
members), and what the core is (corners, face types, identified by name when it matches a known solid)."""
import itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
STD = {'tetrahedron': np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float), 'octahedron': orbit((1, 0, 0)),
       'cube': np.array(list(itertools.product((-1, 1), repeat=3)), float), 'icosahedron': orbit((0, 1, phi)),
       'dodecahedron': np.vstack([orbit((1, 1, 1)), orbit((0, 1 / phi, phi))])}
NV = {'tetrahedron': 4, 'octahedron': 6, 'cube': 8, 'icosahedron': 12, 'dodecahedron': 20}
def dists(V): D = np.linalg.norm(V[:, None] - V[None], axis=2); return np.sort(D[np.triu_indices(len(V), 1)])
SIG = {k: dists(V) / dists(V)[0] for k, V in STD.items()}
def kind(V):
    if len(V) not in NV.values(): return None
    s = dists(V); s = s / s[0]
    for k, g in SIG.items():
        if len(g) == len(s) and np.allclose(g, s, atol=1e-6): return k
    return None
def feats(V):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 7)), set()).update(sp)
    D = np.linalg.norm(V[:, None] - V[None], axis=2); e = D[D > 1e-9].min()
    E = [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(D[i, j] - e) < 1e-7]
    return {'corners': V, 'edge midpoints': np.array([(V[i] + V[j]) / 2 for i, j in E]), 'face centres': np.array([V[list(s)].mean(0) for s in F.values()])}
def members(P, kname):
    """all regular solids of type kname on point set P (by corner subsets), deduplicated"""
    n = NV[kname]; out = []; seen = set()
    if n > len(P): return out
    # anchor: pick a corner and its neighbours by the right edge length candidates
    for sub in itertools.combinations(range(len(P)), n) if len(P) <= 20 and n <= 8 and len(P) ** 0 else []:
        Q = P[list(sub)]
        if kind(Q) == kname and abs(np.linalg.norm(Q.mean(0))) < 1e-7:
            key = frozenset(sub)
            if key not in seen: seen.add(key); out.append(Q)
    return out
def core(Ms):
    """common core of the compound: vertices = points where three face planes meet and that lie in every member (robust, exact-ish)"""
    H = []
    for M in Ms:
        for eq in ConvexHull(M).equations:
            if not any(np.allclose(eq, g, atol=1e-9) for g in H): H.append(eq)
    H = np.array(H); pts = []
    for i, j, k in itertools.combinations(range(len(H)), 3):
        A = H[[i, j, k], :3]
        if abs(np.linalg.det(A)) < 1e-9: continue
        p = np.linalg.solve(A, -H[[i, j, k], 3])
        if (H[:, :3] @ p + H[:, 3] <= 1e-7).all() and not any(np.linalg.norm(p - q) < 1e-6 for q in pts): pts.append(p)
    return np.array(pts)
def describe(P):
    h = ConvexHull(P); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 6)), set()).update(sp)
    ft = {}
    for s in F.values(): ft[len(s)] = ft.get(len(s), 0) + 1
    names = {(12, (3, 8), (4, 6)): 'cuboctahedron', (30, (3, 20), (5, 12)): 'icosidodecahedron', (32, (4, 30)): 'rhombic triacontahedron',
             (14, (4, 12)): 'rhombic dodecahedron'}
    k = kind(P); tag = k or names.get((len(P),) + tuple(sorted(ft.items())), '')
    return len(P), dict(sorted(ft.items())), tag
for pname, V in STD.items():
    F = feats(V)
    for fname, P in F.items():
        P = np.unique(np.round(P, 9), axis=0)
        for kname in NV:
            if NV[kname] >= len(P) or (len(P) > 12 and NV[kname] > 8) or (len(P) > 20): continue
            Ms = members(P, kname)
            if len(Ms) < 2: continue
            C = core(Ms); n, ft, tag = describe(C)
            print(f"{pname:12s} {fname:14s}: {len(Ms)} {kname}s crossed; core {n} corners, faces {ft} {('= ' + tag) if tag else ''}")
# octahedra on point sets with antipodal pairs: three mutually orthogonal antipodal pairs of equal radius (direct, for large point sets)
def octahedra(P):
    out = []; seen = set()
    pairs = [(i, j) for i, j in itertools.combinations(range(len(P)), 2) if np.allclose(P[i], -P[j], atol=1e-7)]
    for (a, b), (c, d), (e, f) in itertools.combinations(pairs, 3):
        u, v, w = P[a], P[c], P[e]
        if abs(u @ v) < 1e-7 and abs(u @ w) < 1e-7 and abs(v @ w) < 1e-7 and np.allclose([u @ u, v @ v], w @ w):
            key = frozenset((a, b, c, d, e, f))
            if key not in seen: seen.add(key); out.append(P[[a, b, c, d, e, f]])
    return out
for pname, V in STD.items():
    for fname, P in feats(V).items():
        P = np.unique(np.round(P, 9), axis=0); Ms = octahedra(P)
        if len(Ms) >= 2:
            C = core(Ms); n, ft, tag = describe(C)
            print(f"{pname:12s} {fname:14s}: {len(Ms)} octahedra crossed; core {n} corners, faces {ft} {('= ' + tag) if tag else ''}")
# the chiral five-tetrahedra compounds inside the ten (in the dodecahedron's corners)
P = STD['dodecahedron']; T10 = members(P, 'tetrahedron')
fives = [c for c in itertools.combinations(range(len(T10)), 5) if len(set(map(tuple, np.round(np.vstack([T10[k] for k in c]), 6)))) == 20]
print(f"dodecahedron corners: {len(fives)} ways to pick 5 of the 10 tetrahedra using all 20 corners (the two chiral compounds)")
if fives:
    C = core([T10[k] for k in fives[0]]); n, ft, tag = describe(C); print(f"   core of five: {n} corners, faces {ft} {('= ' + tag) if tag else ''}")
print("FINAL ok")
