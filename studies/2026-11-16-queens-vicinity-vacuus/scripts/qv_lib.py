"""Shared tools for the Queens' vicinity Vacuus study and the Queens' chambers study (16 Nov 2026).

Frame: the 600-cell of radius 2 (permutations of (+-2,0,0,0); (+-1,+-1,+-1,+-1); even permutations of (+-phi,+-1,+-1/phi,0)),
all coordinates exact in Q(sqrt5) (q5.Q5 of study 2026-10-27-4d-shadows, reused).
Walls of the Queens:
  mirror walls  = the 60 hyperplanes v-perp, v a corner of the 600-cell (the H4 mirrors; the 120-cell has the same 60);
  cross walls   = the 300 central sections parallel to a pair of opposite tetrahedral cells of the 600-cell, i.e. c-perp,
                  c a cell centre of the 600-cell (= a corner direction of the 120-cell).
A plate (Vacuus) of a 4D shape = the central hyperplane spanned by one 2-face (ridge); of a 3D slice or shadow taken across a
direction n = the central plane spanned by one edge, lifted to the 4D hyperplane span(n, edge).
Every plate normal is computed exactly (generalised cross product), put in canonical form (first nonzero entry 1) and
looked up exactly in the wall sets. Floats (scipy ConvexHull) only propose the face lattice; every ridge used is checked
exactly to lie in its plate.
"""
import os, sys, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-10-27-4d-shadows', 'scripts'))
from q5 import Q5, ZERO, ONE, PHI, IPHI, dot, sub, add, scal, q5str  # noqa: E402
from polytopes import six_hundred_cell, structure  # noqa: E402


def key(v):
    return tuple((x.a, x.b) for x in v)


def neg(v):
    return tuple(-x for x in v)


def fl(v):
    return np.array([float(x) for x in v])


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def cross4(u, v, w):
    """vector orthogonal to u, v, w in R^4 (exact)."""
    out = []
    for i in range(4):
        cols = [j for j in range(4) if j != i]
        m = [[r[j] for j in cols] for r in (u, v, w)]
        d = det3(m)
        out.append(d if i % 2 == 0 else -d)
    return tuple(out)


def canon(n):
    for x in n:
        if not x.iszero():
            inv = x.inv()
            return tuple(y * inv for y in n)
    raise ValueError('zero vector')


def reflect(x, a, aa=None):
    aa = dot(a, a) if aa is None else aa
    k = Q5(2) * dot(x, a) / aa
    return tuple(xi - k * ai for xi, ai in zip(x, a))


def solve(A, b):
    """exact Gauss-Jordan in Q(sqrt5): A x = b, A square nonsingular."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if not M[r][c].iszero())
        M[c], M[p] = M[p], M[c]
        iv = M[c][c].inv(); M[c] = [x * iv for x in M[c]]
        for r in range(n):
            if r != c and not M[r][c].iszero():
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return tuple(M[r][n] for r in range(n))


# ------------------------------------------------------------------ the Queens and their walls
V600 = six_hundred_cell()
ST600 = structure(V600)
CELLS600 = ST600['K4']
C600 = [tuple(sum((V600[i][k] for i in c), ZERO) * Q5(Fr(1, 4)) for k in range(4)) for c in CELLS600]   # 120-cell corners
MIRROR = {key(canon(v)) for v in V600}
CROSS = {key(canon(c)) for c in C600}


def wall_kind(n):
    k = key(canon(n))
    return 'mirror' if k in MIRROR else ('cross' if k in CROSS else 'none')


# simple roots: extreme rays of the cone of positive roots for a generic direction (LP proposes, Gram verified exactly)
def simple_roots():
    from scipy.optimize import linprog
    g = np.array([1.0, 0.3141, 0.0577, 0.01234])
    pos = [v for v in V600 if fl(v) @ g > 0]
    P = np.array([fl(v) for v in pos])
    simp = []
    for i, v in enumerate(pos):
        others = np.delete(P, i, axis=0)
        r = linprog(np.zeros(len(others)), A_eq=others.T, b_eq=P[i], bounds=(0, None), method='highs')
        if r.status != 0:
            simp.append(v)
    assert len(simp) == 4, len(simp)
    # order as a chain 1-5-2-3-3-3-4 (node 1 at the 5-bond end), as in #107
    G = [[dot(a, b) for b in simp] for a in simp]
    m5 = -(PHI * Q5(2))            # |a|^2 = 4: a.b = -4 cos(pi/5) = -2 phi
    m3 = Q5(-2)
    bond = lambda i, j: 5 if G[i][j] == m5 else (3 if G[i][j] == m3 else (2 if G[i][j].iszero() else None))
    ends5 = [i for i in range(4) if any(bond(i, j) == 5 for j in range(4) if j != i)]
    n1 = next(i for i in ends5 if sum(bond(i, j) != 2 for j in range(4) if j != i) == 1)
    order = [n1]
    while len(order) < 4:
        last = order[-1]
        order.append(next(j for j in range(4) if j not in order and bond(last, j) in (3, 5)))
    alpha = [simp[i] for i in order]
    bonds = [bond(order[i], order[i + 1]) for i in range(3)]
    zero_ok = all(dot(alpha[i], alpha[j]).iszero() for i in range(4) for j in range(i + 2, 4))
    assert bonds == [5, 3, 3] and zero_ok, (bonds, zero_ok)
    return alpha


ALPHA = simple_roots()
# fundamental weights: alpha_j . omega_i = delta_ij
OMEGA = [solve(ALPHA, tuple(Q5(1 if j == i else 0) for j in range(4))) for i in range(4)]


def orbit(seed, gens=None, cap=20000):
    gens = ALPHA if gens is None else gens
    aa = [dot(a, a) for a in gens]
    seen = {key(seed): seed}; todo = [seed]
    while todo:
        x = todo.pop()
        for a, q in zip(gens, aa):
            y = reflect(x, a, q); k = key(y)
            if k not in seen:
                seen[k] = y; todo.append(y)
                if len(seen) > cap:
                    raise RuntimeError('orbit cap')
    return list(seen.values())


def wythoff(lam):
    x = tuple(sum((Q5(l) * OMEGA[i][k] for i, l in enumerate(lam)), ZERO) for k in range(4))
    return orbit(x)


# ------------------------------------------------------------------ face lattices (float proposal)
def lattice(Vf, dec=6):
    """facets (frozensets of vertex ids) and ridges (frozensets), from Qhull simplices + neighbours."""
    Vf = np.asarray(Vf, float)
    sc = np.max(np.linalg.norm(Vf - Vf.mean(0), axis=1))
    h = ConvexHull(Vf / sc)
    eq = {}; fid = []
    for e in h.equations:
        k = tuple(np.round(e, dec) + 0.0); fid.append(eq.setdefault(k, len(eq)))
    fv = [set() for _ in eq]
    for j, s in enumerate(h.simplices):
        fv[fid[j]].update(s.tolist())
    fv = [frozenset(x) for x in fv]
    rid = set()
    for j, nb in enumerate(h.neighbors):
        for k in nb:
            if fid[j] != fid[k]:
                rid.add(fv[fid[j]] & fv[fid[k]])
    return fv, sorted(rid, key=sorted), h


def polygon_edges(Vf, face):
    """the sides of a polygon (2-face) given its vertex ids: order by angle in its plane."""
    ids = sorted(face); P = Vf[ids]; c = P.mean(0)
    u, s, vt = np.linalg.svd(P - c)
    xy = (P - c) @ vt[:2].T
    o = np.argsort(np.arctan2(xy[:, 1], xy[:, 0]))
    return {tuple(sorted((ids[o[i]], ids[o[(i + 1) % len(o)]]))) for i in range(len(o))}


def three_independent(Vf, ids):
    ids = list(ids); a = ids[0]
    for b in ids[1:]:
        for c in ids[2:]:
            if c == b:
                continue
            M = Vf[[a, b, c]]
            if np.linalg.matrix_rank(M, tol=1e-9) == 3:
                return a, b, c
    raise ValueError('degenerate ridge')


def vacuus4(V, name='', need_euler=True):
    """V: exact 4D vertex list (centre = origin). Returns the Vacuus record with wall kinds."""
    Vf = np.array([fl(v) for v in V])
    fac, rid, _ = lattice(Vf)
    edges = set()
    for r in rid:
        edges |= polygon_edges(Vf, r)
    plates = {}
    sizes = {}
    for r in rid:
        a, b, c = three_independent(Vf, r)
        n = canon(cross4(V[a], V[b], V[c]))
        assert all(dot(V[i], n).iszero() for i in r), 'ridge off its plate'
        plates.setdefault(key(n), []).append(r)
        sizes[len(r)] = sizes.get(len(r), 0) + 1
    kinds = {'mirror': 0, 'cross': 0, 'none': 0}
    by_kind_ridges = {'mirror': 0, 'cross': 0, 'none': 0}
    per_plate = {}
    for k, rs in plates.items():
        w = 'mirror' if k in MIRROR else ('cross' if k in CROSS else 'none')
        kinds[w] += 1; by_kind_ridges[w] += len(rs)
        per_plate[len(rs)] = per_plate.get(len(rs), 0) + 1
    ks = {key(v) for v in V}
    csym = all(key(neg(v)) in ks for v in V)
    # opposite ridges share a plate (heart kind) when the shape is centrally symmetric
    rec = {'name': name, 'V': len(V), 'E': len(edges), 'F2': len(rid), 'F3': len(fac),
           'euler': len(V) - len(edges) + len(rid) - len(fac), 'ridge_sizes': {str(k): v for k, v in sorted(sizes.items())},
           'plates': len(plates), 'ridges_per_plate': {str(k): v for k, v in sorted(per_plate.items())},
           'central_symmetry': csym, 'kind': 'heart' if csym else 'non-heart',
           'plates_mirror': kinds['mirror'], 'plates_cross': kinds['cross'], 'plates_none': kinds['none'],
           'ridges_mirror': by_kind_ridges['mirror'], 'ridges_cross': by_kind_ridges['cross'], 'ridges_none': by_kind_ridges['none']}
    rec['hidden'] = verdict(rec)
    if need_euler:
        assert rec['euler'] == 0, rec
    return rec


def verdict(rec):
    w = rec['plates_mirror'] + rec['plates_cross']
    return 'hidden' if rec['plates_none'] == 0 else ('not hidden' if w == 0 else 'partly hidden')


# ------------------------------------------------------------------ 3D shapes across a direction n
def basis3(n):
    nf = fl(n); nf = nf / np.linalg.norm(nf)
    q, _ = np.linalg.qr(np.column_stack([nf, np.eye(4)]))
    return q[:, 1:4]


def vacuus3(P, n, centre, name=''):
    """P: exact 4D points of a 3D shape lying in a hyperplane parallel to n-perp; plates lifted to span(n, edge)."""
    B = basis3(n)
    Pf = np.array([fl(p) for p in P]) @ B
    h = ConvexHull(Pf)
    eq = {}; fid = []
    sc = np.max(np.linalg.norm(Pf - Pf.mean(0), axis=1))
    for e in h.equations:
        k = tuple(np.round(e / [1, 1, 1, sc], 6) + 0.0); fid.append(eq.setdefault(k, len(eq)))
    fv = [set() for _ in eq]
    for j, s in enumerate(h.simplices):
        fv[fid[j]].update(s.tolist())
    edges = set()
    for j, nb in enumerate(h.neighbors):
        for k in nb:
            if fid[j] != fid[k]:
                e = fv[fid[j]] & fv[fid[k]]
                assert len(e) == 2, e
                edges.add(tuple(sorted(e)))
    verts = sorted({i for e in edges for i in e})
    plates = {}
    for a, b in edges:
        nn = canon(cross4(n, P[a], P[b]))
        assert dot(P[a], nn).iszero() and dot(P[b], nn).iszero() and dot(n, nn).iszero()
        plates.setdefault(key(nn), []).append((a, b))
    kinds = {'mirror': 0, 'cross': 0, 'none': 0}
    for k in plates:
        kinds['mirror' if k in MIRROR else ('cross' if k in CROSS else 'none')] += 1
    ks = {key(P[i]) for i in verts}
    two_c = scal(Q5(2), centre)
    csym = all(key(sub(two_c, P[i])) in ks for i in verts)
    per = {}
    for rs in plates.values():
        per[len(rs)] = per.get(len(rs), 0) + 1
    rec = {'name': name, 'V': len(verts), 'E': len(edges), 'F': len(fv), 'euler': len(verts) - len(edges) + len(fv),
           'plates': len(plates), 'ridges_per_plate': {str(k): v for k, v in sorted(per.items())},
           'central_symmetry': csym, 'kind': 'heart' if csym else 'non-heart',
           'plates_mirror': kinds['mirror'], 'plates_cross': kinds['cross'], 'plates_none': kinds['none']}
    rec['hidden'] = verdict(rec)
    assert rec['euler'] == 2, rec
    return rec


def slice_points(V, E, n, hv):
    hs = [dot(v, n) for v in V]
    pts = [V[i] for i, x in enumerate(hs) if x == hv]
    for a, b in E:
        ha, hb = hs[a], hs[b]
        if ((ha - hv) * (hb - hv)).sign() < 0:
            t = (hv - ha) / (hb - ha)
            pts.append(tuple(x + t * (y - x) for x, y in zip(V[a], V[b])))
    return pts


def shadow_points(V, n):
    nn = dot(n, n); out = {}
    for v in V:
        p = sub(v, scal(dot(v, n) / nn, n)); out.setdefault(key(p), p)
    return list(out.values())
