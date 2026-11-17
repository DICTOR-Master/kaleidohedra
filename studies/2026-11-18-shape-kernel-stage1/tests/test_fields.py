#!/usr/bin/env python3
"""Tests of the general number fields of the shape kernel (stage 1 proper, 2026-11-18): kernel/field.py (NF, MQ), kernel/zphi.py,
Quad.sqrt and qsign in kernel/exact.py.  The pilot's tests of Quad (tests/test_kernel.py) run unchanged beside this file.
  A. checks ported from the copies (asserts and stated identities in cubes_lib.py, exactlib.py, zsurf.py, mixlib.py,
     octet_special_exact.py and their studies)
  B. field and order axioms on random elements of every field the copies use
  H. the bronze ratio Q(sqrt13) and the heptagonal field Q(cos 2pi/7) (rho = 2cos(pi/7), sigma = rho^2 - 1, T = tan(pi/14)tan(2pi/7))
  L. established libraries: the kernel sign against a certified Arb ball sign (python-flint); irreducibility from FLINT's
     fmpz_poly.factor; the heptagonal and bronze minimal polynomials from sympy.minimal_polynomial
  C. exact sign against mpmath at 150 digits on near-zero elements built from units: Lucas/Fibonacci and Pell units, their
     products and differences in Q(sqrt2, sqrt5); the units 1 + 2^(1/3) + 4^(1/3) and 4 + 3*3^(1/3) + 2*9^(1/3) of the pure cubic
     fields; a unit of the cubic field of #56 Sonsam and Lahdeli found by search; phi^-k in the golden basis
  D. cross-checks between independent methods (interval sign against the quadratic rule; NF over GOLDEN against zphi and Quad)
  E. guards: mixed fields, floats, division by zero, a reducible polynomial, an interval holding two roots
Prints one line per check and FINAL ok only if every check passes.  usage: test_fields.py [n_random]"""
import os, sys, random, math, itertools
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kernel import Quad, qsign, PHI, R2, R5
from kernel.field import NF, MQ, NumberField, GOLDEN, pure_field, sturm_count, NF_STYLES, MQ_STYLES, arb_sign_nf, arb_sign_mq
from kernel import zphi as Z
import mpmath
mpmath.mp.dps = 150

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
rng = random.Random(20261118)
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok)))
    print(('ok   ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail and not ok else ''))


def _try(f, e):
    try: f()
    except e: return True
    except Exception: return False
    return False


def rfr(m=50): return Fr(rng.randint(-m, m), rng.randint(1, m))


# fields under test
CUB2, CUB3, CUB6 = pure_field(2, 3), pure_field(3, 3), pure_field(6, 3)
RAD4 = pure_field(2, 4)                                           # Q(2^(1/4)), degree 4
LAH = NumberField.get([1536, 5184, -3384, 11], Fr(-1, 8), Fr(5, 24), 't')     # #56 Sonsam and Lahdeli (dicto-lahdeli.json)
R6Q = pure_field(6, 2)                                             # octet_special_exact: Q(sqrt6) in the power basis
BRONZE = NumberField.get([1, -3, -1], 3, 4, 'beta').set_fast()      # bronze ratio beta = (3 + sqrt13)/2: beta^2 = 3 beta + 1 (DICTO 18 Nov)
HEPT = NumberField.get([1, -1, -2, 1], Fr(9, 5), Fr(19, 10), 'rho')   # heptagonal field Q(cos 2pi/7): rho = 2cos(pi/7), rho^3 - rho^2 - 2rho + 1 = 0
NFS = {'Q(sqrt13), bronze basis': BRONZE, 'Q(cos 2pi/7), rho basis': HEPT, 'Q(2^(1/3))': CUB2, 'Q(3^(1/3))': CUB3, 'Q(6^(1/3))': CUB6, 'Q(2^(1/4))': RAD4, 'Q(t) of #56': LAH, 'golden': GOLDEN, 'Q(sqrt6) power basis': R6Q}


def rnf(F, m=50):
    k = rng.random()
    c = [rfr(m) for _ in range(F.n)]
    if k < 0.1: c = [c[0]] + [Fr(0)] * (F.n - 1)
    return NF(c, F)


def rmq(m=50):
    v = [rfr(m) if rng.random() > 0.15 else Fr(0) for _ in range(4)]
    return MQ(*v)


# ------------------------------------------------------------------------------------------------ A. ported checks
S2, S5 = MQ(0, 1), MQ(0, 0, 1); KPHI = MQ(Fr(1, 2), 0, Fr(1, 2))
check('A1 cubes_lib: sqrt2^2 = 2, sqrt5^2 = 5, (sqrt2 sqrt5)^2 = 10, phi^2 = phi + 1 in K', S2 * S2 == 2 and S5 * S5 == 5 and (S2 * S5) * (S2 * S5) == 10
      and KPHI * KPHI == KPHI + 1 and S2 * S5 == MQ(0, 0, 0, 1))
check('A2 cubes_lib: conj2 and conj5 are field automorphisms (on 300 random pairs)', all(
    (x * y).conj2() == x.conj2() * y.conj2() and (x + y).conj5() == x.conj5() + y.conj5() and (x * y).conj5() == x.conj5() * y.conj5()
    for x, y in ((rmq(), rmq()) for _ in range(300))))
check('A3 cubes_lib kstr printed form: 1/2 + √2 - 3√5 - √10', repr(MQ(Fr(1, 2), 1, -3, -1)) == '1/2 + √2 - 3√5 - √10' and repr(MQ()) == '0')
r2 = NF([0, 1], CUB2)
check('A4 exactlib KC: r^3 = 2 in Q(2^(1/3)); norm = a^3 + k b^3 + k^2 c^3 - 3kabc (KC.norm) on 300 random elements',
      r2 ** 3 == 2 and all((lambda x, k: x.norm() == x.c[0] ** 3 + k * x.c[1] ** 3 + k * k * x.c[2] ** 3 - 3 * k * x.c[0] * x.c[1] * x.c[2])(rnf(F), F.pure[0])
                           for F in (CUB2, CUB3, CUB6) for _ in range(100)))
check('A5 exactlib KC: sign = sign of the norm (KC.sign, the copy\'s rule: the other two conjugates are complex) on 600 elements',
      all((lambda x: x.sign() == (x.norm() > 0) - (x.norm() < 0))(rnf(F)) for F in (CUB2, CUB3, CUB6) for _ in range(200)))
check('A6 exactlib AlgField: the #56 field: poly_string, key and the 30-digit decimal of t in dicto-lahdeli.json',
      LAH.poly_string() == '1536*t**3 + 5184*t**2 - 3384*t + 11' and NF([0, 1], LAH).dec(30) == '0.003266956983082001167961097613'
      and LAH.key == ('alg', 't', (Fr(1536), Fr(5184), Fr(-3384), Fr(11)), Fr(-1, 8), Fr(5, 24)))
check('A7 exactlib KC printed form: 1/2 + (3/2)*2**(1/3) - 2**(2/3)', NF_STYLES['kc'](NF([Fr(1, 2), Fr(3, 2), -1], CUB2)) == '1/2 + (3/2)*2**(1/3) - 2**(2/3)')
check('A8 octet_special_exact: (2 - sqrt2)^2 = 6 - 4 sqrt2 in the power basis (edge^2 of both pieces); r^3 = 2 for the Delian bond',
      (2 - NF([0, 1], pure_field(2, 2))) ** 2 == NF([6, -4], pure_field(2, 2)) and NF([0, 1], CUB2) ** 3 == NF([2], CUB2))
g = NF([0, 1], GOLDEN)
check('A9 mixlib / zsurf: phi^2 = phi + 1, phi (phi - 1) = 1, norm(a + b phi) = a^2 + ab - b^2 (mixlib inv)', g * g == g + 1 and g * (g - 1) == 1
      and all((lambda a, b: NF([a, b], GOLDEN).norm() == a * a + a * b - b * b)(rfr(), rfr()) for _ in range(300)))
AX6 = [((1, 0), (0, 1), (0, 0)), ((-1, 0), (0, 1), (0, 0)), ((0, 0), (1, 0), (0, 1)), ((0, 0), (-1, 0), (0, 1)), ((0, 1), (0, 0), (1, 0)), ((0, -1), (0, 0), (1, 0))]
def zdot(u, v): return Z.zadd(Z.zadd(Z.zmul(u[0], v[0]), Z.zmul(u[1], v[1])), Z.zmul(u[2], v[2]))
check('A10 zsurf AX6: the six five-fold axes (1, phi, 0) ... have |e|^2 = phi + 2 and pairwise e.f = +-phi (Z[phi], exact)',
      all(zdot(e, e) == (2, 1) for e in AX6) and all(zdot(e, f) in ((0, 1), (0, -1)) for e, f in itertools.combinations(AX6, 2)))
check('A11 zsurf zconj: the Galois twin is a ring automorphism on Z[phi] and x zconj(x) = norm (300 random integer pairs)', all(
    (lambda x, y: Z.zconj(Z.zmul(x, y)) == Z.zmul(Z.zconj(x), Z.zconj(y)) and Z.zmul(x, Z.zconj(x)) == (Z.znorm(x), 0))(
        (rng.randint(-99, 99), rng.randint(-99, 99)), (rng.randint(-99, 99), rng.randint(-99, 99))) for _ in range(300)))

# ------------------------------------------------------------------------------------------------ B. axioms
def axioms(tag, gen, n):
    bad = []
    for _ in range(n):
        x, y, z = gen(), gen(), gen()
        o = [(x + y) + z == x + (y + z), (x * y) * z == x * (y * z), x + y == y + x, x * y == y * x, x * (y + z) == x * y + x * z,
             x + 0 == x, x * 1 == x, x - x == 0, x + (-x) == 0]
        if not x.iszero(): o.append(x * x.inv() == 1 and (y / x) * x == y)
        sx, sy = x.sign(), y.sign()
        o += [sum((x < y, x == y, x > y)) == 1, (x * y).sign() == sx * sy, (-x).sign() == -sx, abs(x).sign() >= 0,
              (x < y) == ((x + z) < (y + z)), (not (x < y and z.sign() > 0)) or x * z < y * z,
              (not (x <= y and y <= z)) or x <= z, (x == y) <= (hash(x) == hash(y)), x ** 3 == x * x * x, x ** 0 == 1]
        if hasattr(x, 'norm'): o.append((x * y).norm() == x.norm() * y.norm())
        if not all(o): bad.append((x, y, z, [i for i, v in enumerate(o) if not v]))
    check(f'B {tag}: field and order axioms on {n} random triples', not bad, f'{len(bad)} failing, e.g. {bad[:1]}')


axioms('Q(sqrt2, sqrt5) (MQ)', rmq, N)
for nm, F in NFS.items(): axioms(nm + ' (NF)', lambda F=F: rnf(F), max(200, N // 4) if F.n > 2 else N // 2)

# ------------------------------------------------------------------------------------------------ C. sign against mpmath, near-zero
def mp_root(F):
    rts = mpmath.polyroots([mpmath.mpf(c.numerator) / c.denominator for c in F.P], maxsteps=400, extraprec=600)
    real = [mpmath.re(r) for r in rts if abs(mpmath.im(r)) < mpmath.mpf(10) ** -100 and mpmath.mpf(F.lo0.numerator) / F.lo0.denominator < mpmath.re(r) < mpmath.mpf(F.hi0.numerator) / F.hi0.denominator]
    assert len(real) == 1
    return real[0]


ROOT = {F.key: mp_root(F) for F in NFS.values()}


def mp_nf(x): t = ROOT[x.F.key]; return sum(mpmath.mpf(c.numerator) / c.denominator * t ** i for i, c in enumerate(x.c))


def mp_mq(x):
    p, q = x.RADS; sp, sq = mpmath.sqrt(p), mpmath.sqrt(q)
    a, b, c, d = (mpmath.mpf(v.numerator) / v.denominator for v in x.v)
    return a + b * sp + c * sq + d * sp * sq


F_, L_ = [0, 1], [2, 1]
for n in range(80): F_.append(F_[-1] + F_[-2]); L_.append(L_[-1] + L_[-2])
hard_mq = []
e2 = MQ(-1, 1); e5 = MQ(Fr(-1, 2), 0, Fr(1, 2))           # sqrt2 - 1 and 1/phi, both in (0, 1): powers are tiny units
for i in range(1, 30, 3):
    for j in range(1, 40, 4):
        u, w = e2 ** i, e5 ** j
        hard_mq += [u * w, -(u * w), u - w, w - u, u * w * MQ(0, 0, 0, 1) - u * w * MQ(3, 1, 1, 0) / 5]
hard_mq += [MQ(L_[n], 0, -F_[n]) for n in range(2, 70, 3)] + [MQ(u, -w) for u, w in ((3, 2), (17, 12), (99, 70), (577, 408), (3363, 2378), (19601, 13860))]
hard_nf = []
units = {BRONZE: NF([0, 1], BRONZE), HEPT: NF([0, 1], HEPT), CUB2: NF([1, 1, 1], CUB2), CUB3: NF([4, 3, 2], CUB3), GOLDEN: NF([0, 1], GOLDEN), R6Q: NF([5, 2], R6Q), RAD4: NF([1, 1], RAD4)}
# a unit of the #56 field: search a + b s + c s^2 in Z[s], s = 24 t (s^3 + 81 s^2 - 1269 s + 99 = 0), |a|, |b|, |c| <= 40, norm +-1
# (integer norm: the determinant of multiplication by the element in the basis 1, s, s^2)
def _norm_int(a, b, c, p=81, q=-1269, r=99):
    def ts(u): return (-r * u[2], u[0] - q * u[2], u[1] - p * u[2])
    c0 = (a, b, c); c1 = ts(c0); c2 = ts(c1)
    return (c0[0] * (c1[1] * c2[2] - c1[2] * c2[1]) - c1[0] * (c0[1] * c2[2] - c0[2] * c2[1]) + c2[0] * (c0[1] * c1[2] - c0[2] * c1[1]))
found = None
for a, b, c in itertools.product(range(-40, 41), repeat=3):
    if (b, c) != (0, 0) and abs(_norm_int(a, b, c)) == 1: found = (a, b, c); break
s24 = NF([0, 24], LAH)
check('C0 the integer norm agrees with the kernel norm on 200 elements of Z[s] (s = 24 t)', all(
    (lambda a, b, c: _norm_int(a, b, c) == (a + b * s24 + c * s24 * s24).norm())(rng.randint(-40, 40), rng.randint(-40, 40), rng.randint(-40, 40)) for _ in range(200)))
if found is not None:
    units[LAH] = found[0] + found[1] * s24 + found[2] * s24 * s24
print(f'     unit of the #56 field with coefficients <= 40 in Z[24 t]: {found if found else "none found (near-zero elements there come from rational approximations of t)"}')
for F, u in units.items():
    if u.sign() < 0: u = -u
    if u > 1: u = u.inv()
    v = u * u + u if F.n > 1 else u
    for k in range(1, 45 if F.n <= 2 else 25, 2):
        w = u ** k; hard_nf += [w, -w, w - u ** (k + 1), u ** (k + 1) - w * (1 + u)]
    for k in range(1, 15): hard_nf += [u ** k - v ** k]
# rational approximations of t: t - p/q with q = 10^k (tiny, both signs)
for F in NFS.values():
    t = NF([0, 1], F); ap = F.approx(Fr(1, 10 ** 30))
    for k in range(5, 30, 4): r = Fr(math.floor(ap * 10 ** k), 10 ** k); hard_nf += [t - r, r + Fr(1, 10 ** k) - t]
rand_mq = [rmq(10 ** 9) for _ in range(N // 3)]; rand_nf = [rnf(F, 10 ** 9) for F in NFS.values() for _ in range(N // 10)]
mism, small = [], 0
for x in hard_mq + rand_mq:
    v = mp_mq(x)
    if v == 0 and not x.iszero(): small += 1
    if mpmath.sign(v) != x.sign(): mism.append(x)
for x in hard_nf + rand_nf:
    v = mp_nf(x)
    if abs(v) < mpmath.mpf(10) ** -120: small += 1; continue
    if mpmath.sign(v) != x.sign(): mism.append(x)
tiny = min(min(abs(mp_mq(x)) for x in hard_mq), min(abs(mp_nf(x)) for x in hard_nf if not x.iszero()))
check(f'C1 exact sign = sign at 150 digits (mpmath) on {len(hard_mq)} near-zero and {len(rand_mq)} random elements of Q(sqrt2, sqrt5), '
      f'{len(hard_nf)} near-zero and {len(rand_nf)} random elements of the NF fields (smallest |x| = {mpmath.nstr(tiny, 3)})',
      not mism and small == 0, f'{len(mism)} mismatches, {small} too small for 150 digits')
fw = sum(1 for x in hard_mq if (float(x) > 0) - (float(x) < 0) != x.sign())
print(f'     (for comparison: float64 gets the sign wrong on {fw} of the {len(hard_mq)} near-zero elements of Q(sqrt2, sqrt5))')
check('C2 digits(40) of NF elements agree with the 150-digit value to 1e-39 (200 random elements)', all(
    abs(mpmath.mpf(x.digits(40)) - mp_nf(x)) <= mpmath.mpf(10) ** -39 for x in rand_nf[:200]))

# ------------------------------------------------------------------------------------------------ H. the bronze and heptagonal scales
bb = NF([0, 1], BRONZE); B13 = Quad(Fr(3, 2), Fr(1, 2), 13)
def b2q(x): return Quad(x.c[0] + Fr(3, 2) * x.c[1], x.c[1] / 2, 13)         # a + b beta = (a + 3b/2) + (b/2) sqrt13
br = [NF([rfr(10 ** 6), rfr(10 ** 6)], BRONZE) for _ in range(N)] + [x for x in hard_nf if x.F is BRONZE]
check(f'H1 bronze ratio: beta^2 = 3 beta + 1, beta (beta - 3) = 1, beta = (3 + sqrt13)/2; sign, product and inverse agree with Quad in Q(sqrt13) ({len(br)} elements, beta^-k near-zero units included)',
      bb * bb == 3 * bb + 1 and bb * (bb - 3) == 1 and b2q(bb) == B13 and B13 * B13 == 3 * B13 + 1
      and all(x.sign() == b2q(x).sign() for x in br) and all(b2q(x * y) == b2q(x) * b2q(y) and (x.iszero() or b2q(x.inv()) == b2q(x).inv()) for x, y in zip(br, br[1:] + br[:1])))
rho = NF([0, 1], HEPT); sig = rho * rho - 1; cc = (rho * rho - 2) / 2       # sigma = rho^2 - 1, c = cos(2pi/7) = (rho^2 - 2)/2
T = 9 - 4 * cc - 16 * cc * cc
check('H2 heptagonal field: rho^3 - rho^2 - 2 rho + 1 = 0; rho sigma = rho + sigma; c = (rho^2 - 2)/2 satisfies 8c^3 + 4c^2 - 4c - 1 = 0',
      rho ** 3 - rho * rho - 2 * rho + 1 == 0 and rho * sig == rho + sig and 8 * cc ** 3 + 4 * cc ** 2 - 4 * cc - 1 == 0)
check('H3 T = 9 - 4c - 16c^2 satisfies its minimal polynomial x^3 - 9x^2 - x + 1 = 0 (exact in Q(rho)), and T = tan(pi/14) tan(2pi/7) to 140 digits',
      T ** 3 - 9 * T * T - T + 1 == 0 and abs(mp_nf(T) - mpmath.tan(mpmath.pi / 14) * mpmath.tan(2 * mpmath.pi / 7)) < mpmath.mpf(10) ** -140
      and abs(mp_nf(rho) - 2 * mpmath.cos(mpmath.pi / 7)) < mpmath.mpf(10) ** -140 and abs(mp_nf(cc) - mpmath.cos(2 * mpmath.pi / 7)) < mpmath.mpf(10) ** -140)
HS = [rho, sig, cc, T, 1 / rho, 1 / sig, rho - sig + 1, T - Fr(1, 3), sig / rho, rho * rho - sig - 1 + Fr(1, 10 ** 30)]
HS += [rho ** i * sig ** j - sig ** j2 * rho ** i2 for i, j, i2, j2 in ((3, -2, -1, 1), (5, -4, -2, 2), (8, -7, 0, 1), (-6, 5, 1, -2))] + [rho ** -k for k in range(1, 40, 3)] + [sig ** -k - rho ** -k for k in range(2, 30, 4)]
okH = all(x.sign() == int(mpmath.sign(mp_nf(x))) for x in HS if abs(mp_nf(x)) > mpmath.mpf(10) ** -120) and all(
    (x < y) == (mp_nf(x) < mp_nf(y)) for x in HS for y in HS)
check(f'H4 heptagonal sign and order: {len(HS)} elements built from rho, sigma, c, T and the units rho, sigma (powers and differences), every sign and all '
      f'{len(HS) ** 2} comparisons agree with 150-digit values', okH)

# ------------------------------------------------------------------------------------------------ L. established libraries
import flint, sympy
allC = hard_mq + rand_mq
okL1 = all(arb_sign_mq(x) == x.sign() for x in allC) and all(arb_sign_nf(list(x.c), x.F) == x.sign() for x in hard_nf + rand_nf + HS)
check(f'L1 kernel sign = certified Arb ball sign (python-flint {flint.__version__}) on all {len(allC) + len(hard_nf) + len(rand_nf) + len(HS)} elements of C1 and H4', okL1)
red = NumberField([1, -3, -2, 6], 1, 2, 'u')
check('L2 irreducibility from FLINT fmpz_poly.factor: every field above irreducible; (x^2 - 2)(x - 3) reducible',
      all(F.irreducible for F in NFS.values()) and red.irreducible is False)
X = sympy.Symbol('x')
mpT = sympy.minimal_polynomial(sympy.tan(sympy.pi / 14) * sympy.tan(2 * sympy.pi / 7), X)
mpB = sympy.minimal_polynomial((3 + sympy.sqrt(13)) / 2, X); mpR = sympy.minimal_polynomial(2 * sympy.cos(sympy.pi / 7), X)
check(f'L3 sympy {sympy.__version__} minimal_polynomial: tan(pi/14)tan(2pi/7) -> {mpT}, (3 + sqrt13)/2 -> {mpB}, 2cos(pi/7) -> {mpR} (the kernel fields\' polynomials)',
      sympy.expand(mpT - (X ** 3 - 9 * X ** 2 - X + 1)) == 0 and sympy.expand(mpB - (X ** 2 - 3 * X - 1)) == 0 and sympy.expand(mpR - (X ** 3 - X ** 2 - 2 * X + 1)) == 0)

# ------------------------------------------------------------------------------------------------ D. cross-checks
def tower_sign(x):
    """sign of P + Q sqrt5 with P, Q in Q(sqrt2): same signs win, else compare P^2 and 5 Q^2 (the cubes_lib rule), via Quad"""
    a, b, c, d = x.v; P, Q = Quad(a, b, 2), Quad(c, d, 2)
    sp, sq = P.sign(), Q.sign()
    if sq == 0: return sp
    if sp == 0 or sp == sq: return sq if sp == 0 else sp
    t = (P * P - Q * Q * 5).sign()
    return sp if t > 0 else sq
check(f'D1 MQ interval sign = tower rule (Quad) on all {len(hard_mq) + len(rand_mq)} elements of C1', all(tower_sign(x) == x.sign() for x in hard_mq + rand_mq))
gl = [NF([rfr(10 ** 6), rfr(10 ** 6)], GOLDEN) for _ in range(N)] + [x for x in hard_nf if x.F is GOLDEN]
def g2q(x): return Quad(x.c[0] + x.c[1] / 2, x.c[1] / 2, 5)          # a + b phi = (a + b/2) + (b/2) sqrt5
check(f'D2 NF over GOLDEN = Quad: sign(a + b phi) = qsign(2a + b, b, 5) = Quad sign, and products and inverses agree ({len(gl)} elements)', all(
    x.sign() == qsign(2 * x.c[0] + x.c[1], x.c[1], 5) == g2q(x).sign() for x in gl) and all(
    g2q(x * y) == g2q(x) * g2q(y) and (x.iszero() or g2q(x.inv()) == g2q(x).inv()) for x, y in zip(gl, gl[1:] + gl[:1])))
zi = [(rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6)) for _ in range(N)] + [((-1) ** k * F_[k + 1], (-1) ** (k + 1) * F_[k]) for k in range(1, 70)]
check(f'D3 zphi = NF over GOLDEN: zadd, zsub, zmul, zneg, zconj, zsign, znorm on {len(zi)} integer pairs (Fibonacci units included); ints stay ints',
      all((lambda x, y, X, Y: Z.zadd(x, y) == (X + Y).c and Z.zsub(x, y) == (X - Y).c and Z.zmul(x, y) == (X * Y).c and Z.zneg(x) == (-X).c
           and Z.zsign(x) == X.sign() and Z.znorm(x) == X.norm() and Z.zconj(x) == (x[0] + x[1], -x[1])
           and all(type(t) is int for t in Z.zmul(x, y) + Z.zadd(x, y)))(x, y, NF(list(x), GOLDEN), NF(list(y), GOLDEN))
          for x, y in zip(zi, zi[1:] + zi[:1])))
q2 = pure_field(2, 2)
check('D4 NF over x^2 - 2 (power basis) = Quad(a, b, 2): sign, product, inverse on 1000 random elements', all(
    (lambda a, b, c, d: (lambda X, Y, A, B: X.sign() == A.sign() and (X * Y).c == ((A * B).a, (A * B).b) and (X.iszero() or (X.inv().c == (A.inv().a, A.inv().b))))(
        NF([a, b], q2), NF([c, d], q2), Quad(a, b, 2), Quad(c, d, 2)))(rfr(10 ** 6), rfr(10 ** 6), rfr(), rfr()) for _ in range(1000)))
check('D5 Quad.sqrt: sqrt(x^2) = |x| on 2000 random x in Q(sqrt d), d = 2, 3, 5, 6; sqrt(3/2 + sqrt5/2) = phi; phi, sqrt2, 2 + sqrt5 are not squares',
      all((lambda x: (x * x).sqrt() == abs(x))(Quad(rfr(), rfr() if rng.random() > 0.2 else 0, rng.choice((2, 3, 5, 6)))) for _ in range(2000))
      and PHI.sqrt() is None and R2.sqrt() is None and Quad(2, 1, 5).sqrt() is None and Quad(Fr(3, 2), Fr(1, 2), 5).sqrt() == PHI)

# ------------------------------------------------------------------------------------------------ E. guards
check('E1 mixed fields refused: NF of two fields, MQ with Q(sqrt3) (ValueError)', _try(lambda: NF([1, 1], CUB2) + NF([1, 1], CUB3), ValueError)
      and _try(lambda: MQ(1, 1) + Quad(0, 1, 3), ValueError))
check('E2 floats refused in arithmetic (TypeError); as a coefficient only a small dyadic float (0.5, -3.0) is taken, 0.1 is refused',
      _try(lambda: NF([1, 1], CUB2) + 0.5, TypeError) and _try(lambda: MQ(1) * 0.5, TypeError) and _try(lambda: NF([0.1], CUB2), TypeError)
      and _try(lambda: MQ(0.1), TypeError) and NF([0.5, -3.0], CUB2) == NF([Fr(1, 2), -3], CUB2) and MQ(1.0, 0.25) == MQ(1, Fr(1, 4)))
check('E3 division by zero raises ZeroDivisionError', _try(lambda: NF([1], CUB2) / NF([0], CUB2), ZeroDivisionError) and _try(lambda: MQ(1) / MQ(0), ZeroDivisionError))
RED = NumberField([1, -3, -2, 6], 1, 2, 'u')                       # (x^2 - 2)(x - 3), root sqrt2 in (1, 2): not irreducible
xz = NF([-2, 0, 1], RED)
check('E4 reducible polynomial (x^2 - 2)(x - 3) on (1, 2): x^2 - 2 has sign 0 and equals 0; x - 3 < 0; dividing by x^2 - 2 raises',
      xz.sign() == 0 and xz == 0 and NF([-3, 1], RED).sign() == -1 and _try(lambda: NF([1], RED) / xz, ZeroDivisionError))
check('E5 an interval holding two roots is refused (Sturm count), as is one without a sign change', _try(lambda: NumberField([1, 0, -2], -2, 2), ValueError)
      and _try(lambda: NumberField([1, 0, -2], 2, 3), ValueError) and sturm_count([-2, 0, 1], -2, 2) == 2)
check('E6 a square or cube is refused as a radical field; Q(sqrt p, sqrt q) needs p, q, pq non-squares', _try(lambda: pure_field(8, 3), ValueError)
      and _try(lambda: type('X', (MQ,), {'RADS': (2, 8), '__slots__': ()})(1), ValueError))

nf = sum(1 for _, ok in results if not ok)
print(f'checks: {len(results)}, failed: {nf}')
print('FINAL ok: field tests all pass' if nf == 0 else f'FINAL FAIL: {nf} field checks failed')
