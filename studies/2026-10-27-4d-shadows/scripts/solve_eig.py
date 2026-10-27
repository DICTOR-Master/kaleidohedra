"""All solutions of a symmetry-reduced equilateral system by the eigenvalue method, with a completeness check.

  * Groebner basis (degrevlex, Singular, exact over Q(sqrt5)); N = dim of the quotient ring (exact): the number of
    complex solutions counted with multiplicity;
  * multiplication matrix of a random rational linear form on the normal basis (exact over Q(sqrt5), then evaluated
    with sqrt5 > 0); its eigenvectors give candidate solutions;
  * every candidate refined by Newton on the exact equations at 120 digits; distinct refined solutions counted;
    if that count equals N, every solution is simple and none is missing (complete);
  * real solutions (|imaginary part| < 1e-80) checked for embedding (solve_slices.embed_check).
Usage: ~/geom/bin/python solve_eig.py V30 full
"""
import json
import pickle
import sys
import time

import mpmath as mp
import numpy as np
import sympy as sp

from sage.all__sagemath_singular import QQ, PolynomialRing, NumberField, polygen, RealField

from large_slices import SLICES, symmetry_group, det3, reduced_system
from q5 import ONE

mp.mp.dps = 120


def main(lab, gname, seed=7, cut=None):
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES[lab]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    V, E, W, F = s["V"], s["E"], s["w"], s["faces"]
    group = symmetry_group(V, E, W)
    if gname == "rotations":
        group = [(a, M) for a, M in group if det3(M) == ONE]
    syms, eqs, pos, info = reduced_system(V, E, W, group)
    if cut is not None and str(cut).startswith("sat:"):
        pass  # handled on the ideal below (saturation)
    elif cut is not None and str(cut).startswith("rab:"):
        # Rabinowitsch: keep only solutions with the named unknown nonzero (extra unknown z, z*t = 1)
        tv = sp.Symbol(cut[4:])
        zz = sp.Symbol("z")
        assert tv in syms
        eqs = list(eqs) + [zz * tv - 1]
        syms = list(syms) + [zz]
    elif cut is not None:
        # sample a positive-dimensional solution set: add one fixed rational linear equation
        rng0 = np.random.default_rng(1234)
        cc = [int(c) for c in rng0.integers(-9, 10, len(syms))]
        eqs = list(eqs) + [sum(c * v for c, v in zip(cc, syms)) - sp.Rational(cut)]
    x = polygen(QQ)
    K = NumberField(x ** 2 - 5, "s", embedding=RealField(200)(5).sqrt())
    sq5 = float(K.gen())
    assert sq5 > 0
    names = [str(v) for v in syms]
    R = PolynomialRing(K, names, order="degrevlex")
    loc = {n: R.gen(i) for i, n in enumerate(names)}
    loc["s"] = K.gen() * R.one()
    I = R.ideal([eval(str(sp.expand(e)).replace("sqrt(5)", "s"), {}, loc) for e in eqs])
    if cut is not None and str(cut).startswith("sat:"):
        t0 = time.time()
        I = I.saturation(R.ideal(loc[cut[4:]]))[0]
        print("saturation seconds", round(time.time() - t0, 1), flush=True)
    rec = {"cut": cut, "label": lab, "group": gname, "group_order": len(group), "orbits": info, "unknowns": len(syms),
           "equations": len(eqs)}
    t0 = time.time()
    G = I.groebner_basis()
    rec["seconds_groebner"] = round(time.time() - t0, 1)
    dim = I.dimension()
    rec["krull_dimension"] = int(dim)
    if dim != 0:
        rec["verdict"] = "no complex solution" if dim < 0 else "positive-dimensional"
        print(json.dumps(rec)); return rec
    B = list(I.normal_basis())
    N = len(B)
    rec["complex_solutions_with_multiplicity"] = N
    idx = {b: i for i, b in enumerate(B)}
    rng = np.random.default_rng(seed)
    cs = [int(c) for c in rng.integers(1, 97, len(syms))]
    ell = sum(c * g for c, g in zip(cs, R.gens()))

    def kfl(c):
        v = list(c.vector())
        return float(v[0]) + float(v[1]) * sq5
    M = np.zeros((N, N))
    t0 = time.time()
    for j, b in enumerate(B):
        r = (ell * b).reduce(G)
        for c, m in zip(r.coefficients(), r.monomials()):
            M[idx[m], j] = kfl(c)
    rec["seconds_matrix"] = round(time.time() - t0, 1)
    # left eigenvectors: M^T v = lambda v, v_b = b(p)
    w, Vec = np.linalg.eig(M.T)
    one = idx[R.one()]
    # value of each unknown as a linear form in the normal-basis monomials (its normal form)
    nf = np.zeros((len(syms), N))
    for i, g in enumerate(R.gens()):
        r = g.reduce(G)
        for c, m in zip(r.coefficients(), r.monomials()):
            nf[i, idx[m]] = kfl(c)
    cand = [(nf @ Vec[:, k]) / Vec[one, k] for k in range(N)]
    # Newton refinement at 120 digits on the exact equations
    f = sp.lambdify(syms, eqs, "mpmath")
    Jm = sp.lambdify(syms, sp.Matrix(eqs).jacobian(syms), "mpmath")
    sols = []
    for c0 in cand:
        xk = mp.matrix([mp.mpc(complex(z)) for z in c0])
        ok = False
        for it in range(60):
            fx = mp.matrix(f(*xk))
            if mp.norm(fx) < mp.mpf(10) ** -100:
                ok = True; break
            try:
                dx = mp.lu_solve(mp.matrix(Jm(*xk)), fx)
            except ZeroDivisionError:
                break
            xk = xk - dx
        if ok:
            if not any(mp.norm(xk - t) < mp.mpf(10) ** -60 for t in sols):
                sols.append(xk)
    rec["distinct_refined_solutions"] = len(sols)
    rec["complete"] = len(sols) == N
    if not rec["complete"]:
        # multiple roots? Newton converges only linearly at a multiple root, so count solutions with a singular
        # Jacobian, and repeat with two further random linear forms to see whether any new solution appears
        sing = 0
        for x_ in sols:
            Jx = np.array([[complex(v) for v in row] for row in mp.matrix(Jm(*x_)).tolist()])
            sv = np.linalg.svd(Jx, compute_uv=False)
            sing += bool(sv[-1] < 1e-8 * sv[0])
        rec["solutions_with_singular_jacobian"] = sing
        extra = 0
        for sd in (11, 23):
            rng2 = np.random.default_rng(sd)
            cs2 = [int(c) for c in rng2.integers(1, 97, len(syms))]
            ell2 = sum(c * g for c, g in zip(cs2, R.gens()))
            M2 = np.zeros((N, N))
            for jj, b in enumerate(B):
                r = (ell2 * b).reduce(G)
                for c, m in zip(r.coefficients(), r.monomials()):
                    M2[idx[m], jj] = kfl(c)
            w2, V2 = np.linalg.eig(M2.T)
            for k in range(N):
                c0 = (nf @ V2[:, k]) / V2[one, k]
                xk = mp.matrix([mp.mpc(complex(z)) for z in c0])
                for it in range(200):
                    fx = mp.matrix(f(*xk))
                    if mp.norm(fx) < mp.mpf(10) ** -100:
                        break
                    try:
                        xk = xk - mp.lu_solve(mp.matrix(Jm(*xk)), fx)
                    except ZeroDivisionError:
                        break
                if mp.norm(mp.matrix(f(*xk))) < mp.mpf(10) ** -40 and not any(mp.norm(xk - t) < mp.mpf(10) ** -20
                                                                             for t in sols):
                    sols.append(xk); extra += 1
        rec["new_solutions_from_two_more_linear_forms"] = extra
        rec["distinct_refined_solutions"] = len(sols)
    reals = [x_ for x_ in sols if all(abs(mp.im(z)) < mp.mpf(10) ** -30 for z in x_)]
    nonreal = [max(abs(mp.im(z)) for z in x_) for x_ in sols if not all(abs(mp.im(z)) < mp.mpf(10) ** -30 for z in x_)]
    rec["real_solutions"] = len(reals)
    rec["min_imag_of_nonreal"] = float(min(nonreal)) if nonreal else None
    sc = np.array([float(np.sqrt(float(w_))) for w_ in W])
    from solve_slices import embed_check
    posf = sp.lambdify(syms, sp.Matrix(pos), "mpmath")
    outs = []
    for x_ in reals:
        xr = [mp.re(z) for z in x_]
        Pm = posf(*xr)
        P = np.array([[float(Pm[i, j]) for j in range(3)] for i in range(len(pos))]) * sc
        chk = embed_check(P, F, E)
        outs.append({"values": {n: mp.nstr(z, 60) for n, z in zip(names, xr)}, "check": chk, "P": P.tolist()})
    rec["solutions"] = outs
    rec["embedded_solutions"] = sum(1 for o in outs if o["check"].get("embedded"))
    rec["verdict"] = f"{rec['embedded_solutions']} embedded of {len(reals)} real solutions (complete: {rec['complete']})"
    short = {k: v for k, v in rec.items() if k != "solutions"}
    short["checks"] = [{k: (round(v, 5) if isinstance(v, float) else v) for k, v in o["check"].items()} for o in outs]
    print(json.dumps(short, default=str), flush=True)
    tag = "" if cut is None else "_cut" + str(cut).replace("/", "over").replace("-", "m").replace(":", "_")
    json.dump(rec, open(f"data/eig_{lab}_{gname}{tag}.json", "w"), indent=1, default=str)
    return rec


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], cut=(sys.argv[3] if len(sys.argv) > 3 else None))
