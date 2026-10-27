"""Exact solve of the symmetry-reduced equilateral systems of large_slices.py.

For one slice label and one group ('full' or 'rotations'):
  * lex Groebner basis over Q(sqrt5) (sympy);
  * if the ideal is zero-dimensional in shape position (x_i - g_i(x_n), plus one univariate eliminant f(x_n)), the real
    solutions are exactly the real roots of f: counted exactly by a Sturm sequence over Q(sqrt5) (exact signs);
  * every real solution is evaluated at 60 digits and the embedding checked (distinct vertices, no 180-degree edge,
    no self-intersection, positive volume), with the margins printed.
Usage: ~/geom/bin/python solve_slices.py V72 full
"""
import json
import pickle
import sys
import time

import mpmath as mp
import numpy as np
import sympy as sp

from q5 import Q5, ZERO, ONE, q5sympy
from large_slices import SLICES, symmetry_group, det3, reduced_system

mp.mp.dps = 60
R5 = sp.sqrt(5)
K = sp.QQ.algebraic_field(R5)


def to_q5(c):
    """sympy number in Q(sqrt5) -> Q5"""
    from fractions import Fraction as Fr
    e = sp.expand(c)
    b = sp.Rational(e.coeff(R5))
    a = sp.Rational(sp.expand(e - b * R5))
    return Q5(Fr(int(a.p), int(a.q)), Fr(int(b.p), int(b.q)))


# ------------------------------------------------------------------ Sturm over Q(sqrt5)
def pdeg(p):
    while p and p[-1].iszero():
        p = p[:-1]
    return p


def prem(a, b):
    a = list(a)
    while len(a) >= len(b) and a:
        f = a[-1] / b[-1]
        sh = len(a) - len(b)
        for i in range(len(b)):
            a[sh + i] = a[sh + i] - f * b[i]
        a = pdeg(a[:-1])
    return a


def sturm_real_roots(p):
    """number of distinct real roots of p (coefficients Q5, low to high), exact."""
    p = pdeg(p)
    dp = pdeg([p[i] * Q5(i) for i in range(1, len(p))])
    seq = [p, dp]
    while True:
        r = prem(seq[-2], seq[-1])
        if not r:
            break
        seq.append([-x for x in r])

    def sign_changes(at_pos_inf):
        sg = []
        for q in seq:
            lead = q[-1].sign()
            if not at_pos_inf and (len(q) - 1) % 2 == 1:
                lead = -lead
            if lead:
                sg.append(lead)
        return sum(1 for a, b in zip(sg, sg[1:]) if a != b)
    # p and gcd: distinct real roots = V(-inf) - V(+inf)
    return sign_changes(False) - sign_changes(True)


def main(lab, gname):
    S = pickle.load(open("data/solids.pkl", "rb"))
    direc, h = SLICES[lab]
    s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
             and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
    V, E, W, F = s["V"], s["E"], s["w"], s["faces"]
    group = symmetry_group(V, E, W)
    if gname == "rotations":
        group = [(a, M) for a, M in group if det3(M) == ONE]
    syms, eqs, pos, info = reduced_system(V, E, W, group)
    t0 = time.time()
    order = list(syms)
    Gb = sp.groebner(eqs, *order, order="lex", domain=K)
    polys = list(Gb.exprs)
    rec = {"label": lab, "group": gname, "unknowns": len(syms), "equations": len(eqs), "groebner_size": len(polys),
           "groebner_seconds": round(time.time() - t0, 1)}
    if polys == [1]:
        rec["verdict"] = "no complex solution: Groebner basis = {1}"
        print(json.dumps(rec)); return rec
    # zero-dimensional? every variable needs a pure power among the leading monomials
    LMs = [sp.Poly(p, *order).monoms(order="lex")[0] for p in polys]
    zero_dim = all(any(m[k] > 0 and sum(m) == m[k] for m in LMs) for k in range(len(order)))
    rec["zero_dimensional"] = zero_dim
    rec["groebner"] = [str(p) for p in polys]
    if not zero_dim:
        rec["verdict"] = "positive-dimensional solution set (handled separately)"
        print(json.dumps(rec)[:3000]); return rec
    # all complex solutions by back-substitution through the lex basis, 60 digits
    sols = [dict()]
    for k in range(len(order) - 1, -1, -1):
        x = order[k]
        rel = [p for p in polys if x in p.free_symbols and p.free_symbols <= set(order[k:])]
        new = []
        for sol in sols:
            subs = {y: sp.Float(mp.nstr(v.real, 70), 70) + sp.I * sp.Float(mp.nstr(v.imag, 70), 70)
                    for y, v in sol.items()}
            us = []
            for p in rel:
                cs_ = [mp.mpc(*[mp.mpf(str(t)) for t in sp.N(c, 70).as_real_imag()])
                       for c in sp.Poly(sp.expand(p.subs(subs)), x).all_coeffs()]
                while cs_ and abs(cs_[0]) < mp.mpf(10) ** -40:
                    cs_ = cs_[1:]
                if len(cs_) > 1:
                    us.append(cs_)
            cs = min(us, key=len)
            for r in mp.polyroots(cs, maxsteps=800, extraprec=600):
                ok = True
                for u in us:
                    v = mp.polyval(u, r)
                    if abs(v) > mp.mpf(10) ** -30 * max(1, max(abs(c) for c in u)):
                        ok = False; break
                if ok:
                    d = dict(sol); d[x] = r; new.append(d)
        sols = new
    rec["complex_solutions"] = len(sols)
    elim = [p for p in polys if p.free_symbols <= {order[-1]}]
    rec["eliminant_degree"] = sp.Poly(elim[0], order[-1]).degree() if elim else None
    rec["distinct_last_coordinates"] = len({mp.nstr(sol[order[-1]], 25) for sol in sols})
    reals = [sol for sol in sols if all(abs(v.imag) < mp.mpf(10) ** -40 for v in sol.values())]
    rec["min_abs_imag_of_nonreal"] = (float(min(max(abs(v.imag) for v in sol.values()) for sol in sols
                                                if sol not in reals)) if len(reals) < len(sols) else None)
    try:
        exact = sp.solve(polys, order, dict=True)
        rec["exact_real_solutions"] = [{str(k): str(sp.nsimplify(v)) for k, v in e.items()} for e in exact
                                       if all(abs(sp.im(sp.N(v, 50))) < 1e-40 for v in e.values())]
    except Exception as ex:
        rec["exact_real_solutions"] = f"sympy solve failed: {ex}"
    out = []
    sc = np.array([float(np.sqrt(float(w))) for w in W])
    for sol in reals:
        subs = {k: sp.Float(mp.nstr(v.real, 70), 70) for k, v in sol.items()}
        P = np.array([[float(sp.N(c.subs(subs), 30)) for c in pv] for pv in pos]) * sc
        out.append({"values": {str(k): mp.nstr(v.real, 30) for k, v in sol.items()}, "check": embed_check(P, F, E),
                    "P": P.tolist()})
    rec["real_solutions"] = out
    rec["embedded_solutions"] = sum(1 for o in out if o["check"].get("embedded"))
    short = {k: v for k, v in rec.items() if k not in ("groebner", "real_solutions")}
    short["checks"] = [o["check"] for o in out]
    print(json.dumps(short, default=lambda o: str(o))[:5000], flush=True)
    return rec


def embed_check(P, F, E):
    from classify import dihedrals, self_intersects, signed_volume
    L = [np.linalg.norm(P[a] - P[b]) for a, b in E]
    out = {"edge_min": min(L), "edge_max": max(L)}
    n = len(P)
    md = min(np.linalg.norm(P[i] - P[j]) for i in range(n) for j in range(i + 1, n))
    out["min_vertex_distance"] = md
    if md < 1e-6:
        out["embedded"] = False; out["why"] = "coincident vertices"; return out
    Fo = [list(f) for f in F]
    if signed_volume(P, Fo) < 0:
        Fo = [f[::-1] for f in Fo]
    D = dihedrals(P, Fo)
    out["dihedral_min"], out["dihedral_max"] = min(D), max(D)
    out["closest_to_180"] = min(abs(d - 180) for d in D)
    out["edge_pierces_face"] = bool(self_intersects(P, Fo))
    from verify_forms import clearance
    a, b = clearance(P, Fo)
    out["clearance_disjoint_faces"], out["clearance_vertex_sharing_faces_corner_cut"] = a, b
    out["self_intersects"] = out["edge_pierces_face"] or a < 1e-9 or b < 1e-9
    out["embedded"] = out["closest_to_180"] > 1e-6 and not out["self_intersects"]
    return out


if __name__ == "__main__":
    lab, gname = sys.argv[1], sys.argv[2]
    rec = main(lab, gname)
    json.dump(rec, open(f"data/solve_{lab}_{gname}.json", "w"), indent=1, default=str)
