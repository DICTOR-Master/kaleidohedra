# DICTO · dictospheres.com — exact library for the paper on Grünbaum's zone question at k = 10 (GET A and GET B).
# Numbers in Z[φ] are integer pairs (x, y) = x + yφ; every sign and equality is decided by integer tests, no floats.
# A point of the six-axis model is p in Z^6, standing for Σ p_i e_i with the six 5-fold axes e_i below; the map Z^6 -> R^3 is
# injective (the axes are independent over Q), so points, faces and cells are compared as integer vectors.
# A face is (q, a, b, s): the rhombus q + [0,1]e_a + [0,1]e_b, a < b, outward normal s·(e_a × e_b), s = ±1 (the format of
# studies/2026-11-15-grunbaum-k10/data/search6.json). A cell (p, (i, j, k)) is the rhombohedron p + Σ [0,1]e_t (tile12.json).
# Written for this paper; the model is that of the 2026-11-15 study (zsurf.py), re-implemented here as an independent check.
import itertools, json, os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIES = os.environ.get('STUDIES', os.path.join(HERE, '..', '..', '..', 'studies'))
K10 = os.path.join(STUDIES, '2026-11-15-grunbaum-k10')

# ---------- Z[φ], φ² = φ + 1 ----------
def add(u, v): return (u[0] + v[0], u[1] + v[1])
def sub(u, v): return (u[0] - v[0], u[1] - v[1])
def mul(u, v): return (u[0] * v[0] + u[1] * v[1], u[0] * v[1] + u[1] * v[0] + u[1] * v[1])
def neg(u): return (-u[0], -u[1])
def sgn(u):
    """exact sign of x + yφ = (2x + y + y√5)/2"""
    a, b = 2 * u[0] + u[1], u[1]
    if a >= 0 and b >= 0: return 0 if a == 0 and b == 0 else 1
    if a <= 0 and b <= 0: return -1
    return (1 if a > 0 else -1) if a * a > 5 * b * b else (1 if b > 0 else -1)
def zabs(u): return u if sgn(u) >= 0 else neg(u)
PHIF = (1 + 5 ** 0.5) / 2
def flt(u): return u[0] + u[1] * PHIF
def zstr(u):
    x, y = u
    if y == 0: return str(x)
    t = ('φ' if y == 1 else ('−φ' if y == -1 else f'{y}φ'))
    if x == 0: return t
    return f'{x} + {t}' if y > 0 else f'{x} − {t[1:] if t.startswith("−") else t}'

O, I, P, M = (0, 0), (1, 0), (0, 1), (0, -1)
# the six 5-fold axes: (1,φ,0), (−1,φ,0), (0,1,φ), (0,−1,φ), (φ,0,1), (−φ,0,1)
AX = [(I, P, O), ((-1, 0), P, O), (O, I, P), (O, (-1, 0), P), (P, O, I), (M, O, I)]
N = 6

def vdot(u, v): return add(add(mul(u[0], v[0]), mul(u[1], v[1])), mul(u[2], v[2]))
def vcross(u, v): return (sub(mul(u[1], v[2]), mul(u[2], v[1])), sub(mul(u[2], v[0]), mul(u[0], v[2])), sub(mul(u[0], v[1]), mul(u[1], v[0])))
def vadd(u, v): return tuple(add(a, b) for a, b in zip(u, v))
def vscale(c, u): return tuple(mul((c, 0), a) for a in u)
def det3(u, v, w): return vdot(u, vcross(v, w))
def pos(p):
    """R^3 point (in Z[φ]^3) of p in Z^6"""
    r = (O, O, O)
    for c, e in zip(p, AX):
        if c: r = vadd(r, vscale(c, e))
    return r
def posf(p): return [flt(c) for c in pos(p)]

D = {(i, j, k): det3(AX[i], AX[j], AX[k]) for i in range(N) for j in range(N) for k in range(N)}
TRIPLES = list(itertools.combinations(range(N), 3))
PAIRS = list(itertools.combinations(range(N), 2))
def unit(i): return tuple(1 if t == i else 0 for t in range(N))
def padd(p, q): return tuple(a + b for a, b in zip(p, q))
def psub(p, q): return tuple(a - b for a, b in zip(p, q))

# ---------- cells and faces ----------
def cell_faces(p, t):
    """the six oriented faces of the cell p + [0,1]^t, as (q, a, b) -> s"""
    out = {}
    for c in t:
        a, b = [x for x in t if x != c]
        s = sgn(D[(a, b, c)])
        assert s != 0
        out[(tuple(p), a, b)] = out.get((tuple(p), a, b), 0) - s          # base face: the cell lies on the +e_c side
        q = padd(p, unit(c)); out[(q, a, b)] = out.get((q, a, b), 0) + s
    return out

def boundary(cells):
    """oriented boundary of a union of cells (interior faces cancel); returns {(q, a, b): s}"""
    acc = {}
    for p, t in cells:
        for f, s in cell_faces(p, t).items(): acc[f] = acc.get(f, 0) + s
    out = {f: s for f, s in acc.items() if s}
    assert all(abs(s) == 1 for s in out.values()), 'a face counted twice the same way'
    return out

def faces_from_json(L): return {(tuple(q), a, b): s for q, a, b, s in L}

def corners(q, a, b):
    return [tuple(q), padd(q, unit(a)), padd(padd(q, unit(a)), unit(b)), padd(q, unit(b))]

def edges_of(q, a, b):
    """the four sides as (start point, direction)"""
    return [(tuple(q), a), (padd(q, unit(b)), a), (tuple(q), b), (padd(q, unit(a)), b)]

def cell_volume(t): return zabs(D[t])

def covolume(B):
    v = [pos(b) for b in B]; return zabs(det3(*v))

# ---------- the 120 symmetries of the six-axis star ----------
def gram(): return [[vdot(AX[i], AX[j]) for j in range(N)] for i in range(N)]

def symmetries():
    """all signed permutations e_i -> s_i e_π(i) that keep the Gram matrix: exactly the isometries of the star; with det sign"""
    G = gram(); out = []
    def rec(i, perm, sg):
        if i == N:
            im = [vscale(sg[t], AX[perm[t]]) for t in range(3)]
            d0 = D[(0, 1, 2)]; d1 = det3(*im)
            assert d1 == d0 or d1 == neg(d0)
            out.append((tuple(perm), tuple(sg), 1 if d1 == d0 else -1)); return
        for j in range(N):
            if j in perm: continue
            for s in (1, -1):
                if all(mul((s * sg[t], 0), G[j][perm[t]]) == G[i][t] for t in range(i)) and G[j][j] == G[i][i]:
                    rec(i + 1, perm + [j], sg + [s])
    rec(0, [], []); return out

def apply_face(g, f):
    """image of the unoriented face (q, a, b) under g = (perm, signs, det)"""
    perm, sg, _ = g; q, a, b = f
    q2 = [0] * N
    for i, c in enumerate(q): q2[perm[i]] += sg[i] * c
    for d in (a, b):
        if sg[d] < 0: q2[perm[d]] -= 1
    a2, b2 = sorted((perm[a], perm[b]))
    return (tuple(q2), a2, b2)

def norm_set(F):
    """unoriented face set, translated so that its lexicographically least face sits at q = 0"""
    F = sorted(F); q0 = F[0][0]
    return frozenset((psub(q, q0), a, b) for q, a, b in F)

def congruences(FX, FY, G):
    """the symmetries g with g(X) a translate of Y (unoriented face sets): (proper, improper) counts"""
    ny = norm_set(FY); pr = im = 0
    for g in G:
        if norm_set(apply_face(g, f) for f in FX) == ny:
            if g[2] > 0: pr += 1
            else: im += 1
    return pr, im

# ---------- zones ----------
def zones(F):
    """for each axis d: the faces with a side of direction d, and whether they form one cycle crossing those sides"""
    out = {}
    for d in range(N):
        Z = [f for f in F if d in (f[1], f[2])]
        side = {}
        for f in Z:
            q, a, b = f; o = b if a == d else a
            for e in [(tuple(q), d), (padd(q, unit(o)), d)]: side.setdefault(e, []).append(f)
        ok = all(len(v) == 2 for v in side.values())
        adj = {f: set() for f in Z}
        for v in side.values():
            if len(v) == 2: adj[v[0]].add(v[1]); adj[v[1]].add(v[0])
        seen, stack = set(), [Z[0]] if Z else []
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x); stack.extend(adj[x] - seen)
        cyc = ok and all(len(v) == 2 for v in adj.values()) and len(seen) == len(Z)
        out[d] = (len(Z), cyc, Z)
    return out

def surface_stats(Fo):
    """closed 2-manifold, Euler characteristic, vertex links, adjacent-face planes (oriented faces Fo)"""
    F = list(Fo)
    V = {c for f in F for c in corners(*f)}
    E = {}
    for f in F:
        for e in edges_of(*f): E.setdefault(e, []).append(f)
    closed = all(len(v) == 2 for v in E.values())
    # vertex links: the faces round each corner form one cycle
    links_ok = True
    for v in V:
        fs = [f for f in F if v in corners(*f)]
        es = [e for e in E if v in (e[0], padd(e[0], unit(e[1])))]
        adj = {f: [] for f in fs}
        for e in es:
            a, b = E[e]; adj[a].append(b); adj[b].append(a)
        if any(len(x) != 2 for x in adj.values()): links_ok = False; continue
        seen, st = set(), [fs[0]]
        while st:
            x = st.pop()
            if x in seen: continue
            seen.add(x); st.extend(y for y in adj[x] if y not in seen)
        if len(seen) != len(fs): links_ok = False
    # adjacent faces: the angle between outward normals (36°, 72° or 108°), never 0
    n2 = None; angs = set(); coplanar = 0
    for e, (f, g) in E.items():
        nf = vscale(Fo[f], vcross(AX[f[1]], AX[f[2]])); ng = vscale(Fo[g], vcross(AX[g[1]], AX[g[2]]))
        nn = vdot(nf, nf); assert n2 is None or n2 == nn; n2 = nn
        if all(c == O for c in vcross(nf, ng)): coplanar += 1; continue
        c2 = mul((2, 0), vdot(nf, ng))          # 2 cos θ · |n|²
        for name, k in [(36, P), (72, (-1, 1)), (108, (1, -1)), (144, M)]:
            if c2 == mul(k, nn): angs.add(name); break
        else: angs.add('other')
    return {'F': len(F), 'V': len(V), 'E': len(E), 'chi': len(V) - len(E) + len(F), 'closed': closed, 'vertex_links_one_cycle': links_ok,
            'coplanar_adjacent': coplanar, 'normal_angles': sorted(angs, key=str), 'valence': sorted({sum(v in corners(*f) for f in F) for v in V})}

def lattice_member(B, v):
    """is v in the Z-row span of the 3 x 6 integer basis B? (exact rational solve, then integrality)"""
    cols = None
    for c in itertools.combinations(range(N), 3):
        m = [[Fr(B[r][j]) for r in range(3)] for j in c]
        dd = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        if dd != 0: cols = c; break
    A = [[Fr(B[r][j]) for r in range(3)] + [Fr(v[j])] for j in cols]
    for i in range(3):
        piv = next(r for r in range(i, 3) if A[r][i] != 0); A[i], A[piv] = A[piv], A[i]
        for r in range(3):
            if r != i and A[r][i] != 0:
                f = A[r][i] / A[i][i]; A[r] = [x - f * y for x, y in zip(A[r], A[i])]
    x = [A[i][3] / A[i][i] for i in range(3)]
    if any(c.denominator != 1 for c in x): return None
    w = tuple(sum(int(x[r]) * B[r][j] for r in range(3)) for j in range(N))
    return [int(c) for c in x] if w == tuple(v) else None

def face_pair_vectors(Fo):
    """λ_ab: for each face type, the vector from the face with outward +1 to the face with outward −1 (two faces per type)"""
    out = {}
    for a, b in PAIRS:
        fs = [(q, s) for (q, x, y), s in Fo.items() if (x, y) == (a, b)]
        assert len(fs) == 2 and {s for _, s in fs} == {1, -1}, (a, b, fs)
        qp = [q for q, s in fs if s == 1][0]; qm = [q for q, s in fs if s == -1][0]
        out[(a, b)] = psub(qp, qm)
    return out

def load():
    S6 = json.load(open(os.path.join(K10, 'data', 'search6.json')))
    T12 = json.load(open(os.path.join(K10, 'data', 'tile12.json')))
    return S6, T12
