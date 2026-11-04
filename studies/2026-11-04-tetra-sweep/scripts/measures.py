#!/usr/bin/env python3
"""Tetrahedron sweep S(mu) = T ∩ mu(-T) (Concordance 6.1 row 3): isoperimetric, Mahler, Dehn — the tests the cube–octahedron sweep already has.
T = {x : -v.x <= 1}, v in V0 (the 4 corners (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)); -T = {v.x <= 1}. mu in (1/3, 3); octahedron at mu = 1; mu <-> 1/mu is a symmetry (S(1/mu) = -S(mu)/mu)."""
import itertools, json, math, numpy as np, sympy as sp
from scipy.spatial import ConvexHull, HalfspaceIntersection
V0 = np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)], float)
def planes(mu): return [(-v, 1.0) for v in V0] + [(v, mu) for v in V0]
def poly(mu):
    H = np.array([[*n, -c] for n, c in planes(mu)]); return np.unique(np.round(HalfspaceIntersection(H, np.zeros(3)).intersections, 12), axis=0)
def measures(mu):
    P = poly(mu); h = ConvexHull(P); V, A = h.volume, h.area
    pol = np.array([n/c for n, c in planes(mu)]); Vp = ConvexHull(pol).volume
    return V, A, 36*math.pi*V**2/A**3, V*Vp
out = {}
mus = np.linspace(1/3 + 1e-3, 3 - 1e-3, 2001)
rows = [(m, *measures(m)) for m in mus]
iq = max(rows, key=lambda r: r[3]); ma = max(rows, key=lambda r: r[4])
out['iq_max_mu'] = iq[0]; out['iq_max'] = iq[3]; out['mahler_max_mu'] = ma[0]; out['mahler_max'] = ma[4]
# exact on 1 <= mu <= 3: corner cut fraction t = (3 - mu)/4 of the edge of T
m = sp.symbols('mu', positive=True); t = (3 - m)/4
Vt = sp.Rational(8, 3)*sp.Integer(1)  # volume of T with corners (+-1..) scaled: check numerically below
VT = measures(3 - 1e-12)[0]
V = VT*(1 - 4*t**3)
# polar volume: fit a rational function on [1, 3] from samples (polar is conv of two tetrahedra; piecewise rational)
xs = np.linspace(1.05, 2.95, 40); ys = [measures(x)[0]*0 + ConvexHull(np.array([n/c for n, c in planes(x)])).volume for x in xs]
# guess form Vp = (a + b mu + c mu^2 + d mu^3)/mu^3
M = np.array([[1, x, x**2, x**3] for x in xs])/np.array(xs)[:, None]**3; coef = np.linalg.lstsq(M, ys, rcond=None)[0]
out['polar_fit_coef_over_mu3'] = coef.tolist(); out['polar_fit_resid'] = float(np.max(np.abs(M @ coef - ys)))
cr = [sp.nsimplify(float(c), [sp.sqrt(3)], tolerance=1e-9) for c in coef]
Vp = sum(c*m**k for k, c in enumerate(cr))/m**3
f = sp.simplify(sp.nsimplify(VT, tolerance=1e-12)*(1 - 4*t**3)*Vp); out['mahler_exact_1_3'] = str(sp.factor(f))
crit = sp.solve(sp.diff(f, m), m); out['mahler_crit'] = [str(c) for c in crit]; out['mahler_crit_num'] = [complex(sp.N(c)).real for c in crit if abs(complex(sp.N(c)).imag) < 1e-12]
out['mahler_ends'] = {'octahedron mu=1': float(f.subs(m, 1)), 'tetrahedron mu=3': float(sp.limit(f, m, 3)), 'Archimedean TT mu=5/3': str(sp.nsimplify(f.subs(m, sp.Rational(5, 3)))), 'Dehn-zero mu=2': str(sp.nsimplify(f.subs(m, 2)))}
# isoperimetric exact: A ∝ (1 - 2t^2), V ∝ (1 - 4t^3): d/dt log(V^2/A^3) = 12 t (1 - 2t)/((1-4t^3)(1-2t^2)) > 0 on (0, 1/2): max at the octahedron
tt = sp.symbols('t'); out['iq_derivative_factor'] = str(sp.factor(sp.together(sp.diff(2*sp.log(1-4*tt**3) - 3*sp.log(1-2*tt**2), tt))))
# Dehn: for 1 < mu < 3 edges: 6 hexagon–hexagon edges length (1-2t)a, angle alpha = arccos(1/3); 12 hexagon–triangle edges length t a, angle pi - alpha.
# Dehn = (6(1-2t) - 12 t) a ⊗ alpha = 6a(1 - 4t) ⊗ alpha: zero iff t = 1/4 iff mu = 2 (and mu = 1/2 by the symmetry). alpha/pi irrational (cos alpha = 1/3).
P = poly(2.0); h = ConvexHull(P)
E = {}
for s in h.simplices:
    pass
out['dehn_zero_mu'] = [0.5, 2]
# numerical check of the Dehn claim from the actual hull at mu=2: edge lengths and dihedrals
def edge_table(mu):
    pl = planes(mu); P = poly(mu); res = []
    for (i, (n1, c1)), (j, (n2, c2)) in itertools.combinations(enumerate(pl), 2):
        on = [p for p in P if abs(p @ n1 - c1) < 1e-9 and abs(p @ n2 - c2) < 1e-9]
        if len(on) == 2:
            L = np.linalg.norm(on[0] - on[1]); ang = math.pi - math.acos(np.clip(n1 @ n2/np.linalg.norm(n1)/np.linalg.norm(n2), -1, 1)); res.append((round(L, 9), round(math.degrees(ang), 6)))
    return res
from collections import Counter
for mu in (5/3, 2.0, 1.5):
    tab = Counter(edge_table(mu)); al = math.acos(1/3)
    d = sum(k*L*(1 if abs(math.radians(a) - al) < 1e-6 else -1) for (L, a), k in tab.items())  # coefficient of ⊗alpha (pi - alpha ≡ -alpha)
    out[f'edges_mu_{mu:.4f}'] = {f'{L} @ {a}': k for (L, a), k in tab.items()}; out[f'dehn_coeff_mu_{mu:.4f}'] = d
print(json.dumps(out, indent=1))
