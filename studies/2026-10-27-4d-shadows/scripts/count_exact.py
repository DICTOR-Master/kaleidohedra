"""Exact count of the distinct complex and of the real solutions of a zero-dimensional reduced system.

The multiplication matrix of a random rational linear form l on the quotient ring is built exactly over Q(sqrt5);
its characteristic polynomial chi(u) has the values of l at the solutions as roots (with multiplicity).  The
squarefree part of chi gives the number of distinct values, and its real roots (isolated exactly over the real
algebraic numbers) the number of real values.  A second random form is used to confirm that l separates the
solutions (same counts).
Usage: ~/geom/bin/python count_exact.py V42 rotations [sat:t0_0]
"""
import json
import pickle
import sys
import time

import numpy as np
import sympy as sp

from sage.all__sagemath_singular import QQ, AA, PolynomialRing, NumberField, polygen, RealField, matrix

from large_slices import SLICES, symmetry_group, det3, reduced_system
from q5 import ONE


def main(lab, gname, cut=None):
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES[lab]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    V, E, W = s["V"], s["E"], s["w"]
    group = symmetry_group(V, E, W)
    if gname == "rotations":
        group = [(a, M) for a, M in group if det3(M) == ONE]
    syms, eqs, pos, info = reduced_system(V, E, W, group)
    x = polygen(QQ)
    K = NumberField(x ** 2 - 5, "s", embedding=RealField(200)(5).sqrt())
    names = [str(v) for v in syms]
    R = PolynomialRing(K, names, order="degrevlex")
    loc = {n: R.gen(i) for i, n in enumerate(names)}
    loc["s"] = K.gen() * R.one()
    I = R.ideal([eval(str(sp.expand(e)).replace("sqrt(5)", "s"), {}, loc) for e in eqs])
    if cut and cut.startswith("sat:"):
        I = I.saturation(R.ideal(loc[cut[4:]]))[0]
    G = I.groebner_basis()
    B = list(I.normal_basis())
    N = len(B)
    idx = {b: i for i, b in enumerate(B)}
    rec = {"label": lab, "group": gname, "cut": cut, "N_with_multiplicity": N, "forms": []}
    Ku = PolynomialRing(K, "u")
    for seed in (7, 11):
        rng = np.random.default_rng(seed)
        cs = [int(c) for c in rng.integers(1, 97, len(syms))]
        ell = sum(c * g for c, g in zip(cs, R.gens()))
        t0 = time.time()
        M = matrix(K, N, N)
        for j, b in enumerate(B):
            r = (ell * b).reduce(G)
            for c, m in zip(r.coefficients(), r.monomials()):
                M[idx[m], j] = c
        chi = Ku(M.charpoly())
        sq = chi // chi.gcd(chi.derivative())
        real_roots = sq.change_ring(AA).roots(multiplicities=False) if False else None
        # real roots exactly: squarefree factorisation over K, then each factor's real roots in AA
        nreal = 0
        for fac, e in sq.factor():
            nreal += len(fac.change_ring(AA).roots(multiplicities=False))
        rec["forms"].append({"seed": seed, "distinct_values": int(sq.degree()), "real_values": nreal,
                             "seconds": round(time.time() - t0, 1)})
        print(json.dumps(rec["forms"][-1]), flush=True)
    json.dump(rec, open(f"data/count_{lab}_{gname}{'_' + cut.replace(':', '_') if cut else ''}.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
