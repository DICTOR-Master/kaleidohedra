"""Amber-Ammann summary: reads every data/ammann_<solid>_<triple>_<scale>_<seed>.json and the patch (data/patch.json).
Per solid, scale (S0 = common tightest scale, S65 = 6/5 S0, 1 = each cell its own tightest scale) and seeds:
 - validity in all 10 prolate and all 10 oblate orientations (re-checked: exact volume gap 0, sampling 0 miscounted);
 - rotation check: every orientation's kinds congruent (float isometry search + volume) to those of the reference orientation of its type,
   with the same multiplicities (the method has no preferred orientation, so the 10 runs of a type must agree);
 - kinds across the whole patch = congruence classes over both cell types; scutoid pieces, Y vertices; totals over the patch;
 - frequencies in the infinite tiling: prolate : oblate = phi (exact, from the window, tiling.py); kind k occurs with frequency
   phi*mP(k) + mO(k) per (oblate frequency); two kinds with mP1*mO2 != mP2*mO1 have an irrational frequency ratio, which no periodic
   arrangement can have.
Last line SUMMARY OK when every run file exists, every valid run passes the re-checks and every rotation check agrees."""
import glob, json, os, sys
from collections import defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("RESIN_DIR", os.path.join(HERE, "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts")))
from resin import congruent
from tiling import TRIPLES, tvol, absq
vP = max((absq(tvol(A)) for A in TRIPLES), key=float)
TYPE = {"".join(map(str, A)): ("P" if (absq(tvol(A)) - vP).sign() == 0 else "O") for A in TRIPLES}
REF = {"P": "023", "O": "012"}
patch = json.load(open(os.path.join(HERE, "../data/patch.json")))
NP = sum(t["kind"] == "P" for t in patch["tiles"]); NO = sum(t["kind"] == "O" for t in patch["tiles"])
runs = defaultdict(dict)
for f in glob.glob(os.path.join(HERE, "../data/ammann_*.json")):
    d = json.load(open(f)); b = os.path.basename(f)[len("ammann_"):-5].split("_")
    seed, scale, tri = b[-1], b[-2], b[-3]; solid = "_".join(b[:-3])
    runs[(solid, scale, seed)][tri] = d
def same(k1, k2): return abs(k1["vol"] - k2["vol"]) < 1e-9 and congruent(np.array(k1["verts"]), np.array(k2["verts"]))
allok = True; rows = []
print(f"patch: {len(patch['tiles'])} cells (prolate {NP}, oblate {NO}); patch checks {patch['checks_ok']}; prolate:oblate frequency {patch['freq_ratio_P_O']}")
NAMES = {"C1": "Fullerene Star", "C2": "Rollerball"}
for (solid, scale, seed) in sorted(runs):
    R = runs[(solid, scale, seed)]
    if len(R) != 20: print(f"MISSING runs for {solid} {scale} {seed}: {len(R)}/20"); allok = False; continue
    val = {t: bool(R[t].get("valid")) for t in R}
    for t, d in R.items():
        if d.get("valid"):
            if d.get("volume_gap") != "0" or d.get("sampling", {}).get("miscounted", 1) != 0 or not d.get("orbit_members_congruent"):
                print(f"RECHECK FAILED {solid} {scale} {seed} {t}"); allok = False
    vp = sum(val[t] for t in R if TYPE[t] == "P"); vo = sum(val[t] for t in R if TYPE[t] == "O")
    line = f"{NAMES.get(solid, solid):18s} {({'1': 'own'}).get(scale, scale):4s} {seed:5s} valid P {vp}/10 O {vo}/10"
    if 0 < vp < 10 or 0 < vo < 10: print(f"ORIENTATION DISAGREEMENT {solid} {scale} {seed}"); allok = False
    if vp < 10 or vo < 10:
        whyP = R[REF['P']].get("why", "")[:70]; whyO = R[REF['O']].get("why", "")[:70]
        rows.append(line + f"  | P: {whyP if not val[REF['P']] else 'ok'} | O: {whyO if not val[REF['O']] else 'ok'}"); continue
    # rotation check
    for t, d in R.items():
        ref = R[REF[TYPE[t]]]
        ka, kb = d["kinds"], ref["kinds"]
        if len(ka) != len(kb): print(f"ROTATION CHECK FAILED {solid} {scale} {seed} {t}: kinds {len(ka)} vs {len(kb)}"); allok = False; continue
        for k in ka:
            m = [r for r in kb if same(k, r) and len(r["members"]) == len(k["members"])]
            if not m: print(f"ROTATION CHECK FAILED {solid} {scale} {seed} {t}: kind {k['F']}"); allok = False
    # kinds across both types
    classes = []   # dict(rep, mP, mO, scut, Y)
    for typ in ("P", "O"):
        for k in R[REF[typ]]["kinds"]:
            for c in classes:
                if same(c["rep"], k): c["m" + typ] += len(k["members"]); break
            else: classes.append(dict(rep=k, mP=len(k["members"]) if typ == "P" else 0, mO=len(k["members"]) if typ == "O" else 0))
    shared = sum(1 for c in classes if c["mP"] and c["mO"])
    dP, dO = R[REF["P"]], R[REF["O"]]
    pcP, pcO = dP["n_faces"], dO["n_faces"]
    scP, scO = dP["n_scutoid_pieces"], dO["n_scutoid_pieces"]
    yP, yO = dP["n_Y"], dO["n_Y"]
    irr = any(a["mP"]*b["mO"] != b["mP"]*a["mO"] for i, a in enumerate(classes) for b in classes[i+1:])
    rows.append(line + f"  kinds P {len(dP['kinds'])} O {len(dO['kinds'])} patch {len(classes)} (shared {shared})  scutoids/cell P {scP}/{pcP} O {scO}/{pcO}"
                f"  Y/cell P {yP} O {yO}  patch: pieces {NP*pcP + NO*pcO}, scutoids {NP*scP + NO*scO}, Y {NP*yP + NO*yO}  irrational kind frequencies {irr}")
    print(f"--- {NAMES.get(solid, solid)} {scale} {seed}: kinds (type, face kind, per prolate cell, per oblate cell, scutoid, Y, facets, volume)")
    for c in classes:
        k = c["rep"]; print(f"     {k['kind']:5s} mP {c['mP']:3d} mO {c['mO']:3d} scutoid {k['scutoid']!s:5s} Y {k['Y']} facets {k['n_facets']} vol {k['vol']:.6f}")
print("\nsolid              scale seeds  result")
for r in rows: print(r)
print("SUMMARY OK" if allok else "SUMMARY FAILED")
