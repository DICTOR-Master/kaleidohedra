"""Aim 1, step 6 (16 Nov 2026): the 3D Hurwitz constant along the icosahedral line.
Scheme at x > 0 as in steps 4-5: lattice Z^6, physical map P(x), internal map Q_x = P(-1/x); pi, pi_perp the orthogonal projections.
    c(x) = liminf_{n in Z^6, |n| -> oo} |pi n| |pi_perp n|.
Exponent: physical and internal space both have dimension 3, so the Dirichlet/Minkowski exponent is 1 (a cylinder of radius L along
physical space and radius r across it has volume (4pi/3)^2 L^3 r^3); the natural invariant is |pi n|^3 |pi_perp n|^3 = (|pi n||pi_perp n|)^3,
whose liminf is c(x)^3. The plain product is the analogue of q|qx - p| (1 + 1 dimensions).
Reduction (proved in the README): with a = (n0-n1, n2-n3, n4+n5), b = (n4-n5, n0+n1, n2+n3) (pairs w_i = (a_i, b_i) in Z^2, parity
a1=b2, a2=b3, a3=b1 mod 2) and F(a,b) = (a + x b)(x a - b):
    4 (1+x^2)^2 |pi n|^2 |pi_perp n|^2 = S^2 + (1+x^2)^2 sum_{i<j} D_ij^2,   S = sum F(w_i),  D_ij = det(w_i, w_j)   (Lagrange identity).
For quadratic x with minimal form G(a,b) = p2 a^2 + p1 ab + p0 b^2 (disc Dd):
    c(x) = min( 3 mu11/(2 sqrt Dd), 2 muM/sqrt Dd, sqrt(1 + m^2/Dd)/2, c2 ),  c2 >= 1/sqrt2,
    mu11 = min |G| on primitive (odd, odd) vectors, muM = min |G| on primitive mixed-parity vectors,
    m = min |G(w) + G(w')| over unimodular (w, w') with w = (1,0), w' = (0,1) mod 2.
This script: certified finite searches for mu11, muM, m (balancing by an automorph of G in Gamma(2)); direct checks against the
projections; positive controls (1/2 at phi, step 5b; Fibonacci 1/sqrt5 and Markov 1/sqrt8 in 1D with the same projection code);
negative controls (crystal 0; parity dropped; wrong exponents). usage: python3 ico_hurwitz.py [--scan H]"""
import itertools, math, random, sys, time
from fractions import Fraction as Fr
import mpmath as mp
import numpy as np
mp.mp.dps = 60
T0 = time.time()
def prog(m): print(f'PROGRESS [{time.time()-T0:7.1f}s] {m}', flush=True)
OK = {}

def Prows(t): return [[1, -1, 0, 0, t, -t], [t, t, 1, -1, 0, 0], [0, 0, t, t, 1, 1]]
def ab(n):
    return (n[0] - n[1], n[2] - n[3], n[4] + n[5]), (n[4] - n[5], n[0] + n[1], n[2] + n[3])
def n_from(a, b):   # inverse of ab; None if not integral
    v = [(a[0] + b[1]), (b[1] - a[0]), (a[1] + b[2]), (b[2] - a[1]), (a[2] + b[0]), (a[2] - b[0])]
    if any(t % 2 for t in v): return None
    return tuple(t // 2 for t in v)

def proj_prod2(rows, n):
    """|pi n|^2 |pi_perp n|^2 for the row space of `rows` (any k x N), mpmath; pi_perp from |n|^2 - |pi n|^2."""
    R = mp.matrix(rows); nv = mp.matrix([mp.mpf(t) for t in n])
    G = R * R.T; y = R * nv; p2 = (y.T * mp.inverse(G) * y)[0]
    return p2 * (sum(mp.mpf(t) ** 2 for t in n) - p2)
def proj_pq(rows, n):
    R = mp.matrix(rows); nv = mp.matrix([mp.mpf(t) for t in n])
    G = R * R.T; y = R * nv; p2 = (y.T * mp.inverse(G) * y)[0]
    return mp.sqrt(p2), mp.sqrt(max(sum(mp.mpf(t) ** 2 for t in n) - p2, mp.mpf(0)))

# ---------------------------------------------------------------- 0. exponent: Minkowski constant
mink = (mp.mpf(36) / mp.pi ** 2) ** (mp.mpf(1) / 3)
prog(f'0. Minkowski: for every L there is n != 0 with |pi n| <= L, |pi_perp n| <= {mp.nstr(mink, 6)}/L, so c(x) <= {mp.nstr(mink, 6)} for every x')

# ---------------------------------------------------------------- 1. the Lagrange identity, exact at rational x (projection side independent of Q)
def F(a, b, x): return (a + x * b) * (x * a - b)
def formula_prod2(n, x):
    a, b = ab(n); S = sum(F(a[i], b[i], x) for i in range(3))
    D2 = sum((a[i] * b[j] - a[j] * b[i]) ** 2 for i, j in ((0, 1), (0, 2), (1, 2)))
    return (S * S + (1 + x * x) ** 2 * D2) / (4 * (1 + x * x) ** 2)
def exact_prod2(n, x):   # Fractions: |pi n|^2 = |P n|^2 / (2(1+x^2)) since P P^T = 2(1+x^2) I
    Pn = [sum(r[k] * n[k] for k in range(6)) for r in Prows(x)]
    p2 = sum(t * t for t in Pn) / (2 * (1 + x * x)); return p2 * (sum(t * t for t in n) - p2)
random.seed(6)
xs = [Fr(1, 3), Fr(2, 5), Fr(1), Fr(7, 4), Fr(3), Fr(13, 5), Fr(8, 5), Fr(100, 7), Fr(5, 2), Fr(11, 9)]
bad = 0; ntest = 0
for x in xs:
    for _ in range(300):
        n = tuple(random.randint(-9, 9) for _ in range(6))
        if not any(n): continue
        ntest += 1; bad += exact_prod2(n, x) != formula_prod2(n, x)
OK['Lagrange identity exact (3000 n, 10 rational x)'] = bad == 0
prog(f'1. identity 4(1+x^2)^2|pi n|^2|pi_perp n|^2 = S^2 + (1+x^2)^2 sum D_ij^2: {ntest} cases, {bad} failures')
# the identity is a polynomial identity of degree <= 8 in x for fixed n; 10 values of x and the hand proof cover it.

# ---------------------------------------------------------------- 2. crystals: c = 0 (negative control)
for x, per in ((Fr(3, 2), (-3, -3, -2, 2, 0, 0)), (Fr(8, 5), (-8, -8, -5, 5, 0, 0)), (Fr(2), None)):
    if per is None:   # find a period of the 2/1 crystal: a - b/x = 0 -> b = 2a: a=(1,0,0) b=(2,0,0)? parity a1=b2.. use a=(2,0,0),b=(4,0,0)
        per = n_from((2, 0, 0), (4, 0, 0))
    OK[f'NEG crystal {x}: period {per} has product 0 (all multiples too)'] = exact_prod2(per, x) == 0 and exact_prod2(tuple(7 * t for t in per), x) == 0
prog('2. crystals: periods (and all their multiples, |n| -> oo) give product 0, so c(rational) = 0')

# ---------------------------------------------------------------- 3. quadratic x: certified mu11, muM, m
def egcd(a, b):
    if b == 0: return (a, 1, 0) if a >= 0 else (-a, -1, 0)
    g, s, t = egcd(b, a % b); return g, t, s - (a // b) * t
class Quad:
    def __init__(s, p2, p1, p0):
        s.p2, s.p1, s.p0 = p2, p1, p0; s.D = p1 * p1 - 4 * p2 * p0
        r = math.isqrt(s.D); assert r * r != s.D and s.D > 0
        sq = mp.sqrt(s.D); s.xi = (-p1 + sq) / (2 * p2); s.xi2 = (-p1 - sq) / (2 * p2)
        s.x = s.xi if s.xi > 0 else s.xi2       # the root used as x
        s.xc = s.xi2 if s.x == s.xi else s.xi
        # automorph in SL2(Z) via t^2 - D u^2 = 4, then a power = I mod 2
        u = 1
        while True:   # least u with D u^2 + 4 a square; past 10^4 use t = 2X, u = 2Y from Pell X^2 - D Y^2 = 1 (still an automorph)
            t2 = s.D * u * u + 4; t = math.isqrt(t2)
            if t * t == t2: break
            u += 1
            if u > 10 ** 4:
                X, Y = pell1(s.D); t, u = 2 * X, 2 * Y; break
        g = [[(t - p1 * u) // 2, -p0 * u], [p2 * u, (t + p1 * u) // 2]]
        assert (t - p1 * u) % 2 == 0
        assert s.comp(g) == (p2, p1, p0), 'automorph'
        k, gk = 1, g
        while not (gk[0][0] % 2 == 1 and gk[1][1] % 2 == 1 and gk[0][1] % 2 == 0 and gk[1][0] % 2 == 0):
            gk = mul(gk, g); k += 1
        s.g0 = gk; s.eps = ((t + u * sq) / 2) ** k
        assert s.comp(gk) == (p2, p1, p0) and gk[0][0] * gk[1][1] - gk[0][1] * gk[1][0] == 1
        sc = mp.sqrt(abs(p2) / sq)
        Lm = mp.matrix([[sc, -sc * s.xi], [sc, -sc * s.xi2]])
        Li = mp.inverse(Lm); s.invF = mp.sqrt(sum(Li[i, j] ** 2 for i in range(2) for j in range(2)))
    def G(s, a, b): return s.p2 * a * a + s.p1 * a * b + s.p0 * b * b
    def comp(s, g):
        (al, be), (ga, de) = g
        return (s.G(al, ga), 2 * s.p2 * al * be + s.p1 * (al * de + be * ga) + 2 * s.p0 * ga * de, s.G(be, de))
    def box(s, T): return int(mp.ceil(s.invF * mp.sqrt(2) * T)) + 2
    def mu(s, cls):   # min |G| over primitive w = cls mod 2 (cls in (1,1), (1,0), (0,1)); certified by balancing
        best = None
        for a in range(-30, 31):
            for b in range(-30, 31):
                if (a % 2, b % 2) == cls and math.gcd(a, b) == 1:
                    v = abs(s.G(a, b)); best = v if best is None or v < best else best
        B = s.box(mp.sqrt(s.eps * best / mp.sqrt(s.D)))
        if B > 400: return None, B
        for a in range(-B, B + 1):
            for b in range(-B, B + 1):
                if (a % 2, b % 2) == cls and math.gcd(a, b) == 1:
                    v = abs(s.G(a, b));
                    if v < best: best = v
        return best, B
    def m_min(s, cap=260, unconstrained=False):
        best = abs(s.p2 + s.p0); arg = ((1, 0), (0, 1))
        if best == 0: return 0, 0, arg
        B = s.box(mp.sqrt(s.eps * mp.sqrt(1 + mp.mpf(best) ** 2 / s.D)))
        if B > cap: return None, B, None
        for al in range(-B, B + 1):
            for c in range(-B, B + 1):
                if not unconstrained and (al % 2 != 1 or c % 2 != 0): continue
                if math.gcd(al, c) != 1: continue
                g, d0, mb0 = egcd(al, c)          # al*d0 + c*mb0 = 1 -> beta0 = -mb0
                be0 = -mb0
                Ga = s.G(al, c)
                # w' = (be0 + t al, d0 + t c), need |.| <= B and (unconstrained or be even, d odd)
                if al != 0:
                    lo = math.floor((-B - be0) / abs(al)) - 1; hi = math.ceil((B - be0) / abs(al)) + 1
                else:
                    lo, hi = -2 * B - 2, 2 * B + 2
                for t in range(lo, hi + 1):
                    be, d = be0 + t * al, d0 + t * c
                    if abs(be) > B or abs(d) > B: continue
                    if not unconstrained and (be % 2 != 0 or d % 2 != 1): continue
                    v = abs(Ga + s.G(be, d))
                    if v < best: best = v; arg = ((al, c), (be, d))
        return best, B, arg
def pell1(D):   # fundamental solution of X^2 - D Y^2 = 1 by the continued fraction of sqrt D
    a0 = math.isqrt(D); m, d, a = 0, 1, a0; p0, p1, q0, q1 = 1, a0, 0, 1
    while p1 * p1 - D * q1 * q1 != 1:
        m = d * a - m; d = (D - m * m) // d; a = (a0 + m) // d
        p0, p1 = p1, a * p1 + p0; q0, q1 = q1, a * q1 + q0
    return p1, q1
def mul(g, h): return [[g[0][0] * h[0][0] + g[0][1] * h[1][0], g[0][0] * h[0][1] + g[0][1] * h[1][1]],
                       [g[1][0] * h[0][0] + g[1][1] * h[1][0], g[1][0] * h[0][1] + g[1][1] * h[1][1]]]

R2 = 1 / mp.sqrt(2)
def c_of(p2, p1, p0, cap=260):
    q = Quad(p2, p1, p0)
    mu11, B1 = q.mu((1, 1)); m10, B2 = q.mu((1, 0)); m01, B3 = q.mu((0, 1))
    m, Bm, arg = q.m_min(cap)
    if None in (mu11, m10, m01, m): return q, None
    sD = mp.sqrt(q.D)
    D0 = min(3 * mu11 / (2 * sD), 2 * min(m10, m01) / sD); dl = mp.sqrt(1 + mp.mpf(m) ** 2 / q.D) / 2
    up = min(D0, dl)
    return q, dict(mu11=mu11, muM=min(m10, m01), m=m, D0=D0, delta=dl, c=up if up <= R2 else None, lo=up if up <= R2 else R2, up=up,
                   boxes=(B1, B2, B3, Bm), arg=arg)

named = {'phi': (1, -1, -1), '1+sqrt2 (silver)': (1, -2, -1), '(3+sqrt13)/2 (bronze)': (1, -3, -1), 'sqrt2': (1, 0, -2),
         'sqrt3': (1, 0, -3), '1/sqrt2': (2, 0, -1), '1/phi': (1, 1, -1), 'sqrt5': (1, 0, -5), '(1+sqrt3)/2': (2, -2, -1),
         '1+sqrt3': (1, -2, -2), 'sqrt6': (1, 0, -6), 'sqrt7': (1, 0, -7), '1+sqrt5 = 2phi': (1, -2, -4),
         'g(sqrt2) = (10+sqrt2)/7 (one icosahedral hop)': (7, -20, 14), 'g(sqrt3) = (16+sqrt3)/11': (11, -32, 23)}
res = {}
for name, pq in named.items():
    q, r = c_of(*pq); res[name] = (q, r)
    if r is None: prog(f'3. {name}: search box too large, skipped'); continue
    cs = mp.nstr(r['c'], 12) if r['c'] is not None else f'in [{mp.nstr(r["lo"], 8)}, {mp.nstr(r["up"], 8)}]'
    prog(f'3. x = {name} = {mp.nstr(q.x, 10)}: D = {q.D}, mu11 = {r["mu11"]}, muM = {r["muM"]}, m = {r["m"]} -> cusps {mp.nstr(r["D0"], 10)}, '
         f'point i {mp.nstr(r["delta"], 10)}; c = {cs}  (boxes {r["boxes"]}, eps {mp.nstr(q.eps, 6)})')
cphi = res['phi'][1]['c']; cs2 = res['sqrt2'][1]['c']; cs3 = res['sqrt3'][1]['c']
OK['POS c(phi) = 1/2 (step 5b)'] = abs(cphi - mp.mpf(1) / 2) < mp.mpf(10) ** -50
OK['c(1/phi) = c(phi) (turn)'] = abs(res['1/phi'][1]['c'] - cphi) < mp.mpf(10) ** -50
OK['c(silver) = 1/2'] = abs(res['1+sqrt2 (silver)'][1]['c'] - mp.mpf(1) / 2) < mp.mpf(10) ** -50
OK['c(sqrt2) = 3/(4 sqrt2)'] = abs(cs2 - 3 / (4 * mp.sqrt(2))) < mp.mpf(10) ** -50
OK['c(1/sqrt2) = c(sqrt2) (turn)'] = abs(res['1/sqrt2'][1]['c'] - cs2) < mp.mpf(10) ** -50
OK['c(sqrt3) = 1/sqrt3'] = abs(cs3 - 1 / mp.sqrt(3)) < mp.mpf(10) ** -50
OK['c(sqrt2), c(sqrt3) > c(phi)'] = cs2 > cphi and cs3 > cphi

# theta-group invariance (Theorem 6c): c(x+2) = c(x), c(x/(2x+1)) = c(x), c(g(x)) = c(x), c(1/x) = c(x); NOT under h(x) = 1 + 1/x or x + 1
def tr(pq, M):   # form of gamma(x) for gamma = M acting by Mobius: G'(a,b) = G(M^-1 (a,b)) up to sign, det M = +-1
    p2, p1, p0 = pq; (al, be), (ga, de) = M; dt = al * de - be * ga
    ia, ib, ic, id_ = de * dt, -be * dt, -ga * dt, al * dt    # inverse
    A = p2 * ia * ia + p1 * ia * ic + p0 * ic * ic
    C = p2 * ib * ib + p1 * ib * id_ + p0 * id_ * id_
    B = 2 * p2 * ia * ib + p1 * (ia * id_ + ib * ic) + 2 * p0 * ic * id_
    g_ = math.gcd(math.gcd(abs(A), abs(B)), abs(C)); A, B, C = A // g_, B // g_, C // g_
    return (A, B, C) if A > 0 else (-A, -B, -C)
inv_ok = True; noninv = []; inv_n = inv_skip = 0
for name in ('sqrt2', 'sqrt3', '(1+sqrt3)/2', 'sqrt7', '(3+sqrt13)/2 (bronze)'):
    base = res[name][1]['up']
    for lab, M in (('x+2', ((1, 2), (0, 1))), ('x/(2x+1)', ((1, 0), (2, 1))), ('g', ((3, 2), (2, 1))), ('1/x', ((0, 1), (1, 0)))):
        r_ = c_of(*tr(named[name], M))[1]
        if r_ is None: inv_skip += 1; continue          # certified search box over the cap: not computed
        inv_n += 1; this = abs(r_['up'] - base) < mp.mpf(10) ** -40
        if not this: prog(f'    invariance FAILS {name} {lab}: form {tr(named[name], M)} -> {float(r_["up"])} vs {float(base)}')
        inv_ok &= this
    for lab, M in (('h = 1+1/x', ((1, 1), (1, 0))), ('x+1', ((1, 1), (0, 1)))):
        r_ = c_of(*tr(named[name], M))[1]; noninv.append((name, lab, float(base), float(r_['up'])))
OK['theta-group invariance (x+2, x/(2x+1), g, 1/x) on every computed case, >= 15 cases'] = inv_ok and inv_n >= 15
OK['NEG not invariant under h or x+1 (some x changes)'] = any(abs(a - b) > 1e-9 for _, _, a, b in noninv)
prog(f'    invariance under x+2, x/(2x+1), g, 1/x: {inv_ok} on {inv_n} cases ({inv_skip} over the box cap); under h and x+1: ' + '; '.join(f'{n} {l}: {a:.6f} -> {b:.6f}' for n, l, a, b in noninv))
# the three end forms G_x, G1 (root 1/x), G2 (root -x) give the same mu and m (used in the proof)
for name in ('sqrt2', 'sqrt3', '(1+sqrt3)/2'):
    p2, p1, p0 = named[name]
    vals = []
    for pq in ((p2, p1, p0), (p0, p1, p2), (p2, -p1, p0)):
        qq = Quad(*pq); vals.append((qq.mu((1, 1))[0], min(qq.mu((1, 0))[0], qq.mu((0, 1))[0]), qq.m_min()[0]))
    OK[f'{name}: G_x, G_1, G_2 give equal (mu11, muM, m)'] = len(set(vals)) == 1
    prog(f'    {name}: (mu11, muM, m) for G_x, G_1, G_2 = {vals}')

# ---------------------------------------------------------------- 4. direct checks in Z^6 through the projections
def fam_check(name, nfam=7):
    """explicit n in Z^6 realising each term of the formula; product computed from the projections of P(x)"""
    q, r = res[name]; x = q.x; rows = [[mp.mpf(v) if not isinstance(v, int) else mp.mpf(v) for v in row] for row in Prows(x)]
    G1 = Quad(q.p0, q.p1, q.p2)                    # form with root a/b = 1/x (the end of G_x where pairs approach 1/x)
    out = {}
    # (i) D = 1 family: g0^j * minimiser pair of G1, at positions 1, 2
    m1, _, arg = G1.m_min()
    seq = []
    for j in range(-nfam, nfam + 1):
        g = [[arg[0][0], arg[1][0]], [arg[0][1], arg[1][1]]]
        gp = g0p = G1.g0 if j >= 0 else inv2(G1.g0)
        for _ in range(abs(j)): g = mul(gp, g)
        w, w2 = (g[0][0], g[1][0]), (g[0][1], g[1][1])
        n = n_from((w[0], w2[0], 0), (w[1], w2[1], 0)); assert n is not None
        seq.append((sum(t * t for t in n), mp.sqrt(proj_prod2(rows, n))))
    out['D1'] = seq
    # (ii) cusp families: g0^j w* with lambda = (1,1,1) (odd class) or (2,0,0)
    for cls, lam in (((1, 1), (1, 1, 1)), ((1, 0), (2, 0, 0)), ((0, 1), (2, 0, 0))):
        best = None
        for a in range(-40, 41):
            for b in range(-40, 41):
                if (a % 2, b % 2) == cls and math.gcd(a, b) == 1 and (best is None or abs(G1.G(a, b)) < abs(G1.G(*best))): best = (a, b)
        s2 = []
        for j in range(-nfam, nfam + 1):
            w = best; gp = G1.g0 if j >= 0 else inv2(G1.g0)
            for _ in range(abs(j)): w = (gp[0][0] * w[0] + gp[0][1] * w[1], gp[1][0] * w[0] + gp[1][1] * w[1])
            n = n_from(tuple(l * w[0] for l in lam), tuple(l * w[1] for l in lam)); assert n is not None
            s2.append((sum(t * t for t in n), mp.sqrt(proj_prod2(rows, n))))
        out[cls] = s2
    return out
def inv2(g): return [[g[1][1], -g[0][1]], [-g[1][0], g[0][0]]]
for name in ('phi', 'sqrt2', 'sqrt3', '1+sqrt2 (silver)', '(1+sqrt3)/2'):
    q, r = res[name]; out = fam_check(name)
    sD = mp.sqrt(q.D)
    pred = {'D1': r['delta'], (1, 1): 3 * r['mu11'] / (2 * sD), (1, 0): None, (0, 1): None}
    # limits: the family converges (in the direction where |n| grows toward the end 1/x) to the predicted term
    for key, seq in out.items():
        tail = [v for (_, v) in seq]
        lim = min(tail[-1], tail[0])
        if key == 'D1':
            OK[f'{name}: D=1 family -> point-i term {mp.nstr(r["delta"], 10)}'] = min(abs(tail[-1] - r['delta']), abs(tail[0] - r['delta'])) < mp.mpf(10) ** -6
        prog(f'4. {name} family {key}: |n|^2 {seq[0][0]} .. {seq[-1][0]}; product at the two ends {mp.nstr(tail[0], 12)}, {mp.nstr(tail[-1], 12)}')
    # the least of all family limits equals c (upper bound realised by explicit n)
    lims = []
    for key, seq in out.items():
        lims.append(min(seq[0][1], seq[-1][1]))
    if r['c'] is not None:
        OK[f'{name}: explicit families in Z^6 reach c = {mp.nstr(r["c"], 10)}'] = abs(min(lims) - r['c']) < mp.mpf(10) ** -6
# at phi, the D=1 family is exactly 1/2 at every size and contains the A-orbit of e1 (step 5b)
A = [[2, 1, 1, -1, 1, -1], [1, 2, 1, -1, -1, 1], [1, 1, 2, 1, 1, 1], [-1, -1, 1, 2, 1, 1], [1, -1, 1, 1, 2, -1], [-1, 1, 1, 1, -1, 2]]
phi = (1 + mp.sqrt(5)) / 2; rows_phi = [[mp.mpf(v) for v in row] for row in Prows(phi)]
v = (1, 0, 0, 0, 0, 0); orbit_vals = []
for _ in range(7):
    orbit_vals.append(mp.sqrt(proj_prod2(rows_phi, v))); v = tuple(sum(A[i][k] * v[k] for k in range(6)) for i in range(6))
OK['POS phi: A-orbit of e1 has product 1/2 (projection code)'] = all(abs(t - mp.mpf(1) / 2) < mp.mpf(10) ** -40 for t in orbit_vals)

# ---------------------------------------------------------------- 5. 1D controls with the same projection code
def conv(xv, k):
    a = []; y = xv
    for _ in range(k): ai = int(mp.floor(y)); a.append(ai); y = 1 / (y - ai)
    h, h1, g, g1 = 1, 0, 0, 1; out = []
    for ai in a: h, h1 = ai * h + h1, h; g, g1 = ai * g + g1, g; out.append((h, g))
    return out
for nm, al, lim in (('Fibonacci 1/phi', 1 / phi, 1 / mp.sqrt(5)), ('Ammann-Beenker 1/sqrt2', 1 / mp.sqrt(2), 1 / mp.sqrt(8))):
    vals = [mp.sqrt(proj_prod2([[mp.mpf(1), al]], (qq, pp))) for pp, qq in conv(al, 30)[15:]]   # q < 1e12: |n|^2 - |pi n|^2 needs ~2 log10 q^2 digits
    OK[f'POS 1D {nm}: projection product -> {mp.nstr(lim, 8)}'] = abs(min(vals) - lim) < mp.mpf(10) ** -12
    prog(f'5. 1D {nm}: |pi n||pi_perp n| on convergents -> {mp.nstr(min(vals), 12)} (Hurwitz/Markov {mp.nstr(lim, 12)})')

# ---------------------------------------------------------------- 6. negative controls
# (a) parity dropped: the unconstrained minimum at sqrt2 is 0 (would give 1/2), but those pairs are not in Z^6
q2 = res['sqrt2'][0]; mu_, Bu, argu = q2.m_min(cap=40, unconstrained=True)
w, w2 = argu
placements = [((w[0], w2[0], 0), (w[1], w2[1], 0)), ((0, w[0], w2[0]), (0, w[1], w2[1])), ((w2[0], 0, w[0]), (w2[1], 0, w[1])),
              ((w2[0], w[0], 0), (w2[1], w[1], 0)), ((0, w2[0], w[0]), (0, w2[1], w[1])), ((w[0], 0, w2[0]), (w[1], 0, w2[1]))]
OK['NEG parity dropped at sqrt2: min 0, but no placement lies in Z^6'] = mu_ == 0 and all(n_from(a_, b_) is None for a_, b_ in placements)
prog(f'6a. sqrt2 without the parity condition: m = {mu_} at pair {argu} (would give 1/2); integral placements: {[n_from(a_, b_) for a_, b_ in placements]}')
# (b) wrong exponents: along the sqrt2 odd-class family |pi n|^1 |pi_perp n|^2 -> 0 and |pi n|^2 |pi_perp n| -> oo
x2 = q2.x; rows2 = [[mp.mpf(v) for v in row] for row in Prows(x2)]
gp = Quad(q2.p0, q2.p1, q2.p2).g0; fams = []
for gdir in (gp, inv2(gp)):
    fam = []; w = (1, 1)
    for j in range(8):
        n = n_from((w[0],) * 3, (w[1],) * 3); pp, qp = proj_pq(rows2, n); fam.append((pp * qp, pp * qp * qp, pp * pp * qp))
        w = (gdir[0][0] * w[0] + gdir[0][1] * w[1], gdir[1][0] * w[0] + gdir[1][1] * w[1])
    fams.append(fam)
fam = min(fams, key=lambda f: f[-1][0])
OK['NEG exponents (1,2) -> 0 and (2,1) -> oo; only (1,1) stays finite'] = fam[-1][1] < 1e-5 and fam[-1][2] > 1e4 and abs(fam[-1][0] - 3 / (4 * mp.sqrt(2))) < 1e-6
prog('6b. exponents along an extremal family at sqrt2 (a,b) = (1,1),(1,2),(2,1): ' + '; '.join(f'{mp.nstr(t[0], 6)}, {mp.nstr(t[1], 3)}, {mp.nstr(t[2], 3)}' for t in fam[::3]))

# ---------------------------------------------------------------- 7. brute force in a box: every n agrees with the formula; small values only at small n
for name in ('phi', 'sqrt2', 'sqrt3'):
    q, r = res[name]; xv = float(q.x); R = 3
    grid = np.array(list(itertools.product(range(-R, R + 1), repeat=6)), dtype=np.int64); grid = grid[np.any(grid != 0, axis=1)]
    Pm = np.array(Prows(xv), dtype=float); Pn = grid @ Pm.T
    p2 = (Pn ** 2).sum(1) / (2 * (1 + xv * xv))
    prod = np.sqrt(p2 * ((grid ** 2).sum(1) - p2))
    a = np.stack([grid[:, 0] - grid[:, 1], grid[:, 2] - grid[:, 3], grid[:, 4] + grid[:, 5]], 1)
    b = np.stack([grid[:, 4] - grid[:, 5], grid[:, 0] + grid[:, 1], grid[:, 2] + grid[:, 3]], 1)
    S = ((a + xv * b) * (xv * a - b)).sum(1)
    D2 = sum((a[:, i] * b[:, j] - a[:, j] * b[:, i]) ** 2 for i, j in ((0, 1), (0, 2), (1, 2)))
    form = np.sqrt(S ** 2 + (1 + xv * xv) ** 2 * D2) / (2 * (1 + xv * xv))
    err = float(np.max(np.abs(form - prod)))
    mn = float(prod.min()); below = grid[prod < float(r['up']) - 1e-9]
    OK[f'{name}: box [-3,3]^6 formula = projections (max err {err:.1e}); global min 1/2'] = err < 1e-9 and abs(mn - 0.5) < 1e-9
    prog(f'7. {name}: {len(grid)} n in [-3,3]^6: max |formula - projection| = {err:.1e}; least product {mn:.10f}; '
         f'{len(below)} n below c(x) = {float(r["up"]):.6f}, largest |n|^2 among them {int((below ** 2).sum(1).max()) if len(below) else 0}')

# ---------------------------------------------------------------- 8. scan of quadratic x (numerical survey; each value certified as in 3)
H = int(sys.argv[sys.argv.index('--scan') + 1]) if '--scan' in sys.argv else 0
if H:
    seen = {}; skipped = 0
    for p2 in range(1, H + 1):
        for p1 in range(-H, H + 1):
            for p0 in range(-H, 0):
                if math.gcd(math.gcd(p2, abs(p1)), abs(p0)) != 1: continue
                D = p1 * p1 - 4 * p2 * p0; r_ = math.isqrt(D)
                if r_ * r_ == D: continue
                q, r = c_of(p2, p1, p0, cap=200)
                key = mp.nstr(q.x, 25)
                if key in seen: continue
                if r is None: skipped += 1; continue
                seen[key] = (float(q.x), (p2, p1, p0), q.D, r)
    turn_bad = 0
    for key, (xv, pq, D, r) in seen.items():
        k2 = mp.nstr(1 / mp.mpf(key), 25)
        if k2 in seen and abs(seen[k2][3]['up'] - r['up']) > 1e-30: turn_bad += 1
    OK[f'scan H={H}: c(x) = c(1/x) for every pair found'] = turn_bad == 0
    top = sorted(seen.values(), key=lambda t: -t[3]['up'])
    prog(f'8. scan H = {H}: {len(seen)} quadratic x (one sign of root, x > 0), {skipped} skipped (box too large)')
    above = [t for t in top if t[3]['c'] is None]
    prog(f'    exact c known for {len(seen) - len(above)}; {len(above)} have min(cusp, point-i) > 1/sqrt2 (c only bounded below by 1/sqrt2)')
    for xv, pq, D, r in top[:15]:
        cs = f'{float(r["c"]):.6f}' if r['c'] is not None else f'>= 0.707107, <= {float(r["up"]):.6f}'
        prog(f'    x = {xv:.6f} {pq} D={D}: c = {cs}  (mu11 {r["mu11"]}, muM {r["muM"]}, m {r["m"]})')
    half = [t for t in seen.values() if t[3]['c'] is not None and abs(t[3]['c'] - 0.5) < 1e-30]
    prog(f'    c = 1/2 exactly at {len(half)} x: ' + ', '.join(f'{t[0]:.5f}{t[1]}' for t in sorted(half)[:12]))
    lt = [t for t in seen.values() if t[3]['up'] < 0.5]
    prog(f'    c < 1/2 at {len(lt)} x, c > 1/2 at {len([t for t in seen.values() if t[3]["up"] > 0.5])} x')

for k_, v in OK.items(): print(f'CHECK {k_}: {v}')
print(f'PROGRESS [{time.time()-T0:7.1f}s] done')
print('FINAL ok' if all(OK.values()) else 'FINAL FAIL')
