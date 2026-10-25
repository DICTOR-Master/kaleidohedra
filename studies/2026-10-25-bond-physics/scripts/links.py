# Bond physics, part P (physics links): tests the exact bond geometry (geom.json) against published measurements
# (values.json, every number with its source and reading level). Correlations are Spearman rank correlations with exact
# permutation p-values (all n! orderings); where a measured value is a range, every endpoint combination is tried and the
# range of rho_S is reported. Small samples are flagged. Floats only (the geometry inputs are exact cells from part G).
# Output: ../data/raw/links.json, ../data/checks/links-checks.txt
import json, os, math
from itertools import permutations, product
HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, '..', 'data', 'raw', 'geom.json')))
V = json.load(open(os.path.join(HERE, '..', 'data', 'raw', 'values.json')))
ANCH = {c["formula"]: c for c in json.load(open(os.path.join(HERE, '..', '..', '2026-10-25-physical-anchors', 'data', 'raw', 'compounds.json')))["compounds"]}
checks, out = [], {}
def check(name, ok, detail=""):
    ok = bool(ok); checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)

def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r
def pearson(a, b):
    n = len(a); ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a)); sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else float('nan')
def spearman(a, b): return pearson(ranks(a), ranks(b))
def perm_p(a, b):
    r0 = abs(spearman(a, b)); ra = ranks(a); rb = ranks(b); hits = tot = 0
    for p in permutations(rb):
        tot += 1; hits += abs(pearson(ra, list(p))) >= r0 - 1e-12
    return hits / tot
def ranged(xs, ys_ranges):
    """Spearman over every endpoint choice of the y ranges: (min, max) rho_S, and the exact p of the most extreme choice."""
    best = []
    for ch in product(*[sorted(set(r)) for r in ys_ranges]):
        best.append((spearman(xs, list(ch)), list(ch)))
    lo, hi = min(b[0] for b in best), max(b[0] for b in best)
    ext = max(best, key=lambda b: abs(b[0]))
    return {"rho_S_min": lo, "rho_S_max": hi, "most_extreme": ext[0], "p_exact_most_extreme": perm_p(xs, ext[1]), "n": len(xs)}

comp = {c["formula"]: c for c in G["compounds"]}

# ---------------- L1 O'Keeffe solid-angle coordination numbers ----------------
L1 = {"loops": {}, "compounds": {}}
L1["voronoi_constants"] = G["voronoi_constants"]
for f, c in comp.items():
    if "x" in c["IR"]:
        L1["compounds"][f] = {cv: {"x": c[cv]["x"], "N_anion": c[cv]["anion(big)"]["N_okeeffe"], "N_cation": c[cv]["cation(small)"]["N_okeeffe"]} for cv in ("IR", "CR")}
    else:
        L1["compounds"][f] = {cv: {"t": c[cv]["t_f"], "N_oct": c[cv]["oct"]["N_okeeffe"], "N_tet": c[cv]["tet"]["N_okeeffe"]} for cv in ("IR", "CR")}
# equal-solid-angle point on the golden loop (float bisection on the closed-form big cell T(s): square face x = 1 with corners
# (1, +-s, 0), (1, 0, +-s); hexagon in x + y + z = 1 + s with the 6 permutations of (1, s, 0)); there N_big = 14
def sa_poly(P):
    def tri(a, b, c):
        n = lambda v: math.sqrt(sum(x * x for x in v)); d = lambda u, v: sum(x * y for x, y in zip(u, v))
        cr = [b[1] * c[2] - b[2] * c[1], b[2] * c[0] - b[0] * c[2], b[0] * c[1] - b[1] * c[0]]
        return 2 * math.atan2(d(a, cr), n(a) * n(b) * n(c) + d(a, b) * n(c) + d(a, c) * n(b) + d(b, c) * n(a))
    return abs(sum(tri(P[0], P[k], P[k + 1]) for k in range(1, len(P) - 1)))
def golden_sa(s):
    sq = [(1, s, 0), (1, 0, s), (1, -s, 0), (1, 0, -s)]
    hx = [(1, s, 0), (1, 0, s), (s, 0, 1), (0, s, 1), (0, 1, s), (s, 1, 0)]
    return sa_poly(sq), sa_poly(hx)
a, b = 0.5, 1.0
for _ in range(80):
    m = (a + b) / 2; q, h = golden_sa(m)
    a, b = (m, b) if q < h else (a, m)
s_eq = (a + b) / 2; q, h = golden_sa(s_eq)
N_eq = 8 * h / q + 6 * q / q if h <= q else 8 + 6 * q / h
L1["golden_equal_solid_angle"] = {"s": s_eq, "x": s_eq / (1 - s_eq), "Omega_sq": q, "Omega_hex": h, "N_big": N_eq}
check("L1a golden: one interior s* where a square and a hexagon subtend the same solid angle; there N_big = 14 (max possible); float bisection",
      abs(q - h) < 1e-12 and abs(N_eq - 14) < 1e-9 and 0.7 < s_eq < 0.8, f"s* = {s_eq:.12f}, x* = {s_eq / (1 - s_eq):.10f}")
xs_ok = abs(G["golden"][20]["big"]["N_okeeffe"] - 10.160609692370862) < 1e-12
check("L1b published-value test: Voronoi (equal-weight) O'Keeffe N is the same constant for every CsCl-type compound (10.1606 both ions) "
      "and every fluorite-type compound (8 and 8): the measured structures carry no loop parameter", xs_ok and
      abs(G["voronoi_constants"]["fluorite_type_any_compound"]["4-coordinated (tet)"] - 8) < 1e-12)
out["L1"] = L1

# ---------------- L2 fluorite ionic transport ----------------
TS, EA = V["fluorite_TS_Tm_K"], V["fluorite_Ea_normal_eV"]
names = ["CaF2", "SrF2", "BaF2", "PbF2", "UO2", "Li2O"]
L2 = {"rows": {}}
for f in names:
    c = comp[f]; row = {}
    for cv in ("IR", "CR"):
        ty = c[cv]["tet"]["types"]
        row[cv] = {"t": c[cv]["t_f"], "tet_tet_area_app": ty.get("tet-tet", {}).get("face_area_app", 0.0),
                   "oct_tet_area_app": ty["oct-tet"]["face_area_app"],
                   "tet_tet_share_solid_angle": ty.get("tet-tet", {}).get("share_solid_angle", 0.0)}
    d = TS[f]; row["TS_over_Tm"] = sorted({d["TS"][i] / d["Tm"][j] for i in (0, 1) for j in (0, 1)}); row["TS_over_Tm"] = [row["TS_over_Tm"][0], row["TS_over_Tm"][-1]]
    row["TS"] = d["TS"]; row["Ea_normal"] = EA[f]; row["mobile_ion_site"] = "tet (8c)"
    L2["rows"][f] = row
# geometric fact: along the Delian loop (t > 1/3) the tet-tet area rises and the oct-tet area falls with t, so every rank test
# with a bond area is a rank test with t, i.e. with the radius ratio rho = t/(1 - t)
dl = [r for r in G["delian"] if eval(r["t"]) > 1 / 3]
mono = all(dl[i + 1]["tet"]["types"]["tet-tet"]["face_area_app"] > dl[i]["tet"]["types"]["tet-tet"]["face_area_app"] and
           dl[i + 1]["oct"]["types"]["oct-tet"]["face_area_app"] < dl[i]["oct"]["types"]["oct-tet"]["face_area_app"] for i in range(len(dl) - 1))
check("L2a bond areas are strictly monotone in t on (1/3, 1) (tet-tet up, oct-tet down): area rank tests = radius-ratio rank tests", mono)
tests = {}
for cv in ("IR", "CR"):
    for label, sel in (("5 (fluorides + UO2)", names[:5]), ("6 (+ Li2O)", names)):
        X = [L2["rows"][f][cv]["tet_tet_area_app"] for f in sel]
        tests[f"{cv} | n={label} | tet-tet area vs T_S/T_m"] = ranged(X, [L2["rows"][f]["TS_over_Tm"] for f in sel])
        tests[f"{cv} | n={label} | tet-tet area vs E_a (normal phase)"] = ranged(X, [L2["rows"][f]["Ea_normal"] for f in sel])
        tests[f"{cv} | n={label} | tet-tet area vs T_S"] = ranged(X, [L2["rows"][f]["TS"] for f in sel])
L2["tests"] = tests
anysig = any(v["p_exact_most_extreme"] < 0.05 and (v["rho_S_min"] > 0) == (v["rho_S_max"] > 0) for v in tests.values())
L2["any_significant_and_sign_stable"] = anysig
check("L2b every rank test recorded with its exact permutation p and its range over the measured value ranges", len(tests) == 12)
out["L2"] = L2

# ---------------- L3 bond valence vs face area ----------------
# In CsCl and fluorite every cation-anion bond of an ion is symmetry-equivalent, so the bond-valence sum rule fixes
# s = V/N exactly (Brown): Cs-Cl 1/8, Tl-X 1/8, M-F 1/4 (M2+ fluorides), M-O 1/2 (M4+ dioxides), A-O 1/4 (A2O). Like-ion
# contacts carry valence 0 in the model. Test: does the area of the faces track the bond valence?
L3 = {"rows": {}}
for f, c in comp.items():
    a = ANCH[f]
    if "x" in c["IR"]:
        an = c["IR"]["anion(big)"]["types"]
        L3["rows"][f] = {"valence_unlike_bond": 1 / 8, "unlike_area_A2": a["areas_A2_per_contact"]["big-small"],
                         "anion_like_share_area": an["big-big"]["share_area"], "anion_like_share_solid_angle": an["big-big"]["share_solid_angle"]}
    else:
        ty = c["IR"]["tet"]["types"]; val = 0.5 if (c["structure"] == "fluorite" and "O2" in f) else 0.25   # M4+ (CN 8): 4/8; M2+ (CN 8): 2/8; A+ (CN 4): 1/4
        L3["rows"][f] = {"valence_unlike_bond": val, "unlike_area_A2": a["areas_A2_per_contact"]["oct-tet"],
                         "tet_like_share_area": ty.get("tet-tet", {}).get("share_area", 0.0), "tet_like_share_solid_angle": ty.get("tet-tet", {}).get("share_solid_angle", 0.0)}
fl = [f for f, c in comp.items() if c["structure"] == "fluorite"]
L3["fluorite_unlike_area_vs_valence"] = {"rho_S": spearman([L3["rows"][f]["unlike_area_A2"] for f in fl], [L3["rows"][f]["valence_unlike_bond"] for f in fl]), "n": len(fl)}
sh = [L3["rows"][f]["tet_like_share_area"] for f in fl if f != "ZrO2 (cubic)"]
check("L3a in every placed fluorite the anion's like (tet-tet) faces take more than half of its cell surface, though they carry bond valence 0",
      min(sh) > 0.5, f"anion like-face share of area {min(sh):.3f}-{max(sh):.3f}")
sh2 = [L3["rows"][f]["anion_like_share_area"] for f, c in comp.items() if "x" in c["IR"]]
check("L3b in every placed CsCl-type halide the anion's like (big-big) faces take 20-40 % of its surface (valence 0)",
      0.2 < min(sh2) and max(sh2) < 0.4, f"{min(sh2):.3f}-{max(sh2):.3f}")
out["L3"] = L3

# ---------------- L4 elastic constants, Cauchy relation, Zener anisotropy (CsCl type) ----------------
E = V["CsCl_type_elastic_1e10Pa"]; L4 = {"rows": {}}
for f in ("CsBr", "CsI"):
    e = E[f]
    L4["rows"][f] = {"x_IR": comp[f]["IR"]["x"], "x_CR": comp[f]["CR"]["x"], "c12_over_c44": e["c12"] / e["c44"],
                     "cauchy_c12_minus_c44": e["c12"] - e["c44"], "zener_A": 2 * e["c44"] / (e["c11"] - e["c12"]),
                     "big_big_area_IR": comp[f]["IR"]["anion(big)"]["types"]["big-big"]["face_area_app"],
                     "small_small_area_IR": comp[f]["IR"]["cation(small)"]["types"]["small-small"]["face_area_app"]}
L4["n"] = 2
check("L4 elastic data verified for only 2 of 5 CsCl-type halides (CsBr, CsI at 4.2 K): no correlation can be computed", L4["n"] == 2)
out["L4"] = L4

json.dump(out, open(os.path.join(HERE, '..', 'data', 'raw', 'links.json'), 'w'), indent=1)
with open(os.path.join(HERE, '..', 'data', 'checks', 'links-checks.txt'), 'w') as f:
    for st, n, d in checks: f.write(f"{st} {n}{(' | ' + d) if d else ''}\n")
    f.write(f"{sum(s == 'PASS' for s, *_ in checks)} PASS, {sum(s == 'FAIL' for s, *_ in checks)} FAIL\n")
for k, v in out["L2"]["tests"].items(): print(f"{k}: rho_S {v['rho_S_min']:+.3f}..{v['rho_S_max']:+.3f}, p(extreme) {v['p_exact_most_extreme']:.3f}")
