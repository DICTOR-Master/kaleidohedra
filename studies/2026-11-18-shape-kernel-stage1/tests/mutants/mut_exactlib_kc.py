# Mutant for the harness self-test (G7): a KC whose norm has the wrong sign on the 3kabc term (so its sign rule is wrong).
from fractions import Fraction as Fr
class KC:
    __slots__ = ('c', 'k')
    def __init__(s, a=0, b=0, c=0, k=2): s.c = (Fr(a), Fr(b), Fr(c)); s.k = k
    def _c(s, o): return o if isinstance(o, KC) else KC(o, 0, 0, s.k)
    def __add__(s, o): o = s._c(o); return KC(*(x + y for x, y in zip(s.c, o.c)), k=s.k)
    def __mul__(s, o):
        o = s._c(o); (a, b, c), (x, y, z), k = s.c, o.c, s.k
        return KC(a * x + k * (b * z + c * y), a * y + b * x + k * c * z, a * z + b * y + c * x, k=k)
    def norm(s):
        (a, b, c), k = s.c, s.k
        return a ** 3 + k * b ** 3 + k * k * c ** 3 + 3 * k * a * b * c
    def sign(s): n = s.norm(); return (n > 0) - (n < 0)
    def __eq__(s, o): o = s._c(o); return s.c == o.c
