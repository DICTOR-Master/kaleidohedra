#!/usr/bin/env python3
"""One table for the paper (CSV + Markdown) from data/catalogue-all.json.

One row per solid. Johnson solids: values about the corner centroid; the column 'volume centroid' says
'same' when every Vacuus and Resonus column is equal about the volume centroid, else lists what changes."""
import json, os, csv
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "../data")
rows = json.load(open(os.path.join(D, "catalogue-all.json")))
FAM = ["Platonic", "Platonic polar", "Archimedean", "Catalan", "prism", "bipyramid", "antiprism", "trapezohedron", "Johnson"]
ORDER_P = ["dodecahedron", "icosahedron", "cube", "tetrahedron", "octahedron"]   # D, I, C, T, O

def key(r):
    f = FAM.index(r["family"])
    if r["family"] == "Platonic": return (f, ORDER_P.index(r["name"]), 0)
    if r["family"] == "Platonic polar": return (f, ORDER_P.index(r["dual"]), 0)
    if r["family"] == "Johnson": return (f, r["J"], 0)
    return (f, r.get("n", 0), r["name"])

COLS = ["V", "E", "F", "centrally_symmetric", "mirrors", "vacuus_plates", "vacuus_full", "vacuus_shared", "vacuus_single", "vacuus_kind",
        "vacuus_on_mirrors", "vacuus_regions", "vacuus_simplicial", "resonus_planes", "resonus_two_faces", "resonus_one_face",
        "resonus_on_mirrors", "resonus_regions", "resonus_simplicial", "both", "both_on_mirrors",
        "vacuus_meets_polar_resonus", "resonus_meets_polar_vacuus"]

def flat(a):
    o = {c: a[c] for c in COLS if c in a}
    o["vacuus_regions"] = a["vacuus_arr"]["regions"]; o["vacuus_simplicial"] = a["vacuus_arr"]["simplicial"]
    o["resonus_regions"] = a["resonus_arr"]["regions"]; o["resonus_simplicial"] = a["resonus_arr"]["simplicial"]
    o["vacuus_sphere"] = f"{a['vacuus_arr'].get('sphere_V')}/{a['vacuus_arr'].get('sphere_E')}/{a['vacuus_arr']['regions']}"
    o["resonus_sphere"] = f"{a['resonus_arr'].get('sphere_V')}/{a['resonus_arr'].get('sphere_E')}/{a['resonus_arr']['regions']}"
    return o

out = []
rows = [r for r in rows if r["family"] != "Platonic polar"]   # the polars of the Platonic solids are Platonic solids again (kept in the JSON)
for r in sorted(rows, key=key):
    if r["family"] == "Johnson":
        a, b = flat(r["corner"]), flat(r["volume"])
        diff = [c for c in a if a[c] != b[c]]
        o = {"family": "Johnson", "solid": f"J{r['J']} " + r["name"].split("_", 1)[1].replace("_", " ").lower(), **a,
             "centres_equal": r["same_centre"], "volume_centroid": "same" if not diff else "; ".join(f"{c} {b[c]}" for c in diff)}
    else:
        o = {"family": r["family"], "solid": r["name"], **flat(r), "centres_equal": "", "volume_centroid": ""}
    out.append(o)
fields = ["family", "solid"] + COLS[:11] + ["vacuus_simplicial", "vacuus_sphere"] + COLS[13:18] + ["resonus_simplicial", "resonus_sphere"] + COLS[19:] + ["centres_equal", "volume_centroid"]
fields = [f for f in fields if f not in ("vacuus_regions", "resonus_regions")]
with open(os.path.join(D, "vacuus-resonus-catalogue.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader()
    for o in out: w.writerow({k: o.get(k, "") for k in fields})

yn = lambda x: "yes" if x is True else ("no" if x is False else str(x))
md = ["| family | solid | V | E | F | c.s. | mirrors | Vacuus plates (full+shared+single) | kind | on mirrors | sphere V/E/regions | simpl. | Resonus planes (2-face+1-face) | on mirrors | sphere V/E/regions | simpl. | R∩V (mirrors) | V(P)∩R(P*) | R(P)∩V(P*) | volume centroid |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for o in out:
    md.append(f"| {o['family']} | {o['solid']} | {o['V']} | {o['E']} | {o['F']} | {yn(o['centrally_symmetric'])} | {o['mirrors']} | "
              f"{o['vacuus_plates']} ({o['vacuus_full']}+{o['vacuus_shared']}+{o['vacuus_single']}) | {o['vacuus_kind']} | {o['vacuus_on_mirrors']} | "
              f"{o['vacuus_sphere']} | {yn(o['vacuus_simplicial'])} | {o['resonus_planes']} ({o['resonus_two_faces']}+{o['resonus_one_face']}) | "
              f"{o['resonus_on_mirrors']} | {o['resonus_sphere']} | {yn(o['resonus_simplicial'])} | {o['both']} ({o['both_on_mirrors']}) | "
              f"{o['vacuus_meets_polar_resonus']} | {o['resonus_meets_polar_vacuus']} | {o['volume_centroid'] or ''} |")
open(os.path.join(D, "vacuus-resonus-catalogue.md"), "w").write("\n".join(md) + "\n")
print("rows", len(out))
print("FINAL ok table" if len(out) == len(rows) else "row count mismatch")
