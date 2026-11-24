#!/usr/bin/env python3
"""Planes at right angles to whole classes of rotation axes (octahedral and icosahedral groups), exact.

For the octahedral group (frame of the cube in vacuus_exact) the classes are the 3 four-fold axes, the 4 three-fold
axes and the 6 two-fold axes; for the icosahedral group (frame of the icosahedron) the 6 five-fold, 10 three-fold and
15 two-fold axes. For each of the 7 nonempty unions of classes (per group) the central arrangement of the planes at
right angles to those axes is computed exactly (catalogue.arrangement: counts plus face tracing). Then every
Platonic, Archimedean and Catalan solid of data/catalogue-all.json is matched exactly (same field, same frame):
its Resonus and its Vacuus are compared with each union.
"""
import os, sys, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import catalogue as C
from vacuus_exact import vkey, canon, vsub, vadd, scal, dot, cross
VX = C.VX

def lines(F, vecs):
    out = {}
    for v in vecs:
        if any(v): out.setdefault(vkey(F, canon(F, v)), canon(F, v))
    return out

def classes(F, V, faces):
    """rotation-axis classes of a Platonic solid: through corners, through face centres, through edge midpoints"""
    edges = {(min(f["verts"][j], f["verts"][(j + 1) % len(f["verts"])]), max(f["verts"][j], f["verts"][(j + 1) % len(f["verts"])]))
             for f in faces for j in range(len(f["verts"]))}
    cor = lines(F, V)
    fc = lines(F, [tuple(sum((V[i][t] for i in f["verts"]), F.zero) for t in range(3)) for f in faces])
    em = lines(F, [vadd(V[a], V[b]) for a, b in edges])
    return cor, fc, em

if __name__ == "__main__":
    S = VX.uniform_solids()
    res = {}
    groups = {}
    F, gen, _ = S["cube"]; V = VX.build_set(F, gen); r, faces = VX.analyse("cube", F, V, True)
    cor, fc, em = classes(F, V, faces)
    groups["Oh"] = (F, {"4-fold": fc, "3-fold": cor, "2-fold": em})
    F, gen, _ = S["icosahedron"]; V = VX.build_set(F, gen); r, faces = VX.analyse("icosahedron", F, V, True)
    cor, fc, em = classes(F, V, faces)
    groups["Ih"] = (F, {"5-fold": cor, "3-fold": fc, "2-fold": em})
    # the other icosahedral solids of vacuus_exact use the other golden orientation: the dodecahedron's frame
    F, gen, _ = S["dodecahedron"]; V = VX.build_set(F, gen); r, faces = VX.analyse("dodecahedron", F, V, True)
    cor, fc, em = classes(F, V, faces)
    groups["Ih'"] = (F, {"5-fold": fc, "3-fold": cor, "2-fold": em})
    unions = {}
    for g, (F, cl) in groups.items():
        assert sorted(len(x) for x in cl.values()) == ([3, 4, 6] if g == "Oh" else [6, 10, 15])
        names = list(cl)
        for k in range(1, 4):
            for sub in itertools.combinations(names, k):
                planes = {}
                for nm in sub: planes.update(cl[nm])
                arr = C.arrangement(F, list(planes.values()))
                unions[(g, sub)] = set(map(str, planes))
                res[f"{g}: " + " + ".join(sub)] = {"planes": len(planes), **{k2: v for k2, v in arr.items() if k2 != "planes"}}
                if g == "Ih'":
                    a0 = res["Ih: " + " + ".join(sub)]
                    assert (a0["regions"], a0["simplicial"], a0["region_sides"]) == (arr["regions"], arr["simplicial"], arr["region_sides"])
                print(g, sub, len(planes), "regions", arr["regions"], "simplicial", arr["simplicial"], arr.get("region_sides"), flush=True)
    rows = json.load(open(os.path.join(HERE, "../data/catalogue-all.json")))
    match = {}
    for r in rows:
        if r["family"] not in ("Platonic", "Archimedean", "Catalan"): continue
        gs = ("Ih", "Ih'") if r["group"] in ("Ih", "I") else ("Oh",)
        mm = {}
        for what in ("res", "vac"):
            ks = set(r["_keys"][what])
            hit = [" + ".join(sub) for (gg, sub), u in unions.items() if gg in gs and u == ks]
            mm["resonus" if what == "res" else "vacuus"] = hit[0] if hit else None
        match[r["name"]] = mm
        print(r["name"], mm, flush=True)
    json.dump({"unions": res, "solids": match}, open(os.path.join(HERE, "../data/axis-classes.json"), "w"), indent=1)
    print("FINAL ok axis classes", len(res), "unions;", len(match), "solids matched or not", flush=True)
