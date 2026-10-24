# Markdown tables for the README from ../data/raw/*.json (no computation; formatting only).
import json
from fractions import Fraction as Fr
from collections import Counter
NAMES = ["square", "honeycomb", "kagome", "bcc", "delian", "nacl", "zincblende", "hcpholes", "a15", "c15"]
def fs(s):
    if s.get("vanished"): return "point"
    if max(s["face_sizes"]) <= 2: return f"{s['corners']}-gon"
    c = Counter(s["face_sizes"]); return "+".join(f"{v}×{k}" for k, v in sorted(c.items()))
def bd(s): return "" if s.get("vanished") else ", ".join(f"{v} {k}" for k, v in s["bonds"].items())
for key in NAMES:
    d = json.load(open(f"../data/raw/{key}.json"))
    rows = [(Fr(r["lam"]), 0, r["lam"], r) for r in d["stops"]] + [(Fr(r["lo"]), 1, f"({r['lo']}, {r['hi']})", r) for r in d["intervals"]]
    rows.sort(key=lambda x: (x[0], x[1]))
    print(f"\n**{key}** — {d['name']}; λ = {d['lam']}; {d['units']}\n")
    kinds = d["kinds"]
    print("| λ | bond types | " + " | ".join(f"{k} cell (faces) | {k} bonds" for k in kinds) + " |")
    print("|---|---|" + "---|---|" * len(kinds))
    for _, _, lab, r in rows:
        cells = []
        for k in kinds:
            ss = [s for s in r["sites"] if s["kind"] == k]; sig = sorted(set((fs(s), bd(s)) for s in ss))
            cells.append(" / ".join(a for a, b in sig) + " | " + " / ".join(b for a, b in sig))
        print(f"| {lab} | {', '.join(r['bond_types'])} | " + " | ".join(cells) + " |")
