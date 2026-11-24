#!/usr/bin/env python3
"""Rings in the fins of the 1232 numbered Aequi (25 Nov 2026): a double-precision screen with stated margins.

Data: study 2026-11-20-aequi-picker/dice.json (face directions, one depth per face orbit, 15 digits). Each die is the
intersection of the half-spaces u.x <= d; its corners are found as the facets of the hull of the polar points u/d (scipy).
Per die and edge ab: ring radius r, tangent length t from the centre, central angle aOb (formulas as rings_catalogue.py).
Values within 1e-9 (relative) are grouped; two groups count as different only if they differ by more than 1e-6
(relative), a margin 10^9 times the rounding of the data. Dice with any gap between 1e-9 and 1e-6 are listed as unsure.
Also the smallest angle between corner directions (struts) and the core ratio R/r = 1/sin(theta/2).
Output data/aequi-rings.json; FINAL ok if every die gave the catalogued corner count.
"""
import os, json, itertools
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
D = json.load(open(os.path.join(HERE, "../../2026-11-20-aequi-picker/dice.json")))
dirs = np.array(D["dirs"], float)

def groups(vals, tol=1e-9):
    vals = sorted(vals); gs = [[vals[0]]]
    for v in vals[1:]:
        if abs(v - gs[-1][-1]) <= tol * max(1.0, abs(v)): gs[-1].append(v)
        else: gs.append([v])
    reps = [g[0] for g in gs]
    gaps = [abs(b - a) / max(1.0, abs(b)) for a, b in zip(reps, reps[1:])]
    return len(gs), (min(gaps) if gaps else None), reps

out = []; bad = 0
for die in D["dice"]:
    orb = D["groups"][die["g"]]
    U, d = [], []
    for oi, depth in zip(die["o"], die["d"]):
        for k in orb[oi]["dirs"]:
            U.append(dirs[k]); d.append(depth)
    U = np.array(U); d = np.array(d)
    P = U / d[:, None]
    H = ConvexHull(P)
    fac = {}
    for simp, eq in zip(H.simplices, H.equations):
        fac.setdefault(tuple(np.round(eq, 8)), set()).update(int(i) for i in simp)
    V, F = [], []
    for eq, s in fac.items():
        n = np.array(eq[:3]); off = eq[3]
        V.append(n / (-off)); F.append(s)
    V = np.array(V)
    if len(V) != die["c"]: bad += 1
    E = [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if len(F[i] & F[j]) >= 2]
    R, T, Aa = [], [], []
    for i, j in E:
        a, b = V[i], V[j]; la, lb, lab = np.linalg.norm(a), np.linalg.norm(b), np.linalg.norm(a - b)
        R.append(np.linalg.norm(np.cross(a, b)) / (la + lb + lab)); T.append((la + lb - lab) / 2)
        Aa.append(np.dot(a, b) / (la * lb))
    nr, gr, reps = groups(R); nt, gt, _ = groups(T); na, ga, _ = groups(Aa)
    W = V / np.linalg.norm(V, axis=1)[:, None]
    G = W @ W.T; np.fill_diagonal(G, -2); c = G.max()
    unsure = any(g is not None and g < 1e-6 for g in (gr, gt, ga))
    out.append(dict(num=die["num"], name=die["name"], V=len(V), E=len(E), n_radii=nr, min_rel_gap_radii=gr,
                    radii_ratio=[x / max(reps) for x in reps], n_tangent=nt, n_angles=na, unsure=unsure,
                    strut_min_angle_deg=float(np.degrees(np.arccos(c))), core_R_over_r=float(np.sqrt(2 / (1 - c)))))
    if die["num"] % 100 == 0: print(f"PROGRESS {die['num'] / len(D['dice']):.3f}", flush=True)
json.dump(out, open(os.path.join(STUDY, "data/aequi-rings.json"), "w"), indent=1)
eq = [o for o in out if o["n_radii"] == 1]
print("dice", len(out), "corner-count mismatches", bad, "equal radius", len(eq), "unsure", sum(o["unsure"] for o in out),
      "fewest radii", min(o["n_radii"] for o in out), "equal tangent", sum(o["n_tangent"] == 1 for o in out),
      "equal angle", sum(o["n_angles"] == 1 for o in out))
print("smallest core ratio", min(out, key=lambda o: o["core_R_over_r"]))
print("FINAL ok" if bad == 0 else f"FINAL FAIL {bad} corner-count mismatches")
