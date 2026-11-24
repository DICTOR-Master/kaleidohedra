# Exact arithmetic in Q(sqrt5) and exact convex spherical polygons (cones) over it.
from fractions import Fraction as Q
import itertools
class K:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a = Q(a); s.b = Q(b)
    def __add__(s, o): o = o if isinstance(o, K) else K(o); return K(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, K) else K(o); return K(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return K(o) - s
    def __neg__(s): return K(-s.a, -s.b)
    def __mul__(s, o): o = o if isinstance(o, K) else K(o); return K(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return K(s.a / n, -s.b / n)
    def __truediv__(s, o): o = o if isinstance(o, K) else K(o); return s * o.inv()
    def sign(s):
        sa = (s.a > 0) - (s.a < 0); sb = (s.b > 0) - (s.b < 0)
        if sa == 0: return sb
        if sb == 0 or sa == sb: return sa
        d = s.a * s.a - 5 * s.b * s.b       # opposite signs: sign of a + b sqrt5 is sign(a) iff a^2 > 5 b^2
        return sa if d > 0 else (-sa if d < 0 else 0)
    def __float__(s): return float(s.a) + float(s.b) * 5 ** .5
    def __eq__(s, o): o = o if isinstance(o, K) else K(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __repr__(s): return '(%s%+s*r5)' % (s.a, s.b)
PHI = K(Q(1, 2), Q(1, 2)); IPHI = PHI - 1
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def add(a, b): return tuple(x + y for x, y in zip(a, b))
def scl(c, a): return tuple(c * x for x in a)
def vec(*c): return tuple(x if isinstance(x, K) else K(x) for x in c)
def cyc_signs(t):
    out = []
    for s in itertools.product((1, -1), repeat=3):
        q = tuple(K(si) * ti for si, ti in zip(s, t))
        for k in range(3):
            w = q[k:] + q[:k]
            if w not in out: out.append(w)
    return out
def clip(poly, n):
    """keep n.x >= 0 of a convex polygon given by its generators in cyclic order (pointed cone); exact"""
    if not poly: return []
    out = []; L = len(poly)
    val = [dot(n, v) for v in poly]; sg = [x.sign() for x in val]
    for i in range(L):
        j = (i + 1) % L; a, b = poly[i], poly[j]
        if sg[i] >= 0: out.append(a)
        if sg[i] * sg[j] < 0:   # crossing: point a*(n.b) - b*(n.a) has n.x = 0 and lies between a and b
            c = sub(scl(val[j], a), scl(val[i], b))
            if sg[i] > 0: c = scl(K(-1), c)   # make it a positive combination of a and b
            out.append(c)
    # drop duplicates (parallel consecutive generators)
    res = []
    for v in out:
        if res and all(x.sign() == 0 for x in cross(res[-1], v)) and dot(res[-1], v).sign() > 0: continue
        res.append(v)
    if len(res) > 1 and all(x.sign() == 0 for x in cross(res[-1], res[0])) and dot(res[-1], res[0]).sign() > 0: res.pop()
    return res if len(res) >= 3 else []
def region(start, k, P, S):
    """{x in start : P[k].x >= P[j].x for all j in S}"""
    poly = list(start)
    for j in S:
        if j == k: continue
        poly = clip(poly, sub(P[k], P[j]))
        if not poly: return []
    return poly
