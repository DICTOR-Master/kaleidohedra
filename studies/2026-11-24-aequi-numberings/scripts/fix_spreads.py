"""One-off correction (24 Nov 2026): the first runs stored the stage-1 corner spread; stage 2 can lower it. Set corner_spread to the
spread of the stored numbers (keeping the stage-1 value as corner_spread_stage1) and corner_status OPTIMAL iff it equals the bound."""
import json, glob, os, sys
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.json"))):
    r = json.load(open(f)); b = r["schemes"]["balanced"]
    if b.get("status") == "pending" or "corner_spread_stage1" in b: continue
    x = b["numbers"]; s = [sum(x[i] for i in v) for v in r["corner_faces"]]; a = max(s) - min(s)
    b["corner_spread_stage1"] = b["corner_spread"]; b["corner_spread"] = a
    b["corner_status"] = "OPTIMAL" if a == b["corner_spread_lower_bound"] else "FEASIBLE"
    json.dump(r, open(f + ".tmp", "w"), separators=(",", ":")); os.replace(f + ".tmp", f)
print("fixed")
