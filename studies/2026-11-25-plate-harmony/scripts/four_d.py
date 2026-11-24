"""Harmony tests for the 4D Queens' walls (plate-harmony study, 25 Nov 2026), exact.

The 600-cell (corners: the 120 unit icosians, here doubled to have entries in Z[phi]) is rebuilt; its 600 facets are the
4-cliques of its edge graph, its 1200 ridges the triangles. Resonus(600-cell) = hyperplanes through O parallel to the facets
(normals = facet corner sums, 300 hyperplanes); Vacuus(600-cell) = hyperplanes through O and each ridge (60). By study
2026-11-24-resonus-4d (Theorem 3 and its table) the 120-cell's Resonus and Vacuus are both the 60 mirrors of H4, the same
arrangement as the 600-cell's Vacuus, so two arrangements are tested: H4 (60) and the 300 (normals along the 120-cell's corners).

Exact arithmetic: integers a + b phi as int pairs (phi^2 = phi + 1); vectors are compared up to scale by a canonical key
(multiply by the conjugate of the first nonzero entry, divide by the gcd). Intersection lattice: 2-flats (pairs grouped by their
Pluecker coordinates), lines (rank-3 flats: each 2-flat cut by every other hyperplane, grouped). Moebius function and
characteristic polynomial chi(t) (Orlik-Solomon); regions |chi(-1)| (Zaslavsky); simplicial when the chambers' facet count
2 sum_H r(A^H) equals 4 r(A). Angles and pencils as in harmony.py (rational multiples of pi by minimal polynomials, exact).
Coxeter plane: simple roots of H4 found exactly (positive roots whose reflection permutes the other positive roots), Coxeter
element c = s1 s2 s3 s4, Coxeter plane = kernel of c^2 - 2cos(2pi/30) c + 1 over Q(cos(2pi/30)) (degree 4, contains sqrt5);
each hyperplane's trace on it is tested for a regular pencil of lines."""
import os, sys, json, itertools, time
from math import gcd
from fractions import Fraction as Fr
from collections import Counter
import multiprocessing as mpr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from nf import NF, rational_angle, cheb_C
from flint import arb, fmpz_poly

T0 = time.time()
def say(*a): print(f"[{time.time() - T0:7.1f} s]", *a, flush=True)

# ---------------------------------------------------------------- Z[phi]
def m(x, y): return (x[0] * y[0] + x[1] * y[1], x[0] * y[1] + x[1] * y[0] + x[1] * y[1])
def ad(x, y): return (x[0] + y[0], x[1] + y[1])
def sb(x, y): return (x[0] - y[0], x[1] - y[1])
def ng(x): return (-x[0], -x[1])
def conj(x): return (x[0] + x[1], -x[1])
Z = (0, 0)
def dotz(u, v):
    s = Z
    for a, b in zip(u, v): s = ad(s, m(a, b))
    return s
def isz(x): return x[0] == 0 and x[1] == 0
def sgn(x):
    """exact sign of a + b phi = ((2a + b) + b sqrt5)/2"""
    p, q = 2 * x[0] + x[1], x[1]
    if q == 0: return (p > 0) - (p < 0)
    if p == 0: return (q > 0) - (q < 0)
    if p > 0 and q > 0: return 1
    if p < 0 and q < 0: return -1
    d = p * p - 5 * q * q
    return (1 if p > 0 else -1) if d > 0 else (1 if q > 0 else -1)

def key(v):
    c = next(x for x in v if not isz(x))
    w = [m(x, conj(c)) for x in v]
    g = 0
    for x in w: g = gcd(g, gcd(abs(x[0]), abs(x[1])))
    w = [(x[0] // g, x[1] // g) for x in w]
    f = next(x for x in w if not isz(x))
    if f[0] < 0 or (f[0] == 0 and f[1] < 0): w = [ng(x) for x in w]
    return tuple(w)

def det3(a, b, c):
    t1 = m(a[0], sb(m(b[1], c[2]), m(b[2], c[1])))
    t2 = m(a[1], sb(m(b[0], c[2]), m(b[2], c[0])))
    t3 = m(a[2], sb(m(b[0], c[1]), m(b[1], c[0])))
    return ad(sb(t1, t2), t3)

def gcross(a, b, c):
    out = []
    for i in range(4):
        cols = [j for j in range(4) if j != i]
        d = det3([a[j] for j in cols], [b[j] for j in cols], [c[j] for j in cols])
        out.append(d if i % 2 == 0 else ng(d))
    return out

def plucker(u, v): return [sb(m(u[i], v[j]), m(u[j], v[i])) for i, j in itertools.combinations(range(4), 2)]

# ---------------------------------------------------------------- the 600-cell, doubled
def cell600():
    V = set()
    for i in range(4):
        for s in (2, -2):
            v = [Z] * 4; v[i] = (s, 0); V.add(tuple(v))
    for sg in itertools.product((1, -1), repeat=4): V.add(tuple((s, 0) for s in sg))
    base = [(0, 1), (1, 0), (-1, 1), Z]            # phi, 1, phi - 1, 0
    even = [p for p in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]
    for sg in itertools.product((1, -1), repeat=3):
        b = [(base[0][0] * sg[0], base[0][1] * sg[0]), (base[1][0] * sg[1], base[1][1] * sg[1]), (base[2][0] * sg[2], base[2][1] * sg[2]), Z]
        for p in even: V.add(tuple(b[p[i]] for i in range(4)))
    V = sorted(V)
    assert len(V) == 120 and all(dotz(v, v) == (4, 0) for v in V)
    return V

# ---------------------------------------------------------------- lattice
def flats2(N):
    X = {}
    for i, j in itertools.combinations(range(len(N)), 2):
        X.setdefault(key(plucker(N[i], N[j])), set()).update((i, j))
    return [frozenset(s) for s in X.values()]

def _lines_chunk(args):
    N, X2, ids = args
    L = {}
    for x in ids:
        S = X2[x]; a, b = sorted(S)[:2]
        for k in range(len(N)):
            if k in S: continue
            kk = key(gcross(N[a], N[b], N[k]))
            e = L.get(kk)
            if e is None: e = L[kk] = [set(), set()]
            e[0].update(S); e[0].add(k); e[1].add(x)
    return L

def lattice(N, procs):
    X2 = flats2(N)
    say("  2-flats", len(X2), Counter(len(s) for s in X2))
    ch = [list(range(i, len(X2), procs * 4)) for i in range(procs * 4)]
    L = {}
    with mpr.get_context("fork").Pool(procs) as pool:
        for part in pool.imap_unordered(_lines_chunk, [(N, X2, c) for c in ch]):
            for kk, (S, xs) in part.items():
                e = L.get(kk)
                if e is None: L[kk] = [S, xs]
                else: e[0] |= S; e[1] |= xs
    lines = [(frozenset(S), xs) for S, xs in L.values()]
    say("  lines", len(lines), Counter(len(S) for S, _ in lines))
    return X2, lines

def chi(n, X2, lines):
    muX = [len(S) - 1 for S in X2]
    s2 = sum(muX)
    muL = []
    for S, xs in lines:
        assert all(X2[x] <= S for x in xs)
        muL.append(-(1 - len(S) + sum(muX[x] for x in xs)))
    s3 = sum(muL)
    mu0 = -(1 - n + s2 + s3)
    return [1, -n, s2, s3, mu0]      # t^4 - n t^3 + s2 t^2 + s3 t + mu0

def int_roots(c):
    p = fmpz_poly(list(reversed(c)))
    fac = p.factor()[1]
    roots = []
    for f, e in fac:
        if f.degree() != 1: return None
        cf = f.coeffs(); roots += [-int(cf[0]) // int(cf[1])] * e
    return sorted(roots)

# ---------------------------------------------------------------- angles (exact in Q(sqrt5))
F5 = NF([-5, 0, 1], "2.2360679774997896964091736687312762354406183596115")
PHI5 = (F5.gen() + 1) / 2
def toF(x): return F5.c(x[0]) + PHI5 * x[1]

def analyse4(name, N, procs):
    n = len(N); out = {"name": name, "planes": n}
    say(name, n, "hyperplanes")
    X2, lines = lattice(N, procs)
    c = chi(n, X2, lines)
    R = abs(c[0] - c[1] + c[2] - c[3] + c[4])
    assert sum(c) == 0, "chi(1) != 0"
    out["chi_coefficients"] = c; out["regions"] = R
    rts = int_roots(c); out["p7_factors"] = rts is not None; out["exponents"] = rts
    out["two_flats"] = {str(k): v for k, v in sorted(Counter(len(s) for s in X2).items())}
    out["lines"] = {str(k): v for k, v in sorted(Counter(len(S) for S, _ in lines).items())}
    # simplicial: sum over hyperplanes of the regions of the restriction
    f0 = Counter(); f1 = Counter()
    for S, xs in lines:
        for H in S: f0[H] += 1
        for x in xs:
            for H in X2[x]:
                if H in S: f1[H] += 1
    facets = 2 * sum(2 * (1 - f0[H] + f1[H]) for H in range(n))
    out["simplicial"] = facets == 4 * R
    out["mean_facets_per_chamber"] = str(Fr(facets, R))
    # reflection arrangement
    keys = {key(v) for v in N}; nn = [dotz(v, v) for v in N]
    refl = all(key([sb(m(nn[i], N[j][t]), m(m((2, 0), dotz(N[j], N[i])), N[i][t])) for t in range(4)]) in keys
               for i in range(n) for j in range(n) if i != j)
    out["reflection"] = refl
    # angle classes
    cls = {}
    for i, j in itertools.combinations(range(n), 2):
        d = dotz(N[i], N[j]); q = m(d, d); den = m(nn[i], nn[j])
        cls.setdefault(key([q, den]), []).append((i, j))
    ang = {}; pa = {}
    for k, prs in cls.items():
        i, j = prs[0]; d = toF(dotz(N[i], N[j]))
        cc = d * d / (toF(nn[i]) * toF(nn[j])) * 4 - 2
        a = rational_angle(cc); ang[k] = a
        for pr in prs: pa[pr] = a
    out["angle_classes"] = len(cls)
    out["angles_over_pi"] = sorted(str(a) for a in set(ang.values()) if a is not None)
    out["p6_rational"] = all(a is not None for a in ang.values())
    out["p3_equiangular"] = len(cls) == 1
    # perpendicular triples
    adj = [set() for _ in range(n)]
    for (i, j), a in pa.items():
        if a == Fr(1, 2): adj[i].add(j); adj[j].add(i)
    sys.path.insert(0, HERE)
    from harmony import perp_triples
    out["p4_perp_triples"] = perp_triples(n, adj)
    # pencils around 2-flats
    pt = {}; allreg = True; lune = True; why = ""
    for S in X2:
        k = len(S); idx = sorted(S)
        prs = [pa[a, b] for a, b in itertools.combinations(idx, 2)]
        ok = all(a is not None and (a * k).denominator == 1 for a in prs)
        t = pt.setdefault(k, [0, 0]); t[0] += 1; t[1] += ok
        allreg = allreg and ok
        if lune:
            if any(a is None for a in prs): lune = False; why = "a pencil with an irrational angle"
            elif ok and Fr(R, 2 * k).denominator != 1: lune = False; why = f"a regular {k}-pencil: R/(2k) = {Fr(R, 2 * k)}"
            elif not ok: lune = None; why = "an irregular pencil with rational angles (gaps not resolved)"
    out["pencils"] = {str(k): {"count": v[0], "regular": v[1]} for k, v in sorted(pt.items())}
    out["max_pencil"] = max(pt)
    out["p9_all_pencils_regular"] = allreg
    if lune is False: out["p5_equal_volume"] = False; out["p5_how"] = "lune test fails: " + why
    elif refl: out["p5_equal_volume"] = True; out["p5_how"] = "reflection arrangement: congruent chambers"
    else: out["p5_equal_volume"] = None; out["p5_how"] = "open: " + why
    if not out["p7_factors"]: out["p7_free"] = False; out["p7_how"] = "chi does not factor over Z (Terao)"
    elif refl: out["p7_free"] = True; out["p7_how"] = "reflection arrangement (Saito; Terao)"
    else: out["p7_free"] = None; out["p7_how"] = "chi factors; freeness not decided here"
    return out

# ---------------------------------------------------------------- Coxeter plane of H4
def coxeter_plane_traces(roots, arrs):
    w = [(1, 0), (3, 0), (7, 0), (19, 0)]                  # generic: no root is orthogonal to it (checked)
    allr = roots + [[ng(x) for x in r] for r in roots]
    assert all(not isz(dotz(r, w)) for r in allr)
    pos = [r for r in allr if sgn(dotz(r, w)) > 0]
    pk = {tuple(r) for r in pos}
    simple = []
    for r in pos:
        ok = True
        for x in pos:
            if tuple(x) == tuple(r): continue
            d = dotz(x, r)
            y = [sb(x[t], (lambda h: (h[0] // 2, h[1] // 2))(m(d, r[t]))) for t in range(4)]
            # exactness: d * r[t] must be even in Z[phi]
            assert all(m(d, r[t])[0] % 2 == 0 and m(d, r[t])[1] % 2 == 0 for t in range(4))
            if tuple(y) not in pk: ok = False; break
        if ok: simple.append(r)
    assert len(simple) == 4, len(simple)
    # field K = Q(2cos(2pi/30)); sqrt5 = 2 * 2cos(2pi/5) + 1 = 2 C_6(x) + 1
    K = NF([int(c) for c in fmpz_poly.cos_minpoly(30).coeffs()], "1.9562952014676112738")
    x = K.gen(); s5 = cheb_C(6, x, K.one) * 2 + 1
    assert s5 * s5 == 5 and s5.sign() > 0
    ph = (s5 + 1) / 2
    toK = lambda z: K.c(z[0]) + ph * z[1]
    I = [[K.one if i == j else K.zero for j in range(4)] for i in range(4)]
    def refm(r):
        rk = [toK(t) for t in r]
        return [[I[i][j] - rk[i] * rk[j] / 2 for j in range(4)] for i in range(4)]
    def mul(A, B): return [[sum((A[i][k] * B[k][j] for k in range(4)), K.zero) for j in range(4)] for i in range(4)]
    C = refm(simple[0])
    for r in simple[1:]: C = mul(C, refm(r))
    C2 = mul(C, C)
    M = [[C2[i][j] - x * C[i][j] + I[i][j] for j in range(4)] for i in range(4)]
    # kernel by Gaussian elimination
    A = [row[:] for row in M]; piv = []; r = 0
    for c in range(4):
        p = next((i for i in range(r, 4) if A[i][c]), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; iv = A[r][c].inv(); A[r] = [t * iv for t in A[r]]
        for i in range(4):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(4) if c not in piv]
    assert len(free) == 2, "Coxeter plane not 2-dimensional"
    basis = []
    for fc in free:
        v = [K.zero] * 4; v[fc] = K.one
        for i, pc in enumerate(piv): v[pc] = -A[i][fc]
        basis.append(v)
    p1, p2 = basis
    dK = lambda u, v: sum((a * b for a, b in zip(u, v)), K.zero)
    # check: the plane is c-invariant and c acts on it with order 30
    out = {"simple_roots": len(simple)}
    for name, N in arrs.items():
        dirs = {}; contain = 0
        for nrm in N:
            nk = [toK(t) for t in nrm]
            a, b = dK(nk, p1), dK(nk, p2)
            if not a and not b: contain += 1; continue
            d = [b * u - a * v for u, v in zip(p1, p2)]
            f = next(t for t in d if t); iv = f.inv(); d = [t * iv for t in d]
            dirs.setdefault(tuple(t.key() for t in d), d)
        D = list(dirs.values()); k = len(D)
        reg = all(cheb_C(k, (dK(u, v) * dK(u, v) / (dK(u, u) * dK(v, v))) * 4 - 2, K.one) == 2 for u, v in itertools.combinations(D, 2))
        hits = Counter()
        for nrm in N:
            nk = [toK(t) for t in nrm]; a, b = dK(nk, p1), dK(nk, p2)
            if a or b:
                d = [b * u - a * v for u, v in zip(p1, p2)]; f = next(t for t in d if t); iv = f.inv()
                hits[tuple((t * iv).key() for t in d)] += 1
        out[name] = {"trace_lines": k, "regular_pencil": reg, "hyperplanes_containing_the_plane": contain,
                     "hyperplanes_per_trace_line": sorted(Counter(hits.values()).items())}
        say("  Coxeter plane trace:", name, out[name])
    return out


if __name__ == "__main__":
    procs = int(os.environ.get("PROCS", "12"))
    V = cell600()
    adj = {i: [j for j in range(120) if j != i and dotz(V[i], V[j]) == (0, 2)] for i in range(120)}
    assert all(len(a) == 12 for a in adj.values())
    tets = set(); tris = set()
    for i in range(120):
        for j, k, l in itertools.combinations(adj[i], 3):
            if k in adj[j] and l in adj[j] and l in adj[k]: tets.add(tuple(sorted((i, j, k, l))))
        for j, k in itertools.combinations(adj[i], 2):
            if k in adj[j]: tris.add(tuple(sorted((i, j, k))))
    assert len(tets) == 600 and len(tris) == 1200
    R300 = {}
    for t in tets:
        s = [Z] * 4
        for i in t: s = [ad(a, b) for a, b in zip(s, V[i])]
        R300.setdefault(key(s), s)
    V60 = {}
    for t in tris:
        g = gcross(*[V[i] for i in t]); V60.setdefault(key(g), g)
    roots = {}
    for v in V: roots.setdefault(key(v), list(v))
    assert len(R300) == 300 and len(V60) == 60 and set(V60) == set(roots), "Resonus 300 / Vacuus = the 60 H4 mirrors"
    say("600-cell: Resonus 300, Vacuus 60 = the H4 mirrors (exact)")
    H4 = list(roots.values()); A300 = list(R300.values())
    res = {}
    res["H4"] = analyse4("H4: 60 mirrors (Vacuus of the 600-cell; Resonus and Vacuus of the 120-cell)", H4, procs)
    assert res["H4"]["exponents"] == [1, 11, 19, 29] and res["H4"]["regions"] == 14400 and res["H4"]["simplicial"] and res["H4"]["reflection"], "H4 control"
    say("H4 control ok:", json.dumps(res["H4"]))
    res["R300"] = analyse4("Resonus of the 600-cell (300 hyperplanes, normals along the 120-cell's corners)", A300, procs)
    say("R300:", json.dumps(res["R300"]))
    res["coxeter_plane"] = coxeter_plane_traces([list(r) for r in roots.values()], {"H4": H4, "R300": A300})
    json.dump(res, open(os.path.join(STUDY, "data/four-d.json"), "w"), indent=1, default=str)
    print("FINAL ok four_d", flush=True)
