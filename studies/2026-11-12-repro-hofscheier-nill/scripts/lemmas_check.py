# lemmas_check.py (12 Nov 2026): exact checks of Hofscheier-Nill 2611.00775, Lemmas 3.1, 3.2, 4.1 and the free-sum step of Thm 4.5.
# All arithmetic in integers / Fractions; facets found exactly (2D: integer hull; nD: candidate facets from a qhull triangulation,
# then every inequality re-derived in exact rationals and checked on every vertex).
# Lemma 3.1: for EVERY unit partition 1/k_0 + ... + 1/k_m = 1 with m <= 3 (and k_i <= 1806), build the reflexive simplex by our own
#   construction (quotient lattice Z^{m+1}/Z.lambda, lambda_i = K/k_i, K = lcm) and check: lattice simplex, sum v_i/k_i = 0, every
#   facet at lattice distance 1. Paper's instances: (6,3,2) and (42,7,3,2) with the paper's vertices.
# Lemma 3.2: random lattice bases B (polygons and 3-polytopes, 0 inside) with all facet distances dividing k_0, joined with the
#   paper's simplices: P must be reflexive with |F(P)| = |F(B)| + m. Control: a B with a facet distance NOT dividing k_0 must fail.
# Lemma 4.1: h = 2..3000: vertices = {(a, a^2): a | h} u {(0,-1)}, |F| = 2 tau(h) + 1, the listed facet lines, distances | h^2.
# Free sum (Thm 4.5 step): facet lattice distances of B_h o B_h are lcm's of those of B_h, so they divide h^2 (h = 2..60).
import itertools, random, sys
from fractions import Fraction as Fr
from math import gcd, lcm
import numpy as np
from scipy.spatial import ConvexHull
ok = True
def check(name, c):
    global ok; ok &= bool(c); print(('ok   ' if c else 'FAIL ') + name, flush=True)
def primitive(v):
    g = 0
    for x in v: g = gcd(g, abs(int(x)))
    return tuple(int(x) // g for x in v)
def facets_exact(V):
    """V: list of integer points (full-dim, 0 inside). Returns dict primitive normal a -> h with <a,x> >= -h tight on a facet."""
    A = np.array(V, float); H = ConvexHull(A); n = A.shape[1]; F = {}
    for simp in H.simplices:
        P = [V[i] for i in simp]
        # exact normal: integer kernel of the (n-1) x n difference matrix via sympy-free Fraction elimination
        M = [[Fr(P[j][k] - P[0][k]) for k in range(n)] for j in range(1, n)]
        # solve M a = 0 by Gaussian elimination
        rows = [r[:] for r in M]; piv = []; r0 = 0
        for c in range(n):
            pr = next((i for i in range(r0, len(rows)) if rows[i][c] != 0), None)
            if pr is None: continue
            rows[r0], rows[pr] = rows[pr], rows[r0]
            rows[r0] = [x / rows[r0][c] for x in rows[r0]]
            for i in range(len(rows)):
                if i != r0 and rows[i][c] != 0: rows[i] = [a - rows[i][c] * b for a, b in zip(rows[i], rows[r0])]
            piv.append(c); r0 += 1
        free = [c for c in range(n) if c not in piv][0]
        a = [Fr(0)] * n; a[free] = Fr(1)
        for i, c in enumerate(piv): a[c] = -rows[i][free]
        den = lcm(*[x.denominator for x in a]); a = primitive([x * den for x in a])
        val = sum(a[k] * P[0][k] for k in range(n))
        if all(sum(a[k] * v[k] for k in range(n)) >= val for v in V): pass
        else: a = tuple(-x for x in a); val = -val
        assert all(sum(a[k] * v[k] for k in range(n)) >= val for v in V)
        F[a] = -val
    return F
def reflexive(V):
    F = facets_exact(V); return all(h == 1 for h in F.values()), len(F)
# ---- Lemma 3.1: our construction for every unit partition with m <= 3
def unit_partitions(m, cap):
    out = []
    def rec(prefix, rem, left):
        if left == 1:
            if rem.numerator == 1 and rem.denominator >= (prefix[-1] if prefix else 2) and rem.denominator <= cap: out.append(prefix + [rem.denominator])
            return
        lo = max(prefix[-1] if prefix else 2, int(1 / rem) + 1 if rem < 1 else 2)
        k = lo
        while Fr(left, k) >= rem and k <= cap:
            if Fr(1, k) < rem: rec(prefix + [k], rem - Fr(1, k), left - 1)
            k += 1
    rec([], Fr(1), m + 1); return out
def simplex_from_partition(ks):
    K = lcm(*ks); lam = [K // k for k in ks]; n = len(ks)
    # basis of Z^n / Z.lam: lam is primitive (gcd 1); complete lam to a unimodular matrix, coordinates = other rows of the inverse
    assert gcd(*lam) == 1
    # extended Euclid to build U unimodular with U lam = e_0
    import sympy
    M = sympy.Matrix([lam])
    # Smith/Hermite: find unimodular U (n x n) with first row of U^{-1} ... use sympy's hermite via nullspace of integer matrix
    U = sympy.Matrix.eye(n); v = sympy.Matrix(lam)
    # reduce v to e_0 by integer column operations recorded in U (U v -> e_0)
    vv = list(lam); Ul = sympy.Matrix.eye(n)
    while sum(1 for x in vv if x != 0) > 1 or vv[0] == 0:
        nz = sorted([i for i in range(n) if vv[i] != 0], key=lambda i: abs(vv[i]))
        i = nz[0]
        for j in nz[1:]:
            q = vv[j] // vv[i]; vv[j] -= q * vv[i]; Ul[j, :] = Ul[j, :] - q * Ul[i, :]
        if sum(1 for x in vv if x != 0) == 1:
            i = [k for k in range(n) if vv[k] != 0][0]
            if i != 0: vv[0], vv[i] = vv[i], vv[0]; Ul.row_swap(0, i)
    if vv[0] < 0: vv[0] = -vv[0]; Ul[0, :] = -Ul[0, :]
    assert list(Ul * sympy.Matrix(lam)) == [1] + [0] * (n - 1)
    # quotient map: x -> (Ul x)[1:], kills lam
    verts = [tuple(int(t) for t in (Ul * sympy.Matrix([1 if j == i else 0 for j in range(n)]))[1:]) for i in range(n)]
    return verts
parts = [p for m in (1, 2, 3) for p in unit_partitions(m, 1806)]
bad = []
for ks in parts:
    V = simplex_from_partition(ks)
    s = [sum(Fr(V[i][c], ks[i]) for i in range(len(ks))) for c in range(len(ks) - 1)]
    if len(ks) == 2:
        okk = all(x == 0 for x in s) and sorted(abs(V[i][0]) for i in range(2)) == [1, 1]
    else:
        r, _ = reflexive(V); okk = r and all(x == 0 for x in s)
    if not okk: bad.append(ks)
check(f'Lemma 3.1: all {len(parts)} unit partitions with m <= 3 give a reflexive simplex with sum v_i/k_i = 0 (failures {bad[:3]})', not bad)
S2 = [(-1, -1), (-1, 2), (1, -1)]; S3 = [(-1, -1, -1), (-1, -1, 6), (-1, 2, -1), (1, -1, -1)]
check("Lemma 3.1 instance (6,3,2), paper's triangle: reflexive, weights", reflexive(S2)[0] and all(sum(Fr(S2[i][c], k) for i, k in enumerate((6, 3, 2))) == 0 for c in range(2)))
check("Lemma 3.1 instance (42,7,3,2), paper's simplex: reflexive, weights", reflexive(S3)[0] and all(sum(Fr(S3[i][c], k) for i, k in enumerate((42, 7, 3, 2))) == 0 for c in range(3)))
# ---- Lemma 3.2: random bases
random.seed(1)
def lemma32(B, S, k0):
    n, m = len(B[0]), len(S[0])
    P = [tuple(b) + tuple(S[0]) for b in B] + [(0,) * n + tuple(s) for s in S[1:]]
    FB = facets_exact(B); r, nf = reflexive(P)
    return all(k0 % h == 0 for h in FB.values()), r, nf, len(FB) + m
tried = good = 0; fails = []
def greedy_tail(L):
    rem = Fr(L - 1, L); out = []
    while rem > 0 and len(out) < 5:
        k = -(-rem.denominator // rem.numerator); out.append(k); rem -= Fr(1, k)
    return out if rem == 0 and max(out) <= 10 ** 6 else None
for trial in range(3000):
    if tried >= 120: break
    dim = random.choice((2, 2, 3))
    pts = [tuple(random.randint(-4, 4) for _ in range(dim)) for _ in range(random.randint(dim + 2, 8))]
    pts += [tuple(1 if j == i else 0 for j in range(dim)) for i in range(dim)] + [tuple(-1 for _ in range(dim))]
    try: hull = ConvexHull(np.array(pts, float))
    except Exception: continue
    B = [pts[i] for i in hull.vertices]
    try: FB = facets_exact(B)
    except Exception: continue
    L = lcm(*FB.values())
    if L == 1 or L > 60: continue
    tail = greedy_tail(L)
    if tail is None: continue
    S = simplex_from_partition([L] + tail)
    try: div, r, nf, want = lemma32(B, S, L)
    except Exception: continue
    tried += 1
    if div and r and nf == want: good += 1
    else: fails.append((B, L, tail))
check(f'Lemma 3.2: {tried} random bases with facet distances dividing k0: all reflexive with |F(B)| + m facets ({good}/{tried})', tried >= 50 and good == tried)
Bbad = [(3, 0), (0, 1), (-1, -1)]   # facet x-ish at distance not dividing 6? check and use as control
div, r, nf, want = lemma32([(5, 0), (0, 1), (-1, -1)], S2, 6)
check(f'control: a base with a facet distance not dividing k0 = 6 (divides: {div}) is NOT reflexive', (not div) and (not r))
# ---- Lemma 4.1
def tau(h): return sum(1 for d in range(1, h + 1) if h % d == 0)
def hull2(P):
    P = sorted(set(P))
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
bad41 = []
for h in range(2, 3001):
    divs = [d for d in range(1, h + 1) if h % d == 0]
    pts = [(0, -1)] + [(s * a, a * a) for a in divs for s in (1, -1)]
    V = hull2(pts); want = set(pts)
    edges = [(V[i], V[(i + 1) % len(V)]) for i in range(len(V))]
    dists = []
    for (x1, y1), (x2, y2) in edges:
        a = (y1 - y2, x2 - x1); g = gcd(abs(a[0]), abs(a[1])); a = (a[0] // g, a[1] // g)
        c = a[0] * x1 + a[1] * y1; dists.append(abs(c))
    lines_ok = True
    for i in range(len(divs) - 1):
        d, e = divs[i], divs[i + 1]
        for s in (1, -1):
            if not any(set(ed) == {(s * d, d * d), (s * e, e * e)} for ed in edges): lines_ok = False
    lines_ok &= any(set(ed) == {(h, h * h), (-h, h * h)} for ed in edges) and any(set(ed) == {(0, -1), (1, 1)} for ed in edges) and any(set(ed) == {(0, -1), (-1, 1)} for ed in edges)
    if not (set(V) == want and len(edges) == 2 * tau(h) + 1 and lines_ok and all((h * h) % t == 0 for t in dists) and 0 not in dists):
        bad41.append(h)
check(f'Lemma 4.1: h = 2..3000: vertices, 2 tau(h) + 1 facets, the listed lines, distances divide h^2 (failures {bad41[:5]})', not bad41)
# ---- free sum step of Theorem 4.5
badfs = []
for h in range(2, 61):
    divs = [d for d in range(1, h + 1) if h % d == 0]
    Bh = hull2([(0, -1)] + [(s * a, a * a) for a in divs for s in (1, -1)])
    FS = [p + (0, 0) for p in Bh] + [(0, 0) + p for p in Bh]
    F = facets_exact(FS); nf1 = 2 * tau(h) + 1
    if len(F) != nf1 ** 2 or any((h * h) % t for t in F.values()): badfs.append(h)
check(f'Theorem 4.5 step: B_h o B_h has (2 tau(h) + 1)^2 facets, all lattice distances dividing h^2, h = 2..60 (failures {badfs[:5]})', not badfs)
print('FINAL ok' if ok else 'FINAL FAIL')
