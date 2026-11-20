# Packet screen 2026-11-21: exact number-field arithmetic (no floats in any claim).
# A field K = Q[x]/(m(x)) with a fixed real embedding x -> r (r known to high precision).
# Elements are tuples of Fractions (coefficients of 1, x, ..., x^(n-1)).
# Exact sqrt test, exact minimal polynomials (characteristic polynomial of multiplication, factored by sympy),
# and a formal radical ring K[y_1..y_k]/(y_i^2 - a_i) used for SOUND identity proofs: an identity that holds
# in the formal ring holds for every choice of square roots, in particular for the positive real ones.
from fractions import Fraction as Fr
import mpmath as mp
import sympy as sp

mp.mp.dps = 120
X = sp.Symbol('x')


class Field:
    def __init__(self, name, poly, root_guess):
        self.name = name
        self.m = [Fr(c) for c in poly]           # low -> high, monic
        self.n = len(poly) - 1
        assert self.m[-1] == 1
        P = sp.Poly(list(reversed([int(c) for c in poly])), X)
        assert P.is_irreducible, name
        f = lambda t: sum(int(c) * t ** i for i, c in enumerate(poly))
        self.r = mp.findroot(f, mp.mpf(root_guess))
        assert abs(f(self.r)) < mp.mpf(10) ** -100
        self.pw = [self.r ** i for i in range(self.n)]
        self.cache_sqrt = {}

    # ---- basic arithmetic
    def el(self, c):
        c = [Fr(t) for t in c] + [Fr(0)] * (self.n - len(c)); return tuple(c[:self.n])
    def q(self, a): return self.el([a])
    def add(self, a, b): return tuple(x + y for x, y in zip(a, b))
    def sub(self, a, b): return tuple(x - y for x, y in zip(a, b))
    def neg(self, a): return tuple(-x for x in a)
    def scal(self, k, a): k = Fr(k); return tuple(k * x for x in a)
    def mul(self, a, b):
        n = self.n; p = [Fr(0)] * (2 * n - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y: p[i + j] += x * y
        for d in range(2 * n - 2, n - 1, -1):   # reduce x^d = -sum m_k x^(d-n+k)
            c = p[d]
            if c:
                p[d] = Fr(0)
                for k in range(n): p[d - n + k] -= c * self.m[k]
        return tuple(p[:n])
    def iszero(self, a): return all(x == 0 for x in a)
    def eq(self, a, b): return self.iszero(self.sub(a, b))
    def mulmat(self, a):
        cols = []; e = a
        for i in range(self.n):
            cols.append(e); e = self.mul(e, self.el([0, 1]))
        return [[cols[j][i] for j in range(self.n)] for i in range(self.n)]
    def inv(self, a):
        assert not self.iszero(a)
        M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row] for row in self.mulmat(a)])
        sol = M.LUsolve(sp.Matrix([1] + [0] * (self.n - 1)))
        out = self.el([Fr(int(sp.fraction(s)[0]), int(sp.fraction(s)[1])) for s in sol])
        assert self.eq(self.mul(out, a), self.q(1))
        return out
    def div(self, a, b): return self.mul(a, self.inv(b))
    def num(self, a): return sum(mp.mpf(x.numerator) / x.denominator * p for x, p in zip(a, self.pw))
    def sign(self, a):
        if self.iszero(a): return 0
        v = self.num(a); assert abs(v) > mp.mpf(10) ** -80, 'sign undecided'
        return 1 if v > 0 else -1
    def dot(self, u, w):
        s = self.q(0)
        for x, y in zip(u, w): s = self.add(s, self.mul(x, y))
        return s
    def vsub(self, u, w): return tuple(self.sub(x, y) for x, y in zip(u, w))
    def vscal(self, k, u): return tuple(self.mul(k, x) for x in u)
    def perp(self, u, d):
        return self.vsub(u, self.vscal(self.div(self.dot(u, d), self.dot(d, d)), d))
    def charpoly(self, a):
        M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row] for row in self.mulmat(a)])
        return sp.Poly(M.charpoly(X).as_expr(), X)
    def minpoly(self, a):
        """exact minimal polynomial over Q (primitive, integer coefficients) of the real number num(a)"""
        return minpoly_of_root(self.charpoly(a), self.num(a))
    def tostr(self, a):
        return ' + '.join(f'({x})*x^{i}' for i, x in enumerate(a) if x) or '0'
    # ---- exact square roots in K
    def sqrt(self, b):
        """return s in K with s*s == b and num(s) > 0, or None (None = no square root found; only completeness, never soundness, depends on it)"""
        if b in self.cache_sqrt: return self.cache_sqrt[b]
        out = None
        if self.iszero(b): out = b
        elif self.num(b) > 0:
            s = mp.sqrt(self.num(b))
            with mp.workdps(100):
                rel = mp.pslq([s] + self.pw, maxcoeff=10 ** 14, maxsteps=10 ** 5, tol=mp.mpf(10) ** -80)
            if rel and rel[0] != 0:
                cand = self.el([Fr(-c, rel[0]) for c in rel[1:]])
                if self.eq(self.mul(cand, cand), b) and self.num(cand) > 0: out = cand
        self.cache_sqrt[b] = out
        return out


def minpoly_of_root(poly, val):
    """the irreducible factor of poly (over Q) vanishing at the real number val; checked to be unique"""
    fs = [f for f, _ in sp.factor_list(poly)[1]]
    def ev(f):
        cs = [sp.Rational(c) for c in sp.Poly(f, X).monic().all_coeffs()]
        return abs(mp.polyval([mp.mpf(c.p) / c.q for c in cs], val))
    vals = [(ev(f), f) for f in fs]
    zs = [(v, f) for v, f in vals if v < mp.mpf(10) ** -60]
    assert len(zs) >= 1, 'no factor vanishes'
    # distinct irreducible factors have no common roots; if two factors appear to vanish, precision is insufficient
    assert len(set(sp.Poly(f, X).monic().as_expr() for _, f in zs)) == 1, 'two factors vanish'
    f = sp.Poly(zs[0][1], X)
    c = f.all_coeffs(); L = sp.ilcm(*[sp.Rational(t).q for t in c]); f = sp.Poly([sp.Rational(t) * L for t in c], X)
    g = sp.igcd(*[int(t) for t in f.all_coeffs()]); f = sp.Poly([int(t) // g for t in f.all_coeffs()], X)
    if f.LC() < 0: f = -f
    return f


# ---- the fields used
def fields():
    F = {}
    F['A'] = Field('Q(sqrt2,sqrt5)', [9, 0, -14, 0, 1], 3.650281539872885)      # gamma = sqrt2 + sqrt5
    F['S4'] = Field('Q(2^(1/4))', [-2, 0, 0, 0, 1], 1.189207115002721)
    F['T'] = Field('Q(t), t^3=t^2+t+1', [-1, -1, -1, 1], 1.839286755214161)     # tribonacci constant
    F['X'] = Field('Q(xi), xi^3-2xi=phi', [-1, 2, 4, -1, -4, 0, 1], 1.7155615415)  # snub dodecahedron
    return F

def A_consts(K):
    g = K.el([0, 1]); g3 = K.mul(g, K.mul(g, g))
    s2 = K.scal(Fr(1, 6), K.sub(g3, K.scal(11, g)))
    s5 = K.sub(g, s2)
    assert K.eq(K.mul(s2, s2), K.q(2)) and K.eq(K.mul(s5, s5), K.q(5)) and K.num(s2) > 0 and K.num(s5) > 0
    return s2, s5


class Radicals:
    """formal ring K[y_1..y_k]/(y_i^2 - a_i), elements dict {bitmask: K-element}.  y_i stands for the positive root of a_i
    (a_i > 0) or for i*sqrt(-a_i) (a_i = -1 only, the imaginary unit).  New radicands are reduced against single
    registered ones (a/r_i a square in K) so that the ring stays close to a field; identities proven here are sound regardless."""
    def __init__(self, K, full=10):
        self.K = K; self.rads = []; self.full = full
    def unit(self, a): return {0: a}
    def register(self, a):
        """return the formal element equal to sqrt(a) (positive real root), a in K, a > 0"""
        K = self.K
        s = K.sqrt(a)
        if s is not None: return {0: s}
        real = [i for i, r in enumerate(self.rads) if r != K.q(-1)]
        if len(real) <= self.full:   # all products of registered radicands
            subsets = [S for k in range(1, len(real) + 1) for S in __import__('itertools').combinations(real, k)]
        else:
            subsets = [(i,) for i in real]
        for S in subsets:
            den = K.q(1)
            for i in S: den = K.mul(den, self.rads[i])
            m = K.sqrt(K.div(a, den))
            if m is not None: return {sum(1 << i for i in S): m}
        self.rads.append(a); return {1 << (len(self.rads) - 1): K.q(1)}
    def imag(self):
        K = self.K
        if K.q(-1) not in self.rads: self.rads.append(K.q(-1))
        return {1 << self.rads.index(K.q(-1)): K.q(1)}
    def add(self, u, v):
        out = dict(u)
        for k, x in v.items(): out[k] = self.K.add(out.get(k, self.K.q(0)), x)
        return {k: x for k, x in out.items() if not self.K.iszero(x)}
    def neg(self, u): return {k: self.K.neg(x) for k, x in u.items()}
    def sub(self, u, v): return self.add(u, self.neg(v))
    def scal(self, c, u): return {k: self.K.mul(c, x) for k, x in u.items() if not self.K.iszero(self.K.mul(c, x))}
    def mul(self, u, v):
        K = self.K; out = {}
        for a, x in u.items():
            for b, y in v.items():
                c = K.mul(x, y); both = a & b; i = 0
                while both:
                    if both & 1: c = K.mul(c, self.rads[i])
                    both >>= 1; i += 1
                k = a ^ b; out[k] = K.add(out.get(k, K.q(0)), c)
        return {k: x for k, x in out.items() if not K.iszero(x)}
    def pow(self, u, e):
        r = {0: self.K.q(1)}
        while e:
            if e & 1: r = self.mul(r, u)
            u = self.mul(u, u); e >>= 1
        return r
    def iszero(self, u): return all(self.K.iszero(x) for x in u.values())
    def num(self, u):
        """complex value with y_i -> positive real root (or i)"""
        v = mp.mpc(0)
        for k, x in u.items():
            t = mp.mpc(self.K.num(x)); i = 0
            while k:
                if k & 1:
                    r = self.rads[i]
                    t *= mp.mpc(0, 1) if r == self.K.q(-1) else mp.sqrt(self.K.num(r))
                k >>= 1; i += 1
            v += t
        return v
