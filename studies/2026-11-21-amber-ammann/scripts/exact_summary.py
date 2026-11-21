"""Exact summary of the exact runs (22 Nov 2026; data/exact/ammann_<solid>_<triple>_<scale>_<seed>.json from exact_cell.py).
Everything here is exact in Q(sqrt5); no floating-point decision is made.  Per setting (solid, scale, seeds):
 - validity in each of the 20 orientations (exact_cell.py: manifold, exact embedding, exact cancellation, exact volume);
 - orbit check: for every element g of the cell's stabiliser in I_h (D3d) and every face F, g maps the piece on F onto the piece on gF
   (exact boundary signatures: facets as sets of boundary edges between exact points);
 - rotation check: for every orientation T of a type there is g in I_h mapping the reference mould (023 prolate, 012 oblate) onto T's
   mould exactly, and g maps every piece of the reference cell onto the piece of T on the image face;
 - kinds: the orbits of the reference cell; two orbits are different kinds when their exact volumes differ (asserted for all pairs);
 - no kind in both types: the exact volumes of the prolate kinds and of the oblate kinds are disjoint; the closest pair is printed
   with its exact difference.
Usage: python exact_summary.py [SOLID SCALE SEED ...] -> one block per setting; last line EXACT SUMMARY OK if every check passed."""
import glob, json, os, sys, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
from ammann_cell import Q, IH, act, key
from aligned import aligned
from tiling import E, TRIPLES, tvol, absq
def parseQ(t):
    t = t.strip()
    if "r5" not in t: return Q(Fr(t))
    a, b = t[:-2].rsplit("+", 1) if "+" in t[1:] else ("0", t[:-2])
    return Q(Fr(a), Fr(b))
def pt(s): return [parseQ(x) for x in s.split(",")]
def kstr(v): return ",".join(map(str, v))
vP = max((absq(tvol(A)) for A in TRIPLES), key=float)
TYPE = {"".join(map(str, A)): ("P" if (absq(tvol(A)) - vP).sign() == 0 else "O") for A in TRIPLES}
REF = {"P": "023", "O": "012"}
def corners(t, s):
    A = [int(c) for c in t]
    return frozenset(kstr([sum((Fr(sg[q], 6)*s*E[A[q]][r] for q in range(3)), Q(0)) for r in range(3)]) for sg in itertools.product((1, -1), repeat=3))
def gmap(g, cache):
    def m(p):
        if p not in cache: cache[p] = kstr(act(g, pt(p)))
        return cache[p]
    return m
def sigset(sig, m=lambda p: p): return frozenset(frozenset(frozenset(m(p) for p in e) for e in f) for f in sig)
NAMES = {"C1": "Fullerene Star", "C2": "Rollerball"}
SCALE = {}
for line in open(os.path.join(HERE, "../data/s0.txt")):
    w = line.split(); SCALE[w[0]] = Q(Fr(w[1]), Fr(w[2]))
def run(solid, scale, seed):
    out = []; ok = True
    R = {}
    for t in TYPE:
        f = os.path.join(HERE, f"../data/exact/ammann_{solid}_{t}_{scale}_{seed}.json")
        if not os.path.exists(f): return [f"{solid} {scale} {seed}: MISSING {t}"], False
        R[t] = json.load(open(f))
    vp = sum(bool(R[t]["valid"]) for t in R if TYPE[t] == "P"); vo = sum(bool(R[t]["valid"]) for t in R if TYPE[t] == "O")
    head = f"{NAMES.get(solid, solid):18s} {scale:4s} {seed:5s} valid P {vp}/10 O {vo}/10"
    if vp < 10 or vo < 10:
        why = {T: R[REF[T]].get("why", "")[:90] for T in "PO" if not R[REF[T]]["valid"]}
        mixed = (0 < vp < 10) or (0 < vo < 10)
        return [head + ("  ORIENTATIONS DISAGREE" if mixed else "") + "  | " + " | ".join(f"{T}: {w}" for T, w in why.items())], not mixed
    C = aligned(solid, IH, act); V, faces = C["V"], C["faces"]
    keyv = {key(v): i for i, v in enumerate(V)}; fid = {frozenset(f): i for i, (f, k) in enumerate(faces)}
    def gface(g, fi): return fid[frozenset(keyv[key(act(g, V[i]))] for i in faces[fi][0])]
    sc = SCALE[solid] if scale == "S0" else SCALE[solid]*Fr(6, 5) if scale == "S65" else None
    # the scale of each run from its exact s0 and factor (own: each cell at its own s0)
    def sx(t): return parseQ(R[t]["s0"]) if scale in ("own", "1") else sc
    sig = {t: {p["F"]: sigset(p["sig"]) for p in R[t]["pieces"]} for t in R}
    vol = {t: {p["F"]: parseQ(p["volx"]) for p in R[t]["pieces"]} for t in R}
    cor = {t: corners(t, sx(t)) for t in R}
    # orbit check (every cell) and rotation check
    orbit_ok = True; rot_ok = True; stab = {}
    for t in R:
        cache = {}
        st = [g for g in IH if frozenset(kstr(act(g, pt(c))) for c in cor[t]) == cor[t]]
        stab[t] = st
        for g in st:
            m = gmap(g, {})
            for F in sig[t]:
                if sigset([[list(e) for e in f] for f in sig[t][F]], m) != sig[t][gface(g, F)]: orbit_ok = False
        ref = REF[TYPE[t]]
        if t != ref:
            gs = [g for g in IH if frozenset(kstr(act(g, pt(c))) for c in cor[ref]) == cor[t]]
            if not gs: rot_ok = False; continue
            g = gs[0]; m = gmap(g, {})
            for F in sig[ref]:
                if sigset([[list(e) for e in f] for f in sig[ref][F]], m) != sig[t][gface(g, F)]: rot_ok = False
    ok &= orbit_ok and rot_ok and all(len(stab[t]) == 12 for t in R)
    # kinds = orbits of the reference cells; exact volumes distinct between orbits; types disjoint
    kinds = {}
    for T in "PO":
        t = REF[T]; done = set(); K = []
        for F in sorted(sig[t]):
            if F in done: continue
            orb = sorted({gface(g, F) for g in stab[t]}); done |= set(orb)
            rec = next(p for p in R[t]["pieces"] if p["F"] == F)
            K.append(dict(F=F, n=len(orb), vol=vol[t][F], kind=rec["kind"], scutoid=rec["scutoid"], Y=rec["Y"], facets=rec["n_facets"]))
        kinds[T] = K
        for a, b in itertools.combinations(K, 2):
            if (a["vol"] - b["vol"]).sign() == 0: ok = False; out.append(f"  EQUAL VOLUMES in {T}: faces {a['F']} {b['F']} (needs a congruence test)")
    shared = [(a, b) for a in kinds["P"] for b in kinds["O"] if (a["vol"] - b["vol"]).sign() == 0]
    ok &= not shared
    cl = min(((a, b) for a in kinds["P"] for b in kinds["O"]), key=lambda ab: abs(float(ab[0]["vol"] - ab[1]["vol"])))
    d = cl[0]["vol"] - cl[1]["vol"]
    dP, dO = R["023"], R["012"]
    out.append(head + f"  orbit check {orbit_ok}  rotation check {rot_ok}  kinds P {len(kinds['P'])} O {len(kinds['O'])} shared {len(shared)}"
               f"  scutoids/cell P {dP['n_scutoid_pieces']}/{dP['n_faces']} O {dO['n_scutoid_pieces']}/{dO['n_faces']}  Y/cell P {dP['n_Y']} O {dO['n_Y']}")
    out.append(f"  closest prolate/oblate kind volumes: {cl[0]['vol']} = {float(cl[0]['vol']):.6f} and {cl[1]['vol']} = {float(cl[1]['vol']):.6f};"
               f" exact difference {d} = {float(d):.6f}")
    for T in "PO":
        for k in kinds[T]:
            out.append(f"  {T} {k['kind']:5s} x{k['n']:3d} scutoid {k['scutoid']!s:5s} Y {k['Y']} facets {k['facets']} vol {k['vol']} = {float(k['vol']):.6f}")
    return out, ok
if __name__ == "__main__":
    a = sys.argv[1:]
    sets = [tuple(a[i:i+3]) for i in range(0, len(a), 3)] if a else sorted({tuple(os.path.basename(f)[len("ammann_"):-5].rsplit("_", 3)[i] for i in (0, 2, 3))
                                                                              for f in glob.glob(os.path.join(HERE, "../data/exact/ammann_*.json"))})
    allok = True
    for st in sets:
        o, k = run(*st); allok &= k; print("\n".join(o), flush=True)
    print("EXACT SUMMARY OK" if allok else "EXACT SUMMARY FAILED")
