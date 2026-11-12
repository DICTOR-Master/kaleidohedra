"""Aim 2, chunk 3 closed forms (12 Nov 2026): exact forms of the icosahedral numbers chunk 3 gave only numerically
(data/canon-turn.log): the zero mu* = 2.891793 of the order-6 anisotropy of Omega(S(mu); t u) in the chamber (phi^2, (5+sqrt5)/2),
and c2/c0, anisotropy/c0 at the turn's fixed point mu = sqrt((25+11 sqrt5)/6).
Method: in that chamber every facet of S has b = 1 or b = mu, so each vertex term of the expansion is a polynomial in nu = 1/mu
over Q(sqrt5): build the coefficients EXACTLY as polynomials in nu (collect powers, radsimp each coefficient), then
anisotropy/c0 = P(nu)/(K nu); mu* from the factor of P over Q(sqrt5) (and the norm polynomial over Q); fixed-point values as
algebraic numbers with their minimal polynomials over Q.
Controls: (C1) the nu-polynomials equal the raw chunk-3 sums at 3 rational mu exactly; (C2) values agree with the chunk-3 numbers
(2.891792659030825, 0.778317125037227, 0.000431717368330967) to 1e-12; (C3) each minimal polynomial vanishes at its value to
1e-30 and is irreducible over Q; (N) a perturbed polynomial (constant term + 1) does not vanish there.
Definitions reused verbatim from canon_turn.py (its function block and its icosahedron setup block)."""
import sys, os, re
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'canon_turn.py')).read()
defs = src[:src.index('# ---------- controls on the cube ----------')]
ico = src[src.index('# ---------- icosahedron / dodecahedron ----------'):src.index('Hi_, pi_, fixi')]
g = {'__name__': 'canon_turn_defs'}; exec(defs, g); exec(ico, g)
sp, mu, phi, check = g['sp'], g['mu'], g['phi'], g['check']
import mpmath as mp
mp.mp.dps = 60
H = g['sweep'](g['icoA'], g['icoV']); faces, icoV = g['faces'], g['icoV']
nu = sp.Symbol('nu', positive=True); s5 = sp.sqrt(5)
m0 = sp.Rational(1559, 500)                                   # inside (phi^2, (5+sqrt5)/2) = (2.618, 3.618)
dirs = {'vertex axis': sp.Matrix([0, 1, phi]), 'face axis': sp.Matrix([sum(icoV[f][q] for f in faces[0]) for q in range(3)])}
ORD = 6
def series_nu(u, order):
    """t-coefficients of Omega(S(mu); t u) built directly as polynomials in nu = 1/mu over Q(sqrt5): each facet has b = 1 or mu,
    so 1/b = 1 or nu (pilot 12 Nov: the raw sums hid nu in compound denominators)"""
    vs = g['vertices'](H, m0); co = [sp.Integer(0)] * (order + 1)
    for X, tight0 in vs.items():
        for tri in g['vertex_triangles'](H, X, tight0):
            d = abs(sp.nsimplify(sp.radsimp(sp.Matrix.hstack(*[H[k][0] for k in tri]).det()), [s5]))
            ser = [d] + [sp.Integer(0)] * order
            for k in tri:
                ib = sp.Integer(1) if H[k][1] == 1 else nu
                c = sp.radsimp(sp.expand((H[k][0].T * u)[0])); gg = [sp.expand((c * ib) ** j) for j in range(order + 1)]
                ser = [sp.expand(ib * sum(ser[i] * gg[j - i] for i in range(j + 1))) for j in range(order + 1)]
            for j in range(order + 1): co[j] += ser[j]
    return [sp.Poly(sp.radsimp(sp.expand(x)), nu) for x in co]
co = {}
for dn, u in dirs.items():
    n2 = sp.radsimp(sp.expand(sum(x ** 2 for x in u)))
    pn = series_nu(u, ORD)
    co[dn] = {j: sp.Poly(sp.expand(sp.radsimp(pn[j].as_expr() / n2 ** (j // 2))), nu) for j in (0, 2, ORD)}
    print(f'PROGRESS 0.3 series along the {dn}', flush=True)
raw = {dn: g['series_warren'](H, m0, u, ORD, raw=True) for dn, u in dirs.items()}
n2s = {dn: sp.radsimp(sp.expand(sum(x ** 2 for x in u))) for dn, u in dirs.items()}
c0 = co['vertex axis'][0]; c2 = co['vertex axis'][2]
an = sp.Poly(sp.radsimp(sp.expand(co['vertex axis'][ORD].as_expr() - co['face axis'][ORD].as_expr())), nu)
print(f'c0 = {c0.as_expr()}', flush=True)
print(f'c2 = {sp.factor(c2.as_expr(), extension=s5)}', flush=True)
print(f'order-6 anisotropy (vertex axis minus face axis) = {sp.factor(an.as_expr(), extension=s5)}', flush=True)
for x in (sp.Rational(27, 10), sp.Rational(3, 1), sp.Rational(7, 2)):
    E = lambda e: sp.radsimp(sp.expand(e))
    okx = all(E(raw['vertex axis'][j].subs(mu, x) / n2s['vertex axis'] ** (j // 2) - P.as_expr().subs(nu, 1 / x)) == 0 for j, P in ((0, c0), (2, c2))) and \
          E((raw['vertex axis'][ORD] / n2s['vertex axis'] ** 3 - raw['face axis'][ORD] / n2s['face axis'] ** 3).subs(mu, x) - an.as_expr().subs(nu, 1 / x)) == 0
    check(f'(C1) nu-polynomials = the raw chunk-3 sums exactly at mu = {x}', okx)
print('PROGRESS 0.6 exact polynomials', flush=True)
# the zero mu*: factor the anisotropy numerator over Q(sqrt5); norm polynomial over Q
A = an.as_expr(); Abar = A.subs(s5, -s5)
N = sp.Poly(sp.expand(A * Abar), nu)
Nf = sp.factor_list(N.as_expr())
target = mp.mpf(1) / mp.mpf('2.891792659030825')
best = None
for fac, mult in Nf[1]:
    if not fac.has(nu): continue
    for r in sp.Poly(fac, nu).nroots(n=50):
        if abs(complex(r).imag) < 1e-30 and abs(mp.mpf(complex(r).real) - target) < 1e-10: best = (fac, r)
fac, r = best; mustar = 1 / r
mp_mu = sp.Poly(sp.expand(sp.numer(sp.together(fac.subs(nu, 1 / mu)))), mu)
print(f'mu* = {sp.N(mustar, 30)}: 1/mu* is a root of {sp.factor(fac)} (irreducible over Q, degree {sp.degree(fac, nu)}); '
      f'mu* is a root of {mp_mu.as_expr()}', flush=True)
check('(C2) mu* agrees with chunk 3 (2.891792659030825) to 1e-12', abs(float(mustar) - 2.891792659030825) < 1e-12)
check('(C3) its minimal polynomial is irreducible over Q', len(sp.factor_list(mp_mu.as_expr())[1]) == 1 and sp.factor_list(mp_mu.as_expr())[1][0][1] == 1)
facs5 = sp.factor_list(A, extension=s5)[1]
for f5, m5 in facs5:
    if f5.has(nu) and abs(complex(sp.N(f5.subs(nu, r), 40))) < 1e-25:
        print(f'   over Q(sqrt5): 1/mu* is a root of {sp.expand(f5)}', flush=True)
# fixed-point values
F = sp.sqrt((25 + 11 * s5) / 6); nuF = 1 / F
vals = {'c2/c0': sp.cancel(c2.as_expr() / c0.as_expr()), 'anisotropy/c0': sp.cancel(an.as_expr() / c0.as_expr())}
ref = {'c2/c0': 0.778317125037227, 'anisotropy/c0': 0.000431717368330967}
x = sp.Symbol('x')
for k, e in vals.items():
    v = sp.radsimp(sp.expand(e.subs(nu, nuF)))
    mpoly = sp.minimal_polynomial(v, x)
    num = sp.N(v, 40)
    print(f'{k} at the fixed point = {sp.nsimplify(v)} = {sp.N(v, 20)}; minimal polynomial {mpoly}', flush=True)
    check(f'(C2) {k} agrees with chunk 3 ({ref[k]}) to 1e-12', abs(float(num) - ref[k]) < 1e-12)
    check(f'(C3) its minimal polynomial vanishes there (1e-30) and is irreducible', abs(sp.N(mpoly.subs(x, v), 50)) < 1e-30 and len(sp.factor_list(mpoly)[1]) == 1)
    check(f'(N) the perturbed polynomial (constant + 1) does not vanish there', abs(sp.N((mpoly + 1).subs(x, v), 50)) > 1e-6)
print('PROGRESS 1.0 closed forms', flush=True)
print('FINAL ok: all controls held' if g['ok'] else 'FINAL FAIL')
