#!/usr/bin/env python3
"""Exact space tilings by convex Scutoid Frusta from power diagrams whose weights change linearly with height.
Power diagram (Laguerre/Voronoi with weights, Aurenhammer 1987): cell(p) = {X : |X-p|^2 - w_p <= |X-q|^2 - w_q for all q}.
If w_p = a_p + b_p z, each inequality is LINEAR in (x, y, z): the cells of the slab 0 <= z <= 1 are convex polyhedra with
planar parallel ends, and every vertical change of neighbours is a Y-corner. Sites: centred rectangular set
{(i + (r mod 2)/2, r)}; even rows carry weight d(z), odd rows 0. Everything in Fractions; types checked with sf_enum's
exact routines."""
import sys, json, os
sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import sf_enum as S

def cell(site, d0, d1, R=4):
    """planes of the cell of `site`; even-row weight d(z) = d0 + (d1 - d0) z, odd rows 0."""
    def w(p):  # (a, b) with w = a + b z
        return (d0, d1 - d0) if p[1] % 2 == 0 else (Fr(0), Fr(0))
    px, py = site; ap, bp = w(site)
    planes = [(Fr(0), Fr(0), Fr(-1), Fr(0)), (Fr(0), Fr(0), Fr(1), Fr(1))]
    for r in range(py - R, py + R + 1):
        for i in range(-R - 1, R + 2):
            q = (Fr(i) + Fr(r % 2, 2), r)
            if q == (px, py):
                continue
            aq, bq = w(q)
            # 2 X.(q-p) + (b_q - b_p) z <= |q|^2 - |p|^2 - a_q + a_p
            planes.append((2 * (q[0] - px), Fr(2 * (q[1] - py)), bq - bp,
                           q[0] ** 2 + Fr(q[1]) ** 2 - px ** 2 - Fr(py) ** 2 - aq + ap))
    v = S.polytope(planes)
    keep = [i for i in range(len(planes)) if i < 2 or sum(1 for t in v.values() if i in t) >= 3]
    planes = [planes[i] for i in keep]
    v = S.polytope(planes)
    mp, why = S.build_map(planes, v)
    if mp is None:
        return None, why, planes, v
    return S.analyse(planes, mp), None, planes, v

out = {}
for name, d0, d1 in (("pair", Fr(0), Fr(-1)), ("single", Fr(1), Fr(-1))):
    res = {}
    for lab, site in (("even", (Fr(0), 0)), ("odd", (Fr(1, 2), 1))):
        an, why, planes, v = cell(site, d0, d1)
        if an is None:
            print(name, lab, "FAILED", why); continue
        res[lab] = dict(bottom=an["m"], top=an["n"], Y=an["k"], lateral_faces=an["lateral_faces"],
                        every_lateral_meets_end=an["every_lateral_meets_end"], code=an["code"],
                        verts=sorted([[str(c) for c in x] for x in v]))
        print(name, lab, "bottom", an["m"], "top", an["n"], "Y", an["k"], "lateral", an["lateral_faces"], "meets end", an["every_lateral_meets_end"])
    # congruence for the single-kind slab: glide g(x,y,z) = (x + 1/2, y + 1, 1 - z) maps the even cell onto the odd cell
    if name == "single" and "even" in res and "odd" in res:
        ev = {tuple(Fr(c) for c in x) for x in res["even"]["verts"]}; od = {tuple(Fr(c) for c in x) for x in res["odd"]["verts"]}
        img = {(x + Fr(1, 2), y + 1, 1 - z) for x, y, z in ev}
        mir = {(-x, y, z) for x, y, z in ev}
        print("single: glide maps even cell onto odd cell exactly:", img == od, "; even cell mirror-symmetric (x -> -x):", mir == ev)
        res["glide_even_to_odd"] = img == od; res["even_mirror_symmetric"] = mir == ev
    if name == "pair" and "even" in res:
        for lab in ("even", "odd"):
            V = {tuple(Fr(c) for c in x) for x in res[lab]["verts"]}
            c = (Fr(0), 0) if lab == "even" else (Fr(1, 2), 1)
            res[lab]["mirror_symmetric_x"] = {(2 * c[0] - x, y, z) for x, y, z in V} == V
            print("pair", lab, "mirror-symmetric in the vertical plane through its site:", res[lab]["mirror_symmetric_x"])
    out[name] = dict(d0=str(d0), d1=str(d1), cells=res)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/tilings.json"), "w"), indent=0, default=str)
P, Sg = out["pair"]["cells"], out["single"]["cells"]
good = (all(lab in P and lab in Sg for lab in ("even", "odd")) and Sg.get("glide_even_to_odd") is True and Sg.get("even_mirror_symmetric") is True
        and (P["even"]["bottom"], P["even"]["top"], P["even"]["Y"]) == (6, 4, 2) and (P["odd"]["bottom"], P["odd"]["top"], P["odd"]["Y"]) == (6, 8, 2)
        and P["even"]["every_lateral_meets_end"] and P["odd"]["every_lateral_meets_end"] and Sg["even"]["every_lateral_meets_end"])
print("FINAL ok" if good else "FINAL FAIL (a tiling cell is missing or not as expected)")
sys.exit(0 if good else 1)
