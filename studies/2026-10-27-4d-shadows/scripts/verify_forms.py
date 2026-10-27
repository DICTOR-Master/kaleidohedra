"""Clearance check of every embedded equilateral form found by solve_slices.py, and saving of its coordinates.

For each pair of faces that share no vertex: minimum distance between the two triangles.
For each pair that shares one vertex v: minimum distance between the two triangles with the corner at v cut away
(barycentric weight of v at most 0.8), which is positive exactly when the faces meet only at v near that corner.
For each pair sharing an edge: the dihedral angle's distance from 0 and 360 degrees (faces folding onto each other).
Floats (the solutions are known to 60 digits); the margins are printed so they can be judged.
Usage: ~/geom/bin/python verify_forms.py data/solve_V28_full.json
"""
import itertools
import json
import pickle
import sys

import numpy as np

from large_slices import SLICES


def seg_seg(p1, q1, p2, q2):
    d1, d2, r = q1 - p1, q2 - p2, p1 - p2
    a, e, f = d1 @ d1, d2 @ d2, d2 @ r
    c, b = d1 @ r, d1 @ d2
    den = a * e - b * b
    s = np.clip((b * f - c * e) / den, 0, 1) if den > 1e-14 else 0.0
    t = (b * s + f) / e
    if t < 0:
        t, s = 0.0, np.clip(-c / a, 0, 1)
    elif t > 1:
        t, s = 1.0, np.clip((b - c) / a, 0, 1)
    return np.linalg.norm((p1 + d1 * s) - (p2 + d2 * t))


def pt_tri(p, a, b, c):
    n = np.cross(b - a, c - a); n = n / np.linalg.norm(n)
    q = p - (p - a) @ n * n
    inside = all(np.cross(v - u, q - u) @ n >= 0 for u, v in ((a, b), (b, c), (c, a)))
    if inside:
        return abs((p - a) @ n)
    return min(seg_seg(p, p, u, v) for u, v in ((a, b), (b, c), (c, a)))


def tri_tri(A, B):
    d = min(pt_tri(p, *B) for p in A)
    d = min(d, min(pt_tri(p, *A) for p in B))
    for (u1, v1) in ((A[0], A[1]), (A[1], A[2]), (A[2], A[0])):
        for (u2, v2) in ((B[0], B[1]), (B[1], B[2]), (B[2], B[0])):
            d = min(d, seg_seg(u1, v1, u2, v2))
    return d


def cut_corner(T, i, w=0.8):
    """triangle T with the corner i cut away: two triangles."""
    v, a, b = T[i], T[(i + 1) % 3], T[(i + 2) % 3]
    pa, pb = v + (1 - w) * (a - v), v + (1 - w) * (b - v)
    return [np.array([pa, a, b]), np.array([pa, b, pb])]


def clearance(P, F):
    P = np.asarray(P)
    no_share, one_share = np.inf, np.inf
    for f, g in itertools.combinations(F, 2):
        sh = set(f) & set(g)
        A, B = P[list(f)], P[list(g)]
        if not sh:
            no_share = min(no_share, tri_tri(A, B))
        elif len(sh) == 1:
            v = sh.pop()
            for a in cut_corner(A, list(f).index(v)):
                for b in cut_corner(B, list(g).index(v)):
                    one_share = min(one_share, tri_tri(a, b))
    return no_share, one_share


def mp_positions(lab, gname, values, dps=50):
    """positions of all vertices at high precision from the solution values (30 digits given)."""
    import mpmath as mp
    import sympy as sp
    from large_slices import symmetry_group, det3, reduced_system
    from q5 import ONE
    mp.mp.dps = dps
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES[lab]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    group = symmetry_group(s["V"], s["E"], s["w"])
    if gname == "rotations":
        group = [(a, M) for a, M in group if det3(M) == ONE]
    syms, eqs, pos, info = reduced_system(s["V"], s["E"], s["w"], group)
    sub = {x: sp.Float(values[str(x)], 40) for x in syms}
    # refine the 30-digit values by Newton on the exact equations
    J = sp.Matrix(eqs).jacobian(syms)
    v = sp.Matrix([sub[x] for x in syms])
    for _ in range(4):
        d = dict(zip(syms, v))
        v = v - J.subs(d).evalf(dps).LUsolve(sp.Matrix(eqs).subs(d).evalf(dps))
    d = dict(zip(syms, v))
    W = [mp.sqrt(mp.mpf(w.a.numerator) / w.a.denominator + mp.mpf(w.b.numerator) / w.b.denominator * mp.sqrt(5))
         for w in s["w"]]
    P = [[mp.mpf(str(sp.N(c.subs(d), dps))) * W[i] for i, c in enumerate(pv)] for pv in pos]
    return P


def mp_seg_seg(p1, q1, p2, q2):
    import mpmath as mp
    d1 = [q - p for p, q in zip(p1, q1)]; d2 = [q - p for p, q in zip(p2, q2)]
    r = [a - b for a, b in zip(p1, p2)]
    dot = lambda u, v: sum(x * y for x, y in zip(u, v))
    a, e, f, c, b = dot(d1, d1), dot(d2, d2), dot(d2, r), dot(d1, r), dot(d1, d2)
    best = None
    cands = []
    den = a * e - b * b
    if den > mp.mpf(10) ** -30:
        s_ = (b * f - c * e) / den; t_ = (a * f - b * c) / den
        if 0 <= s_ <= 1 and 0 <= t_ <= 1:
            cands.append((s_, t_))
    for s_ in (0, 1):
        t_ = min(max((b * s_ + f) / e, 0), 1); cands.append((mp.mpf(s_), t_))
    for t_ in (0, 1):
        s_ = min(max((b * t_ - c) / a, 0), 1); cands.append((s_, mp.mpf(t_)))
    for s_, t_ in cands:
        dv = [p + s_ * x - (q + t_ * y) for p, x, q, y in zip(p1, d1, p2, d2)]
        dd = mp.sqrt(dot(dv, dv))
        best = dd if best is None else min(best, dd)
    return best


def main(path):
    r = json.load(open(path))
    lab = r["label"]
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES[lab]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    F = s["faces"]
    out = []
    for k, sol in enumerate(r.get("real_solutions", [])):
        if not sol["check"].get("embedded"):
            continue
        P = np.array(sol["P"])
        a, b = clearance(P, F)
        rec = {"solution": k, "values": sol["values"], "clearance_disjoint_faces": a,
               "clearance_vertex_sharing_faces_corner_cut": b, "dihedral_min": sol["check"]["dihedral_min"],
               "dihedral_max": sol["check"]["dihedral_max"], "closest_to_180": sol["check"]["closest_to_180"]}
        if min(a, b) < 1e-9:
            # locate the contact and measure it at 50 digits
            Pm = mp_positions(lab, r["group"], sol["values"])
            worst = None
            for f, g in itertools.combinations(F, 2):
                if set(f) & set(g):
                    continue
                if tri_tri(P[list(f)], P[list(g)]) < 1e-9:
                    for i in range(3):
                        for j in range(3):
                            dd = mp_seg_seg(Pm[f[i]], Pm[f[(i + 1) % 3]], Pm[g[j]], Pm[g[(j + 1) % 3]])
                            if worst is None or dd < worst[0]:
                                worst = (dd, (f[i], f[(i + 1) % 3]), (g[j], g[(j + 1) % 3]))
            rec["contact_50_digits"] = None if worst is None else {"distance": str(worst[0]), "edge_a": worst[1],
                                                                   "edge_b": worst[2]}
        np.save(f"data/form_{lab}_{r['group']}_{k}.npy", P)
        out.append(rec)
        print(json.dumps(rec), flush=True)
    json.dump(out, open(f"data/verify_{lab}_{r['group']}.json", "w"), indent=1)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
