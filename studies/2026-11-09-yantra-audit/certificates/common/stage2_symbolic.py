"""Stage 2 (symbolic, generic): the model of model.py run with SYMBOLS, for each case.
usage: python -u stage2_symbolic.py D|K|G   (G: general u, v unscaled, the generic statement behind Theorem 1)
Scaled coordinates: every x-coordinate is divided by u (> 0). This is an affine map (x, d) -> (x/u, d): it keeps every line,
every meeting, every concurrency (each det3 of model.py is multiplied by 1/u^2) and every orientation sign. Circle conditions
w^2 + b^2 - b become y W^2 + b^2 - b with y = u^2 and W = w/u. Then every quantity is rational in y (and p = uv for case D):
  case K (Kulaichev, v = u):      P = y/(1+y),        R = 1/(1+y), W3 = 1/(1+y),       W7 = 1/(1+y)
  case D (DICTO Yantra, v = p/u): P = p^2/(y+p^2),    R = 1/(1+y), W3 = p/(y+p^2),     W7 = 1/(1+y)
(from P = v^2/(1+v^2), R = 1/(1+u^2), w3 = v/(1+v^2), w7 = u/(1+u^2)). The unknowns are Q, S and t = b1 (supplied to model.solve).
Proves, in Q(y, p, Q, S, t) with Singular via sage (second system: sympy):
  LEMMA: every condition of model.all_conditions (18 marmas, 6 corner touches, 7 apex-on-base, t3 and t7 inscribed) is either
  identically zero or equal to (closing numerator) x (rational function). So at any point where the closing equation holds
  and no divisor used by model.solve vanishes, all of them hold.
Writes stage2-<case>.json: the four polynomials to verify at the exact point (closing numerator Fc, (b) Eb, (c) Ec, (d) Ed,
as polynomials in y, p, Q, S, t), and every divisor used by model.solve and by the extra conditions (to be shown nonzero)."""
import sys, json, time
sys.path.insert(0, '.')
import model
from sage.all__sagemath_singular import QQ, PolynomialRing
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
case = sys.argv[1]
Rg = PolynomialRing(QQ, 'y,p,Q,S,t'); y, p, Q, S, t = Rg.gens(); Fd = Rg.fraction_field()
DIV = []
class T:
    """wrapper that logs every divisor"""
    def __init__(s, v): s.v = Fd(v)
    def _w(o): return o if isinstance(o, T) else T(o)
    def __add__(s, o): return T(s.v + T._w(o).v)
    __radd__ = __add__
    def __sub__(s, o): return T(s.v - T._w(o).v)
    def __rsub__(s, o): return T(T._w(o).v - s.v)
    def __mul__(s, o): return T(s.v * T._w(o).v)
    __rmul__ = __mul__
    def __truediv__(s, o):
        d = T._w(o).v; DIV.append(d); return T(s.v / d)
    def __rtruediv__(s, o): DIV.append(s.v); return T(T._w(o).v / s.v)
    def __neg__(s): return T(-s.v)
    def __pow__(s, k): return T(s.v ** k)
one = T(1)
if case == 'G':        # general great slopes, unscaled: here the symbol y stands for u and p for v
    P = T(p * p) / (one + p * p); R = one / (one + T(y) * y); W3 = T(p) / (one + p * p); W7 = T(y) / (one + T(y) * y)
elif case == 'K':
    P = T(y) / (one + y); R = one / (one + y); W3 = one / (one + y); W7 = one / (one + y)
else:
    P = T(p * p) / (T(y) + p * p); R = one / (one + y); W3 = T(p) / (T(y) + p * p); W7 = one / (one + y)
tri = model.solve(P, T(Q), R, T(S), W3, W7, sqrt=None, b1=T(t))
A, B, C = tri['quad']
closing = A * T(t) * T(t) + B * T(t) + C
b, w, a = tri['b'], tri['w'], tri['a']
m1 = w[1] / (b[6] - b[1])                                    # t1's leg slope (scaled); apex a1 = b6 = Q
half = Fd(1) / 2
Eb = T(y) * w[1] * w[1] + b[1] * b[1] - b[1]                  # (b) t1's corners on the circle
Ec = T(y) * w[9] * w[9] + b[9] * b[9] - b[9]                  # (c) t9's corners on the circle
Ed = T(y) * m1 * m1 * (T(Q) - half) ** 2 - (T(half) - b[5]) ** 2 * (one + T(y) * m1 * m1)   # (d) centre equidistant from leg and base
say(f'case {case}: model run symbolically, {len(DIV)} divisions logged')
Fc = closing.v.numerator()
fac = Fc.factor()
say('closing numerator factors (degree in y, p, Q, S, t):', [tuple(f.degree(x) for x in (y, p, Q, S, t)) + (m,) for f, m in fac])
# LEMMA
ok = True
names = []
for name, val in model.all_conditions(tri):
    if name.startswith('circle'):
        i = int(name[-1]); val = (one if case == 'G' else T(y)) * w[i] * w[i] + b[i] * b[i] - b[i]
    v = val.v if isinstance(val, T) else Fd(val)
    if v == 0: kind = 'identically 0'
    else:
        num = v.numerator()
        kind = 'closing x rational function' if Fc.divides(num) else 'NOT REDUCED'
    if kind == 'NOT REDUCED': ok = False
    names.append((name, kind))
for name, kind in names: say(f'   {name:28s} {kind}')
say('LEMMA (Singular/sage):', 'holds' if ok else 'FAILS')
# second system: sympy on the same lemma for the one condition that is not an identity (and spot identities)
import sympy as sp
ys, ps, Qs, Ss, ts = sp.symbols('y p Q S t')
conv = lambda e: sp.sympify(str(e).replace('^', '**'), locals={'y': ys, 'p': ps, 'Q': Qs, 'S': Ss, 't': ts})
Fc_s = conv(Fc)
nonid = [(n, v) for (n, v) in model.all_conditions(tri) if not n.startswith('circle')]
ok2 = True
for name, val in nonid:
    v = val.v if isinstance(val, T) else Fd(val)
    if v == 0: continue
    num_s = sp.Poly(conv(v.numerator()), ts)
    q, rr = sp.div(sp.Poly(num_s.as_expr(), ys, ps, Qs, Ss, ts), sp.Poly(Fc_s, ys, ps, Qs, Ss, ts))
    good = rr.is_zero
    say(f'   sympy: {name}: numerator = Fc x quotient exactly: {good}')
    ok2 = ok2 and good
say('LEMMA (sympy cross-check):', 'holds' if ok2 else 'FAILS')
# divisors (deduplicated) as (numerator, denominator) strings
seen = []; divs = []
for d in DIV + [b[6] - b[1]]:
    dv = d.v if isinstance(d, T) else d
    if dv in seen: continue
    seen.append(dv); divs.append([str(dv.numerator()), str(dv.denominator())])
# denominators of the four checked rational functions (must be nonzero too)
for e in (closing, Eb, Ec, Ed):
    divs.append([str(e.v.denominator()), '1'])
out = {'case': case, 'Fc': str(Fc), 'Eb': str(Eb.v.numerator()), 'Ec': str(Ec.v.numerator()), 'Ed': str(Ed.v.numerator()),
       'divisors': divs, 'lemma': names}
for k in ('Eb', 'Ec', 'Ed'):
    e = Rg(out[k]); say(f'{k}: degrees in (y, p, Q, S, t) =', tuple(e.degree(x) for x in (y, p, Q, S, t)), ', terms', len(e.monomials()))
say('Fc: degrees =', tuple(Fc.degree(x) for x in (y, p, Q, S, t)), ', terms', len(Fc.monomials()), f'; {len(divs)} distinct divisors')
json.dump(out, open(f'stage2-{case}.json', 'w'))
print('FINAL ok' if ok and ok2 else 'FINAL FAIL: the generic lemma does not hold')
