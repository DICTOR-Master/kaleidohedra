#!/usr/bin/env python3
"""Shared exact tools for the Queens construct/deconstruct study (16 Nov 2026).

Q5 = numbers a + b*phi with rational a, b (Fractions); every sign and zero is decided exactly. The Q5 class is copied from
studies/2026-11-15-echo-shapes/scripts/echo_lib.py.
Coordinates: R^5 with coordinate sum 0, where S5 (= W(A4), the 5-cell's symmetry group) permutes coordinates. For 4-volumes the
point y = (x1, x2, x3, x4) is used. The map y -> (y, -sum y) scales 4-volume by sqrt5 (det(I + 11^T) = 5), so a 4-simplex has
volume sqrt5 * |det| / 24, exact in Q(sqrt5).
Polytopes: qhull (scipy) proposes the facets; every facet plane is then recomputed exactly and certified (its vertices exactly on
it, every other point strictly on one side). 2-faces = 2-dimensional intersections of two facets (exact rank), edges = sides of the
2-faces (exact orientation in the plane). Volume = cones from one vertex over a triangulation built from this exact lattice."""
import itertools, math
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog

class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = q5(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return q5(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = q5(o); return Q5(s.a*o.a + s.b*o.b, s.a*o.b + s.b*o.a + s.b*o.b)   # phi^2 = phi + 1
    __rmul__ = __mul__
    def conj(s): return Q5(s.a + s.b, -s.b)            # phi -> 1 - phi
    def norm(s): return s.a*s.a + s.a*s.b - s.b*s.b      # (a + b phi)(a + b phi')
    def inv(s): n = s.norm(); c = s.conj(); return Q5(c.a/n, c.b/n)
    def __truediv__(s, o): return s*q5(o).inv()
    def __rtruediv__(s, o): return q5(o)*s.inv()
    def iszero(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): o = q5(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        # sign of a + b phi = a + b/2 + (b/2) sqrt5
        x, y = s.a + s.b/2, s.b/2
        if y == 0: return (x > 0) - (x < 0)
        if x == 0: return (y > 0) - (y < 0)
        if (x > 0) == (y > 0): return 1 if x > 0 else -1
        d = x*x - 5*y*y          # compare |x| with |y| sqrt5
        return (1 if x > 0 else -1) if d > 0 else (1 if y > 0 else -1)
    def __lt__(s, o): return (s - o).sign() < 0
    def mpf(s): return mp.mpf(s.a.numerator)/s.a.denominator + mp.mpf(s.b.numerator)/s.b.denominator*mp.phi
    def __float__(s): return float(s.a) + float(s.b)*(1 + 5**0.5)/2
    def key(s): return (s.a, s.b)
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f'({s.a}{"+" if s.b >= 0 else "-"}{abs(s.b)}phi)'

def q5(x): return x if isinstance(x, Q5) else Q5(x, 0)
PHI = Q5(0, 1); IPHI = Q5(-1, 1)          # 1/phi = phi - 1
SQ5 = Q5(-1, 2)                          # sqrt5 = 2 phi - 1
ZERO = Q5(0)
SQRT5_F = 5 ** 0.5
def dot(u, v):
    s = Q5()
    for x, y in zip(u, v): s = s + x*y
    return s
def vadd(u, v): return tuple(x + y for x, y in zip(u, v))
def vsub(u, v): return tuple(x - y for x, y in zip(u, v))
def vscale(c, u): return tuple(c*x for x in u)
def vkey(u): return tuple(x.key() for x in u)
def vneg(u): return tuple(-x for x in u)
def flt(u): return np.array([float(x) for x in u])
def uniq(pts):
    seen = {}
    for p in pts: seen.setdefault(vkey(p), p)
    return list(seen.values())
def to4(x): return tuple(x[:4])
def to5(y): return tuple(y) + (-sum(y, Q5()),)

def det(M):
    M = [list(r) for r in M]; n = len(M); d = Q5(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if not M[i][c].iszero()), None)
        if piv is None: return Q5(0)
        if piv != c: M[c], M[piv] = M[piv], M[c]; d = -d
        d = d*M[c][c]; inv = M[c][c].inv()
        for i in range(c + 1, n):
            if not M[i][c].iszero():
                f = M[i][c]*inv; M[i] = [a - f*b for a, b in zip(M[i], M[c])]
    return d
def rank(rows):
    M = [list(r) for r in rows]
    if not M: return 0
    r = 0
    for c in range(len(M[0])):
        piv = next((i for i in range(r, len(M)) if not M[i][c].iszero()), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; inv = M[r][c].inv()
        for i in range(len(M)):
            if i != r and not M[i][c].iszero():
                f = M[i][c]*inv; M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r
def solve(A, b):
    """exact solution of a square nonsingular system"""
    n = len(A); M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = next(i for i in range(c, n) if not M[i][c].iszero())
        M[c], M[piv] = M[piv], M[c]; inv = M[c][c].inv(); M[c] = [x*inv for x in M[c]]
        for i in range(n):
            if i != c and not M[i][c].iszero():
                f = M[i][c]; M[i] = [a - f*b for a, b in zip(M[i], M[c])]
    return tuple(M[i][n] for i in range(n))
def cofactor_normal(rows):
    """vector orthogonal to the n-1 rows (length n), by signed maximal minors"""
    n = len(rows[0]); out = []
    for j in range(n):
        m = [[r[k] for k in range(n) if k != j] for r in rows]
        out.append(det(m) if j % 2 == 0 else -det(m))
    return tuple(out)
def affdim(pts):
    if len(pts) <= 1: return 0
    return rank([vsub(p, pts[0]) for p in pts[1:]])
def parallel(u, v):
    """exact: u and v (nonzero) are parallel"""
    i = next(k for k in range(len(u)) if not u[k].iszero())
    if v[i].iszero(): return False
    c = v[i]/u[i]
    return all((v[k] - c*u[k]).iszero() for k in range(len(u)))
def sqd(u, v): w = vsub(u, v); return dot(w, w)

class Poly:
    """convex hull of exact points in R^4 (y coordinates); exact facets, lattice, volume"""
    def __init__(s, pts, name='', lattice=True):
        s.name = name; pts = uniq(pts); s.allP = pts
        F = np.array([flt(p) for p in pts]); h = ConvexHull(F)
        groups = {}
        for eq in h.equations: groups.setdefault(tuple(np.round(eq, 6) + 0.0), eq)
        facets, seen = [], set()
        for eq in groups.values():
            idx = [i for i in range(len(pts)) if abs(eq[:4] @ F[i] + eq[4]) < 1e-7]
            if frozenset(idx) in seen: continue
            seen.add(frozenset(idx))
            base = [idx[0]]
            for i in idx[1:]:
                if affdim([pts[j] for j in base + [i]]) == len(base): base.append(i)
                if len(base) == 4: break
            assert len(base) == 4, 'facet not 3-dimensional'
            n = cofactor_normal([vsub(pts[j], pts[base[0]]) for j in base[1:]]); d = dot(n, pts[base[0]])
            vals = [dot(n, p) - d for p in pts]
            on = [i for i, v in enumerate(vals) if v.iszero()]
            assert on == idx, 'exact facet set differs from float'
            sg = {v.sign() for v in vals if not v.iszero()}; assert len(sg) == 1, 'facet plane not supporting'
            if sg == {1}: n = vneg(n); d = -d
            facets.append((on, n, d))
        # keep only extreme points (vertices): a point is a vertex iff the facets through it meet only in it
        verts = []
        for i in range(len(pts)):
            through = [set(f[0]) for f in facets if i in f[0]]
            if len(through) >= 4 and set.intersection(*through) == {i}: verts.append(i)
        remap = {i: k for k, i in enumerate(verts)}
        s.P = [pts[i] for i in verts]
        s.facets = [([remap[i] for i in on if i in remap], n, d) for on, n, d in facets]
        s.float_vol = h.volume*SQRT5_F
        if lattice: s._lattice()
    def _lattice(s):
        fac = [frozenset(f[0]) for f in s.facets]
        two = {}
        bits = [sum(1 << i for i in f) for f in fac]
        for a in range(len(fac)):
            for b in range(a + 1, len(fac)):
                c = bits[a] & bits[b]
                if bin(c).count('1') >= 3:
                    cs = frozenset(i for i in fac[a] if c >> i & 1)
                    if cs not in two and affdim([s.P[i] for i in cs]) == 2: two[cs] = (a, b)
                    elif cs in two: pass
        s.two = two
        s.gedges = {g: s._polygon_edges(sorted(g)) for g in two}
        s.edges = set().union(*s.gedges.values()) if two else set()
        s.fvec = (len(s.P), len(s.edges), len(two), len(fac))
        s.euler = s.fvec[0] - s.fvec[1] + s.fvec[2] - s.fvec[3]
    def _polygon_edges(s, g):
        if len(g) == 3: return {frozenset(e) for e in itertools.combinations(g, 2)}
        u0 = s.P[g[0]]; e1 = vsub(s.P[g[1]], u0)
        e2 = next(vsub(s.P[k], u0) for k in g[2:] if affdim([u0, s.P[g[1]], s.P[k]]) == 2)
        G = [[dot(e1, e1), dot(e1, e2)], [dot(e1, e2), dot(e2, e2)]]
        c2 = {k: solve(G, [dot(e1, vsub(s.P[k], u0)), dot(e2, vsub(s.P[k], u0))]) for k in g}
        out = set()
        for i, j in itertools.combinations(g, 2):
            a, b = c2[i], c2[j]; sg = set()
            for k in g:
                if k in (i, j): continue
                c = c2[k]; o = (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0]); sg.add(o.sign())
            if len(sg) == 1 and 0 not in sg: out.add(frozenset((i, j)))
        assert len(out) == len(g), 'polygon edge count'
        return out
    def volume(s):
        a = 0; A = s.P[a]; tot = Q5()
        fac_two = {}
        for g, (fa, fb) in s.two.items(): fac_two.setdefault(fa, []).append(g); fac_two.setdefault(fb, []).append(g)
        for fi, (on, n, d) in enumerate(s.facets):
            if a in on: continue
            f0 = on[0]
            for g in fac_two[fi]:
                if f0 in g: continue
                g0 = min(g)
                for e in s.gedges[g]:
                    if g0 in e: continue
                    e0, e1 = sorted(e)
                    M = [vsub(s.P[k], A) for k in (f0, g0, e0, e1)]
                    v = det(M); tot = tot + (v if v.sign() >= 0 else -v)
        return tot*SQ5/24
    def cells(s):
        """per facet: (vertex count, sorted 2-face sizes)"""
        fac_two = {}
        for g, (fa, fb) in s.two.items(): fac_two.setdefault(fa, []).append(len(g)); fac_two.setdefault(fb, []).append(len(g))
        return [(len(on), tuple(sorted(fac_two[fi]))) for fi, (on, n, d) in enumerate(s.facets)]
    def contains(s, q):
        return all((dot(n, q) - d).sign() <= 0 for on, n, d in s.facets)
    def halfspaces(s): return [(n, d) for on, n, d in s.facets]

CELLNAME = {(4, (3, 3, 3, 3)): 'tetrahedron', (6, (3,)*8): 'octahedron', (12, (3,)*20): 'icosahedron',
            (20, (5,)*12): 'dodecahedron', (12, (3,)*4 + (6,)*4): 'truncated tetrahedron', (12, (3,)*8 + (4,)*6): 'cuboctahedron',
            (6, (3, 3, 4, 4, 4)): 'triangular prism', (10, (3,)*10 + (5, 5)): 'pentagonal antiprism',
            (6, (3,)*4 + (4,)): 'square pyramid', (5, (3,)*6): 'triangular bipyramid', (6, (3,)*5 + (5,)): 'pentagonal pyramid',
            (8, (4,)*6): 'cube', (12, (4,)*6 + (6,)*2): 'hexagonal prism', (10, (4,)*5 + (5, 5)): 'pentagonal prism',
            (13, (3,)*20): 'icosahedral pyramid'}
def cell_census(poly):
    c = {}
    for v, f in poly.cells():
        nm = CELLNAME.get((v, f), f'{v}-vertex cell with faces {dict(sorted({k: f.count(k) for k in set(f)}.items()))}')
        c[nm] = c.get(nm, 0) + 1
    return dict(sorted(c.items()))

def hs_intersect(H, tol=1e-9):
    """exact polytope {y : n.y <= d for (n, d) in H}; None if it has no interior"""
    A = np.array([flt(n) for n, d in H]); b = np.array([float(d) for n, d in H]); nr = np.linalg.norm(A, axis=1)
    res = linprog(c=[0, 0, 0, 0, -1], A_ub=np.hstack([A, nr[:, None]]), b_ub=b, bounds=[(None, None)]*4 + [(0, 10)], method='highs')
    if res.status != 0 or res.x[4] < 1e-7: return None
    hs = HalfspaceIntersection(np.hstack([A, -b[:, None]]), res.x[:4])
    verts = []
    for v in hs.intersections:
        act = [i for i in range(len(H)) if abs(A[i] @ v - b[i]) < 1e-7*max(1, nr[i])]
        sel = []
        for i in act:
            if np.linalg.matrix_rank(A[sel + [i]], tol=1e-9) == len(sel) + 1: sel.append(i)
            if len(sel) == 4: break
        assert len(sel) == 4
        y = solve([H[i][0] for i in sel], [H[i][1] for i in sel])
        assert all((dot(n, y) - d).sign() <= 0 for n, d in H), 'exact vertex violates a halfspace'
        verts.append(y)
    return Poly(uniq(verts))

def closure(seed, cap=10000):
    """closure of a point set under reflection in its own members (exact)"""
    S = {vkey(p): p for p in seed}; frontier = list(S.values())
    def refl(a, b): return vsub(b, vscale(2*dot(a, b)/dot(a, a), a))
    while frontier:
        old = list(S.values()); new = []
        pairs = [(a, b) for a in old for b in frontier] + [(a, b) for a in frontier for b in old]
        for a, b in pairs:
            c = refl(a, b)
            if vkey(c) not in S: S[vkey(c)] = c; new.append(c)
            if len(S) > cap: return None
        frontier = new
    return list(S.values())

def build_600():
    """600-cell P in sum-zero R^5: closure of X = perms (phi^2,phi^2,phi^2,phi,0) minus centre (the golden A4 study)"""
    P2 = PHI*PHI
    def cen(v): m = sum(v, Q5())/5; return tuple(x - m for x in v)
    X = uniq([cen(t) for t in itertools.permutations((P2, P2, P2, PHI, Q5(0)))])
    Y = uniq([cen(t) for t in itertools.permutations((P2, P2, Q5(1), Q5(1), Q5(0)))])
    P = closure(X, cap=200)
    return P, X, Y

def perm_rep(P, maps):
    """permutation of the indices of P for each map (a function on exact points)"""
    idx = {vkey(p): i for i, p in enumerate(P)}
    return [np.array([idx[vkey(m(p))] for p in P]) for m in maps]

def group_closure(gens, order_cap=20000):
    n = len(gens[0]); e = np.arange(n); seen = {e.tobytes(): e}; frontier = [e]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                k = h[g]; kb = k.tobytes()
                if kb not in seen: seen[kb] = k; new.append(k)
        frontier = new
        if len(seen) > order_cap: raise RuntimeError('group too large')
    return np.array(list(seen.values()))

def canon_set(G, S):
    """canonical form of a vertex-index set under the permutation group G (rows)"""
    im = np.sort(G[:, sorted(S)], axis=1)
    order = np.lexsort(im.T[::-1]); return tuple(im[order[0]])

def dist_invariant(pts5):
    return tuple(sorted(sqd(a, b).key() for a, b in itertools.combinations(pts5, 2)))

def orbit_pattern(x):
    """sorted coordinates (descending) and block multiplicities; an S5 orbit's hull type follows the blocks (Wythoff rings)"""
    xs = sorted(x, key=lambda q: float(q), reverse=True); blocks = [1]
    for a, b in zip(xs, xs[1:]):
        if (a - b).iszero(): blocks[-1] += 1
        else: blocks.append(1)
    gaps = [a - b for a, b in zip(xs, xs[1:]) if not (a - b).iszero()]
    return xs, blocks, gaps
A4NAME = {(1, 4): '5-cell (simplex)', (4, 1): '5-cell (simplex)', (2, 3): 'rectified 5-cell', (3, 2): 'rectified 5-cell',
          (1, 1, 3): 'truncated 5-cell', (3, 1, 1): 'truncated 5-cell', (1, 3, 1): 'runcinated (expanded) 5-cell',
          (1, 2, 2): 'cantellated 5-cell', (2, 2, 1): 'cantellated 5-cell', (2, 1, 2): 'bitruncated 5-cell',
          (1, 1, 1, 2): 'cantitruncated 5-cell', (2, 1, 1, 1): 'cantitruncated 5-cell', (1, 2, 1, 1): 'runcitruncated 5-cell',
          (1, 1, 2, 1): 'runcitruncated 5-cell', (1, 1, 1, 1, 1): 'omnitruncated 5-cell (permutohedron)'}

class Checks:
    def __init__(s): s.n = 0; s.fails = []
    def __call__(s, c, msg):
        s.n += 1; print(('CHECK ok   ' if c else 'CHECK FAIL ') + msg, flush=True)
        if not c: s.fails.append(msg)
        return c
    def final(s):
        print(f'{s.n} checks, {len(s.fails)} failed')
        for f in s.fails: print('  failed:', f)
        print('FINAL ok' if not s.fails else 'FINAL FAIL')

def cap(outer, n, d):
    """outer ∩ {n.y >= d}, built exactly from outer's corners beyond the plane and its edge crossings; None if no interior"""
    f = [dot(n, p) - d for p in outer.P]
    if not any(v.sign() > 0 for v in f): return None
    pts = [p for p, v in zip(outer.P, f) if v.sign() >= 0]
    for e in outer.edges:
        a, b = tuple(e)
        if f[a].sign()*f[b].sign() < 0:
            t = f[a]/(f[a] - f[b]); pts.append(vadd(outer.P[a], vscale(t, vsub(outer.P[b], outer.P[a]))))
    pts = uniq(pts)
    if affdim(pts[:min(len(pts), 40)]) < 4 and affdim(pts) < 4: return None
    return Poly(pts)

def weyl_perms(P5):
    """W(H4) (order 14400) as permutations of the 600-cell corners, generated by the reflections in the 60 mirrors"""
    Pk = {vkey(p): i for i, p in enumerate(P5)}; gens = []
    for m in P5:
        mm = dot(m, m); gens.append(np.array([Pk[vkey(vsub(p, vscale(2*dot(m, p)/mm, m)))] for p in P5]))
    return group_closure(gens)
def same_orbit(G, S, T): return canon_set(G, S) == canon_set(G, T)
def vol_simplex(pts4):
    v = det([vsub(p, pts4[0]) for p in pts4[1:]]); return (v if v.sign() >= 0 else -v)*SQ5/24
