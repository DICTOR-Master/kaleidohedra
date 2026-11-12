#!/usr/bin/env python3
"""Exact checks of three floating-point results of DICTO's Platonic book draft (13 Nov 2026).
  A. The crossed-nest cores (Ch 1; study 2026-11-06-crossed-nest, compounds.py): stella octangula -> octahedron; on the dodecahedron's
     20 corners the 5 cubes -> rhombic triacontahedron, the 10 tetrahedra and each chiral 5 -> icosahedron (edge ratio); on the
     icosahedron's 30 edge midpoints the 5 octahedra -> icosahedron (edge ratio, orientation).
  B. The octet thresholds (Ch 10; overlap.py, roofs.py): every Pacioli icosahedron (and the nest's dodecahedron = its face centres) of
     the octet grown by s about its own centre. Events: first touch, tetrahedral-hole centres reached, full cover, coplanar faces of
     neighbours meeting. Each is a minimum over ALL cells, taken over a finite list made complete by an exact norm bound; the range
     considered is 0 < s <= 3.
  C. Dogstar's discs (Ch 4; orbit study 2026-11-11, vacuus_census.py, and the #87 definition in vacuus.py): exact census of the central
     planes of its edges and of its #87 central discs (closed flat sheets of fins, apex angles summing to 2 pi).
Everything is exact in Q(sqrt5) with the field class of the #87 study (studies/2026-11-02-dicto-vacuus/scripts/qf.py, executed from its
file, not retyped). The octet is scaled so that its cube side is 2 (sites on integer points): s is scale-free, so no sqrt2 is needed.
Dogstar's corners are read from the registry floats (data/dogstar_vacuus.json of the orbit study) and recognised in Q(sqrt5) with
denominator 4; from then on every statement is exact (planarity of every face, closed surface, volume, symmetry).
Controls: POSITIVE octahedron 3 square discs (both definitions), cuboctahedron 4 x 6, icosidodecahedron 6 x 10, stella octangula core =
octahedron; NEGATIVE cube 0 discs, dodecahedron 0 discs; threshold machinery: a ball-like check that the gauge of a corner of K is 1.
Usage: platonic_exact.py [--pilot]   (pilot: controls and part A only)"""
import sys, os, time, json, itertools, math
from fractions import Fraction as Fr
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); STUD = os.path.normpath(os.path.join(HERE, '..', '..'))
exec(open(os.path.join(STUD, '2026-11-02-dicto-vacuus', 'scripts', 'qf.py')).read(), globals())   # QF, vsub, vadd, vmul, dot, cross, det3
QF.D = 5
QF.__abs__ = lambda s_: s_ if s_.sign() >= 0 else -s_      # exact |x| (added here; qf.py unchanged)
PILOT = '--pilot' in sys.argv
OUT = {}
NCHK = [0, 0]
def check(name, cond, detail=''):
    NCHK[0] += 1
    if not cond: NCHK[1] += 1
    print(f"{'ok  ' if cond else 'FAIL'} {name} {detail}", flush=True)
    return cond
def progress(f, what): print(f'PROGRESS {f:.2f} {what} ({time.time() - T0:.0f} s)', flush=True)
Z, ONE = QF(0), QF(1)
PHI = QF(Fr(1, 2), Fr(1, 2)); IPHI = PHI - 1; S5 = QF(0, 1)
def q(x): return x if isinstance(x, QF) else QF(x)
def V3(*xs): return tuple(q(x) for x in xs)
def ex(x):
    """exact string a + b sqrt5"""
    x = q(x)
    if x.b == 0: return str(x.a)
    if x.a == 0: return f'({x.b})√5'
    return f'{x.a} + ({x.b})√5'
def fl(x): return f'{float(x):.6f}'
def neg(v): return tuple(-x for x in v)
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def mul(v, k): return tuple(x * k for x in v)
def dv(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cr(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def iszero(v): return all(x == 0 for x in v)
def sgn(x): return q(x).sign()
def qmax(xs):
    m = None
    for x in xs:
        if m is None or (x - m).sign() > 0: m = x
    return m
def qmin(xs):
    m = None
    for x in xs:
        if m is None or (x - m).sign() < 0: m = x
    return m
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit_cs(v):
    """cyclic permutations with all sign changes (pyritohedral orbit)"""
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return sorted(S, key=lambda p: tuple(float(x) for x in p))
def allperm_cs(v):
    S = set()
    for p in itertools.permutations(v):
        for s in itertools.product((1, -1), repeat=3): S.add(tuple(a * b for a, b in zip(s, p)))
    return sorted(S, key=lambda p: tuple(float(x) for x in p))

# ---------------------------------------------------------------- convex hulls and half-space intersections, exact
def hull_facets(V):
    """facets of conv(V) (0 strictly inside): list of (N, idx) with N.x <= 1 the facet, idx the corners on it"""
    F = {}
    for i, j, k in itertools.combinations(range(len(V)), 3):
        n = cr(sub(V[j], V[i]), sub(V[k], V[i]))
        if iszero(n): continue
        h = dv(n, V[i])
        if h == 0: continue
        N = mul(n, ONE / h)                      # N.x = 1 on the plane, N.0 = 0 < 1
        if N in F: continue
        if all(sgn(dv(N, p) - 1) <= 0 for p in V): F[N] = [t for t, p in enumerate(V) if dv(N, p) == 1]
    return list(F.items())
def halfspace_vertices_r(H):
    """corners of {x : N.x <= r for all (N, r) in H} (Cramer, exact)"""
    P = {}
    for a, b, c in itertools.combinations(range(len(H)), 3):
        (Na, ra), (Nb, rb), (Nc, rc) = H[a], H[b], H[c]
        d = det3(list(Na), list(Nb), list(Nc))
        if d == 0: continue
        x = mul(add(add(mul(cr(Nb, Nc), ra), mul(cr(Nc, Na), rb)), mul(cr(Na, Nb), rc)), ONE / d)
        if x in P: continue
        if all(sgn(dv(N, x) - r) <= 0 for N, r in H): P[x] = 1
    return list(P)
def halfspace_vertices(Ns): return halfspace_vertices_r([(N, ONE) for N in Ns])
def edges_from_facets(V, Fs):
    inc = [set(fi for fi, (N, idx) in enumerate(Fs) if t in idx) for t in range(len(V))]
    return [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if len(inc[i] & inc[j]) >= 2]
def describe(V):
    Fs = hull_facets(V); E = edges_from_facets(V, Fs)
    fsz = {}
    for N, idx in Fs: fsz[len(idx)] = fsz.get(len(idx), 0) + 1
    e2 = sorted({dv(sub(V[i], V[j]), sub(V[i], V[j])) for i, j in E}, key=float)
    r2 = sorted({dv(p, p) for p in V}, key=float)
    return dict(corners=len(V), faces=dict(sorted(fsz.items())), edges=len(E), edge2=e2, radius2=r2, Fs=Fs, E=E)
def planes_of(M):
    return [N for N, idx in hull_facets(M)]
def core(members):
    Ns = []
    for M in members:
        for N in planes_of(M):
            if N not in Ns: Ns.append(N)
    return halfspace_vertices(Ns), len(Ns)
def d2(u, v): w = sub(u, v); return dv(w, w)

# ================================================================ PART A: the crossed-nest cores
def tetrahedra_on(P):
    out = []
    for c in itertools.combinations(range(len(P)), 4):
        ds = {d2(P[a], P[b]) for a, b in itertools.combinations(c, 2)}
        if len(ds) == 1 and iszero(mul(add(add(P[c[0]], P[c[1]]), add(P[c[2]], P[c[3]])), ONE)): out.append(frozenset(c))
    return out
def is_regular(D, name):
    want = {'octahedron': (6, {3: 8}, 12), 'icosahedron': (12, {3: 20}, 30), 'cube': (8, {4: 6}, 12)}[name]
    return D['corners'] == want[0] and D['faces'] == want[1] and D['edges'] == want[2] and len(D['edge2']) == 1 and len(D['radius2']) == 1
def same_set(A, B): return set(A) == set(B)
def part_A():
    print('== PART A: crossed-nest cores (exact)', flush=True)
    R = {}
    # A0 stella octangula (POSITIVE control)
    C8 = [V3(*p) for p in itertools.product((1, -1), repeat=3)]
    T2 = tetrahedra_on(C8)
    check('A0 stella: 2 regular tetrahedra on the cube corners', len(T2) == 2)
    cv, npl = core([[C8[i] for i in t] for t in T2]); D = describe(cv)
    check('A0 stella core is a regular octahedron', is_regular(D, 'octahedron'), f"(corners {sorted(set(tuple(float(x) for x in p) for p in cv))[:2]}...)")
    R['stella'] = dict(core='octahedron', corners=len(cv))
    # A1 dodecahedron corners
    DOD = C8 + [V3(*p) for p in orbit_cs((Z, IPHI, PHI))]
    DD = describe(DOD)
    check('A1 dodecahedron: 20 corners, 12 pentagons, one edge length, one radius', len(set(DOD)) == 20 and DD['faces'] == {5: 12} and len(DD['edge2']) == 1 and len(DD['radius2']) == 1)
    eD2 = DD['edge2'][0]
    T10 = tetrahedra_on(DOD)
    check('A1 exactly 10 regular tetrahedra on the 20 corners', len(T10) == 10)
    # cubes: a cube inscribed in the circumsphere is T u -T; check every such union is a cube and that there are no others
    cubes = []
    for t in T10:
        mt = frozenset(DOD.index(neg(DOD[i])) for i in t)
        if mt in T10 and (mt | t) not in cubes: cubes.append(mt | t)
    okc = all(is_regular(describe([DOD[i] for i in c]), 'cube') for c in cubes)
    check('A1 exactly 5 cubes (each the union T u -T of two of the ten tetrahedra; every inscribed cube is of this form)', len(cubes) == 5 and okc)
    cv, npl = core([[DOD[i] for i in c] for c in cubes]); D = describe(cv)
    rad = D['radius2']; fs = D['faces']
    rhombi = True
    for N, idx in D['Fs']:
        P = [cv[i] for i in idx]
        if len(P) != 4: rhombi = False; break
        sides = {d2(P[a], P[b]) for a, b in itertools.combinations(range(4), 2)}
        # a rhombus: 4 equal sides + 2 diagonals; golden: diagonal^2 ratio phi^2
        ds = sorted(sides, key=float)
        if len(ds) != 3 or not (ds[2] / ds[1] == PHI * PHI or ds[1] / ds[0] == PHI * PHI): rhombi = False
    gold_ratio = None
    for N, idx in D['Fs'][:1]:
        P = [cv[i] for i in idx]; ds = sorted({d2(P[a], P[b]) for a, b in itertools.combinations(range(4), 2)}, key=float)
        gold_ratio = ex(ds[2] / ds[1]) if len(ds) == 3 else None
    is_rt = D['corners'] == 32 and fs == {4: 30} and D['edges'] == 60 and len(D['edge2']) == 1 and len(rad) == 2
    check('A1 core of the 5 cubes is a rhombic triacontahedron (32 corners, 30 congruent golden rhombi, 60 equal edges, corners on 2 spheres)',
          is_rt and rhombi, f'(diagonal^2 ratio {gold_ratio}; corner radius^2 {[ex(r) for r in rad]})')
    R['five_cubes'] = dict(core='rhombic triacontahedron', corners=D['corners'], faces=fs, edge2=ex(D['edge2'][0]), radius2=[ex(r) for r in rad],
                           edge_over_dodeca_edge_sq=ex(D['edge2'][0] / eD2))
    cv, npl = core([[DOD[i] for i in t] for t in T10]); D = describe(cv)
    ok = is_regular(D, 'icosahedron')
    ratio2 = D['edge2'][0] / eD2
    check('A1 core of the 10 tetrahedra is a regular icosahedron', ok, f'(edge^2 / dodecahedron edge^2 = {ex(ratio2)} = 1/phi^2: {ratio2 == ONE / (PHI * PHI)})')
    check('A1 its edge is exactly 1/phi times the dodecahedron edge', ratio2 == ONE / (PHI * PHI))
    ico10 = cv
    # orientation of that icosahedron: its corners point along the dodecahedron's face normals (the dual) or along its corners?
    dual_dirs = [N for N, idx in hull_facets(DOD)]
    along_faces = all(any(iszero(cr(p, N)) and sgn(dv(p, N)) > 0 for N in dual_dirs) for p in ico10)
    check('A1 the 10-tetrahedra core icosahedron has its corners on the dodecahedron face axes (the dual position)', along_faces)
    fives = [c for c in itertools.combinations(T10, 5) if len(set().union(*c)) == 20]
    check('A1 exactly 2 ways to take 5 of the 10 tetrahedra using all 20 corners (the chiral pair)', len(fives) == 2)
    same = True
    for c in fives:
        cv5, _ = core([[DOD[i] for i in t] for t in c])
        same &= same_set(cv5, ico10)
    check('A1 each chiral five has the SAME core icosahedron as the ten', same)
    R['ten_tetrahedra'] = dict(core='icosahedron', edge_over_dodeca_edge=ex(ONE / PHI), orientation='corners on the dodecahedron face axes')
    R['chiral_fives'] = dict(count=len(fives), core_same_as_ten=bool(same))
    # A2 icosahedron edge midpoints: 5 octahedra
    ICO = [V3(*p) for p in orbit_cs((Z, ONE, PHI))]
    Di = describe(ICO); eI2 = Di['edge2'][0]
    check('A2 icosahedron: 12 corners, 20 triangles, regular', is_regular(Di, 'icosahedron'))
    mids = [mul(add(ICO[i], ICO[j]), QF(Fr(1, 2))) for i, j in Di['E']]
    check('A2 30 edge midpoints, all at one radius', len(set(mids)) == 30 and len({dv(m, m) for m in mids}) == 1)
    pairs = [(a, b) for a, b in itertools.combinations(range(30), 2) if iszero(add(mids[a], mids[b]))]
    octs = []
    for (a, b), (c, d), (e, f) in itertools.combinations(pairs, 3):
        u, v, w = mids[a], mids[c], mids[e]
        if dv(u, v) == 0 and dv(u, w) == 0 and dv(v, w) == 0: octs.append([mids[i] for i in (a, b, c, d, e, f)])
    check('A2 exactly 5 octahedra (three mutually orthogonal antipodal pairs) on the 30 midpoints', len(octs) == 5)
    cv, _ = core(octs); D = describe(cv)
    check('A2 core of the 5 octahedra is a regular icosahedron', is_regular(D, 'icosahedron'))
    # same orientation: cv = lam * ICO, lam > 0
    lam = None
    for p in cv:
        if iszero(cr(p, ICO[0])) and sgn(dv(p, ICO[0])) > 0: lam = dv(p, ICO[0]) / dv(ICO[0], ICO[0])
    same_or = lam is not None and same_set(cv, [mul(p, lam) for p in ICO])
    check('A2 the core is lam x the icosahedron itself (same orientation), lam exact', same_or, f'(lam = {ex(lam) if lam is not None else None} = {fl(lam) if lam is not None else None})')
    check('A2 lam = 1/phi: the golden loop shrinks by 1/phi per turn', lam == IPHI)
    R['five_octahedra'] = dict(core='icosahedron', scale=ex(lam), same_orientation=bool(same_or))
    OUT['A'] = R

# ================================================================ PART B: the octet thresholds
# sites (octahedral holes) on the lattice L = {integer vectors with even sum} (fcc); octet corners at L + e1; tetrahedral holes at L +- (1,1,1)/2
def L_points(B):
    """all v in L with v.v <= B (B exact), v != 0"""
    m = int(math.floor(math.sqrt(float(B)))) + 1; out = []
    for v in itertools.product(range(-m, m + 1), repeat=3):
        if sum(v) % 2 == 0 and any(v) and sgn(QF(v[0] ** 2 + v[1] ** 2 + v[2] ** 2) - B) <= 0: out.append(V3(*v))
    return out
def gauge(Ns, v): return qmax([dv(N, v) for N in Ns])
def argmax_facets(Ns, v):
    g = gauge(Ns, v); return g, [N for N in Ns if dv(N, v) == g]
def contact_set(KV, s, v):
    """corners of sK cap (sK + v), exact"""
    Ns = [N for N, idx in hull_facets(KV)]
    return halfspace_vertices_r([(N, s) for N in Ns] + [(N, s + dv(N, v)) for N in Ns])   # sK: N.x <= s; sK + v: N.x <= s + N.v
def affdim(P):
    if len(P) <= 1: return len(P) - 1
    D = [sub(p, P[0]) for p in P[1:]]
    r = 0
    if any(not iszero(d) for d in D): r = 1
    for a, b in itertools.combinations(D, 2):
        if not iszero(cr(a, b)): r = 2
        for c in D:
            if det3(list(a), list(b), list(c)) != 0: return 3
    return r
def name_shell(v):
    a = sorted(abs(int(x.a)) for x in v); return '(' + ','.join(map(str, a[::-1])) + ')'
SMAX = QF(3)
def part_B():
    print('== PART B: octet thresholds (exact; cube side 2, sites on L = even-sum integer vectors; range 0 < s <= 3)', flush=True)
    R = {}
    a, b = ONE / (PHI * PHI), IPHI
    I = [V3(*p) for p in orbit_cs((Z, a, b))]
    check('B0 Pacioli icosahedron: corners divide the octahedron edges in the golden ratio (|x|_1 = 1, ratio phi)', all(sum((x if sgn(x) >= 0 else -x for x in p), Z) == 1 for p in I) and b / a == PHI and a + b == 1)
    FI = hull_facets(I); NI = [N for N, idx in FI]
    check('B0 icosahedron: 20 facets', len(FI) == 20 and all(len(idx) == 3 for N, idx in FI))
    layer = [N for N in NI if all(abs(x) == 1 for x in N)]
    check('B0 s = 1: 8 faces lie in the octahedron face planes |x|+|y|+|z| = 1 (the octet layer planes)', len(layer) == 8)
    rect = [p for p in I if p[0] == 0]
    check('B0 s = 1: the 4 corners with x = 0 form a golden rectangle in the cube plane x = 0 through the site (side ratio phi)',
          len(rect) == 4 and (2 * b) / (2 * a) == PHI)
    # nest dodecahedron = face centres of I
    Dd = [mul(add(add(I[idx[0]], I[idx[1]]), I[idx[2]]), QF(Fr(1, 3))) for N, idx in FI]
    FD = hull_facets(Dd); ND = [N for N, idx in FD]
    check('B0 nest dodecahedron (face centres of the icosahedron): 20 corners, 12 pentagons, regular',
          len(FD) == 12 and all(len(idx) == 5 for N, idx in FD) and len(describe(Dd)['edge2']) == 1)
    check('B0 gauge control: every corner of K has gauge exactly 1', all(gauge(NI, p) == 1 for p in I) and all(gauge(ND, p) == 1 for p in Dd))
    R2I = qmax([dv(p, p) for p in I]); R2D = qmax([dv(p, p) for p in Dd])
    # ---- E1 first touch: sK and sK + v intersect iff s >= ||v||_{2K} = ||v||_K / 2 (K centrally symmetric); ||v||_K >= |v| / R
    def touches(Ns, R2, KV, label):
        assert all(neg(N) in Ns for N in Ns)                                # central symmetry
        cand = L_points(QF(36) * R2)                                       # all v with ||v||/2 <= 3 are in here
        vals = {}
        for v in cand:
            s = gauge(Ns, v) / 2
            if sgn(s - SMAX) <= 0: vals.setdefault(s, []).append(v)
        ss = sorted(vals, key=float)
        s1 = ss[0]; v1 = vals[s1][0]
        g, Nmax = argmax_facets(Ns, v1)
        C = contact_set(KV, s1, v1); dim = affdim(C)
        shells = sorted({name_shell(v) for v in vals[s1]})
        print(f'   {label}: touch values <= 3 (s, offsets, shell): ' + '; '.join(f'{ex(s)} = {fl(s)} x{len(vals[s])} {sorted({name_shell(v) for v in vals[s]})}' for s in ss), flush=True)
        return s1, vals, Nmax, C, dim, shells, len(cand)
    s1, vals, Nmax, C, dim, shells, ncand = touches(NI, R2I, I, 'icosahedra')
    check('B1 icosahedra first touch at s = sqrt5/2 exactly (minimum over all cells; the bound |v|^2 <= 36 R^2 leaves ' + str(ncand) + ' offsets)', s1 == QF(0, Fr(1, 2)), f'(s = {ex(s1)})')
    check('B1 first contact is face to face with a 2-dimensional overlap (one facet pair attains the gauge)', len(Nmax) == 1 and dim == 2,
          f'(offsets {len(vals[s1])} of shell {shells}, facet normal {[ex(x) for x in Nmax[0]]}, contact polygon of {len(C)} corners, dim {dim})')
    R['ico_touch'] = dict(s=ex(s1), offsets=len(vals[s1]), shell=shells, contact=f'{len(C)}-gon face to face' if dim == 2 else f'dim {dim}',
                          facet_normal=[ex(x) for x in Nmax[0]], later_values=[ex(s) for s in sorted(vals, key=float)[1:]])
    sD, valsD, NmaxD, CD, dimD, shellsD, ncD = touches(ND, R2D, Dd, 'dodecahedra')
    check('B6 dodecahedra first touch at s = 3/2 exactly', sD == QF(Fr(3, 2)), f'(s = {ex(sD)}; {len(valsD[sD])} offsets {shellsD}; contact dim {dimD}, {len(CD)} corners; facets attaining {len(NmaxD)})')
    R['dod_touch'] = dict(s=ex(sD), offsets=len(valsD[sD]), shell=shellsD, contact_dim=dimD, contact_corners=len(CD),
                          later_values=[ex(s) for s in sorted(valsD, key=float)[1:]])
    progress(0.45, 'touch thresholds')
    # ---- E2 tetrahedral-hole centres reached: min over sites c of ||t - c||_K
    def reached(Ns, R2, label):
        res = {}
        for t in (V3(Fr(1, 2), Fr(1, 2), Fr(1, 2)), V3(Fr(-1, 2), Fr(-1, 2), Fr(-1, 2))):
            B = QF(9) * R2; m = 4; vals = {}
            for c in itertools.product(range(-m, m + 1), repeat=3):
                if sum(c) % 2: continue
                w = sub(t, V3(*c))
                if sgn(dv(w, w) - B) > 0: continue
                s = gauge(Ns, w)
                if sgn(s - SMAX) <= 0: vals.setdefault(s, []).append(c)
            ss = sorted(vals, key=float); res[t] = (ss[0], vals[ss[0]], ss)
        return res
    rI = reached(NI, R2I, 'icosahedra')
    sI = [v[0] for v in rI.values()]
    check('B2 tetrahedral-hole centres (both kinds) are first reached at s = 3/2 exactly', all(x == QF(Fr(3, 2)) for x in sI),
          f'(reached by {len(list(rI.values())[0][1])} cells at once: the 4 octahedra sharing a face with the hole)')
    t0 = V3(Fr(1, 2), Fr(1, 2), Fr(1, 2)); c0 = V3(*list(rI.values())[0][1][0])
    g, Nm = argmax_facets(NI, sub(t0, c0))
    check('B2 the hole centre lies on a grown layer face (normal (+-1,+-1,+-1)), in its interior (one facet attains the gauge)',
          len(Nm) == 1 and all(abs(x) == 1 for x in Nm[0]))
    R['hole_centres'] = dict(s=ex(sI[0]), cells=len(list(rI.values())[0][1]), on='a layer-plane face (centre of the grown face)')
    # ---- E3 full cover at s = phi
    E = [V3(1, 0, 0), V3(0, 1, 0), V3(0, 0, 1)]
    gv = [gauge(NI, p) for p in E + [neg(p) for p in E]]
    check('B3 (i) the octahedron corners have gauge exactly phi: O subset of phi I, so at s = phi every octahedron is covered', all(x == PHI for x in gv))
    # (ii) tetrahedron T = conv(e1, e2, e3, (1,1,1)) of the octet (cell at the site 0 shares the face e1 e2 e3); split T into 4 cones from
    # its centre t; the cone over each face lies in phi I + c(face) if all 4 of its corners do
    Tc = [V3(1, 0, 0), V3(0, 1, 0), V3(0, 0, 1), V3(1, 1, 1)]
    t = mul(add(add(Tc[0], Tc[1]), add(Tc[2], Tc[3])), QF(Fr(1, 4)))
    okT = True; worst = Z
    for face in itertools.combinations(range(4), 3):
        P = [Tc[i] for i in face]
        # the octahedron on the far side of the face: its site c is the lattice point with P inside |x - c|_1 <= 1 and c not the 4th corner side
        cs = [V3(*c) for c in itertools.product(range(-1, 3), repeat=3) if sum(c) % 2 == 0 and all(sum(abs(float(x)) for x in sub(p, V3(*c))) == 1 for p in P)]
        if len(cs) != 1: okT = False; continue
        c = cs[0]
        gs = [gauge(NI, sub(p, c)) for p in P + [t]]
        worst = qmax([worst] + gs)
        okT &= all(sgn(x - PHI) <= 0 for x in gs)
    check('B3 (ii) each of the 4 cones of a tetrahedral hole lies in the grown icosahedron of its face-neighbour at s = phi (corners <= phi)', okT, f'(largest corner gauge {ex(worst)})')
    # (iii) lower bound: the octet corner e1 is at gauge >= phi from every site
    w1 = V3(1, 0, 0); B = PHI * PHI * QF(4) * R2I   # any site with gauge <= phi is within |w| <= phi R
    m = 4; gmin = None; nmin = 0
    for c in itertools.product(range(-m, m + 1), repeat=3):
        if sum(c) % 2: continue
        w = sub(w1, V3(*c))
        if sgn(dv(w, w) - B) > 0: continue
        gw = gauge(NI, w)
        if gmin is None or sgn(gw - gmin) < 0: gmin, nmin = gw, 1
        elif gw == gmin: nmin += 1
    check('B3 (iii) the octet corners are reached only at s = phi (by their 6 neighbouring cells): below phi they are uncovered', gmin == PHI and nmin == 6)
    # (iv) last points: inside an octahedron the gauge reaches phi only at corners iff no two adjacent corners share a facet of phi I
    share = [(i, j) for i, j in itertools.combinations(E + [neg(p) for p in E], 2) if dv(i, j) == 0 and any(dv(N, i) == PHI and dv(N, j) == PHI for N in NI)]
    check('B3 (iv) no edge of the octahedron lies on a facet of phi I, and the hole centre is at 3/2 < phi: the octet corners are the ONLY last points covered',
          len(share) == 0 and sgn(QF(Fr(3, 2)) - PHI) < 0)
    R['cover'] = dict(s=ex(PHI), last_points='the octet corners only (each reached by 6 cells at once)')
    progress(0.60, 'cover threshold')
    # ---- E4 coplanar faces of neighbours meet: per facet F (normal N), v in L with N.v = 0; sF and sF + v meet iff s >= ||v||_{F-F}
    def coplanar(KV, FK, label):
        rows = []
        for N, idx in FK:
            P = [KV[i] for i in idx]
            Dif = list({sub(p, r) for p in P for r in P if p != r})
            lines = []
            for p, r in itertools.combinations(Dif, 2):
                mvec = cr(sub(r, p), N)
                if iszero(mvec): continue
                sides = {sgn(dv(mvec, sub(x, p))) for x in Dif} - {0}
                if len(sides) == 1:
                    h = dv(mvec, p)
                    if h == 0: continue
                    M = mul(mvec, ONE / h)
                    if M not in lines: lines.append(M)
            Rp2 = qmax([dv(x, x) for x in Dif])
            B = QF(9) * Rp2; mm = int(math.floor(math.sqrt(float(B)))) + 1
            vals = {}
            for v in itertools.product(range(-mm, mm + 1), repeat=3):
                if sum(v) % 2 or not any(v): continue
                v = V3(*v)
                if dv(N, v) != 0 or sgn(dv(v, v) - B) > 0: continue
                s = qmax([dv(M, v) for M in lines])
                if sgn(s - SMAX) <= 0: vals.setdefault(s, []).append(v)
            rows.append((N, idx, vals, len(lines)))
        return rows
    def meet_contact(KV, N, idx, s, v):
        """corners of sF cap (sF + v) in the plane of F (exact): dimension and kind"""
        P = [mul(KV[i], s) for i in idx]
        # order the polygon's corners: edges are pairs of P whose line leaves all others on one side
        edges = []
        for a_, b_ in itertools.combinations(range(len(P)), 2):
            mvec = cr(sub(P[b_], P[a_]), N)
            sides = {sgn(dv(mvec, sub(x, P[a_]))) for x in P} - {0}
            if len(sides) == 1: edges.append((a_, b_, sides.pop()))
        def inside(x, Q):
            for a_, b_, sd in edges:
                if sgn(dv(cr(sub(Q[b_], Q[a_]), N), sub(x, Q[a_]))) * sd < 0: return False
            return True
        Q = [add(p, v) for p in P]
        pts = set(p for p in P if inside(p, Q)) | set(x for x in Q if inside(x, P))
        for a_, b_, _ in edges:
            for c_, d_, _ in edges:
                p0, p1, q0, q1 = P[a_], P[b_], Q[c_], Q[d_]
                den = dv(cr(sub(p1, p0), sub(q1, q0)), N)
                if den == 0: continue
                al = dv(cr(sub(q0, p0), sub(q1, q0)), N) / den; be = dv(cr(sub(q0, p0), sub(p1, p0)), N) / den
                if sgn(al) >= 0 and sgn(al - 1) <= 0 and sgn(be) >= 0 and sgn(be - 1) <= 0: pts.add(add(p0, mul(sub(p1, p0), al)))
        pts = list(pts); dim = affdim(pts)
        kind = 'none'
        if dim == 0:
            p = pts[0]; kind = 'corner to corner' if (p in P and p in Q) else 'corner on edge'
            if kind == 'corner on edge':                                    # where on the edge: exact fraction from its nearer end
                for G in (P, Q):
                    if p in G: continue
                    for a_, b_, _ in edges:
                        A_, B_ = G[a_], G[b_]
                        if iszero(cr(sub(p, A_), sub(B_, A_))):
                            t_ = dv(sub(p, A_), sub(B_, A_)) / dv(sub(B_, A_), sub(B_, A_)); t_ = qmin([t_, 1 - t_])
                            kind = f'corner on edge, at {ex(t_)} of the edge from its nearer end'
        elif dim == 1:
            L2 = qmax([d2(x, y) for x in pts for y in pts]); e2 = qmin([d2(P[a_], P[b_]) for a_, b_, _ in edges])
            kind = 'edge to edge (a whole edge)' if L2 == e2 else f'edge to edge (segment, length^2 {ex(L2)})'
        elif dim == 2: kind = 'overlap with area'
        return kind, dim
    def fam_key(N): return tuple(sorted((abs(float(x)) for x in N)))
    for KV, FK, label, claims in ((I, FI, 'icosahedra', {'layer': QF(1, Fr(1, 2)), 'golden': PHI * PHI}), (Dd, FD, 'dodecahedra', {'all': QF(3)})):
        rows = coplanar(KV, FK, label)
        fams = {}
        for N, idx, vals, nl in rows:
            kind = 'layer' if (label == 'icosahedra' and all(abs(x) == 1 for x in N)) else ('golden' if label == 'icosahedra' else 'all')
            if not vals: fams.setdefault(kind, []).append((N, None, [], None, None)); continue
            ss = sorted(vals, key=float); s0 = ss[0]
            ck, cd = meet_contact(KV, N, idx, s0, vals[s0][0])
            fams.setdefault(kind, []).append((N, s0, vals[s0], ss, ck))
        for kind, items in fams.items():
            s0s = {x[1] for x in items}
            s0 = list(s0s)[0]
            nco = sorted({len(x[2]) for x in items}); kinds = sorted({x[4] for x in items})
            allv = sorted({s for x in items for s in (x[3] or [])}, key=float)
            print(f'   {label} {kind} faces ({len(items)} per cell): coplanar faces first meet at s = {ex(s0)} = {fl(s0)} with {nco} neighbours; contact {kinds}; all meet values <= 3: {[ex(s) for s in allv]}', flush=True)
            check(f'B4 {label} {kind} faces: coplanar neighbouring faces first meet at s = {ex(claims[kind])} exactly (every face of the family)',
                  len(s0s) == 1 and s0 == claims[kind], f'(found {[ex(s) for s in s0s]}; contact {kinds})')
            R[f'{label}_{kind}_meet'] = dict(s=ex(s0), faces=len(items), neighbours_meeting=nco, contact=kinds, all_values_le_3=[ex(s) for s in allv])
        allfaces = sum(len(v) for v in fams.values())
        check(f'B4 {label}: every face ({allfaces}) has coplanar neighbours and falls into the families above', allfaces == len(FK) and all(x[1] is not None for v in fams.values() for x in v))
    progress(0.80, 'coplanar faces')
    OUT['B'] = R

# ================================================================ PART C: discs (the #87 definition and the 11-11 plane count)
def recog(x):
    """x (float) = a + b sqrt5 with a, b in Z/4, |a|, |b| <= 3: unique match within 1e-9, else None"""
    hits = []
    for bq in range(-12, 13):
        a = x - bq / 4 * math.sqrt(5); aq = round(a * 4)
        if abs(aq) <= 12 and abs(aq / 4 + bq / 4 * math.sqrt(5) - x) < 1e-9: hits.append(QF(Fr(aq, 4), Fr(bq, 4)))
    return hits[0] if len(hits) == 1 else None
def edges_of_faces(F):
    E = set()
    for f in F:
        for i in range(len(f)): E.add(tuple(sorted((f[i], f[(i + 1) % len(f)]))))
    return sorted(E)
def disc_census(V, E, label):
    """(1) 11-11 census: central planes through the edges, a disc = plane with >= 3 edges; (2) #87: fins O-A-B joined into flat sheets
    across shared corner rays (coplanar, on opposite sides of the ray); a central disc = a sheet whose apex angles sum to 2 pi, decided
    exactly: the sheet's fins form one closed cycle of corners and wind once round O (count of fins containing a fixed in-plane ray)."""
    planes = {}; through = 0
    for a, b in E:
        n = cr(V[a], V[b])
        if iszero(n): through += 1; continue
        k = next(i for i in range(3) if n[i] != 0); n = mul(n, ONE / n[k])        # primitive exact key: first nonzero coordinate = 1
        planes.setdefault(n, []).append((a, b))
    per = {}
    for p, l in planes.items(): per[len(l)] = per.get(len(l), 0) + 1
    discs_plane = {p: l for p, l in planes.items() if len(l) >= 3}
    # #87 sheets
    fins = list(E); pf = list(range(len(fins)))
    def fp(x):
        while pf[x] != x: pf[x] = pf[pf[x]]; x = pf[x]
        return x
    at = {}
    for i, (a, b) in enumerate(fins):
        at.setdefault(a, []).append(i); at.setdefault(b, []).append(i)
    for v, l in at.items():
        for i, j in itertools.combinations(l, 2):
            a = [x for x in fins[i] if x != v][0]; b = [x for x in fins[j] if x != v][0]
            if det3(list(V[v]), list(V[a]), list(V[b])) == 0 and sgn(dv(cr(V[v], V[a]), cr(V[v], V[b]))) < 0: pf[fp(i)] = fp(j)
    comp = {}
    for i in range(len(fins)): comp.setdefault(fp(i), []).append(i)
    discs87 = []; apex_float_agree = True; open_full = 0
    for r, l in comp.items():
        deg = {}
        for i in l:
            for x in fins[i]: deg[x] = deg.get(x, 0) + 1
        closed = all(d == 2 for d in deg.values()) and len(l) >= 3
        apex = sum(math.acos(max(-1, min(1, float(dv(V[a], V[b])) / math.sqrt(float(dv(V[a], V[a])) * float(dv(V[b], V[b])))))) for a, b in (fins[i] for i in l))
        w = None
        if closed:
            # connected single cycle?
            seen = {fins[l[0]][0]}; frontier = [fins[l[0]][0]]
            while frontier:
                x = frontier.pop()
                for i in l:
                    if x in fins[i]:
                        y = fins[i][0] if fins[i][1] == x else fins[i][1]
                        if y not in seen: seen.add(y); frontier.append(y)
            closed = len(seen) == len(deg)
        if closed:
            m = cr(V[fins[l[0]][0]], V[fins[l[0]][1]])
            for cand in (V3(1, 0, 0), V3(0, 1, 0), V3(0, 0, 1), V3(1, 2, 3), V3(3, 1, 7)):
                rr = cr(m, cand)
                if iszero(rr) or any(iszero(cr(rr, V[x])) for x in deg): continue
                break
            w = 0
            for i in l:
                a, b = fins[i]; o = sgn(dv(cr(V[a], V[b]), m))
                if sgn(dv(cr(V[a], rr), m)) == o and sgn(dv(cr(rr, V[b]), m)) == o: w += 1
        is_disc = closed and w == 1
        if (abs(apex - 2 * math.pi) < 1e-9) != is_disc: apex_float_agree = False
        if not closed and abs(apex - 2 * math.pi) < 1e-9: open_full += 1
        if is_disc:
            n = cr(V[fins[l[0]][0]], V[fins[l[0]][1]]); k = next(i for i in range(3) if n[i] != 0)
            discs87.append((mul(n, ONE / n[k]), len(l)))
    sizes87 = {}
    for n, k in discs87: sizes87[k] = sizes87.get(k, 0) + 1
    sheet_of = {fins[i]: fp(i) for i in range(len(fins))}
    return dict(planes=planes, per_plane=dict(sorted(per.items())), discs_plane=discs_plane, through=through, sheet_of=sheet_of,
                discs87=discs87, sizes87=dict(sorted(sizes87.items())), sheets=len(comp), apex_float_agree=apex_float_agree, open_full=open_full)
def convex_solid(V):
    Fs = hull_facets(V); return edges_from_facets(V, Fs)
def part_C_controls():
    print('== PART C controls: discs of convex solids (exact; both definitions)', flush=True)
    sols = {
        'octahedron': [V3(*p) for p in allperm_cs((1, 0, 0))],
        'cube': [V3(*p) for p in itertools.product((1, -1), repeat=3)],
        'cuboctahedron': [V3(*p) for p in allperm_cs((1, 1, 0))],
        'icosidodecahedron': [V3(*p) for p in allperm_cs((0, 0, PHI))] + [V3(*p) for p in orbit_cs((Fr(1, 2), PHI / 2, PHI * PHI / 2))],
        'dodecahedron': [V3(*p) for p in itertools.product((1, -1), repeat=3)] + [V3(*p) for p in orbit_cs((Z, IPHI, PHI))],
    }
    sols['icosidodecahedron'] = list(dict.fromkeys(sols['icosidodecahedron']))
    want = {'octahedron': {4: 3}, 'cube': {}, 'cuboctahedron': {6: 4}, 'icosidodecahedron': {10: 6}, 'dodecahedron': {}}
    R = {}
    for name, V in sols.items():
        E = convex_solid(V); c = disc_census(V, E, name)
        pl = {k: v for k, v in c['per_plane'].items() if k >= 3}
        R[name] = dict(corners=len(V), edges=len(E), planes_per_edges=c['per_plane'], discs87=c['sizes87'])
        kind = 'NEGATIVE' if name in ('cube', 'dodecahedron') else 'POSITIVE'
        check(f'C0 {kind} {name}: {len(V)} corners, {len(E)} edges; #87 discs {c["sizes87"]} and planes with >= 3 edges {pl} (expect {want[name]})',
              c['sizes87'] == want[name] and pl == want[name] and c['apex_float_agree'])
    OUT['C_controls'] = R
def icosa_mirrors(orient):
    """15 mirror normals (primitive keys) of the icosahedral group of the icosahedron cyclic(0, +-1, +-phi) (orient 'a') or
    cyclic(0, +-phi, +-1) (orient 'b'): perpendicular to the 2-fold axes = the edge midpoints"""
    ICO = [V3(*p) for p in orbit_cs((Z, ONE, PHI) if orient == 'a' else (Z, PHI, ONE))]
    E = convex_solid(ICO); ks = set()
    for i, j in E:
        n = add(ICO[i], ICO[j]); k = next(t for t in range(3) if n[t] != 0); ks.add(mul(n, ONE / n[k]))
    return ks
def part_C_dogstar():
    print('== PART C: Dogstar (exact)', flush=True)
    d = json.load(open(os.path.join(STUD, '2026-11-11-orbit-polytopes', 'data', 'dogstar_vacuus.json')))
    Vf, F = d['V'], [list(f) for f in d['F']]
    V = []
    for p in Vf:
        r = [recog(x) for x in p]
        if any(x is None for x in r): check('C1 every Dogstar coordinate recognised in Q(sqrt5)/4', False, str(p)); return
        V.append(tuple(r))
    check('C1 all 168 coordinates recognised uniquely as (a + b sqrt5)/4 (|registry - exact| < 1e-9)', True)
    check('C1 56 distinct corners, centroid exactly 0', len(set(V)) == 56 and iszero(mul(tuple(sum((p[i] for p in V), Z) for i in range(3)), ONE)))
    E = edges_of_faces(F)
    def newell(f):
        n = (Z, Z, Z)
        for i in range(len(f)): n = add(n, cr(V[f[i]], V[f[(i + 1) % len(f)]]))
        return n
    planar = all(not iszero(newell(f)) and all(dv(newell(f), sub(V[x], V[f[0]])) == 0 for x in f) for f in F)
    check('C1 every one of the 84 faces is exactly planar', planar and len(F) == 84)
    # closed oriented surface: every directed edge once, reversed once
    dire = {}
    for f in F:
        for i in range(len(f)): dire[(f[i], f[(i + 1) % len(f)])] = dire.get((f[i], f[(i + 1) % len(f)]), 0) + 1
    closed = all(c == 1 for c in dire.values()) and all((b, a) in dire for a, b in dire)
    check('C1 closed oriented surface: each of the 138 edges in exactly 2 faces, opposite directions; V - E + F = 2', closed and len(E) == 138 and 56 - 138 + 84 == 2)
    # face normals (Newell, exact), signed cone volumes from O
    cones = []
    for f in F:
        n = (Z, Z, Z)
        for i in range(len(f)): n = add(n, cr(V[f[i]], V[f[(i + 1) % len(f)]]))
        cones.append(dv(n, V[f[0]]) / 6)
    vol = sum(cones, Z); sgns = {sgn(c) for c in cones}
    if sgn(vol) < 0: vol = -vol; sgns = {-x for x in sgns}
    check('C1 volume exactly phi/2 = cube of edge phi minus the six roofs of the neighbouring dodecahedra (2 phi^3 - (15 + 7 sqrt5)/4)',
          vol == PHI / 2 and 2 * (PHI * PHI * PHI) - QF(Fr(15, 4), Fr(7, 4)) == PHI / 2, f'(volume {ex(vol)})')
    central = sum(1 for c in cones if c == 0)
    check('C1 every face cone from O has positive volume (O on the inner side of every face plane; #87 Theorem 1: the Vacuus is well defined)', sgns == {1})
    # independent identity: every face plane is a plane of the cube [-phi/2, phi/2]^3 or of a dodecahedron (edge 1) centred at +-phi e_i
    DODc = [mul(p, PHI / 2) for p in [V3(*p) for p in itertools.product((1, -1), repeat=3)] + [V3(*p) for p in orbit_cs((Z, IPHI, PHI))]]
    DODc2 = [mul(p, PHI / 2) for p in [V3(*p) for p in itertools.product((1, -1), repeat=3)] + [V3(*p) for p in orbit_cs((Z, PHI, IPHI))]]
    def planes_dod(Dv):
        out = set()
        for N, idx in hull_facets(Dv):
            for i in range(3):
                for sg_ in (1, -1):
                    c = [Z, Z, Z]; c[i] = PHI * sg_; c = tuple(c)
                    # N.(x - c) = 1  ->  N.x = 1 + N.c ; key (N, rhs)
                    out.add((N, 1 + dv(N, c)))
        return out
    cubepl = set()
    for i in range(3):
        for sg_ in (1, -1):
            N = [Z, Z, Z]; N[i] = ONE; cubepl.add((tuple(N), PHI / 2 * sg_))
    def key_plane(f):
        n = newell(f); h = dv(n, V[f[0]])
        return n, h
    def on(f, Pset):
        n, h = key_plane(f)
        for N, r in Pset:
            if iszero(cr(n, N)):
                lam = next(n[i] / N[i] for i in range(3) if N[i] != 0)
                if h == lam * r: return True
        return False
    res = {}
    for nm, Dv in (('a', DODc), ('b', DODc2)):
        Pd = planes_dod(Dv); res[nm] = all(on(f, cubepl | Pd) for f in F)
    orient = 'a' if res['a'] else ('b' if res['b'] else None)
    check('C1 identity: every face lies on a face plane of the cube or of one of the six neighbouring dodecahedra (all of one orientation)',
          orient is not None, f'(orientation {orient}: dodecahedra with corners (phi/2) x cyclic(0, +-{"1/phi, +-phi" if orient == "a" else "phi, +-1/phi"}))')
    check('C1 central faces (face plane through O): exactly 0 (the draft says 1; the 11-11 census JSON already had 0)', central == 0, f'(central faces = {central})')
    # symmetry: signed permutations preserving corners and faces
    G = []
    for perm in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            g = lambda p: tuple(p[perm[i]] * s[i] for i in range(3))
            img = [g(p) for p in V]
            if set(img) != set(V): continue
            idx = {p: i for i, p in enumerate(V)}
            fs = {frozenset(f) for f in F}
            if all(frozenset(idx[g(V[x])] for x in f) in fs for f in F): G.append((perm, s))
    check('C1 symmetry: exactly 24 signed permutations keep the Dogstar (pyritohedral group, order 24; not the full octahedral 48)', len(G) == 24)
    c = disc_census(V, E, 'Dogstar')
    pp = c['per_plane']; on3 = sum(len(l) for l in c['discs_plane'].values())
    print(f'   Dogstar: {len(c["planes"])} central edge planes, edges per plane {pp}; edges through O {c["through"]}; planes with >= 3 edges: {len(c["discs_plane"])} carrying {on3}', flush=True)
    print(f'   Dogstar #87: {c["sheets"]} flat sheets; central discs (closed, winding once) {c["sizes87"]}; float apex sums agree with the exact test: {c["apex_float_agree"]}', flush=True)
    check('C2 11-11 count: 27 central planes; 12 carry 8 edges, 3 carry 6, 12 carry 2; 114 of 138 edges on the 15 planes with >= 3 edges',
          len(c['planes']) == 27 and pp == {2: 12, 6: 3, 8: 12} and on3 == 114 and c['through'] == 0, f'(found {len(c["planes"])}, {pp}, {on3})')
    n87 = sum(c['sizes87'].values()); e87 = sum(k * v for k, v in c['sizes87'].items())
    check('C2 #87 definition: the central discs (closed sheets, apex angles summing to 2 pi)', True, f'= {c["sizes87"]}: {n87} discs carrying {e87} of 138 edges')
    check('C2 the #87 exact test agrees with the float apex-angle sum on every sheet', c['apex_float_agree'])
    disc_normals_87 = {n for n, k in c['discs87']}
    plane_normals = set(c['discs_plane'])
    print(f'   FINDING: the #87 discs and the 15 planes with >= 3 edges coincide: {disc_normals_87 == plane_normals} ({len(disc_normals_87)} #87 discs vs {len(plane_normals)} planes)', flush=True)
    # anatomy of each plane with >= 3 edges: its fins split into flat sheets (#87 joining rule); per sheet: fins, corners of degree 1
    # (open ends), angle swept round O (float, for reading only), and how much of the full turn the plane's fins cover together
    anat = {}; FANCOS = {}; fanok = []
    for p_, l in sorted(c['discs_plane'].items(), key=lambda kv: (-len(kv[1]), [float(x) for x in kv[0]])):
        sh = {}
        for e in l: sh.setdefault(c['sheet_of'][e], []).append(e)
        desc = []
        for r_, fl_ in sh.items():
            deg = {}
            for a_, b_ in fl_:
                deg[a_] = deg.get(a_, 0) + 1; deg[b_] = deg.get(b_, 0) + 1
            ang = sum(math.degrees(math.acos(max(-1, min(1, float(dv(V[a_], V[b_])) / math.sqrt(float(dv(V[a_], V[a_])) * float(dv(V[b_], V[b_]))))))) for a_, b_ in fl_)
            ends = [v_ for v_, k_ in deg.items() if k_ == 1]
            if len(ends) == 2:                                              # exact cos of the fan's opening (angle between its end rays)
                A_, B_ = V[ends[0]], V[ends[1]]; dd = dv(A_, B_)
                c2 = dd * dd / (dv(A_, A_) * dv(B_, B_)); csign = '-' if sgn(dd) < 0 else '+'
                exact_cos = f'cos = {csign}sqrt({ex(c2)})'; FANCOS[exact_cos] = (-1 if csign == '-' else 1) * math.sqrt(float(c2))
            else: exact_cos = None
            desc.append((len(fl_), len(ends), round(ang, 3), exact_cos)); fanok.append(exact_cos is not None and abs(math.degrees(math.acos(FANCOS[exact_cos])) - ang) < 1e-9)
        desc.sort(reverse=True)
        tot = round(sum(x[2] for x in desc), 3)
        key = (len(l), tuple(desc), tot)
        anat[key] = anat.get(key, 0) + 1
    for (ne, desc, tot), k in anat.items():
        print(f'   anatomy: {k} plane(s) with {ne} edges -> {len(desc)} flat sheets (fins, open ends, degrees swept, exact opening) {list(desc)}; fins sweep {tot} deg of 360 in all', flush=True)
    OUT['C_dogstar_anatomy'] = [dict(planes=k, edges=ne, sheets=[dict(fins=a_, open_ends=b_, degrees=c_, opening=d_) for a_, b_, c_, d_ in desc], degrees_swept=tot) for (ne, desc, tot), k in anat.items()]
    check(f'C2 every fan opening (exact cos of the angle between its end rays) equals the sum of its fin angles (float, 1e-9; {len(fanok)} fans)', all(fanok))
    check('C2 every Dogstar plane with >= 3 edges has open sheets only (no closed loop of fins round O)', all(x[1] > 0 for (ne, desc, tot) in anat for x in desc))
    # each 8-plane / 6-plane: do its edges form ONE closed loop round O?
    loops = {}
    for p, l in c['discs_plane'].items():
        loops.setdefault(len(l), []).append(p in disc_normals_87)
    print(f'   Dogstar: planes with >= 3 edges that are #87 discs, by size: { {k: f"{sum(v)} of {len(v)}" for k, v in loops.items()} }', flush=True)
    MA, MB = icosa_mirrors('a'), icosa_mirrors('b')
    coord = {V3(1, 0, 0), V3(0, 1, 0), V3(0, 0, 1)}
    which = 'a' if plane_normals == MA else ('b' if plane_normals == MB else None)
    check('C3 the 15 disc planes are exactly the 15 mirror planes of one icosahedral group containing the Dogstar\'s group', which is not None,
          f'(the group of the icosahedron cyclic(0, +-{"1, +-phi" if which == "a" else "phi, +-1"}))')
    check('C3 3 of them are the coordinate planes (the 6-edge planes) and 12 are golden (the 8-edge planes)',
          {p for p, l in c['discs_plane'].items() if len(l) == 6} == coord and len([p for p, l in c['discs_plane'].items() if len(l) == 8]) == 12)
    # which disc planes are mirrors of the Dogstar itself
    def reflect(n, p):
        k = dv(n, p) / dv(n, n); return sub(p, mul(n, 2 * k))
    fs = {frozenset(f) for f in F}; idx = {p: i for i, p in enumerate(V)}
    mir = []
    for n in plane_normals:
        img = [reflect(n, p) for p in V]
        if set(img) == set(V) and all(frozenset(idx[reflect(n, V[x])] for x in f) in fs for f in F): mir.append(n)
    check('C3 only the 3 coordinate planes are mirrors of the Dogstar itself', set(mir) == coord, f'({len(mir)} mirrors among the 15)')
    share = Fr(on3, 138)
    OUT['C_dogstar'] = dict(corners=56, edges=138, faces=84, faces_by_size={3: sum(1 for f in F if len(f) == 3), 4: sum(1 for f in F if len(f) == 4)},
                            volume=ex(vol), central_faces=central, symmetry_order=len(G), central_planes=len(c['planes']), edges_per_plane=pp,
                            discs_1111=len(c['discs_plane']), edges_on_discs=on3, share=f'{share} = {float(share):.4f}',
                            discs_87=c['sizes87'], discs_87_equal_plane_discs=disc_normals_87 == plane_normals,
                            mirror_planes=f'icosahedral group of orientation {which}', own_mirrors=len(mir), dodecahedra_orientation=orient)

if __name__ == '__main__':
    part_C_controls(); progress(0.10, 'disc controls')
    part_A(); progress(0.30, 'part A')
    if not PILOT:
        part_B(); progress(0.85, 'part B')
        part_C_dogstar(); progress(0.97, 'part C Dogstar')
    json.dump(OUT, open(os.path.join(HERE, '..', 'data', 'platonic-exact' + ('-pilot' if PILOT else '') + '.json'), 'w'), indent=1, default=str)
    print(f'{NCHK[0]} checks, {NCHK[1]} failed, {time.time() - T0:.0f} s')
    print('FINAL ok: all checks and controls held' if NCHK[1] == 0 else 'FINAL FAIL')
