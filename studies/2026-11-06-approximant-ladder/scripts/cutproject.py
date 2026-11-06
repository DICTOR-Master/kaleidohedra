"""Rungs by cut-and-project (DICTO 11-06 "keep climbing ... then rung 2"). The icosahedral quasilattice = the points x of Z^6 whose
'perpendicular' shadow lies in the window (the 6D cube's shadow, a rhombic triacontahedron); their physical shadow are the vertices of
the 3D Penrose tiling (golden rhombohedra). Approximant q (= 1/1, 2/1, 3/2, 5/3 ... -> phi): phi replaced by q in the PHYSICAL
directions only, so the physical shadow becomes periodic (cubic cell). For each rung: points per cubic cell, how many have the full
icosahedral star (12 neighbours along the six directions, both ways), and their arrangement. Usage: cutproject.py q_num q_den [R]"""
import itertools, sys, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
qn, qd = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1, 1)
q = qd / qn; R = int(sys.argv[3]) if len(sys.argv) > 3 else 3
def dirs(t): return np.array([[1, t, 0], [-1, t, 0], [0, 1, t], [0, -1, t], [t, 0, 1], [t, 0, -1]], float)
Epar = dirs(phi); Eperp = dirs(-q)                # standard approximant: physical space keeps the golden directions, the hidden (perp) space
                                                  # uses the rational q ~ 1/phi (1/1 -> 1, 2/1 -> 1/2, 3/2 -> 2/3, 5/3 -> 3/5): Z^6 vectors with zero perp
                                                  # shadow become exact periods of the physical set
W = ConvexHull(np.array([np.array(s) @ Eperp for s in itertools.product((0, 1), repeat=6)]) - 0.5 * Eperp.sum(0))
def in_window(P): return ((P @ W.equations[:, :3].T + W.equations[:, 3]) <= 1e-9).all(1)
pts = np.array(list(itertools.product(range(-R, R + 1), repeat=6)))
gamma = np.array([0.1, 0.07, 0.03, -0.05, 0.02, -0.08])          # generic shift so no point sits on the window's boundary
ok = in_window((pts + gamma) @ Eperp); V = pts[ok]; X = V @ Epar
print(f"approximant {qn}/{qd}: {ok.sum()} points from Z^6 box R={R}")
# period of the physical set: the vectors of Z^6 with zero perpendicular... for the approximant, the cubic period is the smallest
# integer combination of Epar rows that is a multiple of (1,0,0); find it by scanning small integer vectors
per = []
import os
PR = int(os.environ.get('PR', '3'))
for v in itertools.product(range(-PR, PR + 1), repeat=6):
    v = np.array(v)
    if not v.any() or np.linalg.norm(v @ Eperp) > 1e-9: continue
    per.append(v @ Epar)
per = sorted(per, key=lambda p: np.linalg.norm(p))
L = np.linalg.norm(per[0]) if per else None
axes = [p for p in per if abs(np.linalg.norm(p) - L) < 1e-6] if per else []
print("shortest periods:", len(axes), "of length", None if L is None else round(L, 6), "e.g.", [tuple(np.round(p, 4)) for p in axes[:3]])
best = (L, None) if L else None
# icosahedral stars: points with all 12 neighbours x +- e_i present
S = {tuple(np.round(x, 6)) for x in X}
star = [x for x in X if all(tuple(np.round(x + s * e, 6)) in S for e in Epar for s in (1, -1))]
print(f"points with the full icosahedral star: {len(star)} of {len(X)}")
if per:
    B = [per[0]]
    for p in per[1:]:
        M = np.array(B + [p])
        if np.linalg.matrix_rank(M, tol=1e-6) > len(B): B.append(p)
        if len(B) == 3: break
    B = np.array(B); vol = abs(np.linalg.det(B))
    G = np.array([[np.dot(a, b) for b in B] for a in B])
    print(f"period lattice: lengths {np.round(np.linalg.norm(B, axis=1), 4)}, angles(cos) {np.round([G[0,1]/np.sqrt(G[0,0]*G[1,1]), G[0,2]/np.sqrt(G[0,0]*G[2,2]), G[1,2]/np.sqrt(G[1,1]*G[2,2])], 4)}, cell volume {vol:.4f}")
    Binv = np.linalg.inv(B.T)
    def cellcount(Y):
        f = (np.array(Y) @ Binv.T) if len(Y) else np.zeros((0, 3)); return int(np.all((f >= -1e-9) & (f < 1 - 1e-9), axis=1).sum())
    print(f"per cell: {cellcount(X)} points, {cellcount(star)} with the full icosahedral star")
print("FINAL ok")
