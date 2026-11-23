"""Checks for the Aequi numberings (24 Nov 2026).  Usage: python checks.py STUDYDIR  -> prints FINAL ok or FAIL lines.
Independent of numberings.py: the face lattice is rebuilt here from the picker's own float data (src/dice.json: directions and
12-digit depths) and must give the same corners (as sets of faces) as the stored one.  Then, in integers, for every die:
 every scheme is a bijection faces -> 1..N; plain = 1..N; opposite present iff centrally symmetric (classification CSV) and each
 face + its exactly opposite face (picker directions negated) sum to N + 1; balanced: the stored corner and neighbour spreads are
 the spreads of its numbers, bound <= value, OPTIMAL only with bound = value; spin_down: consecutive numbers on faces sharing an
 edge, and N next to 1 when it says cycle.  Names: distinct, rule reproduced, every name parses back to exactly its number."""
import csv, json, os, sys, itertools
import numpy as np
S = sys.argv[1]
D = json.load(open(os.path.join(S, "src/dice.json")))
ROWS = {int(r["n"]): r for r in csv.DictReader(open(os.path.join(S, "../2026-11-24-aequi-vacuus-scutoids/data/aequi_classification.csv")))}
sys.path.insert(0, os.path.join(S, "scripts"))
READ = {0: ["o", "re", "maru"], 1: ["i", "hi"], 2: ["ni", "fu"], 3: ["mi", "sa"], 4: ["yo", "shi"], 5: ["go", "ko"],
        6: ["mu", "ro"], 7: ["na"], 8: ["ya", "ha"], 9: ["ku"]}
SYL = {s: d for d, rs in READ.items() for s in rs}
def parses(w):
    w = w.lower(); out = []
    def go(i, acc):
        if i == len(w): out.append(acc); return
        for s, d in SYL.items():
            if w.startswith(s, i): go(i + len(s), acc + str(d))
    go(0, ""); return out
def rule(n):
    o = []
    for ch in str(n):
        rs = READ[int(ch)]; s = rs[0]
        if o and s == o[-1] and len(rs) > 1: s = rs[1]
        o.append(s)
    w = "".join(o); return w[0].upper() + w[1:]
def float_corners(e):
    nf, df = [], []
    for k, oi in enumerate(e["o"]):
        for i in D["groups"][e["g"]][oi]["dirs"]: nf.append(D["dirs"][i]); df.append(e["d"][k])
    nf = np.array(nf); df = np.array(df); N = len(df); C = set()
    for a, b, c in itertools.combinations(range(N), 3):
        A = nf[[a, b, c]]
        if abs(np.linalg.det(A)) < 1e-9: continue
        x = np.linalg.solve(A, df[[a, b, c]]); s = nf @ x - df
        if s.max() < 1e-8: C.add(frozenset(np.nonzero(np.abs(s) < 1e-7)[0].tolist()))
    return C, nf
bad = []; cnt = {"dice": 0, "opposite": 0, "balanced_opt": 0, "balanced_both_opt": 0, "cycle": 0, "path": 0}
names = {}
for n in range(1, len(D["dice"]) + 1):
    fn = os.path.join(S, "data/dice/%04d.json" % n)
    if not os.path.exists(fn): bad.append((n, "missing")); continue
    r = json.load(open(fn)); e = D["dice"][n - 1]; N = e["N"]; cnt["dice"] += 1
    def err(m): bad.append((n, m))
    C, nf = float_corners(e)
    if C != set(frozenset(v) for v in r["corner_faces"]) or len(C) != e["c"]: err("corners differ from the float rebuild")
    edges = set()
    for f in r["face_vertices"]:
        for t in range(len(f)): edges.add(frozenset((f[t], f[(t + 1) % len(f)])))
    cf = r["corner_faces"]; adj = set()
    for ed in edges:
        a, b = tuple(ed); two = set(cf[a]) & set(cf[b])
        if len(two) != 2: err("edge not on two faces")
        adj.add(frozenset(two))
    nb = [[g for g in range(N) if frozenset((f, g)) in adj] for f in range(N)]
    sch = r["schemes"]
    for k in ("plain", "spin_down") + (("balanced",) if sch["balanced"].get("status") != "pending" else ()) + (("opposite",) if sch["opposite"]["available"] else ()):
        if sorted(sch[k]["numbers"]) != list(range(1, N + 1)): err(k + " not a bijection")
    if sch["plain"]["numbers"] != list(range(1, N + 1)): err("plain")
    cs = ROWS[n]["centrally_symmetric"] == "True"
    if sch["opposite"]["available"] != cs: err("opposite availability")
    if cs:
        cnt["opposite"] += 1; num = sch["opposite"]["numbers"]
        for i in range(N):
            j = [k for k in range(N) if np.abs(nf[k] + nf[i]).max() < 1e-9]
            if len(j) != 1 or num[i] + num[j[0]] != N + 1: err("opposite sum")
    b = sch["balanced"]
    if b.get("status") == "pending": cnt["balanced_pending"] = cnt.get("balanced_pending", 0) + 1
    else:
        x = b["numbers"]
        sv = [sum(x[f] for f in v) for v in cf]; sn = [sum(x[g] for g in nb[f]) for f in range(N)]
        if max(sv) - min(sv) != b["corner_spread"] or max(sn) - min(sn) != b["neighbour_spread"]: err("balanced spreads")
        if b["corner_spread_lower_bound"] > b["corner_spread"] or b["neighbour_spread_lower_bound"] > b["neighbour_spread"]: err("bound above value")
        if (b["corner_status"] == "OPTIMAL") != (b["corner_spread_lower_bound"] == b["corner_spread"]): err("corner status vs bound")
        if b["neighbour_status"] == "OPTIMAL" and b["neighbour_spread_lower_bound"] != b["neighbour_spread"]: err("neighbour status vs bound")
        cnt["balanced_opt"] += b["corner_status"] == "OPTIMAL"; cnt["balanced_both_opt"] += b["corner_status"] == "OPTIMAL" and b["neighbour_status"] == "OPTIMAL"
    s = sch["spin_down"]; pos = {v: f for f, v in enumerate(s["numbers"])}
    for k in range(1, N):
        if frozenset((pos[k], pos[k + 1])) not in adj: err("spin-down step %d" % k)
    if s["kind"] == "cycle" and frozenset((pos[N], pos[1])) not in adj: err("spin-down cycle close")
    cnt[s["kind"]] += 1
    if r["name"] != rule(n) or parses(r["name"]) != [str(n)]: err("name")
    names[r["name"]] = n
if len(names) != cnt["dice"]: bad.append((0, "names not distinct"))
print(cnt)
for b_ in bad[:50]: print("FAIL", b_)
print("FINAL ok" if not bad and cnt["dice"] == len(D["dice"]) and not cnt.get("balanced_pending") else "FAIL %d problems" % len(bad))
