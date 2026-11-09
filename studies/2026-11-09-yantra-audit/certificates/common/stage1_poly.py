"""Stage 1 of the certificate for Theorem 9 (case D, DICTO Yantra) or Theorem 10 (case K, Kulaichev's yantra).
usage: python -u stage1_poly.py D|K
  (1) descriptive claims about the polynomial f (degree, evenness, terms, largest coefficient, real roots);
  (2) irreducibility of f(u) and of g(y) = f(sqrt y) over Q, by factorisation degree patterns modulo primes (a pattern set
      certifies irreducibility when the only degrees every pattern can add up to are 0 and deg); PARI factormod gives the
      patterns, a second, independent check is Singular/FLINT via sage (is_irreducible) and PARI polisirreducible;
  (3) case D: g factors over Q(sqrt5) into two factors of degree 40 (PARI nffactor);
  (4) a rational isolating interval [a, b] of width 1e-40 containing exactly one real root of f, the one at the stored
      numerical u: PARI polsturm (exact) and an independent Descartes count on the Moebius-transformed polynomial in pure
      Python integers; then exact bisection by signs of f at rational points down to width 1e-1000 (the root stays the
      unique one of [a, b]).
Writes stage1-<case>.json (intervals as exact decimal strings) and prints FINAL ok / FINAL FAIL."""
import sys, json, time
from fractions import Fraction as Fr
import cypari2
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
pari = cypari2.Pari(); pari.allocatemem(12 * 10**9); pari.set_real_precision(1100)
case = sys.argv[1]
path = {'D': 'dicto-yantra-exact-u.txt', 'K': 'kulaichev-minpoly-u.txt'}[case]
u_num = {'D': '0.679318588706774657388650310391',      # golden_family.json GF1 (30 digits)
         'K': '0.750438516022214024406084657051234510340891003639790315415314'}[case]   # kulaichev-numeric-data.txt (60)
f = pari(open(path).read().strip().replace('x', 'u'))
n = int(pari.poldegree(f, 'u'))
c = [int(pari.polcoef(f, k, 'u')) for k in range(n + 1)]          # c[k] = coefficient of u^k
ok = True
fmt = lambda spec, x: str(pari(f'Strprintf("{spec}", {x})')).strip('"')
def check(cond, msg):
    global ok
    say(('ok   ' if cond else 'FAIL ') + msg); ok = ok and bool(cond)
# (1) descriptive claims
terms = sum(1 for x in c if x); big = max(range(n + 1), key=lambda k: abs(c[k]))
check(all(c[k] == 0 for k in range(1, n + 1, 2)), f'f is even in u (degree {n})')
fac = lambda z: f'{z} = {pari.factor(z)}' if len(str(abs(z))) < 40 else f'({len(str(abs(z)))} digits, not factored)'
nreal = len(pari.polrootsreal(f, precision=600))   # PARI exact real-root isolation (polsturm on all of R was too slow for f160)
say(f'degree {n}, terms {terms}, largest coefficient {len(str(abs(c[big])))} digits at u^{big}, real roots {nreal}, '
    f'leading {fac(c[n])}, constant {fac(c[0])}'.replace('\n', ' '))
expect = {'D': (160, 81, 226, 80, 60), 'K': (348, 175, 33, 210, 34)}[case]
check((n, terms, len(str(abs(c[big]))), big, nreal) == expect, f'matches the paper: (degree, terms, digits, at, real roots) = {expect}')
check(all(x % 1 == 0 for x in c) and pari.content(f) == 1, 'integer coefficients, content 1 (primitive)')
g = pari.substpol(f, pari('u^2'), pari('y'))
m = n // 2
# (2) irreducibility by degree patterns modulo primes
def pattern_cert(P, deg, var, maxp=20000, need=None):
    lc = int(pari.pollead(P, var)); dP = pari.deriv(P, var)
    full = (1 << (deg + 1)) - 1; inter = full; used = []
    p = 2
    while p < maxp:
        p = int(pari.nextprime(p + 1))
        if lc % p == 0: continue
        Pm = P * pari.Mod(1, p)
        if pari.poldegree(pari.gcd(Pm, dP * pari.Mod(1, p)), var) > 0: continue   # not squarefree mod p
        degs = sorted(int(pari.poldegree(F, var)) for F in pari.factormod(P, p)[0])
        s = 1
        for d in degs: s |= s << d
        s &= full
        if inter & s != inter:
            used.append((p, degs)); inter &= s
        if inter == (1 | (1 << deg)): return True, used
    return False, used
for name, P, deg, var in (('f(u)', f, n, 'u'), ('g(y) = f(sqrt y)', g, m, 'y')):
    t = time.time(); good, used = pattern_cert(P, deg, var)
    check(good, f'{name} irreducible over Q by degree patterns mod {[p for p, d in used]} ({time.time() - t:.1f} s)')
    for p, degs in used:
        from collections import Counter
        say(f'      mod {p}: degrees ' + ' + '.join(f'{d}^{k}' if k > 1 else f'{d}' for d, k in sorted(Counter(degs).items())))
check(bool(pari.polisirreducible(f)) and bool(pari.polisirreducible(g)), 'PARI polisirreducible: f and g irreducible')
from sage.all__sagemath_singular import PolynomialRing, ZZ
Rz = PolynomialRing(ZZ, 'x')
check(Rz(c).is_irreducible() and Rz(c[0::2]).is_irreducible(), 'sage (FLINT/NTL factoring): f and g irreducible')
# (3) case D: g over Q(sqrt5)
if case == 'D':
    t = time.time()
    w = pari.varlower('w')
    nf = pari.nfinit(w**2 - 5)
    F = pari.nffactor(nf, g)
    degs = [int(pari.poldegree(F[0][i], 'y')) for i in range(len(F[0]))]
    check(sorted(degs) == [40, 40], f'g factors over Q(sqrt5) as degrees {degs} ({time.time() - t:.1f} s)')
    open('stage1-D-g-over-Qsqrt5.txt', 'w').write(str(F[0][0]) + '\n' + str(F[0][1]) + '\n')
# (4) isolating interval
roots = pari.polrootsreal(f, precision=3700)   # bits (about 1110 digits)
U = pari(u_num)
dist = sorted((abs(r - U), i) for i, r in enumerate(roots))
r0 = roots[dist[0][1]]
say(f'nearest real root differs from the stored u by {fmt('%.3e', dist[0][0])}; next real root is '
    f'{fmt('%.3e', dist[1][0])} away')
k = 40
A = int(pari.floor(r0 * pari(10)**k)); D = 10**k; B = A + 1
a, b = Fr(A, D), Fr(B, D)
check(abs(Fr(u_num) - Fr(fmt('%.200f', r0))) <= Fr(1, 10**(len(u_num) - 2)), f'the interval agrees with the stored numerical u to all its {len(u_num) - 2} digits (rounding)')
cnt = int(pari.polsturm(f, [pari(f'{A}/{D}'), pari(f'{B}/{D}')]))
check(cnt == 1, f'PARI polsturm: exactly one real root of f in [{A}/10^{k}, {B}/10^{k}]')
def descartes(c, A, B, D):
    """sign variations of (D(1+t))^n f((A + B t)/(D (1 + t))); 1 variation => exactly one root in (A/D, B/D)."""
    n = len(c) - 1
    Mp = [[1]]                                   # powers of M = D + D t
    for _ in range(n):
        q = Mp[-1] + [0]
        Mp.append([D * (q[i] + (q[i - 1] if i else 0)) for i in range(len(q))])
    H = [c[n]]
    for kk in range(n - 1, -1, -1):
        NH = [0] * (len(H) + 1)                  # H * (A + B t)
        for i, h in enumerate(H): NH[i] += A * h; NH[i + 1] += B * h
        for i, mcoef in enumerate(Mp[n - kk]): NH[i] += c[kk] * mcoef
        H = NH
    signs = [1 if h > 0 else -1 for h in H if h != 0]
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])
t = time.time(); var = descartes(c, A, B, D)
check(var == 1, f'independent Descartes count (pure Python integers): {var} sign variation(s) on the interval ({time.time() - t:.1f} s)')
sgn = lambda x: (x > 0) - (x < 0)
def fval(x):   # exact f(x) for Fraction x, sign only needed
    num, den = x.numerator, x.denominator; tot = 0
    for kk in range(n, -1, -1): tot = tot * num + c[kk] * den**(n - kk)
    return tot
fa, fb = sgn(fval(a)), sgn(fval(b))
check(fa * fb < 0, 'f changes sign on the interval')
def sgn_at(x):   # exact sign of f at a rational point, PARI exact arithmetic
    return int(pari.sign(pari.subst(f, 'u', pari(f'{x.numerator}/{x.denominator}'))))
L = int(pari.floor(r0 * pari(10)**1000))
lo, hi = Fr(L - 1, 10**1000), Fr(L + 2, 10**1000)
check(a <= lo and hi <= b and sgn_at(lo) == fa and sgn_at(hi) == -fa and sgn_at(a) == fa,
      'refined: f changes sign on a subinterval of width 3e-1000 inside [a, b] (exact signs), so u0 lies there')
y_lo, y_hi = lo * lo, hi * hi
check(int(pari.polsturm(g, [pari(f'{a.numerator**2}/{a.denominator**2}'), pari(f'{b.numerator**2}/{b.denominator**2}')])) == 1,
      'g has exactly one real root in [a^2, b^2] (so y0 = u0^2 is isolated too)')
json.dump({'case': case, 'degree': n, 'interval40': [str(a), str(b)], 'interval1000': [str(lo), str(hi)],
           'u_1000_digits': fmt('%.1000f', r0)}, open(f'stage1-{case}.json', 'w'))
say(f'u0 = {fmt('%.60f', r0)}...')
print('FINAL ok' if ok else 'FINAL FAIL: a stage-1 check failed')
