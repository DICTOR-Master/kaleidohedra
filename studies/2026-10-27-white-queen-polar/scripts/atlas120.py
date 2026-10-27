"""Red Queen 120-cell, stage 3: the exact atlas of its slices and shadows in its four main directions, as #63 did for
the 600-cell. Exact in Q(√5) (q5.Q5, Fractions); floats only propose hull facets, which are verified exactly.

The 120-cell is built from the #63 source model by polarity (as red_queen.py): corners = the 600 cell centres of the
600-cell; edges = pairs of cells sharing a triangle; pentagons = the 5 cells round each 600-cell edge; dodecahedral cells
= the 20 cells round each 600-cell vertex.
Directions d (not unit vectors; heights compare within one direction only): a corner, an edge midpoint, a pentagon
centre, a cell centre of the 120-cell (= the 600-cell's cell-, face-, edge- and vertex-first directions, checked).

1. Slices, centre to tip: at every corner height and inside every gap between neighbouring heights. One-pattern-per-gap
   lemma checked exactly: in every gap the cuts at 1/4, 1/2 and 3/4 of the gap have the same faces, each face given as
   the set of 120-cell edges whose crossing points are its corners; and each face is the cross-section of ONE
   dodecahedral cell (its edges all lie in one cell), one face per cell cut.
2. Shadows: exact hull of the 600 projected corners; front/back/side-on cells by the sign of (cell centre)·d; exact
   volume check that the front cells, and the back cells, each tile the shadow once.
3. Polar checks: the shadow of the 120-cell in direction d is the polar of the central slice of the 600-cell in the same
   direction (V <-> F swapped), and the central slice of the 120-cell is the polar of the 600-cell's shadow.
Faces of every slice and shadow are named exactly (regular, equilateral, equiangular; triangle and quadrilateral kinds;
centrally symmetric even polygons).
usage (dicto-big-brother):  cd scripts && nice ~/geom/bin/python atlas120.py [nproc]
"""
import json
import os
import pickle
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from itertools import combinations
from multiprocessing import Pool

for p in (os.path.expanduser("~/kres-tmp/4d/scripts"), os.path.expanduser("~/k-research/studies/2026-10-27-4d-shadows/scripts")):
    if os.path.isdir(p):
        sys.path.insert(0, p); break
from q5 import Q5, ZERO, dot, sub, add, scal, cross, exact_hull3, q5str  # noqa: E402
from shadows import Space, describe  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
LOG = []


def find_data(name, study):
    for p in (os.path.join(DATA, name), os.path.expanduser("~/kres-tmp/4d/data/" + name),
              os.path.join(HERE, "../..", study, "data", name)):
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)


def check(name, ok):
    LOG.append({"check": name, "pass": bool(ok)})
    print(("PASS " if ok else "FAIL ") + name, flush=True)


# ------------------------------------------------------------------ the 120-cell, exact
S = json.load(open(find_data("600cell-source.json", "2026-10-27-white-queen-600")))
W = [tuple(Q5(Fr(c[0]), Fr(c[1])) for c in v) for v in S["vertices_exact"]]       # 600-cell vertices
Wcells, Wtris, Wedges = S["cells"], S["triangles"], S["edges"]
R = [scal(Q5(Fr(1, 4)), tuple(sum((W[i][k] for i in c), ZERO) for k in range(4))) for c in Wcells]
cells_of_w = defaultdict(list)
for ci, c in enumerate(Wcells):
    for i in c:
        cells_of_w[i].append(ci)
cell_by_tri = defaultdict(list)
for ci, c in enumerate(Wcells):
    for t in combinations(sorted(c), 3):
        cell_by_tri[t].append(ci)
E = [tuple(sorted(cell_by_tri[tuple(sorted(t))])) for t in Wtris]                    # 1200 edges
adj = defaultdict(set)
for a, b in E:
    adj[a].add(b); adj[b].add(a)
PENT = []                                                                            # 720 pentagons, cyclic order
for a, b in Wedges:
    ring = [ci for ci in cells_of_w[a] if b in Wcells[ci]]
    cyc = [ring[0]]
    while len(cyc) < 5:
        cyc.append(next(x for x in ring if x in adj[cyc[-1]] and x not in cyc))
    PENT.append(cyc)
CELLS = [sorted(cells_of_w[i]) for i in range(120)]                                  # 120 dodecahedra
CELL_PENTS = [[p for p, (a, b) in zip(PENT, Wedges) if i in (a, b)] for i in range(120)]
eidx = {e: k for k, e in enumerate(E)}
CELL_EDGES = [{eidx[e] for e in E if e[0] in set(c) and e[1] in set(c)} for c in CELLS]


def out_edge2():
    return q5str(dot(sub(R[E[0][0]], R[E[0][1]]), sub(R[E[0][0]], R[E[0][1]])))


def centroid(idx):
    return scal(Q5(Fr(1, len(idx))), tuple(sum((R[i][k] for i in idx), ZERO) for k in range(4)))


def parallel(u, w):
    return all((u[i] * w[j] - u[j] * w[i]).iszero() for i, j in combinations(range(4), 2))


e0 = next(e for e in E if 0 in e)
p0 = next(p for p in PENT if set(e0) <= set(p))
c0 = next(i for i, c in enumerate(CELLS) if set(p0) <= set(c))
DIRS = {"vertex-first": (R[0], (0,)), "edge-first": (centroid(e0), e0), "face-first": (centroid(p0), tuple(p0)),
        "cell-first": (centroid(CELLS[c0]), tuple(CELLS[c0]))}
LAB = {"vertex-first": "a corner", "edge-first": "an edge midpoint", "face-first": "a pentagon centre",
       "cell-first": "a cell centre"}


def model_checks():
    check("600 corners, 1200 edges, 720 pentagons, 120 cells", len(R) == 600 and len(set(R)) == 600 and len(E) == 1200
          and len(set(E)) == 1200 and len(PENT) == 720 and len(CELLS) == 120)
    check("corners on one sphere, all edges one length, 4 edges at every corner",
          len({dot(p, p) for p in R}) == 1 and len({dot(sub(R[a], R[b]), sub(R[a], R[b])) for a, b in E}) == 1
          and all(len(adj[i]) == 4 for i in range(600)))
    check("every cell: 20 corners, 30 edges, 12 pentagons (each pentagon a 5-cycle of edges)",
          all(len(c) == 20 and len(CELL_EDGES[i]) == 30 and len(CELL_PENTS[i]) == 12 for i, c in enumerate(CELLS))
          and all(p[(k + 1) % 5] in adj[p[k]] for p in PENT for k in range(5)))
    # the four directions are the 600-cell's cell-, triangle-, edge- and vertex-first directions
    ok = parallel(DIRS["vertex-first"][0], tuple(sum((W[i][k] for i in Wcells[0]), ZERO) for k in range(4)))
    shared = sorted(set(Wcells[e0[0]]) & set(Wcells[e0[1]]))          # 120-cell edge e0 <-> the triangle its cells share
    ok &= len(shared) == 3 and parallel(DIRS["edge-first"][0], tuple(sum((W[i][k] for i in shared), ZERO) for k in range(4)))
    a, b = Wedges[PENT.index(p0)]                                       # pentagon p0 <-> 600-cell edge (a, b)
    ok &= parallel(DIRS["face-first"][0], add(W[a], W[b]))
    ok &= parallel(DIRS["cell-first"][0], W[c0])                        # cell c0 <-> 600-cell vertex c0
    check("the four directions = the 600-cell's cell-, triangle-, edge- and vertex-first directions (exactly parallel)", ok)


# ------------------------------------------------------------------ exact naming of polygon faces
def poly_kind(P, sp):
    """P: exact 3D frame points of a convex polygon in cyclic order."""
    n = len(P)
    md = lambda u, w: sp.mdot(u, w)
    sides = [md(sub(P[(i + 1) % n], P[i]), sub(P[(i + 1) % n], P[i])) for i in range(n)]
    angs = []
    for i in range(n):
        u, w = sub(P[i - 1], P[i]), sub(P[(i + 1) % n], P[i])
        x = md(u, w)
        angs.append((x.sign(), x * x / (md(u, u) * md(w, w))))
    eqs = len(set(sides)) == 1
    eqa = len(set(angs)) == 1
    par = lambda u, w: all(c.iszero() for c in cross(u, w))
    if n == 3:
        k = "equilateral triangle" if eqs else ("isosceles triangle" if len(set(sides)) == 2 else "scalene triangle")
        if any(s == 0 for s, _ in angs):
            k += " (right-angled)"
        return k
    if n == 4:
        s = sides
        d1 = md(sub(P[2], P[0]), sub(P[2], P[0])); d2 = md(sub(P[3], P[1]), sub(P[3], P[1]))
        pa = par(sub(P[1], P[0]), sub(P[2], P[3])); pb = par(sub(P[2], P[1]), sub(P[3], P[0]))
        if eqs and d1 == d2: return "square"
        if pa and pb and d1 == d2: return "rectangle"
        if eqs: return "rhombus"
        if pa and pb: return "parallelogram"
        if (pa or pb) and d1 == d2: return "isosceles trapezium"
        if pa or pb: return "trapezium"
        if (s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0]): return "kite"
        return "general quadrilateral"
    name = {5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "enneagon", 10: "decagon"}.get(n, f"{n}-gon")
    if eqs and eqa:
        return "regular " + name
    tags = []
    if eqs: tags.append("equilateral")
    if eqa: tags.append("equiangular")
    if n % 2 == 0:
        m = n // 2
        c = add(P[0], P[m])
        if all(add(P[i], P[i + m]) == c for i in range(m)):
            tags.append("centrally symmetric")
    # mirror symmetry: some reflection j -> m - j (mod n) keeps every angle and every side
    mirror = any(all(angs[j] == angs[(m - j) % n] and sides[j] == sides[(m - j - 1) % n] for j in range(n))
                 for m in range(n))
    if mirror: tags.append("mirror-symmetric")
    return (", ".join(tags) + " " if tags else "irregular ") + name


def face_kinds(V, F, sp):
    return dict(sorted(Counter(poly_kind([V[i] for i in f], sp) for f in F).items()))


def vertex_configs(F):
    """cyclic sequence of face sizes round each vertex, canonical under rotation and reflection, e.g. '3.4.5.4'."""
    at = defaultdict(list)
    for fi, f in enumerate(F):
        for v in f:
            at[v].append(fi)
    out = Counter()
    for v, fs in at.items():
        # order the faces round v: consecutive faces share an edge through v
        def nbrs(fi):
            f = F[fi]; k = f.index(v); return {f[k - 1], f[(k + 1) % len(f)]}
        cyc = [fs[0]]
        while len(cyc) < len(fs):
            cyc.append(next(g for g in fs if g not in cyc and nbrs(g) & nbrs(cyc[-1])))
        seq = [len(F[g]) for g in cyc]
        rots = [tuple(seq[i:] + seq[:i]) for i in range(len(seq))]
        rots += [tuple(reversed(r)) for r in rots]
        out[".".join(map(str, min(rots)))] += 1
    return dict(sorted(out.items()))


UNIFORM = {"3.3.3": ("regular tetrahedron", 1), "5.5.5": ("regular dodecahedron", 1), "3.5.3.5": ("icosidodecahedron", 1),
           "3.4.5.4": ("rhombicosidodecahedron", 2), "5.6.6": ("truncated icosahedron", 2),
           "3.10.10": ("truncated dodecahedron", 2), "3.4.4": ("regular triangular prism", 2),
           "4.4.5": ("regular pentagonal prism", 2), "4.6.10": ("truncated icosidodecahedron", 3)}


def uniform_name(o, V, sp):
    """exact: all faces regular, one edge length, one vertex configuration, all corners on one sphere round the
    centroid, and the uniform solid's number of dihedral-angle classes -> its name; else None."""
    reg = sum(v for k, v in o["face_kinds"].items() if k.startswith("regular") or k in ("square", "equilateral triangle"))
    if reg != o["F"] or len(o["edge_len2_exact"]) != 1 or len(o["vertex_configs"]) != 1:
        return None
    c = tuple(sum((p[k] for p in V), ZERO) / Q5(len(V)) for k in range(3))
    if len({sp.mdot(sub(p, c), sub(p, c)) for p in V}) != 1:
        return None
    cfg = next(iter(o["vertex_configs"]))
    if cfg in UNIFORM and len(o["dihedral_cos2_exact"]) == UNIFORM[cfg][1]:
        return UNIFORM[cfg][0]
    return None


# ------------------------------------------------------------------ one slice
def cut(task):
    lab, hv, at_layer, tip = task
    d = DIRS[lab][0]
    sp = Space(4, d, None)
    H = [dot(p, d) for p in R]
    pts, tag = [], []
    for i, (p, x) in enumerate(zip(R, H)):
        if x == hv:
            pts.append(sp.y(p)); tag.append(("v", i))
    crossing = []
    for k, (a, b) in enumerate(E):
        ha, hb = H[a], H[b]
        if ((ha - hv) * (hb - hv)).sign() < 0:
            t = (hv - ha) / (hb - ha)
            pts.append(sp.y(tuple(x + t * (y - x) for x, y in zip(R[a], R[b])))); tag.append(("e", k)); crossing.append(k)
    base = {"direction": lab, "height": q5str(hv), "h": float(hv), "at_vertex_layer": at_layer, "tip_height": q5str(tip)}
    hh = exact_hull3(pts, sp.mf)
    if hh["dim"] < 3:
        return {**base, "dim": hh["dim"], "V": len(pts)}, None, None
    rec, _ = describe(hh, sp)
    lookup = {p: t for p, t in zip(pts, tag)}
    vt = [lookup[p] for p in hh["V"]]
    faces_by_label = frozenset(frozenset(vt[i] for i in f) for f in hh["faces"])
    item = {**base, **rec, "points_in_cut": len(pts), "every_point_a_slice_vertex": len(hh["V"]) == len(pts),
            "face_kinds": face_kinds(hh["V"], hh["faces"], sp), "vertex_configs": vertex_configs(hh["faces"])}
    item["uniform_solid"] = uniform_name(item, hh["V"], sp)
    if not at_layer:
        # each face = cross-section of one dodecahedral cell, one face per cell cut
        cut_cells = [ci for ci in range(120) if any(k in CELL_EDGES[ci] for k in crossing)]
        own = []
        for f in faces_by_label:
            ks = {k for _, k in f}
            own.append([ci for ci in range(120) if ks <= CELL_EDGES[ci]])
        item["faces_one_cell_each"] = all(len(o) == 1 for o in own) and sorted(o[0] for o in own) == sorted(cut_cells)
        item["cells_cut"] = len(cut_cells)
    keep = {"item": item, "fV": hh["fV"].tolist(), "faces": hh["faces"]}
    return item, keep, faces_by_label


def slice_tasks():
    tasks = []
    for lab, (d, _) in DIRS.items():
        hs = sorted(set(dot(p, d) for p in R), key=float)
        tip = hs[-1]
        for h in hs:
            if h.sign() >= 0:
                tasks.append((lab, h, True, tip))
        for a, b in zip(hs, hs[1:]):
            if (a + b).sign() >= 0:
                for fr in (Fr(1, 2), Fr(1, 4), Fr(3, 4)):
                    tasks.append((lab, a + Q5(fr) * (b - a), ("gap", fr, q5str(a), q5str(b)), tip))
    return tasks


def cut_wrapped(task):
    lab, hv, at, tip = task
    if at is True:
        return task, cut((lab, hv, True, tip))
    return task, cut((lab, hv, False, tip))


# ------------------------------------------------------------------ shadows
def det3(a, b, c):
    return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])


def absq(x):
    return x if x.sign() >= 0 else -x


def shadow(lab):
    d = DIRS[lab][0]
    sp = Space(4, d, None)
    Y = [sp.y(p) for p in R]
    h = exact_hull3(Y, sp.mf)
    rec, _ = describe(h, sp)
    rec["face_kinds"] = face_kinds(h["V"], h["faces"], sp)
    rec["vertex_configs"] = vertex_configs(h["faces"])
    hv = ZERO
    O = tuple(sum((y[k] for y in h["V"]), ZERO) / Q5(len(h["V"])) for k in range(3))
    for f in h["faces"]:
        for j in range(1, len(f) - 1):
            a, b, c = [sub(h["V"][t], O) for t in (f[0], f[j], f[j + 1])]
            hv = hv + absq(det3(a, b, c))

    def cell_vol(ci):
        cen = tuple(sum((Y[i][k] for i in CELLS[ci]), ZERO) / Q5(20) for k in range(3))
        v, signs = ZERO, set()
        for p in CELL_PENTS[ci]:
            for j in range(1, 4):
                x = det3(sub(Y[p[0]], cen), sub(Y[p[j]], cen), sub(Y[p[j + 1]], cen))
                v = v + absq(x)
        return v
    cs = [dot(W[i], d) for i in range(120)]        # cell i of the 120-cell has centre direction W[i]
    front = [i for i in range(120) if cs[i].sign() > 0]
    back = [i for i in range(120) if cs[i].sign() < 0]
    side = [i for i in range(120) if cs[i].sign() == 0]
    fv = sum((cell_vol(i) for i in front), ZERO); bv = sum((cell_vol(i) for i in back), ZERO)
    sv = [cell_vol(i) for i in side]

    # each side-on cell is flat; does its image lie in one hull face, and which face sizes?
    planes = []
    for f in h["faces"]:
        a, b, c = h["V"][f[0]], h["V"][f[1]], h["V"][f[2]]
        n = cross(sub(b, a), sub(c, a)); planes.append((n, dot(n, a), len(f)))
    side_faces = Counter()
    for ci in side:
        hit = [k for n, off, k in planes if all(dot(n, Y[i]) == off for i in CELLS[ci])]
        side_faces[str(hit[0]) if len(hit) == 1 else "none"] += 1
    rec["side_on_cells_on_hull_face_of_size"] = dict(side_faces)
    # hull faces that are not the image of a side-on cell: how many sides
    rec["hull_faces_not_side_on"] = dict(Counter(str(k) for (n, off, k) in planes
                                                 if not any(all(dot(n, Y[i]) == off for i in CELLS[ci]) for ci in side)))

    def key(ci):
        return tuple(sorted((sp.mdot(sub(Y[a], Y[b]), sub(Y[a], Y[b])) for a, b in combinations(CELLS[ci], 2)),
                            key=lambda q: (float(q), q.a, q.b)))
    kinds = Counter(key(i) for i in front)
    # how many hull vertices are images of corners, and how many corners land inside
    rec.update({"direction": lab, "front": len(front), "back": len(back), "side_on": len(side),
                "front_tiles_exactly": fv == hv, "back_tiles_exactly": bv == hv,
                "side_on_flat": all(x.iszero() for x in sv), "front_kinds": len(kinds),
                "front_kind_counts": sorted(kinds.values()), "hull_volume_detsum": q5str(hv)})
    keep = {"item": rec, "fV": h["fV"].tolist(), "faces": h["faces"]}
    return rec, keep


def shadow_wrapped(lab):
    return lab, shadow(lab)


# ------------------------------------------------------------------ main
if __name__ == "__main__":
    t0 = time.time()
    model_checks()
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    tasks = slice_tasks()
    print("slice cuts to compute:", len(tasks), flush=True)
    tasks.sort(key=lambda t: abs(float(t[1])))          # big central slices first
    with Pool(nproc) as pool:
        sh = pool.map_async(shadow_wrapped, list(DIRS))
        res = pool.map(cut_wrapped, tasks, chunksize=1)
        shres = dict(sh.get())
    print("computed in", round(time.time() - t0), "s", flush=True)

    atlas, keep, gapsig = [], [], defaultdict(dict)
    for (lab, hv, at, tip), (item, kp, sig) in res:
        if at is True:
            atlas.append(item)
            if kp: keep.append(kp)
        else:
            _, fr, a, b = at
            gapsig[(lab, a, b)][fr] = (item, kp, sig)
    lemma_ok, one_cell_ok, pts_ok = True, True, True
    for (lab, a, b), g in gapsig.items():
        item, kp, sig = g[Fr(1, 2)]
        same = sig == g[Fr(1, 4)][2] == g[Fr(3, 4)][2] and sig is not None
        same_counts = all(g[f][0].get("face_sizes") == item.get("face_sizes") for f in g)
        lemma_ok &= bool(same and same_counts)
        one_cell_ok &= bool(item.get("faces_one_cell_each", False))
        item = {**item, "gap": [a, b], "pattern_same_at_quarter_half_three_quarter": bool(same)}
        atlas.append(item)
        if kp:
            kp["item"] = item; keep.append(kp)
    for o in atlas:
        if "dim" not in o:
            pts_ok &= o["every_point_a_slice_vertex"]
    order = list(DIRS)
    atlas.sort(key=lambda o: (order.index(o["direction"]), o["h"]))
    check("one pattern per gap: in every gap the cuts at 1/4, 1/2, 3/4 have identical faces (as sets of crossed edges)",
          lemma_ok)
    check("inside every gap each slice face is the cross-section of exactly one dodecahedral cell, one face per cell cut",
          one_cell_ok)
    check("every corner in the cut and every edge crossing is a vertex of its slice", pts_ok)
    allf = Counter()
    for o in atlas:
        for k, v in o.get("face_sizes", {}).items():
            allf[int(k)] += v
    check("slice faces have 3 to 10 sides (cross-sections of dodecahedra)", min(allf) >= 3 and max(allf) <= 10)

    # central symmetry of the 120-cell (far half mirrors near half)
    check("the 120-cell is centrally symmetric (-p is a corner for every corner p)", set(tuple(-x for x in p) for p in R) == set(R))

    # polar checks against #63
    A6 = json.load(open(find_data("atlas600.json", "2026-10-27-white-queen-600")))
    swap = {"vertex-first": "cell-first", "edge-first": "face-first", "face-first": "edge-first", "cell-first": "vertex-first"}
    ok = True
    for lab in DIRS:
        cs6 = next(o for o in A6 if o["direction"] == swap[lab] and o["h"] == 0)
        s = shres[lab][0]
        ok &= s["V"] == cs6["F"] and s["F"] == cs6["V"] and s["E"] == cs6["E"]
    check("each 120-cell shadow is polar to the 600-cell's central slice in the same direction (V, E, F swap with F, E, V)", ok)
    SH6 = json.load(open(find_data("shadows.json", "2026-10-27-4d-shadows")))
    ok = True
    for lab in DIRS:
        s6 = next(o for o in SH6 if o.get("polytope") == "600-cell" and o["direction"] == swap[lab] and o.get("kind") == "shadow")
        c = next(o for o in atlas if o["direction"] == lab and o["h"] == 0)
        ok &= c["V"] == s6["F"] and c["F"] == s6["V"] and c["E"] == s6["E"]
    check("each 120-cell central slice is polar to the 600-cell's shadow in the same direction", ok)
    ok = all(shres[l][0]["front_tiles_exactly"] and shres[l][0]["back_tiles_exactly"] and shres[l][0]["side_on_flat"]
             for l in DIRS)
    check("every shadow: front cells tile it exactly once and back cells tile it exactly once (exact volume), side-on cells flat",
          ok)
    ok = all(shres[l][0]["front"] == shres[l][0]["back"] for l in DIRS)
    check("front and back cell counts equal in every direction", ok)
    ok = all(shres[l][0]["side_on_cells_on_hull_face_of_size"].get("none", 0) == 0 for l in DIRS)
    check("every side-on cell flattens onto one face of its shadow's hull", ok)
    # uniform solids among the slices
    named = [(o["direction"], o["height"], o["uniform_solid"]) for o in atlas if o.get("uniform_solid")]
    for x in named:
        print("  uniform slice:", x)
    exp = {("cell-first", "rhombicosidodecahedron"), ("cell-first", "truncated icosahedron"), ("cell-first", "icosidodecahedron"),
           ("cell-first", "truncated dodecahedron"), ("cell-first", "regular dodecahedron"), ("vertex-first", "regular tetrahedron"),
           ("edge-first", "regular triangular prism"), ("face-first", "regular pentagonal prism")}
    check("the uniform-solid slices (all faces regular, one edge, one vertex type, inscribed, uniform dihedral count) are "
          "exactly: cell-first rhombicosidodecahedron, truncated icosahedron, icosidodecahedron, truncated dodecahedron, "
          "regular dodecahedra; vertex-first regular tetrahedra; edge-first triangular prism; face-first pentagonal prism",
          {(a, c) for a, b, c in named} == exp)
    allpent = [o for o in atlas if o.get("face_sizes") and set(o["face_sizes"]) == {"5"}]
    tipd = sorted(allpent, key=lambda o: o["h"])
    phi2 = Q5(Fr(3, 2), Fr(1, 2))                              # φ² = (3+√5)/2
    e_tip = Q5(Fr(1, 4))
    check("the all-pentagon slices are exactly the 3 cell-first slices from height 5/4 + 9/16√5 to the tip, all regular "
          "dodecahedra: the tip one is the cell (edge² 1/4), the one at 5/4 + 9/16√5 has edge φ times the cell's",
          len(allpent) == 3 and all(o["direction"] == "cell-first" and o["uniform_solid"] == "regular dodecahedron" for o in allpent)
          and tipd[-1]["edge_len2_exact"][0] == out_edge2() == q5str(e_tip) and tipd[0]["height"] == "5/4 + 9/16√5"
          and tipd[0]["edge_len2_exact"][0] == q5str(e_tip * phi2))
    # inside a gap, is the uniform form only at the middle?
    qn = sorted({(lab, g[f][0].get("uniform_solid")) for (lab, x, y), g in gapsig.items() for f in (Fr(1, 4), Fr(3, 4))
                 if g[f][0].get("uniform_solid")})
    print("  uniform at 1/4 or 3/4 of a gap:", qn)
    check("in the gaps the truncated icosahedron and truncated dodecahedron are uniform only at mid-gap (two edge lengths at "
          "1/4 and 3/4); only the gaps below the cell-first tip (regular dodecahedron) and the vertex-first tip (regular "
          "tetrahedron) keep a uniform form throughout",
          qn == [("cell-first", "regular dodecahedron"), ("vertex-first", "regular tetrahedron")])
    # distinct combinatorial types (V, E, F, face sizes, vertex configurations) per direction
    distinct = {}
    for lab in DIRS:
        sig = {(o.get("V"), o.get("E"), o.get("F"), json.dumps(o.get("face_sizes")), json.dumps(o.get("vertex_configs")), o.get("dim"))
               for o in atlas if o["direction"] == lab}
        distinct[lab] = len(sig)

    out = {"name": "120-cell (Red Queen)", "scale": "corners = centres of the 600-cell's cells (#63 source, radius 2)",
           "corner_radius2": q5str(dot(R[0], R[0])), "edge2": q5str(dot(sub(R[E[0][0]], R[E[0][1]]), sub(R[E[0][0]], R[E[0][1]]))),
           "directions": {l: {"through": LAB[l], "d_exact": [q5str(x) for x in DIRS[l][0]], "element": list(DIRS[l][1])} for l in DIRS},
           "slices": atlas, "shadows": {l: shres[l][0] for l in DIRS}, "checks": LOG}
    summ = {}
    for lab in DIRS:
        it = [o for o in atlas if o["direction"] == lab]
        hs = [o for o in it if o["at_vertex_layer"]]
        fsz = sorted({int(k) for o in it for k in o.get("face_sizes", {})})
        big = max((o for o in it if "V" in o and "dim" not in o), key=lambda o: o["V"])
        summ[lab] = {"corner_heights": len(hs), "gaps": len(it) - len(hs), "slice_patterns": len(it),
                     "face_sizes": fsz, "largest": {"height": big["height"], "V": big["V"], "F": big["F"]}}
    for lab in DIRS:
        summ[lab]["distinct_combinatorial_types"] = distinct[lab]
        it = [o for o in atlas if o["direction"] == lab and "dim" not in o]
        m = max(o["V"] for o in it)
        summ[lab]["largest_all"] = [{"height": o["height"], "gap": not o["at_vertex_layer"], "V": o["V"], "F": o["F"]}
                                    for o in it if o["V"] == m]
    out["summary"] = summ
    out["uniform_slices"] = [{"direction": a, "height": b, "solid": c} for a, b, c in named]
    json.dump(out, open(os.path.join(DATA, "atlas120.json"), "w"), indent=1, ensure_ascii=False)
    pickle.dump({"slices": keep, "shadows": {l: shres[l][1] for l in DIRS}}, open(os.path.join(DATA, "atlas120.pkl"), "wb"))
    print(json.dumps(summ, indent=1, ensure_ascii=False))
    print(sum(c["pass"] for c in LOG), "of", len(LOG), "checks passed; total", round(time.time() - t0), "s")
