#!/usr/bin/env python3
"""Which (bottom, top, Y) combinations occur among the resin pieces we already made (amber-cell sweep, Amber-Ammann,
Aequi cells)? bottom = sides of the core face (Nin or sides_in), top = mould-side side count (Nout or sides_out),
Y = Y vertices of the piece, convex = no dihedral angle over 180 degrees (field 'convex' where the study stored it).
Reads the stored JSON only (no recomputation)."""
import json, glob, os, sys, collections
R = os.path.expanduser("~/k-research/studies")
src = [("sweep", "2026-11-21-amber-cell-sweep/data/amber_*.json"), ("ammann", "2026-11-21-amber-ammann/data/ammann_*.json"),
       ("aequi", "2026-11-24-aequi-vacuus-scutoids/data/cells/amber_*.json")]
rows = []; tally = collections.Counter(); law_bad = 0; nonconvex = 0; total = 0
for tag, pat in src:
    for f in sorted(glob.glob(os.path.join(R, pat))):
        d = json.load(open(f))
        if not d.get("valid"):
            continue
        for k in d.get("kinds", []):
            n = k.get("sides_in", len(k["Nin"])); m = k.get("sides_out", len(k["Nout"])); y = k["Y"]
            cv = k.get("convex")
            if cv is None:
                cv = max(k["angles"]) <= 180 + 1e-6
            bent = any(179.0 < a < 181.0 and abs(a - 180) > 1e-6 for a in k["angles"])
            law = abs(n - m) <= y and (n - m - y) % 2 == 0
            total += 1; nonconvex += (not cv); law_bad += (not law)
            lo, hi = sorted((n, m))
            tally[(lo, hi, y, bool(cv))] += len(k.get("members", [1]))
            rows.append(dict(source=tag, file=os.path.basename(f), kind=k["kind"], F=k["F"], bottom=n, top=m, Y=y, convex=bool(cv),
                             near_flat_fold=bent, parity_law=law, per_cell=len(k.get("members", [])) or None))
json.dump(dict(rows=rows), open(sys.argv[1], "w"), indent=0)
print("kinds (with repeats over cells):", total, " non-convex:", nonconvex, " breaking |n-m|<=Y, n-m=Y mod 2:", law_bad)
print("small end, large end, Y, convex -> pieces (members summed over all valid cells)")
for key in sorted(tally):
    print("  ", key, tally[key])
good = total > 0 and len(rows) == total
print("FINAL ok" if good else "FINAL FAIL (no kinds read)")
sys.exit(0 if good else 1)
