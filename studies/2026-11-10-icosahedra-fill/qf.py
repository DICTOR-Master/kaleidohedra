# Exact arithmetic in a real quadratic field Q(sqrt d): numbers a + b*sqrt(d) with Fraction a, b.
# Comparisons are exact (sign of a + b sqrt d decided by squaring), so sorting and floor are exact.
from fractions import Fraction as Fr
import math


class QF:
    __slots__ = ('a', 'b', 'd')

    def __init__(self, a, b=0, d=5):
        self.a = Fr(a); self.b = Fr(b); self.d = d

    def _c(self, o):
        if isinstance(o, QF):
            if o.d != self.d and o.b != 0 and self.b != 0:
                raise ValueError('mixed fields')
            return o
        return QF(o, 0, self.d)

    def __add__(self, o): o = self._c(o); return QF(self.a + o.a, self.b + o.b, self.d)
    __radd__ = __add__
    def __sub__(self, o): o = self._c(o); return QF(self.a - o.a, self.b - o.b, self.d)
    def __rsub__(self, o): return self._c(o) - self
    def __neg__(self): return QF(-self.a, -self.b, self.d)
    def __mul__(self, o):
        o = self._c(o); return QF(self.a * o.a + self.d * self.b * o.b, self.a * o.b + self.b * o.a, self.d)
    __rmul__ = __mul__
    def conj(self): return QF(self.a, -self.b, self.d)
    def norm(self): return self.a * self.a - self.d * self.b * self.b
    def __truediv__(self, o):
        o = self._c(o); n = o.norm()
        if n == 0: raise ZeroDivisionError
        return self * QF(o.a / n, -o.b / n, self.d)
    def __rtruediv__(self, o): return self._c(o) / self

    def sign(self):
        a, b = self.a, self.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        # opposite signs: compare a^2 with d b^2
        s = a * a - self.d * b * b
        if s == 0: return 0
        return (1 if a > 0 else -1) if s > 0 else (1 if b > 0 else -1)

    def __eq__(self, o):
        if not isinstance(o, (QF, int, Fr)): return NotImplemented
        return (self - o).sign() == 0
    def __hash__(self): return hash((self.a, self.b if self.b != 0 else 0))
    def __lt__(self, o): return (self - o).sign() < 0
    def __le__(self, o): return (self - o).sign() <= 0
    def __gt__(self, o): return (self - o).sign() > 0
    def __ge__(self, o): return (self - o).sign() >= 0
    def __float__(self): return float(self.a) + float(self.b) * math.sqrt(self.d)

    def floor(self):
        n = math.floor(float(self))
        while QF(n, 0, self.d) > self: n -= 1
        while QF(n + 1, 0, self.d) <= self: n += 1
        return n

    def __repr__(self):
        if self.b == 0: return str(self.a)
        return f'{self.a} + {self.b}*sqrt({self.d})' if self.a != 0 else f'{self.b}*sqrt({self.d})'
    def tex(self):
        return repr(self)


def fl(x):
    """floor for Fraction or QF"""
    if isinstance(x, QF): return x.floor()
    return math.floor(x)


def frac(x):
    return x - fl(x)
