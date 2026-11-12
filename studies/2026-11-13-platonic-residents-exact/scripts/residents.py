#!/usr/bin/env python3
"""The residents of the Queens, EXACT (13 Nov 2026; Platonic book, Chapter 11; Atlas of the Chains, Observation 5).

Every regular dodecahedron D, icosahedron I, cube C, tetrahedron T and octahedron O whose corners are ALL corners of a polytope is
enumerated in exact arithmetic (Q(sqrt5) for H3/H4, Q(sqrt2) for A/B/F; integers after clearing denominators, no floats in any
decision). Pure Python (stdlib only).

Method (complete by construction):
  * The polytope: the Wythoff orbit of the 0/1 seed x (distance 1 from every ringed mirror, 0 from the others), generated exactly by
    the simple reflections; the reflections are also recorded as permutations of the corners (the group action used for orbits).
  * A finite point set is fixed up to isometry by its distance matrix, and a 3-dimensional solid by any 4 affinely independent corners
    (a 4-dimensional one by 5). For each solid X a FRAME (p0 and dim further corners, nearest first, affinely independent) is chosen in
    a model; every other corner of X is a fixed affine combination of the frame (exact coefficients over the field).
  * Through the corner v0: for every squared distance s from v0, all ordered tuples (v0, P1, .., Pdim) of corners whose squared
    distances equal s times the frame's ratios are listed (exact integer comparison); each tuple fixes one candidate solid; it is kept
    iff every one of its corners is a corner of the polytope; then its full distance matrix is checked exactly against s times the
    model's. Every resident through v0 is found (label it with v0 as p0: its frame is such a tuple). Distinct corner sets are counted.
  * Totals: the polytope is corner-transitive (one orbit), so total = (residents through v0) x corners / (corners of X), required to be
    an integer. For the 600-cell and the 120-cell the full set is also built (closure of the residents through v0 under the four
    reflections) and split into orbits of the full group [3,3,5] and of its rotation subgroup; and, independently of any group, the
    search is repeated from EVERY corner and the union compared with the closure.
  * The field argument for "no D or I outside H4": see the README (Q(sqrt2) cannot hold a regular pentagon).
usage: residents.py pilot|full   -> data/residents-<mode>.json, PROGRESS lines, FINAL ok/FAIL"""
import sys, json, time, itertools
from fractions import Fraction as Fr
from math import lcm
from collections import defaultdict, Counter
from multiprocessing import Pool

# ------------------------------------------------------------------ exact field Q(w): w = phi (d = 5) or sqrt2 (d = 2)
class E:
    __slots__ = ('a', 'b', 'd')
    def __init__(s, a, b=0, d=5): s.a = Fr(a); s.b = Fr(b); s.d = d
    def _c(s, o): return o if isinstance(o, E) else E(o, 0, s.d)
    def __add__(s, o): o = s._c(o); return E(s.a + o.a, s.b + o.b, s.d)
    __radd__ = __add__
    def __sub__(s, o): o = s._c(o); return E(s.a - o.a, s.b - o.b, s.d)
    def __rsub__(s, o): return s._c(o) - s
    def __neg__(s): return E(-s.a, -s.b, s.d)
    def __mul__(s, o):
        o = s._c(o)
        if s.d == 5: return E(s.a * o.a + s.b * o.b, s.a * o.b + s.b * o.a + s.b * o.b, 5)
        return E(s.a * o.a + 2 * s.b * o.b, s.a * o.b + s.b * o.a, 2)
    __rmul__ = __mul__
    def conj(s): return E(s.a + s.b, -s.b, 5) if s.d == 5 else E(s.a, -s.b, 2)
    def inv(s):
        n = (s * s.conj()).a; c = s.conj(); return E(c.a / n, c.b / n, s.d)
    def __truediv__(s, o): return s * s._c(o).inv()
    def __eq__(s, o): o = s._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s): return sgn(2 * s.a + s.b, s.b, 5) if s.d == 5 else sgn(s.a, s.b, 2)
    def __float__(s): return float(s.a) + float(s.b) * ((1 + 5 ** .5) / 2 if s.d == 5 else 2 ** .5)
    def isint(s): return s.a.denominator == 1 and s.b.denominator == 1
    def __repr__(s):
        if s.d == 5: p, q = s.a + s.b / 2, s.b / 2; r = 'sqrt5'
        else: p, q = s.a, s.b; r = 'sqrt2'
        if q == 0: return str(p)
        if p == 0: return f'{q}*{r}'
        return f'{p} {"+" if q > 0 else "-"} {abs(q)}*{r}'
def sgn(p, q, m):
    """exact sign of p + q sqrt(m), p, q rational, m not a square"""
    if p >= 0 and q >= 0: return 0 if (p == 0 and q == 0) else 1
    if p <= 0 and q <= 0: return -1
    return (1 if p > 0 else -1) if p * p > m * q * q else (1 if q > 0 else -1)
def dot(u, v):
    t = E(0, 0, u[0].d)
    for x, y in zip(u, v): t = t + x * y
    return t
def solve(M, rhs):
    """exact Gaussian elimination, M square list of rows of E"""
    n = len(M); A = [list(M[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if not A[r][c] == 0); A[c], A[p] = A[p], A[c]
        iv = A[c][c].inv(); A[c] = [x * iv for x in A[c]]
        for r in range(n):
            if r != c and not A[r][c] == 0:
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] for i in range(n)]
def rank(vecs):
    A = [list(v) for v in vecs]; r = 0; ncol = len(A[0]) if A else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(A)) if not A[i][c] == 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; iv = A[r][c].inv(); A[r] = [x * iv for x in A[r]]
        for i in range(len(A)):
            if i != r and not A[i][c] == 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r

# ------------------------------------------------------------------ root systems (exact)
def root_system(g):
    d = 5 if g[0] == 'H' else 2
    Z = lambda n: [E(0, 0, d) for _ in range(n)]
    R = []
    if g in ('A3', 'A4'):
        n = int(g[1]) + 1
        for i in range(n):
            for j in range(n):
                if i != j: v = Z(n); v[i] = E(1, 0, d); v[j] = E(-1, 0, d); R.append(v)
    elif g in ('B3', 'B4'):
        n = int(g[1])
        for i in range(n):
            for s in (1, -1): v = Z(n); v[i] = E(s, 0, d); R.append(v)
        for i, j in itertools.combinations(range(n), 2):
            for s, t in itertools.product((1, -1), repeat=2): v = Z(n); v[i] = E(s, 0, d); v[j] = E(t, 0, d); R.append(v)
    elif g == 'F4':
        n = 4
        for i in range(n):
            for s in (2, -2): v = Z(n); v[i] = E(s, 0, d); R.append(v)
        for i, j in itertools.combinations(range(n), 2):
            for s, t in itertools.product((2, -2), repeat=2): v = Z(n); v[i] = E(s, 0, d); v[j] = E(t, 0, d); R.append(v)
        for s in itertools.product((1, -1), repeat=4): R.append([E(c, 0, d) for c in s])
    elif g in ('H3', 'H4'):
        n = int(g[1]); ph = E(0, 1, 5); iph = E(-1, 1, 5)
        for i in range(n):
            for s in (2, -2): v = Z(n); v[i] = E(s, 0, d); R.append(v)
        if n == 4:
            for s in itertools.product((1, -1), repeat=4): R.append([E(c, 0, d) for c in s])
            base = [ph, E(1, 0, 5), iph, E(0, 0, 5)]
            perms = [p for p in itertools.permutations(range(4)) if sum(p[a] > p[b] for a in range(4) for b in range(a + 1, 4)) % 2 == 0]
        else:
            base = [ph, E(1, 0, 5), iph]; perms = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
        for p in perms:
            for s in itertools.product((1, -1), repeat=3):
                v = Z(n); signs = list(s) + [1]
                for i in range(len(base)): v[p[i]] = base[i] * signs[i]
                R.append(v)
    key = lambda v: tuple((c.a, c.b) for c in v); U = {}
    for v in R: U.setdefault(key(v), v)
    return list(U.values()), d
def sqrt_norm(nr, d):
    return {1: E(1, 0, d), 2: E(0, 1, 2), 4: E(2, 0, d), 8: E(0, 2, 2)}[int(nr.a)]
def refl(r, rr2, x):
    c = dot(r, x) * rr2; return [xi - c * ri for xi, ri in zip(x, r)]
def simple_roots(g):
    R, d = root_system(g); n = len(R[0])
    f = [E(c, 0, d) for c in (1000003, 1009, 101, 11, 3)[:n]]
    assert all(dot(r, f).sign() != 0 for r in R)
    Pos = [r for r in R if dot(r, f).sign() > 0]; key = lambda v: tuple((c.a, c.b) for c in v); PK = {key(r) for r in Pos}
    S = []
    for r in Pos:
        rr2 = E(2, 0, d) / dot(r, r)
        if all(key(refl(r, rr2, q)) in PK for q in Pos if key(q) != key(r)): S.append(r)
    m = len(S)
    def bond(i, j):
        c2 = float(dot(S[i], S[j]) * dot(S[i], S[j]) / (dot(S[i], S[i]) * dot(S[j], S[j])))
        return min(((0, 2), (.25, 3), (.5, 4), (((1 + 5 ** .5) / 2) ** 2 / 4, 5)), key=lambda t: abs(t[0] - c2))[1]
    adj = {i: [j for j in range(m) if j != i and bond(i, j) > 2] for i in range(m)}
    ends = [i for i in range(m) if len(adj[i]) <= 1]
    big = [i for i in ends if adj[i] and bond(i, adj[i][0]) > 3]
    start = big[0] if big else max(ends, key=lambda i: (float(dot(S[i], S[i])), -i))
    order = [start]
    while len(order) < m: order.append(next(j for j in adj[order[-1]] if j not in order))
    S = [S[i] for i in order]; bonds = [bond(i, i + 1) for i in range(m - 1)]
    return S, d, n, len(R), bonds

# ------------------------------------------------------------------ orbits
def ekey(x): return tuple((c.a, c.b) for c in x)
def orbit(x, S, d, gens=None):
    gens = range(len(S)) if gens is None else gens
    rr = [E(2, 0, d) / dot(r, r) for r in S]
    pts = [x]; idx = {ekey(x): 0}; perm = {g: [] for g in gens}; i = 0
    while i < len(pts):
        for g in gens:
            y = refl(S[g], rr[g], pts[i]); k = ekey(y); j = idx.get(k)
            if j is None: j = len(pts); idx[k] = j; pts.append(y)
            perm[g].append(j)
        i += 1
    return pts, perm
def seed_point(S, d, n, lab):
    rows = [list(r) for r in S]; rhs = [E(l, 0, d) * sqrt_norm(dot(r, r), d) for r, l in zip(S, lab)]
    if n > len(S): rows.append([E(1, 0, d)] * n); rhs.append(E(0, 0, d))     # A_n lives in the hyperplane sum = 0
    return solve(rows, rhs)
def phiform(x):
    """x = c * phi^j with c rational, if so (d = 5)"""
    if x.d != 5: return repr(x)
    ph = E(0, 1, 5); y = E(x.a, x.b, 5)
    for j in range(0, 13):
        for sgn_, z in ((j, x / _pow(ph, j)), (-j, x * _pow(ph, j))):
            if z.b == 0: return f'{z.a}*phi^{sgn_}' if sgn_ else str(z.a)
    return repr(x)
def _pow(x, j):
    r = E(1, 0, x.d)
    for _ in range(j): r = r * x
    return r
def to_int(pts, d):
    L = 1
    for p in pts:
        for c in p: L = lcm(L, c.a.denominator, c.b.denominator)
    return [tuple(v for c in p for v in (int(c.a * L), int(c.b * L))) for p in pts], L

# ------------------------------------------------------------------ integer field arithmetic on pairs
def imul(d, a, b, c, e): return (a * c + b * e, a * e + b * c + b * e) if d == 5 else (a * c + 2 * b * e, a * e + b * c)
def sqd(d, p, q):
    A = B = 0
    for k in range(0, len(p), 2):
        x = p[k] - q[k]; y = p[k + 1] - q[k + 1]
        if d == 5: A += x * x + y * y; B += 2 * x * y + y * y
        else: A += x * x + 2 * y * y; B += 2 * x * y
    return (A, B)
def idot(d, p, q):
    A = B = 0
    for k in range(0, len(p), 2):
        u, v = imul(d, p[k], p[k + 1], q[k], q[k + 1]); A += u; B += v
    return (A, B)
def isign(d, A, B): return sgn(2 * A + B, B, 5) if d == 5 else sgn(A, B, 2)

# ------------------------------------------------------------------ the solids (models)
def models(d):
    ph = E(0, 1, 5); iph = E(-1, 1, 5)
    q = lambda *c: [x if isinstance(x, E) else E(x, 0, d) for x in c]
    T = [q(1, 1, 1), q(1, -1, -1), q(-1, 1, -1), q(-1, -1, 1)]
    C = [q(*s) for s in itertools.product((1, -1), repeat=3)]
    O = [q(*[s if k == i else 0 for k in range(3)]) for i in range(3) for s in (1, -1)]
    M = {'C': C, 'T': T, 'O': O}
    if d == 5:
        cyc = lambda v: [v, [v[2], v[0], v[1]], [v[1], v[2], v[0]]]
        I = [w for a in (1, -1) for b in (1, -1) for w in cyc(q(0, a, b * ph))]
        Dd = C + [w for a in (1, -1) for b in (1, -1) for w in cyc(q(0, a * iph, b * ph))]
        M = {'D': Dd, 'I': I, **M}
    return M
def models4(d):
    q = lambda *c: [x if isinstance(x, E) else E(x, 0, d) for x in c]
    ph = E(0, 1, 5)
    M = {'16-cell': [q(*[s if k == i else 0 for k in range(4)]) for i in range(4) for s in (1, -1)],
         'tesseract': [q(*s) for s in itertools.product((1, -1), repeat=4)],
         '24-cell': [q(*[(s if k == i else t if k == j else 0) for k in range(4)]) for i, j in itertools.combinations(range(4), 2) for s in (1, -1) for t in (1, -1)]}
    if d == 5: M['5-cell'] = [q(2, 0, 0, 0), q(0, 2, 0, 0), q(0, 0, 2, 0), q(0, 0, 0, 2), q(ph, ph, ph, ph)]
    return M
class Model:
    def __init__(s, name, V):
        s.name = name; s.k = len(V); dim = len(V[0]); s.dim = dim; d = V[0][0].d
        sq = lambda u, v: dot([a - b for a, b in zip(u, v)], [a - b for a, b in zip(u, v)])
        order = sorted(range(1, len(V)), key=lambda j: float(sq(V[0], V[j])))
        fr = [0]
        for j in order:
            if rank([[a - b for a, b in zip(V[i], V[0])] for i in fr[1:] + [j]]) == len(fr): fr.append(j)
            if len(fr) == dim + 1: break
        assert len(fr) == dim + 1
        s.frame = fr; base = sq(V[fr[0]], V[fr[1]])
        s.ratio = {(i, j): sq(V[fr[i]], V[fr[j]]) / base for i in range(dim + 1) for j in range(i + 1, dim + 1)}
        cols = [[a - b for a, b in zip(V[fr[i]], V[0])] for i in range(1, dim + 1)]
        Mrows = [[cols[i][r] for i in range(dim)] for r in range(dim)]
        coef = [solve(Mrows, [a - b for a, b in zip(v, V[0])]) for v in V]
        m = 1
        for cs in coef:
            for c in cs: m = lcm(m, c.a.denominator, c.b.denominator)
        s.m = m; s.coef = [[(int(c.a * m), int(c.b * m)) for c in cs] for cs in coef]
        s.pair = {(a, b): sq(V[a], V[b]) / base for a in range(s.k) for b in range(a + 1, s.k)}

def through(P, idx, d, v0, model, shells=None):
    """all residents of type model with v0 among their corners: dict frozenset -> (labelled corners, s)"""
    p0 = P[v0]
    if shells is None:
        shells = defaultdict(list)
        for j, p in enumerate(P):
            if j != v0: shells[sqd(d, p0, p)].append(j)
    dim = model.dim; m = model.m; n2 = len(p0); found = {}
    for s in list(shells):
        sE = E(s[0], s[1], d); T = {}
        bad = False
        for ij, r in model.ratio.items():
            t = sE * r
            if not t.isint(): bad = True; break
            T[ij] = (int(t.a), int(t.b))
        if bad: continue
        cands = [None] + [shells.get(T[(0, i)], ()) for i in range(1, dim + 1)]
        if any(len(c) == 0 for c in cands[1:]): continue
        stack = [[v0]]
        while stack:
            ch = stack.pop(); i = len(ch)
            if i == dim + 1:
                F = [P[c] for c in ch]; corners = []
                for cq in model.coef:
                    pt = []
                    for k in range(0, n2, 2):
                        a = m * F[0][k]; b = m * F[0][k + 1]
                        for t in range(1, dim + 1):
                            x, y = imul(d, cq[t - 1][0], cq[t - 1][1], F[t][k] - F[0][k], F[t][k + 1] - F[0][k + 1]); a += x; b += y
                        if a % m or b % m: break
                        pt += [a // m, b // m]
                    else:
                        j = idx.get(tuple(pt))
                        if j is not None: corners.append(j); continue
                    break
                else:
                    key = frozenset(corners)
                    if key not in found: found[key] = (corners, s)
                continue
            for c in cands[i]:
                if c in ch: continue
                pc = P[c]
                if all(sqd(d, P[ch[j]], pc) == T[(j, i)] for j in range(1, i)): stack.append(ch + [c])
    for key, (corners, s) in found.items():          # exact congruence check of every resident
        sE = E(s[0], s[1], d)
        assert len(key) == model.k
        for (a, b), r in model.pair.items():
            t = sE * r; assert sqd(d, P[corners[a]], P[corners[b]]) == (int(t.a), int(t.b)), (model.name, a, b)
    return found

# ------------------------------------------------------------------ one polytope
NAMES = {'A': ('5-cell', '5-cell'), 'B': ('tesseract', '16-cell'), 'F': ('24-cell', '24-cell'), 'H': ('120-cell', '600-cell')}
NAMES3 = {'A': ('tetrahedron', 'tetrahedron'), 'B': ('cube', 'octahedron'), 'H': ('dodecahedron', 'icosahedron')}
PAT4 = {'1000': '{P}', '0100': 'rectified {P}', '0010': 'rectified {Q}', '0001': '{Q}', '1100': 'truncated {P}', '1010': 'cantellated {P}',
        '1001': 'runcinated {P}', '0110': 'bitruncated {P}', '0101': 'cantellated {Q}', '0011': 'truncated {Q}', '1110': 'cantitruncated {P}',
        '1101': 'runcitruncated {P}', '1011': 'runcitruncated {Q}', '0111': 'cantitruncated {Q}', '1111': 'omnitruncated {P}'}
PAT3 = {'100': '{P}', '010': 'rectified {P}', '001': '{Q}', '110': 'truncated {P}', '101': 'cantellated {P}', '011': 'truncated {Q}', '111': 'omnitruncated {P}'}
H4F0 = {'1000': 600, '0100': 1200, '0010': 720, '0001': 120, '1100': 2400, '1010': 3600, '1001': 2400, '0110': 3600, '0101': 3600,
        '0011': 1440, '1110': 7200, '1101': 7200, '1011': 7200, '0111': 7200, '1111': 14400}
WORD = {'A3': 24, 'B3': 48, 'H3': 120, 'A4': 120, 'B4': 384, 'F4': 1152, 'H4': 14400}
def name_of(g, lab):
    s = ''.join(map(str, lab)); P, Q = (NAMES3 if g[1] == '3' else NAMES)[g[0]]
    return ((PAT3 if g[1] == '3' else PAT4)[s]).format(P=P, Q=Q)
def build(g, lab, prism=False):
    S, d, n, nroots, bonds = simple_roots(g)
    x = seed_point(S, d, n, lab); pts, perm = orbit(x, S, d)
    xg = seed_point(S, d, n, [1] * len(S)); W = len(orbit(xg, S, d)[0])
    J = [i for i, l in enumerate(lab) if l == 0]; WJ = len(orbit(xg, S, d, J)[0]) if J else 1
    if prism:                                    # H3 x A1: the uniform prism, height = edge = 2
        pts = [p + [E(t, 0, d)] for p in pts for t in (1, -1)]; W *= 2
    P, L = to_int(pts, d)
    return P, d, perm, W, WJ, bonds
def analyse(job):
    g, lab, kind = job; t0 = time.time()
    if kind in ('snub24', 'grand'):
        P, d, perm, W, WJ, bonds = build('H4', (0, 0, 0, 1)); nm = 'snub 24-cell' if kind == 'snub24' else 'grand antiprism'
        P = sub600(P, d, kind)
    else:
        P, d, perm, W, WJ, bonds = build(g, lab, prism=(kind == 'prism'))
        nm = name_of(g, lab) + (' prism' if kind == 'prism' else '')
    V = len(P); idx = {p: i for i, p in enumerate(P)}; assert len(idx) == V
    rec = {'group': g, 'seed': ''.join(map(str, lab)) if lab else '-', 'kind': kind, 'name': nm, 'corners': V, 'field': f'Q(sqrt{d})',
           'group_order': W, 'stabiliser_order': WJ, 'bonds': bonds, 'residents': {}}
    p0 = P[0]; shells = defaultdict(list)
    for j, p in enumerate(P):
        if j: shells[sqd(d, p0, p)].append(j)
    e0 = min(shells, key=lambda s: float(E(s[0], s[1], d)))
    for mn, Vm in models(d).items():
        M = Model(mn, Vm)
        if kind in ('snub24', 'grand'):           # not assumed corner-transitive: search from every corner, take the union
            allr = {}
            for v in range(V):
                sh = defaultdict(list)
                for j, p in enumerate(P):
                    if j != v: sh[sqd(d, P[v], p)].append(j)
                allr.update(through(P, idx, d, v, M, sh))
            tot = len(allr); thr = sum(1 for k in allr if 0 in k)
            sizes = Counter(repr(E(s[0], s[1], d) / E(e0[0], e0[1], d)) for _, (c, s) in allr.items())
        else:
            F = through(P, idx, d, 0, M, shells); thr = len(F)
            assert (thr * V) % M.k == 0, (nm, mn, thr, V); tot = thr * V // M.k
            sizes = Counter(repr(E(s[0], s[1], d) / E(e0[0], e0[1], d)) for _, (c, s) in F.items())
        if thr or tot: rec['residents'][mn] = {'through_corner': thr, 'total': tot, 'edge2_over_polytope_edge2_through_corner': dict(sizes)}
    rec['seconds'] = round(time.time() - t0, 1)
    return rec
def sub600(P, d, kind):
    """snub 24-cell = 600-cell minus one inscribed 24-cell (the 24 corners with coordinates in Z: (+-2,0,0,0), (+-1,+-1,+-1,+-1));
    grand antiprism = 600-cell minus two completely orthogonal great decagons"""
    if kind == 'snub24':
        idx = {p: i for i, p in enumerate(P)}
        c24 = next(iter(through(P, idx, d, 0, Model('24-cell', models4(d)['24-cell']))))      # one inscribed 24-cell
        assert len(c24) == 24
        return [p for i, p in enumerate(P) if i not in c24]
    # decagon through corner 0 and a neighbour: the corners in span(P0, P1)
    e = min((sqd(d, P[0], q) for q in P[1:]), key=lambda s: float(E(s[0], s[1], d)))
    v1 = next(q for q in P[1:] if sqd(d, P[0], q) == e)
    def inspan(q, a, b):
        Ev = lambda p: [E(p[k], p[k + 1], d) for k in range(0, 8, 2)]
        return rank([Ev(a), Ev(b), Ev(q)]) == 2
    dec1 = [q for q in P if inspan(q, P[0], v1)]
    perp = [q for q in P if idot(d, q, P[0]) == (0, 0) and idot(d, q, v1) == (0, 0)]
    dec2 = perp
    assert len(dec1) == 10 and len(dec2) == 10, (len(dec1), len(dec2))
    out = set(dec1) | set(dec2)
    return [p for p in P if p not in out]

# ------------------------------------------------------------------ the Queens in depth: orbits, cells, figures, One World
def deep(which, limit=None):
    t0 = time.time(); lab = (0, 0, 0, 1) if which == '600-cell' else (1, 0, 0, 0)
    S, d, n, _, _ = simple_roots('H4'); x = seed_point(S, d, n, lab); pts, perm = orbit(x, S, d); P, L = to_int(pts, d)
    V = len(P); idx = {p: i for i, p in enumerate(P)}; gens = [perm[g] for g in range(4)]
    comp = lambda a, b: [a[b[i]] for i in range(V)]                 # first b then a
    rot = [comp(gens[0], gens[j]) for j in (1, 2, 3)] + [comp(gens[1], gens[2]), comp(gens[2], gens[3])]
    def shells_of(v):
        sh = defaultdict(list)
        for j, p in enumerate(P):
            if j != v: sh[sqd(d, P[v], p)].append(j)
        return sh
    sh0 = shells_of(0); e0 = min(sh0, key=lambda s: float(E(s[0], s[1], d))); E0 = E(e0[0], e0[1], d)
    R2 = E(*idot(d, P[0], P[0]), d)
    nb = [frozenset(j for j in range(V) if j != u and sqd(d, P[u], P[j]) == e0) for u in range(V)]
    vf = set(nb)
    out = {'polytope': which, 'corners': V, 'types': {}}
    allm = dict(models(d)); allm.update(models4(d))
    for mn, Vm in allm.items():
        M = Model(mn, Vm); F0 = through(P, idx, d, 0, M, sh0)
        if not F0: out['types'][mn] = {'total': 0}; continue
        # closure under the four reflections = all residents (corner-transitivity); orbits under [3,3,5] and [3,3,5]+
        def orbits(gs, seeds):
            seen = {}; orbs = []
            for s0 in seeds:
                if s0 in seen: continue
                o = [s0]; seen[s0] = len(orbs); i = 0
                while i < len(o):
                    for gp in gs:
                        im = frozenset(gp[v] for v in o[i])
                        if im not in seen: seen[im] = len(orbs); o.append(im)
                    i += 1
                orbs.append(o)
            return orbs, seen
        orbs, seen = orbits(gens, list(F0))
        allsets = list(seen); total = len(allsets)
        assert (len(F0) * V) % M.k == 0 and total == len(F0) * V // M.k, (mn, total, len(F0))
        rorbs, _ = orbits(rot, allsets)
        # independent of the group: search from every corner (600-cell; 120-cell every corner too)
        union = set()
        for v in range(V if limit is None else limit):
            union |= set(through(P, idx, d, v, M, shells_of(v) if v else sh0))
        assert union <= set(allsets) and (limit is not None or union == set(allsets)), (mn, len(union), total)
        lab_s = {}
        for v in F0: lab_s[v] = F0[v][1]
        info = []
        for o in orbs:
            rep = o[0]; c = sorted(rep); oset = set(o)
            s = next(F0[k][1] for k in o if k in F0)          # every orbit meets the solids through corner 0 (corner-transitive)
            sig = [sum(P[v][k] for v in c) for k in range(2 * 4)]
            cen2 = E(*idot(d, sig, sig), d) / (M.k * M.k) / R2
            h = [idot(d, P[v], sig) for v in range(V)]; hs = h[c[0]]
            on = {v for v in range(V) if h[v] == hs}; above = any(isign(d, h[v][0] - hs[0], h[v][1] - hs[1]) > 0 for v in range(V))
            is_cell = (not all(x == 0 for x in sig)) and on == set(c) and not above
            info.append({'size': len(o), 'stabiliser': 14400 // len(o), 'edge2_over_polytope_edge2': repr(E(s[0], s[1], d) / E0),
                         'edge2_phi_form': phiform(E(s[0], s[1], d) / E0),
                         'centre_dist2_over_R2': repr(cen2), 'central': all(x == 0 for x in sig), 'cell': is_cell,
                         'vertex_figure': rep in vf, 'rotation_orbits': sum(1 for ro in rorbs if ro[0] in oset)})
        out['types'][mn] = {'through_corner': len(F0), 'total': total, 'orbits': info,
                            'orbit_sizes_rotation_group': sorted(len(ro) for ro in rorbs),
                            'search_from_every_corner_equals_closure': limit is None}
        out['types'][mn]['_sets'] = allsets
    # One World: inside each dodecahedron, the cubes on its corners, their tetrahedra; concentric icosahedra and octahedra
    if which == '600-cell':
        Ds, Cs, Ts, Is, Os = (out['types'][k]['_sets'] for k in ('D', 'C', 'T', 'I', 'O'))
        cen = lambda st: tuple(sum(P[v][k] for v in st) * (120 // len(st)) for k in range(8))     # 120 x centre (k divides 120)
        edge2 = lambda st: min((E(*sqd(d, P[a], P[b]), d) for a, b in itertools.combinations(sorted(st), 2)), key=float)
        ow = Counter(); ratios = Counter(); inD = Counter()
        for D in Ds:
            cubes = [C for C in Cs if C <= D]; tets = {T for T in Ts if any(T <= C for C in cubes)}
            ci = [I for I in Is if cen(I) == cen(D)]; co = [O for O in Os if cen(O) == cen(D)]
            ow[(len(cubes), len(tets), len(ci), len(co))] += 1
            for C_ in cubes: inD[('C', C_)] += 1
            for T_ in tets: inD[('T', T_)] += 1
            eD = edge2(D)
            for C in cubes: ratios['C/D ' + repr(edge2(C) / eD)] += 1
            for T in tets: ratios['T/D ' + repr(edge2(T) / eD)] += 1
            for I in ci: ratios['I/D ' + repr(edge2(I) / eD)] += 1
            for O in co: ratios['O/D ' + repr(edge2(O) / eD)] += 1
        mult = Counter((k[0], v) for k, v in inD.items())
        mult[('C', 0)] = len(Cs) - sum(1 for k in inD if k[0] == 'C'); mult[('T of edge phi sqrt2', 0)] = sum(1 for T_ in Ts if edge2(T_) / edge2(Ds[0]) == 2 * E(0, 1, 5) * E(0, 1, 5) and ('T', T_) not in inD)
        out['one_world_containment'] = {f'{t} lying in exactly {m} dodecahedra': c for (t, m), c in mult.items()}
        out['one_world'] = {'per_dodecahedron (cubes on its corners, tetrahedra in them, concentric I, concentric O)': {str(k): v for k, v in ow.items()},
                            'edge2 ratios (summed over all D)': dict(ratios)}
        # One World's sizes (Table 1 of #106, dodecahedron edge 1): which occur at all among the 600-cell's corners (edge2 / D edge2)
        ph = E(0, 1, 5)
        want = {'C phi': ('C', ph * ph), 'T phi sqrt2': ('T', 2 * ph * ph), 'O phi/sqrt2': ('O', ph * ph / 2), 'O phi^2/sqrt2': ('O', ph * ph * ph * ph / 2),
                'I 1/phi': ('I', E(1, 0, 5) / (ph * ph)), 'I 1': ('I', E(1, 0, 5))}
        eD = edge2(Ds[0]); occ = {}
        for k, (t, r) in want.items():
            occ[k] = sum(1 for st in out['types'][t]['_sets'] if edge2(st) / eD == r)
        out['one_world']['one_world_sizes_present (count of solids of that edge, D edge = 1)'] = occ
    for mn in out['types']: out['types'][mn].pop('_sets', None)
    out['seconds'] = round(time.time() - t0, 1)
    return out

# ------------------------------------------------------------------ main
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'pilot'; T0 = time.time()
    seeds = lambda r: [l for l in itertools.product((0, 1), repeat=r) if any(l)]
    jobs = [(g, l, 'wythoff') for g in ('A3', 'B3', 'H3') for l in seeds(3)]
    jobs += [('H3', l, 'prism') for l in seeds(3)]
    jobs += [(g, l, 'wythoff') for g in ('A4', 'B4', 'F4') for l in seeds(4)]
    if mode == 'pilot':
        jobs += [('H4', l, 'wythoff') for l in ((0, 0, 0, 1), (1, 0, 0, 0), (0, 0, 1, 1))]
        deeps = [('600-cell', None), ('120-cell', 3)]
    else:
        jobs += [('H4', l, 'wythoff') for l in seeds(4)] + [('H4', None, 'snub24'), ('H4', None, 'grand')]
        deeps = [('600-cell', None), ('120-cell', None)]
    jobs.sort(key=lambda j: -(H4F0[''.join(map(str, j[1]))] if j[0] == 'H4' and j[1] else 0))
    NJ = len(jobs) + len(deeps); done = 0; res = []; dres = {}
    with Pool(int(sys.argv[2]) if len(sys.argv) > 2 else 10) as pool:
        dfut = [pool.apply_async(deep, w) for w in deeps]
        for r in pool.imap_unordered(analyse, jobs):
            done += 1; res.append(r)
            print(f"PROGRESS {done / NJ:.3f} {r['group']} {r['seed']} {r['name']}: {r['corners']} corners, "
                  + ', '.join(f"{k} {v['total']}" for k, v in r['residents'].items()) + f" ({r['seconds']} s)", flush=True)
        for (w, _), f in zip(deeps, dfut):
            dres[w] = f.get(); done += 1
            print(f"PROGRESS {done / NJ:.3f} deep {w} ({dres[w]['seconds']} s)", flush=True)
    res.sort(key=lambda r: (r['kind'], r['group'], r['seed']))
    # ---------------- checks
    chk = []
    def C(name, ok): chk.append((name, bool(ok))); print(('ok   ' if ok else 'FAIL ') + name, flush=True)
    for r in res:
        if r['kind'] == 'wythoff':
            C(f"group order {r['group']} = {WORD[r['group']]}", r['group_order'] == WORD[r['group']])
            C(f"corners {r['group']} {r['seed']} = |W|/|W_J| = {r['group_order'] // r['stabiliser_order']}", r['corners'] == r['group_order'] // r['stabiliser_order'])
            if r['group'] == 'H4': C(f"corners H4 {r['seed']} = {H4F0[r['seed']]} (Coxeter)", r['corners'] == H4F0[r['seed']])
        if r['kind'] == 'prism': C(f"prism corners {r['seed']} = 2 x |W|/|W_J|", r['corners'] == 2 * (r['group_order'] // 2) // r['stabiliser_order'])
    get = lambda g, s: next(r for r in res if r['group'] == g and r['seed'] == s and r['kind'] == 'wythoff')
    tot = lambda r: {k: v['total'] for k, v in r['residents'].items()}
    C('control: tetrahedron holds T 1 only', tot(get('A3', '100')) == {'T': 1})
    C('control: cube holds C 1, T 2 only', tot(get('B3', '100')) == {'C': 1, 'T': 2})
    C('control: octahedron holds O 1 only', tot(get('B3', '001')) == {'O': 1})
    C('control: dodecahedron holds D 1, C 5, T 10 only (Euclid XIII.17; Kepler)', tot(get('H3', '100')) == {'D': 1, 'C': 5, 'T': 10})
    C('control: icosahedron holds I 1 only', tot(get('H3', '001')) == {'I': 1})
    C('control: icosidodecahedron holds O 5 only', tot(get('H3', '010')) == {'O': 5})
    q = dres['600-cell']['types']
    C('control: 600-cell 600 tetrahedral cells (Coxeter)', sum(o['size'] for o in q['T']['orbits'] if o['cell']) == 600)
    C('control: 600-cell 120 icosahedral vertex figures (Coxeter)', sum(o['size'] for o in q['I']['orbits'] if o['vertex_figure']) == 120)
    C('control: 600-cell 25 inscribed 24-cells', q['24-cell']['total'] == 25)
    C('control: 600-cell 75 inscribed 16-cells', q['16-cell']['total'] == 75)
    if mode == 'full':
        h = dres['120-cell']['types']
        C('control: 120-cell 120 dodecahedral cells (Coxeter)', sum(o['size'] for o in h['D']['orbits'] if o['cell']) == 120)
        C('control: 120-cell 5-cells in two orbits, 120 (full stabiliser S5, the regular compound of 120 5-cells) and 720',
          sorted(o['size'] for o in h['5-cell']['orbits']) == [120, 720] and any(o['size'] == 120 and o['stabiliser'] == 120 for o in h['5-cell']['orbits']))
        C('control: 120-cell 675 inscribed 16-cells', h['16-cell']['total'] == 675)
    # the Law of Residents, exact
    fam = defaultdict(set); every = defaultdict(list)
    for r in res:
        if r['kind'] == 'wythoff' and r['group'][1] == '4':
            fam[r['group']] |= set(r['residents']); every[r['group']].append(set(r['residents']))
    for g in fam: print(f"LAW {g}: union of residents {sorted(fam[g])}; per polytope {[''.join(sorted(s)) for s in every[g]]}", flush=True)
    C('no D or I in any A4, B4, F4 polytope (and the field argument)', all(not ({'D', 'I'} & fam[g]) for g in ('A4', 'B4', 'F4')))
    if mode == 'full':
        C('every H4 polytope houses all five', len(every['H4']) == 15 and all(s == {'D', 'I', 'C', 'T', 'O'} for s in every['H4']))
    json.dump({'mode': mode, 'polytopes': res, 'queens': dres, 'checks': chk}, open(f'data/residents-{mode}.json', 'w'), indent=1)
    print(f"{len(chk)} checks, {sum(1 for c in chk if not c[1])} failed, {time.time() - T0:.0f} s", flush=True)
    print('FINAL ok' if chk and all(c[1] for c in chk) else 'FINAL FAIL', flush=True)
