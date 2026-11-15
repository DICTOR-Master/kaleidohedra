"""Exact arithmetic for the law-giving census.

K: constants a + b*sqrt(D) (a, b rational, flint fmpq), D a squarefree integer fixed per run (2 or 5).
E: polynomials A(t) + B(t)*sqrt(D) in one parameter t (A, B flint fmpq_poly).
Roots of an E-polynomial are certified with arb balls: a root of the rational norm A^2 - D B^2 that makes A - B sqrt(D)
nonzero (ball excludes 0) is a genuine root of A + B sqrt(D) (since the product vanishes exactly there).
"""
from flint import fmpq, fmpq_poly, arb, acb, ctx
ctx.prec = 400
D = 2
def set_field(d):
    global D, SQ
    D = d; SQ = arb(d).sqrt()
SQ = arb(2).sqrt()

from fractions import Fraction as _F
def _q(x):
    if isinstance(x, _F): return fmpq(x.numerator, x.denominator)
    return fmpq(x)

class K:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0):
        s.a = a if isinstance(a, fmpq) else _q(a); s.b = b if isinstance(b, fmpq) else _q(b)
    def __add__(s, o): o = kk(o); return K(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = kk(o); return K(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return kk(o) - s
    def __neg__(s): return K(-s.a, -s.b)
    def __mul__(s, o):
        if isinstance(o, E): return E.const(s) * o
        o = kk(o); return K(s.a*o.a + D*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def inv(s):
        n = s.a*s.a - D*s.b*s.b; assert n != 0; return K(s.a/n, -s.b/n)
    def __truediv__(s, o): return s * kk(o).inv()
    def __rtruediv__(s, o): return kk(o) * s.inv()
    def iszero(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): o = kk(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a.p, s.a.q, s.b.p, s.b.q))
    def key(s): return (int(s.a.p), int(s.a.q), int(s.b.p), int(s.b.q))
    def ar(s): return arb(s.a) + arb(s.b)*SQ
    def __float__(s): return float(s.ar().mid())
    def sign(s):
        if s.iszero(): return 0
        x = s.ar(); assert not x.contains(0), 'sign undecided'
        return 1 if x > 0 else -1
    def conj(s): return K(s.a, -s.b)
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f'({s.a}{"+" if s.b >= 0 else ""}{s.b}*sqrt{D})'

def kk(x):
    if isinstance(x, K): return x
    return K(x, 0)

def pev(P, x):
    """Horner evaluation of a rational polynomial at an arb ball"""
    r = arb(0)
    for c in reversed(list(P.coeffs())): r = r*x + arb(c)
    return r

class E:
    """A(t) + B(t) sqrt(D)."""
    __slots__ = ('A', 'B')
    def __init__(s, A=None, B=None):
        s.A = A if A is not None else fmpq_poly(0); s.B = B if B is not None else fmpq_poly(0)
    @staticmethod
    def const(k):
        k = kk(k); return E(fmpq_poly([k.a]), fmpq_poly([k.b]))
    @staticmethod
    def t(): return E(fmpq_poly([0, 1]), fmpq_poly(0))
    def __add__(s, o): o = ee(o); return E(s.A + o.A, s.B + o.B)
    __radd__ = __add__
    def __sub__(s, o): o = ee(o); return E(s.A - o.A, s.B - o.B)
    def __rsub__(s, o): return ee(o) - s
    def __neg__(s): return E(-s.A, -s.B)
    def __mul__(s, o):
        o = ee(o); return E(s.A*o.A + D*s.B*o.B, s.A*o.B + s.B*o.A)
    __rmul__ = __mul__
    def __pow__(s, n):
        r = E.const(1); b = s
        while n:
            if n & 1: r = r*b
            b = b*b; n >>= 1
        return r
    def iszero(s): return s.A.is_zero() and s.B.is_zero()
    def deriv(s): return E(s.A.derivative(), s.B.derivative())
    def degree(s): return max(s.A.degree(), s.B.degree())
    def ev(s, t):
        """exact value at rational t (fmpq) -> K"""
        t = t if isinstance(t, fmpq) else _q(t); return K(s.A(t), s.B(t))
    def ar(s, x):
        """arb value at ball x"""
        return pev(s.A, x) + pev(s.B, x)*SQ
    def ar_conj(s, x): return pev(s.A, x) - pev(s.B, x)*SQ
    def norm(s):
        """rational polynomial A^2 - D B^2 (= product with conjugate)"""
        return s.A*s.A - D*s.B*s.B if not s.B.is_zero() else s.A
    def coeffs_k(s):
        n = max(s.A.degree(), s.B.degree()) + 1
        a = list(s.A.coeffs()) + [fmpq(0)]*(n - s.A.degree() - 1)
        b = list(s.B.coeffs()) + [fmpq(0)]*(n - s.B.degree() - 1)
        return [K(a[i], b[i]) for i in range(n)]
    def __repr__(s):
        return f'[{s.A}]' + (f' + [{s.B}]*sqrt{D}' if not s.B.is_zero() else '')

def ee(x):
    if isinstance(x, E): return x
    return E.const(x)

def positive_roots(e, lo=fmpq(0)):
    """Certified positive real roots of the E-polynomial e (not identically zero).
    Returns list of dicts {minpoly (Q[t] irreducible, as coefficient list), value (str 30 digits), mult_hint}."""
    assert not e.iszero()
    nm = e.norm()
    out = []
    if nm.degree() <= 0: return out
    num = nm.numer() if hasattr(nm, 'numer') else nm
    c, facs = nm.factor()
    for f, m in facs:
        if f.degree() < 1: continue
        for r, _ in f.complex_roots():
            if not r.imag.is_zero(): continue
            # real root: refine as real
            x = r.real
            if x < lo or (x.contains(lo)):
                if not (x > lo): continue
            # genuine root of e?  e(x) * conj(e)(x) = nm(x) = 0 exactly
            if e.B.is_zero():
                gen = True
            else:
                vc = e.ar_conj(x)
                if vc.contains(0):
                    ve = e.ar(x)
                    gen = None if ve.contains(0) else False
                else: gen = True
            if gen is False: continue
            out.append({'minpoly': [str(q) for q in f.coeffs()], 'deg': f.degree(), 'value': x.mid().str(30, radius=False),
                        'genuine': gen, 'mult': int(m), 'x': x})
    out.sort(key=lambda d: float(d['x'].mid()))
    return out

def same_algebraic(r1, r2):
    """two certified roots equal? same minimal polynomial and overlapping balls"""
    return r1['minpoly'] == r2['minpoly'] and r1['x'].overlaps(r2['x'])
