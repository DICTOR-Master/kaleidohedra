"""Independent check of the two exact results (DICTO 9 Nov 2026: "do we need independent verification"). Each yantra is solved again
straight from its geometric conditions by Newton's method at 260 digits (no elimination, no polynomial used); then each minimal
polynomial is evaluated there, relative to the size of its terms, and irreducibility is re-checked in a second system (Singular via
sage, besides PARI). Pass: relative residual below 1e-240 for both, both irreducible in both systems."""
import mpmath as mp
mp.mp.dps = 260
from model import solve
phi = (1 + mp.sqrt(5)) / 2
def yan(u, v, Q, S):
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root=1)
def inc(t, Q):
    b, w = t['b'], t['w']; m1 = w[1] / (Q - b[1]); h = abs(Q - b[5]); hw = m1 * h; r = hw * h / (hw + mp.sqrt(hw**2 + h**2))
    return b[5] + (r if Q > b[5] else -r)
def F_dicto(u, Q, S):
    t = yan(u, 2 / phi**3 / u, Q, S); b, w = t['b'], t['w']
    return [w[1]**2 + b[1]**2 - b[1], w[9]**2 + b[9]**2 - b[9], inc(t, Q) - mp.mpf(1) / 2]
def F_kul(u, Q, S):
    t = yan(u, u, Q, S); b, w = t['b'], t['w']
    return [w[1]**2 + b[1]**2 - b[1], w[9]**2 + b[9]**2 - b[9], inc(t, Q) - mp.mpf(1) / 2]
def rel(coeffs, x):
    tot = mp.mpf(0); size = mp.mpf(0); p = mp.mpf(1)
    for c in coeffs: tot += c * p; size += abs(c * p); p *= x
    return abs(tot) / size
def coeffs_of(path):
    import re
    s = open(path).read().replace(' ', '').replace('\n', '').replace('u', 'x')
    from sympy import Poly, symbols, sympify
    x = symbols('x'); P = Poly(sympify(s.replace('^', '**')), x)
    return [mp.mpf(int(c)) for c in reversed(P.all_coeffs())], P
res = {}
for name, F, start, path in (('DICTO Yantra', F_dicto, ('0.679318588706774657388650310391', '0.576510321707840', '0.968268607459'), 'dicto-yantra-exact-u.txt'),
                             ('Kulaichev', F_kul, ('0.750438516022214024406084657051234510340891003639790315415314', '0.537', '0.835'), 'kulaichev-minpoly-u.txt')):
    u0 = mp.mpf(start[0])
    Qs = [mp.mpf(start[1])] if name == 'DICTO Yantra' else [mp.mpf(x) / 100 for x in range(50, 60)]
    sol = None
    for Q0 in Qs:
        for S0 in ([mp.mpf(start[2])] if name == 'DICTO Yantra' else [mp.mpf(x) / 100 for x in range(80, 99)]):
            try:
                u, Q, S = mp.findroot(F, (u0, Q0, S0), tol=mp.mpf(10)**-250, maxsteps=200)
                if abs(u - u0) < mp.mpf(10)**-25 and max(abs(e) for e in F(u, Q, S)) < mp.mpf(10)**-245: sol = u; break
            except Exception: pass
        if sol is not None: break
    c, P = coeffs_of(path)
    r = rel(c, sol) if sol is not None else mp.mpf(1)
    print(f'{name}: Newton u (first 70 digits) {mp.nstr(sol, 70) if sol is not None else None}; polynomial degree {P.degree()}; relative residual {mp.nstr(r, 3)}', flush=True)
    res[name] = (r, P)
from sage.all__sagemath_singular import PolynomialRing, ZZ
R = PolynomialRing(ZZ, 'x'); irr = {}
for name, (r, P) in res.items():
    q = R([int(a) for a in reversed(P.all_coeffs())]); irr[name] = q.is_irreducible(); print(f'{name}: irreducible (Singular/sage): {irr[name]}', flush=True)
ok = all(r < mp.mpf(10)**-240 for r, P in res.values()) and all(irr.values())
print('FINAL ok' if ok else 'FINAL FAIL: an exact form did not survive the independent check')
