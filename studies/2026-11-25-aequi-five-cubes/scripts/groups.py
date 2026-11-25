# Frames, groups, orbits for the Aequi of the five cubes (study 2026-11-25-aequi-five-cubes).
# Icosahedron frame of study 2026-11-19-aequi-complete (placement A: vertices (0, ±φ, ±1) cyclic); its 74 directions keep
# their indices 0..73: C6, O8, RD12 (cube 0 = the coordinate cube), D12, I12, RT24.
# The dodecahedron dual to placement A has the 20 vertices (±1, ±1, ±1) and (0, ±1/φ, ±φ) cyclic. Its 60 face diagonals
# (length 2) are the 60 edges of the five inscribed cubes (12 each). Cube k's directions:
#   C6_k (face normals)      = 3 of the 15 icosahedral 2-fold axes (the five cubes share out all 15: C6 + RT24 = RT30);
#   O8_k (body diagonals)    = 4 of the 10 icosahedral 3-fold axes (each 3-fold axis lies in two cubes: O8 + I12 = I20);
#   RD12_k (edge midpoints)  = 12 directions on NO icosahedral axis (checked below). Cube 0's RD12_0 is the RD12 of the
#   earlier studies; the other four cubes add 48 new directions, which Th splits into two orbits of 24:
#   RDa = (1, 2-φ, 1+φ)/(2√2) with all signs and cyclic orders, RDb = (φ, φ-1, 2φ-1)/(2√2) likewise.
# Union: 74 + 48 = 122 directions; Ih permutes all 122 and RD60 = RD12 + RDa + RDb is one Ih orbit.
# The octahedron dual to cube k has the same three direction sets (vertices C6_k, face normals O8_k, edge midpoints RD12_k).
import itertools, numpy as np
phi = (1 + 5 ** .5) / 2
def u(v): v = np.array(v, float); return v / np.linalg.norm(v)
def cyc_signs(t):
    S = set()
    for s in itertools.product((1, -1), repeat=3):
        q = tuple(a * b for a, b in zip(s, t))
        for k in range(3): S.add(tuple(np.roll(q, k)))
    return [u(p) for p in S]
def dedup(L, tol=1e-9):
    out = []
    for v in L:
        if not any(np.abs(v - w).max() < tol for w in out): out.append(v)
    return out
def key(M): return tuple(np.round(np.asarray(M).ravel(), 6))
def closure(gens):
    G = {key(np.eye(3)): np.eye(3)}; frontier = [np.eye(3)]
    while frontier:
        nf = []
        for A in frontier:
            for g in gens:
                B = g @ A; k = key(B)
                if k not in G: G[k] = B; nf.append(B)
        frontier = nf
    return list(G.values())
def rot(axis, ang):
    a = u(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
P3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)
OH = closure([rot((0, 0, 1), np.pi / 2), P3, -np.eye(3)])
IH = closure([rot((0, phi, 1), 2 * np.pi / 5), P3, rot((0, 0, 1), np.pi), -np.eye(3)])
assert len(OH) == 48 and len(IH) == 120

# ---- exact Z[phi] arithmetic: (a, b) = a + b*phi, phi^2 = phi + 1 ----
def zadd(x, y): return (x[0] + y[0], x[1] + y[1])
def zsub(x, y): return (x[0] - y[0], x[1] - y[1])
def zmul(x, y): return (x[0] * y[0] + x[1] * y[1], x[0] * y[1] + x[1] * y[0] + x[1] * y[1])
def zf(x): return x[0] + x[1] * phi
ONE, PH, IPH, Z0 = (1, 0), (0, 1), (-1, 1), (0, 0)        # 1, phi, 1/phi = phi - 1, 0
def zcyc_signs(t):
    out = set()
    for s in itertools.product((1, -1), repeat=3):
        q = tuple((s[i] * t[i][0], s[i] * t[i][1]) for i in range(3))
        for k in range(3): out.add(q[k:] + q[:k])
    return sorted(out)
DODV = zcyc_signs((ONE, ONE, ONE)) + zcyc_signs((Z0, IPH, PH))
assert len(DODV) == 20
def zdist2(v, w):
    d = [zsub(a, b) for a, b in zip(v, w)]; s = Z0
    for c in d: s = zadd(s, zmul(c, c))
    return s
EDGES = [(i, j) for i, j in itertools.combinations(range(20), 2) if zdist2(DODV[i], DODV[j]) == (4, 0)]
assert len(EDGES) == 60
# the five cubes: cube 0 = (±1, ±1, ±1); cube k = R^k cube 0, R the 5-fold rotation about the vertex (0, φ, 1)
DV = np.array([[zf(c) for c in v] for v in DODV])
R5 = rot((0, phi, 1), 2 * np.pi / 5)
def vid(x): j = int(np.argmin(np.abs(DV - x).max(1))); assert np.abs(DV[j] - x).max() < 1e-9; return j
CUBEV = []
c0 = [i for i, v in enumerate(DODV) if all(c in ((1, 0), (-1, 0)) for c in v)]
for k in range(5): CUBEV.append(sorted(vid(np.linalg.matrix_power(R5, k) @ DV[i]) for i in c0))
assert len({tuple(c) for c in CUBEV}) == 5 and all(sum(i in c for c in CUBEV) == 2 for i in range(20))
ECUBE = []
for i, j in EDGES:
    ks = [k for k in range(5) if i in CUBEV[k] and j in CUBEV[k]]; assert len(ks) == 1; ECUBE.append(ks[0])
assert all(ECUBE.count(k) == 12 for k in range(5))
RDQ = [tuple(zadd(a, b) for a, b in zip(DODV[i], DODV[j])) for i, j in EDGES]   # exact unnormalised edge-midpoint directions
def znorm2(q):
    s = Z0
    for c in q: s = zadd(s, zmul(c, c))
    return s
assert all(znorm2(q) == (8, 0) for q in RDQ)          # |q|^2 = 8 exactly: q / (2 sqrt 2) is a unit vector

FAM = {}
FAM['C6'] = dedup(cyc_signs((1, 0, 0)))
FAM['O8'] = dedup(cyc_signs((1, 1, 1)))
FAM['RD12'] = dedup(cyc_signs((1, 1, 0)))
FAM['D12'] = dedup(cyc_signs((0, phi, 1)))
FAM['I12'] = dedup(cyc_signs((0, 1 / phi, phi)))
FAM['RT24'] = dedup(cyc_signs((1, phi, 1 / phi)))
FAM['RDa'] = dedup(cyc_signs((1, 2 - phi, 1 + phi)))
FAM['RDb'] = dedup(cyc_signs((phi, phi - 1, 2 * phi - 1)))
FAMS = ['C6', 'O8', 'RD12', 'D12', 'I12', 'RT24', 'RDa', 'RDb']
DIRS = []; DFAM = []
for f in FAMS:
    for v in FAM[f]: DIRS.append(v); DFAM.append(f)
DIRS = np.array(DIRS)
assert len(DIRS) == 122 and len(set(map(tuple, np.round(DIRS, 6)))) == 122
DKEY = {tuple(np.round(v, 6)): i for i, v in enumerate(DIRS)}
# cube of each RD direction (-1 for the 62 icosahedral axis directions)
DCUBE = [-1] * len(DIRS)
for q, k in zip(RDQ, ECUBE):
    i = DKEY[tuple(np.round(u([zf(c) for c in q]), 6))]; assert DCUBE[i] == -1; DCUBE[i] = k
assert [DCUBE[i] >= 0 for i in range(122)] == [f in ('RD12', 'RDa', 'RDb') for f in DFAM]
assert all(DCUBE[i] == 0 for i in range(122) if DFAM[i] == 'RD12')
# the five cubes' C6 and O8 lie on icosahedral 2- and 3-fold axes; RD60 lies on none
ICOAX = [i for i in range(122) if DFAM[i] in ('C6', 'O8', 'D12', 'I12', 'RT24')]
for k in range(5):
    Rk = np.linalg.matrix_power(R5, k)
    for v in FAM['C6'] + FAM['O8']:
        assert min(np.abs(DIRS[ICOAX] - Rk @ v).max(1)) < 1e-9
RD60 = [i for i in range(122) if DCUBE[i] >= 0]
AXN = {'C6': 2, 'RT24': 2, 'O8': 3, 'I12': 3, 'D12': 5}
for i in RD60:
    assert min(np.abs(DIRS[ICOAX] - DIRS[i]).max(1)) > 0.1
def dperm(g):
    return [DKEY.get(tuple(np.round(g @ v, 6)), -1) for v in DIRS]
assert all(min(dperm(g)) >= 0 for g in IH), 'Ih must permute the 122 directions'
_orb0 = {dperm(g)[RD60[0]] for g in IH}; assert _orb0 == set(RD60), 'RD60 is one Ih orbit'
TH = [g for g in IH if any(np.allclose(g, h) for h in OH)]; assert len(TH) == 24
for f in ('RDa', 'RDb'):
    I0 = [i for i in range(122) if DFAM[i] == f]
    assert {dperm(g)[I0[0]] for g in TH} == set(I0), f + ' is one Th orbit'
def subgroups(G):
    keys = [key(g) for g in G]; idx = {k: i for i, k in enumerate(keys)}
    mult = np.array([[idx[key(a @ b)] for b in G] for a in G])
    e = idx[key(np.eye(3))]
    def clo(gens):
        S = {e}; fr = [e]
        while fr:
            nf = []
            for a in fr:
                for g in gens:
                    c = mult[a, g]
                    if c not in S: S.add(c); nf.append(c)
            fr = nf
        return frozenset(S)
    subs = {}
    for i in range(len(G)):
        S = clo([i]); subs.setdefault(S, [i])
    frontier = list(subs)
    while frontier:
        nf = []
        for S in frontier:
            gens = subs[S]
            for i in range(len(G)):
                if i not in S:
                    T = clo(gens + [i])
                    if T not in subs: subs[T] = gens + [i]; nf.append(T)
        frontier = nf
    return [[G[i] for i in sorted(S)] for S in subs]
def schoenflies(H):
    """name a finite point group from its elements"""
    n = len(H); inv = any(np.allclose(h, -np.eye(3)) for h in H)
    proper = [h for h in H if np.linalg.det(h) > 0]; improper = [h for h in H if np.linalg.det(h) < 0]
    def order(h):
        A = np.eye(3)
        for k in range(1, 200):
            A = A @ h
            if np.allclose(A, np.eye(3), atol=1e-8): return k
    ro = [order(h) for h in proper]
    mirrors = sum(1 for h in improper if np.allclose(h @ h, np.eye(3), atol=1e-8) and not np.allclose(h, -np.eye(3)))
    np_ = len(proper); mx = max(ro)
    c2 = ro.count(2)
    if np_ == 60: R = 'I'
    elif np_ == 24 and mx == 4 and c2 == 9: R = 'O'
    elif np_ == 12 and ro.count(3) == 8: R = 'T'
    elif mx == np_: R = 'C%d' % np_
    else: R = 'D%d' % (np_ // 2)
    if not improper: return R
    if R == 'I': return 'Ih'
    if R == 'O': return 'Oh'
    if R == 'T': return 'Th' if inv else 'Td'
    k = int(R[1:])
    if R[0] == 'C':
        if mirrors == k and k >= 1 and not (k == 1 and inv): return 'Cs' if k == 1 else 'C%dv' % k
        if k == 1: return 'Ci'
        hm = any(np.allclose(h @ h, np.eye(3), atol=1e-8) and not np.allclose(h, -np.eye(3)) for h in improper)
        if hm and mirrors == 1: return 'C%dh' % k
        return 'S%d' % (2 * k)
    return 'D%dh' % k if mirrors == k + 1 else 'D%dd' % k
def mixed(fams_of_orbits):
    """NEW orbit set: its RD directions come from at least two of the five cubes (orbit_fams carry 'cubeK' tags).
    A set whose directions all lie in the 74 of one cube k (62 icosahedral + RD12_k) is an orbit set of study
    2026-11-19-aequi-complete, up to an icosahedral rotation carrying cube k to cube 0."""
    return len({f for fs in fams_of_orbits for f in fs if f.startswith('cube')}) >= 2
if __name__ == '__main__':
    for f in FAMS: print(f, len(FAM[f]))
    print('exact RD patterns (a + b phi):', sorted({tuple(sorted(tuple(map(abs, c)) for c in q)) for q in RDQ}))
    print('directions', len(DIRS), '| RD60 on no icosahedral axis: min sup-distance %.3f' % min(min(np.abs(DIRS[ICOAX] - DIRS[i]).max(1)) for i in RD60))
    print('FINAL ok' if len(DIRS) == 122 and len(RD60) == 60 and len(EDGES) == 60 else 'FINAL FAIL')
