# Exact weight walks of the two control networks (hbn, sodalite) with the relay census's own engine and checks (#53 [S]).
# Output: ../data/<key>-walk.json, ../data/<key>-walk-checks.txt.  Usage: python walks.py [hbn] [sodalite]
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "2026-10-25-relay-census", "scripts"))
import extra_nets  # noqa: E402,F401
from networks import NETS  # noqa: E402
from census import Census  # noqa: E402

allc = []
for key in sys.argv[1:] or ["hbn", "sodalite"]:
    C = Census(key); d = C.walk()
    for e in NETS[key].get("expect", []):
        C.expect(*e)
    d["checks"] = C.checks; allc += C.checks
    json.dump(d, open(os.path.join(HERE, "..", "data", f"{key}-walk.json"), "w"), indent=1, default=str)
    with open(os.path.join(HERE, "..", "data", f"{key}-walk-checks.txt"), "w") as fh:
        for s, n, det in C.checks: fh.write(f"{s} {n} {det}\n")
    print(f"== {key}: intervals {[(r['lo'], r['hi']) for r in d['intervals']]}", flush=True)
    for r in d["intervals"] + d["stops"]:
        tag = r.get("lam") or f"({r['lo']}, {r['hi']})"
        print("  ", tag, [(s["kind"], s.get("bonds"), s.get("orbits")) for s in r["sites"][:2]], flush=True)
nf = sum(1 for c in allc if c[0] == "FAIL")
print('FINAL ok' if allc and nf == 0 else f'FINAL FAIL: {nf} of {len(allc)} checks failed')
