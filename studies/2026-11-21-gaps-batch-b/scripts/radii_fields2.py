# Item 3, exact elimination (radii_fields.py finds the farthest corners; here the field of R^2).
# On all three dice (and the O ∩ D control) the farthest corners lie on three B planes only, so R = mu_f * rho with
# rho^2 = kappa in Q(sqrt5) (the corner of the B solid with face distance 1). With Corollary 7,
#   mu_f = ba + bu t,  t^2 = T = tan^2(pi/m) (1 - c)/(1 + c) - 1,  c = cos(2 theta),
# and on these lines ba^2, bu^2, ba*bu, tan^2(pi/m) all lie in Q(sqrt5) (checked exactly). So
#   y = R^2 = P + Q t,  P = kappa (ba^2 + bu^2 T),  Q = 2 kappa ba bu,
# y is a root of g(Y) = (Y - P)^2 - Q^2 T over Q(sqrt5, c), and of R(Y) = Res_s(Res_c(g, minpoly c), s^2 - 5) over Q.
# The minimal polynomial of y is the one irreducible factor of R that vanishes at y (distinct irreducible factors have no
# common root; identified at 120 digits with a wide gap). Then: degree, real roots (exact count), discriminant primes,
# and a Galois test: for every root beta, PSLQ looks for beta = h(alpha) of degree < n, and each found h is checked
# exactly by f(h(x)) = 0 mod f(x). Usage: radii_fields2.py td|dt|it|od
import sys, os, json, itertools
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
mode = sys.argv[1]
mp.mp.dps = 150
checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


s5 = sp.sqrt(5); s3 = sp.sqrt(3)
phi = (1 + s5) / 2
Y, S, C = sp.symbols("Y s c")
# the farthest triple of B planes found by radii_fields.py (indices into B), as exact unnormalised normals
def ico_vertices():
    V = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [(0, s1 * phi, s2), (s2, 0, s1 * phi), (s1 * phi, s2, 0)]
    return V


AX = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def rt_normals():
    V = list(AX)
    for a, b, c in itertools.product((1, -1), repeat=3):
        V += [(a, b * phi, c / phi), (c / phi, a, b * phi), (b * phi, c / phi, a)]
    return V


LINES = {
    "td": dict(B=ico_vertices(), nA=4, tri=(4, 5, 8), m=3, N=16, ba=sp.sqrt((5 + 2 * s5) / 15), bu=sp.sqrt((5 - s5) / 30)),
    "dt": dict(B=rt_normals(), nA=12, tri=(12, 20, 23), m=5, N=42, ba=sp.sqrt((5 + s5) / 10), bu=sp.sqrt((5 + s5) / 10) / 2),
    "it": dict(B=rt_normals(), nA=20, tri=(20, 26, 28), m=3, N=50, ba=(s3 + sp.sqrt(15)) / 6, bu=(sp.sqrt(15) - s3) / 12),
    "od": dict(B=ico_vertices(), nA=8, tri=(8, 9, 12), m=3, N=20, ba=sp.sqrt((5 + 2 * s5) / 15), bu=sp.sqrt((5 - s5) / 30)),
}
L = LINES[mode]
m, N = L["m"], L["N"]
theta = sp.pi / 2 - (N - 2) * sp.pi / (m * N)
cval = sp.cos(2 * theta)
mc = sp.minimal_polynomial(cval, C)
print(f"{mode}: theta = {theta}, c = cos({2 * theta}) of degree {sp.degree(mc, C)}", flush=True)


def inQ5(e, what):
    """Exact a + b sqrt5 for an expression known to lie in Q(sqrt5); checked by exact simplification."""
    e2 = sp.nsimplify(sp.N(e, 120), [s5])
    a, b = sp.Rational(e2.subs(s5, 0)), sp.Rational(sp.expand(e2 - e2.subs(s5, 0)) / s5)
    ok = sp.simplify(sp.radsimp(sp.sqrtdenest(e)) - (a + b * s5)) == 0 or sp.minimal_polynomial(e - (a + b * s5), Y) == Y
    check(f"{mode}: {what} = {a} + ({b})√5 exactly", ok)
    return a + b * S


ba2 = inQ5(L["ba"] ** 2, "ba^2"); bu2 = inQ5(L["bu"] ** 2, "bu^2"); babu = inQ5(L["ba"] * L["bu"], "ba*bu")
tm2 = inQ5(sp.tan(sp.pi / m) ** 2, "tan^2(pi/m)")
# kappa from the three B planes at distance 1 (unit normals)
B = L["B"]
if L["tri"] is None:
    # O ∩ D control: find the farthest triple numerically among the B planes (all B), as in radii_fields.py
    L["tri"] = None
tri = L["tri"]
if tri is None:
    import numpy as np
    raise SystemExit("od: run radii_fields.py od for the triple")
rows = [B[k - L["nA"]] for k in tri]
Mx = sp.Matrix([[sp.nsimplify(x) for x in r] for r in rows])
d = sp.Matrix([sp.sqrt(sum(sp.nsimplify(x) ** 2 for x in r)) for r in rows])
xv = Mx.LUsolve(d)
kappa = inQ5(sum(sp.radsimp(z) ** 2 for z in xv), "kappa = rho^2 (B-solid corner at face distance 1)")
T = tm2 * (1 - C) / (1 + C) - 1
P = kappa * (ba2 + bu2 * T); Q = 2 * kappa * babu
g = sp.together((Y - P) ** 2 - Q ** 2 * T)
g = sp.expand(sp.numer(g))
# numeric y, from the closed form
tnum = sp.sqrt(sp.tan(sp.pi / m) ** 2 * (1 - cval) / (1 + cval) - 1)
mu = L["ba"] + L["bu"] * tnum
ynum = mp.mpf(str(sp.N(sp.N(kappa.subs(S, s5), 160) * sp.N(mu, 160) ** 2, 150)))
print(f"  kappa = {kappa}, R^2 = {mp.nstr(ynum, 40)}", flush=True)
REF = {"td": "1.780578767490521713029785733501241702811", "dt": "1.162616082432337391906887210533841387303",
       "it": "1.42537560591380050487035295757248559552", "od": "1.66873708001009457235966390089874069885"}
check(f"{mode}: R^2 = kappa mu_f^2 agrees with the corner search (radii_fields.py) to 1e-38",
      abs(ynum - mp.mpf(REF[mode])) < mp.mpf(10) ** -38)
R1 = sp.resultant(g, mc, C)
R2 = sp.resultant(sp.expand(R1), S ** 2 - 5, S)
R2 = sp.Poly(R2, Y)
print(f"  eliminant degree {R2.degree()}", flush=True)
facs = sp.factor_list(R2)[1]
vals = []
for f, e in facs:
    fp = sp.Poly(f, Y)
    v = mp.polyval([mp.mpf(int(cf)) for cf in sp.Poly(fp * sp.lcm([sp.Rational(cf).q for cf in fp.all_coeffs()]), Y).all_coeffs()], ynum)
    vals.append((abs(v) / max(1, max(abs(int(cf)) for cf in sp.Poly(fp * sp.lcm([sp.Rational(cf).q for cf in fp.all_coeffs()]), Y).all_coeffs())), fp))
zero = [fp for v, fp in vals if v < mp.mpf(10) ** -100]
other = min([v for v, fp in vals if v >= mp.mpf(10) ** -100], default=mp.mpf(1))
check(f"{mode}: exactly one irreducible factor of the eliminant vanishes at R^2 (gap: others >= {mp.nstr(other, 3)})",
      len(zero) == 1 and other > mp.mpf(10) ** -20)
f = sp.Poly(sp.monic(zero[0].as_expr(), Y), Y)
f = sp.Poly(f.as_expr() * sp.lcm([sp.Rational(cf).q for cf in f.all_coeffs()]), Y)
n = f.degree()
check(f"{mode}: minimal polynomial irreducible over Q", f.is_irreducible)
nreal = f.count_roots()
print(f"  {mode}: minimal polynomial of (R/r)^2, degree {n}, real roots {nreal}:\n  {f.as_expr()}", flush=True)
disc = sp.discriminant(f)
dpr = sorted(sp.factorint(abs(disc), limit=10 ** 6).keys())
print(f"  discriminant primes (trial division to 1e6): {dpr}", flush=True)
res = dict(mode=mode, N=N, m=m, theta=str(theta), kappa=str(kappa), R2=mp.nstr(ynum, 60), eliminant_degree=R2.degree(),
           minpoly=str(f.as_expr()), degree=n, real_roots=int(nreal), discriminant_primes=dpr)
# Galois test
if nreal < n:
    res["galois"] = "no (mixed signature)"
    print(f"  {mode}: not Galois (both real and non-real conjugates): in no field of a regular polygon", flush=True)
else:
    roots = [mp.mpf(str(r)) for r in sp.Poly(f, Y).nroots(n=140, maxsteps=500)]
    alpha = min(roots, key=lambda r: abs(r - ynum))
    check(f"{mode}: R^2 is one of the real roots", abs(alpha - ynum) < mp.mpf(10) ** -100)
    found = 0; exact_ok = True; hs = []
    for beta in roots:
        vec = [beta] + [alpha ** k for k in range(n)]
        rel = mp.pslq(vec, maxcoeff=10 ** 40, maxsteps=10 ** 6)
        if rel is None or rel[0] == 0: continue
        h = sum(sp.Rational(-rel[k + 1], rel[0]) * Y ** k for k in range(n))
        ok = sp.rem(sp.Poly(f.as_expr().subs(Y, h), Y), f).is_zero
        exact_ok &= ok; found += ok; hs.append(str(h))
    res["galois"] = "yes (all conjugates are polynomials in R^2, checked exactly)" if found == n else f"undecided: {found} of {n} conjugates found as polynomials in R^2"
    print(f"  {mode}: Galois test: {res['galois']}", flush=True)
    if found == n:
        # abelian? test commutativity of the automorphisms h_i o h_j = h_j o h_i mod f
        Hs = [sp.Poly(sp.sympify(h), Y) for h in hs]
        comm = all(sp.rem(sp.Poly(Hi.as_expr().subs(Y, Hj.as_expr()), Y) - sp.Poly(Hj.as_expr().subs(Y, Hi.as_expr()), Y), f).is_zero
                   for Hi, Hj in itertools.combinations(Hs, 2))
        res["abelian"] = comm
        print(f"  {mode}: Galois group abelian: {comm} (exact)", flush=True)
        check(f"{mode}: Galois group computed exactly", True)
if mode == "od":
    check("control O ∩ D: minimal polynomial x^2 - 218x + 361, i.e. (R/r)^2 = 109 - 48√5 (#111 Theorem 4A)",
          sp.expand(f.as_expr() - (Y ** 2 - 218 * Y + 361)) == 0)
json.dump(res, open(os.path.join(HERE, "..", "data", f"field-{mode}.json"), "w"), indent=1)
with open(os.path.join(HERE, "..", "data", f"field-{mode}-checks.txt"), "w") as fh:
    for s_, nm, det in checks: fh.write(f"{s_} {nm} {det}\n")
nf = sum(1 for c in checks if c[0] == "FAIL")
print(f"{len(checks) - nf}/{len(checks)} PASS")
print("FINAL ok" if checks and nf == 0 else f"FINAL FAIL: {nf} of {len(checks)} checks failed")
