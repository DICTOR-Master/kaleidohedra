"""Step 1b: the corner charts.  F~ = 0 has exactly two zeros on the boundary of the closed box (b1_polys.py; face analysis in the README):
the corner points (u, tau, rho) = (0, 0, 1) and (1, 1, 2).  Every function vanishes there, so no box touching them can be closed by a sign.
They are resolved by blow-up charts (weighted at (0, 0, 1), where D~ ~ tau^2 + u^8 and H~ ~ -2 tau^3 - u^12 on G~ = 0; homogeneous at
(1, 1, 2)).  Each chart is a polynomial map from a parameter box (all parameters >= 0) to (u, tau, rho):
    C1: (s, th, rho) -> (s, s^4 th, rho),        s in [0, 1/4], th in [0, 1]     covers  u <= 1/4, tau <= u^4
    C2: (s, et, rho) -> (s et, s^4, rho),        s in [0, 1/2], et in [0, 1]     covers  tau <= 1/16, tau >= u^4
    A:  (x, th, rho) -> (1 - x, 1 - x th, rho),  x in [0, 1/8], th in [0, 1]     covers  1 - u <= 1/8, 1 - tau <= 1 - u
    B:  (y, et, rho) -> (1 - y et, 1 - y, rho),  y in [0, 1/8], et in [0, 1]     covers  1 - tau <= 1/8, 1 - u <= 1 - tau
so the main chart only needs the box minus the holes [0, 1/4] x [0, 1/16] x [0, 6] and [7/8, 1] x [7/8, 1] x [0, 6].
Every pulled-back polynomial is divided by the largest power of each parameter (positive inside the chart) and by its other factors with
positive coefficients; tests keep their sign bookkeeping as in b1_polys.py.  Writes data/polys-<chart>.json.  FINAL ok iff every chart
was written and, at the chart's exceptional face (first parameter = 0), F~ does not vanish identically."""
import json, os, sys, time
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(ROOT, *p)
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
TAG = sys.argv[1] if len(sys.argv) > 1 else 'utr'
main = json.load(open(D_('data', f'polys-{TAG}.json')))
Rm = PolynomialRing(QQ, 'u,tau,rho'); um, tm, rm = Rm.gens()
def dec(p): return sum(QQ(c) * um**e[0] * tm**e[1] * rm**e[2] for e, c in p)
Fm = {k: dec(p) for k, p in main['F'].items()}
Tm = {k: (dec(v['N']), dec(v['D'])) for k, v in main['tests'].items()}
Rc = PolynomialRing(QQ, 'p,q,r'); p, q, r = Rc.gens()
# chart maps (u, tau, rho) = map(p, q, r), parameters >= 0; see the README section "Corner charts" for the covering argument
Zt, Zr = 4, 4                                         # corner-0 tower scales (zeta in [-4, 4], x in [-4, 4])
CH = {
  # corner (1, 1, 2): homogeneous blow-up
  'A': ((1 - p, 1 - p * q, r), [[0, '1/8'], [0, 1], [0, 6]]),
  'B': ((1 - p * q, 1 - p, r), [[0, '1/8'], [0, 1], [0, 6]]),
  # corner (0, 0, 1), level 1: weights (u, tau) = (1, 4)
  'C1': ((p, p**4 * q, r), [[0, '1/4'], [0, 2], [0, 6]]),
  'C2': ((p * q, p**4, r), [[0, '1/2'], [0, '27/32'], [0, 6]]),
  # level 2 around the C1 point (s, th, rho) = (0, 1, 1) along the curve th = 1, rho = 1 + s: weights (s, th - 1, rho - 1 - s) = (1, 4, 2)
  'W': ((p, p**4 * (1 + p**4 * (q - Zt)), 1 + p + p**2 * (r - Zr)), [[0, '1/16'], [0, 2 * Zt], [0, 2 * Zr]]),
  'Wt+': ((p * q, (p * q)**4 * (1 + Zt * p**4), 1 + p * q + Zr * p**2 * (r - 1)), [[0, '3/5'], [0, 1], [0, 2]]),
  'Wt-': ((p * q, (p * q)**4 * (1 - Zt * p**4), 1 + p * q + Zr * p**2 * (r - 1)), [[0, '3/5'], [0, 1], [0, 2]]),
  'Wr+': ((p * q, (p * q)**4 * (1 + Zt * p**4 * (r - 1)), 1 + p * q + Zr * p**2), [[0, '3/8'], [0, 1], [0, 2]]),
  'Wr-': ((p * q, (p * q)**4 * (1 + Zt * p**4 * (r - 1)), 1 + p * q - Zr * p**2), [[0, '3/8'], [0, 1], [0, 2]]),
}
ONLY = sys.argv[2].split(',') if len(sys.argv) > 2 else list(CH)
CH = {k: v for k, v in CH.items() if k in ONLY}
def is_pos(g): return g in (p, q, r) or (g.degree() > 0 and all(c > 0 for c in g.coefficients()))
def is_neg(g): return (-g) in (p, q, r) or (g.degree() > 0 and all(c < 0 for c in g.coefficients()))
def integ(f):
    den = ZZ(1)
    for c in f.coefficients(): den = den.lcm(QQ(c).denominator())
    f = f * den; g = ZZ(0)
    for c in f.coefficients(): g = g.gcd(ZZ(c))
    return f / g
def strip_eq(f):
    fl = f.factor(); out = Rc(1); dropped = []
    for g, m in fl:
        if is_pos(g) or is_neg(g): dropped.append((str(g), m))
        else: out *= g**m
    return integ(out), dropped
STRICT = True; EVEN = []
def strip_test(f):
    fl = f.factor(); sign = 1 if fl.unit() > 0 else -1; out = Rc(1)
    for g, m in fl:
        if is_pos(g): continue
        if is_neg(g): sign *= (-1)**m; continue
        if m % 2 == 0:                               # even power: >= 0; dropped only for strict tests (it cannot make q > 0 hold
            if STRICT: continue                      # where it vanishes); kept for the closed-disc tests, where q = 0 is allowed
            EVEN.append(str(g)[:60]); out *= g**2; continue
        out *= g
    return integ(sign * out) if out.degree() > 0 or True else out
def enc(f): return [[list(map(int, e)), str(ZZ(c))] for e, c in Rc(f).dict().items()]
ok = True
for nm, (mp, box) in CH.items():
    print(f'PROGRESS {list(CH).index(nm) / len(CH):.2f} chart {nm}', flush=True)
    F = {}
    for k, f in Fm.items():
        g = Rc(f(*mp)); s, dr = strip_eq(g); F[k] = s
        at0 = Rc(s.subs({p: 0}))
        say(f'{nm} {k}: {len(s.monomials())} terms, degrees ({s.degree(p)}, {s.degree(q)}, {s.degree(r)}), dropped {dr}; at p = 0: '
            f'{"ZERO" if at0 == 0 else (str(at0.factor()) if len(str(at0)) < 160 else str(len(at0.monomials())) + " terms")}')
    if all(Rc(F[k].subs({p: 0})) == 0 for k in F): ok = False; say(nm, ': F vanishes identically on p = 0')
    T = {}
    for k, (N, Dd) in Tm.items():
        STRICT = 'in disc' not in k; EVEN.clear()
        T[k] = (strip_test(Rc(N(*mp))), strip_test(Rc(Dd(*mp))))
        if EVEN: say(f'{nm} test {k}: even-power factors kept (closed condition): {EVEN}')
    json.dump({'vars': ['p', 'q', 'r'], 'chart': nm, 'map': [str(x) for x in mp], 'box': box,
               'F': {k: enc(F[k]) for k in F}, 'tests': {k: {'N': enc(a), 'D': enc(b)} for k, (a, b) in T.items()}},
              open(D_('data', f'polys-{TAG}-{nm}.json'), 'w'))
    say(f'{nm}: wrote data/polys-{TAG}-{nm}.json; test sizes', sum(len(a.monomials()) + len(b.monomials()) for a, b in T.values()))
print('PROGRESS 1.0 done')
print('FINAL ok' if ok else 'FINAL FAIL')
