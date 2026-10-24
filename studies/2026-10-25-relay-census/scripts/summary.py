# Summary of the census runs: per network, the intervals (bond types, coordination per kind, cell signature, dual cells) and stops.
import json, sys, glob, os
from collections import Counter
for f in sys.argv[1:] or sorted(glob.glob("../data/raw/*.json")):
    d = json.load(open(f))
    if "intervals" not in d: continue
    print(f"\n#### {d['key']}: {d['name']}  lam = {d['lam']}  [{d['units']}]")
    rows = [("iv", r) for r in d["intervals"]] + [("stop", r) for r in d["stops"]]
    rows.sort(key=lambda x: eval(x[1]["lo"] if x[0] == "iv" else x[1]["lam"], {}) + (0.5 if x[0] == "iv" else 0) * 0)
    from fractions import Fraction as Fr
    def keyf(x):
        if x[0] == "stop": return (Fr(x[1]["lam"]), 0)
        return (Fr(x[1]["lo"]), 1)
    rows.sort(key=keyf)
    for t, r in rows:
        lab = f"({r['lo']}, {r['hi']})" if t == "iv" else f"= {r['lam']}"
        sig = Counter()
        for s in r["sites"]:
            if s.get("vanished"): sig[(s["kind"], "point")] += 1; continue
            fs = Counter(s["face_sizes"]); fsz = ",".join(f"{v}x{k}" for k, v in sorted(fs.items())) if len(s.get("face_sizes", [])) and max(s["face_sizes"]) > 2 else f"{s['corners']}-gon"
            sig[(s["kind"], f"{s['faces']}f [{fsz}] bonds {s['bonds']}")] += 1
        print(f"  {t:4} lam {lab:18} types {r['bond_types']}")
        for (k, sg), n in sorted(sig.items()): print(f"        {k} x{n}: {sg}")
        if r.get("dual"): print(f"        dual corners: {r['dual']}")
        if t == "iv":
            for s in r["sites"][:]:
                pass
            seen = set()
            for s in r["sites"]:
                if s["kind"] in seen: continue
                seen.add(s["kind"]); print(f"        {s['kind']} area^2: {s['area2']}  vol: {s['volume']}")
