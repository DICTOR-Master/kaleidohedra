# Bond physics, part G (geometry): solid angles, O'Keeffe coordination numbers and bond-face shares of the exact
# DICTONIC power cells, along both loops and at the placed compounds.
#  Cells: built from scratch over Q with the web-of-bonds lib (power_cell / cell_faces), at rational parameters only;
#         every face area^2 is checked exactly against the web-of-bonds closed forms.
#  Solid angles: transcendental, so evaluated with mpmath at 40 digits from the exact corners (Van Oosterom-Strackee
#         triangle formula, fan from one corner); check: the faces of every cell add up to 4 pi.
#  O'Keeffe (1979) coordination number: N = sum_i Omega_i / Omega_max (each face weighted by its solid angle relative to
#         the largest face). The formula is the one that reproduces the published bcc value 10.16 (G0) - the original paper
#         could not be read (see README).
#  The site is always inside its own cell: every site has a cubic point group fixing only the site, the convex cell is
#         invariant, so its centroid is the site.
# Output: ../data/raw/geom.json, ../data/checks/geom-checks.txt
import json, os, sys, time
from fractions import Fraction as Fr
from itertools import product
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-10-25-web-of-bonds', 'scripts'))
from lib import QQ, power_cell, cell_faces, enough_sites, vsub, dot
from samples import golden_sites, golden_forms, delian_sites, delian_forms

mp.mp.dps = 40
PHI = (1 + mp.sqrt(5)) / 2
checks = []
def check(name, ok, detail=""):
    ok = bool(ok); checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)

def fr(e): return e.c[0] if hasattr(e, "c") else Fr(e)
def mv(p): return [mp.mpf(fr(x).numerator) / fr(x).denominator for x in p]
def sub3(a, b): return [x - y for x, y in zip(a, b)]
def dot3(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cr3(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def nrm(a): return mp.sqrt(dot3(a, a))

def tri_sa(a, b, c):  # signed solid angle of triangle (a, b, c) seen from the origin
    la, lb, lc = nrm(a), nrm(b), nrm(c)
    den = la * lb * lc + dot3(a, b) * lc + dot3(a, c) * lb + dot3(b, c) * la
    return 2 * mp.atan2(dot3(a, cr3(b, c)), den)

def face_sa(poly, site):
    P = [sub3(mv(p), site) for p in poly]
    return abs(sum(tri_sa(P[0], P[k], P[k + 1]) for k in range(1, len(P) - 1)))

def analyse(sites, w, kind, c, Dsq, forms=None, D=None):
    """Exact power cell of the site (kind, c) among sites within sqrt(Dsq); per bond type: count, area (exact area^2 ->
    mp sqrt, native units) and solid angle; O'Keeffe N; checks area^2 against forms and sum of solid angles = 4 pi."""
    sub = [y for y in sites if dot(vsub(y[1], c), vsub(y[1], c)) <= Dsq]; i = sub.index((kind, c))
    cell = power_cell(i, sub, w, QQ); fc, vol = cell_faces(cell, QQ)
    ok_sites = enough_sites(cell, sub, w, D)[0] if D else True
    site = mv(c); per = {}; oms = []; forms_ok = True
    for j, (poly, a2, n) in fc.items():
        typ = "-".join(sorted((kind, sub[j][0])))
        om = face_sa(poly, site); A = mp.sqrt(mp.mpf(fr(a2).numerator) / fr(a2).denominator)
        d = per.setdefault(typ, {"count": 0, "area": mp.mpf(0), "omega": mp.mpf(0), "omega_face": om, "area_face": A, "sides": len(poly)})
        d["count"] += 1; d["area"] += A; d["omega"] += om; oms.append(om)
        if forms is not None and not (a2 == forms[tuple(sorted((kind, sub[j][0])))]): forms_ok = False
    tot = sum(oms); N = tot / max(oms)
    return dict(per=per, N=N, total=tot, forms_ok=forms_ok, sites_ok=ok_sites, vol=vol)

def summ(r, area_unit):
    """JSON-ready summary: per type count, face area (app units), share of the cell's surface and of its solid angle."""
    A = sum(d["area"] for d in r["per"].values())
    return {"N_okeeffe": float(r["N"]),
            "types": {t: {"count": d["count"], "sides": d["sides"], "face_area_app": float(d["area_face"] * area_unit),
                          "face_solid_angle_sr": float(d["omega_face"]), "share_area": float(d["area"] / A),
                          "share_solid_angle": float(d["omega"] / (4 * mp.pi))} for t, d in sorted(r["per"].items())}}

GS = golden_sites(4); DS = delian_sites(3)
GU = PHI ** 2 / 4          # golden: half-edge units -> app units (L = phi), areas
DU = mp.mpf(1) / 2         # Delian: tetPiece units -> app units (lengths / sqrt2), areas
BIG, SMALL = ("big", (Fr(0),) * 3), ("small", (Fr(1),) * 3)
OCT, TET = ("oct", (Fr(1), Fr(0), Fr(0))), ("tet", (Fr(1, 2),) * 3)

def golden(s, kind):
    w = {"big": QQ(2 * s - 1), "small": QQ(0)}            # w_big - w_small = (L/2)^2 (2s - 1)
    k, c = BIG if kind == "big" else SMALL
    return analyse(GS, w, k, c, 16, golden_forms(QQ(s)), 4)

def delian(t, kind):
    w = {"tet": QQ(Fr(3, 4) * (2 * t - 1)), "oct": QQ(0)}  # tetPiece units: w_tet - w_oct = (3/4)(2t - 1)
    k, c = OCT if kind == "oct" else TET
    return analyse(DS, w, k, c, 9, delian_forms(QQ(t)), 3)

def tol(r): return abs(r["total"] - 4 * mp.pi) < mp.mpf(10) ** -30

raw = {"sanity": {}, "golden": [], "delian": [], "compounds": [], "hop": {}}
t0 = time.time()
# ---------------- G0 sanity: published O'Keeffe values (bcc 10.16, diamond 4.54) ----------------
r = golden(Fr(1, 2), "big")
check("G0a bcc Voronoi (Kelvin, x = 1): O'Keeffe N = 8 + 6 Omega_sq/Omega_hex rounds to the published 10.16", tol(r) and r["forms_ok"]
      and round(float(r["N"]), 2) == 10.16, f"N = {mp.nstr(r['N'], 12)}")
raw["sanity"]["bcc"] = summ(r, GU)
dia = []                                                    # diamond, cubic edge 4: A = even coords, sum = 0 mod 4; B = A + (1,1,1)
for m in product(range(-6, 7), repeat=3):
    if all(x % 2 == 0 for x in m) and sum(m) % 4 == 0:
        dia.append(("A", tuple(Fr(x) for x in m))); dia.append(("B", tuple(Fr(x + 1) for x in m)))
rd = analyse(dia, {"A": QQ(0), "B": QQ(0)}, "A", (Fr(0),) * 3, 40, None, None)
cnts = sorted((d["sides"], d["count"]) for d in rd["per"].values())
check("G0b diamond Voronoi (triakis truncated tetrahedron: 4 hexagons + 12 triangles): O'Keeffe N rounds to the published 4.54",
      tol(rd) and cnts == [(3, 12), (6, 4)] and round(float(rd["N"]), 2) == 4.54, f"N = {mp.nstr(rd['N'], 12)}, faces {cnts}")
raw["sanity"]["diamond"] = {"N_okeeffe": float(rd["N"]), "faces": cnts}

# ---------------- G1 golden sweep, s = k/40 (s = x/(1+x)) ----------------
allok = True
for k in range(0, 41):
    s = Fr(k, 40); row = {"s": str(s), "x": (float(s / (1 - s)) if s != 1 else None)}
    for kind in ("big", "small"):
        r = golden(s, kind); allok &= tol(r) and r["forms_ok"] and r["sites_ok"]; row[kind] = summ(r, GU)
    raw["golden"].append(row)
check("G1 golden loop, s = 0, 1/40, ..., 1 (41 x 2 cells): areas^2 = closed forms exactly, solid angles add to 4 pi, site list enough", allok)
g = {r["s"]: r for r in raw["golden"]}
check("G1b swap x <-> 1/x: N_big(s) = N_small(1 - s) at every sample",
      all(abs(g[str(Fr(k, 40))]["big"]["N_okeeffe"] - g[str(Fr(40 - k, 40))]["small"]["N_okeeffe"]) < 1e-12 for k in range(41)))
Nb = [g[str(Fr(k, 40))]["big"]["N_okeeffe"] for k in range(41)]
kmax = max(range(41), key=lambda k: Nb[k])
check("G1c N_big is not monotone in s: it peaks inside (0, 1)", 0 < kmax < 40, f"max N_big = {Nb[kmax]:.6f} at s = {Fr(kmax, 40)}; ends {Nb[0]:.6f}, {Nb[40]:.6f}")

# ---------------- G2 Delian sweep, t = k/60, 0 < t < 1 ----------------
allok = True
for k in range(1, 60):
    t = Fr(k, 60); row = {"t": str(t)}
    for kind in ("oct", "tet"):
        r = delian(t, kind); allok &= tol(r) and r["forms_ok"] and r["sites_ok"]; row[kind] = summ(r, DU)
    raw["delian"].append(row)
check("G2 Delian loop, t = 1/60 ... 59/60 (59 x 2 cells): areas^2 = closed forms exactly, solid angles add to 4 pi, site list enough", allok)
dl = {r["t"]: r for r in raw["delian"]}
o13 = dl["1/3"]
check("G2b octet t = 1/3: oct cell = 8 equal triangles (N = 8), tet cell = 4 equal triangles (N = 4)",
      abs(o13["oct"]["N_okeeffe"] - 8) < 1e-12 and abs(o13["tet"]["N_okeeffe"] - 4) < 1e-12)

# ---------------- G3 compounds (Shannon IR and CR, from the physical-anchors study) ----------------
CMP = json.load(open(os.path.join(HERE, '..', '..', '2026-10-25-physical-anchors', 'data', 'raw', 'compounds.json')))["compounds"]
allok = True
for cpd in CMP:
    out = {"formula": cpd["formula"], "structure": cpd["structure"]}
    for conv in ("IR", "CR"):
        rc, ra = Fr(cpd[f"r_cation_{conv}"]), Fr(cpd[f"r_anion_{conv}"])
        if cpd["structure"].startswith("CsCl"):
            rho = rc / ra; s = (2 - rho) / (1 + rho)                 # anion on big; contact map
            rb, rs = golden(s, "big"), golden(s, "small")
            allok &= tol(rb) and tol(rs) and rb["forms_ok"] and rs["forms_ok"]
            if conv == "IR": allok &= abs(float(s) - float(Fr(cpd["s"]))) < 1e-15
            out[conv] = {"s": str(s), "x": float(s / (1 - s)), "anion(big)": summ(rb, GU), "cation(small)": summ(rs, GU)}
        else:
            rtet, roct = (ra, rc) if cpd["structure"] == "fluorite" else (rc, ra)
            t = rtet / (rtet + roct)
            ro, rt = delian(t, "oct"), delian(t, "tet")
            allok &= tol(ro) and tol(rt) and ro["forms_ok"] and rt["forms_ok"]
            if conv == "IR": allok &= (t == Fr(cpd["t"]))
            out[conv] = {"t": str(t), "t_f": float(t), "oct": summ(ro, DU), "tet": summ(rt, DU)}
    raw["compounds"].append(out)
check("G3 17 compounds x 2 radius conventions: cells exact, areas = closed forms, solid angles add to 4 pi, IR parameters = anchors study", allok)

# ---------------- G4 unweighted Voronoi cells of the measured structures ----------------
# Published Voronoi-Dirichlet descriptors use equal weights. Equal weights are s = 1/2 (golden) and t = 1/2 (Delian),
# whatever the compound: CsCl and fluorite have no free atomic coordinates, so the measured structure fixes only a.
check("G4 equal weights <-> s = 1/2 (golden) and t = 1/2 (Delian): weight difference vanishes there and only there",
      (2 * Fr(1, 2) - 1) == 0 and Fr(3, 4) * (2 * Fr(1, 2) - 1) == 0)
raw["voronoi_constants"] = {"CsCl_type_any_compound": {"anion": g["1/2"]["big"]["N_okeeffe"], "cation": g["1/2"]["small"]["N_okeeffe"]},
                            "fluorite_type_any_compound": {"8-coordinated (oct)": dl["1/2"]["oct"]["N_okeeffe"], "4-coordinated (tet)": dl["1/2"]["tet"]["N_okeeffe"]}}

# ---------------- G5 the anion hop in fluorite: which face does the straight <100> path cross? ----------------
def hop(t):
    """Midpoint of the tet sites (1/2,1/2,1/2) and (3/2,1/2,1/2) (a nearest tet-tet pair, the <100> vacancy hop).
    Returns the kinds of the cells whose power is minimal there, and for t > 1/3 whether it is inside the shared face."""
    w = {"tet": QQ(Fr(3, 4) * (2 * t - 1)), "oct": QQ(0)}
    m = (Fr(1), Fr(1, 2), Fr(1, 2))
    pw = sorted(((dot(vsub(m, c), vsub(m, c)) - fr(w[k]), k, c) for k, c in DS if dot(vsub(m, c), vsub(m, c)) <= 4))
    low = [(k, c) for p, k, c in pw if p == pw[0][0]]
    return {"t": str(t), "min_power_cells": sorted({k for k, c in low}), "n_cells": len(low)}
raw["hop"] = {str(t): hop(t) for t in (Fr(1, 6), Fr(1, 4), Fr(1, 3), Fr(2, 5), Fr(1, 2), Fr(3, 5), Fr(9, 10))}
okh = all(raw["hop"][str(t)]["min_power_cells"] == ["tet"] and raw["hop"][str(t)]["n_cells"] == 2 for t in (Fr(2, 5), Fr(1, 2), Fr(3, 5), Fr(9, 10))) \
      and all("tet" not in raw["hop"][str(t)]["min_power_cells"] for t in (Fr(1, 6), Fr(1, 4)))
check("G5 hop: for t > 1/3 the <100> anion-hop midpoint lies on the shared tet-tet face, in no other cell (the hop crosses that bond face); "
      "for t < 1/3 it lies in oct cells only (the path leaves the tet cells and crosses oct space)", okh,
      "; ".join(f"t={v['t']}: {v['min_power_cells']}x{v['n_cells']}" for v in raw["hop"].values()))

raw["seconds"] = time.time() - t0
os.makedirs(os.path.join(HERE, '..', 'data', 'checks'), exist_ok=True)
json.dump(raw, open(os.path.join(HERE, '..', 'data', 'raw', 'geom.json'), 'w'), indent=1)
with open(os.path.join(HERE, '..', 'data', 'checks', 'geom-checks.txt'), 'w') as f:
    for st, n, d in checks: f.write(f"{st} {n}{(' | ' + d) if d else ''}\n")
    f.write(f"{sum(s == 'PASS' for s, *_ in checks)} PASS, {sum(s == 'FAIL' for s, *_ in checks)} FAIL, {raw['seconds']:.1f} s\n")
print(f"done {raw['seconds']:.1f} s")
