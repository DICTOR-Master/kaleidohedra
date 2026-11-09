"""Second-system check (sympy, exact) of the Q(sqrt5) splitting in Theorem 9: the two degree-40 factors written by stage 1 (PARI
nffactor) multiply back to g(y) = f160(sqrt y) up to a rational constant, and they are conjugate (w -> -w). With g irreducible
over Q (stage 1, three ways) this shows each factor is irreducible over Q(sqrt5): a proper factor h of one of them would give
a proper factor h * conj(h) (or h itself) of g over Q. So u^2 has degree 40 over Q(sqrt5), and sqrt5 lies in Q(u^2)."""
import sympy as sp
y, w = sp.symbols('y w')
L = [l for l in open('stage1-D-g-over-Qsqrt5.txt').read().split('\n') if l.strip()]
def parse(s):
    s = s.replace('Mod(', 'MOD(').replace('^', '**')
    return sp.sympify(s, locals={'MOD': lambda a, m: a, 'y': y, 'w': w})
g1, g2 = (sp.Poly(sp.rem(sp.Poly(parse(s), w), sp.Poly(w**2 - 5, w)).as_expr(), y, w) for s in L)
f = sp.Poly(sp.sympify(open('dicto-yantra-exact-u.txt').read().strip().replace('^', '**').replace('x', 'u')), sp.Symbol('u'))
g = sp.Poly(sum(c * y**(k[0] // 2) for k, c in f.terms()), y)
prod = sp.Poly(sp.rem(sp.Poly((g1 * g2).as_expr(), w), sp.Poly(w**2 - 5, w)).as_expr(), y, w)
ratio = sp.Rational(g.LC(), sp.Poly(prod.as_expr(), y).LC())
same = sp.expand(prod.as_expr() * ratio - g.as_expr()) == 0
conj = sp.expand(sp.rem(sp.Poly(g1.as_expr().subs(w, -w), w), sp.Poly(w**2 - 5, w)).as_expr() * sp.Poly(g2.as_expr(), y, w).LC() - g2.as_expr() * sp.Poly(g1.as_expr().subs(w, -w), y, w).LC()) == 0
print('degrees in y:', g1.degree(y), g2.degree(y), '; product = g up to the constant', ratio if len(str(ratio)) < 60 else '(large)', ':', same, '; conjugate pair:', conj)
print('FINAL ok' if same and conj and g1.degree(y) == g2.degree(y) == 40 else 'FINAL FAIL: Q(sqrt5) splitting not confirmed')
