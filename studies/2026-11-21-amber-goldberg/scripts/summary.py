"""Table of all runs (data/amber_*.json) + combinatorial counts per core: face orbits under T_h (T for chiral cores), number of
hexagon-hexagon edges whose midpoint lies on a 2-fold axis (coordinate axes and their icosahedral images: the 15 axes through the
icosahedron's edge midpoints), and whether a 2-fold axis passes through a hexagon centre instead.  Ends FINAL ok only if every run file
was read, every valid run has 0 volume gap within 1e-40 and 0 sampling miscounts, and every run's face count equals 10T + 2."""
import glob, gzip, json, os, re, sys, itertools
import numpy as np
sys.argv = [sys.argv[0], "GP_1_0"]; os.environ["SOLIDS_FAST"] = "1"   # counts only (the runs themselves checked convexity)
here = os.path.dirname(os.path.abspath(__file__))
rows, ok = {}, True
for f in sorted(glob.glob(os.path.join(here, "../data/amber_GP*_bcc_*_cen.json*"))):
    r = json.load(gzip.open(f) if f.endswith(".gz") else open(f)); m = re.match(r"(GPc?)_(\d+)_(\d+)", r["solid"]); form, a, b = m.group(1), int(m.group(2)), int(m.group(3))
    T = a*a + a*b + b*b
    if r["n_faces"] != 10*T + 2: ok = False; print("face count wrong", f)
    if r["valid"]:
        if abs(float(r["volume_gap"])) > 1e-40 or r["sampling"]["miscounted"] != 0: ok = False; print("check failed", f)
    rows[(form, T, a, b, r["factor"])] = r
phi = (1 + 5**.5)/2
ax = []                                              # 2-fold axes: through the edge midpoints of the icosahedron cyc(0, +-1, +-phi)
ico = []
for s1, s2 in itertools.product((1, -1), repeat=2):
    for c in range(3):
        v = [0, s1, s2*phi]; ico.append(np.array([v[(i - c) % 3] for i in range(3)]))
for i, j in itertools.combinations(range(12), 2):
    if abs(np.linalg.norm(ico[i] - ico[j]) - 2) < 1e-9:
        u = (ico[i] + ico[j]); u /= np.linalg.norm(u)
        if not any(abs(abs(u @ w) - 1) < 1e-9 for w in ax): ax.append(u)
assert len(ax) == 15
def combi(a, b):
    import importlib, resin
    resin.TH = [g for g in resin.TH_FULL if g[1].count(-1) % 2 == 0] if 0 < b < a else resin.TH_FULL
    import solids; importlib.reload(solids)
    S = solids.build(f"GP_{a}_{b}"); V = np.array([[float(x) for x in v] for v in S["V"]])
    E = {}
    for fi, (f, k) in enumerate(S["faces"]):
        for i in range(len(f)): E.setdefault(frozenset((f[i], f[(i+1) % len(f)])), []).append(k)
    on = lambda p: any(np.linalg.norm(np.cross(p/np.linalg.norm(p), u)) < 1e-9 for u in ax)
    hh = sum(1 for e, ks in E.items() if ks == ["hex", "hex"] and on(V[list(e)].mean(0)))
    pp = sum(1 for e, ks in E.items() if ks == ["pent", "pent"] and on(V[list(e)].mean(0)))
    hc = sum(1 for f, k in S["faces"] if on(V[f].mean(0)))
    orb, seen = 0, set()
    P = [tuple(np.round([float(x) for x in n], 9)) for n, c in S["planes"]]; idx = {p: i for i, p in enumerate(P)}
    for i in range(len(P)):
        if i in seen: continue
        orb += 1
        for g in resin.TH: seen.add(idx[tuple(np.round([float(x) for x in resin.act(g, list(S["planes"][i][0]))], 9))])
    return dict(hexhex_on_2fold=hh, pentpent_on_2fold=pp, faces_on_2fold=hc, orbits=orb)
cache = {}
print("| form | GP(m,n) | T | faces | face orbits (T_h; T if chiral) | hex-hex edges on 2-fold axes | faces centred on 2-fold axes | s | valid | kinds | scutoids | Y | why (if not valid) |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for key in sorted(rows):
    form, T, a, b, fac = key; r = rows[key]
    if (a, b) not in cache: cache[(a, b)] = combi(a, b)
    c = cache[(a, b)]
    s = "s0" if fac == "1" else "6/5 s0"
    if r["valid"]:
        print(f"| {form} | ({a},{b}) | {T} | {r['n_faces']} | {c['orbits']} | {c['hexhex_on_2fold'] + c['pentpent_on_2fold']} | {c['faces_on_2fold']} | {s} | yes | {r['n_kinds']} | {r['n_scutoid_pieces']} | {r['n_Y']} | |")
    else:
        print(f"| {form} | ({a},{b}) | {T} | {r['n_faces']} | {c['orbits']} | {c['hexhex_on_2fold'] + c['pentpent_on_2fold']} | {c['faces_on_2fold']} | {s} | no | | | | {r['why'][:90]} |")
nv = sum(1 for r in rows.values() if r["valid"]); ny = sum(r.get("n_Y", 0) or 0 for r in rows.values() if r["valid"]); ns = sum(r.get("n_scutoid_pieces", 0) or 0 for r in rows.values() if r["valid"])
print(f"runs {len(rows)}, valid {nv}, total Y over valid runs {ny}, total scutoid pieces over valid runs {ns}")
print("FINAL ok" if ok and rows else "FINAL FAIL")
