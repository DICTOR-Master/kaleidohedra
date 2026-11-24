"""Resonus (one plane through O parallel to each face) of the A3, B3, H3 permutahedra, exact in Q(sqrt5).
Also checks the polar link (task 1) exactly on the same solids: every face-parallel plane is at right angles to O->polar vertex,
and every edge plane (Vacuus plate) is at right angles to the dual edge of the polar.
Arrangement data in the projective plane: f = (f0, f1, f2), t_j (points on exactly j lines), r_j (lines carrying exactly j points)."""
import os, sys, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../2026-11-24-permutahedron-leads/scripts"))
from perm_solid import build
from solids import Q, dot, cross, vsub, vsc


def pkey(v):
    """projective key of a nonzero vector: scale so the first nonzero coordinate is 1"""
    for x in v:
        if x.sign() != 0:
            return tuple((y / x).key() for y in v)
    raise ValueError("zero vector")


def is_mirror(n, V):
    keys = {tuple(x.key() for x in p) for p in V}
    nn = dot(n, n)
    for p in V:
        k = dot(n, p) / nn * Q(2)
        q = vsub(p, vsc(k, n))
        if tuple(x.key() for x in q) not in keys:
            return False
    return True


def run(name, group):
    S = build(name); V = S["V"]; faces = S["faces"]; planes = S["planes"]
    lines, kinds = {}, {}
    for (f, kind), (n, d) in zip(faces, planes):
        k = pkey(n); lines.setdefault(k, n); kinds.setdefault(k, set()).add(len(f))
    L = list(lines.values()); Lk = list(lines.keys())
    # task 1: polar vertex a_F = n/d (P* = {y : y.x <= 1 for x in P}); Resonus plane n.x = 0 is at right angles to O->a_F
    polar = [vsc(Q(1) / d, n) for (n, d) in planes]
    assert all(pkey(polar[i]) == pkey(planes[i][0]) for i in range(len(planes)))
    n_edges = 0
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            sh = set(faces[i][0]) & set(faces[j][0])
            if len(sh) == 2:
                n_edges += 1
                u, v = [V[k] for k in sh]
                e = vsub(polar[i], polar[j])               # direction of the dual edge of P*
                assert dot(e, u).sign() == 0 and dot(e, v).sign() == 0
                c = cross(u, v)                             # normal of the Vacuus plate through O, u, v
                assert any(x.sign() != 0 for x in c), "O on the line of an edge"
                assert pkey(c) == pkey(e)
    per_line = Counter(pkey(n) for n, d in planes)
    pts = {}
    for a in range(len(L)):
        for b in range(a + 1, len(L)):
            pts.setdefault(pkey(cross(L[a], L[b])), set()).update((a, b))
    f0 = len(pts)
    on_line = Counter()
    for s in pts.values():
        for a in s:
            on_line[a] += 1
    f1 = sum(on_line.values()); f2 = 1 - f0 + f1          # Euler characteristic of the projective plane is 1
    t = Counter(len(s) for s in pts.values()); r = Counter(on_line.values())
    simplicial = (2 * f1 == 3 * f2)                        # sum of sides over faces = 2 f1, each >= 3
    mirrors = [a for a in range(len(L)) if is_mirror(L[a], V)]
    return dict(solid=name, group=group, vertices=len(V), faces=len(faces), edges=n_edges,
                resonus_planes=len(L), faces_per_plane=dict(Counter(per_line.values())),
                planes_by_face_sides={str(k): v for k, v in sorted(Counter(tuple(sorted(kinds[k])) for k in Lk).items())},
                f=(f0, f1, f2), regions_in_space=2 * f2, t={j: t[j] for j in sorted(t)}, r={j: r[j] for j in sorted(r)},
                simplicial=simplicial, mirrors_among_planes=len(mirrors),
                mirror_face_sides=sorted({tuple(sorted(kinds[Lk[a]])) for a in mirrors}),
                polar_checks="ok: every Resonus plane at right angles to O->polar vertex; every Vacuus plate at right angles to its dual edge (%d edges)" % n_edges)


if __name__ == "__main__":
    res = [run("truncated_octahedron", "A3"), run("B3_permutahedron_123", "B3"), run("truncated_icosidodecahedron", "H3")]
    for o in res:
        print(json.dumps(o, default=str))
    json.dump(res, open(os.path.join(HERE, "../data/resonus_3d.json"), "w"), indent=1, default=str)
    print("FINAL ok" if all(o["simplicial"] for o in res) else "FINAL fail")
