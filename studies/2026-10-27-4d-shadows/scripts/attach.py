"""Attachability of the variants found (same face pattern as a convex deltahedron, other shape) against their regular
counterparts and the rest of their 4D shadow family; and exact deltahedral realisations of the two icosahedral
shadow patterns.  Exact (sympy); floats only to screen angle sums.

Variants (from shadows.py):
  TBP-5  : 5-cell edge-first (= face-first) shadow, graph of the triangular bipyramid J12
  OCT-16 : 16-cell edge-first shadow (= its central slice), graph of the octahedron
Run on dicto-big-brother after shadows.py:  ~/geom/bin/python attach.py
"""
import itertools
import json
import math
import pickle

import sympy as sp

from q5 import Q5, q5sympy, q5str

X = sp.Symbol("x")


def is_zero(e):
    e = sp.nsimplify(sp.expand(e)) if False else sp.expand(e)
    if e == 0:
        return True
    if abs(complex(sp.N(e, 50))) > 1e-30:
        return False
    return sp.minimal_polynomial(e, X) == X


def sums_to_2pi(cosines):
    """exact: sum of arccos(c_k) == 2*pi  <=>  prod (c_k + i s_k) == 1 (float screen picks the winding)."""
    tot = sum(math.acos(float(c)) for c in cosines)
    if abs(tot - 2 * math.pi) > 1e-9:
        return False
    z = sp.Integer(1)
    for c in cosines:
        z = sp.expand(z * (c + sp.I * sp.sqrt(1 - c ** 2)))
    return is_zero(sp.re(z) - 1) and is_zero(sp.im(z))


def solid_edges(s):
    """per edge: exact squared length, exact dihedral cosine, shapes of the two faces at that edge (squared side
    lengths of each face polygon, starting after the edge)."""
    V, F, w = s["V"], s["faces"], s["w"]

    def l2(a, b):
        u = [x - y for x, y in zip(V[a], V[b])]
        t = Q5(0)
        for x, ww in zip(u, w):
            t = t + x * x * ww
        return t
    ef = {}
    for fi, f in enumerate(F):
        for k in range(len(f)):
            a, b = f[k], f[(k + 1) % len(f)]
            ef.setdefault((min(a, b), max(a, b)), []).append(fi)
    out = []
    for (a, b), fs in ef.items():
        sg, c2, ang = s["dih"][(a, b)]
        cos = sg * sp.sqrt(q5sympy(c2))
        shapes = []
        for fi in fs:
            f = F[fi]
            sides = sorted(q5str(l2(f[k], f[(k + 1) % len(f)])) for k in range(len(f)))
            shapes.append((len(f), tuple(sides)))
        out.append({"L2": q5sympy(s["L2"][(a, b)]), "cos": sp.nsimplify(sp.radsimp(cos)), "deg": ang,
                    "faces": tuple(sorted(shapes))})
    return out


def regular(name, L2):
    """dihedral data of a regular convex deltahedron scaled to squared edge L2 (exact)."""
    eq = (3, tuple([q5str(Q5(0))] * 0))
    face = (3, tuple(sorted([str(L2)] * 3)))
    data = {"tetrahedron": [sp.Rational(1, 3)], "octahedron": [sp.Rational(-1, 3)],
            "triangular bipyramid (J12)": [sp.Rational(1, 3), sp.Rational(-7, 9)],
            "icosahedron": [-sp.sqrt(5) / 3]}[name]
    return [{"L2": L2, "cos": c, "deg": math.degrees(math.acos(float(c))), "faces": (face, face)} for c in data]


def stars(pool, maxk=8):
    """all multisets of dihedral angles from the pool (same edge length) with exact sum 2*pi."""
    res = []
    items = list(pool.items())
    for k in range(2, maxk + 1):
        for combo in itertools.combinations_with_replacement(range(len(items)), k):
            tot = sum(items[i][1]["deg"] for i in combo)
            if abs(tot - 360) > 1e-6:
                continue
            if sums_to_2pi([items[i][1]["cos"] for i in combo]):
                res.append([items[i][0] for i in combo])
    return res


def face_ok(star, pool):
    """necessary face-to-face condition round an edge: the 2k faces can be paired cyclically into congruent pairs
    (each tile may be turned over); checked over all cyclic orders."""
    tiles = [pool[n]["faces"] for n in star]
    k = len(tiles)
    for order in itertools.permutations(range(1, k)):
        seq = [0] + list(order)
        for flips in itertools.product((0, 1), repeat=k):
            ok = True
            for t in range(k):
                a = tiles[seq[t]][1 - flips[t]]           # right face of tile t
                b = tiles[seq[(t + 1) % k]][flips[(t + 1) % k]]  # left face of next
                if a != b:
                    ok = False; break
            if ok:
                return True
    return False


def main():
    S = pickle.load(open("data/solids.pkl", "rb"))

    def find(poly, direc, kind, height=None):
        for s in S:
            it = s["item"]
            if it["polytope"] == poly and it["direction"] == direc and it["kind"] == kind and \
                    (height is None or it.get("height") == height):
                return s
    report = {}
    cases = {
        "TBP-5": (find("5-cell", "edge-first", "shadow"), "triangular bipyramid (J12)", "5-cell"),
        "OCT-16": (find("16-cell", "edge-first", "shadow"), "octahedron", "16-cell"),
    }
    for label, (s, regname, poly) in cases.items():
        E = solid_edges(s)
        rec = {"solid": f'{s["item"]["polytope"]} {s["item"]["direction"]} {s["item"]["kind"]}', "regular": regname}
        # (1) faces
        fshapes = sorted({f for e in E for f in e["faces"]})
        rec["face_shapes"] = [list(f) for f in fshapes]
        rec["faces_all_congruent"] = len(fshapes) == 1
        rec["has_equilateral_face"] = any(len(set(f[1])) == 1 for f in fshapes)
        # (2) dihedrals
        dd = {}
        for e in E:
            dd.setdefault((str(e["L2"]), str(e["cos"])), []).append(e["deg"])
        rec["dihedrals"] = [{"edge_len2": k[0], "cos": k[1], "deg": round(v[0], 6), "edges": len(v)}
                            for k, v in dd.items()]
        # edge stars by edge length: pool = this variant + regular counterpart (scaled to that length) + the other
        # solids of the same 4D polytope (all its shadows, layers and slices) carrying an edge of that length
        rec["stars"] = []
        for L2 in sorted({e["L2"] for e in E}, key=float):
            pool, src = {}, {}

            def put(name, e):
                key = (str(e["cos"]), e["faces"])
                if key not in pool:
                    pool[key] = dict(e, name=name)
                src.setdefault(key, set()).add(name)
            for e in E:
                if e["L2"] == L2:
                    put(label, e)
            for nm in (regname, "tetrahedron", "octahedron"):
                for e in regular(nm, L2):
                    put("regular " + nm, e)
            fam_names = set()
            for t in S:
                ti = t["item"]
                if ti["polytope"] != poly or t is s:
                    continue
                for e in solid_edges(t):
                    if sp.simplify(e["L2"] - L2) == 0:
                        nm = f'{ti["polytope"]} {ti["direction"]} {ti["kind"]} {ti.get("height")}'
                        put(nm, e)
                        fam_names.add(nm)
            pool = {f'{min(src[k])} [{len(src[k])} sources] cos {k[0]} faces {k[1]}': v for k, v in pool.items()}
            st = stars(pool)
            rec["stars"].append({
                "edge_len2": str(L2), "pool_size": len(pool), "family_solids_with_this_edge": sorted(fam_names),
                "stars": [{"tiles": x, "face_to_face_possible": face_ok(x, pool)} for x in st]})
        report[label] = rec
        print(label, json.dumps({k: v for k, v in rec.items() if k != "stars"}, default=str), flush=True)
        for x in rec["stars"]:
            print("  edge^2", x["edge_len2"], "pool", x["pool_size"])
            for y in x["stars"]:
                print("    ", y["face_to_face_possible"], [t.split(" faces")[0] for t in y["tiles"]])

    # ------------------------------------------------- exact deltahedral realisations of the icosahedral patterns
    r5 = sp.sqrt(5)
    phi = (1 + r5) / 2
    cons = {}
    # pentagonal pyramid J2, edge 1: height h, base-edge dihedral beta, lateral-edge dihedral gamma
    Rp2 = (5 + r5) / 10                       # squared circumradius of the unit pentagon
    rp2 = (5 + 2 * r5) / 20                   # squared inradius of the unit pentagon
    h2 = sp.nsimplify(1 - Rp2)
    cosb = sp.sqrt(rp2 / (rp2 + h2))         # cos(beta): beta = angle between lateral face and base
    beta = sp.acos(cosb)
    # lateral dihedral of J2: icosahedron dihedral (the pyramid is an icosahedron corner)
    gamma = sp.acos(-r5 / 3)
    thetaD = sp.acos(-1 / r5)                 # dodecahedron dihedral
    # icosidodecahedron dihedral (pentagon-triangle)
    thetaID = sp.acos(-sp.sqrt((5 + 2 * r5) / 15))
    cons["J2"] = {"h^2": str(sp.simplify(h2)), "h": float(sp.sqrt(h2)), "beta_deg": float(sp.deg(beta)),
                  "gamma_deg": float(sp.deg(gamma))}
    # icosidodecahedron + outward pyramids is flat: thetaID + beta == pi exactly
    flat = sp.simplify(sp.cos(thetaID + beta) + 1)
    cons["icosidodecahedron + 12 J2 outward: theta_ID + beta - pi"] = str(sp.nsimplify(sp.simplify(
        sp.expand_trig(sp.cos(thetaID + beta)))))
    cons["outward_is_flat (cos(theta_ID+beta) = -1)"] = bool(is_zero(sp.expand_trig(sp.cos(thetaID + beta)) + 1))
    cons["dented icosahedron: edge dihedral theta_ID - beta (deg)"] = float(sp.deg(thetaID - beta))
    cons["dented icosahedron: pyramid lateral edges reflex (deg)"] = float(360 - sp.deg(gamma))
    # distances from centre to faces, edge 1 (to compare with the pyramid height for the cone argument)
    cons["icosidodecahedron: centre-to-pentagon distance"] = float(sp.sqrt((5 + 2 * r5) / 5))
    cons["dodecahedron: inradius"] = float(sp.sqrt((25 + 11 * r5) / 40))
    cons["augmented dodecahedron: edge dihedral theta_D + 2 beta (deg)"] = float(sp.deg(thetaD + 2 * beta))
    cons["dented dodecahedron: edge dihedral theta_D - 2 beta (deg)"] = float(sp.deg(thetaD - 2 * beta))
    cons["theta_D + 2beta != pi"] = not is_zero(sp.expand_trig(sp.cos(thetaD + 2 * beta)) + 1)
    cons["theta_D - 2beta > 0"] = float(thetaD - 2 * beta) > 0
    report["icosahedral_realisations"] = cons
    print(json.dumps(cons, indent=1), flush=True)
    json.dump(report, open("data/attachability.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
