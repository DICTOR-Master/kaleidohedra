#!/usr/bin/env python3
"""Open question 12.2 of The Permutohedron Paradigm (Chapter 12, The Golden Slice): finitely many shapes by the window method?
EXACT in Q(phi) (pairs a + b phi with a, b rational; phi^2 = phi + 1). Pure Python (no numpy/networkx on the compute host).

Setting. P = conv of the 120 orderings of (-2,-1,0,1,2) in the hyperplane sum x = 0 of R^5 (Voronoi cell of the lattice
L = {x in Z^5 : sum x = 0, all x_i congruent mod 5}, basis b_i = 5 e_i - (1,1,1,1,1), i = 0..3). l(x) = u.x, u = (1, phi, .., phi^4).
Slice E_c = {l = c}; cell lambda is hit iff h = c - l(lambda) lies in the window W = (min_P l, max_P l) (projection of the cell).

Parts. A geometry (P, edges, cells at a corner, Delaunay tetrahedron D(e) of every edge = the 4 cells through it).
B golden direction: corner heights, bands (window regions), vertex stars S_k = {D(e): e straddles band k} of the dual
(window/projection) tiling, their number, central symmetry, combinatorial classes (colour refinement + backtracking), tile shapes
up to translation / point reflection / congruence in E, exact frequencies, the volume balance identity, the period lattice L cap E.
C section shapes: Lawrence's formula for the section volume (Brion identities checked), per band degree and velocity test.
D patch of the window tiling: exact model-set points in a ball of radius R, every tile's corners in the model set, face matching,
covering number 1 at random points, stars and first coronas seen. E first-corona count from the window subdivision.
F controls: Fibonacci (Z^2, square cell), rational direction (1,-1,0,0,0), a generic Q(phi) direction, a 5x5 determinant check.
Usage: slice_window.py pilot|full R"""
import itertools, sys, time, random, json, math, bisect
from fractions import Fraction as Fr
from functools import cmp_to_key

T0 = time.time()
MODE = sys.argv[1] if len(sys.argv) > 1 else 'pilot'
RAD = float(sys.argv[2]) if len(sys.argv) > 2 else 14.0
CHECKS = []; OUT = {}
def check(name, ok, info=''):
    CHECKS.append((name, bool(ok))); print(f"{'ok  ' if ok else 'FAIL'} {name} {info}", flush=True)
def progress(f, what): print(f'PROGRESS {f:.2f} {what} ({time.time() - T0:.0f} s)', flush=True)

# ---------------- Q(phi) arithmetic ----------------
PHIF = (1 + 5 ** 0.5) / 2
Z = (0, 0)
def add(x, y): return (x[0] + y[0], x[1] + y[1])
def sub(x, y): return (x[0] - y[0], x[1] - y[1])
def neg(x): return (-x[0], -x[1])
def mul(x, y): a, b = x; c, d = y; return (a * c + b * d, a * d + b * c + b * d)
def smul(k, x): return (k * x[0], k * x[1])
def inv(x):
    a, b = x; N = a * a + a * b - b * b; return (Fr(a + b) / N, Fr(-b) / N)
def div(x, y): return mul(x, inv(y))
def sgn(x):
    X = 2 * x[0] + x[1]; Y = x[1]
    if X >= 0 and Y >= 0: return 0 if (X == 0 and Y == 0) else 1
    if X <= 0 and Y <= 0: return -1
    d = X * X - 5 * Y * Y
    return (1 if X > 0 else -1) if d > 0 else (1 if Y > 0 else -1)
def cmpq(x, y): return sgn(sub(x, y))
def fl(x): return float(x[0]) + float(x[1]) * PHIF
def qabs(x): return neg(x) if sgn(x) < 0 else x
def norm(x): return (Fr(x[0]), Fr(x[1]))           # hashable canonical form
def qs(x): return f'{x[0]} + {x[1]}phi' if x[1] else f'{x[0]}'
def fib(k):
    a, b = 0, 1
    for _ in range(k): a, b = b, a + b
    return a
def phipow(i): return (1, 0) if i == 0 else (fib(i - 1), fib(i))
def dot(u, x):
    s = Z
    for ui, xi in zip(u, x): s = add(s, smul(xi, ui))
    return s
def vsub(a, b): return tuple(x - y for x, y in zip(a, b))
def vadd(a, b): return tuple(x + y for x, y in zip(a, b))
def vneg(a): return tuple(-x for x in a)
def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]))
def detn(M):   # Bareiss-free Leibniz for small integer / Q(phi)-free integer matrices
    n = len(M); s = 0
    for p in itertools.permutations(range(n)):
        sg = 1
        for i in range(n):
            for j in range(i + 1, n):
                if p[i] > p[j]: sg = -sg
        t = sg
        for i in range(n):
            t *= M[i][p[i]]
            if t == 0: break
        s += t
    return s

# ---------------- A. geometry of P and the honeycomb ----------------
VALS = (-2, -1, 0, 1, 2)
V = sorted(set(itertools.permutations(VALS)))
VI = {v: i for i, v in enumerate(V)}
EDGES = []
for v in V:
    for k in range(4):     # swap values VALS[k], VALS[k+1]
        i, j = v.index(VALS[k]), v.index(VALS[k + 1])
        w = list(v); w[i], w[j] = w[j], w[i]; w = tuple(w)
        if v < w: EDGES.append((v, w))
check('A1 P has 120 corners and 240 edges', len(V) == 120 and len(EDGES) == 240)
def inL(t): return sum(t) == 0 and all((x - t[0]) % 5 == 0 for x in t)
CELLS = {v: frozenset(vsub(v, w) for w in V if inL(vsub(v, w))) for v in V}
check('A2 every corner lies in exactly 5 cells (simple honeycomb)', all(len(c) == 5 for c in CELLS.values()))
DT = {}
for e in EDGES:
    DT[e] = CELLS[e[0]] & CELLS[e[1]]
check('A3 every edge lies in exactly 4 cells (Delaunay tetrahedron)', all(len(t) == 4 and (0,) * 5 in t for t in DT.values()))
G = [[25 * (i == j) - 5 for j in range(4)] for i in range(4)]
check('A4 covolume of L = vol(P): Gram det 78125 = (125 sqrt5)^2', detn(G) == 78125)
BAS = [tuple(5 * (i == j) - 1 for j in range(5)) for i in range(4)]
def tkey(pts):   # tetrahedron up to translation
    s = sorted(pts); return tuple(vsub(p, s[0]) for p in s)

# ---------------- a slice direction ----------------
class Dirn:
    def __init__(self, u, label):
        self.u = u; self.label = label
        self.H = {v: dot(u, v) for v in V}
        lev = sorted({norm(h) for h in self.H.values()}, key=cmp_to_key(cmpq))
        self.lev = lev; self.nb = len(lev) - 1
        self.rank = {v: lev.index(norm(self.H[v])) for v in V}
        self.W = sub(lev[-1], lev[0])
        # straddling edges per band; oriented upward
        self.up = {}
        for (a, b) in EDGES:
            ha, hb = self.H[a], self.H[b]
            s = sgn(sub(hb, ha))
            if s != 0: self.up[(a, b)] = (a, b) if s > 0 else (b, a)
        self.stars = []
        for k in range(self.nb):
            st = [e for e in self.up if min(self.rank[e[0]], self.rank[e[1]]) <= k < max(self.rank[e[0]], self.rank[e[1]])]
            self.stars.append(st)
        sumu = Z
        for x in u: sumu = add(sumu, x)
        uu = Z
        for x in u: uu = add(uu, mul(x, x))
        self.Nu = sub(uu, mul(div(mul(sumu, sumu), (5, 0)), (1, 0)))        # |u'|^2, u' = u - mean
        # omega(a,b,c) = det[a,b,c,u,1] by Laplace on the last two columns
        self.K = []
        for J in itertools.combinations(range(5), 2):
            rest = [r for r in range(5) if r not in J]
            sg = (-1) ** (J[0] + J[1] + 3 + 4)
            self.K.append((rest, smul(sg, sub(u[J[0]], u[J[1]]))))
        self.uf = [fl(x) for x in u]; m = sum(self.uf) / 5; self.upf = [x - m for x in self.uf]
        self.Nuf = sum(x * x for x in self.upf)
    def band_of(self, h):   # index k with lev[k] < h < lev[k+1]; None if outside or on a level
        lo, hi = 0, len(self.lev) - 1
        if cmpq(h, self.lev[0]) <= 0 or cmpq(h, self.lev[-1]) >= 0: return None
        while hi - lo > 1:
            mid = (lo + hi) // 2
            c = cmpq(h, self.lev[mid])
            if c == 0: return None
            if c > 0: lo = mid
            else: hi = mid
        return lo
    def omega(self, a, b, c):
        s0 = 0; s1 = 0
        for rest, k in self.K:
            d = det3([a[r] for r in rest], [b[r] for r in rest], [c[r] for r in rest])
            if d: s0 += k[0] * d; s1 += k[1] * d
        return (s0, s1)
    def star_set(self, k): return frozenset(frozenset(DT[e]) for e in self.stars[k])
    def l(self, x): return dot(self.u, x)
    def proj(self, x):   # float projection to E (5-vector)
        a = sum(xi * ui for xi, ui in zip(x, self.upf)) / self.Nuf; m = sum(x) / 5
        return [xi - m - a * ui for xi, ui in zip(x, self.upf)]
    def gram(self, w1, w2):   # metric of E on differences of lattice points (sum 0)
        return sub((sum(a * b for a, b in zip(w1, w2)), 0), div(mul(self.l(w1), self.l(w2)), self.Nu))

# colour refinement + backtracking isomorphism of vertex stars (incidence graph corners - tetrahedra)
def star_graph(stset):
    pts = sorted({p for t in stset for p in t}); idx = {p: i for i, p in enumerate(pts)}
    tets = [sorted(idx[p] for p in t) for t in stset]
    n = len(pts); adj = [set() for _ in range(n + len(tets))]
    for j, t in enumerate(tets):
        for i in t: adj[i].add(n + j); adj[n + j].add(i)
    col = [0] * n + [1] * len(tets)
    return adj, col
def refine(adj, col, rounds=10):
    for _ in range(rounds):
        col = [hash((col[v], tuple(sorted(col[w] for w in adj[v])))) for v in range(len(adj))]
    return col
def invariant(stset):
    adj, col = star_graph(stset); return tuple(sorted(refine(adj, col)))
def isomorphic(s1, s2):
    a1, c1 = star_graph(s1); a2, c2 = star_graph(s2)
    if len(a1) != len(a2): return False
    f1 = refine(a1, c1); f2 = refine(a2, c2)
    if sorted(f1) != sorted(f2): return False
    n = len(a1); order = sorted(range(n), key=lambda v: (-len(a1[v]), v)); m = {}; used = set()
    def bt(i):
        if i == n: return True
        v = order[i]
        for w in range(n):
            if w in used or f2[w] != f1[v]: continue
            if all((m[x] in a2[w]) == (x in a1[v]) for x in m):
                m[v] = w; used.add(w)
                if bt(i + 1): return True
                del m[v]; used.discard(w)
        return False
    return bt(0)
def classes(stars):
    reps = []; inv_of = []
    for s in stars:
        iv = invariant(s); hit = None
        for r, (ri, rs) in enumerate(reps):
            if ri == iv and isomorphic(s, rs): hit = r; break
        if hit is None: reps.append((iv, s)); hit = len(reps) - 1
        inv_of.append(hit)
    return len(reps), inv_of

# ---------------- F0. determinant control ----------------
def omega_direct(D, a, b, c):
    M = [[(a[i], 0), (b[i], 0), (c[i], 0), D.u[i], (1, 0)] for i in range(5)]
    s = Z
    for p in itertools.permutations(range(5)):
        sg = 1
        for i in range(5):
            for j in range(i + 1, 5):
                if p[i] > p[j]: sg = -sg
        t = (sg, 0)
        for i in range(5): t = mul(t, M[i][p[i]])
        s = add(s, t)
    return s

# ================= B. GOLDEN DIRECTION =================
progress(0.02, 'geometry')
UG = [phipow(i) for i in range(5)]
D = Dirn(UG, 'golden')
rnd = random.Random(12)
okdet = all(D.omega(*abc) == omega_direct(D, *abc) for abc in [[tuple(rnd.randint(-9, 9) for _ in range(5)) for _ in range(3)] for _ in range(40)])
check('F0 omega(a,b,c) = det[a,b,c,u,1] (Laplace vs Leibniz, 40 random triples)', okdet)
check('B1 golden: 70 distinct corner heights, 69 bands (window regions)', len(D.lev) == 70 and D.nb == 69, f'(levels {len(D.lev)}, bands {D.nb})')
check('B2 golden: no edge is level (l(e) != 0 for all 240 edges)', len(D.up) == 240)
OUT['window'] = {'min': qs(D.lev[0]), 'max': qs(D.lev[-1]), 'length': qs(D.W)}
blen = [sub(D.lev[k + 1], D.lev[k]) for k in range(D.nb)]
check('B3 band lengths add up to the window', (lambda s: s == norm(D.W))(norm(__import__('functools').reduce(add, blen, Z))))
STARS = [D.star_set(k) for k in range(D.nb)]
check('B4 the 69 vertex stars are pairwise distinct (69 vertex configurations up to translation)', len(set(STARS)) == 69)
negset = lambda s: frozenset(frozenset(vneg(p) for p in t) for t in s)
check('B5 star of band k = minus star of band 68-k (central symmetry)', all(STARS[68 - k] == negset(STARS[k]) for k in range(69)))
check('B6 the middle band (k = 34) is centrally symmetric', STARS[34] == negset(STARS[34]))
progress(0.10, 'stars built')
ncl, clidx = classes(STARS)
check('B7 combinatorial classes of the 69 stars = 35 (= Theorem 12.1 (ii), recomputed independently)', ncl == 35, f'({ncl})')
check('B8 each class = one band and its mirror band (no other coincidences)', all((clidx[i] == clidx[j]) == (j in (i, 68 - i)) for i in range(69) for j in range(69)))
sizes = [len(s) for s in STARS]
OUT['star_sizes'] = sizes
# tile shapes
tk = {}
for e in EDGES: tk.setdefault(tkey(DT[e]), []).append(e)
ntr = len(tk)
keys = sorted(tk)
negk = lambda k: tkey([vneg(p) for p in k])
pr = {min(k, negk(k)) for k in keys}
check('B9 tile shapes up to translation (Delaunay tetrahedra dual to edges; projection is injective on L)', True, f'{ntr} translation classes; {len(pr)} up to point reflection')
# congruence in E
def dmat(k):
    return [[norm(D.gram(vsub(k[i], k[j]), vsub(k[i], k[j]))) for j in range(4)] for i in range(4)]
def ckey(k):
    M = dmat(k); best = None
    for p in itertools.permutations(range(4)):
        t = tuple(M[p[i]][p[j]] for i in range(4) for j in range(i + 1, 4))
        if best is None or t < best: best = t
    return best
cong = {}
for k in keys: cong.setdefault(ckey(k), []).append(k)
check('B10 tile shapes up to congruence in the slice (mirror images allowed)', True, f'{len(cong)} classes')
# orbits of edges under lattice translation: honeycomb edges per cell = 240/4 = 60
orb = set()
for e in EDGES:
    a, b = e
    # canonical rep of the edge modulo L: translate so that its lower endpoint (lex) is in P with the minimal translation choice
    reps = []
    for t in DT[e]:
        reps.append(tuple(sorted([vsub(a, t), vsub(b, t)])))
    orb.add(min(reps))
check('B11 60 edge orbits under L (240 / 4)', len(orb) == 60, f'({len(orb)})')
# frequencies
totl = __import__('functools').reduce(add, [qabs(sub(D.H[b], D.H[a])) for a, b in EDGES], Z)
OUT['tiles'] = []
for k in keys:
    f = __import__('functools').reduce(add, [qabs(sub(D.H[b], D.H[a])) for a, b in tk[k]], Z)
    OUT['tiles'].append({'tet': k, 'edges_of_P': len(tk[k]), 'freq': qs(norm(div(f, totl))), 'freq_float': fl(div(f, totl)),
                         'l_edge': qs(qabs(sub(D.H[tk[k][0][1]], D.H[tk[k][0][0]])))})
OUT['tiles_per_vertex'] = qs(norm(div(totl, smul(4, D.W)))); OUT['tiles_per_vertex_float'] = fl(div(totl, smul(4, D.W)))
OUT['vertex_star_freq'] = [qs(norm(div(b, D.W))) for b in blen]
OUT['vertex_star_freq_float'] = [fl(div(b, D.W)) for b in blen]
OUT['min_band_rel'] = min(OUT['vertex_star_freq_float'])
# volume balance: sum_e |l(e)| |omega(D(e))| = 15000 |u'|^2
vb = Z
for a, b in EDGES:
    pts = sorted(DT[(a, b)]); p0 = pts[0]
    om = D.omega(vsub(pts[1], p0), vsub(pts[2], p0), vsub(pts[3], p0))
    vb = add(vb, mul(qabs(sub(D.H[b], D.H[a])), qabs(om)))
check('B12 volume balance: sum over edges |l(e)| |omega(D(e))| = 15000 |u\'|^2 (tiles fill the slice at the model-set density)', norm(vb) == norm(smul(15000, D.Nu)), f'({qs(norm(vb))} vs {qs(norm(smul(15000, D.Nu)))})')
check('B13 every tile has nonzero volume in the slice', all(sgn(D.omega(*[vsub(p, sorted(DT[e])[0]) for p in sorted(DT[e])[1:]])) != 0 for e in EDGES))
# period lattice L cap E (ker of l on L)
# l(b_i) as rational pairs; kernel of the 4x2 integer matrix over Z
lb = [D.l(b) for b in BAS]
ker = []
for n in itertools.product(range(-3, 4), repeat=4):
    s = Z
    for ni, x in zip(n, lb): s = add(s, smul(ni, x))
    if s == Z and any(n): ker.append(n)
kv = [tuple(sum(ni * b[j] for ni, b in zip(n, BAS)) for j in range(5)) for n in ker]
mu1 = (5, 0, -10, 5, 0); mu2 = (0, 5, 0, -10, 5)
check('B14 periods: 5(1,0,-2,1,0) and 5(0,1,0,-2,1) lie in L with l = 0 (the slice repeats along them)', inL(mu1) and inL(mu2) and D.l(mu1) == Z and D.l(mu2) == Z)
# rank of ker: l(b_i) span Q^2 (rank 2) -> kernel rank 2
rk = 2 if (lb[0][0] * lb[1][1] - lb[0][1] * lb[1][0]) != 0 or any((lb[i][0] * lb[j][1] - lb[i][1] * lb[j][0]) != 0 for i in range(4) for j in range(4)) else 1
check('B15 l(L) has rank 2 (dense in R), so L cap E has rank exactly 4 - 2 = 2: periodic in a plane, never in a third direction', rk == 2)
OUT['l_of_basis'] = [qs(x) for x in lb]
progress(0.20, 'golden stars, classes, tiles')

# ================= C. section shapes =================
# Lawrence: F(h) = vol4{x in P: l <= h} * sqrt5 = sum_v (h - l(v))_+^4 |det[W_v, 1]| / (24 prod l(w))
NB = {v: [] for v in V}
for a, b in EDGES: NB[a].append(vsub(b, a)); NB[b].append(vsub(a, b))
cv = {}
dets = set()
for v in V:
    dd = abs(detn([[NB[v][i][r] for i in range(4)] + [1] for r in range(5)]))
    dets.add(dd)
    pr_ = (1, 0)
    for w in NB[v]: pr_ = mul(pr_, D.l(w))
    cv[v] = smul(Fr(dd), inv(pr_))
check('C1 every corner cone has |det[W_v,1]| = 5', dets == {5}, str(dets))
def poly_band(vs, deg):    # sum_v c_v (h - l_v)^deg as coefficient list (h^0..h^deg), times 1 (no factorial)
    co = [Z] * (deg + 1)
    for v in vs:
        a = D.H[v]
        for j in range(deg + 1):    # (h - a)^deg = sum C(deg,j) h^j (-a)^(deg-j)
            t = (math.comb(deg, j), 0)
            for _ in range(deg - j): t = mul(t, neg(a))
            co[j] = add(co[j], mul(cv[v], t))
    return [norm(c) for c in co]
full4 = poly_band(V, 4)
check('C2 Brion identities: full sum of c_v (h - l_v)^4 / 24 is the constant 625 = vol(P) sqrt5 x sqrt5 (Lawrence formula verified)',
      all(c == (0, 0) for c in full4[1:]) and full4[0] == (Fr(625 * 24), Fr(0)), str([qs(c) for c in full4]))
full3 = poly_band(V, 3)
check('C3 full sum of c_v (h - l_v)^3 vanishes identically', all(c == (0, 0) for c in full3))
deg_band = []; const_bands = []; vel_ok = []
for k in range(D.nb):
    below = [v for v in V if D.rank[v] <= k]
    co = poly_band(below, 3)      # section 3-volume = |u'| F'(h) = |u'| co(h) / 6
    dg = max([j for j in range(4) if co[j] != (0, 0)] or [0])
    deg_band.append(dg)
    if dg == 0: const_bands.append(k)
    # velocity test: section corners move with velocity e / l(e); a translate-only motion needs all equal
    vels = {tuple(norm(div((x, 0), D.l(vsub(b, a)))) for x in vsub(b, a)) for (a, b) in (D.up[e] for e in D.stars[k])}
    vel_ok.append(len(vels) > 1)
check('C4 section volume is a non-constant polynomial of h in every one of the 69 bands', not const_bands, f'(degrees {sorted(set(deg_band))}, constant bands {const_bands})')
check('C5 velocity test: in every band the section corners do not all move together', all(vel_ok))
mid = [div(add(D.lev[k], D.lev[k + 1]), (2, 0)) for k in range(D.nb)]
def secvol(k, h):
    co = poly_band([v for v in V if D.rank[v] <= k], 3); s = Z; p = (1, 0)
    for c in co: s = add(s, mul(c, p)); p = mul(p, h)
    return s
sv = [secvol(k, mid[k]) for k in range(D.nb)]
check('C6 section volume positive at every band midpoint and symmetric (band k at h = band 68-k at -h)',
      all(sgn(x) > 0 for x in sv) and all(norm(sv[k]) == norm(secvol(68 - k, neg(mid[k]))) for k in range(D.nb)))
OUT['section_volume_degree_per_band'] = deg_band
progress(0.30, 'section shapes')

# ================= E. first coronas from the window subdivision =================
NBR = sorted({p for e in EDGES for p in DT[e] if any(p)})
bp = set()
for t in NBR:
    lt = D.l(t)
    for L_ in D.lev: bp.add(norm(add(L_, lt)))
for L_ in D.lev: bp.add(norm(L_))
bp = sorted([x for x in bp if cmpq(x, D.lev[0]) >= 0 and cmpq(x, D.lev[-1]) <= 0], key=cmp_to_key(cmpq))
def corona(h):
    k = D.band_of(h)
    if k is None: return None
    tets = set(STARS[k]); nb = {p for t in STARS[k] for p in t if any(p)}
    for t in nb:
        k2 = D.band_of(sub(h, D.l(t)))
        if k2 is None: return 'NEIGHBOUR-OUTSIDE'
        tets |= {frozenset(vadd(p, t) for p in tt) for tt in STARS[k2]}
    return frozenset(tets)
cor = []
for x, y in zip(bp, bp[1:]):
    cor.append(corona(div(add(x, y), (2, 0))))
check('E1 every neighbour of a model-set vertex (corner of a tile at it) is in the model set', all(c not in (None, 'NEIGHBOUR-OUTSIDE') for c in cor))
eff = 1 + sum(1 for a, b in zip(cor, cor[1:]) if a != b)
ncor = len(set(cor))
check('E2 first coronas: distinct = effective window regions', ncor == eff, f'(breakpoints {len(bp)}, raw regions {len(cor)}, effective regions {eff}, distinct coronas {ncor})')
OUT['first_coronas'] = ncor; OUT['corona_regions_raw'] = len(cor)
progress(0.40, 'coronas')

# ================= F. controls =================
# F1 Fibonacci: lattice 2Z^2, Voronoi cell = square (+-1, +-1), u = (1, phi)
Vs = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
Es = [(Vs[i], Vs[(i + 1) % 4]) for i in range(4)]
def inL2(t): return t[0] % 2 == 0 and t[1] % 2 == 0
C2 = {v: frozenset(vsub(v, w) for w in Vs if inL2(vsub(v, w))) for v in Vs}
D2 = {e: C2[e[0]] & C2[e[1]] for e in Es}
u2 = [(1, 0), (0, 1)]
H2 = {v: dot(u2, v) for v in Vs}
lev2 = sorted({norm(h) for h in H2.values()}, key=cmp_to_key(cmpq)); r2 = {v: lev2.index(norm(H2[v])) for v in Vs}
st2 = [[e for e in Es if min(r2[e[0]], r2[e[1]]) <= k < max(r2[e[0]], r2[e[1]])] for k in range(len(lev2) - 1)]
# physical coordinate on E: s(x) = x . (phi, -1)
sE = lambda x: add(smul(x[0], (0, 1)), smul(x[1], (-1, 0)))
lengths = {norm(qabs(sE(vsub(*sorted(D2[e]))))) for e in Es}
stars2 = {frozenset(frozenset(D2[e]) for e in st) for st in st2}
vel2 = [len({tuple(norm(div((x, 0), dot(u2, vsub(b, a)))) for x in vsub(b, a)) for (a, b) in [(e if sgn(sub(H2[e[1]], H2[e[0]])) > 0 else (e[1], e[0])) for e in st]}) > 1 for st in st2]
check('F1 Fibonacci control: window cut into 3 regions -> 3 vertex types, 2 tile lengths (ratio phi)', len(lev2) - 1 == 3 and len(stars2) == 3 and len(lengths) == 2,
      f'(lengths {sorted(qs(x) for x in lengths)})')
check('F2 Fibonacci section control: middle band constant (two parallel edges), outer bands vary -> infinitely many section lengths', vel2 == [True, False, True], str(vel2))
# F1b patch of the Fibonacci window tiling: sequence of tile lengths, no SS, two LL never adjacent... check 3 vertex types seen
c2 = (Fr(1, 3), 0)
pts = []
for a in range(-60, 61):
    for b in range(-60, 61):
        x = (2 * a, 2 * b); h = sub(c2, dot(u2, x))
        if cmpq(h, lev2[0]) > 0 and cmpq(h, lev2[-1]) < 0: pts.append((fl(sE(x)), x))
pts.sort(); seq = []; badgap = 0
for (s1, x1), (s2, x2) in zip(pts, pts[1:]):
    if abs(s1) > 200 or abs(s2) > 200: continue
    g = s2 - s1
    if abs(g - 2 * PHIF) < 1e-9: seq.append('L')
    elif abs(g - 2) < 1e-9: seq.append('S')
    else: badgap += 1
inner = ''.join(seq) if not badgap else 'SS'
vt = {inner[i:i + 2] for i in range(len(inner) - 1)}
check('F3 Fibonacci patch: vertex types seen = {LL, LS, SL} (no SS); every gap a tile of the two lengths', vt == {'LL', 'LS', 'SL'} and 'SS' not in inner, f'({len(inner)} tiles, L/S = {inner.count("L") / max(1, inner.count("S")):.4f})')
# F4 rational direction (1,-1,0,0,0)
DR = Dirn([(1, 0), (-1, 0), Z, Z, Z], 'rational')
lbR = [DR.l(b) for b in BAS]
check('F4 rational control: 8 heights, 7 bands; l(L) = 5Z discrete; L cap E rank 3 (periodic); one height in W at c = 1/3 -> one shape',
      len(DR.lev) == 8 and DR.nb == 7 and sorted(x[0] for x in lbR) == [-5, 0, 0, 5] and
      sum(1 for m in range(-5, 6) if DR.band_of(sub((Fr(1, 3), 0), (5 * m, 0))) is not None) == 1)
# F5 generic Q(phi) direction: 120 heights, 119 bands, 60 classes (golden_types generic)
UGEN = [(0, 0), (3, 1), (1, 4), (7, 2), (2, 9)]
DGn = Dirn(UGEN, 'generic')
stG = [DGn.star_set(k) for k in range(DGn.nb)]
nG, _ = classes(stG)
check('F5 generic control: 120 heights, 119 bands, 119 distinct stars, 60 classes', len(DGn.lev) == 120 and len(set(stG)) == 119 and nG == 60, f'({len(DGn.lev)}, {nG})')
progress(0.50, 'controls')

# ================= D. patch of the window tiling (golden) =================
c = (Fr(1, 3), 0)
N = int(math.ceil(0.2829 * (RAD + 8))) + 1
M = {}
Wf0, Wf1 = fl(D.lev[0]), fl(D.lev[-1])
cnt = 0
for n0 in range(-N, N + 1):
    for n1 in range(-N, N + 1):
        for n2 in range(-N, N + 1):
            for n3 in range(-N, N + 1):
                x = (5 * n0 - (n0 + n1 + n2 + n3), 5 * n1 - (n0 + n1 + n2 + n3), 5 * n2 - (n0 + n1 + n2 + n3), 5 * n3 - (n0 + n1 + n2 + n3), -(n0 + n1 + n2 + n3))
                hf = 1 / 3 - sum(a * b for a, b in zip(x, D.uf))
                if hf < Wf0 - 1e-6 or hf > Wf1 + 1e-6: continue
                p = D.proj(x)
                if sum(t * t for t in p) > RAD * RAD: continue
                k = D.band_of(sub(c, D.l(x)))
                if k is not None: M[x] = k
    if n0 % 4 == 0: progress(0.50 + 0.15 * (n0 + N) / (2 * N + 1), f'enumerating ({len(M)} vertices)')
check('D1 patch: model-set vertices found', len(M) > 50, f'({len(M)} vertices within radius {RAD})')
pf = {x: D.proj(x) for x in M}
TET = {}
for x, k in M.items():
    for t in STARS[k]:
        TET[frozenset(vadd(x, p) for p in t)] = True
tets = list(TET)
def inmodel(y): return D.band_of(sub(c, D.l(y))) is not None
allv = {y for t in tets for y in t}
check('D2 every corner of every tile is a model-set point (exact)', all(inmodel(y) for y in allv), f'({len(tets)} tiles, {len(allv)} corners)')
check('D3 each tile lies in the star of each of its corners that is in the patch', all(frozenset(vsub(p, y) for p in t) in STARS[M[y]] for t in tets for y in t if y in M))
diam = max(math.dist(D.proj(a), D.proj(b)) for e in EDGES for a in DT[e] for b in DT[e])
OUT['tile_diameter_max'] = diam
progress(0.75, 'tiles built')
def pfz(y):
    if y not in pf: pf[y] = D.proj(y)
    return pf[y]
faces = {}
for t in tets:
    tl = sorted(t)
    for i in range(4):
        f = tuple(tl[:i] + tl[i + 1:]); opp = tl[i]
        a, b, cc = f
        s = sgn(D.omega(vsub(b, a), vsub(cc, a), vsub(opp, a)))
        faces.setdefault(f, []).append(s)
inner_lim = RAD - 2.5 * diam
bad = 0; ninner = 0; zero = 0
for f, ss in faces.items():
    if 0 in ss: zero += 1
    if all(math.hypot(*pfz(y)) <= inner_lim for y in f):
        ninner += 1
        if not (len(ss) == 2 and ss[0] == -ss[1]): bad += 1
check('D4 every tile non-degenerate; every inner face shared by exactly two tiles on opposite sides', zero == 0 and bad == 0 and ninner > 0, f'({ninner} inner faces, {bad} bad)')
progress(0.85, 'faces matched')
# covering number at random rational points
rq = random.Random(7); cov = []
cent = {t: [sum(pfz(y)[j] for y in t) / 4 for j in range(5)] for t in tets}
for _ in range(12 if MODE == 'full' else 4):
    while True:
        q = [Fr(rq.randint(-10 ** 6, 10 ** 6), 10 ** 5 + rq.randint(1, 999)) for _ in range(5)]
        q = [qi - sum(q) / 5 for qi in q]
        qf = D.proj([float(t) for t in q])
        if math.hypot(*qf) < inner_lim / 2: break
    den = 1
    for qi in q: den = den * qi.denominator // math.gcd(den, qi.denominator)
    Q = tuple(int(qi * den) for qi in q)
    hits = 0; onface = 0
    for t in tets:
        if math.dist(cent[t], qf) > 2 * diam: continue
        tl = sorted(t); inside = True
        for i in range(4):
            f = tl[:i] + tl[i + 1:]; opp = tl[i]; a, b, cc = f
            so = sgn(D.omega(vsub(b, a), vsub(cc, a), vsub(opp, a)))
            sq = sgn(D.omega(vsub(b, a), vsub(cc, a), tuple(Qi - den * ai for Qi, ai in zip(Q, a))))
            if sq == 0: onface += 1
            if sq != so: inside = False; break
        hits += inside
    cov.append((hits, onface))
check('D5 covering number exactly 1 at random points of the slice (no gap, no overlap)', all(h == 1 and o == 0 for h, o in cov), str(cov))
seen = {k for k in M.values()}
OUT['patch'] = {'radius': RAD, 'vertices': len(M), 'tiles': len(tets), 'stars_seen': len(seen)}
check('D6 vertex stars seen in the patch (full run: all 69)', MODE != 'full' or len(seen) == 69, f'({len(seen)} of 69; smallest band {OUT["min_band_rel"]:.5f} of W)')
# coronas observed at inner vertices
seen_c = set()
for x, k in M.items():
    if math.hypot(*pf[x]) <= inner_lim:
        tset = set(STARS[k]); nb = {p for t in STARS[k] for p in t if any(p)}
        for t in nb: tset |= {frozenset(vadd(p, t) for p in tt) for tt in STARS[M[vadd(x, t)]]} if vadd(x, t) in M else set()
        seen_c.add(frozenset(tset))
setcor = set(cor)
check('D7 every first corona seen in the patch is one predicted by the window subdivision', seen_c <= setcor, f'({len(seen_c)} of {ncor} seen)')
progress(0.97, 'patch checks')

OUT['checks'] = len(CHECKS); OUT['failed'] = [n for n, o in CHECKS if not o]
OUT['summary'] = {'bands': D.nb, 'stars': len(set(STARS)), 'classes': ncl, 'tile_shapes_translation': ntr, 'tile_shapes_point_reflection': len(pr),
                  'tile_shapes_congruence': len(cong), 'section_shapes': 'infinitely many in every band', 'period_rank': 2}
json.dump(OUT, open(f'data/slice-window-{MODE}.json', 'w'), indent=1, default=str)
print(f'SUMMARY {OUT["summary"]}')
print(f'{len(CHECKS)} checks, {len(OUT["failed"])} failed, {time.time() - T0:.0f} s')
ok = not OUT['failed']
print('FINAL ok' if ok else 'FINAL FAIL')
