# web of bonds, part A (exact, symbolic in the parameter, sympy): for every open regime
#   golden  s = x/(1+x) in (0, 1)          (x in (0, inf); x = 1 is s = 1/2)
#   delian  t in (0, 1/3) and t in (1/3, 1)
# prove, for ALL parameters of the regime at once:
#   A1 every app piece lies in its power cell (fixed sites, weights linear in the parameter): every corner satisfies every
#      bisector inequality of every site within D, with slack >= 0 on the whole open interval (slacks are linear: no root inside);
#   A2 the facets of the piece are bisectors (power cell inside the piece): the facet planes' own corners (symbolic vertex
#      enumeration, all triples) are corners of the piece, and the facet normals sum to 0 with rank 3 (bounded) => piece = power cell;
#   A3 the face of every bond, its corner count and its area in closed form (area^2 identities), per bond type;
#   A4 volumes in closed form, adding to the lattice cell; A5 faces pair up face to face (symbolic corner sets);
#   A6 monotonicity / births / deaths / the swap x <-> 1/x / equality at x = 1 / single-type parameters from the closed forms;
#   A7 the finite site list is enough for the whole regime (uniform distance bound).
# Units as in samples.py. Output: ../data/raw/symbolic.json, ../data/checks/symbolic-checks.txt.
import json, time
from itertools import combinations, product, permutations
import sympy as sp

checks, raw = [], {}
def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail)); print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)

s, t = sp.symbols("s t", real=True)
R = sp.Rational; half = R(1, 2)

def sign_on(expr, x, lo, hi):
    """Sign of a rational function of x on the open interval (lo, hi): 0 (identically), +1, -1, or None (changes sign inside)."""
    e = sp.cancel(sp.together(expr))
    num, den = sp.fraction(e)
    if sp.expand(num) == 0:
        return 0
    for f in (num, den):
        P = sp.Poly(f, x)
        if P.degree() > 0:
            try: roots = sp.real_roots(P)
            except Exception: roots = list(sp.solveset(f, x, sp.Interval.open(lo, hi)))
            if any(lo < r < hi for r in roots): return None
    v = e.subs(x, (lo + hi) / 2)
    return 1 if v > 0 else -1

def V(*a): return tuple(sp.nsimplify(c) if not isinstance(c, sp.Basic) else c for c in a)
def add(a, b): return tuple(sp.expand(x + y) for x, y in zip(a, b))
def sub(a, b): return tuple(sp.expand(x - y) for x, y in zip(a, b))
def dot(a, b): return sp.expand(a[0] * b[0] + a[1] * b[1] + a[2] * b[2])
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def eqv(a, b): return all(sp.expand(x - y) == 0 for x, y in zip(a, b))
def ptset(P): return {tuple(sp.expand(c) for c in p) for p in P}

def bisectors(c, kind, sites, w, D):
    """(site, n, b) with n.p <= b for every site within D (power cell of `kind` at c)."""
    out = []
    for kj, cj in sites:
        if cj == c: continue
        n = sub(cj, c)
        if dot(n, n) > D * D: continue
        out.append(((kj, cj), n, sp.expand((dot(cj, cj) - dot(c, c) + w[kind] - w[kj]) / 2)))
    return out

def analyse(label, x, lo, hi, kind, c, piece, sites, w, D, rho2max):
    """A1, A2, A7 for one piece; returns faces {neighbour: ordered corners} and the volume."""
    mid = (lo + hi) / 2
    P = list(ptset(piece))
    H = bisectors(c, kind, sites, w, D)
    bad, on = 0, {}
    for p in P:
        for nb, n, b in H:
            sg = sign_on(b - dot(n, p), x, lo, hi)
            if sg is None or sg < 0: bad += 1
            elif sg == 0: on.setdefault(nb, []).append(p)
    check(f"{label} {kind}@{c}: A1 piece inside its power cell for all {x} in ({lo}, {hi})", bad == 0, f"{len(P)} corners x {len(H)} sites")
    # facets: planes holding >= 3 corners that span a polygon
    facets = {}
    for nb, pts in on.items():
        if len(pts) < 3: continue
        A = (0, 0, 0)
        cen = [sum(q[i] for q in pts) / len(pts) for i in range(3)]
        nf = [float(sp.sympify(z).subs(x, mid)) for z in sub(nb[1], c)]
        import numpy as np
        Pf = np.array([[float(sp.sympify(z).subs(x, mid)) for z in q] for q in pts]); cf = Pf.mean(0)
        u = Pf[0] - cf; u /= np.linalg.norm(u); vv = np.cross(np.array(nf) / np.linalg.norm(nf), u)
        order = np.argsort(np.arctan2((Pf - cf) @ vv, (Pf - cf) @ u)); poly = [pts[k] for k in order]
        for k in range(len(poly)): A = add(A, cross(poly[k], poly[(k + 1) % len(poly)]))
        a2 = sp.factor(sp.expand(dot(A, A) / 4))
        if sign_on(a2, x, lo, hi) == 0: continue
        facets[nb] = (poly, a2, sub(nb[1], c))
    # A2: vertex enumeration of the facet planes alone
    Hf = [(nb, n, b) for nb, n, b in H if nb in facets]
    found = set()
    for (n1, b1), (n2, b2), (n3, b3) in combinations([(n, b) for _, n, b in Hf], 3):
        M = sp.Matrix([n1, n2, n3])
        if M.det() == 0: continue
        q = tuple(sp.expand(z) for z in M.inv() * sp.Matrix([b1, b2, b3]))
        if all((sg := sign_on(b - dot(n, q), x, lo, hi)) is not None and sg >= 0 for _, n, b in Hf):
            found.add(q)
    nsum = tuple(sum(n[i] for _, n, _ in Hf) for i in range(3))
    rank = sp.Matrix([list(n) for _, n, _ in Hf]).rank()
    check(f"{label} {kind}@{c}: A2 facets are bisectors, their corners = the piece's (piece = power cell)",
          found == set(P) and all(z == 0 for z in nsum) and rank == 3, f"{len(Hf)} facets, {len(found)} corners")
    r2 = max(sp.expand(dot(sub(p, c), sub(p, c))).subs(x, mid) for p in P)
    ok7 = all(sign_on(rho2max - dot(sub(p, c), sub(p, c)), x, lo, hi) in (0, 1) for p in P)
    check(f"{label} {kind}@{c}: A7 corners within rho^2 = {rho2max} of the centre (site list D = {D} enough)", ok7)
    vol = 0
    for nb, (poly, a2, n) in facets.items():
        for k in range(1, len(poly) - 1):
            vol += dot(poly[0], cross(poly[k], poly[k + 1])) / 6
    return facets, sp.factor(sp.expand(vol))

def regime(label, x, lo, hi, sites, w, reps, D, rho2max, forms, rep_of, vol_target, per_cell):
    t0 = time.time(); res = {}
    F = {}
    for r, (kind, c, piece) in reps.items():
        F[r] = analyse(label, x, lo, hi, kind, c, piece, sites, w, D, rho2max)
    out = {}
    for r, (kind, c, piece) in reps.items():
        facets, vol = F[r]; cnt = {}; ok = True; shapes = {}
        for nb, (poly, a2, n) in facets.items():
            typ = "-".join(sorted((kind, nb[0])))
            cnt[typ] = cnt.get(typ, 0) + 1
            if sp.simplify(a2 - forms[typ] ** 2) != 0: ok = False; print("area", r, typ, a2, forms[typ])
            shapes.setdefault(typ, set()).add(len(poly))
        check(f"{label} {r}: A3 bond areas = closed forms", ok, json.dumps({k: sorted(v) for k, v in shapes.items()}))
        out[r] = {"counts": cnt, "corners_per_face": {k: sorted(v) for k, v in shapes.items()}, "volume": str(vol)}
        # A5 face to face (symbolic): the neighbour's own piece is a translate of its representative
        okp = True
        for nb, (poly, a2, n) in facets.items():
            rj = rep_of(*nb); kj, cj0, _ = reps[rj]; shift = sub(nb[1], cj0)
            back = sub(c, shift); fj = F[rj][0].get((kind, back))
            if fj is None or ptset([add(p, shift) for p in fj[0]]) != ptset(poly): okp = False
        check(f"{label} {r}: A5 every face shared face to face", okp)
    tot = sp.factor(sum(sp.sympify(F[r][1]) * per_cell[r] for r in reps))
    check(f"{label}: A4 volumes add to the lattice cell ({vol_target})", sp.simplify(tot - vol_target) == 0, str({r: out[r]['volume'] for r in out}))
    out["seconds"] = round(time.time() - t0, 1)
    raw[label] = out
    print(label, json.dumps(out), flush=True)

# ---------------- Golden (units L/2) ----------------
def golden():
    D = 4; Rg = D + 2
    sites = [("big", tuple(sp.Integer(2 * a) for a in m)) for m in product(range(-Rg, Rg + 1), repeat=3)] + \
            [("small", tuple(sp.Integer(2 * a + 1) for a in m)) for m in product(range(-Rg, Rg + 1), repeat=3)]
    w = {"big": (2 * s - 1) / 2, "small": -(2 * s - 1) / 2}
    def T(u, c):
        pts = set()
        for p in set(permutations((sp.Integer(1), u, sp.Integer(0)))):
            for sg in product((1, -1), repeat=3): pts.add(tuple(sp.expand(ci + a * g) for a, g, ci in zip(p, sg, c)))
        return list(pts)
    reps = {"big": ("big", (0, 0, 0), T(s, (0, 0, 0))), "small": ("small", (1, 1, 1), T(1 - s, (1, 1, 1)))}
    reps = {k: (a, tuple(sp.Integer(z) for z in c), p) for k, (a, c, p) in reps.items()}
    forms = {"big-big": 2 * s ** 2, "small-small": 2 * (1 - s) ** 2, "big-small": sp.sqrt(3) / 2 * (1 + 2 * s - 2 * s ** 2)}
    regime("golden s in (0,1)", s, sp.Integer(0), sp.Integer(1), sites, w, reps, D, 2, forms, lambda k, c: k, 8, {"big": 1, "small": 1})
    return forms

# ---------------- Delian (tetPiece units) ----------------
def delian():
    D = 3; Rd = D + 2
    sites = [("tet", tuple(sp.Integer(a) + half for a in m)) for m in product(range(-Rd, Rd + 2), repeat=3)] + \
            [("oct", tuple(sp.Integer(a) for a in m)) for m in product(range(-Rd, Rd + 2), repeat=3) if sum(m) % 2 == 1]
    w = {"tet": R(3, 4) * (2 * t - 1), "oct": sp.Integer(0)}
    odd = lambda p: sum(p) % 2 == 1
    def tet(k, left):
        C = [tuple(sp.Integer(a + d) for a, d in zip(k, dd)) for dd in product((0, 1), repeat=3)]
        even = [p for p in C if not odd(p)]; octs = [p for p in C if odd(p)]; q = tuple(sp.Integer(a) + half for a in k)
        if left: return [add(q, tuple(3 * t * z for z in sub(v, q))) for v in even]
        a = R(3, 2) * (1 - t)
        return even + [add(o, tuple(a * z for z in sub(v, o))) for o in octs for v in even if dot(sub(v, o), sub(v, o)) == 1]
    def octp(c, left):
        AX = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        if not left:
            a = R(3, 2) * (1 - t); return [tuple(ci + g * a * e for ci, e in zip(c, ax)) for ax in AX for g in (1, -1)]
        out = [tuple(ci + g * e for ci, e in zip(c, ax)) for ax in AX for g in (1, -1)]
        for sg in product((-1, 1), repeat=3):
            q = tuple(ci + R(g, 2) for ci, g in zip(c, sg))
            for v in (add(c, (sg[0], 0, 0)), add(c, (0, sg[1], 0)), add(c, (0, 0, sg[2]))):
                out.append(add(q, tuple(3 * t * z for z in sub(v, q))))
        return out
    a = R(3, 2) * (1 - t)
    def rep_of(kind, c):
        if kind == "oct": return "oct"
        return "tet1" if sum(int(z - half) for z in c) % 2 else "tet0"
    out = {}
    for left, lo, hi in ((True, sp.Integer(0), R(1, 3)), (False, R(1, 3), sp.Integer(1))):
        reps = {"oct": ("oct", (sp.Integer(1), sp.Integer(0), sp.Integer(0)), octp((1, 0, 0), left)),
                "tet0": ("tet", (half, half, half), tet((0, 0, 0), left)),
                "tet1": ("tet", (R(3, 2), half, half), tet((1, 0, 0), left))}
        forms = {"oct-tet": (9 * sp.sqrt(3) / 2 * t ** 2) if left else (sp.sqrt(3) / 2 * a ** 2),
                 "oct-oct": sp.sqrt(2) / 2 * (1 - 9 * t ** 2), "tet-tet": 1 - a ** 2}
        regime(f"delian t in ({lo},{hi})", t, lo, hi, sites, w, reps, D, 1, forms, rep_of, 8, {"oct": 4, "tet0": 4, "tet1": 4})
        out[left] = forms
    return out

def closed_form_facts(G, Dl):
    x = sp.symbols("x", positive=True)
    # ---- golden, in x (s = x/(1+x)); app units: multiply areas by (L/2)^2 = phi^2/4
    phi = (1 + sp.sqrt(5)) / 2; k = phi ** 2 / 4
    A = {kk: sp.simplify(v.subs(s, x / (1 + x)) * k) for kk, v in G.items()}
    raw["golden areas (app units, x)"] = {kk: str(sp.factor(v)) for kk, v in A.items()}
    check("A6 golden: swap x <-> 1/x: big-big(1/x) = small-small(x), big-small(1/x) = big-small(x)",
          sp.simplify(A["big-big"].subs(x, 1 / x) - A["small-small"]) == 0 and sp.simplify(A["big-small"].subs(x, 1 / x) - A["big-small"]) == 0)
    check("A6 golden: big-big = small-small only at x = 1, value phi^2/8",
          set(sp.solve(sp.Eq(A["big-big"], A["small-small"]), x)) == {1} and sp.simplify(A["big-big"].subs(x, 1) - phi ** 2 / 8) == 0,
          f"phi^2/8 = {float(phi**2/8):.6f}")
    check("A6 golden at x = tau: big-big = 1/2, small-small = 1/(2 phi^2)",
          sp.simplify(A["big-big"].subs(x, phi) - R(1, 2)) == 0 and sp.simplify(A["small-small"].subs(x, phi) - 1 / (2 * phi ** 2)) == 0,
          f"{float(A['big-big'].subs(x, phi)):.6f}, {float(A['small-small'].subs(x, phi)):.6f}")
    d = {kk: sp.simplify(sp.diff(v, x)) for kk, v in A.items()}
    check("A6 golden: big-big strictly increasing, small-small strictly decreasing on (0, inf)",
          sign_on(d["big-big"], x, sp.Integer(0), sp.Integer(10 ** 9)) == 1 and sign_on(d["small-small"], x, sp.Integer(0), sp.Integer(10 ** 9)) == -1
          and sp.solve(d["big-big"], x) == [] and sp.solve(d["small-small"], x) == [])
    check("A6 golden: big-small rises on (0,1), falls on (1,inf), max (3 sqrt3/16) phi^2 at x = 1, -> (sqrt3/8) phi^2 at both ends, never 0",
          sign_on(d["big-small"], x, sp.Integer(0), sp.Integer(1)) == 1 and sign_on(d["big-small"], x, sp.Integer(1), sp.Integer(10 ** 9)) == -1
          and sp.simplify(A["big-small"].subs(x, 1) - 3 * sp.sqrt(3) / 16 * phi ** 2) == 0
          and sp.simplify(sp.limit(A["big-small"], x, 0) - sp.sqrt(3) / 8 * phi ** 2) == 0 and sp.simplify(sp.limit(A["big-small"], x, sp.oo) - sp.sqrt(3) / 8 * phi ** 2) == 0)
    check("A6 golden: big-big -> 0 as x -> 0 (born at 0+), small-small -> 0 as x -> inf; both > 0 on (0, inf)",
          sp.limit(A["big-big"], x, 0) == 0 and sp.limit(A["small-small"], x, sp.oo) == 0 and sp.simplify(sp.limit(A["big-big"], x, sp.oo) - phi ** 2 / 2) == 0
          and sp.simplify(sp.limit(A["small-small"], x, 0) - phi ** 2 / 2) == 0)
    # weights in app units: w_big - w_small = (L/2)^2 (2s - 1) = (phi^2/4)(x - 1)/(x + 1)
    wd = sp.simplify(k * (2 * s - 1).subs(s, x / (1 + x)))
    check("A6 golden weight: w_big - w_small = (phi^2/4)(x-1)/(x+1) (app units), = 1/(4 phi) at x = tau, odd under x -> 1/x",
          sp.simplify(wd - phi ** 2 / 4 * (x - 1) / (x + 1)) == 0 and sp.simplify(wd.subs(x, phi) - 1 / (4 * phi)) == 0
          and sp.simplify(wd.subs(x, 1 / x) + wd) == 0)
    raw["golden weight difference (app units)"] = "(phi^2/4)(x-1)/(x+1)"
    # ---- Delian; app units (octet edge 1) = tetPiece units / sqrt2: areas / 2, weights / 2
    L_, Rr = Dl[True], Dl[False]
    ot = sp.Piecewise((L_["oct-tet"] / 2, t <= R(1, 3)), (Rr["oct-tet"] / 2, True))
    raw["delian areas (app units, t)"] = {"oct-tet": [str(sp.factor(L_["oct-tet"] / 2)), str(sp.factor(Rr["oct-tet"] / 2))],
                                          "oct-oct (t<=1/3)": str(sp.factor(L_["oct-oct"] / 2)), "tet-tet (t>=1/3)": str(sp.factor(sp.expand(Rr["tet-tet"] / 2)))}
    third = R(1, 3)
    check("A6 delian: oct-tet continuous at t = 1/3 (sqrt3/4, the octet triangle), 0 at t = 0 and t = 1, > 0 on (0,1)",
          sp.simplify(L_["oct-tet"].subs(t, third) - Rr["oct-tet"].subs(t, third)) == 0 and sp.simplify(L_["oct-tet"].subs(t, third) / 2 - sp.sqrt(3) / 4) == 0
          and L_["oct-tet"].subs(t, 0) == 0 and Rr["oct-tet"].subs(t, 1) == 0)
    dl, dr = sp.diff(L_["oct-tet"], t), sp.diff(Rr["oct-tet"], t)
    check("A6 delian: oct-tet rises on (0,1/3), falls on (1/3,1); a corner at 1/3 (slopes 3 sqrt3 and -3 sqrt3/2, tetPiece units)",
          sign_on(dl, t, sp.Integer(0), third) == 1 and sign_on(dr, t, third, sp.Integer(1)) == -1
          and sp.simplify(dl.subs(t, third) - 3 * sp.sqrt(3)) == 0 and sp.simplify(dr.subs(t, third) + 3 * sp.sqrt(3) / 2) == 0)
    check("A6 delian: oct-oct (sqrt2/2)(1 - 9t^2) strictly decreasing on [0,1/3], = sqrt2/2 (RD rhombus) at 0, dies exactly at t = 1/3",
          sign_on(sp.diff(L_["oct-oct"], t), t, sp.Integer(0), third) == -1 and L_["oct-oct"].subs(t, third) == 0
          and set(sp.solve(L_["oct-oct"], t)) == {-third, third})
    check("A6 delian: tet-tet 1 - a^2 strictly increasing on [1/3,1], born exactly at t = 1/3, = 1 (cube face) at t = 1",
          sign_on(sp.diff(Rr["tet-tet"], t), t, third, sp.Integer(1)) == 1 and Rr["tet-tet"].subs(t, third) == 0 and Rr["tet-tet"].subs(t, 1) == 1
          and [r for r in sp.solve(Rr["tet-tet"], t) if 0 <= r <= 1] == [third])
    check("A6 delian: weight w_tet - w_oct = (3/8)(2t - 1) (app units), from -3/8 (RD) through -1/8 (octet) to 3/8 (cubes)",
          (R(3, 8) * (2 * t - 1)).subs(t, third) == -R(1, 8))
    tb = 1 - R(2, 3) * 2 ** R(-1, 3)
    raw["delian bond"] = {"t": str(tb), "w_tet - w_oct (app)": str(sp.nsimplify(sp.expand(R(3, 8) * (2 * tb - 1)))),
                          "oct-tet (app)": str(sp.nsimplify(sp.simplify(Rr['oct-tet'].subs(t, tb) / 2))), "tet-tet (app)": str(sp.simplify(Rr['tet-tet'].subs(t, tb) / 2))}
    raw["golden tau"] = {"big-small (app)": str(sp.nsimplify(sp.simplify(A["big-small"].subs(x, phi))))}

if __name__ == "__main__":
    T0 = time.time()
    G = golden(); Dl = delian(); closed_form_facts(G, Dl)
    raw["seconds_total"] = round(time.time() - T0, 1)
    json.dump(raw, open("../data/raw/symbolic.json", "w"), indent=1, default=str)
    with open("../data/checks/symbolic-checks.txt", "w") as f:
        for c in checks: f.write("  ".join(c) + "\n")
        f.write(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL, {raw['seconds_total']} s\n")
    print(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL, total {raw['seconds_total']} s")
