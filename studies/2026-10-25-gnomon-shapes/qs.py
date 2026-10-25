# Exact arithmetic in Q(√5): numbers a + b√5 with a, b rational (Fractions). Exact sign, square roots, φ-power recognition.
from fractions import Fraction as F
import math

class Q:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a, s.b = F(a), F(b)
    @staticmethod
    def c(x): return x if isinstance(x, Q) else Q(x)
    def __add__(s, o): o = Q.c(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = Q.c(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q.c(o) - s
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): o = Q.c(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def norm(s): return s.a * s.a - 5 * s.b * s.b
    def __truediv__(s, o):
        o = Q.c(o); n = o.norm()
        if n == 0: raise ZeroDivisionError
        return s * Q(o.a / n, -o.b / n)
    def __rtruediv__(s, o): return Q.c(o) / s
    def __eq__(s, o): o = Q.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        # exact sign of a + b√5
        sa = (s.a > 0) - (s.a < 0); sb = (s.b > 0) - (s.b < 0)
        if sb == 0: return sa
        if sa == 0: return sb
        if sa == sb: return sa
        # opposite signs: compare a² with 5b²
        return sa if s.a * s.a > 5 * s.b * s.b else (sb if s.a * s.a < 5 * s.b * s.b else 0)
    def __lt__(s, o): return (s - o).sign() < 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def f(s): return float(s.a) + float(s.b) * 5 ** .5
    def __repr__(s):
        if s.b == 0: return f'{s.a}'
        if s.a == 0: return f'{s.b}√5'
        return f'{s.a} {"+" if s.b > 0 else "−"} {abs(s.b)}√5'

PHI = Q(F(1, 2), F(1, 2))

def qsqrt_rat(x):
    x = F(x)
    if x < 0: return None
    n, d = x.numerator, x.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    return F(rn, rd) if rn * rn == n and rd * rd == d else None

def qsqrt(z):
    """exact square root in Q(√5) (positive), or None if z is not a square there"""
    z = Q.c(z)
    if z.sign() < 0: return None
    if z == 0: return Q(0)
    r = qsqrt_rat(z.norm())
    if r is None: return None
    for x2 in ((z.a + r) / 2, (z.a - r) / 2):
        x = qsqrt_rat(x2)
        if x is None: continue
        for xx in ([x, -x] if x != 0 else [x]):
            if xx != 0:
                y = z.b / (2 * xx)
                if xx * xx + 5 * y * y == z.a:
                    w = Q(xx, y)
                    return w if w.sign() > 0 else -w
            else:
                y = qsqrt_rat(z.a / 5)
                if y is not None and z.b == 0: return Q(0, y)
    return None

def phi_form(z, kmax=30):
    """'q·φ^k' if z = q·φ^k (q rational, k integer, |k| ≤ kmax), else ''"""
    z = Q.c(z)
    if z == 0: return '0'
    p = Q(1)
    pw = [Q(1)]
    for _ in range(kmax): p = p * PHI; pw.append(p)
    for k in range(0, kmax + 1):
        for sgn, w in ((1, pw[k]), (-1, Q(1) / pw[k])):
            q = z / w
            if q.b == 0:
                kk = k * sgn
                qs = '' if q.a == 1 else f'{q.a}·'
                return f'{qs}φ^{kk}' if kk != 0 else f'{q.a}'
    return ''

def pretty(z):
    s = phi_form(z)
    return f'{z!r}' + (f' = {s}' if s and s != f'{Q.c(z).a}' else '')
