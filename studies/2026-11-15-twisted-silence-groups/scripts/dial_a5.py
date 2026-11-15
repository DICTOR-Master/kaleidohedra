"""Turning the dial for the golden twist (2I, sigma outer) = A5 acting on R^4 = {x in R^5 : sum x = 0} by even permutations
(the A4 picture of the 600-cell; Fable's golden A4 study shows the twisted classes are S5/A5-orbits there).
For a base point x0 on S^3 the twisted orbit kills degree k iff every A5-invariant harmonic of degree k vanishes at x0
(Goethals-Seidel); the silence locus L_k is that common zero set.  Everything below is in rational arithmetic unless marked.
 A. exact invariant harmonics h_k (k <= KH) from centred power sums q2..q5 and the Vandermonde; dims checked against the
    harmonic Molien series (1+t^10)/((1-t^3)(1-t^4)(1-t^5)).
 B. EDGES (1-dim strata, exact): the C3-fixed circle (a,a,a,b,c) [contains X] and the C2-fixed circle (a,a,b,b,c) [contains F].
    F_k(s u + v) = sum_{g in A5} |x|^2k U_k(<gx,x>/|x|^2) is a polynomial in s with rational coefficients, zero exactly on L_k.
    A gcd-free basis of {sqfree F_k : k <= KSIG} gives every special point on the circle with its exact silence signature;
    real roots by Sturm sequences.  Ordinary comparison on the same circles: the plain S5 action is the same here, so the
    'loud' control is the generic circle point (signature = forced {1,2} only).
 C. FACES (2-dim, transposition-fixed points (a,a,b,c,d)) and INTERIOR (3-dim): numerical Newton from many starts for every
    set K of degrees whose invariant equations number = the dimension (square systems); every root is then CERTIFIED by a
    Krawczyk test in exact rational interval arithmetic (unique zero in a box), and its signature for k <= KH is certified
    (nonzero = some h_k interval excludes 0; zero = defining equation); extra zeros beyond the defining set (overdetermined =
    law-giving candidates) are numerical, flagged.
 D. figures (DICTO mark): signature strip along both edges; loci curves on a face; certified points in the chamber.
Prints CHECK / PROGRESS lines; FINAL ok only if all checks pass."""
import sys, itertools, random, math, json, warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)   # 16 Nov guard: divergent Newton starts printed warnings with absolute paths into the log (privacy guard refused the push)
from fractions import Fraction as Fr
from collections import defaultdict, Counter

KH = int(sys.argv[1]) if len(sys.argv) > 1 else 12          # exact invariant harmonics up to this degree
KSIG = int(sys.argv[2]) if len(sys.argv) > 2 else 30        # edge signatures up to this degree
NSTART = int(sys.argv[3]) if len(sys.argv) > 3 else 400     # Newton starts per system
OUT = sys.argv[4] if len(sys.argv) > 4 else 'data'
fails = 0
def check(ok, what):
    global fails
    if not ok: fails += 1
    print(('CHECK OK   ' if ok else 'CHECK FAIL ') + what, flush=True)

# ---------------- multivariate polynomials over Q (dict exps -> Fraction) ----------------
NV = 5
def padd(a, b, c=1):
    r = dict(a)
    for e, v in b.items():
        r[e] = r.get(e, 0) + c * v
        if r[e] == 0: del r[e]
    return r
def pmul(a, b):
    r = defaultdict(Fr)
    for e1, v1 in a.items():
        for e2, v2 in b.items():
            r[tuple(x + y for x, y in zip(e1, e2))] += v1 * v2
    return {e: v for e, v in r.items() if v != 0}
def ppow(a, n, cache={}):
    key = (id(a), n)
    r = {(0,) * NV: Fr(1)}
    for _ in range(n): r = pmul(r, a)
    return r
def lap(a):
    r = defaultdict(Fr)
    for e, v in a.items():
        for i in range(NV):
            if e[i] >= 2:
                f = list(e); f[i] -= 2; r[tuple(f)] += v * e[i] * (e[i] - 1)
    return {e: v for e, v in r.items() if v != 0}
def lin(c): return {tuple(1 if j == i else 0 for j in range(NV)): Fr(ci) for i, ci in enumerate(c) if ci != 0}

# centred variables y_i = x_i - mean
Y = [lin([Fr(4, 5) if j == i else Fr(-1, 5) for j in range(NV)]) for i in range(NV)]
def q(j):
    r = {}
    for i in range(NV): r = padd(r, ppow(Y[i], j))
    return r
Qs = {j: q(j) for j in (2, 3, 4, 5)}
VDM = {(0,) * NV: Fr(1)}
for i in range(NV):
    for j in range(i + 1, NV): VDM = pmul(VDM, padd(lin([1 if t == i else 0 for t in range(NV)]), lin([1 if t == j else 0 for t in range(NV)]), -1))

def molien_dims(K):
    num = [0] * (K + 1); num[0] = 1
    if K >= 10: num[10] = 1
    ser = num[:]
    for d in (3, 4, 5):
        for i in range(d, K + 1): ser[i] += ser[i - d]
    return ser

def nullspace(rows, ncols):
    """rows: list of dict col->Fr (equations); returns basis of solutions as lists"""
    M = [dict(r) for r in rows]
    piv = {}
    rr = []
    for r in M:
        r = dict(r)
        for c, pr in piv.items():
            if c in r and r[c] != 0:
                f = r[c]
                for cc, vv in pr.items(): r[cc] = r.get(cc, 0) - f * vv
                r = {cc: vv for cc, vv in r.items() if vv != 0}
        if not r: continue
        c0 = min(r); f = r[c0]; r = {cc: vv / f for cc, vv in r.items()}
        for c, pr in list(piv.items()):
            if c0 in pr:
                g = pr[c0]; npr = dict(pr)
                for cc, vv in r.items(): npr[cc] = npr.get(cc, 0) - g * vv
                piv[c] = {cc: vv for cc, vv in npr.items() if vv != 0}
        piv[c0] = r
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fc in free:
        v = [Fr(0)] * ncols; v[fc] = Fr(1)
        for c, pr in piv.items(): v[c] = -pr.get(fc, 0)
        basis.append(v)
    return basis

print('PROGRESS 0.00 A invariant harmonics', flush=True)
mol = molien_dims(KH + 2)
H = {}
for k in range(1, KH + 1):
    mons = []
    for a in range(k // 2 + 1):
        for b in range(k // 3 + 1):
            for c in range(k // 4 + 1):
                for d in range(k // 5 + 1):
                    if 2*a + 3*b + 4*c + 5*d == k: mons.append(('q', a, b, c, d))
                    if 10 + 2*a + 3*b + 4*c + 5*d == k: mons.append(('v', a, b, c, d))
    polys = []
    for m in mons:
        p = {(0,) * NV: Fr(1)}
        for j, e in zip((2, 3, 4, 5), m[1:]):
            if e: p = pmul(p, ppow(Qs[j], e))
        if m[0] == 'v': p = pmul(p, VDM)
        polys.append(p)
    laps = [lap(p) for p in polys]
    allm = sorted({e for L in laps for e in L})
    rows = [{i: laps[i][e] for i in range(len(polys)) if e in laps[i]} for e in allm]
    ns = nullspace(rows, len(polys))
    hs = []
    for v in ns:
        h = {}
        for ci, p in zip(v, polys):
            if ci: h = padd(h, p, ci)
        if h: hs.append(h)
    # harmonic polynomials that vanish identically on the hyperplane would be spurious: none can, as q's are independent there
    H[k] = hs
    print(f'   k={k}: invariant harmonics dim {len(hs)}', flush=True)
hm = [mol[k] for k in range(KH + 1)]
harm_dims = {k: hm[k] - (hm[k - 2] if k >= 2 else 0) for k in range(1, KH + 1)}   # harmonic part of invariants
# the Molien series of the full invariant ring is 1/((1-t^2)) * harmonic series; our mol[] is the HARMONIC series already (no q2 factor)?
# mol[] above uses only 3,4,5 (+t^10): that IS the harmonic series. Compare directly:
check(all(len(H[k]) == molien_dims(KH)[k] for k in range(1, KH + 1)), f'dims of invariant harmonics == harmonic Molien series for k <= {KH}: {[len(H[k]) for k in range(1, KH+1)]}')

def peval(p, x):
    t = 0
    for e, v in p.items():
        m = v
        for xi, ei in zip(x, e):
            if ei: m = m * xi ** ei
        t += m
    return t
def pevalf(p, x):
    t = 0.0
    for e, v in p.items():
        m = float(v)
        for xi, ei in zip(x, e):
            if ei: m *= xi ** ei
        t += m
    return t

# ---------------- B. edges: exact univariate analysis ----------------
A5 = [p for p in itertools.permutations(range(5)) if sum(1 for i in range(5) for j in range(i + 1, 5) if p[i] > p[j]) % 2 == 0]
def u_poly(): pass
# univariate polys in s: list of Fr, low -> high
def uadd(a, b):
    n = max(len(a), len(b)); return utrim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])
def usc(a, c): return utrim([c * x for x in a])
def umul(a, b):
    if not a or not b: return []
    r = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    return utrim(r)
def utrim(a):
    a = list(a)
    while a and a[-1] == 0: a.pop()
    return a
def udivmod(a, b):
    a = list(a); q = [Fr(0)] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        c = a[-1] / b[-1]; s = len(a) - len(b); q[s] = c
        for i, y in enumerate(b): a[s + i] -= c * y
        a = utrim(a)
    return utrim(q), a
def umonic(a): return [x / a[-1] for x in a] if a else a
def ugcd(a, b):
    a, b = utrim(a), utrim(b)
    while b: a, b = b, udivmod(a, b)[1]
    return umonic(a)
def uderiv(a): return utrim([i * a[i] for i in range(1, len(a))])
def usqfree(a): return umonic(udivmod(a, ugcd(a, uderiv(a)))[0]) if len(a) > 1 else a
def ueval(a, x):
    r = 0
    for c in reversed(a): r = r * x + c
    return r
def sturm_count(p):
    """number of distinct real roots of p"""
    if len(p) <= 1: return 0
    seq = [p, uderiv(p)]
    while len(seq[-1]) > 1:
        r = udivmod(seq[-2], seq[-1])[1]
        if not r: break
        seq.append([-x for x in r])
    def var(signs):
        s = [x for x in signs if x != 0]; return sum(1 for i in range(len(s) - 1) if (s[i] > 0) != (s[i + 1] > 0))
    at_pinf = [q[-1] for q in seq]
    at_minf = [q[-1] * (-1) ** (len(q) - 1) for q in seq]
    return var(at_minf) - var(at_pinf)
def real_roots_float(p):
    import cmath
    # Durand-Kerner-free: use numpy if available
    import numpy as np
    r = np.roots([float(c) for c in reversed(p)])
    return sorted(x.real for x in r if abs(x.imag) < 1e-7)

def cheb_coeffs(k):
    """U_k(c) = sum_j (-1)^j C(k-j, j) (2c)^(k-2j)"""
    return [((-1) ** j * math.comb(k - j, j) * 2 ** (k - 2 * j), k - 2 * j) for j in range(k // 2 + 1)]
def edge_F_all(u, v, K):
    """F_k(s u + v), k = 1..K, as univariate polys in s (exact); V_k = nn^k U_k(c/nn) by V_k = 2c V_(k-1) - nn^2 V_(k-2)"""
    x = [[Fr(v[i]), Fr(u[i])] for i in range(5)]
    def ip(a, b):
        r = []
        for i in range(5): r = uadd(r, umul(a[i], b[i]))
        return r
    nn = ip(x, x); nn2 = umul(nn, nn)
    cs = Counter(tuple(ip([x[g[i]] for i in range(5)], x)) for g in A5)
    out = {k: [] for k in range(1, K + 1)}
    for c, mult in cs.items():
        c = list(c); V0, V1 = [Fr(1)], usc(c, Fr(2))
        out[1] = uadd(out[1], usc(V1, Fr(mult)))
        for k in range(2, K + 1):
            V0, V1 = V1, uadd(usc(umul(c, V1), Fr(2)), usc(umul(nn2, V0), Fr(-1)))
            out[k] = uadd(out[k], usc(V1, Fr(mult)))
    return out
def F_at(xv, k):
    nn = sum(t * t for t in xv)
    tot = 0
    for g in A5:
        c = sum(xv[g[i]] * xv[i] for i in range(5))
        for coef, e in cheb_coeffs(k): tot += coef * c ** e * nn ** (k - e)
    return tot

class Q5:   # a + b sqrt5 for exact checks of X and F
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __pow__(s, n):
        r = Q5(1)
        for _ in range(n): r = r * s
        return r
    def z(s): return s.a == 0 and s.b == 0
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
PHI = Q5(Fr(1, 2), Fr(1, 2))
def centred(v):
    m = sum(v, Q5(0)) * Q5(Fr(1, 5)); return [t - m for t in v]
Xp = centred([PHI ** 2, PHI ** 2, PHI ** 2, PHI, Q5(0)])
Fp = centred([PHI ** 2, PHI ** 2, Q5(1), Q5(1), Q5(0)])
sx = [k for k in range(1, 16) if F_at(Xp, k).z()]
sf = [k for k in range(1, 16) if F_at(Fp, k).z()]
check(sx == [1, 2, 5, 7], f'X = perms(phi^2,phi^2,phi^2,phi,0) kills {sx} (expected [1,2,5,7]) in the A5-on-R^4 model')
check(sf == [1, 2, 3, 6], f'F = perms(phi^2,phi^2,1,1,0) kills {sf} (expected [1,2,3,6])')
for k in range(3, KH + 1):     # the exact harmonics vanish at X iff k in signature
    zx = all(peval(h, Xp).z() for h in H[k]); zf = all(peval(h, Fp).z() for h in H[k])
    check(zx == (k in sx) and zf == (k in sf), f'invariant harmonics of degree {k} vanish at X/F exactly as the direct sums say ({zx},{zf})')

EDGES = {'C3 edge (a,a,a,b,c)': ([1, 1, 1, -3, 0], [0, 0, 0, 1, -1]), 'C2 edge (a,a,b,b,c)': ([1, 1, -1, -1, 0], [1, 1, 1, 1, -4])}
edge_report = {}
for ename, (u, v) in EDGES.items():
    print(f'PROGRESS 0.{10 if "C3" in ename else 25} B {ename}', flush=True)
    Fk = edge_F_all(u, v, KSIG)
    inf_sig = [k for k in range(1, KSIG + 1) if F_at([Fr(t) for t in u], k) == 0]     # the point s = infinity (x = u)
    basis = []
    for k in range(1, KSIG + 1):
        f = usqfree(Fk[k]) if len(Fk[k]) > 1 else []
        if len(f) <= 1: continue
        nb = []
        for b in basis:
            g = ugcd(b, f)
            if len(g) <= 1: nb.append(b); continue
            nb.append(g); bb = udivmod(b, g)[0]
            if len(bb) > 1: nb.append(umonic(bb))
            f = udivmod(f, g)[0]
        if len(f) > 1: nb.append(umonic(f))
        basis = nb
    pts = []
    for b in basis:
        nr = sturm_count(b)
        if nr == 0: continue
        sig = [k for k in range(1, KSIG + 1) if len(Fk[k]) <= 1 and not Fk[k] or (len(Fk[k]) > 1 and not udivmod(Fk[k], b)[1])]
        roots = real_roots_float(b)
        pts.append({'minpoly_deg': len(b) - 1, 'minpoly': [str(c) for c in b] if len(b) <= 4 else None, 'real_roots': nr,
                    's_values': roots, 'signature': sig})
    # every point of the circle kills 1, 2 (forced); generic points nothing else
    gen = [k for k in range(1, KSIG + 1) if not Fk[k]]
    check(gen == [1, 2], f'{ename}: degrees killed identically along the edge = {gen} (forced by A5: [1, 2])')
    print(f'TABLE {ename}: special points (s = coordinate along the edge, x = s u + v; s = inf -> u kills {inf_sig})')
    for p in sorted(pts, key=lambda p: -len(p['signature'])):
        extra = [k for k in p['signature'] if k > 2]
        print(f'   minpoly deg {p["minpoly_deg"]} ({p["real_roots"]} real) s~{[round(r, 6) for r in p["s_values"]]} kills<=30: {p["signature"]}  {"MULTI-SILENT" if len(extra) >= 2 else ""} {p["minpoly"] or ""}', flush=True)
    edge_report[ename] = {'points': pts, 'infinity_signature': inf_sig}
json.dump(edge_report, open(f'{OUT}/dial_a5_edges.json', 'w'), indent=1)

# ---------------- C. faces and interior: certified multi-silent points ----------------
print('PROGRESS 0.40 C numeric location + Krawczyk certification', flush=True)
import numpy as np
W = [[1, -1, 0, 0, 0], [1, 1, -2, 0, 0], [1, 1, 1, -3, 0], [1, 1, 1, 1, -4]]
def to_x(y): return [sum(y[i] * W[i][j] for i in range(4)) for j in range(5)]
def compose(h, A):
    """substitute x = A y (A: 5 x m rational) into h: returns poly in m variables"""
    m = len(A[0])
    global NV
    lins = [{tuple(1 if t == c else 0 for t in range(m)): Fr(A[j][c]) for c in range(m) if A[j][c] != 0} for j in range(5)]
    r = {}
    for e, v in h.items():
        t = {(0,) * m: v}
        for j, ej in enumerate(e):
            for _ in range(ej): t = pmul2(t, lins[j])
        r = padd(r, t)
    return r
def pmul2(a, b):
    r = defaultdict(Fr)
    for e1, v1 in a.items():
        for e2, v2 in b.items(): r[tuple(x + y for x, y in zip(e1, e2))] += v1 * v2
    return {e: v for e, v in r.items() if v != 0}
def deriv(p, i):
    r = {}
    for e, v in p.items():
        if e[i]:
            f = list(e); f[i] -= 1; r[tuple(f)] = r.get(tuple(f), 0) + v * e[i]
    return r
def ev_np(p, y):
    t = 0.0
    for e, v in p.items():
        m = float(v)
        for yi, ei in zip(y, e):
            if ei: m *= yi ** ei
        t += m
    return t

# interval arithmetic on Fractions
def imul(a, b):
    c = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]; return (min(c), max(c))
def ipow(a, n):
    if n == 0: return (Fr(1), Fr(1))
    lo, hi = a
    if n % 2 == 0 and lo < 0 < hi: return (Fr(0), max(lo ** n, hi ** n))
    c = [lo ** n, hi ** n]; return (min(c), max(c))
def ieval(p, box):
    lo = hi = Fr(0)
    pw = [{} for _ in box]
    for e, v in p.items():
        t = (Fr(v), Fr(v))
        for i, ei in enumerate(e):
            if ei:
                if ei not in pw[i]: pw[i][ei] = ipow(box[i], ei)
                t = imul(t, pw[i][ei])
        lo += t[0]; hi += t[1]
    return (lo, hi)
def krawczyk(polys, y0, rad):
    """polys: n polys in n vars (rational); y0 float approx root; returns (ok, box) with ok = unique root certified in box"""
    n = len(polys)
    c = [Fr(t).limit_denominator(10 ** 14) for t in y0]
    box = [(ci - rad, ci + rad) for ci in c]
    J = [[deriv(p, i) for i in range(n)] for p in polys]
    Jc = np.array([[ev_np(J[a][b], [float(t) for t in c]) for b in range(n)] for a in range(n)])
    try: Yf = np.linalg.inv(Jc)
    except np.linalg.LinAlgError: return False, box
    Yq = [[Fr(Yf[a][b]).limit_denominator(10 ** 12) for b in range(n)] for a in range(n)]
    fc = [ieval(p, [(ci, ci) for ci in c])[0] for p in polys]
    JX = [[ieval(J[a][b], box) for b in range(n)] for a in range(n)]
    for a in range(n):
        val = c[a] - sum(Yq[a][b] * fc[b] for b in range(n))
        lo = hi = val
        for b in range(n):
            # (I - Y J(X))_{ab} (X_b - c_b)
            m = (Fr(1 if a == b else 0), Fr(1 if a == b else 0))
            for t in range(n):
                prod = imul((Yq[a][t], Yq[a][t]), JX[t][b])
                m = (m[0] - prod[1], m[1] - prod[0])
            d = imul(m, (box[b][0] - c[b], box[b][1] - c[b]))
            lo += d[0]; hi += d[1]
        if not (box[a][0] < lo and hi < box[a][1]): return False, box
    return True, box

def search(stratum, A, dimS, KSET_LIMIT):
    """A: 5 x m matrix (rational) of the chart x = A y with last chart coordinate fixed to 1; dimS = dim of the stratum on S^3"""
    m = len(A[0])
    Hc = {k: [compose(h, A) for h in H[k]] for k in range(3, KH + 1)}
    # dehomogenise: set y_{m-1} = 1
    def dehom(p):
        r = {}
        for e, v in p.items(): r[e[:-1]] = r.get(e[:-1], 0) + v
        return {e: v for e, v in r.items() if v != 0}
    Hd = {k: [dehom(p) for p in Hc[k]] for k in Hc}
    Hd = {k: [p for p in L if p] for k, L in Hd.items()}
    dims = {k: len(Hd[k]) for k in Hd}
    nv = m - 1
    found = []
    ks = [k for k in range(3, KH + 1) if dims[k] > 0]
    combos = []
    for r in range(1, nv + 1):
        for K in itertools.combinations(ks, r):
            # use as many equations as unknowns: if total > nv the system is overdetermined (skip here: found as extras)
            eqs = [(k, p) for k in K for p in Hd[k]]
            if len(eqs) == nv: combos.append((K, eqs))
    rng = np.random.default_rng(7)
    def comp(p):
        E = np.array(list(p.keys()), dtype=float).reshape(-1, nv); c = np.array([float(v) for v in p.values()]); return E, c
    def bev(Ec, Yb):
        E, c = Ec
        return (np.prod(Yb[:, None, :] ** E[None, :, :], axis=2)) @ c
    for ci, (K, eqs) in enumerate(combos):
        sols = []
        Fc = [comp(p) for _, p in eqs]
        Jc = [[comp(deriv(p, i)) if deriv(p, i) else None for i in range(nv)] for _, p in eqs]
        Yb = rng.normal(size=(NSTART, nv)) * 1.5
        for it in range(80):
            f = np.stack([bev(e, Yb) for e in Fc], 1)
            Jm = np.stack([np.stack([bev(Jc[a][i], Yb) if Jc[a][i] is not None else np.zeros(len(Yb)) for i in range(nv)], 1) for a in range(len(eqs))], 1)
            ok = np.abs(np.linalg.det(Jm)) > 1e-300
            dy = np.zeros_like(Yb)
            dy[ok] = np.linalg.solve(Jm[ok], -f[ok][:, :, None])[:, :, 0]
            Yb = Yb + dy
            Yb[~np.isfinite(Yb)] = 1e9
        for y in Yb:
            if not np.all(np.isfinite(y)) or np.linalg.norm(y) > 1e6: continue
            f = np.array([ev_np(p, y) for _, p in eqs])
            if np.linalg.norm(f) > 1e-9: continue
            # polish
            for it in range(5):
                Jm1 = np.array([[ev_np(deriv(p, i), y) for i in range(nv)] for _, p in eqs])
                try: y = y + np.linalg.solve(Jm1, -np.array([ev_np(p, y) for _, p in eqs]))
                except np.linalg.LinAlgError: break
            x = np.array([float(sum(A[j][i] * (y[i] if i < nv else 1) for i in range(m))) for j in range(5)])
            x = x / np.linalg.norm(x)
            key = tuple(np.round(sorted(x), 7))
            key2 = tuple(np.round(sorted(-x), 7))
            if any(np.allclose(key, s_[0], atol=1e-6) or np.allclose(key2, s_[0], atol=1e-6) for s_ in sols): continue
            sols.append((key, y.copy(), x))
        for key, y, x in sols:
            ok, box = krawczyk([p for _, p in eqs], y, Fr(1, 10 ** 8))
            # certified signature for k <= KH
            sig_c = []
            for k in range(1, KH + 1):
                if k <= 2: sig_c.append(k); continue
                if k in K: sig_c.append(k); continue
                nz = any((lambda iv: iv[0] > 0 or iv[1] < 0)(ieval(p, box)) for p in Hd[k]) if ok else False
                if not nz:
                    vals = [abs(ev_np(p, y)) for p in Hd[k]]
                    sig_c.append(f'{k}?')        # numerically zero or not certified
            sig_n = [k for k in range(1, KSIG + 1) if abs(F_at(list(x), k)) < 1e-9 * 60]
            extra = [k for k in sig_n if k > 2 and k not in K]
            stab = sum(1 for g in A5 if np.allclose([x[g[i]] for i in range(5)], x, atol=1e-3))
            found.append({'stratum': stratum, 'K': list(K), 'x_sorted': [float(t) for t in key], 'certified': ok,
                          'signature_certified_k<=%d' % KH: [str(s) for s in sig_c], 'signature_numeric_k<=%d' % KSIG: sig_n,
                          'extra_numeric': extra, 'orbit_size': 60 // stab})
            print(f'   {stratum} K={K} x~{np.round(key, 5).tolist()} |orbit|={60//stab} krawczyk={ok} sig(cert,k<={KH})={sig_c} sig(num,k<={KSIG})={sig_n} {"OVERDETERMINED extra=" + str(extra) if extra else ""}', flush=True)
        print(f'PROGRESS {0.4 + 0.25 * (1 if stratum == "interior" else 0) + 0.25 * (ci + 1) / len(combos):.3f} {stratum} K={K}: {len(sols)} solutions', flush=True)
    return found

# face x1 = x2 (transposition-fixed): x = A y, y in R^3 ; chart fixes the last coordinate
AF = [[1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [-2, -1, -1]]
AI = [[W[i][j] for i in range(4)] for j in range(5)]
res = search('face', AF, 2, 2) + search('interior', AI, 3, 3)
json.dump(res, open(f'{OUT}/dial_a5_points.json', 'w'), indent=1)
def classify(r):
    x = r['x_sorted']
    if r['certified']: return 'certified'
    if not all(k in r['signature_numeric_k<=%d' % KSIG] for k in r['K']): return 'spurious (Newton false convergence; defining zeros not confirmed by the direct sums)'
    if r['orbit_size'] < 60: return 'lower stratum (edge or line; treated exactly in B)'
    if all(abs(a + b) < 1e-5 for a, b in zip(x, reversed(x))): return 'antipodal circle (a,b,0,-b,-a): odd degrees forced by -1 in the orbit, so the system is singular there'
    return 'UNEXPLAINED'
for r in res: r['class'] = classify(r)
from collections import Counter as _C
print('TABLE located points by class:', dict(_C(r['class'] for r in res)))
for r in res:
    if r['class'] == 'UNEXPLAINED': print('   UNEXPLAINED', r)
check(all(r['class'] != 'UNEXPLAINED' for r in res), f'every located point is certified or explained (lower stratum / antipodal circle / spurious); total {len(res)}')
json.dump(res, open(f'{OUT}/dial_a5_points.json', 'w'), indent=1)
print('TABLE certified isolated multi-silent points (generic = 60-point orbit off the antipodal circle):')
seen = set()
for r in res:
    if r['class'] != 'certified': continue
    anti = all(abs(a + b) < 1e-5 for a, b in zip(r['x_sorted'], reversed(r['x_sorted'])))
    key = (tuple(round(t, 5) for t in r['x_sorted']))
    if key in seen: continue
    seen.add(key)
    print(f"   {r['stratum']:8s} {'antipodal' if anti else 'generic  '} defining K={r['K']} certified sig(k<={KH})={r['signature_certified_k<=%d' % KH]} numeric sig(k<={KSIG})={r['signature_numeric_k<=%d' % KSIG]} x={[round(t, 6) for t in r['x_sorted']]}")
# ---------------- D. figures ----------------
print('PROGRESS 0.92 D figures', flush=True)
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 1, figsize=(9, 6.5))
    for ax, (ename, (u, v)) in zip(axs, EDGES.items()):
        th = np.linspace(0, np.pi, 1441)
        uu = np.array(u, float); vv = np.array(v, float); uu /= np.linalg.norm(uu); vv /= np.linalg.norm(vv)
        for k in range(3, 16):
            vals = np.array([F_at(list(np.cos(t) * vv + np.sin(t) * uu), k) for t in th])
            ax.plot(np.degrees(th), k + 0.8 * vals / vals.max(), lw=0.8, color='0.35')
        for p in edge_report[ename]['points']:
            for s in p['s_values']:
                xx = s * np.array(u, float) + np.array(v, float)
                t = np.arctan2(np.dot(xx, uu), np.dot(xx, vv)) % np.pi
                for k in p['signature']:
                    if 3 <= k < 16: ax.plot(np.degrees(t), k, 'o', ms=4, color='#c0392b' if len([q for q in p['signature'] if q > 2]) >= 2 else '#2c7fb8')
        ax.set_title(f'{ename}: silence of degree k (rows) as the base point turns; red = multi-silent', fontsize=9)
        ax.set_ylabel('degree k'); ax.set_yticks(range(3, 16))
    axs[-1].set_xlabel('angle along the edge circle (degrees)')
    fig.text(0.99, 0.005, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
    fig.tight_layout(); fig.savefig('figs/dial_edges.png', dpi=150)
    # face map: sign of h_k for k = 3..7 on the face chart (2 parameters)
    Hf = {k: [compose(h, AF) for h in H[k]] for k in range(3, 8)}
    fig, ax = plt.subplots(figsize=(7, 7))
    a_ = np.linspace(-3, 3, 241)
    A_, B_ = np.meshgrid(a_, a_)
    cols = {3: '#1b9e77', 4: '#d95f02', 5: '#7570b3', 6: '#e7298a', 7: '#66a61e'}
    for k in range(3, 8):
        Z = np.vectorize(lambda a, b: ev_np(Hf[k][0], [a, b, 1.0]))(A_, B_)
        ax.contour(A_, B_, Z, levels=[0], colors=cols[k], linewidths=1.1)
        ax.plot([], [], color=cols[k], label=f'L{k}')
    for r in res:
        if r['stratum'] == 'face':
            x = np.array(r['x_sorted'])
    ax.legend(fontsize=8); ax.set_title('silence loci L3..L7 on the face x1 = x2 (chart y3 = 1)', fontsize=9)
    fig.text(0.99, 0.005, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
    fig.tight_layout(); fig.savefig('figs/dial_face_loci.png', dpi=150)
    # chamber map: certified points, coordinates (x5 - x4, x2 - x1) of the sorted point, colour = defining degrees
    fig, ax = plt.subplots(figsize=(7.5, 6))
    for r in res:
        if r['class'] not in ('certified',): continue
        x = r['x_sorted']; anti = all(abs(a + b) < 1e-5 for a, b in zip(x, reversed(x)))
        ax.plot(x[4] - x[3], x[1] - x[0], 'o' if r['stratum'] == 'interior' else 's', ms=6, color='#c0392b' if anti else '#2c7fb8', alpha=0.8)
        ax.annotate(','.join(map(str, r['K'])), (x[4] - x[3], x[1] - x[0]), fontsize=6, xytext=(3, 2), textcoords='offset points')
    for nm, xx in (('X', Xp), ('F', Fp)):
        v = sorted(float(t) for t in xx); n_ = sum(t * t for t in v) ** 0.5; v = [t / n_ for t in v]
        ax.plot(v[4] - v[3], v[1] - v[0], '*', ms=14, color='#f1c40f', mec='k'); ax.annotate(nm, (v[4] - v[3], v[1] - v[0]), fontsize=9, xytext=(5, 5), textcoords='offset points')
    ax.set_xlabel('x5 - x4 (sorted coordinates)'); ax.set_ylabel('x2 - x1')
    ax.set_title('certified multi-silent base points (squares: face, dots: interior; red: antipodal circle; stars: X, F)', fontsize=8)
    fig.text(0.99, 0.005, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
    fig.tight_layout(); fig.savefig('figs/dial_chamber_points.png', dpi=150)
    check(True, 'figures written')
except Exception as e:
    check(False, f'figures: {e}')
print(f'checks failed: {fails}')
print('FINAL ok' if fails == 0 else 'FINAL FAIL')
