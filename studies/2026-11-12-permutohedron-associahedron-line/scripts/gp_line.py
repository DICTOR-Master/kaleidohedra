"""Aim 2 (geometry gives laws), 12 Nov 2026: a Hopscotch-style line from the permutohedron (the crystal) to the associahedron (the
law-giving shape) inside the deformation cone of generalized permutohedra (Postnikov 2009, "Permutohedra, associahedra, and beyond").

A generalized permutohedron in R^n:  P(z) = { x : sum_i x_i = z_[n],  sum_{i in S} x_i >= z_S  for every nonempty proper S }.
Coordinates u = (x_1, ..., x_{n-1}) (x_n eliminated); dimension d = n - 1.  Everything is EXACT (fractions.Fraction; sympy only
for the closed forms in the line parameter).

Lines (each a straight line in the facet heights z_S):
  A  Postnikov line: z = (1-t) z_Pi + t z_L, t in [0,1].  Pi = sum_{i<j} Delta_ij shifted to coordinates 1..n (z_Pi(S) = C(|S|+1,2));
     L = Loday's associahedron = sum over intervals Delta_[i,j] (Postnikov's y_I = 1 on intervals; z_L(S) = number of intervals in S).
     Interval heights agree at both ends, so only the non-interval facets move, each outward at speed D_S = z_Pi(S) - z_L(S).
  B  equal-speed line (Hopscotch style: every removed facet moves at the same speed): z_S(s) = z_Pi(S) - s for every
     non-interval S, interval heights fixed, s in [0, max D_S]; at the end only Loday's facets remain.
  C  ABHY line: z = (1-t) z_Pi + t z_A, A = the kinematic associahedron of Arkani-Hamed-Bai-He-Yan with chunk 4's own random c
     (studies/2026-11-12-abhy-associahedron, setup(N), N = n + 2), written as a generalized permutohedron (interval [i,j] <-> diagonal
     (i, j+2)), its non-interval heights its tight support values, translated so its vertex centroid is Pi's centre.
  Z  control line Pi0 -> cube: z = (1-t) C(|S|,2) + t #{i : i, i+1 in S} (graphic zonotopes of K_n -> path); must tile all along.

At every station: vertices (all d-subsets of the 2^n - 2 inequalities, exact), face lattice (closure of facet vertex sets), f-vector,
simple?, generalized permutohedron? (every edge parallel to some e_i - e_j), Venkov-McMullen parallelohedron test (centrally symmetric,
centrally symmetric facets, every belt of 4 or 6 facets), canonical form at the fixed interior point Y = centre of Pi (pulling
triangulation formula; Warren's vertex formula as an independent check where simple).
Walls: z is affine in the parameter p, so each candidate vertex (d-subset) is a vertex exactly on a closed p-interval; the type can
change only at the end points of these intervals; each candidate is checked by comparing the labelled face structure at the point and
on both sides.
CONTROLS (FINAL ok only if all hold): Pi passes the parallelohedron test, Loday and ABHY fail it, Z passes at every station;
Omega(Pi; centre) = 2^(n-1) n/(n-1)!; vertex counts n!, Catalan(n); greedy vertices = enumerated vertices on the generalized
permutohedron lines; Omega(L) = m_{n+2} with X = Loday facet values (mesh constants all 1); Omega(A) = chunk 4's amplitude at the
same point, a tree-dropped amplitude differs; triangulation = vertex formula where simple; Euler; Omega continuous across walls.
Usage: python -u gp_line.py n [json_out]"""
import itertools, json, sys, time, os, importlib.util
from fractions import Fraction as F
from math import comb, factorial
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ABHY = os.path.join(HERE, '..', '..', '2026-11-12-abhy-associahedron', 'scripts', 'abhy.py')
_spec = importlib.util.spec_from_file_location('abhy', ABHY); abhy = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(abhy)

n = int(sys.argv[1]); d = n - 1
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'data', f'gp-line-n{n}.json')
FULL = frozenset(range(1, n + 1))
SUBS = sorted((frozenset(c) for k in range(1, n) for c in itertools.combinations(range(1, n + 1), k)), key=lambda S: (len(S), sorted(S)))
M = len(SUBS)
lab = lambda S: ''.join(map(str, sorted(S)))
isint = lambda S: max(S) - min(S) + 1 == len(S)
T0 = time.time(); ALLOK = True; LOG = []
def chk(name, cond):
    global ALLOK
    ALLOK &= bool(cond); print(('ok   ' if cond else 'FAIL ') + f'n={n}: ' + name, flush=True)

# ---------- exact linear algebra ----------
def det(Mx):
    A = [list(map(F, r)) for r in Mx]; k = len(A); s = F(1)
    for c in range(k):
        p = next((i for i in range(c, k) if A[i][c] != 0), None)
        if p is None: return F(0)
        if p != c: A[c], A[p] = A[p], A[c]; s = -s
        s *= A[c][c]
        for i in range(c + 1, k):
            if A[i][c] != 0:
                f = A[i][c] / A[c][c]; A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return s
def inv(Mx):
    k = len(Mx); A = [list(map(F, r)) + [F(int(i == j)) for j in range(k)] for i, r in enumerate(Mx)]
    for c in range(k):
        p = next((i for i in range(c, k) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; pv = A[c][c]; A[c] = [a / pv for a in A[c]]
        for i in range(k):
            if i != c and A[i][c] != 0:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return [r[k:] for r in A]
def rank(rows):
    A = [list(r) for r in rows]; r = 0
    if not A: return 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r
def affdim(pts):
    pts = list(pts)
    if not pts: return -1
    return rank([[a - b for a, b in zip(p, pts[0])] for p in pts[1:]])
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
W = [sp.Rational(p, 97) for p in (1, 3, 7, 13, 29)][:d]   # generic direction for the exact limit in omega_tri

# ---------- the fixed arrangement of 2^n - 2 normals ----------
NORM = [tuple((1 if i in S else 0) - (1 if n in S else 0) for i in range(1, n)) for S in SUBS]   # a_S . u >= z_S - [n in S] z_full
def bvec(z): return [z[S] - (z[FULL] if n in S else 0) for S in SUBS]
BASES = []
for idx in itertools.combinations(range(M), d):
    Ai = inv([NORM[i] for i in idx])
    if Ai is not None: BASES.append((idx, Ai))
print(f'n={n}: d={d}, {M} inequalities, {len(BASES)} nonsingular {d}-subsets', flush=True)
def full(u, z): return tuple(u) + (z[FULL] - sum(u),)

def vertices(z):
    b = bvec(z); V = {}
    for idx, Ai in BASES:
        v = tuple(sum(Ai[r][c] * b[idx[c]] for c in range(d)) for r in range(d))
        if v in V: continue
        sl = [dot(NORM[k], v) - b[k] for k in range(M)]
        if min(sl) < 0: continue
        V[v] = frozenset(k for k in range(M) if sl[k] == 0)
    return V

class Poly:
    def __init__(self, z):
        self.z = z; Vd = vertices(z); self.V = sorted(Vd); self.tight = [Vd[v] for v in self.V]
        T = {k: frozenset(i for i, t in enumerate(self.tight) if k in t) for k in range(M)}
        self.facets = {k: T[k] for k in range(M) if T[k] and affdim(self.V[i] for i in T[k]) == d - 1}
        faces = {frozenset(range(len(self.V)))}; front = list(set(self.facets.values()))
        faces |= set(front)
        while front:
            nxt = []
            for f in front:
                for g in self.facets.values():
                    h = f & g
                    if h and h not in faces: faces.add(h); nxt.append(h)
            front = nxt
        self.dim = {f: affdim(self.V[i] for i in f) for f in faces}
        self.fv = [sum(1 for f in faces if self.dim[f] == k) for k in range(d)]
        self.bydim = {k: [f for f in faces if self.dim[f] == k] for k in range(-1, d + 1)}
        self.vfac = [frozenset(k for k in self.facets if i in self.facets[k]) for i in range(len(self.V))]
        self.simple = all(len(s) == d for s in self.vfac)
        self.struct = frozenset(frozenset(lab(SUBS[k]) for k in s) for s in self.vfac)   # labelled vertex-facet structure
        self.euler = sum((-1) ** k * self.fv[k] for k in range(d)) == 1 - (-1) ** d
        self._tri = {}
    def X(self, i): return full(self.V[i], self.z)
    def gp(self):   # every edge parallel to some e_i - e_j
        for e in self.bydim[1]:
            a, b = sorted(e); dv = [p - q for p, q in zip(self.X(a), self.X(b))]
            nz = [x for x in dv if x != 0]
            if len(nz) != 2 or nz[0] != -nz[1]: return False
        return True
    def tri(self, f):
        if f in self._tri: return self._tri[f]
        if self.dim[f] == 0: r = [tuple(f)]
        else:
            v0 = min(f); r = []
            for g in self.bydim[self.dim[f] - 1]:
                if g < f and v0 not in g: r += [(v0,) + s for s in self.tri(g)]
        self._tri[f] = r; return r
    def omega_tri(self, Y):
        tot = F(0); Yh = (1,) + tuple(Y); bad = []
        for s in self.tri(frozenset(range(len(self.V)))):
            Z = [(1,) + self.V[i] for i in s]; o = det(Z)
            if o == 0: continue
            if o < 0: Z[0], Z[1] = Z[1], Z[0]; o = -o
            den = F(1)
            for j in range(d + 1): den *= det([Z[k] if k != j else Yh for k in range(d + 1)])
            if den == 0: bad.append((Z, o)); continue
            tot += o ** d / den
        if bad:   # Y on an inner wall of the triangulation (symmetric centre): exact limit at Y + eps*W, eps -> 0, by Laurent series.
            # Each bracket is affine in eps: c_j + e_j eps (e_j = bracket with the row (0, W)). A term o^d / prod(c_j + e_j eps) with
            # k zero c_j contributes o^d / prod(e_zero) times the eps^k coefficient of prod_{c_j != 0} 1/(c_j + e_j eps); the
            # negative powers cancel in the sum (the total is regular at Y), so the constant terms give the exact value.
            Wh = (0,) + tuple(F(str(w)) for w in W); lim = F(0); poles = {}
            for Z, o in bad:
                cs = [det([Z[k] if k != j else Yh for k in range(d + 1)]) for j in range(d + 1)]
                es = [det([Z[k] if k != j else Wh for k in range(d + 1)]) for j in range(d + 1)]
                zero = [j for j in range(d + 1) if cs[j] == 0]; K = len(zero)
                pre = o ** d
                for j in zero: pre /= es[j]
                ser = [F(1)] + [F(0)] * K                     # power series of prod 1/(c + e eps) up to eps^K
                for j in range(d + 1):
                    if cs[j] == 0: continue
                    r = -es[j] / cs[j]; geo = [r ** m / cs[j] for m in range(K + 1)]
                    ser = [sum(ser[a] * geo[m - a] for a in range(m + 1)) for m in range(K + 1)]
                lim += pre * ser[K]
                for m in range(K):                            # coefficient of eps^(m-K): must cancel in total
                    poles[K - m] = poles.get(K - m, F(0)) + pre * ser[m]
            assert all(v == 0 for v in poles.values()), 'pole terms did not cancel'
            tot += lim
        return tot
    def omega_vert(self, Y):
        b = bvec(self.z); tot = F(0)
        for s in self.vfac:
            ks = sorted(s); den = F(1)
            for k in ks: den *= dot(NORM[k], Y) - b[k]
            tot += abs(det([NORM[k] for k in ks])) / den
        return tot
    def interior(self, Y):
        b = bvec(self.z); return all(dot(NORM[k], Y) - b[k] > 0 for k in self.facets)
    def parallelohedron(self):
        V = self.V; Vs = {v: i for i, v in enumerate(V)}; N = len(V)
        c = tuple(sum(v[j] for v in V) / N for j in range(d))
        if any(tuple(2 * c[j] - v[j] for j in range(d)) not in Vs for v in V): return False, 'not centrally symmetric'
        cen = {}
        for k, f in self.facets.items():
            cf = tuple(sum(V[i][j] for i in f) / len(f) for j in range(d)); cen[k] = cf
            pts = {V[i] for i in f}
            if any(tuple(2 * cf[j] - V[i][j] for j in range(d)) not in pts for i in f): return False, f'facet {lab(SUBS[k])} not centrally symmetric'
        ridges = set(self.bydim[d - 2]); seen = set(); lengths = []
        fac_of = {g: [k for k, f in self.facets.items() if g <= f] for g in ridges}
        for g0 in ridges:
            if g0 in seen: continue
            if len(fac_of[g0]) != 2: return False, 'ridge not in two facets'
            k = fac_of[g0][0]; g = g0; L = 0
            while True:
                seen.add(g); L += 1; cf = cen[k]
                g2 = frozenset(Vs[tuple(2 * cf[j] - V[i][j] for j in range(d))] for i in g)
                if g2 not in ridges: return False, 'opposite ridge missing'
                k2 = [q for q in fac_of[g2] if q != k][0]; g, k = g2, k2
                if g == g0 or L > 64: break
            lengths.append(L)
        bad = sorted(set(L for L in lengths if L not in (4, 6)))
        if bad: return False, f'belt lengths {sorted(set(lengths))}'
        return True, f'parallelohedron, belts {dict(sorted((L, lengths.count(L)) for L in set(lengths)))}'
    def facet_vol(self, k):   # (d-1)-volume of facet k, projected along a coordinate with nonzero normal component (fixed per facet)
        f = self.facets.get(k)
        if f is None: return F(0)
        j = next(i for i in range(d) if NORM[k][i] != 0); tot = F(0)
        for s in self.tri(f):
            rows = [[a - b for a, b in zip(self.V[s[i]], self.V[s[0]])] for i in range(1, d)]
            rows = [[r[q] for q in range(d) if q != j] for r in rows]
            tot += abs(det(rows)) if rows else F(1)
        return tot / factorial(d - 1)
    def greedy_ok(self):   # vertices of a generalized permutohedron by the greedy rule x_{s_k} = z(T_k) - z(T_{k-1})
        zz = dict(self.z); zz[frozenset()] = F(0); G = set()
        for s in itertools.permutations(range(1, n + 1)):
            x = [None] * n; T = frozenset()
            for i in s: T2 = T | {i}; x[i - 1] = zz[T2] - zz[T]; T = T2
            G.add(tuple(x[:d]))
        return G == set(self.V)

def zline(z0, z1, p): return {S: z0[S] + p * (z1[S] - z0[S]) for S in z0}
def S2(S): return lab(S)
def frs(x): return str(x)

# ---------- heights ----------
ALL = SUBS + [FULL]
zPi = {S: F(comb(len(S) + 1, 2)) for S in ALL}
zL = {S: F(sum(1 for i in S for j in S if i <= j and all(k in S for k in range(i, j + 1)))) for S in ALL}
D = {S: zPi[S] - zL[S] for S in ALL}
assert all(D[S] == 0 for S in ALL if isint(S)) and all(D[S] > 0 for S in SUBS if not isint(S))
zPi0 = {S: F(comb(len(S), 2)) for S in ALL}
zCube = {S: F(sum(1 for i in S if i + 1 in S)) for S in ALL}
_PC = Poly(zCube); _cc = [sum(full(v, zCube)[i] for v in _PC.V) / len(_PC.V) for i in range(n)]
zCube = {S: zCube[S] + sum(F(n - 1, 2) - _cc[i - 1] for i in S) for S in ALL}   # cube translated: vertex centroid = centre of Pi0
Y = tuple(F(n + 1, 2) for _ in range(d))            # centre of Pi (coordinates 1..n)
Y0 = tuple(F(n - 1, 2) for _ in range(d))           # centre of Pi0 (coordinates 0..n-1)

# ABHY with chunk 4's c (N = n + 2): interval [i, j] <-> diagonal (i, j + 2)
N = n + 2; ysym, Xab, diags, cab = abhy.setup(N)
zA = {}
for (i, j) in diags:
    I = frozenset(range(i, j - 1)); ps = lambda m: ysym[m] if 1 <= m <= n - 1 else 0   # ps_m = y_{m+2} = ysym[m-1+...]
    lin = (ysym[j - 2 - 1] if 1 <= j - 2 <= n - 1 else 0) - (ysym[i - 1 - 1] if 1 <= i - 1 <= n - 1 else 0)
    rest = sp.expand(Xab[(i, j)] - lin)
    assert rest.free_symbols == set(), f'ABHY diagonal {(i, j)} linear part is not the interval form'
    zA[I] = F(int(sp.numer(-rest)), int(sp.denom(-rest)))
zA[FULL] = F(0)
BIG = F(-10 ** 6)
zA_raw = {S: zA.get(S, BIG) for S in ALL}
PA_raw = Poly(zA_raw)
for S in SUBS:   # tight support values
    zA_raw[S] = min(sum(full(v, zA_raw)[i - 1] for i in S) for v in PA_raw.V)
cent = [sum(full(v, zA_raw)[i] for v in PA_raw.V) / len(PA_raw.V) for i in range(n)]
shift = [F(n + 1, 2) - cent[i] for i in range(n)]
zAt = {S: zA_raw[S] + sum(shift[i - 1] for i in S) for S in ALL}
Y_orig = tuple(Y[i] - shift[i] for i in range(d))   # Y in A's unshifted coordinates

def amp_X(Xval, drop=None):   # m_N = sum over triangulations of the N-gon of prod 1/X_d
    abhy.len_n[0] = N; tot = F(0)
    for k, T in enumerate(sorted(set(abhy.triangulations(list(range(1, N + 1)))), key=sorted)):
        if k == drop: continue
        den = F(1)
        for dg in T: den *= Xval[dg]
        tot += 1 / den
    return tot

# ---------- the lines ----------
LINES = [
    ('A', 'Postnikov line Pi -> Loday', zPi, zL, F(1), Y),
    ('B', 'equal-speed line Pi -> Loday', zPi, {S: (zPi[S] - 1 if not isint(S) and S != FULL else zPi[S]) for S in ALL}, max(D.values()), Y),
    ('C', 'ABHY line Pi -> kinematic associahedron (chunk 4 c)', zPi, zAt, F(1), Y),
    ('Z', 'control line Pi0 -> cube (graphic zonotopes)', zPi0, zCube, F(1), Y0),
]
# line B uses z0 + s*(z1 - z0) with z1 - z0 = -1 on non-intervals, s in [0, max D]

def walls(z0, z1, P):
    dz = {S: z1[S] - z0[S] for S in z0}; b0 = bvec(z0); b1 = bvec(dz); pts = set()
    for idx, Ai in BASES:
        v0 = [sum(Ai[r][c] * b0[idx[c]] for c in range(d)) for r in range(d)]
        v1 = [sum(Ai[r][c] * b1[idx[c]] for c in range(d)) for r in range(d)]
        lo, hi, ok = F(0), P, True
        for k in range(M):
            a = dot(NORM[k], v0) - b0[k]; be = dot(NORM[k], v1) - b1[k]
            if be == 0:
                if a < 0: ok = False; break
            elif be > 0: lo = max(lo, -a / be)
            else: hi = min(hi, -a / be)
            if lo > hi: ok = False; break
        if ok: pts.add(lo); pts.add(hi)
    return sorted(pts)

RESULT = {'n': n, 'dimension': d, 'subsets': [lab(S) for S in SUBS], 'interval': {lab(S): isint(S) for S in SUBS},
          'interior_point_Y_u': [frs(x) for x in Y], 'coordinates': 'u = (x_1..x_{n-1}); x_n = z_[n] - sum u', 'lines': {}}
WORK = len(LINES) * 3 + 1; done = 0
def progress(what):
    global done; done += 1; print(f'PROGRESS {done / WORK:.3f} {what}', flush=True)

POLY = {}
for name, desc, z0, z1, P, Yp in LINES:
    t1 = time.time()
    if name == 'B': z1eff = {S: z0[S] + (z1[S] - z0[S]) * P for S in z0}   # end of B at s = P (all non-intervals lowered by max D)
    else: z1eff = z1
    dz1 = {S: z1eff[S] - z0[S] for S in z0}
    cand = walls(z0, z1eff, F(1))                                    # parameter q in [0,1]; p = q * P
    progress(f'line {name}: {len(cand)} candidate break points')
    grid = sorted(set([F(k, 8) for k in range(9)] + cand + [(a + b) / 2 for a, b in zip(cand, cand[1:])]))
    st = {q: Poly(zline(z0, z1eff, q)) for q in grid}
    progress(f'line {name}: {len(grid)} stations built')
    # true walls: structure at q differs from the open intervals on either side
    wl = []
    for q in cand:
        left = st.get(max([g for g in grid if g < q], default=None)) if q > 0 else None
        right = st.get(min([g for g in grid if g > q], default=None)) if q < 1 else None
        here = st[q]
        if (left and left.struct != here.struct) or (right and right.struct != here.struct):
            wl.append(q)
    stations = []
    for q in grid:
        Pq = st[q]; tiles, why = Pq.parallelohedron(); om = Pq.omega_tri(Yp)
        rec = {'q': frs(q), 'param': frs(q * P), 'wall': q in wl, 'z': {lab(S): frs(Pq.z[S]) for S in ALL},
               'vertices': [[frs(x) for x in Pq.X(i)] for i in range(len(Pq.V))],
               'facets': {lab(SUBS[k]): sorted(f) for k, f in sorted(Pq.facets.items())},
               'f_vector': Pq.fv, 'simple': Pq.simple, 'generalized_permutohedron': Pq.gp(), 'euler': Pq.euler,
               'tiles_by_translation': tiles, 'tiling_test': why, 'omega_at_Y': frs(om), 'omega_float': float(om)}
        if Pq.simple: rec['omega_vertex_formula_agrees'] = Pq.omega_vert(Yp) == om
        rec['Y_interior'] = Pq.interior(Yp)
        stations.append(rec)
    # closed form of Omega on every open interval (vertex formula with symbolic parameter), continuity at walls
    pts = [F(0)] + [q for q in wl if 0 < q < 1] + [F(1)]
    pieces = []; p_ = sp.Symbol('p'); b0 = bvec(z0); b1 = bvec(dz1)
    for a, b in zip(pts, pts[1:]):
        mid = Poly(zline(z0, z1eff, (a + b) / 2))
        if not mid.simple: pieces.append({'from': frs(a * P), 'to': frs(b * P), 'omega': 'not simple'}); continue
        expr = 0
        for s in mid.vfac:
            ks = sorted(s); den = 1
            for k in ks:
                den *= sp.Rational(str(dot(NORM[k], Yp) - b0[k])) - p_ / sp.Rational(str(P)) * sp.Rational(str(b1[k]))
            expr += sp.Rational(str(abs(det([NORM[k] for k in ks])))) / den
        expr = sp.factor(sp.cancel(sp.together(expr)))
        lv = expr.subs(p_, sp.Rational(str(a * P))); rv = expr.subs(p_, sp.Rational(str(b * P)))
        ok_l = lv == sp.Rational(str(st[a].omega_tri(Yp))); ok_r = rv == sp.Rational(str(st[b].omega_tri(Yp)))
        pieces.append({'from': frs(a * P), 'to': frs(b * P), 'omega': str(expr), 'continuous_at_ends': bool(ok_l and ok_r)})
    progress(f'line {name}: stations, tiling tests and canonical forms done')
    # wall table
    wtab = []
    for q in wl:
        here = st[q]; lefts = [g for g in grid if g < q]; rights = [g for g in grid if g > q]
        Lp = st[max(lefts)] if lefts else None; Rp = st[min(rights)] if rights else None
        fl = set(lab(SUBS[k]) for k in Lp.facets) if Lp else None; fh = set(lab(SUBS[k]) for k in here.facets)
        fr = set(lab(SUBS[k]) for k in Rp.facets) if Rp else None
        gone = sorted(fl - fh, key=lambda s: (len(s), s)) if fl is not None else []
        shrink = {}
        for s in gone:
            k = SUBS.index(frozenset(int(c) for c in s)); tset = [i for i, t in enumerate(here.tight) if k in t]
            shrink[s] = affdim(here.V[i] for i in tset)
        wtab.append({'param': frs(q * P), 'float': float(q * P), 'facets_shrinking_to_nothing': gone,
                     'face_dimension_they_shrink_to': shrink, 'facets_new_after': sorted(fr - fh) if fr is not None else [],
                     'facets_gone_after': sorted(fh - fr, key=lambda s: (len(s), s)) if fr is not None else [],
                     'f_before': Lp.fv if Lp else None, 'f_at': here.fv, 'f_after': Rp.fv if Rp else None,
                     'simple_before': Lp.simple if Lp else None, 'gp_after': Rp.gp() if Rp else None})
    RESULT['lines'][name] = {'description': desc, 'parameter_range': [0, frs(P)], 'z_start': {lab(S): frs(z0[S]) for S in ALL},
                             'z_end': {lab(S): frs(z1eff[S]) for S in ALL}, 'walls': wtab, 'stations': stations,
                             'omega_closed_forms': pieces, 'interior_point': [frs(x) for x in Yp]}
    POLY[name] = st
    print(f'--- line {name} ({desc}), parameter 0..{P}: {len(wl)} walls; {time.time() - t1:.1f}s', flush=True)
    for w in wtab:
        print(f'    WALL at {w["param"]} (= {w["float"]:.6f}): facets shrinking to nothing {w["facets_shrinking_to_nothing"]} '
              f'(to faces of dim {w["face_dimension_they_shrink_to"]}); f {w["f_before"]} -> {w["f_at"]} -> {w["f_after"]}', flush=True)
    for r in stations:
        print(f'    station {r["param"]:>8}: f {r["f_vector"]} simple {r["simple"]} GP {r["generalized_permutohedron"]} '
              f'tiles {r["tiles_by_translation"]} ({r["tiling_test"]}) Omega(Y) = {r["omega_at_Y"]} ({r["omega_float"]:.6g})', flush=True)
    for pc in pieces: print(f'    Omega on [{pc["from"]}, {pc["to"]}]: {pc["omega"]}', flush=True)

# ---------- checks and controls ----------
A, B, C, Zl = POLY['A'], POLY['B'], POLY['C'], POLY['Z']
Pi = A[F(0)]; Lo = A[F(1)]; Ab = C[F(1)]
cat = comb(2 * n, n) // (n + 1)
chk(f'Pi has n! = {factorial(n)} vertices, simple, Euler', len(Pi.V) == factorial(n) and Pi.simple and Pi.euler)
chk(f'Loday end has Catalan({n}) = {cat} vertices; B ends at Loday too; ABHY end has {cat}', len(Lo.V) == cat and B[F(1)].struct == Lo.struct and len(Ab.V) == cat)
chk('CONTROL: the permutohedron passes the Venkov-McMullen parallelohedron test: ' + Pi.parallelohedron()[1], Pi.parallelohedron()[0])
chk('CONTROL: Loday\'s associahedron fails it (' + Lo.parallelohedron()[1] + ')', not Lo.parallelohedron()[0])
chk('CONTROL: the ABHY associahedron fails it (' + Ab.parallelohedron()[1] + ')', not Ab.parallelohedron()[0])
chk('CONTROL line Z: every station Pi0 -> cube tiles (graphic zonotopes)', all(Zl[q].parallelohedron()[0] for q in Zl))
oc = F(2 ** (n - 1) * n, factorial(n - 1))
chk(f'Omega(Pi; centre) = 2^(n-1) n/(n-1)! = {oc}', Pi.omega_tri(Y) == oc)
chk('Euler relation at every station of every line', all(P.euler for L in POLY.values() for P in L.values()))
chk('triangulation formula = Warren vertex formula at every simple station',
    all(r.get('omega_vertex_formula_agrees', True) for L in RESULT['lines'].values() for r in L['stations']))
chk('Y interior at every station', all(r['Y_interior'] for L in RESULT['lines'].values() for r in L['stations']))
chk('greedy vertices = enumerated vertices on lines A, C, Z (generalized permutohedra)', all(P.greedy_ok() for L in (A, C, Zl) for P in L.values()))
chk('lines A, C, Z stay generalized permutohedra (edge test) at every station', all(P.gp() for L in (A, C, Zl) for P in L.values()))
chk('Omega closed forms continuous at every wall and end', all(pc.get('continuous_at_ends', True) for L in RESULT['lines'].values() for pc in L['omega_closed_forms']))
# Loday = ABHY with every mesh constant 1; Omega(L) = m_N
zLe = dict(zL); zLe[frozenset()] = F(0)
def zint(i, j): return zLe[frozenset(range(i, j + 1))] if j >= i else F(0)
mesh = set()
for a_ in range(1, N):
    for b_ in range(a_ + 2, N):
        mesh.add(zint(a_, b_ - 1) + zint(a_ + 1, b_ - 2) - zint(a_, b_ - 2) - zint(a_ + 1, b_ - 1))
chk(f'Loday\'s heights satisfy the ABHY mesh relations with every c = 1 (found {sorted(mesh)})', mesh == {F(1)})
XL = {(i, j): sum(full(Y, zL)[k - 1] for k in range(i, j - 1)) - zL[frozenset(range(i, j - 1))] for (i, j) in diags}
mL = amp_X(XL)
chk(f'Omega(Loday; Y) = m_{N}(X = Loday facet values at Y) = {mL}', Lo.omega_tri(Y) == mL)
# chunk 4's amplitude at the same point, with chunk 4's own X functions
yv = []; acc = F(0)
for k in range(d): acc += Y_orig[k]; yv.append(acc)
sub = {ysym[k]: sp.Rational(str(yv[k])) for k in range(d)}
XA = {dg: F(str(Xab[dg].subs(sub))) for dg in diags}
mA = amp_X(XA)
chk(f'Omega(ABHY; Y) = chunk 4 amplitude m_{N} at the same point = {mA}', Ab.omega_tri(Y) == mA)
chk('negative: chunk 4 amplitude with one tree dropped differs', amp_X(XA, drop=0) != Ab.omega_tri(Y))
# facet sizes along line A: polynomial in t, order of vanishing at t = 1
sizes = {}; tsym = sp.Symbol('t'); grid = sorted(A)
gridk = [q for q in grid if q.denominator <= 8]
for k in range(M):
    S = SUBS[k]
    if k not in Pi.facets: continue
    vals = [(q, A[q].facet_vol(k)) for q in gridk]
    fitp = vals[:d]
    poly = sp.interpolate([(sp.Rational(str(q)), sp.Rational(str(v))) for q, v in fitp], tsym)
    good = all(poly.subs(tsym, sp.Rational(str(q))) == sp.Rational(str(v)) for q, v in vals)
    rel = sp.factor(poly / sp.Rational(str(vals[0][1])))
    order = 0; pp = sp.Poly(poly, tsym)
    while pp.eval(1) == 0 and not pp.is_zero: pp = sp.Poly(sp.quo(pp.as_expr(), tsym - 1), tsym); order += 1
    sizes[lab(S)] = {'relative_size': str(rel), 'vanishing_order_at_t1': order, 'interval': isint(S), 'polynomial_checked': bool(good)}
chk('facet sizes along A are polynomials of degree <= d-1 (checked on all 9 stations)', all(v['polynomial_checked'] for v in sizes.values()))
chk('along A exactly the non-interval facets reach size 0, all at t = 1', all((v['vanishing_order_at_t1'] > 0) == (not v['interval']) for v in sizes.values()))
RESULT['lines']['A']['facet_sizes'] = sizes
for s, v in sorted(sizes.items(), key=lambda kv: (len(kv[0]), kv[0])):
    if not v['interval']: print(f'    A facet {s}: size/size(0) = {v["relative_size"]} (vanishes to order {v["vanishing_order_at_t1"]} at t = 1)', flush=True)
RESULT['controls'] = {'omega_Pi_centre': frs(oc), 'm_N_Loday_at_Y': frs(mL), 'm_N_ABHY_chunk4_at_Y': frs(mA), 'N': N,
                      'abhy_c': {f'{a},{b}': frs(F(str(v))) for (a, b), v in cab.items()}, 'abhy_shift': [frs(x) for x in shift]}
RESULT['all_checks_ok'] = bool(ALLOK)
with open(OUT, 'w') as fh: json.dump(RESULT, fh, indent=1)
progress('json written')
print(f'n={n}: total {time.time() - T0:.1f}s, json {os.path.basename(OUT)}', flush=True)
print('FINAL ok: all checks and controls held' if ALLOK else 'FINAL FAIL')
