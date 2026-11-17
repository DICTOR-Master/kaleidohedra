#!/usr/bin/env python3
"""Library for the mixing study: the three k = 10 solids as signed cell lists in Z^6, their images under the 120 symmetries
and Z^6 translations, and an EXACT overlap test.

Solids (all exact, Z^6 face form of zsurf.py, copied unchanged from study 2026-11-15-grunbaum-k10):
  A  = GET A (candidate 0), 16 cells (tile12.json), all +1
  B  = GET B (candidate 1), 16 cells (tile12.json), all +1
  C  = Inchbald's dimpled triacontahedron (candidate 2, in Inchbald's own position from study 2026-11-17-inchbald-check):
       17 cells of a fine tiling of T that holds three of its four removed corner cells, with +1, and the fourth corner cell k
       with -1. 1_C = sum(+cells) - 1_k almost everywhere; certified in build_C().

Exact overlap test (interiors meet <=> intersection volume > 0, for closed polyhedral solids):
  vol(X n Y) = sum over cell pairs s_x s_y vol(x n y). zsurf.Geo.relation (exact separating-axis test on the 15 normals, exact for
  two parallelepipeds on these axes) gives vol(x n y) = 0 for 'apart'/'touch'; for 'cross' pairs the volume is computed exactly in
  Q(phi) (vertex enumeration of the 12 half-spaces and facet fans). For A, B (all cells +1) overlap <=> some pair crosses."""
import sys, json, itertools, functools
from fractions import Fraction as Fr
import numpy as np
HERE = __file__.rsplit('/', 1)[0]
sys.path.insert(0, HERE)
from zsurf import *

G = Geo(6); n = 6
SYMS = signed_perms(G)                       # 120: (perm, sg, det)
assert len(SYMS) == 120
def sym_matrix(sym):
    perm, sg, _ = sym; M = np.zeros((6, 6), dtype=np.int64)
    for i in range(6): M[perm[i], i] = sg[i]
    return M
MATS = [sym_matrix(s) for s in SYMS]
MKEY = {M.tobytes(): i for i, M in enumerate(MATS)}
def mat_index(M): return MKEY[np.asarray(M, dtype=np.int64).tobytes()]
IDENT = mat_index(np.eye(6, dtype=np.int64))
INV = [mat_index(M.T) for M in MATS]
def compose(i, j): return mat_index(MATS[i] @ MATS[j])

def tcell(cell, gi, t):
    """image of the cell (p, ijk) under x -> M x + t"""
    p, ax = cell; perm, sg, _ = SYMS[gi]; M = MATS[gi]
    q = M @ np.array(p, dtype=np.int64)
    for i in ax:
        if sg[i] < 0: q[perm[i]] -= 1
    q = q + np.array(t, dtype=np.int64)
    return (tuple(int(x) for x in q), tuple(sorted(perm[i] for i in ax)))
def tfaces(S, gi, t):
    T = apply_sym(G, S, SYMS[gi])
    return {(tuple(int(a + b) for a, b in zip(f[0], t)), f[1], f[2]): s for f, s in T.items()}

# ---------------- exact Q(phi) ----------------
class Q:
    __slots__ = ('a', 'b')            # a + b*phi, a, b Fractions
    def __init__(s, a, b=0): s.a = a if isinstance(a, Fr) else Fr(a); s.b = b if isinstance(b, Fr) else Fr(b)
    def __add__(s, o): return Q(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o): return Q(s.a*o.a + s.b*o.b, s.a*o.b + s.b*o.a + s.b*o.b)
    def __neg__(s): return Q(-s.a, -s.b)
    def inv(s):
        N = s.a*s.a + s.a*s.b - s.b*s.b
        return Q((s.a + s.b)/N, -s.b/N)
    def __truediv__(s, o): return s*o.inv()
    def sign(s): return zsign((s.a, s.b))
    def iszero(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b)*(1 + 5**0.5)/2
ZERO = Q(0)
EQ = [[Q(*c) for c in e] for e in G.E]          # axes in Q(phi)^3
def vq(p): return [sum((EQ[i][j]*Q(c) for i, c in enumerate(p) if c), ZERO) for j in range(3)]
def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
def cross(u, v): return [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0]]
def sub(u, v): return [x - y for x, y in zip(u, v)]
def det3q(u, v, w): return dot(u, cross(v, w))
NORM = {pr: cross(EQ[pr[0]], EQ[pr[1]]) for pr in G.pairs}

def cell_halfspaces(cell):
    """6 half-spaces (normal, c) with normal . x <= c"""
    p, ax = cell; o = vq(p); H = []
    for x, y in itertools.combinations(ax, 2):
        z = [w for w in ax if w not in (x, y)][0]
        nv = NORM[(x, y)]; lo = dot(nv, o); hi = lo + dot(nv, EQ[z])
        if (hi - lo).sign() < 0: lo, hi = hi, lo
        H.append((nv, hi)); H.append(([-c for c in nv], -lo))
    return H

def polytope_volume(H):
    """exact volume (in Q(phi)) of {x : n.x <= c for (n, c) in H} (bounded); vertex enumeration and facet fans"""
    V = []
    for (n1, c1), (n2, c2), (n3, c3) in itertools.combinations(H, 3):
        d = det3q(n1, n2, n3)
        if d.iszero(): continue
        # Cramer: x = (c1 (n2 x n3) + c2 (n3 x n1) + c3 (n1 x n2)) / d
        a, b, c = cross(n2, n3), cross(n3, n1), cross(n1, n2)
        x = [(c1*a[j] + c2*b[j] + c3*c[j])/d for j in range(3)]
        if all((cc - dot(nn, x)).sign() >= 0 for nn, cc in H):
            key = tuple((t.a, t.b) for t in x)
            if key not in {tuple((t.a, t.b) for t in v) for v in V}: V.append(x)
    if len(V) < 4: return ZERO
    v0 = V[0]; tot = ZERO
    seen_planes = set()
    for nn, cc in H:
        F = [v for v in V if (dot(nn, v) - cc).iszero()]
        if len(F) < 3: continue
        key = frozenset(tuple((t.a, t.b) for t in v) for v in F)
        if key in seen_planes: continue
        seen_planes.add(key)
        g = [sum((v[j] for v in F), ZERO)/Q(len(F)) for j in range(3)]
        u = sub(F[0], g); w = cross(nn, u)
        def coords(v): r = sub(v, g); return dot(u, r), dot(w, r)
        def half(xy): x, y = xy; return 0 if (y.sign() > 0 or (y.iszero() and x.sign() > 0)) else 1
        def cmp(p1, p2):
            c1, c2 = coords(p1), coords(p2); h1, h2 = half(c1), half(c2)
            if h1 != h2: return h1 - h2
            s = (c1[0]*c2[1] - c1[1]*c2[0]).sign()
            return -s
        F.sort(key=functools.cmp_to_key(cmp))
        for i in range(1, len(F) - 1):
            tot = tot + det3q(sub(F[0], v0), sub(F[i], v0), sub(F[i + 1], v0))
    if tot.sign() < 0: tot = -tot
    return tot/Q(6)

def cell_volume(cell):
    p, ax = cell; d = det3q(*[EQ[i] for i in ax]); return d if d.sign() > 0 else -d

@functools.lru_cache(maxsize=None)
def pair_volume(c1, c2):
    """exact vol(c1 n c2), translation-normalised by the caller's cache key"""
    r = G.relation(c1[0], c1[1], c2[0], c2[1])
    if r != 'cross': return ZERO
    if c1 == c2: return cell_volume(c1)
    return polytope_volume(cell_halfspaces(c1) + cell_halfspaces(c2))

def norm_pair(c1, c2):
    o = c1[0]
    return ((tuple(0 for _ in o), c1[1]), (tuple(b - a for a, b in zip(o, c2[0])), c2[1]))

def overlap_volume(X, Y):
    """X, Y: lists of (cell, sign). Exact vol(X n Y) as Q; short-circuits are not used, so the value is the full exact volume."""
    tot = ZERO
    for cx, sx in X:
        for cy, sy in Y:
            if G.relation(cx[0], cx[1], cy[0], cy[1]) != 'cross': continue
            v = pair_volume(*norm_pair(cx, cy))
            tot = tot + (v if sx*sy > 0 else -v)
    return tot

def overlaps(X, Y):
    """exact: True iff interiors of X and Y meet. Fast path when all signs are +1."""
    if all(s > 0 for _, s in X) and all(s > 0 for _, s in Y):
        return any(G.relation(cx[0], cx[1], cy[0], cy[1]) == 'cross' for cx, _ in X for cy, _ in Y)
    v = overlap_volume(X, Y)
    assert v.sign() >= 0, 'negative overlap volume: decomposition error'
    return v.sign() > 0

# ---------------- the solids ----------------
def load_solids(k10_dir, inch_json):
    d = json.load(open(k10_dir + '/data/search6.json')); t = json.load(open(k10_dir + '/data/tile12.json'))
    sol = {}
    for name, idx in (('A', 0), ('B', 1)):
        S = {(tuple(f[0]), f[1], f[2]): f[3] for f in d['candidates_rank_le_3'][idx]['faces']}
        cells = [(tuple(c[0]), tuple(c[1])) for c in t['results'][idx]['cells']]
        assert from_cells(G, cells) == S
        sol[name] = {'faces': S, 'cells': [(c, 1) for c in cells], 'basis': t['results'][idx]['basis']}
    ij = json.load(open(inch_json))
    S = {(tuple(f[0]), f[1], f[2]): f[3] for f in ij['candidates_rank_le_3'][0]['faces']}
    sol['C'] = {'faces': S, 'cells': build_C(S)}
    info, _ = analyse(G, S); sol['C']['basis'] = int_rank_basis(list(face_pair_vectors(G, S, info).values()))
    return sol

REM = [((0,1,0,0,0,0),(0,2,5)), ((0,0,0,0,0,0),(0,3,4)), ((0,0,0,1,0,1),(1,2,4)), ((1,0,1,0,1,0),(1,3,5))]

def build_C(S):
    """signed decomposition of Inchbald's solid: flip search (as in inchbald-check/overlap_float.py, but every step exact)
    for a fine tiling of T holding three of the four corner cells; then +17 cells, -1 corner. Certified exactly:
    (i) the 20 cells tile T (surface = T, no two cross); (ii) the four corners are pairwise non-crossing and lie in T
    (T = intersection of its 15 slabs, so containment is exact on the 15 normals); (iii) T minus the four corners has surface S."""
    from collections import deque
    T = zonotope(G); E = np.array([[zfloat(c) for c in e] for e in G.E])
    h = np.random.default_rng(0).normal(size=n); W = np.hstack([E, h[:, None]]); start = []
    for t in itertools.combinations(range(n), 3):
        d3 = np.linalg.det(E[list(t)]); q = [0]*n
        for l in range(n):
            if l not in t and np.sign(np.linalg.det(W[list(t) + [l]])) * np.sign(d3) > 0: q[l] = 1
        start.append((tuple(q), t))
    if from_cells(G, start) != T: start = [(tuple(1 - x if i not in t else 0 for i, x in enumerate(q)), t) for q, t in start]
    def valid(cells): return from_cells(G, cells) == T and not any(G.relation(a[0], a[1], b[0], b[1]) == 'cross' for a, b in itertools.combinations(cells, 2))
    assert valid(start)
    seen = {frozenset(start)}; Qu = deque([frozenset(start)]); best = None
    while Qu and best is None:
        til = Qu.popleft()
        for r4 in REM:
            if all(r in til for r in REM if r != r4): best = (til, r4); break
        bt = {c[1]: c for c in til}
        for Aa in itertools.combinations(range(n), 4):
            cs = [bt[tuple(x for x in Aa if x != l)] for l in Aa]
            if len({tuple(c[0][i] for i in range(n) if i not in Aa) for c in cs}) != 1: continue
            new = set(til)
            for l, c in zip(Aa, cs): q = list(c[0]); q[l] = 1 - q[l]; new.discard(c); new.add((tuple(q), c[1]))
            k = frozenset(new)
            if k not in seen and valid(list(k)): seen.add(k); Qu.append(k)
    til, r4 = best
    assert valid(list(til))
    # corners pairwise not crossing, and inside T
    assert not any(G.relation(a[0], a[1], b[0], b[1]) == 'cross' for a, b in itertools.combinations(REM, 2))
    Tlo = {}; Thi = {}
    for xy in G.pairs:
        lo, hi = G.interval(tuple([0]*6), tuple(range(6)), xy); Tlo[xy] = lo; Thi[xy] = hi
    for c in REM:
        for xy in G.pairs:
            lo, hi = G.interval(c[0], c[1], xy)
            assert zsign(zsub(lo, Tlo[xy])) >= 0 and zsign(zsub(Thi[xy], hi)) >= 0
    # surface of T minus the four corners (as a Z/2-free signed chain): T's faces, plus/minus corner faces
    cnt = {f: s for f, s in T.items()}
    for c in REM:
        for f, s in cell_out_faces(c).items():           # removing c: its faces with inward... boundary of T - c
            if f in cnt and cnt[f] == s: del cnt[f]
            else: cnt[f] = -s
    assert cnt == S, 'T minus the four corners is not the solid'
    signed = [(c, 1) for c in til if c not in REM] + [(r4, -1)]
    assert len(signed) == 18
    # volume check: sum of signed cell volumes = volume of S
    v = sum((cell_volume(c)*Q(s) for c, s in signed), ZERO)
    v3 = volume3(G, S); assert v*Q(3) == Q(*v3)
    return signed

def cell_out_faces(cell):
    p, (i, j, k) = cell; out = {}
    for (a, b), o in (((i, j), k), ((i, k), j), ((j, k), i)):
        so = zsign(G.D[(a, b, o)])
        out[(p, a, b)] = -so; out[(vadd(p, unit(n, o)), a, b)] = so
    return out

def place(sol, name, gi, t):
    """placed solid: (faces dict, signed cells)"""
    return tfaces(sol[name]['faces'], gi, t), [(tcell(c, gi, t), s) for c, s in sol[name]['cells']]

def face_key(F): return frozenset(F.items())
