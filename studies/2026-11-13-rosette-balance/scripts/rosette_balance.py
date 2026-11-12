"""Open question 8.2 (The Permutohedron Paradigm, Chapter 8): the balance law for rosette tissues.
EXACT arithmetic throughout (Fractions; Q(sqrt5) for H4). Parts:
 W  every Wythoff 4-polytope of A4, B4, F4, H4 (all 0/1 seeds): local face structure at the base corner (edges, 2-faces, cells with
    their kinds), the sweep ledger of corner events in several exact generic directions, checks of:
    (a) the ledger is the same in every generic direction (Lemma 1),
    (b) every event class is matched by its reverse (Theorem 2), coarse (kinds) and fine (orbit of the down-set under the corner's
        stabiliser),
    (c) the toric h-vector of the dual, summed corner by corner (Proposition 3), equals the global formula, is palindromic, and for
        the simple rows is the classical h-vector (controls: Chapter 7 / #108 table),
    (d) the swap ledger of the simple rows against #108 (Theorem 1 table), and the edge count of Theorem 8.1.
 G  general (non-symmetric) rosette tissues: generic rational perturbations of the 16-cell and the 600-cell (combinatorics kept,
    checked exactly), every corner a rosette (6 resp. 12 edges), one cell type; test (b) in random exact directions.
Usage: rosette_balance.py [pilot|full] [jobs]   prints PROGRESS lines and FINAL ok / FAIL."""
import sys, json, itertools, random, time, os
from fractions import Fraction as Fr
from collections import Counter, defaultdict
from multiprocessing import Pool

class QF:
    """a + b sqrt5, a, b rational"""
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = o if isinstance(o, QF) else QF(o); return QF(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, QF) else QF(o); return QF(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return QF(o) - s
    def __neg__(s): return QF(-s.a, -s.b)
    def __mul__(s, o): o = o if isinstance(o, QF) else QF(o); return QF(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return QF(s.a / n, -s.b / n)
    def __truediv__(s, o): o = o if isinstance(o, QF) else QF(o); return s * o.inv()
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        c = a * a - 5 * b * b          # a and b of opposite signs
        return (1 if a > 0 else -1) if c > 0 else (1 if b > 0 else -1)
    def __eq__(s, o): o = o if isinstance(o, QF) else QF(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __repr__(s): return f'{s.a}' if s.b == 0 else f'({s.a}+{s.b}r5)'

def dot(u, v):
    t = QF(0)
    for a, b in zip(u, v): t = t + a * b
    return t
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def scal(c, v): return tuple(c * a for a in v)
def refl(al, nal, v): return sub(v, scal(QF(2) * dot(al, v) / nal, al))   # nal = al.al
def rank(vecs):
    M = [list(v) for v in vecs]; r = 0; ncol = len(M[0]) if M else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(M)) if M[i][c].sign() != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c].sign() != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def solve(G, b):   # G square, exact
    n = len(G); M = [list(G[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c].sign() != 0); M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c and M[i][c].sign() != 0:
                f = M[i][c] / M[c][c]; M[i] = [a - f * bb for a, bb in zip(M[i], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]

H = Fr(1, 2); PHI = QF(H, H)
def roots(g):
    q = lambda *xs: tuple(QF(x) if not isinstance(x, QF) else x for x in xs)
    if g == 'A4': return [q(*[1 if k == i else -1 if k == i + 1 else 0 for k in range(5)]) for i in range(4)]
    if g == 'B4': return [q(0, 0, 0, 1), q(0, 0, 1, -1), q(0, 1, -1, 0), q(1, -1, 0, 0)]     # node 1 short: seed 1000 = tesseract
    if g == 'F4': return [q(0, 1, -1, 0), q(0, 0, 1, -1), q(0, 0, 0, 1), q(H, -H, -H, -H)]   # seed 1000 = 24-cell
    if g == 'H4':
        R = h4_roots(); f = lambda u, v: float(dot(u, v))
        target = {(0, 1): -float(PHI) / 2, (1, 2): -0.5, (2, 3): -0.5, (0, 2): 0, (0, 3): 0, (1, 3): 0}
        a1 = R[0]
        for a2 in R:
            if abs(f(a1, a2) - target[(0, 1)]) > 1e-9: continue
            for a3 in R:
                if abs(f(a2, a3) + .5) > 1e-9 or abs(f(a1, a3)) > 1e-9: continue
                for a4 in R:
                    if abs(f(a3, a4) + .5) > 1e-9 or abs(f(a1, a4)) > 1e-9 or abs(f(a2, a4)) > 1e-9: continue
                    S = [a1, a2, a3, a4]
                    assert dot(a1, a2) == -PHI * H and dot(a2, a3) == QF(-H) and dot(a3, a4) == QF(-H)
                    return S                                     # bond 5 between nodes 1, 2: seed 1000 = 120-cell
    raise ValueError(g)
def h4_roots():
    R = set(); ip = QF(-H, H)  # 1/phi = phi - 1
    for i in range(4):
        for s in (1, -1): v = [QF(0)] * 4; v[i] = QF(s); R.add(tuple(v))
    for ss in itertools.product((H, -H), repeat=4): R.add(tuple(QF(x) for x in ss))
    base = [PHI * H, QF(H), ip * H, QF(0)]
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2: continue
        for ss in itertools.product((1, -1), repeat=3):
            v = [QF(0)] * 4; vals = [base[0] * ss[0], base[1] * ss[1], base[2] * ss[2], QF(0)]
            for k in range(4): v[p[k]] = vals[k]
            R.add(tuple(v))
    R = sorted(R, key=lambda v: [float(x) for x in v]); assert len(R) == 120, len(R)
    return R

BONDS = {'A4': (3, 3, 3), 'B4': (4, 3, 3), 'F4': (3, 4, 3), 'H4': (5, 3, 3)}
def parab_order(g, nodes):
    b = BONDS[g]; nodes = sorted(nodes); total = 1; pieces = []
    for v in nodes:
        if pieces and pieces[-1][-1] == v - 1: pieces[-1].append(v)
        else: pieces.append([v])
    for p in pieces:
        bb = tuple(b[k] for k in range(p[0], p[-1]))
        if len(p) == 1: total *= 2
        elif len(p) == 2: total *= 2 * bb[0]
        elif len(p) == 3: total *= {(3, 3): 24, (4, 3): 48, (3, 4): 48, (5, 3): 120, (3, 5): 120}[bb]
        else: total *= {'A4': 120, 'B4': 384, 'F4': 1152, 'H4': 14400}[g]
    return total
def thm81(g, lab):
    U = {i for i in range(4) if not lab[i]}
    return sum(parab_order(g, U) // parab_order(g, U - {i - 1, i + 1}) for i in range(4) if lab[i])

def build(g, lab):
    """the Wythoff polytope: base corner x, all corners with a word, local structure at x"""
    A = roots(g); nA = [dot(a, a) for a in A]
    G = [[dot(A[i], A[j]) for j in range(4)] for i in range(4)]
    # fundamental weights in span(A): omega_j = sum_k c_jk A_k with A_i . omega_j = delta_ij
    om = []
    for j in range(4):
        c = solve(G, [QF(1 if i == j else 0) for i in range(4)])
        w = tuple(sum((c[k] * A[k][t] for k in range(4)), QF(0)) for t in range(len(A[0]))); om.append(w)
    x = tuple(sum((QF(lab[j]) * om[j][t] for j in range(4)), QF(0)) for t in range(len(A[0])))
    for i in range(4): assert dot(A[i], x) == QF(lab[i])
    # corners: BFS, keep the word (list of simple reflections, applied right to left: v = s_i1 s_i2 ... x  -> store parent + i)
    idx = {x: 0}; verts = [x]; parent = [(-1, -1)]; q = [0]
    while q:
        nq = []
        for vi in q:
            for i in range(4):
                y = refl(A[i], nA[i], verts[vi])
                if y not in idx: idx[y] = len(verts); verts.append(y); parent.append((vi, i)); nq.append(idx[y])
        q = nq
    V = len(verts)
    # stabiliser W_U of x, edges at x = W_U-orbits of roots alpha_i (i ringed); directions y - x
    U = [i for i in range(4) if not lab[i]]
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
        if not lab[i]: continue
        for beta in orbit(A[i], U):
            y = refl(beta, dot(beta, beta), x); assert y in idx, 'neighbour not a corner'
            d = sub(y, x)
            if d not in edges: edges.append(d)
    e = len(edges)
    assert e == thm81(g, lab), ('Theorem 8.1 count', e, thm81(g, lab))
    # cells through x: W_U-orbit of omega_j; genuine iff the edges in the supporting hyperplane have rank 3
    cells = []   # (type j, frozenset of edge indices, normal)
    for j in range(4):
        for n in orbit(om[j], U):
            E = frozenset(k for k, d in enumerate(edges) if dot(n, d).sign() == 0)
            assert all(dot(n, d).sign() <= 0 for d in edges)
            if len(E) >= 3 and rank([edges[k] for k in E]) == 3: cells.append((j + 1, E, n))
    cellsets = [c[1] for c in cells]; assert len(set(cellsets)) == len(cellsets)
    faces = []   # (pair of edge indices, kind = sorted pair of cell types, the two cells)
    for a, b in itertools.combinations(range(e), 2):
        cont = [ci for ci, c in enumerate(cells) if a in c[1] and b in c[1]]
        if len(cont) < 2: continue
        inter = frozenset.intersection(*[cells[ci][1] for ci in cont])
        if inter == {a, b}:
            assert len(cont) == 2, 'a 2-face lies in exactly two cells'
            faces.append(((a, b), tuple(sorted((cells[cont[0]][0], cells[cont[1]][0]))), tuple(cont)))
    assert e - len(faces) + len(cells) == 2, 'Euler for the corner figure'
    # every cell's edges at x form a cycle in the corner figure: number of faces of the cell at x = its edge count at x
    for ci, c in enumerate(cells): assert sum(1 for f in faces if ci in f[2]) == len(c[1])
    # sizes: corners of each 2-face and cell (exact scan) for the f-vector
    def verts_on(normals):
        return sum(1 for v in verts if all(dot(n, sub(v, x)).sign() == 0 for n in normals))
    cell_size = [verts_on([c[2]]) for c in cells]
    face_size = [verts_on([cells[f[2][0]][2], cells[f[2][1]][2]]) for f in faces]
    # edge -> number of cells containing it
    n_e = [sum(1 for c in cells if k in c[1]) for k in range(e)]
    # images of the edge directions at every corner (incremental along the BFS tree): edge k at corner v is w(d_k)
    img = [None] * V; img[0] = edges
    for vi in range(1, V):
        p, i = parent[vi]; img[vi] = [refl(A[i], nA[i], d) for d in img[p]]
    # permutation action of W_U on the edges at x (fine classes)
    perms = []
    for k in U:
        perm = []
        for d in edges:
            y = refl(A[k], nA[k], d); perm.append(edges.index(y))
        perms.append(tuple(perm))
    grp = {tuple(range(e))}; st = [tuple(range(e))]
    while st:
        p = st.pop()
        for s in perms:
            q2 = tuple(s[p[t]] for t in range(e))
            if q2 not in grp: grp.add(q2); st.append(q2)
    return dict(A=A, x=x, V=V, edges=edges, cells=cells, faces=faces, cell_size=cell_size, face_size=face_size, n_e=n_e, img=img,
                grp=sorted(grp), roots_all=None)

def event(P, D):
    """corner event for a down-set D (set of edge indices at the corner)"""
    e = len(P['edges']); Up = frozenset(range(e)) - D
    lost = tuple(sorted(f[1] for f in P['faces'] if f[0][0] in D and f[0][1] in D))
    made = tuple(sorted(f[1] for f in P['faces'] if f[0][0] in Up and f[0][1] in Up))
    die = tuple(sorted(c[0] for c in P['cells'] if c[1] <= D)); born = tuple(sorted(c[0] for c in P['cells'] if c[1] <= Up))
    return (len(D), lost, made, die, born)
def rev(ev): return (None, ev[2], ev[1], ev[4], ev[3])
def fine(P, D):
    return min(tuple(sorted(p[k] for k in D)) for p in P['grp'])
def toric_local(P, D):
    """phi_v(x) = sum over faces G with lowest corner v of g((P/G)^*)(x-1)^dim G, as coefficient list of degree 4"""
    e = len(P['edges']); Up = frozenset(range(e)) - D
    poly = [0] * 5
    def add(p):
        for i, c in enumerate(p): poly[i] += c
    def mul(p, q):
        r = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q): r[i + j] += a * b
        return r
    xm1 = [-1, 1]
    add([1, len(P['cells']) - 4])                                     # G = v: g(dual corner figure) = 1 + (f2 - 4)x
    for k in Up: add(mul([1, P['n_e'][k] - 3], xm1))                  # G = edge up from v: polygon with n_e sides
    m = sum(1 for f in P['faces'] if f[0][0] in Up and f[0][1] in Up); add([c * m for c in mul(xm1, xm1)])
    b = sum(1 for c in P['cells'] if c[1] <= Up); add([c * b for c in mul(mul(xm1, xm1), xm1)])
    if len(Up) == e: add(mul(mul(xm1, xm1), mul(xm1, xm1)))
    return poly
def toric_global(P):
    V = P['V']; e = len(P['edges'])
    f1 = Fr(V * e, 2); f2 = sum(Fr(V, s) for s in P['face_size']); f3 = sum(Fr(V, s) for s in P['cell_size'])
    assert V - f1 + f2 - f3 == 0, 'Euler'
    S = sum(Fr(V * (P['n_e'][k] - 3), 2) for k in range(e))           # sum over edges of (n_e - 3)
    # V[1+(c-4)x] + sum_edges [1+(n_e-3)x](x-1) + f2 (x-1)^2 + f3 (x-1)^3 + (x-1)^4
    c = len(P['cells']); h = [Fr(0)] * 5
    h[0] += V; h[1] += V * (c - 4)
    h[0] += -f1; h[1] += f1 - S; h[2] += S
    h[0] += f2; h[1] += -2 * f2; h[2] += f2
    h[0] += -f3; h[1] += 3 * f3; h[2] += -3 * f3; h[3] += f3
    for i, cc in enumerate([1, -4, 6, -4, 1]): h[i] += cc
    return [int(t) for t in h], (V, int(f1), int(f2), int(f3))

def rand_dir(g, rng, k):
    n = 5 if g == 'A4' else 4
    if g == 'H4': return tuple(QF(rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6)) for _ in range(n))
    return tuple(QF(rng.randint(-10 ** 6, 10 ** 6)) for _ in range(n))

def ledger(P, u):
    hist = Counter(); fh = Counter(); tor = [0] * 5; deg = Counter(); pure = Counter()
    for vi in range(P['V']):
        s = [dot(u, d).sign() for d in P['img'][vi]]
        if 0 in s: return None
        D = frozenset(k for k, t in enumerate(s) if t < 0)
        ev = event(P, D); hist[ev] += 1; fh[fine(P, D)] += 1; deg[len(D)] += 1
        for i, c in enumerate(toric_local(P, D)): tor[i] += c
    return hist, fh, tor, deg

def run_wythoff(args):
    g, lab, ndir, seed = args
    t0 = time.time(); P = build(g, lab); rng = random.Random(seed)
    th, fv = toric_global(P)
    res = dict(group=g, seed=''.join(map(str, lab)), corners=P['V'], edges_per_corner=len(P['edges']),
               simple=len(P['edges']) == 4, cells_at_corner=Counter(c[0] for c in P['cells']), fvector=fv, toric_h_dual=th, checks=[])
    ok = True; first = None; firstfine = None
    for k in range(ndir):
        while True:
            u = rand_dir(g, rng, k); L = ledger(P, u)
            if L is not None: break
        hist, fh, tor, deg = L
        c1 = tor == th
        c2 = all(hist[ev] == sum(n for e2, n in hist.items() if (None,) + e2[1:] == rev(ev)) for ev in hist)
        # fine reverse: complement of the down-set
        e = len(P['edges'])
        def fcomp(D): return fine(P, frozenset(range(e)) - frozenset(D))
        c3 = all(fh[D] == fh[fcomp(D)] for D in fh)
        c4 = first is None or (hist == first and fh == firstfine)
        if first is None: first, firstfine = hist, fh
        ok &= c1 and c2 and c3 and c4
        res['checks'].append(dict(direction=[str(t) for t in u], toric_local_sum_eq_global=c1, reversal_kinds=c2, reversal_fine=c3,
                                  same_as_first_direction=c4, corners_by_down_edges=dict(sorted(deg.items())), toric_sum=tor))
    res['ledger'] = [dict(down=ev[0], lost=ev[1], made=ev[2], die=ev[3], born=ev[4], corners=n) for ev, n in sorted(first.items())]
    res['fine_classes'] = len(firstfine)
    # swap ledger in #108 form for simple rows: kind lost -> kind made at corners with 2 down edges
    if res['simple']:
        res['swaps_108'] = {f'{ev[1][0]}->{ev[2][0]}': n for ev, n in first.items() if ev[0] == 2}
    res['ok'] = ok; res['seconds'] = round(time.time() - t0, 1)
    res['cells_at_corner'] = dict(res['cells_at_corner'])
    return res

# ---------- G: general rosette tissues without symmetry (perturbed simplicial polytopes) ----------
def general(args):
    name, seed, ndir = args
    rng = random.Random(seed)
    if name == '16-cell':
        base = []
        for i in range(4):
            for s in (1, -1): v = [0] * 4; v[i] = s * 1000; base.append(v)
        V = [tuple(QF(c + rng.randint(-150, 150)) for c in v) for v in base]
        F0 = [tuple(2 * i + (sg[i] < 0) for i in range(4)) for sg in itertools.product((1, -1), repeat=4)]
    else:   # 600-cell, unit corners = the 120 roots of H4, scaled 1000
        R = h4_roots(); V = [tuple(QF(1000) * c + QF(rng.randint(-15, 15)) for c in v) for v in R]
        D2 = Counter(); m = None
        dist = lambda a, b: dot(sub(R[a], R[b]), sub(R[a], R[b]))
        el = min(float(dist(0, j)) for j in range(1, 120))
        adj = [[j for j in range(120) if j != i and abs(float(dist(i, j)) - el) < 1e-9] for i in range(120)]
        F0 = set()
        for a in range(120):
            for b, c, d in itertools.combinations(adj[a], 3):
                if c in adj[b] and d in adj[b] and d in adj[c]: F0.add(tuple(sorted((a, b, c, d))))
        F0 = sorted(F0); assert len(F0) == 600
    n = len(V)
    # verify every 4-set is still a facet exactly: hyperplane normal by cofactors, all other corners strictly on one side
    def normal(pts):
        M = [sub(p, pts[0]) for p in pts[1:]]
        cof = []
        for k in range(4):
            cols = [c for c in range(4) if c != k]
            m = [[M[r][c] for c in cols] for r in range(3)]
            det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                   + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
            cof.append(det if k % 2 == 0 else -det)
        return tuple(cof)
    for F in F0:
        nn = normal([V[i] for i in F]); s = set(dot(nn, sub(V[j], V[F[0]])).sign() for j in range(n) if j not in F)
        assert len(s) == 1 and 0 not in s, 'perturbation changed the combinatorics'
    # ridges in exactly two facets (closed pseudomanifold) => these facets are the whole boundary
    rc = Counter(tuple(sorted(t)) for F in F0 for t in itertools.combinations(F, 3)); assert set(rc.values()) == {2}
    nbr = defaultdict(set); tri = defaultdict(set); tets = defaultdict(list)
    for F in F0:
        for a in F:
            nbr[a] |= set(F) - {a}; tets[a].append(frozenset(set(F) - {a}))
            for b, c in itertools.combinations(sorted(set(F) - {a}), 2): tri[a].add((b, c))
    e = len(nbr[0]); assert all(len(nbr[a]) == e for a in range(n))
    out = dict(polytope=f'perturbed {name}', perturbation_seed=seed, corners=n, edges_per_corner=e, directions=[])
    allok = True; witness = None
    for k in range(ndir):
        while True:
            u = tuple(QF(rng.randint(-10 ** 6, 10 ** 6)) for _ in range(4))
            h = [dot(u, v) for v in V]
            if all((h[a] - h[b]).sign() != 0 for a in range(n) for b in nbr[a]): break
        hist = Counter(); tor = [0] * 5
        ce = len(tets[0]); ne = 4 if name == '16-cell' else 5      # tetrahedra at a corner, tetrahedra round an edge
        for a in range(n):
            D = frozenset(b for b in nbr[a] if (h[b] - h[a]).sign() < 0); Up = frozenset(nbr[a]) - D
            lost = sum(1 for (b, c) in tri[a] if b in D and c in D); made = sum(1 for (b, c) in tri[a] if b in Up and c in Up)
            die = sum(1 for T in tets[a] if T <= D); born = sum(1 for T in tets[a] if T <= Up)
            hist[(len(D), lost, made, die, born)] += 1
            k = len(Up); poly = [1, ce - 4, 0, 0, 0]
            for i, c in enumerate([-k, k - k * (ne - 3), k * (ne - 3)]): poly[i] += c          # k [1+(ne-3)x](x-1)
            for i, c in enumerate([made, -2 * made, made]): poly[i] += c
            for i, c in enumerate([-born, 3 * born, -3 * born, born]): poly[i] += c
            if k == e: 
                for i, c in enumerate([1, -4, 6, -4, 1]): poly[i] += c
            tor = [t + c for t, c in zip(tor, poly)]
        assert tor == ([1, 12, 14, 12, 1] if name == '16-cell' else [1, 596, 846, 596, 1]), ('toric', tor)
        bal = all(hist[ev] == hist[(e - ev[0], ev[2], ev[1], ev[4], ev[3])] for ev in hist)
        if not bal and witness is None:
            witness = dict(corners=[[str(c) for c in v] for v in V], direction=[str(c) for c in u],
                           ledger={str(ev): c for ev, c in sorted(hist.items())})
        allok &= bal
        out['directions'].append(dict(balanced=bal, toric_sum=tor, ledger={str(ev): c for ev, c in sorted(hist.items())}))
    out['all_balanced'] = allok; out['witness'] = witness
    return out

def small_witness():
    """smallest exact counterexample: 16-cell corners +-10 e_i moved by integers in [-2, 2], direction in [-3, 3]^4"""
    best = None; rng = random.Random(1)
    nbrs = lambda i: [j for j in range(8) if j // 2 != i // 2]
    for trial in range(60):
        V = []
        for i in range(4):
            for sg in (1, -1):
                v = [rng.randint(-2, 2) for _ in range(4)]; v[i] += 10 * sg; V.append(tuple(v))
        Vq = [tuple(QF(c) for c in v) for v in V]
        okc = True
        for sg in itertools.product((0, 1), repeat=4):
            F = [2 * i + sg[i] for i in range(4)]; pts = [Vq[i] for i in F]
            M = [sub(p, pts[0]) for p in pts[1:]]
            nn = []
            for k in range(4):
                cols = [c for c in range(4) if c != k]; m = [[M[r][c] for c in cols] for r in range(3)]
                det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                       + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
                nn.append(det if k % 2 == 0 else -det)
            sgs = set(dot(tuple(nn), sub(Vq[j], pts[0])).sign() for j in range(8) if j not in F)
            if len(sgs) != 1 or 0 in sgs: okc = False; break
        if not okc: continue
        for u in itertools.product(range(-3, 4), repeat=4):
            h = [sum(a * b for a, b in zip(u, v)) for v in V]
            if any(h[a] == h[b] for a in range(8) for b in nbrs(a)): continue
            hist = Counter()
            for a in range(8):
                D = {b for b in nbrs(a) if h[b] < h[a]}; Up = set(nbrs(a)) - D
                tri = [(b, c) for b, c in itertools.combinations(nbrs(a), 2) if b // 2 != c // 2]
                tets = [T for T in itertools.combinations(nbrs(a), 3) if len({t // 2 for t in T}) == 3]
                hist[(len(D), sum(b in D and c in D for b, c in tri), sum(b in Up and c in Up for b, c in tri),
                      sum(set(T) <= D for T in tets), sum(set(T) <= Up for T in tets))] += 1
            if all(hist[ev] == hist[(6 - ev[0], ev[2], ev[1], ev[4], ev[3])] for ev in hist): continue
            size = sum(abs(c) for v in V for c in v) - 80 + sum(map(abs, u))
            if best is None or size < best[0]: best = (size, V, u, dict(hist))
    return best

def worker(t): return (t[0], run_wythoff(t[1]) if t[0] == 'W' else general(t[1]))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'pilot'; jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    seeds = [lab for lab in itertools.product((0, 1), repeat=4) if any(lab)]
    if mode == 'pilot':
        W = [(g, lab, 3, 7) for g in ('A4', 'B4') for lab in seeds] + [('F4', (1, 0, 0, 0), 3, 7), ('H4', (1, 0, 0, 0), 2, 7), ('H4', (0, 0, 0, 1), 2, 7)]
        Gs = [('16-cell', s, 20) for s in range(5)]
    else:
        W = [(g, lab, 3 if g != 'H4' else 2, 11) for g in ('A4', 'B4', 'F4', 'H4') for lab in seeds]
        W.sort(key=lambda t: -{'H4': 4, 'F4': 3, 'B4': 2, 'A4': 1}[t[0]] * sum(t[1]))
        Gs = [('16-cell', s, 200) for s in range(40)] + [('600-cell', s, 10) for s in range(6)]
    tasks = [('W', t) for t in W] + [('G', t) for t in Gs]
    out = {'mode': mode, 'wythoff': [], 'general': []}; ok = True; done = 0; t0 = time.time()
    with Pool(jobs) as pool:
        for kind, r in pool.imap_unordered(worker, tasks):
            done += 1
            if kind == 'W':
                out['wythoff'].append(r); ok &= r['ok']
                print(f"{r['group']} {r['seed']}: corners {r['corners']}, edges {r['edges_per_corner']}, simple {r['simple']}, "
                      f"toric h(P*) {r['toric_h_dual']}, classes {len(r['ledger'])}/{r['fine_classes']} fine, checks "
                      f"{'ok' if r['ok'] else 'FAIL'} ({r['seconds']} s)" + (f", swaps {r['swaps_108']}" if r['simple'] else ''))
            else:
                out['general'].append(r)
                print(f"{r['polytope']} seed {r['perturbation_seed']}: balanced in {sum(d['balanced'] for d in r['directions'])}"
                      f"/{len(r['directions'])} directions")
            print(f'PROGRESS {done / len(tasks):.3f} {kind} task {done}/{len(tasks)} ({time.time() - t0:.0f} s)')
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'rosette-{mode}.json'), 'w'),
              indent=1, default=str)
    # POSITIVE controls: the classical h-vectors and the swap ledger of Chapter 7 / #108 (Theorem 1 table)
    CTRL = {('A4', '1111'): ([1, 26, 66, 26, 1], {'(1, 2)->(3, 4)': 6, '(1, 3)->(2, 4)': 16, '(1, 4)->(2, 3)': 11}),
            ('A4', '0001'): ([1, 1, 1, 1, 1], None), ('B4', '1000'): ([1, 4, 6, 4, 1], None),
            ('H4', '1000'): ([1, 116, 366, 116, 1], None), ('H4', '1100'): ([1, 716, 966, 716, 1], {'(1, 4)->(4, 4)': 483}),
            ('H4', '0110'): ([1, 716, 2166, 716, 1], {'(1, 1)->(4, 4)': 601, '(4, 4)->(1, 1)': 601, '(1, 4)->(1, 4)': 964}),
            ('F4', '0110'): ([1, 44, 198, 44, 1], {'(1, 1)->(4, 4)': 73, '(1, 4)->(1, 4)': 52})}
    for r in out['wythoff']:
        key = (r['group'], r['seed'])
        if key in CTRL:
            hv, sw = CTRL[key]; c = r['toric_h_dual'] == hv and (sw is None or all(r['swaps_108'].get(k) == v for k, v in sw.items()))
            print('CONTROL', key, 'h', r['toric_h_dual'], 'swaps', r.get('swaps_108'), 'ok' if c else 'FAIL'); ok &= c
    print('Wythoff rows', len(out['wythoff']), 'all checks', ok)
    if mode == 'full':
        b = small_witness()
        if b:
            out['small_witness'] = dict(corners=b[1], direction=b[2], ledger={str(k): v for k, v in sorted(b[3].items())})
            print('SMALL WITNESS corners', b[1], 'direction', b[2]); [print('   ', k, v) for k, v in sorted(b[3].items())]
        # linear invariants of the ledgers of the perturbed 16-cells: nullspace of the centred data
        L = [d['ledger'] for r in out['general'] if r['polytope'].endswith('16-cell') for d in r['directions']]
        cls = sorted({k for l in L for k in l}); rows = [[Fr(l.get(k, 0)) for k in cls] for l in L]
        mean = [sum(c) / len(rows) for c in zip(*rows)]; Mc = [[a - m for a, m in zip(r, mean)] for r in rows]
        rk = rank([tuple(QF(a) for a in r) for r in Mc]) if Mc else 0
        ev = [eval(k) for k in cls]
        cnt = [[QF(1)] * len(cls)] + [[QF(t[i]) for t in ev] for i in range(5)]      # corners, |D|, lost, made, die, born
        rc = rank([tuple(r) for r in cnt])
        print(f'perturbed 16-cells: {len(L)} ledgers over {len(cls)} classes; data rank {rk}; invariant relations {len(cls) - rk}; '
              f'counting relations (corners, edges, contacts, cells by lowest/highest corner) {rc}')
        out['invariants_16'] = dict(ledgers=len(L), classes=cls, data_rank=rk, relations=len(cls) - rk, counting_relations=rc)
        json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'rosette-{mode}.json'), 'w'),
                  indent=1, default=str)
    print('general rosette tissues: balanced in every direction tested:', all(r['all_balanced'] for r in out['general']))
    sys.exit(0 if ok else 1)
