# Mutant for the harness self-test: a QF copy with the field parameter dropped from the product (b b' d term uses 5 always).
from fractions import Fraction as Fr
class QF:
    D = 5
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): return QF(s.a + o.a, s.b + o.b)
    def __mul__(s, o): return QF(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
