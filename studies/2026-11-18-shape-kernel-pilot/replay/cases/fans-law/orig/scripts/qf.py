# Exact arithmetic in a real quadratic field Q(sqrt d) (d = 1 means Q), with exact sign. Used by every DICTO Vacuus script.
from fractions import Fraction as Fr
import math

class QF:
    """a + b sqrt(d); d is fixed per field (class attribute set by field())."""
    __slots__ = ('a', 'b')
    D = 5
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def _c(s, o): return o if isinstance(o, QF) else QF(o)
    def __add__(s, o): o = s._c(o); return QF(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = s._c(o); return QF(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return s._c(o) - s
    def __neg__(s): return QF(-s.a, -s.b)
    def __mul__(s, o): o = s._c(o); return QF(s.a * o.a + QF.D * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = s._c(o); n = o.a * o.a - QF.D * o.b * o.b
        return QF((s.a * o.a - QF.D * s.b * o.b) / n, (s.b * o.a - s.a * o.b) / n)
    def __rtruediv__(s, o): return s._c(o) / s
    def sign(s):
        a, b = s.a, s.b
        if b == 0 or QF.D == 1:
            v = a + (b if QF.D == 1 else 0); return (v > 0) - (v < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        d = a * a - QF.D * b * b
        return ((d > 0) - (d < 0)) if a > 0 else -((d > 0) - (d < 0))
    def __float__(s): return float(s.a) + float(s.b) * math.sqrt(QF.D)
    def __eq__(s, o): o = s._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __lt__(s, o): return (s - o).sign() < 0
    def __str__(s):
        if s.b == 0: return f'{s.a}'
        return f'{s.a} + ({s.b})*sqrt({QF.D})'

FIELDS = {'Q': 1, 'Q(sqrt(5))': 5, 'Q(sqrt(3))': 3, 'Q(sqrt(2))': 2}
def field(name):
    """set the field; returns d or None (not quadratic: float only)"""
    d = FIELDS.get(name)
    if d is not None: QF.D = d if d != 1 else 5          # Q: any d works (b = 0 throughout); keep 5 so parse is uniform
    return d
def parse(s):
    import sympy as sp
    d = QF.D; r = sp.sqrt(d); e = sp.expand(sp.sympify(s, locals={'sqrt': sp.sqrt})); b = e.coeff(r); a = sp.expand(e - b * r)
    if not (a.is_Rational and b.is_Rational): raise ValueError(f'not in Q(sqrt{d}): ' + s)
    return QF(Fr(int(a.p), int(a.q)), Fr(int(b.p), int(b.q)))
def vsub(p, q): return [p[i] - q[i] for i in range(3)]
def vadd(p, q): return [p[i] + q[i] for i in range(3)]
def vmul(p, k): return [x * k for x in p]
def dot(p, q): return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]
def cross(p, q): return [p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0]]
def det3(a, b, c): return dot(a, cross(b, c))

# cos(2 theta) of a rational multiple of pi lying in a quadratic field: cos(2 pi k / n) with phi(n) <= 4, n in 1,2,3,4,5,6,8,10,12
def cos2_exact(frac):
    """cos(2 pi * frac) as (a, b, d) with value a + b sqrt d, for denominators 1..12 with phi(n) <= 4"""
    n = frac.denominator; k = frac.numerator % n
    t = {1: {0: (1, 0, 1)}, 2: {1: (-1, 0, 1)}, 3: {1: (Fr(-1, 2), 0, 1), 2: (Fr(-1, 2), 0, 1)}, 4: {1: (0, 0, 1), 3: (0, 0, 1)},
         6: {1: (Fr(1, 2), 0, 1), 5: (Fr(1, 2), 0, 1)},
         5: {1: (Fr(-1, 4), Fr(1, 4), 5), 4: (Fr(-1, 4), Fr(1, 4), 5), 2: (Fr(-1, 4), Fr(-1, 4), 5), 3: (Fr(-1, 4), Fr(-1, 4), 5)},
         10: {1: (Fr(1, 4), Fr(1, 4), 5), 9: (Fr(1, 4), Fr(1, 4), 5), 3: (Fr(1, 4), Fr(-1, 4), 5), 7: (Fr(1, 4), Fr(-1, 4), 5)},
         8: {1: (0, Fr(1, 2), 2), 7: (0, Fr(1, 2), 2), 3: (0, Fr(-1, 2), 2), 5: (0, Fr(-1, 2), 2)},
         12: {1: (0, Fr(1, 2), 3), 11: (0, Fr(1, 2), 3), 5: (0, Fr(-1, 2), 3), 7: (0, Fr(-1, 2), 3)}}
    return t[n][k]
def rational_pi(c2, theta):
    """exact test: is theta (in [0, pi]) a rational multiple of pi, given c2 = cos(2 theta) exactly in QF? returns 'k/n' (of pi) or None.
    Niven-type: cos(2 theta) has degree <= 2 over Q, so 2 theta = 2 pi k / n with phi(n) <= 4."""
    for n in (1, 2, 3, 4, 5, 6, 8, 10, 12):
        for k in range(n):
            if math.gcd(k, n) != 1 and not (k == 0 and n == 1): continue
            a, b, d = cos2_exact(Fr(k, n))
            if b != 0 and d != QF.D: continue
            if c2.a == Fr(a) and c2.b == Fr(b):
                # theta in [0, pi]: 2 theta = 2 pi k/n or 2 pi (n-k)/n; pick the one matching the float
                for m in (Fr(k, n), 1 - Fr(k, n)):
                    if abs(float(m) * math.pi - theta) < 1e-7: return f'{m.numerator}/{m.denominator}' if m.denominator != 1 else f'{m.numerator}'
    return None
def rational_pi_float(theta, qmax=360, tol=1e-9):
    for q in range(1, qmax + 1):
        p = round(theta / math.pi * q)
        if abs(p / q * math.pi - theta) < tol and math.gcd(p, q) == 1: return f'{p}/{q}' if q != 1 else f'{p}'
    return None
