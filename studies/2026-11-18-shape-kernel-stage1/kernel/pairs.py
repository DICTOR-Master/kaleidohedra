"""Q(sqrt5) as Fraction pairs (a, b) = a + b sqrt5: the function names of the pair-style copies (group G3), computed by the kernel.
Every function takes and returns plain tuples of Fractions, exactly as the copies do, so a study can switch with one import line.
Name clash in the copies: qstr is a sqrt5 text in reuleaux/aristotle, a 'a|b (float)' text in the fable reviews; here qstr is the
first and qstr_float the second."""
from fractions import Fraction as Fr
import functools
from .exact import Quad

D = 5
Z = (Fr(0), Fr(0)); ONE = (Fr(1), Fr(0)); PHI = (Fr(1, 2), Fr(1, 2)); IPHI = (Fr(-1, 2), Fr(1, 2))


def _q(x): return Quad(x[0], x[1], D)
def _p(x): return (x.a, x.b)


def q(s):
    """'a|b' -> (a, b)"""
    a, b = s.split('|'); return (Fr(a), Fr(b))
def qs_(x): return f'{x[0]}|{x[1]}'
def qa(x, y): return _p(_q(x) + _q(y))
def qs(x, y): return _p(_q(x) - _q(y))
def qm(x, y): return _p(_q(x) * _q(y))
def qn(x): return _p(-_q(x))
def qr(r): return (Fr(r), Fr(0))
def qinv(x): return _p(_q(x).inv())
def qd(x, y): return _p(_q(x) / _q(y))
def qf(x): return float(_q(x))
def sgn(x): return _q(x).sign()
qsgn = sgn
def cmp(x, y): return _q(x)._cmp(_q(y))
def qsum(xs): return functools.reduce(qa, xs, Z)
def qconj(x): return (x[0], -x[1])
def qnorm(x): return _q(x).norm()
def qstr(x):
    a, b = x
    return f'{a}' if b == 0 else f'{a} + {b}*sqrt5' if a != 0 else f'{b}*sqrt5'
def qstr_float(x): return qs_(x) + f' ({qf(x):.9f})'
