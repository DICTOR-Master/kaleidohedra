# Exact arithmetic in Q(sqrt r): a + b*sqrt(r), a, b rational.  Written for this recheck (no code from the studies checked).
from fractions import Fraction as F


class Q:
    __slots__ = ('a', 'b', 'r')

    def __init__(self, a=0, b=0, r=5):
        self.a = a if isinstance(a, F) else F(a)
        self.b = b if isinstance(b, F) else F(b)
        self.r = r

    def _c(self, o):
        return o if isinstance(o, Q) else Q(o, 0, self.r)

    def __add__(self, o): o = self._c(o); return Q(self.a + o.a, self.b + o.b, self.r)
    __radd__ = __add__
    def __sub__(self, o): o = self._c(o); return Q(self.a - o.a, self.b - o.b, self.r)
    def __rsub__(self, o): return self._c(o) - self
    def __neg__(self): return Q(-self.a, -self.b, self.r)

    def __mul__(self, o):
        o = self._c(o)
        return Q(self.a * o.a + self.r * self.b * o.b, self.a * o.b + self.b * o.a, self.r)
    __rmul__ = __mul__

    def conj(self): return Q(self.a, -self.b, self.r)
    def norm(self): return self.a * self.a - self.r * self.b * self.b

    def __truediv__(self, o):
        o = self._c(o); n = o.norm()
        if n == 0: raise ZeroDivisionError
        p = self * o.conj(); return Q(p.a / n, p.b / n, self.r)
    def __rtruediv__(self, o): return self._c(o) / self

    def sign(self):
        a, b = self.a, self.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        # opposite signs: compare a^2 with r b^2
        d = a * a - self.r * b * b
        if d == 0: return 0
        return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)

    def __eq__(self, o): o = self._c(o); return self.a == o.a and self.b == o.b
    def __hash__(self): return hash((self.a, self.b))
    def __lt__(self, o): return (self - o).sign() < 0
    def __le__(self, o): return (self - o).sign() <= 0
    def __gt__(self, o): return (self - o).sign() > 0
    def __ge__(self, o): return (self - o).sign() >= 0
    def iszero(self): return self.a == 0 and self.b == 0
    def __float__(self): return float(self.a) + float(self.b) * self.r ** 0.5
    def __repr__(self):
        if self.b == 0: return str(self.a)
        return f"({self.a}{'+' if self.b >= 0 else '-'}{abs(self.b)}*sqrt{self.r})"


def dot(u, v):
    s = u[0] * v[0]
    for i in range(1, len(u)): s = s + u[i] * v[i]
    return s


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def solve3(A, b):
    """Cramer for 3x3 with entries in Q(sqrt r)."""
    def det(M):
        return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    D = det(A)
    if D.iszero(): return None
    out = []
    for k in range(3):
        M = [list(row) for row in A]
        for i in range(3): M[i][k] = b[i]
        out.append(det(M) / D)
    return tuple(out)


def nullspace(rows, ncols, zero, one):
    """Exact row reduction over a field; returns a basis of the null space of the matrix `rows`."""
    M = [list(r) for r in rows]; piv = []; r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(M)):
            if not M[i][c].iszero() if hasattr(M[i][c], 'iszero') else M[i][c] != 0:
                p = i; break
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        inv = one / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r:
                f = M[i][c]
                if (f.iszero() if hasattr(f, 'iszero') else f == 0): continue
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fc in free:
        v = [zero] * ncols; v[fc] = one
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        basis.append(v)
    return basis
