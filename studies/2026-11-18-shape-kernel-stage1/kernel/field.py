"""General real number fields for the shape kernel (stage 1 proper, 2026-11-18).

Two element types beside Quad (exact.py):

  NF(c, F)       an element c_0 + c_1 t + ... + c_(n-1) t^(n-1) of the real field F = Q(t), where t is the only root of an integer
                 polynomial p in a rational isolating interval (lo, hi).  Covers the pure cubic fields Q(k^(1/3)) (KC of exactlib.py),
                 the fields Q(t) of exactlib.py (AlgField / RF), the pure radical fields Q(k^(1/n)) (octet_special_exact.py) and the
                 golden basis a + b phi (mixlib.py; Z[phi] of zsurf.py through kernel/zphi.py).
  MQ(a, b, c, d) a + b sqrt p + c sqrt q + d sqrt(pq) in the four-term field Q(sqrt p, sqrt q) (K of cubes_lib.py, p = 2, q = 5).

Exact sign, never a float decision:
  NF  interval arithmetic (Horner) on the rational isolating interval of t, bisected (exact signs of p at rational midpoints) until
      the interval of the value excludes 0.  The bisection is the one of exactlib's AlgField, step for step, so a field shared with
      a study refines its interval in the same order and the study's printed decimals stay the same.  A nonzero element of an
      irreducible field is never 0 at t, so the loop ends; every 64 bisections an exact zero test runs as a guard (gcd of the
      element's polynomial with p, and a Sturm count of that gcd on the interval), so a reducible p cannot loop forever.
  MQ  rational enclosures of sqrt p, sqrt q, sqrt pq from integer square roots (math.isqrt) at 32, 64, 128, ... bits, until the
      interval of the value excludes 0.  1, sqrt p, sqrt q, sqrt pq are independent over Q (checked: p, q, pq not squares), so a
      nonzero element is never 0 and the loop ends.

Printed forms, floats, decimals and hashes follow the copies through named styles (NF_STYLES, NF_FLOATS, MQ_STYLES), as in exact.py.
Libraries: where python-flint (FLINT and Arb; W. Hart, F. Johansson et al.) is installed, irreducibility of the defining polynomial
comes from fmpz_poly.factor, and arb_sign_nf / arb_sign_mq give a second, independent certified sign with Arb ball arithmetic.
The kernel's own sign keeps exactlib's bisection order, which the copies' printed decimals depend on (a compatibility layer).
Floats are refused in arithmetic (TypeError), as in exact.py.
"""
from fractions import Fraction as Fr
from decimal import Decimal
import math

from .exact import Quad, _fr, qsign

__all__ = ['arb_sign_nf', 'arb_sign_mq', 'NumberField', 'NF', 'MQ', 'GOLDEN', 'pure_field', 'sturm_count', 'poly_gcd', 'NF_STYLES', 'NF_FLOATS', 'MQ_STYLES',
           'iroot']


def _frx(x):
    """a coefficient as a Fraction.  A float is taken only when it is a small dyadic rational (denominator <= 2^16, e.g. 1.0, -0.5,
    0.375), the one case where its value is beyond doubt; a float such as 0.1 (stored as 3602879701896397/2^55) raises TypeError.
    (The copies took every float at its binary value; cubes_lib's s10 study builds K(abs(float(c))) from such small values.)"""
    if isinstance(x, float):
        if not math.isfinite(x) or Fr(x).denominator > 2 ** 16: raise TypeError('exact only: convert floats explicitly with Fraction(x)')
        return Fr(x)
    return _fr(x)


def iroot(k, n):
    """floor of the real n-th root of a positive integer k"""
    if k < 0: raise ValueError('negative radicand')
    if k < 2: return k
    r = int(round(k ** (1.0 / n))) if k < 2 ** 1000 else 1 << ((k.bit_length() + n - 1) // n)
    while r ** n > k: r -= 1
    while (r + 1) ** n <= k: r += 1
    return r


# ------------------------------------------------------------------------------------------------ polynomials over Q (low -> high)
def _trim(a):
    a = list(a)
    while a and a[-1] == 0: a.pop()
    return a


def _pdivmod(a, b):
    a = _trim(a); b = _trim(b)
    if not b: raise ZeroDivisionError('polynomial division by zero')
    q = [Fr(0)] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        c = Fr(a[-1]) / b[-1]; k = len(a) - len(b); q[k] = c
        for i, bi in enumerate(b): a[i + k] -= c * bi
        a = _trim(a)
    return q, a


def poly_gcd(a, b):
    """monic gcd of two polynomials (coefficient lists low -> high)"""
    a, b = _trim(a), _trim(b)
    while b: a, b = b, _pdivmod(a, b)[1]
    return [Fr(x) / a[-1] for x in a] if a else []


def _peval_low(a, x):
    v = Fr(0)
    for c in reversed(a): v = v * x + c
    return v


def _deriv(a): return [i * a[i] for i in range(1, len(a))]


def sturm_count(a, lo, hi):
    """number of distinct real roots of a (low -> high) in (lo, hi]; exact (Sturm's theorem)"""
    a = _trim(a)
    if len(a) <= 1: return 0
    seq = [a, _trim(_deriv(a))]
    while len(seq[-1]) > 1:
        r = _pdivmod(seq[-2], seq[-1])[1]
        if not r: break
        seq.append([-x for x in r])

    def var(x):
        s = [v for v in (_peval_low(p, x) for p in seq) if v != 0]
        return sum(1 for u, w in zip(s, s[1:]) if (u > 0) != (w > 0))
    return var(Fr(lo)) - var(Fr(hi))


def _rational_roots(P):
    """rational roots of an integer-or-rational polynomial (high -> low)"""
    den = 1
    for c in P: den = den * Fr(c).denominator // math.gcd(den, Fr(c).denominator)
    Z = [int(Fr(c) * den) for c in P]
    while Z and Z[-1] == 0: return [Fr(0)]
    out = []
    a0, an = abs(Z[-1]), abs(Z[0])

    def divs(m): return [d for d in range(1, m + 1) if m % d == 0] if m < 10 ** 6 else None
    pa, qa = divs(a0), divs(an)
    if pa is None or qa is None: return None
    for p_ in pa:
        for q_ in qa:
            for s in (1, -1):
                x = Fr(s * p_, q_); v = Fr(0)
                for c in Z: v = v * x + c
                if v == 0 and x not in out: out.append(x)
    return out


# ------------------------------------------------------------------------------------- python-flint (FLINT / Arb), where installed
try:
    import flint as _flint
except ImportError:
    _flint = None


def _flint_irreducible(P):
    """irreducibility over Q of a rational polynomial (highest degree first) by python-flint's fmpz_poly.factor; None without flint"""
    if _flint is None: return None
    den = 1
    for c in P: den = den * Fr(c).denominator // math.gcd(den, Fr(c).denominator)
    f = _flint.fmpz_poly([int(Fr(c) * den) for c in reversed(P)])
    _, facs = f.factor()
    return len(facs) == 1 and facs[0][1] == 1 and facs[0][0].degree() == len(P) - 1


def _arb_q(q): return _flint.arb(_flint.fmpq(q.numerator, q.denominator))


def arb_sign_nf(c, F, prec=64):
    """independent certified sign of sum c_k t^k with Arb ball arithmetic (python-flint): t is enclosed by a ball over a local copy of
    the rational isolating interval (bisected here, never the field's own state); precision and interval both tighten until the
    ball of the value excludes 0.  Used by the tests as a second, library-based decision beside NumberField.sign."""
    if all(x == 0 for x in c): return 0
    lo, hi = F.lo0, F.hi0; plo = F.peval(lo)
    for k in range(400):
        _flint.ctx.prec = prec
        mid, rad = (lo + hi) / 2, (hi - lo) / 2
        t = _flint.arb(_flint.fmpq(mid.numerator, mid.denominator), _flint.arb(_flint.fmpq(rad.numerator, rad.denominator)).upper())
        v = _flint.arb(0)
        for ck in reversed(c): v = v * t + _arb_q(ck)
        if v > 0: return 1
        if v < 0: return -1
        m = (lo + hi) / 2; pm = F.peval(m)
        if (plo < 0) == (pm < 0): lo, plo = m, pm
        else: hi = m
        prec = min(prec * 2, 4096) if k % 4 == 3 else prec
    raise ArithmeticError('arb_sign_nf: undecided (is the element zero?)')


def arb_sign_mq(x, prec=64):
    """certified sign of an MQ element with Arb balls for sqrt p, sqrt q (python-flint), doubling the precision until decided"""
    if x.iszero(): return 0
    p, q = x.RADS
    while prec <= 1 << 16:
        _flint.ctx.prec = prec
        a, b, c, d = (_arb_q(v) for v in x.v)
        v = a + b * _flint.arb(p).sqrt() + c * _flint.arb(q).sqrt() + d * _flint.arb(p * q).sqrt()
        if v > 0: return 1
        if v < 0: return -1
        prec *= 2
    raise ArithmeticError('arb_sign_mq: undecided')


# ------------------------------------------------------------------------------------------------------------- the field Q(t)
class NumberField:
    """Q(t), t the only root of the polynomial p (integer or rational coefficients, highest degree first, as written) in the open
    interval (lo, hi).  Same constructor, attributes and methods as exactlib's AlgField (P, n, name, mon, lo, hi, lo0, hi0, key,
    get, peval, poly_string, bisect, approx, interval_value, sign, reduce), plus: exact zero test, Sturm check of the interval,
    pure radical fields (pure_field) and the golden field (GOLDEN)."""
    _reg = {}

    def __init__(s, coeffs, lo, hi, name='t'):
        s.P = [_frx(c) for c in coeffs]
        s.n = len(s.P) - 1; s.name = name
        if s.n < 1 or s.P[0] == 0: raise ValueError('need a polynomial of degree >= 1 with nonzero leading coefficient')
        lead = s.P[0]; s.mon = [c / lead for c in s.P]
        s.lo, s.hi = Fr(lo), Fr(hi); s.lo0, s.hi0 = s.lo, s.hi
        s.key = ('alg', name, tuple(s.P), Fr(lo), Fr(hi))
        if not s.peval(s.lo) * s.peval(s.hi) < 0: raise ValueError('p must change sign on the isolating interval')
        s.low = list(reversed(s.P))                       # low -> high
        if sturm_count(s.low, s.lo, s.hi) != 1: raise ValueError('the interval holds more than one root of p')
        s.irreducible = _flint_irreducible(s.P)            # python-flint fmpz_poly.factor when available (any degree)
        if s.irreducible is None and s.n <= 3:
            rr = _rational_roots(s.P)
            s.irreducible = (rr == []) if rr is not None else None      # degree <= 3: irreducible iff no rational root
        if s.n == 1: s.irreducible = True
        s.pure = None                                     # (k, n) for x^n - k
        s.zero_tests = 0
        s.fast = False                                    # quadratic fast path (set_fast); off for fields built as AlgField
        if s.n == 2:
            m1, m0 = s.mon[1], s.mon[2]                   # t^2 + m1 t + m0 = 0
            s._r = (-m0, -m1)                             # t^2 = r0 + r1 t
            D = m1 * m1 - 4 * m0
            from .exact import _rat_sqrt
            if D > 0 and _rat_sqrt(D) is None:
                s.irreducible = True
                up = sturm_count(s.low, -m1 / 2, s.hi) == 1 if -m1 / 2 < s.hi else False   # t is the larger root
                s._q = (m1, 1 if up else -1, D)            # t = (-m1 + e sqrt D) / 2

    def set_fast(s):
        """degree 2 only: decide signs by the quadratic rule (exact.qsign) instead of bisection.  Exact either way; the fast path
        leaves the isolating interval untouched, so it is used only for fields the kernel makes (GOLDEN, pure_field(k, 2)), never
        for a field that a study builds as AlgField (whose printed decimals depend on the bisection history)."""
        if s.n == 2 and getattr(s, '_q', None): s.fast = True
        return s

    @classmethod
    def get(cls, coeffs, lo, hi, name='t'):
        k = ('alg', name, tuple(Fr(c) for c in coeffs), Fr(lo), Fr(hi))
        if k not in cls._reg: cls._reg[k] = cls(coeffs, lo, hi, name)
        return cls._reg[k]

    def peval(s, x):
        v = Fr(0)
        for c in s.P: v = v * x + c
        return v

    def poly_string(s):
        out = []
        for i, c in enumerate(s.P):
            e = s.n - i
            if c == 0: continue
            m = '' if e == 0 else (s.name if e == 1 else f'{s.name}**{e}')
            a = abs(c); cs = (str(a) if a.denominator == 1 else f'({a})')
            term = cs if e == 0 else (m if a == 1 else f'{cs}*{m}')
            out.append(('-' if c < 0 else '+', term))
        t = ('-' if out[0][0] == '-' else '') + out[0][1]
        for sg, term in out[1:]: t += f' {sg} {term}'
        return t

    def bisect(s):
        m = (s.lo + s.hi) / 2; v = s.peval(m)
        if v == 0: raise ArithmeticError('p has the rational root %s: not a field' % m)
        if (s.peval(s.lo) < 0) == (v < 0): s.lo = m
        else: s.hi = m

    def approx(s, eps):
        while s.hi - s.lo > eps: s.bisect()
        return (s.lo + s.hi) / 2

    def interval_value(s, c):
        """interval [a, b] containing sum c_k t^k for t in [lo, hi] (Horner in interval arithmetic); c low -> high"""
        a = b = Fr(0)
        for ck in reversed(c):
            ps = [a * s.lo, a * s.hi, b * s.lo, b * s.hi]
            a, b = min(ps) + ck, max(ps) + ck
        return a, b

    def is_zero_at_t(s, c):
        """exact: is sum c_k t^k = 0?  (t is a root of g = gcd(c, p) iff g has a root in (lo, hi), the only root of p there)"""
        c = _trim(c)
        if not c: return True
        if s.irreducible: return False
        s.zero_tests += 1
        g = poly_gcd(c, s.low)
        return len(g) > 1 and sturm_count(g, s.lo, s.hi) > 0

    def sign(s, c):
        if all(x == 0 for x in c): return 0
        if s.fast:
            m1, e, D = s._q
            return qsign(2 * c[0] - c[1] * m1, c[1] * e, D)
        k = 0
        while True:
            a, b = s.interval_value(c)
            if a > 0: return 1
            if b < 0: return -1
            k += 1
            if k % 64 == 0 and s.is_zero_at_t(c): return 0
            s.bisect()

    def reduce(s, q):
        """q: list low -> high of any length; reduce modulo the monic polynomial"""
        q = list(q); m = list(reversed(s.mon))
        for deg in range(len(q) - 1, s.n - 1, -1):
            c = q[deg]
            if c == 0: continue
            for k in range(s.n + 1): q[deg - s.n + k] -= c * m[k]
        q = q[:s.n] + [Fr(0)] * max(0, s.n - len(q))
        return tuple(q[:s.n])

    def gen(s): return NF([0, 1], s)
    def __repr__(s): return f'Q({s.name}), {s.poly_string()} = 0, {s.name} in ({s.lo0}, {s.hi0})'


_PURE = {}


def pure_field(k, n):
    """Q(k^(1/n)) for a positive integer k that is not an n-th power: x^n - k, interval (floor root, floor root + 1)"""
    key = (k, n)
    F = _PURE.get(key)
    if F is not None: return F
    if not (isinstance(k, int) and k > 0): raise ValueError('pure field: k must be a positive integer')
    r = iroot(k, n)
    if r ** n == k: raise ValueError(f'{k} is an {n}-th power: Q({k}^(1/{n})) = Q')
    F = NumberField([1] + [0] * (n - 1) + [-k], r, r + 1, name=f'{k}**(1/{n})')
    if n in (2, 3): F.irreducible = True                  # x^2 - k, x^3 - k with k not a square / cube
    if n == 2: F.set_fast()
    F.pure = (k, n)
    _PURE[key] = F
    return F


GOLDEN = NumberField([1, -1, -1], 1, 2, name='phi').set_fast()     # phi^2 = phi + 1, phi in (1, 2)


# ------------------------------------------------------------------------------------------------------------------ NF elements
def _r(q): return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'


def _join_terms(out):
    if not out: return '0'
    t = out[0]
    for u in out[1:]: t += f' - {u[1:]}' if u.startswith('-') else f' + {u}'
    return t


def _fmt_basis(x, base):
    out = []
    for i, q in enumerate(x.c):
        if q == 0: continue
        if i == 0: out.append(_r(q)); continue
        b = base(i)
        out.append(b if q == 1 else (f'-{b}' if q == -1 else f'({_r(q)})*{b}'))
    return _join_terms(out)


NF_STYLES = {
    'rf': lambda x: _fmt_basis(x, lambda i: x.F.name if i == 1 else f'{x.F.name}**{i}'),                 # exactlib RF.fmt
    'kc': lambda x: _fmt_basis(x, lambda i: f'{x.F.pure[0]}**({i}/{x.F.pure[1]})'),                      # exactlib KC.fmt
    'r^i': lambda x: ' + '.join(f'{a}·r^{i}' for i, a in enumerate(x.c) if a) or '0',                    # octet_special_exact K
    '(a+-bphi)': lambda x: str(x.c[0]) if x.c[1] == 0 else f'({x.c[0]}{"+" if x.c[1] >= 0 else "-"}{abs(x.c[1])}{x.F.name})',   # echo_lib, qlib Q5
    'pair': lambda x: f'({x.c[0]}, {x.c[1]})' if x.F.n == 2 else repr(tuple(x.c)),
}


def _f_interval(x): return float(x.at(x.F.approx(Fr(1, 10 ** 22))))


def _f_kc(x):
    r = x.F.pure[0] ** (1 / 3); c = x.c
    return float(c[0]) + float(c[1]) * r + float(c[2]) * r * r


def _f_rpow(x):
    k, n = x.F.pure; r = k ** (1 / n)
    return sum(float(a) * r ** i for i, a in enumerate(x.c))


def _f_golden(x): return float(x.c[0]) + float(x.c[1]) * (1 + 5 ** 0.5) / 2


def _f_golden_phi(x): return float(x.c[0]) + float(x.c[1]) * ((1 + 5 ** .5) / 2)      # residents.py: phi rounded first


NF_FLOATS = {'interval': _f_interval, 'kc': _f_kc, 'r^i': _f_rpow, 'golden': _f_golden, 'golden (phi first)': _f_golden_phi}


def _quant(x, places):
    q = x.quantize(Decimal(1).scaleb(-places))
    return format(q, 'f') if q != 0 else format(Decimal(0).quantize(Decimal(1).scaleb(-places)), 'f')


class NF:
    """c_0 + c_1 t + ... in F = Q(t).  NF(c, F): c a list of rationals (low -> high, any length: longer lists are reduced mod p)."""
    __slots__ = ('c', 'F')
    STYLE = 'rf'            # printed form, see NF_STYLES
    FLOAT = 'interval'      # float(x), see NF_FLOATS
    DEC = 'interval'        # dec(): 'interval' (exactlib RF) or 'kc' (exactlib KC, Decimal root)
    MP = 'interval'         # mp():  'interval' (exactlib RF) or 'kc' (mpmath.cbrt)

    def __init__(s, c, F):
        if not isinstance(c, (list, tuple)): c = [c]
        c = [_frx(x) for x in c]; s.F = F
        s.c = tuple(c + [Fr(0)] * (F.n - len(c))) if len(c) <= F.n else F.reduce(c)

    def _new(s, c, other=None):
        cls = type(other) if other is not None and type(other) is not type(s) and issubclass(type(other), type(s)) else type(s)
        o = object.__new__(cls); o.c = c; o.F = s.F; return o

    def _c(s, o):
        if isinstance(o, NF):
            if o.F is not s.F: raise ValueError('mixed fields')
            return o
        if isinstance(o, (int, Fr)): return s._new((_fr(o),) + (Fr(0),) * (s.F.n - 1))
        if isinstance(o, Quad) and o.b == 0: return s._new((o.a,) + (Fr(0),) * (s.F.n - 1))
        if isinstance(o, float): raise TypeError('exact only: convert floats explicitly with Fraction(x)')
        return NotImplemented

    @property
    def d(s): return s.F.key
    @property
    def a(s): return s.c[0]
    @property
    def b(s): return s.c[1]
    @property
    def k(s): return s.F.pure[0] if s.F.pure else None

    def __add__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return s._new(tuple(x + y for x, y in zip(s.c, o.c)), o)
    __radd__ = __add__

    def __sub__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return s._new(tuple(x - y for x, y in zip(s.c, o.c)), o)

    def __rsub__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return o - s

    def __neg__(s): return s._new(tuple(-x for x in s.c))
    def __pos__(s): return s

    def __mul__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        n = s.F.n
        if n == 2:
            (a, b), (c, d) = s.c, o.c; r0, r1 = s.F._r; bd = b * d
            return s._new((a * c + r0 * bd, a * d + b * c + r1 * bd), o)
        q = [Fr(0)] * (2 * n - 1)
        for i, x in enumerate(s.c):
            if x == 0: continue
            for j, y in enumerate(o.c): q[i + j] += x * y
        return s._new(s.F.reduce(q), o)
    __rmul__ = __mul__

    def inv(s):
        """exact inverse by the extended Euclidean algorithm in Q[x] modulo p"""
        a, b = _trim(s.c), _trim(s.F.low)
        if not a or s.F.is_zero_at_t(list(s.c)): raise ZeroDivisionError('NF division by zero')
        r0, r1, u0, u1 = b, a, [], [Fr(1)]
        while len(r1) > 1:
            q, r = _pdivmod(r0, r1)
            prod = [Fr(0)] * (len(q) + len(u1)) if q and u1 else []
            for i, x in enumerate(q):
                for j, y in enumerate(u1): prod[i + j] += x * y
            nu = [Fr(0)] * max(len(u0), len(prod))
            for i, x in enumerate(u0): nu[i] += x
            for i, x in enumerate(prod): nu[i] -= x
            r0, r1, u0, u1 = r1, _trim(r), u1, _trim(nu)
        if not r1: raise ArithmeticError('p is reducible and the element shares a factor with it')
        c = r1[0]
        return s._new(s.F.reduce([x / c for x in u1] or [Fr(0)]))

    def __truediv__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return s * o.inv()

    def __rtruediv__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return o * s.inv()

    def __pow__(s, k):
        if not isinstance(k, int): raise TypeError('integer powers only')
        if k < 0: return s.inv() ** (-k)
        r = s._new((Fr(1),) + (Fr(0),) * (s.F.n - 1)); x = s
        while k:
            if k & 1: r = r * x
            x = x * x; k >>= 1
        return r

    def conj(s):
        """degree 2: the Galois conjugate (t -> the other root -m1 - t); golden basis: a + b phi -> (a + b) - b phi (mixlib, echo_lib, zsurf)"""
        if s.F.n != 2: raise ValueError('conj: degree 2 fields only (use the norm for higher degree)')
        m1 = s.F.mon[1]; a, b = s.c
        return s._new((a - m1 * b, -b))
    gal = sig = conj

    def norm(s):
        """field norm: the determinant of multiplication by s (a rational)"""
        n = s.F.n; M = []
        e = s._new((Fr(1),) + (Fr(0),) * (n - 1)); t = s._new((Fr(0), Fr(1)) + (Fr(0),) * (n - 2)) if n > 1 else None
        for j in range(n):
            M.append(list((s * e).c)); e = e * t if t is not None else e
        M = [list(r) for r in zip(*M)]; det = Fr(1)
        for col in range(n):
            piv = next((r for r in range(col, n) if M[r][col] != 0), None)
            if piv is None: return Fr(0)
            if piv != col: M[col], M[piv] = M[piv], M[col]; det = -det
            det *= M[col][col]
            for r in range(col + 1, n):
                f = M[r][col] / M[col][col]
                if f: M[r] = [x - f * y for x, y in zip(M[r], M[col])]
        return det

    # exact decisions
    def sign(s): return s.F.sign(s.c)
    def iszero(s): return all(x == 0 for x in s.c) if s.F.irreducible else s.F.is_zero_at_t(list(s.c))
    is_zero = zero = z = iszero
    def __bool__(s): return not s.iszero()

    def __eq__(s, o):
        if isinstance(o, float): return NotImplemented
        o = s._c(o)
        if o is NotImplemented: return o
        return s.c == o.c if s.F.irreducible else (s - o).iszero()

    def __ne__(s, o):
        r = s.__eq__(o)
        return r if r is NotImplemented else not r

    def __hash__(s): return hash(s.c)
    def _cmp(s, o): return (s - o).sign()
    def __lt__(s, o): return s._cmp(o) < 0
    def __le__(s, o): return s._cmp(o) <= 0
    def __gt__(s, o): return s._cmp(o) > 0
    def __ge__(s, o): return s._cmp(o) >= 0
    def __abs__(s): return -s if s.sign() < 0 else s

    # conversions
    def at(s, x): return sum((q * x ** i for i, q in enumerate(s.c)), Fr(0))
    def __float__(s): return NF_FLOATS[type(s).FLOAT](s)
    def f(s): return float(s)

    def mp(s):
        import mpmath
        if type(s).MP == 'kc':
            r = mpmath.cbrt(s.F.pure[0])
            return sum((mpmath.mpf(x.numerator) / x.denominator * r ** i for i, x in enumerate(s.c)), mpmath.mpf(0))
        r = s.F.approx(Fr(1, 10 ** 70)); v = s.at(r)
        return mpmath.mpf(v.numerator) / v.denominator

    def dec(s, places=15):
        if type(s).DEC == 'kc':
            r = Decimal(s.F.pure[0]) ** (Decimal(1) / Decimal(3))
            x = sum((Decimal(q.numerator) / Decimal(q.denominator) * r ** i for i, q in enumerate(s.c)), Decimal(0))
            return _quant(x, places)
        v = s.at(s.F.approx(Fr(1, 10 ** 45)))
        return _quant(Decimal(v.numerator) / Decimal(v.denominator), places)

    def digits(s, places=60):
        """exact decimal string truncated toward minus infinity (bisection to an interval that fixes `places` digits)"""
        if s.iszero(): return '0.' + '0' * places
        sc = Fr(10 ** places)
        while True:
            lo, hi = s.F.interval_value(s.c)
            a, b = math.floor(lo * sc), math.floor(hi * sc)
            if a == b:
                sg = '-' if a < 0 else ''; t = str(abs(a)).rjust(places + 1, '0')
                return f'{sg}{t[:-places]}.{t[-places:]}' if places else f'{sg}{t}'
            s.F.bisect()

    def fmt(s): return NF_STYLES[type(s).STYLE](s)
    def __repr__(s): return s.fmt()
    def __str__(s): return s.__repr__()


# ------------------------------------------------------------------------------------------------- four-term field Q(sqrt p, sqrt q)
def _sqrt_enclosure(m, bits):
    """rational lo <= sqrt(m) <= hi (m a positive integer, not a square), width 2^-bits"""
    s = 1 << bits; r = math.isqrt(m * s * s)
    return Fr(r, s), Fr(r + 1, s)


def _scal(c, lo, hi):
    return (c * lo, c * hi) if c >= 0 else (c * hi, c * lo)


def _kname(q, n):
    return f'{q}{n}' if n == '' else (f'{q}{n}' if q not in (1, -1) else ('-' if q == -1 else '') + n)


MQ_STYLES = {
    'roots': lambda x: (' + '.join(_kname(q, n) for q, n in zip(x.v, ('', f'√{x.RADS[0]}', f'√{x.RADS[1]}', f'√{x.RADS[0] * x.RADS[1]}'))
                                   if q != 0).replace('+ -', '- ') or '0'),          # cubes_lib kstr
    'tuple': lambda x: repr(tuple(x.v)),
}


class MQ:
    """a + b sqrt p + c sqrt q + d sqrt(pq), a..d rationals; (p, q) = RADS, a class setting (default (2, 5): K of cubes_lib.py)"""
    __slots__ = ('v',)
    RADS = (2, 5)
    STYLE = 'roots'
    _ok = {}

    def __init__(s, a=0, b=0, c=0, d=0):
        s.v = (_frx(a), _frx(b), _frx(c), _frx(d))
        R = type(s).RADS
        if R not in MQ._ok:
            p, q = R
            if not all(isinstance(m, int) and m > 1 and math.isqrt(m) ** 2 != m for m in (p, q, p * q)):
                raise ValueError(f'Q(sqrt {p}, sqrt {q}) is not a four-term field (p, q, pq must be non-square integers > 1)')
            MQ._ok[R] = True

    def _new(s, v, other=None):
        cls = type(other) if other is not None and type(other) is not type(s) and issubclass(type(other), type(s)) else type(s)
        o = object.__new__(cls); o.v = v; return o

    @classmethod
    def c(cls, x): return x if isinstance(x, MQ) else cls(x)
    of = c

    def _c(s, o):
        if isinstance(o, MQ):
            if type(o).RADS != type(s).RADS: raise ValueError('mixed fields')
            return o
        if isinstance(o, (int, Fr)): return s._new((_fr(o), Fr(0), Fr(0), Fr(0)))
        if isinstance(o, Quad):
            p, q = type(s).RADS
            if o.b == 0: return s._new((o.a, Fr(0), Fr(0), Fr(0)))
            if o.d == p: return s._new((o.a, o.b, Fr(0), Fr(0)))
            if o.d == q: return s._new((o.a, Fr(0), o.b, Fr(0)))
            if o.d == p * q: return s._new((o.a, Fr(0), Fr(0), o.b))
            raise ValueError('mixed fields')
        if isinstance(o, float): raise TypeError('exact only: convert floats explicitly with Fraction(x)')
        return NotImplemented

    def __add__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return s._new(tuple(x + y for x, y in zip(s.v, o.v)), o)
    __radd__ = __add__

    def __sub__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return s._new(tuple(x - y for x, y in zip(s.v, o.v)), o)

    def __rsub__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return o - s

    def __neg__(s): return s._new(tuple(-x for x in s.v))
    def __pos__(s): return s

    def __mul__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        p, q = type(s).RADS; a, b, c, d = s.v; e, f, g, h = o.v
        return s._new((a * e + p * b * f + q * c * g + p * q * d * h, a * f + b * e + q * (c * h + d * g),
                       a * g + c * e + p * (b * h + d * f), a * h + d * e + b * g + c * f), o)
    __rmul__ = __mul__

    def conj_p(s): a, b, c, d = s.v; return s._new((a, -b, c, -d))
    def conj_q(s): a, b, c, d = s.v; return s._new((a, b, -c, -d))
    conj2, conj5 = conj_p, conj_q            # the names in cubes_lib.py (p = 2, q = 5)

    def norm(s):
        m = s * s.conj_p(); n = m * m.conj_q()
        return n.v[0]

    def inv(s):
        if s.iszero(): raise ZeroDivisionError('MQ division by zero')
        m = s * s.conj_p(); n = m * m.conj_q()
        return s.conj_p() * m.conj_q() * s._new((1 / n.v[0], Fr(0), Fr(0), Fr(0)))

    def __truediv__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return s * o.inv()

    def __rtruediv__(s, o):
        o = s._c(o)
        if o is NotImplemented: return o
        return o * s.inv()

    def __pow__(s, k):
        if not isinstance(k, int): raise TypeError('integer powers only')
        if k < 0: return s.inv() ** (-k)
        r = s._new((Fr(1), Fr(0), Fr(0), Fr(0))); x = s
        while k:
            if k & 1: r = r * x
            x = x * x; k >>= 1
        return r

    def interval(s, bits):
        p, q = type(s).RADS; a, b, c, d = s.v
        I = [_scal(b, *_sqrt_enclosure(p, bits)), _scal(c, *_sqrt_enclosure(q, bits)), _scal(d, *_sqrt_enclosure(p * q, bits))]
        return a + sum(i[0] for i in I), a + sum(i[1] for i in I)

    def sign(s):
        if s.iszero(): return 0
        bits = 32
        while True:
            lo, hi = s.interval(bits)
            if lo > 0: return 1
            if hi < 0: return -1
            bits *= 2

    def iszero(s): return all(x == 0 for x in s.v)
    is_zero = zero = z = iszero
    def __bool__(s): return not s.iszero()

    def __eq__(s, o):
        if isinstance(o, float): return NotImplemented
        o = s._c(o)
        if o is NotImplemented: return o
        return s.v == o.v

    def __ne__(s, o):
        r = s.__eq__(o)
        return r if r is NotImplemented else not r

    def __hash__(s): return hash(s.v)
    def _cmp(s, o): return (s - s._c(o)).sign()
    def __lt__(s, o): return s._cmp(o) < 0
    def __le__(s, o): return s._cmp(o) <= 0
    def __gt__(s, o): return s._cmp(o) > 0
    def __ge__(s, o): return s._cmp(o) >= 0
    def __abs__(s): return -s if s.sign() < 0 else s

    def __float__(s):
        p, q = type(s).RADS; a, b, c, d = s.v; rp, rq = math.sqrt(p), math.sqrt(q)
        return float(a) + float(b) * rp + float(c) * rq + float(d) * rp * rq
    def f(s): return float(s)

    def __repr__(s): return MQ_STYLES[type(s).STYLE](s)
    def __str__(s): return s.__repr__()
