"""Exact arithmetic in Q(g), g^2 = D (D a rational number, not necessarily square-free).
Elements a + b g with a, b Fractions.  Pure standard library, no floats anywhere."""
from fractions import Fraction as Fr


class QF:
    D = None  # set per field with QF.field(D)

    def __init__(self, a, b=0):
        self.a = Fr(a); self.b = Fr(b)

    @classmethod
    def field(cls, D):
        return type('QF_' + str(abs(hash(Fr(D))) % 10**6), (cls,), {'D': Fr(D)})

    def _c(self, o):
        return o if isinstance(o, QF) else type(self)(o)

    def __add__(self, o): o = self._c(o); return type(self)(self.a + o.a, self.b + o.b)
    __radd__ = __add__
    def __neg__(self): return type(self)(-self.a, -self.b)
    def __sub__(self, o): return self + (-self._c(o))
    def __rsub__(self, o): return self._c(o) - self
    def __mul__(self, o):
        o = self._c(o); D = self.D
        return type(self)(self.a * o.a + self.b * o.b * D, self.a * o.b + self.b * o.a)
    __rmul__ = __mul__
    def inv(self):
        n = self.a * self.a - self.b * self.b * self.D
        if n == 0: raise ZeroDivisionError('zero divisor in Q(sqrt D)')
        return type(self)(self.a / n, -self.b / n)
    def __truediv__(self, o): return self * self._c(o).inv()
    def __rtruediv__(self, o): return self._c(o) * self.inv()
    def __pow__(self, k):
        r = type(self)(1)
        for _ in range(k): r = r * self
        return r
    def is_zero(self): return self.a == 0 and self.b == 0
    def __float__(self):
        import math
        return float(self.a) + float(self.b) * math.sqrt(float(self.D))
    def __lt__(self, o): return exact_sign(self - self._c(o)) < 0
    def __le__(self, o): return exact_sign(self - self._c(o)) <= 0
    def __gt__(self, o): return exact_sign(self - self._c(o)) > 0
    def __repr__(self): return f'({self.a}) + ({self.b})*sqrt({self.D})'


def exact_sign(z):
    """Exact sign of a + b sqrt(D), D > 0, by comparing squares (no floats)."""
    a, b, D = z.a, z.b, z.D
    sa = (a > 0) - (a < 0); sb = (b > 0) - (b < 0)
    if sb == 0: return sa
    if sa == 0 or sa == sb: return sb if sa == 0 else sa
    # opposite signs: compare a^2 with b^2 D
    c = a * a - b * b * D
    return sa if c > 0 else (sb if c < 0 else 0)
