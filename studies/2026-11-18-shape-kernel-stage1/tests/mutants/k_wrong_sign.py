# Mutant for the harness self-test (G4): a K = Q(sqrt2, sqrt5) whose sign compares P^2 with 2 Q^2 instead of 5 Q^2.
from fractions import Fraction as Fr
def _s2sign(p, q):
    if p >= 0 and q >= 0: return 0 if (p == 0 and q == 0) else 1
    if p <= 0 and q <= 0: return -1
    d = p * p - 2 * q * q
    return (1 if p > 0 else -1) if d > 0 else (-1 if p > 0 else 1) if d < 0 else 0
class K:
    __slots__ = ('v',)
    def __init__(s, a=0, b=0, c=0, d=0): s.v = (Fr(a), Fr(b), Fr(c), Fr(d))
    @staticmethod
    def c(x): return x if isinstance(x, K) else K(x)
    def __add__(s, o): o = K.c(o); return K(*(x + y for x, y in zip(s.v, o.v)))
    def __mul__(s, o):
        o = K.c(o); a, b, c, d = s.v; e, f, g, h = o.v
        return K(a*e + 2*b*f + 5*c*g + 10*d*h, a*f + b*e + 5*(c*h + d*g), a*g + c*e + 2*(b*h + d*f), a*h + d*e + b*g + c*f)
    def sign(s):
        a, b, c, d = s.v
        sp, sq = _s2sign(a, b), _s2sign(c, d)
        if sq == 0: return sp
        if sp == 0 or sp == sq: return sq if sp == 0 else sp
        P2 = K(a, b) * K(a, b); Q2 = K(c, d) * K(c, d) * 2
        t = _s2sign(*(P2 + Q2 * (-1)).v[:2])
        return sp if t > 0 else sq if t < 0 else 0
def kstr(x): return repr(x.v)
