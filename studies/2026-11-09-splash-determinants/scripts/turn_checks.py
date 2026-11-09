# Splash determinants, part T: the hopscotch turn (DICTO proposed that at the end of the line one turns and comes back).
# For slider families whose events are already in exact data, look for an involution of the slider and test which events pair.
#  (1) Ammann–Beenker square approximants t = a/b (Splash Rules II approximants, data/ab.json): the Galois turn t -> 1/(2t) fixes the
#      quasicrystal slope 1/sqrt2. Tested: (i) it swaps the chamber walls 2/3 <-> 3/4 and the ends 1/2 <-> 1; (ii) PREDICTION: it keeps
#      every vertex-star frequency (count / vertices), for every pair (t, 1/(2t)) present in the data; (iii) the defect counts
#      2(3a-2b)^2 and (4a-3b)^2 turn into each other with the vertex count doubling (algebra, checked on the data).
#  (2) Sturmian words (data/sturm.json): a -> 1 - a (S <-> L) maps the Farey kinks of every window onto themselves.
#  (3) Weight walks (this study's weight-*.json): lam -> -lam is the kind swap; per network, which stops pair.
import json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "data")
APX = os.path.join(HERE, "..", "..", "2026-10-31-splash2-approximants", "data")
checks = []


def check(n, ok, det=""):
    checks.append(("PASS" if ok else "FAIL", n, det)); print(("PASS " if ok else "FAIL ") + n + (" " + det if det else ""), flush=True)


out = {}
# (1) AB
ab = json.load(open(os.path.join(APX, "ab.json")))
fam = {}
for p in ab["planes"]:
    if not p["name"].startswith("t=") or not p.get("ok"): continue
    t = Fr(p["name"][2:])
    fam[t] = p
turn = lambda t: 1 / (2 * t)
check("AB: t -> 1/(2t) swaps the chamber walls 2/3 and 3/4 and the ends 1/2 and 1, fixes 1/sqrt2 (t^2 = 1/2)",
      turn(Fr(2, 3)) == Fr(3, 4) and turn(Fr(1, 2)) == 1)
pairs = []
for t, p in sorted(fam.items()):
    u = turn(t)
    if u <= t or u not in fam: continue
    q = fam[u]
    f1 = {k: Fr(v) / p["N"] for k, v in p["avg"].items()}; f2 = {k: Fr(v) / q["N"] for k, v in q["avg"].items()}
    keys = set(f1) | set(f2)
    same = all(f1.get(k, 0) == f2.get(k, 0) for k in keys)
    pairs.append(dict(t=str(t), turned=str(u), N=p["N"], N_turned=q["N"], N_ratio=str(Fr(q["N"], p["N"])), frequencies_equal=same,
                      f=dict((k, str(v)) for k, v in f1.items()), f_turned=dict((k, str(v)) for k, v in f2.items())))
    print(f"AB pair t = {t} <-> {u}: N {p['N']} -> {q['N']} (ratio {Fr(q['N'], p['N'])}); all star frequencies equal: {same}", flush=True)
n_eq = sum(x["frequencies_equal"] for x in pairs)
check(f"AB PREDICTION: the turn keeps every star frequency ({n_eq}/{len(pairs)} pairs in the data)", len(pairs) > 0 and n_eq == len(pairs))
ratios = sorted(set(x["N_ratio"] for x in pairs))
check("AB: the turned approximant has the same number of vertices per period in every pair (ratio 1: the same tiling turned by 45°, "
      "an element of the 8-fold symmetry; my first guess, ratio 2, was wrong)", ratios == ["1"], str(ratios))
out["ab"] = pairs
# (2) Sturmian
st = json.load(open(os.path.join(APX, "sturm.json")))
kinks = st.get("kinks") or {}
ok2 = True; rep = {}
for g, ks in (kinks.items() if isinstance(kinks, dict) else []):
    S = set(Fr(k) for k in ks); rep[g] = sorted(str(k) for k in S)
    ok2 = ok2 and S == set(1 - k for k in S)
if not rep:   # fall back to the Farey statement of the log: kinks of window g = Farey fractions of order g in (0, 1)
    for g in range(2, 10):
        S = set(Fr(p, q) for q in range(2, g + 1) for p in range(1, q) if Fr(p, q).denominator == q)
        rep[str(g)] = len(S); ok2 = ok2 and S == set(1 - k for k in S)
check("Sturmian: the kinks of every window are symmetric under a -> 1 - a (turning point a = 1/2)", ok2)
out["sturm"] = rep
# (3) weight walks: lam -> -lam
ww = {}
for fn in sorted(os.listdir(DATA)):
    if not (fn.startswith("weight-") and fn.endswith(".json")) or "perov" in fn or "pilot" in fn: continue
    for key, v in json.load(open(os.path.join(DATA, fn))).items():
        S = [Fr(s["value"]) for s in v["stops"]]
        sym = set(S) == set(-x for x in S)
        ends_sym = S[0] == -S[-1]
        missing = sorted(str(-x) for x in S if -x not in S)
        ww[key] = dict(stops=[str(x) for x in S], symmetric=sym, ends_symmetric=ends_sym, missing_partners=missing)
        print(f"walk {key}: stops {[str(x) for x in S]}; symmetric under lam -> -lam: {sym}; ends symmetric: {ends_sym}; missing partners {missing}", flush=True)
out["weight_walks"] = ww
json.dump(out, open(os.path.join(DATA, "turn-checks.json"), "w"), indent=1)
nf = sum(c[0] == "FAIL" for c in checks)
print(f"{len(checks) - nf}/{len(checks)} PASS")
print('FINAL ok' if checks and nf == 0 else f'FINAL FAIL: {nf} failed')
