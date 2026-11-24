"""Step (3): which Aequi have their Resonus inside the 31 planes of the H3 permutahedron, and does any depth ratio of such a die equal a
step of the stellation cycle (a phi-power times the depth ratio of I_k, D_k, RT_k or the uniform H3 permutahedron)?
Inputs (read only): study 2026-11-19-aequi-complete data/dice/*.json (4553 dice, depths to 60 digits) and study
2026-11-24-aequi-certify-extend data/certify*.jsonl.gz (the extension's dice, certified enclosures of radius 1e-44).
High precision with Python's decimal module (70 digits). -> data/aequi.json"""
import glob, gzip, json, os, re, sys
from decimal import Decimal as D, getcontext
getcontext().prec = 70
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, "../..")
S5 = D(5).sqrt(); PHI = (1 + S5) / 2; LPHI = PHI.ln()
def q5(a, b): return D(a.numerator) / D(a.denominator) + D(b.numerator) / D(b.denominator) * S5
from fractions import Fraction as Fr
# station face depths, squared (exact values from cycle.py, data/cycle.json): I0 inradius^2 (3-fold), D0 inradius^2 (5-fold),
# RT0 = hull of I0 + D0: rhombi through the midsphere points, depth^2 = phi^2 (2-fold); uniform H3 permutahedron depths^2
cyc = {"3": q5(Fr(7, 6), Fr(1, 2)), "5": None, "2": q5(Fr(3, 2), Fr(1, 2))}
cyc["5"] = (q5(Fr(3, 2), Fr(1, 2)) ** 2) / q5(Fr(5, 2), Fr(1, 2))
per = {"2": q5(Fr(27, 2), Fr(7, 2)), "3": q5(Fr(21, 2), Fr(9, 2)), "5": q5(Fr(25, 2), Fr(5, 2))}
assert abs(cyc["3"] - (PHI ** 4) / 3) < D(10) ** -60
base = {t: [cyc[t].sqrt(), per[t].sqrt()] for t in "235"}
TYPE = {"C6": "2", "RT24": "2", "O8": "3", "I12": "3", "D12": "5", "RD12": "c", "C6p": "2", "RT24p": "2", "O8p": "3", "I12p": "3", "D12p": "5"}
def fams(label): return [p for p in label.split("/")[0].split("+")]

def targets(ta, tb):
    return [x / y for x in base[ta] for y in base[tb]] if ta != tb else [D(1)] + [x / y for x in base[ta] for y in base[tb]]

def miss(q, ta, tb):
    """distance of log_phi(q / target) to the nearest integer, minimised over the targets"""
    best = None
    for t in targets(ta, tb):
        x = (q / t).ln() / LPHI; m = abs(x - x.to_integral_value())
        if best is None or m < best[0]: best = (m, t, int(x.to_integral_value()))
    return best

def frame(label):
    F = [f for l in label for f in fams(l)]
    if any(f.startswith("RD12") for f in F): return "cube-RD12"
    pr = any(f.endswith("p") for f in F); un = any(f in ("D12", "I12", "RT24") for f in F)
    return "both" if (pr and un) else "primed31" if pr else "31"

def test(depths, orbits):
    """depths per orbit (Decimal), orbit labels; returns smallest miss over all pairs of (orbit, axis type)"""
    items = []; equal.clear()
    for d, o in zip(depths, orbits):
        for t in sorted({TYPE[f] for f in fams(o)}): items.append((d, t, o))
    best = None
    for i in range(len(items)):
        for j in range(len(items)):
            if i == j: continue
            (da, ta, oa), (db, tb, ob) = items[i], items[j]
            if oa == ob and ta == tb: continue
            m = miss(da / db, ta, tb)
            if ta == tb and m[2] == 0 and m[1] == 1 and m[0] < D(10) ** -30:
                equal.append((oa, ob)); continue          # two orbits at the same depth: recorded apart, not a cycle step
            if best is None or m[0] < best[0]: best = (m[0], oa, ob, ta, tb, m[2], str(m[1])[:14])
    return best

rows = []; counts = {}; equal = []; nequal = []
for f in sorted(glob.glob(os.path.join(ST, "2026-11-19-aequi-complete/data/dice/*.json"))):
    d = json.load(open(f)); fr = frame(d["orbits"]); key = ("4553", d["group"], fr); counts[key] = counts.get(key, 0) + 1
    if fr in ("31", "primed31"):
        b = test([D(x) for x in d["depths_60_digits"]], d["orbits"])
        if equal: nequal.append(("4553", d["sid"], d["label"]))
        rows.append(dict(src="4553", id=d["sid"], label=d["label"], group=d["group"], best=b))
enc = re.compile(r"\[([-0-9.e]+) \+/- ([0-9.e-]+)\]")
for f in sorted(glob.glob(os.path.join(ST, "2026-11-24-aequi-certify-extend/data/certify*.jsonl.gz"))):
    batch = os.path.basename(f)[7:-9]
    for line in gzip.open(f, "rt"):
        d = json.loads(line)
        if d.get("status") != "certified": continue
        lab = d["label"].split(": ", 1)[1]; orbits = [o.strip() for o in lab.split(" + ")]
        fr = frame(orbits); key = ("ext " + batch, d["group"], fr); counts[key] = counts.get(key, 0) + 1
        if fr in ("31", "primed31"):
            t = eval(d["tight"]) if isinstance(d["tight"], str) else d["tight"]
            dep = [D(1)] + [D(enc.match(s).group(1)) for s in t["enclosure"]][:len(orbits) - 1]   # orbit 0 is the unit; the enclosure lists orbits 1..m-1 (fixed 25 Nov: the first run dropped the 1 and shifted the labels)
            b = test(dep, orbits)
            if equal: nequal.append(("ext " + batch, d["sid"], d["label"]))
            rows.append(dict(src="ext " + batch, id=d["sid"], label=d["label"], group=d["group"], best=b))
hits = [r for r in rows if r["best"] is not None and r["best"][0] < D(10) ** -30]
near = sorted(rows, key=lambda r: r["best"][0] if r["best"] else D(1))[:10]
out = dict(counts={" | ".join(k): v for k, v in sorted(counts.items())},
           dice_with_resonus_in_31=len(rows), dice_with_two_orbits_of_one_axis_type_at_equal_depth=len(nequal), equal_depth_dice=nequal, coincidences=[dict(r, best=[str(x) for x in r["best"]]) for r in hits],
           nearest_ten=[dict(r, best=[str(r["best"][0])[:12]] + [str(x) for x in r["best"][1:]]) for r in near])
json.dump(out, open(os.path.join(HERE, "../data/aequi.json"), "w"), indent=1)
print(json.dumps(out["counts"], indent=0)); print("in 31:", len(rows), "coincidences:", len(hits), "equal-depth dice:", len(nequal))
for r in out["nearest_ten"]: print(r)
print("FINAL ok" if len(rows) > 0 else "FINAL none tested")
