# Bond Relay, part C (floats, cross-check only): the app's own pieces and web (data/raw/app-dump.json, from app_dump.mjs) against
# the exact results of parts A/B. C1 frame/scale: the app's T(x) and Delian pieces are the study's pieces (golden x (phi/2), Delian
# x 1/sqrt2); C2 every app bond's area = the closed form; C3 bond types present per parameter (the float findings); C4 bonds per
# interior piece. Output: ../data/checks/app-checks.txt.
import json, math
from itertools import permutations, product
PHI = (1 + 5 ** 0.5) / 2; R2 = 0.5 ** 0.5
d = json.load(open("../data/raw/app-dump.json"))
checks = []
def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail)); print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""))
def close_sets(A, B, tol=1e-9):
    return len(A) == len(B) and all(min(math.dist(a, b) for b in B) < tol for a in A)
def T(u):
    return {tuple(sg[i] * p[i] * PHI / 2 for i in range(3)) for p in set(permutations((1, u, 0))) for sg in product((1, -1), repeat=3)}
GX = {"0": 0, "1/3": 1 / 3, "1/2": .5, "1": 1, "2": 2, "3": 3, "tau": PHI, "1/tau": 1 / PHI, "sqrt2": 2 ** .5, "inf": math.inf}
for k, x in GX.items():
    g = d["golden"][k]; s = 1.0 if x == math.inf else x / (1 + x)
    check(f"golden x={k}: C1 app T(x), T(1/x) = study pieces (phi/2 frame)", close_sets([tuple(v) for v in g["big"]], T(s)) and close_sets([tuple(v) for v in g["small"]], T(1 - s)))
    kind = {}
    okf = True
    for role, n, a in g["pieces"]:
        okf &= all(abs(a[i] - n[i] * PHI / 2) < 1e-12 for i in range(3)) and ((role == "gsBig") == all(c % 2 == 0 for c in n))
        kind[tuple(round(c, 6) for c in a)] = "big" if role == "gsBig" else "small"
    check(f"golden x={k}: C1 sites: big on even n, small on odd n, at n phi/2", okf)
    F = {"big-big": PHI ** 2 * s * s / 2, "small-small": PHI ** 2 * (1 - s) ** 2 / 2, "big-small": 3 ** .5 / 8 * PHI ** 2 * (1 + 2 * s - 2 * s * s)}
    err, types, per = 0, {}, {}
    for A, B, area in g["web"]:
        ka, kb = kind[tuple(round(c, 6) for c in A)], kind[tuple(round(c, 6) for c in B)]; typ = "-".join(sorted((ka, kb)))
        err = max(err, abs(area - F[typ])); types[typ] = types.get(typ, 0) + 1
        for P in (A, B): per.setdefault(tuple(round(c, 6) for c in P), {}).setdefault(typ, 0); per[tuple(round(c, 6) for c in P)][typ] += 1
    check(f"golden x={k}: C2 every app bond area = closed form", err < 1e-9, f"max err {err:.1e}; types {types}")
    exp = {"big": {"big-small": 8, **({"big-big": 6} if s > 0 else {})}, "small": {"big-small": 8, **({"small-small": 6} if s < 1 else {})}}
    inner = [p for p in per if math.hypot(*p) < 0.6]  # the central piece(s): all neighbours present
    check(f"golden x={k}: C4 bonds of the central piece", all(per[p] == exp[kind[p]] for p in inner) and inner, str({kind[p]: per[p] for p in inner}))
    if k == "1": check("golden x=1: C3 float finding: big-big = small-small = 0.3273", abs(F["big-big"] - 0.3273) < 5e-5 and abs(F["small-small"] - F["big-big"]) < 1e-15)
    if k == "tau": check("golden x=tau: C3 float finding: big-big 0.5000, small-small 0.1910", abs(F["big-big"] - .5) < 5e-5 and abs(F["small-small"] - .1910) < 5e-5)
ST = {"stop:rd": 0, "stop:equilateralRd": (2 * 6 ** .5 - 3) / 15, "stop:octet": 1 / 3, "stop:half": 1 - 6 ** (1 / 3) / 3, "stop:delian": 1 - (2 / 3) * 2 ** (-1 / 3),
      "stop:equilateralCube": 5 / 3 - (2 / 3) * 2 ** .5, "stop:cube": 1}
for k, g in d["delian"].items():
    t = g["t"]; a = 1.5 * (1 - t)
    if k in ST: check(f"delian {k}: C1 app stop value = exact stop", abs(t - ST[k]) < 1e-15)
    F = {"oct-tet": (9 * 3 ** .5 / 4 * t * t) if t <= 1 / 3 else (3 ** .5 / 4 * a * a), "oct-oct": 2 ** .5 / 4 * (1 - 9 * t * t), "tet-tet": (1 - a * a) / 2}
    kind, okf = {}, True
    for role, c, A, nv in g["pieces"]:
        okf &= all(abs(A[i] - c[i] * R2) < 1e-12 for i in range(3))
        okf &= (role == "dlTet") == all(abs(z % 1 - .5) < 1e-12 for z in c)
        kind[tuple(round(z, 6) for z in A)] = "tet" if role == "dlTet" else "oct"
    check(f"delian t={k}: C1 sites: tet pieces at cube centres, oct pieces at odd points, x 1/sqrt2", okf)
    err, types, per = 0, {}, {}
    for A, B, area in g["web"]:
        ka, kb = kind[tuple(round(z, 6) for z in A)], kind[tuple(round(z, 6) for z in B)]; typ = "-".join(sorted((ka, kb)))
        err = max(err, abs(area - F[typ])); types[typ] = types.get(typ, 0) + 1
        for P in (A, B): per.setdefault(tuple(round(z, 6) for z in P), {}).setdefault(typ, 0); per[tuple(round(z, 6) for z in P)][typ] += 1
    check(f"delian t={k}: C2 every app bond area = closed form", err < 1e-9, f"max err {err:.1e}; types {sorted(types)}")
    want = ({"oct-oct"} if t == 0 else {"oct-oct", "oct-tet"} if t < 1 / 3 - 1e-12 else {"oct-tet"} if abs(t - 1 / 3) < 1e-12 else {"tet-tet"} if t == 1 else {"oct-tet", "tet-tet"})
    check(f"delian t={k}: C3 float finding: bond types {sorted(want)}", set(types) == want)
    expo = {} if t == 1 else ({"oct-oct": 12} if t == 0 else {"oct-oct": 12, "oct-tet": 8} if t < 1 / 3 - 1e-12 else {"oct-tet": 8})
    expt = {} if t == 0 else ({"tet-tet": 6} if t == 1 else {"oct-tet": 4} if t <= 1 / 3 + 1e-12 else {"oct-tet": 4, "tet-tet": 6})
    pc = [p for p in per if math.hypot(*[z / R2 for z in p]) < 1.01]
    okc = all(per[p] == (expo if kind[p] == "oct" else expt) for p in pc) and pc
    check(f"delian t={k}: C4 bonds of the central pieces", okc, str(sorted({(kind[p], json.dumps(per[p], sort_keys=True)) for p in pc})))
with open("../data/checks/app-checks.txt", "w") as f:
    for c in checks: f.write("  ".join(c) + "\n")
    f.write(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL\n")
print(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL")
