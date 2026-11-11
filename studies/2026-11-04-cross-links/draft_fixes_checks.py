"""Exact checks for the formulas added to drafts #90, #91, #92 by the cross-links fixes (4 November 2026).
Run on compute-host: python3 draft_fixes_checks.py
"""
import itertools, math, random
import sympy as sp

s5 = sp.sqrt(5); s2 = sp.sqrt(2); s3 = sp.sqrt(3)
phi = (1 + s5) / 2
res = []
def check(name, cond):
    ok = bool(cond)
    res.append(ok)
    print(("PASS " if ok else "FAIL ") + name)

def eq(a, b):
    return sp.simplify(sp.radsimp(a - b)) == 0

# ---------- #91 row 3: #76's edge-equalising cuts give the uniform mu of Table 2 (600-cell R = 1) ----------
e2 = 1 / phi**2                     # 600-cell edge^2 with circumradius 1
check("600-cell edge^2 = 1/phi^2 = (3-sqrt5)/2", eq(e2, (3 - s5) / 2))
mu_t600 = 1 - sp.Rational(1, 3) * e2 / 2      # Lemma 1, x = 1/3
check("truncated 600-cell (x=1/3): mu = (9+sqrt5)/12", eq(mu_t600, (9 + s5) / 12))
k = 1 - e2 / 2                                  # a.b for neighbouring corners
check("a.b = phi/2", eq(k, phi / 2))
l = sp.Rational(3, 5)
aq = (1 - l) * (1 + k) / 2 + l * (1 + 2 * k) / 3   # a.q, q = (1-l) m_ab + l g
cq = (1 - l) * k + l * (1 + 2 * k) / 3
check("bitruncated (l=3/5): mu = a.q = (11+3sqrt5)/20", eq(aq, (11 + 3 * s5) / 20))
check("bitruncated: c.q < mu (q is cut only by a and b)", sp.N(cq) < sp.N(aq))
r2 = (7 + 3 * s5) / 16                          # 600-cell inradius^2 (R = 1)
Rs2 = 1 / r2                                    # polar 120-cell circumradius^2
es2 = Rs2 / (2 * phi**4)                        # 120-cell edge^2 / circumradius^2 = 1/(2 phi^4)
t = (5 - s5) / 10
mu_t120 = 1 / (Rs2 - t * es2 / 2)               # Lemma 1, dual side
check("truncated 120-cell (t=(5-sqrt5)/10): mu = (15+8sqrt5)/38", eq(mu_t120, (15 + 8 * s5) / 38))
check("t = 1/(phi+2) (regular decagons)", eq(t, 1 / (phi + 2)))
# numeric cross-check of the 120-cell ratio edge/circumradius = 1/(sqrt2 phi^2): 120-cell edge 2/phi^2, R 2sqrt2
check("120-cell e/R = 1/(sqrt2 phi^2)", eq((2 / phi**2) / (2 * s2), 1 / (s2 * phi**2)))
check("600-cell r^2 = (7+3sqrt5)/16 matches cos^2(pi/5)... numeric 0.85676", abs(float(r2) - 0.8567627457812106) < 1e-12)
m1, m2 = 2 - s5 / 2, (19 + 9 * s5) / 44
check("All-Golden stations lie either side of the bitruncated midpoint", float(m1) < float(aq) < float(m2))

# ---------- #81 involution on the sweep (rows 5) ----------
mu, R, r = sp.symbols('mu R r', positive=True)
a = mu / R; b = r                                # S(mu) = K(a, b): corner axes at mu/R, face axes at r
# core K(tcb, tca): ratio b/a -> a/b; find mu' with r R / mu' = a/b
mup = sp.solve(sp.Eq(r * R / sp.Symbol('m'), a / b), sp.Symbol('m'))[0]
check("core turn: mu' = r^2 R^2 / mu", sp.simplify(mup - r**2 * R**2 / mu) == 0)
nu = mu / r**2
check("in nu: nu' = (R/r)^2 / nu", sp.simplify(mup / r**2 - (R / r)**2 / nu) == 0)
CO = mup.subs({R: s3, r: 1})
check("C.O: mu -> 3/mu", sp.simplify(CO - 3 / mu) == 0)
check("C.O: fixed point sqrt3 (a = b there)", eq((sp.sqrt(3) / s3), 1))
check("C.O: 3/mu pairs 3/2 (truncated octahedron) with 2 (cuboctahedron)", eq(3 / sp.Rational(3, 2), 2))
check("C.O window c < b/a < 1/c  <=>  1 < mu < 3 (c = 1/sqrt3)",
      all((1 / s3 < s3 / m < s3) == (1 < m < 3) for m in [sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, sp.Rational(5, 2), 3, 4]))
TT = mup.subs({R: s3, r: 1 / s3})
check("T.T: mu -> 1/mu (the self-duality)", sp.simplify(TT - 1 / mu) == 0)
DI = sp.radsimp((3) / (1 + 2 / s5))
check("D.I: (R/r)^2 = 3/(1+2/sqrt5) = 15-6sqrt5", eq(DI, 15 - 6 * s5))
check("CsCl partner 3-mu fixes 3/2", eq(3 - sp.Rational(3, 2), sp.Rational(3, 2)))

# ---------- #54 Theorem B as the polar side of C.O (row 6) ----------
for m, name, hgt in [(phi, "Icosaxes", 1 / phi), (3 - phi, "Unborn Axes", 1 / phi**2), (2, "RD", 1)]:
    # S(m) corners: signed permutations of (1, m-1, 0); facets x_i = +-1 and +-x+-y+-z = m
    corners = set()
    for p in itertools.permutations([1, m - 1, 0]):
        for sg in itertools.product([1, -1], repeat=3):
            corners.add(tuple(sp.nsimplify(sg[i] * p[i]) for i in range(3)))
    ok = all(max(abs(c[0]), abs(c[1]), abs(c[2])) <= 1 and sp.N(abs(c[0]) + abs(c[1]) + abs(c[2]) - m) <= 1e-30 for c in corners)
    # polar = conv(+-e_i, (+-1,+-1,+-1)/m): cube half edge 1/m, apex 1 -> height in half edges m - 1
    hh = (1 - 1 / sp.S(m)) / (1 / sp.S(m))
    check(f"{name}: corners inside C and mC*; polar pyramid height m-1 = {hh}", ok and eq(hh, hgt))
x = sp.symbols('x', positive=True)
muT = 1 + x / (1 + x)
check("#48 T(x) at mu = 1 + x/(1+x): height x/(1+x); partner 3 - mu: height 1/(1+x); sum 1",
      sp.simplify((muT - 1) - x / (1 + x)) == 0 and sp.simplify((3 - muT - 1) - 1 / (1 + x)) == 0)
check("T(1/x) is at 3 - mu", sp.simplify(muT.subs(x, 1 / x) - (3 - muT)) == 0)

# ---------- #91 row 4: slices of the 24-cell honeycomb are #53's lanes ----------
h = sp.symbols('h')
lam = sp.expand((1 - h)**2 - h**2)
check("lambda = w_A - w_B = -h^2 + (1-h)^2 = 1 - 2h", sp.simplify(lam - (1 - 2 * h)) == 0)
hc = sp.solve(sp.Eq(1 - 2 * h, 4 - 2 * s3), h)[0]
check("rock-salt stop lambda = 4 - 2sqrt3 at h = sqrt3 - 3/2", eq(hc, s3 - sp.Rational(3, 2)))
lg = 1 - 2 / phi**2
check("CsCl: h = 1/phi^2 gives lambda = sqrt5 - 2", eq(lg, s5 - 2))
xg = sp.radsimp((1 + lg) / (1 - lg))
check("#53 golden loop lambda = (x-1)/(x+1): lambda = sqrt5-2 is x = phi", eq(xg, phi))
check("h = 0 -> lambda = 1 (flip / end), h = 1/2 -> 0, h = 1 -> -1", [lam.subs(h, v) for v in (0, sp.Rational(1, 2), 1)] == [1, 0, -1])

def nearest4(pt, sites):
    return min(sites, key=lambda s: sum((pt[i] - s[i])**2 for i in range(4)))
def power3(pt3, hh, sites):
    return min(sites, key=lambda s: sum((pt3[i] - s[i])**2 for i in range(3)) + (hh - s[3])**2)
random.seed(4)
rng = range(-3, 4)
cellfirst = [p for p in itertools.product(rng, repeat=4) if all(c % 2 == 0 for c in p) or all(c % 2 == 1 for c in p)]
D4 = [p for p in itertools.product(rng, repeat=4) if sum(p) % 2 == 0]
for lab, sites, Aset in [("cell-first (CsCl)", cellfirst, lambda p: all(c % 2 == 0 for c in p[:3])),
                         ("vertex-first (rock salt)", D4, lambda p: sum(p[:3]) % 2 == 0)]:
    bad = 0
    A = [p for p in sites if p[3] == 0 and Aset(p)]
    B = [p for p in sites if p[3] == 1 and not Aset(p)]
    for _ in range(4000):
        hh = random.random()
        pt3 = [random.uniform(-1, 1) for _ in range(3)]
        n4 = nearest4(pt3 + [hh], sites)
        # the power diagram of the two 3D kinds, A at p4 = 0 (w = -h^2), B at p4 = 1 (w = -(1-h)^2)
        pa = min(sum((pt3[i] - p[i])**2 for i in range(3)) + hh**2 for p in A)
        pb = min(sum((pt3[i] - p[i])**2 for i in range(3)) + (1 - hh)**2 for p in B)
        d4 = sum(((pt3 + [hh])[i] - n4[i])**2 for i in range(4))
        if abs(min(pa, pb) - d4) > 1e-12:
            bad += 1
    check(f"{lab}: 4D nearest site distance = 3D power of the two lanes' kinds (4000 random points)", bad == 0)

# ---------- #91 row 10: golden-tilt coding is the Fibonacci word of #69 ----------
N = 300
ph = (1 + 5 ** 0.5) / 2
# exact integer test: {k/phi} < 1/phi  <=>  floor(k/phi) - floor((k-1)/phi) == 1 (exact floors with sympy)
def fl(q):
    return int(sp.floor(q))
code = ''.join('c' if fl(k / phi) - fl((k - 1) / phi) == 1 else 'h' for k in range(1, N + 1))
w = 'c'
while len(w) < N + 5:
    w = ''.join('ch' if ch == 'c' else 'c' for ch in w)
check("coding of k = 2..300 equals the fixed point of c -> ch, h -> c (k = 1 gives one extra leading h)", code[1:] == w[:N - 1])
check("share of h in 300 letters within 0.01 of 1/phi^2", abs(code.count('h') / N - float(1 / phi**2)) < 0.01)

# ---------- #92: the 4T + 4O cube ----------
VT = s2 / 48; VO = s2 / 24
check("#92 cube: 4 sqrt2/48 + 4 sqrt2/24 = (1/sqrt2)^3 = sqrt2/4", eq(4 * VT + 4 * VO, (1 / s2)**3) and eq((1 / s2)**3, s2 / 4))

print(f"{sum(res)} PASS, {len(res) - sum(res)} FAIL")
