# Mutant for the harness self-test: a Q5 copy whose sign rule compares a with b (not a^2 with 5 b^2). The differential test must flag it.
from fractions import Fraction as Fr
class Q5:
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): return Q5(s.a + o.a, s.b + o.b)
    def __mul__(s, o): return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) if abs(a) > abs(b) else (1 if b > 0 else -1)
