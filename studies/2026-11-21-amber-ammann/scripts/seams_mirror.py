"""Seams, part 1: can the cores be placed so that every pair of neighbouring cores is mirrored across the shared wall?
Why this matters: with seeds that move with the core (face centroids), a core with I_h symmetry, and a wall perpendicular to a 2-fold
axis of the core (every rhombic wall is: e_i x e_j is a 2-fold axis, exact check below), the two outer patterns on the wall agree
whenever the two cores are mirror images across the wall (the reflection maps one seed set onto the other, so it maps one Voronoi
diagram onto the other, and it fixes the wall pointwise).
Placement rule: choose x_0 in a start cell; carry it to every cell by reflecting across shared walls (g_T = product of the reflections
along a path). Exact in Q(sqrt5): (1) every wall normal is a 2-fold axis of I_h; (2) the rule is consistent: for every shared wall,
g_B = R_W g_A exactly (path independence); (3) feasibility: x_0 must lie in g_T^{-1}(T shrunk by the core) for every cell T.
LP (float, scipy) for the largest core scale r and the best x_0, then an exact check at a rational point.  Also per column (cells
chained through walls of one direction): the core heights obey t_{k+1} = h_k - t_k; the alternating sums are printed.
Usage: python seams_mirror.py SOLID"""
import json, os, sys, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__))
from ammann_cell import Q, dot, cross, vsub, vadd, vsc, det3, IH, act
from aligned import aligned
from tiling import E
def fl(v): return np.array([float(x) for x in v])
def parseQ(t):
    t = t.strip()
    if "r5" not in t: return Q(Fr(t))
    a, b = t[:-2].rsplit("+", 1) if "+" in t[1:] else ("0", t[:-2])
    return Q(Fr(a), Fr(b))
solid = sys.argv[1] if len(sys.argv) > 1 else "icosahedron"
patch = json.load(open(os.path.join(HERE, "../data/patch.json"))); tiles = patch["tiles"]
def P3(v6): return [sum((E[i][r]*v6[i] for i in range(6)), Q(0)) for r in range(3)]
# (1) wall normals are 2-fold axes: the half-turn about n is in I_h
def is_halfturn_axis(n):
    nn = dot(n, n)
    M = [[(2*n[r]*n[c])/nn - (1 if r == c else 0) for c in range(3)] for r in range(3)]
    return any(all((M[r][c] - g[r][c]).sign() == 0 for r in range(3) for c in range(3)) for g in IH)
ok2 = all(is_halfturn_axis(cross(E[i], E[j])) for i, j in itertools.combinations(range(6), 2))
print(f"every wall normal e_i x e_j is a 2-fold axis of the core: {ok2}")
# affine maps as (M, t): x -> M x + t
def refl(n, f):
    nn = dot(n, n); M = [[(1 if r == c else 0) - (2*n[r]*n[c])/nn for c in range(3)] for r in range(3)]
    Mf = [dot(M[r], f) for r in range(3)]; return (M, vsub(f, Mf))
def comp(a, b):   # a after b
    Ma, ta = a; Mb, tb = b
    M = [[sum((Ma[r][k]*Mb[k][c] for k in range(3)), Q(0)) for c in range(3)] for r in range(3)]
    return (M, vadd([dot(Ma[r], tb) for r in range(3)], ta))
def eq(a, b): return all((x - y).sign() == 0 for r in range(3) for x, y in zip(a[0][r] + [a[1][r]], b[0][r] + [b[1][r]]))
Id = ([[Q(1) if r == c else Q(0) for c in range(3)] for r in range(3)], [Q(0)]*3)
adj = {}
walls = []
for t1, t2, pts in patch["shared"]:
    X = [P3(p) for p in pts]; n = cross(vsub(X[1], X[0]), vsub(X[3], X[0])); W = refl(n, X[0])
    adj.setdefault(t1, []).append((t2, W)); adj.setdefault(t2, []).append((t1, W)); walls.append((t1, t2, W, n, X))
# BFS from the cell nearest the origin
start = min(range(len(tiles)), key=lambda i: sum(x*x for x in tiles[i]["centre"]))
g = {start: Id}; order = [start]
for a in order:
    for b, W in adj.get(a, []):
        if b not in g: g[b] = comp(W, g[a]); order.append(b)
print(f"cells reached {len(g)}/{len(tiles)}")
cons = all(eq(g[t2], comp(W, g[t1])) for t1, t2, W, n, X in walls)
print(f"path independence (g_B = R_W g_A at all {len(walls)} shared walls, exact): {cons}")
# holonomy of every loop (non-tree wall), carried back to the start cell; x0 must be fixed by all of them
def inv(a):
    M, t = a; Mt = [[M[c][r] for c in range(3)] for r in range(3)]   # orthogonal linear part
    return (Mt, vsc(-1, [dot(Mt[r], t) for r in range(3)]))
rows = []; kinds = {}
for t1, t2, W, n, X in walls:
    h = comp(inv(g[t2]), comp(W, g[t1]))
    if eq(h, Id): kinds["identity"] = kinds.get("identity", 0) + 1; continue
    M, t = h; det = det3(*M)
    kinds["improper" if det.sign() < 0 else "proper"] = kinds.get("improper" if det.sign() < 0 else "proper", 0) + 1
    for r in range(3): rows.append([M[r][c] - (1 if r == c else 0) for c in range(3)] + [-t[r]])
print(f"loop holonomies: {kinds}")
# exact elimination over Q(sqrt5): solve (M - I) x = -t for all loops
R = [list(r) for r in rows]; piv = []; rk = 0
for c in range(3):
    p_ = next((k for k in range(rk, len(R)) if R[k][c].sign() != 0), None)
    if p_ is None: continue
    R[rk], R[p_] = R[p_], R[rk]; pv = R[rk][c]; R[rk] = [x/pv for x in R[rk]]
    for k in range(len(R)):
        if k != rk and R[k][c].sign() != 0:
            f = R[k][c]; R[k] = [a - f*b for a, b in zip(R[k], R[rk])]
    piv.append(c); rk += 1
incons = any(all(x.sign() == 0 for x in r[:3]) and r[3].sign() != 0 for r in R)
print(f"common fixed set of all holonomies: rank {rk}, {'EMPTY (inconsistent equations)' if incons else ('point ' + str([R[k][3] for k in range(rk)]) if rk == 3 else 'affine set of dim ' + str(3 - rk))}")
# (3) LP: x0 in g_T^{-1}(T) shrunk by r*core, maximise r
C = aligned(solid, IH, act); Vc = np.array([fl(v) for v in C["V"]])
A_ub, b_ub = [], []
def tile_halfspaces(t):
    A = t["A"]; c = [parseQ(x) for x in t["centre_exact"]]; H = []
    for k in range(3):
        n = cross(E[A[(k+1) % 3]], E[A[(k+2) % 3]]); h = dot(n, E[A[k]])
        if h.sign() < 0: n = vsc(-1, n); h = -h
        for s in (1, -1): nn = vsc(s, n); H.append((nn, dot(nn, c) + h/2))
    return H
exactH = []
for T, t in enumerate(tiles):
    M, tt = g[T]
    for n, c in tile_halfspaces(t):
        # n.(M x0 + tt) + r h(n) <= c  ->  (M^T n).x0 + r h(n) <= c - n.tt ; h(n) = max_v n.v (core with its symmetry carried by M)
        m = [sum((M[k][r]*n[k] for k in range(3)), Q(0)) for r in range(3)]
        hn = float(np.max(Vc @ fl(m)))   # core at x0 with the original orientation; g_T maps it to the core at x_T (I_h-invariant)
        A_ub.append(list(fl(m)) + [hn]); b_ub.append(float(c - dot(n, tt))); exactH.append((m, c - dot(n, tt)))
res = linprog([0, 0, 0, -1], A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=[(None, None)]*3 + [(None, None)], method="highs")
print(f"LP: status {res.status}; largest core scale r = {(-res.fun if res.status == 0 else float('nan')):.6f} (r <= 0: no point of the start cell works)")
if res.status == 0:
    x0 = res.x[:3]; print(f"   x0 = {np.round(x0, 6)}")
    # exact check of r=0 feasibility at a rational point (point-sized core) and at r/2
    xq = [Q(Fr(float(v)).limit_denominator(10**6)) for v in x0]
    worst = min(float(c - dot(m, xq)) for m, c in exactH)
    print(f"   exact slack at rational x0 (point core): min over all constraints {worst:.6f}")
# columns: alternating sums of thickness along each wall direction
for i, j in itertools.combinations(range(6), 2):
    pass
json.dump(dict(solid=solid, twofold=ok2, consistent=cons, lp_status=int(res.status), r=float(-res.fun) if res.status == 0 else None),
          open(os.path.join(HERE, f"../data/seams_mirror_{solid}.json"), "w"))
# local witness: interior edges by number of cells round them (float angles; interior = angles add to 360 deg)
from collections import Counter
Ef = np.array([fl(v) for v in E]); ed = {}
for t in tiles:
    n, A = t["n"], t["A"]
    for k in range(3):
        l = A[k]; o1, o2 = [A[q] for q in range(3) if q != k]
        u = Ef[l]/np.linalg.norm(Ef[l])
        p1 = Ef[o1] - (Ef[o1] @ u)*u; p2 = Ef[o2] - (Ef[o2] @ u)*u
        th = np.degrees(np.arccos(p1 @ p2/np.linalg.norm(p1)/np.linalg.norm(p2)))
        for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
            v = list(n); v[o1] += a; v[o2] += b; w = list(v); w[l] += 1
            ed.setdefault((tuple(v), tuple(w)), []).append(th if a == b else 180 - th)
inner = {e: L for e, L in ed.items() if abs(sum(L) - 360) < 1e-6}
deg = Counter(len(L) for L in inner.values())
print(f"interior edges {len(inner)} by number of cells round them: {dict(sorted(deg.items()))}; odd: {sum(c for d, c in deg.items() if d % 2)}")
print("an odd edge forces each core round it onto one plane through the edge (the holonomy is a reflection); the planes of different odd edges have no common point (exact, above)")
