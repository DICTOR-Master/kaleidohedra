"""Step 4: re-check every amber run of approx.py from its own files and test the Y vertices EXACTLY (Q(sqrt5)) against the core's
2-fold axes (the 15 lines through the sweep icosidodecahedron's vertices; for the capped icosidodecahedron the half-turn about each of
these lines maps the core onto itself as well, since the core is icosahedral).  Writes the log (../log.txt) ending FINAL ok only if:
every run file is present and agrees with its approx record; every valid run has volume gap 0 and 0 miscounted sampling points;
Y count = 30 where Y exist; the cases whose shells do not fit are confirmed by the float bound (s_real < s0) with margin > 0.5 %."""
import os, sys, json, glob
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "../data")
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts")))
from resin import Q, PHI, cross, dot
import itertools

def orbitQ(base):
    out, seen = [], set()
    for b in base:
        for sg in itertools.product((1, -1), repeat=3):
            t = [b[i] * sg[i] for i in range(3)]
            for c in ([t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]):
                k = tuple(x.key() for x in c)
                if k not in seen: seen.add(k); out.append(c)
    return out
H = Fr(1, 2)
AX = orbitQ([(Q(0), Q(0), PHI), (Q(H), PHI * H, PHI * PHI * H)])
CUBE = [[Q(1), Q(0), Q(0)], [Q(0), Q(1), Q(0)], [Q(0), Q(0), Q(1)]]
def V(p): return [Q(Fr(a), Fr(b)) for a, b in p]
def on(y, axes): return any(all(x.sign() == 0 for x in cross(y, a)) for a in axes)

lines, ok = [], True
def say(s): lines.append(s); print(s, flush=True)
for f in sorted(glob.glob(os.path.join(DATA, "approx_*.json"))):
    R = json.load(open(f)); name = R["case"]
    if not R["fits"]:
        good = R["ratio"] < 0.995
        say(f"{name}: shell does not fit its bcc Voronoi cell, s_real/s0 = {R['ratio']:.4f} ({'margin ok' if good else 'MARGIN TOO SMALL'})")
        ok &= good; continue
    A = json.load(open(os.path.join(DATA, f"amber_{name}.json")))
    agree = (A["valid"] == R["valid"]) and (A.get("n_Y") == R.get("n_Y"))
    s = f"{name}: valid {A['valid']}, kinds {A.get('n_kinds')}, scutoids {A.get('n_scutoid_pieces')}/{A.get('n_faces')}, Y {A.get('n_Y')}, volume gap {A.get('volume_gap')}, sampling {A.get('sampling')}"
    if A["valid"]:
        good = str(A.get("volume_gap")) == "0" and A["sampling"]["miscounted"] == 0
        ok &= good
        if not good: s += "  CHECK FAILED"
    ok &= agree
    if A.get("n_Y"):
        Y = [V(y["Y"]) for y in json.load(open(os.path.join(DATA, f"ydump_{name}.json")))]
        n2 = sum(on(y, AX) for y in Y); nc = sum(on(y, CUBE) for y in Y)
        s += f"; Y exactly on a 2-fold axis of the core: {n2}/{len(Y)} (on a cube axis {nc})"
        if n2 < len(Y):
            # how far off (float), for the record
            import math
            offs = []
            for y in Y:
                if on(y, AX): continue
                yf = [float(x) for x in y]; best = 9
                for a in AX:
                    af = [float(x) for x in a]; na = math.sqrt(sum(t * t for t in af)); pr = sum(p * q for p, q in zip(yf, af)) / na
                    best = min(best, math.sqrt(max(sum(t * t for t in yf) - pr * pr, 0)))
                offs.append(best)
            s += f"; off-axis Y: {len(offs)}, distance {min(offs):.2e} to {max(offs):.2e} amber units = {min(offs)*R['k']:.4f} to {max(offs)*R['k']:.4f} A"
        ok &= len(Y) == 30
        if R["solid"] == "capped_icosidodecahedron":
            # the core itself is icosahedral: every half-turn about the 15 axes maps its vertex set onto itself (exact)
            os.environ.update(SWEEP_DIR=os.path.abspath(os.path.join(HERE, "../../2026-11-21-amber-cell-sweep/scripts")), CAP_LAMBDA=R["cap_lambda"],
                              RESIN_DIR=os.path.abspath(os.path.join(HERE, "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts")))
            sys.path.insert(0, os.path.join(HERE, "shim")); import importlib, solids as SS; importlib.reload(SS)
            Cv = SS.build("capped_icosidodecahedron")["V"]; keys = {tuple(x.key() for x in v) for v in Cv}
            def half(u, x): t = dot(u, x) / dot(u, u) * 2; return [t * u[i] - x[i] for i in range(3)]
            sym = all(all(tuple(c.key() for c in half(u, v)) in keys for v in Cv) for u in AX)
            s += f"; capped core invariant under all 15 half-turns (exact): {sym}"; ok &= sym
    say(s)
say("FINAL ok" if ok else "FINAL FAILED")
open(os.path.join(HERE, "../log.txt"), "w").write("\n".join(lines) + "\n")
