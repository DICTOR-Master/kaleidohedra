#!/usr/bin/env python3
"""The associahedron shell (24 Nov 2026), exact.

The region between a hidden associahedron Asso_c (Hohlweg-Lange-Thomas) and the permutahedron P inside it, for A3, B3, H3 and
all four Coxeter elements c (linear s1s2s3, s3s2s1; bipartite s2s1s3, s1s3s2).

Division rule (the equal-speed rule, a straight skeleton): P grows into Asso_c. The kept faces of P already lie on the faces of
Asso_c and stay. Every removed face R moves outward, parallel to itself, at the same speed; at time t the solid is
P_t = {x : kept inequalities, d_R(x) <= t for every removed R}, with d_R the signed Euclidean distance to the plane of R.
P_0 = P, and P_t = Asso_c for t large. A point x of the shell belongs to the face that reaches it first:
    piece(R) = {x in Asso_c : d_R(x) >= 0 and d_R(x) >= d_F(x) for every removed F}.
Inner end = R itself; outer end = the part of the associahedron's surface in the piece; walls = bisector planes.
Baseline (rule "cone"): the same with d_R(x) = (n_R.x - b_R)/b_R (gauge of P): walls through the centre (Lemma 3 setting).

Arithmetic: every number lies in a tower of real quadratic fields Q(sqrt r1)(sqrt r2)..., stored as nested pairs (a, b) = a + b sqrt(r)
over Fractions. Signs are exact (recursive comparison of a^2 with b^2 r; each r is a non-square in the field below, argued in the README).
No floats in any decision; floats only for the JSON preview coordinates.
Usage: shell.py A3 B3 H3   -> data/shell-<type>.json, log on stdout, FINAL ok only if every check passed.
"""
import sys, os, json, itertools, time, functools
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "../data")
def pr(*a): print(*a, flush=True)

# ---------------------------------------------------------------- tower field
class Tower:
    def __init__(self, rads):
        # rads[k] builds the radicand of level k+1, an element of level k (nested pairs over Fractions)
        self.R = []; self.L = 0
        for mk in rads:
            self.R.append(mk(self)); self.L += 1
    def z(self, k):                 # zero of level k
        x = Fr(0)
        for _ in range(k): x = (x, x)
        return x
    def o(self, k):                 # one of level k
        x = Fr(1)
        for j in range(k): x = (x, self.z(j))
        return x
    def lift(self, x, k):           # embed an element of level k at the top level
        for j in range(k, self.L): x = (x, self.z(j))
        return x
    def q(self, x): return self.lift(Fr(x), 0)
    def sq(self, k):                # sqrt(r_k) at the top level (k = 1..L)
        return self.lift((self.z(k - 1), self.o(k - 1)), k)


def _add(x, y, k):
    if k == 0: return x + y
    return (_add(x[0], y[0], k - 1), _add(x[1], y[1], k - 1))
def _sub(x, y, k):
    if k == 0: return x - y
    return (_sub(x[0], y[0], k - 1), _sub(x[1], y[1], k - 1))
def _neg(x, k):
    if k == 0: return -x
    return (_neg(x[0], k - 1), _neg(x[1], k - 1))
def _isz(x, k):
    if k == 0: return x == 0
    return _isz(x[0], k - 1) and _isz(x[1], k - 1)

class F_:
    """Operations at the top level of a tower T."""
    def __init__(self, T):
        self.T = T; self.L = T.L; self.R = T.R
        self.zero = T.lift(Fr(0), 0); self.one = T.lift(Fr(1), 0)
    def add(self, x, y): return _add(x, y, self.L)
    def sub(self, x, y): return _sub(x, y, self.L)
    def neg(self, x): return _neg(x, self.L)
    def isz(self, x): return _isz(x, self.L)
    def mul(self, x, y, k=None):
        if k is None: k = self.L
        if k == 0: return x * y
        a, b = x; c, d = y
        if _isz(b, k - 1):
            if _isz(d, k - 1): return (self.mul(a, c, k - 1), d)
            return (self.mul(a, c, k - 1), self.mul(a, d, k - 1))
        if _isz(d, k - 1): return (self.mul(a, c, k - 1), self.mul(b, c, k - 1))
        r = self.R[k - 1]
        return (_add(self.mul(a, c, k - 1), self.mul(self.mul(b, d, k - 1), r, k - 1), k - 1),
                _add(self.mul(a, d, k - 1), self.mul(b, c, k - 1), k - 1))
    def inv(self, x, k=None):
        if k is None: k = self.L
        if k == 0:
            assert x != 0; return 1 / x
        a, b = x; r = self.R[k - 1]
        den = _sub(self.mul(a, a, k - 1), self.mul(self.mul(b, b, k - 1), r, k - 1), k - 1)
        di = self.inv(den, k - 1)
        return (self.mul(a, di, k - 1), _neg(self.mul(b, di, k - 1), k - 1))
    def div(self, x, y): return self.mul(x, self.inv(y))
    def sign(self, x, k=None):
        if k is None: k = self.L
        if k == 0: return (x > 0) - (x < 0)
        a, b = x
        sa = self.sign(a, k - 1); sb = self.sign(b, k - 1)
        if sb == 0: return sa
        if sa == 0 or sa == sb: return sb if sa == 0 else sa
        r = self.R[k - 1]
        s = self.sign(_sub(self.mul(a, a, k - 1), self.mul(self.mul(b, b, k - 1), r, k - 1), k - 1), k - 1)
        assert s != 0, "radicand is a square: tower degenerate"
        return sa if s > 0 else sb
    def val(self, x, k=None):
        if k is None: k = self.L
        if k == 0: return float(x)
        return self.val(x[0], k - 1) + self.val(x[1], k - 1) * self.val(self.R[k - 1], k - 1) ** 0.5
    def s(self, x, k=None):
        if k is None: k = self.L
        if k == 0: return str(x)
        if _isz(x[1], k - 1): return self.s(x[0], k - 1)
        return f"({self.s(x[0], k - 1)})+({self.s(x[1], k - 1)})*sqrt[{self.s(self.R[k - 1], k - 1)}]"
    def q(self, v): return self.T.q(v)

# vector helpers
def dot(K, a, b): return K.add(K.add(K.mul(a[0], b[0]), K.mul(a[1], b[1])), K.mul(a[2], b[2]))
def cross(K, a, b): return (K.sub(K.mul(a[1], b[2]), K.mul(a[2], b[1])), K.sub(K.mul(a[2], b[0]), K.mul(a[0], b[2])),
                            K.sub(K.mul(a[0], b[1]), K.mul(a[1], b[0])))
def vsub(K, a, b): return tuple(K.sub(x, y) for x, y in zip(a, b))
def vadd(K, a, b): return tuple(K.add(x, y) for x, y in zip(a, b))
def scal(K, s, a): return tuple(K.mul(s, x) for x in a)
def vneg(K, a): return tuple(K.neg(x) for x in a)
def isz3(K, a): return all(K.isz(x) for x in a)
def det3(K, a, b, c): return dot(K, a, cross(K, b, c))

# ---------------------------------------------------------------- the three groups
def setup(typ):
    if typ == "A3":     # D3 coordinates, a = (2,1,0): uniform truncated octahedron. Tower Q(sqrt3).
        T = Tower([lambda t: Fr(3)]); K = F_(T); q = K.q
        mir = [(1, -1, 0), (1, 1, 0), (1, 0, -1), (1, 0, 1), (0, 1, -1), (0, 1, 1)]
        mir = [tuple(q(x) for x in m) for m in mir]
        a = (q(2), q(1), q(0)); name = "truncated octahedron"
        sqrts = {"1": K.one, "3": T.sq(1)}
        rho = {"1": K.one, "3": q(3)}
    elif typ == "B3":   # a = (1+2r2, 1+r2, 1): uniform truncated cuboctahedron. Tower Q(sqrt2)(sqrt3).
        T = Tower([lambda t: Fr(2), lambda t: (Fr(3), Fr(0))]); K = F_(T); q = K.q
        r2 = T.sq(1)
        mir = [(1, -1, 0), (1, 1, 0), (1, 0, -1), (1, 0, 1), (0, 1, -1), (0, 1, 1), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        mir = [tuple(q(x) for x in m) for m in mir]
        a = (K.add(q(1), K.mul(q(2), r2)), K.add(q(1), r2), q(1)); name = "truncated cuboctahedron"
        sqrts = {"1": K.one, "2": r2, "3": T.sq(2), "6": K.mul(r2, T.sq(2))}
        rho = {"1": K.one, "2": q(2), "3": q(3), "6": q(6)}
    else:               # H3: icosahedron (0,+-1,+-phi); a = (1/phi, 1/phi, 3+phi). Tower Q(sqrt5)(sqrt3)(sqrt((5+sqrt5)/2)).
        T = Tower([lambda t: Fr(5), lambda t: (Fr(3), Fr(0)), lambda t: ((Fr(5, 2), Fr(1, 2)), (Fr(0), Fr(0)))]); K = F_(T); q = K.q
        r5 = T.sq(1); phi = K.mul(K.add(q(1), r5), q(Fr(1, 2))); ip = K.sub(phi, q(1))
        mir = [(q(1), q(0), q(0)), (q(0), q(1), q(0)), (q(0), q(0), q(1))]
        for s1, s2 in itertools.product((1, -1), repeat=2):
            t = (phi, q(s1), K.mul(q(s2), ip))
            mir += [t, (t[2], t[0], t[1]), (t[1], t[2], t[0])]
        a = (ip, ip, K.add(q(3), phi)); name = "truncated icosidodecahedron"
        p2 = K.add(phi, q(2))
        sqrts = {"1": K.one, "3": T.sq(2), "phi+2": T.sq(3), "3(phi+2)": K.mul(T.sq(2), T.sq(3))}
        rho = {"1": K.one, "3": q(3), "phi+2": p2, "3(phi+2)": K.mul(q(3), p2)}
    return T, K, mir, a, name, sqrts, rho

def base_sqrt(K, x, typ):
    """sqrt of x, x in the base field (Q, or Q(sqrt2) / Q(sqrt5) as level 1), returned at the top level, or None."""
    def rsqrt(f):
        if f < 0: return None
        import math
        n, d = f.numerator, f.denominator
        rn, rd = math.isqrt(n), math.isqrt(d)
        return Fr(rn, rd) if rn * rn == n and rd * rd == d else None
    T = K.T
    def down(y, lev):        # project top-level element to level lev (assert higher parts zero)
        for k in range(T.L, lev, -1):
            assert _isz(y[1], k - 1); y = y[0]
        return y
    if typ == "A3":
        f = down(x, 0); r = rsqrt(f)
        return None if r is None else T.lift(r, 0)
    u, v = down(x, 1); dd = T.R[0]
    if v == 0:
        r = rsqrt(u)
        if r is not None: return T.lift((r, Fr(0)), 1)
        r = rsqrt(u / dd)
        return None if r is None else T.lift((Fr(0), r), 1)
    disc = rsqrt(u * u - dd * v * v)
    if disc is None: return None
    for X in ((u + disc) / 2, (u - disc) / 2):
        xx = rsqrt(X)
        if xx: return T.lift((xx, v / (2 * xx)), 1)
    return None

def unit_scale(K, n, typ, sqrts, rho):
    """1/|n| exactly, n with norm^2 in the base field."""
    N = dot(K, n, n)
    for key in rho:
        s = base_sqrt(K, K.div(N, rho[key]), typ)
        if s is not None:
            if K.sign(s) < 0: s = K.neg(s)          # the positive square root
            u = K.inv(K.mul(s, sqrts[key]))
            assert K.sign(u) > 0 and K.isz(K.sub(K.mul(K.mul(u, u), N), K.one)), "unit scale"
            return u, key
    raise AssertionError("norm not in the tower")

# ---------------------------------------------------------------- matrices
def refl(K, m):
    mm = dot(K, m, m); c = K.div(K.q(2), mm)
    return tuple(tuple(K.sub(K.one if i == j else K.zero, K.mul(c, K.mul(m[i], m[j]))) for j in range(3)) for i in range(3))
def mmul(K, A, B): return tuple(tuple(K.add(K.add(K.mul(A[i][0], B[0][j]), K.mul(A[i][1], B[1][j])), K.mul(A[i][2], B[2][j])) for j in range(3)) for i in range(3))
def apply(K, A, v): return tuple(dot(K, A[i], v) for i in range(3))

# ---------------------------------------------------------------- exact convex polytopes by clipping
class Poly:
    """faces: label -> (normal, offset, [vertex keys] counter-clockwise seen from outside); verts: key -> coords."""
    def __init__(self, K): self.K = K; self.faces = {}; self.verts = {}
    def copy(self):
        p = Poly(self.K); p.faces = dict(self.faces); p.verts = dict(self.verts); return p

def box(K, B):
    p = Poly(K); q = K.q
    V = {}
    for s in itertools.product((-1, 1), repeat=3):
        V[s] = tuple(q(B * x) for x in s)
    p.verts = {V[s]: V[s] for s in V}
    for ax in range(3):
        for sg in (-1, 1):
            n = tuple(q(sg if i == ax else 0) for i in range(3))
            vs = [V[s] for s in V if s[ax] == sg]
            p.faces[("box", ax, sg)] = (n, q(B), order_ccw(K, vs, vs, n))
    return p

def order_ccw(K, pts, keys, n):
    m = len(pts)
    c = tuple(K.mul(sum_(K, [p[i] for p in pts]), K.inv(K.q(m))) for i in range(3))
    u = vsub(K, pts[0], c); w = cross(K, n, u)
    xy = [(dot(K, vsub(K, p, c), u), dot(K, vsub(K, p, c), w)) for p in pts]
    def half(t):
        sx, sy = K.sign(t[0]), K.sign(t[1])
        return 0 if (sy > 0 or (sy == 0 and sx > 0)) else 1
    def cmp(i, j):
        hi, hj = half(xy[i]), half(xy[j])
        if hi != hj: return hi - hj
        cr = K.sign(K.sub(K.mul(xy[i][0], xy[j][1]), K.mul(xy[i][1], xy[j][0])))
        return -cr
    idx = sorted(range(m), key=functools.cmp_to_key(cmp))
    return [keys[i] for i in idx]

def sum_(K, xs):
    s = K.zero
    for x in xs: s = K.add(s, x)
    return s

def vkey(K, v): return v   # nested tuples of Fractions are canonical and hashable

def clip(P, n, off, label):
    """P intersected with n.x <= off. Returns new Poly or None (empty / flat)."""
    K = P.K
    hv = {k: K.sub(dot(K, n, v), off) for k, v in P.verts.items()}
    sg = {k: K.sign(h) for k, h in hv.items()}
    if all(s <= 0 for s in sg.values()): return P
    if all(s >= 0 for s in sg.values()): return None
    Q = Poly(K); cap = {}
    newv = {}
    def inter(u, v):
        key = (u, v) if (u, v) < (v, u) else (v, u)
        if key in newv: return newv[key]
        t = K.div(hv[u], K.sub(hv[u], hv[v]))
        x = vadd(K, P.verts[u], scal(K, t, vsub(K, P.verts[v], P.verts[u])))
        newv[key] = x; return x
    coplanar = False
    for lab, (fn, fo, cyc) in P.faces.items():
        if all(sg[k] == 0 for k in cyc): coplanar = True
        out = []
        L = len(cyc)
        for i in range(L):
            u, v = cyc[i], cyc[(i + 1) % L]
            if sg[u] <= 0:
                out.append(u); Q.verts[u] = P.verts[u]
                if sg[u] == 0: cap[u] = P.verts[u]
            if sg[u] * sg[v] < 0:
                x = inter(u, v); Q.verts[x] = x; out.append(x); cap[x] = x
        ded = []
        for k in out:
            if not ded or ded[-1] != k: ded.append(k)
        if len(ded) > 1 and ded[0] == ded[-1]: ded.pop()
        if len(ded) >= 3: Q.faces[lab] = (fn, fo, ded)
    if len(cap) >= 3 and not coplanar:
        ks = list(cap.keys())
        Q.faces[label] = (n, off, order_ccw(K, [cap[k] for k in ks], ks, n))
    used = {k for (_, _, c) in Q.faces.values() for k in c}
    Q.verts = {k: Q.verts[k] for k in used}
    if volume(Q) == K.zero or K.sign(volume(Q)) <= 0: return None
    return Q

def volume(P):
    K = P.K; tot = K.zero
    for (_, _, cyc) in P.faces.values():
        v0 = P.verts[cyc[0]]
        for i in range(1, len(cyc) - 1):
            tot = K.add(tot, det3(K, v0, P.verts[cyc[i]], P.verts[cyc[i + 1]]))
    return K.mul(tot, K.inv(K.q(6)))

def area_vec(P, cyc, verts=None):
    K = P.K; V = verts or P.verts; s = (K.zero, K.zero, K.zero)
    for i in range(len(cyc)):
        s = vadd(K, s, cross(K, V[cyc[i]], V[cyc[(i + 1) % len(cyc)]]))
    return scal(K, K.inv(K.q(2)), s)

# ---------------------------------------------------------------- main
CATALAN = {"A3": 14, "B3": 20, "H3": 32}
PERMF = {"A3": 14, "B3": 26, "H3": 62}
WORD = {"A3": 24, "B3": 48, "H3": 120}

def run(typ):
    t0 = time.time()
    T, K, mir, a, name, sqrts, rho = setup(typ)
    N = len(mir)
    mir = [m if K.sign(dot(K, m, a)) > 0 else vneg(K, m) for m in mir]
    R = [refl(K, m) for m in mir]
    I = tuple(tuple(K.one if i == j else K.zero for j in range(3)) for i in range(3))
    def length(A):
        b = apply(K, A, a); return sum(1 for m in mir if K.sign(dot(K, m, b)) < 0)
    simple = [k for k in range(N) if length(R[k]) == 1]
    assert len(simple) == 3
    S0 = [R[k] for k in simple]; al0 = [mir[k] for k in simple]
    def order(A):
        B = A
        for o in range(1, 13):
            if B == I: return o
            B = mmul(K, B, A)
        raise AssertionError
    m0 = [[order(mmul(K, S0[i], S0[j])) if i != j else 1 for j in range(3)] for i in range(3)]
    mid = [i for i in range(3) if all(m0[i][j] > 2 for j in range(3) if j != i)][0]
    ends = sorted([i for i in range(3) if i != mid], key=lambda i: -m0[i][mid])
    perm = [ends[0], mid, ends[1]]
    S = [S0[i] for i in perm]; al = [al0[i] for i in perm]
    M = [[order(mmul(K, S[i], S[j])) if i != j else 1 for j in range(3)] for i in range(3)]
    # the group
    W = {I: I}; fr = [I]
    while fr:
        nf = []
        for A in fr:
            for s in S:
                B = mmul(K, A, s)
                if B not in W: W[B] = B; nf.append(B)
        fr = nf
    W = list(W)
    assert len(W) == WORD[typ], len(W)
    pr(f"{typ} ({name}): |W| = {len(W)}, mirrors {N}, Coxeter matrix {M}, tower radicands {[K.s(r, k) for k, r in enumerate(T.R)]}")
    om = []
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        w = cross(K, al[j], al[k])
        if K.sign(dot(K, w, al[i])) < 0: w = vneg(K, w)
        om.append(w)
    Vp = [apply(K, A, a) for A in W]
    keyV = {v: i for i, v in enumerate(Vp)}
    assert len(keyV) == len(W)
    facets = {}; vfac = {}
    us = [unit_scale(K, om[i], typ, sqrts, rho) for i in range(3)]
    for A in W:
        v = apply(K, A, a)
        for i in range(3):
            n = apply(K, A, om[i])
            j, l = [x for x in range(3) if x != i]
            facets.setdefault(n, {"n": n, "b": dot(K, a, om[i]), "type": i, "sides": 2 * M[j][l], "u": us[i][0]})
            vfac.setdefault(keyV[v], set()).add(n)
    assert len(facets) == PERMF[typ]
    fkeys = sorted(facets, key=lambda k: (facets[k]["type"], [K.val(x) for x in k]))
    fid = {k: i for i, k in enumerate(fkeys)}
    pr(f"  facet types (sides): {[2 * M[[x for x in range(3) if x != i][0]][[x for x in range(3) if x != i][1]] for i in range(3)]}; |n|^2 = q^2 * {[us[i][1] for i in range(3)]}")
    # the permutahedron, exactly, by clipping a box
    Bx = 10 ** 4
    def build(keys):
        p = box(K, Bx)
        for k in keys:
            p = clip(p, facets[k]["n"], facets[k]["b"], ("F", fid[k]))
        assert not any(l[0] == "box" for l in p.faces), "box face survived"
        return p
    P = build(fkeys)
    assert len(P.verts) == len(W) and len(P.faces) == PERMF[typ]
    for k in fkeys:
        assert len(P.faces[("F", fid[k])][2]) == facets[k]["sides"]
    volP = volume(P)
    pr(f"  permutahedron: {len(P.verts)} vertices, {len(P.faces)} faces, volume {K.val(volP):.6f} (exact)")
    CW = {"s1 s2 s3 (linear)": [0, 1, 2], "s3 s2 s1 (linear, inverse)": [2, 1, 0],
          "s2 s1 s3 (bipartite)": [1, 0, 2], "s1 s3 s2 (bipartite, inverse)": [0, 2, 1]}
    out = {"type": typ, "permutahedron": name, "W": len(W), "coxeter_matrix": M, "vol_perm": K.s(volP),
           "vol_perm_float": K.val(volP), "results": {}}
    ok_all = True
    for cname, cw in CW.items():
        word, A = [], I
        while length(A) < N:
            for s in cw:
                B = mmul(K, A, S[s])
                if length(B) > length(A): word.append(s); A = B
                if length(A) == N: break
        cls = {tuple(word)}; fr = [tuple(word)]
        while fr:
            nf = []
            for w in fr:
                for p in range(len(w) - 1):
                    if M[w[p]][w[p + 1]] == 2:
                        u = w[:p] + (w[p + 1], w[p]) + w[p + 2:]
                        if u not in cls: cls.add(u); nf.append(u)
            fr = nf
        sing = {}
        for w in cls:
            A = I; sing[A] = A
            for s in w: A = mmul(K, A, S[s]); sing[A] = A
        singV = {keyV[apply(K, A, a)] for A in sing}
        kept = set()
        for vi in singV: kept |= vfac[vi]
        removed = [k for k in fkeys if k not in kept]
        keptl = [k for k in fkeys if k in kept]
        assert len(kept) == 3 + N
        Asso = build(keptl)
        assert len(Asso.verts) == CATALAN[typ], len(Asso.verts)
        volA = volume(Asso)
        shellvol = K.sub(volA, volP)
        res = {"kept": len(keptl), "removed": len(removed), "vol_assoc": K.s(volA), "vol_shell": K.s(shellvol),
               "vol_shell_float": K.val(shellvol), "rules": {}}
        pr(f"  c = {cname}: kept {len(keptl)}, removed {len(removed)} "
           f"(by sides {sorted((facets[k]['sides'] for k in removed))}); associahedron {len(Asso.verts)} vertices; "
           f"shell volume {K.val(shellvol):.6f}")
        # P faces adjacency (edges) for rim analysis
        Pedge = {}
        for lab, (_, _, cyc) in P.faces.items():
            for i in range(len(cyc)):
                e = frozenset((cyc[i], cyc[(i + 1) % len(cyc)])); Pedge.setdefault(e, []).append(lab[1])
        remid = {fid[k] for k in removed}
        rim_edges = sum(1 for e, fs in Pedge.items() if (fs[0] in remid) != (fs[1] in remid))
        res["rim_edges"] = rim_edges
        # shell components: clusters of removed faces joined by edges
        adj = {r: set() for r in remid}
        for e, fs in Pedge.items():
            if fs[0] in remid and fs[1] in remid: adj[fs[0]].add(fs[1]); adj[fs[1]].add(fs[0])
        comps = []; seen = set()
        for r in sorted(remid):
            if r in seen: continue
            st = [r]; cc = set()
            while st:
                x = st.pop()
                if x in cc: continue
                cc.add(x); st += list(adj[x])
            seen |= cc; comps.append(sorted(cc))
        res["components"] = [[facets[fkeys[r]]["sides"] for r in c] for c in comps]
        pr(f"    rim edges (removed face next to kept face) {rim_edges}; shell components (clusters of removed faces): "
           f"{len(comps)}, sizes {[len(c) for c in comps]}")
        for rule in ("equal-speed", "cone"):
            r_ok, rr = pieces(K, typ, facets, fkeys, fid, removed, keptl, Asso, P, shellvol, rule, us)
            ok_all &= r_ok
            res["rules"][rule] = rr
        out["results"][cname] = res
    # c and c^-1 isometric: compare piece-type multisets
    keys = list(CW)
    for rule in ("equal-speed", "cone"):
        for x, y in ((keys[0], keys[1]), (keys[2], keys[3])):
            tx = sorted(out["results"][x]["rules"][rule]["type_multiset"]); ty = sorted(out["results"][y]["rules"][rule]["type_multiset"])
            pr(f"  {rule}: piece types of {x} and {y} {'agree' if tx == ty else 'DIFFER'}")
    out["secs"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(OUT, f"shell-{typ}.json"), "w"), indent=1, default=str)
    pr(f"{typ} done in {out['secs']} s, checks {'ok' if ok_all else 'FAILED'}")
    return ok_all

def pieces(K, typ, facets, fkeys, fid, removed, keptl, Asso, P, shellvol, rule, us):
    ok = True
    def wgt(k):
        f = facets[k]
        return f["u"] if rule == "equal-speed" else K.inv(f["b"])
    keptid = {fid[k] for k in keptl}
    pcs = {}
    for k in removed:
        r = fid[k]; n, b = facets[k]["n"], facets[k]["b"]
        Q = clip(Asso, vneg(K, n), K.neg(b), ("R", r))
        assert Q is not None
        wr = wgt(k)
        for k2 in removed:
            if k2 == k: continue
            w2 = wgt(k2); n2, b2 = facets[k2]["n"], facets[k2]["b"]
            # w2 (n2.x - b2) - wr (n.x - b) <= 0
            nn = vsub(K, scal(K, w2, n2), scal(K, wr, n)); off = K.sub(K.mul(w2, b2), K.mul(wr, b))
            Q = clip(Q, nn, off, ("W", fid[k2]))
            assert Q is not None, "empty piece"
        pcs[r] = Q
    # ---- global checks
    tot = sum_(K, [volume(Q) for Q in pcs.values()])
    vol_ok = K.isz(K.sub(tot, shellvol))
    # inner ends = the removed faces of P exactly
    inner_ok = all(set(pcs[r].faces[("R", r)][2]) == set(P.faces[("F", r)][2]) for r in pcs)
    # walls match pairwise
    wall_ok = True; walls = 0
    for r, Q in pcs.items():
        for lab, (_, _, cyc) in Q.faces.items():
            if lab[0] == "W":
                o = pcs[lab[1]].faces.get(("W", r))
                if o is None or set(o[2]) != set(cyc): wall_ok = False
                walls += 1
    # outer areas: sum over pieces of outer faces = area(Asso faces) - area(kept P faces), per kept face, exactly
    area_ok = True
    for k in keptl:
        lab = ("F", fid[k]); u = facets[k]["u"]; n = facets[k]["n"]
        nh = scal(K, u, n)
        aA = dot(K, area_vec(Asso, Asso.faces[lab][2]), nh)
        aP = dot(K, area_vec(P, P.faces[lab][2]), nh)
        s = K.zero
        for Q in pcs.values():
            if lab in Q.faces: s = K.add(s, dot(K, area_vec(Q, Q.faces[lab][2]), nh))
        if not K.isz(K.sub(s, K.sub(aA, aP))): area_ok = False
    # ---- per piece classification
    types = {}; tm = []; rows = []
    for r, Q in pcs.items():
        F_in = set(Q.faces[("R", r)][2])
        outer = [lab for lab in Q.faces if lab[0] == "F"]
        wl = [lab for lab in Q.faces if lab[0] == "W"]
        F_out = set(k for lab in outer for k in Q.faces[lab][2])
        Y = [v for v in Q.verts if v not in F_in and v not in F_out]
        meet = F_in & F_out
        # edges
        edge_f = {}
        for lab, (_, _, cyc) in Q.faces.items():
            for i in range(len(cyc)):
                e = frozenset((cyc[i], cyc[(i + 1) % len(cyc)])); edge_f.setdefault(e, []).append(lab)
        closed = all(len(v) == 2 for v in edge_f.values())
        deg = {}
        for e in edge_f:
            for v in e: deg[v] = deg.get(v, 0) + 1
        simple = all(d == 3 for d in deg.values())
        Vn, En, Fn = len(Q.verts), len(edge_f), len(Q.faces)
        euler = Vn - En + Fn == 2
        # inner: neighbours across walls along R's edges; rim edges = R edges to an outer face
        n_sides = len(Q.faces[("R", r)][2])
        in_nb = sorted(l[1] for e, fl in edge_f.items() if ("R", r) in fl for l in fl if l[0] == "W")
        in_rim = sum(1 for e, fl in edge_f.items() if ("R", r) in fl and any(l[0] == "F" for l in fl))
        # outer patch: boundary edges = edges between an outer face and a non-outer face
        ob = [(e, fl) for e, fl in edge_f.items() if sum(1 for l in fl if l[0] == "F") == 1]
        out_nb = sorted({l[1] for e, fl in ob for l in fl if l[0] == "W"})
        out_rim = sum(1 for e, fl in ob if any(l[0] == "R" for l in fl))
        out_edges = len(ob)
        # outer patch connected?
        par = {lab: lab for lab in outer}
        def fd(x):
            while par[x] != x: x = par[x]
            return x
        for e, fl in edge_f.items():
            fo = [l for l in fl if l[0] == "F"]
            if len(fo) == 2: par[fd(fo[0])] = fd(fo[1])
        out_conn = len({fd(l) for l in outer}) == 1 if outer else False
        # outer neighbour count by distinct walls; side count change
        in_set = sorted(set(in_nb)); m_nb = len(out_nb)
        changed = in_set != out_nb
        # every wall meets an end along an edge?
        wall_meets = all(any((lab in fl) and any(l[0] in ("R", "F") for l in fl) for e, fl in edge_f.items()) for lab in wl)
        # tiers
        disjoint = not meet
        k_Y = len(Y)
        n_tot = len(in_set); m_tot = m_nb
        if disjoint and out_conn and wall_meets and closed:
            if len(outer) == 1 and simple: tier = "convex Scutoid Frustum" if k_Y > 0 else "convex frustum"
            else: tier = "Scutoid Frustum (general tier)" if k_Y > 0 else "frustum (general tier)"
        else:
            why = []
            if not disjoint: why.append("ends meet")
            if not out_conn: why.append("outer end not connected")
            if not wall_meets: why.append("a wall meets no end")
            tier = "not a scutoid frustum: " + ", ".join(why)
        law = (k_Y >= abs(n_sides - out_edges)) and ((k_Y - n_sides - out_edges) % 2 == 0)
        law_nb = (k_Y >= abs(n_tot - m_tot)) and ((k_Y - n_tot - m_tot) % 2 == 0)
        row = {"face": r, "face_sides": n_sides, "inner_walls": len(in_nb), "inner_rim_edges": in_rim,
               "outer_faces": len(outer), "outer_edges": out_edges, "outer_walls": m_nb, "outer_rim_edges": out_rim,
               "Y": k_Y, "ends_meet_vertices": len(meet), "simple": simple, "closed": closed, "euler": euler,
               "neighbours_change": changed, "neighbour_count_change": len(in_set) != m_nb,
               "tier": tier, "law_edges": law, "law_neighbours": law_nb,
               "V": Vn, "E": En, "F": Fn, "volume": K.s(volume(Q)), "volume_float": K.val(volume(Q)),
               "verts_float": [[K.val(x) for x in v] for v in Q.verts],
               "faces": {str(lab): [list(Q.verts).index(v) for v in cyc] for lab, (_, _, cyc) in Q.faces.items()}}
        if not (closed and euler): ok = False
        rows.append(row)
        sig = (n_sides, len(in_nb), in_rim, len(outer), out_edges, m_nb, out_rim, k_Y, len(meet), simple, tier)
        tm.append(str(sig))
        types[sig] = types.get(sig, 0) + 1
    ok &= vol_ok and inner_ok and wall_ok and area_ok
    nY = sum(rw["Y"] > 0 for rw in rows); nch = sum(rw["neighbours_change"] for rw in rows)
    ncc = sum(rw["neighbour_count_change"] for rw in rows)
    tiers = {}
    for rw in rows: tiers[rw["tier"]] = tiers.get(rw["tier"], 0) + 1
    pr(f"    rule {rule}: {len(pcs)} pieces; exact checks: volumes sum to vol(assoc)-vol(perm) {vol_ok}; inner ends = removed faces {inner_ok}; "
       f"walls match pairwise {wall_ok} ({walls // 2} walls); outer areas per associahedron face {area_ok}")
    pr(f"      pieces with a Y-corner {nY}; neighbours change inside->outside {nch}; neighbour count changes {ncc}; "
       f"tiers {tiers}")
    for sig, c in sorted(types.items(), key=lambda t: -t[1]):
        n_s, inw, inr, nof, oe, onb, orim, kY, mt, smp, tier = sig
        pr(f"      {c:3d} x  {n_s}-gon face: inner walls {inw}, inner rim edges {inr} | outer: {nof} associahedron face(s), {oe} boundary edges, "
           f"{onb} walls, {orim} rim edges | Y {kY} | ends share {mt} vertices | simple {smp} | {tier}")
    lawc = {"edges": sum(rw["law_edges"] for rw in rows), "neighbours": sum(rw["law_neighbours"] for rw in rows)}
    pr(f"      law Y >= |n-m|, Y = n+m mod 2 holds for {lawc['edges']}/{len(rows)} (m = outer boundary edges, n = face sides) and "
       f"{lawc['neighbours']}/{len(rows)} (n, m = wall neighbours inside, outside)")
    return ok, {"pieces": len(pcs), "checks": {"volume": vol_ok, "inner": inner_ok, "walls": wall_ok, "outer_area": area_ok},
                "with_Y": nY, "neighbours_change": nch, "neighbour_count_change": ncc, "tiers": tiers,
                "types": {str(k): v for k, v in types.items()}, "type_multiset": tm, "law": lawc, "rows": rows}

if __name__ == "__main__":
    allok = True
    todo = sys.argv[1:] or ["A3", "B3", "H3"]
    for i, typ in enumerate(todo):
        allok &= run(typ)
        pr(f"PROGRESS {(i + 1) / len(todo):.2f} {typ}")
    if allok: pr("FINAL ok")
    else: pr("FINAL FAILED")
