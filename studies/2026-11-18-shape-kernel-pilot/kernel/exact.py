"""Exact numbers for the shape kernel (pilot, 2026-11-18): Q and the real quadratic fields Q(sqrt d).

One element type, Quad(a, b, d) = a + b*sqrt(d), with a, b Fractions and d a positive rational that is not a square
(d = 2, 3, 5, 6 are the fields of the studies; any such d works).  Rationals are the elements with b = 0; they combine
with any field.  Two elements with irrational parts in different fields raise ValueError (no silent mixing).

Everything that decides is exact: sign, comparisons, equality, floor.  Floats appear only in float(x) / x.f(), on request.
Built from the three most-copied exact-number groups of the studies (see README): the Q5 / Q classes, the QF classes and
the Fraction-pair functions; the pair functions live in kernel/pairs.py, vectors in kernel/vec.py.

Exact sign of a + b sqrt d (the rule every copy uses): if a and b have the same sign (or one is 0) the sign is theirs;
otherwise the term with the larger square wins, i.e. compare a^2 with d b^2 (never equal, since d is not a square).
"""
from fractions import Fraction as Fr
from decimal import Decimal
import math

__all__ = ['Quad', 'fmt', 'STYLES', 'q5', 'qf', 'PHI', 'IPHI', 'R2', 'R3', 'R5', 'R6', 'ZERO', 'ONE',
           'parse', 'parse_sympy', 'cos2_exact', 'rational_pi', 'rational_pi_float', 'floor', 'frac']


def _fr(x):
    if isinstance(x, Fr): return x
    if isinstance(x, bool): return Fr(int(x))
    return Fr(x)                         # int, str ('3/4', '0.25'), float (exact binary value), Decimal


def _rat_sqrt(d):
    """sqrt of a positive Fraction if it is rational, else None"""
    n, m = d.numerator, d.denominator
    rn, rm = math.isqrt(n), math.isqrt(m)
    return Fr(rn, rm) if rn * rn == n and rm * rm == m else None


_FIELD_CACHE = {}


def _field(d):
    """validate a field parameter; returns (d as int or Fraction, rational sqrt or None)"""
    r = _FIELD_CACHE.get(d)
    if r is not None: return r
    D = _fr(d)
    if D <= 0: raise ValueError(f'field parameter must be positive: {d}')
    Dn = int(D) if D.denominator == 1 else D
    r = (Dn, _rat_sqrt(D))
    _FIELD_CACHE[d] = r
    return r


class Quad:
    """a + b*sqrt(d).  Quad(a) is rational; Quad(a, b) uses the class default field D (5); Quad(a, b, d) any field."""
    __slots__ = ('a', 'b', 'd')
    D = 5                    # default field for new elements (copies that set QF.D per run do the same here)
    HASH_PAIR = False        # False: hash(x) == hash(a) when b == 0 (consistent with x == a); True: hash((a, b)) as most copies
    STYLE = 'kernel'         # repr style, see STYLES

    def __init__(s, a=0, b=0, d=None):
        if isinstance(a, Quad):
            if b != 0: raise TypeError('Quad(Quad, b) is ambiguous')
            s.a, s.b, s.d = a.a, a.b, a.d if d is None else _field(d)[0]
            return
        D, r = _field(type(s).D if d is None else d)
        A, B = _fr(a), _fr(b)
        if B != 0 and r is not None: A, B = A + B * r, Fr(0)     # d a square: the number is rational
        s.a, s.b, s.d = A, B, D

    # -- coercion ------------------------------------------------------------------------------------------------
    def _new(s, a, b, d, other=None):
        # result class: the more derived of the two operands' classes, so a study's subclass (its own repr) survives Quad + subclass
        cls = type(other) if other is not None and type(other) is not type(s) and issubclass(type(other), type(s)) else type(s)
        o = object.__new__(cls); o.a, o.b, o.d = a, b, d; return o

    def _c(s, o):
        if isinstance(o, Quad): return o
        if isinstance(o, (int, Fr)): return s._new(_fr(o), Fr(0), s.d)
        if isinstance(o, float): raise TypeError('exact only: convert floats explicitly with Quad(Fraction(x))')
        return NotImplemented

    @classmethod
    def c(cls, x):
        """x as an element of this class (copies: Q5.c, QF.of, q(x))"""
        return x if isinstance(x, Quad) else cls(x)
    of = c

    def _join(s, o):
        if s.b == 0: return o.d if o.b != 0 else s.d
        if o.b == 0 or o.d == s.d: return s.d
        raise ValueError(f'mixed fields: sqrt({s.d}) and sqrt({o.d})')

    # -- arithmetic -----------------------------------------------------------------------------------------------
    def __add__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return s._new(s.a + o.a, s.b + o.b, s._join(o), o)
    __radd__ = __add__

    def __sub__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return s._new(s.a - o.a, s.b - o.b, s._join(o), o)

    def __rsub__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return o - s

    def __neg__(s): return s._new(-s.a, -s.b, s.d)
    def __pos__(s): return s

    def __mul__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        d = s._join(o)
        return s._new(s.a * o.a + d * s.b * o.b, s.a * o.b + s.b * o.a, d, o)
    __rmul__ = __mul__

    def norm(s):
        """field norm a^2 - d b^2 (a Fraction); zero only for 0"""
        return s.a * s.a - s.d * s.b * s.b

    def trace(s): return 2 * s.a

    def conj(s):
        """Galois conjugate a - b sqrt d (copies: conj, gal, sig)"""
        return s._new(s.a, -s.b, s.d)
    gal = sig = conj

    def inv(s):
        n = s.norm()
        if n == 0: raise ZeroDivisionError('Quad division by zero')
        return s._new(s.a / n, -s.b / n, s.d)

    def __truediv__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        s._join(o)
        return s * o.inv()

    def __rtruediv__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return o * s.inv()

    def __pow__(s, k):
        if not isinstance(k, int): raise TypeError('integer powers only')
        if k < 0: return s.inv() ** (-k)
        r = s._new(Fr(1), Fr(0), s.d); x = s
        while k:
            if k & 1: r = r * x
            x = x * x; k >>= 1
        return r

    # -- exact decisions ------------------------------------------------------------------------------------------
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) if a * a > s.d * b * b else (1 if b > 0 else -1)

    def iszero(s): return s.a == 0 and s.b == 0
    is_zero = zero = z = iszero
    def __bool__(s): return not s.iszero()
    def is_rational(s): return s.b == 0
    def is_int(s): return s.b == 0 and s.a.denominator == 1
    def key(s): return (s.a, s.b)

    def __eq__(s, o):
        o = s._c(o) if not isinstance(o, float) else NotImplemented
        if o is NotImplemented: return NotImplemented
        if s.b == 0 and o.b == 0: return s.a == o.a
        return s.a == o.a and s.b == o.b and s.d == o.d

    def __ne__(s, o):
        r = s.__eq__(o)
        return r if r is NotImplemented else not r

    def __hash__(s):
        if s.b == 0 and not type(s).HASH_PAIR: return hash(s.a)
        return hash((s.a, s.b))

    def _cmp(s, o):
        o = s._c(o) if not isinstance(o, float) else NotImplemented
        if o is NotImplemented: return None
        return (s - o).sign()

    def __lt__(s, o): c = s._cmp(o); return NotImplemented if c is None else c < 0
    def __le__(s, o): c = s._cmp(o); return NotImplemented if c is None else c <= 0
    def __gt__(s, o): c = s._cmp(o); return NotImplemented if c is None else c > 0
    def __ge__(s, o): c = s._cmp(o); return NotImplemented if c is None else c >= 0
    def __abs__(s): return -s if s.sign() < 0 else s

    def floor(s):
        """exact floor (an int)"""
        a, b, d = s.a, s.b, s.d
        if b == 0: return math.floor(a)
        x = b * b * _fr(d)                                   # |b| sqrt d = sqrt(x)
        r = math.isqrt(x.numerator * x.denominator) // x.denominator   # floor(sqrt(x))
        n = math.floor(a) + (r if b > 0 else -r - 1)          # within 2 of the answer
        while s._new(Fr(n), Fr(0), d) > s: n -= 1
        while s._new(Fr(n + 1), Fr(0), d) <= s: n += 1
        return n

    def ceil(s): return -(-s).floor()
    def frac(s): return s - s.floor()

    # -- conversion -----------------------------------------------------------------------------------------------
    def __float__(s): return float(s.a) + float(s.b) * math.sqrt(s.d)
    def f(s): return float(s)

    def float_hp(s):
        """float without cancellation: from >= 20 exact significant digits (as the 60-digit mpmath float of yantra_regions45);
        float(x) above is the plain a + b*sqrt(d) in doubles that most copies use, kept so their printed floats stay the same"""
        if s.b == 0: return float(s.a)
        if s.iszero(): return 0.0
        p = 20
        while True:
            n = (s * s._new(Fr(10 ** p), Fr(0), s.d)).floor()
            if abs(n) >= 10 ** 20: return float(Fr(n, 10 ** p))
            p += 20

    def digits(s, places=60):
        """exact decimal string, truncated toward minus infinity to `places` digits after the point (no float, no rounding error)"""
        n = (s * Quad(10 ** places, 0, s.d)).floor() if s.b else math.floor(s.a * 10 ** places)
        sg = '-' if n < 0 else ''; n = abs(n); t = str(n).rjust(places + 1, '0')
        return f'{sg}{t[:-places]}.{t[-places:]}' if places else f'{sg}{t}'

    def dec(s, places=15):
        """decimal string as in the exactlib copies (Decimal arithmetic, default 28-digit context, quantised)"""
        x = Decimal(s.a.numerator) / Decimal(s.a.denominator) + Decimal(s.b.numerator) / Decimal(s.b.denominator) * Decimal(s.d).sqrt()
        q = x.quantize(Decimal(1).scaleb(-places))
        return format(q, 'f') if q != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-places)), 'f')

    def sympy(s):
        import sympy as sp
        return sp.Rational(s.a.numerator, s.a.denominator) + sp.Rational(s.b.numerator, s.b.denominator) * sp.sqrt(s.d)

    def __repr__(s): return fmt(s, type(s).STYLE)
    def __str__(s): return s.__repr__()
    def tex(s): return repr(s)


# --------------------------------------------------------------------------------------------------- formatting
def _pm(b): return '+' if b > 0 else '-'
def _r(q): return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'


def _parsable(x):
    if x.b == 0: return _r(x.a)
    bs = f'sqrt({x.d})' if x.b == 1 else (f'-sqrt({x.d})' if x.b == -1 else f'({_r(x.b)})*sqrt({x.d})')
    if x.a == 0: return bs
    return f'{_r(x.a)} + {bs}' if not bs.startswith('-') else f'{_r(x.a)} - {bs[1:]}'


def _unit(x):        # 4d-shadows q5str: coefficient 1 dropped
    a, b, d = x.a, x.b, x.d
    if b == 0: return str(a)
    bs = ('' if abs(b) == 1 else str(abs(b))) + f'√{d}'
    if a == 0: return ('-' if b < 0 else '') + bs
    return f"{a} {_pm(b)} {bs}"


# Every repr found in the three groups, generalised from 5 to d (identical output for d = 5).  The keys are the output of
# 1/2 + 3/2 sqrt5 in that style, shortened; the inventory (data/differential.json) lists which copy uses which style.
STYLES = {
    'kernel': _parsable,                                                                               # 1/2 + (3/2)*sqrt(5)
    'parsable': _parsable,                                                                             # exactlib fmt
    'unit_root': _unit,                                                                                # 1/2 + 3/2√5
    'a+b*sqrtd': lambda x: str(x.a) if x.b == 0 else (f'{x.b}*sqrt{x.d}' if x.a == 0 else f'{x.a}{_pm(x.b)}{abs(x.b)}*sqrt{x.d}'),
    '(a+br5)': lambda x: f'({x.a}+{x.b}r{x.d})' if x.b else f'{x.a}',
    '(a+b*r5)': lambda x: str(x.a) if x.b == 0 else (f'{x.b}*r{x.d}' if x.a == 0 else f'({x.a}{_pm(x.b)}{abs(x.b)}*r{x.d})'),
    '(a+br5)signed': lambda x: str(x.a) if x.b == 0 else f'({x.a}{_pm(x.b)}{abs(x.b)}r{x.d})',
    'a + b*sqrtd': lambda x: str(x.a) if x.b == 0 else (f'{x.b}*sqrt{x.d}' if x.a == 0 else f'{x.a} + {x.b}*sqrt{x.d}'),
    '(a + b*sqrtd)': lambda x: f'{x.a}' if x.b == 0 else f'({x.a} + {x.b}*sqrt{x.d})',
    '(a +- b*sqrtd)': lambda x: str(x.a) if x.b == 0 else (f'{x.b}*sqrt{x.d}' if x.a == 0 else f'({x.a} {_pm(x.b)} {abs(x.b)}*sqrt{x.d})'),
    '(a+br5)always': lambda x: f'({x.a}+{x.b}r{x.d})',
    '(a) + (b)√d': lambda x: f'{x.a}' if x.b == 0 else f'({x.a}) + ({x.b})√{x.d}',
    'a + (b)*sqrt(d)': lambda x: f'{x.a}' if x.b == 0 else f'{x.a} + ({x.b})*sqrt({x.d})',
    'a+br5 omit0': lambda x: f'{x.a}' + (f"{'+' if x.b >= 0 else ''}{x.b}r{x.d}" if x.b else ''),
    'a+br5always': lambda x: f'{x.a}+{x.b}r{x.d}',
    'a +- b√d minus': lambda x: f'{x.a}' if x.b == 0 else (f'{x.b}√{x.d}' if x.a == 0 else f'{x.a} {"+" if x.b > 0 else "−"} {abs(x.b)}√{x.d}'),
    'a + b√d omit0': lambda x: f'{x.a}' + (f' + {x.b}√{x.d}' if x.b else ''),
    'a + b√d always': lambda x: f'{x.a} + {x.b}√{x.d}',
    '(a + b√d)always': lambda x: f'({x.a} + {x.b}√{x.d})',
    'a +- b*sqrtd': lambda x: str(x.a) if x.b == 0 else (f'{x.b}*sqrt{x.d}' if x.a == 0 else f'{x.a} {_pm(x.b)} {abs(x.b)}*sqrt{x.d}'),
    'a +- b√d': lambda x: f'{x.a}' if x.b == 0 else (f'{x.b}√{x.d}' if x.a == 0 else f'{x.a} {_pm(x.b)} {abs(x.b)}√{x.d}'),
    'a + b*sqrtd always': lambda x: f'{x.a} + {x.b}*sqrt{x.d}',
    'a + b*sqrt(d) always': lambda x: f'{x.a} + {x.b}*sqrt({x.d})',
    '(a+b*sqrtd)': lambda x: str(x.a) if x.b == 0 else f"({x.a}{'+' if x.b >= 0 else ''}{x.b}*sqrt{x.d})",
    'a + b*sqrt(d)': lambda x: str(x.a) if x.b == 0 else (f'{x.a} + {x.b}*sqrt({x.d})' if x.a != 0 else f'{x.b}*sqrt({x.d})'),
    '(a) + (b)*sqrt(d) always': lambda x: f'({x.a}) + ({x.b})*sqrt({x.d})',
    'a+-b*sqrt(d)': lambda x: str(x.a) if x.b == 0 else f"{x.a}{_pm(x.b)}{abs(x.b)}*sqrt({x.d})",
}


def fmt(x, style='kernel'):
    """x (Quad, int or Fraction) as text in a named style"""
    if not isinstance(x, Quad): x = Quad(x)
    return STYLES[style](x)


# ----------------------------------------------------------------------------------------------- constructors, constants
def q5(a=0, b=0): return Quad(a, b, 5)
def qf(a=0, b=0, d=5): return Quad(a, b, d)


ZERO, ONE = Quad(0), Quad(1)
PHI = Quad(Fr(1, 2), Fr(1, 2), 5); IPHI = Quad(Fr(-1, 2), Fr(1, 2), 5)
R2, R3, R5, R6 = Quad(0, 1, 2), Quad(0, 1, 3), Quad(0, 1, 5), Quad(0, 1, 6)


def floor(x):
    """floor of a Quad, Fraction or int"""
    return x.floor() if isinstance(x, Quad) else math.floor(x)


def frac(x): return x - floor(x)


import re as _re
_NUM = r'\d+(?:/\d+)?'
_RX = _re.compile(rf'(?:([-+]?{_NUM})(?=[-+]|$))?(?:([-+]?)\(?([-+]?{_NUM})?\)?\*?sqrt\((\d+)\))?')


def parse(s, d=None):
    """text -> Quad without sympy: 'a', 'a|b' (pair form, field d or 5), 'a + b*sqrt(d)', 'a - (b)*sqrt(d)', '-sqrt(d)' (the 'parsable'
    and to_str forms of the copies); anything else goes to sympy (parse_sympy)"""
    t = s.replace(' ', '')
    if '|' in t:
        a, b = t.split('|'); return Quad(Fr(a), Fr(b), d or 5)
    m = _RX.fullmatch(t)
    if m and t:
        a, sg, b, dd = m.groups()
        if dd is None: return Quad(Fr(a), 0, d or Quad.D)
        bb = (Fr(b) if b else Fr(1)) * (-1 if sg == '-' else 1)
        return Quad(Fr(a) if a else Fr(0), bb, int(dd))
    return parse_sympy(s, d)


def parse_sympy(s, d=None, cls=None):
    """any sympy expression lying in Q(sqrt d) -> Quad (as the qf.py copies' parse)"""
    import sympy as sp
    d = d or Quad.D; r = sp.sqrt(d); e = sp.expand(sp.sympify(s, locals={'sqrt': sp.sqrt})); b = e.coeff(r); a = sp.expand(e - b * r)
    if not (a.is_Rational and b.is_Rational): raise ValueError(f'not in Q(sqrt{d}): ' + s)
    return (cls or Quad)(Fr(int(a.p), int(a.q)), Fr(int(b.p), int(b.q)), d)


# ------------------------------------------------------------- angles that are rational multiples of pi (from the qf.py copies)
_COS2 = {1: {0: (1, 0, 1)}, 2: {1: (-1, 0, 1)}, 3: {1: (Fr(-1, 2), 0, 1), 2: (Fr(-1, 2), 0, 1)}, 4: {1: (0, 0, 1), 3: (0, 0, 1)},
         6: {1: (Fr(1, 2), 0, 1), 5: (Fr(1, 2), 0, 1)},
         5: {1: (Fr(-1, 4), Fr(1, 4), 5), 4: (Fr(-1, 4), Fr(1, 4), 5), 2: (Fr(-1, 4), Fr(-1, 4), 5), 3: (Fr(-1, 4), Fr(-1, 4), 5)},
         10: {1: (Fr(1, 4), Fr(1, 4), 5), 9: (Fr(1, 4), Fr(1, 4), 5), 3: (Fr(1, 4), Fr(-1, 4), 5), 7: (Fr(1, 4), Fr(-1, 4), 5)},
         8: {1: (0, Fr(1, 2), 2), 7: (0, Fr(1, 2), 2), 3: (0, Fr(-1, 2), 2), 5: (0, Fr(-1, 2), 2)},
         12: {1: (0, Fr(1, 2), 3), 11: (0, Fr(1, 2), 3), 5: (0, Fr(-1, 2), 3), 7: (0, Fr(-1, 2), 3)}}


def cos2_exact(fr):
    """cos(2 pi * fr) as (a, b, d), value a + b sqrt d, for denominators with phi(n) <= 4 (1-6, 8, 10, 12)"""
    n = fr.denominator; k = fr.numerator % n
    return _COS2[n][k]


def rational_pi(c2, theta, field_d=None):
    """is theta (in [0, pi]) a rational multiple of pi, given c2 = cos(2 theta) exactly?  'k/n' (of pi) or None.
    Niven type: cos(2 theta) of degree <= 2 over Q forces 2 theta = 2 pi k / n with phi(n) <= 4.  field_d: the field of the run
    (the qf.py copies use their class-level D; here c2.d, or field_d when c2 is rational)."""
    D = field_d if field_d is not None else (c2.d if isinstance(c2, Quad) else Quad.D)
    ca, cb = (c2.a, c2.b) if isinstance(c2, Quad) else (_fr(c2), Fr(0))
    for n in (1, 2, 3, 4, 5, 6, 8, 10, 12):
        for k in range(n):
            if math.gcd(k, n) != 1 and not (k == 0 and n == 1): continue
            a, b, d = cos2_exact(Fr(k, n))
            if b != 0 and d != D: continue
            if ca == Fr(a) and cb == Fr(b):
                for m in (Fr(k, n), 1 - Fr(k, n)):
                    if abs(float(m) * math.pi - theta) < 1e-7: return f'{m.numerator}/{m.denominator}' if m.denominator != 1 else f'{m.numerator}'
    return None


def rational_pi_float(theta, qmax=360, tol=1e-9):
    """float search (not exact; kept for the copies that report it beside the exact test)"""
    for q in range(1, qmax + 1):
        p = round(theta / math.pi * q)
        if abs(p / q * math.pi - theta) < tol and math.gcd(p, q) == 1: return f'{p}/{q}' if q != 1 else f'{p}'
    return None
