"""Exact arithmetic in Q(sqrt5): a + b*sqrt5 with Fraction a, b."""
from fractions import Fraction as F
class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = F(a); s.b = F(b)
    def _c(o): return o if isinstance(o, Q5) else Q5(o)
    def __add__(s, o): o = Q5._c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q5(-s.a, -s.b)
    def __sub__(s, o): return s + (-Q5._c(o))
    def __rsub__(s, o): return Q5._c(o) - s
    def __mul__(s, o): o = Q5._c(o); return Q5(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def conj(s): return Q5(s.a, -s.b)          # Galois: sqrt5 -> -sqrt5
    def norm(s): return s.a*s.a - 5*s.b*s.b
    def inv(s): n = s.norm(); return Q5(s.a/n, -s.b/n)
    def __truediv__(s, o): return s * Q5._c(o).inv()
    def __rtruediv__(s, o): return Q5._c(o) * s.inv()
    def __eq__(s, o): o = Q5._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def iszero(s): return s.a == 0 and s.b == 0
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def sign(s):
        # exact sign of a + b sqrt5
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        c = a*a - 5*b*b
        return (1 if a > 0 else -1) * ((c > 0) - (c < 0))
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f'{s.b}*r5'
        return f'({s.a}{"+" if s.b > 0 else "-"}{abs(s.b)}*r5)'
PHI = Q5(F(1, 2), F(1, 2))
def dot(x, y):
    r = Q5()
    for p, q in zip(x, y): r = r + p*q
    return r
def gegenbauer(kmax, lam, x):
    """C_k^lam(x), k = 0..kmax (lam = (d-2)/2; for d = 4 these are Chebyshev U_k)."""
    out = [Q5(1), Q5(2*lam)*x]
    for n in range(2, kmax + 1):
        out.append((Q5(2*(n + lam - 1))*x*out[-1] - Q5(n + 2*lam - 2)*out[-2]) / n)
    return out[:kmax + 1]
