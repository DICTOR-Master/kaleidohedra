import sys
from sage.all__sagemath_singular import QQ, PolynomialRing, matrix
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens()
src = {}
for line in open(sys.argv[1]):
    k, e = line.split(' = ', 1); src[k] = Rn(e.strip().replace('^', '**'))
F = [src['G'], src['H1'], src['D']]
for p in ((0, 0, 1), (1, 1, 2)):
    J = matrix(QQ, [[f.derivative(x)(*p) for x in (u, tau, rho)] for f in F])
    print(p, 'F =', [f(*p) for f in F], 'J =', J.rows(), 'det =', J.det())
    # lowest-order terms around p
    sh = {u: u + p[0], tau: tau + p[1], rho: rho + p[2]}
    for nm, f in zip(('G', 'H', 'D'), F):
        g = f.subs(sh); md = min(m.degree() for m in g.monomials())
        low = sum(c * m for c, m in zip(g.coefficients(), g.monomials()) if m.degree() == md)
        print(f'   {nm}: lowest total degree {md}: {str(low)[:300]}')
