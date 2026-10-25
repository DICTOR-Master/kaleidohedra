# Atom onions (2026-10-25), exact part. Question (DICTO): "do the atoms contain alternating shell arrangements?", "does up and
# down remove or add a shell?". Each DICTONIC loop is a power diagram of fixed sites with one weight slid between two kinds of site
# (study 2026-10-25-web-of-bonds = paper #52). A power cell grows when its site's weight grows, so each site's cells along a loop
# are nested shells: an onion. This script proves the nesting and names the shells at the stops.
#   N1 lemma (sympy, symbolic): every power-cell inequality of a site has a slack that moves with its weight only.
#   N2 the onion of each atom in closed form (sympy, symbolic): its nearest-neighbour bisectors are a fixed part plus one moving
#      part whose offset is monotone in the loop parameter; volumes strictly monotone; the two kinds' volumes add to a constant.
#   N3 the stops: exact order of the stop parameters; each stop shell inside the next (exact, sympy).
#   N4 from scratch (exact fields, lib.py of the web-of-bonds study): the power cell of each atom at every stop and at regime
#      interior points = the closed-form shell; the face table (neighbour kind x polygon size); the named-shape properties.
#   N5 the closed-form shells are the whole power cell on every regime: every corner against every site within D (slack affine in
#      the parameter on each regime, so the regime ends suffice) and the distance bound.
# Units: golden L/2 = 1 (app = x phi/2; big sites 2Z^3, small 2Z^3 + (1,1,1)); Delian krp-core tetPiece units (app = x 1/sqrt2).
# Output: ../data/raw/onions.json, ../data/checks/onions-checks.txt.
import os, sys, json, time
from fractions import Fraction as Fr
from itertools import product, permutations, combinations
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../2026-10-25-web-of-bonds/scripts"))
from lib import QQ, Q5, Q2, Q6, C2, C6, power_cell, cell_faces, enough_sites, vsub, vadd, dot  # noqa: E402
from samples import golden_sites, golden_T, delian_sites, tet_piece, oct_piece, golden_vol, delian_vols  # noqa: E402

checks, raw = [], {}
def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail)); print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)

x, t, s, u = sp.symbols("x t s u", nonnegative=True)
phi = (1 + sp.sqrt(5)) / 2
def iszero(e): return sp.simplify(e) == 0
def nonneg(e):
    e = sp.simplify(e)
    if e == 0: return True
    v = sp.N(e, 60); assert abs(v) > 1e-40, f"undecided {e}"
    return bool(v > 0)

# ================= N1 the lemma =================
# slack_j(p) = (|p - c_j|^2 - w_j) - (|p - c_i|^2 - w_i): the cell of i is {p : slack_j(p) >= 0 for all j}.
p = sp.Matrix(sp.symbols("p1:4")); ci = sp.Matrix(sp.symbols("a1:4")); cj = sp.Matrix(sp.symbols("b1:4"))
wi, wj, lam = sp.symbols("w_i w_j lambda")
slack = (p - cj).dot(p - cj) - wj - (p - ci).dot(p - ci) + wi
check("N1 d(slack_j)/d(w_i) = 1 and d(slack_j)/d(w_j) = -1, independent of p (raising w_i - w_j loosens every inequality)",
      sp.diff(slack, wi) == 1 and sp.diff(slack, wj) == -1)
# the loops: w_A - w_B = Delta(param), same-kind differences 0
dG = phi ** 2 / 4 * (x - 1) / (x + 1)                     # golden, app units: w_big - w_small
dD = sp.Rational(3, 8) * (2 * t - 1)                      # Delian, app units: w_tet - w_oct
ddG, ddD = sp.simplify(sp.diff(dG, x)), sp.diff(dD, t)
check("N1 golden dDelta/dx = phi^2/(2(1+x)^2) > 0: big atoms grow, small atoms shrink as x rises", iszero(ddG - phi ** 2 / (2 * (1 + x) ** 2)), str(ddG))
check("N1 Delian dDelta/dt = 3/4 > 0: tet atoms grow, oct atoms shrink as t rises", ddD == sp.Rational(3, 4))
check("N1 golden weight in L/2 units: Delta/(phi/2)^2 = 2s - 1, s = x/(1+x)", iszero(dG / (phi / 2) ** 2 - (2 * x / (1 + x) - 1)))
check("N1 Delian weight in tetPiece units: 2 Delta = (3/4)(2t - 1)", iszero(2 * dD - sp.Rational(3, 4) * (2 * t - 1)))

# ================= N2 closed-form onions =================
AX = [sp.Matrix(v) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
SIG = [sp.Matrix(v) for v in product((1, -1), repeat=3)]
def hrep(kind, prm):
    """Half-spaces n.p <= b about the atom's own site: (n, b, neighbour kind, moving?)."""
    if kind == "big":   return [(n, 1, "big", False) for n in AX] + [(g, 1 + prm, "small", True) for g in SIG]
    if kind == "small": return [(n, 1, "small", False) for n in AX] + [(g, 2 - prm, "big", True) for g in SIG]
    if kind == "tet":   # site q = (1/2,1/2,1/2) (cube k = 0); its 4 odd corners (oct sites)
        D = [sp.Matrix(o) - sp.Matrix([sp.Rational(1, 2)] * 3) for o in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]]
        return [(n, sp.Rational(1, 2), "tet", False) for n in AX] + [(d, sp.Rational(3, 4) * prm, "oct", True) for d in D]
    if kind == "oct":   # site c (odd point); 12 oct neighbours at (+-1,+-1,0), 8 tet neighbours at (+-1/2)^3
        N12 = [sp.Matrix(v) for v in set(permutations((1, 1, 0))) | set(permutations((1, -1, 0))) | set(permutations((-1, -1, 0)))]
        return [(n, 1, "oct", False) for n in N12] + [(g / 2, sp.Rational(3, 4) * (1 - prm), "tet", True) for g in SIG]

def bisector(dc, w_diff):  # site at 0, neighbour at dc, w_i - w_j = w_diff: |p|^2 - w_i <= |p - dc|^2 - w_j  <=>  dc.p <= (|dc|^2 + w_diff)/2
    return dc, (dc.dot(dc) + w_diff) / 2
okb = True
for kind, prm, Dw in [("big", s, 2 * s - 1), ("small", s, -(2 * s - 1)), ("tet", t, sp.Rational(3, 4) * (2 * t - 1)), ("oct", t, -sp.Rational(3, 4) * (2 * t - 1))]:
    for n, b, kk, mov in hrep(kind, prm):
        if kind in ("big", "small"): dc = 2 * n if kk == kind else n          # like neighbour across a square at 2e, unlike at (+-1)^3
        elif kind == "tet": dc = n if kk == "tet" else n                       # cube centre at q + e; odd corner at q + d
        else: dc = n                                                            # oct: neighbour at n (12) or at d = (+-1/2)^3
        wd = 0 if kk == kind else Dw
        m, bb = bisector(dc, wd)
        # same half-space: m = k n, bb = k b with k > 0
        k = (m.dot(n)) / n.dot(n)
        okb &= bool(k > 0) and all(iszero(m[i] - k * n[i]) for i in range(3)) and iszero(bb - k * b)
check("N2 every closed-form half-space is the power bisector of a nearest neighbour (identity in the parameter)", okb)
check("N2 moving offsets are monotone: big 1+s up, small 2-s down (s = x/(1+x) up in x), tet 3t/4 up, oct 3(1-t)/4 down; fixed parts constant",
      sp.diff(1 + s, s) > 0 and sp.diff(2 - s, s) < 0 and sp.diff(sp.Rational(3, 4) * t, t) > 0 and sp.diff(sp.Rational(3, 4) * (1 - t), t) < 0
      and iszero(sp.diff(x / (1 + x), x) - 1 / (1 + x) ** 2))
# volumes (golden in (L/2)^3, Delian in tetPiece units)
VG = sp.Rational(4, 3) * (1 + u) ** 3 - 4 * u ** 3
dVG = sp.expand(sp.diff(VG, u))
roots = sp.solve(dVG, u)
check("N2 golden volume (4/3)(1+u)^3 - 4u^3 strictly increasing on [0,1] (u = s big, 1-s small): dV/du = 4(1+2u-2u^2), roots (1 +- sqrt3)/2 outside [0,1]",
      iszero(dVG - 4 * (1 + 2 * u - 2 * u ** 2)) and all(not (0 <= sp.N(r) <= 1) for r in roots) and dVG.subs(u, 0) > 0)
check("N2 golden V_big + V_small = 8 = L^3 for all s (what one kind gains, the other loses)", sp.expand(VG.subs(u, s) + VG.subs(u, 1 - s)) == 8)
a = sp.Rational(3, 2) * (1 - t)
Vt = sp.Piecewise((9 * t ** 3, t <= sp.Rational(1, 3)), (1 - sp.Rational(2, 3) * a ** 3, True))
Vo = sp.Piecewise((2 - 18 * t ** 3, t <= sp.Rational(1, 3)), (sp.Rational(4, 3) * a ** 3, True))
check("N2 Delian volumes continuous at t = 1/3 (1/3 and 4/3)", 9 * sp.Rational(1, 27) == 1 - sp.Rational(2, 3) and 2 - 18 * sp.Rational(1, 27) == sp.Rational(4, 3))
check("N2 Delian 8 V_tet + 4 V_oct = 8 (cube of side 2) on both regimes", sp.expand(8 * 9 * t ** 3 + 4 * (2 - 18 * t ** 3)) == 8 and sp.expand(8 * (1 - sp.Rational(2, 3) * a ** 3) + 4 * sp.Rational(4, 3) * a ** 3) == 8)
check("N2 Delian volumes strictly monotone: V_tet' = 27t^2, 3a^2 > 0; V_oct' = -54t^2, -6a^2 < 0 (interior)",
      sp.diff(9 * t ** 3, t) == 27 * t ** 2 and sp.expand(sp.diff(1 - sp.Rational(2, 3) * a ** 3, t) - 3 * a ** 2) == 0 and sp.expand(sp.diff(sp.Rational(4, 3) * a ** 3, t) + 6 * a ** 2) == 0)
# ================= N3 stops =================
GST = [("x = 0", 0), ("x = 1/tau", 1 / phi ** 2), ("x = 1 (Kelvin)", sp.Rational(1, 2)), ("x = tau", 1 / phi), ("x = inf", 1)]   # values of s
DST = [("t = 0", 0), ("equilateral (a)", (2 * sp.sqrt(6) - 3) / 15), ("t = 1/3 (octet)", sp.Rational(1, 3)), ("half and half", 1 - sp.cbrt(6) / 3),
       ("Delian bond", 1 - sp.Rational(2, 3) * 2 ** sp.Rational(-1, 3)), ("equilateral (b)", sp.Rational(5, 3) - sp.Rational(2, 3) * sp.sqrt(2)), ("t = 1", 1)]
check("N3 golden stop s-values: x/(1+x) at x = 1/tau, 1, tau is 1/phi^2, 1/2, 1/phi", iszero((1 / phi) / (1 + 1 / phi) - 1 / phi ** 2) and iszero(phi / (1 + phi) - 1 / phi))
for name, ST in (("golden", GST), ("Delian", DST)):
    ok = all(sp.N(ST[i + 1][1] - ST[i][1], 50) > 1e-30 for i in range(len(ST) - 1))
    check(f"N3 {name} stops strictly increasing", ok, ", ".join(f"{n} {float(v):.6f}" for n, v in ST))
check("N3 Delian bond: 1 - (2/3) 2^(-1/3) = 1 - 2^(2/3)/3", iszero(DST[4][1] - (1 - 2 ** sp.Rational(2, 3) / 3)))

ROOT = {"Q": sp.Integer(0), "Q(sqrt5)": sp.sqrt(5), "Q(sqrt2)": sp.sqrt(2), "Q(sqrt6)": sp.sqrt(6), "Q(cbrt2)": sp.cbrt(2), "Q(cbrt6)": sp.cbrt(6)}
def tosym(e):
    r = ROOT[e.F.name]; return sum(sp.Rational(c.numerator, c.denominator) * r ** k for k, c in enumerate(e.c))
GF = {0: (QQ, QQ(0)), 1: (QQ, QQ(1)), "1/2": (QQ, QQ(Fr(1, 2))), "1/phi": (Q5, Q5(Fr(-1, 2), Fr(1, 2))), "1/phi2": (Q5, Q5(Fr(3, 2), Fr(-1, 2)))}
GKEYS = [0, "1/phi2", "1/2", "1/phi", 1]
DF = [(QQ, lambda F: F(0)), (Q6, lambda F: F(Fr(-1, 5), Fr(2, 15))), (QQ, lambda F: F(Fr(1, 3))), (C6, lambda F: F(1, Fr(-1, 3))),
      (C2, lambda F: F(1, 0, Fr(-1, 3))), (Q2, lambda F: F(Fr(5, 3), Fr(-2, 3))), (QQ, lambda F: F(1))]
for (n_, v), (F, f) in zip(DST, DF): assert iszero(tosym(f(F)) - v)
for (n_, v), k in zip(GST, GKEYS): assert iszero(tosym(GF[k][1]) - v)

def shell_pts(kind, i):
    """closed-form corners of the shell of `kind` at stop i (local coordinates about the site), exact field elements"""
    if kind in ("big", "small"):
        F, sv = GF[GKEYS[i]]; sv = sv if kind == "big" else F(1) - sv
        return F, golden_T(sv, F)
    F, f = DF[i]; tv = f(F)
    if kind == "tet":
        if tv.sign() == 0: return F, [tuple(F(Fr(1, 2)) for _ in range(3))]
        return F, tet_piece((0, 0, 0), tv, F)
    if (tv - 1).sign() == 0: return F, [tuple(F(c) for c in (1, 0, 0))]
    return F, oct_piece((1, 0, 0), tv, F)
SITE = {"big": (0, 0, 0), "small": (0, 0, 0), "tet": (Fr(1, 2),) * 3, "oct": (1, 0, 0)}
GROW = {"big": +1, "small": -1, "tet": +1, "oct": -1}  # direction of the loop parameter in which the atom grows

nest = {}
for kind in ("big", "small", "tet", "oct"):
    ST = GST if kind in ("big", "small") else DST
    order = list(range(len(ST))) if GROW[kind] > 0 else list(reversed(range(len(ST))))
    seq, allok = [], True
    for a_, b_ in zip(order, order[1:]):
        F, P = shell_pts(kind, a_)
        prm = ST[b_][1] if kind in ("big", "tet", "oct") else ST[b_][1]
        H = hrep(kind, prm)
        c = sp.Matrix([sp.nsimplify(z) for z in SITE[kind]])
        sl = [b - n.dot(sp.Matrix([tosym(z) for z in q]) - c) for q in P for n, b, *_ in H]
        ok = all(nonneg(e) for e in sl); strict = any(sp.N(e, 40) > 1e-30 for e in sl)
        allok &= ok and strict
        seq.append((ST[a_][0], ST[b_][0], ok, strict))
    nest[kind] = [ST[i][0] for i in order]
    check(f"N3 {kind} atom: every stop shell lies inside the next one outward (exact), and not on it", allok, " -> ".join(nest[kind]))

# ================= N4 from scratch at stops and regime interiors =================
def edges_of(fc):
    E = set()
    for poly, a2, n in fc.values():
        for k in range(len(poly)): E.add(frozenset((poly[k], poly[(k + 1) % len(poly)])))
    return [tuple(e) for e in E]
def d2(p_, q_): return dot(vsub(p_, q_), vsub(p_, q_))

GS = golden_sites(4); DS = delian_sites(3)
def cell_at(kind, F, prm):
    if kind in ("big", "small"):
        w = {"big": (prm * 2 - 1) * Fr(1, 2), "small": -(prm * 2 - 1) * Fr(1, 2)}; c = (Fr(0),) * 3 if kind == "big" else (Fr(1),) * 3
        sub = [z for z in GS if dot(vsub(z[1], c), vsub(z[1], c)) <= 16]; i = sub.index((kind, c)); D = 4
    else:
        w = {"tet": (prm * 2 - 1) * Fr(3, 4), "oct": F(0)}; c = (Fr(1, 2),) * 3 if kind == "tet" else (Fr(1), Fr(0), Fr(0))
        sub = [z for z in DS if dot(vsub(z[1], c), vsub(z[1], c)) <= 9]; i = sub.index((kind, c)); D = 3
    cell = power_cell(i, sub, w, F); fc, vol = cell_faces(cell, F)
    ok, rho = enough_sites(cell, sub, w, D)
    tab = {}
    for j, (poly, a2, n) in fc.items():
        key = f"{kind}-{sub[j][0]} {len(poly)}-gon"; tab[key] = tab.get(key, 0) + 1
    return cell, fc, vol, tab, ok, c

POLY = {3: "triangle", 4: "quadrilateral", 6: "hexagon"}
faces_raw = {}
GSAMP = [("x = 0", 0, QQ, QQ(0)), ("0 < x < 1/tau (x = 1/3)", None, QQ, QQ(Fr(1, 4))), ("x = 1/tau", 1, *GF["1/phi2"]), ("x = 1", 2, QQ, QQ(Fr(1, 2))),
         ("x = tau", 3, *GF["1/phi"]), ("tau < x < inf (x = 3)", None, QQ, QQ(Fr(3, 4))), ("x = inf", 4, QQ, QQ(1))]
DSAMP = [("t = 0", 0), ("0 < t < 1/3 (t = 1/6)", None), ("equilateral (a)", 1), ("t = 1/3", 2), ("half and half", 3), ("Delian bond", 4),
         ("1/3 < t < 1 (t = 2/3)", None), ("equilateral (b)", 5), ("t = 1", 6)]
named = {}
for kind in ("big", "small"):
    faces_raw[kind] = {}
    for lab, i, F, sv in GSAMP:
        cell, fc, vol, tab, okd, c = cell_at(kind, F, sv)
        want = golden_T(sv if kind == "big" else F(1) - sv, F); want = set(vadd(c, q) for q in want)
        same = set(cell["corners"]) == want
        check(f"N4 golden {kind} {lab}: power cell from scratch = closed-form shell T", same and okd, f"{len(want)} corners, faces {tab}")
        vv = golden_vol(sv, kind)
        check(f"N4 golden {kind} {lab}: volume = (4/3)(1+u)^3 - 4u^3", vol == vv, f"{float(vol):.6f}")
        faces_raw[kind][lab] = {"faces": tab, "corners": len(want), "volume_L2units": float(vol)}
        if i is None: continue
        E = edges_of(fc); L2 = set(d2(*e_) for e_ in E)
        nm = {}
        if kind == "big":
            if lab == "x = 0": nm["regular octahedron (6 corners, 8 triangles, 12 equal edges)"] = len(want) == 6 and tab == {"big-small 3-gon": 8} and len(E) == 12 and len(L2) == 1
            if lab == "x = 1": nm["Kelvin's truncated octahedron (24 corners, 8 hexagons + 6 squares, 36 equal edges)"] = len(want) == 24 and len(E) == 36 and len(L2) == 1 and tab == {"big-small 6-gon": 8, "big-big 4-gon": 6}
            if lab == "x = inf": nm["cuboctahedron (12 corners, 8 triangles + 6 squares, 24 equal edges)"] = len(want) == 12 and len(E) == 24 and len(L2) == 1 and tab == {"big-small 3-gon": 8, "big-big 4-gon": 6}
            if lab in ("x = tau", "x = 1/tau"):
                from scipy.spatial import ConvexHull
                # cyclic subset: signed cyclic permutations of (1, s, 0)
                s0 = sv
                cyc = set()
                for perm in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
                    base = (F(1), s0, F(0))
                    for sg in product((1, -1), repeat=3):
                        cyc.add(tuple(base[perm[k]] * sg[k] for k in range(3)))
                cyc = list(cyc)
                h = ConvexHull(np.array([[float(z) for z in q] for q in cyc]))
                HE = set()
                for tri in h.simplices:
                    for e_ in combinations(sorted(tri), 2): HE.add(e_)
                lens = {}
                for i1, i2 in HE:
                    l = d2(cyc[i1], cyc[i2]) * Fr(1, 1)
                    key = None
                    for k_ in lens:
                        if (k_ - l).iszero(): key = k_
                    lens[key if key is not None else l] = lens.get(key if key is not None else l, 0) + 1
                # app units: x (phi/2)^2 for squared lengths
                desc = {f"{float(k_) * float(sp.N(phi ** 2 / 4)):.6f}": v for k_, v in lens.items()}
                if lab == "x = tau":
                    nm["Icosaxes = T(tau) (paper #48 Theorem 4); its 12 corners (1, 1/phi, 0) cyclic span the regular icosahedron, edge 1 (20 triangles, 30 equal edges)"] = len(cyc) == 12 and len(h.simplices) == 20 and len(lens) == 1 and abs(float(list(lens)[0]) * float(sp.N(phi ** 2 / 4)) - 1) < 1e-12
                else:
                    nm["Unborn Axes = T(1/tau) (paper #48 Theorem 4; here at a big site, by the swap x <-> 1/x); its 12 corners (1, 1/phi^2, 0) cyclic span the Unborn: 24 edges 1, 6 edges 1/phi (#48)"] = len(cyc) == 12 and len(h.simplices) == 20 and sorted(lens.values()) == [6, 24] and \
                        all(abs(float(k_) * float(sp.N(phi ** 2 / 4)) - L_) < 1e-12 for k_, L_ in zip(sorted(lens, key=float), [float(sp.N(1 / phi ** 2)), 1.0]))
                nm["(edge lengths^2, app units: " + json.dumps(desc) + ")"] = True
        for k_, v in nm.items():
            check(f"N4 golden {kind} {lab}: {k_}", v)
        named.setdefault(kind, {})[lab] = list(nm)
for kind in ("tet", "oct"):
    faces_raw[kind] = {}
    for lab, i in DSAMP:
        if i is None:
            F = QQ; tv = QQ(Fr(1, 6)) if "1/6" in lab else QQ(Fr(2, 3))
        else:
            F, f = DF[i]; tv = f(F)
        cell, fc, vol, tab, okd, c = cell_at(kind, F, tv)
        point = (kind == "tet" and tv.sign() == 0) or (kind == "oct" and (tv - 1).sign() == 0)
        if point:
            ok = len(cell["corners"]) == 1 and vol.iszero() and list(cell["corners"])[0] == tuple(F(z) for z in c)
            check(f"N4 Delian {kind} {lab}: power cell from scratch is the single point at the site", ok)
            faces_raw[kind][lab] = {"faces": {}, "corners": 1, "volume": 0.0}; named.setdefault(kind, {})[lab] = ["point"]; continue
        want = set(tet_piece((0, 0, 0), tv, F) if kind == "tet" else oct_piece((1, 0, 0), tv, F))
        check(f"N4 Delian {kind} {lab}: power cell from scratch = closed-form shell (krp-core piece)", set(cell["corners"]) == want and okd, f"{len(want)} corners, faces {tab}")
        vt, vo = delian_vols(tv)
        check(f"N4 Delian {kind} {lab}: volume = #51 closed form", vol == (vt if kind == "tet" else vo), f"{float(vol):.6f}")
        faces_raw[kind][lab] = {"faces": tab, "corners": len(want), "volume": float(vol)}
        if i is None: continue
        E = edges_of(fc); L2 = set(d2(*e_) for e_ in E)
        other = cell_at("oct" if kind == "tet" else "tet", F, tv)
        L2o = set(d2(*e_) for e_ in edges_of(other[1])) if other[1] else set()
        nm = {}
        if lab == "t = 0": nm["Kepler's rhombic dodecahedron (14 corners, 12 rhombi)"] = len(want) == 14 and tab == {"oct-oct 4-gon": 12} and all(len(set(d2(poly[k], poly[(k + 1) % 4]) for k in range(4))) == 1 for poly, *_ in fc.values())
        if lab == "equilateral (a)":
            nm[{"tet": "regular tetrahedron", "oct": "rhombic dodecahedron with 8 cut corners"}[kind] + ": every edge of both pieces equal"] = len(L2 | L2o) == 1 and \
                (tab == {"tet-oct 3-gon": 4} if kind == "tet" else tab == {"oct-oct 6-gon": 12, "oct-tet 3-gon": 8})
        if lab == "t = 1/3":
            nm[{"tet": "octet tetrahedron (regular, edge sqrt2 = octet edge)", "oct": "octet octahedron (regular, edge sqrt2 = octet edge)"}[kind]] = all(l_ == 2 for l_ in L2) and \
                (len(want) == 4 and tab == {"tet-oct 3-gon": 4} if kind == "tet" else len(want) == 6 and tab == {"oct-tet 3-gon": 8})
        if lab == "half and half":
            nm["each kind fills half of space: 8 V_tet = 4 V_oct = 4 (cube of side 2)"] = (vol * (8 if kind == "tet" else 4)) == 4
        if lab == "Delian bond":
            if kind == "tet": nm["Samson (#51): the cut cube, volume 2/3 = twice the octet tetrahedron (1/3)"] = vol == Fr(2, 3) and tab == {"tet-oct 3-gon": 4, "tet-tet 6-gon": 6}
            else: nm["Delilah (#51): the octahedron, volume 2/3 = half the octet octahedron (4/3); the octet octahedron shrunk by 2^(-1/3)"] = vol == Fr(2, 3) and \
                    all(d2(q, tuple(F(z) for z in c)) == C2(0, Fr(1, 2)) for q in want)  # |q - c|^2 = 2^(-2/3) = 2^(1/3)/2
        if lab == "equilateral (b)":
            nm[{"tet": "cube with 4 cut corners", "oct": "regular octahedron"}[kind] + ": every edge of both pieces equal"] = len(L2 | L2o) == 1
        if lab == "t = 1": nm["cube (8 corners, 6 squares)"] = len(want) == 8 and tab == {"tet-tet 4-gon": 6}
        for k_, v in nm.items():
            check(f"N4 Delian {kind} {lab}: {k_}", v)
        named.setdefault(kind, {})[lab] = list(nm)
# Delilah corners: at a = 2^(-1/3) along the axes; |q - c|^2 = 2^(-2/3) = 2^(1/3)/2 (in Q(cbrt2): (0, 1/2, 0))
F, f = DF[4]; tv = f(F); aa = (F(1) - tv) * Fr(3, 2)
check("N4 Delian bond: a = 3(1-t)/2 = 2^(-1/3) exactly (a^3 = 1/2)", (aa * aa * aa - Fr(1, 2)).iszero(), str(aa))

# ================= N5 the closed-form shells are the whole power cell on every regime =================
def n5(kind, regimes):
    ok_all = True
    for lo, hi in regimes:
        for prm in (lo, hi):
            F = QQ; v = QQ(prm)
            if kind in ("big", "small"):
                c = (Fr(0),) * 3 if kind == "big" else (Fr(1),) * 3
                P = [vadd(c, q) for q in golden_T(v if kind == "big" else F(1) - v, F)]
                w = {"big": (v * 2 - 1) * Fr(1, 2), "small": -(v * 2 - 1) * Fr(1, 2)}; S = GS; D = 4
            else:
                c = (Fr(1, 2),) * 3 if kind == "tet" else (Fr(1), Fr(0), Fr(0))
                if (kind == "tet" and prm == 0) or (kind == "oct" and prm == 1): P = [tuple(F(z) for z in c)]
                else:
                    # the closed form of the regime [lo, hi] evaluated at its end (tet_piece/oct_piece switch at 1/3 by their own test)
                    P = tet_piece((0, 0, 0), v, F) if kind == "tet" else oct_piece((1, 0, 0), v, F)
                w = {"tet": (v * 2 - 1) * Fr(3, 4), "oct": F(0)}; S = DS; D = 3
            for kk, cc in S:
                if cc == tuple(c) and kk == kind: continue
                if dot(vsub(cc, c), vsub(cc, c)) > D * D: continue
                for q in P:
                    sl = (dot(vsub(q, cc), vsub(q, cc)) - w[kk]) - (dot(vsub(q, c), vsub(q, c)) - w[kind])
                    if sl.sign() < 0: ok_all = False
    return ok_all
check("N5 golden big: closed-form corners satisfy every power inequality (sites within D = 4) at s = 0 and 1; slack affine in s, so on all of [0, 1]", n5("big", [(0, 1)]))
check("N5 golden small: same", n5("small", [(0, 1)]))
check("N5 Delian tet: same on [0, 1/3] and [1/3, 1] (D = 3)", n5("tet", [(0, Fr(1, 3)), (Fr(1, 3), 1)]))
check("N5 Delian oct: same on [0, 1/3] and [1/3, 1] (D = 3)", n5("oct", [(0, Fr(1, 3)), (Fr(1, 3), 1)]))

raw = {"onions_inside_out": nest, "faces_by_regime": faces_raw, "named": named,
       "stops": {"golden_s": {n: str(v) for n, v in GST}, "delian_t": {n: str(v) for n, v in DST}}}
if __name__ == "__main__":
    T0 = time.time()
    os.makedirs(os.path.join(HERE, "../data/raw"), exist_ok=True); os.makedirs(os.path.join(HERE, "../data/checks"), exist_ok=True)
    json.dump(raw, open(os.path.join(HERE, "../data/raw/onions.json"), "w"), indent=1)
    with open(os.path.join(HERE, "../data/checks/onions-checks.txt"), "w") as f:
        for c in checks: f.write("  ".join(c) + "\n")
        f.write(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL\n")
    print(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL")
