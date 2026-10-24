# Physical anchors, part A (exact, sympy): radius <-> weight, the loop maps rho(x), rho(t), the non-overlap windows, the stops,
# and the structure identification (CsCl B2, fluorite C1).
# Units: the app's (golden: cube edge L = phi; Delian: octet edge 1, i.e. krp-core units / sqrt2).
# Output: ../data/raw/symbolic.json, ../data/checks/symbolic-checks.txt
import json, time, itertools
import sympy as sp

checks, raw = [], {}
def check(name, ok, detail=""):
    ok = bool(ok); checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)
def zero(e): return sp.simplify(sp.radsimp(sp.expand(e))) == 0

T0 = time.time()
phi = (1 + sp.sqrt(5)) / 2

# ---------- A1: weight = squared radius, up to one common constant ----------
p = sp.Matrix(sp.symbols('p1:4', real=True)); ci = sp.Matrix(sp.symbols('a1:4', real=True)); cj = sp.Matrix(sp.symbols('b1:4', real=True))
ri, rj, C, wi, wj = sp.symbols('r_i r_j C w_i w_j', real=True)
pow_i = (p - ci).dot(p - ci) - ri**2; pow_j = (p - cj).dot(p - cj) - rj**2
# radical plane of two spheres  <=>  power-diagram bisector with w = r^2 + C (C common): identical linear equation
bis = ((p - ci).dot(p - ci) - (ri**2 + C)) - ((p - cj).dot(p - cj) - (rj**2 + C))
check("A1a radical plane (equal powers) = power bisector with w = r^2 + C, any common C", sp.expand(bis - (pow_i - pow_j)) == 0)
# the bisector is linear in p: 2 p.(cj - ci) = |cj|^2 - |ci|^2 + w_i - w_j ; so its offset fixes w_i - w_j and nothing else
lin = sp.expand(((p - ci).dot(p - ci) - wi) - ((p - cj).dot(p - cj) - wj))
quad = [sp.degree(lin, v) for v in p]
form = 2 * p.dot(cj - ci) + ci.dot(ci) - cj.dot(cj) - wi + wj
check("A1b bisector is the plane 2p.(cj-ci) = |cj|^2-|ci|^2 + w_i - w_j: depends on the weights only through w_i - w_j",
      quad == [1, 1, 1] and sp.expand(lin - form) == 0 and sp.expand(lin.subs({wi: wi + C, wj: wj + C}, simultaneous=True) - lin) == 0, str(quad))
# so on a connected adjacency graph all weights are fixed up to one common constant: w_i = r_i^2 + C. (Every cell here has
# positive volume except at the Delian ends t = 0, 1, where the vanishing kind's weight is only bounded, see Bond Relay B1.)
# A1c: touching spheres -> their radical plane is the common tangent plane, through the contact point, perpendicular to ci cj
D = sp.symbols('D', positive=True)
cA = sp.Matrix([0, 0, 0]); cB = sp.Matrix([D, 0, 0]); rA = sp.symbols('rA', positive=True); rB_ = D - rA
x_plane = sp.solve(sp.Eq((sp.Symbol('X'))**2 - rA**2, (sp.Symbol('X') - D)**2 - rB_**2), sp.Symbol('X'))[0]
check("A1c touching spheres: radical plane passes through the contact point (x = r_A)", sp.simplify(x_plane - rA) == 0, str(x_plane))
# ---------- A2: golden map ----------
x, s, rho, t, u = sp.symbols('x s rho t u', nonnegative=True)
aG = phi                      # cube edge (big-big = small-small nearest distance)
dG = sp.sqrt(3) / 2 * phi     # big-small nearest distance (half the body diagonal)
DeltaG = phi**2 / 4 * (x - 1) / (x + 1)       # w_big - w_small (Bond Relay)
# contact model: r_B + r_S = d, r_B^2 - r_S^2 = Delta  =>  r_B - r_S = Delta/d
rB = (dG + DeltaG / dG) / 2; rS = (dG - DeltaG / dG) / 2
rhoG = sp.simplify(rS / rB)
check("A2a golden contact map rho = r_small/r_big = (x + 2)/(2x + 1)", sp.simplify(rhoG - (x + 2) / (2 * x + 1)) == 0, str(rhoG))
check("A2b inverse x = (2 - rho)/(2 rho - 1); in s = x/(1+x): rho = (2 - s)/(1 + s)",
      sp.simplify(((2 - rho) / (2 * rho - 1) + 2) / (2 * (2 - rho) / (2 * rho - 1) + 1) - rho) == 0
      and sp.simplify(rhoG.subs(x, s / (1 - s)) - (2 - s) / (1 + s)) == 0)
check("A2c x -> 1/x sends rho -> 1/rho (big and small swap)", sp.simplify(rhoG.subs(x, 1 / x) * rhoG - 1) == 0)
check("A2d r_big/d = (1+s)/3, r_small/d = (2-s)/3 (fractions of the unlike bond)",
      sp.simplify((rB / dG).subs(x, s / (1 - s)) - (1 + s) / 3) == 0 and sp.simplify((rS / dG).subs(x, s / (1 - s)) - (2 - s) / 3) == 0)
# non-overlap window for the contact model: also 2 r_B <= a and 2 r_S <= a
xlo, xhi = (sp.sqrt(3) - 1) / 2, sp.sqrt(3) + 1
check("A2e like spheres touch (2 r_big = a) exactly at x = sqrt3 + 1, rho = sqrt3 - 1 (Pauling's 0.732)",
      zero((2 * rB - aG).subs(x, xhi)) and zero(rhoG.subs(x, xhi) - (sp.sqrt(3) - 1)))
check("A2f like spheres touch (2 r_small = a) exactly at x = (sqrt3 - 1)/2, rho = (sqrt3 + 1)/2",
      zero((2 * rS - aG).subs(x, xlo)) and zero(rhoG.subs(x, xlo) - (sp.sqrt(3) + 1) / 2))
# monotone: 2 r_B - a and 2 r_S - a are monotone in x, so the window is [xlo, xhi]
check("A2g d rho/dx = -3/(2x+1)^2 < 0 (rho strictly decreasing, 2 at x=0, 1/2 at x=inf)",
      sp.simplify(sp.diff(rhoG, x) + 3 / (2 * x + 1)**2) == 0 and rhoG.subs(x, 0) == 2 and sp.limit(rhoG, x, sp.oo) == sp.Rational(1, 2))
inside = sp.solve_univariate_inequality(sp.simplify((2 * rB - aG) * 4 / phi) <= 0, x, relational=False)
inside2 = sp.solve_univariate_inequality(sp.simplify((2 * rS - aG) * 4 / phi) <= 0, x, relational=False)
win = sp.Intersection(inside, inside2, sp.Interval(0, sp.oo))
check("A2h contact-model window (unlike touching, like not overlapping) is x in [(sqrt3-1)/2, sqrt3+1]",
      sp.simplify(win.inf - xlo) == 0 and sp.simplify(win.sup - xhi) == 0, str(win))

# ---------- A3: general non-overlap (not only touching): u = r_B + r_S ----------
def feasibility(Delta, d, like_big, like_small, name):
    """Delta = w_big - w_small; for Delta != 0, r_B = (u + Delta/u)/2, r_S = (u - Delta/u)/2, u = r_B + r_S.
    Both radii increase with u on u^2 >= |Delta|; rho = (u^2 - Delta)/(u^2 + Delta) moves monotonically toward 1.
    So the feasible set is u in [sqrt|Delta|, u_max] and is nonempty iff the larger radius sqrt|Delta| (smaller one 0)
    fits: sqrt|Delta| <= like/2 and sqrt|Delta| <= d."""
    U = sp.symbols('U', positive=True); De = sp.symbols('De', real=True)
    rb = (U + De / U) / 2; rs = (U - De / U) / 2
    ok1 = sp.simplify(sp.diff(rb, U) - (1 - De / U**2) / 2) == 0 and sp.simplify(sp.diff(rs, U) - (1 + De / U**2) / 2) == 0
    ok2 = sp.simplify(rs / rb - (U**2 - De) / (U**2 + De)) == 0
    check(f"A3 {name}: u-parametrisation (radii increase with u where both >= 0; rho = (u^2-Delta)/(u^2+Delta))", ok1 and ok2)
    return rb, rs

feasibility(DeltaG, dG, aG, aG, "golden")
check("A3g golden: |Delta| <= (a/2)^2 = phi^2/4 for all x in [0, inf] (equality only at x = 0, inf) => every x has a "
      "non-overlapping sphere packing (at the ends one kind is a point)",
      sp.simplify((phi**2 / 4)**2 - DeltaG**2 - (phi**4 / 16) * (1 - ((x - 1) / (x + 1))**2)) == 0
      and sp.simplify(1 - ((x - 1) / (x + 1))**2 - 4 * x / (x + 1)**2) == 0)
# max-contact (rho closest to 1) branches for the golden loop
rho_hi_branch = sp.sqrt(2 / (x + 1))           # x >= sqrt3+1: big spheres touch along the cube edge, small ones rattle
U = sp.symbols('U', positive=True)
rb_like = aG / 2; rs_like = sp.sqrt(rb_like**2 - DeltaG)
check("A3h golden x >= sqrt3+1: max rho = sqrt(2/(x+1)) (big-big contact); = contact map at x = sqrt3+1; -> 0 as x -> inf",
      sp.simplify((rs_like / rb_like)**2 - 2 / (x + 1)) == 0 and zero(rho_hi_branch.subs(x, xhi) - (sp.sqrt(3) - 1))
      and sp.limit(rho_hi_branch, x, sp.oo) == 0)
check("A3i golden x <= (sqrt3-1)/2: max-contact rho = sqrt((x+1)/(2x)) (small-small contact), by the x <-> 1/x swap",
      sp.simplify(1 / rho_hi_branch.subs(x, 1 / x) - sp.sqrt((x + 1) / (2 * x))) == 0)
check("A3j golden x = 1 forces rho = 1 (Delta = 0: equal spheres; any radius <= d/2 gives the Kelvin cell)", DeltaG.subs(x, 1) == 0)

# ---------- A4: Delian map ----------
aOO = sp.Integer(1); aQQ = 1 / sp.sqrt(2); dD = sp.sqrt(6) / 4     # O-O (octet edge), Q-Q (half cube edge), Q-O
DeltaD = sp.Rational(3, 8) * (2 * t - 1)                          # w_tet - w_oct (Bond Relay)
check("A4a Delian: unlike distance^2 d^2 = 3/8 (= |(1/2,1/2,1/2)|^2/2)", zero(dD**2 - sp.Rational(3, 8)))
rQ = (dD + DeltaD / dD) / 2; rO = (dD - DeltaD / dD) / 2
rhoD = sp.simplify(rQ / rO)
check("A4b Delian contact map rho = r_tet-site/r_oct-site = t/(1 - t); t = rho/(1+rho) = r_tet/d",
      sp.simplify(rhoD - t / (1 - t)) == 0 and sp.simplify(rQ / dD - t) == 0 and sp.simplify(rO / dD - (1 - t)) == 0, str(rhoD))
tlo, thi = 1 - sp.sqrt(sp.Rational(2, 3)), 1 / sp.sqrt(3)
check("A4c oct-site spheres touch (2 r_O = 1) exactly at t = 1 - sqrt(2/3); rho = sqrt(3/2) - 1 (Pauling's 0.225)",
      zero((2 * rO - aOO).subs(t, tlo)) and zero(rhoD.subs(t, tlo) - (sp.sqrt(sp.Rational(3, 2)) - 1)))
check("A4d tet-site spheres touch (2 r_Q = 1/sqrt2) exactly at t = 1/sqrt3; rho = (sqrt3+1)/2 = 1/0.732...",
      zero((2 * rQ - aQQ).subs(t, thi)) and zero(rhoD.subs(t, thi) - (sp.sqrt(3) + 1) / 2) and zero(1 / rhoD.subs(t, thi) - (sp.sqrt(3) - 1)))
winD = sp.Intersection(sp.solve_univariate_inequality(2 * rO - aOO <= 0, t, relational=False),
                       sp.solve_univariate_inequality(2 * rQ - aQQ <= 0, t, relational=False), sp.Interval(0, 1))
check("A4e Delian contact window t in [1 - sqrt(2/3), 1/sqrt3] (~[0.1835, 0.5774])",
      zero(winD.inf - tlo) and zero(winD.sup - thi), str(winD))
feasibility(DeltaD, dD, aQQ, aOO, "delian")
check("A4f Delian: a non-overlapping packing exists iff t in [1/6, 2/3]: -Delta <= (1/2)^2 <=> t >= 1/6; "
      "Delta <= (1/(2 sqrt2))^2 <=> t <= 2/3; |Delta| <= d^2 always",
      sp.solve(sp.Eq(-DeltaD, sp.Rational(1, 4)), t) == [sp.Rational(1, 6)] and sp.solve(sp.Eq(DeltaD, sp.Rational(1, 8)), t) == [sp.Rational(2, 3)]
      and sp.Abs(DeltaD).subs(t, 0) <= dD**2 and sp.Abs(DeltaD).subs(t, 1) <= dD**2)
check("A4g Delian max-contact branches: t in [1/6, 1-sqrt(2/3)]: rho = sqrt((6t-1)/2) (oct-oct contact); "
      "t in [1/sqrt3, 2/3]: rho = 1/sqrt(4 - 6t) (tet-tet contact); both meet the contact map at the window ends",
      sp.simplify((sp.sqrt(sp.Rational(1, 4) + DeltaD) / sp.Rational(1, 2))**2 - (6 * t - 1) / 2) == 0
      and sp.simplify((aQQ / 2)**2 / ((aQQ / 2)**2 - DeltaD) - 1 / (4 - 6 * t)) == 0
      and zero(sp.sqrt((6 * tlo - 1) / 2) - rhoD.subs(t, tlo)) and zero(1 / sp.sqrt(4 - 6 * thi) - rhoD.subs(t, thi)))

# ---------- A5: the stops ----------
stops = {}
for nm, xv in [("0", 0), ("1 (Kelvin)", 1), ("tau = phi", phi), ("1/tau", 1 / phi), ("inf", sp.oo)]:
    r = sp.limit(rhoG, x, xv) if xv == sp.oo else sp.nsimplify(sp.radsimp(sp.simplify(rhoG.subs(x, xv))))
    stops["golden x=" + nm] = dict(rho=str(r), rho_f=float(r), in_contact_window=bool(xlo <= xv <= xhi) if xv != sp.oo else False)
check("A5a golden stops: rho(0) = 2, rho(1) = 1, rho(tau) = sqrt5/phi^2 = (3 sqrt5 - 5)/2, rho(inf) = 1/2",
      rhoG.subs(x, 0) == 2 and rhoG.subs(x, 1) == 1 and zero(rhoG.subs(x, phi) - sp.sqrt(5) / phi**2)
      and zero(rhoG.subs(x, phi) - (3 * sp.sqrt(5) - 5) / 2) and sp.limit(rhoG, x, sp.oo) == sp.Rational(1, 2))
check("A5b golden: x = tau inside the contact window, x = 0 and inf outside (like spheres would overlap)",
      bool(xlo < phi < xhi) and not (xlo <= 0) and True)
tdel = 1 - sp.Rational(2, 3) * 2**sp.Rational(-1, 3)
for nm, tv in [("0", 0), ("1/6 (packing limit)", sp.Rational(1, 6)), ("octet 1/3", sp.Rational(1, 3)), ("Delian bond", tdel),
               ("1/2 (Voronoi)", sp.Rational(1, 2)), ("2/3 (packing limit)", sp.Rational(2, 3)), ("1", 1)]:
    r = sp.oo if tv == 1 else sp.radsimp(sp.simplify(rhoD.subs(t, tv)))
    stops["delian t=" + nm] = dict(t_f=float(tv), rho=str(r), rho_f=float(r) if r != sp.oo else None,
                                   in_contact_window=bool(tlo <= tv <= thi), packing_exists=bool(sp.Rational(1, 6) <= tv <= sp.Rational(2, 3)))
check("A5c Delian stops: rho(0) = 0, rho(1/3) = 1/2, rho(Delian bond) = (3/2) 2^(1/3) - 1, rho(1/2) = 1, rho -> inf at 1",
      rhoD.subs(t, 0) == 0 and rhoD.subs(t, sp.Rational(1, 3)) == sp.Rational(1, 2) and zero(rhoD.subs(t, tdel) - (sp.Rational(3, 2) * 2**sp.Rational(1, 3) - 1))
      and rhoD.subs(t, sp.Rational(1, 2)) == 1 and sp.limit(rhoD, t, 1, '-') == sp.oo)
check("A5d Delian: octet 1/3 and the Delian bond inside the contact window; t = 0, 1 outside and without any packing",
      bool(tlo < sp.Rational(1, 3) < thi) and bool(tlo < tdel < thi) and not (sp.Rational(1, 6) <= 0) and not (1 <= sp.Rational(2, 3)))
raw["stops"] = stops

# ---------- A6: the structures (exact, coset comparison) ----------
# Golden sites: B = phi Z^3, S = phi Z^3 + (phi/2)(1,1,1). CsCl (B2, Pm-3m): A at 1a (0,0,0), B at 1b (1/2,1/2,1/2), cube a.
# In fractions of a = phi: B -> Z^3, S -> Z^3 + (1/2,1/2,1/2): identical to B2 with a = phi.
check("A6a golden sites / phi = Z^3 and Z^3 + (1/2)(1,1,1): CsCl (B2) with a = phi (app) ; nearest unlike = sqrt3 a/2, like = a",
      zero(dG - sp.sqrt(3) * aG / 2) and aG == phi)
# Delian: O = {n in Z^3 : sum odd}/sqrt2, Q = (Z+1/2)^3/sqrt2. Shift by (1,0,0)/sqrt2 and use a = 2/sqrt2 = sqrt2:
# O' = {sum even} = fcc 4a: (0,0,0),(0,1/2,1/2),(1/2,0,1/2),(1/2,1/2,0) in units of a; Q' = (Z+1/2)^3 in units 2 -> 8c (1/4,1/4,1/4)+...
Ofrac = set(); Qfrac = set()
for n in itertools.product(range(-2, 4), repeat=3):
    if sum(n) % 2 == 1:
        m = (n[0] - 1, n[1], n[2]); Ofrac.add(tuple(sp.Rational(k, 2) % 1 for k in m))
    q = tuple(sp.Rational(2 * k + 1, 2) for k in n); m = (q[0] - 1, q[1], q[2]); Qfrac.add(tuple((k / 2) % 1 for k in m))
fcc4a = {(0, 0, 0), (0, sp.Rational(1, 2), sp.Rational(1, 2)), (sp.Rational(1, 2), 0, sp.Rational(1, 2)), (sp.Rational(1, 2), sp.Rational(1, 2), 0)}
f8c = {tuple(sp.Rational(k, 4) for k in v) for v in itertools.product((1, 3), repeat=3)}
check("A6b Delian oct sites = fluorite cation 4a (fcc), tet sites = fluorite anion 8c (all tetrahedral holes), a = sqrt2 (app)",
      Ofrac == fcc4a and Qfrac == f8c, f"{sorted(Ofrac)} | {len(Qfrac)} 8c")
# coordination by distance (exact): Q has 4 O at sqrt3 a/4, O has 8 Q at sqrt3 a/4; next O-O at a/sqrt2 (12), Q-Q at a/2 (6)
aF = sp.sqrt(2)
check("A6c fluorite distances in app units: M-X = sqrt3 a/4 = sqrt6/4 = d; M-M = a/sqrt2 = 1 (octet edge); X-X = a/2 = 1/sqrt2",
      zero(sp.sqrt(3) * aF / 4 - dD) and zero(aF / sp.sqrt(2) - 1) and zero(aF / 2 - aQQ))

# ---------- A7: Delian oct-tet face in the contact model, in real units (scale^2 = (8/3) u^2 with u = r_tet + r_oct) ----------
uu = sp.symbols('u', positive=True)
A_hi = sp.Rational(9, 16) * sp.sqrt(3) * (1 - t)**2 * sp.Rational(8, 3) * uu**2      # t >= 1/3
A_lo = sp.Rational(9, 4) * sp.sqrt(3) * t**2 * sp.Rational(8, 3) * uu**2             # t <= 1/3
check("A7 Delian contact model: oct-tet triangle area = (3 sqrt3/2) r_oct^2 for t >= 1/3 and 6 sqrt3 r_tet^2 for t <= 1/3 "
      "(r_oct = (1-t)u, r_tet = t u); the two agree at the octet (r_oct = 2 r_tet)",
      sp.simplify(A_hi - sp.Rational(3, 2) * sp.sqrt(3) * ((1 - t) * uu)**2) == 0 and sp.simplify(A_lo - 6 * sp.sqrt(3) * (t * uu)**2) == 0
      and sp.simplify((A_hi - A_lo).subs(t, sp.Rational(1, 3))) == 0)

raw["maps"] = {"golden_rho_of_x": str(rhoG), "golden_x_of_rho": "(2 - rho)/(2 rho - 1)", "golden_rho_of_s": "(2 - s)/(1 + s)",
               "golden_contact_window_x": [str(xlo), str(xhi)], "golden_contact_window_rho": ["sqrt(3) - 1", "(sqrt(3) + 1)/2"],
               "delian_rho_of_t": str(rhoD), "delian_t_of_rho": "rho/(1 + rho)", "delian_contact_window_t": [str(tlo), str(thi)],
               "delian_contact_window_rho": ["sqrt(3/2) - 1", "(sqrt(3) + 1)/2"], "delian_packing_exists_t": ["1/6", "2/3"]}
raw["seconds"] = round(time.time() - T0, 1)
json.dump(raw, open("../data/raw/symbolic.json", "w"), indent=1)
with open("../data/checks/symbolic-checks.txt", "w") as f:
    for c in checks: f.write("  ".join(c) + "\n")
    f.write(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL, {raw['seconds']} s\n")
print(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL, {raw['seconds']} s")
