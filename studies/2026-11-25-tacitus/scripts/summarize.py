# Tables for the README from data/*.jsonl (Tacitus census). Prints Markdown.
import json, glob, os, collections
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
L = lambda f: [json.loads(l) for l in open(os.path.join(D, f))]
poly = L("poly.jsonl"); fd = L("4d.jsonl"); aq = sum((L("aequi-%d.jsonl" % i) for i in range(3)), [])
assert len(poly) == 163 and len(aq) == 4553 + 1083 + 9490
fmt = lambda s: ",".join(map(str, s)) or "-"
print("## Polyhedra (unweighted i | solid-angle weighted ii); k <= 20\n")
print("| polyhedron | family | faces | |G| | silent (i) | beyond symmetry (i) | beyond (ii) |\n|---|---|---|---|---|---|---|")
for r in poly:
    if r["family"] in ("Platonic", "Archimedean", "Catalan") or r["i"]["beyond"] or r["ii"]["beyond"]:
        print("| %s | %s | %d | %d | %s | %s | %s |" % (r["name"], r["family"], r["N"], r["i"]["G"], fmt(r["i"]["silent"]),
              fmt(r["i"]["beyond"]), fmt(r["ii"]["beyond"])))
fam = collections.Counter(r["family"] for r in poly)
print("\nfamilies:", dict(fam), "| polyhedra with any silence beyond symmetry (i):", sum(bool(r["i"]["beyond"]) for r in poly),
      "(ii):", sum(bool(r["ii"]["beyond"]) for r in poly))
print("| (i) and (ii) silent sets differ for:", [r["name"] for r in poly if r["i"]["silent"] != r["ii"]["silent"]])
print("\n## Regular 4D polytopes (facet normals on S^3, Gegenbauer test)\n\n| polytope | normals | silent k <= 20 | beyond |\n|---|---|---|---|")
for r in fd: print("| %s | %d | %s | %s |" % (r["name"], r["N"], fmt(r["i"]["silent"]), fmt(r["i"]["beyond"])))
print("\n## Aequi (%d dice)\n" % len(aq))
tot = collections.Counter(r["family"] for r in aq); hit = collections.Counter(r["family"] for r in aq if r["i"]["beyond"])
for f in tot: print("- %s: %d dice, %d silent beyond symmetry" % (f, tot[f], hit[f]))
for t in ("1232", "4404", "cycle"):
    S = [r for r in aq if t in r["tags"]]; print("- tag %s: %d dice, %d beyond" % (t, len(S), sum(bool(r["i"]["beyond"]) for r in S)))
cat = collections.Counter(); byg = collections.Counter(); pat = collections.Counter(); ex = {}
for r in aq:
    for k, w in r["i"].get("why", {}).items(): cat[w] += 1
    if r["i"]["beyond"]:
        key = (r["group"], fmt(r["i"]["beyond"]), "".join(r["i"]["why"][str(k)] for k in r["i"]["beyond"]))
        pat[key] += 1; ex.setdefault(key, r["label"] + " [" + r["name"] + "]")
print("\nexplanations (die-degree pairs): E even, forced by X+(-X) symmetry %d; P pieces forced %d; S pieces silent %d; C cancellation %d"
      % (cat["E"], cat["P"], cat["S"], cat["C"]))
print("\n| group | beyond degrees | why | dice | example |\n|---|---|---|---|---|")
for key, n in sorted(pat.items(), key=lambda t: -t[1]): print("| %s | %s | %s | %d | %s |" % (*key, n, ex[key]))
grey = [(r["name"], v, r[v]["grey"]) for r in poly + aq + fd for v in ("i", "ii") if v in r and r[v]["grey"]]
mn = min(r[v]["min_nonzero"] for r in poly + aq for v in ("i", "ii") if v in r and r[v]["min_nonzero"])
print("\ngrey energies (1e-11..1e-8):", grey, "| smallest nonzero energy elsewhere: %.3g" % mn)
print("FINAL ok" if {g[0] for g in grey} <= {"triakis tetrahedron"} else "FINAL FAIL unexpected grey energies")
