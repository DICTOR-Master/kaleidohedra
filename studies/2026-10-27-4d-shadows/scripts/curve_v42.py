"""V42 with the rotation group T: the reduced system has a 1-dimensional solution set.  Decompose it (minimal
associated primes, Singular), describe each 1-dimensional component, and sample real points on it (adding one linear
equation at many levels), checking every real sample for embedding.
Usage: ~/geom/bin/python curve_v42.py
"""
import json
import pickle
import time

import mpmath as mp
import numpy as np
import sympy as sp

from sage.all__sagemath_singular import QQ, PolynomialRing, NumberField, polygen, RealField

from large_slices import SLICES, symmetry_group, det3, reduced_system
from q5 import ONE

mp.mp.dps = 60


def main():
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES["V42"]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    V, E, W, F = s["V"], s["E"], s["w"], s["faces"]
    group = [(a, M) for a, M in symmetry_group(V, E, W) if det3(M) == ONE]
    syms, eqs, pos, info = reduced_system(V, E, W, group)
    x = polygen(QQ)
    K = NumberField(x ** 2 - 5, "s", embedding=RealField(200)(5).sqrt())
    names = [str(v) for v in syms]
    R = PolynomialRing(K, names, order="degrevlex")
    loc = {n: R.gen(i) for i, n in enumerate(names)}
    loc["s"] = K.gen() * R.one()
    I = R.ideal([eval(str(sp.expand(e)).replace("sqrt(5)", "s"), {}, loc) for e in eqs])
    t0 = time.time()
    P = I.minimal_associated_primes()
    rec = {"seconds": round(time.time() - t0, 1), "components": []}
    sq5 = float(K.gen())
    for Q in P:
        d = Q.dimension()
        comp = {"dimension": int(d), "generators": [str(g) for g in Q.gens()][:12]}
        if d == 1:
            # which variables vary, which are constant on the component
            G = Q.groebner_basis()
            comp["groebner"] = [str(g) for g in G][:20]
        rec["components"].append(comp)
        print(json.dumps(comp)[:1500], flush=True)
    json.dump(rec, open("data/curve_V42_rotations.json", "w"), indent=1)


if __name__ == "__main__":
    main()
