"""Target 3 (#91 Lemma 6 / #76 stations; gaps R4, L26 part, L33): the 600-cell x 120-cell sweep
S(mu) = P ∩ mu P*, P the 600-cell with circumradius 1 (corners V/2), P* = conv of its 600 face poles N (a 120-cell),
exact in Q(sqrt5) with Normaliz + e-antic.

A. Lemma 6, proved in general (not only at stations). In the facet frame the cell rule is an identity:
   cell on the facet N.x = 1 of P (tetrahedron, centre c = N/|N|^2, |c|^2 = r^2):   T ∩ (mu - r^2) T*_loc
   cell on the facet v.x = mu of mu P* (dodecahedron mu D, centre mu v):            mu (D ∩ (1/mu - 1) D*_loc)
   PROVIDED only the facet's own corners cut it (4 corners of P / 20 poles of P*). That proviso is checked once for
   ALL mu at once: lift mu to a 5th coordinate; Q = {(x, mu): facet, own cuts, r^2 <= mu <= 1} is a polytope; every
   other constraint w.x <= mu (resp. N.x <= 1) is redundant on Q iff it holds at every vertex of Q (exact).
B. Stations: S(mu) built exactly at the three uniform members ((9+√5)/12, (11+3√5)/20, (15+8√5)/38), the two
   rectified ones, and the six golden values of #91 Table 2; counts, cells, edge lengths, sphere; uniform members
   compared corner for corner with #76's Table 1 builds from the 600-cell's own edges, triangles and cells; each
   cell's 3D sweep parameter nu3 = mu3 / r3^2 compared with #91's D·I and T·T tables."""
import json, sys, time
from collections import Counter
from itertools import combinations
from fractions import Fraction as Fr
from qphi import QP, dot, ZERO, ONE, PHI, SQRT5
from polys import cell600
import nz

t0 = time.time(); ok = True; out = {}
V = [tuple(x / 2 for x in v) for v in cell600()]                 # circumradius 1
F = nz.facets(nz.hull(V))
N = [tuple(x / (-c) for x in n) for n, c in F]                    # poles: P = {N.x <= 1}
r2 = 1 / dot(N[0], N[0])
assert all(dot(n, n) == 1 / r2 for n in N) and r2 == QP(Fr(7, 16)) + QP(Fr(3, 16)) * SQRT5
inc = [[i for i, v in enumerate(V) if dot(n, v) == ONE] for n in N]
E = sorted({tuple(sorted(e)) for c in inc for e in combinations(c, 2)})
own_poles = {j: [k for k, n in enumerate(N) if dot(n, V[j]) == ONE] for j in range(len(V))}
assert all(len(x) == 4 for x in inc) and len(E) == 720 and all(len(x) == 20 for x in own_poles.values())
out["frame"] = {"r^2": r2.s5(), "edge^2": dot(*(tuple(a - b for a, b in zip(V[E[0][0]], V[E[0][1]])),) * 2).s5()}
print("frame r^2 =", r2.s5(), flush=True)

# ---------------------------------------------------------------- A. Lemma 6 for all mu at once
def lift(rows_x, rows_mu):
    return [list(a) + [b] + [c] for (a, c), b in zip(rows_x, rows_mu)]

Z = QP(0)
# A1. tetrahedral cells: facet 0 of P
k0 = 0; own = inc[k0]
ineq = [list(n) + [Z, ONE] for n in [tuple(-x for x in n) for n in N]]          # -N.x + 1 >= 0  (x in P)
ineq += [[-x for x in V[j]] + [ONE, Z] for j in own]                             # mu - v.x >= 0  (own cuts)
ineq += [[Z] * 4 + [ONE, -r2], [Z] * 4 + [-ONE, ONE]]                            # r^2 <= mu <= 1
eqs = [[-x for x in N[k0]] + [Z, ONE]]                                           # N.x = 1
Q = nz.poly(ineq, eqs); QV = nz.verts(Q)
worst = max(((dot(V[j], q[:4]) - q[4]), j) for j in range(len(V)) if j not in own for q in QV)[0]
a1 = worst.sign() <= 0
print("A1 tetrahedral cells: lifted polytope has", len(QV), "vertices; max over other corners of w.x - mu =",
      worst.s5(), "->", "redundant" if a1 else "NOT redundant", flush=True)
# A2. dodecahedral cells: facet v0.x = mu of mu P*
j0 = 0; ownp = own_poles[j0]
ineq = [[-x for x in V[j]] + [ONE, Z] for j in range(len(V))]                    # x in mu P*: mu - w.x >= 0
ineq += [[-x for x in N[k]] + [Z, ONE] for k in ownp]                            # own cuts N.x <= 1
ineq += [[Z] * 4 + [ONE, -r2], [Z] * 4 + [-ONE, ONE]]
eqs = [[-x for x in V[j0]] + [ONE, Z]]                                           # v0.x = mu
Q2 = nz.poly(ineq, eqs); QV2 = nz.verts(Q2)
worst2 = max((dot(N[k], q[:4]) - ONE) for k in range(len(N)) if k not in ownp for q in QV2)
a2 = worst2.sign() <= 0
print("A2 dodecahedral cells: lifted polytope has", len(QV2), "vertices; max over other poles of N.x - 1 =",
      worst2.s5(), "->", "redundant" if a2 else "NOT redundant", flush=True)
ok &= a1 and a2
out["lemma6"] = {"tetrahedral_cells": {"lifted_vertices": len(QV), "max_other": worst.s5(), "redundant": a1},
                 "dodecahedral_cells": {"lifted_vertices": len(QV2), "max_other": worst2.s5(), "redundant": a2}}
print("PROGRESS 0.3 Lemma 6", round(time.time() - t0), "s", flush=True)

# ---------------------------------------------------------------- B. stations
def q(a, b=0): return QP(Fr(a)) + QP(Fr(b)) * SQRT5
STATIONS = [
    ("truncated 600-cell (uniform)", q(Fr(9, 12), Fr(1, 12))),
    ("rectified 600-cell", (2 + PHI) / 4),
    ("bitruncated (uniform midpoint)", q(Fr(11, 20), Fr(3, 20))),
    ("rectified 120-cell", PHI * PHI / 3),
    ("truncated 120-cell (uniform)", q(Fr(15, 38), Fr(8, 38))),
    ("golden 1: (13+5√5)/28", q(Fr(13, 28), Fr(5, 28))),
    ("golden 2: (111+45√5)/244", q(Fr(111, 244), Fr(45, 244))),
    ("golden 3 (Prop 7): 2-√5/2", q(2, Fr(-1, 2))),
    ("golden 4 (Prop 7): (19+9√5)/44", q(Fr(19, 44), Fr(9, 44))),
    ("golden 5: 3(√5-1)/4", q(Fr(-3, 4), Fr(3, 4))),
    ("golden 6: (5+2√5)/10", q(Fr(5, 10), Fr(2, 10))),
]
# #91 three-dimensional tables, as nu = mu/r^2 (dual end 1)
TT = {"-T": q(1), "Lesser GCT (dual side)": 3 * q(5, -2), "truncated (-T)": q(Fr(9, 5)),
      "Greater GCT (dual side)": 3 * q(Fr(3, 11), Fr(2, 11)), "octahedron": q(3),
      "Greater GCT": 3 * q(-3, 2), "truncated tetrahedron": q(5), "Lesser GCT": 3 * (q(1) + 2 / SQRT5), "T": q(9)}
DI = {"icosahedron": q(1), "Lesser GCI": q(-10, 5), "truncated icosahedron": q(Fr(30, 19), Fr(-3, 19)),
      "Greater GCI": q(Fr(5, 11), Fr(4, 11)), "icosidodecahedron": 3 - PHI, "Greater GCD": q(Fr(20, 3), Fr(-7, 3)),
      "truncated dodecahedron": q(-3, 2), "Lesser GCD": q(Fr(50, 11), Fr(-15, 11)), "dodecahedron": q(15, -6)}
RT2 = 1 - r2; rT2 = RT2 / 9                       # facet tetrahedron of P, frame centred at c
RD2 = 1 / r2 - 1; rD2 = RD2 / q(15, -6)           # facet dodecahedron D of P*, corner vectors N_i - v


def name_of(table, nu):
    for k, x in table.items():
        if x == nu: return k
    return None


ineqP = [[-x for x in n] + [ONE] for n in N]
res = []
for si, (lab, mu) in enumerate(STATIONS):
    ineq = ineqP + [[-x for x in v] + [mu] for v in V]
    S = nz.poly(ineq); SV = nz.verts(S); SF = nz.facets(S); fv = S.FVector()
    ic = nz.incid(SF, SV)
    cells = Counter(len(x) for x in ic)
    # edges: vertex pairs on >= 3 common facets (4D)
    vf = [[] for _ in SV]
    for fi, x in enumerate(ic):
        for i in x: vf[i].append(fi)
    key = {}
    for i, fs in enumerate(vf):                      # two corners on 3 common facets span an edge (4D)
        for tr in combinations(sorted(fs), 3): key.setdefault(tr, set()).add(i)
    edges = sorted({tuple(sorted(x)) for x in key.values() if len(x) == 2})
    assert len(edges) == fv[2]
    L = Counter(dot(*(tuple(a - b for a, b in zip(SV[i], SV[j])),) * 2) for i, j in edges)
    radii = Counter(dot(p, p) for p in SV)
    # cell classes via Lemma 6
    mu3 = mu - r2; nuT = mu3 / rT2
    lamD = 1 / mu - 1; nuD = lamD / rD2
    # direct exact check of Lemma 6 at this station: the S(mu) facet on N[0].x = 1 / on v0.x = mu equals the
    # facet cut by its own constraints only
    tet = [i for i, p in enumerate(SV) if dot(N[0], p) == ONE]
    Cown = nz.poly([list(-x for x in V[j]) + [mu] for j in inc[0]] + ineqP, [[-x for x in N[0]] + [ONE]])
    dod = [i for i, p in enumerate(SV) if dot(V[0], p) == mu]
    Down = nz.poly([[-x for x in V[j]] + [mu] for j in range(len(V))] + [[-x for x in N[k]] + [ONE] for k in own_poles[0]],
                   [[-x for x in V[0]] + [mu]])
    l6 = (set(nz.verts(Cown)) == {SV[i] for i in tet}) and (set(nz.verts(Down)) == {SV[i] for i in dod})
    rec = {"station": lab, "mu": mu.s5(), "mu_float": round(float(mu), 6), "f_vector": fv[1:5],
           "cells_by_vertex_count": {str(k): v for k, v in sorted(cells.items())},
           "edge_lengths^2": {k.s5(): v for k, v in L.items()}, "one_sphere": len(radii) == 1,
           "tetrahedral_cell": {"vertices": len(tet), "nu3": nuT.s5(), "TT_station": name_of(TT, nuT)},
           "dodecahedral_cell": {"vertices": len(dod), "nu3": nuD.s5(), "DI_station": name_of(DI, nuD)},
           "lemma6_direct": l6}
    ok &= l6 and len(radii) == 1
    if len(L) == 2:
        a, b = sorted(L, key=float); rec["edge_ratio^2"] = (b / a).s5(); rec["golden_ratio_of_edges"] = (b / a) == PHI * PHI
    res.append(rec)
    print(json.dumps(rec, ensure_ascii=False), flush=True)
    print("PROGRESS %.2f %s" % (0.3 + 0.6 * (si + 1) / len(STATIONS), lab), flush=True)
out["stations"] = res

# #76 Table 1 builds at the uniform members (from the 600-cell's own elements), compared corner for corner
tri = sorted({tuple(sorted(t)) for c in inc for t in combinations(c, 3)})
def lerp(a, b, t): return tuple(x + t * (y - x) for x, y in zip(a, b))
def cen(idx): return tuple(sum((V[i][k] for i in idx), ZERO) / len(idx) for k in range(4))
T600 = {lerp(V[a], V[b], QP(Fr(1, 3))) for a, b in E} | {lerp(V[b], V[a], QP(Fr(1, 3))) for a, b in E}
BIT = set()
for t in tri:
    g = cen(t)
    for a, b in combinations(t, 2):
        BIT.add(lerp(cen((a, b)), g, QP(Fr(3, 5))))
cc = [cen(c) for c in inc]                    # 120-cell corners (cell centres)
nb = [(i, j) for i in range(600) for j in range(i + 1, 600) if len(set(inc[i]) & set(inc[j])) == 3]
tt = q(Fr(5, 10), Fr(-1, 10))
T120 = {lerp(cc[i], cc[j], tt) for i, j in nb} | {lerp(cc[j], cc[i], tt) for i, j in nb}
cmp = {}
for (lab, mu), build in zip([STATIONS[0], STATIONS[2], STATIONS[4]], [T600, BIT, T120]):
    S = nz.poly(ineqP + [[-x for x in v] + [mu] for v in V]); SV = set(nz.verts(S))
    # #76 builds sit at their own scale; compare after scaling to the sweep's radius
    p = next(iter(build)); s = next(iter(SV)); k = dot(s, s) / dot(p, p)
    # scale factor sqrt(k) must be in Q(sqrt5): find it as the ratio of a matching corner along the same ray
    ratio = None
    for x in SV:
        if all(x[i] * p[j] == x[j] * p[i] for i in range(4) for j in range(4)) and dot(x, p).sign() > 0:
            ratio = next(x[i] / p[i] for i in range(4) if p[i] != ZERO); break
    same = ratio is not None and {tuple(ratio * c for c in b) for b in build} == SV
    cmp[lab] = {"corners_76": len(build), "corners_sweep": len(SV), "scale": ratio.s5() if ratio else None, "identical": same}
    ok &= same
    print("#76 build vs sweep:", lab, cmp[lab], flush=True)
out["76_vs_91"] = cmp
json.dump(out, open("../data/stations.json", "w"), indent=1, ensure_ascii=False)
print("PROGRESS 1.0 done", round(time.time() - t0), "s", flush=True)
print("FINAL ok" if ok else "FINAL FAIL", flush=True)
