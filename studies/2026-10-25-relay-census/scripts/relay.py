# Relay census, part B: from the walked intervals (../data/raw/<net>.json), the life of every bond type and bond orbit
# (type @ squared site distance), the flips, the hinge parameters (both kinds present, only unlike bonds), the overlap of the two
# like bonds, and named stops (2D: equal-edge parameters; 3D: equal like-bond areas) solved exactly with sympy.
# Output: ../data/raw/relay-summary.json and ../data/checks/relay-checks.txt
import json, sys, glob
from fractions import Fraction as Fr
import sympy as sp
LAM = sp.Symbol("lam")
NAMES = ["square", "honeycomb", "kagome", "bcc", "delian", "nacl", "zincblende", "hcpholes", "a15", "c15"]
checks = []; summary = {}
def check(n, ok, det=""):
    checks.append(("PASS" if ok else "FAIL", n, det)); print(("PASS " if ok else "FAIL ") + n + (" " + det if det else ""))

def life(recs, key):
    """Where bond `key` is present: list of (lam or interval) records; returns a compact description (min, max, closed ends)."""
    pts = []
    for kind, r in recs:
        if key in r[kind]:
            pts.append((Fr(r["lo"]), Fr(r["hi"]), False) if "lo" in r else (Fr(r["lam"]), Fr(r["lam"]), True))
    if not pts: return None
    lo = min(p[0] for p in pts); hi = max(p[1] for p in pts)
    lo_closed = any(p[2] and p[0] == lo for p in pts); hi_closed = any(p[2] and p[1] == hi for p in pts)
    return {"lo": str(lo), "hi": str(hi), "lo_closed": lo_closed, "hi_closed": hi_closed,
            "text": ("[" if lo_closed else "(") + f"{lo}, {hi}" + ("]" if hi_closed else ")")}

for key in sys.argv[1:] or NAMES:
    d = json.load(open(f"../data/raw/{key}.json")); A, B = d["lam"].replace("w_", "").split(" - ")
    recs = [("bond_types", r) for r in d["intervals"]] + [("bond_types", r) for r in d["stops"]]
    orecs = [("bond_orbits", r) for r in d["intervals"]] + [("bond_orbits", r) for r in d["stops"]]
    types = sorted(set(t for _, r in recs for t in r["bond_types"])); orbs = sorted(set(t for _, r in orecs for t in r["bond_orbits"]))
    stops = d["stops"]; ends = [Fr(s["lam"]) for s in stops if s["vanish"]]; lo_end, hi_end = min(ends), max(ends)
    flips = [s["lam"] for s in stops if not s["vanish"]]
    AA, BB = "-".join(sorted((A, A))), "-".join(sorted((B, B))); AB = "-".join(sorted((A, B)))
    L = {t: life(recs, t) for t in types}; LO = {t: life(orecs, t) for t in orbs}
    # contiguity check: the life of each type is one interval (it is present on every record between its ends)
    allr = sorted([(Fr(r["lo"]), Fr(r["hi"]), r) for r in d["intervals"]] + [(Fr(r["lam"]), Fr(r["lam"]), r) for r in stops], key=lambda x: (x[0], x[1]))
    for t in types:
        lo, hi = Fr(L[t]["lo"]), Fr(L[t]["hi"])
        inside = [x for x in allr if lo <= x[0] and x[1] <= hi and not (x[0] == x[1] == lo and not L[t]["lo_closed"]) and not (x[0] == x[1] == hi and not L[t]["hi_closed"])]
        check(f"{key}: bond type {t} lives on one interval {L[t]['text']}", all(t in x[2]["bond_types"] for x in inside))
    hinge = []
    for x in allr:
        live = [s for s in x[2]["sites"] if not s.get("vanished")]
        if len(set(s["kind"] for s in live)) == 2 and x[2]["bond_types"] == [AB]:
            hinge.append(str(x[0]) if x[0] == x[1] else f"({x[0]}, {x[1]})")
    # relay class from the two like-bond lives
    la, lb = L.get(AA), L.get(BB)
    cls = None
    if la and lb:
        a_birth, b_death = Fr(la["lo"]), Fr(lb["hi"])  # A-A grows with lam (A heavier), B-B dies
        if a_birth < b_death: cls = f"overlap: both like bonds on ({a_birth}, {b_death})"
        elif a_birth == b_death: cls = f"touch: like bonds hand over at {a_birth}"
        else: cls = f"gap: no like bond on ({b_death}, {a_birth})"
    out = {"name": d["name"], "lam": d["lam"], "units": d["units"], "range": [str(lo_end), str(hi_end)], "flips": flips,
           "interior_flips": [f for f in flips if lo_end < Fr(f) < hi_end], "types": {t: L[t]["text"] for t in types},
           "orbits": {t: LO[t]["text"] for t in orbs}, "hinge": hinge, "class": cls}
    # named stops: equal edges (2D) / equal like-bond areas (3D), exact
    named = []
    for r in d["intervals"]:
        lo, hi = sp.Rational(r["lo"]), sp.Rational(r["hi"])
        a2 = set(); like = {}
        for s in r["sites"]:
            for k, v in s["area2"].items():
                for e in v:
                    a2.add(sp.sympify(e, locals={"lam": LAM}))
                    typ = "-".join(sorted((s["kind"], k)))
                    if typ in (AA, BB): like.setdefault(typ, set()).add(sp.sympify(e, locals={"lam": LAM}))
        a2 = sorted(a2, key=str)
        if len(a2) > 1 and len(d["kinds"]) and d["key"] in ("square", "honeycomb", "kagome"):
            sols = None
            for e in a2[1:]:
                z = set(x for x in sp.solve(sp.Eq(a2[0], e), LAM) if x.is_real and lo < x < hi)
                sols = z if sols is None else sols & z
            for x in sorted(sols or [], key=float):
                named.append({"interval": f"({r['lo']}, {r['hi']})", "what": "all edges equal", "lam": str(sp.nsimplify(x)), "float": float(x)})
        if AA in like and BB in like and d["key"] not in ("square", "honeycomb", "kagome"):
            for ea in like[AA]:
                for eb in like[BB]:
                    for x in sp.solve(sp.Eq(ea, eb), LAM):
                        if x.is_real and lo < x < hi:
                            named.append({"interval": f"({r['lo']}, {r['hi']})", "what": f"{AA} area = {BB} area", "lam": str(sp.nsimplify(x)), "float": float(x)})
    # 3D: parameters where every edge of one kind's cell, or of the whole tiling, has the same length (exact)
    if d["key"] not in ("square", "honeycomb", "kagome"):
        for r in d["intervals"]:
            lo, hi = sp.Rational(r["lo"]), sp.Rational(r["hi"]); per = {}
            for s in r["sites"]:
                per.setdefault(s["kind"], set()).update(sp.sympify(e, locals={"lam": LAM}) for e in s["edge_len2"])
            for scope, E in list(per.items()) + [("tiling", set().union(*per.values()))]:
                E = sorted(E, key=str); sols = None
                if len(E) == 1:
                    named.append({"interval": f"({r['lo']}, {r['hi']})", "what": f"{scope}: one edge length throughout", "lam": "all"}); continue
                for e in E[1:]:
                    z = set(x for x in sp.solve(sp.Eq(E[0], e), LAM) if x.is_real and lo < x < hi)
                    sols = z if sols is None else sols & z
                for x in sorted(sols or [], key=float):
                    named.append({"interval": f"({r['lo']}, {r['hi']})", "what": f"{scope}: all edges equal", "lam": str(sp.nsimplify(x)), "float": float(x)})
    # 2D stops: number of distinct edge lengths (limits of the neighbouring intervals' closed forms)
    if d["key"] in ("square", "honeycomb", "kagome"):
        for st in stops:
            l = sp.Rational(st["lam"]); vals = set()
            for r in d["intervals"]:
                if sp.Rational(r["lo"]) == l or sp.Rational(r["hi"]) == l:
                    for s in r["sites"]:
                        for v in s["area2"].values():
                            for e in v:
                                x = sp.sympify(e, locals={"lam": LAM}).subs(LAM, l)
                                if x > 0: vals.add(x)
            named.append({"stop": st["lam"], "edge_len2": sorted(str(v) for v in vals)})
            if st["lam"] in hinge:
                check(f"{key}: hinge {st['lam']} has a single edge length", len(vals) == 1, str(sorted(vals)))
    out["named"] = named
    summary[key] = out
    print(key, json.dumps(out, indent=1))
# regressions against the Bond Relay study (2026-10-25-bond-relay README, closed forms in app units / L/2 units)
x, t = sp.symbols("x t", positive=True)
def area2(key, ivlo, kind, nb):
    d = json.load(open(f"../data/raw/{key}.json"))
    r = [r for r in d["intervals"] if r["lo"] == ivlo][0]; s = [s for s in r["sites"] if s["kind"] == kind][0]
    return sp.sympify(s["area2"][nb][0], locals={"lam": LAM})
if "bcc" in summary:
    lam_x = (x - 1) / (x + 1)  # lam = 2s - 1, s = x/(1+x); areas in (L/2)^2: multiply the study's forms by 4/phi^2
    check("regression bcc = golden loop: big-small area^2 = ((sqrt3/2)(x^2+4x+1)/(1+x)^2)^2",
          sp.simplify(area2("bcc", "-1", "big", "small").subs(LAM, lam_x) - (sp.sqrt(3) / 2 * (x**2 + 4*x + 1) / (1 + x)**2)**2) == 0)
    check("regression bcc = golden loop: big-big area^2 = (2x^2/(1+x)^2)^2",
          sp.simplify(area2("bcc", "-1", "big", "big").subs(LAM, lam_x) - (2 * x**2 / (1 + x)**2)**2) == 0)
    check("regression bcc: the golden loop [-1, 1] is exactly the overlap chamber, between the flips -1 and 1",
          summary["bcc"]["interior_flips"] == ["-1", "1"])
if "delian" in summary:
    lam_t = sp.Rational(3, 8) * (2 * t - 1)
    check("regression delian: oct-tet area^2 = ((9 sqrt3/4) t^2)^2 for t < 1/3",
          sp.simplify(area2("delian", "-3/8", "tet", "oct").subs(LAM, lam_t) - (9 * sp.sqrt(3) / 4 * t**2)**2) == 0)
    check("regression delian: oct-oct area^2 = ((sqrt2/4)(1 - 9t^2))^2 for t < 1/3",
          sp.simplify(area2("delian", "-3/8", "oct", "oct").subs(LAM, lam_t) - (sp.sqrt(2) / 4 * (1 - 9 * t**2))**2) == 0)
    check("regression delian: tet-tet area^2 = ((3t - 1)(5 - 3t)/8)^2 for t > 1/3",
          sp.simplify(area2("delian", "-1/8", "tet", "tet").subs(LAM, lam_t) - ((3*t - 1) * (5 - 3*t) / 8)**2) == 0)
    nm = {(n.get("what"), n.get("lam")) for n in summary["delian"]["named"]}
    check("regression delian: equilateral RD stop t = (2 sqrt6 - 3)/15 found as the oct all-edges-equal parameter",
          any(w == "oct: all edges equal" and sp.simplify(sp.sympify(l) - lam_t.subs(t, (2 * sp.sqrt(6) - 3) / 15)) == 0 for w, l in nm))
    check("regression delian: equilateral cube stop t = 5/3 - (2/3) sqrt2 found as the tet all-edges-equal parameter",
          any(w == "tet: all edges equal" and sp.simplify(sp.sympify(l) - lam_t.subs(t, sp.Rational(5, 3) - 2 * sp.sqrt(2) / 3)) == 0 for w, l in nm))
    check("regression delian: single flip at t = 1/3 (lam = -1/8), hinge there", summary["delian"]["interior_flips"] == ["-1/8"] and summary["delian"]["hinge"] == ["-1/8"])
json.dump(summary, open("../data/raw/relay-summary.json", "w"), indent=1)
with open("../data/checks/relay-checks.txt", "w") as fh:
    for s, n, det in checks: fh.write(f"{s} {n} {det}\n")
print(sum(c[0] == "PASS" for c in checks), "/", len(checks))
