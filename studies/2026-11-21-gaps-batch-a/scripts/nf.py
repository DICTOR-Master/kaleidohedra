# nf.py -- exact arithmetic in a number field Q(theta), theta a fixed real root of an irreducible rational polynomial.
# Elements are coefficient tuples (Fractions) in the power basis 1, theta, ..., theta^(n-1). Zero tests are exact (all coefficients 0);
# the sign of a NONZERO element is read from a 150-digit evaluation (mpmath) and refused if |value| < 1e-100 (never happened).
# Study 2026-11-21-gaps-batch-a.
from fractions import Fraction as Fr
from mpmath import mp, mpf, polyroots, findroot
mp.dps = 150

class Field:
    def __init__(self, name, minpoly, approx):
        """minpoly: integer/Fraction coefficients, highest degree first, monic after scaling; approx: float near the chosen real root"""
        c = [Fr(x) for x in minpoly]; c = [x / c[0] for x in c]; self.n = len(c) - 1; self.name = name
        self.red = [-x for x in c[1:]][::-1]                  # theta^n = sum red[i] theta^i
        f = lambda x: sum(mpf(ci.numerator) / ci.denominator * x ** (self.n - i) for i, ci in enumerate(c))
        self.theta = findroot(f, mpf(approx)); assert abs(f(self.theta)) < mpf(10) ** -140
        self.pw = [self.theta ** i for i in range(self.n)]
        self.minpoly = c
    def __call__(self, *coef):
        v = [Fr(0)] * self.n
        for i, x in enumerate(coef): v[i] = Fr(x)
        return E(self, tuple(v))
    def gen(self): return self(0, 1) if self.n > 1 else self(0)

class E:
    __slots__ = ('F', 'c')
    def __init__(s, F, c): s.F = F; s.c = c
    def _o(s, o): return o if isinstance(o, E) else E(s.F, (Fr(o),) + (Fr(0),) * (s.F.n - 1))
    def __add__(s, o): o = s._o(o); return E(s.F, tuple(a + b for a, b in zip(s.c, o.c)))
    __radd__ = __add__
    def __sub__(s, o): o = s._o(o); return E(s.F, tuple(a - b for a, b in zip(s.c, o.c)))
    def __rsub__(s, o): return s._o(o) - s
    def __neg__(s): return E(s.F, tuple(-a for a in s.c))
    def __mul__(s, o):
        if not isinstance(o, E):
            o = Fr(o); return E(s.F, tuple(a * o for a in s.c))
        n = s.F.n; p = [Fr(0)] * (2 * n - 1)
        for i, a in enumerate(s.c):
            if a:
                for j, b in enumerate(o.c):
                    if b: p[i + j] += a * b
        for k in range(2 * n - 2, n - 1, -1):              # reduce theta^k
            if p[k]:
                x = p[k]; p[k] = Fr(0)
                for i, r in enumerate(s.F.red): p[k - n + i] += x * r
        return E(s.F, tuple(p[:n]))
    __rmul__ = __mul__
    def inv(s):
        # solve s * y = 1 by linear algebra over Q (multiplication matrix)
        n = s.F.n; cols = []
        b = [Fr(0)] * n
        for j in range(n):
            ej = E(s.F, tuple(Fr(1) if k == j else Fr(0) for k in range(n))); cols.append((s * ej).c)
        A = [[cols[j][i] for j in range(n)] + [Fr(1) if i == 0 else Fr(0)] for i in range(n)]
        for col in range(n):
            piv = next(r for r in range(col, n) if A[r][col] != 0); A[col], A[piv] = A[piv], A[col]
            pv = A[col][col]; A[col] = [x / pv for x in A[col]]
            for r in range(n):
                if r != col and A[r][col] != 0:
                    m = A[r][col]; A[r] = [x - m * y for x, y in zip(A[r], A[col])]
        return E(s.F, tuple(A[i][n] for i in range(n)))
    def __truediv__(s, o):
        if not isinstance(o, E): return s * (Fr(1) / Fr(o))
        return s * o.inv()
    def __rtruediv__(s, o): return s._o(o) * s.inv()
    def iszero(s): return not any(s.c)
    def __eq__(s, o): o = s._o(o); return s.c == o.c
    def __hash__(s): return hash(s.c)
    def mp(s): return sum(mpf(a.numerator) / a.denominator * p for a, p in zip(s.c, s.F.pw))
    def sign(s):
        if s.iszero(): return 0
        v = s.mp()
        if abs(v) < mpf(10) ** -100: raise ArithmeticError('sign undecided at 150 digits')
        return 1 if v > 0 else -1
    def __float__(s): return float(s.mp())
    def __repr__(s): return '[' + ', '.join(str(a) for a in s.c) + ']'

def vadd(u, v): return [a + b for a, b in zip(u, v)]
def vsub(u, v): return [a - b for a, b in zip(u, v)]
def vmul(k, u): return [k * a for a in u]
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cross(u, v): return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
def iszerov(u): return all(x.iszero() for x in u)
def key(u): return tuple(x.c for x in u)

# the four fields used (each contains sqrt5, so the golden star t = phi is exact everywhere)
def fields():
    Q5 = Field('Q(sqrt5)', [1, 0, -5], 2.236)
    Q25 = Field('Q(sqrt2, sqrt5) = Q(theta), theta = sqrt2 + sqrt5', [1, 0, -14, 0, 9], 3.65)
    # snub cube: tribonacci t (t^3 = t^2 + t + 1) with sqrt5; primitive element theta = t + sqrt5 (minimal polynomial x^6 - 2x^5 - 16x^4 + 20x^3 + 68x^2 - 88x - 44, from sympy; t and sqrt5 recovered and checked exactly in build_dataset.py)
    QT5 = Field('Q(t, sqrt5) = Q(theta), theta = t + sqrt5, t the tribonacci constant', [1, -2, -16, 20, 68, -88, -44], 4.0754)
    # snub dodecahedron: xi^3 - 2 xi = phi, i.e. xi^6 - 4 xi^4 - xi^3 + 4 xi^2 + 2 xi - 1 = 0 (phi = xi^3 - 2 xi)
    QXI = Field('Q(xi), xi^3 - 2 xi = phi', [1, 0, -4, -1, 4, 2, -1], 1.7155615)
    return Q5, Q25, QT5, QXI
