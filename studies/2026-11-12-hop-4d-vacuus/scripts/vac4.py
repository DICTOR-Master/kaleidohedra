"""vac4.py - one engine for the 4D Vacuus of ANY 4D polytope (DICTO 11 Nov 2026: "c the permutahedron 4D vacuus"; study 2026-11-12).
A 4D polytope is given by facets n_f . x <= h_f with EXACT coefficients (R5 = a + b sqrt5, gmpy2 rationals; integers are b = 0).
  - enumerate(): vertices + incidences from a float halfspace intersection (tolerance tol, relative); f-vector and Euler
    V - E + F2 - F3 = 0; 2-faces = facet pairs whose common corners span a plane (affine rank 2). NUMERICAL (gap printed).
  - nu_line(): the central 3D slice through c(t) = c0 + t u carrying the 2-face (f, g) has normal
        nu = (h_g - n_g.c) n_f - (h_f - n_f.c) n_g = A + t B   (EXACT).
  - count_exact(): distinct central slices at an exact height t, by exact equality of normalised normals.
  - special_heights(): pairs of 2-faces whose slices coincide at some t: float prefilter on the six 2x2 minors (quadratics in t), each
    candidate CONFIRMED EXACTLY by the gcd of the six minor polynomials over Q(sqrt5). Heights: exact R5 (linear gcd or a square
    discriminant) or ('q', c0, c1, sign) for a root of an irreducible monic quadratic t^2 + c1 t + c0 (float value attached).
  - slice_shape(): the 3D slice through c with normal nu (float; tolerance, Euler checked): corners, edges, faces by sides, which facets
    give faces, carried 2-faces (faces given by two facets).
  - classes(): slices grouped into orbits under a list of 4x4 symmetries (float, normals rounded to 1e-7)."""
import itertools, os
from collections import Counter, defaultdict
import numpy as np, gmpy2
from gmpy2 import mpq
from scipy.spatial import HalfspaceIntersection, cKDTree
from scipy.sparse import csr_matrix

S5 = 5 ** .5
DEBUG = False
MPQ = type(mpq(0))
class R5:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a = a if isinstance(a, MPQ) else mpq(a); s.b = b if isinstance(b, MPQ) else mpq(b)
    def __add__(s, o): return R5(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return R5(s.a - o.a, s.b - o.b)
    def __neg__(s): return R5(-s.a, -s.b)
    def __mul__(s, o): return R5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return R5(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * o.inv()
    def iszero(s): return s.a == 0 and s.b == 0
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) * (1 if a * a > 5 * b * b else -1)
    def __eq__(s, o): return isinstance(o, R5) and s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * S5
    def __repr__(s): return f'{s.a}+{s.b}r5'
ZERO, ONE = R5(0), R5(1)
def dot(u, v):
    s = ZERO
    for x, y in zip(u, v): s = s + x * y
    return s
def sqrt_r5(d):
    """exact square root of d in Q(sqrt5) if it exists, else None (x + y sqrt5)^2 = a + b sqrt5."""
    a, b = d.a, d.b
    if d.sign() < 0: return None
    if b == 0:
        if gmpy2.is_square(a.numerator) and gmpy2.is_square(a.denominator): return R5(mpq(gmpy2.isqrt(a.numerator), gmpy2.isqrt(a.denominator)))
        a5 = a / 5                                            # a = 5 y^2
        if gmpy2.is_square(a5.numerator) and gmpy2.is_square(a5.denominator): return R5(0, mpq(gmpy2.isqrt(a5.numerator), gmpy2.isqrt(a5.denominator)))
        return None
    n = a * a - 5 * b * b                                     # x^2 = (a +- sqrt(n)) / 2
    if n < 0 or not (gmpy2.is_square(n.numerator) and gmpy2.is_square(n.denominator)): return None
    r = mpq(gmpy2.isqrt(n.numerator), gmpy2.isqrt(n.denominator))
    for x2 in ((a + r) / 2, (a - r) / 2):
        if x2 > 0 and gmpy2.is_square(x2.numerator) and gmpy2.is_square(x2.denominator):
            x = mpq(gmpy2.isqrt(x2.numerator), gmpy2.isqrt(x2.denominator)); y = b / (2 * x); c = R5(x, y)
            if c * c == d: return c if c.sign() >= 0 else -c
    return None

# ---------- polynomials over Q(sqrt5), coefficient lists low -> high ----------
def pstrip(p):
    p = list(p)
    while p and p[-1].iszero(): p.pop()
    return p
def pmod(p, q):
    p = pstrip(p); q = pstrip(q); lq = q[-1].inv()
    while p and len(p) >= len(q):
        c = p[-1] * lq; sh = len(p) - len(q)
        for i, x in enumerate(q): p[i + sh] = p[i + sh] - c * x
        assert p[-1].iszero()                                 # leading term cancels exactly
        p = pstrip(p)
    return p
def pgcd(polys):
    g = []
    for p in polys:
        p = pstrip(p)
        if not p: continue
        if not g: g = p; continue
        a, b = g, p
        while b: a, b = b, pmod(a, b)
        g = a
        if len(g) == 1: return [ONE]
    if not g: return None                                     # all zero: coincide at every t
    li = g[-1].inv(); return [x * li for x in g]

def rank_r5(rows):
    """exact rank of a list of R5 vectors (Gaussian elimination over Q(sqrt5))."""
    M = [list(r) for r in rows]; r = 0
    for c in range(len(M[0]) if M else 0):
        pr = next((i for i in range(r, len(M)) if not M[i][c].iszero()), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]; li = M[r][c].inv()
        for i in range(r + 1, len(M)):
            if not M[i][c].iszero():
                f = M[i][c] * li; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r

def dedupe(P, tol):
    t = cKDTree(P); seen = -np.ones(len(P), int); out = []
    for i in range(len(P)):
        if seen[i] < 0:
            js = t.query_ball_point(P[i], tol); seen[js] = len(out); out.append(P[js].mean(0))
    return np.array(out)

class Poly4:
    def __init__(s, N, H, labels=None):
        s.N, s.H = N, H; s.Nf = np.array([[x.f() for x in n] for n in N]); s.Hf = np.array([h.f() for h in H])
        s.labels = labels if labels is not None else ['f'] * len(N)
    def enumerate(s, interior, tol=1e-9):
        sc = max(1.0, np.abs(s.Hf).max(), np.abs(s.Nf).max())
        hs = HalfspaceIntersection(np.hstack([s.Nf, -s.Hf[:, None]]), np.asarray(interior, float))
        ext = np.abs(hs.intersections).max(); s0 = max(1.0, float(np.median(np.abs(s.Hf))))   # s0 = size of the solid near its cells
        P = dedupe(hs.intersections, float(os.environ.get("VAC4_MERGE", "1e-9")) * s0)
        pn = np.maximum(s0, np.linalg.norm(P, axis=1))                    # per-corner scale (the far cap corners are large)
        R = np.abs(s.Nf @ P.T - s.Hf[:, None]) / (np.linalg.norm(s.Nf, axis=1)[:, None] * pn[None, :])
        inc = R < tol; s.gap = float(R[~inc].min()); s.maxres = float(R[inc].max())
        s.P, s.inc = P, inc
        I = csr_matrix(inc.astype(np.int32))
        # facets (real ones span 3D), 2-faces (facet pairs, common corners span a plane), edges (vertex pairs, shared normals rank 3)
        def arank(pts): return np.linalg.matrix_rank(pts - pts[0], tol=1e-8 * max(s0, np.abs(pts).max())) if len(pts) else -1
        s.facets = [f for f in range(len(s.N)) if inc[f].sum() >= 4 and arank(P[inc[f]]) == 3]
        C = (I @ I.T).tocoo(); s.ridges = []
        for f, g, c in zip(C.row, C.col, C.data):
            if f < g and c >= 3 and arank(P[inc[f] & inc[g]]) == 2: s.ridges.append((int(f), int(g)))
        D = (I.T @ I).tocoo(); ne = 0
        for u, v, c in zip(D.row, D.col, D.data):
            if u < v and c >= 3:
                sh = inc[:, u] & inc[:, v]
                if np.linalg.matrix_rank(s.Nf[sh] / np.linalg.norm(s.Nf[sh], axis=1)[:, None], tol=1e-7) == 3: ne += 1
        s.fvec = (len(P), ne, len(s.ridges), len(s.facets))
        s.euler = s.fvec[0] - s.fvec[1] + s.fvec[2] - s.fvec[3]
        return s
    # ---- central slices ----
    def nu_line(s, ridges, c0, u):
        """exact A, B (lists of R5 4-tuples) with nu(t) = A + t B for each 2-face (f, g)."""
        A, B = [], []
        for f, g in ridges:
            nf, ng = s.N[f], s.N[g]
            af = s.H[f] - dot(nf, c0); ag = s.H[g] - dot(ng, c0); uf = dot(nf, u); ug = dot(ng, u)
            A.append(tuple(ag * x - af * y for x, y in zip(nf, ng)))
            B.append(tuple(uf * y - ug * x for x, y in zip(nf, ng)))            # d/dt: -(n_g.u) n_f + (n_f.u) n_g
        return A, B
    @staticmethod
    def canon(v):
        for x in v:
            if not x.iszero():
                li = x.inv(); return tuple(y * li for y in v)
        return None
    def count_exact(s, A, B, t):
        groups = defaultdict(list); through = []
        for q, (a, b) in enumerate(zip(A, B)):
            k = Poly4.canon(tuple(x + t * y for x, y in zip(a, b)))
            (through.append(q) if k is None else groups[k].append(q))
        return groups, through

def minors_float(A1, B1, A2, B2):
    """six 2x2 minors of (A1 + t B1, A2 + t B2) as quadratics (W, 6, 3)."""
    out = []
    for p, q in itertools.combinations(range(4), 2):
        c0 = A1[p] * A2[:, q] - A1[q] * A2[:, p]
        c1 = A1[p] * B2[:, q] + B1[p] * A2[:, q] - A1[q] * B2[:, p] - B1[q] * A2[:, p]
        c2 = B1[p] * B2[:, q] - B1[q] * B2[:, p]
        out.append(np.stack([c0, c1, c2], -1))
    return np.stack(out, 1)

def minors_exact(a1, b1, a2, b2):
    out = []
    for p, q in itertools.combinations(range(4), 2):
        out.append([a1[p] * a2[q] - a1[q] * a2[p], a1[p] * b2[q] + b1[p] * a2[q] - a1[q] * b2[p] - b1[q] * a2[p], b1[p] * b2[q] - b1[q] * b2[p]])
    return out

def special_heights(A, B, progress=None, ftol=1e-7):
    """returns (always_pairs, {height_key: (float t, [pairs])}, stats). height_key: R5 or ('q', c0, c1, sign)."""
    W = len(A); Af = np.array([[x.f() for x in a] for a in A]); Bf = np.array([[x.f() for x in b] for b in B])
    always, heights = [], {}; n_cand = n_conf = n_rej = 0; min_rej = np.inf
    for w1 in range(W - 1):
        if progress and w1 % max(1, W // 20) == 0: progress(w1 / W)
        A2, B2 = Af[w1 + 1:], Bf[w1 + 1:]
        M = minors_float(Af[w1], Bf[w1], A2, B2)                                   # (m, 6, 3)
        scl = (np.abs(Af[w1]).sum() + np.abs(Bf[w1]).sum()) * (np.abs(A2).sum(1) + np.abs(B2).sum(1))
        Mn = M / scl[:, None, None]
        alw = np.abs(Mn).max((1, 2)) < 1e-9          # loose: every always-pair is confirmed exactly (gcd = 0)
        cand = []
        for j in np.where(alw)[0]: cand.append((w1, w1 + 1 + int(j), None))
        best = np.abs(Mn).max(2).argmax(1); P = Mn[np.arange(len(Mn)), best]          # strongest minor
        c0, c1, c2 = P[:, 0], P[:, 1], P[:, 2]
        roots = []
        quad = np.abs(c2) > 1e-9 * np.abs(P).max(1)
        disc = c1 * c1 - 4 * c2 * c0; sq = np.sqrt(np.maximum(disc, 0))
        with np.errstate(divide='ignore', invalid='ignore'):
            r1 = np.where(quad, (-c1 + sq) / (2 * c2), np.where(np.abs(c1) > 1e-12, -c0 / c1, np.nan))
            r2 = np.where(quad, (-c1 - sq) / (2 * c2), np.nan)
            ok = ~alw & (~quad | (disc >= -1e-9 * (c1 * c1 + np.abs(4 * c2 * c0))))
        for r in (r1, r2):
            good = ok & np.isfinite(r)
            if not good.any(): continue
            rr = np.where(good, r, 0.0)
            n1 = Af[w1][None, :] + rr[:, None] * Bf[w1][None, :]; n2 = A2 + rr[:, None] * B2
            val = (Mn[:, :, 0] + Mn[:, :, 1] * rr[:, None] + Mn[:, :, 2] * (rr * rr)[:, None]) * scl[:, None]
            res = np.abs(val).max(1) / (np.linalg.norm(n1, axis=1) * np.linalg.norm(n2, axis=1) + 1e-300)
            hit = good & (res < ftol)
            miss = good & ~hit
            if miss.any(): min_rej = min(min_rej, float(res[miss].min()))
            for j in np.where(hit)[0]: cand.append((w1, w1 + 1 + int(j), float(r[j])))
        seen = set()
        for (i, j, tf) in cand:
            if (i, j) in seen: continue
            seen.add((i, j)); n_cand += 1
            g = pgcd(minors_exact(A[i], B[i], A[j], B[j]))
            if g is None: always.append((i, j)); n_conf += 1; continue
            if len(g) == 1: n_rej += 1; continue
            n_conf += 1
            if len(g) == 2:
                rt = -g[0]; heights.setdefault(rt, (rt.f(), []))[1].append((i, j))
            else:
                c0e, c1e = g[0], g[1]; d = c1e * c1e - R5(4) * c0e
                if d.sign() < 0: continue                                          # no real height
                sd = sqrt_r5(d)
                if sd is not None:
                    for sgn in (1, -1):
                        rt = (-c1e + (sd if sgn > 0 else -sd)) / R5(2); heights.setdefault(rt, (rt.f(), []))[1].append((i, j))
                else:
                    for sgn in (1, -1):
                        key = ('q', c0e, c1e, sgn); tf2 = (-c1e.f() + sgn * d.f() ** .5) / 2
                        heights.setdefault(key, (tf2, []))[1].append((i, j))
    return always, heights, dict(candidates=n_cand, confirmed=n_conf, rejected_exactly=n_rej, min_float_rejected=min_rej)

def uf_count(W, pairs):
    par = list(range(W))
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i, j in pairs:
        a, b = find(i), find(j)
        if a != b: par[a] = b
    lab = [find(x) for x in range(W)]
    return len(set(lab)), lab

def slice_shape(poly, c, nu, tol=1e-10, ridge_set=None):
    """3D slice of the polytope through c with normal nu (floats). Returns a dict, or None if c not strictly inside."""
    nu = np.asarray(nu, float); nu = nu / np.linalg.norm(nu); c = np.asarray(c, float)
    Bm = np.linalg.svd(nu[None, :])[2][1:]                                       # 3 x 4 orthonormal basis of nu-perp
    Ns = poly.Nf @ Bm.T; hs_ = poly.Hf - poly.Nf @ c
    if hs_.min() <= 1e-12 * max(1, np.abs(poly.Hf).max()): return None
    keep = np.linalg.norm(Ns, axis=1) > 1e-12                                   # facets parallel to the slice cannot be faces
    hs = HalfspaceIntersection(np.hstack([Ns[keep], -hs_[keep][:, None]]), np.zeros(3))
    ext = max(1, np.abs(hs.intersections).max())
    P = dedupe(hs.intersections, 1e-11 * ext)
    idx = np.where(keep)[0]
    R = np.abs(Ns[keep] @ P.T - hs_[keep][:, None]) / (np.linalg.norm(Ns[keep], axis=1)[:, None] * ext)
    inc = R < tol; gap = float(R[~inc].min()) if (~inc).any() else np.inf; maxres = float(R[inc].max())
    faces = {}
    for r in range(len(idx)):
        vs = np.where(inc[r])[0]
        if len(vs) >= 3 and np.linalg.matrix_rank(P[vs] - P[vs[0]], tol=1e-7 * ext) == 2:
            faces.setdefault(tuple(vs), []).append(int(idx[r]))
    F = len(faces); fl_ = list(faces)
    vf = defaultdict(set)
    for fi, vs in enumerate(fl_):
        for v in vs: vf[v].add(fi)
    E = sum(1 for u, v in itertools.combinations(range(len(P)), 2) if len(vf[u] & vf[v]) >= 2)
    sizes = Counter(len(vs) for vs in fl_)
    carried = [tuple(sorted(fs)) for fs in faces.values() if len(fs) == 2]
    deg = Counter(len(vf[v]) for v in range(len(P)))
    return dict(V=len(P), E=E, F=F, euler=len(P) - E + F, sizes=dict(sorted(sizes.items())), deg=dict(sorted(deg.items())),
                facets_met=sorted({f for fs in faces.values() for f in fs}), carried=carried, multi=[fs for fs in faces.values() if len(fs) > 2],
                gap=gap, maxres=maxres)

def class_key(nu, Gm, decimals=7):
    """Gm: the symmetries as matrices acting on NORMALS (M^-T of the point map)."""
    nu = np.asarray(nu, float); best = None
    for M in Gm:
        w = M @ nu; w = w / np.linalg.norm(w)
        j = np.argmax(np.abs(w) > 1e-9); w = w if w[j] > 0 else -w
        k = tuple(np.round(w, decimals) + 0.0)
        if best is None or k < best: best = k
    return best

def solve_r5(M, rhs):
    """exact solution of a square R5 system (None if singular)."""
    n = len(M); A = [list(M[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        pr = next((i for i in range(c, n) if not A[i][c].iszero()), None)
        if pr is None: return None
        A[c], A[pr] = A[pr], A[c]; li = A[c][c].inv(); A[c] = [x * li for x in A[c]]
        for i in range(n):
            if i != c and not A[i][c].iszero():
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [A[i][n] for i in range(n)]

def slice_shape_exact(poly, c, nu, cf, nuf, band=1e-4, vband=1e-2):
    """EXACT 3D slice through exact c with exact normal nu: float slice proposes corners; every corner is recomputed exactly from
    H and three facets among those within `band` (relative) of it, all such triples tried, kept if exactly feasible for every facet
    within `vband` of the exact corner (facets outside vband are satisfied with a float margin >= vband), and only if it is the corner
    the float slice proposed (within 1e-4 of the size; float halfspace corners are only good to ~1e-8); points on edges (face planes of rank 2) dropped; incidences exact; faces = facets with >= 3 exact corners
    spanning a plane; Euler exact. Returns the same dict as slice_shape plus 'exact': True."""
    nuf = np.asarray(nuf, float); nn = nuf / np.linalg.norm(nuf); cf = np.asarray(cf, float)
    Bm = np.linalg.svd(nn[None, :])[2][1:]
    Ns = poly.Nf @ Bm.T; hs_ = poly.Hf - poly.Nf @ cf
    keep = np.linalg.norm(Ns, axis=1) > 1e-12
    hs = HalfspaceIntersection(np.hstack([Ns[keep], -hs_[keep][:, None]]), np.zeros(3))
    ext = max(1, np.abs(hs.intersections).max())
    P = dedupe(hs.intersections, 1e-9 * ext)
    idx = np.where(keep)[0]
    Rel = np.abs(Ns[keep] @ P.T - hs_[keep][:, None]) / (np.linalg.norm(Ns[keep], axis=1)[:, None] * ext)
    Hc = dot(nu, c); verts = {}; minband = np.inf; ntri = 0
    H = list(poly.H)
    for v in range(len(P)):
        T = [int(idx[r]) for r in np.where(Rel[:, v] < band)[0]]; TV = [int(idx[r]) for r in np.where(Rel[:, v] < vband)[0]]
        out = Rel[:, v][Rel[:, v] >= vband]; minband = min(minband, float(out.min()) if len(out) else np.inf)
        for tri in itertools.combinations(T, 3):
            x = solve_r5([nu] + [poly.N[f] for f in tri], [Hc] + [H[f] for f in tri]); ntri += 1
            if x is None: continue
            key = tuple(x)
            if key in verts: continue
            xf = np.array([y.f() for y in x])
            rx = (poly.Nf @ xf - poly.Hf) / (np.linalg.norm(poly.Nf, axis=1) * ext)
            if DEBUG and v < 2: print('    dbg v', v, 'T', T, 'tri', tri, 'dist', np.linalg.norm(xf - (cf + Bm.T @ P[v])) / ext, 'rxmax', rx.max(), 'argmax', int(rx.argmax()), 'cap', poly.Hf[-1], H[-1].f(), 'xf', xf.round(4))
            if np.linalg.norm(xf - (cf + Bm.T @ P[v])) > 1e-4 * ext: continue        # another crossing of the same three planes
            if rx.max() > 1e-6: continue                                             # outside some facet (float, clear margin)
            TV = [int(f) for f in np.where(np.abs(rx) < vband)[0]]
            res = {f: dot(poly.N[f], x) - H[f] for f in TV}
            if all(r.sign() <= 0 for r in res.values()):
                verts[key] = frozenset(f for f, r in res.items() if r.iszero())
    def faces_of(V):
        byf = defaultdict(list)
        for vi, x in enumerate(V):
            for f in verts[x]: byf[f].append(vi)
        faces = {}
        for f, vs in byf.items():
            if len(vs) >= 3:
                p0 = V[vs[0]]
                if rank_r5([[a - b for a, b in zip(V[w], p0)] for w in vs[1:]]) == 2: faces.setdefault(tuple(sorted(vs)), []).append(f)
        return faces
    V = list(verts); dropped = 0
    for _ in range(4):                       # keep true corners only: the face planes through a corner have rank 3 (with nu: rank 4)
        faces = faces_of(V); onf = defaultdict(set)
        for vs, fs in faces.items():
            for w in vs: onf[w].update(fs)
        keepv = [x for w, x in enumerate(V) if rank_r5([nu] + [poly.N[f] for f in onf[w]]) == 4]
        if len(keepv) == len(V): break
        dropped += len(V) - len(keepv); V = keepv
    fl_ = list(faces); vf = defaultdict(set)
    for fi, vs in enumerate(fl_):
        for w in vs: vf[w].add(fi)
    E = sum(1 for u, w in itertools.combinations(range(len(V)), 2) if len(vf[u] & vf[w]) >= 2)
    sizes = Counter(len(vs) for vs in fl_); deg = Counter(len(vf[w]) for w in range(len(V)))
    return dict(V=len(V), E=E, F=len(fl_), euler=len(V) - E + len(fl_), sizes=dict(sorted(sizes.items())), deg=dict(sorted(deg.items())),
                facets_met=sorted({f for fs in faces.values() for f in fs}), carried=[tuple(sorted(fs)) for fs in faces.values() if len(fs) == 2],
                multi=[fs for fs in faces.values() if len(fs) > 2], gap=minband, maxres=0.0, exact=True, _V=V, _faces=faces, _verts=verts, triples=ntri, float_corners=len(P), dropped_points=dropped)
