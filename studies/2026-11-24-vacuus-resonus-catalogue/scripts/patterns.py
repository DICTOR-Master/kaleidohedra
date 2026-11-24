#!/usr/bin/env python3
"""Patterns across the catalogue (data/catalogue-all.json): every theorem of the README is checked on every row,
and every observation's exact scope (the list of solids) is printed. Writes data/patterns.txt."""
import json, os
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "../data")
rows = json.load(open(os.path.join(D, "catalogue-all.json")))
out = []
def say(*a): out.append(" ".join(str(x) for x in a)); print(*a, flush=True)

def items():
    """(label, family, row-like dict) for every solid and centre; the Platonic polars are left out (they repeat solids)"""
    for r in rows:
        if r["family"] == "Platonic polar": continue
        if r["family"] == "Johnson":
            nm = f"J{r['J']}"
            yield nm + " (corner centroid)", r, r["corner"]
            if not r["same_centre"]: yield nm + " (volume centroid)", r, r["volume"]
        else:
            yield r["name"], r, r

ALL = list(items())
say("solids:", len([r for r in rows if r["family"] != "Platonic polar"]), "; solid-centre pairs:", len(ALL))

# ---- Lemma 1 (vacuus-enumeration): heart <=> centrally symmetric
bad = [l for l, r, a in ALL if (a["vacuus_kind"] == "heart") != a["centrally_symmetric"]]
assert not bad, bad
say("Lemma 1 (heart iff centrally symmetric): holds on all", len(ALL))

# ---- Theorem A: centrally symmetric => every Resonus plane carries two faces
bad = [l for l, r, a in ALL if a["centrally_symmetric"] and a["resonus_one_face"] != 0]
assert not bad, bad
paired_not_cs = [l for l, r, a in ALL if a["resonus_one_face"] == 0 and not a["centrally_symmetric"]]
say("Theorem A(b) (centrally symmetric => all Resonus planes carry 2 faces): holds on all")
say("A(c) scope: every Resonus plane carries 2 faces but the solid is not centrally symmetric:", paired_not_cs)
mixed = [l for l, r, a in ALL if a["resonus_one_face"] and a["resonus_two_faces"]]
single = [l for l, r, a in ALL if a["resonus_two_faces"] == 0]
say("Resonus with both kinds of plane:", len(mixed), "; only single-face planes (no two faces parallel):", single)

# ---- Resonus independent of the centre (Johnson, asserted in the run) and the Vacuus about the two centres
diffJ = []
for r in rows:
    if r["family"] != "Johnson": continue
    a, b = r["corner"], r["volume"]
    ks = [k for k in ("vacuus_plates", "vacuus_full", "vacuus_shared", "vacuus_single", "vacuus_kind", "vacuus_on_mirrors", "both",
                      "both_on_mirrors", "vacuus_meets_polar_resonus", "resonus_meets_polar_vacuus") if a[k] != b[k]]
    if a["vacuus_arr"]["regions"] != b["vacuus_arr"]["regions"] or a["vacuus_arr"]["simplicial"] != b["vacuus_arr"]["simplicial"]: ks.append("vacuus arrangement counts")
    elif a["vacuus_arr"].get("region_sides") != b["vacuus_arr"].get("region_sides") or a["vacuus_arr"].get("point_multiplicities") != b["vacuus_arr"].get("point_multiplicities"):
        ks.append("vacuus arrangement: same counts, different region shapes or crossing points")
    if ks: diffJ.append((r["J"], ks))
say("Johnson solids whose Vacuus data differ between the two centres:", diffJ)
say("Johnson solids with equal centres:", [r["J"] for r in rows if r["family"] == "Johnson" and r["same_centre"]])

# ---- Resonus ∩ Vacuus
say("\nResonus ∩ Vacuus nonempty:")
for l, r, a in ALL:
    if a["both"]:
        say(f"  {l}: {a['both']} planes ({a['both_on_mirrors']} mirrors); " + "; ".join(f"{x['edges']} edge(s) on a plane parallel to faces {x['faces_parallel']}{' (mirror)' if x['mirror'] else ''}" for x in a["both_info"]))
say("count nonempty:", sum(1 for l, r, a in ALL if a["both"]), "of", len(ALL))
say("nonempty with no shared plane a mirror:", [l for l, r, a in ALL if a["both"] and not a["both_on_mirrors"]])

# ---- simplicial
for what in ("resonus", "vacuus"):
    say(f"\n{what} simplicial:")
    byfam = defaultdict(list)
    for l, r, a in ALL:
        if a[f"{what}_arr"]["simplicial"]: byfam[r["family"]].append(l)
    for f, ls in byfam.items(): say(f"  {f} ({len(ls)}):", ls)

# ---- prisms: Resonus always simplicial (a near pencil); Resonus ∩ Vacuus
pr = [(r["n"], r) for r in rows if r["family"] == "prism"]
assert all(r["resonus_arr"]["simplicial"] for n, r in pr)
say("\nprisms n=3..12: Resonus simplicial for all; Resonus ∩ Vacuus sizes:", [(n, r["both"]) for n, r in sorted(pr)])
for fam in ("antiprism", "bipyramid", "trapezohedron"):
    say(f"{fam}s: (n, Resonus planes, simplicial, both):", [(r["n"], r["resonus_planes"], r["resonus_arr"]["simplicial"], r["both"]) for r in sorted((r for r in rows if r["family"] == fam), key=lambda r: r["n"])])

# ---- duality
say("\nduality (P row): |Vac(P) ∩ Res(P*)|, |Res(P) ∩ Vac(P*)|, |Res(P*)| = corner lines of P, |Vac(P*)| = edge directions of P")
byname = {r["name"]: r for r in rows}
for r in rows:
    if "dual" in r and r["family"] in ("Platonic", "Archimedean", "prism", "antiprism"):
        d = byname[r["dual"]]
        assert d["resonus_planes"] == r["polar_resonus"] and d["vacuus_plates"] == r["polar_vacuus"]
        assert d["resonus_meets_polar_vacuus"] == r["vacuus_meets_polar_resonus"] and d["vacuus_meets_polar_resonus"] == r["resonus_meets_polar_vacuus"]
        say(f"  {r['name']} / {r['dual']}: Vac(P)∩Res(P*) {r['vacuus_meets_polar_resonus']}, Res(P)∩Vac(P*) {r['resonus_meets_polar_vacuus']},"
            f" Res(P*) {r['polar_resonus']} (V={r['V']}), Vac(P*) {r['polar_vacuus']} (E={r['E']})")
say("duality counts agree on both rows of every pair")

# ---- independent checks: mirror counts and plate counts against known values
GM = {"Td": 6, "Oh": 9, "Ih": 15, "O": 0, "I": 0}
for r in rows:
    if r["family"] in ("Platonic", "Platonic polar", "Archimedean", "Catalan"):
        assert r["mirrors"] == GM[r["group"]], r["name"]
    if r["family"] in ("prism", "bipyramid", "antiprism", "trapezohedron"):
        n = r["n"]; ev = n % 2 == 0
        if r["family"] in ("prism", "bipyramid"): m = 9 if n == 4 else n + 1
        else: m = 9 if n == 3 else n
        assert r["mirrors"] == m, r["name"]
        pred = {"prism": (3 * n // (2 if ev else 1), n // (2 if ev else 1) + 1),
                "antiprism": (4 * n // (1 if ev else 2), 2 * n // (1 if ev else 2) + 1),
                "bipyramid": (n // (2 if ev else 1) + 1, 2 * n // (2 if ev else 1)),
                "trapezohedron": (3 * n if ev else 2 * n, 2 * n if ev else n)}[r["family"]]
        if not (r["family"] == "antiprism" and n == 3) and not (r["family"] == "bipyramid" and n == 4) and not (r["family"] == "prism" and n == 4) and not (r["family"] == "trapezohedron" and n == 3):
            assert (r["vacuus_plates"], r["resonus_planes"]) == pred, (r["name"], r["vacuus_plates"], r["resonus_planes"], pred)
say("mirror counts equal the group's (Td 6, Oh 9, Ih 15, O and I 0; D_nh n+1, D_nd n; the cube and octahedron as prism-family members 9);"
    " prism-family plate and plane counts equal the closed forms (prism 3n or 3n/2 and n+1 or n/2+1; antiprism 2n or 4n and n+1 or 2n+1;"
    " bipyramid n+1 or n/2+1 and 2n or n; trapezohedron 2n or 3n and n or 2n; odd or even n; the 3- and 4-members that are Platonic excepted)")
PJ = {r["J"]: r for r in json.load(open(os.path.join(HERE, "../../2026-11-24-vacuus-enumeration/data/johnson-pilot.json")))}
for r in rows:
    if r["family"] == "Johnson":
        p = PJ[r["J"]]; a = r["corner"]
        assert a["mirrors"] == p["mirrors"] and a["vacuus_plates"] == p["plates"] and a["vacuus_kind"] == p["kind"], r["J"]
        assert a["centrally_symmetric"] == p["centrally_symmetric"]
say("Johnson: mirrors, plates, kind and central symmetry equal the independent floating-point pilot (full symmetry group by search) for all 92")

# ---- Johnson summary
J = [r for r in rows if r["family"] == "Johnson"]
assert len(J) == 92
say("\nJohnson kinds (corner centroid):", Counter(r["corner"]["vacuus_kind"] for r in J))
say("Johnson field degrees J84-J90:", {r["J"]: r.get("field_degree") for r in J if r["J"] >= 84 and r["J"] <= 90})
open(os.path.join(D, "patterns.txt"), "w").write("\n".join(out) + "\n")
print("FINAL ok patterns")
