# qf.py for the replay of 2026-11-13-platonic-fans-law (exec'd by fans_law.py): the field class QF and its helpers now come from the
# shape kernel (kernel/exact.py, kernel/vec.py), with the original's printed form, hash and class-level field D.
from fractions import Fraction as Fr
import math
from kernel.exact import Quad, parse_sympy as _parse_sympy, cos2_exact, rational_pi as _rational_pi, rational_pi_float
from kernel import vec as _vec

class QF(Quad):
    """a + b sqrt(d); d is fixed per field (class attribute set by field())."""
    __slots__ = ()
    D = 5; STYLE = 'a + (b)*sqrt(d)'; HASH_PAIR = True

FIELDS = {'Q': 1, 'Q(sqrt(5))': 5, 'Q(sqrt(3))': 3, 'Q(sqrt(2))': 2}
def field(name):
    """set the field; returns d or None (not quadratic: float only)"""
    d = FIELDS.get(name)
    if d is not None: QF.D = d if d != 1 else 5
    return d
def parse(s): return _parse_sympy(s, QF.D, cls=QF)
def vsub(p, q): return _vec.sub(p, q, out=list)
def vadd(p, q): return _vec.add(p, q, out=list)
def vmul(p, k): return _vec.mulk(p, k, out=list)
dot = _vec.dot3
def cross(p, q): return _vec.cross(p, q, out=list)
det3 = _vec.det3
def rational_pi(c2, theta): return _rational_pi(c2, theta, field_d=QF.D)
