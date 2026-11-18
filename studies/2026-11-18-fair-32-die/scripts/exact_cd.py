# Exact fair member of C∩D (18 faces, pyritohedral). The cube face x = 1 is cut by the dodecahedron planes
# (x ± φz) = s and (φx ± y) = s (unnormalised normals (1,0,±φ), (φ,±1,0); s = μ·√(φ+2)) into a rectangle with corners
# (1, ±Y, ±Z), Y = s − φ, Z = (s − 1)/φ. Its cone has four equal corner angles; Girard (or the rectangle formula
# Ω = 4 arcsin(YZ/√((1+Y²)(1+Z²)))) with Ω = 4π/18 gives YZ = sin(π/18)·√((1+Y²)(1+Z²)).
# Check against the computed μ_f (140 digits), then the minimal polynomial of μ_f over Q by resultants.
import json, sympy as sp
from mpmath import mp, mpf, sqrt as msqrt, sin as msin, pi as mpi, findroot
mp.dps = 120
s, r5, x, m = sp.symbols('s r5 x m')
phi = (1 + r5) / 2
Y = s - phi; Z = (s - 1) / phi
# x = sin(pi/18): 8x^3 - 6x + 1 = 0 (sin 3θ = 1/2)
E = sp.expand(sp.numer(sp.together((Y*Z)**2 - x**2*(1 + Y**2)*(1 + Z**2))))
mu0 = mpf(json.load(open('verts-cd.json'))['mu'])
ph = (1 + msqrt(5))/2; k = msqrt(ph + 2)
f = lambda S: ((S-ph)*(S-1)/ph)**2 - msin(mpi/18)**2*(1+(S-ph)**2)*(1+((S-1)/ph)**2)
S0 = findroot(f, mu0*k)
print('mu from the rectangle equation:', mp.nstr(S0/k, 50), ' |diff| vs computed', mp.nstr(abs(S0/k - mu0), 3))
ok = abs(S0/k - mu0) < mpf(10)**-100
# eliminate r5 (r5^2 = 5) and x (8x^3 - 6x + 1), then pass from s to mu: s^2 = mu^2 (phi + 2) -> work with s first
R = sp.resultant(sp.resultant(E, r5**2 - 5, r5), 8*x**3 - 6*x + 1, x)
fac = sp.factor_list(sp.Poly(R, s))[1]
best = None
for fp, e in fac:
    val = abs(mp.mpf(sp.Poly(fp, s).eval(sp.Float(str(S0), 110)).evalf(110)))
    if best is None or val < best[0]: best = (val, fp)
print('minimal polynomial of s = mu*sqrt(phi+2): degree', sp.degree(best[1], s), ' value at s', mp.nstr(best[0], 3))
print(sp.Poly(best[1], s).as_expr())
# mu itself: eliminate s with s^2 = m^2 (phi+2), phi+2 = (5 + r5)/2
G = sp.resultant(sp.resultant(best[1].subs(s, s), s**2 - m**2*(5 + r5)/2, s), r5**2 - 5, r5)
facm = sp.factor_list(sp.Poly(G, m))[1]
bm = min(facm, key=lambda t: abs(mp.mpf(sp.Poly(t[0], m).eval(sp.Float(str(mu0), 110)).evalf(110))))[0]
print('minimal polynomial of mu_f: degree', sp.degree(bm, m), ' value', mp.nstr(abs(mp.mpf(sp.Poly(bm, m).eval(sp.Float(str(mu0), 110)).evalf(110))), 3))
print(sp.Poly(bm, m).as_expr())
ok = ok and best[0] < mpf(10)**-60
print('FINAL ok' if ok else 'FINAL FAIL')
