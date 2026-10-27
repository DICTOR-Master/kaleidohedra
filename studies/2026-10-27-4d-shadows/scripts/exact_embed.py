"""Embedding check of an equilateral form with exact orientation predicates.

Vertex coordinates are taken at 80 digits (from the 60-digit solution refined by Newton on the exact equations) and
rounded to rationals; every orientation predicate is then evaluated exactly on those rationals.  The rounding moves
each predicate by far less than 1e-50, so a predicate whose exact value has |value| > 1e-40 has the same sign for the
true form.  Tests:
  * faces sharing no vertex: no edge of one meets the other (closed segment against closed triangle);
  * faces sharing one vertex v: the edges not through v do not meet the other face; the edges through v are not
    coplanar with the other face (otherwise they could run inside it);
  * faces sharing an edge: dihedral strictly between 0 and 360 degrees (checked as non-coplanarity of the two
    opposite vertices with the shared edge, or opposite sides when coplanar);
  * all edges equal: |edge|^2 - 1 < 1e-50.
Prints the smallest |predicate| that decided a test (the margin).
Usage: ~/geom/bin/python exact_embed.py data/eig_V48_full.json 36
"""
import itertools
import json
import pickle
import sys
from fractions import Fraction as Fr

import mpmath as mp
import sympy as sp

from large_slices import SLICES, symmetry_group, det3, reduced_system
from q5 import ONE

mp.mp.dps = 90


def orient(a, b, c, d):
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    wx, wy, wz = d[0] - a[0], d[1] - a[1], d[2] - a[2]
    return ux * (vy * wz - vz * wy) - uy * (vx * wz - vz * wx) + uz * (vx * wy - vy * wx)


class Margin:
    def __init__(self):
        self.m = None

    def sign(self, x):
        ax = abs(float(x)) if x != 0 else 0.0
        if self.m is None or ax < self.m:
            self.m = ax
        return (x > 0) - (x < 0)


def seg_meets_tri(p, q, a, b, c, M):
    s1, s2 = M.sign(orient(a, b, c, p)), M.sign(orient(a, b, c, q))
    if s1 == 0 and s2 == 0:
        return None  # coplanar: report
    if s1 * s2 > 0:
        return False
    t = [M.sign(orient(p, q, a, b)), M.sign(orient(p, q, b, c)), M.sign(orient(p, q, c, a))]
    return all(x >= 0 for x in t) or all(x <= 0 for x in t)


def main(path, k):
    r = json.load(open(path))
    lab, gname = r["label"], r["group"]
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES[lab]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    F, E, W = s["faces"], s["E"], s["w"]
    group = symmetry_group(s["V"], s["E"], W)
    if gname == "rotations":
        group = [(a, M) for a, M in group if det3(M) == ONE]
    syms, eqs, pos, info = reduced_system(s["V"], s["E"], W, group)
    vals = r["solutions"][k]["values"]
    f = sp.lambdify(syms, eqs, "mpmath")
    Jm = sp.lambdify(syms, sp.Matrix(eqs).jacobian(syms), "mpmath")
    x = mp.matrix([mp.mpf(vals[str(v)]) for v in syms])
    for _ in range(8):
        x = x - mp.lu_solve(mp.matrix(Jm(*x)), mp.matrix(f(*x)))
    res = mp.norm(mp.matrix(f(*x)))
    posf = sp.lambdify(syms, sp.Matrix(pos), "mpmath")
    Pm = posf(*x)
    sc = [mp.sqrt(mp.mpf(w.a.numerator) / w.a.denominator + mp.mpf(w.b.numerator) / w.b.denominator * mp.sqrt(5))
          for w in W]
    P = [tuple(Fr(mp.nstr(Pm[i, j] * sc[j], 85)) for j in range(3)) for i in range(len(pos))]
    M = Margin()
    L = [sum((P[a][i] - P[b][i]) ** 2 for i in range(3)) for a, b in E]
    edge_err = max(abs(float(l - 1)) for l in L)
    bad = []
    coplanar_flags = []
    for fi, gi in itertools.combinations(range(len(F)), 2):
        f_, g_ = F[fi], F[gi]
        sh = set(f_) & set(g_)
        A = [P[v] for v in f_]; B = [P[v] for v in g_]
        if len(sh) == 2:
            a, b = sorted(sh)
            o1 = next(v for v in f_ if v not in sh); o2 = next(v for v in g_ if v not in sh)
            sg = M.sign(orient(P[a], P[b], P[o1], P[o2]))
            if sg == 0:
                coplanar_flags.append((fi, gi, "edge-sharing faces coplanar"))
            continue
        for (X, Y, fx, gy) in ((A, B, f_, g_), (B, A, g_, f_)):
            for i in range(3):
                p, q = fx[i], fx[(i + 1) % 3]
                if p in sh or q in sh:
                    if len(sh) == 1:
                        w_ = q if p in sh else p
                        if M.sign(orient(*Y, P[w_])) == 0:
                            coplanar_flags.append((fi, gi, "edge through shared vertex coplanar"))
                    continue
                t = seg_meets_tri(P[p], P[q], *Y, M)
                if t is None:
                    coplanar_flags.append((fi, gi, "coplanar edge"))
                elif t:
                    bad.append((fi, gi, (p, q)))
    out = {"label": lab, "group": gname, "solution": k, "newton_residual": float(res), "edge_length_error": edge_err,
           "intersections": len(bad), "first_intersections": bad[:5], "coplanar_flags": coplanar_flags[:10],
           "smallest_deciding_predicate": M.m,
           "embedded": not bad and not coplanar_flags and M.m > 1e-40 and edge_err < 1e-50}
    print(json.dumps(out))
    json.dump({"check": out, "coordinates_85_digits": [[str(c) for c in mp.matrix([[0]])] if False else
                                                        [mp.nstr(Pm[i, j] * sc[j], 60) for j in range(3)]
                                                        for i in range(len(pos))], "faces": F},
              open(f"data/form_{lab}_{gname}_{k}.json", "w"), indent=1)
    return out


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
