"""DICTO 11-06 (premise challenge, #47 <-> HexOct): in HexOct's Fibonacci figure (rock salt at lambda = 1/3, Figure 7.1) cube-like,
tetrahedron-like and octahedron-like pieces stack freely, while #47 shows regular C, T, O of edge 1 barely fit. DICTO proposed that
the freedom comes from the premise: let the pieces deform. Here: the exact shape of every kind of piece (power cells of the same sites
and weights as tower69.py / #64), per kind of layer: faces, corners, edges, dihedral angles, volume, and the distance from the nearest
regular solid. Kinds: ball pieces S in cubic (c) / hexagonal (h) layers; octahedral pieces O between layers of kinds cc / ch / hc / hh;
tetrahedral pieces C, Y (weight 0). Words: the Fibonacci 16-layer word and pure cubic / pure hexagonal for reference."""
import itertools, sys
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
POS = {'A': (0, 0), 'B': (1 / 3, 1 / 3), 'C': (2 / 3, 2 / 3)}
a1 = np.array([1.0, 0, 0]); a2 = np.array([0.5, np.sqrt(3) / 2, 0]); h = np.sqrt(2 / 3)
LAM = float(sys.argv[1]) if len(sys.argv) > 1 else 1 / 3
def types(w): return ['h' if w[k - 1] == w[(k + 1) % len(w)] else 'c' for k in range(len(w))]
def sites(WORD):
    n = len(WORD); S = []
    for k in range(n):
        X, Y = WORD[k], WORD[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
        for role, P, f, w in (('S', X, 0, LAM), ('C', X, .75, 0), ('O', Z, .5, LAM), ('Y', Y, .25, 0)):
            u, v = POS[P]; S.append((role, k, u * a1 + v * a2 + np.array([0, 0, (k + f) * h]), w))
    return S
def cell(S, i, cz):
    p, wp = S[i][2], S[i][3]; H = []
    for j, (r, k, q, w) in enumerate(S):
        for da, db, dc in itertools.product(range(-2, 3), range(-2, 3), (-1, 0, 1)):
            qq = q + da * a1 + db * a2 + np.array([0, 0, dc * cz])
            if j == i and da == db == dc == 0: continue
            if np.linalg.norm(qq - p) > 2.2: continue
            H.append(np.r_[2 * (qq - p), -(qq @ qq - p @ p - w + wp)])
    try:
        hs = HalfspaceIntersection(np.array(H), p)
    except Exception: return None
    P = hs.intersections
    if len(P) < 4: return None
    try: hull = ConvexHull(P)
    except Exception: return None
    if hull.volume < 1e-9: return None
    return P, hull
def describe(P, hull):
    F = {}
    for eq, sp in zip(hull.equations, hull.simplices): F.setdefault(tuple(np.round(eq, 6)), set()).update(sp)
    V = np.unique(np.round(P, 7), axis=0)
    faces = sorted(len({tuple(np.round(P[i], 7)) for i in idx}) for idx in F.values())
    E = set(); norms = list(F.keys())
    for key, idx in F.items():
        pts = np.unique(np.round(P[list(idx)], 7), axis=0); c = pts.mean(0); n = np.array(key[:3]); u = pts[0] - c; w = np.cross(n, u)
        o = pts[np.argsort(np.arctan2((pts - c) @ w, (pts - c) @ u))]
        for a, b in zip(o, np.roll(o, -1, 0)): E.add(tuple(sorted((tuple(a), tuple(b)))))
    L = sorted({round(float(np.linalg.norm(np.subtract(*e))), 4) for e in E})
    dih = set()
    for (k1, i1), (k2, i2) in itertools.combinations(F.items(), 2):
        s1 = {tuple(np.round(P[i], 7)) for i in i1}; s2 = {tuple(np.round(P[i], 7)) for i in i2}
        if len(s1 & s2) >= 2: dih.add(round(180 - np.degrees(np.arccos(np.clip(np.dot(k1[:3], k2[:3]), -1, 1))), 2))
    return len(V), faces, L, sorted(dih), round(hull.volume, 6)
REG = {'cube': (8, [4] * 6, [90.0]), 'tetrahedron': (4, [3] * 4, [70.53]), 'octahedron': (6, [3] * 8, [109.47])}
for name, WORD in (('pure cubic', 'ABC'), ('pure hexagonal', 'AB'), ('Fibonacci 16', 'ABACBCACBABCACBC')):
    S = sites(WORD); T = types(WORD); n = len(WORD); cz = n * h; seen = {}
    for i, (role, k, p, w) in enumerate(S):
        kind = role + ':' + (T[k] if role == 'S' else T[k] + T[(k + 1) % n])
        if kind in seen: continue
        c = cell(S, i, cz)
        seen[kind] = describe(*c) if c else None
    print(f'== {name} ({WORD}), lambda = {LAM:.4f}')
    for kind, d in sorted(seen.items()):
        if d is None: print(f'  {kind:6s} empty'); continue
        nv, faces, L, dih, vol = d
        reg = [r for r, (vv, ff, dd) in REG.items() if nv == vv and faces == ff and dih == dd and len(L) == 1]
        print(f'  {kind:6s} corners {nv:2d} faces {faces} edges {L} dihedrals {dih} volume {vol}' + (f'  = regular {reg[0]}' if reg else ''))
print('FINAL ok')
