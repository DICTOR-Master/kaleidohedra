"""Shared ball-arithmetic model for the certificates of this study (python-flint / Arb).

The (b), (c) family of #103 on the rhombus u = v (every (b), (c) yantra with uv = c is the image of one with u = v = sqrt(c)
under the viewpoint map of #103 Theorem 5). Unknowns as in #103 Theorem 15's census (study 2026-11-15-dicto-yantra-uniqueness,
s1_system.py) and study 2026-11-20-cleo-antonius-selection (yfam.py, data/system-uv.json):
  u = slope of t7 = slope of t3,  t = b1/w1 (t1's corners on the circle, (b), by construction),  S = b9.
  G(u, S) = 0 is (c) (quadratic in S); H1(u, t, S) = 0 is the closing marma (1,4,6) (degree 10 in t); C is the concurrency of
  t4's right leg, t5's base and t6's right leg (the corner touch (5,5,6) met by t4's leg).
Everything here is rigorous ball arithmetic: every returned ball contains the true value.

Main tools
  branch_point(U)   : enclosures of S and t on the admissible branch for every u in the ball U (parametric interval Newton:
                      exactly one t in the returned box for every (u, S) of the box).
  build(u, t, S)    : the yantra (b, w, a) in AD numbers (value, d/du), the construction of yfam.build line by line.
  centred(fm, fB, r): mean-value enclosure f(m) + f'(box) [-r, r] over the u-box m +- r.
"""
import json, os, itertools
import flint
from flint import arb, fmpq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SYS = json.load(open(os.path.join(ROOT, 'data', 'system-uv.json')))


def poly_vu(name):
    """Polynomial with v = u: dict (e_u, e_t, e_S) -> int coefficient."""
    out = {}
    for e, c in SYS[name]:
        k = (e[0] + e[1], e[2], e[3]); out[k] = out.get(k, 0) + int(c)
    return {k: c for k, c in out.items() if c}


def pdiff(P, j):
    out = {}
    for e, c in P.items():
        if e[j]:
            k = list(e); k[j] -= 1; out[tuple(k)] = out.get(tuple(k), 0) + c * e[j]
    return out


G = poly_vu('G'); H1 = poly_vu('H1'); C = poly_vu('C')
Gu, GS = pdiff(G, 0), pdiff(G, 2)
Hu, Ht, HS = pdiff(H1, 0), pdiff(H1, 1), pdiff(H1, 2)
assert all(e[1] == 0 for e in G), 'G involves t'
GA = {(e[0],): c for e, c in G.items() if e[2] == 2}; GB = {(e[0],): c for e, c in G.items() if e[2] == 1}
GC = {(e[0],): c for e, c in G.items() if e[2] == 0}


def peval(P, X):
    """P at arb (or AD) values X = (u, t, S); powers cached."""
    pw = {}
    def p(j, k):
        if (j, k) not in pw: pw[(j, k)] = X[j] ** k if k else 1
        return pw[(j, k)]
    tot = 0
    for e, c in P.items():
        term = arb(c)
        for j, k in enumerate(e):
            if k: term = term * p(j, k)
        tot = tot + term
    return tot


def ueval(P, u):
    return sum((arb(c) * u ** e[0] for e, c in P.items()), arb(0))


class AD:
    """Forward derivative in u: value and d/du, both arb balls."""
    __slots__ = ('v', 'd')
    def __init__(s, v, d=0): s.v = v if isinstance(v, arb) else arb(v); s.d = d if isinstance(d, arb) else arb(d)
    @staticmethod
    def c(o): return o if isinstance(o, AD) else AD(o, 0)
    def __add__(s, o): o = AD.c(o); return AD(s.v + o.v, s.d + o.d)
    __radd__ = __add__
    def __sub__(s, o): o = AD.c(o); return AD(s.v - o.v, s.d - o.d)
    def __rsub__(s, o): return AD.c(o) - s
    def __mul__(s, o): o = AD.c(o); return AD(s.v * o.v, s.d * o.v + s.v * o.d)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = AD.c(o); q = s.v / o.v; return AD(q, (s.d - q * o.d) / o.v)
    def __rtruediv__(s, o): return AD.c(o) / s
    def __neg__(s): return AD(-s.v, -s.d)
    def __pow__(s, k):
        r = AD(arb(1))
        for _ in range(k): r = r * s
        return r


def S_roots(U):
    """Both roots of the quadratic G in S at u in U (balls), the larger first."""
    A, B, Cc = ueval(GA, U), ueval(GB, U), ueval(GC, U)
    disc = B * B - 4 * A * Cc
    if not disc > 0: raise ValueError('discriminant of G not certified positive')
    sq = disc.sqrt()
    r1, r2 = (-B + sq) / (2 * A), (-B - sq) / (2 * A)
    return (r1, r2) if r1 > r2 else (r2, r1)


def S_branch(U):
    """The root of G in (R, 1); the other root must lie outside [R, 1]."""
    R = 1 / (1 + U * U)
    r = S_roots(U)
    inside = [x for x in r if (x - R) > 0 and (1 - x) > 0]
    outside = [x for x in r if (x - R) < 0 or (x - 1) > 0]
    if len(inside) != 1 or len(outside) != 1: raise ValueError('S root separation not certified')
    return inside[0]


def t_refine(um, Sm, tg, it=60):
    """Point Newton at the midpoint (no claim), arb midpoints only."""
    t = arb(tg)
    for _ in range(it):
        h = peval(H1, (um, t, Sm)); hd = peval(Ht, (um, t, Sm))
        t = arb((t - h / hd).mid())
    return t


Htu, Htt, HtS = pdiff(Ht, 0), pdiff(Ht, 1), pdiff(Ht, 2)


def cpeval(P, dP, mid, box):
    """Centred (mean-value) form of P over the box: P(mid) + sum_j dP_j(box) (box_j - mid_j)."""
    tot = peval(P, mid)
    for j in range(3):
        if dP[j] is not None and dP[j]: tot = tot + peval(dP[j], box) * (box[j] - mid[j])
    return tot


def branch(U, tguess):
    """For the u-ball U: (Sbox, Tbox, t_mid) with, for every u in U, S(u) in Sbox the root of G in (R, 1) and exactly one root t
    of H1(u, ., S(u)) in Tbox (parametric interval Newton: N(T) inside T). Raises ValueError when not certified."""
    Sb0 = S_branch(U)                                    # naive enclosure, also certifies the root separation on U
    um = arb(U.mid()); Sm = S_branch(um); zero = arb(0)
    if U.rad() > 0:
        dS = -peval(Gu, (U, zero, Sb0)) / peval(GS, (U, zero, Sb0))
        Sb = Sm + dS * (U - um)
        Sb = Sb.intersection(Sb0) if hasattr(Sb, 'intersection') else Sb
    else:
        Sb = Sb0
    tm = t_refine(um, arb(Sm.mid()), tguess)
    mid = (um, tm, Sm)
    hb = cpeval(H1, (Hu, None, HS), mid, (U, tm, Sb))   # H1 at t = tm over the whole (u, S) box
    htm = abs(peval(Ht, (um, tm, Sm)).mid())
    delta = (abs(hb.mid()) + hb.rad()) / htm
    for scale in [2, 4, 16, 64, 256, 2 ** 12, 2 ** 16]:
        T = arb(tm.mid(), arb(delta * scale + arb(2) ** (-flint.ctx.prec + 30)).upper())
        htT = cpeval(Ht, (Htu, Htt, HtS), mid, (U, T, Sb))
        if htT.contains(0): continue
        Nt = tm - hb / htT
        if T.contains_interior(Nt): return Sb, Nt, tm
    raise ValueError('interval Newton for t not certified')


_PD = {}
def cp(P, mid, box):
    """Centred form of P over the box with its partial derivatives computed (and cached) here."""
    k = id(P)
    if k not in _PD: _PD[k] = (P, [pdiff(P, j) for j in range(3)])
    return cpeval(P, _PD[k][1], mid, box)


def branch_derivs(U, Tb, Sb, mid):
    """Enclosures over the box of S'(u) and t'(u) along the branch (implicit differentiation of G = 0 and H1 = 0)."""
    zero = arb(0)
    mS = (mid[0], zero, mid[2]); bS = (U, zero, Sb)
    Sd = -cp(Gu, mS, bS) / cp(GS, mS, bS)
    box = (U, Tb, Sb)
    td = -(cp(Hu, mid, box) + cp(HS, mid, box) * Sd) / cp(Ht, mid, box)
    return Sd, td


def build(u, t, S):
    """yfam.build in AD (or arb) arithmetic with v = u; returns dict b, w, a (1..9)."""
    v = u
    P = v * v / (1 + v * v); R = 1 / (1 + u * u)
    w3 = v / (1 + v * v); w7 = u / (1 + u * u)
    b1 = t * t / (1 + t * t); w1 = t / (1 + t * t)
    xW = w7 * P / R
    xX = xW * (S - R) / (S - P)
    k9 = xX / (R - P)
    w9 = k9 * (S - P)
    k3 = w3 / (1 - P)
    xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1)
    Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1)
    b8 = (k3 + k9 * P) / (k3 + k9)
    xF = k9 * (Q - P)
    w6 = xW * (S - Q) / (S - P)
    k7 = w7 / R
    b2 = m1 * Q / (m1 + k7)
    c4 = xF / (b8 - Q); c8 = xZ / (R - b1)
    b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9)
    w5 = w6 * (b5 - b2) / (Q - b2)
    one = AD(arb(1)) if isinstance(u, AD) else arb(1); zero = AD(arb(0)) if isinstance(u, AD) else arb(0)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {1: Q, 2: S, 3: one, 4: b8, 5: R, 6: b2, 7: zero, 8: b1, 9: P}
    w = {1: w1, 2: xW * (S - b2) / (S - P), 3: w3, 4: xF * (b8 - b4) / (b8 - Q), 5: w5, 6: w6, 7: w7,
         8: xZ * (b8 - b1) / (R - b1), 9: w9}
    return dict(b=b, w=w, a=a)


NAMES = [f'{k}{i}' for i in range(1, 10) for k in 'BRL']
TRIPLES = list(itertools.combinations(NAMES, 3))
DOWN = (1, 2, 3, 4, 5)
# the corner touch (5,5,6) met by t4's leg, and its mirror image: the six triples that vanish at both ends of the window
THRESH = {tuple(sorted(x)) for x in [('R4', 'B5', 'R5'), ('R4', 'B5', 'R6'), ('R4', 'R5', 'R6'),
                                     ('L4', 'B5', 'L5'), ('L4', 'B5', 'L6'), ('L4', 'L5', 'L6')]}
C_TRIPLE = tuple(sorted(('R4', 'B5', 'R6')))


def segments(y):
    """Each of the 27 drawn sides as (endpoint 1, endpoint 2)."""
    b, w, a = y['b'], y['w'], y['a']; zero = a[7]; L = {}
    for i in range(1, 10):
        L[f'B{i}'] = ((-w[i], b[i]), (w[i], b[i])); L[f'R{i}'] = ((w[i], b[i]), (zero, a[i])); L[f'L{i}'] = ((-w[i], b[i]), (zero, a[i]))
    return L


def lc(pp):
    (x1, y1), (x2, y2) = pp
    return (y1 - y2, x2 - x1, x1 * y2 - x2 * y1)


def det3(A, B, C_):
    return (A[0] * (B[1] * C_[2] - B[2] * C_[1]) - A[1] * (B[0] * C_[2] - B[2] * C_[0]) + A[2] * (B[0] * C_[1] - B[1] * C_[0]))


def meet_params(S3):
    """Parameters (lam, mu, nu) of the meeting point of the first two sides along sides 1, 2 and (projected) along side 3;
    0 and 1 are the endpoints. If the three lines meet, the meeting point is on all three closed sides iff all three lie in [0, 1]."""
    (p1, p2), (q1, q2), (r1, r2) = S3
    den = (p2[0] - p1[0]) * (q2[1] - q1[1]) - (p2[1] - p1[1]) * (q2[0] - q1[0])
    lam = ((q1[0] - p1[0]) * (q2[1] - q1[1]) - (q1[1] - p1[1]) * (q2[0] - q1[0])) / den
    mu = ((q1[0] - p1[0]) * (p2[1] - p1[1]) - (q1[1] - p1[1]) * (p2[0] - p1[0])) / den
    X0 = p1[0] + lam * (p2[0] - p1[0]); X1 = p1[1] + lam * (p2[1] - p1[1])
    vx, vy = r2[0] - r1[0], r2[1] - r1[1]
    nu = ((X0 - r1[0]) * vx + (X1 - r1[1]) * vy) / (vx * vx + vy * vy)
    return lam, mu, nu


def centred(fm, fB, r):
    """f(m) + f'(box) * [-r, r]: fm, fB are AD values at the centre and over the box."""
    return fm.v + fB.d * arb(0, r)


def finite(x): return x.is_finite()


def admissibility(y):
    """The strict admissibility quantities of #103 Theorem 1 (each must be > 0), as (name, AD value)."""
    b, w, a = y['b'], y['w'], y['a']; out = []
    for i in range(1, 9): out.append((f'b{i}<b{i+1}', b[i + 1] - b[i]))
    out.append(('b9<1', 1 - b[9]))
    for i in range(1, 10): out.append((f'w{i}>0', w[i]))
    for i in range(1, 10):
        if i in (3, 7): continue                         # apexes on the circle: a3 = 1, a7 = 0 exactly
        out.append((f'apex side t{i}', (a[i] - b[i]) if i in DOWN else (b[i] - a[i])))
    for i in (2, 4, 5, 6, 8):                            # corners strictly inside the disc (1, 3, 7, 9 are on the circle)
        out.append((f't{i} corner inside', -(w[i] * w[i] + b[i] * b[i] - b[i])))
    return out
