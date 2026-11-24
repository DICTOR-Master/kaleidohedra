"""Exact field helpers: Q (Fraction) and Q(sqrt2) (pairs of Fractions)."""
from fractions import Fraction as Fr


class Q2:
    """a + b*sqrt(2), a, b rational."""
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = Fr(a); self.b = Fr(b)

    def _c(self, o):
        return o if isinstance(o, Q2) else Q2(o)

    def __add__(self, o): o = self._c(o); return Q2(self.a + o.a, self.b + o.b)
    __radd__ = __add__
    def __sub__(self, o): o = self._c(o); return Q2(self.a - o.a, self.b - o.b)
    def __rsub__(self, o): return self._c(o) - self
    def __neg__(self): return Q2(-self.a, -self.b)
    def __mul__(self, o):
        o = self._c(o)
        return Q2(self.a * o.a + 2 * self.b * o.b, self.a * o.b + self.b * o.a)
    __rmul__ = __mul__
    def __truediv__(self, o):
        o = self._c(o)
        n = o.a * o.a - 2 * o.b * o.b  # nonzero for o != 0 since sqrt2 irrational
        return self * Q2(o.a / n, -o.b / n)
    def __eq__(self, o): o = self._c(o); return self.a == o.a and self.b == o.b
    def __hash__(self): return hash((self.a, self.b))
    def iszero(self): return self.a == 0 and self.b == 0
    def positive(self):
        a, b = self.a, self.b
        if a >= 0 and b >= 0:
            return a > 0 or b > 0
        if a > 0 and b < 0:
            return a * a > 2 * b * b
        if a < 0 and b > 0:
            return 2 * b * b > a * a
        return False

    def __lt__(self, o): return (self._c(o) - self).positive()

    def __repr__(self): return f"({self.a}+{self.b}r2)"


def iszero(x):
    return x.iszero() if isinstance(x, Q2) else x == 0


def rref(rows):
    """Row-reduce a list of lists over the field; return (reduced rows, pivot cols)."""
    M = [list(r) for r in rows]
    piv = []
    r = 0
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(M)) if not iszero(M[i][c])), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c] if not isinstance(M[r][c], Q2) else Q2(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and not iszero(M[i][c]):
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def rank(rows):
    return len(rref(rows)[1]) if rows else 0


def nullspace(rows, ncol):
    R, piv = rref(rows)
    free = [c for c in range(ncol) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * ncol
        v[f] = Fr(1)
        for i, pc in enumerate(piv):
            v[pc] = -R[i][f]
        basis.append(v)
    return basis


def normalize(v):
    """Scale a nonzero vector so its first nonzero entry is 1 (a key up to scale and sign)."""
    k = next(x for x in v if not iszero(x))
    inv = (Q2(1) / k) if isinstance(k, Q2) else 1 / k
    w = [x * inv for x in v]
    if any(isinstance(x, Q2) for x in w):  # one type per key, so hashes agree
        w = [x if isinstance(x, Q2) else Q2(x) for x in w]
    return tuple(w)
