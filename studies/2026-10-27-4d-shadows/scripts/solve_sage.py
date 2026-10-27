"""Exact solve of the symmetry-reduced equilateral systems with Singular (passagemath-singular in the geom venv).

Field K = Q(s), s^2 = 5, embedded with s = +sqrt5.  For one slice and one group ('full' or 'rotations'):
  * Groebner basis (Singular), Krull dimension;
  * zero-dimensional: all real solutions exactly as real algebraic numbers (Sage AA, variety over AA), each with its
    vertex coordinates evaluated to 60 digits and checked for embedding (solve_slices.embed_check: distinct
    vertices, no 180-degree edge, clearance between faces);
  * positive-dimensional: reported (dimension, number of components) for separate treatment.
Usage: ~/geom/bin/python solve_sage.py V30 full
"""
import json
import sys
import time

import numpy as np
import sympy as sp

from sage.all__sagemath_singular import QQ, PolynomialRing, NumberField, polygen, RealField, ComplexField

from large_slices import SLICES, symmetry_group, det3, reduced_system
from q5 import ONE

RF = RealField(220)


def back_substitute(I, R, names, K, CF):
    """all complex solutions of a zero-dimensional ideal: lex Groebner basis by FGLM (Singular), then root finding
    variable by variable (400 bits), keeping a root only where every basis element vanishes (< 1e-90)."""
    lexR = PolynomialRing(K, names, order="lex")
    G = [lexR(str(p)) for p in I.transformed_basis("fglm", lexR)] if False else list(
        I.transformed_basis("fglm", lexR))
    gens = lexR.gens()
    n = len(gens)
    emb = K.embeddings(CF)
    emb = [e for e in emb if e(K.gen()).real() > 0][0]
    Cx = PolynomialRing(CF, "u"); u = Cx.gen()
    tol = RealField(400)(10) ** -90
    sols = [dict()]
    for k in range(n - 1, -1, -1):
        rel = [p for p in G if p.degree(gens[k]) > 0 and all(p.degree(gens[j]) == 0 for j in range(k))]
        new = []
        for sol in sols:
            us = []
            for p in rel:
                q = Cx(0)
                for c, m in zip(p.coefficients(), p.monomials()):
                    term = CF(emb(c))
                    for j in range(k + 1, n):
                        e = m.degree(gens[j])
                        if e:
                            term *= sol[gens[j]] ** e
                    q += term * u ** m.degree(gens[k])
                cs = q.list()
                scale = max(abs(c) for c in cs) if cs else 0
                while cs and abs(cs[-1]) < tol * max(1, scale):
                    cs = cs[:-1]
                if len(cs) > 1:
                    us.append(Cx(cs))
            u0 = min(us, key=lambda q: q.degree())
            for r in u0.roots(multiplicities=False):
                if all(abs(q(r)) < RealField(400)(10) ** -60 * max(1, max(abs(c) for c in q.list())) for q in us):
                    d = dict(sol); d[gens[k]] = r; new.append(d)
        sols = new
    # dedupe
    out = []
    for so in sols:
        if not any(all(abs(so[g] - t[g]) < RealField(400)(10) ** -50 for g in gens) for t in out):
            out.append(so)
    return out


def main(lab, gname):
    import pickle
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES[lab]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    V, E, W, F = s["V"], s["E"], s["w"], s["faces"]
    group = symmetry_group(V, E, W)
    if gname == "rotations":
        group = [(a, M) for a, M in group if det3(M) == ONE]
    syms, eqs, pos, info = reduced_system(V, E, W, group)
    x = polygen(QQ)
    K = NumberField(x ** 2 - 5, "s", embedding=RF(5).sqrt())
    names = [str(v) for v in syms]
    R = PolynomialRing(K, names, order="degrevlex")
    loc = {n: R.gen(i) for i, n in enumerate(names)}
    loc["s"] = K.gen() * R.one()
    conv = lambda e: eval(str(sp.expand(e)).replace("sqrt(5)", "s").replace("^", "**"), {}, loc)
    I = R.ideal([conv(e) for e in eqs])
    t0 = time.time()
    dim = I.dimension()
    rec = {"label": lab, "group": gname, "group_order": len(group), "orbits": info, "unknowns": len(syms),
           "equations": len(eqs), "krull_dimension": int(dim), "seconds_dimension": round(time.time() - t0, 1)}
    if dim < 0:
        rec["verdict"] = "no complex solution (ideal = whole ring)"
    elif dim > 0:
        rec["verdict"] = "positive-dimensional"
        rec["primary_components"] = None
    else:
        rec["complex_solutions_with_multiplicity"] = int(I.vector_space_dimension())
        t1 = time.time()
        CF = ComplexField(400)
        allsols = back_substitute(I, R, names, K, CF)
        rec["distinct_complex_solutions"] = len(allsols)
        tiny = RealField(400)(10) ** -100
        sols = [so for so in allsols if all(abs(v.imag()) < tiny for v in so.values())]
        nonreal = [max(abs(v.imag()) for v in so.values()) for so in allsols if so not in sols]
        rec["min_imag_of_nonreal"] = float(min(nonreal)) if nonreal else None
        rec["seconds_variety"] = round(time.time() - t1, 1)
        rec["real_solutions"] = len(sols)
        # exact cross-check: real roots of the norm of the eliminant of the last unknown (Sturm, over Q)
        last = R.gen(len(names) - 1)
        el = I.elimination_ideal([R.gen(k) for k in range(len(names) - 1)]).gens()[0]
        coeffs = el.univariate_polynomial().list()
        Qx = PolynomialRing(QQ, "z"); z = Qx.gen()
        f1 = sum(Qx(list(c.vector())[0]) * z ** k for k, c in enumerate(coeffs))
        f2 = sum(Qx(list(c.vector())[1]) * z ** k for k, c in enumerate(coeffs))
        norm = f1 ** 2 - 5 * f2 ** 2
        rec["eliminant_degree_last_unknown"] = el.degree()
        rec["real_roots_of_norm_exact"] = int(norm.squarefree_decomposition().radical_value().number_of_real_roots())
        rec["distinct_real_last_coordinates"] = len({str(RealField(100)(so[last].real())) for so in sols})
        sc = np.array([float(np.sqrt(float(w))) for w in W])
        outs = []
        from solve_slices import embed_check
        for sol in sols:
            vals = {str(k): v.real() for k, v in sol.items()}
            sub = {sp.Symbol(k): sp.Float(str(v), 100) for k, v in vals.items()}
            P = np.array([[float(sp.N(c.subs(sub), 30)) for c in pv] for pv in pos]) * sc
            chk = embed_check(P, F, E)
            o = {"values_60": {k: str(v)[:64] for k, v in vals.items()}, "check": chk, "P": P.tolist()}
            outs.append(o)
        rec["solutions"] = outs
        rec["embedded_solutions"] = sum(1 for o in outs if o["check"].get("embedded"))
        rec["verdict"] = (f"{rec['embedded_solutions']} embedded of {len(sols)} real solutions")
    short = {k: v for k, v in rec.items() if k != "solutions"}
    if "solutions" in rec:
        short["checks"] = [{k: (round(v, 5) if isinstance(v, float) else v) for k, v in o["check"].items()}
                           for o in rec["solutions"]]
    print(json.dumps(short, default=str), flush=True)
    json.dump(rec, open(f"data/sage_{lab}_{gname}.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
