#!/usr/bin/env python3
"""Plate-system coincidences between solids (exact keys within a shared field) and the CSV."""
import json, csv, itertools
U = json.load(open("data/exact-uniform.json")); Pz = json.load(open("data/exact-prisms.json"))
J = json.load(open("data/johnson-pilot.json"))
allx = U + Pz
def fieldgrp(r):
    if r["name"] in ("snub cube", "pentagonal icositetrahedron"): return "cube-snub"
    if r["name"] in ("snub dodecahedron", "pentagonal hexecontahedron"): return "ico-snub"
    return r["frame"]
out = []
for a, b in itertools.combinations(allx, 2):
    if fieldgrp(a) != fieldgrp(b): continue
    for la, ka in (("edge plates", "_plate_keys"), ("face plates", "_face_plate_keys")):
        for lb, kb in (("edge plates", "_plate_keys"), ("face plates", "_face_plate_keys")):
            if a[ka] == b[kb]:
                out.append(f"{a['name']} ({la}) = {b['name']} ({lb}): {len(a[ka])} plates")
# within one solid: edge plates = face plates
for a in allx:
    if a["_plate_keys"] == a["_face_plate_keys"]:
        out.append(f"{a['name']}: edge plates = face plates ({len(a['_plate_keys'])})")
# TID check: icosidodecahedron edge plates inside TID face plates
by = {r["name"]: r for r in U}
tid, idd = by["truncated icosidodecahedron"], by["icosidodecahedron"]
sub = set(idd["_plate_keys"]) <= set(tid["_face_plate_keys"])
out.append(f"CHECK icosidodecahedron's 6 edge plates are among the truncated icosidodecahedron's face plates: {sub}")
# snub floats vs others in their frame (inequality certified by float distance)
for s, fr in (("snub cube", "cube"), ("snub dodecahedron", "ico")):
    S = by[s]
    for r in U:
        if r["frame"] == fr and r["name"] != s and fieldgrp(r) == fr:
            common = set(map(tuple, S["_plate_float"])) & set(map(tuple, r["_plate_float"]))
            if common: out.append(f"{s} shares {len(common)} edge plate(s) with {r['name']} (float match, check exactly)")
open("data/coincidences.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
with open("data/vacuus-enumeration.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "solid", "exact", "V", "E", "F", "symmetry", "centrally_symmetric", "unique_symmetry_centre", "mirrors",
                "kind", "edge_plates", "edge_plate_classes (count x edges/plate sheet slice [M=mirror])", "edge_plates_on_mirrors",
                "face_plates", "face_plate_classes (count x faces slice [M])", "face_plates_on_mirrors"])
    for r in allx:
        pc = "; ".join(f"{c['count']}x{c['edges_per_plate']} {c['sheet']} {c['slice']}{' M' if c['mirror'] else ''}" for c in r["plate_classes"])
        fc = "; ".join(f"{c['count']}x{'+'.join(map(str, c['faces']))} {c['slice']}{' M' if c['mirror'] else ''}" for c in r["face_plate_classes"])
        w.writerow([r["family"], r["name"], "yes", r["V"], r["E"], r["F"], r.get("group", f"n={r.get('n')}"), r["centrally_symmetric"], True, r["mirrors"],
                    r["kind"], r["plates"], pc, r["plates_on_mirrors"], r["face_plates"], fc, r["face_plates_on_mirrors"]])
    for r in J:
        pc = "; ".join(f"{c['count']}x{c['edges_per_plate']} {c['sheet']} {c['slice_sides']}-gon{' M' if c['mirror'] else ''}" for c in r["plate_classes"])
        w.writerow(["Johnson", r["name"], "no (float pilot)", r["V"], r["E"], r["F"], f"order {r['group_order']}", r["centrally_symmetric"],
                    r["unique_symmetry_centre"], r["mirrors"], r["kind"], r["plates"], pc, sum(c["count"] for c in r["plate_classes"] if c["mirror"]), "", "", ""])
