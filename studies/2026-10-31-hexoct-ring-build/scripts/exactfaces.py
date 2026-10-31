# Exact outer faces of a HexOct tile as ONE solid (union of its pieces), all in rational arithmetic.
# Coordinates: lattice units (u, v, z) of tiles.py; Cartesian x = u + v/2, y = v*sqrt(3)/2, z' = z*sqrt(2/3).
# Inner products use the metric G (u.u = v.v = 1, u.v = 1/2, z.z = 2/3), so lengths squared and cosines squared are rational.
# Method (replaces the approximate merge of tilefaces.py):
#  1. each piece is convex: its facets are found exactly (every plane through three corners with all corners on one side);
#  2. facets are grouped by plane; on each plane the facets of all pieces are cut by ALL their edge lines, which gives the
#     common refinement (line arrangement) of the plane; each cell gets coefficient (+1 per facet facing +n, -1 per facet facing -n);
#     cells with coefficient 0 are glued (inner), the others are on the surface;
#  3. surface cells of the same sign are merged across shared edges into faces; a face's border is the set of cell edges used
#     once; collinear corners are dropped. Faces touching only at a corner stay separate faces.
#  4. ring test: a face can be laid with rings (rounded triangles of side h) iff all its sides run along three directions at 60
#     degrees and all its corners sit on one triangular lattice of spacing h. Then rings = area / (sqrt(3)/4 h^2), exact.
import itertools, os, sys
from fractions import Fraction as Fr
from math import gcd, isqrt
from functools import reduce

def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def add(a, b): return tuple(x + y for x, y in zip(a, b))
def mul(a, k): return tuple(x * k for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def gip(a, b):  # metric inner product
    return a[0] * b[0] + a[1] * b[1] + (a[0] * b[1] + a[1] * b[0]) / Fr(2) + Fr(2, 3) * a[2] * b[2]
def len2(a): return gip(a, a)

def prim(n):
    """primitive integer vector along n, first nonzero component positive (returns vector, sign used)"""
    den = reduce(lambda x, y: x * y // gcd(x, y), [Fr(x).denominator for x in n], 1)
    m = [int(Fr(x) * den) for x in n]; g = reduce(gcd, [abs(x) for x in m]); m = [x // g for x in m]
    s = 1 if next(x for x in m if x) > 0 else -1
    return tuple(s * x for x in m), s

def facets(X):
    """exact facets of the convex hull of points X: list of (n (outward, primitive int, in lattice coords), c, points on it)"""
    X = sorted(set(X)); out = {}
    for a, b, c in itertools.combinations(X, 3):
        n = cross(sub(b, a), sub(c, a))
        if n == (0, 0, 0): continue
        s = [dot(n, sub(x, a)) for x in X]
        if all(t <= 0 for t in s): pass
        elif all(t >= 0 for t in s): n = mul(n, -1)
        else: continue
        m, sg = prim(n); m = tuple(sg * x for x in m)   # outward primitive (prim forces a positive lead; undo it)
        key = (m, dot(m, a))
        if key not in out: out[key] = [x for x in X if dot(m, x) == key[1]]
    return [(k[0], k[1], v) for k, v in out.items()]

# ---------- 2D work inside one plane: drop the coordinate where |n| is largest ----------
def proj_axes(n):
    k = max(range(3), key=lambda i: abs(n[i])); ax = [i for i in range(3) if i != k]
    return k, ax
def cr2(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
def hull2(P):
    P = sorted(set(P))
    if len(P) < 3: return P
    lo, hi = [], []
    for p in P:
        while len(lo) >= 2 and cr2(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(hi) >= 2 and cr2(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]           # counter-clockwise, collinear points dropped
def clip(poly, L, keep):
    """convex ccw polygon cut by line L=(a,b,c): a x + b y = c; keep side sign(keep) of a x + b y - c (closed)"""
    a, b, c = L; out = []; f = lambda p: keep * (a * p[0] + b * p[1] - c)
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]; fp, fq = f(p), f(q)
        if fp >= 0: out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = fp / (fp - fq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    H = hull2(out)
    return H if len(H) >= 3 else None
def line(p, q):
    a, b = q[1] - p[1], p[0] - q[0]; c = a * p[0] + b * p[1]
    m = [a, b, c]; den = reduce(lambda x, y: x * y // gcd(x, y), [Fr(x).denominator for x in m], 1)
    m = [int(Fr(x) * den) for x in m]; g = reduce(gcd, [abs(x) for x in m if x]); m = [x // g for x in m]
    s = 1 if (m[0] > 0 or (m[0] == 0 and m[1] > 0)) else -1
    return tuple(s * x for x in m)

GLUE = set()   # pairs of pieces glued over some area, filled by union_faces
def union_faces(pieces):
    """pieces: list of corner lists (exact). Returns list of faces: dict(n (outward), c, loops [list of 3D corner loops, ccw
    about n; loop 0 the outer border], cells)"""
    planes = {}; GLUE.clear()
    for pi, X in enumerate(pieces):
        for n, c, pts in facets(X):
            m, s = prim(n)                                  # unoriented key: m, with c scaled by the same sign
            planes.setdefault((m, s * c), []).append((s, pi, pts))
    faces = []
    for (m, c), group in planes.items():
        k, ax = proj_axes(m)
        P2 = [(s, hull2([(p[ax[0]], p[ax[1]]) for p in pts]), pi) for s, pi, pts in group]
        lines = sorted({line(Q[i], Q[(i + 1) % len(Q)]) for s, Q, pi in P2 for i in range(len(Q))})
        cells = {}
        for s, Q, pi in P2:
            cur = [Q]
            for L in lines:
                nxt = []
                for C in cur:
                    for keep in (1, -1):
                        D = clip(C, L, keep)
                        if D: nxt.append(D)
                cur = nxt
            for C in cur:
                key = tuple(sorted(C)); cells.setdefault(key, [C, 0, []]); cells[key][1] += s; cells[key][2].append(pi)
        for C, w, ps in cells.values():
            if w == 0: GLUE.add(tuple(sorted(ps)))
        for sign in (1, -1):
            S = [C for C, w, ps in cells.values() if w == sign]
            assert all(abs(w) <= 1 for C, w, ps in cells.values()), 'overlapping pieces'
            if not S: continue
            # edges -> cells, merge by shared edges (union-find)
            par = list(range(len(S)))
            def fd(i):
                while par[i] != i: par[i] = par[par[i]]; i = par[i]
                return i
            emap = {}
            for i, C in enumerate(S):
                for j in range(len(C)):
                    e = frozenset((C[j], C[(j + 1) % len(C)])); emap.setdefault(e, []).append(i)
            for e, L in emap.items():
                for i in L[1:]: par[fd(i)] = fd(L[0])
            comps = {}
            for i in range(len(S)): comps.setdefault(fd(i), []).append(i)
            for idx in comps.values():
                # directed border edges (ccw cells): edge (p,q) used once among the component's cells
                de = {}
                for i in idx:
                    C = S[i]
                    for j in range(len(C)):
                        p, q = C[j], C[(j + 1) % len(C)]
                        if (q, p) in de: del de[(q, p)]
                        else: de[(p, q)] = 1
                nxt = {}
                for p, q in de: nxt.setdefault(p, []).append(q)
                loops = []; used = set()
                for p0 in sorted(nxt):
                    for q0 in nxt[p0]:
                        if (p0, q0) in used: continue
                        loop = [p0]; p, q = p0, q0; used.add((p, q))
                        while q != p0:
                            loop.append(q)
                            cand = [r for r in nxt[q] if (q, r) not in used]
                            # at a pinch corner take the sharpest left turn (keeps loops simple)
                            r = min(cand, key=lambda r: _turn(p, q, r)); used.add((q, r)); p, q = q, r
                        loops.append(loop)
                # drop collinear corners
                L2 = []
                for lp in loops:
                    lp2 = [lp[i] for i in range(len(lp)) if cr2(lp[i - 1], lp[i], lp[(i + 1) % len(lp)]) != 0]
                    L2.append(lp2)
                area2 = lambda lp: sum(lp[i][0] * lp[(i + 1) % len(lp)][1] - lp[(i + 1) % len(lp)][0] * lp[i][1] for i in range(len(lp)))
                L2.sort(key=lambda lp: -abs(area2(lp)))
                # back to 3D
                def lift(p):
                    x = [None] * 3; x[ax[0]], x[ax[1]] = p
                    x[k] = (c - m[ax[0]] * p[0] - m[ax[1]] * p[1]) / Fr(m[k]); return tuple(Fr(t) for t in x)
                # orientation: projected ccw is ccw about +m if m[k] > 0 (axes ax are (k+1, k+2) cyclic or not)
                cyc = (ax == [(k + 1) % 3, (k + 2) % 3])
                ccw_about_m = (m[k] > 0) == cyc
                n_out = m if sign > 0 else tuple(-x for x in m)
                loops3 = []
                for lp in L2:
                    lp3 = [lift(p) for p in lp]
                    # want ccw about outward normal
                    want_rev = (ccw_about_m != (sign > 0))
                    loops3.append(lp3[::-1] if want_rev else lp3)
                faces.append(dict(n=n_out, c=c * (1 if sign > 0 else -1), loops=loops3, ncells=len(idx)))
    return faces

def _turn(p, q, r):
    """angle-like key for choosing the next edge: smaller = sharper left turn"""
    import math
    a = (float(q[0] - p[0]), float(q[1] - p[1])); b = (float(r[0] - q[0]), float(r[1] - q[1]))
    ang = math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])
    return -ang

def is_sq(f):
    f = Fr(f)
    if f < 0: return None
    a, b = isqrt(f.numerator), isqrt(f.denominator)
    return Fr(a, b) if a * a == f.numerator and b * b == f.denominator else None

def ring_test(face, h=Fr(1, 2)):
    """None if the face cannot be laid with rings of side h; else dict(rings, e1, e2, coords) with the lattice of spacing h."""
    loops = face['loops']; V = [p for lp in loops for p in lp]
    E = [(lp[i], lp[(i + 1) % len(lp)]) for lp in loops for i in range(len(lp))]
    units = []
    for p, q in E:
        d = sub(q, p); L = is_sq(len2(d))
        if L is None or (L / h).denominator != 1: return None
        units.append(mul(d, h / L))
    e1 = units[0]; e2 = None
    for f in units[1:]:
        cs = gip(e1, f) / (h * h)
        if cs == Fr(1, 2): e2 = f; break
        if cs == Fr(-1, 2): e2 = add(e1, f); break
    if e2 is None: return None
    o = V[0]; A = [[gip(e1, e1), gip(e1, e2)], [gip(e2, e1), gip(e2, e2)]]; det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    def co(w):
        b1, b2 = gip(e1, w), gip(e2, w)
        a = (b1 * A[1][1] - b2 * A[0][1]) / det; b = (A[0][0] * b2 - A[1][0] * b1) / det
        if add(mul(e1, a), mul(e2, b)) != w: return None
        return (a, b)
    C = {}
    for p in V:
        ab = co(sub(p, o))
        if ab is None or ab[0].denominator != 1 or ab[1].denominator != 1: return None
        C[p] = ab
    for p, q in E:
        da, db = C[q][0] - C[p][0], C[q][1] - C[p][1]
        if not (da == 0 or db == 0 or da == -db): return None
    tri = 0
    for lp in loops:
        s = sum(C[lp[i]][0] * C[lp[(i + 1) % len(lp)]][1] - C[lp[(i + 1) % len(lp)]][0] * C[lp[i]][1] for i in range(len(lp)))
        tri += s                      # 2 x signed area in rhombus units = number of triangles (signed)
    # orientation sign of (e1, e2) relative to the loop orientation; outer loop dominates
    return dict(rings=abs(tri), e1=e1, e2=e2, coords=C, origin=o)

def face_info(face):
    lp = face['loops'][0]; n = len(lp)
    sides = [is_sq(len2(sub(lp[(i + 1) % n], lp[i]))) for i in range(n)]
    return n, sides

def volume6(faces):
    """6 x volume in lattice-coordinate units (divergence theorem on fan triangles), exact"""
    v = Fr(0)
    for f in faces:
        for lp in f['loops']:
            for i in range(1, len(lp) - 1): v += dot(lp[0], cross(lp[i], lp[i + 1]))
    return v

def piece_volume6(X):
    fs = facets(X); cen = tuple(sum(p[i] for p in X) / Fr(len(X)) for i in range(3)); v = Fr(0)
    for n, c, pts in fs:
        k, ax = proj_axes(n); Q2 = hull2([(p[ax[0]], p[ax[1]]) for p in pts])
        mp = {(p[ax[0]], p[ax[1]]): p for p in pts}; Q = [mp[q] for q in Q2]
        for i in range(1, len(Q) - 1): v += abs(dot(sub(Q[0], cen), cross(sub(Q[i], cen), sub(Q[i + 1], cen))))
    return v

def edge_multiplicity(faces):
    """every border edge of the surface, split at all corners on it, should be used by exactly two faces (in opposite directions)"""
    from collections import Counter
    segs = Counter(); V = sorted({p for f in faces for lp in f['loops'] for p in lp})
    for f in faces:
        for lp in f['loops']:
            for i in range(len(lp)):
                p, q = lp[i], lp[(i + 1) % len(lp)]; d = sub(q, p)
                on = [x for x in V if cross(sub(x, p), d) == (0, 0, 0) and 0 <= dot(sub(x, p), d) <= dot(d, d)]
                on.sort(key=lambda x: dot(sub(x, p), d))
                for a, b in zip(on, on[1:]): segs[(a, b)] += 1
    bad = [(e, c) for e, c in segs.items() if c != 1 or segs.get((e[1], e[0]), 0) != 1]
    return segs, bad
