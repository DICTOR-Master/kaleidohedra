"""Exact vertex sets of the four regular 4-polytopes with triangular 2-faces, their edges, 2-faces and cells, and the
four principal directions (vertex-, edge-, face-, cell-first), all exact (Q or Q(sqrt5)).

5-cell: vertices e_1..e_5 of R^5 (in the hyperplane sum = 1); a regular 4-simplex has no rational coordinates in R^4
(Schoenberg), so the study works in R^5 and always projects out n0 = (1,1,1,1,1) as well.
16-cell: ±e_i.   24-cell: all permutations of (±1,±1,0,0).
600-cell (radius 2): permutations of (±2,0,0,0); (±1,±1,±1,±1); even permutations of (±φ,±1,±1/φ,0).
"""
from itertools import permutations, product, combinations
from fractions import Fraction as Fr

from q5 import Q5, ZERO, ONE, PHI, IPHI, dot, sub, add, scal


def _uniq(vs):
    out = []
    s = set()
    for v in vs:
        k = tuple((x.a, x.b) for x in v)
        if k not in s:
            s.add(k)
            out.append(v)
    return out


def five_cell():
    V = [tuple(Q5(1 if i == j else 0) for j in range(5)) for i in range(5)]
    return V


def sixteen_cell():
    V = []
    for i in range(4):
        for s in (1, -1):
            V.append(tuple(Q5(s if j == i else 0) for j in range(4)))
    return V


def twentyfour_cell():
    V = []
    for i, j in combinations(range(4), 2):
        for si, sj in product((1, -1), repeat=2):
            v = [Q5(0)] * 4
            v[i] = Q5(si); v[j] = Q5(sj)
            V.append(tuple(v))
    return V


def even_perms4():
    out = []
    for p in permutations(range(4)):
        inv = sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b])
        if inv % 2 == 0:
            out.append(p)
    return out


def six_hundred_cell():
    V = []
    for i in range(4):
        for s in (2, -2):
            V.append(tuple(Q5(s if j == i else 0) for j in range(4)))
    for sg in product((1, -1), repeat=4):
        V.append(tuple(Q5(s) for s in sg))
    base = [PHI, ONE, IPHI, ZERO]
    for p in even_perms4():
        for sg in product((1, -1), repeat=3):
            b = [base[0] * sg[0], base[1] * sg[1], base[2] * sg[2], ZERO]
            v = [None] * 4
            for k in range(4):
                v[p[k]] = b[k]
            V.append(tuple(v))
    return _uniq(V)


def structure(V):
    """edges = minimal-distance pairs; triangles = 3-cliques; tetrahedral cells = 4-cliques."""
    n = len(V)
    d2 = {}
    m = None
    for i in range(n):
        for j in range(i + 1, n):
            w = sub(V[i], V[j])
            x = dot(w, w)
            d2[(i, j)] = x
            if m is None or x < m:
                m = x
    E = [k for k, x in d2.items() if x == m]
    adj = {i: set() for i in range(n)}
    for i, j in E:
        adj[i].add(j); adj[j].add(i)
    T = sorted({tuple(sorted((i, j, k))) for i, j in E for k in adj[i] & adj[j]})
    C = sorted({tuple(sorted((i, j, k, l))) for (i, j, k) in T for l in adj[i] & adj[j] & adj[k]})
    return {"edge2": m, "E": E, "adj": adj, "T": T, "K4": C}


def centroid(V, idx):
    s = tuple(ZERO for _ in V[0])
    for i in idx:
        s = add(s, V[i])
    return scal(Q5(Fr(1, len(idx))), s)


def polytope(name):
    if name == "5-cell":
        V = five_cell(); n0 = tuple(Q5(1) for _ in range(5)); centre = tuple(Q5(Fr(1, 5)) for _ in range(5))
    elif name == "16-cell":
        V = sixteen_cell(); n0 = None; centre = tuple(ZERO for _ in range(4))
    elif name == "24-cell":
        V = twentyfour_cell(); n0 = None; centre = tuple(ZERO for _ in range(4))
    elif name == "600-cell":
        V = six_hundred_cell(); n0 = None; centre = tuple(ZERO for _ in range(4))
    st = structure(V)
    # a vertex, an edge, a 2-face and a cell through vertex 0
    v0 = 0
    e = next(e for e in st["E"] if v0 in e)
    t = next(t for t in st["T"] if set(e) <= set(t))
    if name == "24-cell":
        # octahedral cell: the 6 vertices on the facet hyperplane through t (found exactly: x . c = max)
        c_t = centroid(V, t)
        # facets of the 24-cell are x_i = ±1 and (±1,±1,±1,±1).x = 2; pick the facet normal maximising on t
        normals = [tuple(Q5(s if j == i else 0) for j in range(4)) for i in range(4) for s in (1, -1)]
        normals += [tuple(Q5(s) for s in sg) for sg in product((1, -1), repeat=4)]
        cell = None
        for nv in normals:
            vals = [dot(nv, v) for v in V]
            mx = max(vals, key=float)
            on = [i for i, x in enumerate(vals) if x == mx]
            if set(t) <= set(on) and len(on) == 6:
                cell = tuple(on); break
    else:
        cell = next(c for c in st["K4"] if set(t) <= set(c))
    dirs = {}
    for lab, idx in (("vertex-first", (v0,)), ("edge-first", e), ("face-first", t), ("cell-first", cell)):
        dirs[lab] = {"d": sub(centroid(V, idx), centre), "element": idx}
    counts = {"V": len(V), "E": len(st["E"]), "T": len(st["T"]), "K4": len(st["K4"])}
    return {"name": name, "V": V, "n0": n0, "centre": centre, "st": st, "dirs": dirs, "counts": counts}
