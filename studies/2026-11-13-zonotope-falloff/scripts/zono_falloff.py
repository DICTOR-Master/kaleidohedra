"""Zonotope fall-off law (13 Nov 2026; lead 1 of studies/2026-11-13-amplitude-at-distance).
Far from a d-polytope P the canonical function falls off as Omega_P(t u) = sum_{k>=1} c_k(u) t^-(d+k). Call e(P) the first k with
c_k != 0 (decay r^-(d+e)). This script computes c_0 .. c_K EXACTLY (rationals, or Q(sqrt5) for golden solids) at 3 generic
directions for 3D, 4D and 5D test solids, and checks the theorems of the README against them:
  T2 central symmetry: c_k = 0 whenever d + k is odd;
  T3 zonotopes: c_k = 0 for k < d and c_d = (-1)^d 2^d sum_S |det G_S|^(2d-1) / prod_i det(G_S, column i -> u)^2 (S = bases among
     the generators), so e = d exactly (decay r^-2d);
  T4/T5 (3D form): c_1 = 0 iff every pair of parallel facets has equal edge-asymmetry and every unpaired facet is centrally
     symmetric; then c_2 = 0 iff every facet is centrally symmetric; hence 3D trichotomy e in {1, 2, 3}, e = 3 iff zonotope;
     local check of the residue mechanism: w c_1 and w^2 c_2 near each facet hyperplane n_F . u = 0;
  T6 products: e(P x Q) = e(P) + e(Q); Omega_{PxQ} = Omega_P Omega_Q exactly (independent check of the higher-d triangulation);
  T7 Minkowski lineality bound: P = Q_1 + ... + Q_m, c_k = 0 for k < (least number of summands whose spans add up to R^d).
Method: vertex formula Omega(x) = sum_v sum_{simplices S of a pulling triangulation of the normal cone at v} |det n_S| / prod_{F in S}
(b_F - n_F.x) (Warren; = d! vol((P - x)°) inside P, Arkani-Hamed-Bai-Lam). Expansion at x = t u: c_k = (-1)^d sum |det n_S|
h_k(b_F / w_F) / prod w_F, w_F = n_F.u, h_k the complete symmetric polynomial. Facets: float hull (scipy) for the combinatorics only,
then every facet plane is recomputed and verified EXACTLY (all vertices on the correct side, facet = exact incidence set).
Usage: zono_falloff.py [--pilot] [--workers N] out.json"""
import sys, os, itertools, random, time, json, math
from fractions import Fraction as Fr
from multiprocessing import Pool
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, '..', '..', '2026-11-02-dicto-vacuus', 'scripts', 'qf.py')).read(), globals())   # QF (Q(sqrt5))
QF.D = 5
T0 = time.time()
PILOT = '--pilot' in sys.argv
args = [a for a in sys.argv[1:] if a != '--pilot']
WORKERS = 2
if '--workers' in args: i = args.index('--workers'); WORKERS = int(args[i + 1]); del args[i:i + 2]
OUT = args[0] if args else 'zono.json'
CHECKS = []
def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok))); print(('ok   ' if ok else 'FAIL ') + name + (('  [' + detail + ']') if detail else ''), flush=True)
def prog(f, what): print(f'PROGRESS {f:.3f} {what} ({time.time() - T0:.0f} s)', flush=True)

# ---------------------------------------------------------------- exact helpers (Fraction or QF)
def sgn(x): return x.sign() if isinstance(x, QF) else (x > 0) - (x < 0)
def aabs(x): return -x if sgn(x) < 0 else x
def fl(x): return float(x)
def pw(x, k):
    r = Fr(1)
    for _ in range(k): r = r * x
    return r
def dotv(a, b): return sum((x * y for x, y in zip(a, b)), Fr(0))
def ex(x): return x if isinstance(x, (Fr, QF)) else Fr(x)
def det(M):
    M = [[ex(x) for x in r] for r in M]; n = len(M); d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d = d * M[c][c]
        for r in range(c + 1, n):
            if M[r][c] != 0:
                f = M[r][c] / M[c][c]; M[r] = [M[r][j] - f * M[c][j] for j in range(n)]
    return d
def rank(vs):
    M = [[ex(x) for x in v] for v in vs]; r = 0; ncol = len(M[0]) if M else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [M[i][j] - f * M[r][j] for j in range(ncol)]
        r += 1
    return r
def normal_through(pts):
    """exact normal of the hyperplane through d points in R^d (generalised cross product of the differences)"""
    d = len(pts[0]); D = [[a - b for a, b in zip(p, pts[0])] for p in pts[1:]]
    return tuple(((-1) ** j) * det([[r[i] for i in range(d) if i != j] for r in D]) for j in range(d))

# ---------------------------------------------------------------- polytope with exact facets and pulling triangulations
class Poly:
    def __init__(s, name, V, info=None):
        s.name = name; s.info = info or {}
        assert not any(isinstance(x, float) for v in V for x in v), 'float coordinate'
        V = [tuple(x if isinstance(x, (Fr, QF)) else Fr(x) for x in v) for v in V]
        V = list(dict.fromkeys(V)); s.d = d = len(V[0])
        c = tuple(sum((v[i] for v in V), Fr(0)) / len(V) for i in range(d))        # centre at the vertex centroid (exact)
        V = [tuple(v[i] - c[i] for i in range(d)) for v in V]
        if d == 1:
            lo, hi = min(V, key=lambda v: fl(v[0])), max(V, key=lambda v: fl(v[0])); s.V = [lo, hi]
            s.Fv = [frozenset([1]), frozenset([0])]; s.N = [(Fr(1),), (Fr(-1),)]; s.B = [hi[0], -lo[0]]
            s.vf = [frozenset([1]), frozenset([0])]; s.memo = {}; s.cs = lo[0] == -hi[0]; return
        Vf = np.array([[fl(x) for x in v] for v in V])
        H = ConvexHull(Vf)
        cand = sorted(set(H.vertices.tolist())); s.V = [V[i] for i in cand]; Vf = Vf[cand]
        H = ConvexHull(Vf)
        facets = {}
        seen = set()
        for eq in H.equations:
            onf = [i for i in range(len(s.V)) if abs(Vf[i] @ eq[:-1] + eq[-1]) < 1e-7 * (1 + np.abs(Vf[i]).max())]
            if frozenset(onf) in seen: continue
            seen.add(frozenset(onf)); sel = [onf[0]]
            for i in onf[1:]:                       # greedy affinely independent subset (exact rank)
                if rank([[a - b for a, b in zip(s.V[j], s.V[sel[0]])] for j in sel[1:] + [i]]) == len(sel): sel.append(i)
                if len(sel) == d: break
            if len(sel) < d: raise ValueError('facet of low rank')
            pts = [s.V[i] for i in sel]; n = normal_through(pts); b = dotv(n, pts[0])
            if all(x == 0 for x in n): raise ValueError('degenerate facet normal')
            if sgn(b) < 0: n = tuple(-x for x in n); b = -b
            if sgn(b) == 0: raise ValueError('facet through the centre')
            on = frozenset(i for i, v in enumerate(s.V) if dotv(n, v) == b)
            if any(sgn(dotv(n, v) - b) > 0 for v in s.V): raise ValueError('hull facet not supporting (exact)')
            facets[on] = (n, b)
        s.Fv = list(facets.keys()); s.N = [facets[k][0] for k in s.Fv]; s.B = [facets[k][1] for k in s.Fv]
        s.vf = [frozenset(j for j, f in enumerate(s.Fv) if i in f) for i in range(len(s.V))]
        s.memo = {}
        s.cs = set(s.V) == set(tuple(-x for x in v) for v in s.V)
    def closure_sets(s, S):
        """facet sets of the faces covering the face with facet set S (maximal proper S_w)"""
        VS = frozenset.intersection(*[s.Fv[j] for j in S])
        cand = set()
        for j in S:
            for w in s.Fv[j]:
                if w not in VS: cand.add(frozenset(S & s.vf[w]))
        cand = [c for c in cand if c]
        return [c for c in cand if not any(c < o for o in cand)]
    def tri(s, S):
        S = frozenset(S)
        if S in s.memo: return s.memo[S]
        r = rank([s.N[j] for j in S])
        if len(S) == r: out = [tuple(sorted(S))]
        else:
            F0 = min(S); out = []
            for Sp in s.closure_sets(S):
                if F0 in Sp: continue
                for simp in s.tri(Sp): out.append(tuple(sorted(simp + (F0,))))
        s.memo[S] = out; return out
    def simplices(s):
        if not hasattr(s, '_simp'):
            out = []
            for i in range(len(s.V)):
                for S in s.tri(s.vf[i]):
                    if len(S) != s.d: raise ValueError('bad simplex size')
                    out.append((S, aabs(det([s.N[j] for j in S]))))
            s._simp = out
        return s._simp
    def omega(s, x):
        f = [b - dotv(n, x) for n, b in zip(s.N, s.B)]; tot = Fr(0)
        for S, D in s.simplices():
            p = Fr(1)
            for j in S: p = p * f[j]
            tot = tot + D / p
        return tot
    def far(s, u, K):
        """exact c_0 .. c_K at direction u"""
        w = [dotv(n, u) for n in s.N]
        if any(x == 0 for x in w): return None
        z = [b / x for b, x in zip(s.B, w)]; c = [Fr(0)] * (K + 1)
        for S, D in s.simplices():
            h = [Fr(1)] + [Fr(0)] * K
            for j in S:
                for k in range(1, K + 1): h[k] = h[k] + z[j] * h[k - 1]
            p = Fr(1)
            for j in S: p = p * w[j]
            for k in range(K + 1): c[k] = c[k] + D * h[k] / p
        sg = (-1) ** s.d
        return [sg * x for x in c]

# ---------------------------------------------------------------- builders
def zonotope_pts(G):
    d = len(G[0]); pts = set()
    for sg in itertools.product((1, -1), repeat=len(G)):
        pts.add(tuple(sum((Fr(si) * g[i] for si, g in zip(sg, G)), Fr(0)) for i in range(d)))
    return list(pts)
def mink(A, B): return [tuple(a + b for a, b in zip(p, q)) for p in A for q in B]
def prod(A, B): return [tuple(p) + tuple(q) for p in A for q in B]
def allperm_signs(v):
    out = set()
    for p in itertools.permutations(v):
        for sg in itertools.product((1, -1), repeat=len(v)): out.add(tuple(Fr(a) * b for a, b in zip(sg, p)))
    return sorted(out)
def cyc_signs(v):
    out = set()
    for k in range(3):
        p = v[k:] + v[:k]
        for sg in itertools.product((1, -1), repeat=3): out.add(tuple(a * b for a, b in zip(p, sg)))
    return list(out)
def halfspace_vertices(H):
    d = len(H[0][0]); out = set()
    for comb in itertools.combinations(range(len(H)), d):
        M = [list(H[i][0]) for i in comb]; D = det(M)
        if D == 0: continue
        x = []
        for c in range(d):
            Mc = [list(r) for r in M]
            for r in range(d): Mc[r][c] = H[comb[r]][1]
            x.append(det(Mc) / D)
        if all(sgn(dotv(n, x) - b) <= 0 for n, b in H):
            assert all(isinstance(t, (Fr, QF)) for t in x); out.add(tuple(x))
    return list(out)
PHI = QF(Fr(1, 2), Fr(1, 2)); Z0 = QF(0); ONE = QF(1)
def ico_axes():   # the 6 five-fold axes of the icosahedron cyclic(0, +-1, +-phi), one per antipodal pair
    V = cyc_signs((Z0, ONE, PHI)); ax = []
    for v in V:
        if not any(all(a == -b for a, b in zip(v, w)) for w in ax): ax.append(v)
    return ax
R = random.Random(20261113)
def rint(lo=-4, hi=4):
    while True:
        x = R.randint(lo, hi)
        if x: return Fr(x)
def rvec(d, lo=-4, hi=4): return tuple(rint(lo, hi) for _ in range(d))
SEG = [(Fr(-1),), (Fr(1),)]
TRI = [(Fr(0), Fr(0)), (Fr(3), Fr(0)), (Fr(1), Fr(2))]                   # a generic (non-symmetric) triangle
SQ = [(Fr(a), Fr(b)) for a in (-1, 1) for b in (-1, 1)]
PENT = [(Fr(0), Fr(0)), (Fr(4), Fr(0)), (Fr(5), Fr(2)), (Fr(2), Fr(5)), (Fr(-1), Fr(3))]

def solids(pilot):
    R.seed(20261113)
    S = []   # (name, points builder, info: predicted e from theory or None, zonotope generators or None, summands spans)
    # ---- 3D zonotopes
    E3 = [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0)), (Fr(0), Fr(0), Fr(1))]
    RDg = [(Fr(1), Fr(1), Fr(1)), (Fr(1), Fr(1), Fr(-1)), (Fr(1), Fr(-1), Fr(1)), (Fr(-1), Fr(1), Fr(1))]
    TOg = [(Fr(1), Fr(-1), Fr(0)), (Fr(1), Fr(0), Fr(-1)), (Fr(0), Fr(1), Fr(-1)), (Fr(1), Fr(1), Fr(0)), (Fr(1), Fr(0), Fr(1)), (Fr(0), Fr(1), Fr(1))]
    HPg = [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0)), (Fr(1), Fr(1), Fr(0)), (Fr(0), Fr(0), Fr(1))]
    TCOg = E3 + TOg
    zs = [('cube', E3), ('rhombic dodecahedron', RDg), ('truncated octahedron', TOg), ('hexagonal prism (affine)', HPg),
          ('generic parallelepiped', [rvec(3) for _ in range(3)]), ('generic 4-zonotope', [rvec(3) for _ in range(4)]),
          ('generic 5-zonotope', [rvec(3) for _ in range(5)]), ('truncated cuboctahedron', TCOg),
          ('rhombic triacontahedron', ico_axes()), ('rhombic icosahedron', ico_axes()[:5])]
    if pilot: zs = zs[:3] + zs[8:9]
    for name, G in zs: S.append((name, lambda G=G: zonotope_pts(G), dict(zono=G, kind='zonotope')))
    # ---- 3D others
    TRDH = [((Fr(1), Fr(-1), Fr(0)), 1), ((Fr(0), Fr(1), Fr(-1)), 1), ((Fr(1), Fr(0), Fr(-1)), 1), ((Fr(-1), Fr(1), Fr(0)), 1),
            ((Fr(0), Fr(-1), Fr(1)), 1), ((Fr(-1), Fr(0), Fr(1)), 1), ((Fr(1), Fr(0), Fr(1)), 1), ((Fr(0), Fr(1), Fr(1)), 1),
            ((Fr(1), Fr(1), Fr(0)), 1), ((Fr(-1, 3), Fr(-4, 3), Fr(-1, 3)), 1), ((Fr(-4, 3), Fr(-1, 3), Fr(-1, 3)), 1), ((Fr(-1, 3), Fr(-1, 3), Fr(-4, 3)), 1)]
    tet = [(Fr(1), Fr(1), Fr(1)), (Fr(1), Fr(-1), Fr(-1)), (Fr(-1), Fr(1), Fr(-1)), (Fr(-1), Fr(-1), Fr(1))]
    others = [
        ('tetrahedron', lambda: tet, {}),
        ('octahedron', lambda: allperm_signs((1, 0, 0)), {}),
        ('cuboctahedron', lambda: allperm_signs((1, 1, 0)), {}),
        ('icosahedron', lambda: cyc_signs((Z0, ONE, PHI)), {}),
        ('TRD (hcp Voronoi cell)', lambda: halfspace_vertices(TRDH), {}),
        ('triangular prism', lambda: prod(TRI, SEG), {'prod': (1, 1)}),
        ('dodecahedron', lambda: [tuple(QF(x) for x in v) for v in itertools.product((1, -1), repeat=3)] + cyc_signs((Z0, 1 / PHI, PHI)), {}),
        ('truncated tetrahedron', lambda: [p for p in allperm_signs((3, 1, 1)) if (p[0] * p[1] * p[2]) > 0], {}),
        ('cube with corners cut at 1/3 (truncated-cube type)', lambda: allperm_signs((Fr(1, 3), 1, 1)), {}),
        ('rhombicuboctahedron', lambda: allperm_signs((1, 1, 3)), {}),
        ('pentagonal prism (irregular)', lambda: prod(PENT, SEG), {'prod': (1, 1)}),
        ('oblique triangular prism', lambda: [(p[0], p[1], Fr(0)) for p in TRI] + [(p[0] + 1, p[1] + 2, Fr(3)) for p in TRI], {}),
        ('triangular frustum', lambda: [(p[0], p[1], Fr(0)) for p in TRI] + [(p[0] / 2, p[1] / 2, Fr(2)) for p in TRI], {}),
        ('square antiprism (rational)', lambda: [(Fr(a), Fr(b), Fr(0)) for a in (-2, 2) for b in (-2, 2)] + [(Fr(a), Fr(b), Fr(3)) for a, b in ((3, 0), (-3, 0), (0, 3), (0, -3))], {}),
        ('triangle + generic 3-zonotope', lambda: mink([(p[0], p[1], Fr(0)) for p in TRI], zonotope_pts([rvec(3) for _ in range(3)])), {'mink_r': 2}),
        ('tetrahedron + cube', lambda: mink(tet, zonotope_pts(E3)), {'mink_r': 1}),
        ('corner-cut cube', lambda: [v for v in itertools.product((Fr(-1), Fr(1)), repeat=3) if v != (1, 1, 1)] + [(Fr(1, 2), Fr(1), Fr(1)), (Fr(1), Fr(1, 2), Fr(1)), (Fr(1), Fr(1), Fr(1, 2))], {}),
        ('random hull (12 points)', lambda: [rvec(3, -6, 6) for _ in range(12)], {}),
    ]
    if pilot: others = others[:6]
    S += others
    # ---- 4D
    E4 = [tuple(Fr(int(i == j)) for j in range(4)) for i in range(4)]
    A4 = [tuple(Fr(int(k == i) - int(k == j)) for k in range(4)) for i in range(4) for j in range(i + 1, 4)] + E4   # e_i - e_j, e_i (A4 permutohedron, projected)
    four = [
        ('tesseract', lambda: zonotope_pts(E4), dict(zono=E4, kind='zonotope')),
        ('generic 5-zonotope (4D)', lambda G=[rvec(4) for _ in range(5)]: zonotope_pts(G), None),
        ('A4 permutohedron (10 generators)', lambda: zonotope_pts(A4), dict(zono=A4, kind='zonotope')),
        ('4-simplex', lambda: [tuple(Fr(int(i == j)) for j in range(4)) for i in range(4)] + [tuple(Fr(-1) for _ in range(4))], {}),
        ('16-cell', lambda: allperm_signs((1, 0, 0, 0)), {}),
        ('24-cell', lambda: allperm_signs((1, 1, 0, 0)), {}),
        ('triangle x square', lambda: prod(TRI, SQ), {'prod': (1, 2)}),
        ('triangle x triangle', lambda: prod(TRI, TRI), {'prod': (1, 1)}),
        ('tetrahedron x segment', lambda: prod(tet, SEG), {'prod': (1, 1)}),
        ('octahedron x segment', lambda: prod(allperm_signs((1, 0, 0)), SEG), {'prod': (1, 1)}),
        ('TRD x segment', lambda: prod(halfspace_vertices(TRDH), SEG), {'prod': (2, 1)}),
        ('triangle + generic 4-zonotope', lambda: mink([(p[0], p[1], Fr(0), Fr(0)) for p in TRI], zonotope_pts([rvec(4) for _ in range(4)])), {'mink_r': 3}),
    ]
    g5 = [rvec(4) for _ in range(5)]
    four[1] = ('generic 5-zonotope (4D)', lambda G=g5: zonotope_pts(G), dict(zono=g5, kind='zonotope'))
    if pilot: four = [four[0], four[4], four[6]]
    S += four
    if not pilot:
        E5 = [tuple(Fr(int(i == j)) for j in range(5)) for i in range(5)]; g6 = [rvec(5) for _ in range(6)]
        S += [('5-cube', lambda: zonotope_pts(E5), dict(zono=E5, kind='zonotope')),
              ('generic 6-zonotope (5D)', lambda G=g6: zonotope_pts(G), dict(zono=g6, kind='zonotope')),
              ('5-simplex', lambda: E5 + [tuple(Fr(-1) for _ in range(5))], {}),
              ('5-cross-polytope', lambda: allperm_signs((1, 0, 0, 0, 0)), {}),
              ('triangle x triangle x segment', lambda: prod(prod(TRI, TRI), SEG), {'prod3': (1, 1, 1)})]
    return S

def zono_formula(G, u):
    d = len(u); tot = Fr(0)
    for S in itertools.combinations(G, d):
        D = det([list(g) for g in S])
        if D == 0: continue
        den = Fr(1)
        for i in range(d):
            M = [list(g) for g in S]; M[i] = list(u); den = den * pw(det(M), 2)
        tot = tot + pw(aabs(D), 2 * d - 1) / den
    return (-1) ** d * 2 ** d * tot

# ---------------------------------------------------------------- 3D facet-pairing predicate (edge asymmetry)
def pairing_3d(P):
    """returns (pairing_holds, all_faces_cs, per-line details). Edges of P = pairs of vertices whose common facet set has rank 2."""
    nV = len(P.V); E = []
    for i in range(nV):
        for j in range(i + 1, nV):
            S = P.vf[i] & P.vf[j]
            if len(S) >= 2 and rank([P.N[k] for k in S]) == 2: E.append((i, j))
    def key(n):
        k = next(t for t in range(3) if n[t] != 0); return tuple(x / n[k] for x in n)
    lines = {}
    for f in range(len(P.Fv)): lines.setdefault(key(P.N[f]), []).append(f)
    def asym(f, m):
        vs = P.Fv[f]; c = tuple(sum((P.V[i][t] for i in vs), Fr(0)) / len(vs) for t in range(3)); A = {}
        for i, j in E:
            if i in vs and j in vs:
                p, q = P.V[i], P.V[j]; e = tuple(b - a for a, b in zip(p, q))
                cr = (e[1] * (c[2] - p[2]) - e[2] * (c[1] - p[1]), e[2] * (c[0] - p[0]) - e[0] * (c[2] - p[2]), e[0] * (c[1] - p[1]) - e[1] * (c[0] - p[0]))
                if sgn(dotv(cr, m)) < 0: e = tuple(-x for x in e)
                k = key(e); A[k] = tuple(a + b for a, b in zip(A.get(k, (Fr(0),) * 3), e))
        return {k: v for k, v in A.items() if any(x != 0 for x in v)}
    ok = True; allcs = True; det_ = []
    for m, fs in lines.items():
        As = [asym(f, m) for f in fs]
        if any(As): allcs = False
        if len(fs) == 1: good = not As[0]
        else: good = As[0] == As[1]
        ok = ok and good; det_.append((len(fs), good))
    return ok, allcs, E, lines

def local_residues(P, E, lines, rng):
    """for each facet line: u = u0 + eps n (u0 generic, n.u0 = 0): returns [(paired?, w*c1, w^2*c2)] as floats of exact values"""
    out = []
    for m, fs in lines.items():
        n = P.N[fs[0]]
        for _ in range(20):
            a = tuple(Fr(rng.randint(-7, 7)) for _ in range(3)); u0 = tuple(x - dotv(a, n) / dotv(n, n) * y for x, y in zip(a, n))
            if all(dotv(P.N[g], u0) != 0 for g in range(len(P.N)) if key3(P.N[g]) != key3(n)): break
        eps = Fr(1, 10 ** 12); u = tuple(x + eps * y for x, y in zip(u0, n)); c = P.far(u, 2)
        if c is None: continue
        w = dotv(n, u); out.append((len(fs), fl(w * c[1]), fl(w * w * c[2])))
    return out
def key3(n):
    k = next(t for t in range(3) if n[t] != 0); return tuple(x / n[k] for x in n)

# ---------------------------------------------------------------- one solid
ITEMS = None
def run_one(idx):
    global ITEMS
    if ITEMS is None: ITEMS = solids(PILOT)
    name, build, info = ITEMS[idx]; t = time.time(); rng = random.Random(sum(map(ord, name)))
    info = info or {}
    try:
        P = Poly(name, build(), info)
    except Exception as ex:
        return dict(name=name, error=repr(ex))
    d = P.d; K = 2 * d + 1 if d <= 4 else d + 2
    res = dict(name=name, d=d, V=len(P.V), F=len(P.Fv), simplices=len(P.simplices()), cs=P.cs, info={k: v for k, v in info.items() if k != 'zono'})
    golden = any(isinstance(x, QF) for v in P.V for x in v)
    dirs = []; cs = []
    while len(dirs) < 3:
        u = tuple(Fr(rng.randint(-9, 9)) for _ in range(d))
        c = P.far(u, K)
        if c is None or all(x == 0 for x in u): continue
        dirs.append(u); cs.append(c)
    E = [next((k for k in range(K + 1) if c[k] != 0), None) for c in cs]
    res['e_per_dir'] = E; res['e'] = min(x for x in E if x is not None) if any(x is not None for x in E) else None
    res['decay'] = f"r^-{d + res['e']}" if res['e'] is not None else 'faster than computed'
    res['c_float'] = [[fl(x) for x in c] for c in cs]
    res['dirs'] = [[str(x) for x in u] for u in dirs]
    res['zero_pattern'] = [[c[k] == 0 for k in range(K + 1)] for c in cs]
    res['c0_zero'] = all(c[0] == 0 for c in cs)
    if P.cs: res['cs_parity_ok'] = all(c[k] == 0 for c in cs for k in range(K + 1) if (d + k) % 2 == 1)
    if 'zono' in info:
        res['zono_formula_ok'] = all(c[d] == zono_formula(info['zono'], u) for c, u in zip(cs, dirs)) and all(c[k] == 0 for c in cs for k in range(d))
    # Omega at an interior point vs d! vol(polar) (float, independent hull of the polar points)
    if not golden:
        x0 = tuple(Fr(R2) / 97 for R2 in (rng.randint(-3, 3) for _ in range(d)))
        if all(sgn(b - dotv(n, x0)) > 0 for n, b in zip(P.N, P.B)):
            om = P.omega(x0); Q = np.array([[fl(x) / fl(b - dotv(n, x0)) for x in n] for n, b in zip(P.N, P.B)])
            vol = ConvexHull(Q).volume; res['polar_check'] = abs(fl(om) - math.factorial(d) * vol) <= 1e-9 * abs(fl(om))
        # far point vs series
        u = dirs[0]; T = Fr(10 ** 6); x = tuple(T * a for a in u); om = P.omega(x); ser = sum((cs[0][k] * T ** (-(d + k)) for k in range(K + 1)), Fr(0))
        res['series_check'] = abs(fl((om - ser) / om)) < 1e-12 if om != 0 else False
    if d == 3:
        ok, allcs, E3, lines = pairing_3d(P); res['pairing'] = ok; res['all_faces_cs'] = allcs
        pred = 1 if not ok else (2 if not allcs else 3)
        res['predicted_e_3d'] = pred
        if not golden:
            lr = local_residues(P, E3, lines, rng); res['local'] = lr
    res['seconds'] = round(time.time() - t, 2)
    return res

def product_check():
    """Omega_{P x Q}(x, y) = Omega_P(x) Omega_Q(y) exactly at random points (tests the 4D/5D triangulation independently)"""
    rng = random.Random(7); ok = True; n = 0
    tet = [(Fr(1), Fr(1), Fr(1)), (Fr(1), Fr(-1), Fr(-1)), (Fr(-1), Fr(1), Fr(-1)), (Fr(-1), Fr(-1), Fr(1))]
    pairs = [(TRI, SQ), (TRI, TRI), (tet, SEG), (allperm_signs((1, 0, 0)), SEG)]
    if not PILOT: pairs.append((prod(TRI, TRI), SEG))
    for A, B in pairs:
        PA, PB, PP = Poly('A', A), Poly('B', B), Poly('AxB', prod(A, B))
        for _ in range(3):
            x = tuple(Fr(rng.randint(-20, 20), 7) for _ in range(PA.d)); y = tuple(Fr(rng.randint(-20, 20), 7) for _ in range(PB.d))
            try: ok = ok and PP.omega(x + y) == PA.omega(x) * PB.omega(y); n += 1
            except ZeroDivisionError: pass
    return ok, n

if __name__ == '__main__':
    print(f'zono_falloff {"PILOT" if PILOT else "FULL"} workers={WORKERS}', flush=True)
    # method checks
    cube = Poly('c', zonotope_pts([(Fr(1, 2), 0, 0), (0, Fr(1, 2), 0), (0, 0, Fr(1, 2))]))
    check('M1 Omega_cube(0) = 64 for the cube [-1/2,1/2]^3 (known value)', cube.omega((Fr(0),) * 3) == 64)
    x = (Fr(1, 7), Fr(-2, 9), Fr(3, 11)); exact = Fr(1)
    for xi in x: exact = exact / ((Fr(1, 2) - xi) * (Fr(1, 2) + xi))
    check('M2 cube: vertex formula = product formula prod 1/((1/2 - x_i)(1/2 + x_i)) exactly at an interior point', cube.omega(x) == exact)
    ok, n = product_check(); check(f'M3 products: Omega_PxQ = Omega_P Omega_Q exactly at {n} random points (2D x 2D, 3D x 1D, 4D x 1D)', ok and n >= 9)
    prog(0.05, 'method checks')
    items = solids(PILOT)
    results = []
    with Pool(WORKERS) as pool:
        for k, r in enumerate(pool.imap(run_one, range(len(items)))):
            results.append(r); prog(0.05 + 0.9 * (k + 1) / len(items), f"{r['name']}: " + (r.get('error') or f"d={r['d']} V={r['V']} F={r['F']} e={r['e']} decay {r['decay']} ({r['seconds']} s)"))
    by = {r['name']: r for r in results}
    errs = [r['name'] for r in results if 'error' in r]
    check('M4 every solid built with exact facets' + (f' (errors: {errs})' if errs else ''), not errs)
    good = [r for r in results if 'error' not in r]
    check('M5 c_0 = 0 exactly at every direction (complete-fan identity)', all(r['c0_zero'] for r in good))
    pc = [r for r in good if 'polar_check' in r]; sc = [r for r in good if 'series_check' in r]
    check(f'M6 Omega(x0) = d! vol((P - x0)°) at an interior point (float polar hull, 1e-9) for {len(pc)} rational solids', all(r['polar_check'] for r in pc) and len(pc) >= 5)
    check(f'M7 exact Omega(10^6 u) agrees with the series c_0..c_K to relative 1e-12 for {len(sc)} rational solids', all(r['series_check'] for r in sc) and len(sc) >= 5)
    check('M8 e is the same at all 3 directions for every solid', all(len(set(r['e_per_dir'])) == 1 for r in good))
    Z = [r for r in good if 'zono_formula_ok' in r]
    check(f'T3 zonotopes ({len(Z)}): c_k = 0 for k < d and c_d = the explicit formula, exactly, at every direction', all(r['zono_formula_ok'] for r in Z) and len(Z) >= 4)
    check('T3 zonotopes: e = d (decay r^-2d) for every zonotope', all(r['e'] == r['d'] for r in Z))
    CS = [r for r in good if r['cs']]
    check(f'T2 centrally symmetric solids ({len(CS)}): c_k = 0 whenever d + k is odd (k <= K)', all(r['cs_parity_ok'] for r in CS))
    T3d = [r for r in good if r['d'] == 3 and 'predicted_e_3d' in r]
    check(f'T5 3D trichotomy ({len(T3d)} solids): e = 1 / 2 / 3 exactly as the facet predicate says (pairing; all faces centrally symmetric)',
          all(r['e'] == r['predicted_e_3d'] for r in T3d), '; '.join(f"{r['name']}: e={r['e']} pred={r['predicted_e_3d']}" for r in T3d if r['e'] != r['predicted_e_3d']))
    check('T5 3D: decay orders only r^-4, r^-5, r^-6', all(r['e'] in (1, 2, 3) for r in T3d))
    # local residue mechanism
    loc_ok = True; nloc = 0
    for r in T3d:
        for (npair, wc1, w2c2) in r.get('local', []):
            nloc += 1
            if r['e'] >= 2 and abs(wc1) > 1e-6: loc_ok = False
            if r['e'] == 3 and abs(w2c2) > 1e-6: loc_ok = False
    check(f'T4 local: w c_1 -> 0 at every facet hyperplane when e >= 2, w^2 c_2 -> 0 when e = 3 ({nloc} facet lines, eps 1e-12)', loc_ok and nloc > 0)
    some = any(abs(w2c2) > 1e-3 for r in T3d if r['e'] == 2 for (_, _, w2c2) in r.get('local', []))
    check('T4 local NEGATIVE: for e = 2 solids some facet line has a true double pole of c_2 (w^2 c_2 not -> 0)', some)
    PR = [r for r in good if 'prod' in r['info'] or 'prod3' in r['info']]
    check(f'T6 products ({len(PR)}): e(P x Q) = e(P) + e(Q)', all(r['e'] == sum(r['info'].get('prod', r['info'].get('prod3'))) for r in PR))
    MK = [r for r in good if 'mink_r' in r['info']]
    check(f'T7 Minkowski lineality bound ({len(MK)}): e >= r', all(r['e'] >= r['info']['mink_r'] for r in MK))
    # the brief's refined hypothesis, tested
    ico = by.get('icosahedron'); octa = by.get('octahedron')
    hyp_cs = [r for r in good if r['cs'] and not r.get('zono_formula_ok') and r['d'] == 3]
    check('H brief hypothesis "centrally symmetric => r^-(d+2)" REFUTED in 3D: centrally symmetric non-zonotopes decay like r^-4 (e = 1): '
          + ', '.join(r['name'] for r in hyp_cs), all(r['e'] == 1 for r in hyp_cs) and len(hyp_cs) >= 3)
    z4 = [r for r in Z if r['d'] == 4]
    if z4: check('H brief hypothesis "all 2-faces symmetric => r^-(d+3)" REFUTED in 4D: zonotopes decay like r^-8 = r^-2d, not r^-7', all(r['e'] == 4 for r in z4))
    nonz = [r for r in good if r['d'] >= 4 and 'zono_formula_ok' not in r]
    check('C conjecture e(P) <= d with equality only for zonotopes: holds on every non-zonotope tested in 4D/5D (' + ', '.join(f"{r['name']} e={r['e']}" for r in nonz) + ')',
          all(r['e'] is not None and r['e'] < r['d'] for r in nonz))
    json.dump(dict(results=results, checks=CHECKS), open(OUT, 'w'), indent=1, default=str)
    nf = sum(1 for _, o in CHECKS if not o)
    print('\nTABLE  name | d | V | F | e | decay | cs | 3D pairing | all faces cs')
    for r in good: print(f"TABLE  {r['name']} | {r['d']} | {r['V']} | {r['F']} | {r['e']} | {r['decay']} | {r['cs']} | {r.get('pairing', '-')} | {r.get('all_faces_cs', '-')}")
    print(f'{len(CHECKS)} checks, {nf} failed, {time.time() - T0:.0f} s')
    print('FINAL ok' if nf == 0 else f'FINAL FAIL ({nf} checks)')
