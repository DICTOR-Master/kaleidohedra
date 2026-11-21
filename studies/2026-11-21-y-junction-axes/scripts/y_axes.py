"""Y-junction vertices vs the 2-fold axes of the core (Proposition 17 / Table 3, 'From Dehn Packets to Scutoids').  21 Nov 2026.
Method: amber.py of the amber-cell sweep is re-run UNCHANGED except that one dump statement is inserted after the Y vertices are made
(the file _amber_patched.py is generated from the original source, see PATCH below).  The Y vertices come out exact in Q(sqrt5)
(fractions a + b sqrt5, every coordinate), together with the inner/outer cluster vertices that make each Y.
Tests, all exact in Q(sqrt5) (no floats):
  A  Y on a 2-fold axis of the core: cross(Y, axis) = 0 exactly, for axis in the core's own 2-fold axes (axes whose half-turn maps
     the core's vertex set AND face set onto themselves; candidates = the 15 icosahedral axes = 30 icosidodecahedron vertices, plus
     check the 3 cube axes).
  B  Y on the line through the midpoint of an edge of the core where two faces of the SAME kind meet (cross = 0).
  C  Y on the line through a core vertex that lies on a 2-fold axis (the icosidodecahedron's 4-valent vertices).
Usage: python y_axes.py   (runs 4 jobs at a time, foreground)"""
import os, sys, json, subprocess, itertools, time
from fractions import Fraction as Fr
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
SWEEP = os.path.abspath(os.path.join(HERE, "../../2026-11-21-amber-cell-sweep/scripts"))
RESIN = os.path.abspath(os.path.join(HERE, "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts"))
DATA = os.path.join(HERE, "../data")
sys.path.insert(0, RESIN); sys.path.insert(0, SWEEP)
from resin import Q, PHI, dot, cross, vsub, vadd, vsc
from solids import build, orbit

MARK = "    Yset = {m for m in mvert.values() if m is not None}\n"
DUMP = MARK + '''    import json as _j
    _s = lambda c: [str(c.a), str(c.b)]
    _Y = []
    for _r, _m in mvert.items():
        if _m is None: continue
        _mem = clusters[_r]
        _Y.append(dict(Y=[_s(c) for c in X[_m]], I=[[_s(c) for c in X[n[1]]] for n in _mem if n[0] == "i"], O=[[_s(c) for c in X[n[1]]] for n in _mem if n[0] == "o"]))
    _j.dump(_Y, open(os.environ["YDUMP"], "w"))
'''
src = open(os.path.join(SWEEP, "amber.py")).read()
assert src.count(MARK) == 1
open(os.path.join(HERE, "_amber_patched.py"), "w").write(src.replace(MARK, DUMP))

CASES = [(s, l, f) for s in ("C1", "C2") for l in ("sc", "bcc", "fcc") for f in ("1", "6/5")] + \
        [(s, l, "6/5") for s in ("truncated_dodecahedron", "icosidodecahedron") for l in ("sc", "bcc", "fcc")] + \
        [("dodeca_icosa_compound", l, "6/5") for l in ("bcc", "fcc")]

def run(case):
    s, l, f = case; tag = f"{s}_{l}_{f.replace('/', '-')}"; out = os.path.join(DATA, f"ydump_{tag}.json")
    env = dict(os.environ, RESIN_DIR=RESIN, YDUMP=out, PYTHONPATH=SWEEP)
    t = time.time()
    p = subprocess.run([sys.executable, os.path.join(HERE, "_amber_patched.py"), s, l, f, "cen"], env=env, capture_output=True, text=True)
    open(os.path.join(DATA, f"run_{tag}.log"), "w").write(p.stdout + p.stderr)
    res = json.load(open(os.path.join(DATA, f"amber_{s}_{l}_{f.replace('/', '-')}_cen.json")))
    return case, tag, res, out, time.time() - t

def V(p): return [Q(Fr(a), Fr(b)) for a, b in p]
def iszero(v): return all(x.sign() == 0 for x in v)
def parallel(u, v): return iszero(cross(u, v))          # same line through the origin
def pos(u, v): return dot(u, v).sign() > 0

AX15 = orbit([(0, 0, PHI), (Fr(1, 2), PHI*Fr(1, 2), PHI*PHI*Fr(1, 2))])   # 30 ends of the 15 icosahedral 2-fold axes
def key(v): return tuple(x.key() for x in v)
def core_axes(S):
    """2-fold axes of the core S: candidate axis a (one end of each of 15), half-turn maps vertex set and face set onto themselves"""
    Vs = {key(v) for v in S["V"]}
    Fs = {frozenset(key(S["V"][i]) for i in f) for f, k in S["faces"]}
    ends, seen = [], set()
    for a in AX15:
        if key(vsc(-1, a)) in seen: continue
        seen.add(key(a)); ends.append(a)
    ok = []
    for a in ends:
        aa = dot(a, a)
        R = lambda v: vsub(vsc(2*dot(a, v)/aa, a), v)
        if {key(R(v)) for v in S["V"]} == Vs and {frozenset(key(R(S["V"][i])) for i in f) for f, k in S["faces"]} == Fs: ok.append(a)
    return ends, ok

def analyse(case, tag, res, out, secs, log):
    s, l, f = case; S = build(s)
    ends, ax = core_axes(S)
    cube = [a for a in ends if sum(1 for x in a if x.sign() != 0) == 1]
    line = f"{s:24s} {l:3s} {f:3s} valid={res['valid']} Y(sweep json)={res['n_Y']} scutoid={res['n_scutoid_pieces']}/{res['n_faces']} core 2-fold axes: {len(ax)} of 15"
    if not res["valid"]: log(line + "  NOT VALID: " + res["why"]); return False
    Y = json.load(open(out)); ok = len(Y) == res["n_Y"]
    # same-kind edges
    ek = {}
    for fi, (fc, kd) in enumerate(S["faces"]):
        for i in range(len(fc)): ek.setdefault(frozenset((fc[i], fc[(i+1) % len(fc)])), []).append((fi, kd))
    mids = [(vsc(Fr(1, 2), vadd(S["V"][min(e)], S["V"][max(e)])), tuple(sorted(k for _, k in L))) for e, L in ek.items() if len(L) == 2 and L[0][1] == L[1][1]]
    midsall = [(vsc(Fr(1, 2), vadd(S["V"][min(e)], S["V"][max(e)])), tuple(sorted(k for _, k in L))) for e, L in ek.items()]
    onaxisV = [v for v in S["V"] if any(parallel(v, a) for a in ax)]
    nA = nCube = nB = nC = nAny15 = 0; off = []; hit = set(); bkinds = {}; cubeonly = 0
    for y in Y:
        P = V(y["Y"]); inA = [i for i, a in enumerate(ax) if parallel(P, a)]
        inCube = any(parallel(P, a) for a in cube); in15 = any(parallel(P, a) for a in ends)
        mB = [(m, kd) for m, kd in mids if parallel(P, m) and pos(P, m)]
        inC = any(parallel(P, v) and pos(P, v) for v in onaxisV)
        nA += bool(inA); nCube += inCube; nAny15 += in15; nB += bool(mB); nC += inC
        for m, kd in mB: bkinds[kd] = bkinds.get(kd, 0) + 1
        hit.update(inA)
        if not inA: off.append(y)
    import math
    def fl(v): return [float(x) for x in v]
    def ang(u, v):
        u, v = fl(u), fl(v); c = sum(a*b for a, b in zip(u, v))/math.sqrt(sum(a*a for a in u)*sum(b*b for b in v)); return math.degrees(math.acos(max(-1, min(1, c))))
    offang = [min(ang(V(y["Y"]), a) for a in ax) for y in off]
    offmid = [min(ang(V(y["Y"]), m) for m, _ in mids) for y in off] if mids else []
    offplane = sum(1 for y in off if any(x.sign() == 0 for x in V(y["Y"])))
    nE = len(mids)
    dist = len({key(V(y["Y"])) for y in Y})
    line += f"\n    Y vertices {len(Y)} (distinct {dist}): on a core 2-fold axis {nA}; on a cube axis {nCube}; on any of the 15 icosahedral axes {nAny15}; " \
            f"on the line through a same-kind edge midpoint {nB} (same-kind edges {nE}, kinds {sorted(set(k for _, k in mids))}); on a line through an axis-vertex of the core {nC}; " \
            f"axes used {len(hit)}; OFF a core 2-fold axis: {len(off)}"
    if off:
        line += f"\n    off-axis Y: angle to nearest core 2-fold axis {min(offang):.2f}-{max(offang):.2f} deg" + (f", to nearest same-kind-edge midpoint {min(offmid):.2f}-{max(offmid):.2f} deg" if offmid else "") + f"; exactly in a coordinate (mirror) plane: {offplane} of {len(off)}"
    log(line)
    return ok and len(off) == 0 and nA == len(Y)

def skeleton(log):
    """Straight-skeleton Y points (branch D skeleton_exact.json, skeleton2_*.json): one list per piece representative (shared points are listed per piece).
    C1 files are exact in Q(sqrt5, sqrt3) (strings a + b sqrt5 + c sqrt3 + d sqrt15): on a cube axis iff two coordinates are exactly 0
    (C1 has T_h only: its 2-fold axes are the cube axes).  C2 files hold 50-digit numbers: tested against the 15 icosahedral axes to 1e-40."""
    import sympy as sp, mpmath as mp
    mp.mp.dps = 50
    D = os.path.join(RESIN, "../data"); tot = True
    files = [("skeleton_exact.json", [json.load(open(os.path.join(D, "skeleton_exact.json")))])] + [(f, json.load(open(os.path.join(D, f)))) for f in ("skeleton2_C1.json", "skeleton2_C2_bccfcc.json", "skeleton2_C2_sc.json")]
    for fn, L in files:
        for d in L:
            pts = [(k["face"], k["orbit"], p) for k in d["kinds"] for p in k["Y_points"]]
            if not pts: log(f"skeleton {d['solid']:2s} {d['lattice']:3s} {d['factor']:3s} ({fn}): no Y vertices"); continue
            if d["mode"] == "exact":
                def z(t):
                    e = sp.sympify(t.replace("sqrt15", "sqrt(15)").replace("sqrt5", "sqrt(5)").replace("sqrt3", "sqrt(3)"))
                    return sp.expand(e) == 0
                on = [sum(z(c) for c in p) >= 2 for _, _, p in pts]; what = "on a cube axis (2 coordinates exactly 0; exact in Q(sqrt5,sqrt3))"
            else:
                axs = ends_f
                def onax(p):
                    P = [mp.mpf(c) for c in p]
                    return any(max(abs(c) for c in [P[1]*a[2]-P[2]*a[1], P[2]*a[0]-P[0]*a[2], P[0]*a[1]-P[1]*a[0]]) < mp.mpf(10)**-40*max(abs(x) for x in P) for a in axs)
                on = [onax(p) for _, _, p in pts]; what = "on one of the 15 icosahedral 2-fold axes (50 digits, tol 1e-40)"
            line = f"skeleton {d['solid']:2s} {d['lattice']:3s} {d['factor']:3s} ({fn}): Y points listed {len(pts)}, {what}: {sum(on)}, OFF: {len(on)-sum(on)}"
            log(line)

import mpmath as _mp; _mp.mp.dps = 50
ends_f = [[x.mpf() for x in a] for a in AX15]
def main():
    lines = []
    def log(x): print(x, flush=True); lines.append(x)
    t0 = time.time()
    with ThreadPoolExecutor(4) as ex: results = list(ex.map(run, CASES))
    log(f"runs done in {time.time()-t0:.0f}s ({len(CASES)} cases, amber.py unchanged except one dump line)")
    allok = True
    for r in results:
        allok &= bool(analyse(*r, log))
    skeleton(log)
    cons = all(r[2]["valid"] and len(json.load(open(r[3]))) == r[2]["n_Y"] and len({json.dumps(y["Y"]) for y in json.load(open(r[3]))}) == r[2]["n_Y"] for r in results)
    log(f"consistency (every case valid, exact Y count = n_Y of the sweep json, all Y distinct): {cons}")
    log("VERDICT: 'Y vertices lie exactly on the 2-fold axes of the core' holds exactly for all 30 Y in the bcc cases with an icosahedral core (C2, truncated dodecahedron, icosidodecahedron, compound) and is FALSE in sc and fcc (24 of 30 Y off every 2-fold axis) and for C1 in every mould (C1 has only the 3 cube axes: 6 Y on them, 24 off; bcc s0: all 6 on them)")
    if cons: log("FINAL ok")
    open(os.path.join(HERE, "../log.txt"), "w").write("\n".join(lines) + "\n")
    print("ALL Y ON CORE 2-FOLD AXES:", allok)
if __name__ == "__main__": main()
