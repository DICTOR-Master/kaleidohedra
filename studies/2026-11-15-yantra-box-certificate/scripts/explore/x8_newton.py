"""Exploration: Newton polygons of H~, D~ (and the key inequalities) restricted to G~ = 0 near the two corner points."""
import sys, pickle
from sage.all__sagemath_singular import QQ, PolynomialRing, PowerSeriesRing
Rn = PolynomialRing(QQ, 'u,tau,rho'); u, tau, rho = Rn.gens()
src = {}
for line in open(sys.argv[1]):
    k, e = line.split(' = ', 1); src[k] = Rn(e.strip().replace('^', '**'))
ineq = {k: (Rn(a), Rn(b)) for k, (a, b) in pickle.load(open(sys.argv[2], 'rb')).items()}
G, H, D = src['G'], src['H1'], src['D']
N = 40
for (pu, pt, pr), sx in (((0, 0, 1), 1), ((1, 1, 2), -1)):
    # local coords: u = pu + sx*x, tau = pt + sx*y   (x, y >= 0 inside the domain)
    Ps = PowerSeriesRing(QQ, 'x', default_prec=N); x = Ps.gen()
    Rx = PolynomialRing(Ps, 'r'); r = Rx.gen()
    g = Rx(G(pu + sx * x, 0, pr + r))
    phi = Ps(0)
    for it in range(8):                      # Newton iteration for the root r(x) of g with r(0) = 0
        val = g(phi); der = g.derivative()(phi)
        phi = phi - val / der
    phi = phi.add_bigoh(N)
    print(f'corner {(pu, pt, pr)}: rho - {pr} = {phi.add_bigoh(4)}')
    R2 = PolynomialRing(QQ, 'X,Y'); X, Y = R2.gens()
    phip = phi.polynomial()
    def restrict(f, keep=14):
        Rxy = PolynomialRing(QQ, 'xx,yy'); xx, yy = Rxy.gens()
        h = f(pu + sx * xx, pt + sx * yy, pr + phip(xx))
        # truncate: keep monomials with x-degree < N-? (series accurate below N)
        terms = [(c, m) for c, m in zip(h.coefficients(), h.monomials()) if m.degree(xx) < N - 2]
        return terms, xx, yy
    for name, f in (('H', H), ('D', D)) + tuple((k + ' N', ineq[k][0]) for k in ('b4-b3', 'disc2', 'Q-1/2', 'w5', 'b5-b4')) + tuple((k + ' D', ineq[k][1]) for k in ('b4-b3', 'Q-1/2', 'w5', 'b5-b4')):
        terms, xx, yy = restrict(f)
        pts = sorted(set((m.degree(xx), m.degree(yy)) for c, m in terms))
        # lower-left Newton polygon vertices
        hull = []
        for p in sorted(pts):
            while len(hull) >= 2 and (hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1]) - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0]) <= 0: hull.pop()
            hull.append(p)
        hull = [h for h in hull]
        lo = [p for p in hull if p[1] <= min(q[1] for q in hull if q[0] <= p[0])]
        coef = {(m.degree(xx), m.degree(yy)): c for c, m in terms}
        print(f'   {name}: Newton vertices (deg x, deg y): {[(p, str(coef[p])[:12]) for p in lo][:8]}')
