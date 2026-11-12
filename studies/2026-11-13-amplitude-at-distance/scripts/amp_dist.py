#!/usr/bin/env python3
"""Amplitude at a distance (13 Nov 2026; aim 2): test of DICTO's proposition "law giving shapes act at a distance governed by their
amplitude" (amplitude = canonical form Omega_P). Pre-registered tests T0-T3 are in ../README.md (written before this ran).
Exact arithmetic: each shape lives in Q or Q(sqrt D) (class QD below); Omega by Warren's vertex formula; Laurent series in eps along
lines decide poles / zeros / critical points / Hessian signs exactly. Lattice incidence (points on facet planes) is decided exactly
with sympy (minimal polynomials, PSLQ coordinates verified exactly, integer Hermite reduction). Lattice sums are floating point with
a certified rounding bound (standard model, unit roundoff 2^-53); their tails are extrapolated (not certified).
Usage: python -u amp_dist.py [--pilot]"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import sys, time, json, itertools, random, math
from fractions import Fraction as Fr
from multiprocessing import get_context
import numpy as np
from scipy.spatial import ConvexHull
import sympy as sp
import mpmath as mp

PILOT = '--pilot' in sys.argv
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
OK = True; NCHK = 0
OUT = {'pilot': PILOT}
def check(name, cond):
    global OK, NCHK
    NCHK += 1; OK &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)
def prog(fr, what): print(f'PROGRESS {fr:.2f} {what} ({time.time() - T0:.0f} s)', flush=True)

# ---------------------------------------------------------------- exact field Q(sqrt D)
class QD:
    __slots__ = ('a', 'b', 'D')
    def __init__(s, a=0, b=0, D=0): s.a = Fr(a); s.b = Fr(b); s.D = D
    def c(s, o): return o if isinstance(o, QD) else QD(o, 0, s.D)
    def _d(s, o): return s.D if s.D else o.D
    def __add__(s, o): o = s.c(o); return QD(s.a + o.a, s.b + o.b, s._d(o))
    __radd__ = __add__
    def __sub__(s, o): o = s.c(o); return QD(s.a - o.a, s.b - o.b, s._d(o))
    def __rsub__(s, o): return s.c(o) - s
    def __neg__(s): return QD(-s.a, -s.b, s.D)
    def __mul__(s, o):
        o = s.c(o); D = s._d(o)
        if s.D and o.D and s.D != o.D and s.b and o.b: raise ValueError('field mix')
        return QD(s.a * o.a + D * s.b * o.b, s.a * o.b + s.b * o.a, D)
    __rmul__ = __mul__
    def inv(s):
        n = s.a * s.a - s.D * s.b * s.b
        if n == 0: raise ZeroDivisionError
        return QD(s.a / n, -s.b / n, s.D)
    def __truediv__(s, o): return s * s.c(o).inv()
    def __rtruediv__(s, o): return s.c(o) * s.inv()
    def __pow__(s, k):
        r = QD(1, 0, s.D)
        for _ in range(k): r = r * s
        return r
    def z(s): return s.a == 0 and s.b == 0
    def sign(s):
        sa = (s.a > 0) - (s.a < 0); sb = (s.b > 0) - (s.b < 0)
        if sb == 0: return sa
        if sa == 0 or sa == sb: return sb if sa == 0 else sa
        return sa if s.a * s.a > s.D * s.b * s.b else sb
    def __abs__(s): return -s if s.sign() < 0 else s
    def f(s): return float(s.a) + float(s.b) * math.sqrt(s.D) if s.b else float(s.a)
    def sym(s): return sp.Rational(s.a.numerator, s.a.denominator) + sp.Rational(s.b.numerator, s.b.denominator) * sp.sqrt(s.D)
    def key(s): return (s.a, s.b)
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f'({s.a}{"+" if s.b > 0 else "-"}{abs(s.b)}*sqrt{s.D})'

def vec(D, *xs): return tuple(x if isinstance(x, QD) else QD(x, 0, D) for x in xs)
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def det3(u, v, w): return dot(u, cross(v, w))
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def mul(k, u): return tuple(k * a for a in u)
def fl(u): return np.array([x.f() for x in u])
def vkey(u): return tuple(x.key() for x in u)
def det4(M):
    def d3(r): return (r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1]) - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
                       + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0]))
    tot = 0
    for j in range(4):
        t = M[0][j] * d3([[M[i][k] for k in range(4) if k != j] for i in range(1, 4)])
        tot = tot + t if j % 2 == 0 else tot - t
    return tot

# ---------------------------------------------------------------- exact polytope from halfspaces
class Poly:
    def __init__(s, name, H, D):
        s.name, s.D = name, D
        H = [(vec(D, *n), b if isinstance(b, QD) else QD(b, 0, D)) for n, b in H]
        V = {}
        for i, j, k in itertools.combinations(range(len(H)), 3):
            (ni, bi), (nj, bj), (nk, bk) = H[i], H[j], H[k]
            dt = det3(ni, nj, nk)
            if dt.z(): continue
            x = mul(QD(1, 0, D) / dt, add(add(mul(bi, cross(nj, nk)), mul(bj, cross(nk, ni))), mul(bk, cross(ni, nj))))
            if all((b - dot(n, x)).sign() >= 0 for n, b in H): V[vkey(x)] = x
        s.V = list(V.values()); s.Vf = np.array([fl(v) for v in s.V])
        F = []
        for n, b in H:
            on = [q for q, v in enumerate(s.V) if (b - dot(n, v)).z()]
            if len(on) >= 3: F.append((n, b, on))
        s.F = F; s.Nf = np.array([fl(n) for n, b, _ in F]); s.bf = np.array([b.f() for n, b, _ in F])
        s.tight = [[fi for fi, (n, b, on) in enumerate(F) if q in on] for q in range(len(s.V))]
        s.terms = []
        for q, T in enumerate(s.tight):
            if len(T) == 3: tris = [tuple(T)]
            else:
                Nn = s.Nf[T] / np.linalg.norm(s.Nf[T], axis=1)[:, None]
                c = Nn.sum(0); c /= np.linalg.norm(c); e1 = Nn[0] - (Nn[0] @ c) * c; e1 /= np.linalg.norm(e1); e2 = np.cross(c, e1)
                o = [T[i] for i in np.argsort([np.arctan2(x @ e2, x @ e1) for x in Nn])]
                tris = [(o[0], o[i], o[i + 1]) for i in range(1, len(o) - 1)]
            for tr in tris:
                d = abs(det3(*[F[k][0] for k in tr])); assert not d.z()
                s.terms.append((q, tr, d))
        s.ia = np.array([t[1][0] for t in s.terms]); s.ib = np.array([t[1][1] for t in s.terms]); s.ic = np.array([t[1][2] for t in s.terms])
        s.df = np.array([t[2].f() for t in s.terms])
        # facet polygons in cyclic order (for the triangulation formula)
        s.Fcyc = []
        for n, b, on in F:
            nf = fl(n); c = s.Vf[on].mean(0); e1 = s.Vf[on[0]] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(nf, e1); e2 /= np.linalg.norm(e2)
            s.Fcyc.append([on[i] for i in np.argsort([np.arctan2((s.Vf[v] - c) @ e2, (s.Vf[v] - c) @ e1) for v in on])])
        E = sum(len(on) for _, _, on in F) // 2
        assert len(s.V) - E + len(F) == 2, (name, 'Euler')
        s.vol = s.vol6() / 6
    def fvals(s, Y): return [b - dot(n, Y) for n, b, _ in s.F]
    def omega(s, Y, drop=None):
        f = s.fvals(Y); tot = QD(0, 0, s.D)
        for i, (q, (a, b, c), d) in enumerate(s.terms):
            if i != drop: tot = tot + d / (f[a] * f[b] * f[c])
        return tot
    def omega_tri(s, Y):
        one = QD(1, 0, s.D); Zh = lambda p: (one, p[0], p[1], p[2]); Yh = Zh(Y); tot = QD(0, 0, s.D)
        for (n, b, on), cyc in zip(s.F, s.Fcyc):
            if 0 in on: continue
            for i in range(1, len(cyc) - 1):
                Z = [Zh(s.V[0]), Zh(s.V[cyc[0]]), Zh(s.V[cyc[i]]), Zh(s.V[cyc[i + 1]])]
                o = det4(Z)
                if o.sign() < 0: Z[0], Z[1] = Z[1], Z[0]; o = -o
                den = one
                for j in range(4): den = den * det4([Z[k] if k != j else Yh for k in range(4)])
                tot = tot + o ** 3 / den
        return tot
    def vol6(s):
        cen = mul(QD(Fr(1, len(s.V)), 0, s.D), tuple(sum((v[i] for v in s.V), QD(0, 0, s.D)) for i in range(3)))
        tot = QD(0, 0, s.D)
        for cyc in s.Fcyc:
            for i in range(1, len(cyc) - 1):
                tot = tot + abs(det3(sub(s.V[cyc[0]], cen), sub(s.V[cyc[i]], cen), sub(s.V[cyc[i + 1]], cen)))
        return tot
    def polar6(s, Y):
        f = s.fvals(Y); assert all(x.sign() > 0 for x in f)
        U = [mul(QD(1, 0, s.D) / fi, n) for (n, b, _), fi in zip(s.F, f)]
        h = ConvexHull(np.array([fl(u) for u in U])); tot = QD(0, 0, s.D)
        for a, b, c in h.simplices: tot = tot + abs(det3(U[a], U[b], U[c]))
        return tot
    def centrally_symmetric(s):
        keys = {vkey(v) for v in s.V}
        return all(vkey(mul(QD(-1, 0, s.D), v)) in keys for v in s.V)

# ---------------------------------------------------------------- exact Laurent series in eps
NS = 2   # orders kept in results
def ls_lininv(c0, c1, N):
    """1/(c0 + c1 eps) as {order: coeff}"""
    if c0.z():
        if c1.z(): raise ZeroDivisionError('degenerate line (factor identically 0)')
        return {-1: 1 / c1}
    r = 1 / c0; q = -c1 * r; out = {}; t = r
    for k in range(N + 1): out[k] = t; t = t * q
    return out
def ls_mul(A, B, N):
    out = {}
    for i, a in A.items():
        for j, b in B.items():
            if i + j <= N: out[i + j] = out.get(i + j, 0) + a * b
    return out
def ls_add(A, B):
    out = dict(A)
    for k, v in B.items(): out[k] = out.get(k, 0) + v
    return out
def ls_clean(A, D): return {k: (v if isinstance(v, QD) else QD(v, 0, D)) for k, v in A.items() if not (v if isinstance(v, QD) else QD(v, 0, D)).z()}

def omega_series(P, x0, w, N=NS):
    """Laurent series of Omega_P(x0 + eps w) up to order N (exact)"""
    M = N + 3; f0 = P.fvals(x0); f1 = [-dot(n, w) for n, b, _ in P.F]
    inv = [ls_lininv(a, b, M) for a, b in zip(f0, f1)]
    tot = {}
    for q, (a, b, c), d in P.terms:
        tot = ls_add(tot, {k: d * v for k, v in ls_mul(ls_mul(inv[a], inv[b], M), inv[c], N).items()})
    return ls_clean(tot, P.D)

def hk_series(xs, k, M):
    """complete homogeneous symmetric polynomial h_k of three Laurent series"""
    pw = []
    for x in xs:
        p = [{0: 1}]
        for _ in range(k): p.append(ls_mul(p[-1], x, M))
        pw.append(p)
    tot = {}
    for i in range(k + 1):
        for j in range(k + 1 - i):
            tot = ls_add(tot, ls_mul(ls_mul(pw[0][i], pw[1][j], M), pw[2][k - i - j], M))
    return tot
def ak_series(P, u0, dl, k, N=NS):
    """series of the far-field coefficient a_k(u0 + eps dl), where Omega(r u) = sum_k a_k(u) r^(-3-k),
    a_k(u) = -sum_terms d h_k(b_a/w_a, b_b/w_b, b_c/w_c) / (w_a w_b w_c), w = n.u (exact)"""
    M = N + 2 * k + 8
    inv = [ls_lininv(dot(n, u0), dot(n, dl), M) for n, b, _ in P.F]
    tot = {}
    for q, (a, b, c), d in P.terms:
        pr = ls_mul(ls_mul(inv[a], inv[b], M), inv[c], M)
        h = hk_series([{kk: P.F[j][1] * v for kk, v in inv[j].items()} for j in (a, b, c)], k, M)
        tot = ls_add(tot, {kk: -d * v for kk, v in ls_mul(pr, h, M).items()})
    return ls_clean({kk: v for kk, v in tot.items() if kk <= N}, P.D)
def far_series(P, u0, dl, k, N=NS):
    """series of F(u) = a_k(u)^2 (u.u)^(3+k): degree 0, rational; its critical type equals that of the profile a_k on the sphere
    where a_k > 0 and is flipped where a_k < 0"""
    A = ak_series(P, u0, dl, k, N + 4)
    if any(kk < 0 for kk in A): return A
    nrm = {0: dot(u0, u0), 1: 2 * dot(u0, dl), 2: dot(dl, dl)}; pw = {0: 1}
    for _ in range(3 + k): pw = ls_mul(pw, nrm, N)
    return ls_clean(ls_mul(ls_mul(A, A, N), pw, N), P.D)
def far_classify(P, u0, k, seed):
    d1, d2 = tangent_pair(P, u0, seed)
    A = ak_series(P, u0, d1, k)
    if any(kk < 0 for kk in A): return {'kind': 'pole', 'order': min(A)}
    a0 = A.get(0, QD(0, 0, P.D))
    if a0.z(): return {'kind': 'zero of the profile'}
    r = classify(lambda u, dl: far_series(P, u, dl, k), u0, d1, d2)
    if r['kind'] == 'critical' and a0.sign() < 0: r['type'] = {'max': 'min', 'min': 'max'}.get(r['type'], r['type'])
    r['value'] = a0.f(); r['sign'] = a0.sign()
    return r
def ak_exact(P, u, k):
    w = [dot(n, u) for n, b, _ in P.F]; tot = QD(0, 0, P.D)
    for q, (a, b, c), d in P.terms:
        x = [P.F[j][1] / w[j] for j in (a, b, c)]; h = QD(0, 0, P.D)
        for i in range(k + 1):
            for j in range(k + 1 - i): h = h + x[0] ** i * x[1] ** j * x[2] ** (k - i - j)
        tot = tot - d * h / (w[a] * w[b] * w[c])
    return tot
def ak_float(P, U, k):
    W = U @ P.Nf.T; X = [P.bf[None, ia] / W[:, ia] for ia in (P.ia, P.ib, P.ic)]
    h = np.zeros_like(X[0])
    for i in range(k + 1):
        for j in range(k + 1 - i): h += X[0] ** i * X[1] ** j * X[2] ** (k - i - j)
    return -(P.df[None, :] * h / (W[:, P.ia] * W[:, P.ib] * W[:, P.ic])).sum(1)

def fan_identity(P, u):
    w = [dot(n, u) for n, b, _ in P.F]; tot = QD(0, 0, P.D)
    for q, (a, b, c), d in P.terms: tot = tot + d / (w[a] * w[b] * w[c])
    return tot

def tangent_pair(P, x0, seed):
    """two exact tangent vectors at x0 (perpendicular to x0), generic for the planes that meet x0 (facet planes through x0,
    and planes through 0 with n.x0 = 0, which carry the far-field poles)"""
    rng = random.Random(seed)
    crit = [n for n, b, _ in P.F if dot(n, x0).z() or (b - dot(n, x0)).z()]
    while True:
        a = vec(P.D, *[rng.randint(-29, 29) for _ in range(3)])
        d1 = sub(mul(dot(x0, x0), a), mul(dot(a, x0), x0)); d2 = cross(x0, d1)
        if any(not x.z() for x in d1) and all(not dot(n, d1).z() and not dot(n, d2).z() and not dot(n, add(d1, d2)).z() for n in crit):
            return d1, d2

def classify(series_fn, x0, d1, d2, curv=None):
    """series_fn(x0, dir) -> Laurent dict. Returns kind: pole / zero-crit / critical(max|min|saddle|degenerate) / regular, value"""
    S1, S2, S3 = series_fn(x0, d1), series_fn(x0, d2), series_fn(x0, add(d1, d2))
    if any(k < 0 for S in (S1, S2, S3) for k in S):
        return {'kind': 'pole', 'order': min(min(S) for S in (S1, S2, S3) if S)}
    val = S1.get(0, QD(0, 0, x0[0].D))
    g1, g2 = S1.get(1), S2.get(1)
    if g1 is not None or g2 is not None:
        return {'kind': 'regular', 'value': val.f(), 'sign': val.sign()}
    q1, q2, q3 = [S.get(2, QD(0, 0, x0[0].D)) for S in (S1, S2, S3)]
    if curv is not None:   # finite sphere: subtract |d|^2/(2 r^2) * (grad.x0)
        q1, q2, q3 = q1 - curv(d1), q2 - curv(d2), q3 - curv(add(d1, d2))
    q12 = (q3 - q1 - q2) / 2; det = q1 * q2 - q12 * q12
    if det.sign() > 0: typ = 'max' if q1.sign() < 0 else 'min'
    elif det.sign() < 0: typ = 'saddle'
    else: typ = 'degenerate'
    return {'kind': 'critical', 'type': typ, 'value': val.f(), 'sign': val.sign(), 'zero': val.z()}

# ---------------------------------------------------------------- shapes
def perms3(v):
    return {p for p in itertools.permutations(v)}
def signs(v):
    out = set()
    for s in itertools.product([1, -1], repeat=3): out.add(tuple(a * b for a, b in zip(s, v)))
    return out
def all_sp(v):
    out = set()
    for p in perms3(v): out |= signs(p)
    return out
RDn = sorted(x for x in all_sp((1, 1, 0)))
HCPnb = [(1, -1, 0), (0, 1, -1), (1, 0, -1), (-1, 1, 0), (0, -1, 1), (-1, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 0),
         (Fr(-1, 3), Fr(-4, 3), Fr(-1, 3)), (Fr(-4, 3), Fr(-1, 3), Fr(-1, 3)), (Fr(-1, 3), Fr(-1, 3), Fr(-4, 3))]
def build_shapes():
    S = {}
    S['RD'] = Poly('RD', [(n, 1) for n in RDn], 0)
    S['TRD'] = Poly('TRD', [(n, Fr(sum(x * x for x in n)) / 2) for n in HCPnb], 0)
    S['cube'] = Poly('cube', [(n, Fr(1, 2)) for n in all_sp((1, 0, 0))], 0)
    S['TO'] = Poly('TO', [(n, Fr(1, 2)) for n in all_sp((1, 0, 0))] + [(n, Fr(3, 4)) for n in signs((1, 1, 1))], 0)
    S['HP'] = Poly('HP', [(n, 1) for n in HCPnb[:6]] + [((1, 1, 1), QD(0, Fr(1, 2), 6)), ((-1, -1, -1), QD(0, Fr(1, 2), 6))], 6)
    phi = QD(Fr(1, 2), Fr(1, 2), 5); iphi = phi - 1; one = QD(1, 0, 5); zero = QD(0, 0, 5)
    def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
    ico = [p for s1 in (1, -1) for s2 in (1, -1) for p in cyc((zero, one * s1, phi * s2))]
    dod = [vec(5, *s) for s in signs((1, 1, 1))] + [p for s1 in (1, -1) for s2 in (1, -1) for p in cyc((zero, phi * s1, iphi * s2))]
    def from_normals(name, normals, corners):
        H = []
        for n in normals:
            b = max((dot(n, v) for v in corners), key=lambda x: x.f()); H.append((n, b))
        return Poly(name, H, 5)
    S['icosahedron'] = from_normals('icosahedron', dod, ico)
    S['dodecahedron'] = from_normals('dodecahedron', ico, dod)
    S['RD-perturbed'] = Poly('RD-perturbed', [(n, Fr(21, 20) if n == (1, 1, 0) else 1) for n in RDn], 0)
    return S
def from_vertices(name, pts, D):
    P = {vkey(p): p for p in pts}; P = list(P.values()); Pf = np.array([fl(p) for p in P]); h = ConvexHull(Pf)
    cen = mul(QD(Fr(1, len(P)), 0, D), tuple(sum((p[i] for p in P), QD(0, 0, D)) for i in range(3)))
    H, seen = [], set()
    for eq in h.equations:
        idx = tuple(i for i in range(len(P)) if abs(Pf[i] @ eq[:3] + eq[3]) < 1e-7)
        if idx in seen: continue
        seen.add(idx)
        for i, j, k in itertools.combinations(idx, 3):
            n = cross(sub(P[j], P[i]), sub(P[k], P[i]))
            if not all(x.z() for x in n): break
        b = dot(n, P[i])
        if (b - dot(n, cen)).sign() < 0: n = mul(QD(-1, 0, D), n); b = -b
        H.append((n, b))
    return Poly(name, H, D)
def zonotope(name, gens, D):
    pts = []
    for sg in itertools.product([1, -1], repeat=len(gens)):
        p = vec(D, 0, 0, 0)
        for s_, g in zip(sg, gens): p = add(p, mul(QD(s_, 0, D), vec(D, *g)))
        pts.append(p)
    return from_vertices(name, pts, D)
def census_shapes():
    phi = QD(Fr(1, 2), Fr(1, 2), 5)
    C = {}
    C['octahedron (cs, not zonotope, no tiling)'] = Poly('oct', [(n, 1) for n in signs((1, 1, 1))], 0)
    C['cuboctahedron (cs, not zonotope, no tiling)'] = Poly('cubo', [(n, 1) for n in all_sp((1, 0, 0))] + [(n, 2) for n in signs((1, 1, 1))], 0)
    C['tetrahedron (no tiling)'] = Poly('tet', [((1, 1, 1), 1), ((1, -1, -1), 1), ((-1, 1, -1), 1), ((-1, -1, 1), 1)], 0)
    C['triangular prism (tiles, not cs)'] = Poly('tprism', [((0, 0, 1), 1), ((0, 0, -1), 1), ((0, -1, 0), 1), ((2, 1, 0), 2), ((-2, 1, 0), 2)], 0)
    C['generic parallelepiped (zonotope, tiles)'] = zonotope('ppd', [(3, 1, 0), (1, 4, 1), (-1, 2, 5)], 0)
    C['generic 4-generator zonotope (tiling not claimed)'] = zonotope('z4', [(3, 1, 0), (1, 4, 1), (-1, 2, 5), (4, 5, 1)], 0)
    C['generic 5-generator zonotope (tiling not claimed)'] = zonotope('z5', [(3, 1, 0), (1, 4, 1), (-1, 2, 5), (2, -3, 1), (1, 1, 7)], 0)
    C['rhombic triacontahedron (zonotope, no tiling)'] = zonotope('rtc', [(0, 1, phi), (1, phi, 0), (phi, 0, 1), (0, 1, -phi), (1, -phi, 0), (-phi, 0, 1)], 5)
    C['rhombic icosahedron (zonotope, no tiling)'] = zonotope('ric', [(0, 1, phi), (1, phi, 0), (phi, 0, 1), (0, 1, -phi), (1, -phi, 0)], 5)
    C['corner-cut cube (cs, not zonotope)'] = Poly('tc', [(n, 1) for n in all_sp((1, 0, 0))] + [(n, Fr(5, 2)) for n in signs((1, 1, 1))], 0)
    return C
def far_order(P):
    u = vec(P.D, 3, -5, 7); u2 = vec(P.D, 13, 5, -29); kk = 0
    while ak_exact(P, u, kk).z() and ak_exact(P, u2, kk).z() and kk < 9: kk += 1
    return kk

LAWGIVING = ['RD', 'TRD', 'cube', 'TO', 'HP']; CONTROLS = ['icosahedron', 'dodecahedron', 'RD-perturbed']
OWN = {'RD': 'fcc', 'TRD': 'hcp', 'cube': 'sc', 'TO': 'bcc', 'HP': 'sh'}

# ---------------------------------------------------------------- lattices (sympy exact, Euclidean, common frame)
R_ = sp.Rational; s6 = sp.sqrt(6)
def M3(*rows): return [sp.Matrix(r) for r in rows]
LATT = {
    'fcc': (M3((1, 1, 0), (1, 0, 1), (0, 1, 1)), [sp.Matrix([0, 0, 0])]),
    'hcp': (M3((1, -1, 0), (0, 1, -1), (R_(4, 3), R_(4, 3), R_(4, 3))), [sp.Matrix([0, 0, 0]), sp.Matrix([1, 0, 1])]),
    'dhcp': (M3((1, -1, 0), (0, 1, -1), (R_(8, 3), R_(8, 3), R_(8, 3))),
             [sp.Matrix([0, 0, 0]), sp.Matrix([1, 0, 1]), sp.Matrix([R_(4, 3)] * 3), sp.Matrix([R_(8, 3), R_(2, 3), R_(8, 3)])]),
    'bcc': (M3((1, 0, 0), (0, 1, 0), (R_(1, 2), R_(1, 2), R_(1, 2))), [sp.Matrix([0, 0, 0])]),
    'sc': (M3((1, 0, 0), (0, 1, 0), (0, 0, 1)), [sp.Matrix([0, 0, 0])]),
    'sh': (M3((1, -1, 0), (0, 1, -1), (s6 / 3, s6 / 3, s6 / 3)), [sp.Matrix([0, 0, 0])]),
}
LNAMES = ['fcc', 'hcp', 'dhcp', 'bcc', 'sc', 'sh']
def covol(L):
    B, S = LATT[L]; return sp.nsimplify(sp.Abs(sp.Matrix.hstack(*B).det()) / len(S))

XS = sp.Symbol('X')
KB = [sp.Integer(1), sp.sqrt(2), sp.sqrt(3), sp.sqrt(6), sp.sqrt(5), sp.sqrt(10), sp.sqrt(15), sp.sqrt(30)]
mp.mp.dps = 80
KBf = [mp.mpf(1), mp.sqrt(2), mp.sqrt(3), mp.sqrt(6), mp.sqrt(5), mp.sqrt(10), mp.sqrt(15), mp.sqrt(30)]
CK = {}
def is_zero_exact(e):
    if e == 0: return True
    return sp.minimal_polynomial(e, XS) == XS
def coords_K(e):
    """rational coordinates of e in basis KB, verified exactly; None if e is not in K = Q(sqrt2, sqrt3, sqrt5)"""
    kk = sp.srepr(e)
    if kk not in CK: CK[kk] = _coords_K(e)
    return CK[kk]
def _coords_K(e):
    if e.is_Rational: return [e] + [sp.Integer(0)] * 7, 1
    deg = sp.degree(sp.minimal_polynomial(e, XS), XS)
    if 8 % deg != 0: return None, deg
    v = mp.mpf(str(sp.N(e, 90)))
    rel = mp.pslq([v] + KBf, maxcoeff=10 ** 12, maxsteps=10 ** 6)
    if rel is None or rel[0] == 0: raise RuntimeError(f'PSLQ failed on {e}')
    co = [sp.Rational(-r, rel[0]) for r in rel[1:]]
    if not is_zero_exact(e - sum(c * k for c, k in zip(co, KB))): raise RuntimeError(f'PSLQ coords not exact for {e}')
    return co, deg
def zmember(cols, t):
    """is the integer vector t in the Z-span of the integer column vectors cols (exact)"""
    rem = [c[:] for c in cols]; t = t[:]
    for i in range(len(t)):
        nz = [c for c in rem if c[i] != 0]; zr = [c for c in rem if c[i] == 0]
        while len(nz) > 1:
            nz.sort(key=lambda c: abs(c[i])); p = nz[0]; new = [p]
            for c in nz[1:]:
                q = c[i] // p[i]; c2 = [a - q * b for a, b in zip(c, p)]
                (new if c2[i] != 0 else zr).append(c2)
            nz = new
        if nz:
            p = nz[0]
            if t[i] % p[i] != 0: return False
            q = t[i] // p[i]; t = [a - q * b for a, b in zip(t, p)]
        elif t[i] != 0: return False
        rem = zr
    return all(x == 0 for x in t)

def incidence(P, L):
    """exact: does lambda*L (covolume = vol P) have a point on a facet plane of P? returns dict"""
    B, S = LATT[L]; lam3 = sp.nsimplify(P.vol.sym() / covol(L)); lam = lam3 ** R_(1, 3)
    res = {'lambda3': str(lam3), 'planes_hit': 0, 'decided': True, 'reason': ''}
    cache = {}
    for (n, b, _) in P.F:
        ns = sp.Matrix([x.sym() for x in n]); bs = b.sym()
        c = bs / lam
        cc, deg = coords_K(c)
        if cc is None:
            res['reason'] = f'b/lambda has degree {deg} (not in Q(sqrt2,sqrt3,sqrt5))'; continue
        beta = [coords_K(sp.expand((ns.T * e)[0]))[0] for e in B]
        hit = False
        for s in S:
            g = coords_K(sp.expand(c - (ns.T * s)[0]))[0]
            den = sp.ilcm(*[x.q for x in sum(beta, []) + g])
            cols = [[int(x * den) for x in bb] for bb in beta]; t = [int(x * den) for x in g]
            if zmember(cols, t): hit = True
        res['planes_hit'] += hit
    res['incident'] = res['planes_hit'] > 0
    return res

# ---------------------------------------------------------------- float lattice sums (worker)
U53 = 2.0 ** -53
def lattice_points(L, lam, Rmax, rot=None):
    B, S = LATT[L]
    Bf = np.array([[float(x) for x in b] for b in B]).T * lam   # columns
    Sf = [np.array([float(x) for x in s]) * lam for s in S]
    Binv = np.linalg.inv(Bf); K = np.ceil(np.linalg.norm(Binv, axis=1) * (Rmax + 3 * lam)).astype(int) + 1
    g = np.stack(np.meshgrid(*[np.arange(-k, k + 1) for k in K], indexing='ij'), -1).reshape(-1, 3)
    pts = np.concatenate([g @ Bf.T + s for s in Sf])
    r = np.linalg.norm(pts, axis=1); keep = (r <= Rmax) & (r > 1e-9 * lam)
    pts = pts[keep]
    if rot is not None: pts = pts @ rot.T
    r = np.linalg.norm(pts, axis=1); o = np.argsort(r)
    return pts[o], r[o]
def omega_pts(Pd, X):
  with np.errstate(all='ignore'):
    return _omega_pts(Pd, X)
def _omega_pts(Pd, X):
    Nf, bf, ia, ib, ic, df = Pd
    out = np.empty(len(X)); err = np.empty(len(X)); onp = np.zeros(len(X), bool); fmin = np.empty(len(X))
    n1 = np.abs(Nf).sum(1)
    for i in range(0, len(X), 20000):
        x = X[i:i + 20000]; f = bf[None, :] - x @ Nf.T
        af = np.abs(f); fmin[i:i + 20000] = af.min(1)
        on = (af < 1e-9 * (1 + np.abs(bf)[None, :])).any(1); onp[i:i + 20000] = on
        f = np.where(af < 1e-300, 1e-300, f)
        t = df[None, :] / (f[:, ia] * f[:, ib] * f[:, ic])
        eps = 8 * U53 * (np.abs(bf)[None, :] + n1[None, :] * np.abs(x).max(1)[:, None]) / np.abs(f)
        te = np.abs(t) * (eps[:, ia] + eps[:, ib] + eps[:, ic] + (len(df) + 8) * U53)
        out[i:i + 20000] = t.sum(1); err[i:i + 20000] = te.sum(1)
    return out, err, onp, fmin
def rand_rot(rng):
    q = rng.normal(size=4); q /= np.linalg.norm(q); a, b, c, d = q
    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)], [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
                     [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]])
def sum_job(args):
    pname, Pd, vol, L, Rs, rots = args
    t0 = time.time(); rho = vol ** (1 / 3); lam = (vol / float(covol(L))) ** (1 / 3)
    out = {'P': pname, 'L': L}
    X, r = lattice_points(L, lam, Rs[-1] * rho)
    om, er, on, fmin = omega_pts(Pd, X)
    out['n_points'] = int(len(X)); out['on_plane_within_R'] = int(on.sum())
    out['min_abs_f_offplane'] = float(fmin[~on].min()) if (~on).any() else None
    full, dele = [], []
    for R in Rs:
        m = r <= R * rho
        dele.append((float(om[m & ~on].sum()), float(er[m & ~on].sum() + m.sum() * U53 * np.abs(om[m & ~on]).sum())))
        full.append(None if (m & on).any() else dele[-1][0])
    out['R'] = Rs; out['E_full'] = full; out['E_deleted'] = dele
    out['rand'] = []
    rng = np.random.default_rng(sum(ord(ch) * 31 ** i for i, ch in enumerate(pname + L)) % 2 ** 32)
    for k in range(rots):
        Xr, rr = lattice_points(L, lam, 20 * rho, rand_rot(rng))
        o2, e2, on2, f2 = omega_pts(Pd, Xr)
        out['rand'].append((float(o2[~on2].sum()), int(on2.sum()), float(f2.min())))
    out['secs'] = time.time() - t0
    return out
def extrapolate(Rs, E):
    R = np.array(Rs, float); E = np.array(E, float)
    m3 = R >= 12; A = np.stack([np.ones(m3.sum()), 1 / R[m3], 1 / R[m3] ** 2], 1); c3 = np.linalg.lstsq(A, E[m3], rcond=None)[0]
    m2 = R >= 20; A2 = np.stack([np.ones(m2.sum()), 1 / R[m2]], 1); c2 = np.linalg.lstsq(A2, E[m2], rcond=None)[0]
    return float(c3[0]), float(abs(c3[0] - c2[0])), float(c3[1])

# ================================================================= MAIN
if __name__ == '__main__':
    print(f'amp_dist.py {"PILOT" if PILOT else "FULL"}', flush=True)
    S = build_shapes()
    for k, P in S.items():
        fc = {}
        for n, b, on in P.F: fc[len(on)] = fc.get(len(on), 0) + 1
        print(f'  {k}: {len(P.V)} corners, {len(P.F)} facets {fc}, {len(P.terms)} Warren terms, vol = {P.vol}', flush=True)
    OUT['shapes'] = {k: {'corners': len(P.V), 'facets': len(P.F), 'terms': len(P.terms), 'vol': str(P.vol)} for k, P in S.items()}
    check('volumes: RD 2, TRD 2, cube 1, TO 1/2, HP sqrt6 (= covolumes of fcc, hcp, sc, bcc, sh)',
          [S[k].vol.sym() for k in LAWGIVING] == [2, 2, 1, sp.Rational(1, 2), sp.sqrt(6)]
          and all(sp.simplify(S[k].vol.sym() - covol(OWN[k])) == 0 for k in LAWGIVING))
    check('face counts: RD 12 rhombi, TRD 12, cube 6, TO 14, HP 8, icosahedron 20, dodecahedron 12, perturbed RD 12',
          [len(S[k].F) for k in S] == [12, 12, 6, 14, 8, 20, 12, 12])
    check('central symmetry: RD, cube, TO, HP yes; TRD no (it tiles hcp in two orientations); perturbed RD no (so no translation tiling, Minkowski)',
          not S['RD-perturbed'].centrally_symmetric() and not S['TRD'].centrally_symmetric() and all(S[k].centrally_symmetric() for k in ['RD', 'cube', 'TO', 'HP']))
    prog(0.03, 'shapes built')

    # ---------------- T0 method checks
    rng = random.Random(11); KSTAR = {}
    def rpt(P, box, inside):
        while True:
            Y = vec(P.D, *[Fr(rng.randint(-1000, 1000), 1000) * box for _ in range(3)])
            f = P.fvals(Y)
            if inside and all(x.sign() > 0 for x in f): return Y
            if not inside and any(x.sign() < 0 for x in f) and all(not x.z() for x in f): return Y
    for k, P in S.items():
        ins = [rpt(P, Fr(1, 2), True) for _ in range(2)]; outs = [rpt(P, 3, False) for _ in range(2)]
        check(f'T0 {k}: vertex formula = 3! vol(polar) at 2 interior points (exact)', all((P.omega(Y) - P.polar6(Y)).z() for Y in ins))
        check(f'T0 {k}: vertex formula = triangulation formula at 2 exterior points (exact)', all((P.omega(Y) - P.omega_tri(Y)).z() for Y in outs))
        u = vec(P.D, 3, -5, 7)
        check(f'T0 {k}: complete-fan identity sum d/(w w w) = 0 (the r^-3 terms cancel)', fan_identity(P, u).z())
        u2 = vec(P.D, 13, 5, -29); kk = 0
        while ak_exact(P, u, kk).z() and ak_exact(P, u2, kk).z() and kk < 9: kk += 1
        KSTAR[k] = kk
        uf = fl(u) / np.linalg.norm(fl(u)); Pd = (P.Nf, P.bf, P.ia, P.ib, P.ic, P.df)
        v1, v2 = [omega_pts(Pd, (r * uf)[None, :])[0][0] * r ** (3 + kk) for r in (1e3, 2e3)]
        val = 2 * v2 - v1; akv = ak_float(P, uf[None, :], kk)[0]   # Richardson: removes the 1/r correction
        print(f'      {k}: far field Omega ~ a_{kk}(u) r^-{3 + kk} (a_0 .. a_{kk - 1} vanish exactly at two generic directions)', flush=True)
        check(f'T0 {k}: r^{3 + kk} Omega(r u) -> a_{kk}(u) (Richardson from r = 1000, 2000: {val:.6g} vs {akv:.6g})', abs(val - akv) <= 1e-3 * abs(akv))
        # simple pole on a facet plane at a generic point
        n, b, on = P.F[0]; p = P.V[on[0]]; t1, t2 = tangent_pair(P, n, 5)
        x0 = add(p, add(mul(Fr(37, 10), t1), mul(Fr(-23, 10), t2)))
        Sx = omega_series(P, x0, add(n, mul(Fr(1, 7), t1)))
        check(f'T0 {k}: Laurent order -1 at a generic point of a facet plane (simple pole)', min(Sx) == -1)
    check('T0 known values: Omega_cube(0) = 64, Omega_RD(0) = 40', S['cube'].omega(vec(0, 0, 0, 0)).sym() == 64 and S['RD'].omega(vec(0, 0, 0, 0)).sym() == 40)
    Y = rpt(S['TO'], Fr(1, 4), True)
    check('T0 NEGATIVE: dropping one Warren term breaks the polar identity (TO)', not (S['TO'].omega(Y, drop=3) - S['TO'].polar6(Y)).z())
    CEN = {}
    for name, P in census_shapes().items():
        fc = {}
        for n, b, on in P.F: fc[len(on)] = fc.get(len(on), 0) + 1
        kk = far_order(P); CEN[name] = {'decay_power': 3 + kk, 'facets': fc, 'centrally_symmetric': P.centrally_symmetric()}
        print(f'DECAY census: {name}: Omega ~ r^-{3 + kk} (faces {fc}, centrally symmetric {P.centrally_symmetric()})', flush=True)
    for k in S: CEN[k] = {'decay_power': 3 + KSTAR[k]}
    OUT['decay_census'] = CEN
    prog(0.10, 'T0 done')

    # ---------------- probe directions / neighbour points
    def nb_points(P):
        """the point across each facet at twice the facet distance (= own lattice neighbour for a Voronoi cell); grouped by value"""
        return [mul(2 * b / dot(n, n), n) for n, b, _ in P.F]
    AX = {'cubic': {'4-fold (1,0,0)': (1, 0, 0), '3-fold (1,1,1)': (1, 1, 1), '2-fold (1,1,0)': (1, 1, 0)},
          'hex': {'c-axis (1,1,1)': (1, 1, 1), 'in-plane a (1,-1,0)': (1, -1, 0), 'in-plane (1,1,-2)': (1, 1, -2)},
          'ico': {'2-fold (1,0,0)': (1, 0, 0), '3-fold (1,1,1)': (1, 1, 1), '5-fold (0,1,phi)': (0, 1, QD(Fr(1, 2), Fr(1, 2), 5))}}
    FAM = {'RD': 'cubic', 'cube': 'cubic', 'TO': 'cubic', 'RD-perturbed': 'cubic', 'TRD': 'hex', 'HP': 'hex', 'icosahedron': 'ico', 'dodecahedron': 'ico'}
    T2 = {}; T3 = {}
    for idx, (k, P) in enumerate(S.items()):
        T2[k] = {'neighbours_far': [], 'neighbours_sphere': [], 'axes_far': {}}; T3[k] = []
        seen = set()
        for fi, x0 in enumerate(nb_points(P)):
            n, b, _ = P.F[fi]
            # orbit dedup by (|x0|^2, b/|n|, value of Omega at a test point) is unsafe; we classify every facet (cheap) and dedupe results
            d1, d2 = tangent_pair(P, x0, 100 + fi)
            far = far_classify(P, x0, KSTAR[k], 100 + fi)
            r2 = dot(x0, x0)
            gS = omega_series(P, x0, x0)
            def curv(dl, gS=gS, r2=r2):
                g = gS.get(1, QD(0, 0, P.D)) if not any(kk < 0 for kk in gS) else QD(0, 0, P.D)
                return dot(dl, dl) / (2 * r2) * g
            sph = classify(lambda x, dl: omega_series(P, x, dl), x0, d1, d2, curv=curv)
            line = omega_series(P, x0, n)
            if any(kk < 0 for kk in line): lk = {'kind': 'pole', 'order': min(line)}
            elif 0 not in line: lk = {'kind': 'zero'}
            elif 1 not in line: lk = {'kind': 'critical', 'value': line[0].f()}
            else: lk = {'kind': 'regular', 'value': line[0].f(), 'slope_sign': line[1].sign()}
            # which facet planes pass through x0 (exact)
            through = sum(1 for nn, bb, _ in P.F if (bb - dot(nn, x0)).z())
            rec = {'facet': fi, 'normal': [str(x) for x in n], 'point': [str(x) for x in x0], 'planes_through_point': through}
            T2[k]['neighbours_far'].append({**rec, **far}); T2[k]['neighbours_sphere'].append({**rec, **sph})
            T3[k].append({**rec, **lk})
        for an, a in AX[FAM[k]].items():
            u = vec(P.D, *a)
            T2[k]['axes_far'][an] = far_classify(P, u, KSTAR[k], 7)
        def summ(lst):
            out = {}
            for e in lst:
                key = e['kind'] + ('/' + e['type'] if e.get('type') else '') + (f"/order{e['order']}" if e['kind'] == 'pole' else '')
                out[key] = out.get(key, 0) + 1
            return out
        print(f'T2/T3 {k}: far-field at neighbour dirs {summ(T2[k]["neighbours_far"])}; sphere {summ(T2[k]["neighbours_sphere"])}; '
              f'line at 2h {summ(T3[k])}; planes through the 2h points {sorted({e["planes_through_point"] for e in T3[k]})}', flush=True)
        print(f'      axes (far field): ' + '; '.join(f'{an}: {v["kind"]}{"/" + v["type"] if v.get("type") else ""}' for an, v in T2[k]['axes_far'].items()), flush=True)
        prog(0.10 + 0.25 * (idx + 1) / len(S), f'T2/T3 {k}')
    # T3 exploratory: along each facet normal, float scan s0 < s <= 6 s0
    T3x = {}
    for k, P in S.items():
        rows = []
        for fi, (n, b, _) in enumerate(P.F):
            nf = fl(n); s0 = b.f() / (nf @ nf)
            s = np.linspace(s0 * 1.0005, 6 * s0, 60001); X = s[:, None] * nf[None, :]
            v = omega_pts((P.Nf, P.bf, P.ia, P.ib, P.ic, P.df), X)[0]
            poles = sorted({round((bb.f() / (fl(nn) @ nf)) / s0, 9) for nn, bb, _ in P.F if fl(nn) @ nf > 1e-12 and s0 < bb.f() / (fl(nn) @ nf) <= 6 * s0 + 1e-12})
            fin = np.isfinite(v) & (np.abs(v) < 1e6)
            zs = [float(s[i] / s0) for i in range(len(s) - 1) if fin[i] and fin[i + 1] and v[i] * v[i + 1] < 0 and abs(v[i]) + abs(v[i + 1]) < 1e3]
            dv = np.diff(v); cs = [float(s[i + 1] / s0) for i in range(len(dv) - 1) if fin[i] and fin[i + 2] and dv[i] * dv[i + 1] < 0 and abs(dv[i]) < 1e2]
            rows.append({'facet': fi, 'poles_s_over_s0': poles, 'zeros_s_over_s0': [round(z, 4) for z in zs], 'crit_s_over_s0': [round(c, 4) for c in cs]})
        T3x[k] = rows
        uniq = {json.dumps({kk: vv for kk, vv in r.items() if kk != 'facet'}) for r in rows}
        print(f'T3x {k}: {len(uniq)} distinct line profiles: ' + ' | '.join(sorted(uniq))[:900], flush=True)
    OUT['far_field_order'] = {k: 3 + v for k, v in KSTAR.items()}; OUT['T2'] = T2; OUT['T3'] = T3; OUT['T3_explore'] = T3x
    prog(0.40, 'T2/T3 exact done')

    # ---------------- T1 exact incidence
    INC = {}
    for idx, (k, P) in enumerate(S.items()):
        INC[k] = {}
        for L in LNAMES:
            INC[k][L] = incidence(P, L)
        print(f'T1 incidence {k}: ' + ', '.join(f'{L}: {"HIT " + str(v["planes_hit"]) + " planes" if v["incident"] else "none"}' for L, v in INC[k].items()), flush=True)
        prog(0.40 + 0.15 * (idx + 1) / len(S), f'incidence {k}')
    OUT['T1_incidence'] = INC

    # ---------------- T1 float lattice sums (2 workers)
    Rs = [6, 8, 10, 12] if PILOT else [8, 10, 12, 14, 16, 20, 24, 28, 32, 36, 40]
    rots = 2 if PILOT else 16
    jobs = [(k, (P.Nf, P.bf, P.ia, P.ib, P.ic, P.df), P.vol.f(), L, Rs, rots) for k, P in S.items() for L in LNAMES]
    jobs.sort(key=lambda j: -len(S[j[0]].terms))
    res = []
    with get_context('fork').Pool(2) as pool:
        for i, r in enumerate(pool.imap_unordered(sum_job, jobs)):
            res.append(r)
            if (i + 1) % 6 == 0: prog(0.55 + 0.40 * (i + 1) / len(jobs), f'lattice sums {i + 1}/{len(jobs)} (last {r["P"]}/{r["L"]} {r["secs"]:.0f} s)')
    SUMS = {}
    for r in res:
        k, L = r['P'], r['L']; SUMS.setdefault(k, {})[L] = r
        exact_hit = INC[k][L]['incident']
        check(f'T1 {k}/{L}: float on-plane points ({r["on_plane_within_R"]}) agree with the exact incidence ({exact_hit})',
              (r['on_plane_within_R'] > 0) == exact_hit)
        if not PILOT:
            Ed = [e for e, _ in r['E_deleted']]; einf, eerr, a = extrapolate(Rs, Ed)
            r['E_deleted_inf'] = einf; r['E_deleted_err'] = eerr + r['E_deleted'][-1][1]; r['tail_a'] = a
        else:
            r['E_deleted_inf'] = r['E_deleted'][-1][0]; r['E_deleted_err'] = float('nan'); r['tail_a'] = float('nan')
    OUT['T1_sums'] = SUMS
    print('T1 lattice sums (pole-deleted E\'; "inf" = own points on facet planes, E undefined):', flush=True)
    verdict = {}
    for k in S:
        row = []
        for L in LNAMES:
            r = SUMS[k][L]
            tag = 'POLE ' if INC[k][L]['incident'] else ''
            rv = [x[0] for x in r['rand']]
            row.append(f'{L}: {tag}{r["E_deleted_inf"]:.5g} +- {r["E_deleted_err"]:.2g} [rand {min(rv):.3g}..{max(rv):.3g}]')
        print(f'  {k}: ' + '; '.join(row), flush=True)
        if k in LAWGIVING:
            own = OWN[k]; vals = {L: SUMS[k][L]['E_deleted_inf'] for L in LNAMES}
            fin = {L: v for L, v in vals.items() if not INC[k][L]['incident']}
            verdict[k] = {'own': own, 'own_E_defined': not INC[k][own]['incident'],
                          'own_is_min_deleted': min(vals, key=vals.get) == own, 'own_is_max_deleted': max(vals, key=vals.get) == own,
                          'own_is_min_finite': (own in fin and min(fin, key=fin.get) == own), 'own_is_max_finite': (own in fin and max(fin, key=fin.get) == own),
                          'incident_lattices': [L for L in LNAMES if INC[k][L]['incident']],
                          'argmin_deleted': min(vals, key=vals.get), 'argmax_deleted': max(vals, key=vals.get)}
        else:
            vals = {L: SUMS[k][L]['E_deleted_inf'] for L in LNAMES}
            verdict[k] = {'argmin_deleted': min(vals, key=vals.get), 'argmax_deleted': max(vals, key=vals.get),
                          'incident_lattices': [L for L in LNAMES if INC[k][L]['incident']]}
        print(f'  {k} verdict data: {verdict[k]}', flush=True)
    OUT['T1_verdict_data'] = verdict
    C1 = all(verdict[k]['own_E_defined'] for k in LAWGIVING) and (all(verdict[k]['own_is_min_finite'] for k in LAWGIVING) or all(verdict[k]['own_is_max_finite'] for k in LAWGIVING))
    C1d = all(verdict[k]['own_is_min_deleted'] for k in LAWGIVING) or all(verdict[k]['own_is_max_deleted'] for k in LAWGIVING)
    C2 = all(verdict[k]['incident_lattices'] == [OWN[k]] for k in LAWGIVING)
    print(f'T1 RESULT: C1 {"PASS" if C1 else "FAIL"}; C1\' (pole-deleted) {"PASS" if C1d else "FAIL"}; C2 (own lattice the unique one on the poles) {"PASS" if C2 else "FAIL"}', flush=True)
    OUT['T1_result'] = {'C1': C1, 'C1_deleted': C1d, 'C2': C2}
    OUT['checks'] = NCHK; OUT['secs'] = time.time() - T0
    json.dump(OUT, open(os.path.join(DATA, 'amp-pilot.json' if PILOT else 'amp.json'), 'w'), indent=1, default=str)
    prog(0.99, 'written')
    print(f'{NCHK} checks, {time.time() - T0:.0f} s', flush=True)
    print('FINAL ok' if OK else 'FINAL FAIL', flush=True)
