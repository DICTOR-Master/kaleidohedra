# Mutant for the harness self-test (G8): a Q(sqrt D) class whose inverse uses a^2 + D b^2 instead of a^2 - D b^2.
from fractions import Fraction as Fr
class QD:
    __slots__ = ('a', 'b', 'D')
    def __init__(s, a=0, b=0, D=0): s.a = Fr(a); s.b = Fr(b); s.D = D
    def c(s, o): return o if isinstance(o, QD) else QD(o, 0, s.D)
    def __add__(s, o): o = s.c(o); return QD(s.a + o.a, s.b + o.b, s.D or o.D)
    def __mul__(s, o): o = s.c(o); D = s.D or o.D; return QD(s.a * o.a + D * s.b * o.b, s.a * o.b + s.b * o.a, D)
    def inv(s): n = s.a * s.a + s.D * s.b * s.b; return QD(s.a / n, -s.b / n, s.D)
