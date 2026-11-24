"""Exact real number fields Q[x]/(g) with one certified real root, for the plate-harmony study (25 Nov 2026).

Elements are python-flint fmpq_poly reduced modulo g (exact). Signs and numerical values come from Arb balls around the
chosen real root of g: the root is isolated by Arb's complex root finder and certified real by an exact sign change of g
at the rational ends of its ball. Minimal polynomials over Q come from the characteristic polynomial of the multiplication
map, factored over Z (FLINT). Rational multiples of pi are decided exactly (Niven; Conway-Jones): theta/pi = k/n exactly
when the minimal polynomial of 2cos(2 theta) equals FLINT's cos_minpoly(n) and the ball picks k.
"""
from fractions import Fraction
from math import gcd
from flint import fmpq_poly, fmpz_poly, fmpq, fmpz, arb, arb_poly, fmpz_mat, ctx

ctx.prec = 640


def q(s):
    s = str(s)
    if "/" in s:
        a, b = s.split("/")
        return fmpq(int(a), int(b))
    return fmpq(int(s))


class NF:
    def __init__(self, coeffs, eta, name=""):
        """coeffs: low -> high (ints or 'a/b' strings) of a polynomial with a simple real root near the decimal eta."""
        self.g = fmpq_poly([q(c) for c in coeffs])
        lc = self.g.coeffs()[-1]
        self.g = self.g / lc
        self.D = self.g.degree()
        self.name = name
        self.eta = str(eta)
        self._root = {}
        self._mp = {}
        self._rat = {}
        self.x = fmpq_poly([0, 1]) % self.g if self.D > 1 else fmpq_poly([-self.g.coeffs()[0]])
        self.zero = E(self, fmpq_poly([0]))
        self.one = E(self, fmpq_poly([1]))
        self.root(640)

    def c(self, v):
        if isinstance(v, E): return v
        if isinstance(v, (int, fmpz)): return E(self, fmpq_poly([v]))
        if isinstance(v, (fmpq, Fraction)): return E(self, fmpq_poly([fmpq(v.numerator, v.denominator)]))
        return E(self, fmpq_poly([q(v)]))

    def from_coeffs(self, cl):
        return E(self, fmpq_poly([q(c) for c in cl]) % self.g)

    def gen(self):
        return E(self, self.x)

    def root(self, prec):
        if prec in self._root: return self._root[prec]
        old = ctx.prec; ctx.prec = prec
        if self.D == 1:
            r = arb(-self.g.coeffs()[0])
        else:
            den = self.g.denom()
            gz = fmpz_poly([int(c * den) for c in self.g.coeffs()])
            eta = arb(self.eta)
            rts = sorted((abs(float((rr.real - eta).mid())), rr) for rr, m in gz.complex_roots() if abs(rr.imag) < arb(10) ** -20)
            assert rts and (len(rts) == 1 or rts[1][0] > 3 * rts[0][0]), f"root of {self.name} not isolated near {self.eta}"
            r0 = rts[0][1].real
            lo, hi = r0.lower(), r0.upper()
            # rational ends; exact sign change certifies a real root in the ball (and the balls isolate the roots)
            lq = _arf_to_fmpq(lo); hq = _arf_to_fmpq(hi)
            assert self.g(lq) * self.g(hq) < 0, "real root not certified by a sign change"
            r = arb(r0.mid(), r0.rad())
        ctx.prec = old
        self._root[prec] = r
        return r


def _arf_to_fmpq(a):
    """exact rational value of an Arb endpoint (an arb with radius 0)"""
    m, e = a.man_exp()
    m, e = int(m), int(e)
    return fmpq(m * 2 ** e) if e >= 0 else fmpq(m, 2 ** (-e))


class E:
    __slots__ = ("F", "p")

    def __init__(self, F, p):
        self.F = F; self.p = p

    def _c(self, o):
        if isinstance(o, E): return o.p
        return fmpq_poly([q(o)]) if not isinstance(o, (int, fmpz, fmpq)) else fmpq_poly([o])

    def __add__(s, o): return E(s.F, s.p + s._c(o))
    __radd__ = __add__
    def __sub__(s, o): return E(s.F, s.p - s._c(o))
    def __rsub__(s, o): return E(s.F, s._c(o) - s.p)
    def __neg__(s): return E(s.F, -s.p)
    def __mul__(s, o): return E(s.F, (s.p * s._c(o)) % s.F.g)
    __rmul__ = __mul__

    def inv(s):
        if s.F.D == 1:
            return E(s.F, fmpq_poly([1 / s.p.coeffs()[0]]))
        d, a, b = s.p.xgcd(s.F.g)
        assert d == 1, "not invertible"
        return E(s.F, a % s.F.g)

    def __truediv__(s, o):
        if not isinstance(o, E): o = s.F.c(o)
        return s * o.inv()

    def __rtruediv__(s, o): return s.F.c(o) * s.inv()

    def __bool__(s): return s.p.degree() >= 0
    def __eq__(s, o): return not bool(s - o)
    def __hash__(s): return hash(s.key())
    def key(s): return tuple(str(c) for c in s.p.coeffs())

    def ball(s, prec=640):
        old = ctx.prec; ctx.prec = prec
        r = s.F.root(prec)
        v = arb_poly([arb(c) for c in s.p.coeffs()])(r) if s.p.degree() >= 0 else arb(0)
        ctx.prec = old
        return v

    def sign(s):
        if not s: return 0
        for prec in (640, 2560, 10240):
            v = s.ball(prec)
            if v > 0: return 1
            if v < 0: return -1
        raise AssertionError("sign not certified")

    def minpoly(s):
        """monic minimal polynomial over Q (fmpq_poly)"""
        F = s.F; k = s.key()
        if k in F._mp: return F._mp[k]
        if F.D == 1 or s.p.degree() <= 0:
            c = s.p.coeffs()[0] if s.p.degree() >= 0 else fmpq(0)
            m = fmpq_poly([-c, 1])
        else:
            D = F.D
            cols = []
            t = s.p
            for j in range(D):
                cs = list(t.coeffs()) + [fmpq(0)] * (D - t.degree() - 1)
                cols.append(cs[:D])
                t = (t * F.x) % F.g
            L = 1
            for col in cols:
                for c in col: L = L * c.q // gcd(L, int(c.q))
            N = fmpz_mat([[int(cols[j][i] * L) for j in range(D)] for i in range(D)])
            P = N.charpoly()
            fac = [f for f, e in P.factor()[1]]
            # minimal polynomial of L*s: the factor vanishing at its ball
            v = s.ball() * L
            hits = [f for f in fac if arb_poly([arb(c) for c in f.coeffs()])(v).contains(0)]
            assert len(hits) == 1, "minimal polynomial factor not unique"
            f = hits[0]
            d = f.degree(); fc = f.coeffs()
            m = fmpq_poly([fmpq(fc[i]) / fmpq(L) ** (d - i) / fmpq(fc[d]) for i in range(d + 1)])  # m(t) = f(L t)/(lc L^d)
        F._mp[k] = m
        return m


# ---------------------------------------------------------------- rational multiples of pi
_PHI = None


def totients(N=40000):
    global _PHI
    if _PHI is None or len(_PHI) <= N:
        ph = list(range(N + 1))
        for p in range(2, N + 1):
            if ph[p] == p:
                for m in range(p, N + 1, p): ph[m] -= ph[m] // p
        _PHI = ph
    return _PHI


_CM = {}


def cos_minpoly(n):
    if n not in _CM: _CM[n] = fmpz_poly.cos_minpoly(n)
    return _CM[n]


def rational_angle(c):
    """c = 2cos(2 theta) in a field, theta in [0, pi/2]. Returns Fraction k/n with theta = (k/n) pi exactly, or None when
    theta/pi is irrational (decided exactly: Niven / Conway-Jones via minimal polynomials)."""
    F = c.F; k = c.key()
    if k in F._rat: return F._rat[k]
    m = c.minpoly()
    out = None
    if all(x.q == 1 for x in m.coeffs()):
        mz = fmpz_poly([int(x.p) for x in m.coeffs()])
        d = mz.degree()
        ph = totients()
        cands = [1, 2, 3, 4, 6] if d == 1 else [n for n in range(5, 8 * d * d + 13) if ph[n] == 2 * d]
        old = ctx.prec; ctx.prec = 640
        half = c.ball() / 2
        if half > 1: half = arb(1)
        if half < -1: half = arb(-1)
        tp = half.acos() / (2 * arb.pi())          # theta / pi
        for n in cands:
            if cos_minpoly(n) == mz:
                kk = round(float((tp * n).mid()))
                for kc in (kk - 1, kk, kk + 1):
                    if 0 <= kc and 2 * kc <= n and gcd(kc, n) == 1 and abs(tp * n - kc) < arb(10) ** -30:
                        out = Fraction(kc, n)
                assert out is not None, "rational angle: k not identified"
                break
        ctx.prec = old
    F._rat[k] = out
    return out


def cheb_C(k, y, one):
    """C_k(y) = 2 T_k(y/2): C_k(2cos a) = 2cos(k a)"""
    a, b = one * 2, y
    if k == 0: return a
    for _ in range(k - 1):
        a, b = b, y * b - a
    return b
