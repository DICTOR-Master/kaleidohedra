"""Tables for the README (one-structure study): reads data/shadows.json, yantra-sat.json, control-yantra-sat.json, internal.json,
a-items.json, yantra-degree.json; writes data/tables.md."""
import os, json
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
J = lambda n: json.load(open(os.path.join(STUDY, "data", n)))
sh = J("shadows.json"); sat = J("yantra-sat.json"); ctl = J("control-yantra-sat.json"); inn = J("internal.json")
A = J("a-items.json"); deg = J("yantra-degree.json")
L = []
h = lambda d: ", ".join(f"{k}:{v}" for k, v in sorted(d.items(), key=lambda kv: int(kv[0]))) if d else "–"
satk = {(r["polyhedron"], r["direction"]): r for r in sat}

L.append("## B1. Symmetric directions (3D skeletons: edges + struts)\n")
L.append("| polyhedron | direction | lines | marmas (by number of lines) | mixed points | lines through the centre | largest parallel class | pencil test |")
L.append("|---|---|---|---|---|---|---|---|")
for s in sh["shadows"]:
    if s["kind"] != "symmetric": continue
    L.append(f"| {s['polyhedron']} | {s['direction']} | {s['lines']} | {s['marmas']} ({h(s['marma_hist'])}) | {s['mixed_points']} | {s['centre_lines']} | {s['max_parallel']} | {'pass' if s['yantra_test']['pass'] else 'fail'} |")

L.append("\n## B1. Dense scan: every primitive integer direction with coordinates up to %d\n" % sh["nscan"])
L.append("| polyhedron | corners | edges | directions | with a marma | most marmas | at | pencil-test passes |")
L.append("|---|---|---|---|---|---|---|---|")
by = defaultdict(list)
for s in sh["shadows"]:
    if s["kind"] == "scan": by[s["polyhedron"]].append(s)
for m in sh["meta"]:
    ss = by[m["polyhedron"]]
    best = max(ss, key=lambda s: s["marmas"])
    L.append(f"| {m['polyhedron']} | {m['corners']} | {m['edges']} | {len(ss)} | {sum(1 for s in ss if s['marmas'])} | {best['marmas']} | {best['direction'] if best['marmas'] else '–'} | {sum(1 for s in ss if s['yantra_test']['pass'])} |")

L.append("\n## B1. 4D Queens (edges + struts), orthographic onto a plane\n")
L.append("| polytope | plane | lines | marmas (by number of lines) | mixed points | lines through the centre | pencil test | exhaustive search (SAT) |")
L.append("|---|---|---|---|---|---|---|---|")
for s in sh["shadows"]:
    if s["kind"] != "4D": continue
    r = satk.get((s["polyhedron"], s["direction"]))
    sv = "–" if r is None else ("no map (UNSAT)" if r["sat"] is False else ("MAP FOUND" if r["sat"] else "undecided: " + r.get("why", "")))
    L.append(f"| {s['polyhedron']} | {s['direction']} | {s['lines']} | {s['marmas']} ({h(s['marma_hist'])}) | {s['mixed_points']} | {s['centre_lines']} | {'pass' if s['yantra_test']['pass'] else 'fail'} | {sv} |")
L.append("\nAll pencil-test passes and their search results:\n")
L.append("| shadow | result | variables | clauses | seconds |")
L.append("|---|---|---|---|---|")
for r in ctl + sat:
    res = "UNSAT (no map)" if r["sat"] is False else ("SAT (map found)" if r["sat"] else "undecided")
    L.append(f"| {r['polyhedron']} / {r['direction']} | {res} {r.get('why', '')} | {r.get('vars', '–')} | {r.get('clauses', '–')} | {r['secs']} |")

import glob
pen = {}
for fn in sorted(glob.glob(os.path.join(STUDY, "data/yantra-sat-pencils-*.json"))):
    for r in json.load(open(fn)):
        for row in r["rows"]:
            c = row["pencil"]
            if c not in pen or pen[c]["sat"] is None: pen[c] = row
if pen:
    L.append("\nThe 600-cell Coxeter plane split by pencil (the bases lie in exactly one pencil, so the instance is the union):\n")
    L.append(f"pencils {len(pen)}; UNSAT {sum(r['sat'] is False for r in pen.values())}; SAT {sum(bool(r['sat']) for r in pen.values())}; "
             f"undecided {sum(r['sat'] is None for r in pen.values())} {[c for c, r in sorted(pen.items()) if r['sat'] is None]}")

L.append("\n## B2. Internal crossings (struts S, face diagonals FD, space diagonals SD, plate lines PL)\n")
L.append("| polyhedron | Vacuus plates | plate lines | lines at O | inside: points by number of lines | inside marmas (3+) | boundary: points by number of lines | densest inside point(s) |")
L.append("|---|---|---|---|---|---|---|---|")
for r in sorted(inn, key=lambda r: r.get("corners", 999)):
    if r["capped"]:
        L.append(f"| {r['polyhedron']} | capped ({r['candidate_pairs_over']} candidate pairs) | | | | | | |"); continue
    ins = [p for p in r["patterns"] if p["where"] == "inside"]
    top = max((p["lines"] for p in ins), default=0)
    tops = "; ".join(f"{p['points']} × {top} lines ({', '.join(f'{k} {v}' for k, v in p['families'].items())})" for p in ins if p["lines"] == top) or "–"
    L.append(f"| {r['polyhedron']} | {r['vacuus_plates']} | {r['plate_lines']} | {r['centre']['lines'] if r['centre'] else 0} | {h(r['inside_points_by_lines'])} | {r['inside_marmas']} | {h(r['boundary_points_by_lines'])} | {tops} |")

L.append("\n## A. Exact checks (a-items.json, yantra-degree.json)\n")
L.append("```")
L.append(json.dumps({"A2a": A["A2a"], "A2b": A["A2b"]}, indent=1))
L.append(json.dumps(A["A3"], indent=1, ensure_ascii=False))
L.append(json.dumps(deg, indent=1))
L.append("```")
open(os.path.join(STUDY, "data/tables.md"), "w").write("\n".join(L) + "\n")
print("FINAL ok summarize", flush=True)
