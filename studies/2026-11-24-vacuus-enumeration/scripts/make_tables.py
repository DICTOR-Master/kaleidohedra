#!/usr/bin/env python3
"""Markdown tables for the README from the data files."""
import json
U = json.load(open("data/exact-uniform.json")); P = json.load(open("data/exact-prisms.json")); J = json.load(open("data/johnson-pilot.json"))
def pc(r):
    return "; ".join(f"{c['count']}×{c['edges_per_plate']} {c['sheet']}, {c['slice']}{' (mirror)' if c['mirror'] else ''}" for c in r["plate_classes"])
def fc(r):
    return "; ".join(f"{c['count']}×[{'+'.join(map(str, c['faces']))}], {c['slice']}{' (mirror)' if c['mirror'] else ''}" for c in r["face_plate_classes"])
o = []
o.append("### Table 1. Platonic, Archimedean, Catalan (exact)\n")
o.append("Edge plates: count × edges on the plate, sheet kind, slice (the solid cut by the plate). Face plates: count × [sides of the faces parallel to it], slice. Mirror = the plate is a mirror of the solid's full symmetry group.\n")
o.append("| solid | group | mirrors | centr. symm. | kind | edge plates | edge-plate classes | on mirrors | face plates | face-plate classes |")
o.append("|---|---|---|---|---|---|---|---|---|---|")
for r in U:
    o.append(f"| {r['name']} | {r['group']} | {r['mirrors']} | {'yes' if r['centrally_symmetric'] else 'no'} | **{r['kind']}** | {r['plates']} | {pc(r)} | {r['plates_on_mirrors']} | {r['face_plates']} | {fc(r)} |")
o.append("\n### Table 2. Prisms, antiprisms (regular faces, unit circumradius base) and their duals, n = 3 to 12 (exact)\n")
o.append("| solid | mirrors | centr. symm. | kind | edge plates | edge-plate classes | face plates |")
o.append("|---|---|---|---|---|---|---|")
for r in P:
    o.append(f"| {r['name']} | {r['mirrors']} | {'yes' if r['centrally_symmetric'] else 'no'} | **{r['kind']}** | {r['plates']} | {pc(r)} | {r['face_plates']} |")
o.append("\n### Table 3. The 92 Johnson solids (FLOAT PILOT, not exact; O = corner centroid)\n")
o.append("Symmetry centre: 'point' when the full symmetry group fixes only O; 'axis/plane' when it fixes a line or plane (C_nv, C_s), so O is fixed only by the corner-centroid convention. Classes: count × edges per plate, sheet, slice sides (M = on a mirror).\n")
o.append("| J | solid | group order | mirrors | symmetry centre | kind | edge plates | classes |")
o.append("|---|---|---|---|---|---|---|---|")
for r in J:
    nm = r["name"].split("_", 1)[1].replace("_", " ").lower()
    cl = "; ".join(f"{c['count']}×{c['edges_per_plate']} {c['sheet']} {c['slice_sides']}-gon{' M' if c['mirror'] else ''}" for c in r["plate_classes"])
    o.append(f"| {r['J']} | {nm} | {r['group_order']} | {r['mirrors']} | {'point' if r['unique_symmetry_centre'] else 'axis/plane'} | **{r['kind']}** | {r['plates']} | {cl} |")
open("data/tables.md", "w").write("\n".join(o) + "\n")
