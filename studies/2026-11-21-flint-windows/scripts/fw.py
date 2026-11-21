"""Window edges of DICTO's growth rule T on the edge-cut cube (#80) and the edge-cut dodecahedron (#80, #81), with python-flint.

T(S) = {x : v.x <= v.v for every corner v of S}.  Starting solids exactly as in study 2026-11-09-b1-walls (chain_sym.py, chain_sym5.py):
  cube:  planes (n, 1) for n = (+-1, 0, 0) and cyclic, (n, 2s) for n = (+-1, +-1, 0) and cyclic;
  dodecahedron: planes (n, |n|^2) for the 12 five-fold n = (0, +-1, +-phi) cyclic, (n, s|n|^2) for the 30 two-fold
  n = (0, 0, +-phi) cyclic and (+-1/2, +-phi^2/2, +-phi/2) cyclic.
A 'type' of a chain is, for every step, the list of corners, each with its tight planes and one independent triple of them.
A type found in floating point at one depth is TRANSPORTED to other depths and other number systems by solving each corner
from its triple (Cramer's rule): arb balls (python-flint, any precision), exact rationals (fmpq), Q(sqrt5) (class Q5 below),
or an exact number field Q[x]/(f) (class NF below, fmpq_poly arithmetic modulo f)."""
import itertools
import numpy as np
from scipy.spatial import HalfspaceIntersection
from flint import fmpq, fmpz, arb, fmpq_poly, fmpz_poly, fmpz_mat, ctx

# ---------------------------------------------------------------- the starting solids, as exact specs a + b*sqrt5
H = fmpq(1, 2)
def _cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def spec(kind):
    """list of (normal, offset): normal = 3 pairs (a, b) meaning a + b sqrt5; offset = ((p_a, p_b), (q_a, q_b)) meaning p + q s."""
    Z, O = (fmpq(0), fmpq(0)), (fmpq(1), fmpq(0))
    def r(x): return (fmpq(x), fmpq(0))
    if kind == 'cube':
        out = []
        for i in range(3):
            for sg in (1, -1):
                out.append((tuple(r(sg) if k == i else Z for k in range(3)), (O, Z)))
        for a, b in itertools.product((1, -1), repeat=2):
            for v in _cyc((a, b, 0)):
                out.append((tuple(r(x) for x in v), (Z, r(2))))
        return out
    phi = (H, H); phi2h = (fmpq(3, 4), fmpq(1, 4)); phih = (fmpq(1, 4), fmpq(1, 4))
    def neg(p): return (-p[0], -p[1])
    five, two = [], []
    for a, b in itertools.product((1, -1), repeat=2):
        five += _cyc((Z, r(a), phi if b > 0 else neg(phi)))
    for c in (1, -1):
        two += _cyc((Z, Z, phi if c > 0 else neg(phi)))
    for a, b, c in itertools.product((1, -1), repeat=3):
        two += _cyc(((H * a, fmpq(0)), phi2h if b > 0 else neg(phi2h), phih if c > 0 else neg(phih)))
    assert len(five) == 12 and len(two) == 30
    n5 = ((fmpq(5, 2), H), Z)            # |n|^2 = 1 + phi^2 = (5 + sqrt5)/2
    n2 = (Z, (fmpq(3, 2), H))            # s |n|^2 = s phi^2 = s (3 + sqrt5)/2
    return [(v, n5) for v in five] + [(v, n2) for v in two]

# ---------------------------------------------------------------- number systems
class Q5:
    """a + b sqrt5 with a, b exact rationals (fmpq)."""
    __slots__ = ('a', 'b')
    def __init__(z, a, b=0): z.a, z.b = fmpq(a), fmpq(b)
    def _c(z, o): return o if isinstance(o, Q5) else Q5(o)
    def __add__(z, o): o = z._c(o); return Q5(z.a + o.a, z.b + o.b)
    __radd__ = __add__
    def __neg__(z): return Q5(-z.a, -z.b)
    def __sub__(z, o): o = z._c(o); return Q5(z.a - o.a, z.b - o.b)
    def __rsub__(z, o): return z._c(o) - z
    def __mul__(z, o): o = z._c(o); return Q5(z.a * o.a + 5 * z.b * o.b, z.a * o.b + z.b * o.a)
    __rmul__ = __mul__
    def __truediv__(z, o):
        o = z._c(o); n = o.a * o.a - 5 * o.b * o.b; return z * Q5(o.a / n, -o.b / n)
    def sign(z):
        a, b = z.a, z.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) if a * a > 5 * b * b else (1 if b > 0 else -1)
    def is_zero(z): return z.a == 0 and z.b == 0
    def __float__(z): return float(z.a) + float(z.b) * 5 ** 0.5

class NF:
    """exact element of Q[x]/(f), f irreducible; x stands for the edge s*.  SQ5: the element sqrt5 of the field, when set."""
    f = None; SQ5 = None
    __slots__ = ('p',)
    def __init__(z, p): z.p = p if isinstance(p, fmpq_poly) and p.degree() < NF.f.degree() else fmpq_poly(p) % NF.f
    def _c(z, o): return o if isinstance(o, NF) else NF(fmpq_poly([o]))
    def __add__(z, o): return NF(z.p + z._c(o).p)
    __radd__ = __add__
    def __neg__(z): return NF(-z.p)
    def __sub__(z, o): return NF(z.p - z._c(o).p)
    def __rsub__(z, o): return z._c(o) - z
    def __mul__(z, o): return NF((z.p * z._c(o).p) % NF.f)
    __rmul__ = __mul__
    def inv(z):
        g, u, v = z.p.xgcd(NF.f); assert g.degree() == 0 and not g.is_zero(), 'not invertible'
        return NF(u / g[0])
    def __truediv__(z, o): return z * z._c(o).inv()
    def __rtruediv__(z, o): return z._c(o) * z.inv()
    def is_zero(z): return z.p.is_zero()

def field_ops(field):
    """returns (const(a, b) -> scalar for a + b sqrt5, s -> scalar)."""
    if field == 'arb':
        r5 = arb(5).sqrt(); return (lambda a, b: arb(a) + arb(b) * r5 if b != 0 else arb(a))
    if field == 'fmpq':
        def c(a, b): assert b == 0; return fmpq(a)
        return c
    if field == 'Q5': return lambda a, b: Q5(a, b)
    if field == 'NF':
        def c(a, b):
            v = NF(fmpq_poly([a]))
            return v if b == 0 else v + NF.SQ5 * NF(fmpq_poly([b]))
        return c
    raise ValueError(field)

def start_planes(kind, field, s):
    c = field_ops(field)
    out = []
    for n, (p, q) in spec(kind):
        out.append((tuple(c(*x) for x in n), c(*p) + c(*q) * s))
    return out

def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def det3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def solve(planes, tri):
    A = [planes[i][0] for i in tri]; b = [planes[i][1] for i in tri]; D = det3(*A)
    return tuple(det3(*[tuple(b[r] if k == col else A[r][k] for k in range(3)) for r in range(3)]) / D for col in range(3))

# ---------------------------------------------------------------- floating point: find the type at one depth
def float_start(kind, s):
    P = start_planes(kind, 'arb', arb(s))
    return np.array([[float(x.mid()) for x in n] for n, c in P]), np.array([float(c.mid()) for n, c in P])

def float_step(Nm, cv):
    X = HalfspaceIntersection(np.hstack([Nm, -cv[:, None]]), np.zeros(3)).intersections
    R = np.linalg.norm(X, axis=1).max()
    X = X[np.unique(np.round(X / R, 8), axis=0, return_index=True)[1]]
    Nu = Nm / np.linalg.norm(Nm, axis=1)[:, None]; cu = cv / np.linalg.norm(Nm, axis=1)
    out, typ = [], []
    for x in X:
        sl0 = Nu @ x - cu; got = None
        for tol in (1e-11, 1e-10, 1e-9, 1e-8, 1e-7):
            T = np.nonzero(np.abs(sl0) < tol * R)[0]
            best, bd = None, 0
            for t in itertools.combinations(T, 3):
                d = abs(np.linalg.det(Nu[list(t)]))
                if d > bd + 1e-12: best, bd = t, d
            if best is None or bd < 1e-6: continue
            y = np.linalg.solve(Nu[list(best)], cu[list(best)])          # polish the corner on its triple
            sl = Nu @ y - cu
            if sl.max() < 1e-10 * R: got = (y, best, np.nonzero(np.abs(sl) < 1e-10 * R)[0]); break
        assert got is not None, 'no clean corner'
        y, best, T = got
        out.append(y); typ.append((tuple(int(i) for i in best), tuple(int(i) for i in T)))
    out = np.array(out)
    keep = np.unique(np.round(out / R, 9), axis=0, return_index=True)[1]
    keep = sorted(keep)
    return out[keep], [typ[i] for i in keep], None

def float_chain(kind, s, N):
    """types and corners of steps 0..N (each step rescaled to radius 1 for stability; T(kS) = kT(S))."""
    Nm, cv = float_start(kind, s); types, Vs = [], []
    for k in range(N + 1):
        X, typ, S = float_step(Nm, cv); types.append(typ); Vs.append(X)
        R = np.linalg.norm(X, axis=1).max(); Y = X / R
        Nm, cv = Y, np.einsum('ij,ij->i', Y, Y)
    return types, Vs

def kinds_of(typ, nplanes):
    cnt = {}
    for tri, T in typ:
        for i in T: cnt[i] = cnt.get(i, 0) + 1
    out = {}
    for i, k in cnt.items():
        if k >= 3: out[k] = out.get(k, 0) + 1
    return tuple(sorted(out.items()))

def float_similar(A, B, tol=1e-7):
    if len(A) != len(B): return None
    a = A / np.linalg.norm(A, axis=1)[:, None]; b = B / np.linalg.norm(B, axis=1)[:, None]
    ra = np.linalg.norm(A, axis=1); rb = np.linalg.norm(B, axis=1); rat = []
    for v, nb in zip(b, rb):
        d = np.linalg.norm(a - v, axis=1); i = d.argmin()
        if d[i] > tol: return None
        rat.append(nb / ra[i])
    rat = np.array(rat); return rat.mean() if rat.std() < 1e-7 * rat.mean() else None

def float_closure(kind, s, N):
    """first (j, k) with step k similar to step j (same corner directions, one scale), corner counts per step."""
    types, Vs = float_chain(kind, s, N)
    for k in range(1, N + 1):
        for j in range(k):
            if len(Vs[j]) == len(Vs[k]) and float_similar(Vs[j], Vs[k]) is not None:
                return (j, k), [len(v) for v in Vs], types
    return None, [len(v) for v in Vs], types

# ---------------------------------------------------------------- transport of a type
def transport(kind, field, s, types, upto, last_only=None):
    """corners of steps 0..upto solved from the type's triples; returns list of (planes, corners) per step.
    last_only = set of corner indices: at step upto solve only those (others None)."""
    planes = start_planes(kind, field, s); out = []
    for k in range(upto + 1):
        typ = types[k]
        V = [solve(planes, tri) if (last_only is None or k < upto or j in last_only) else None for j, (tri, T) in enumerate(typ)]
        out.append((planes, V))
        if k < upto: planes = [(v, dot(v, v)) for v in V]
    return out

def slack(planes, v, i): return dot(planes[i][0], v) - planes[i][1]

# ---------------------------------------------------------------- integer relations (LLL in FLINT)
def arb_to_fmpq(x):
    m, e = x.mid().man_exp(); m, e = int(m), int(e)
    return fmpq(m * 2 ** e) if e >= 0 else fmpq(m, 2 ** (-e))

def guess_poly(alpha, deg, bits, with_sqrt5=False):
    """LLL on 1, a, ..., a^deg (and sqrt5 times them): returns integer coefficient vector(s) of a small relation, or None."""
    ctx.prec = bits + 64
    a = alpha; pw = [arb(1)]
    for k in range(deg): pw.append(pw[-1] * a)
    cols = pw + ([p * arb(5).sqrt() for p in pw] if with_sqrt5 else [])
    C = fmpz(2) ** bits
    n = len(cols)
    rows = []
    for i, x in enumerate(cols):
        q = arb_to_fmpq(x) * C
        rows.append([1 if j == i else 0 for j in range(n)] + [int(q.p // q.q)])
    M = fmpz_mat(rows).lll()
    v = [int(M[0, j]) for j in range(n)]
    return v
