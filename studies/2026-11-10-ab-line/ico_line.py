"""Aim 1, step 4 (DICTO 10 Nov 2026): the icosahedral line. Physical star of the icosahedral cut-and-project scheme from Z^6, with the
golden ratio replaced by a parameter x: e(x) = (1,x,0), (-1,x,0), (0,1,x), (0,-1,x), (x,0,1), (-x,0,1) (3 x 6 matrix P(x)).
x = phi: the icosahedral quasicrystal (golden rhombohedra); x = F(n+1)/F(n) = 1/1, 2/1, 3/2, 5/3, ...: the cubic approximants.
Search: an integer 6 x 6 matrix A (a map of Z^6) with P(x) A = c(x) R P(g(x)) for a rational map g, a scalar c and a fixed rotation R,
identically in x; then g is a hop or a turn of the line. Method: A from the golden inflation (P(phi) A = phi P(phi), exact in Q(sqrt5)),
then test it on the whole line symbolically. usage: python ico_line.py"""
import sympy as sp, itertools
x = sp.symbols('x', positive=True); phi = (1 + sp.sqrt(5)) / 2
def P(t): return sp.Matrix([[1, -1, 0, 0, t, -t], [t, t, 1, -1, 0, 0], [0, 0, t, t, 1, 1]])
# integer A: inflation by phi^3 in physical space and by phi'^3 = (-1/phi)^3 in internal space (Galois conjugate): 6 x 6 linear system
phc = (1 - sp.sqrt(5)) / 2
Big = sp.Matrix.vstack(P(phi), P(phc))
Tgt = sp.Matrix.vstack(phi**3 * P(phi), phc**3 * P(phc))
Asol = sp.simplify(Big.inv() * Tgt)
print('A (exact):', Asol.tolist(), ' integer:', all(sp.nsimplify(v).is_integer for v in Asol))
cols = [list(Asol[:, k]) for k in range(6)]
A = sp.Matrix(cols).T
print('A =', A.tolist(), ' det', A.det())
M = sp.simplify(P(x) * A)
# does P(x) A equal c(x) P(g(x)) for some g? compare column 0 and the pattern
print('P(x) A columns:'); sp.pprint(M)
c = sp.simplify(M[0, 0]); g = sp.simplify(M[1, 0] / c)
print('read off from column 0: c(x) =', c, ', g(x) =', sp.factor(g))
D = sp.simplify(M - c * P(g)); print('P(x) A == c(x) P(g(x)) for every x:', D == sp.zeros(3, 6))
h = lambda y: 1 + 1/y
print('g equals the Fibonacci hop applied three times, h(h(h(x))):', sp.simplify(g - h(h(h(x)))) == 0)
print('fixed points of g:', sp.solve(sp.Eq(g, x), x))
F = [1, 1]
while len(F) < 12: F.append(F[-1] + F[-2])
print('g on the cubic approximants:', ', '.join(f'{F[n+1]}/{F[n]} -> {sp.nsimplify(g.subs(x, sp.Rational(F[n+1], F[n])))}' for n in range(1, 7)))
print('FINAL ok' if D == sp.zeros(3, 6) else 'FINAL FAIL')
