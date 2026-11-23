#!/usr/bin/env python3
"""V + SF on the three permutahedra (24 Nov 2026), exact.

For each permutahedron P (uniform truncated octahedron, truncated cuboctahedron, truncated icosidodecahedron; exact in Q, Q(sqrt2),
Q(sqrt5)) and each of two plate systems through its centre O:
  (a) its Vacuus (edge plates, #110): one plane through O and each edge, merged when equal;
  (b) its face-parallel planes (a separate construction): one plane through O parallel to each pair of opposite faces;
cut P by all the planes. Every plane passes through O, so each piece is the cone from O over one patch of P's surface:
the pieces correspond one to one with the patches into which the planes cut the surface. Method: each face polygon is clipped
by every plane exactly (2D, exact intersection points); each sub-polygon gets its sign vector (side of every plane, read at its
centroid, exactly); sub-polygons with the same sign vector form one patch (one per face at most). Checks: the sub-polygon areas of
every face add up to the face area exactly; the cone volumes add up to vol(P) exactly; every patch is connected.
For each piece we record: the faces of P it covers, its patch corners (true corners: collinear points merged exactly), the number of
lateral faces (plates on its boundary), and whether the patch contains a corner of P inside or on its boundary.
The shell variant: the region between P and lambda*P (0 < lambda < 1) cut by the same planes; each piece is the cone piece minus
its homothetic copy, ends = the patch and lambda * patch.
Usage: python cut.py [A3|B3|H3 ...] -> data/cut-<type>.json
"""
import sys, os, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../2026-11-24-vacuus-enumeration/scripts"))
from vacuus_exact import analyse, dot, cross, vsub, vadd, scal, vneg, vkey, fl, canon
from perm_checks import refl_matrix, closure, apply
from assoc import setup
OUT = os.path.join(HERE, "../data")
def pr(*a): print(*a, flush=True)

def clip_split(F, poly, m):
    """split a convex polygon (list of exact points) by the plane m.x = 0; returns (neg, pos) lists or None if not split"""
    s = [F.sign(dot(m, p)) for p in poly]
    if all(x >= 0 for x in s) or all(x <= 0 for x in s): return None
    neg, pos = [], []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]; sp_, sq = s[i], s[(i + 1) % n]
        if sp_ <= 0: neg.append(p)
        if sp_ >= 0: pos.append(p)
        if sp_ * sq < 0:
            dp, dq = dot(m, p), dot(m, q)
            x = tuple((dq * a - dp * b) / (dq - dp) for a, b in zip(p, q))
            neg.append(x); pos.append(x)
    return neg, pos

def area_vec(F, poly):
    a = (F.zero, F.zero, F.zero)
    for i in range(1, len(poly) - 1):
        a = vadd(a, cross(vsub(poly[i], poly[0]), vsub(poly[i + 1], poly[0])))
    return a

def run(typ, lam_note=True):
    t0 = time.time()
    F, mir, a, name = setup(typ)
    mir = [m if F.sign(dot(m, a)) > 0 else vneg(m) for m in mir]
    W = closure(F, [refl_matrix(m) for m in mir])
    V = [apply(A, a) for A in W]
    res, faces = analyse(name, F, V, uniform=True)
    edges = set()
    for f in faces:
        p = f["verts"]
        for j in range(len(p)): edges.add(tuple(sorted((p[j], p[(j + 1) % len(p)]))))
    systems = {}
    ep = {}
    for a_, b_ in edges:
        m = canon(F, cross(V[a_], V[b_])); ep.setdefault(vkey(F, m), m)
    fp = {}
    for f in faces:
        m = canon(F, f["N"]); fp.setdefault(vkey(F, m), m)
    systems["edge plates (Vacuus)"] = list(ep.values())
    systems["face-parallel planes"] = list(fp.values())
    mirset = {vkey(F, canon(F, m)) for m in mir}
    out = {"type": typ, "solid": name, "V": len(V), "E": len(edges), "F": len(faces), "systems": {}}
    # exact volume of P
    volP = F.zero
    for f in faces:
        volP = volP + f["d"] * area_len(F, [V[i] for i in f["verts"]], f["N"])
    for sname, planes in systems.items():
        pieces = {}   # sign vector -> list of (face index, polygon)
        for fi, f in enumerate(faces):
            polys = [[V[i] for i in f["verts"]]]
            for m in planes:
                nxt = []
                for poly in polys:
                    sp2 = clip_split(F, poly, m)
                    if sp2 is None: nxt.append(poly)
                    else: nxt += [q for q in sp2 if len(q) >= 3]
                polys = nxt
            # area check
            A0 = area_vec(F, [V[i] for i in f["verts"]])
            As = (F.zero, F.zero, F.zero)
            for q in polys: As = vadd(As, area_vec(F, q))
            assert vkey(F, As) == vkey(F, A0), "face areas add up"
            for q in polys:
                c = tuple(sum((p[i] for p in q), F.zero) / F.c(len(q)) for i in range(3))
                sv = tuple(F.sign(dot(m, c)) for m in planes)
                assert 0 not in sv
                pieces.setdefault(sv, []).append((fi, q))
        # volume check: sum of cones = vol P
        vol = F.zero
        for sv, L in pieces.items():
            for fi, q in L:
                vol = vol + faces[fi]["d"] * area_len(F, q, faces[fi]["N"])
        assert vkey(F, [vol]) == vkey(F, [volP]), "cone volumes add up to vol P"
        rows = []
        vk = {vkey(F, v): i for i, v in enumerate(V)}
        for sv, L in pieces.items():
            assert len({fi for fi, q in L}) == len(L), "one sub-polygon per face per piece"
            # boundary of the patch: segments used once
            segs = {}
            for fi, q in L:
                for i in range(len(q)):
                    p1, p2 = q[i], q[(i + 1) % len(q)]
                    k = frozenset((vkey(F, p1), vkey(F, p2)))
                    segs.setdefault(k, []).append((p1, p2))
            # sub-polygon vertices may have T-junctions on shared segments: resolve by splitting segments at points of other segments
            pts = {}
            for fi, q in L:
                for p in q: pts[vkey(F, p)] = p
            def split_seg(p1, p2):
                inner = []
                d = vsub(p2, p1)
                for k, p in pts.items():
                    if k in (vkey(F, p1), vkey(F, p2)): continue
                    e = vsub(p, p1)
                    if any(cross(d, e)): continue
                    t = dot(e, d) / dot(d, d)
                    if F.sign(t) > 0 and F.sign(t - 1) < 0: inner.append((t, p))
                inner.sort(key=lambda x: float(F.val(x[0])))
                chain = [p1] + [p for _, p in inner] + [p2]
                return list(zip(chain[:-1], chain[1:]))
            cnt = {}
            for fi, q in L:
                for i in range(len(q)):
                    for s1, s2 in split_seg(q[i], q[(i + 1) % len(q)]):
                        k = frozenset((vkey(F, s1), vkey(F, s2)))
                        cnt.setdefault(k, [0, s1, s2]); cnt[k][0] += 1
            bnd = [(v[1], v[2]) for v in cnt.values() if v[0] == 1]
            # walk the boundary cycle
            adj = {}
            for s1, s2 in bnd:
                adj.setdefault(vkey(F, s1), []).append(s2); adj.setdefault(vkey(F, s2), []).append(s1)
            assert all(len(x) == 2 for x in adj.values()), "boundary is a simple cycle"
            start = bnd[0][0]; cyc = [start]; prev = None; cur = start
            while True:
                nb = [p for p in adj[vkey(F, cur)] if prev is None or vkey(F, p) != vkey(F, prev)]
                nx = nb[0]
                if vkey(F, nx) == vkey(F, start): break
                cyc.append(nx); prev, cur = cur, nx
            assert len(cyc) == len(adj), "patch connected, one boundary cycle"
            n = len(cyc)
            corners = [cyc[i] for i in range(n) if any(cross(vsub(cyc[i], cyc[i - 1]), vsub(cyc[(i + 1) % n], cyc[i])))]
            # lateral faces: maximal runs of boundary segments on one plate (each boundary segment lies on a plate through O)
            def plate_of(p, q):
                return vkey(F, canon(F, cross(p, q)))
            sp_ = [plate_of(cyc[i], cyc[(i + 1) % n]) for i in range(n)]
            lat = sum(1 for i in range(n) if sp_[i] != sp_[i - 1]) or 1
            on_plates = {k for k in sp_}
            # corners of P on the patch
            inner_corner = 0; bcorner = 0
            ckeys = {vkey(F, p) for p in cyc}
            fset = {fi for fi, q in L}
            for k in vk:
                if k in pts:
                    if k in ckeys: bcorner += 1
                    else: inner_corner += 1
            rows.append({"faces_covered": len(L), "face_sides": sorted(len(faces[fi]["verts"]) for fi in fset),
                         "patch_corners": len(corners), "lateral_faces": lat,
                         "lateral_on_coxeter_mirror": sum(1 for k in on_plates if k in mirset),
                         "corner_of_P_inside": inner_corner, "corners_of_P_on_boundary": bcorner})
        # classify
        summ = {}
        for r in rows:
            if r["faces_covered"] == 1:
                cls = f"pyramid from O over a {r['patch_corners']}-gon (in a {r['face_sides'][0]}-gon face)"
            else:
                cls = f"cone from O over a bent patch: {r['faces_covered']} faces {r['face_sides']}, {r['patch_corners']} corners, {r['lateral_faces']} lateral faces" + (", holds a corner of P" if r["corner_of_P_inside"] else "")
            summ[cls] = summ.get(cls, 0) + 1
        summ = dict(sorted(summ.items(), key=lambda kv: -kv[1]))
        nsingle = sum(1 for r in rows if r["faces_covered"] == 1)
        pr(f"{typ} {name} | {sname}: {len(planes)} planes, {len(rows)} pieces ({nsingle} over one face, {len(rows) - nsingle} over bent patches); cone volumes add to vol P exactly")
        for k, v in summ.items(): pr(f"   {v:5d}  {k}")
        out["systems"][sname] = {"planes": len(planes), "planes_on_coxeter_mirrors": sum(1 for m in planes if vkey(F, canon(F, m)) in mirset),
                                 "pieces": len(rows), "over_one_face": nsingle, "classes": summ,
                                 "shell_frusta_convex": nsingle, "shell_frusta_bent_ends": len(rows) - nsingle}
    out["secs"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(OUT, f"cut-{typ}.json"), "w"), indent=1)
    return out

def area_len(F, poly, N):
    """(area vector . N) / |N|^2 * ... : returns the exact cone-volume factor area(poly) . N / (3 |N|^2) scaled so that d * this = volume.
    For a face plane N.x = d, the cone from O over poly has volume (1/3) * area * (d/|N|) = d * (A.N) / (6 |N|^2) with A = area vector (2*area*unit normal)."""
    A = area_vec(F, poly)
    return dot(A, N) / (F.c(6) * dot(N, N))

if __name__ == "__main__":
    todo = sys.argv[1:] or ["A3", "B3", "H3"]; done = 0
    for typ in todo:
        run(typ); done += 1
    print("FINAL ok" if done == len(todo) else "FINAL FAIL")
