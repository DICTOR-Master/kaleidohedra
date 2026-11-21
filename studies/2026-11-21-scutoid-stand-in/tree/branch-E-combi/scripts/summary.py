"""Branch E summary: reads ../data/combi_*.json, re-checks each claimed partition record, prints the table.
FINAL ok only if every run claimed valid has exact volume gap 0, no problems, sampling with 0 miscounted points, and at least one run is valid."""
import glob, json, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
rows, okall, nvalid = [], True, 0
order = {"bcc_1": 0, "bcc_6-5": 1, "sc_1": 2, "fcc_1": 3}
files = sorted(glob.glob(os.path.join(D, "combi_*.json")), key=lambda f: (order.get("_".join(os.path.basename(f)[6:-5].split("_")[:2]), 9), f))
for f in files:
    r = json.load(open(f))
    line = f"{r['lattice']:4s} {r['factor']:>4s} s0  seeds {r['seeds']:5s}  "
    if r["valid"]:
        nvalid += 1
        good = r.get("volume_gap") == "0" and not r.get("problems") and r.get("sampling", {}).get("miscounted", 1) == 0
        okall &= good
        line += (f"PARTITION  scutoid pieces {r['n_scutoid_pieces']:2d}/80  kinds {r['n_kinds']}  Y vertices {r['n_Y']}  "
                 f"157.7612 {'present' if r['lambda_present'] else 'absent'}  facets per kind {[k['n_facets'] for k in r['kinds']]}"
                 f"  sampling {r['sampling']['points']} pts ok" + ("" if good else "  RECHECK FAILED"))
    else:
        line += f"not valid: {r['why'][:150]}"
    rows.append(line)
print("\n".join(rows))
print("FINAL ok" if okall and nvalid > 0 else "FINAL FAIL")
