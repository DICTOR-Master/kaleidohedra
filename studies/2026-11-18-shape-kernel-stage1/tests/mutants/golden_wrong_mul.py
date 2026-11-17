# Mutant for the harness self-test (G5): a golden-basis Q5 whose product drops the b*d term of phi^2 = phi + 1 in the phi part.
from fractions import Fraction as Fr
class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return Q5(s.a + o.a, s.b + o.b)
    def __mul__(s, o): return Q5(s.a*o.a + s.b*o.b, s.a*o.b + s.b*o.a)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
