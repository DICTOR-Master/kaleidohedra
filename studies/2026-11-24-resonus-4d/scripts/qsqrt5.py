"""Exact arithmetic in Q(sqrt5): a + b*sqrt5 with a, b rational (Fractions). No floating point anywhere."""
from fractions import Fraction as Fr

class K:
    __slots__ = ("a", "b")
    def __init__(self, a=0, b=0):
        self.a = a if isinstance(a, Fr) else Fr(a)
        self.b = b if isinstance(b, Fr) else Fr(b)
    @staticmethod
    def c(x):
        return x if isinstance(x, K) else K(x)
    def __add__(s, o): o = K.c(o); return K(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = K.c(o); return K(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return K.c(o) - s
    def __neg__(s): return K(-s.a, -s.b)
    def __mul__(s, o):
        o = K.c(o); return K(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b
        if n == 0: raise ZeroDivisionError
        return K(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * K.c(o).inv()
    def __rtruediv__(s, o): return K.c(o) * s.inv()
    def __eq__(s, o): o = K.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __bool__(s): return bool(s.a) or bool(s.b)
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        # opposite signs: compare a^2 with 5 b^2
        d = a * a - 5 * b * b
        return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f"({s.a}{'+' if s.b >= 0 else ''}{s.b}*r5)"
    def key(s): return (s.a, s.b)

R5 = K(0, 1)
PHI = K(Fr(1, 2), Fr(1, 2))
IPHI = PHI - 1          # 1/phi
ZERO, ONE = K(0), K(1)

def dot(u, v):
    s = ZERO
    for x, y in zip(u, v): s = s + x * y
    return s

def sub(u, v): return tuple(x - y for x, y in zip(u, v))
def add(u, v): return tuple(x + y for x, y in zip(u, v))
def scal(c, u): return tuple(c * x for x in u)

def vkey(v): return tuple(x.key() for x in v)

def linekey(v):
    """Key of the line through O spanned by v (v up to a nonzero scalar, sign included)."""
    for x in v:
        if x: c = x.inv(); return tuple((c * y).key() for y in v)
    raise ValueError("zero vector")

def nullspace(rows, n):
    """Exact nullspace basis of the matrix with the given rows (each of length n)."""
    M = [list(r) for r in rows]; piv = []; r = 0
    for col in range(n):
        p = next((i for i in range(r, len(M)) if M[i][col]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        iv = M[r][col].inv(); M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col]:
                f = M[i][col]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(col); r += 1
        if r == len(M): break
    free = [c for c in range(n) if c not in piv]; basis = []
    for fc in free:
        v = [ZERO] * n; v[fc] = ONE
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        basis.append(tuple(v))
    return basis

def rank(rows, n): return n - len(nullspace(rows, n))
