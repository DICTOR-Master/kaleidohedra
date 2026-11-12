"""Aim 2, chunk 5 (12 Nov 2026): DICTO's solids as positive geometries (canonical forms).
Solids, all exact (Q or Q(sqrt5)):
  Cleo-Icos = conv(centre, one icosahedron face), icosahedron (0, +-1, +-phi) cyclic; Antonius = the golden prolate rhombohedron
  spanned by one face's corners a, b, c minus its two Cleo-Icos corners (#44); the rhombohedron itself; the icosahedron as 20 Cleo-Icos;
  Narcissus (HexOct h-piece, #? HexOct: Narcissus and Covenant) in the rational affine frame (x, sqrt3 y, sqrt(3/2) z) of study
  2026-11-04-dehn-screen (mahler_exact.py); Covenant = Narcissus + Narcissus turned over on the hexagon and turned 60 deg; the straight
  pair (turned over only); the Ogdoecontahedron OG = pentakis dodecahedron with its 20 six-fold corners cut flat through the midpoints
  of the six-fold-to-six-fold edges (built here from the truncated icosahedron); the Hecatodihedron = polar of OG.
Canonical form Omega(P; Y) of a convex 3-polytope {b_i - n_i.Y >= 0}: Warren's vertex formula (chunks 3-4), fan over the dual polygon
at a vertex on more than three facets. Independent second formula: a triangulation (cone from one vertex over fan-triangulated facets)
of positively oriented simplex forms <Z0Z1Z2Z3>^3 / prod <Y ..> (chunk 2).
CHECKS (positive controls with known answers first):
 (C1) cube [0,1]^3: Omega = prod 1/(x(1-x)); Omega(centre) * vol = 6 * 32/3 = 64; unit simplex: Omega * vol at centroid = 6 * 64/9.
 (C2) Narcissus: volume 3/4 in the rational frame (= sqrt2/4 x 3/sqrt2) and Mahler product about the corner centroid = 34/3 (published
      11-04, mahler_exact.py) <=> Omega(N; centroid) * vol(N) = 68.
 (C3) OG: 102 corners, 80 faces (20 regular hexagons, 60 kites); squared radii and squared edge lengths equal the published
      4/9, (170+2sqrt5)/361; 2/9 - 2sqrt5/27 (120 edges), 86/3249 + 2sqrt5/361 (60 edges) after one scale; Hecatodihedron 80 corners, 102 faces.
 (P1) Warren = triangulation formula at generic points, every solid.
 (P2) BRIDGE: Omega(P; Y) = 3! vol(polar of P about Y), exact, at interior generic points, every solid.
 (P3) POSITIVE GEOMETRY BY RESIDUES: on every facet F, Res_F Omega(P) = Omega(F) (canonical form of the facet polygon), exact at
      generic points of the facet plane (the defining recursive property).
 (P4) JOINS = POLE CANCELLATION: for DICTO's dissections (rhombohedron = Cleo + Antonius + Cleo; icosahedron = 20 Cleo-Icos;
      Covenant = two Narcissus) Omega(whole) = sum Omega(pieces), and on every inner joining plane the poles cancel (residue 0).
      Rhombohedron and Covenant: PROVED as rational-function identities (the cleared numerator has degree <= D in each variable and
      vanishes on a (D+1)^3 grid). Icosahedron: exact at sample points.
 (P5) affine images: Cleo-Icos, Antonius, rhombohedron are the images under Y -> [a b c] Y of the cube's corner simplex, middle
      octahedron piece and the cube (Omega transforms with 1/det).
 (N1) dropping one Warren term (OG) breaks P1.  (N2) a mis-joined pair (second Narcissus shifted 1/7 along the hexagon) leaves a pole
      on the join plane.  (N3) Antonius with only one fan triangle per four-facet corner (treated as simple) breaks P2.
RESULTS: Mahler product = Omega(P; s) vol(P) / 6 at the Santalo point s (Omega's minimum inside P), exactly; adjoint degree on a line.
Usage: python -u solids_canon.py [pilot]"""
import sys, itertools, random, time
from fractions import Fraction as Fr
from multiprocessing import get_context
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
import sympy as sp

PILOT = sys.argv[1:] == ['pilot']
T0 = time.time()
OK = True
def check(name, cond):
    global OK
    OK &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)

class Q5:
    """a + b sqrt5, a, b rational (exact)"""
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    @staticmethod
    def c(x): return x if isinstance(x, Q5) else Q5(x)
    def __add__(s, o): o = Q5.c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = Q5.c(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q5.c(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = Q5.c(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = Q5.c(o); n = o.a * o.a - 5 * o.b * o.b
        if n == 0: raise ZeroDivisionError
        return s * Q5(o.a / n, -o.b / n)
    def __rtruediv__(s, o): return Q5.c(o) / s
    def __pow__(s, k):
        r = Q5(1)
        for _ in range(k): r = r * s
        return r
    def sign(s):
        sa = (s.a > 0) - (s.a < 0); sb = (s.b > 0) - (s.b < 0)
        if sb == 0: return sa
        if sa == 0 or sa == sb: return sb if sa == 0 else sa
        return sa if s.a * s.a > 5 * s.b * s.b else sb
    def z(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): o = Q5.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __abs__(s): return -s if s.sign() < 0 else s
    def f(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f'{s.b}*sqrt5'
        return f'({s.a} {"+" if s.b > 0 else "-"} {abs(s.b)}*sqrt5)'

S5 = Q5(0, 1); PHI = Q5(Fr(1, 2), Fr(1, 2)); ZERO = Q5(0); ONE = Q5(1)
def V3(*x): return tuple(Q5.c(Fr(t)) if not isinstance(t, Q5) else t for t in x)
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def mul(k, u): return tuple(k * a for a in u)
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def det3(u, v, w): return dot(u, cross(v, w))
def fl(u): return np.array([x.f() for x in u])
def key(u): return tuple((x.a, x.b) for x in u)
def det4(M):
    """exact 4x4 determinant by cofactors on the first column of ones? general Laplace"""
    def d3(r): return (r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1]) - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
                       + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0]))
    tot = ZERO
    for j in range(4):
        minor = [[M[i][k] for k in range(4) if k != j] for i in range(1, 4)]
        t = M[0][j] * d3(minor)
        tot = tot + t if j % 2 == 0 else tot - t
    return tot

class Poly:
    """exact convex 3-polytope from a point set (keeps only true corners); facets (n, b, corner list in cyclic order), b - n.Y >= 0"""
    def __init__(s, name, pts):
        s.name = name
        uniq = {}
        for p in pts: uniq[key(p)] = p
        P = list(uniq.values()); Pf = np.array([fl(p) for p in P])
        h = ConvexHull(Pf)
        cen = mul(Q5(Fr(1, len(P))), tuple(sum((p[i] for p in P), ZERO) for i in range(3)))
        planes, seen = [], set()
        for eq in h.equations:
            idx = tuple(i for i in range(len(P)) if abs(Pf[i] @ eq[:3] + eq[3]) < 1e-7)
            if idx in seen: continue
            seen.add(idx)
            for i, j, k in itertools.combinations(idx, 3):
                n = cross(sub(P[j], P[i]), sub(P[k], P[i]))
                if not all(x.z() for x in n): break
            b = dot(n, P[i])
            if (b - dot(n, cen)).sign() < 0: n = tuple(-x for x in n); b = -b
            m = abs(next(x for x in n if not x.z())); n = tuple(x / m for x in n); b = b / m
            on = [q for q in range(len(P)) if (b - dot(n, P[q])).z()]
            assert all((b - dot(n, P[q])).sign() >= 0 for q in range(len(P))), 'not convex / bad plane'
            assert tuple(on) == idx, (name, 'float/exact facet mismatch')
            planes.append((n, b, on))
        # true corners: tight normals of rank 3
        corner = [q for q in range(len(P)) if np.linalg.matrix_rank(np.array([fl(n) for n, b, on in planes if q in on]), 1e-9) == 3]
        ren = {q: i for i, q in enumerate(corner)}
        s.V = [P[q] for q in corner]; s.Vf = np.array([fl(v) for v in s.V])
        s.F = []
        for n, b, on in planes:
            vs = [ren[q] for q in on if q in ren]
            nf = fl(n); c = s.Vf[vs].mean(0); e1 = s.Vf[vs[0]] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(nf, e1); e2 /= np.linalg.norm(e2)
            vs = [vs[i] for i in np.argsort([np.arctan2((s.Vf[v] - c) @ e2, (s.Vf[v] - c) @ e1) for v in vs])]
            s.F.append((n, b, vs))
        s.cen = mul(Q5(Fr(1, len(s.V))), tuple(sum((v[i] for v in s.V), ZERO) for i in range(3)))
        s.tight = [[fi for fi, (n, b, vs) in enumerate(s.F) if v in vs] for v in range(len(s.V))]
        # Warren terms: (fi, fj, fk, |det|) per vertex, fan over the cyclically ordered tight normals
        s.terms = []
        for v, T in enumerate(s.tight):
            if len(T) == 3: tris = [tuple(T)]
            else:
                Nn = np.array([fl(s.F[k][0]) for k in T]); Nn /= np.linalg.norm(Nn, axis=1)[:, None]
                c = Nn.sum(0); c /= np.linalg.norm(c); e1 = Nn[0] - (Nn[0] @ c) * c; e1 /= np.linalg.norm(e1); e2 = np.cross(c, e1)
                o = [T[i] for i in np.argsort([np.arctan2(x @ e2, x @ e1) for x in Nn])]
                tris = [(o[0], o[i], o[i + 1]) for i in range(1, len(o) - 1)]
            for tr in tris:
                d = abs(det3(*[s.F[k][0] for k in tr])); assert not d.z()
                s.terms.append((v, tr, d))
        s.E = sum(len(vs) for _, _, vs in s.F) // 2
        assert len(s.V) - s.E + len(s.F) == 2, (name, 'Euler')
    def fvals(s, Y): return [b - dot(n, Y) for n, b, _ in s.F]
    def omega(s, Y, drop=None, simple_only=False):
        f = s.fvals(Y); tot = ZERO; seenv = set()
        for i, (v, (a, b, c), d) in enumerate(s.terms):
            if i == drop: continue
            if simple_only:
                if v in seenv: continue
                seenv.add(v)
            tot = tot + d / (f[a] * f[b] * f[c])
        return tot
    def omega_tri(s, Y):
        Zh = lambda p: (ONE, p[0], p[1], p[2]); Yh = Zh(Y); tot = ZERO
        for n, b, vs in s.F:
            if 0 in vs: continue
            for i in range(1, len(vs) - 1):
                Z = [Zh(s.V[0]), Zh(s.V[vs[0]]), Zh(s.V[vs[i]]), Zh(s.V[vs[i + 1]])]
                o = det4(Z)
                if o.sign() < 0: Z[0], Z[1] = Z[1], Z[0]; o = -o
                den = ONE
                for j in range(4): den = den * det4([Z[k] if k != j else Yh for k in range(4)])
                tot = tot + o ** 3 / den
        return tot
    def vol6(s):
        tot = ZERO
        for n, b, vs in s.F:
            for i in range(1, len(vs) - 1):
                tot = tot + abs(det3(sub(s.V[vs[0]], s.cen), sub(s.V[vs[i]], s.cen), sub(s.V[vs[i + 1]], s.cen)))
        return tot
    def polar_vol6(s, Y):
        f = s.fvals(Y); assert all(x.sign() > 0 for x in f)
        U = [mul(ONE / fi, n) for (n, b, _), fi in zip(s.F, f)]
        h = ConvexHull(np.array([fl(u) for u in U])); tot = ZERO
        for a, b, c in h.simplices: tot = tot + abs(det3(U[a], U[b], U[c]))
        return tot
    def inside(s, Y): return all(x.sign() > 0 for x in s.fvals(Y))
    def generic(s, Y): return all(not x.z() for x in s.fvals(Y))
    def counts(s):
        from collections import Counter
        return dict(sorted(Counter(len(vs) for _, _, vs in s.F).items())), dict(sorted(Counter(len(T) for T in s.tight).items()))

def rnd_point(rng, lo, hi):
    return tuple(Q5(Fr(rng.randint(0, 10 ** 6), 10 ** 6) * (h - l) + l) for l, h in zip(lo, hi))
def bbox(P): return [Fr(int(np.floor(P.Vf[:, i].min() * 4)) - 2, 4) for i in range(3)], [Fr(int(np.ceil(P.Vf[:, i].max() * 4)) + 2, 4) for i in range(3)]
def interior_points(P, k, seed):
    rng = random.Random(seed); out = []
    lo, hi = bbox(P)
    while len(out) < k:
        Y = rnd_point(rng, lo, hi)
        if P.inside(Y): out.append(Y)
    return out
def any_points(Ps, k, seed):
    rng = random.Random(seed); out = []; lo, hi = bbox(Ps[0])
    while len(out) < k:
        Y = rnd_point(rng, lo, hi)
        if all(P.generic(Y) for P in Ps): out.append(Y)
    return out

def residue_check(P, fi, npts=2, seed=0):
    """Res_F Omega(P) = Omega(F) at generic points of F's plane; returns (#ok, #pts)"""
    n, b, vs = P.F[fi]; p0 = P.V[vs[0]]; u = sub(P.V[vs[1]], p0); v = sub(P.V[vs[2]], p0)
    if all(x.z() for x in cross(u, v)): v = sub(P.V[vs[3]], p0)
    w = mul(-ONE / dot(n, n), n); J = abs(det3(u, v, w))
    # polygon edges -> the other facet through both ends; 2D lines g = c - m.(s,t)
    edges = []
    for i in range(len(vs)):
        p, q = vs[i], vs[(i + 1) % len(vs)]
        G = [g for g in range(len(P.F)) if g != fi and p in P.F[g][2] and q in P.F[g][2]]; assert len(G) == 1
        nG, bG, _ = P.F[G[0]]; edges.append((bG - dot(nG, p0), dot(nG, u), dot(nG, v)))
    rng = random.Random(seed * 1009 + fi); good = 0; tried = 0
    while tried < npts:
        s_, t_ = Q5(Fr(rng.randint(-300, 1300), 1000)), Q5(Fr(rng.randint(-300, 1300), 1000))
        Y = add(p0, add(mul(s_, u), mul(t_, v))); f = P.fvals(Y)
        if any(f[k].z() for k in range(len(f)) if k != fi): continue
        g = [c - m1 * s_ - m2 * t_ for c, m1, m2 in edges]
        if any(x.z() for x in g): continue
        tried += 1
        res = ZERO
        for _, tr, d in P.terms:
            if fi in tr:
                o = [k for k in tr if k != fi]; res = res + d / (f[o[0]] * f[o[1]])
        om2 = ZERO
        for i in range(len(edges)):
            (c1, a1, b1), (c2, a2, b2) = edges[i - 1], edges[i]
            om2 = om2 + abs(a1 * b2 - a2 * b1) / (g[i - 1] * g[i])
        good += (res * J == om2)
    return good, npts

def join_residue(pieces, plane_n, plane_b, Y):
    """lim g -> 0 of g * sum Omega(pieces) at Y on the plane g = plane_b - plane_n.Y = 0 (0 = the pole cancels)"""
    tot = ZERO
    for P in pieces:
        f = P.fvals(Y)
        for _, tr, d in P.terms:
            hit = [k for k in tr if all(x.z() for x in cross(P.F[k][0], plane_n)) and (P.F[k][1] * dot(plane_n, plane_n) == plane_b * dot(P.F[k][0], plane_n))]
            if not hit: continue
            k = hit[0]; lam = dot(P.F[k][0], plane_n) / dot(plane_n, plane_n)        # f_k = lam * g
            o = [j for j in tr if j != k]; tot = tot + d / (lam * f[o[0]] * f[o[1]])
    return tot

# ---------- identity certificate on a grid ----------
def plane_key(n, b):
    m = next(x for x in n if not x.z()); return key(tuple(x / m for x in n)) + ((b / m).a, (b / m).b)
def cert_setup(whole, pieces):
    keys = {}
    for P in [whole] + pieces:
        for n, b, _ in P.F:
            k = plane_key(n, b)
            if k not in keys:
                m = next(x for x in n if not x.z()); keys[k] = (tuple(x / m for x in n), b / m)
    K = list(keys); idx = {k: i for i, k in enumerate(K)}
    rows = []                                                   # (sign, coeff, set of key indices in the term)
    for sgn, P in [(1, whole)] + [(-1, Q) for Q in pieces]:
        for _, tr, d in P.terms:
            ks, lam = [], ONE
            for j in tr:
                n, b, _ = P.F[j]; k = plane_key(n, b); ks.append(idx[k]); m = next(x for x in n if not x.z()); lam = lam * m
            rows.append((sgn, d / lam, frozenset(ks)))
    return [keys[k] for k in K], rows
def cert_eval(args):
    planes, rows, pts = args; bad = 0
    for Y in pts:
        g = [b - dot(n, Y) for n, b in planes]; tot = ZERO
        for sgn, c, ks in rows:
            t = c
            for i, gi in enumerate(g):
                if i not in ks: t = t * gi
            tot = tot + t if sgn > 0 else tot - t
        bad += not tot.z()
    return bad, len(pts)

def mahler_line(P, A, B, var):
    """Omega(P; A + z B) * vol(P)/6 as an exact sympy rational function of z (P rational)"""
    z = var; R = lambda q: sp.Rational(q.a.numerator, q.a.denominator) if q.b == 0 else None
    tot = 0
    for _, tr, d in P.terms:
        den = 1
        for j in tr:
            n, b, _ = P.F[j]; den *= (R(b) - sum(R(n[i]) * (R(A[i]) + z * R(B[i])) for i in range(3)))
        tot += R(d) / den
    return sp.together(tot * R(P.vol6()) / 36)

def adjoint_degree(P, seed):
    """degree of A(t) = Omega * prod f on a generic line, by Newton divided differences on len(F)-2 nodes"""
    rng = random.Random(seed); lo, hi = bbox(P)
    Y0 = rnd_point(rng, lo, hi); W = rnd_point(rng, lo, hi)
    N = len(P.F) - 2; ts, vals = [], []
    t = 0
    while len(ts) < N:
        t += 1; Y = add(Y0, mul(Q5(Fr(t, 7)), W))
        if not P.generic(Y): continue
        f = P.fvals(Y); pr = ONE
        for x in f: pr = pr * x
        ts.append(Q5(Fr(t, 7))); vals.append(P.omega(Y) * pr)
    c = list(vals)
    for j in range(1, N):
        for i in range(N - 1, j - 1, -1): c[i] = (c[i] - c[i - 1]) / (ts[i] - ts[i - j])
    return max(i for i in range(N) if not c[i].z())

# ======================= build the solids =======================
def cyc(t):
    out = {}
    for sg in itertools.product(*[[1, -1] if not x.z() else [1] for x in t]):
        a = tuple(x * s for x, s in zip(t, sg))
        for r in range(3):
            v = a[r:] + a[:r]; out[key(v)] = v
    return list(out.values())

def build():
    S = {}
    S['cube'] = Poly('cube', [V3(*p) for p in itertools.product([0, 1], repeat=3)])
    S['simplex'] = Poly('simplex', [V3(0, 0, 0), V3(1, 0, 0), V3(0, 1, 0), V3(0, 0, 1)])
    e = [V3(1, 0, 0), V3(0, 1, 0), V3(0, 0, 1)]
    S['cube middle octahedron'] = Poly('cube middle octahedron', [e[0], e[1], e[2], add(e[0], e[1]), add(e[0], e[2]), add(e[1], e[2])])
    a, b, c = V3(0, 1, PHI), V3(0, -1, PHI), V3(PHI, 0, 1); s = add(add(a, b), c); O = V3(0, 0, 0)
    S['Cleo-Icos'] = Poly('Cleo-Icos', [O, a, b, c])
    S['Antonius'] = Poly('Antonius', [a, b, c, add(a, b), add(a, c), add(b, c)])
    S['Cleo-Icos (far corner)'] = Poly('Cleo-Icos (far corner)', [s, add(b, c), add(a, c), add(a, b)])
    S['golden prolate rhombohedron'] = Poly('golden prolate rhombohedron', [O, a, b, c, add(a, b), add(a, c), add(b, c), s])
    ico = cyc(V3(0, 1, PHI)); S['icosahedron'] = Poly('icosahedron', ico)
    S['_ico_cleos'] = [Poly(f'Cleo {i}', [O] + [S['icosahedron'].V[v] for v in vs]) for i, (n, bb, vs) in enumerate(S['icosahedron'].F)]
    # Narcissus, rational frame
    h = Fr(1, 2)
    N = [V3(0, 0, 0), V3(0, 1, 0), V3(h, -h, 0), V3(h, 3 * h, 0), V3(1, 0, 0), V3(1, 1, 0), V3(0, 1, -h), V3(h, -h, -h), V3(1, 1, -h), V3(h, h, -1)]
    S['Narcissus'] = Poly('Narcissus', N)
    M = lambda p: (p[0], p[1], -p[2])
    def R60(p):
        X, Y = p[0] - h, p[1] - h
        return (X * h - Y * h + h, X * 3 * h + Y * h + h, p[2])
    S['_N_turned_over'] = Poly('Narcissus turned over', [M(p) for p in N])
    S['_N_covenant_partner'] = Poly('Narcissus turned over and 60 deg', [R60(M(p)) for p in N])
    S['_N_shifted'] = Poly('Narcissus turned over, shifted 1/7', [add(M(p), V3(Fr(1, 7), 0, 0)) for p in N])
    S['Covenant'] = Poly('Covenant', N + [R60(M(p)) for p in N])
    S['straight pair'] = Poly('twisted cube (straight pair)', N + [M(p) for p in N])
    # OG from the truncated icosahedron
    two, three = Q5(2), Q5(3)
    TI = cyc(V3(0, 1, three * PHI)) + cyc(V3(1, two + PHI, two * PHI)) + cyc(V3(PHI, two, PHI ** 3))
    TIp = Poly('truncated icosahedron', TI); assert len(TIp.V) == 60 and len(TIp.F) == 32
    PK = Poly('pentakis dodecahedron', [mul(ONE / bb, n) for n, bb, _ in TIp.F]); assert len(PK.V) == 32 and len(PK.F) == 60
    six = [v for v in range(32) if len(PK.tight[v]) == 6]; assert len(six) == 20
    cuts = []
    for q in six:
        hs = set()
        for r in six:
            if r != q and sum(1 for k in PK.tight[q] if k in PK.tight[r]) == 2:      # edge q-r
                hs.add(dot(PK.V[q], mul(Q5(Fr(1, 2)), add(PK.V[q], PK.V[r]))))
        assert len(hs) == 1; cuts.append((PK.V[q], hs.pop()))
    H = [(n, bb) for n, bb, _ in PK.F] + cuts
    A_ = np.array([np.append(fl(n), -bb.f()) for n, bb in H]); hsi = HalfspaceIntersection(A_, np.zeros(3))
    pts = {}
    for x in hsi.intersections:
        T = [i for i, (n, bb) in enumerate(H) if abs(fl(n) @ x - bb.f()) < 1e-8]
        for tr in itertools.combinations(T, 3):
            D = det3(*[H[k][0] for k in tr])
            if not D.z(): break
        n1, n2, n3 = [H[k][0] for k in tr]; d1, d2, d3 = [H[k][1] for k in tr]
        X = tuple(det3(*[tuple((d1, d2, d3)[r] if j == col else (n1, n2, n3)[r][j] for j in range(3)) for r in range(3)]) / D for col in range(3))
        assert all((bb - dot(n, X)).sign() >= 0 for n, bb in H); pts[key(X)] = X
    S['OG'] = Poly('Ogdoecontahedron (OG)', list(pts.values()))
    S['Hecatodihedron'] = Poly('Hecatodihedron', [mul(ONE / bb, n) for n, bb, _ in S['OG'].F])
    return S

S = {}
def p12(k):
    P = S[k]; ptsI = interior_points(P, 1 if PILOT else 4, 11); ptsA = any_points([P], 1 if PILOT else 4, 12)
    r1 = all(P.omega(Y) == P.omega_tri(Y) for Y in ptsI + ptsA)
    r2 = all(P.omega(Y) == P.polar_vol6(Y) for Y in ptsI)
    return k, r1, r2, len(ptsI) + len(ptsA), len(ptsI)
def res_task(k, fi, npts): return residue_check(S[k], fi, npts, 3)
def adj_task(k): return adjoint_degree(S[k], 41)

if __name__ == '__main__':
    print(f'chunk 5 {"PILOT" if PILOT else "FULL"} run', flush=True)
    S.update(build()); print(f'built in {time.time() - T0:.1f}s', flush=True)
    for k, P in S.items():
        if k.startswith('_'): continue
        fc, vc = P.counts()
        print(f'  {P.name}: {len(P.V)} corners, {P.E} edges, {len(P.F)} faces (by sides {fc}); corners by number of faces {vc}; Warren terms {len(P.terms)}', flush=True)
    print('PROGRESS 0.10 built', flush=True)

    # ---- (C1) controls with known answers
    cube = S['cube']; Y = V3(Fr(1, 97), Fr(1, 89), Fr(1, 83))
    check('(C1) cube: Omega = prod 1/(x(1-x)) at a generic point', cube.omega(Y) == ONE / ((Y[0] * (1 - Y[0])) * (Y[1] * (1 - Y[1])) * (Y[2] * (1 - Y[2]))))
    check('(C1) cube: Omega(centre) * vol = 64 (Mahler 32/3)', cube.omega(V3(Fr(1, 2), Fr(1, 2), Fr(1, 2))) * cube.vol6() / 6 == 64)
    sx = S['simplex']; check('(C1) simplex: Omega(centroid) * vol = 128/3 (Mahler 64/9)', sx.omega(V3(Fr(1, 4), Fr(1, 4), Fr(1, 4))) * sx.vol6() / 6 == Q5(Fr(128, 3)))
    N = S['Narcissus']
    check(f'(C2) Narcissus volume 3/4 in the rational frame (got {N.vol6() / 6})', N.vol6() / 6 == Q5(Fr(3, 4)))
    check(f'(C2) Narcissus: Omega(corner centroid) * vol = 68 (published Mahler 34/3)', N.omega(N.cen) * N.vol6() / 6 == 68)
    fc, vc = N.counts(); check(f'(C2) Narcissus: 10 corners, faces 1 hexagon + 3 quads + 6 triangles', len(N.V) == 10 and fc == {3: 6, 4: 3, 6: 1})
    OG = S['OG']; fc, vc = OG.counts()
    check('(C3) OG: 102 corners, 80 faces = 20 hexagons + 60 four-sided', len(OG.V) == 102 and fc == {4: 60, 6: 20})
    r2 = sorted({dot(v, v) for v in OG.V}, key=lambda x: x.f()); k = Q5(Fr(4, 9)) / r2[0]
    check(f'(C3) OG: two corner radii; scaled so 90 corners have r^2 = 4/9, the other 12 have (170+2sqrt5)/361 (got {r2[1] * k})',
          len(r2) == 2 and sum(1 for v in OG.V if dot(v, v) == r2[0]) == 90 and r2[1] * k == Q5(Fr(170, 361), Fr(2, 361)))
    el = {}
    for n, bb, vs in OG.F:
        for i in range(len(vs)):
            p, q = sorted((vs[i], vs[(i + 1) % len(vs)])); d = sub(OG.V[p], OG.V[q]); el[(p, q)] = dot(d, d) * k
    from collections import Counter
    cnt = Counter(el.values())
    check(f'(C3) OG: squared edges 120 x (2/9 - 2sqrt5/27), 60 x (86/3249 + 2sqrt5/361) (got {dict(cnt)})',
          cnt == Counter({Q5(Fr(2, 9), Fr(-2, 27)): 120, Q5(Fr(86, 3249), Fr(2, 361)): 60}))
    hexok = all(len({dot(sub(OG.V[vs[i]], OG.V[vs[i - 1]]), sub(OG.V[vs[i]], OG.V[vs[i - 1]])) for i in range(6)}) == 1
                and len({dot(sub(OG.V[vs[i]], OG.V[vs[i - 2]]), sub(OG.V[vs[i]], OG.V[vs[i - 2]])) for i in range(6)}) == 1 for n, bb, vs in OG.F if len(vs) == 6)
    check('(C3) OG: every hexagon regular (equal sides and equal short diagonals)', hexok)
    HC = S['Hecatodihedron']; check(f'(C3) Hecatodihedron: 80 corners, 102 faces', len(HC.V) == 80 and len(HC.F) == 102)
    print('PROGRESS 0.20 controls', flush=True)

    SOL = [k for k in S if not k.startswith('_')]
    ctx = get_context('fork')
    with ctx.Pool(4) as pool:
        # ---- (P1) Warren = triangulation, (P2) bridge
        for k, r1, r2, n1, n2 in pool.map(p12, SOL):
            check(f'(P1) {S[k].name}: Warren = triangulation formula at {n1} generic points (inside and outside)', r1)
            check(f'(P2) {S[k].name}: Omega(P;Y) = 3! vol(polar about Y) at {n2} interior points', r2)
        print('PROGRESS 0.40 P1 P2', flush=True)
        # ---- (N1), (N3)
        Y = interior_points(OG, 1, 5)[0]
        check('(N1) OG with one Warren term dropped: Warren != triangulation (caught)', OG.omega(Y, drop=7) != OG.omega_tri(Y))
        An = S['Antonius']; Y = interior_points(An, 1, 6)[0]
        check('(N3) Antonius treated as simple (one fan triangle per 4-face corner): bridge fails (caught)', An.omega(Y, simple_only=True) != An.polar_vol6(Y))
        # ---- (P3) residues on every facet
        tasks = [(k, fi) for k in SOL for fi in range(len(S[k].F))]
        res = pool.starmap(res_task, [(k, fi, 1 if PILOT else 3) for k, fi in tasks])
        for k in SOL:
            r = [res[i] for i, (kk, fi) in enumerate(tasks) if kk == k]
            check(f'(P3) {S[k].name}: residue on each of its {len(r)} faces = canonical form of that face ({sum(g for g, n in r)}/{sum(n for g, n in r)} points)', all(g == n for g, n in r))
        print('PROGRESS 0.60 P3 residues', flush=True)
        # ---- (P4) joins
        R, C1, An, C2 = S['golden prolate rhombohedron'], S['Cleo-Icos'], S['Antonius'], S['Cleo-Icos (far corner)']
        planes, rows = cert_setup(R, [C1, An, C2]); D = len(planes) - 3
        grid = [Q5(Fr(i, D + 1) - Fr(1, 3)) for i in range(D + 1)]
        G = [(x, y, zz) for x in grid for y in grid for zz in grid]
        chunks = [(planes, rows, G[i::4]) for i in range(4)]
        out = pool.map(cert_eval, chunks); bad = sum(b for b, n in out)
        check(f'(P4) Omega(rhombohedron) = Omega(Cleo) + Omega(Antonius) + Omega(Cleo) as rational functions: {len(planes)} planes, '
              f'cleared numerator degree <= {D}, zero on all {len(G)} points of a {D + 1}^3 grid', bad == 0)
        # inner planes of the rhombohedron = the two cut planes
        cutA = [(n, bb) for n, bb, vs in An.F if len(vs) == 3 and not any(all(x.z() for x in cross(n, m)) and bb * dot(m, m) == b2 * dot(n, m) for m, b2, _ in R.F)]
        rng = random.Random(9); okj = True; nj = 0
        for n, bb in cutA:
            p0 = next(v for v in An.V if (bb - dot(n, v)).z()); u = cross(n, V3(1, 0, 0)); w = cross(n, u)
            for _ in range(3):
                Y = add(p0, add(mul(Q5(Fr(rng.randint(-999, 999), 1000)), u), mul(Q5(Fr(rng.randint(-999, 999), 1000)), w)))
                try: okj &= join_residue([C1, An, C2], n, bb, Y).z(); nj += 1
                except ZeroDivisionError: pass
        check(f'(P4) rhombohedron: on both inner cut planes the poles of Cleo + Antonius + Cleo cancel ({nj} points, residue 0)', okj and len(cutA) == 2)
        print('PROGRESS 0.70 rhombohedron joins', flush=True)
        I = S['icosahedron']; cl = S['_ico_cleos']
        pts = any_points([I] + cl, 2 if PILOT else 8, 21)
        check(f'(P4) Omega(icosahedron) = sum of the 20 Cleo-Icos forms at {len(pts)} generic points (inside and outside)',
              all(I.omega(Y) == sum((c.omega(Y) for c in cl), ZERO) for Y in pts))
        inner = {}
        for n, bb, vs in I.F:
            for i in range(3):
                p, q = I.V[vs[i]], I.V[vs[(i + 1) % 3]]; nn = cross(p, q); m = next(x for x in nn if not x.z()); nn = mul(ONE / m, nn); inner[key(nn)] = (nn, p, q)
        okj = True; rng = random.Random(10)
        for nn, p, q in inner.values():
            Y = add(mul(Q5(Fr(rng.randint(1, 999), 1000)), p), mul(Q5(Fr(rng.randint(-999, 999), 1000)), q))
            okj &= join_residue(cl, nn, ZERO, Y).z()
        check(f'(P4) icosahedron: on all {len(inner)} inner planes (centre + two opposite edges, four Cleo-Icos faces each) the poles of the 20 Cleo-Icos cancel', okj and len(inner) == 15)
        N, Np, Ns = S['Narcissus'], S['_N_covenant_partner'], S['_N_shifted']; Cov = S['Covenant']
        check(f'(P4) Covenant is the convex union of the two Narcissus (vol = 2 vol N)', Cov.vol6() == 2 * N.vol6())
        planes, rows = cert_setup(Cov, [N, Np]); D = len(planes) - 3
        grid = [Q5(Fr(i, D + 1) - Fr(1, 2)) for i in range(D + 1)]; G = [(x, y, zz) for x in grid for y in grid for zz in grid]
        if PILOT: G = G[::50]
        out = pool.map(cert_eval, [(planes, rows, G[i::4]) for i in range(4)]); bad = sum(b for b, n in out)
        check(f'(P4) Omega(Covenant) = Omega(N) + Omega(N turned) {"(pilot: grid subsample)" if PILOT else "as rational functions"}: {len(planes)} planes, '
              f'degree <= {D}, zero on {len(G)} grid points', bad == 0)
        hexn = (V3(0, 0, 1), ZERO); rng = random.Random(12); hp = [V3(Fr(rng.randint(-999, 1999), 1000), Fr(rng.randint(-999, 1999), 1000), 0) for _ in range(4)]
        check('(P4) Covenant: on the hexagon plane the poles of the two Narcissus cancel (4 points)', all(join_residue([N, Np], *hexn, Y).z() for Y in hp))
        Nm = S['_N_turned_over']
        check('(P4) straight pair: on the hexagon plane the poles cancel (4 points)', all(join_residue([N, Nm], *hexn, Y).z() for Y in hp))
        check('(N2) mis-joined pair (second Narcissus shifted 1/7): a pole is left on the hexagon plane (caught)', any(not join_residue([N, Ns], *hexn, Y).z() for Y in hp))
        SP = S['straight pair']; conv_sp = SP.vol6() == 2 * N.vol6()
        # off-axis control point must avoid the hexagon's mirror planes: (1/3, 1/2, z) lies on one and gives equal values (debug 12 Nov)
        axp = [V3(Fr(1, 2), Fr(1, 2), Fr(k_, 13)) for k_ in (-5, -2, 3, 7)]
        check('(P4) Covenant and twisted cube (straight pair) have the same canonical form all along the 3-fold axis (4 points; the 60 deg turn fixes the axis, det 1)',
              all(Cov.omega(Y) == SP.omega(Y) for Y in axp) and Cov.omega(V3(Fr(1, 3), Fr(3, 7), Fr(1, 5))) != SP.omega(V3(Fr(1, 3), Fr(3, 7), Fr(1, 5))))
        print(f'straight pair convex (hull volume = 2 vol N): {conv_sp}; hull faces {SP.counts()[0]}', flush=True)
        print('PROGRESS 0.85 joins', flush=True)
        # ---- (P5) affine images
        L = lambda y: add(add(mul(y[0], a_), mul(y[1], b_)), mul(y[2], c_))
        a_, b_, c_ = V3(0, 1, PHI), V3(0, -1, PHI), V3(PHI, 0, 1); dL = det3(a_, b_, c_)
        pts = any_points([S['cube'], S['simplex'], S['cube middle octahedron']], 3, 31)
        check('(P5) Cleo-Icos, Antonius, rhombohedron = images of the cube corner simplex, middle octahedron, cube: Omega(L y) |det L| = Omega(y)',
              all(S['Cleo-Icos'].omega(L(y)) * abs(dL) == S['simplex'].omega(y) and S['Antonius'].omega(L(y)) * abs(dL) == S['cube middle octahedron'].omega(y)
                  and S['golden prolate rhombohedron'].omega(L(y)) * abs(dL) == S['cube'].omega(y) for y in pts))

        # ---- RESULTS: Mahler products = Omega * vol / 6 at the Santalo point
        print('\nRESULTS: Omega at the Santalo point and the Mahler product (= Omega * vol / 6)', flush=True)
        for k, Y in [('Cleo-Icos', None), ('Antonius', None), ('golden prolate rhombohedron', None), ('icosahedron', V3(0, 0, 0)),
                     ('OG', V3(0, 0, 0)), ('Hecatodihedron', V3(0, 0, 0)), ('Covenant', V3(Fr(1, 2), Fr(1, 2), 0))]:
            P = S[k]; Y = Y or P.cen; om = P.omega(Y); m = om * P.vol6() / 36
            print(f'  {P.name}: Santalo point {"centre" if k != "Cleo-Icos" else "centroid"}; Omega = {om} = {om.f():.9f}; vol = {P.vol6() / 6}; Mahler = {m} = {m.f():.9f}', flush=True)
            if k == 'OG': mOG = m; omOG = om
            if k == 'Hecatodihedron': mH = m; omH = om
            if k in ('Antonius', 'golden prolate rhombohedron'): check(f'(P5) {P.name}: Mahler = 32/3 (affine octahedron / cube)', m == Q5(Fr(32, 3)))
            if k == 'Cleo-Icos': check('(P5) Cleo-Icos: Mahler = 64/9 (affine simplex)', m == Q5(Fr(64, 9)))
        check('(P2) OG and Hecatodihedron: Omega(OG;0) = 6 vol(Heca), Omega(Heca;0) = 6 vol(OG), same Mahler', omOG == HC.vol6() and omH == OG.vol6() and mOG == mH)
        for k, sym in [('icosahedron', True), ('OG', True), ('Covenant', True)]:
            P = S[k]; Y = V3(0, 0, 0) if k != 'Covenant' else V3(Fr(1, 2), Fr(1, 2), 0); m = (P.omega(Y) * P.vol6() / 36).f()
            check(f'    {P.name}: 32/3 <= Mahler <= (4pi/3)^2 (Iriyeh-Shibata 2020; Blaschke-Santalo) and <= 8E/9 (Winter 2026, E={P.E}): {m:.6f}',
                  32 / 3 - 1e-12 <= m <= (4 * np.pi / 3) ** 2 and m <= 8 * P.E / 9 + 1e-12)
        zs = sp.symbols('z', real=True)
        for k, A0, zlo, zhi in [('Narcissus', V3(Fr(1, 2), Fr(1, 2), 0), -1, 0)] + ([('straight pair', V3(Fr(1, 2), Fr(1, 2), 0), -1, 1)] if conv_sp else []):
            P = S[k]; Mz = mahler_line(P, A0, V3(0, 0, 1), zs)
            num = sp.Poly(sp.numer(sp.together(sp.diff(Mz, zs))), zs)
            roots = [r for r in sp.Poly(num, zs).real_roots() if zlo < r < zhi]
            print(f'  {P.name}: on the 3-fold axis (1/2,1/2,z): dM/dz numerator factors {sp.factor_list(num.as_expr())}', flush=True)
            check(f'    {P.name}: exactly one critical point on the axis inside', len(roots) == 1)
            if len(roots) == 1:
                r = roots[0]; mval = Mz.subs(zs, r); mn = sp.N(mval, 30)
                msym = sp.Symbol('m')
                if r.is_rational: mp_ = sp.nsimplify(mval)
                else:
                    p_, q_ = sp.fraction(sp.together(Mz))
                    g = [f for f, _ in sp.factor_list(num.as_expr())[1] if abs(sp.N(f.subs(zs, r), 50)) < 1e-30][0]
                    resm = sp.resultant(g, msym * q_ - p_, zs)
                    mp_ = [f for f, _ in sp.factor_list(resm, msym)[1] if abs(sp.N(f.subs(msym, sp.N(mval, 60)), 50)) < 1e-25][0]
                print(f'  {P.name}: Santalo point z = {r} = {sp.N(r, 20)}; Mahler = {sp.N(mval, 20)}; minimal polynomial {mp_}', flush=True)
                if k == 'Narcissus':
                    check(f'    Narcissus: Santalo Mahler < 34/3 (corner-centroid value) and >= 64/9 (conjectured simplex minimum)', sp.Rational(64, 9) <= mn < sp.Rational(34, 3))
        print('\nADJOINT degree on a generic line (affine chart; <= faces - 4 by Warren)', flush=True)
        ks = [k for k in SOL if k not in ('OG', 'Hecatodihedron')] + ([] if PILOT else ['OG', 'Hecatodihedron'])
        degs = pool.map(adj_task, ks)
        for k, dgr in zip(ks, degs):
            check(f'    {S[k].name}: adjoint degree {dgr} <= {len(S[k].F) - 4} (faces - 4)', dgr <= len(S[k].F) - 4)
        print('PROGRESS 1.00 done', flush=True)
    print(f'time {time.time() - T0:.1f}s', flush=True)
    print('FINAL ok: all checks and controls held' if OK else 'FINAL FAIL: a check or control failed', flush=True)
