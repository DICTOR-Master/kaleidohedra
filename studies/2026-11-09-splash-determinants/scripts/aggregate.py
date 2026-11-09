# Splash determinants, part A: the events table, the coverage map and the hopscotch turn.
# DICTO proposed reading the splash patterns for coverage: the areas where local rules suffice for now; DICTO proposed that at the
# end of the line one turns and comes back (the hopscotch turn). Reads every data file of this study, adds the events already
# computed exactly in earlier studies (each with its own exact factor check here, in sympy), and writes
#   data/events.csv, data/events.json, data/coverage.json, data/sfam-lines.json, figures/splash-coverage.png, figures/s-lambda.png
import json, os, csv, sys
from fractions import Fraction as Fr
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "data"); FIG = os.path.join(HERE, "..", "figures")
os.makedirs(FIG, exist_ok=True)
checks = []


def check(n, ok, det=""):
    checks.append(("PASS" if ok else "FAIL", n, det)); print(("PASS " if ok else "FAIL ") + n + (" " + det if det else ""), flush=True)


rows = []
STATUS = {"circuit": "covered: circuit determinant (exact witness here)", "metric": "covered: metric linear factor (exact here)",
          "turn": "covered: turned event (incidence of the polar partner)", "form": "covered by form (linear in the slider; exact in its source study, not re-derived)",
          "partial": "partial: factor read from data, circuit not identified", "critical": "NOT covered: critical point (derivative zero), no determinant factor",
          "harmonic": "NOT covered: harmonic zero of degree > 2, no determinant factor",
          "turnpoint": "covered by the hopscotch turn: fixed point of the slider's involution (no determinant root)"}


def add(family, group, quadric, slider, event, value, status, factor, source, lo=None, hi=None, turn=""):
    v = sp.nsimplify(value) if not isinstance(value, sp.Basic) else value
    rows.append(dict(family=family, group=group, quadric=quadric, slider=slider, event=event, value=str(v), value_float=float(sp.N(v)),
                     status=status, status_text=STATUS[status], factor=factor, source=source, range_lo=lo, range_hi=hi, turn=turn))


SRC_W = {"square": "#53", "honeycomb": "#53", "kagome": "#53", "bcc": "#53 (CsCl; golden DICTONIC loop)", "delian": "#53 (fluorite; Delian DICTONIC loop)",
         "nacl": "#53", "zincblende": "#53", "hcpholes": "#53 (hcp holes)", "a15": "#53", "c15": "#53", "hbn": "switch-theorem study (control)",
         "sodalite": "switch-theorem study (control)"}
# ---------- weight walks (paraboloid)
sfam = {}
for fn in sorted(os.listdir(DATA)):
    if not (fn.startswith("weight-") and fn.endswith(".json")) or fn in ("weight-pilot.json",) or "perov" in fn: continue
    for key, v in json.load(open(os.path.join(DATA, fn))).items():
        st = v["stops"]; lo, hi = Fr(st[0]["value"]), Fr(st[-1]["value"])
        if key.startswith("h57_"):
            fam = f"#57 holes {v['word']} (d² = {v['s']}·2/3)"; src = "#57" if v["s"] == "1" else "Splash Rules run 1"
            if "predict" in fn: src = "this study (prediction test)"
            sfam.setdefault(v["word"], {})[v["s"]] = v
        elif key.startswith("py_"):
            fam = f"#60 pyrochlore {key[3:]}"; src = "#60"
        else:
            fam = {"square": "square + centres", "honeycomb": "honeycomb + centres", "kagome": "kagome + centres", "bcc": "CsCl / bcc (golden loop)",
                   "delian": "fluorite (Delian loop)", "nacl": "rock salt", "zincblende": "zinc blende", "hcpholes": "hcp holes", "a15": "A15", "c15": "C15 Laves",
                   "hbn": "h-BN", "sodalite": "sodalite Si/Al"}.get(key, key) + " (#53 web of bonds)"; src = SRC_W.get(key, "#53")
        S = set(Fr(s["value"]) for s in st)
        for s in st:
            w = s["witness"]; L = Fr(s["value"])
            fac = f"S0 − λ·S_A = {w['S0']} − λ·({w['S'][0]}), circuit {''.join(k[0] for k in w['kinds'])}, dual cell {w['cell_sites']} sites" if w else "none found"
            if w: assert Fr(w["S0"]) / Fr(w["S"][0]) == L
            turn = "λ → −λ partner present" if -L in S else f"partner {-L} absent"
            add(fam, "weight λ", "paraboloid", "λ = w_A − w_B", s["where"], sp.Rational(L.numerator, L.denominator),
                "circuit" if s["covered"] else "partial", fac, src, float(lo), float(hi), turn)
# perovskite: one row per wall line (segments merged)
pv = json.load(open(os.path.join(DATA, "weight-perov.json")))["perovskite"]["segments"]
lines = {}
for sg in pv:
    c = tuple(Fr(x) for x in sg["line"]); k = next(x for x in c[1:] if x != 0); c = tuple(x / k for x in c)
    lines.setdefault(c, []).append(sg)
for c, sgs in lines.items():
    ok = all(s["covered"] for s in sgs); w = sgs[0]["witness"]
    lbl = f"{c[0]} + {c[1]}λ + {c[2]}μ = 0".replace("+ -", "− ")
    add("perovskite ABX3 (λ, μ)", "two weights (λ, μ)", "paraboloid", "(λ, μ) = (w_A − w_X, w_B − w_X)", f"wall line {lbl} ({len(sgs)} segments)",
        0, "circuit" if ok else "partial", f"S0 − λS_A − μS_B = {w['S0']} − λ({w['S'][0]}) − μ({w['S'][1]}), circuit {''.join(w['kinds'])}", "#53 (perovskite chamber map)")
# ---------- sweeps (sphere quadric), unit-normal parameter m; for the cube family also mu = sqrt3 m (#81, octahedral-constant study)
sw = json.load(open(os.path.join(DATA, "sweep-events.json")))
NAMES = {"tetra": "tetrahedron sweep T ∩ m(−T)", "cube": "cube–octahedron sweep (μ = √3·m)", "dodeca": "dodecahedron–icosahedron sweep"}
for name, d in sw.items():
    fam = NAMES[name]; ev = d["events"]
    lo = min(e["m_float"] for e in ev); hi = max(e["m_float"] for e in ev)
    evm = [sp.sympify(e["m"]) for e in ev]
    for e, mval in zip(ev, evm):
        partner = any(abs(float(sp.N(mval * f)) - 1) < 1e-12 for f in evm)
        add(fam, "scale m", "sphere", "m (corner planes at distance m, faces at 1)", "incidence (face lattice changes)" if e["change"] else "incidence (no change)",
            mval, "circuit", f"4-plane determinant affine in m: {e['det_factor']}; min. poly {e['minpoly']}", "this study; #81 / octahedral-constant",
            lo, hi, "turn partner 1/m is an event of S" if partner else "turn partner 1/m is an event of S^∨ only (t_min kink)")
    for k, g in d["golden"].items():
        add(fam, "scale m", "sphere", "m", f"golden cut {k}", sp.sympify(g["m"]) if len(g["m"]) < 400 else sp.Float(g["m_float"], 15),
            "metric", f"edge ratio − φ: linear in m; min. poly {g['minpoly']}", "#88 (golden cuts), as S(m) = P ∩ m·P*", lo, hi,
            "partner golden" if any(x["partner_is_golden_cut"] for x in d["turn"]["golden_pairs"] if x["cut"] == k) else "no golden partner")
    for kk in d["tmin"]["kinks"]:
        mv = kk["nearest_event_or_turned_event"]
        if any(abs(mv - e["m_float"]) < 1e-9 for e in ev): continue
        add(fam, "scale m", "sphere", "m", "t_min kink = turned incidence event (event of S^∨)", sp.Float(mv, 12), "turn",
            "incidence determinant of S^∨ = S(1/m): root 1/m* of an S event m*", "octahedral-constant (3/2 on the cube sweep); this study", lo, hi, "pairs with 1/m")
    add(fam, "scale m", "sphere", "m", "turning point m = 1: t_min maximal, = R(S(1))²", 1, "turnpoint",
        f"fixed point of the core turn m → 1/m; t_min(1) = {d['tmin']['at_turning_point'][:80]} (min. poly {d['tmin']['at_turning_point_minpoly']})",
        "this study (prediction, 3/3 families)", lo, hi, "turning point")
# ---------- events from earlier studies, each with its factor checked here
mu, t, lam, a = sp.symbols('mu t lam a')
# tetra sweep (study 2026-11-04-tetra-sweep): same parameter as m
f = 4 * (mu ** 3 - 9 * mu ** 2 + 27 * mu - 11) / (3 * mu)
crit = [r for r in sp.solve(sp.diff(f, mu), mu) if r.is_real and r > 0]
ms = (11 - sp.sqrt(33)) / 4
check("tetra sweep: on 1 ≤ μ ≤ 3 the Mahler derivative vanishes at (11 − √33)/4 (root of 2μ² − 11μ + 11); the maximum at 1/μ* is its turn (S(1/μ) = −S(μ)/μ)",
      any(sp.simplify(r - ms) == 0 for r in crit) and sp.expand(sp.numer(sp.together(sp.diff(f, mu))) / 4 - (mu + 1) * (2 * mu ** 2 - 11 * mu + 11)) == 0)
dehn = 6 * a * (1 - 4 * (3 - mu) / 4)
check("tetra sweep: Dehn coefficient 6a(1 − 4t), t = (3 − μ)/4, is linear in μ with root 2", sp.solve(dehn, mu) == [2])
add("tetrahedron sweep T ∩ m(−T)", "scale m", "sphere", "m", "Dehn invariant zero", 2, "metric", "6a(1 − 4t) = 6a(μ − 2): linear", "tetra-sweep study", 1 / 3, 3, "partner 1/2 (Dehn zero of the turned member, same solid scaled)")
add("tetrahedron sweep T ∩ m(−T)", "scale m", "sphere", "m", "Mahler volume maximum", ms, "critical", "root of 2μ² − 11μ + 11 (derivative), not a determinant", "tetra-sweep study", 1 / 3, 3, "pairs with 1/μ* (also a maximum)")
add("tetrahedron sweep T ∩ m(−T)", "scale m", "sphere", "m", "isoperimetric maximum (octahedron)", 1, "turnpoint", "derivative zero at the turning point", "tetra-sweep study", 1 / 3, 3, "turning point")
# CO sweep: Q4 zero at Icosaxes mu = phi = golden cut of the octahedron
phi = (1 + sp.sqrt(5)) / 2
gold_oct = sp.sympify(sw["cube"]["golden"]["P* 3-gon x_G"]["m"]) * sp.sqrt(3)
check("cube–octahedron sweep: the octahedron's golden cut x_G sits at μ = φ (Icosaxes, where Q4 vanishes)", sp.simplify(gold_oct - phi) == 0)
add("cube–octahedron sweep (μ = √3·m)", "scale m", "sphere", "m", "harmonic Q4 = 0 (Icosaxes, μ = φ)", phi / sp.sqrt(3), "metric",
    "falls on the golden-cut factor of the octahedron (x_G); why Q4 vanishes there is open", "harmonic-fingerprint study; #59", None, None, "")
# CO ∩ mu RD
cr = json.load(open(os.path.join(DATA, "corrd-events.json")))
for e in cr["events"]:
    add("CO ∩ μ·RD sweep", "scale μ", "sphere (three plane families)", "μ", "incidence (face lattice changes)", sp.Rational(e["mu"]), "circuit",
        "4-plane determinant affine in μ (exact, Q)", "co-rd-sweep study; this study", 1, 2, "no turn (polar not in the family)")
add("CO ∩ μ·RD sweep", "scale μ", "sphere (three plane families)", "μ", "Dehn invariant zero", sp.Rational(5, 3), "partial",
    "Dehn coefficient linear in μ on (3/2, 2) (edge lengths affine); root 5/3 from the source, factor not re-derived", "Concordance ledger 4 Nov", 1, 2, "")
x0 = sp.Symbol('x0')
q4 = 1 + sp.sqrt((6 * sp.sqrt(30) - 31) / 17)
check("CO ∩ μ·RD: Q4 zero μ0 = 1 + sqrt((6√30 − 31)/17) is a root of 17a⁴ + 62a² − 7 (a = μ0 − 1), degree 4", sp.simplify(17 * (q4 - 1) ** 4 + 62 * (q4 - 1) ** 2 - 7) == 0)
add("CO ∩ μ·RD sweep", "scale μ", "sphere (three plane families)", "μ", "harmonic Q4 = 0", q4, "harmonic", "17a⁴ + 62a² − 7 = 0, a = μ − 1: degree 4, no linear factor", "co-rd-sweep study", 1, 2, "")
# #43 scale slider t: S ⊂ t·P(S) starts at t_min = (R/r)^2 for the five solids: vertex-on-plane incidence, linear in t
for nm, val in [("tetrahedron", 9), ("cube", 3), ("octahedron", 3), ("dodecahedron", 15 - 6 * sp.sqrt(5)), ("icosahedron", 15 - 6 * sp.sqrt(5))]:
    add("#43 containment t (five solids)", "scale t", "sphere", "t in S ⊂ t·P(S)", f"containment starts ({nm})", val, "form",
        "m_G·v − t·h_G = 0: linear in t (vertex v on face G of t·P(S))", "#43; nesting-proof study", None, None, "")
# #59 Icosaxes twenty: centre distance d, ratios to first touch
for nm, val in [("first touch (Bloom)", 1), ("windows close (Bud)", 1 / phi), ("hollow fills (Icosaxes)", sp.Rational(1, 3)), ("Tricap tips meet (Lotus Jewel Axes)", 1 / phi ** 3)]:
    add("#59 twenty Icosaxes (d / first touch)", "scale d", "translation (plane pencil)", "d", nm, sp.nsimplify(val), "form",
        "separating-plane or centre-on-plane incidence, affine in d", "#59 (icosaxes-twenty study)", None, None, "")
# HexOct Dehn zeros and the 4:5:6 end window on the #57 walk
add("#57 holes AC (d² = 1·2/3)", "weight λ", "paraboloid", "λ", "Dehn zero of the h pieces (HexOct)", sp.Rational(5, 24), "metric",
    "36(5/24 − λ)⊗β: linear; root = the hcp-holes flip 5/24 (circuit toott)", "Concordance ledger 4 Nov (#86)", -11 / 24, 3 / 8, "")
add("#57 holes ABC (d² = 1·2/3)", "weight λ", "paraboloid", "λ", "Dehn zero of the c pieces (HexOct)", sp.Rational(3, 8), "metric",
    "24(3/8 − λ)⊗β: linear; root = the range end 3/8 (circuit ttott)", "Concordance ledger 4 Nov (#86)", -3 / 8, 3 / 8, "")
# approximants
for g, ks in [(9, sorted(set(Fr(p, q) for q in range(2, 10) for p in range(1, q))))]:
    for k in ks:
        add("1D Sturmian slope a (windows g ≤ 9)", "slope a", "cut-and-project (lattice line)", "a = share of S",
            f"kink of the window-{k.denominator} counts", sp.Rational(k.numerator, k.denominator), "circuit",
            f"det[[1, a], [{k.denominator}, {k.numerator}]] = {k.numerator} − {k.denominator}a: the line through lattice point ({k.denominator}, {k.numerator})",
            "splash2-approximants", 0, 1, "a → 1 − a partner present")
for nm, val, fac in [("end", sp.Rational(1, 2), "end of the square-approximant family"), ("chamber wall", sp.Rational(2, 3), "3a − 2b (defect star count 2(3a − 2b)²)"),
                     ("chamber wall", sp.Rational(3, 4), "4a − 3b (defect star count (4a − 3b)²)"), ("end", 1, "end of the family")]:
    add("Ammann–Beenker square approximants t = a/b", "slope t", "cut-and-project (lattice plane)", "t = a/b", nm, val,
        "partial" if "wall" in nm else "form", fac, "splash2-approximants", 0.5, 1, "t → 1/(2t) partner present")
add("Ammann–Beenker square approximants t = a/b", "slope t", "cut-and-project (lattice plane)", "t = a/b", "turning point = the quasicrystal 1/√2",
    1 / sp.sqrt(2), "turnpoint", "fixed point of t → 1/(2t); not an event of any approximant", "this study", 0.5, 1, "turning point")
# ---------- s-family lines lam(s) = (S0_lat + s S0_z)/S_A from the witnesses
HEX = [[1, sp.Rational(1, 2)], [sp.Rational(1, 2), 1]]
s = sp.Symbol('s')


def line_of(w, n):
    al = [sp.Rational(x) for x in w["alpha"]]; P = [[sp.Rational(x) for x in c] for c in w["coords"]]
    S0 = sum(aa * (sum(HEX[i][j] * p[i] * p[j] for i in range(2) for j in range(2)) + s * sp.Rational(2, 3) * n * n * p[2] ** 2) for aa, p in zip(al, P))
    return sp.simplify(S0 / sp.Rational(w["S"][0]))


sl = {}
for word, bys in sfam.items():
    n = len(word); L = {}
    for sv, v in bys.items():
        for st in v["stops"]:
            if not st["witness"]: continue
            ln = line_of(st["witness"], n)
            assert ln.subs(s, sp.Rational(sv)) == sp.Rational(st["value"])
            L.setdefault(str(sp.expand(ln)), []).append(sv)
    sl[word] = L
    print(f"s-family {word}: wall lines λ(s) and the spacings where they are stops: " + "; ".join(f"{k}: {sorted(vv, key=Fr)}" for k, vv in L.items()), flush=True)
json.dump(sl, open(os.path.join(DATA, "sfam-lines.json"), "w"), indent=1)
# prediction test: stops at the test spacings lie on lines found at the training spacings
TRAIN = {"1/2", "3/4", "1", "3/2", "2"}
for word, bys in sfam.items():
    train_lines = {k for k, vv in sl[word].items() if set(vv) & TRAIN}
    for sv in sorted(set(bys) - TRAIN, key=Fr):
        got = sorted(Fr(st["value"]) for st in bys[sv]["stops"])
        pred_all = sorted(set(Fr(str(sp.sympify(k).subs(s, sp.Rational(sv)))) for k in train_lines))
        # bracket rule: lines that are stops at both neighbouring training spacings
        lo_s = max((x for x in TRAIN if Fr(x) < Fr(sv)), key=Fr, default=None); hi_s = min((x for x in TRAIN if Fr(x) > Fr(sv)), key=Fr, default=None)
        br = sorted(set(Fr(str(sp.sympify(k).subs(s, sp.Rational(sv)))) for k, vv in sl[word].items() if lo_s in vv and hi_s in vv))
        on = all(g in pred_all for g in got)
        check(f"s-family PREDICTION {word} at s = {sv}: every stop lies on a wall line from the training spacings", on,
              f"stops {[str(x) for x in got]}; bracket prediction {[str(x) for x in br]}; bracket hits {sum(1 for x in br if x in got)}/{len(br)}")
# concurrency: points where 3 or more distinct wall lines (both words) meet
allL = sorted(set(sp.sympify(k) for L in sl.values() for k in L), key=str)
pts = {}
for l1, l2 in [(a_, b_) for i, a_ in enumerate(allL) for b_ in allL[i + 1:]]:
    sol = sp.solve(sp.Eq(l1, l2), s)
    for x in sol:
        pts.setdefault((x, l1.subs(s, x)), set()).update({l1, l2})
multi = {k: v for k, v in pts.items() if len(v) >= 3}
for k, v in multi.items(): print(f"concurrency: {len(v)} wall lines meet at (s, λ) = ({k[0]}, {k[1]}): {sorted(map(str, v))}", flush=True)
conc = len(multi.get((sp.Integer(1), sp.Rational(-1, 8)), []))
check("s-family: the wall lines of ABC and AC meet at the octet point (s, λ) = (1, −1/8)", conc >= 3, f"{conc} lines")
json.dump({f"({k[0]}, {k[1]})": sorted(map(str, v)) for k, v in multi.items()}, open(os.path.join(DATA, "sfam-concurrency.json"), "w"), indent=1)
# ---------- write table and coverage
rows.sort(key=lambda r: (r["group"], r["family"], r["value_float"]))
with open(os.path.join(DATA, "events.csv"), "w", newline="") as fh:
    wtr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wtr.writeheader(); wtr.writerows(rows)
json.dump(rows, open(os.path.join(DATA, "events.json"), "w"), indent=1)
cov = {}
for r in rows:
    c = cov.setdefault(r["family"], dict(total=0, strict=0, covered=0, uncovered=0, partial=0, group=r["group"]))
    c["total"] += 1
    if r["status"] in ("circuit", "metric", "turn"): c["strict"] += 1
    if r["status"] in ("circuit", "metric", "turn", "form", "turnpoint"): c["covered"] += 1
    if r["status"] in ("critical", "harmonic"): c["uncovered"] += 1
    if r["status"] == "partial": c["partial"] += 1
json.dump(cov, open(os.path.join(DATA, "coverage.json"), "w"), indent=1)
tot = len(rows); strict = sum(c["strict"] for c in cov.values()); covd = sum(c["covered"] for c in cov.values())
unc = sum(c["uncovered"] for c in cov.values()); par = sum(c["partial"] for c in cov.values())
print(f"EVENTS {tot}: strict local rule {strict}, covered incl. form {covd}, partial {par}, not covered {unc}")
for k, c in cov.items():
    print(f"  {k}: {c['covered']}/{c['total']} covered ({c['strict']} strict), partial {c['partial']}, uncovered {c['uncovered']}")
# ---------- figures
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
COL = {"turnpoint": "#7b3fbf", "circuit": "#1b7f3b", "metric": "#2a6fdb", "turn": "#7b3fbf", "form": "#8fbf8f", "partial": "#e0a020", "critical": "#c0392b", "harmonic": "#c0392b"}
MK = {"turnpoint": "|", "circuit": "o", "metric": "D", "turn": "s", "form": "o", "partial": "^", "critical": "x", "harmonic": "x"}
fams = []
for r in rows:
    if r["family"] not in fams and r["group"] != "two weights (λ, μ)": fams.append(r["family"])
# keep one #57 row per word at s = 1 and the spacings in a separate panel
fams = [f for f in fams if not (f.startswith("#57 holes") and "1·2/3" not in f)]
fig, ax = plt.subplots(figsize=(13, 0.42 * (len(fams) + 4) + 2.6))
for yi, fname in enumerate(fams):
    R = [r for r in rows if r["family"] == fname]
    vals = [r["value_float"] for r in R]
    lo = min([r["range_lo"] for r in R if r["range_lo"] is not None] + vals); hi = max([r["range_hi"] for r in R if r["range_hi"] is not None] + vals)
    if hi == lo: hi = lo + 1
    span = lambda v: (v - lo) / (hi - lo)
    unc_any = any(r["status"] in ("critical", "harmonic", "partial") for r in R)
    ax.plot([0, 1], [yi, yi], color="#cccccc", lw=6, solid_capstyle="butt", zorder=0)
    # covered areas: segments between consecutive events that are both covered
    pts = sorted(R, key=lambda r: r["value_float"])
    for p1, p2 in zip(pts, pts[1:]):
        good = all(p["status"] in ("circuit", "metric", "turn", "form", "turnpoint") for p in (p1, p2))
        ax.plot([span(p1["value_float"]), span(p2["value_float"])], [yi, yi], color="#9fd4a8" if good else "#f2c4bd", lw=6, solid_capstyle="butt", zorder=1)
    for r in R:
        ax.scatter([span(r["value_float"])], [yi], c=COL[r["status"]], marker=MK[r["status"]], s=46, zorder=3, linewidths=1.6)
    TURN = {"weight λ": lambda v: -v, "scale m": lambda v: 1 / v if v else None, "slope a": lambda v: 1 - v, "slope t": lambda v: 1 / (2 * v)}
    tf = TURN.get(R[0]["group"])
    if tf and "CO ∩" not in fname:
        V = sorted(set(round(r["value_float"], 9) for r in R if r["status"] in ("circuit", "turn", "partial", "form")))
        import numpy as _np
        for v1 in V:
            v2 = tf(v1)
            if v2 is None or v2 <= v1 + 1e-12: continue
            if any(abs(v2 - x) < 1e-7 for x in V):
                x1, x2 = span(v1), span(v2); xm = (x1 + x2) / 2; h = 0.38
                th_ = _np.linspace(0, _np.pi, 40)
                ax.plot(xm + (x2 - x1) / 2 * _np.cos(th_), yi - h * _np.sin(th_), color="#7b3fbf", lw=0.6, alpha=0.7, zorder=2)
    tp = [r for r in R if "turning point" in r["turn"]]
    for r in tp:
        ax.plot([span(r["value_float"])] * 2, [yi - 0.32, yi + 0.32], color="#7b3fbf", lw=1.2, zorder=2)
    c = cov[fname]
    ax.text(1.02, yi, f"{c['covered']}/{c['total']}", va="center", fontsize=8)
NODATA = ["#103 yantra viewpoint (hyperboloid): no slider events computed", "#89/#91 4D golden families: cuts listed, no sweep",
          "Theorem E CsCl ↔ zinc blende (scale −2): not tested here", "Window Law counts (perovskite, Frank–Kasper): stackings, no slider"]
for k, txt in enumerate(NODATA):
    yi = len(fams) + k
    ax.plot([0, 1], [yi, yi], color="#cccccc", lw=6, solid_capstyle="butt", zorder=0)
    ax.text(1.02, yi, "no data", va="center", fontsize=8, color="#777")
fams = fams + NODATA
ax.set_yticks(range(len(fams))); ax.set_yticklabels([f[:62] for f in fams], fontsize=7.5)
ax.set_xlim(-0.02, 1.1); ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(["range start", "middle", "range end"], fontsize=8)
ax.invert_yaxis()
from matplotlib.lines import Line2D
leg = [Line2D([], [], marker=MK[k], color=COL[k], ls="", label=STATUS[k][:60]) for k in ["circuit", "metric", "turn", "form", "turnpoint", "partial", "critical"]]
leg += [Line2D([], [], color="#7b3fbf", lw=0.8, label="hopscotch turn pair (λ→−λ, m→1/m, a→1−a, t→1/(2t))"), Line2D([], [], color="#9fd4a8", lw=6, label="area between covered events"), Line2D([], [], color="#f2c4bd", lw=6, label="area touching an uncovered event"),
        Line2D([], [], color="#cccccc", lw=6, label="no events computed"), Line2D([], [], color="#7b3fbf", lw=1.2, label="turning point (hopscotch turn)")]
ax.legend(handles=leg, fontsize=7, loc="upper center", bbox_to_anchor=(0.45, -0.04), ncol=3, frameon=False)
ax.set_title("Splash coverage: where a local rule (one determinant factor) suffices, slider by slider", fontsize=10)
fig.text(0.99, 0.005, "DICTO · dictospheres.com", ha="right", fontsize=7, color="#666")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "splash-coverage.png"), dpi=170)
# (s, lambda) panel
fig, ax = plt.subplots(figsize=(7, 5))
sg = sp.Symbol('s')
cols = {"ABC": "#1b7f3b", "AC": "#2a6fdb"}
for word, L in sl.items():
    for k, vv in L.items():
        ss = sorted(Fr(x) for x in vv); f = sp.lambdify(sg, sp.sympify(k))
        xs = [float(ss[0]), float(ss[-1])]
        ax.plot(xs, [f(x) for x in xs], color=cols[word], lw=1, alpha=0.6)
        for x in ss:
            ax.scatter([float(x)], [f(float(x))], color=cols[word], s=18 if str(x) in TRAIN else 60, marker="o" if str(x) in TRAIN else "*", zorder=3)
ax.annotate(f"octet point (1, −1/8): {conc} wall lines meet", (1, -0.125), (1.15, 0.02), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.6))
ax.set_xlabel("layer spacing s (d² = s·2/3)"); ax.set_ylabel("λ at a stop")
ax.set_title("#57 hole walk: every stop on a straight wall line λ(s) = (a + b·s)/S_A\ngreen ABC (c), blue AC (h); dots = spacings walked first, stars = predicted then walked (5/8, 5/4)", fontsize=9)
fig.text(0.99, 0.005, "DICTO · dictospheres.com", ha="right", fontsize=7, color="#666")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "s-lambda.png"), dpi=170)
nf = sum(c[0] == "FAIL" for c in checks)
print(f"{len(checks) - nf}/{len(checks)} PASS")
print('FINAL ok' if checks and nf == 0 and tot > 0 else f'FINAL FAIL: {nf} failed')
