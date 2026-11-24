#!/usr/bin/env python3
"""Rings in fins, struts at the centre: exact quantities for the 163 catalogue polyhedra (25 Nov 2026).

For every polyhedron of study 2026-11-24-vacuus-resonus-catalogue (same builders, same centres: symmetry centre;
Johnson polyhedra about the corner centroid and the volume centroid) and every edge ab, the fin is the triangle O, a, b.
With A = |Oa|^2, B = |Ob|^2, C = |ab|^2 (exact field elements):
  ring (incircle) radius   r = sqrt(4AB - (A+B-C)^2) / (2 (sqrt A + sqrt B + sqrt C))
  tangent length from O    t = (sqrt A + sqrt B - sqrt C) / 2      (where the ring touches the spokes Oa and Ob)
  central angle aOb        cos = (A + B - C) / (2 sqrt(A B))
Fins are grouped by the exact key (unordered {A, B}, C): one key = congruent fins. Distinct keys are compared by
rigorous interval arithmetic (mpmath iv around a certified enclosure of the field generator; Arb balls for J84-J90).
Struts (item 3): the smallest angle between any two corner directions, from all pairs, by the same intervals.
Johnson polyhedra also: is there a sphere through all corners whose centre is strictly inside (exact)?
Output data/rings-catalogue.json; FINAL ok only if every comparison was decided.
Run: PROCS=3 python rings_catalogue.py [names...]
"""
import os, sys, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
CAT = os.path.normpath(os.path.join(HERE, "../../2026-11-24-vacuus-resonus-catalogue/scripts"))
sys.path.insert(0, CAT)
import catalogue as C            # sets the rigorous sign, imports VX, JX (enumeration builders, unchanged)
VX, JX = C.VX, C.JX
import mpmath as mp
from flint import arb, arb_poly, ctx
import multiprocessing as mpr
from vacuus_exact import vsub, dot, cross

DPS = 60
mp.mp.dps = 90; mp.iv.dps = 90
def M(x): return mp.mpf(x.mid)

def ival(F, a):
    """rigorous interval of a field element"""
    if isinstance(F, C.NF):
        old = ctx.prec; ctx.prec = 400
        v = arb_poly([arb(c) for c in a.p.coeffs()])(F.ball(400)) if not a.p.is_zero() else arb(0)
        mid = mp.mpf(v.mid().str(110, radius=False)); rad = mp.mpf(v.rad().str(10, radius=False)) if v.rad() != 0 else mp.mpf(0)
        ctx.prec = old
        rad += mp.mpf(10) ** -100
        return mp.iv.mpf([mid - rad, mid + rad])
    k = F.key(a)
    lo, hi = C._alpha_iv(F, DPS)
    A = mp.iv.mpf([lo, hi]); v = mp.iv.mpf(0)
    for co in k:
        v = v * A + mp.iv.mpf(int(co.numerator)) / int(co.denominator)
    return v

def cluster(items):
    """items: list of (key, interval). Groups keys whose intervals overlap (chains). Returns list of groups and
    flag 'decided': every two different groups are disjoint, and inside a group all keys equal OR flagged."""
    items = sorted(items, key=lambda kv: kv[1].a)
    groups = []
    for k, iv in items:
        if groups and iv.a <= groups[-1]["hi"]:
            g = groups[-1]; g["keys"].append(k); g["hi"] = max(g["hi"], iv.b)
        else:
            groups.append({"keys": [k], "lo": iv.a, "hi": iv.b, "iv": iv})
    return groups

def s(x, n=25): return mp.nstr(M(x) if hasattr(x, "mid") else x, n)

def analyse_fins(F, W, faces, label):
    edges = set()
    for f in faces:
        p = f["verts"]
        for j in range(len(p)):
            a, b = p[j], p[(j + 1) % len(p)]
            edges.add((min(a, b), max(a, b)))
    edges = sorted(edges)
    n2 = [dot(v, v) for v in W]
    n2iv = [ival(F, x) for x in n2]
    sq = [mp.iv.sqrt(x) for x in n2iv]
    cls = {}
    for a, b in edges:
        d = vsub(W[a], W[b]); Cc = dot(d, d)
        ka, kb = F.key(n2[a]), F.key(n2[b])
        key = (tuple(sorted([ka, kb])), F.key(Cc))
        if key not in cls:
            Ai, Bi, Ci = n2iv[a], n2iv[b], ival(F, Cc)
            sa, sb, sc = sq[a], sq[b], mp.iv.sqrt(Ci)
            area2 = mp.iv.sqrt(4 * Ai * Bi - (Ai + Bi - Ci) ** 2)     # = 2 * area * 2 / ... : |a x b| * 2 / 2
            r = area2 / (2 * (sa + sb + sc))
            t = (sa + sb - sc) / 2
            cosang = (Ai + Bi - Ci) / (2 * sa * sb)
            el = sc
            cls[key] = {"count": 0, "r": r, "t": t, "cos": cosang, "edge": el, "A": str(n2[a]), "B": str(n2[b]), "C": str(Cc),
                        "ends_equal_radius": ka == kb}
        cls[key]["count"] += 1
    keys = list(cls)
    rg = cluster([(k, cls[k]["r"]) for k in keys])
    tg = cluster([(k, cls[k]["t"]) for k in keys])
    ag = cluster([(k, cls[k]["cos"]) for k in keys])
    undecided = [g for g in rg + tg + ag if len(g["keys"]) > 1]
    emin = min(cls[k]["edge"].a for k in keys)
    rmax = max(cls[k]["r"].b for k in keys)
    # struts: all pairs of corner directions
    best = None; pairs = []
    n = len(W)
    for i in range(n):
        for j in range(i + 1, n):
            dd = dot(W[i], W[j])
            key = (tuple(sorted([F.key(n2[i]), F.key(n2[j])])), F.key(dd))
            pairs.append((key, i, j, dd))
    pk = {}
    for key, i, j, dd in pairs:
        if key not in pk:
            pk[key] = (ival(F, dd) / (sq[i] * sq[j]), i, j, dd)
    cmax_lo = max(v[0].a for v in pk.values())
    top = [k for k, v in pk.items() if v[0].b >= cmax_lo]
    c = pk[top[0]][0]
    c_exact = None
    if len(top) == 1 and top[0][0][0] == top[0][0][1]:
        _, i, j, dd = pk[top[0]]
        q = dd / n2[i]
        c_exact = str(F.K.to_sympy(q)) if hasattr(F, "K") else "poly " + str(q.p)
    Rr = mp.iv.sqrt(2 / (1 - c)); ar = mp.iv.sqrt((1 + c) / (1 - c))
    out = {
        "label": label, "V": n, "E": len(edges),
        "fin_classes": [{"count": cls[k]["count"], "A": cls[k]["A"], "B": cls[k]["B"], "C": cls[k]["C"],
                         "r_over_edge_min": s(cls[k]["r"] / emin), "t_over_edge_min": s(cls[k]["t"] / emin),
                         "angle_deg": s(mp.degrees(mp.acos(M(cls[k]["cos"])))), "r_over_rmax": s(cls[k]["r"] / rmax)}
                        for k in sorted(keys, key=lambda k: -M(cls[k]["r"]))],
        "n_fin_classes": len(keys),
        "n_radii": len(rg), "n_tangent_lengths": len(tg), "n_angles": len(ag),
        "radii_ratio_to_max": [s(g["iv"] / rmax) for g in sorted(rg, key=lambda g: -g["lo"])],
        "all_fins_congruent": len(keys) == 1,
        "equal_inradius": verdict(keys, rg),
        "equal_tangent_length": verdict(keys, tg),
        "equal_central_angle": verdict(keys, ag),
        "undecided_groups": len(undecided),
        "strut_cos_min_angle": s(c, 30), "strut_cos_exact": c_exact,
        "strut_min_angle_deg": s(mp.degrees(mp.acos(M(c))), 20),
        "core_R_over_r_sphere_cut": s(Rr, 25), "core_a_over_r_flat_cut": s(ar, 25),
        "strut_min_pairs_keys": len(top),
    }
    return out

def verdict(keys, groups):
    """yes: one congruence class; no: two disjoint intervals (certified); UNDECIDED: one interval group, several classes"""
    if len(keys) == 1: return "yes"
    if len(groups) > 1: return "no"
    return "UNDECIDED"

def circumcentre(F, W, faces):
    """exact: a point c with |w - c| equal for all corners, strictly inside? None if no such sphere"""
    n2 = [dot(v, v) for v in W]
    base = W[0]
    rows = []
    for i in range(1, len(W)):
        rows.append((tuple(2 * (x - y) for x, y in zip(W[i], base)), n2[i] - n2[0]))
    # find 3 independent rows
    for (r1, b1), (r2, b2), (r3, b3) in itertools.combinations(rows, 3):
        det = dot(r1, cross(r2, r3))
        if det:
            break
    else:
        return {"sphere": False, "why": "degenerate"}
    def d3(a, b, c): return dot(a, cross(b, c))
    cols = list(zip(r1, r2, r3))
    M = [r1, r2, r3]; bb = [b1, b2, b3]
    def rep(k):
        R = [list(M[i]) for i in range(3)]
        for i in range(3): R[i][k] = bb[i]
        return d3(tuple(R[0]), tuple(R[1]), tuple(R[2]))
    c = tuple(rep(k) / det for k in range(3))
    ok = all(not (dot(r, c) - b) for r, b in rows)
    if not ok:
        return {"sphere": False}
    inside = all(F.sign(dot(f["N"], c) - f["d"]) < 0 for f in faces)
    return {"sphere": True, "inside": inside, "c": c}

def task(t):
    kind, arg = t; t0 = time.time(); rows = []
    try:
        if kind == "uniform":
            nm = arg; F, gen, grp = C.S[nm]
            if nm == "snub dodecahedron":
                V = None
                for cand in gen:
                    Vc = VX.build_set(F, cand)
                    try:
                        if len(Vc) == 60: VX.analyse("probe", F, Vc, True); V = Vc; break
                    except AssertionError:
                        pass
            else:
                V = VX.build_set(F, gen)
            r, faces = VX.analyse(nm, F, V, True)
            fam = "Platonic" if nm in C.PLATONIC else "Archimedean"
            rows.append({"name": nm, "family": fam, **analyse_fins(F, V, faces, "symmetry centre")})
            dn = {"cube": "octahedron (polar of the cube)", "octahedron": "cube (polar of the octahedron)", "tetrahedron": "tetrahedron (polar)",
                  "dodecahedron": "icosahedron (polar of the dodecahedron)", "icosahedron": "dodecahedron (polar of the icosahedron)"}.get(nm, C.CATALAN.get(nm))
            D = VX.dual_vertices(F, faces); r2, f2 = VX.analyse(dn, F, D, False)
            rows.append({"name": dn, "family": "Catalan" if nm in C.CATALAN else "Platonic polar", **analyse_fins(F, D, f2, "symmetry centre")})
        elif kind == "prism":
            n = arg; F, pr, ap = VX.prism_family(n)
            for nm, V0, fam, dn, dfam in ((f"{n}-gonal prism", pr, "prism", f"{n}-gonal bipyramid", "bipyramid"),
                                          (f"{n}-gonal antiprism", ap, "antiprism", f"{n}-gonal trapezohedron", "trapezohedron")):
                V = VX.build_set(F, V0); r, faces = VX.analyse(nm, F, V, True)
                rows.append({"name": nm, "family": fam, **analyse_fins(F, V, faces, "symmetry centre")})
                D = VX.dual_vertices(F, faces); r2, f2 = VX.analyse(dn, F, D, False)
                rows.append({"name": dn, "family": dfam, **analyse_fins(F, D, f2, "symmetry centre")})
        else:
            nm = arg; F, V, recipe = C.johnson_solid(nm)
            Oc, Ov = JX.centroids(F, V)
            row = {"name": nm, "family": "Johnson"}
            for lab, O in (("corner", Oc), ("volume", Ov)):
                W = [vsub(v, O) for v in V]
                r, faces = VX.analyse(nm, F, W, True, None, check_centre=False)
                row[lab] = analyse_fins(F, W, faces, lab + " centroid")
                if lab == "corner":
                    cc = circumcentre(F, W, faces)
                    row["circumsphere"] = {k: v for k, v in cc.items() if k != "c"}
                    if cc.get("sphere") and cc.get("inside"):
                        W2 = [vsub(w, cc["c"]) for w in W]
                        r, faces2 = VX.analyse(nm, F, W2, True, None, check_centre=False)
                        row["circumcentre"] = analyse_fins(F, W2, faces2, "circumcentre")
            rows.append(row)
    except Exception as e:
        import traceback
        return {"task": t, "error": repr(e), "tb": traceback.format_exc()}
    return {"task": t, "rows": rows, "secs": round(time.time() - t0, 1)}

if __name__ == "__main__":
    only = sys.argv[1:]
    procs = int(os.environ.get("PROCS", "3"))
    C.S = VX.uniform_solids()
    tasks = [("uniform", nm) for nm in C.S] + [("prism", n) for n in range(3, 13)]
    os.chdir(C.VE)
    for m in (3, 4, 5, 6, 8, 10): JX.axial(m)
    JX.prisms_augmented(); JX.gyrobifastigium(); JX.platonic_archimedean_based()
    import sympy as sp
    JX.recognise("J91_BILUNABIROTUNDA", [sp.sqrt(5)], [sp.Integer(1), sp.sqrt(5)])
    JX.recognise("J92_TRIANGULAR_HEBESPHENOROTUNDA", [sp.sqrt(3), sp.sqrt(5)], [sp.Integer(1), sp.sqrt(3), sp.sqrt(5), sp.sqrt(15)])
    os.chdir(HERE)
    C.J8X.update(json.load(open(os.path.join(C.STUDY, "data/j84_90_exact.json"))))
    names = sorted(set(JX.BUILT) | {k for k in JX.REG if k.split("_")[0] in C.J8X}, key=lambda s: int(s.split("_")[0][1:]))
    assert len(names) == 92
    tasks += [("johnson", nm) for nm in names]
    if only:
        tasks = [t for t in tasks if str(t[1]) in only or str(t[1]).split("_")[0] in only]
    heavy = ("snub dodecahedron", "truncated icosidodecahedron", "rhombicosidodecahedron", "truncated icosahedron", "truncated dodecahedron", "snub cube")
    tasks.sort(key=lambda t: (t[1] not in heavy, str(t)))
    print("tasks", len(tasks), flush=True)
    out, bad = [], []
    with mpr.get_context("fork").Pool(procs) as pool:
        for i, res in enumerate(pool.imap_unordered(task, tasks)):
            if "error" in res:
                bad.append(res); print("ERROR", res["task"], res["error"], res["tb"], flush=True)
            else:
                out += res["rows"]
                for r in res["rows"]:
                    a = r.get("corner", r)
                    print(f"PROGRESS {(i + 1) / len(tasks):.3f} {r['name']}: classes {a['n_fin_classes']} radii {a['n_radii']} "
                          f"t {a['n_tangent_lengths']} strut {a['strut_min_angle_deg'][:8]} R/r {a['core_R_over_r_sphere_cut'][:8]} ({res['secs']}s)", flush=True)
    tag = "pilot" if only else "all"
    json.dump(out, open(os.path.join(STUDY, f"data/rings-catalogue-{tag}.json"), "w"), indent=1, default=str)
    nrows = len(out)
    und = sum(1 for r in out for a in ([r[k] for k in ("corner", "volume", "circumcentre") if k in r] or [r]) if a["undecided_groups"])
    print("rows", nrows, "errors", len(bad), "undecided", und, flush=True)
    print("FINAL ok" + (" (pilot)" if only else "") if not bad and (only or nrows == 168) else f"FINAL FAIL errors {len(bad)} rows {nrows}")
