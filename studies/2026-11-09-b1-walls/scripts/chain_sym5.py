# B1 / #80, #81: as chain_sym.py, for the edge-cut dodecahedron of #80 (five-fold planes at foot 1, two-fold planes at foot s),
# exact in the field Q(sqrt5)(s). Sample values live in Q(sqrt5) (class Q5, exact sign). Walls: real roots of the slack numerators;
# a numerator with sqrt5 in it is multiplied by its conjugate to get a rational polynomial (its roots are a superset, so the hop
# found is never too large); each wall is marked genuine when the Q(sqrt5) factor itself vanishes there (60-digit check).
# Usage: python chain_sym5.py <s0> <steps>
import sys, itertools, time
from fractions import Fraction as Fr
import numpy as np, sympy as sp
from scipy.spatial import HalfspaceIntersection
s = sp.Symbol('s'); r5 = sp.sqrt(5); A = sp.QQ.algebraic_field(r5); K = A.frac_field(s)
def kel(x): return K.from_sympy(sp.sympify(x))
ZERO, ONE = kel(0), kel(1)
class Q5:
    __slots__ = ('a', 'b')
    def __init__(z, a, b=0): z.a, z.b = Fr(a), Fr(b)
    def _c(z, o): return o if isinstance(o, Q5) else Q5(o)
    def __add__(z, o): o = z._c(o); return Q5(z.a + o.a, z.b + o.b)
    __radd__ = __add__
    def __neg__(z): return Q5(-z.a, -z.b)
    def __sub__(z, o): return z + (-z._c(o))
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
    def __eq__(z, o): o = z._c(o); return z.a == o.a and z.b == o.b
    def __hash__(z): return hash((z.a, z.b))
    def __float__(z): return float(z.a) + float(z.b) * 5 ** 0.5
def anp(c):
    L = c.to_list() if hasattr(c, 'to_list') else c.rep
    L = [Fr(int(x.numerator), int(x.denominator)) for x in L]
    return Q5(L[-1] if L else 0, L[-2] if len(L) > 1 else 0)
def evp(p, s0):
    v = Q5(0)
    for (k,), c in p.terms(): v = v + anp(c) * (s0 ** k)
    return v
def evq(x, s0): return evp(x.numer, s0) / evp(x.denom, s0)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def det3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def iszero(x): return x == 0 if isinstance(x, Q5) else x == ZERO

def sym_halfspace(planes, s0):
    P0 = [(tuple(evq(x, s0) for x in n), evq(c, s0)) for n, c in planes]
    Nf = np.array([[float(x) for x in n] for n, c in P0]); cf = np.array([float(c) for n, c in P0])
    X = HalfspaceIntersection(np.hstack([Nf, -cf[:, None]]), np.zeros(3)).intersections
    X = X[np.unique(np.round(X, 9), axis=0, return_index=True)[1]]
    C0 = {}
    for x in X:
        tight = [i for i in range(len(P0)) if abs(Nf[i] @ x - cf[i]) < 1e-7 * max(1, abs(cf[i]))]
        tri = next(t for t in itertools.combinations(tight, 3) if not iszero(det3(*(P0[i][0] for i in t))))
        Am = [P0[i][0] for i in tri]; b = [P0[i][1] for i in tri]; D = det3(*Am)
        C0[tuple(det3(*[tuple(b[r] if k == col else Am[r][k] for k in range(3)) for r in range(3)]) / D for col in range(3))] = None
    out, tights, polys = [], [], set()
    for c0 in C0:
        sl0 = [(dot(n, c0) - c).sign() for n, c in P0]
        assert all(v <= 0 for v in sl0), 'corner outside'
        T = [i for i, v in enumerate(sl0) if v == 0]
        tri = next(t for t in itertools.combinations(T, 3) if not iszero(det3(*(P0[i][0] for i in t))))
        Am = [planes[i][0] for i in tri]; b = [planes[i][1] for i in tri]; D = det3(*Am)
        polys.add(D.numer.as_expr())
        c = tuple(det3(*[tuple(b[r] if k == col else Am[r][k] for k in range(3)) for r in range(3)]) / D for col in range(3))
        for i in range(len(planes)):
            sl = dot(planes[i][0], c) - planes[i][1]
            if i in T: assert sl == ZERO, 'incidence holds only at the sample (s0 is a wall)'
            else: polys.add(sl.numer.as_expr())
        out.append(c); tights.append(frozenset(T))
    kinds = {}
    for i in range(len(planes)):
        k = sum(1 for T in tights if i in T)
        if k >= 3: kinds[k] = kinds.get(k, 0) + 1
    return out, tights, polys, dict(sorted(kinds.items()))

def hop(polys, s0, lo, hi):
    """nearest genuine walls on either side of s0: real roots of a slack numerator p (norm taken when p has sqrt5) at which p
    itself vanishes (100-digit evaluation; a root of the conjugate factor only is not a wall)."""
    a, b = lo, hi; s0 = sp.Rational(s0); seen = set(); nwall = 0
    for p in polys:
        p = sp.expand(p)
        if not p.has(s): continue
        q = sp.Poly(sp.expand(p * p.subs(r5, -r5)) if p.has(r5) else p, s)
        key = (tuple(q.monic().all_coeffs()), p.has(r5))
        if key in seen: continue
        seen.add(key)
        for f, m in sp.factor_list(q)[1]:
            for r in sp.Poly(f, s).real_roots():
                if not (lo < r < hi): continue
                if p.has(r5) and abs(sp.N(p.subs(s, r), 100)) > sp.Float(10) ** -70: continue
                nwall += 1
                assert r != s0, 's0 is a wall'
                if r < s0 and r > a: a = r
                if r > s0 and r < b: b = r
    return a, b, nwall, None

def similar_sym(Aa, B):
    if len(Aa) != len(B): return None
    g = None
    for v in B:
        m = next((u for u in Aa if all(x == ZERO for x in cross(u, v))), None)
        if m is None or dot(v, m) == ZERO: return None
        r = dot(v, v) / dot(m, m)
        if g is None: g = r
        elif (r - g).numer: return None   # 11-10 FIX: a field element is zero iff its numerator polynomial is zero ('!=' compared representations)
    return g

if __name__ == '__main__':
    # SELF-CONTROL (11-10, ONLY HAPPENS ONCE): the similarity test must recognise a shape and its own scaled copy, else stop.
    _A = [tuple(kel(x) for x in v) for v in ((1, 2, 3), (-2, 1, 0), (0, sp.sqrt(5), 1))]
    _B = [tuple(kel(sp.Rational(3, 2) * (1 + sp.sqrt(5))) * x for x in v) for v in _A]
    assert similar_sym(_A, _B) is not None, 'similarity test fails its own known-answer control'
    s0 = Fr(sys.argv[1]); N = int(sys.argv[2]); t0 = time.time()
    import os   # the depth window (10 Nov: was fixed at [1, 3/2], which clipped hops for samples below 1 - the 'artefact' of the 3/4 run)
    lo, hi = sp.Rational(os.environ.get('LO', '2/5')), sp.Rational(os.environ.get('HI', '3/2'))
    ph = (1 + r5) / 2
    def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
    five = {tuple(sp.nsimplify(x) for x in w) for a, b in itertools.product((1, -1), repeat=2) for w in cyc((0, a, b * ph))}
    two = {w for c in (1, -1) for w in cyc((0, 0, c * ph))}
    two |= {w for a, b, c in itertools.product((1, -1), repeat=3) for w in cyc((sp.Rational(a, 2), b * ph ** 2 / 2, c * ph / 2))}
    assert len(five) == 12 and len(two) == 30
    five = [tuple(kel(sp.expand(x)) for x in v) for v in five]; two = [tuple(kel(sp.expand(x)) for x in v) for v in two]
    planes = [(n, dot(n, n)) for n in five] + [(n, kel(s) * dot(n, n)) for n in two]
    hist = []; HOP = [lo, hi]
    V, T, polys, kinds = sym_halfspace(planes, s0)
    for k in range(0, N + 1):
        if k:
            V, T, polys, kinds = sym_halfspace([(v, dot(v, v)) for v in V], s0)
        a, b, ga, gb = hop(polys, s0, lo, hi); HOP = [max(HOP[0], a), min(HOP[1], b)]
        print(f'step {k}: {len(V)} corners, kinds {kinds}, hop ({a}, {b}) ~ ({float(a):.6f}, {float(b):.6f}) walls {ga}; {time.time()-t0:.0f}s', flush=True)
        closed = None
        for j, (Aa, ka) in enumerate(hist):
            if ka == kinds:
                g = similar_sym(Aa, V)
                if g is not None:
                    # 11-10: the gain is a huge unreduced element; test it against the constant (35 - 15 sqrt5)^k-period form exactly
                    tgt = kel(sp.expand((35 - 15 * sp.sqrt(5)) ** 2)) ** ((k - j) // 4) if (k - j) % 4 == 0 else None
                    const = tgt is not None and not (g - tgt).numer
                    closed = dict(enters=j, period=k - j, gain2=('(35 - 15 sqrt5)^2 for every depth s in the hop' if const else f'not constant; at s0 ~ {float(sp.N(K.to_sympy(g).subs(s, s0))):.12f}'))
                    break
        hist.append((V, kinds))
        if closed: break
    print('chain hop', HOP, f'~ ({float(HOP[0]):.6f}, {float(HOP[1]):.6f})')
    print('closure', closed)
    print('FINAL ok' if closed else 'FINAL FAIL: no closure identity on this hop within the steps run')
