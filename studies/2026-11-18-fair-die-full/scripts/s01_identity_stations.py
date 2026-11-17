"""Protocol steps 1-3 for the fair 14-face die: exact identity, symmetry and orbits, similarity invariant, catalogue screen,
station check against every named point of the cube-octahedron line, turn and swap partners, Turn Law t_min.
Control shape: Kelvin's truncated octahedron (mu = 3/2). Exact (sympy resultants, fdlib.minpoly_of) unless marked float."""
import itertools, math, json, sys, os
import numpy as np, sympy as sp, mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fdlib import *

C = Checks(); R = {}
print("STEP 1. Exact definition")
cub = sp.Poly(sp.Symbol('x')**3 - 9*sp.Symbol('x')**2 - sp.Symbol('x') + 1)
C("T = tan(pi/14)tan(2pi/7) is a root of x^3-9x^2-x+1 (60 digits)", abs(mp.polyval([1, -9, -1, 1], T_HP)) < mp.mpf(10)**-55)
C("b_f is a root of m_b = y^6-18y^4-4y^2+8 (60 digits)", abs(mp.polyval([1, 0, -18, 0, -4, 0, 8], B_HP)) < mp.mpf(10)**-55)
C("m_b irreducible over Q", sp.Poly(M_B, y).is_irreducible)
pmu, _ = minpoly_of(y + 1)
want = sp.Poly(z**6 - 6*z**5 - 3*z**4 + 52*z**3 - 97*z**2 + 74*z - 13, z)
C("minimal polynomial of mu_f equals the God's Dice value", pmu == want, str(pmu.as_expr()))
# fairness, 60 digits: square face of half-diagonal b at distance 1 subtends 4 atan(b^2/(2 sqrt(1+b^2)))
pC = 4*mp.atan(B_HP**2/(2*mp.sqrt(1 + B_HP**2)))/(4*mp.pi)
C("p(square) = 1/14 at mu_f (60-digit evaluation of the exact formula)", abs(pC - mp.mpf(1)/14) < mp.mpf(10)**-50, mp.nstr(pC, 20))
R['mu_f'] = mp.nstr(MU_HP, 40); R['minpoly_mu_f'] = str(pmu.as_expr())

print("\nSTEP 2. Counts, symmetry, orbits (fair die and Kelvin control)")
SP = [np.array(P)*np.array(s) for P in itertools.permutations(np.eye(3)) for s in itertools.product((1, -1), repeat=3)]
def orbit_count(items, act):
    seen, k = set(), 0
    for it in items:
        if it in seen: continue
        k += 1; seen |= {act(g, it) for g in SP}
    return k
for name, mu in (("fair die", MUF), ("Kelvin TO (control)", KELVIN)):
    V = corners(mu); F, N, H = faces(V)
    E = {tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f in F for i in range(len(f))}
    kinds = sorted(len(f) for f in F)
    C(f"{name}: 24 corners, 36 edges, 14 faces (6 squares, 8 hexagons), Euler 2", (len(V), len(E), len(F)) == (24, 36, 14) and kinds == [4]*6 + [6]*8 and len(V) - len(E) + len(F) == 2)
    key = lambda p: tuple(np.round(p, 9))
    Vs = {key(v) for v in V}
    C(f"{name}: all 48 signed permutation matrices (group Oh) map the corner set to itself", all({key(g @ v) for v in V} == Vs for g in SP))
    cor = orbit_count([key(v) for v in V], lambda g, p: key(g @ np.array(p)))
    fac = orbit_count([key(n) for n in N], lambda g, p: key(g @ np.array(p)))
    mids = [key((V[a] + V[b])/2) for a, b in E]
    edg = orbit_count(mids, lambda g, p: key(g @ np.array(p)))
    C(f"{name}: orbits under Oh: corners 1, edges 2, faces 2 (isogonal, not isohedral)", (cor, edg, fac) == (1, 2, 2), f"{cor},{edg},{fac}")
    L = sorted({round(float(np.linalg.norm(V[a] - V[b])), 9) for a, b in E})
    print(f"    {name}: edge lengths {L}; circumradius {np.linalg.norm(V[0]):.9f}")
    R[name] = {'edge_lengths': L, 'orbits': (cor, edg, fac)}
print("  Symmetry group is exactly Oh (order 48): it contains Oh; the finite subgroups of O(3) containing Oh are Oh itself (Ih does not contain Oh).")
C("fair die hexagon is not regular (edge lengths sqrt2 b and sqrt2(1-b) differ): a truncated triangle", abs(BF - 0.5) > 0.1)

print("\nSTEP 3. Similarity invariant and catalogue screen")
# hexagon edges (0,-b,b) and (0,1-b,b-1) are parallel with lengths in ratio b:(1-b); affine maps keep it
px, xval = minpoly_of(y/(1 - y))
print(f"  x = b/(1-b) = {mp.nstr(xval, 25)}; minimal polynomial {px.as_expr()}")
C("x = b/(1-b) has degree 6 (so mu_f is not rational and no member of chamber I with rational x)", px.degree() == 6)
print("  x is the parameter of #48 Theorem 4 (DICTONIC golden bond): T(x) = hull perms(±(1+x), ±x, 0) = (1+x)·S(1 + x/(1+x)); Kelvin x = 1, Icosaxes x = tau.")
C("Kelvin control: x = 1 (rational)", abs(0.5/(1 - 0.5) - 1) < 1e-15)
C("x_f is not 1 (Kelvin) and not tau (Icosaxes)", px != sp.Poly(z - 1, z) and px != sp.Poly(z**2 - z - 1, z))
print("  Catalogue: not uniform (Archimedean) and not Johnson (faces not regular); not Catalan (2 face orbits); not a zonohedron (the")
print("  hexagons are not centrally symmetric: opposite edges b vs 1-b); a parallelohedron needs centrally symmetric faces, so it is not one.")
R['x_f'] = mp.nstr(xval, 30); R['minpoly_x'] = str(px.as_expr())

print("\nSTEP 4. Station check: mu_f against every named point of the line (exact minimal polynomials)")
mu = sp.Symbol('mu')
stations = [
    ("wall: octahedron", mu - 1), ("wall: cuboctahedron", mu - 2), ("wall: cube", mu - 3),
    ("Kelvin TO, swap fixed point, midsphere", 2*mu - 3), ("Icosaxes tau (Q4 = Q8 = 0, #94)", mu**2 - mu - 1),
    ("turn fixed point sqrt3 (insphere, Lindelof IQ max)", mu**2 - 3),
    ("Q6 zero in chamber I: b^4-(17/2)b^2+1", sp.expand(2*(mu - 1)**4 - 17*(mu - 1)**2 + 2)),
    ("Q8 zero (sqrt13-1)/2", mu**2 + mu - 3),
    ("Mahler global max 2mu^3-9mu+6", 2*mu**3 - 9*mu + 6),
    ("Mahler second local max 2mu^3-9mu^2+21", 2*mu**3 - 9*mu**2 + 21),
    ("canonical order-4 anisotropy zero mu^4+2mu^3+mu^2-4mu-14", mu**4 + 2*mu**3 + mu**2 - 4*mu - 14),
]
pm = sp.Poly(pmu.as_expr().subs(z, mu), mu)
for name, p in stations:
    g = sp.gcd(pm, sp.Poly(p, mu))
    C(f"mu_f is not the station '{name}' (gcd of minimal polynomials = 1)", g.degree() == 0)
R['stations_checked'] = [s for s, _ in stations]

print("\nSTEP 5. Turn and swap partners; Turn Law t_min (studies/2026-11-09-turn-theorem; c = h^2 R^2 = 3 for the cube, hops [1,2], [2,3])")
pturn, vturn = minpoly_of(3/(1 + y)); pswap, vswap = minpoly_of(2 - y)
print(f"  turn partner 3/mu_f = {mp.nstr(vturn, 15)} (minpoly {pturn.as_expr()}); swap partner 3 - mu_f = {mp.nstr(vswap, 15)}")
def pC_of(muv):
    bb = muv - 1; return 4*mp.atan(bb**2/(2*mp.sqrt(1 + bb**2)))/(4*mp.pi)
print(f"  p(square) at the turn partner {mp.nstr(pC_of(vturn), 10)}, at the swap partner {mp.nstr(pC_of(vswap), 10)} (fair = {mp.nstr(mp.mpf(1)/14, 10)})")
C("neither partner is fair (turn and swap do not fix fairness)", abs(pC_of(vturn) - mp.mpf(1)/14) > 1e-3 and abs(pC_of(vswap) - mp.mpf(1)/14) > 1e-3)
# both mu_f and 3/mu_f lie in hop [1,2]: h^2 t_min = 1 + (mu - 1)(3/mu - 1)
tmin = 1 + B_HP*(3/MU_HP - 1); tmax = 5 - 2*mp.sqrt(3)
ptm, _ = minpoly_of(1 + y*(3/(1 + y) - 1))
C("t_min(mu_f) < t_min(sqrt3) = 5 - 2 sqrt3 (the Turn Law maximum)", tmin < tmax, f"{mp.nstr(tmin, 12)} < {mp.nstr(tmax, 12)}")
C("Kelvin control: t_min(3/2) = 1 + (1/2)(1) = 3/2", abs((1 + 0.5*(3/1.5 - 1)) - 1.5) < 1e-15)
print(f"  t_min(mu_f) = {mp.nstr(tmin, 15)}, minimal polynomial {ptm.as_expr()}; gap to the maximum {mp.nstr(tmax - tmin, 6)}")
R.update({'turn_partner': mp.nstr(vturn, 20), 'swap_partner': mp.nstr(vswap, 20), 't_min': mp.nstr(tmin, 20), 'minpoly_turn_partner': str(pturn.as_expr())})
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
json.dump(R, open(os.path.join(os.path.dirname(__file__), '..', 'data', 's01-identity-stations.json'), 'w'), indent=1, default=str)
C.final()
