# Exact fair member of RD∩D (24 faces, pyritohedral). A dodecahedron face is an isosceles trapezoid-like quadrilateral with
# corner angles a1, a1, a2, a2 (computed). Girard: 2 a1 + 2 a2 - 2pi = 4pi/24, so a1 + a2 = 13pi/12. With c_i = cos a_i and
# C = cos(13pi/12): c1^2 + c2^2 - 2C c1 c2 = 1 - C^2 (from cos(a1 + a2) = C). Corners are exact in s = mu*sqrt(phi+2):
# planes (±1,±1,0)-type . x = sqrt2 (rhombic dodecahedron at 1) and (0,±phi,±1)-type . x = s (dodecahedron at mu).
import json, itertools, sympy as sp
from mpmath import mp, mpf, sqrt as msqrt, acos as macos, pi as mpi
mp.dps = 120
s, r2, r3, r5, m = sp.symbols('s r2 r3 r5 m')
phi = (1 + r5)/2
D = json.load(open('verts-rdd.json')); mu0 = mpf(D['mu'])
ph = (1 + msqrt(5))/2; k = msqrt(ph + 2); S0 = mu0*k
RD = [v for v in itertools.product((1,-1,0), repeat=3) if sum(1 for c in v if c) == 2]
DO = [p for s1 in (1,-1) for s2 in (1,-1) for p in ((0, s1, s2), (s2, 0, s1), (s1, s2, 0))]   # pattern; phi on first nonzero slot below
def dod(p):   # ico_vertices pattern: (0, s1*phi, s2), (s2, 0, s1*phi), (s1*phi, s2, 0)
    out = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            out += [((0, s1, 0), (0, 0, s2)), ((0, 0, s1), (s2, 0, 0)), ((s1, 0, 0), (0, s2, 0))]
    return out
B = []
for s1 in (1, -1):
    for s2 in (1, -1):
        B += [(0, s1, s2, 'y'), (s2, 0, s1, 'z'), (s1, s2, 0, 'x')]   # the coordinate named carries phi
def Bvec(b, sym=True):
    a = list(b[:3]); i = 'xyz'.index(b[3]); f = phi if sym else ph
    return [a[t]*(f if t == i else 1) for t in range(3)]
planes_sym = [([sp.Integer(c) for c in v], r2) for v in RD] + [(Bvec(b), s) for b in B]
planes_num = [([mpf(c) for c in v], msqrt(2)) for v in RD] + [([mpf(c) for c in Bvec(b, False)], S0) for b in B]
# first dodecahedron face in the dump (keys 12..23)
face = [[mpf(c) for c in v] for v in D['faces']['12']]
assert len(face) == 4
# cyclic order around the face centre
cen = [sum(v[t] for v in face)/4 for t in range(3)]
import mpmath
nrm = [cen[t] for t in range(3)]; u = [face[0][t]-cen[t] for t in range(3)]
w = [nrm[1]*u[2]-nrm[2]*u[1], nrm[2]*u[0]-nrm[0]*u[2], nrm[0]*u[1]-nrm[1]*u[0]]
face.sort(key=lambda v: float(mpmath.atan2(sum((v[t]-cen[t])*w[t] for t in range(3)), sum((v[t]-cen[t])*u[t] for t in range(3)))))
import time; t0 = time.time()
GENS = (s, r2, r3, r5)
REL = [sp.Poly(r2**2 - 2, *GENS), sp.Poly(r3**2 - 3, *GENS), sp.Poly(r5**2 - 5, *GENS)]
def red(P):   # reduce modulo r2^2 = 2, r3^2 = 3, r5^2 = 5, term by term (Poly.rem does not fully reduce here)
    d = {}
    for (a, i, j, kk), c in P.terms():
        key = (a, i % 2, j % 2, kk % 2)
        d[key] = d.get(key, 0) + c * 2**(i//2) * 3**(j//2) * 5**(kk//2)
    return sp.Poly.from_dict({k_: v for k_, v in d.items() if v != 0} or {(0, 0, 0, 0): 0}, *GENS, domain='QQ')
numsub = {s: sp.Float(str(S0), 110), r2: sp.sqrt(2), r3: sp.sqrt(3), r5: sp.sqrt(5)}
V = []
for v in face:
    idx = [i for i, (n, d) in enumerate(planes_num) if abs(sum(a*b for a, b in zip(n, v)) - d) < mpf(10)**-60]
    assert len(idx) == 3, idx
    M = sp.Matrix([planes_sym[i][0] for i in idx]); rhs = sp.Matrix([planes_sym[i][1] for i in idx])
    sol = [sp.together(c) for c in M.LUsolve(rhs)]
    den = sp.lcm([sp.denom(c) for c in sol])
    sg = 1 if sp.N(den.subs(numsub), 50) > 0 else -1          # scale by a positive multiple only
    V.append([red(sp.Poly(sp.expand(sp.cancel(c*den*sg)), *GENS)) for c in sol])
print('exact corners built %.0fs' % (time.time()-t0), flush=True)
dot = lambda a, b: red(sum((x*y for x, y in zip(a, b)), sp.Poly(0, *GENS)))
def cosang(Vc, W1, W2):   # cos of the spherical corner angle at Vc = N/sqrt(D)
    vv = dot(Vc, Vc); a, b = dot(Vc, W1), dot(Vc, W2)
    N = red(dot(W1, W2)*vv - a*b)
    D = red(red(dot(W1, W1)*vv - a*a)*red(dot(W2, W2)*vv - b*b))
    return N, D
angs = []
for i in range(4):
    N_, D_ = cosang(V[i], V[i-1], V[(i+1) % 4])
    c = mpf(str(sp.N(N_.as_expr().subs(numsub)/sp.sqrt(D_.as_expr().subs(numsub)), 110)))
    angs.append((macos(c), N_, D_))
print('corner angles / pi:', [mp.nstr(a/mpi, 12) for a, _, _ in angs], ' Girard excess / pi:', mp.nstr((sum(a for a, _, _ in angs) - 2*mpi)/mpi, 20), ' %.0fs' % (time.time()-t0), flush=True)
a1 = angs[0]; a2 = next(t for t in angs if abs(t[0] - a1[0]) > mpf(10)**-30)
assert sum(1 for t in angs if abs(t[0]-a1[0]) < mpf(10)**-30) == 2
(N1, D1), (N2, D2) = (a1[1], a1[2]), (a2[1], a2[2])
C2 = sp.Poly((2 + r3)/4, *GENS)          # cos^2(13pi/12) = cos^2(pi/12)
one = sp.Poly(1, *GENS)
L = red(red(N1*N1)*D2 + red(N2*N2)*D1 - red((one - C2)*red(D1*D2)))
E = red(red(L*L) - red(red(4*C2*red(N1*N1))*red(red(N2*N2)*red(D1*D2))))
print('equation: degree in s', E.degree(s), ' terms', len(E.terms()), ' %.0fs' % (time.time()-t0), flush=True)
def numE(P, x0):
    with mp.workdps(400):
        sub = {s: sp.Float(str(x0), 140), r2: sp.sqrt(2), r3: sp.sqrt(3), r5: sp.sqrt(5)}
        return sp.N(P.as_expr().subs(sub), 120)
print('E at s_f:', numE(E, S0), '  E at s_f + 1e-6:', numE(E, S0 + mpf(10)**-6), flush=True)
print('N1, D1, N2, D2 degrees in s:', N1.degree(s), D1.degree(s), N2.degree(s), D2.degree(s), flush=True)
Ee = E.as_expr()
for rr, q in ((r2, 2), (r3, 3), (r5, 5)):
    assert sp.degree(Ee, rr) <= 1
    # E = P0 + rr*P1 (degree <= 1 in rr after reduction): eliminate by P0^2 - q*P1^2
    P1 = sp.Poly(Ee.as_expr(), rr).coeff_monomial(rr).as_expr(); P0 = sp.Poly(Ee.as_expr(), rr).coeff_monomial(1).as_expr()
    Ee = red(sp.Poly(sp.expand(P0**2 - q*P1**2), *GENS)).as_expr()   # reduce r^2 = q again before the next split
    print('eliminated', rr, ' degree in s', sp.degree(Ee, s), ' %.0fs' % (time.time()-t0), flush=True)
fac = sp.factor_list(sp.Poly(Ee, s))[1]
def val(p, x0, var):   # distance to the nearest root, |f/f'| at 3000 digits (huge coefficients: no cancellation loss)
    P = sp.Poly(p, var); cs = [int(c) if c.is_Integer else c for c in P.all_coeffs()]
    with mp.workdps(3000):
        x = mpf(str(x0)); f = mpmath.polyval([mpf(sp.Rational(c).p)/mpf(sp.Rational(c).q) for c in cs], x, derivative=True)
        return abs(f[0]/f[1]) if f[1] != 0 else mpf(1)
best = min(fac, key=lambda t: val(t[0], S0, s))[0]
print('factors:', [(sp.degree(t[0], s), mp.nstr(val(t[0], S0, s), 3)) for t in fac])
print('minimal polynomial of s: degree', sp.degree(best, s), ' distance to a root', mp.nstr(val(best, S0, s), 3), ' %.0fs' % (time.time()-t0), flush=True)
print(sp.Poly(best, s).as_expr())
G = sp.resultant(sp.resultant(best, s**2 - m**2*(5 + r5)/2, s), r5**2 - 5, r5)
bm = min(sp.factor_list(sp.Poly(G, m))[1], key=lambda t: val(t[0], mu0, m))[0]
print('minimal polynomial of mu_f: degree', sp.degree(bm, m), ' distance to a root', mp.nstr(val(bm, mu0, m), 3))
print(sp.Poly(bm, m).as_expr())
ok = abs(sum(a for a, _, _ in angs) - 2*mpi - 4*mpi/24) < mpf(10)**-80 and val(best, S0, s) < mpf(10)**-100 and val(bm, mu0, m) < mpf(10)**-100
print('FINAL ok' if ok else 'FINAL FAIL')
