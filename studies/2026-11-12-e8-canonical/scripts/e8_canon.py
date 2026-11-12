"""Aim 2, chunk 7 (12 Nov 2026): E8 at the Golden Ladder's top rung as a positive geometry.
The top rung (closing chapter of The Golden Ladder, study 2026-11-05-golden-ladder-e8): the 240 E8 roots are the 120 unit icosians and
the 120 icosians / phi; under the golden projection they fall on two 600-cells (radii 1 and 1/phi); the golden twist sqrt5 -> -sqrt5
swaps the two sides. Object chosen here: the E8 root polytope (Gosset 4_21) = conv(240 roots), its polar (the Voronoi cell of E8), and
their golden shadows/slices in the two 4D spaces E_par, E_perp (the cut-and-project pair that makes the Elser-Sloane H4 quasicrystal).

Canonical form at a point Y of a polytope A = {N_f . x <= 1}:  Omega(A; Y) = n! vol((A - Y)polar)   (the bridge of chunk 2).
Two independent exact formulas:
  F1 (dual): pulling triangulation of the boundary of A-polar, built from the face lattice of A (vertex/facet bitsets),
      Omega(A; Y) = sum_s |det N_s| / prod_{f in s} (1 - N_f . Y).
  F2 (primal): pulling triangulation of the boundary of A, cones from the origin, sum of simplex forms 1/(|det Z| prod t_i)
      (t = barycentric coordinates of Y).
TASKS
  L*  lattice chain: for every root lattice (A2 A3 A4 D4 D5 E6 E7), in simple-root coordinates, Omega(conv roots; 0) = n! sqrt(det)
      <=> the coordinate Voronoi cell has volume exactly 1 (PROVED: Voronoi cell of a root lattice = polar of conv(roots), Conway-Sloane
      ch. 21); bcc: with only the 8 shortest vectors the identity FAILS (negative control: the truncated octahedron needs the 6 square
      walls), with all 14 relevant vectors it holds (Omega = 3!/2 = 3).  F1 = F2 at generic Y where small.
  E8  standard coordinates: the 19440 facets of 4_21 (2160 deep holes = norm-4 vectors/2, beta7 facets; 17280 shallow holes = norm-8
      vectors not 2r, /3, alpha7 facets), verified exactly; vol(Voronoi) by F1 at one root (x 240, transitivity of W(E8)), repeated at a
      root of the other coordinate type: expect 1, hence Omega(4_21; 0) = 8! = 40320. vol(4_21) exactly from all 19440 facet cones,
      hence Omega(Voronoi; 0) = 8! vol(4_21) and the Mahler product of the pair.
  H4  icosian coordinates (matched simple roots, map checked on all 240 roots): golden shadows of 4_21 and of the Voronoi cell in
      E_par and E_perp; exact hulls over Q(sqrt5); Omega by F1 and F2; 600-cell positive control (Omega(600-cell; 0) = 4! vol(120-cell),
      closed form (15/4)(105 + 47 sqrt5) a^4); the window W = pi_perp(Voronoi): Omega(4_21 cap E_perp; 0) = 4! vol(W) = 4! x the point
      density of the quasicrystal (section-projection duality, proved); density checked by counting lattice points (numerical).
  N*  negative controls: bcc short vectors; one pulled child dropped; one F1 term sign-flipped; the shadow of the roots as a wrong window;
      the par/perp scale factors swapped.
Usage: python -u e8_canon.py [pilot] [cores]"""
import sys, itertools, time, math
from fractions import Fraction as Fr
from multiprocessing import get_context
import numpy as np
from scipy.spatial import ConvexHull

PILOT = 'pilot' in sys.argv[1:]
CORES = int(([a for a in sys.argv[1:] if a.isdigit()] or ['4'])[0])
T0 = time.time()
OK = True
def check(name, cond):
    global OK
    OK &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)
def say(*a): print(*a, flush=True)

# ---------------- Q(sqrt5) exact ----------------
class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    @staticmethod
    def c(x): return x if isinstance(x, Q5) else Q5(x)
    def __add__(s, o): o = Q5.c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = Q5.c(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q5.c(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = Q5.c(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = Q5.c(o); n = o.a * o.a - 5 * o.b * o.b
        if n == 0: raise ZeroDivisionError
        return s * Q5(o.a / n, -o.b / n)
    def __rtruediv__(s, o): return Q5.c(o) / s
    def sign(s):
        sa = (s.a > 0) - (s.a < 0); sb = (s.b > 0) - (s.b < 0)
        if sb == 0: return sa
        if sa == 0: return sb
        if sa == sb: return sa
        return sa if s.a * s.a > 5 * s.b * s.b else sb
    def z(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): o = Q5.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __abs__(s): return -s if s.sign() < 0 else s
    def f(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def sig(s): return Q5(s.a, -s.b)
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f'{s.b}*sqrt5'
        return f'({s.a} {"+" if s.b > 0 else "-"} {abs(s.b)}*sqrt5)'
PHI = Q5(Fr(1, 2), Fr(1, 2)); IPHI = Q5(Fr(-1, 2), Fr(1, 2))
def iszero(x): return x.z() if isinstance(x, Q5) else x == 0
def sgn(x): return x.sign() if isinstance(x, Q5) else (x > 0) - (x < 0)
def fl(x): return x.f() if isinstance(x, Q5) else float(x)
def key(v): return tuple((x.a, x.b) if isinstance(x, Q5) else x for x in v)
def dotg(u, v):
    t = u[0] * v[0]
    for a, b in zip(u[1:], v[1:]): t = t + a * b
    return t

def solve(M, rhs):
    """exact Gauss-Jordan over Fraction or Q5; M square"""
    n = len(M); A = [list(M[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if not iszero(A[r][c]))
        A[c], A[p] = A[p], A[c]
        inv = 1 / A[c][c] if not isinstance(A[c][c], Fr) else Fr(1) / A[c][c]
        A[c] = [x * inv for x in A[c]]
        for r in range(n):
            if r != c and not iszero(A[r][c]):
                k = A[r][c]; A[r] = [x - k * y for x, y in zip(A[r], A[c])]
    return [A[i][n] for i in range(n)]

def det_field(M):
    n = len(M); A = [list(r) for r in M]; d = Fr(1) if not any(isinstance(x, Q5) for r in M for x in r) else Q5(1)
    for c in range(n):
        p = next((r for r in range(c, n) if not iszero(A[r][c])), None)
        if p is None: return d * 0
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d = d * A[c][c]; inv = 1 / A[c][c] if isinstance(A[c][c], Q5) else Fr(1) / A[c][c]
        for r in range(c + 1, n):
            if not iszero(A[r][c]):
                k = A[r][c] * inv; A[r] = [x - k * y for x, y in zip(A[r], A[c])]
    return d

def det_int(M):
    """Bareiss, exact integers"""
    A = [list(map(int, r)) for r in M]; n = len(A); sign = 1; prev = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            p = next((r for r in range(k + 1, n) if A[r][k] != 0), None)
            if p is None: return 0
            A[k], A[p] = A[p], A[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]

def bits(x):
    while x:
        b = x & -x; yield b.bit_length() - 1; x ^= b
def popc(x): return bin(x).count('1')

# ---------------- exact convex hull (float qhull proposes, exact arithmetic decides) ----------------
def exact_hull(P):
    """P: list of points (tuples of Fraction or Q5), origin strictly inside. Returns (vertex indices, facet normals N with N.x <= 1,
    inc_f bitsets over P). Every facet normal is solved exactly through d independent points; every point is tested exactly."""
    d = len(P[0]); X = np.array([[fl(x) for x in p] for p in P])
    H = ConvexHull(X)
    planes = {}
    for eq in H.equations:
        a = -eq[:d] / eq[d]; planes.setdefault(tuple(np.round(a, 7)), a)
    N, incf = [], []
    for a in planes.values():
        on = np.where(np.abs(X @ a - 1) < 1e-7)[0]
        sel = []
        for i in on:
            if np.linalg.matrix_rank(X[sel + [i]], tol=1e-9) == len(sel) + 1: sel.append(int(i))
            if len(sel) == d: break
        assert len(sel) == d, 'facet without d independent points'
        n = solve([P[i] for i in sel], [Fr(1) if not isinstance(P[0][0], Q5) else Q5(1)] * d)
        inc = 0; bad = 0
        for i in range(len(P)):
            if abs(X[i] @ a - 1) > 1e-6:
                if X[i] @ a > 1: bad += 1
                continue                      # float margin 1e-6 >> rounding 1e-13: strictly inside (exact test below on a sample)
            s = 1 - dotg(n, P[i])
            if iszero(s): inc |= 1 << i
            elif sgn(s) < 0: bad += 1
        assert bad == 0, 'point outside a facet'
        N.append(tuple(n)); incf.append(inc)
    # exact spot-check of the float margin: 400 random (point, facet) pairs with margin > 1e-6 tested exactly
    rng = np.random.default_rng(5)
    for _ in range(400):
        i = int(rng.integers(len(P))); f = int(rng.integers(len(N)))
        assert sgn(1 - dotg(N[f], P[i])) >= 0
    allinc = 0
    for x in incf: allinc |= x
    verts = sorted(bits(allinc))
    # a vertex must lie on facets of full rank
    vv = []
    for v in verts:
        fs = [f for f in range(len(N)) if incf[f] >> v & 1]
        if np.linalg.matrix_rank(np.array([[fl(x) for x in N[f]] for f in fs]), tol=1e-9) == d: vv.append(v)
    return vv, N, incf

# ---------------- face-lattice pulling triangulation ----------------
class Lattice:
    """top items T (indexed t) and low items L (indexed l); inc_t[t] = bitset over L, inc_l[l] = bitset over T.
    Faces are closed low-sets U; dual face D(U) = {t : U subset inc_t[t]}. tri(U) = pulling triangulation of conv(D(U)) as tuples of t."""
    def __init__(s, inc_t, inc_l, drop=None):
        s.it, s.il, s.memo, s.drop = inc_t, inc_l, {}, drop
    def S(s, U):
        r = -1
        for l in bits(U): r &= s.il[l]
        return r
    def closure(s, S2):
        r = -1
        for t in bits(S2): r &= s.it[t]
        return r
    def children(s, U, S):
        cand = 0
        for t in bits(S): cand |= s.it[t]
        cand &= ~U; seen = {}
        for w in bits(cand):
            S2 = S & s.il[w]
            if S2 and S2 != S:
                C = s.closure(S2)
                if C not in seen: seen[C] = S2
        cs = sorted(seen.items(), key=lambda kv: popc(kv[0])); out = []
        for C, S2 in cs:
            if not any((C & K) == K for K, _ in out): out.append((C, S2))
        return out
    def tri(s, U, S=None):
        if U in s.memo: return s.memo[U]
        if S is None: S = s.S(U)
        if S & (S - 1) == 0: r = [(S.bit_length() - 1,)]
        else:
            p = (S & -S).bit_length() - 1; r = []
            ch = [c for c in s.children(U, S) if not (c[1] >> p & 1)]
            if s.drop is not None and len(ch) > 1 and U == s.drop: ch = ch[1:]
            for C, S2 in ch: r += [(p,) + t for t in s.tri(C, S2)]
        s.memo[U] = r; return r

def incidences(V, N):
    inc_f = []
    for n in N:
        b = 0
        for i, v in enumerate(V):
            if iszero(1 - dotg(n, v)): b |= 1 << i
        inc_f.append(b)
    inc_v = [0] * len(V)
    for f, b in enumerate(inc_f):
        for v in bits(b): inc_v[v] |= 1 << f
    return inc_f, inc_v

def F1_terms(V, N, inc_f, inc_v, drop=None):
    """triangulation of the boundary of A-polar: list of (simplex of facet indices, |det N_s|)"""
    Lt = Lattice(inc_f, inc_v); out = []; seen = set()
    for v in range(len(V)):
        for s in Lt.tri(1 << v):
            if s not in seen: seen.add(s); out.append((s, abs(det_field([N[f] for f in s]))))
    return out
def F1_eval(terms, N, Y):
    one = Q5(1) if isinstance(N[0][0], Q5) or isinstance(Y[0], Q5) else Fr(1)
    h = {}; tot = one * 0
    for s, D in terms:
        pr = one
        for f in s:
            if f not in h: h[f] = one - dotg(N[f], Y)
            pr = pr * h[f]
        tot = tot + D / pr
    return tot
def F2_terms(V, N, inc_f, inc_v):
    """triangulation of the boundary of A (roles swapped): list of vertex-index simplices"""
    Lt = Lattice(inc_v, inc_f); out = set()
    for f in range(len(N)): out.update(Lt.tri(1 << f))
    return sorted(out)
def F2_eval(simps, V, Y):
    one = Q5(1) if isinstance(V[0][0], Q5) or isinstance(Y[0], Q5) else Fr(1)
    tot = one * 0
    for s in simps:
        Z = [V[i] for i in s]; n = len(Z)
        D = abs(det_field(Z))
        t = solve([[Z[i][j] for i in range(n)] for j in range(n)], list(Y))
        t0 = one - sum(t[1:], t[0])
        pr = t0
        for x in t: pr = pr * x
        tot = tot + one / (D * pr)
    return tot
def vol_polar(terms, n):
    tot = terms[0][1] * 0
    for _, D in terms: tot = tot + D
    return tot / math.factorial(n)
def vol_primal(simps, V, n):
    tot = None
    for s in simps:
        D = abs(det_field([V[i] for i in s])); tot = D if tot is None else tot + D
    return tot / math.factorial(n)

# ---------------- root systems in simple-root coordinates ----------------
def cartan(name):
    t, n = name[0], int(name[1:])
    C = [[2 if i == j else 0 for j in range(n)] for i in range(n)]
    def link(i, j): C[i][j] = C[j][i] = -1
    if t == 'A':
        for i in range(n - 1): link(i, i + 1)
    elif t == 'D':
        for i in range(n - 2): link(i, i + 1)
        link(n - 3, n - 1)
    elif t == 'E':   # Bourbaki: 1-3-4-5-6-7-8, 2 on 4
        lab = [(0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 3)]
        for i, j in lab:
            if i < n and j < n: link(i, j)
    return C
def roots_from_cartan(C):
    n = len(C); simple = [tuple(1 if i == j else 0 for j in range(n)) for i in range(n)]
    R = set(simple) | {tuple(-x for x in r) for r in simple}; frontier = list(R)
    while frontier:
        nxt = []
        for r in frontier:
            Gr = [sum(C[i][j] * r[j] for j in range(n)) for i in range(n)]
            for i in range(n):
                s = tuple(r[j] - (Gr[i] if j == i else 0) for j in range(n))
                if s not in R: R.add(s); nxt.append(s)
        frontier = nxt
    return sorted(R)

def lattice_task(name, generic=True):
    C = cartan(name); n = len(C); R = roots_from_cartan(C)
    P = [tuple(Fr(sum(C[i][j] * r[j] for j in range(n))) for i in range(n)) for r in R]      # G d: polar of conv(Gd) = Voronoi (coords)
    verts, N, inc_f = exact_hull(P)
    inc_f, inc_v = incidences(P, N)
    T = F1_terms(P, N, inc_f, inc_v); vol = vol_polar(T, n)
    detC = det_field([[Fr(x) for x in r] for r in C])
    res = {'name': name, 'n': n, 'roots': len(R), 'vertices': len(verts), 'facets': len(N), 'volVor_coords': vol, 'det': detC,
           'F1_terms': len(T)}
    # numerical cross-check of the polar volume (qhull on the polar's vertices = facet normals)
    res['vol_qhull'] = ConvexHull(np.array([[float(x) for x in f] for f in N])).volume
    if generic and len(T) < 60000:
        S2 = F2_terms(P, N, inc_f, inc_v)
        Ys = [tuple(Fr(k + 1, 13 * (k + 3)) * (-1) ** k for k in range(n)), tuple(Fr(1, 7 + k) for k in range(n))]
        res['F1F2'] = [(F1_eval(T, N, Y) == F2_eval(S2, P, Y)) for Y in Ys]
        res['volP_F2'] = vol_primal(S2, P, n)
        res['volP_qhull'] = ConvexHull(np.array([[float(x) for x in p] for p in P])).volume
        res['F2_terms'] = len(S2)
    return res

def bcc_task():
    out = {}
    h = Fr(1, 2)
    short = [tuple(h * s for s in sg) for sg in itertools.product((1, -1), repeat=3)]
    longv = [tuple(Fr(s) if i == j else Fr(0) for j in range(3)) for i in range(3) for s in (1, -1)]
    for lab, rel in (('short only (8)', short), ('all relevant (14)', short + longv)):
        P = [tuple(2 * x / dotg(r, r) for x in r) for r in rel]
        verts, N, inc_f = exact_hull(P); inc_f, inc_v = incidences(P, N)
        T = F1_terms(P, N, inc_f, inc_v); out[lab] = (vol_polar(T, 3), len(N))
    return out

# ---------------- E8 standard coordinates ----------------
def e8_roots2():
    """doubled coordinates (integers)"""
    R = []
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product((2, -2), repeat=2):
            v = [0] * 8; v[i] = si; v[j] = sj; R.append(tuple(v))
    for sg in itertools.product((1, -1), repeat=8):
        if sg.count(-1) % 2 == 0: R.append(tuple(sg))
    return R
def e8_vectors2(norm):
    """E8 vectors of the given norm, doubled coordinates: integer part (even entries, sum/2 even) or half part (odd entries)"""
    out = []
    for vals in ((-4, -2, 0, 2, 4), (-5, -3, -1, 1, 3, 5)):
        A = np.array(list(itertools.product(vals, repeat=8)), dtype=np.int64)
        m = ((A * A).sum(1) == 4 * norm) & (A.sum(1) % 4 == 0)
        out += [tuple(int(x) for x in r) for r in A[m]]
    return out
def e8_setup():
    R2 = e8_roots2(); assert len(R2) == 240
    deep = [tuple(3 * x for x in v) for v in e8_vectors2(4)]                          # 12 n, n = v/2 (v norm 4) -> 12n = 3*(2v)/... see note
    twoR = {tuple(2 * x for x in r) for r in R2}
    sh8 = [v for v in e8_vectors2(8) if v not in twoR]
    shallow = [tuple(2 * x for x in v) for v in sh8]                                 # n = v/3, 12n = 4v = 2*(2v)
    N12 = deep + shallow
    return R2, N12, len(deep), len(shallow)
# note: doubled coords x2 = 2x. deep hole n = v/2 -> 12n = 6v = 3*x2. shallow n = v/3 -> 12n = 4v = 2*x2.  root r: 2r = x2.  n.r = 1 <=> (12n).(2r) = 24.

E8 = {}
def e8_init():
    if E8: return
    R2, N12, nd, ns = e8_setup()
    Rm = np.array(R2, dtype=np.int64); Nm = np.array(N12, dtype=np.int64)
    Dm = Rm @ Nm.T
    inc_f = [0] * len(N12); inc_v = [0] * 240
    for v, f in zip(*np.where(Dm == 24)):
        inc_f[f] |= 1 << int(v); inc_v[v] |= 1 << int(f)
    E8.update(R2=R2, N12=N12, nd=nd, ns=ns, Dm=Dm, inc_f=inc_f, inc_v=inc_v)

def e8_child_task(args):
    """sum of |det| over the pulled simplices p + tri(child) of the polar facet F_v (dual to root v), one child"""
    v, ci, drop = args
    e8_init(); Lt = Lattice(E8['inc_f'], E8['inc_v']); U = 1 << v; S = E8['inc_v'][v]
    p = (S & -S).bit_length() - 1
    ch = [c for c in Lt.children(U, S) if not (c[1] >> p & 1)]
    C, S2 = ch[ci]
    tot = 0; cnt = 0
    for t in Lt.tri(C, S2):
        s = (p,) + t; d = det_int([E8['N12'][f] for f in s])
        assert d != 0; tot += abs(d); cnt += 1
    return v, ci, cnt, tot
def e8_children(v):
    e8_init(); Lt = Lattice(E8['inc_f'], E8['inc_v']); U = 1 << v; S = E8['inc_v'][v]
    p = (S & -S).bit_length() - 1
    return len([c for c in Lt.children(U, S) if not (c[1] >> p & 1)]), len(Lt.children(U, S))

def e8_vol421_task(chunk):
    """exact volume of 4_21 = sum over facets of cone volumes; alpha7: |det of 8 roots|/8!; beta7: 128 simplices (0, centre, facet of beta7)"""
    e8_init(); R2, N12, inc_f = E8['R2'], E8['N12'], E8['inc_f']
    tot = Fr(0)
    for f in chunk:
        vs = list(bits(inc_f[f]))
        if len(vs) == 8: tot += Fr(abs(det_int([R2[i] for i in vs])), 2 ** 8)
        else:
            assert len(vs) == 14
            # opposite vertices of the cross-polytope facet are the orthogonal pairs (inner product 0 among facet vertices)
            M = np.array([R2[i] for i in vs]); G = M @ M.T
            used = set(); pairs = []
            for a in range(14):
                if a in used: continue
                b = [b for b in range(14) if b != a and G[a, b] == 0]; assert len(b) == 1; b = b[0]
                used |= {a, b}; pairs.append((vs[a], vs[b]))
            assert len(pairs) == 7
            cen = [Fr(sum(R2[i][k] for i in vs), 14) for k in range(8)]       # doubled coords
            for ch in itertools.product((0, 1), repeat=7):
                rows = [cen] + [[Fr(x) for x in R2[pr[c]]] for pr, c in zip(pairs, ch)]
                tot += abs(det_field(rows)) / 2 ** 8
    return tot

# ---------------- icosian coordinates ----------------
def even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0: out.append([v[k] for k in p])
    return out
def icosians():
    Z, O, H = Q5(0), Q5(1), Q5(Fr(1, 2))
    U = set()
    for i in range(4):
        for s in (1, -1):
            v = [Z] * 4; v[i] = Q5(s); U.add(tuple(v))
    for sg in itertools.product((1, -1), repeat=4): U.add(tuple(H * s for s in sg))
    for v in even_perms([PHI, O, IPHI, Z]):
        for sg in itertools.product((1, -1), repeat=3):
            k = 0; w = []
            for c in v:
                if c.z(): w.append(Z)
                else: w.append(c * Fr(1, 2) * sg[k]); k += 1
            U.add(tuple(w))
    U = sorted(U, key=key); assert len(U) == 120
    return U, [tuple(x * IPHI for x in u) for u in U]
def Bic(q, p):
    d = dotg(q, p); return 2 * (d.a + d.b)
def simple_roots(R, Bf, emb):
    g = np.random.default_rng(11).normal(size=len(emb(R[0])))
    pos = [r for r in R if emb(r) @ g > 0]; pk = {key(r) for r in pos}
    simple = [r for r in pos if not any(key(tuple(x - y for x, y in zip(r, a))) in pk for a in pos)]
    return simple
def ico_setup():
    U, Ui = icosians(); Ric = U + Ui
    emb = lambda q: np.array([x.f() for x in q] + [x.sig().f() for x in q])
    sic = simple_roots(Ric, Bic, emb)
    R2 = e8_roots2(); Rstd = [tuple(Fr(x, 2) for x in r) for r in R2]
    sst = simple_roots(Rstd, None, lambda r: np.array([float(x) for x in r]))
    assert len(sic) == 8 and len(sst) == 8
    Gs = [[dotg(a, b) for b in sst] for a in sst]; Gi = [[Bic(a, b) for b in sic] for a in sic]
    def bt(pm):
        k = len(pm)
        if k == 8: return pm
        for j in range(8):
            if j in pm: continue
            if all(Gs[k][i] == Gi[j][pm[i]] for i in range(k)) and Gs[k][k] == Gi[j][j]:
                r = bt(pm + [j])
                if r: return r
        return None
    pm = bt([]); assert pm is not None
    sic = [sic[j] for j in pm]
    Sinv_T = None
    St = [[sst[i][k] for i in range(8)] for k in range(8)]    # columns = simple roots
    def to_q(x):
        c = solve(St, list(x))
        q = [Q5(0)] * 4
        for ci, s in zip(c, sic):
            if ci != 0: q = [a + ci * b for a, b in zip(q, s)]
        return tuple(q)
    return Ric, Rstd, to_q

def hull4_task(args):
    label, P = args
    verts, N, inc_f = exact_hull(P)
    Vv = [P[i] for i in verts]
    inc_f, inc_v = incidences(Vv, N)
    T = F1_terms(Vv, N, inc_f, inc_v)
    S2 = F2_terms(Vv, N, inc_f, inc_v)
    volpolar = vol_polar(T, 4); vol = vol_primal(S2, Vv, 4)
    r2 = sorted({key((dotg(v, v),)) for v in Vv})
    out = dict(label=label, V=Vv, N=N, nv=len(Vv), nf=len(N), volpolar=volpolar, vol=vol, nT=len(T), nS=len(S2),
               radii2=[Q5(a, b) for (a, b), in r2], facet_sizes=sorted({popc(b) for b in inc_f}))
    out['qhull'] = (ConvexHull(np.array([[x.f() for x in v] for v in Vv])).volume,
                    ConvexHull(np.array([[x.f() for x in n] for n in N])).volume)
    Ys = [tuple(Q5(Fr(1, 17 + k), Fr(1, 31 + 2 * k)) * (-1) ** k for k in range(4))]
    if len(T) < 40000:
        out['F1F2'] = [F1_eval(T, N, Y) == F2_eval(S2, Vv, Y) for Y in Ys]
        Tbad = [(T[0][0], -T[0][1])] + T[1:]
        out['neg_flip'] = F1_eval(Tbad, N, Ys[0]) != F2_eval(S2, Vv, Ys[0])
    # f-vector by orbits of faces: edges/2-faces via the lattice of the polytope
    out['inc'] = (inc_f, inc_v)
    from collections import Counter
    out['vert_orbits'] = sorted(Counter(key((dotg(v, v),))[0] for v in Vv).items())
    out['polar_orbits'] = sorted(Counter((key((dotg(f, f),))[0], popc(inc_f[i])) for i, f in enumerate(N)).items())
    out['vdeg'] = sorted(Counter(popc(x) for x in inc_v).items())
    return out

# ---------------- density count (numerical) ----------------
def e8_points_upto(normmax):
    out = []
    for vals in (np.arange(-10, 11, 2), np.arange(-9, 10, 2)):
        A6 = np.array(list(itertools.product(vals.tolist(), repeat=6)), dtype=np.int64)
        A6 = A6[(A6 * A6).sum(1) <= 4 * normmax]; n6 = (A6 * A6).sum(1); s6 = A6.sum(1)
        for a0, a1 in itertools.product(vals.tolist(), repeat=2):
            if a0 * a0 + a1 * a1 > 4 * normmax: continue
            m = (n6 + a0 * a0 + a1 * a1 <= 4 * normmax) & ((s6 + a0 + a1) % 4 == 0)
            B = A6[m]; out.append(np.c_[np.full(len(B), a0), np.full(len(B), a1), B])
    return np.concatenate(out) / 2.0

def main():
    say(f'chunk 7: E8 at the top rung; pilot={PILOT}; cores={CORES}')
    ctx = get_context('fork')
    # ---------- controls: lattice chain ----------
    names = ['A2', 'A3', 'D4'] if PILOT else ['A2', 'A3', 'A4', 'D4', 'D5', 'E6', 'E7']
    with ctx.Pool(min(CORES, len(names))) as pool:
        LR = pool.map(lattice_task, names)
    for r in LR:
        n = r['n']
        say(f"{r['name']}: {r['roots']} roots, conv = {r['vertices']} vertices / {r['facets']} facets; Voronoi volume (simple-root coords) = {r['volVor_coords']}; "
            f"det = {r['det']}; F1 simplices {r['F1_terms']}; qhull {r['vol_qhull']:.12f}")
        check(f"{r['name']}: Omega(conv roots; 0) = {n}! sqrt(det) <=> coordinate Voronoi volume = 1 (exact)", r['volVor_coords'] == 1)
        check(f"{r['name']}: qhull polar volume = 1 (numerical, 1e-9)", abs(r['vol_qhull'] - 1) < 1e-9)
        if 'F1F2' in r:
            check(f"{r['name']}: F1 = F2 at 2 generic points (exact)", all(r['F1F2']))
            check(f"{r['name']}: vol(conv roots) by F2 = qhull ({float(r['volP_F2']):.10f})", abs(float(r['volP_F2']) - r['volP_qhull']) < 1e-9)
    if 'D4' in names:
        d4 = next(r for r in LR if r['name'] == 'D4')
        check('24-cell (D4 roots, norm 2): Omega(0) = 4! * vol(Voronoi 24-cell of edge 1) = 4! * 2 = 48', 24 * d4['volVor_coords'] * 2 == 48 and d4['vertices'] == 24 and d4['facets'] == 24)
    say(f'PROGRESS 0.20 lattice chain ({time.time()-T0:.0f} s)')
    # negative control (bcc) + drop-one-child
    b = bcc_task()
    say(f'bcc: {b}')
    check('NEG bcc, shortest 8 only: Omega(0)/3! = 9/16 != covolume 1/2 (missing square walls of the truncated octahedron)', b['short only (8)'][0] == Fr(9, 16))
    check('bcc, all 14 relevant vectors: polar = truncated octahedron, volume 1/2 = covolume (Omega(0) = 3)', b['all relevant (14)'][0] == Fr(1, 2))
    C = cartan('D4'); R = roots_from_cartan(C); P = [tuple(Fr(sum(C[i][j] * r[j] for j in range(4))) for i in range(4)) for r in R]
    _, N, _ = exact_hull(P); inc_f, inc_v = incidences(P, N)
    Lt = Lattice(inc_f, inc_v, drop=1 << 0); tot = Fr(0); seen = set()
    for v in range(len(P)):
        for s in Lt.tri(1 << v):
            if s not in seen: seen.add(s); tot += abs(det_field([N[f] for f in s]))
    check(f'NEG D4 with one pulled child dropped: volume {tot/24} != 1', tot / 24 != 1)
    say(f'PROGRESS 0.30 negatives ({time.time()-T0:.0f} s)')

    # ---------- E8 standard ----------
    e8_init(); R2, N12 = E8['R2'], E8['N12']; Dm = E8['Dm']
    check(f"E8: 2160 deep holes + 17280 shallow holes = 19440 facets of 4_21 ({E8['nd']} + {E8['ns']})", E8['nd'] == 2160 and E8['ns'] == 17280)
    check('E8: every facet normal n has n.r <= 1 on all 240 roots (exact integers)', int(Dm.max()) == 24)
    cnt = (Dm == 24).sum(0)
    check('E8: deep holes touch 14 roots (beta7), shallow 8 (alpha7)', set(cnt[:2160]) == {14} and set(cnt[2160:]) == {8})
    rk = [np.linalg.matrix_rank(np.array([R2[i] for i in bits(E8['inc_f'][f])], dtype=float)) for f in (0, 1, 2160, 2161, 19439)]
    check('E8: facets span rank 8 (samples of both types)', set(rk) == {8})
    deg = {popc(x) for x in E8['inc_v']}
    check(f'E8: each root lies on 702 facets (576 alpha7 + 126 beta7): {deg}', deg == {702})
    vtypes = [0, next(i for i, r in enumerate(R2) if abs(r[0]) == 1)]
    jobs = []
    for v in (vtypes[:1] if PILOT else vtypes):
        k, kall = e8_children(v); say(f'E8 polar facet at root {v}: {kall} facets (edges at the root), {k} pulled children')
        jobs += [(v, ci, None) for ci in (range(1) if PILOT else range(k))]
    t1 = time.time()
    with ctx.Pool(CORES) as pool:
        res = []
        for i, r in enumerate(pool.imap_unordered(e8_child_task, jobs)):
            res.append(r); say(f'PROGRESS {0.30 + 0.4 * (i + 1) / len(jobs):.3f} E8 child {r[0]}:{r[1]} simplices {r[2]} ({time.time()-t1:.0f} s)')
    for v in sorted({r[0] for r in res}):
        cnt = sum(r[2] for r in res if r[0] == v); tot = sum(r[3] for r in res if r[0] == v)
        vol = Fr(240 * tot, math.factorial(8) * 12 ** 8)
        say(f'E8 root {v}: pulled triangulation of its polar facet: {cnt} simplices; 240 x cone volume = {vol}' + (' (pilot: one child only)' if PILOT else ''))
        if not PILOT:
            check(f'E8: vol(Voronoi cell) = 1 from root {v} (exact) => Omega(4_21; 0) = 8! = 40320', vol == 1)
    # vol(4_21)
    nf = len(N12); chunks = [list(range(i, nf, 64)) for i in range(64)] if not PILOT else [list(range(0, nf, 997))]
    with ctx.Pool(CORES) as pool: parts = pool.map(e8_vol421_task, chunks)
    if not PILOT:
        v421 = sum(parts, Fr(0)) / math.factorial(8); say(f'vol(4_21), roots of norm 2: {v421} = {float(v421):.12f}')
        a7 = Fr(abs(det_int([R2[i] for i in bits(E8['inc_f'][2160])])), 2 ** 8 * math.factorial(8))
        check(f'E8: vol(4_21) = 17280 alpha7 cones ({a7} each) + 2160 beta7 cones; Mahler product vol(4_21) vol(Voronoi) = vol(4_21) < ball bound (pi^4/24)^2 = {(math.pi**4/24)**2:.6f}', float(v421) < (math.pi ** 4 / 24) ** 2)
        say(f'Omega(Voronoi E8; 0) = 8! vol(4_21) = {v421 * 40320}; Mahler/ball = {float(v421) / (math.pi**4/24)**2:.6f}')
    say(f'PROGRESS 0.75 E8 ({time.time()-T0:.0f} s)')

    # ---------- icosian / H4 ----------
    Ric, Rstd, to_q = ico_setup()
    Rq = [to_q(r) for r in Rstd]
    check('icosian map: the 240 standard roots go exactly onto the 240 icosian roots (120 units + 120 units/phi)', {key(q) for q in Rq} == {key(q) for q in Ric})
    pairs = [(0, j) for j in range(240)] + [(5, 77), (100, 200), (13, 239)]
    check('icosian map is an isometry: B(q(x), q(y)) = x.y on 243 pairs (exact)', all(Bic(Rq[i], Rq[j]) == dotg(Rstd[i], Rstd[j]) for i, j in pairs))
    Nstd = [tuple(Fr(x, 12) for x in n) for n in (N12 if not PILOT else N12[:2160] + N12[2160::40])]
    Nq = [to_q(n) for n in Nstd]
    check('icosian map: B(q(n), q(r)) <= 1 with equality exactly on incidences (sample of 50 x 240, exact)',
          all(Bic(Nq[i], Rq[j]) == dotg(Nstd[i], Rstd[j]) for i in range(0, len(Nq), max(1, len(Nq) // 50)) for j in range(240)))
    def dedup(P):
        d = {}
        for p in P: d.setdefault(key(p), p)
        return list(d.values())
    sets = [('shadow of 4_21 in E_par (roots q)', dedup(Rq)), ('shadow of 4_21 in E_perp (roots sigma q)', dedup([tuple(x.sig() for x in q) for q in Rq]))]
    sets += [('window W_perp = pi_perp(Voronoi)', dedup([tuple(x.sig() for x in q) for q in Nq])), ('twin window W_par = pi_par(Voronoi)', dedup(Nq))]
    with ctx.Pool(min(CORES, 4)) as pool: H = pool.map(hull4_task, sets)
    cpar, cperp = Q5(1, Fr(1, 5)), Q5(1, Fr(-1, 5))        # metric on E_par / E_perp in q coordinates = c * Euclid (c = 2 w1, 2 w2)
    for h in H:
        say(f"{h['label']}: {h['nv']} vertices (squared radii {h['radii2']}), {h['nf']} facets (vertices per facet {h['facet_sizes']}); "
            f"vol_coord = {h['vol']} = {h['vol'].f():.10f}; vol_coord(polar) = {h['volpolar']} = {h['volpolar'].f():.10f}; F1 {h['nT']} / F2 {h['nS']} simplices")
        say(f"   vertices by squared radius: {h['vert_orbits']}; facets per vertex: {h['vdeg']}; polar vertices (squared radius, vertices of the dual facet): {h['polar_orbits']}")
        check(f"{h['label']}: exact volumes = qhull (1e-9)", abs(h['vol'].f() - h['qhull'][0]) < 1e-9 and abs(h['volpolar'].f() - h['qhull'][1]) < 1e-9)
        if 'F1F2' in h:
            check(f"{h['label']}: F1 = F2 at a generic Q(sqrt5) point (exact)", all(h['F1F2']))
            check(f"NEG {h['label']}: one F1 term sign-flipped breaks F1 = F2", h['neg_flip'])
    sp, spp, Wp, Wq = H
    # 600-cell control
    check('E_par shadow = 600-cell of radius 1 (120 vertices, 600 tetrahedra)', sp['nv'] == 120 and sp['nf'] == 600 and sp['facet_sizes'] == [4] and sp['radii2'] == [Q5(1)])
    Np = sp['N']; e2 = min((dotg(tuple(a - b for a, b in zip(Np[0], Np[j])), tuple(a - b for a, b in zip(Np[0], Np[j]))) for j in range(1, len(Np))), key=lambda x: x.f())
    closed = Q5(Fr(15, 4)) * Q5(105, 47) * e2 * e2
    check(f'600-cell: Omega(0) = 4! vol(polar) and the polar is a 120-cell: vol = (15/4)(105+47 sqrt5) a^4 with a^2 = {e2} (exact)', sp['volpolar'] == closed)
    say(f"Omega_coord(600-cell; 0) = 24 vol(120-cell) = {24 * sp['volpolar']} = {(24 * sp['volpolar']).f():.10f}")
    check('E_perp shadow = 600-cell of radius phi (the twin of the 1/phi cell)', spp['nv'] == 120 and spp['nf'] == 600 and spp['radii2'] == [PHI * PHI])
    for h, c, side in ((sp, cpar, 'par'), (spp, cperp, 'perp')):
        Om = 24 * h['volpolar'] / (c * c); vv = h['volpolar'] * c * c / (c * c * c * c)
        say(f"{h['label']}: Omega_true(shadow; 0) = 4! vol(Voronoi cap E_{side}) = {Om} = {Om.f():.10f}; vol_true(Voronoi cap E_{side}) = {Om / 24} (a 120-cell); vol_true(shadow) = {c * c * h['vol']} = {(c * c * h['vol']).f():.10f}")
    # true-metric values
    for h, c, side in ((Wp, cperp, 'perp'), (Wq, cpar, 'par')):
        vt = c * c * h['vol']; Om = 24 * h['volpolar'] / (c * c)
        say(f"{h['label']}: true volume = density of the quasicrystal = {vt} = {vt.f():.12f}; Omega_true(W; 0) = 4! vol(4_21 cap E_{side}) = {Om} = {Om.f():.10f}; "
            f"Omega_true(4_21 cap E_{side}; 0) = 4! density = {24 * vt} = {(24 * vt).f():.10f}")
        h['dens'] = vt
    say(f'PROGRESS 0.90 H4 ({time.time()-T0:.0f} s)')
    # ---------- density by counting (numerical) ----------
    if not PILOT:
        X = e8_points_upto(26)
        Sm = np.array([[float(x) for x in s] for s in [r for r in Rstd]])
        # float linear map standard -> (q, sigma q) through the exact map of a basis
        B = [tuple(Fr(1 if i == j else 0) for j in range(8)) for i in range(8)]
        Mq = np.array([[x.f() for x in to_q(b)] for b in B]); Ms = np.array([[x.sig().f() for x in to_q(b)] for b in B])
        qp, qs = X @ Mq, X @ Ms
        for h, coords, other, cin, cout, lab in ((Wp, qs, qp, cperp, cpar, 'W_perp'), (Wq, qp, qs, cpar, cperp, 'W_par')):
            Nf = np.array([[x.f() for x in n] for n in h['N']]); rmax = max(v_.f() for v_ in h['radii2'])
            cand = np.where(((coords * coords).sum(1) <= rmax + 1e-9) & (cout.f() * (other * other).sum(1) <= 25 + 1e-9))[0]
            inside = np.zeros(len(coords), bool); insh = np.zeros(len(coords), bool)
            gam = np.random.default_rng(23).normal(size=4) * 1e-3
            for i0 in range(0, len(cand), 20000):
                cc = cand[i0:i0 + 20000]; inside[cc] = (coords[cc] @ Nf.T <= 1 + 1e-9).all(1)
                insh[cc] = ((coords[cc] - gam) @ Nf.T <= 1).all(1)
            mg = np.abs(((coords[cand] - gam) @ Nf.T) - 1).min()
            say(f'{lab}: closest lattice point to the shifted window boundary: {mg:.2e} (generic shift, no ties)')
            for R2_ in (9.0, 16.0, 25.0):
                r2 = cout.f() * (other * other).sum(1)
                cnt_ = int((inside & (r2 <= R2_)).sum()); exp_ = h['dens'].f() * math.pi ** 2 / 2 * R2_ ** 2; cs = int((insh & (r2 <= R2_)).sum())
                say(f'{lab}: lattice points with |par| <= {R2_**0.5:.0f}: closed window {cnt_} (ratio {cnt_/exp_:.4f}; boundary points have positive density), generically shifted window {cs} (ratio {cs/exp_:.4f}); density x ball = {exp_:.1f}')
            check(f'{lab}: shifted-window count / (density x ball) within 5% at radius 5 (numerical)', abs(cs / exp_ - 1) < 0.05); h['cnt25'] = cnt_; cnt_ = cs
            wrong = (h['dens'] / (cin * cin) * (cout * cout)).f() * math.pi ** 2 / 2 * 625
            check(f'NEG {lab}: scale factors swapped predicts {wrong:.0f}, off by more than 30%', abs(cnt_ / wrong - 1) > 0.30)
        Nsh = np.array([[x.f() for x in n] for n in spp['N']]); ins2 = np.zeros(len(qs), bool)
        cand = np.where(((qs * qs).sum(1) <= PHI.f() ** 2 + 1e-9) & (cpar.f() * (qp * qp).sum(1) <= 25 + 1e-9))[0]
        for i0 in range(0, len(cand), 20000):
            cc = cand[i0:i0 + 20000]; ins2[cc] = (qs[cc] @ Nsh.T <= 1 + 1e-9).all(1)
        r2 = cpar.f() * (qp * qp).sum(1); cnt2 = int((ins2 & (r2 <= 25)).sum())
        check(f"NEG window = shadow of the roots (600-cell of radius phi) instead of pi_perp(Voronoi): count {cnt2} vs {Wp['cnt25']}, ratio {cnt2/Wp['cnt25']:.3f} (must differ by > 15%)", abs(cnt2 / Wp['cnt25'] - 1) > 0.15)
        # Fibonacci control
        ph = (1 + 5 ** 0.5) / 2; e = np.array([ph, 1]) / math.hypot(ph, 1); f_ = np.array([-1, ph]) / math.hypot(ph, 1)
        sq = np.array([[a, b] for a in (-.5, .5) for b in (-.5, .5)]) @ f_; w = sq.max() - sq.min()
        g = np.array(list(itertools.product(range(-400, 401), repeat=2)))
        par, perp = g @ e, g @ f_; c1 = int(((perp >= sq.min()) & (perp <= sq.max()) & (np.abs(par) <= 200)).sum())
        check(f'Fibonacci control: Z^2 points in the window per unit length = |W| = {w:.6f} (count {c1}, expected {400*w:.1f}, 1%)', abs(c1 / (400 * w) - 1) < 0.01)
    say(f'PROGRESS 1.00 done ({time.time()-T0:.0f} s)')
    print('FINAL ok' if OK else 'FINAL FAIL', flush=True)

if __name__ == '__main__':
    main()
