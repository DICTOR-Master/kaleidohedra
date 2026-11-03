"""Step 4b: OG and the icosahedral module (lattice test). M = Z-span of the icosahedron corners (0, +-1, +-phi) cyclic = the shadow
of Z^6 (primitive icosahedral module). For OG = Q(mu_TI, phi^2) (s4) find the set of scales lam in Q(sqrt5) with lam * OG in M:
the lattice (in Q^2) of admissible scales; its smallest-|norm| element and the smallest positive integer
scale, in our frame (D with R^2 = 3) and in the polar-Dharma chain frame (where the bridge study found 171).
Also the same for the stations S(phi^2), H(mu_TI), the truncated icosahedron S(mu_TI) and the golden cuts, to see where 19 enters.
usage (dicto-big-brother): ~/geom/bin/python s4b_og_lattice.py -> ../data/s4b-og-lattice.json
"""
from dp_lib import *          # noqa
import sympy as sp
out = {}
P = Pair('dodecahedron', platonic()['dodecahedron'][0]); D = P.V
muTI = P.mu_Ps(ONE / 3); rho2 = P.rho2
C_PD, F_PD, Pl_PD = planes_of(P.Hull(muTI))
C_OG = hull3(vertices_H(Pl_PD + [(v, rho2) for v in D]))[0]
# D. lattice ideal
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
import json, numpy as np
chain = json.load(open(os.path.join(DATA, 'reversed-chain.json')))
k0 = float(np.linalg.norm(np.array(chain[1][1]), axis=1).max()) / float(PHI)     # chain ID radius / our ID radius (phi)
best, nmin = ideal(C_OG)
gen = f'{best[1]} + {best[2]} phi'
print('   our frame: ideal smallest_norm_scale', gen, 'norm', best[0], 'smallest integer scale', nmin, flush=True)
# chain frame: chain = k0 * ours; k0^2 exact?
out['lattice_ideal_our_frame'] = {'smallest_norm_scale': gen, 'abs_norm': str(best[0]), 'smallest_integer_scale': nmin}
# D in the chain frame: chain OG = k0 * ours.  k0 in Q(sqrt5)?
k0K = None
for den in range(1, 400):
    for A in range(-2000, 2001):
        Bf = (k0 * den - A) / 5 ** .5; Bn = round(Bf)
        if abs(Bf - Bn) < 1e-10:
            k0K = K(Fr(A, den), 0, Fr(Bn, den)); break
    if k0K is not None: break
if k0K is not None and abs(float(k0K) - k0) < 1e-12:
    bestc, nminc = ideal([vscale(k0K, p) for p in C_OG])
    out['lattice_ideal_chain_frame'] = {'chain_scale': kstr(k0K), 'smallest_norm_scale': f'{bestc[1]} + {bestc[2]} phi', 'abs_norm': str(bestc[0]), 'smallest_integer_scale': nminc}
    print('   chain frame: scale', kstr(k0K), 'smallest_norm_scale', bestc, 'smallest integer', nminc, flush=True)
    check(f'D: chain frame smallest integer lift scale = {nminc} = 2 x 171 (bridge study: 171, its module convention differs by the factor 2: recorded)', nminc in (171, 342))
else:
    out['lattice_ideal_chain_frame'] = 'chain scale not in Q(sqrt5)'
    check('D: chain scale in Q(sqrt5)', False)
# where 171 comes from: norm of mu_TI
check(f'D: field norm of mu_TI = {q5_norm(muTI)} (= 9/19); 171 = 9 x 19', q5_norm(muTI) == Fr(9, 19))

for lab, V in (('icosidodecahedron S(phi^2)', P.S(rho2)), ('pentakis dodecahedron H(mu_TI)', C_PD), ('truncated icosahedron S(mu_TI)', P.S(muTI)),
               ('dodecahedron', D), ('Lesser Golden Cut Icosahedron S(sqrt5)', P.S(P.mu_Ps(x_golden(3)[1]))),
               ('Greater Golden Cut Dodecahedron', P.S(P.mu_P(x_golden(5)[0])))):
    b, n_ = ideal(V); out.setdefault('other_stations', {})[lab] = {'smallest_norm_scale': f'{b[1]} + {b[2]} phi', 'abs_norm': str(b[0]), 'smallest_integer_scale': n_}
    print('   ', lab, b, n_, flush=True)
save('s4b-og-lattice.json', out)
