"""Audit item 6 of #118 (24 Nov 2026): the TRUE reason the Fullerene Star (C1) with centroid seeds fails in the prolate cell.
Exact in Q(sqrt5).  Same solid, orientation, moulds and seeds as exact_cell.py (imported from it, unchanged).

For a face F with centroid seed p_F, let Vor_F = {x : |x - p_F| <= |x - p_G| for all G} (the 3D nearest-seed region; the outer
pattern of exact_cell.py is Vor_F intersected with the mould surface).  For each of the six mould planes n.x <= s c (c = the s = 1
offset) we solve  max n.x over Vor_F  as a linear programme: floating point only PROPOSES three active bisectors; the answer is then
CERTIFIED exactly: the three bisector planes meet in x* (exact), x* satisfies all 79 bisector inequalities (primal feasible, exact),
and n = sum lam_j a_j with all lam_j >= 0 (dual feasible, exact).  Then max = n.x* exactly (weak duality both ways).
sigma_F = max over the six planes of (max n.x)/c is then the exact smallest scale with Vor_F inside sigma_F*M.
Lemma: Vor_F is convex and contains p_F, which lies inside the mould.  If s > sigma_F, Vor_F lies inside sigma_F*M, which lies in the
interior of s*M (M convex with the centre inside), so Vor_F misses the mould surface: F gets NO outer region.  If s < sigma_F, Vor_F
has a point outside s*M and p_F inside, so it crosses the surface in a set with interior: F gets a region of positive area.
(s = sigma_F exactly is flagged if it ever occurs.)  The script checks the prediction against every C1 centroid-seed log
(30 runs: 20 orientations x own s0 / S0 / 6/5 S0) and prints FINAL ok only if all agree.
Usage: python buried_hex.py   (in scripts/); log ../logs/buried_hex.log"""
import os, sys, re, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import exact_cell as X
from exact_cell import Q, dot, cross, vsub, vsc, det3, shell, IH, act, fl
from aligned import aligned
from tiling import E as E5

def pr(*a): print(*a, flush=True)
C = aligned("C1", IH, act); V, faces = C["V"], C["faces"]; NF = len(faces)
cent = [[sum((V[i][j] for i in f), Q(0))/len(f) for j in range(3)] for f, k in faces]
kinds = [k for f, k in faces]
HEX = [F for F in range(NF) if kinds[F] == "hex"]
pr(f"Fullerene Star: {NF} faces, hexagons {HEX[0]}..{HEX[-1]} ({len(HEX)}), triangles {NF-len(HEX)}")

def solve3(A, b):
    D = det3(*A)
    if D.sign() == 0: return None
    cx, cy, cz = cross(A[1], A[2]), cross(A[2], A[0]), cross(A[0], A[1])
    return [(b[0]*cx[t] + b[1]*cy[t] + b[2]*cz[t])/D for t in range(3)]

def region(F):
    """bisector inequalities a.x <= b of Vor_F (exact) and float copies"""
    A, B = [], []
    for G in range(NF):
        if G == F: continue
        A.append(vsc(2, vsub(cent[G], cent[F]))); B.append(dot(cent[G], cent[G]) - dot(cent[F], cent[F]))
    return A, B, np.array([fl(a) for a in A]), np.array([float(b) for b in B])

def certified_max(n, A, B, Af, Bf):
    """exact max of n.x over {A x <= B}; returns (value, x*, active) or None if unbounded"""
    r = linprog(-fl(n), A_ub=Af, b_ub=Bf, bounds=[(None, None)]*3, method="highs")
    if r.status == 3: return None
    assert r.status == 0, r.message
    xs = r.x; slack = Bf - Af @ xs
    cand = [int(j) for j in np.argsort(slack) if slack[j] < 1e-6*(1 + abs(Bf[j]))]          # all (nearly) tight bisectors
    if len(cand) < 3: cand = [int(j) for j in np.argsort(slack)[:3]]
    for tri in itertools.combinations(cand, 3):
        x = solve3([A[j] for j in tri], [B[j] for j in tri])
        if x is None: continue
        if any((dot(A[j], x) - B[j]).sign() > 0 for j in range(len(A))): continue      # primal feasible, exact
        lam = solve3([[A[tri[i]][r] for i in range(3)] for r in range(3)], n)          # sum lam_i a_i = n
        if lam is None or any(l.sign() < 0 for l in lam): continue                     # dual feasible, exact
        return dot(n, x), x, tri
    raise RuntimeError("no exact certificate among the proposed active sets")

def qmin(L):
    m = L[0]
    for y in L:
        if (y - m).sign() < 0: m = y
    return m
def qstr(x): return f"{x}  (= {float(x):.6f})"

# scales of the 30 centroid runs (joblist): own s0, S0 = (15+9r5)/2, S65 = 9 + 27/5 r5
S0, S65 = Q(Fr(15, 2), Fr(9, 2)), Q(Fr(9), Fr(27, 5))
OBL = ["012", "013", "025", "034", "045", "124", "135", "145", "234", "235"]
PRO = ["014", "015", "023", "024", "035", "123", "125", "134", "245", "345"]
LOG = os.path.join(HERE, "../logs/exact")
allok = True
# Vor_F once per face (it does not depend on the mould); bounded or not is tested by the LP in +-x, +-y, +-z
REG = {F: region(F) for F in range(NF)}
bounded = {}
for F in range(NF):
    bounded[F] = all(certified_max([Q(int(i == k)*sg) for i in range(3)], *REG[F]) is not None for k in range(3) for sg in (1, -1))
pr(f"faces whose centroid region Vor_F is BOUNDED (seed strictly inside the hull of the other 79 seeds): "
   f"{[F for F in range(NF) if bounded[F]]}")
pr(f"  = all hexagons and only them: {sorted(F for F in range(NF) if bounded[F]) == HEX}")
allok &= sorted(F for F in range(NF) if bounded[F]) == HEX

summary = {}
for lat in OBL + PRO:
    H1 = shell(lat, Q(1))
    s0 = None
    for n, c in H1:
        for v in V:
            r = dot(n, v)/c
            if s0 is None or (r - s0).sign() > 0: s0 = r
    typ = "oblate" if lat in OBL else "prolate"
    pr(f"\n=== {typ} {lat}: s0 = {qstr(s0)}")
    A3 = [vsc(Fr(1, 3), E5[int(ch)]) for ch in lat]
    diag = None
    for e1, e2 in itertools.product((1, -1), repeat=2):     # the 3-fold axis: the diagonal whose three edges meet at equal angles
        a, b, c = A3[0], vsc(e1, A3[1]), vsc(e2, A3[2])
        if (dot(a, b) - dot(a, c)).sign() == 0 and (dot(a, b) - dot(b, c)).sign() == 0:
            diag = [a[t] + b[t] + c[t] for t in range(3)]; ang = dot(a, b)
    assert diag is not None
    others = []
    for e1, e2 in itertools.product((1, -1), repeat=2):
        d = [A3[0][t] + e1*A3[1][t] + e2*A3[2][t] for t in range(3)]
        if not all(t.sign() == 0 for t in cross(d, diag)): others.append(dot(d, d))
    pr(f"  3-fold diagonal length^2 {qstr(dot(diag, diag))} (edges at {'acute' if ang.sign() > 0 else 'obtuse'} angles there); "
       f"other diagonals length^2 {[round(float(o), 4) for o in others]}  -> the 3-fold axis is the {'LONGEST' if all((dot(diag, diag) - o).sign() > 0 for o in others) else 'SHORTEST' if all((dot(diag, diag) - o).sign() < 0 for o in others) else 'middle'} diagonal")
    sig = {}
    for F in HEX:
        best = None
        for (n, c) in H1:
            val, x, tri = certified_max(n, *REG[F])
            q = val/c
            if best is None or (q - best[0]).sign() > 0: best = (q, x, n)
        sig[F] = best
    for F in HEX:
        q, x, n = sig[F]
        on_axis = all(t.sign() == 0 for t in cross(cent[F], diag))
        pr(f"  hex {F:2d}: sigma = {qstr(q)}  {'ON the cell 3-fold axis' if on_axis else ''}")
    for tag, s in (("1", s0), ("S0", S0), ("S65", S65)):
        assert all((sig[F][0] - s).sign() != 0 for F in HEX), "boundary case s = sigma"
        pred = sorted(F for F in HEX if (sig[F][0] - s).sign() < 0)
        txt = open(os.path.join(LOG, f"C1_{lat}_{'own' if tag == '1' else tag}_cen.log")).read()
        m = re.search(r"^RESULT .*", txt, re.M).group(0)
        mm = re.search(r"empty outer cells \[([0-9, ]*)\]", m)
        got = sorted(int(t) for t in mm.group(1).split(",")) if mm else []
        agree = pred == got; allok &= agree
        pr(f"  scale {tag:3s} ({float(s):.4f}): predicted empty hexagons {pred}; log {got}  agree {agree}")
    onax = [F for F in HEX if all(t.sign() == 0 for t in cross(cent[F], diag))]
    summary[lat] = (typ, s0, qmin([sig[F][0] for F in HEX]), [sig[F][0] for F in onax], onax)

pr("\n=== SUMMARY (exact)")
for typ in ("oblate", "prolate"):
    rows = [summary[l] for l in summary if summary[l][0] == typ]
    s0s = {r[1].key() for r in rows}; mins = {r[2].key() for r in rows}; ax = {tuple(x.key() for x in r[3]) for r in rows}
    pr(f"{typ}: s0 {sorted(s0s)}; smallest sigma over the 20 hexagons {sorted(mins)}; sigma of the two hexagons on the cell's 3-fold axis {sorted(ax)}")
    s0 = rows[0][1]; mn = rows[0][2]
    pr(f"  s0 = {qstr(s0)}; min sigma = {qstr(mn)}; min sigma {'<' if (mn - s0).sign() < 0 else '>'} s0;  min sigma / s0 = {qstr(mn/s0)}")
    pr(f"  two axis hexagons give the smallest sigma: {all(r[2].key() in [x.key() for x in r[3]] for r in rows)}")
pro = [summary[l] for l in PRO]; obl = [summary[l] for l in OBL]
allok &= all((r[2] - r[1]).sign() < 0 for r in pro)            # prolate: some hexagon closed off already at s0, so at every s >= s0
allok &= all((r[2] - r[1]).sign() > 0 for r in obl)
pr("\nTHEOREM (exact): in every prolate cell, the two hexagons on the cell's long (3-fold) axis have sigma < s0, so with centroid seeds")
pr("they get no outer region at ANY admissible scale s >= s0; in every oblate cell every hexagon has sigma > s0.")
print("FINAL ok" if allok else "FINAL FAIL")
