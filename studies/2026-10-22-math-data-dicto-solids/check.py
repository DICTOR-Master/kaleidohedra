#!/usr/bin/env python3
# DICTO · dictospheres.com — Created by DICTO. Licence CC BY-SA 4.0.
# Standalone verifier for the DICTO math-data dataset: needs only python3 and sympy.
# It reads solids/*.json and packings/*.json and re-proves every stated property EXACTLY:
# Fields (version 2): each file states its `field`: "Q(sqrt(5))" (a + b*sqrt(5)) or "Q(2**(1/3))" (a + b*2**(1/3) + c*2**(2/3), the
#             Delian bond); every exact string must parse into that field, a, b, c rational. Signs in Q(2**(1/3)) are decided exactly
#             by the norm (see KC).
#   solids:   exact strings parse into the stated field; decimals agree with them; faces are valid index cycles; the surface is a closed
#             2-manifold (each directed edge once, its reverse once, each vertex link one cycle), consistently wound; Euler
#             characteristic 2; every face exactly planar; exact volume (positive, so the winding is outward) equals the stated value;
#             for solids stated convex: every face is a strictly convex polygon wound counter-clockwise seen from outside and every
#             other corner lies strictly inside its plane; f-vector, faces by sides, squared edge lengths and their counts; the full
#             symmetry group (orthogonal maps of the corner set about its centroid that also map the faces to faces) has the stated order, rotation count and inversion,
#             consistent with the stated Schoenflies symbol; every value marked "published" equals the computed one.
#   packings: lattice vectors exact; the cell volume |det| as stated; piece rotations exactly orthogonal; the sum of the piece
#             volumes equals the cell volume exactly; no two pieces (all lattice translates that could meet) overlap: for every pair
#             either their float bounding boxes are apart by more than 1e-9 (coordinates are within 1e-14 of the exact values, so
#             the boxes are apart exactly too) or an exact separating plane is found (separating-axis theorem for convex polyhedra:
#             face normals of either piece and cross products of edge directions). Volume sum = cell volume plus no overlap
#             proves that the translates fill space (a tiling).
#   packings-nonfilling: published packings that do NOT fill space: lattice vectors exact (decimals agree, nonzero cell); cell volume as
#             stated; rotations exactly orthogonal, pieces convex; density = sum of the piece volumes / cell volume, exactly, equal to the
#             stated exact density (the published closed form) and its decimal, and the published percentage equals that decimal at the
#             published precision; no two pieces overlap (same exact separating-plane test as above).
#   unit volume: for every solid, the stated scale is exactly (stated volume)^(-1/3) (checked to 50 digits), the centre is the exact
#             corner centroid, every decimal unit-volume corner is centre + s (corner - centre) (1e-14), and the decimal unit-volume solid
#             has volume 1 (1e-12); the *-unit-volume.off files match.
#   decomposition (version 2): a non-convex solid stated as a convex solid of this dataset minus (dents) or plus (keys) its 8 Tricaps:
#             each Tricap is the #48 one (cyclic orientation: its three base corners are corners of the Unborn at the stated centre, its
#             apex a corner of that Unborn's dodecahedron cube), all of volume (3 - sqrt5)/24; the base corners are corners of the convex
#             solid on one face plane, the apex strictly inside the convex solid (dent) or strictly outside that face (key); the Tricaps
#             are pairwise interior-disjoint (exact separating plane); the corner set is the convex solid's corners plus the 8 apices;
#             every face lies in a face plane of the convex solid or of a Tricap; and the exact volume is the convex volume minus (plus)
#             the 8 Tricap volumes.
#   keyed fill (version 2, `"proof": "decomposition"`): the same lattice and placements as a convex fill of this dataset (which must
#             pass); each keyed piece is its convex piece minus/plus Tricaps; every dent equals exactly one key up to a lattice vector
#             (and vice versa), so every Tricap removed from one piece is added to exactly one other: the keyed pieces fill space too.
#   version 3 (2026-10-27): two more fields: "Q" (rationals; David, Goliath, Ian Dury, Blockhead, Chucky, Fang, Triskelion Tetrahedron)
#             and "Q(t)" with a `field_definition` (Sonsam, Lahdeli): t the only root of an irreducible integer polynomial in a rational
#             isolating interval; checked: irreducible over Q, exactly one root in the interval (Sturm, sympy), decimal of t; signs decided
#             exactly by interval arithmetic on a bisected isolating interval (see RF). Composition (`composition`, non-convex solids of
#             #59): the solid = union of convex dataset pieces (placed exactly) minus / plus Tricaps: pieces orthogonally placed and pairwise
#             interior-disjoint, each Tricap #48's ("tricap") or #48's mirrored in its base plane ("mirrored tricap"), of volume
#             (3 - sqrt5)/24, standing on a face of one piece (dent: apex strictly inside it; key: apex strictly outside that face, key
#             interior-disjoint from every piece and every other Tricap), corners within the pieces' corners and the apices (every apex a
#             corner), every face in a face plane of a piece or Tricap, and volume = pieces - dents + keys, exactly.
#   version 4 (2026-10-28): one more field, "Q(sqrt(3))" (Ganesha), read like Q(sqrt(5)); no new kind of check (Ganesha, Shadow-17 and
#             Humpty Dumpty take the solid checks above).
# Usage: python3 check.py            (prints a PASS/FAIL table; exit code 0 only if everything passes)
import glob, itertools, json, math, os, sys
from fractions import Fraction as Fr
import sympy

HERE = os.path.dirname(os.path.abspath(__file__))


class QF:
    __slots__ = ('a', 'b', 'd')
    def __init__(s, a, b=0, d=5): s.a, s.b, s.d = Fr(a), Fr(b), d
    def _c(s, o): return o if isinstance(o, QF) else QF(o, 0, s.d)
    def __add__(s, o): o = s._c(o); return QF(s.a + o.a, s.b + o.b, s.d)
    __radd__ = __add__
    def __neg__(s): return QF(-s.a, -s.b, s.d)
    def __sub__(s, o): return s + (-s._c(o))
    def __rsub__(s, o): return s._c(o) - s
    def __mul__(s, o): o = s._c(o); return QF(s.a * o.a + s.d * s.b * o.b, s.a * o.b + s.b * o.a, s.d)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = s._c(o); n = o.a * o.a - s.d * o.b * o.b
        if n == 0: raise ZeroDivisionError
        return s * QF(o.a / n, -o.b / n, s.d)
    def sign(s):
        a, b, d = s.a, s.b, s.d
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) if a * a > d * b * b else (1 if b > 0 else -1)
    def __eq__(s, o): o = s._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    # version 7: rounded once, from a 40-digit rational value of the square root (float(a) + float(b)*sqrt(d) loses digits when a and b*sqrt(d) nearly cancel, as in Hamlet and Ophelia)
    def f(s): return float(s.a + s.b * Fr(math.isqrt(s.d * 10 ** 80), 10 ** 40))


class KC:
    """a + b r + c r^2, r = k**(1/3) real (the pure cubic field Q(k**(1/3))); Fractions. Exact sign: the norm
    a^3 + k b^3 + k^2 c^3 - 3k abc equals x |x'|^2 (the other two conjugates are complex conjugates), so it has the sign of x."""
    __slots__ = ('c', 'k')
    def __init__(s, a=0, b=0, c=0, k=2): s.c = (Fr(a), Fr(b), Fr(c)); s.k = k
    @property
    def d(s): return ('cbrt', s.k)
    def _c(s, o): return o if isinstance(o, KC) else KC(o, 0, 0, s.k)
    def __add__(s, o): o = s._c(o); return KC(*(x + y for x, y in zip(s.c, o.c)), k=s.k)
    __radd__ = __add__
    def __neg__(s): return KC(*(-x for x in s.c), k=s.k)
    def __sub__(s, o): return s + (-s._c(o))
    def __rsub__(s, o): return s._c(o) - s
    def __mul__(s, o):
        o = s._c(o); (a, b, c), (x, y, z), k = s.c, o.c, s.k
        return KC(a * x + k * (b * z + c * y), a * y + b * x + k * c * z, a * z + b * y + c * x, k=k)
    __rmul__ = __mul__
    def norm(s): (a, b, c), k = s.c, s.k; return a ** 3 + k * b ** 3 + k * k * c ** 3 - 3 * k * a * b * c
    def __truediv__(s, o):
        o = s._c(o); (a, b, c), k = o.c, o.k; n = o.norm()
        if n == 0: raise ZeroDivisionError
        return s * KC((a * a - k * b * c) / n, (k * c * c - a * b) / n, (b * b - a * c) / n, k=k)
    def sign(s): n = s.norm(); return (n > 0) - (n < 0)
    def __eq__(s, o): o = s._c(o); return s.c == o.c
    def __hash__(s): return hash(s.c)
    def f(s): r = s.k ** (1 / 3); return float(s.c[0]) + float(s.c[1]) * r + float(s.c[2]) * r * r


class AlgField:
    """version 3: Q(t), t the only root of the irreducible integer polynomial P (highest degree first) in the open interval (lo, hi).
    Signs: interval arithmetic (Horner) on a rational isolating interval, bisected by exact signs of P until the value's interval
    excludes 0 (a nonzero element is never 0 at t, P being irreducible)."""
    REG = {}
    def __init__(s, P, lo, hi, name):
        s.P = [Fr(c) for c in P]; s.n = len(P) - 1; s.mon = [c / s.P[0] for c in s.P]; s.lo, s.hi = Fr(lo), Fr(hi); s.name = name
        s.key = ('alg', name, tuple(s.P), Fr(lo), Fr(hi))
    @classmethod
    def get(cls, P, lo, hi, name):
        k = ('alg', name, tuple(Fr(c) for c in P), Fr(lo), Fr(hi))
        if k not in cls.REG: cls.REG[k] = cls(P, lo, hi, name)
        return cls.REG[k]
    def peval(s, x):
        v = Fr(0)
        for c in s.P: v = v * x + c
        return v
    def bisect(s):
        m = (s.lo + s.hi) / 2; v = s.peval(m)
        if v == 0: raise ValueError('rational root: the polynomial is not irreducible')
        if (s.peval(s.lo) < 0) == (v < 0): s.lo = m
        else: s.hi = m
    def approx(s, eps):
        while s.hi - s.lo > eps: s.bisect()
        return (s.lo + s.hi) / 2
    def sign(s, c):
        if all(x == 0 for x in c): return 0
        while True:
            a = b = Fr(0)
            for ck in reversed(c):
                ps = [a * s.lo, a * s.hi, b * s.lo, b * s.hi]; a, b = min(ps) + ck, max(ps) + ck
            if a > 0: return 1
            if b < 0: return -1
            s.bisect()
    def reduce(s, q):
        q = list(q); m = list(reversed(s.mon))
        for deg in range(len(q) - 1, s.n - 1, -1):
            c = q[deg]
            if c != 0:
                for k in range(s.n + 1): q[deg - s.n + k] -= c * m[k]
        q = q[:s.n] + [Fr(0)] * max(0, s.n - len(q))
        return tuple(q[:s.n])


class RF:
    """an element sum c_k t^k (k < n) of an AlgField."""
    __slots__ = ('c', 'F')
    def __init__(s, c, F):
        s.F = F; c = [Fr(x) for x in c]; s.c = tuple(c + [Fr(0)] * (F.n - len(c))) if len(c) <= F.n else F.reduce(c)
    @property
    def d(s): return s.F.key
    def _c(s, o): return o if isinstance(o, RF) else RF([o], s.F)
    def __add__(s, o): o = s._c(o); return RF([x + y for x, y in zip(s.c, o.c)], s.F)
    __radd__ = __add__
    def __neg__(s): return RF([-x for x in s.c], s.F)
    def __sub__(s, o): return s + (-s._c(o))
    def __rsub__(s, o): return s._c(o) - s
    def __mul__(s, o):
        o = s._c(o); q = [Fr(0)] * (2 * s.F.n - 1)
        for i, x in enumerate(s.c):
            if x != 0:
                for j, y in enumerate(o.c): q[i + j] += x * y
        return RF(s.F.reduce(q), s.F)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = s._c(o); n = s.F.n
        if all(x == 0 for x in o.c): raise ZeroDivisionError
        cols = []; e = o; t = RF([0, 1], s.F)
        for j in range(n): cols.append(list(e.c)); e = e * t
        M = [[cols[j][i] for j in range(n)] + [Fr(1 if i == 0 else 0)] for i in range(n)]
        for c in range(n):
            piv = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[piv] = M[piv], M[c]
            pv = M[c][c]; M[c] = [x / pv for x in M[c]]
            for r in range(n):
                if r != c and M[r][c] != 0:
                    f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
        return s * RF([M[i][n] for i in range(n)], s.F)
    def sign(s): return s.F.sign(s.c)
    def __eq__(s, o): o = s._c(o); return s.c == o.c
    def __hash__(s): return hash(s.c)
    def at(s, x): return sum((q * x ** i for i, q in enumerate(s.c)), Fr(0))
    def f(s): return float(s.at(s.F.approx(Fr(1, 10 ** 22))))


def fz(d, a=0):
    """the constant a in the field d (int: Q(sqrt d), 1: Q; ('cbrt', k): Q(k**(1/3)); ('alg', ...): Q(t), version 3)."""
    if isinstance(d, tuple):
        if d[0] == 'alg': return RF([a], AlgField.get(d[2], d[3], d[4], d[1]))
        return KC(a, 0, 0, d[1])
    return QF(a, 0, d)


def mpx(x):
    import mpmath
    if isinstance(x, RF):
        v = x.at(x.F.approx(Fr(1, 10 ** 70))); return mpmath.mpf(v.numerator) / v.denominator
    if isinstance(x, KC):
        r = mpmath.cbrt(x.k); return sum((mpmath.mpf(q.numerator) / q.denominator * r ** i for i, q in enumerate(x.c)), mpmath.mpf(0))
    return mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(x.d)


def parse(txt, d):
    """exact string -> a field element, refusing anything outside the field d."""
    if isinstance(d, tuple) and d[0] == 'alg':
        t = sympy.Symbol(d[1]); e = sympy.expand(sympy.sympify(txt, locals={d[1]: t})); F = AlgField.get(d[2], d[3], d[4], d[1])
        if e.free_symbols - {t}: raise ValueError(f'{txt} is not in Q({d[1]})')
        cs = sympy.Poly(e, t).all_coeffs()
        if not all(c.is_Rational for c in cs): raise ValueError(f'{txt} is not in Q({d[1]})')
        return RF([Fr(int(c.p), int(c.q)) for c in reversed(cs)], F)
    if isinstance(d, tuple):
        k = d[1]; e = sympy.expand(sympy.sympify(txt)); cs = [Fr(0)] * 3
        basis = {sympy.Integer(1): 0, sympy.Integer(k) ** sympy.Rational(1, 3): 1, sympy.Integer(k) ** sympy.Rational(2, 3): 2}
        for t, c in e.as_coefficients_dict().items():
            if not c.is_Rational or t not in basis: raise ValueError(f'{txt} is not in Q({k}**(1/3))')
            cs[basis[t]] += Fr(int(c.p), int(c.q))
        return KC(*cs, k=k)
    e = sympy.expand(sympy.sympify(txt))
    a = Fr(0); b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        if not c.is_Rational: raise ValueError(txt)
        c = Fr(int(c.p), int(c.q))
        if t == 1: a += c
        elif d > 1 and t == sympy.sqrt(d): b += c
        else: raise ValueError(f'{txt} is not in Q(sqrt({d}))')
    return QF(a, b, d)


dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
sub = lambda u, v: (u[0] - v[0], u[1] - v[1], u[2] - v[2])
cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
det3 = lambda a, b, c: dot(a, cross(b, c))
RESULTS = []


def rec(item, test, ok, note=''):
    RESULTS.append((item, test, bool(ok), note))
    return ok


def field_of(doc):
    f = doc['field']
    if 'field_definition' in doc:                      # version 3: Q(t)
        fd = doc['field_definition']; t = sympy.Symbol(fd['generator'])
        P = [Fr(int(c.p), int(c.q)) for c in sympy.Poly(sympy.sympify(fd['minimal_polynomial'], locals={fd['generator']: t}), t).all_coeffs()]
        return ('alg', fd['generator'], tuple(P), Fr(fd['isolating_interval'][0]), Fr(fd['isolating_interval'][1]))
    if f.endswith('**(1/3))'): return ('cbrt', int(f[2:f.index('**')]))
    return 1 if f == 'Q' else int(f[f.index('sqrt(') + 5:f.index(')')])


def load_vertices(doc, d):
    V = [tuple(parse(x, d) for x in v['exact']) for v in doc['vertices']]
    dec_ok = all(abs(float(s) - x.f()) < 1e-14 for v, w in zip(doc['vertices'], V) for s, x in zip(v['decimal'], w))
    return V, dec_ok


def newell(V, f):
    n = (fz(V[0][0].d),) * 3
    for i in range(len(f)):
        a, b = V[f[i]], V[f[(i + 1) % len(f)]]; c = cross(a, b); n = (n[0] + c[0], n[1] + c[1], n[2] + c[2])
    return n


def volume(V, F):
    s = fz(V[0][0].d)
    for f in F:
        for k in range(1, len(f) - 1): s = s + det3(V[f[0]], V[f[k]], V[f[k + 1]])
    return s / 6


def symmetry(V, F):
    d = V[0][0].d; n = len(V); Z = fz(d)
    c = tuple(sum((v[k] for v in V), Z) / n for k in range(3)); W = [sub(v, c) for v in V]; S = set(W)
    norms = [dot(w, w) for w in W]; cnt = {}
    for x in norms: cnt[x] = cnt.get(x, 0) + 1
    order = sorted(range(n), key=lambda i: (cnt[norms[i]], norms[i].f()))
    a = order[0]
    fl = [[x.f() for x in w] for w in W]
    dist = lambda i, j: math.dist(fl[i], fl[j])
    b = min((i for i in order if any(x.sign() for x in cross(W[a], W[i]))), key=lambda i: (cnt[norms[i]], dist(i, a)))
    ab = cross(W[a], W[b])
    cc = min((i for i in order if dot(ab, W[i]).sign()), key=lambda i: (cnt[norms[i]], dist(i, a)))
    A = [W[a], W[b], W[cc]]; G = [[dot(A[i], A[j]) for j in range(3)] for i in range(3)]; FS = {frozenset(f) for f in F}
    Dt = det3(*A); adj = [cross(A[1], A[2]), cross(A[2], A[0]), cross(A[0], A[1])]
    pick = lambda i, cons: [j for j in range(n) if norms[j] == G[i][i] and all(dot(W[j], W[k]) == G[i][m] for m, k in cons)]
    out = []
    for ja in pick(0, []):
        for jb in pick(1, [(0, ja)]):
            for jc in pick(2, [(0, ja), (1, jb)]):
                B = [W[ja], W[jb], W[jc]]
                M = [[sum((B[k][i] * adj[k][j] for k in range(3)), Z) / Dt for j in range(3)] for i in range(3)]
                if all(tuple(dot(M[i], w) for i in range(3)) in S for w in W):
                    img = {w: j for j, w in enumerate(W)}; perm = [img[tuple(dot(M[i], w) for i in range(3))] for w in W]
                    if all(frozenset(perm[i] for i in f) in FS for f in F): out.append(M)
    detsign = [det3(*M).sign() for M in out]
    inv = any(all(M[i][j] == (fz(d, -1) if i == j else Z) for i in range(3) for j in range(3)) for M in out)
    return len(out), sum(1 for s in detsign if s > 0), inv


# Schoenflies symbol -> (order, rotations, contains inversion); 'n' symbols handled generically
def schoenflies(sym):
    fixed = {'Ih': (120, 60, True), 'I': (60, 60, False), 'Oh': (48, 24, True), 'O': (24, 24, False), 'Th': (24, 12, True),
             'Td': (24, 12, False), 'T': (12, 12, False), 'C1': (1, 1, False), 'Ci': (2, 1, True), 'Cs': (2, 1, False)}
    if sym in fixed: return fixed[sym]
    import re
    m = re.fullmatch(r'([CDS])(\d+)([hvd]?)', sym); L, k, t = m.group(1), int(m.group(2)), m.group(3)
    if L == 'C' and t == '': return (k, k, False)
    if L == 'C' and t == 'v': return (2 * k, k, False)
    if L == 'C' and t == 'h': return (2 * k, k, k % 2 == 0)
    if L == 'S': return (k, k // 2, (k // 2) % 2 == 1)
    if L == 'D' and t == '': return (2 * k, 2 * k, False)
    if L == 'D' and t == 'h': return (4 * k, 2 * k, k % 2 == 0)
    if L == 'D' and t == 'd': return (4 * k, 2 * k, k % 2 == 1)
    raise ValueError(sym)


def check_solid(path):
    doc = json.load(open(path)); slug = os.path.basename(path)[:-5]; d = field_of(doc)
    if 'field_definition' in doc:                      # version 3: the field Q(t) itself
        fd = doc['field_definition']; t = sympy.Symbol(fd['generator']); P = sympy.Poly(sympy.sympify(fd['minimal_polynomial'], locals={fd['generator']: t}), t)
        lo, hi = (sympy.Rational(x) for x in fd['isolating_interval']); F0 = AlgField.get(d[2], d[3], d[4], d[1])
        rec(slug, f"field Q({fd['generator']}): {fd['minimal_polynomial']} irreducible over Q, exactly one root in ({fd['isolating_interval'][0]}, "
                  f"{fd['isolating_interval'][1]}), its decimal as stated (1e-25)", P.is_irreducible and P.count_roots(lo, hi) == 1 and
            P.eval(lo) * P.eval(hi) < 0 and abs(F0.approx(Fr(1, 10 ** 40)) - Fr(fd['decimal'])) < Fr(1, 10 ** 25), fd['decimal'])
    V, dec_ok = load_vertices(doc, d); F = doc['faces']; nV = len(V)
    rec(slug, 'exact strings parse; decimals agree (1e-14)', dec_ok)
    rec(slug, 'corners distinct', len(set(V)) == nV)
    valid = all(len(f) >= 3 and len(set(f)) == len(f) and all(0 <= i < nV for i in f) for f in F)
    rec(slug, 'faces are valid index cycles', valid)
    E = {}
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]): E[(a, b)] = E.get((a, b), 0) + 1
    closed = all(m == 1 for m in E.values()) and all((b, a) in E for (a, b) in E)
    # vertex links: faces round each vertex form one cycle
    link_ok = True
    for v in range(nV):
        nxt = {}
        for f in F:
            if v in f:
                k = f.index(v); nxt[f[k - 1]] = f[(k + 1) % len(f)]
        if not nxt: link_ok = False; break
        s = next(iter(nxt)); cur = s; steps = 0
        while True:
            cur = nxt.get(cur); steps += 1
            if cur is None or steps > len(nxt): link_ok = False; break
            if cur == s: break
        if steps != len(nxt): link_ok = False
    rec(slug, 'closed 2-manifold, consistently wound (each edge once each way; vertex links single cycles)', closed and link_ok)
    nE = len(E) // 2
    rec(slug, 'Euler characteristic V - E + F = 2', nV - nE + len(F) == 2, f'{nV} - {nE} + {len(F)}')
    planar = True; normals = []
    for f in F:
        n = newell(V, f); normals.append(n)
        if not any(x.sign() for x in n) or any(dot(n, sub(V[i], V[f[0]])).sign() for i in f): planar = False
    rec(slug, 'every face exactly planar', planar)
    vol = volume(V, F)
    rec(slug, 'exact volume positive (outward winding) and equal to stated', vol.sign() > 0 and vol == parse(doc['volume']['exact'], d), doc['volume']['exact'])
    rec(slug, 'stated volume decimal agrees', abs(float(doc['volume']['decimal']) - vol.f()) < 1e-12)
    if doc.get('convex'):
        cv = True
        for f, n in zip(F, normals):
            fs = set(f)
            for i in range(nV):
                sg = dot(n, sub(V[i], V[f[0]])).sign()
                if (i in fs and sg != 0) or (i not in fs and sg >= 0): cv = False
            for k in range(len(f)):
                a, b, c = V[f[k]], V[f[(k + 1) % len(f)]], V[f[(k + 2) % len(f)]]
                if dot(cross(sub(b, a), sub(c, b)), n).sign() <= 0: cv = False
        rec(slug, 'convex: faces strictly convex, CCW from outside, all other corners strictly inside', cv)
    fv = doc['f_vector']
    rec(slug, 'f-vector as stated', (fv['vertices'], fv['edges'], fv['faces']) == (nV, nE, len(F)))
    fk = {}
    for f in F: fk[str(len(f))] = fk.get(str(len(f)), 0) + 1
    rec(slug, 'faces by number of sides as stated', fk == doc['faces_by_sides'])
    edges = {tuple(sorted(e)) for e in E}
    el = {}
    for a, b in edges:
        x = dot(sub(V[a], V[b]), sub(V[a], V[b])); el[x] = el.get(x, 0) + 1
    stated = {parse(e['exact'], d): e['count'] for e in doc['squared_edge_lengths']}
    rec(slug, 'squared edge lengths and counts as stated', el == stated)
    order, rot, inv = symmetry(V, F); sy = doc['symmetry']
    rec(slug, f"symmetry group order {order}, rotations {rot}, inversion {inv} as stated", (order, rot, inv) == (sy['order'], sy['rotations'], sy['contains_inversion']))
    rec(slug, f"Schoenflies {sy['schoenflies']} consistent with order/rotations/inversion", schoenflies(sy['schoenflies']) == (order, rot, inv))
    pub = doc.get('published_values', {})
    if pub:
        ok = True
        for k, v in pub.items():
            if k == 'volume': ok &= parse(v, d) == vol
            elif k == 'f_vector': ok &= tuple(v) == (nV, nE, len(F))
            elif k == 'faces_by_sides': ok &= {str(a): b for a, b in v.items()} == fk
            elif k == 'squared_edge_lengths': ok &= {parse(x, d) for x in v} == set(el)
            elif k == 'symmetry_order': ok &= v == order
        rec(slug, 'agrees with the published values recorded (' + ', '.join(pub) + ')', ok)
    if 'unit_volume' in doc: check_unit_volume(slug, doc, V, F, vol, d)
    return V, F, vol, d


def check_unit_volume(slug, doc, V, F, vol, d):
    import mpmath
    mpmath.mp.dps = 60
    uv = doc['unit_volume']; Z = fz(d)
    e = sympy.sympify(uv['scale_exact']); Vs = sympy.sympify(doc['volume']['exact'])
    if isinstance(d, tuple) and d[0] == 'alg':          # version 3: put in the value of t (70 digits)
        tv = sympy.Rational(fz(d).F.approx(Fr(1, 10 ** 70))); ts = sympy.Symbol(d[1]); e = e.subs(ts, tv); Vs = Vs.subs(ts, tv)
    rec(slug, 'unit volume: scale_exact = (stated volume)^(-1/3) (50 digits)', vol == parse(doc['volume']['exact'], d) and
        e.free_symbols == set() and abs(sympy.N(e ** -3 - Vs, 60)) < sympy.Float('1e-50'), uv['scale_exact'])
    s = mpmath.mpf(str(sympy.N(e, 60)))
    rec(slug, 'unit volume: scale decimal agrees (1e-14)', abs(float(uv['scale_decimal']) - float(s)) < 1e-14)
    c = tuple(sum((v[k] for v in V), Z) / len(V) for k in range(3))
    rec(slug, 'unit volume: centre = exact corner centroid; decimals agree', tuple(parse(x, d) for x in uv['centre']['exact']) == c and
        all(abs(float(a) - x.f()) < 1e-14 for a, x in zip(uv['centre']['decimal'], c)))
    mq = mpx
    W = [[float(x) for x in w] for w in uv['vertices_decimal']]
    rec(slug, 'unit volume: every corner = centre + s (corner - centre) (1e-14)', len(W) == len(V) and
        all(abs(W[i][k] - float(mq(c[k]) + s * (mq(V[i][k]) - mq(c[k])))) < 1e-14 for i in range(len(V)) for k in range(3)))
    vu = 0.0
    for f in F:
        for k in range(1, len(f) - 1):
            a, b, cc = W[f[0]], W[f[k]], W[f[k + 1]]
            vu += a[0] * (b[1] * cc[2] - b[2] * cc[1]) + a[1] * (b[2] * cc[0] - b[0] * cc[2]) + a[2] * (b[0] * cc[1] - b[1] * cc[0])
    rec(slug, 'unit volume: the decimal unit-volume solid has volume 1 (1e-12)', abs(vu / 6 - 1) < 1e-12, f'{vu / 6:.15f}')


def emax(L):
    m = L[0]
    for x in L[1:]:
        if (x - m).sign() > 0: m = x
    return m


def emin(L): return -emax([-x for x in L])


def sat_disjoint(A, B):
    """A, B: (vertices, faces) of convex polyhedra, exact. True if an exact separating plane exists (interiors disjoint)."""
    (VA, FA), (VB, FB) = A, B
    axes = [newell(VA, f) for f in FA] + [newell(VB, f) for f in FB]
    eA = {sub(VA[f[(k + 1) % len(f)]], VA[f[k]]) for f in FA for k in range(len(f))}
    eB = {sub(VB[f[(k + 1) % len(f)]], VB[f[k]]) for f in FB for k in range(len(f))}
    def gap(n):
        nf = [x.f() for x in n]; a = [sum(p[i].f() * nf[i] for i in range(3)) for p in VA]; b = [sum(p[i].f() * nf[i] for i in range(3)) for p in VB]
        return max(min(b) - max(a), min(a) - max(b)) / (math.sqrt(sum(x * x for x in nf)) or 1)
    cand = axes + [cross(u, v) for u in eA for v in eB]
    cand = [n for n in cand if any(x.sign() for x in n)]
    cand.sort(key=lambda n: -gap(n))
    for n in cand:
        pa = [dot(n, p) for p in VA]; pb = [dot(n, p) for p in VB]
        if (emax(pa) - emin(pb)).sign() <= 0 or (emax(pb) - emin(pa)).sign() <= 0: return True
    return False


def check_packing(path, solids, filling=True):
    doc = json.load(open(path)); slug = os.path.basename(path)[:-5]; d = field_of(doc)
    L = [tuple(parse(x, d) for x in v['exact']) for v in doc['lattice_vectors']]
    if not filling:
        rec(slug, 'kind: "packing, not a fill"', doc.get('kind') == 'packing, not a fill')
        rec(slug, 'lattice vectors exact; decimals agree (1e-14); cell nonzero', det3(*L).sign() != 0 and
            all(abs(float(a) - x.f()) < 1e-14 for v, w in zip(doc['lattice_vectors'], L) for a, x in zip(v['decimal'], w)))
    cv = det3(*L); cv = cv if cv.sign() > 0 else -cv
    rec(slug, 'cell volume |det(lattice)| as stated', cv.sign() > 0 and cv == parse(doc['cell_volume']['exact'], d), doc['cell_volume']['exact'])
    pieces = []; vsum = fz(d); orth = True
    for p in doc['pieces']:
        V, F, vol, _ = solids[p['solid']]
        R = [[parse(x, d) for x in r] for r in p['rotation']]; t = tuple(parse(x, d) for x in p['translation'])
        RRt = [[sum((R[i][k] * R[j][k] for k in range(3)), fz(d)) for j in range(3)] for i in range(3)]
        orth &= all(RRt[i][j] == (1 if i == j else 0) for i in range(3) for j in range(3))
        sgn = det3(*[tuple(R[i][k] for i in range(3)) for k in range(3)]).sign()
        W = [tuple(sum((R[i][k] * v[k] for k in range(3)), fz(d)) + t[i] for i in range(3)) for v in V]
        FF = F if sgn > 0 else [f[::-1] for f in F]
        if not json.load(open(os.path.join(HERE, 'solids', p['solid'] + '.json'))).get('convex'): orth = False
        pieces.append((W, FF)); vsum = vsum + vol
    rec(slug, 'piece rotations exactly orthogonal; pieces convex', orth)
    if filling:
        rec(slug, 'sum of piece volumes = cell volume (exact)', vsum == cv)
    else:
        dens = vsum / cv; st = doc['density']
        rec(slug, 'density = sum of piece volumes / cell volume, exactly the stated (published) closed form', dens == parse(st['exact'], d), st['exact'])
        rec(slug, 'stated density decimal agrees (1e-14); below 1 (not a fill)', abs(float(st['decimal']) - dens.f()) < 1e-14 and (dens - 1).sign() < 0)
        pp = st['published_percent']; places = len(pp.split('.')[1]) if '.' in pp else 0
        rec(slug, f'published percentage {pp}% = the exact density rounded to {places} places', f'{dens.f() * 100:.{places}f}' == pp, f'{dens.f() * 100:.6f}%')
    ok, nexact = no_overlaps(L, pieces, d)
    rec(slug, f'no overlaps: {nexact} nearby piece pairs each separated by an exact plane', ok)
    if filling: rec(slug, 'volume sum = cell volume and no overlaps => the pieces tile space', ok and vsum == cv)


def no_overlaps(L, pieces, d):
    # all translates that could meet: lattice combinations with |t| <= 2 * max radius (+ margin)
    Lf = [[x.f() for x in v] for v in L]
    rad = max(max(math.dist([x.f() for x in w], [0, 0, 0]) for w in W) for W, _ in pieces)
    G = [[sum(Lf[i][k] * Lf[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
    # bound on coefficients: |c_i| <= (2 rad + 1e-6) * sqrt((G^-1)_ii)
    Gs = sympy.Matrix(G).inv(); K = [int(math.ceil((2 * rad + 1e-6) * math.sqrt(float(Gs[i, i])))) for i in range(3)]
    ok = True; nexact = 0
    for c in itertools.product(*[range(-k, k + 1) for k in K]):
        t = tuple(sum((L[i][k] * c[i] for i in range(3)), fz(d)) for k in range(3))
        for i, (WA, FA) in enumerate(pieces):
            for j, (WB, FB) in enumerate(pieces):
                if c == (0, 0, 0) and j <= i: continue
                WBt = [tuple(w[k] + t[k] for k in range(3)) for w in WB]
                fa = [[x.f() for x in w] for w in WA]; fb = [[x.f() for x in w] for w in WBt]
                if any(min(q[k] for q in fb) - max(p[k] for p in fa) > 1e-9 or min(p[k] for p in fa) - max(q[k] for q in fb) > 1e-9 for k in range(3)): continue
                nexact += 1
                if not sat_disjoint((WA, FA), (WBt, FB)): ok = False
    return ok, nexact


def tet_faces(T):
    """the 4 faces of a tetrahedron (corner list), wound outward."""
    F = [[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]
    return F if det3(sub(T[1], T[0]), sub(T[2], T[0]), sub(T[3], T[0])).sign() < 0 else [f[::-1] for f in F]


def tet_volume(T):
    v = det3(sub(T[1], T[0]), sub(T[2], T[0]), sub(T[3], T[0])) / 6
    return v if v.sign() > 0 else -v


def check_decomposition(slug, doc, solids):
    """version 2: a non-convex solid = a convex solid of this dataset minus (dents) or plus (keys) its 8 #48 Tricaps."""
    dc = doc['decomposition']; d = field_of(doc); V, F, vol, _ = solids[slug]
    VB, FB, vb, _ = solids[dc['base_solid']]
    bdoc = json.load(open(os.path.join(HERE, 'solids', dc['base_solid'] + '.json')))
    rec(slug, f"decomposition: base {dc['base_solid']} is a convex solid of this dataset, operation '{dc['operation']}'", bdoc.get('convex') is True and dc['operation'] in ('minus', 'plus'))
    caps = []; orient = True
    PH = QF(Fr(1, 2), Fr(1, 2), 5); H = PH / 2; IH = (PH - 1) / 2; Z = fz(d); HALF = fz(d, Fr(1, 2))
    for c in dc['tricaps']:
        u = tuple(parse(x, d) for x in c['unborn_centre']); a = tuple(parse(x, d) for x in c['apex']); B = [tuple(parse(x, d) for x in b) for b in c['base']]
        caps.append([a] + B)
        # the Unborn at u: u + cyclic permutations of (+-phi/2, +-1/(2 phi), 0) (#48); its dodecahedron's cube: u + (+-1/2, +-1/2, +-1/2)
        unb = {tuple(u[k] + p[k] for k in range(3)) for s1 in (1, -1) for s2 in (1, -1) for p in
               [(s1 * H, s2 * IH, Z), (Z, s1 * H, s2 * IH), (s2 * IH, Z, s1 * H)]}
        sv = [2 * (a[k] - u[k]) for k in range(3)]
        if not all(x == 1 or x == -1 for x in sv): orient = False; continue
        # #48 Tricap of the Unborn at u towards s: apex u + s/2, base u + (s_x phi/2, s_y/(2 phi), 0), u + (0, s_y phi/2, s_z/(2 phi)), u + (s_x/(2 phi), 0, s_z phi/2)
        want = {tuple(u[k] + w[k] for k in range(3)) for w in [(sv[0] * H, sv[1] * IH, Z), (Z, sv[1] * H, sv[2] * IH), (sv[0] * IH, Z, sv[2] * H)]}
        if not (set(B) <= unb and set(B) == want): orient = False
    rec(slug, "decomposition: every Tricap is #48's (cyclic orientation): its 3 base corners are corners of the Unborn at the stated centre "
              "(cyclic permutations of (+-phi/2, +-1/(2 phi), 0)) and its apex a corner of that Unborn's dodecahedron cube", orient and len(caps) == 8)
    tv = parse(dc['tricap_volume'], d)
    rec(slug, 'decomposition: 8 Tricaps, each of volume exactly the stated (3 - sqrt5)/24', len(caps) == 8 and tv == fz(d, Fr(1, 8)) + QF(0, Fr(-1, 24), 5) and all(tet_volume(T) == tv for T in caps))
    planes = [(newell(VB, f), dot(newell(VB, f), VB[f[0]])) for f in FB]; VBs = set(VB); place = True
    for T in caps:
        a, B = T[0], T[1:]
        hit = [(n, h) for n, h in planes if all(dot(n, b) == h for b in B)]
        if not (set(B) <= VBs and len(hit) == 1): place = False; continue
        n, h = hit[0]
        if dc['operation'] == 'minus': place &= all((dot(m, a) - g).sign() < 0 for m, g in planes)
        else: place &= (dot(n, a) - h).sign() > 0
    rec(slug, 'decomposition: each Tricap stands on one face of the convex base (base corners = base corners), apex ' +
        ('strictly inside the base (a dent; the Tricap lies in the base)' if dc['operation'] == 'minus' else 'strictly outside that face (a key)'), place)
    pieces = [(T, tet_faces(T)) for T in caps]
    rec(slug, 'decomposition: the 8 Tricaps are pairwise interior-disjoint (exact separating planes)', all(sat_disjoint(pieces[i], pieces[j]) for i in range(8) for j in range(i + 1, 8)))
    rec(slug, 'decomposition: corners = the base corners and the 8 apices', set(V) == VBs | {T[0] for T in caps} and len(V) == len(VB) + 8)
    allp = planes + [(newell(T, f), dot(newell(T, f), T[f[0]])) for T, FT in pieces for f in FT]
    def onplane(f):
        n = newell(V, f)
        return any(all(x.sign() == 0 for x in cross(n, m)) and dot(m, V[f[0]]) == h for m, h in allp)
    rec(slug, 'decomposition: every face lies in a face plane of the base or of a Tricap', all(onplane(f) for f in F))
    sgn = -1 if dc['operation'] == 'minus' else 1
    rec(slug, f"decomposition: exact volume = base volume {'-' if sgn < 0 else '+'} 8 Tricaps", vol == vb + sgn * 8 * tv, f"{doc['volume']['exact']}")
    return caps


def check_composition(slug, doc, solids):
    """version 3: a non-convex solid = the union of convex dataset pieces (interior-disjoint, placed by x -> R x + t), minus the
    Tricaps in `minus` (dents), plus those in `plus` (keys); each Tricap is #48's ("tricap") or #48's mirrored in its base plane
    ("mirrored tricap")."""
    cp = doc['composition']; d = field_of(doc); V, F, vol, _ = solids[slug]
    PH = QF(Fr(1, 2), Fr(1, 2), 5); H = PH / 2; IH = (PH - 1) / 2; Z = fz(d)
    P = []; orth = True; vp = Z
    for p in cp['pieces']:
        bdoc = json.load(open(os.path.join(HERE, 'solids', p['solid'] + '.json'))); VB, FB, vb, _ = solids[p['solid']]
        R = [[parse(x, d) for x in r] for r in p['rotation']]; t = tuple(parse(x, d) for x in p['translation'])
        orth &= bdoc.get('convex') is True and all(sum((R[i][k] * R[j][k] for k in range(3)), Z) == (1 if i == j else 0) for i in range(3) for j in range(3))
        sg = det3(*[tuple(R[i][k] for i in range(3)) for k in range(3)]).sign()
        W = [tuple(sum((R[i][k] * v[k] for k in range(3)), Z) + t[i] for i in range(3)) for v in VB]
        FF = FB if sg > 0 else [f[::-1] for f in FB]
        P.append((W, FF, [(newell(W, f), dot(newell(W, f), W[f[0]])) for f in FF])); vp = vp + vb
    rec(slug, f"composition: {len(P)} convex pieces of this dataset ({', '.join(sorted({p['solid'] for p in cp['pieces']}))}), placed by exact orthogonal maps", orth)
    rec(slug, 'composition: the pieces are pairwise interior-disjoint (exact separating planes)', all(sat_disjoint(P[i][:2], P[j][:2]) for i in range(len(P)) for j in range(i + 1, len(P))))
    tv = parse(cp['tricap_volume'], d)
    tets = {'minus': [], 'plus': []}; kind_ok = True
    for side in ('minus', 'plus'):
        for c in cp[side]:
            u = tuple(parse(x, d) for x in c['unborn_centre']); a = tuple(parse(x, d) for x in c['apex']); B = [tuple(parse(x, d) for x in b) for b in c['base']]
            unb = {tuple(u[k] + w[k] for k in range(3)) for s1 in (1, -1) for s2 in (1, -1) for w in [(s1 * H, s2 * IH, Z), (Z, s1 * H, s2 * IH), (s2 * IH, Z, s1 * H)]}
            ok = False
            for sv in itertools.product((1, -1), repeat=3):   # the #48 Tricap of the Unborn at u towards sv: apex u + sv/2, base as in check_decomposition
                want = {tuple(u[k] + w[k] for k in range(3)) for w in [(sv[0] * H, sv[1] * IH, Z), (Z, sv[1] * H, sv[2] * IH), (sv[0] * IH, Z, sv[2] * H)]}
                if set(B) != want or not want <= unb: continue
                a0 = tuple(u[k] + fz(d, Fr(sv[k], 2)) for k in range(3))
                if c['kind'] == 'tricap': ok = a == a0
                elif c['kind'] == 'mirrored tricap':
                    n = cross(sub(B[1], B[0]), sub(B[2], B[0])); kk = 2 * dot(n, sub(a0, B[0])) / dot(n, n)
                    ok = a == tuple(a0[k] - kk * n[k] for k in range(3))
            kind_ok &= ok and tet_volume([a] + B) == tv
            tets[side].append([a] + B)
    nT = len(tets['minus']) + len(tets['plus'])
    rec(slug, f"composition: {len(tets['minus'])} dents and {len(tets['plus'])} keys, each #48's Tricap of the stated Unborn (cyclic orientation) or "
              "its mirror image in its base plane, as stated, of volume exactly (3 - sqrt5)/24", kind_ok and tv == fz(d, Fr(1, 8)) + QF(0, Fr(-1, 24), 5))
    place = True
    for side in ('minus', 'plus'):
        for T in tets[side]:
            a, B = T[0], T[1:]; hits = [(W, pl, n, h) for W, FF, pl in P for n, h in pl if set(B) <= set(W) and all(dot(n, b) == h for b in B)]
            if len(hits) != 1: place = False; continue
            W, pl, n, h = hits[0]
            place &= all((dot(m, a) - g).sign() < 0 for m, g in pl) if side == 'minus' else (dot(n, a) - h).sign() > 0
    rec(slug, 'composition: each Tricap stands on one face of one piece (its base corners are corners of that piece); a dent\'s apex strictly '
              'inside that piece, a key\'s apex strictly outside that face', place)
    TP = [(T, tet_faces(T)) for T in tets['minus'] + tets['plus']]; nm = len(tets['minus'])
    dis = all(sat_disjoint(TP[i], TP[j]) for i in range(nT) for j in range(i + 1, nT))
    dis &= all(sat_disjoint(TP[i], P[k][:2]) for i in range(nm, nT) for k in range(len(P)))
    rec(slug, 'composition: the Tricaps are pairwise interior-disjoint, and every key is interior-disjoint from every piece (exact separating planes)', dis)
    PV = {v for W, FF, pl in P for v in W}; AP = {T[0] for T in tets['minus'] + tets['plus']}
    rec(slug, "composition: every corner is a piece's corner or a Tricap apex, and every apex is a corner", set(V) <= PV | AP and AP <= set(V))
    allp = [x for W, FF, pl in P for x in pl] + [(newell(T, f), dot(newell(T, f), T[f[0]])) for T, FT in TP for f in FT]
    def onplane(f):
        n = newell(V, f)
        return any(all(x.sign() == 0 for x in cross(n, m)) and dot(m, V[f[0]]) == h for m, h in allp)
    rec(slug, 'composition: every face lies in a face plane of a piece or of a Tricap', all(onplane(f) for f in F))
    rec(slug, f"composition: exact volume = pieces - {len(tets['minus'])} + {len(tets['plus'])} Tricaps", vol == vp - nm * tv + len(tets['plus']) * tv, doc['volume']['exact'])


def check_keyed_packing(path, solids):
    """version 2: a fill by non-convex keyed pieces, proved from a convex fill of this dataset and the Tricap decompositions."""
    doc = json.load(open(path)); slug = os.path.basename(path)[:-5]; d = field_of(doc)
    base = json.load(open(os.path.join(HERE, 'packings', doc['base_packing'] + '.json')))
    base_ok = [ok for it, t, ok, note in RESULTS if it == doc['base_packing']]
    rec(slug, f"base fill {doc['base_packing']} passed all its checks (a tiling by convex pieces)", base_ok and all(base_ok))
    L = [tuple(parse(x, d) for x in v['exact']) for v in doc['lattice_vectors']]
    LB = [tuple(parse(x, d) for x in v['exact']) for v in base['lattice_vectors']]
    cv = det3(*L); cv = cv if cv.sign() > 0 else -cv
    rec(slug, 'same lattice as the base fill; cell volume as stated', L == LB and cv == parse(doc['cell_volume']['exact'], d))
    same = len(doc['pieces']) == len(base['pieces']); vsum = fz(d); dents = []; keys = []; orth = True
    for i, p in enumerate(doc['pieces']):
        sdoc = json.load(open(os.path.join(HERE, 'solids', p['solid'] + '.json'))); dc = sdoc['decomposition']; bp = base['pieces'][i]
        same &= dc['base_solid'] == bp['solid'] and p['rotation'] == bp['rotation'] and p['translation'] == bp['translation']
        R = [[parse(x, d) for x in r] for r in p['rotation']]; t = tuple(parse(x, d) for x in p['translation'])
        orth &= all(sum((R[a][k] * R[b][k] for k in range(3)), fz(d)) == (1 if a == b else 0) for a in range(3) for b in range(3))
        vsum = vsum + solids[p['solid']][2]
        for c in dc['tricaps']:
            T = [tuple(parse(x, d) for x in c['apex'])] + [tuple(parse(x, d) for x in b) for b in c['base']]
            T = tuple(tuple(sum((R[a][k] * v[k] for k in range(3)), fz(d)) + t[a] for a in range(3)) for v in T)
            (dents if dc['operation'] == 'minus' else keys).append((i, T))
    rec(slug, 'each keyed piece is the base fill\'s convex piece (same solid, rotation, translation) with its Tricaps removed or added; rotations orthogonal', same and orth)
    rec(slug, 'sum of piece volumes = cell volume (exact)', vsum == cv)
    Lf = [[x.f() for x in v] for v in L]
    import numpy as _np
    M = _np.array(Lf).T
    def lattice_diff(T1, T2):
        # T1 = T2 + integer combination of L, corner for corner (as sets), exactly
        g1 = [sum(x.f() for x in col) / 4 for col in zip(*T1)]; g2 = [sum(x.f() for x in col) / 4 for col in zip(*T2)]
        cf = _np.linalg.solve(M, _np.array(g1) - _np.array(g2)); ci = [int(round(x)) for x in cf]
        if max(abs(x - y) for x, y in zip(cf, ci)) > 1e-6: return False
        sh = tuple(sum((L[j][k] * ci[j] for j in range(3)), fz(d)) for k in range(3))
        return set(T1) == {tuple(v[k] + sh[k] for k in range(3)) for v in T2}
    used = set(); match = len(dents) == len(keys)
    for _, D in dents:
        js = [j for j, (_, Kt) in enumerate(keys) if j not in used and lattice_diff(D, Kt)]
        if len(js) != 1: match = False; break
        used.add(js[0])
    rec(slug, f'every dent ({len(dents)} per cell) is exactly one key ({len(keys)} per cell) moved by a lattice vector: each Tricap '
              'taken from one piece is given to exactly one other', match and len(used) == len(keys))
    rec(slug, 'base fill tiles + the Tricaps only change owner => the keyed pieces tile space (' + doc.get('keying', '') + ')',
        base_ok and all(base_ok) and same and match and vsum == cv)


def main():
    solids = {}
    for p in sorted(glob.glob(os.path.join(HERE, 'solids', '*.json'))):
        try: solids[os.path.basename(p)[:-5]] = check_solid(p)
        except Exception as e: rec(os.path.basename(p)[:-5], 'checks ran', False, repr(e))
    for slug in sorted(solids):   # version 2: non-convex solids stated as a convex solid -/+ Tricaps
        doc = json.load(open(os.path.join(HERE, 'solids', slug + '.json')))
        if 'decomposition' in doc:
            try: check_decomposition(slug, doc, solids)
            except Exception as e: rec(slug, 'decomposition checks ran', False, repr(e))
    for slug in sorted(solids):   # version 3: non-convex solids stated as convex pieces -/+ Tricaps
        doc = json.load(open(os.path.join(HERE, 'solids', slug + '.json')))
        if 'composition' in doc:
            try: check_composition(slug, doc, solids)
            except Exception as e: rec(slug, 'composition checks ran', False, repr(e))
    keyed = []
    for p in sorted(glob.glob(os.path.join(HERE, 'packings', '*.json'))):
        if json.load(open(p)).get('proof') == 'decomposition': keyed.append(p); continue
        try: check_packing(p, solids)
        except Exception as e: rec(os.path.basename(p)[:-5], 'checks ran', False, repr(e))
    for p in keyed:
        try: check_keyed_packing(p, solids)
        except Exception as e: rec(os.path.basename(p)[:-5], 'checks ran', False, repr(e))
    for p in sorted(glob.glob(os.path.join(HERE, 'packings-nonfilling', '*.json'))):
        try: check_packing(p, solids, filling=False)
        except Exception as e: rec(os.path.basename(p)[:-5], 'checks ran', False, repr(e))
    # also the OFF files: same corners (decimals) and faces as the JSON
    for p in sorted(glob.glob(os.path.join(HERE, 'solids', '*.off'))):
        unit = p.endswith('-unit-volume.off'); slug = os.path.basename(p)[:-(len('-unit-volume.off') if unit else 4)]
        doc = json.load(open(os.path.join(HERE, 'solids', slug + '.json')))
        lines = [l for l in open(p).read().split('\n') if l and not l.startswith('#')]
        nv, nf, _ = map(int, lines[1].split())
        vs = [list(map(float, l.split())) for l in lines[2:2 + nv]]; fs = [list(map(int, l.split()))[1:] for l in lines[2 + nv:2 + nv + nf]]
        ref = doc['unit_volume']['vertices_decimal'] if unit else [w['decimal'] for w in doc['vertices']]
        rec(slug, ('unit-volume ' if unit else '') + 'OFF file matches the JSON', lines[0] == 'OFF' and len(vs) == len(ref) and fs == doc['faces'] and all(abs(a - float(b)) < 1e-14 for v, w in zip(vs, ref) for a, b in zip(v, w)))
    items = {}
    for it, t, ok, note in RESULTS: items.setdefault(it, []).append(ok)
    w = max(len(i) for i in items)
    print('DICTO math-data dataset · check.py · Created by DICTO · dictospheres.com')
    print(f"{'item'.ljust(w)}  tests  result")
    for it, oks in items.items(): print(f"{it.ljust(w)}  {len(oks):5d}  {'PASS' if all(oks) else 'FAIL'}")
    bad = [(it, t, note) for it, t, ok, note in RESULTS if not ok]
    for it, t, note in bad: print('FAIL', it, '-', t, note)
    print(f'TOTAL: {len(RESULTS)} checks, {len(RESULTS) - len(bad)} passed, {len(bad)} failed; '
          f'{len(solids)} solids, {len(glob.glob(os.path.join(HERE, "packings", "*.json")))} packings (fills), '
          f'{len(glob.glob(os.path.join(HERE, "packings-nonfilling", "*.json")))} packings (not fills)')
    if '-v' in sys.argv:
        for it, t, ok, note in RESULTS: print('PASS' if ok else 'FAIL', it, '|', t, '|', note)
    sys.exit(0 if not bad else 1)


if __name__ == '__main__':
    main()
