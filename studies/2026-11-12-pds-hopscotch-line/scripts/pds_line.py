#!/usr/bin/env python3
"""Aim 2 chunk 6: the PDS's first mode (degree-12 W(H4)-invariant harmonic P12) along the Queens' Hopscotch line
S(mu) = {a.x <= 1, a in 600 facet normals of the 600-cell (R = 1)} cap {v.x <= mu, v in its 120 corners}, r^2 <= mu <= 1.
(i) corners: P12(corner(mu)) exactly per hop -> 19-design stations; (ii) canonical form Omega(S; y) = sum |det q| / prod(1 - q.y)
over a pulling triangulation of the boundary of S* = conv(q), q = a (type 0) or v/mu (type 1); Taylor coefficients along three
directions as exact polynomials in nu = 1/mu over Q(sqrt5); order-12 anisotropy B(mu).
Controls: 3D cube-octahedron line reproduces chunks 2/3 exactly; B4 line shows order-4 anisotropy (negative); dropped simplex breaks
isotropy (negative); 600-cell / 120-cell 11-designs (Silent Queens) exact; icosian left multiplication permutes the corners.
Usage: pds_line.py [--pilot]"""
import sys, time, itertools, json
from fractions import Fraction as Fr
from multiprocessing import get_context
Pool = get_context("fork").Pool
import numpy as np
from scipy.spatial import ConvexHull
import sympy as sp

PILOT = '--pilot' in sys.argv
T0 = time.time()
CHECKS = []
def check(name, ok, info=''):
    CHECKS.append((name, bool(ok)))
    print(f"{'ok  ' if ok else 'FAIL'} {name} {info}", flush=True)

class K:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0):
        s.a = a if type(a) is Fr else Fr(a); s.b = b if type(b) is Fr else Fr(b)
    def __add__(s, o):
        if type(o) is not K: o = K(o)
        return K(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o):
        if type(o) is not K: o = K(o)
        return K(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return K(o) - s
    def __mul__(s, o):
        if type(o) is not K:
            o = o if type(o) is Fr else Fr(o)
            return K(s.a * o, s.b * o)
        return K(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __neg__(s): return K(-s.a, -s.b)
    def norm(s): return s.a * s.a - 5 * s.b * s.b
    def __truediv__(s, o):
        if type(o) is not K: o = K(o)
        n = o.norm(); c = s * K(o.a, -o.b); return K(c.a / n, c.b / n)
    def __rtruediv__(s, o): return K(o) / s
    def z(s): return s.a == 0 and s.b == 0
    def __eq__(s, o):
        if type(o) is not K: o = K(o)
        return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        a, b = s.a, s.b
        if a >= 0 and b >= 0: return 0 if (a == 0 and b == 0) else 1
        if a <= 0 and b <= 0: return -1
        if a > 0: return 1 if a * a > 5 * b * b else -1
        return 1 if 5 * b * b > a * a else -1
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __abs__(s): return s if s.sign() >= 0 else -s
    def sym(s): return sp.Rational(s.a.numerator, s.a.denominator) + sp.Rational(s.b.numerator, s.b.denominator) * sp.sqrt(5)
    def __repr__(s): return f'({s.a}+{s.b}r5)'

ZERO, ONE = K(0), K(1)
def dot(u, v):
    r = K(0)
    for x, y in zip(u, v): r = r + x * y
    return r

def det(M):
    M = [list(r) for r in M]; n = len(M); d = K(1)
    for c in range(n):
        p = next((i for i in range(c, n) if not M[i][c].z()), None)
        if p is None: return K(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d = d * M[c][c]
        for i in range(c + 1, n):
            if not M[i][c].z():
                f = M[i][c] / M[c][c]
                M[i] = [M[i][j] - f * M[c][j] for j in range(n)]
    return d

def solve(M, rhs):
    n = len(M); A = [list(M[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if not A[i][c].z())
        A[c], A[p] = A[p], A[c]
        inv = ONE / A[c][c]; A[c] = [x * inv for x in A[c]]
        for i in range(n):
            if i != c and not A[i][c].z():
                f = A[i][c]; A[i] = [A[i][j] - f * A[c][j] for j in range(n + 1)]
    return [A[i][n] for i in range(n)]

def rank_rows(rows):
    """indices of a maximal independent subset (greedy, exact)"""
    basis, idx = [], []
    for k, r in enumerate(rows):
        v = list(r)
        for (b, piv) in basis:
            if not v[piv].z():
                f = v[piv] / b[piv]; v = [x - f * y for x, y in zip(v, b)]
        piv = next((j for j, x in enumerate(v) if not x.z()), None)
        if piv is not None: basis.append((v, piv)); idx.append(k)
    return idx

# ---------------- pulling triangulation of a small polytope given by points (exact) ----------------
def local_coords(pts):
    """pts: list of K-vectors; returns (dim, list of K-coordinate tuples in an affine frame)"""
    b = pts[0]; D = [[x - y for x, y in zip(p, b)] for p in pts]
    ind = rank_rows(D); dim = len(ind); E = [D[i] for i in ind]
    if dim == 0: return 0, [() for _ in pts]
    # pick dim independent coordinate columns
    cols = rank_rows([[E[i][j] for i in range(dim)] for j in range(len(b))])
    M = [[E[i][j] for i in range(dim)] for j in cols]  # dim x dim, M c = d_cols
    out = [tuple(solve(M, [d[j] for j in cols])) for d in D]
    return dim, out

def facets_of(idx, coords, dim):
    """codim-1 faces of conv(points) in R^dim (exact), as frozensets of indices"""
    F = set(); n = len(idx)
    for sub in itertools.combinations(range(n), dim):
        s0 = coords[sub[0]]
        base = [[x - y for x, y in zip(coords[t], s0)] for t in sub[1:]]
        sg = set(); on = []
        for z in range(n):
            d = det(base + [[x - y for x, y in zip(coords[z], s0)]]).sign()
            if d == 0: on.append(z)
            else: sg.add(d)
        if len(sg) == 1 and len(on) < n:
            # require sub spans a hyperplane (some point off it already guaranteed) and sub affinely independent
            if len(rank_rows(base)) == dim - 1: F.add(frozenset(idx[z] for z in on))
    return F

def pull(idx, P, dim):
    """pulling triangulation of conv(P[i] for i in idx) (affine dim = dim) -> list of tuples of dim+1 indices"""
    idx = sorted(idx)
    if len(idx) == dim + 1: return [tuple(idx)]
    d, coords = local_coords([P[i] for i in idx])
    assert d == dim, (d, dim)
    p0 = idx[0]; out = []
    for F in facets_of(idx, coords, dim):
        if p0 in F: continue
        for s in pull(F, P, dim - 1): out.append((p0,) + s)
    return out

# ---------------- a polar line: facets a.x <= 1 (type 0), corner planes v.x <= mu (type 1) ----------------
class Line:
    def __init__(s, name, A, V):
        s.name = name; s.raw = [tuple(a) for a in A] + [tuple(v) for v in V]
        s.typ = [0] * len(A) + [1] * len(V); s.d = len(A[0])
        s.rawf = np.array([[float(x) for x in r] for r in s.raw])
    def q_exact(s, mu):
        return [r if t == 0 else tuple(x * (Fr(1) / mu) for x in r) for r, t in zip(s.raw, s.typ)]
    def chamber(s, mu):
        """exact face data of S(mu) at rational mu: list of (tight index set, x0, x1) with corner x = x0 + mu x1, and simplices"""
        mu = Fr(mu); qe = s.q_exact(mu); qf = np.array([[float(x) for x in r] for r in qe])
        hull = ConvexHull(qf)
        seen = {}; minmargin = 1e9
        for eq in hull.equations:
            xa = -eq[:-1] / eq[-1]
            key = tuple(np.round(xa, 7))
            if key in seen: continue
            vals = qf @ xa
            cand = [i for i in range(len(qf)) if abs(vals[i] - 1) < 1e-7]
            seen[key] = cand
        faces = {}
        for key, cand in seen.items():
            rows = [s.raw[i] for i in cand]; ind = rank_rows(rows)
            assert len(ind) == s.d
            M = [s.raw[cand[i]] for i in ind]
            x0 = solve(M, [K(1) if s.typ[cand[i]] == 0 else K(0) for i in ind])
            x1 = solve(M, [K(0) if s.typ[cand[i]] == 0 else K(1) for i in ind])
            x = [p + q * mu for p, q in zip(x0, x1)]
            xf = np.array([float(t) for t in x]); vals = qf @ xf
            tight = []
            for i in range(len(qf)):
                if abs(vals[i] - 1) < 1e-6:
                    if dot(qe[i], x) == ONE: tight.append(i)
                    else: raise RuntimeError('near-tight but not tight')
                else:
                    minmargin = min(minmargin, 1 - vals[i])
                    if vals[i] > 1: raise RuntimeError('point outside facet hyperplane')
            faces[frozenset(tight)] = (x0, x1)
        simp = []; facet_vol = []
        for T, (x0, x1) in faces.items():
            ss = pull(T, qe, s.d - 1)
            tot = K(0)
            for t in ss:
                D = det([qe[i] for i in t]); tot = tot + abs(D)
                m = sum(s.typ[i] for i in t)
                simp.append((t, m, abs(det([s.raw[i] for i in t]))))
            facet_vol.append(tot)
        return faces, simp, facet_vol, minmargin

# ---------------- Taylor coefficients of Omega(S; t u) as polynomials in nu ----------------
G = {}
def _work(args):
    lo, hi, u, KMAX = args
    L = G['line']; simp = G['simp']
    w = [dot(r, u) for r in L.raw]
    acc = [dict() for _ in range(KMAX + 1)]
    pw_cache = {}
    def pw(i):
        if i not in pw_cache:
            p = [K(1)]
            for _ in range(KMAX): p.append(p[-1] * w[i])
            pw_cache[i] = p
        return pw_cache[i]
    def hser(ids):
        h = [K(1)] + [K(0)] * KMAX
        for i in ids:
            p = pw(i); nh = []
            for k in range(KMAX + 1):
                t = K(0)
                for j in range(k + 1):
                    if not h[k - j].z(): t = t + p[j] * h[k - j]
                nh.append(t)
            h = nh
        return h
    for (t, m, D) in simp[lo:hi]:
        hA = hser([i for i in t if L.typ[i] == 0]); hB = hser([i for i in t if L.typ[i] == 1])
        for k in range(KMAX + 1):
            for j in range(k + 1):
                if hA[k - j].z() or hB[j].z(): continue
                acc[k][j + m] = acc[k].get(j + m, K(0)) + D * hA[k - j] * hB[j]
    return [{e: (c.a, c.b) for e, c in a.items()} for a in acc]

def expand(line, simp, u, KMAX, procs=4):
    G['line'] = line; G['simp'] = simp
    n = len(simp); step = max(1, (n + 4 * procs - 1) // (4 * procs))
    jobs = [(i, min(n, i + step), u, KMAX) for i in range(0, n, step)]
    with Pool(procs) as pool: parts = pool.map(_work, jobs)
    acc = [dict() for _ in range(KMAX + 1)]
    for part in parts:
        for k in range(KMAX + 1):
            for e, (a, b) in part[k].items(): acc[k][e] = acc[k].get(e, K(0)) + K(a, b)
    return [{e: c for e, c in a.items() if not c.z()} for a in acc]

nu, mu_s = sp.symbols('nu mu', positive=True)
def topoly(dct):  # dict deg->K  -> sympy expr in nu
    return sp.expand(sum(c.sym() * nu ** e for e, c in dct.items()))
def unitnorm(acc, u, k):  # c_k / |u|^k
    n2 = dot(u, u); f = K(1)
    for _ in range(k // 2): f = f * n2
    return {e: c / f for e, c in acc[k].items()}
def peq(d1, d2):
    keys = set(d1) | set(d2)
    return all((d1.get(e, K(0)) - d2.get(e, K(0))).z() for e in keys)

# ================= CONTROL 1: cube-octahedron line (3D), reproduces chunks 2/3 =================
print('== control: cube-octahedron line (chunks 2, 3)', flush=True)
E3 = [tuple(K(1 if j == i else 0) * sg for j in range(3)) for i in range(3) for sg in (1, -1)]
C3 = [tuple(K(x) for x in v) for v in itertools.product((1, -1), repeat=3)]
L3 = Line('C-O', E3, C3)
exp_c0 = {Fr(1, 2): (48, 3), Fr(3, 2): (48, 2), Fr(5, 2): (24, 1)}
u3 = [(K(1), K(0), K(0)), (K(1), K(1), K(1))]
for mu0, (cst, pw_) in exp_c0.items():
    faces, simp, fv, mm = L3.chamber(mu0)
    accs = [expand(L3, simp, u, 4, procs=1) for u in u3]
    c0 = topoly(accs[0][0])
    check(f'C-O mu={mu0}: Omega(S;0) = {cst}/mu^{pw_}', sp.simplify(c0 - cst * nu ** pw_) == 0, str(c0))
    if mu0 == Fr(3, 2):
        c2 = topoly(unitnorm(accs[0], u3[0], 2))
        check('C-O (1,2): c2/c0 = (mu^2+2mu+7)/(3mu^2) (chunk 3)', sp.simplify((c2 / c0).subs(nu, 1 / mu_s) - (mu_s**2 + 2*mu_s + 7) / (3*mu_s**2)) == 0)
        an = topoly(unitnorm(accs[0], u3[0], 4)) - topoly(unitnorm(accs[1], u3[1], 4))
        target = 2 * (mu_s**4 + 2*mu_s**3 + mu_s**2 - 4*mu_s - 14) / (9 * mu_s**4)
        ratio = sp.simplify((an / c0).subs(nu, 1 / mu_s) / target)
        check('C-O (1,2): order-4 anisotropy/c0 = +-2(mu^4+2mu^3+mu^2-4mu-14)/(9mu^4) (chunk 3 root 1.692590)', ratio in (1, -1), str(ratio))
print(f'PROGRESS 0.10 3D control done ({time.time()-T0:.0f}s)', flush=True)

# ================= H4 data =================
print('== H4: 600-cell (White Queen), 120-cell (Red Queen)', flush=True)
phi = K(Fr(1, 2), Fr(1, 2)); iphi = phi - 1; h = Fr(1, 2)
V = set()
for i in range(4):
    for sg in (1, -1):
        v = [K(0)] * 4; v[i] = K(sg); V.add(tuple(v))
for sg in itertools.product((1, -1), repeat=4): V.add(tuple(K(Fr(s, 2)) for s in sg))
base = [phi * h, K(h), iphi * h, K(0)]
evenp = [p for p in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]
for p in evenp:
    for sg in itertools.product((1, -1), repeat=3):
        b = [base[0] * sg[0], base[1] * sg[1], base[2] * sg[2], K(0)]
        v = [None] * 4
        for i in range(4): v[p[i]] = b[i]
        V.add(tuple(v))
V = sorted(V, key=lambda v: tuple(float(x) for x in v))
check('600-cell: 120 corners, all |v| = 1', len(V) == 120 and all(dot(v, v) == ONE for v in V))
Vf = np.array([[float(x) for x in v] for v in V])
cosE = phi * h
nb = {i: [j for j in range(120) if j != i and abs(Vf[i] @ Vf[j] - float(cosE)) < 1e-9] for i in range(120)}
check('600-cell: 720 edges (12 neighbours each, exact)', all(len(nb[i]) == 12 for i in range(120)) and all(dot(V[i], V[j]) == cosE for i in nb for j in nb[i]))
cells = set()
for i in range(120):
    for j in nb[i]:
        for k in set(nb[i]) & set(nb[j]):
            for l in set(nb[i]) & set(nb[j]) & set(nb[k]):
                cells.add(frozenset((i, j, k, l)))
cells = sorted(tuple(sorted(c)) for c in cells)
W = []
for c in cells:
    cen = [sum((V[i][t] for i in c), K(0)) for t in range(4)]
    s_ = dot(cen, V[c[0]]); W.append(tuple(x / s_ for x in cen))
check('600 cells; facet normals w with w.v = 1 on the cell', len(W) == 600 and all(dot(W[n], V[i]) == ONE for n, c in enumerate(cells) for i in c))
r2 = ONE / dot(W[0], W[0])
check('inradius r^2 equal for all 600 facets', all(ONE / dot(w, w) == r2 for w in W), f'r^2 = {r2} = {float(r2):.12f}')
# flag radii
c0v = cells[0]
fr = [dot(V[c0v[0]], V[c0v[0]])]
for k in (2, 3, 4):
    cen = [sum((V[i][t] for i in c0v[:k]), K(0)) * Fr(1, k) for t in range(4)]
    fr.append(dot(cen, cen))
print('squared flag radii (walls):', [f'{x} = {float(x):.9f}' for x in fr], flush=True)
check('cell centre radius^2 = r^2', fr[3] == r2)

# Silent Queens reproduced: 11-designs (exact polynomial identities)
y = sp.symbols('y1:5')
dom = sp.QQ.algebraic_field(sp.sqrt(5))
def powsum(pts, k):
    tot = sp.Poly(0, *y, domain=dom)
    for v in pts:
        lin = sp.Poly(sum(x.sym() * yy for x, yy in zip(v, y)), *y, domain=dom)
        tot += lin ** k
    return tot
def Ek(k):  # E[x1^k] on S^3
    m = k // 2; num = 1
    for i in range(1, 2 * m, 2): num *= i
    den = 1
    for i in range(m): den *= 4 + 2 * i
    return sp.Rational(num, den)
y2 = sp.Poly(sum(t**2 for t in y), *y, domain=dom)
w2 = dot(W[0], W[0])
design_ok = True
for k in (2, 4, 6, 8, 10):
    if PILOT and k > 4: break
    ps = powsum(V, k); iso = y2 ** (k // 2) * (120 * Ek(k))
    design_ok &= (ps - iso).is_zero
check('White Queen: sum (v.y)^k = 120 E_k |y|^k for k = 2..10 (11-design, Silent Queens)' + (' [pilot: k<=4]' if PILOT else ''), design_ok)
f12 = powsum(V, 12)
P12 = f12 - y2 ** 6 * (120 * Ek(12))
lap = sum(sp.Poly(sp.diff(P12.as_expr(), t, 2), *y, domain=dom) for t in y)
check('P12 = sum (v.y)^12 - 120 E_12 |y|^12 is harmonic (Laplacian 0) and nonzero', lap.is_zero and not P12.is_zero)
if not PILOT:
    psW = powsum(W, 12); isoW = y2 ** 6 * (600 * Ek(12)) * w2.sym() ** 6
    okW = all((powsum(W, k) - y2 ** (k // 2) * (600 * Ek(k)) * w2.sym() ** (k // 2)).is_zero for k in (2, 4, 6, 8, 10))
    check('Red Queen (600 normals): 11-design k = 2..10 exact; degree 12 sounds', okW and not (psW - isoW).is_zero)
# icosian left multiplication permutes the corners (so P12 lives on the PDS)
def qmul(p, q):
    a1, b1, c1, d1 = p; a2, b2, c2, d2 = q
    return (a1*a2 - b1*b2 - c1*c2 - d1*d2, a1*b2 + b1*a2 + c1*d2 - d1*c2, a1*c2 - b1*d2 + c1*a2 + d1*b2, a1*d2 + b1*c2 - c1*b2 + d1*a2)
Vset = set(V)
gens = [V[nb[0][0]], V[nb[0][5]]]
check('left and right multiplication by two icosians permute the 120 corners', all(qmul(g, v) in Vset and qmul(v, g) in Vset for g in gens for v in V))
P12e = P12.as_expr()
def P12K(x):  # exact P12 at K-vector
    f = K(0)
    for v in V:
        t = dot(v, x); p = K(1)
        for _ in range(12): p = p * t
        f = f + p
    n2 = dot(x, x); p = K(1)
    for _ in range(6): p = p * n2
    e = Ek(12) * 120
    return f - p * Fr(e.p, e.q)
print(f'PROGRESS 0.25 H4 data and Silent Queens checks ({time.time()-T0:.0f}s)', flush=True)

# ================= the H4 line =================
LH = Line('H4', W, V)
walls = [float(x) for x in fr]  # 1, rho1^2, rho2^2, r^2
# float scan of the combinatorics: corner count per mu
scan = []
for mu0 in np.linspace(float(r2) + 1e-4, 1 - 1e-4, 13 if PILOT else 41):
    qf = np.array([r if t == 0 else r / mu0 for r, t in zip(LH.rawf, LH.typ)])
    hl = ConvexHull(qf); xs = {tuple(np.round(-e[:-1] / e[-1], 6)) for e in hl.equations}
    scan.append((mu0, len(xs)))
print('corner counts along the line (float scan):', [(round(m, 4), n) for m, n in scan], flush=True)
chg = [(scan[i][0], scan[i + 1][0]) for i in range(len(scan) - 1) if scan[i][1] != scan[i + 1][1]]
check('corner count changes only across the walls rho1^2, rho2^2', all(any(a < w < b for w in walls[1:3]) for a, b in chg) and len(chg) <= 2, str(chg))

hops = [('truncated 600-cell hop', fr[1], ONE), ('middle hop', fr[2], fr[1]), ('truncated 120-cell hop', r2, fr[2])]
dirs = [(K(1), K(0), K(0), K(0)), W[0], (K(1), K(2), K(3), K(5))]
dir_names = ['600-cell corner axis', '120-cell corner axis', 'generic (1,2,3,5)']
KMAX = 4 if PILOT else 12
results = {}
STATIONS = []; P12POLY = {}
for hi, (hname, lo_, hi_) in enumerate(hops):
    if PILOT and hi > 0: break
    mid = (float(lo_) + float(hi_)) / 2; mu0 = Fr(round(mid * 100000), 100000)
    t1 = time.time()
    faces, simp, fv, mm = LH.chamber(mu0)
    nverts = len(faces); kinds = sorted({len(T) for T in faces})
    print(f'== {hname} ({float(lo_):.6f}, {float(hi_):.6f}), sample mu = {mu0}: {nverts} corners, facets per corner {kinds}, '
          f'{len(simp)} simplices, min float margin {mm:.2e} ({time.time()-t1:.0f}s)', flush=True)
    check(f'{hname}: every facet of S* has the same 3-volume (one corner orbit, no simplex missing)', len(set(fv)) == 1)
    # corners: one orbit, P12 the same at every corner (float, all; exact, 6)
    T0f = next(iter(faces)); x0, x1 = faces[T0f]
    xs = [[p + q * mu0 for p, q in zip(*faces[T])] for T in faces]
    norms = {dot(x, x) for x in xs[:50]}
    p12f = []
    Pf = sp.lambdify(y, P12e, 'numpy')
    for x in xs: p12f.append(Pf(*[float(t) for t in x]))
    p12f = np.array(p12f)
    ex = [P12K(x) for x in xs[:6]]
    check(f'{hname}: P12 equal at every corner (float, all {nverts}; exact, 6)', np.ptp(p12f) < 1e-9 * max(1, np.abs(p12f).max()) and len(set(ex)) == 1 and len(norms) == 1)
    # P12(corner(mu)) as an exact polynomial in mu
    m_ = sp.Symbol('m')
    xm = [p.sym() + q.sym() * m_ for p, q in zip(x0, x1)]
    p12mu = sp.Poly(sp.expand(P12e.subs(dict(zip(y, xm)))), m_, domain=dom)
    roots = []
    for fac, mult in sp.factor_list(p12mu.as_expr(), m_, extension=sp.sqrt(5))[1]:
        fq = sp.Poly(fac, m_)
        # norm to Q
        nq = sp.Poly(sp.expand(fac * fac.subs(sp.sqrt(5), -sp.sqrt(5))), m_)
        for rt in sp.Poly(fac, m_).nroots(n=40):
            if abs(sp.im(rt)) < 1e-30 and float(lo_) < float(sp.re(rt)) < float(hi_):
                if abs(complex(fac.subs(m_, sp.re(rt)).evalf(50))) < 1e-25:
                    mp = sp.factor_list(nq.as_expr(), m_)[1]
                    mp = [g for g, _ in mp if abs(complex(g.subs(m_, sp.re(rt)).evalf(60))) < 1e-30][0]
                    roots.append((sp.re(rt), sp.Poly(mp, m_)))
    P12POLY[hname] = (p12mu, float(lo_), float(hi_)); STATIONS += [rt for rt, _ in roots]
    results[hname] = {'mu0': str(mu0), 'corners': nverts, 'facets_per_corner': kinds, 'simplices': len(simp),
                      'P12_corner_poly_degree': p12mu.degree(),
                      'design19_stations': [(sp.N(rt, 30).__str__(), str(mp.as_expr()), mp.degree()) for rt, mp in roots]}
    for rt, mp in roots:
        print(f'   19-design station mu* = {sp.N(rt, 30)}; minimal polynomial over Q (degree {mp.degree()}): {mp.as_expr()}', flush=True)
        # turn image
        tr = r2.sym() / rt
        print(f'   its turn image r^2/mu* = {sp.N(tr, 20)}', flush=True)
        # fixed point test exact: r is root of mp?
        rfix = sp.sqrt(r2.sym())
        mr = sp.Poly(sp.minimal_polynomial(rfix, m_), m_, domain=sp.QQ)
        check(f'{hname}: the fixed point mu = r is NOT a 19-design station (exact: minimal polynomials differ)', mr.monic() != sp.Poly(mp, m_, domain=sp.QQ).monic(), f'r = {sp.N(rfix, 20)}, minpoly(r) = {mr.as_expr()}')
        if hi == 0:
            check('book value 0.924165 (400-point grid, step 2.4e-4) agrees within one grid step; exact value corrects it', abs(float(rt) - 0.924165) < 2.4e-4, f'diff {float(rt)-0.924165:.2e}')
            # negative: perturbed mu is not a station
            check('NEG: mu* + 1/1000 is not a station', p12mu.eval(sp.Rational(str(sp.N(rt, 30))) + sp.Rational(1, 1000)) != 0)
            # float design moments at mu*: degrees 1..19 silent, 20 sounds (numerical)
            mus = float(rt); xsf = np.array([[float(p) + float(q) * mus for p, q in zip(*faces[T])] for T in faces])
            xsf /= np.linalg.norm(xsf, axis=1)[:, None]
            rng = np.random.default_rng(1); U = rng.normal(size=(5, 4)); U /= np.linalg.norm(U, axis=1)[:, None]
            from math import comb
            dev = {}
            for k in range(2, 21, 2):
                mom = ((xsf @ U.T) ** k).mean(axis=0); dev[k] = float(np.abs(mom - float(Ek(k))).max())
            print('   float moment deviations at mu*:', {k: f'{d:.1e}' for k, d in dev.items()}, flush=True)
            check('numerical: 1440 corners at mu* silent to 1e-12 in degrees 2..18, degree 20 sounds (> 1e-10)', max(dev[k] for k in range(2, 19, 2)) < 1e-12 and dev[20] > 1e-10)
    if not roots: print('   no 19-design station in this hop', flush=True)
    # canonical form expansion
    t1 = time.time()
    accs = [expand(LH, simp, u, KMAX) for u in dirs]
    print(f'   expansion to order {KMAX} along 3 directions: {time.time()-t1:.0f}s', flush=True)
    odd_ok = all(not accs[j][k] for j in range(3) for k in range(1, KMAX + 1, 2))
    check(f'{hname}: odd orders vanish', odd_ok)
    iso_ok = all(peq(unitnorm(accs[0], dirs[0], k), unitnorm(accs[j], dirs[j], k)) for j in (1, 2) for k in range(2, min(KMAX, 10) + 1, 2))
    check(f'{hname}: Omega isotropic at orders 2..{min(KMAX,10)} (three directions, exact)', iso_ok)
    c0 = topoly(accs[0][0])
    print(f'   Omega(S;0) = 4! vol(S*) = {sp.factor(c0.subs(nu, 1/mu_s), extension=sp.sqrt(5))}', flush=True)
    results[hname]['Omega0'] = str(sp.factor(c0.subs(nu, 1 / mu_s), extension=sp.sqrt(5)))
    # negative: drop one simplex -> isotropy at order 2 fails
    accd = [expand(LH, simp[1:], u, 2) for u in dirs[:2]]
    check(f'NEG {hname}: one simplex dropped breaks order-2 isotropy', not peq(unitnorm(accd[0], dirs[0], 2), unitnorm(accd[1], dirs[1], 2)))
    if KMAX >= 12:
        pu = [P12K(u) for u in dirs]
        pun = []
        for u, p in zip(dirs, pu):
            n2 = dot(u, u); f = K(1)
            for _ in range(6): f = f * n2
            pun.append(p / f)
        c12 = [unitnorm(accs[j], dirs[j], 12) for j in range(3)]
        Bd = {e: (c12[0].get(e, K(0)) - c12[1].get(e, K(0))) / (pun[0] - pun[1]) for e in set(c12[0]) | set(c12[1])}
        lhs = {e: c12[2].get(e, K(0)) - c12[0].get(e, K(0)) for e in set(c12[2]) | set(c12[0])}
        rhs = {e: Bd[e] * (pun[2] - pun[0]) for e in Bd}
        check(f'{hname}: order 12 = A + B P12(u) (third direction agrees exactly)', peq(lhs, rhs))
        B = topoly(Bd)
        Bmu = sp.factor(sp.together(B.subs(nu, 1 / mu_s)), extension=sp.sqrt(5))
        print(f'   B(mu) (order-12 tone of Omega) = {Bmu}', flush=True)
        results[hname]['B'] = str(Bmu)
        num = sp.Poly(sp.numer(sp.together(B.subs(nu, 1 / mu_s))), mu_s)
        bz = []
        for fac, _ in sp.factor_list(num.as_expr(), mu_s, extension=sp.sqrt(5))[1]:
            for rt in sp.Poly(fac, mu_s).nroots(n=40):
                if abs(sp.im(rt)) < 1e-30 and float(lo_) < float(sp.re(rt)) < float(hi_):
                    bz.append((sp.re(rt), fac))
        for rt, fac in bz:
            print(f'   B = 0 at mu = {sp.N(rt, 30)} (factor over Q(sqrt5): {fac})', flush=True)
        if not bz: print('   B has no zero in this hop', flush=True)
        results[hname]['B_zeros'] = [str(sp.N(rt, 30)) for rt, _ in bz]
        Bfix = sp.N(B.subs(nu, 1 / sp.sqrt(r2.sym())), 30) if float(lo_) < float(r2) ** 0.5 < float(hi_) else None
        if Bfix is not None:
            print(f'   B at the fixed point r: {Bfix}', flush=True); results[hname]['B_at_fixed_point'] = str(Bfix)
            check(f'{hname}: B(r) != 0 at the fixed point', abs(Bfix) > 1e-20)
        results[hname]['B_sign_at_ends'] = [str(sp.sign(sp.N(B.subs(nu, 1 / sp.Float(float(e) * (1 + s * 1e-9))), 20))) for e, s in ((lo_, 1), (hi_, -1))]
    print(f'PROGRESS {0.25 + 0.2 * (hi + 1):.2f} {hname} done ({time.time()-T0:.0f}s)', flush=True)

# ================= the turn and the stations =================
if not PILOT:
    m_ = sp.Symbol('m')
    for st in STATIONS:
        t = sp.N(r2.sym() / st, 50)
        hop = [k for k, (p, lo, hi) in P12POLY.items() if lo < float(t) < hi]
        val = abs(P12POLY[hop[0]][0].as_expr().subs(m_, t).evalf(50)) if hop else None
        scale = max(abs(sp.N(c, 50)) for c in P12POLY[hop[0]][0].all_coeffs()) if hop else 1
        print(f'turn image of station {sp.N(st, 20)}: {sp.N(t, 20)} in {hop}; |P12 poly| there {sp.N(val, 5) if val is not None else None}', flush=True)
        check('the turn does not send a 19-design station to a station (50 digits)', val is None or val > 1e-20 * scale)
# ================= NEGATIVE: B4 line (tesseract cap mu 16-cell) shows anisotropy at order 4 =================
E4 = [tuple(K(1 if j == i else 0) * sg for j in range(4)) for i in range(4) for sg in (1, -1)]
C4 = [tuple(K(x) for x in v) for v in itertools.product((1, -1), repeat=4)]
L4 = Line('B4', E4, C4)
faces4, simp4, fv4, _ = L4.chamber(Fr(3, 2))
a4 = [expand(L4, simp4, u, 4, procs=2) for u in [(K(1), K(0), K(0), K(0)), (K(1), K(1), K(1), K(1))]]
check('NEG: B4 line at mu = 3/2: order-2 isotropic but order-4 anisotropic (code sees anisotropy where the group allows it)',
      peq(unitnorm(a4[0], (K(1), K(0), K(0), K(0)), 2), unitnorm(a4[1], (K(1),) * 4, 2)) and not peq(unitnorm(a4[0], (K(1), K(0), K(0), K(0)), 4), unitnorm(a4[1], (K(1),) * 4, 4)))

out = 'data/pds-line-pilot.json' if PILOT else 'data/pds-line.json'
json.dump({'r2': str(r2), 'walls': [str(x) for x in fr], 'hops': results, 'checks': CHECKS}, open(out, 'w'), indent=1, default=str)
nf = sum(1 for _, ok in CHECKS if not ok)
print(f'{len(CHECKS)} checks, {nf} failed, {time.time()-T0:.0f}s')
print('FINAL ok' if nf == 0 else 'FINAL FAIL')
