#!/usr/bin/env python3
"""Kernel tests (shape-kernel pilot, 2026-11-18).
  A. checks ported from the copies (asserts in their modules and studies)
  B. field axioms and order axioms on random exact elements of Q, Q(sqrt2), Q(sqrt3), Q(sqrt5), Q(sqrt6)
  C. sign agreement with 60-digit decimals (Python decimal) and 80-digit mpmath, including hard near-zero cases
     (Lucas/Fibonacci and Pell pairs, where a and b sqrt d agree to many digits and floats get the sign wrong)
  D. guards: mixed fields refused, floats refused in arithmetic, square d normalised, division by zero raised
Prints one line per check group and FINAL ok only if every check passes.  usage: test_kernel.py [n_random]"""
import os, sys, random, math, itertools
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kernel import Quad, PHI, IPHI, R2, R3, R5, R6, ZERO, ONE, fmt, parse, floor, cos2_exact, rational_pi, STYLES
from kernel import pairs as P, vec as V

N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
rng = random.Random(20261118)
FIELDS = [2, 3, 5, 6]
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok)))
    print(('ok   ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail and not ok else ''))


def rfr(big=False):
    m = 10 ** 12 if big else 50
    return Fr(rng.randint(-m, m), rng.randint(1, m))


def rel(d, big=False):
    k = rng.random()
    if k < 0.1: return Quad(rfr(big), 0, d)
    if k < 0.2: return Quad(0, rfr(big), d)
    return Quad(rfr(big), rfr(big), d)


# ------------------------------------------------------------------------------------------------ A. ported checks
check('A1 phi^2 = phi + 1 (silent_render.py, vacuus_exact.py)', PHI * PHI == PHI + 1)
check('A2 1/phi = phi - 1 and phi * (phi - 1) = 1', ONE / PHI == PHI - 1 and PHI * IPHI == ONE)
def cyc(p): return [p, (p[2], p[0], p[1]), (p[1], p[2], p[0])]
def signs(p): return list({tuple(Quad(s[i]) * p[i] for i in range(3)) for s in itertools.product((1, -1), repeat=3)})
AX5 = sorted({x for p in cyc((ZERO, ONE, PHI)) for x in signs(p)}, key=lambda v: tuple(float(x) for x in v))
AX3 = sorted({x for p in cyc((ZERO, PHI, IPHI)) + [(ONE, ONE, ONE)] for x in signs(p)}, key=lambda v: tuple(float(x) for x in v))
check('A3 icosahedral frame: 12 five-fold, 20 three-fold axes (q5.py, turn-theorem)', len(AX5) == 12 and len(AX3) == 20)
check('A4 each three-fold axis is nearest to exactly three icosahedron corners, all at b.a = phi^2 (q5.py assert, now exact)',
      all(sorted((V.dot3(a, b) for a in AX5))[-3:] == [PHI * PHI] * 3 and sorted(V.dot3(a, b) for a in AX5)[-4] < PHI * PHI for b in AX3))
H = Quad(Fr(1, 2)); ID = set()
for p in [(PHI, ZERO, ZERO)]:
    for c in cyc(p): ID |= set(signs(c))
for p in [(H, PHI * H, PHI * PHI * H)]:
    for c in cyc(p): ID |= set(signs(c))
check('A5 icosidodecahedron: 30 corners, all at |v|^2 = phi^2 (d40_hex.py, exact_cycle.py)', len(ID) == 30 and all(V.dot3(v, v) == PHI * PHI for v in ID))
def _try(f, e):
    try: f()
    except e: return True
    except Exception: return False
    return False
check('A6 mixed fields refused (exactlib.py; exact-vs-dissection exact.py)', _try(lambda: R2 + R5, ValueError) and _try(lambda: R3 * R6, ValueError)
      and (R2 + 1).d == 2 and (Quad(3) * R5).d == 5)
check('A7 a square field parameter is rational (yantra_regions45 assert "Delta a square")', Quad(1, 2, 4) == Quad(5) and Quad(1, 1, Fr(9, 4)) == Quad(Fr(5, 2)))
ok = True
for n in (1, 2, 3, 4, 5, 6, 8, 10, 12):
    for k in range(n):
        if math.gcd(k, n) != 1 and not (k == 0 and n == 1): continue
        a, b, d = cos2_exact(Fr(k, n)); ok &= abs(float(Fr(a)) + float(Fr(b)) * math.sqrt(d) - math.cos(2 * math.pi * k / n)) < 1e-12
check('A8 cos2_exact table = cos(2 pi k/n) for phi(n) <= 4 (qf.py of the Vacuus studies)', ok)
# collect.log of 2026-11-02-dicto-vacuus: octahedron apex 90 deg -> 1/2, cuboctahedron 60 -> 1/3, icosidodecahedron 36 -> 1/5
c2 = lambda deg, val: rational_pi(val, math.radians(deg))
check('A9 rational_pi: 90 deg -> 1/2, 60 -> 1/3, 36 -> 1/5, 45 -> 1/4, 72 -> 2/5 (collect.log of the Vacuus census)',
      c2(90, Quad(-1)) == '1/2' and c2(60, Quad(Fr(-1, 2))) == '1/3' and c2(36, Quad(Fr(-1, 4), Fr(1, 4), 5)) == '1/5'
      and c2(45, Quad(0, 0, 2)) == '1/4' and c2(72, Quad(Fr(-1, 4), Fr(-1, 4), 5)) == '2/5' and c2(35.2644, Quad(Fr(1, 3))) is None)
check('A10 pairs: q/qs_ round trip, PHI^2 = PHI + 1, qinv(PHI) = PHI - 1 (q5.py of the octet studies)',
      P.q(P.qs_(P.PHI)) == P.PHI and P.qm(P.PHI, P.PHI) == P.qa(P.PHI, P.ONE) and P.qinv(P.PHI) == P.qs(P.PHI, P.ONE))
check('A11 parse: pair text, parsable text and plain rationals', parse('1/2|1/2') == PHI and parse(fmt(Quad(Fr(-3, 7), Fr(5, 2), 6), 'parsable')) == Quad(Fr(-3, 7), Fr(5, 2), 6)
      and parse('-3/4') == Quad(Fr(-3, 4)))

# ------------------------------------------------------------------------------------------------ B. axioms
import collections
fails = collections.Counter()
for t in range(N):
    d = rng.choice(FIELDS); x, y, z = rel(d), rel(d), rel(d); r = Quad(rfr())
    if not ((x + y) + z == x + (y + z) and x + y == y + x): fails['add assoc/comm'] += 1
    if not ((x * y) * z == x * (y * z) and x * y == y * x): fails['mul assoc/comm'] += 1
    if not (x * (y + z) == x * y + x * z): fails['distributive'] += 1
    if not (x + 0 == x and x * 1 == x and x + (-x) == 0 and x - y == x + (-y)): fails['identities'] += 1
    if x != 0 and not (x * x.inv() == 1 and (y / x) * x == y): fails['inverse'] += 1
    if not ((x * y).conj() == x.conj() * y.conj() and (x + y).conj() == x.conj() + y.conj()): fails['conj automorphism'] += 1
    if not ((x * y).norm() == x.norm() * y.norm() and x.norm() == (x * x.conj()).a and (x * x.conj()).b == 0): fails['norm multiplicative'] += 1
    if not ((x * y).sign() == x.sign() * y.sign() and (-x).sign() == -x.sign()): fails['sign multiplicative'] += 1
    if not (((x < y) + (x == y) + (x > y)) == 1 and ((x < y) == (y > x)) and ((x <= y) == (not x > y))): fails['trichotomy'] += 1
    if x < y and not (x + z < y + z): fails['order + compatible'] += 1
    if x < y and r > 0 and not (x * r < y * r): fails['order * positive'] += 1
    if x < y and y < z and not x < z: fails['order transitive'] += 1
    k = rng.randint(-4, 6)
    if x != 0 and not (x ** k == (x.inv() ** (-k) if k < 0 else math.prod([x] * k, start=Quad(1, 0, d)))): fails['pow'] += 1
    fx = x.floor()
    if not (Quad(fx) <= x < Quad(fx + 1) and x.ceil() == -((-x).floor())): fails['floor/ceil'] += 1
    if hash(x) != hash(Quad(x.a, x.b, d)) or (x.b == 0 and hash(x) != hash(x.a)): fails['hash consistent with =='] += 1
    if parse(fmt(x, 'parsable')) != x: fails['parsable round trip'] += 1
    if abs(x) != (x if x.sign() >= 0 else -x) or abs(x).sign() < 0: fails['abs'] += 1
for name in ['add assoc/comm', 'mul assoc/comm', 'distributive', 'identities', 'inverse', 'conj automorphism', 'norm multiplicative',
             'sign multiplicative', 'trichotomy', 'order + compatible', 'order * positive', 'order transitive', 'pow', 'floor/ceil',
             'hash consistent with ==', 'parsable round trip', 'abs']:
    check(f'B {name} ({N} random triples over d = 2, 3, 5, 6)', fails[name] == 0, f'{fails[name]} failures')

# ------------------------------------------------------------------------------------------------ C. sign vs 60 digits
getcontext().prec = 60
def dec_value(x):
    return Decimal(x.a.numerator) / Decimal(x.a.denominator) + Decimal(x.b.numerator) / Decimal(x.b.denominator) * Decimal(x.d).sqrt()
def dsign(v): return (v > 0) - (v < 0)
hard = []
F_, L_ = [0, 1], [2, 1]
for n in range(2, 130): F_.append(F_[-1] + F_[-2]); L_.append(L_[-1] + L_[-2])
for n in range(1, 120): hard += [Quad(L_[n], -F_[n], 5), Quad(-L_[n], F_[n], 5)]          # L_n - F_n sqrt5 = (-1/phi)^n * 2 ... tiny
pa, pb = 1, 0
for n in range(1, 37):                                                                     # Pell: (3 + 2 sqrt2)^n = p + q sqrt2
    pa, pb = 3 * pa + 4 * pb, 2 * pa + 3 * pb; hard += [Quad(pa, -pb, 2), Quad(-pa, pb, 2)]
for d, (u, w), nmax in ((3, (2, 1), 46), (6, (5, 2), 28)):   # magnitudes below 1e29, so 60 digits decide
    pa, pb = 1, 0
    for n in range(1, nmax): pa, pb = u * pa + d * w * pb, w * pa + u * pb; hard += [Quad(pa, -pb, d), Quad(-pa, pb, d)]
rand = [rel(rng.choice(FIELDS), big=True) for _ in range(N)]
mism = [x for x in rand + hard if dec_value(x) != 0 and dsign(dec_value(x)) != x.sign()]
undecided = [x for x in rand + hard if dec_value(x) == 0 and not x.iszero()]
check(f'C1 exact sign = sign of the 60-digit decimal value ({len(rand)} random with 12-digit parts, {len(hard)} near-zero units)',
      not mism, f'{len(mism)} mismatches, e.g. {mism[:1]}')
try:
    import mpmath
    mpmath.mp.dps = 80
    mm = [x for x in rand + hard if mpmath.sign(mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(x.d)) != x.sign()]
    check('C2 exact sign = sign at 80 digits (mpmath), same elements', not mm, f'{len(mm)} mismatches')
except ImportError:
    check('C2 mpmath available', False, 'mpmath missing')
float_wrong = sum(1 for x in hard if (float(x) > 0) - (float(x) < 0) != x.sign())
print(f'     (for comparison: float64 gets the sign wrong on {float_wrong} of the {len(hard)} near-zero units; 60 digits leaves {len(undecided)} undecided)')
check('C3 exact decimal digits(50) agree with the 60-digit Decimal value to 1e-49', all(
    abs(Decimal(x.digits(50)) - dec_value(x)) <= Decimal(10) ** -49 for x in rand[:500]))
check('C4 pair sgn = kernel sign = copies\' rule on the near-zero units (pairs.sgn)', all(P.sgn((x.a, x.b)) == x.sign() for x in hard if x.d == 5))

# ------------------------------------------------------------------------------------------------ D. guards
check('D1 floats refused in arithmetic and comparison (exact only)', _try(lambda: PHI + 0.5, TypeError) and _try(lambda: PHI < 1.5, TypeError)
      and (PHI == 1.618) is False)
check('D2 division by zero raises ZeroDivisionError', _try(lambda: PHI / ZERO, ZeroDivisionError) and _try(lambda: ZERO.inv(), ZeroDivisionError))
check('D3 rationals mix with every field; result keeps the field', (Fr(1, 3) + R6).d == 6 and (R3 * Fr(2)).b == 2 and (2 - R2) < 1)
check('D4 Quad(Quad) copies; class default field D = 5', Quad(PHI) == PHI and Quad(1, 1).d == 5)
check('D5 styles: every repr style of the copies gives text for every element', all(isinstance(STYLES[s](x), str) for s in STYLES for x in (PHI, Quad(3), R5, -R2, Quad(Fr(-1, 2), Fr(-3, 2), 6))))

nf = sum(1 for _, ok in results if not ok)
print(f'checks: {len(results)}, failed: {nf}')
print('FINAL ok: kernel tests all pass' if nf == 0 else f'FINAL FAIL: {nf} kernel checks failed')
