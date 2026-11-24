"""The own-scale settings in one tiling: the "none shared" check redone with the two core sizes that occur together (24 Nov 2026).

In the own-scale runs ("1" in the file names, "own" in the paper) each cell is at its own s0 with a core of edge 1: the prolate
mould is spanned by s0(P) e_a/3 and the oblate one by s0(O) e_a/3, with s0(O) = phi s0(P). In a tiling all cells have the same
edge, so the oblate cell and everything in it is scaled by s0(P)/s0(O) = 1/phi: the oblate core has edge 1/phi (the prolate core
is the larger) and every oblate piece volume is multiplied by phi^-3 = sqrt5 - 2.  This script, exactly in Q(sqrt5):
 - reads the exact piece volumes (volx) and the exact s0 of all 20 cells of every own-scale setting from data/exact/;
 - checks that the 10 prolate cells share one s0, the 10 oblate cells another, and s0(O) = phi s0(P);
 - forms the set of prolate piece volumes and the set of oblate piece volumes times (s0(P)/s0(O))^3, checks that the factor is
   sqrt5 - 2, and that the two sets are disjoint (no piece of a prolate cell has the volume of any piece of an oblate cell, so no
   kind of piece occurs in both cell types); the closest pair and its exact difference are printed.
Settings not valid in all 20 orientations are reported and skipped. Self-contained (own Q(sqrt5) arithmetic in fractions).
Usage: python core_sizes.py [DATA_DIR]   (default ../data/exact beside this script). Last line FINAL ok only if every check passed."""
import glob, json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../data/exact")

class Q:  # a + b sqrt5, exact
    def __init__(s, a=0, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): return Q(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o): return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    def inv(s):
        n = s.a*s.a - 5*s.b*s.b; assert n != 0
        return Q(s.a/n, -s.b/n)
    def __truediv__(s, o): return s*o.inv()
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):  # exact sign of a + b sqrt5
        sa, sb = (s.a > 0) - (s.a < 0), (s.b > 0) - (s.b < 0)
        if sa == sb or sb == 0: return sa
        if sa == 0: return sb
        return sa if s.a*s.a > 5*s.b*s.b else sb
    def __float__(s): return float(s.a) + float(s.b)*5**.5
    def __repr__(s): return f"{s.a}+{s.b}r5" if s.b else f"{s.a}"

def parseQ(t):
    t = t.strip()
    if "r5" not in t: return Q(Fr(t))
    a, b = t[:-2].rsplit("+", 1) if "+" in t[1:] else ("0", t[:-2])
    return Q(Fr(a), Fr(b))

PHI = Q(Fr(1, 2), Fr(1, 2)); PHI_M3 = Q(-2, 1)  # phi^-3 = sqrt5 - 2
assert PHI*PHI*PHI*PHI_M3 == Q(1)
NAMES = {"C1": "Fullerene Star", "C2": "Rollerball"}
files = sorted(f for f in glob.glob(os.path.join(D, "ammann_*_1_*.json")) if os.path.basename(f)[7:-5].rsplit("_", 3)[2] == "1")
sets = sorted({(os.path.basename(f)[7:-5].rsplit("_", 3)[0], os.path.basename(f)[7:-5].rsplit("_", 3)[3]) for f in files})
print(f"data: {len(files)} own-scale cell files, {len(sets)} settings", flush=True)
allok = True; passed = []
for solid, seed in sets:
    R = {os.path.basename(f)[7:-5].rsplit("_", 3)[1]: json.load(open(f)) for f in files
         if os.path.basename(f)[7:-5].rsplit("_", 3)[0] == solid and os.path.basename(f)[7:-5].rsplit("_", 3)[3] == seed}
    name = f"{NAMES.get(solid, solid)} own {seed}"
    s0 = {t: parseQ(r["s0"]) for t, r in R.items()}
    lo = min(s0.values(), key=float); hi = max(s0.values(), key=float)
    P = [t for t in R if s0[t] == lo]; O = [t for t in R if s0[t] == hi]
    ok_s = len(R) == 20 and len(P) == 10 and len(O) == 10 and hi == PHI*lo
    if not ok_s: allok = False; print(f"{name}: SCALES WRONG ({len(R)} cells, {len(P)} at s0 {lo}, {len(O)} at {hi})"); continue
    nv = sum(bool(R[t]["valid"]) for t in R)
    if nv < 20: print(f"{name}: valid in {nv}/20 orientations; not a setting of Table 2, skipped"); continue
    f3 = (lo/hi)*(lo/hi)*(lo/hi)
    vP = {parseQ(p["volx"]) for t in P for p in R[t]["pieces"]}
    vO1 = {parseQ(p["volx"]) for t in O for p in R[t]["pieces"]}
    vO = {v*f3 for v in vO1}
    shared = vP & vO; shared1 = vP & vO1
    a, b = min(((x, y) for x in vP for y in vO), key=lambda xy: abs(float(xy[0] - xy[1])))
    ok = f3 == PHI_M3 and not shared and (a - b).sign() != 0
    allok &= ok
    if ok: passed.append((solid, seed))
    print(f"{name}: s0 P {lo}, s0 O {hi} = phi s0 P: True; oblate scale factor (s0P/s0O)^3 = {f3} = phi^-3: {f3 == PHI_M3}", flush=True)
    print(f"  distinct exact piece volumes: prolate {len(vP)}, oblate {len(vO)}; pairs compared {len(vP)*len(vO)}; "
          f"shared at core edge 1 in both: {len(shared1)}; shared with the oblate volumes times phi^-3: {len(shared)}")
    print(f"  closest pair: prolate {a} = {float(a):.6f} and oblate x phi^-3 {b} = {float(b):.6f}; exact difference {a - b} = {float(a - b):.6f}; "
          f"{'ok' if ok else 'FAILED'}")
need = {("C2", "cen"), ("icosahedron", "cen"), ("dodecahedron", "cen")}
print(f"Table 2 own-scale settings passing: {len(need & set(passed))}/3 ({', '.join(sorted(NAMES.get(s, s) + ' ' + d for s, d in need & set(passed)))})")
print("FINAL ok" if allok and need <= set(passed) else "FINAL FAILED")
