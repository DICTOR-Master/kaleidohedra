"""Exact arithmetic in Q(sqrt5): a + b*sqrt5 with rational a, b (pure Python, no dependencies)."""
from fractions import Fraction as Fr


class Q:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = a if isinstance(a, Fr) else Fr(a)
        self.b = b if isinstance(b, Fr) else Fr(b)

    @staticmethod
    def c(x):
        return x if isinstance(x, Q) else Q(x)

    def __add__(s, o): o = Q.c(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = Q.c(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q.c(o) - s
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): o = Q.c(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def conj(s): return Q(s.a, -s.b)
    def norm(s): return s.a * s.a - 5 * s.b * s.b

    def __truediv__(s, o):
        o = Q.c(o); n = o.norm()
        if n == 0: raise ZeroDivisionError
        return s * o.conj() * Q(1 / n)

    def __rtruediv__(s, o): return Q.c(o) / s

    def sign(s):
        """exact sign of a + b sqrt5"""
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        # opposite signs: compare a^2 with 5 b^2
        d = a * a - 5 * b * b
        return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)

    def __eq__(s, o): o = Q.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def f(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def key(s): return (s.a, s.b)

    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f"{s.b}√5"
        return f"{s.a} {'+' if s.b > 0 else '-'} {abs(s.b)}√5"


PHI = Q(Fr(1, 2), Fr(1, 2))
IPHI = PHI - 1


def phipow(k):
    r = Q(1)
    for _ in range(abs(k)): r = r * PHI
    return r if k >= 0 else Q(1) / r


def log_phi_exact(x):
    """k if x == phi^k exactly (x > 0), else None"""
    if x.sign() <= 0: return None
    import math
    k = round(math.log(x.f()) / math.log(PHI.f()))
    return k if phipow(k) == x else None


def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def vsub(u, v): return (u[0] - v[0], u[1] - v[1], u[2] - v[2])
def vadd(u, v): return (u[0] + v[0], u[1] + v[1], u[2] + v[2])
def vsc(k, u): return (k * u[0], k * u[1], k * u[2])
def det3(a, b, c): return dot(a, cross(b, c))
def iszero(v): return all(x.sign() == 0 for x in v)
def vkey(v): return tuple(x.key() for x in v)


def pkey(v):
    """projective key: scale so the first nonzero coordinate is 1"""
    for x in v:
        if x.sign() != 0:
            return tuple((y / x).key() for y in v)
    raise ValueError("zero vector")


def solve3(n1, d1, n2, d2, n3, d3):
    D = det3(n1, n2, n3)
    if D.sign() == 0: return None
    c23, c31, c12 = cross(n2, n3), cross(n3, n1), cross(n1, n2)
    return tuple((d1 * c23[i] + d2 * c31[i] + d3 * c12[i]) / D for i in range(3))


def cyclic_signs(base):
    """all cyclic permutations of base with all sign changes (even permutations with signs), deduplicated"""
    out = {}
    for (x, y, z) in base:
        for p in ((x, y, z), (y, z, x), (z, x, y)):
            for sx in (1, -1):
                for sy in (1, -1):
                    for sz in (1, -1):
                        v = (Q.c(p[0]) * sx, Q.c(p[1]) * sy, Q.c(p[2]) * sz)
                        out[vkey(v)] = v
    return list(out.values())
