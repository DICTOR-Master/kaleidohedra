"""Numerical exploration of the real solutions of a reduced system (used where the exact solve shows a
positive-dimensional solution set): many random starts, Levenberg-Marquardt on the exact equations, then the
Jacobian rank at each real solution (rank < n marks a point on a curve of solutions) and the embedding check.
Numerical only: it can find embedded forms on the curve but cannot prove there are none.
Usage: ~/geom/bin/python explore_real.py V42 rotations 3000
"""
import json
import pickle
import sys

import numpy as np
import sympy as sp
from scipy.optimize import least_squares

from large_slices import SLICES, symmetry_group, det3, reduced_system
from q5 import ONE
from solve_slices import embed_check


def main(lab, gname, starts):
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES[lab]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    V, E, W, F = s["V"], s["E"], s["w"], s["faces"]
    group = symmetry_group(V, E, W)
    if gname == "rotations":
        group = [(a, M) for a, M in group if det3(M) == ONE]
    syms, eqs, pos, info = reduced_system(V, E, W, group)
    f = sp.lambdify([syms], eqs, "numpy")
    J = sp.lambdify([syms], sp.Matrix(eqs).jacobian(syms), "numpy")
    pf = sp.lambdify([syms], sp.Matrix(pos), "numpy")
    sc = np.array([float(np.sqrt(float(w))) for w in W])
    rng = np.random.default_rng(5)
    found = []
    stats = {"converged": 0, "rank_deficient": 0, "embedded": 0}
    emb = []
    for k in range(starts):
        x0 = rng.uniform(-1.5, 1.5, len(syms))
        r = least_squares(lambda x: np.array(f(x), float), x0, jac=lambda x: np.array(J(x), float),
                          method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
        if np.abs(r.fun).max() > 1e-12:
            continue
        stats["converged"] += 1
        x = r.x
        sv = np.linalg.svd(np.array(J(x), float), compute_uv=False)
        rd = bool(sv[-1] < 1e-7 * sv[0])
        stats["rank_deficient"] += rd
        P = np.array(pf(x), float).reshape(-1, 3) * sc
        chk = embed_check(P, F, E)
        why = chk.get("why") or ("flat edge" if chk.get("closest_to_180", 99) < 1e-6 else
                                 ("edge pierces face" if chk.get("edge_pierces_face") else
                                  ("faces touch" if chk.get("self_intersects") else "embedded")))
        key = ("curve " if rd else "isolated ") + why
        stats[key] = stats.get(key, 0) + 1
        if chk.get("embedded"):
            stats["embedded"] += 1
            emb.append({"x": x.tolist(), "rank_deficient": rd, "check": chk})
    out = {"label": lab, "group": gname, "starts": starts, **stats, "embedded_examples": emb[:5]}
    print(json.dumps({k: v for k, v in out.items() if k != "embedded_examples"}), flush=True)
    for e in emb[:5]:
        print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in e["check"].items()}), e["rank_deficient"])
    json.dump(out, open(f"data/explore_{lab}_{gname}.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
