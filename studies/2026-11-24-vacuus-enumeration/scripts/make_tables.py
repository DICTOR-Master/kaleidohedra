#!/usr/bin/env python3
"""Markdown tables for the README from the data files."""
import json
U = json.load(open("data/exact-uniform.json")); P = json.load(open("data/exact-prisms.json")); J = json.load(open("data/johnson-pilot.json"))
JX = {r["J"]: r for r in json.load(open("data/johnson-exact.json"))}; D4 = json.load(open("data/four-d.json"))
def pc(r):
    return "; ".join(f"{c['count']}×{c['edges_per_plate']} {c['sheet']}, {c['slice']}{' (mirror)' if c['mirror'] else ''}" for c in r["plate_classes"])
def fc(r):
    return "; ".join(f"{c['count']}×[{'+'.join(map(str, c['faces']))}], {c['slice']}{' (mirror)' if c['mirror'] else ''}" for c in r["face_plate_classes"])
o = []
o.append("### Table 1. Platonic, Archimedean, Catalan (exact)\n")
o.append("Vacuus plates (edge plates): count × edges on the plate, sheet kind, slice (the polygon the plate cuts from the solid). Face-parallel planes (a separate construction, NOT the Vacuus): count × [sides of the faces parallel to it], slice. Mirror = a mirror of the solid's full symmetry group.\n")
o.append("| solid | group | mirrors | centr. symm. | kind | Vacuus plates | plate classes | on mirrors | face-parallel planes (not Vacuus) | their classes |")
o.append("|---|---|---|---|---|---|---|---|---|---|")
for r in U:
    o.append(f"| {r['name']} | {r['group']} | {r['mirrors']} | {'yes' if r['centrally_symmetric'] else 'no'} | **{r['kind']}** | {r['plates']} | {pc(r)} | {r['plates_on_mirrors']} | {r['face_plates']} | {fc(r)} |")
o.append("\n### Table 2. Prisms, antiprisms (regular faces, unit circumradius base) and their duals, n = 3 to 12 (exact)\n")
o.append("| solid | mirrors | centr. symm. | kind | Vacuus plates | plate classes | face-parallel planes (not Vacuus) |")
o.append("|---|---|---|---|---|---|---|")
for r in P:
    o.append(f"| {r['name']} | {r['mirrors']} | {'yes' if r['centrally_symmetric'] else 'no'} | **{r['kind']}** | {r['plates']} | {pc(r)} | {r['face_plates']} |")
o.append("\n### Table 3. The 92 Johnson solids: exact for 85, floating-point pilot for J84-J90\n")
o.append("Symmetry centre: 'point' when the full symmetry group fixes only one point, 'axis/plane' when it fixes a line or plane. Centres: 'equal' when the corner centroid and the volume centroid coincide (exactly). Classes about the corner centroid: count × edges per plate, sheet, slice (M = on a mirror). 'Volume centroid' says what changes when the centre is the volume centroid instead.\n")
o.append("| J | solid | exact | group order | mirrors | symmetry centre | centres | kind | Vacuus plates | classes (corner centroid) | volume centroid |")
o.append("|---|---|---|---|---|---|---|---|---|---|---|")
def agg(cl):
    from collections import Counter
    c = Counter()
    for x in cl: c[(x["edges_per_plate"], x["sheet"], x["mirror"])] += x["count"]
    return sorted(c.items())
for r in J:
    nm = r["name"].split("_", 1)[1].replace("_", " ").lower(); x = JX.get(r["J"])
    if x:
        a, b = x["corner"], x["volume"]
        cl = "; ".join(f"{c['count']}×{c['edges_per_plate']} {c['sheet']} {c['slice']}{' M' if c['mirror'] else ''}" for c in a["plate_classes"])
        if x["same_centre"]: vc = "same centre"
        elif (a["kind"], a["plates"], agg(a["plate_classes"])) == (b["kind"], b["plates"], agg(b["plate_classes"])):
            vc = "same plates" + (" (slices differ)" if x["differ"] else "")
        else: vc = f"DIFFERS: {b['kind']}, {b['plates']} plates"
        o.append(f"| {r['J']} | {nm} | yes | {r['group_order']} | {a['mirrors']} | {'point' if r['unique_symmetry_centre'] else 'axis/plane'} | {'equal' if x['same_centre'] else 'differ'} | **{a['kind']}** | {a['plates']} | {cl} | {vc} |")
    else:
        cl = "; ".join(f"{c['count']}×{c['edges_per_plate']} {c['sheet']} {c['slice_sides']}-gon{' M' if c['mirror'] else ''}" for c in r["plate_classes"])
        o.append(f"| {r['J']} | {nm} | no (float) | {r['group_order']} | {r['mirrors']} | {'point' if r['unique_symmetry_centre'] else 'axis/plane'} | not computed | **{r['kind']}** | {r['plates']} | {cl} | not computed |")
o.append("\n### Table 4. 4D pilot (exact): plates of the Vacuus = hyperplanes through O spanned by the 2-faces\n")
o.append("| polytope | corners | cells | 2-faces | centr. symm. | kind | plates | classes (count × 2-faces per plate [their sides], sheet) | plates on mirrors |")
o.append("|---|---|---|---|---|---|---|---|---|")
for r in D4:
    cl = "; ".join(f"{c['count']}×{c['faces_per_plate']} [{c['face_sides']}] {c['sheet']}{' (mirror)' if c['mirror'] else ''}" for c in r["classes"])
    o.append(f"| {r['name']} | {r['corners']} | {r['cells']} | {r['two_faces']} | {'yes' if r['centrally_symmetric'] else 'no'} | **{r['kind']}** | {r['plates']} | {cl} | {r['plates_on_mirrors']} |")
open("data/tables.md", "w").write("\n".join(o) + "\n")
