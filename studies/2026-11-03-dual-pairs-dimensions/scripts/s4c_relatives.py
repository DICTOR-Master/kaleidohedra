"""Step 4c: golden relatives of OG: Q(mu, phi^2) = H(mu) cap phi^2 D* at the golden mu of the icosahedron side (neutral labels).
Face signature, regular hexagons / kites test, and the smallest integer scale putting the corners in the Z^6 shadow module M.
usage: ~/geom/bin/python s4c_relatives.py L|G -> ../data/s4c-relatives-<L|G>.json
"""
from dp_lib import *          # noqa
import sys, sympy as sp, numpy as np, math
out = {}
P = Pair('dodecahedron', platonic()['dodecahedron'][0]); D = P.V; rho2 = P.rho2
U = [(ZERO, ONE, PHI), (ZERO, ONE, -PHI), (ONE, PHI, ZERO), (ONE, -PHI, ZERO), (PHI, ZERO, ONE), (-PHI, ZERO, ONE)]
def q5(x): a, b, c, d = x.v; return (a, c)         # x = a + c sqrt5
Mq = sp.Matrix([[sp.Rational(*(lambda t: (t.numerator, t.denominator))(q5(U[j][i // 2])[i % 2])) for j in range(6)] for i in range(6)])
Minv = Mq.inv()
def coords(p):
    vec = sp.Matrix([sp.Rational(q5(p[i // 2])[i % 2].numerator, q5(p[i // 2])[i % 2].denominator) for i in range(6)])
    return Minv * vec
zphi = (all(all(c.q == 1 for c in coords(vscale(PHI, u))) for u in U))
out['M_closed_under_phi'] = zphi
check(f'D: M (Z-span of the 12 corners (0, +-1, +-phi), = shadow of Z^6) closed under phi: {zphi} (recorded; the admissible scales still form a lattice in Q^2)', True)
def ideal(V):
    rows = []
    for p in V:
        c1 = coords(p); c2 = coords(vscale(PHI, p))
        for i in range(6): rows.append((c1[i], c2[i]))
    den = sp.ilcm(*[x.q for r in rows for x in r])
    Z = sp.Matrix([[int(x * den) for x in r] for r in rows])
    from sympy.matrices.normalforms import hermite_normal_form
    Hn = hermite_normal_form(Z.T)        # columns span the row module of Z (as 2-vectors)
    Lam = Hn[:, :2] / den                 # basis (columns) of Lambda = Z-span of the functionals
    Ldual = (Lam.T).inv()                 # columns: basis of the dual lattice = allowed (a, b)
    best = None
    L = [[Fr(int(Ldual[r_, c_].p), int(Ldual[r_, c_].q)) for c_ in range(2)] for r_ in range(2)]
    for i in range(-40, 41):
        for j in range(-40, 41):
            if i == 0 and j == 0: continue
            a = L[0][0] * i + L[0][1] * j; b = L[1][0] * i + L[1][1] * j
            nrm = abs(a * a + a * b - b * b)
            if best is None or nrm < best[0]: best = (nrm, a, b)
    Li = Ldual.inv(); Li = [[Fr(int(Li[r_, c_].p), int(Li[r_, c_].q)) for c_ in range(2)] for r_ in range(2)]
    nmin = None
    for n_ in range(1, 1000000):
        if (Li[0][0] * n_).denominator == 1 and (Li[1][0] * n_).denominator == 1: nmin = n_; break
    return best, nmin

which = sys.argv[1]
x = x_golden(3)[1] if which == 'L' else x_golden(3)[0]
lab = 'Lesser' if which == 'L' else 'Greater'
mu = P.mu_Ps(x); Hm = P.Hull(mu); C_, F_, Pl_ = planes_of(Hm)
Cq = hull3(vertices_H(Pl_ + [(v, rho2) for v in D]))[0]; Cq, Fq = hull3(Cq)
def sides(f):
    fp = np.array([[float(t) for t in Cq[i]] for i in f]); fc = fp.mean(0); n = np.cross(fp[1] - fp[0], fp[2] - fp[0])
    u = fp[0] - fc; u /= np.linalg.norm(u); w = np.cross(n / np.linalg.norm(n), u)
    o = sorted(range(len(f)), key=lambda i: math.atan2((fp[i] - fc) @ w, (fp[i] - fc) @ u)); f = [f[i] for i in o]
    return [d2(Cq[f[i]], Cq[f[(i + 1) % len(f)]]) for i in range(len(f))]
hexreg = all(len({s.v for s in sides(f)}) == 1 for f in Fq if len(f) == 6)
kites = all((lambda s: (s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0]))(sides(f)) for f in Fq if len(f) == 4)
b_, n_ = ideal(Cq)
out = {'label': f'Q(mu, phi^2) at the {lab} Golden Cut Icosahedron mu', 'mu': kdesc(mu), 'hull_faces': signature(F_), 'corners': len(Cq),
       'faces': signature(Fq), 'hexagons_regular': hexreg, 'quads_kites': kites, 'smallest_integer_scale_in_M': n_}
check(f'C: Q(mu, phi^2) at mu = {kstr(mu)} ({lab} GCI): hull faces {signature(F_)}, {len(Cq)} corners, faces {signature(Fq)}, '
      f'hexagons regular {hexreg}, kites {kites}, smallest integer lift scale {n_} (OG: 228)', True)
save(f's4c-relatives-{which}.json', out)
