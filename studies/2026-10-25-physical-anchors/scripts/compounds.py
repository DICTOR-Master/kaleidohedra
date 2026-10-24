# Physical anchors, part B (exact): radical (Laguerre) tessellations built from scratch with weight = radius^2.
#  B0 known cases: equal spheres on bcc -> Kelvin truncated octahedron (8 hexagons + 6 squares, all edges equal);
#     equal spheres on fcc -> rhombic dodecahedron (12 congruent rhombi).
#  B1 the loop stops, as touching-sphere packings (w = r^2, not only the weight difference): cell = the app's piece.
#  B2 real compounds, Shannon (1976) ionic radii (via the Imperial College transcription, ../data/raw/shannon.json):
#     rho, x or t, cell = the app's piece, bond counts per piece, bond areas = Bond Relay closed forms.
# Exact: radii are decimals -> Fractions; weights 3 r^2/(r_a + r_c)^2 (golden, half-edge units, unlike distance sqrt3) and
# (3/4) r^2/(r_a + r_c)^2 (Delian, tetPiece units, unlike distance sqrt3/2) are rational, so every cell is over Q.
# Output: ../data/raw/compounds.json, ../data/checks/compounds-checks.txt
import json, os, sys, time
from fractions import Fraction as Fr
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-10-25-web-of-bonds', 'scripts'))
from lib import QQ, power_cell, cell_faces, enough_sites, vadd, vsub, dot
from samples import golden_sites, golden_T, golden_forms, delian_sites, tet_piece, oct_piece, delian_forms

checks, raw = [], {"known": {}, "stops": {}, "compounds": []}
def check(name, ok, detail=""):
    ok = bool(ok); checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)

SH = json.load(open(os.path.join(HERE, '..', 'data', 'raw', 'shannon.json')))
def shannon(el, charge, cn):
    for r in SH[el]:
        if r["charge"] == charge and r["CN"] == cn:
            return Fr(r["IR"]), Fr(r["CR"]), r["key"]
    return None

def edges_sq(poly):
    return [dot(vsub(poly[k], poly[(k + 1) % len(poly)]), vsub(poly[k], poly[(k + 1) % len(poly)])) for k in range(len(poly))]

# ---------------- B0 known cases ----------------
def known_cases():
    S = golden_sites(4); w = {"big": QQ(0), "small": QQ(0)}
    sub = [x for x in S if dot(x[1], x[1]) <= 16]; i = sub.index(("big", (Fr(0),) * 3))
    cell = power_cell(i, sub, w, QQ); fc, vol = cell_faces(cell, QQ)
    sides = sorted(len(p) for p, a2, n in fc.values()); E = {e for p, a2, n in fc.values() for e in edges_sq(p)}
    check("B0a equal spheres on bcc: cell = Kelvin truncated octahedron (6 squares + 8 hexagons, all edges equal, 24 corners)",
          sides == [4] * 6 + [6] * 8 and len(E) == 1 and len(cell["corners"]) == 24, f"edges^2 {[str(e) for e in E]}, vol {vol}")
    raw["known"]["bcc"] = dict(faces=sides, edge2=[str(e) for e in E], volume=str(vol))
    # fcc: only the odd-integer points (oct sites), equal weights
    S = [x for x in delian_sites(3) if x[0] == "oct"]; c = (Fr(1), Fr(0), Fr(0))
    sub = [x for x in S if dot(vsub(x[1], c), vsub(x[1], c)) <= 9]; i = sub.index(("oct", c))
    cell = power_cell(i, sub, {"oct": QQ(0)}, QQ); fc, vol = cell_faces(cell, QQ)
    sides = sorted(len(p) for p, a2, n in fc.values()); A = {a2 for p, a2, n in fc.values()}; E = {e for p, a2, n in fc.values() for e in edges_sq(p)}
    check("B0b equal spheres on fcc: cell = rhombic dodecahedron (12 rhombi, one area, one edge, 14 corners, volume 2)",
          sides == [4] * 12 and len(A) == 1 and len(E) == 1 and len(cell["corners"]) == 14 and vol == 2, f"area^2 {[str(a) for a in A]}")
    raw["known"]["fcc"] = dict(faces=sides, area2=[str(a) for a in A], volume=str(vol))

# ---------------- golden: CsCl-type ----------------
GS = golden_sites(4)
def golden_build(rbig, rsmall, label):
    """Radical tessellation of touching spheres r_big (sites 2Z^3) and r_small (2Z^3 + (1,1,1)); unlike distance sqrt3."""
    u = rbig + rsmall
    w = {"big": QQ(3 * rbig * rbig / (u * u)), "small": QQ(3 * rsmall * rsmall / (u * u))}
    rho = rsmall / rbig; s = (2 - rho) / (1 + rho)              # A2b
    assert 0 <= s <= 1
    sF = QQ(s); out = {"rho": str(rho), "rho_f": float(rho), "s": str(s), "x": (str(s / (1 - s)) if s != 1 else "inf"),
                       "x_f": (float(s / (1 - s)) if s != 1 else None)}
    forms = golden_forms(sF); ok_all = True; cnt = {}; areas = {}
    for kind, c in (("big", (Fr(0),) * 3), ("small", (Fr(1),) * 3)):
        sub = [y for y in GS if dot(vsub(y[1], c), vsub(y[1], c)) <= 16]; i = sub.index((kind, c))
        cell = power_cell(i, sub, w, QQ); fc, vol = cell_faces(cell, QQ)
        ok, _ = enough_sites(cell, sub, w, 4)
        app = [vadd(c, p) for p in golden_T(sF if kind == "big" else QQ(1) - sF, QQ)]
        inside = all(all((b - dot(n, p)).sign() >= 0 for _, n, b in cell["planes"]) for p in app)
        same = inside and set(cell["corners"]) <= set(app) and ok
        k = {}
        for j, (poly, a2, n) in fc.items():
            typ = "-".join(sorted((kind, sub[j][0]))); k[typ] = k.get(typ, 0) + 1
            if not (a2 == forms[tuple(sorted((kind, sub[j][0])))]): same = False
            areas[typ] = float(a2) ** 0.5 * (float((1 + 5 ** 0.5) / 2) ** 2 / 4)   # half-edge units -> app units (L = phi)
        cnt[kind] = k; ok_all &= same
        out[f"vol_{kind}_halfedge3"] = str(vol)
    out["counts"] = cnt; out["areas_app"] = areas
    out["areas_A2_per_contact"] = {k: v / (float((1 + 5 ** 0.5) / 2) ** 2 / 4) * float(u * u) / 3 for k, v in areas.items()}
    check(f"{label}: radical cells (w = r^2) = app T(x) big and T(1/x) small; areas = closed forms; site list enough", ok_all,
          f"rho={float(rho):.4f} x={out['x']} counts={cnt}")
    return out

# ---------------- Delian: fluorite / antifluorite ----------------
DS = delian_sites(3)
REPS = {"oct": ("oct", (Fr(1), Fr(0), Fr(0))), "tet0": ("tet", (Fr(1, 2),) * 3), "tet1": ("tet", (Fr(3, 2), Fr(1, 2), Fr(1, 2)))}
def delian_build(rtet, roct, label):
    u = rtet + roct
    w = {"tet": QQ(Fr(3, 4) * rtet * rtet / (u * u)), "oct": QQ(Fr(3, 4) * roct * roct / (u * u))}
    t = rtet / u; tF = QQ(t)                                      # A4b
    out = {"rho": str(rtet / roct), "rho_f": float(rtet / roct), "t": str(t), "t_f": float(t)}
    forms = delian_forms(tF); ok_all = True; cnt = {}; areas = {}
    for r, (kind, c) in REPS.items():
        sub = [y for y in DS if dot(vsub(y[1], c), vsub(y[1], c)) <= 9]; i = sub.index((kind, c))
        cell = power_cell(i, sub, w, QQ); fc, vol = cell_faces(cell, QQ)
        ok, _ = enough_sites(cell, sub, w, 3)
        app = oct_piece((1, 0, 0), tF, QQ) if kind == "oct" else tet_piece((0, 0, 0) if r == "tet0" else (1, 0, 0), tF, QQ)
        inside = all(all((b - dot(n, p)).sign() >= 0 for _, n, b in cell["planes"]) for p in app)
        same = inside and set(cell["corners"]) <= set(app) and ok
        k = {}
        for j, (poly, a2, n) in fc.items():
            typ = "-".join(sorted((kind, sub[j][0]))); k[typ] = k.get(typ, 0) + 1
            if not (a2 == forms[tuple(sorted((kind, sub[j][0])))]): same = False
            areas[typ] = float(a2) ** 0.5 / 2                          # tetPiece units -> app units (/sqrt2 lengths)
        if r != "tet1": cnt[kind] = k
        ok_all &= same
    out["counts"] = cnt; out["areas_app"] = areas
    out["areas_A2_per_contact"] = {k: v * 2 * float(u * u) * 4 / 3 for k, v in areas.items()}
    check(f"{label}: radical cells (w = r^2) = app tetPiece/octPiece at t; areas = closed forms; site list enough", ok_all,
          f"rho={float(rtet / roct):.4f} t={float(t):.4f} counts={cnt}")
    return out

# ---------------- B1 loop stops as touching packings (rational stops only; irrational stops are A5) ----------------
def stops():
    for x in (Fr(1, 2), Fr(1), Fr(2), Fr(5, 2)):          # inside the golden contact window [0.366, 2.732]
        rho = (x + 2) / (2 * x + 1)
        raw["stops"][f"golden x={x}"] = golden_build(Fr(1), rho, f"B1 golden x={x} (rho={rho})") if rho <= 1 else \
            golden_build(1 / rho, Fr(1), f"B1 golden x={x} (rho={rho}; small is larger)")
    for t in (Fr(1, 5), Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(4, 7)):   # inside the Delian contact window [0.1835, 0.5774]
        raw["stops"][f"delian t={t}"] = delian_build(t, 1 - t, f"B1 delian t={t} (rho={t / (1 - t)})")

# ---------------- B2 compounds ----------------
GOLDEN_C = [  # CsCl type: (formula, cation (el, charge, CN), anion (el, charge, CN), note)
    ("CsCl", ("Cs", 1, "VIII"), ("Cl", -1, "VI"), "Cl- has no CN VIII entry in Shannon 1976: CN VI value used"),
    ("CsBr", ("Cs", 1, "VIII"), ("Br", -1, "VI"), "Br- CN VI value used (no CN VIII entry)"),
    ("CsI", ("Cs", 1, "VIII"), ("I", -1, "VI"), "I- CN VI value used (no CN VIII entry; key A = Ahrens 1952)"),
    ("TlCl", ("Tl", 1, "VIII"), ("Cl", -1, "VI"), "Tl+ VIII key R; Cl- CN VI used"),
    ("TlBr", ("Tl", 1, "VIII"), ("Br", -1, "VI"), "Tl+ VIII key R; Br- CN VI used"),
]
DELIAN_C = [  # fluorite: cation on oct sites (CN8), anion on tet sites (CN4); antifluorite: swapped
    ("CaF2", "fluorite", ("Ca", 2, "VIII"), ("F", -1, "IV"), ""),
    ("SrF2", "fluorite", ("Sr", 2, "VIII"), ("F", -1, "IV"), ""),
    ("BaF2", "fluorite", ("Ba", 2, "VIII"), ("F", -1, "IV"), ""),
    ("CdF2", "fluorite", ("Cd", 2, "VIII"), ("F", -1, "IV"), "Cd2+ VIII key C"),
    ("PbF2", "fluorite", ("Pb", 2, "VIII"), ("F", -1, "IV"), "Pb2+ VIII key C"),
    ("UO2", "fluorite", ("U", 4, "VIII"), ("O", -2, "IV"), "U4+ VIII key R*"),
    ("ThO2", "fluorite", ("Th", 4, "VIII"), ("O", -2, "IV"), "Th4+ VIII key RC"),
    ("CeO2", "fluorite", ("Ce", 4, "VIII"), ("O", -2, "IV"), "Ce4+ VIII key R"),
    ("ZrO2 (cubic)", "fluorite", ("Zr", 4, "VIII"), ("O", -2, "IV"), "Zr4+ VIII key *"),
    ("Li2O", "antifluorite", ("Li", 1, "IV"), ("O", -2, "VIII"), "Li+ IV key *"),
    ("Na2O", "antifluorite", ("Na", 1, "IV"), ("O", -2, "VIII"), ""),
    ("K2O", "antifluorite", ("K", 1, "IV"), ("O", -2, "VIII"), ""),
]
SQ3m1 = 3 ** 0.5 - 1; SQ32m1 = 1.5 ** 0.5 - 1; SQ2m1 = 2 ** 0.5 - 1

def compounds():
    for f, cat, an, note in GOLDEN_C:
        (rc, crc, kc), (ra, cra, ka) = shannon(*cat), shannon(*an)
        big, small = (ra, rc) if ra >= rc else (rc, ra)
        rec = dict(formula=f, structure="CsCl (B2)", cation=f"{cat[0]}{'+' * cat[1]} CN {cat[2]}", anion=f"{an[0]}- CN {an[2]}",
                   r_cation_IR=str(rc), r_anion_IR=str(ra), r_cation_CR=str(crc), r_anion_CR=str(cra), keys=[kc, ka], note=note,
                   big_site="anion" if ra >= rc else "cation", cation_over_anion=float(rc / ra),
                   pauling_CN8_cation_ok=bool(float(rc / ra) >= SQ3m1))
        rec.update(golden_build(big, small, f"B2 {f}"))
        rc2, ra2 = crc, cra; b2, s2 = (ra2, rc2) if ra2 >= rc2 else (rc2, ra2); rho2 = s2 / b2
        rec["CR_sensitivity"] = dict(rho=float(rho2), x=float((2 - rho2) / (2 * rho2 - 1)))
        rec["in_contact_window"] = bool(float(Fr(rec["rho"])) >= SQ3m1)
        raw["compounds"].append(rec)
    for f, st, cat, an, note in DELIAN_C:
        (rc, crc, kc), (ra, cra, ka) = shannon(*cat), shannon(*an)
        if st == "fluorite": rtet, roct, ctet, coct = ra, rc, cra, crc
        else: rtet, roct, ctet, coct = rc, ra, crc, cra
        rec = dict(formula=f, structure=st, cation=f"{cat[0]}{cat[1]}+ CN {cat[2]}", anion=f"{an[0]}{-an[1]}- CN {an[2]}",
                   r_cation_IR=str(rc), r_anion_IR=str(ra), r_cation_CR=str(crc), r_anion_CR=str(cra), keys=[kc, ka], note=note,
                   tet_site="anion" if st == "fluorite" else "cation", cation_over_anion=float(rc / ra))
        if st == "fluorite":   # cation CN8 inside an anion cube: Pauling lower limit sqrt3 - 1; next CN (12) above 1
            rec["pauling"] = dict(rule="cation CN8: r+/r- in [0.732, 1)", ok=bool(SQ3m1 <= float(rc / ra) < 1))
        else:                  # cation CN4 inside an anion tetrahedron: [0.225, 0.414)
            rec["pauling"] = dict(rule="cation CN4: r+/r- in [0.225, 0.414)", ok=bool(SQ32m1 <= float(rc / ra) < SQ2m1))
        rec.update(delian_build(rtet, roct, f"B2 {f}"))
        tt = float(ctet / (ctet + coct)); rec["CR_sensitivity"] = dict(rho=float(ctet / coct), t=tt)
        rec["in_contact_window"] = bool(1 - (2 / 3) ** 0.5 <= rec["t_f"] <= 1 / 3 ** 0.5)
        rec["side_of_octet"] = "t < 1/3 (oct-oct bonds)" if rec["t_f"] < 1 / 3 else ("t = 1/3" if rec["t_f"] == 1 / 3 else "t > 1/3 (tet-tet bonds)")
        raw["compounds"].append(rec)

if __name__ == "__main__":
    T0 = time.time()
    known_cases(); stops(); compounds()
    # B3 consistency: contact window flag agrees with the Pauling limit for every CsCl-type and fluorite compound (same inequality)
    agree = all(c["in_contact_window"] == c.get("pauling_CN8_cation_ok", c.get("pauling", {}).get("ok"))
                for c in raw["compounds"] if c["structure"] in ("CsCl (B2)",))
    agreeF = all(c["in_contact_window"] == (c["cation_over_anion"] >= SQ3m1) for c in raw["compounds"] if c["structure"] == "fluorite")
    check("B3 contact-window test = Pauling's CN8 limit r+/r- >= sqrt3 - 1 (CsCl-type and fluorite, every compound)", agree and agreeF)
    raw["seconds"] = round(time.time() - T0, 1)
    json.dump(raw, open(os.path.join(HERE, '..', 'data', 'raw', 'compounds.json'), 'w'), indent=1)
    with open(os.path.join(HERE, '..', 'data', 'checks', 'compounds-checks.txt'), 'w') as fo:
        for c in checks: fo.write("  ".join(c) + "\n")
        fo.write(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL, {raw['seconds']} s\n")
    print(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL, {raw['seconds']} s")
