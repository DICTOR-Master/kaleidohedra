"""Step 1 of the box certificate: the polynomial system and the admissibility tests in the box coordinates (u, tau, rho).

Input: the system G, H1, D of studies/2026-11-15-yantra-uniqueness (scripts/s1_system.py, after the divisor lemma; data/system-K.txt),
in the unknowns u = w7/b7, t = b1/w1, S = b9.  Box coordinates:
    t = u*tau,   S = R + rho*(1 - u)*(1 - R),   R = 1/(1 + u^2),
so that tau = t/u = (b1 < b3 side) and rho measures S - R in units of (1 - R)(1 - u).  Admissibility gives (justified in the README):
    0 < u < 1   (w7 > 0 and b3 < b7),   0 < tau < 1   (w1 > 0 and b1 < b3),   0 < rho   (b7 < b9),
    rho < 6     (b9 < 1 or the corner of t9 in the disc: see the test 'S<1' and 'disc9'; the box is closed off by these tests).
Each of G, H1, D is pulled back, multiplied by (1 + u^2)^deg_S, and divided by its factors that are positive on the open box
(u, 1 - u, 1 + u^2): F~ = (G~, H~, D~), integer coefficients.  Every admissible yantra has F~ = 0 at its (u, tau, rho).
Admissibility tests (#103 Theorem 1, the list of s3_backsolve.py, plus b9 < 1): each quantity q that must be > 0 (or >= 0 for a corner
in the closed disc) is written q = c * E * N/D with E a product of factors positive on the open box and of even powers; N, D are
kept.  A box on which N and D have certified opposite signs has q < 0 everywhere: it holds no admissible yantra.
Also written: the corner charts (see b1 README section) are built in b1_charts.py from this output.
Writes data/polys-utr.json and data/polys-utr.txt.  FINAL ok iff every pull-back divides exactly and the test list is complete."""
import json, os, sys, time
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(ROOT, *p)
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
SYS = sys.argv[1] if len(sys.argv) > 1 else D_('inputs', 'system-K.txt')
OUT = sys.argv[2] if len(sys.argv) > 2 else 'utr'
R3 = PolynomialRing(QQ, 'u,t,S'); u0, t0, S0 = R3.gens()
src = {}
for line in open(SYS):
    if ' = ' in line: k, e = line.split(' = ', 1); src[k.strip()] = R3(e.strip().replace('^', '**'))
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens(); Fr = Rn.fraction_field()
print('PROGRESS 0.1 pull-back')
Sv = Fr(1 + rho * (1 - u) * u**2) / (1 + u**2)
POSF = [u, 1 - u, 1 + u, tau, 1 - tau, rho, 1 + u**2]          # positive on the open box
def is_pos(g): return any(g == p for p in POSF) or (g.degree() > 0 and all(c > 0 for c in g.coefficients()))
def is_neg(g): return any(g == -p for p in POSF) or (g.degree() > 0 and all(c < 0 for c in g.coefficients()))
F = {}; ok = True
for k in ('G', 'H1', 'D'):
    f = src[k]; dS = f.degree(S0)
    g = Fr(f(u, u * tau, Sv)) * (1 + u**2)**dS
    if g.denominator().degree() != 0: ok = False; say('pull-back of', k, 'is not a polynomial'); continue
    g = Rn(g.numerator() / g.denominator())
    kept = Rn(1); dropped = []
    fl = g.factor()
    for h, m in fl:
        if is_pos(h) or is_neg(h): dropped.append((str(h), m))
        else: kept *= h**m
    kept = kept * (1 if fl.unit() > 0 else -1)
    den = ZZ(1)
    for c in kept.coefficients(): den = den.lcm(c.denominator())
    kept = kept * den
    F[k] = kept
    say(f'{k}~: degrees (u, tau, rho) = ({kept.degree(u)}, {kept.degree(tau)}, {kept.degree(rho)}), {len(kept.monomials())} terms, '
        f'max coefficient {max(abs(c) for c in kept.coefficients())}; dropped positive factors {dropped}')
print('PROGRESS 0.4 admissibility tests')
one = Fr(1); t = u * tau; S = Sv
v = u; P = v**2 / (1 + v**2); R = one / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
k3 = w3 / (1 - P); xZ = k3 * (1 - R)
c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: Fr(0)}
w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q), 8: xZ * (b8 - b1) / (R - b1), 9: w9}
tests = {}
for i in range(1, 9): tests[f'b{i} < b{i + 1}'] = b[i + 1] - b[i]
for i in range(1, 10): tests[f'w{i} > 0'] = w[i]
for i in range(1, 10): tests[f'apex t{i}'] = (a[i] - b[i]) if i <= 5 else (b[i] - a[i])
for i in (2, 4, 5, 6, 8, 9): tests[f'corner t{i} in disc'] = -(w[i]**2 + b[i]**2 - b[i])
tests['b9 < 1'] = 1 - S
tests['b3 < b6'] = Q - P                                # = xZ (P - b1)^2 / c138: the sign of the marma (1,3,8) coefficient
tests['b5 < 1/2'] = one / 2 - b5; tests['Q > 1/2'] = Q - one / 2
STRICT = True; EVEN = []
def strip(f):
    f = Rn(f); fl = f.factor(); sign = 1 if fl.unit() > 0 else -1; out = Rn(1)
    for g, m in fl:
        if is_pos(g): continue
        if is_neg(g): sign *= (-1)**m; continue
        if m % 2 == 0:                               # even power: >= 0; dropped only for strict tests (it cannot make q > 0 hold
            if STRICT: continue                      # where it vanishes); kept for the closed-disc tests, where q = 0 is allowed
            EVEN.append(str(g)[:60]); out *= g**2; continue
        out *= g
    return sign * out
T = {}
for k, q in tests.items():
    STRICT = 'in disc' not in k; EVEN.clear()
    N = strip(q.numerator()); Dd = strip(q.denominator())
    if EVEN: say(f'test {k}: even-power factors kept (closed condition): {EVEN}')
    # integer coefficients, positive content
    for X in ('N', 'D'):
        pass
    def integ(p):
        den = ZZ(1)
        for c in p.coefficients(): den = den.lcm(c.denominator())
        p = p * den; g = ZZ(0)
        for c in p.coefficients(): g = g.gcd(ZZ(c))
        return p / g
    N, Dd = integ(N), integ(Dd)
    T[k] = (N, Dd)
    say(f'test {k}: N {len(N.monomials())} terms deg {N.degree()}, D {len(Dd.monomials())} terms deg {Dd.degree()}')
def enc(p): return [[list(map(int, e)), str(ZZ(c))] for e, c in Rn(p).dict().items()]
out = {'vars': ['u', 'tau', 'rho'], 'box': [[0, 1], [0, 1], [0, 6]],
       'F': {k: enc(F[k]) for k in ('G', 'H1', 'D')},
       'tests': {k: {'N': enc(N), 'D': enc(Dd)} for k, (N, Dd) in T.items()}}
json.dump(out, open(D_('data', f'polys-{OUT}.json'), 'w'))
with open(D_('data', f'polys-{OUT}.txt'), 'w') as fh:
    for k in ('G', 'H1', 'D'): fh.write(f'{k}~ = {F[k]}\n')
    for k, (N, Dd) in T.items(): fh.write(f'[{k}] N = {N}\n[{k}] D = {Dd}\n')
say('wrote', D_('data', f'polys-{OUT}.json'))
ok = ok and len(F) == 3 and len(T) == 36
print('PROGRESS 1.0 done')
print('FINAL ok' if ok else 'FINAL FAIL')
