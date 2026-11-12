# Palindromic middles (13 Nov 2026; lead 4 of studies/2026-11-13-swaps-and-fixed-points, lead 3 of the 13 Nov run).
# Question: for A4 and F4 the seed reversal (a1,a2,a3,a4) -> (a4,a3,a2,a1) is a true symmetry (a diagram automorphism realised by an
# isometry), so near-but-never-on Theorem B predicts that the first tone of the canonical form (and of the corners) vanishes EXACTLY
# at every palindromic seed. Test it exactly; controls that must pass and controls that must fail (B4, H4 middles; non-palindromic seeds).
#
# Words. S = Wythoff polytope of seed lam (edge lengths: the edge along node i has length lam_i), centred at 0. Its polar S° = conv(n/c)
# over the cells {n.z <= c}. Moment t_k(y) = INT_{S°} (x.y)^k dx: the degree-k Taylor term of the canonical form at the centre, up to the
# factor d! C(k+d, d) (moment identity of the aim 2 draft). Corner moment C_k(y) = SUM_corners (v.y)^k.
# Tone: t_k is a W-invariant polynomial in y; when the only degree-k invariants are |y|^k and one harmonic H_k (A4 k = 3: H_3 only;
# B4 k = 4; F4 k = 6; H4 k = 12), t_k(y1) - t_k(y2) at |y1| = |y2| is T (H(y1) - H(y2)), T the tone. In general we test ISOTROPY:
# t_k(y)/|y|^k the same for several y of one norm (for odd k: t_k = 0). Isotropic at the first degree k  <=>  tone T = 0.
# Exact integration: pulling triangulation of each polar facet (combinatorial, from the corner figure: cells at a corner, cyclic order
# of the cells round each edge from the 2-faces), cone from the origin; INT_simplex (l.x)^k = vol k! d!/(k+d)! h_k(l.v_0..l.v_d)
# (h_k the complete homogeneous symmetric polynomial; v_0 = 0). Arithmetic in Q(sqrt m), m = 2 (A4, B4, F4) or 5 (H4). No floats decide.
# The construction of corners, cells and 2-faces at the base corner follows rosette_balance.py build() (studies/2026-11-13-rosette-balance).
import sys, itertools, time, json, os
from fractions import Fraction as Fr
from math import factorial
from multiprocessing import Pool

M = 2
class QS:
    """a + b sqrt(M), a, b rational"""
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a = a if type(a) is Fr else Fr(a); s.b = b if type(b) is Fr else Fr(b)
    def __add__(s, o):
        if type(o) is not QS: o = QS(o)
        return QS(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o):
        if type(o) is not QS: o = QS(o)
        return QS(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return QS(o) - s
    def __neg__(s): return QS(-s.a, -s.b)
    def __mul__(s, o):
        if type(o) is not QS: o = QS(o)
        return QS(s.a * o.a + M * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - M * s.b * s.b; return QS(s.a / n, -s.b / n)
    def __truediv__(s, o):
        if type(o) is not QS: o = QS(o)
        return s * o.inv()
    def z(s): return s.a == 0 and s.b == 0
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        c = a * a - M * b * b
        return (1 if a > 0 else -1) if c > 0 else (1 if b > 0 else -1)
    def __eq__(s, o):
        if type(o) is not QS: o = QS(o)
        return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __float__(s): return float(s.a) + float(s.b) * M ** 0.5
    def __repr__(s): return f'{s.a}' if s.b == 0 else f'({s.a} + {s.b} sqrt{M})'

def dot(u, v):
    t = QS(0)
    for a, b in zip(u, v): t = t + a * b
    return t
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def scal(c, v): return tuple(c * a for a in v)
def refl(al, nal, v): return sub(v, scal(QS(2) * dot(al, v) / nal, al))
def rank(vecs):
    Mx = [list(v) for v in vecs]; r = 0; ncol = len(Mx[0]) if Mx else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(Mx)) if not Mx[i][c].z()), None)
        if p is None: continue
        Mx[r], Mx[p] = Mx[p], Mx[r]
        for i in range(len(Mx)):
            if i != r and not Mx[i][c].z():
                f = Mx[i][c] / Mx[r][c]; Mx[i] = [a - f * b for a, b in zip(Mx[i], Mx[r])]
        r += 1
    return r
def det(Mx):
    Mx = [list(r) for r in Mx]; n = len(Mx); D = QS(1)
    for c in range(n):
        p = next((i for i in range(c, n) if not Mx[i][c].z()), None)
        if p is None: return QS(0)
        if p != c: Mx[c], Mx[p] = Mx[p], Mx[c]; D = -D
        D = D * Mx[c][c]; ic = Mx[c][c].inv()
        for i in range(c + 1, n):
            if not Mx[i][c].z():
                f = Mx[i][c] * ic; Mx[i] = [a - f * b for a, b in zip(Mx[i], Mx[c])]
    return D
def solve(G, b):
    n = len(G); Mx = [list(G[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if not Mx[i][c].z()); Mx[c], Mx[p] = Mx[p], Mx[c]
        for i in range(n):
            if i != c and not Mx[i][c].z():
                f = Mx[i][c] / Mx[c][c]; Mx[i] = [a - f * bb for a, bb in zip(Mx[i], Mx[c])]
    return [Mx[i][n] / Mx[i][i] for i in range(n)]

H = Fr(1, 2)
def h4_roots():
    PHI = QS(H, H); R = set(); ip = QS(-H, H)
    for i in range(4):
        for s in (1, -1): v = [QS(0)] * 4; v[i] = QS(s); R.add(tuple(v))
    for ss in itertools.product((H, -H), repeat=4): R.add(tuple(QS(x) for x in ss))
    base = [PHI * H, QS(H), ip * H, QS(0)]
    for p in itertools.permutations(range(4)):
        if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2: continue
        for ss in itertools.product((1, -1), repeat=3):
            v = [QS(0)] * 4; vals = [base[0] * ss[0], base[1] * ss[1], base[2] * ss[2], QS(0)]
            for k in range(4): v[p[k]] = vals[k]
            R.add(tuple(v))
    R = sorted(R, key=lambda v: [float(x) for x in v]); assert len(R) == 120
    return R
def roots(g):
    q = lambda *xs: tuple(QS(x) for x in xs)
    if g == 'A4': return [q(*[1 if k == i else -1 if k == i + 1 else 0 for k in range(5)]) for i in range(4)]
    if g == 'B4': return [q(0, 0, 0, 1), q(0, 0, 1, -1), q(0, 1, -1, 0), q(1, -1, 0, 0)]
    if g == 'F4': return [q(0, 1, -1, 0), q(0, 0, 1, -1), q(0, 0, 0, 1), q(H, -H, -H, -H)]
    if g == 'H4':
        R = h4_roots(); PHI = QS(H, H); f = lambda u, v: float(dot(u, v))
        a1 = R[0]
        for a2 in R:
            if abs(f(a1, a2) + float(PHI) / 2) > 1e-9: continue
            for a3 in R:
                if abs(f(a2, a3) + .5) > 1e-9 or abs(f(a1, a3)) > 1e-9: continue
                for a4 in R:
                    if abs(f(a3, a4) + .5) > 1e-9 or abs(f(a1, a4)) > 1e-9 or abs(f(a2, a4)) > 1e-9: continue
                    S = [a1, a2, a3, a4]; assert dot(a1, a2) == -PHI * H and dot(a2, a3) == QS(-H)
                    return S
    raise ValueError(g)
FIELD = {'A4': 2, 'B4': 2, 'F4': 2, 'H4': 5}
def rootlen(g, a):    # |a| exactly in Q(sqrt M)
    n2 = dot(a, a)
    if g == 'H4': assert n2 == QS(1); return QS(1)
    if n2 == QS(1): return QS(1)
    assert n2 == QS(2); return QS(0, 1)            # sqrt 2 (M = 2)

def build(g, lam):
    """corners (with the cell normals transported to each), cell offsets, and the triangulation template of the polar facet"""
    A = roots(g); nA = [dot(a, a) for a in A]; n = len(A[0])
    G = [[dot(A[i], A[j]) for j in range(4)] for i in range(4)]
    om = []
    for j in range(4):
        c = solve(G, [QS(1 if i == j else 0) for i in range(4)])
        om.append(tuple(sum((c[k] * A[k][t] for k in range(4)), QS(0)) for t in range(n)))
    # seed by edge lengths: alpha_i . x = lam_i |alpha_i| / 2  (edge x -> s_i x has length lam_i)
    lab = [QS(lam[i]) * rootlen(g, A[i]) * QS(H) for i in range(4)]
    x = tuple(sum((lab[j] * om[j][t] for j in range(4)), QS(0)) for t in range(n))
    for i in range(4): assert dot(A[i], x) == lab[i]
    for i in range(4):
        if lam[i]: assert dot(*(2 * [sub(refl(A[i], nA[i], x), x)])) == QS(lam[i]) * QS(lam[i])
    U = [i for i in range(4) if not lam[i]]
    def orbit(v0, gens):
        seen = {v0}; st = [v0]
        while st:
            v = st.pop()
            for k in gens:
                y = refl(A[k], nA[k], v)
                if y not in seen: seen.add(y); st.append(y)
        return seen
    edges = []
    for i in range(4):
        if not lam[i]: continue
        for beta in orbit(A[i], U):
            d = sub(refl(beta, dot(beta, beta), x), x)
            if d not in edges: edges.append(d)
    e = len(edges)
    cells = []
    for j in range(4):
        for nn in orbit(om[j], U):
            E = frozenset(k for k, d in enumerate(edges) if dot(nn, d).z())
            assert all(dot(nn, d).sign() <= 0 for d in edges)
            if len(E) >= 3 and rank([edges[k] for k in E]) == 3: cells.append((j + 1, E, nn, dot(nn, x)))
    faces = []
    for a, b in itertools.combinations(range(e), 2):
        cont = [ci for ci, c in enumerate(cells) if a in c[1] and b in c[1]]
        if len(cont) < 2: continue
        if frozenset.intersection(*[cells[ci][1] for ci in cont]) == {a, b}:
            assert len(cont) == 2; faces.append(((a, b), tuple(cont)))
    assert e - len(faces) + len(cells) == 2
    # polar facet at x: vertices = cells; its 2-faces = edges at x (the cells round edge k, cyclic via the 2-faces through k)
    tmpl = []
    for k in range(e):
        cs = [ci for ci, c in enumerate(cells) if k in c[1]]
        if 0 in cs: continue
        adj = {ci: [] for ci in cs}
        for (ab, (c1, c2)) in faces:
            if k in ab: adj[c1].append(c2); adj[c2].append(c1)
        assert all(len(v) == 2 for v in adj.values()), 'cells round an edge form a cycle'
        cyc = [cs[0]]; prev = None
        while len(cyc) < len(cs):
            nxt = [c for c in adj[cyc[-1]] if c != prev][0]; prev = cyc[-1]; cyc.append(nxt)
        for i in range(1, len(cyc) - 1): tmpl.append((0, cyc[0], cyc[i], cyc[i + 1]))
    # corners by BFS, cell normals transported
    idx = {x: 0}; verts = [x]; nrm = [[c[2] for c in cells]]; q = [0]
    while q:
        nq = []
        for vi in q:
            for i in range(4):
                y = refl(A[i], nA[i], verts[vi])
                if y not in idx:
                    idx[y] = len(verts); verts.append(y); nrm.append([refl(A[i], nA[i], m_) for m_ in nrm[vi]]); nq.append(idx[y])
        q = nq
    offs = [c[3] for c in cells]
    return dict(A=A, x=x, verts=verts, nrm=nrm, offs=offs, tmpl=tmpl, cells=cells, edges=e, n=n, types=[c[0] for c in cells])

def hseq(vals, K):
    """h_0..h_K of the values"""
    h = [QS(1)] + [QS(0)] * K
    for a in vals:
        pw = [QS(1)]
        for _ in range(K): pw.append(pw[-1] * a)
        h = [sum((h[i] * pw[j - i] for i in range(j + 1)), QS(0)) for j in range(K + 1)]
    return h

def moments(P, ys, ks):
    """t_k(y) (up to one constant factor per polytope family: sqrt5 for A4 in R^5) and C_k(y) for every y, k"""
    K = max(ks); d = 4; ext = P['n'] == 5
    T = {(yi, k): QS(0) for yi in range(len(ys)) for k in ks}; C = {(yi, k): QS(0) for yi in range(len(ys)) for k in ks}
    invo = [o.inv() for o in P['offs']]
    for v, nl in zip(P['verts'], P['nrm']):
        pts = [scal(io, m_) for io, m_ in zip(invo, nl)]
        for yi, y in enumerate(ys):
            vy = dot(v, y); p = QS(1)
            for k in range(1, K + 1):
                p = p * vy
                if k in ks: C[(yi, k)] = C[(yi, k)] + p
        for t in P['tmpl']:
            S = [pts[c] for c in t]
            D = det([list(s) for s in S] + ([[QS(1)] * 5] if ext else []))
            vol = D if D.sign() > 0 else -D
            for yi, y in enumerate(ys):
                h = hseq([dot(s, y) for s in S], K)
                for k in ks: T[(yi, k)] = T[(yi, k)] + vol * h[k]
    for (yi, k) in T: T[(yi, k)] = T[(yi, k)] * QS(Fr(factorial(k) * factorial(d), factorial(k + d) * factorial(d)))   # vol = |det|/d!
    return T, C

def yset(g):
    """four vectors of one squared norm in four DIFFERENT W-orbits (orbit membership checked exactly by BFS over the reflections).
    Pilot fault (13 Nov): (6,3,2,1) and (5,4,3,0) are one F4 orbit, so their difference saw no tone; now excluded by construction."""
    A = roots(g); nA = [dot(a, a) for a in A]; n = len(A[0])
    def orbit(v0):
        seen = {v0}; st = [v0]
        while st:
            v = st.pop()
            for k in range(4):
                y = refl(A[k], nA[k], v)
                if y not in seen: seen.add(y); st.append(y)
        return seen
    rng = range(-8, 9) if n == 4 else range(-5, 6)
    for N in ([26, 30, 34, 36, 38, 42] if n == 5 else [50, 66, 90, 98, 126, 130]):
        cands = sorted({tuple(sorted(v, reverse=True)) for v in itertools.product(rng, repeat=n) if sum(c * c for c in v) == N and (n == 4 or sum(v) == 0)})
        chosen, orbs = [], []
        for c in cands:
            y = tuple(QS(a) for a in c)
            if any(y in o for o in orbs): continue
            chosen.append(y); orbs.append(orbit(y))
            if len(chosen) == 4: return chosen
    raise ValueError('no four orbits')

def iso_report(vals, k, ys):
    """isotropic at degree k: all t_k(y) equal (k even) / all zero (k odd); returns (isotropic, list of values, max difference)"""
    v = [vals[(yi, k)] for yi in range(len(ys))]
    if k % 2: iso = all(x.z() for x in v)
    else: iso = all((x - v[0]).z() for x in v)
    return iso, v

def task(args):
    g, lam, ks, tag, ys = args
    global M; M = FIELD[g]
    t0 = time.time(); P = build(g, lam); ys = [tuple(QS(Fr(a), Fr(b)) for a, b in y) for y in ys]
    for y in ys: assert dot(y, y) == dot(ys[0], ys[0])
    T, C = moments(P, ys, ks)
    out = dict(g=g, lam=[str(l) for l in lam], tag=tag, corners=len(P['verts']), cells_at_corner=len(P['cells']), simple=(len(P['cells']) == 4),
               simplices=len(P['tmpl']) * len(P['verts']), secs=round(time.time() - t0, 1), form={}, corner={})
    for k in ks:
        iso, v = iso_report(T, k, ys); out['form'][k] = dict(isotropic=iso, diff01=repr(v[0] - v[1]), diff01_f=float(v[0] - v[1]),
                                                           val0=repr(v[0]), val0_f=float(v[0]))
        iso, v = iso_report(C, k, ys); out['corner'][k] = dict(isotropic=iso, diff01=repr(v[0] - v[1]), diff01_f=float(v[0] - v[1]),
                                                             val0=repr(v[0]), val0_f=float(v[0]))
    # equal facet distances of the two end cell types (the fixed point of the polar line): c^2/|n|^2 per type
    dist = {}
    for (tp, E, nn, c) in P['cells']: dist.setdefault(tp, c * c / dot(nn, nn))
    out['cell_dist2'] = {tp: repr(v) for tp, v in dist.items()}
    out['ends_equidistant'] = (1 in dist and 4 in dist and dist[1] == dist[4])
    out['raw'] = {'T': {f'{yi},{k}': (str(T[(yi, k)].a), str(T[(yi, k)].b)) for (yi, k) in T},
                  'C': {f'{yi},{k}': (str(C[(yi, k)].a), str(C[(yi, k)].b)) for (yi, k) in C}}
    return out

def control_cube():
    """positive control: tesseract with corners (+-1)^4 (B4 seed (2,0,0,0)): polar = cross-polytope |x|_1 <= 1,
    INT x1^2 = 2/45, INT x1^4 = 1/105, INT (x1 x2)^2 = 4/2520 * ... checked through t_k(e1), t_4((1,1,0,0))"""
    global M; M = 2
    P = build('B4', (2, 0, 0, 0)); assert len(P['verts']) == 16 and all(all(abs(float(c)) == 1 for c in v) for v in P['verts'])
    ys = [tuple(QS(c) for c in (1, 0, 0, 0)), tuple(QS(c) for c in (1, 1, 0, 0))]
    T, C = moments(P, ys, [2, 4])
    # cross-polytope: INT x1^2 = 16 * 2/6! = 2/45; INT x1^4 = 16 * 4!/8! = 1/105; INT x1^2 x2^2 = 16 * 2!2!/8! = 1/630
    exp = {(0, 2): Fr(2, 45), (0, 4): Fr(1, 105), (1, 2): Fr(4, 45), (1, 4): 2 * Fr(1, 105) + 6 * Fr(1, 630)}
    return all(T[key] == QS(v) for key, v in exp.items()), {f'{a},{b}': repr(T[(a, b)]) for (a, b) in exp}

PAL = [(0, 1, 1, 0), (1, 0, 0, 1), (1, 1, 1, 1), (1, 2, 2, 1), (2, 1, 1, 2)]
NONPAL = [(0, 1, 1, 1), (1, 1, 1, 0), (1, 1, 0, 0), (0, 0, 1, 1), (1, 2, 3, 4), (4, 3, 2, 1)]
LINE_T = [Fr(2), Fr(1, 2), Fr(3), Fr(1, 3), Fr(3, 2), Fr(2, 3)]
def tasks(pilot):
    T = []
    for lam in PAL: T.append(('A4', lam, [2, 3, 4, 5], 'palindrome')); T.append(('F4', lam, [2, 4, 6, 8], 'palindrome'))
    for lam in NONPAL: T.append(('A4', lam, [2, 3, 4], 'non-palindrome')); T.append(('F4', lam, [2, 4, 6], 'non-palindrome'))
    for t in LINE_T: T.append(('A4', (0, 1, t, 0), [3], 'line')); T.append(('F4', (0, 1, t, 0), [6], 'line'))
    for t in [Fr(1), Fr(2), Fr(1, 2), Fr(3, 2), Fr(2, 3)]: T.append(('B4', (0, 1, t, 0), [2, 4], 'B4 line'))
    T.append(('B4', (1, 0, 0, 1), [2, 4], 'B4 palindrome')); T.append(('B4', (1, 1, 1, 1), [2, 4], 'B4 palindrome'))
    if not pilot:
        for lam in [(0, 1, 1, 0), (1, 1, 1, 1)]: T.append(('F4', lam, [10, 12], 'palindrome high'))
        T.append(('A4', (0, 1, 1, 0), [6, 7], 'palindrome high')); T.append(('A4', (1, 1, 1, 1), [6, 7], 'palindrome high'))
        T.append(('H4', (0, 1, 1, 0), [2, 6, 12], 'H4 middle'))
        for t in [Fr(2), Fr(1, 2)]: T.append(('H4', (0, 1, t, 0), [12], 'H4 line'))
    return T

def progress(f, what): print(f'PROGRESS {f:.3f} {what}', flush=True)

if __name__ == '__main__':
    pilot = 'pilot' in sys.argv[1:]; nproc = 4; t0 = time.time()
    ok_cube, cube_vals = control_cube(); print(f'CONTROL cross-polytope moments exact: {"ok" if ok_cube else "FAIL"} {cube_vals}', flush=True)
    YS = {}
    for g in sorted({t[0] for t in tasks(pilot)}):
        globals()['M'] = FIELD[g]; YS[g] = [tuple((str(c.a), str(c.b)) for c in y) for y in yset(g)]
        print(f'test vectors {g}: ' + ' '.join('(' + ','.join(a for a, b in y) + ')' for y in YS[g]), flush=True)
    TS = [t + (YS[t[0]],) for t in tasks(pilot)]; TS.sort(key=lambda t: -{'H4': 100, 'F4': 10, 'B4': 3, 'A4': 1}[t[0]] * (1 + sum(1 for a in t[1] if a)))
    res = []
    with Pool(nproc) as pool:
        for i, r in enumerate(pool.imap_unordered(task, TS)):
            res.append(r); progress((i + 1) / len(TS), f"{r['g']} {r['lam']} {r['tag']} ({r['secs']} s)")
    key = lambda r: (r['g'], r['tag'], r['lam'])
    res.sort(key=key)
    checks = []
    def chk(name, cond, expect_pass=True): checks.append((name, bool(cond), expect_pass)); print(f"  {'ok' if bool(cond) else 'FAIL'}  {name}", flush=True)
    chk('control: cross-polytope moments 2/45, 1/105 exact', ok_cube)
    print('\n== per polytope: isotropy of the form moment t_k and the corner moment C_k (iso = no tone in degree k)')
    for r in res:
        fs = ' '.join(f"k{k}: form {'iso' if v['isotropic'] else 'TONE %.6g' % v['diff01_f']}, corners {'iso' if r['corner'][k]['isotropic'] else 'TONE %.6g' % r['corner'][k]['diff01_f']};"
                      for k, v in r['form'].items())
        print(f"{r['g']} {'(' + ','.join(r['lam']) + ')':<16} {r['tag']:<16} corners {r['corners']:>5} cells/corner {r['cells_at_corner']} ends equidistant {r['ends_equidistant']}  {fs}", flush=True)
    get = lambda g, lam, tag: next(r for r in res if r['g'] == g and r['lam'] == [str(Fr(a)) for a in lam] and r['tag'] == tag)
    print('\n== checks')
    for r in res:   # positive controls: degree 2 isotropic everywhere; F4 degree 4 isotropic everywhere; H4 degree 6
        chk(f"{r['g']} {r['lam']} degree 2 isotropic (form and corners)", r['form'].get(2, {'isotropic': True})['isotropic'] and r['corner'].get(2, {'isotropic': True})['isotropic'])
        if r['g'] == 'F4' and 4 in r['form']: chk(f"F4 {r['lam']} degree 4 isotropic (no F4 invariant of degree 4)", r['form'][4]['isotropic'] and r['corner'][4]['isotropic'])
        if r['g'] == 'H4' and 6 in r['form']: chk(f"H4 {r['lam']} degree 6 isotropic (no H4 invariant of degree 6)", r['form'][6]['isotropic'] and r['corner'][6]['isotropic'])
    for lam in PAL:   # THE PREDICTION
        a = get('A4', lam, 'palindrome'); f = get('F4', lam, 'palindrome')
        chk(f"PREDICTION A4 {lam}: degree-3 tone zero (form and corners)", a['form'][3]['isotropic'] and a['corner'][3]['isotropic'])
        chk(f"PREDICTION F4 {lam}: degree-6 tone zero (form and corners)", f['form'][6]['isotropic'] and f['corner'][6]['isotropic'])
        chk(f"A4 {lam}: degree-5 odd moment zero too (-I in the extended group)", a['form'][5]['isotropic'] and a['corner'][5]['isotropic'])
        chk(f"SHOULD FAIL TO VANISH: A4 {lam} degree-4 tone nonzero (even, survives -I)", (not a['form'][4]['isotropic']) and (not a['corner'][4]['isotropic']))
    for lam in [(0, 1, 1, 0)]:
        chk(f"A4 {lam}: ends equidistant (fixed point of the 5-cell polar line = uniform bitruncated 5-cell)", get('A4', lam, 'palindrome')['ends_equidistant'])
        chk(f"F4 {lam}: ends equidistant (fixed point of the 24-cell polar line = uniform bitruncated 24-cell)", get('F4', lam, 'palindrome')['ends_equidistant'])
    for lam in NONPAL:   # controls that must FAIL to vanish
        a = get('A4', lam, 'non-palindrome'); f = get('F4', lam, 'non-palindrome')
        chk(f"SHOULD FAIL TO VANISH: A4 {lam} degree-3 tone nonzero", (not a['form'][3]['isotropic']) and (not a['corner'][3]['isotropic']))
        chk(f"SHOULD FAIL TO VANISH: F4 {lam} degree-6 tone nonzero", (not f['form'][6]['isotropic']) and (not f['corner'][6]['isotropic']))
    # reversed pairs: tone(reverse seed) = eps tone(seed) (same edge lengths, so no rescaling)
    def raw(r, kind, yi, k):
        a, b = r['raw'][kind][f'{yi},{k}']; return QS(Fr(a), Fr(b))
    eps_seen = {}
    for g, k in (('A4', 3), ('F4', 6)):
        globals()['M'] = FIELD[g]
        for l1, l2 in [((0, 1, 1, 1), (1, 1, 1, 0)), ((1, 1, 0, 0), (0, 0, 1, 1)), ((1, 2, 3, 4), (4, 3, 2, 1))]:
            r1, r2 = get(g, l1, 'non-palindrome'), get(g, l2, 'non-palindrome')
            for kind in ('T', 'C'):
                d1 = raw(r1, kind, 0, k) - raw(r1, kind, 1, k); d2 = raw(r2, kind, 0, k) - raw(r2, kind, 1, k)
                eps = 0 if d1.z() else 1 if (d1 - d2).z() else -1 if (d1 + d2).z() else 0
                eps_seen.setdefault((g, kind), set()).add(eps)
                chk(f"{g} reversed pair {l1} / {l2} ({kind}): tone(reverse) = eps tone, eps = {eps}", eps != 0)
    # along the seed line (0,1,t,0): P(0,t,1,0) = t P(0,1,1/t,0) and the reversal isometry: T(t) = eps t^-(d+k) T(1/t); C(t) = eps t^k C(1/t)
    for g, k in (('A4', 3), ('F4', 6)):
        globals()['M'] = FIELD[g]
        for t in [Fr(2), Fr(3), Fr(3, 2)]:
            r1, r2 = get(g, (0, 1, t, 0), 'line'), get(g, (0, 1, 1 / t, 0), 'line')
            for kind, pw in (('T', -(4 + k)), ('C', k)):
                d1 = raw(r1, kind, 0, k) - raw(r1, kind, 1, k); d2 = (raw(r2, kind, 0, k) - raw(r2, kind, 1, k)) * QS(t ** pw)
                eps = 0 if d1.z() else 1 if (d1 - d2).z() else -1 if (d1 + d2).z() else 0
                chk(f"{g} line (0,1,t,0) parity at t = {t} ({kind}): eps = {eps} (0 = degenerate), tone nonzero off t = 1: {not d1.z()}", eps == -1)
    # B4: no reversal symmetry. The same parity identity must FAIL, and the middle's degree-4 tone must be nonzero
    globals()['M'] = 2
    b1 = get('B4', (0, 1, 1, 0), 'B4 line')
    chk('SHOULD FAIL TO VANISH: B4 (0,1,1,0) bitruncated tesseract degree-4 tone nonzero (form and corners)', (not b1['form'][4]['isotropic']) and (not b1['corner'][4]['isotropic']))
    for lam in [(1, 0, 0, 1), (1, 1, 1, 1)]:
        r = get('B4', lam, 'B4 palindrome')
        chk(f'SHOULD FAIL TO VANISH: B4 {lam} degree-4 tone nonzero', (not r['form'][4]['isotropic']) and (not r['corner'][4]['isotropic']))
    for t in [Fr(2), Fr(3, 2)]:
        r1, r2 = get('B4', (0, 1, t, 0), 'B4 line'), get('B4', (0, 1, 1 / t, 0), 'B4 line')
        bad = True
        for kind, pw in (('T', -8), ('C', 4)):
            d1 = raw(r1, kind, 0, 4) - raw(r1, kind, 1, 4); d2 = (raw(r2, kind, 0, 4) - raw(r2, kind, 1, 4)) * QS(t ** pw)
            bad &= not ((d1 - d2).z() or (d1 + d2).z())
        chk(f'SHOULD FAIL: B4 line parity identity at t = {t} (no reversal symmetry)', bad)
    # B4 line: sign of the form tone at t = 1/2, 2/3, 1, 3/2, 2 (where is its zero?)
    sg = []
    for t in [Fr(1, 2), Fr(2, 3), Fr(1), Fr(3, 2), Fr(2)]:
        r = get('B4', (0, 1, t, 0), 'B4 line'); sg.append((str(t), r['form'][4]['diff01_f'], r['corner'][4]['diff01_f']))
    print('B4 line (0,1,t,0) degree-4 tone (form diff, corner diff):', sg, flush=True)
    if not pilot:
        h = get('H4', (0, 1, 1, 0), 'H4 middle')
        chk('SHOULD FAIL TO VANISH: H4 (0,1,1,0) bitruncated 600-cell degree-12 tone nonzero', (not h['form'][12]['isotropic']) and (not h['corner'][12]['isotropic']))
        globals()['M'] = 5
        for t in [Fr(2)]:
            r1, r2 = get('H4', (0, 1, t, 0), 'H4 line'), get('H4', (0, 1, 1 / t, 0), 'H4 line')
            bad = True
            for kind, pw in (('T', -16), ('C', 12)):
                d1 = raw(r1, kind, 0, 12) - raw(r1, kind, 1, 12); d2 = (raw(r2, kind, 0, 12) - raw(r2, kind, 1, 12)) * QS(t ** pw)
                bad &= not ((d1 - d2).z() or (d1 + d2).z())
            chk(f'SHOULD FAIL: H4 line parity identity at t = {t}', bad)
        for lam in [(0, 1, 1, 0), (1, 1, 1, 1)]:
            r = get('F4', lam, 'palindrome high')
            print(f"F4 {lam} degree 10: form {'iso' if r['form'][10]['isotropic'] else 'TONE'}, corners {'iso' if r['corner'][10]['isotropic'] else 'TONE'}; "
                  f"degree 12: form {'iso' if r['form'][12]['isotropic'] else 'TONE'}, corners {'iso' if r['corner'][12]['isotropic'] else 'TONE'}", flush=True)
        for lam in [(0, 1, 1, 0), (1, 1, 1, 1)]:
            r = get('A4', lam, 'palindrome high')
            chk(f'A4 {lam} degree 7 odd moment zero', r['form'][7]['isotropic'] and r['corner'][7]['isotropic'])
            print(f"A4 {lam} degree 6: form {'iso' if r['form'][6]['isotropic'] else 'TONE'}, corners {'iso' if r['corner'][6]['isotropic'] else 'TONE'}", flush=True)
    for r in res:
        if r['g'] == 'F4' and r['tag'] == 'palindrome':
            print(f"F4 {r['lam']} degree 8: form {'iso' if r['form'][8]['isotropic'] else 'TONE %.6g' % r['form'][8]['diff01_f']}, corners {'iso' if r['corner'][8]['isotropic'] else 'TONE %.6g' % r['corner'][8]['diff01_f']}", flush=True)
    print('eps per (group, moment):', {f'{a} {b}': sorted(v) for (a, b), v in eps_seen.items()}, flush=True)
    nbad = sum(1 for c in checks if not c[1])
    json.dump(dict(results=[{k: v for k, v in r.items() if k != 'raw'} for r in res], raw={f"{r['g']} {r['lam']} {r['tag']}": r['raw'] for r in res},
                   checks=[dict(name=a, ok=b) for a, b, _ in checks]),
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f"middles{'-pilot' if pilot else ''}.json"), 'w'), indent=1)
    print(f'{len(checks)} checks, {nbad} FAIL; {time.time() - t0:.0f} s', flush=True)
    if nbad == 0: print('FINAL ok', flush=True)
    else: print('FINAL FAIL', flush=True)
