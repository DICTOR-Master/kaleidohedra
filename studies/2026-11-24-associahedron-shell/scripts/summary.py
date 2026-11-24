#!/usr/bin/env python3
"""Tables for the README from data/shell-<type>.json (no new computation)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "../data")
lines = []
for typ in ("A3", "B3", "H3"):
    p = os.path.join(D, f"shell-{typ}.json")
    if not os.path.exists(p): continue
    d = json.load(open(p))
    for c, r in d["results"].items():
        for rule, x in r["rules"].items():
            rows = x["rows"]
            disj = sum(1 for w in rows if w["ends_meet_vertices"] == 0)
            tiers = "; ".join(f"{k}: {v}" for k, v in sorted(x["tiers"].items()))
            edge_change = sum(1 for w in rows if w["face_sides"] != w["outer_edges"])
            ok = all(x["checks"].values())
            lines.append(f"| {typ} | {c} | {rule} | {x['pieces']} | {r['rim_edges']} | {len(r['components'])} | {x['with_Y']} | "
                         f"{x['neighbours_change']} | {edge_change} | {disj} | {tiers} | {'yes' if ok else 'NO'} |")
print("| group | c | rule | pieces | rim edges | shell parts | pieces with a Y-corner | neighbours change | "
      "side count changes by edges (bent outer end) | ends disjoint | classification | exact checks |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
print("\n".join(lines))
