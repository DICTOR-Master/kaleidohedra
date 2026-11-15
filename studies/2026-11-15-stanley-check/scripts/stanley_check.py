"""Stanley check (15 Nov 2026): is the sweep balance law of #104 Thm 4 / #108 Thm 1 exactly Stanley's fine h-vector symmetry of an
a-balanced simplicial sphere, after the translation  simple 4-polytope P  ->  polar simplicial sphere Delta  ->  sweep = line shelling?

EXACT arithmetic throughout (Fractions; Q(sqrt5) for H4, field class QF imported from studies/2026-11-13-rosette-balance/scripts/
rosette_balance.py, executed from its file, not retyped). For each simple case:
  T1 simple: every corner lies in exactly 4 cells (so the polar Delta is simplicial; its facets are the corners' 4-sets of cells)
  T2 every subset T of a corner's cells is a face of P of dimension 4 - |T| (exact affine rank of the common corners), distinct T give
     distinct faces: Delta's faces = P's faces, reversed
  T3 a-balanced: every corner sees the same multiset a of cell types
  T4 Stanley's fine h-vector from the fine f-vector of Delta, h_b = sum_{c<=b} (-1)^{|b|-|c|} prod_i C(a_i-c_i, b_i-c_i) f_c;
     symmetry h_b = h_{a-b} and h_b >= 0
  per generic direction u (exact):
  T5 line shelling: for every corner v and every T subset of its cells, v is the LOWEST corner of the face T  <=>  R(v) subset T,
     R(v) = the cells at v opposite its down edges (the restriction face of the shelling of Delta by height, Bruggesser-Mani)
  T6 N_u(b) = #corners with colour(R(v)) = b equals h_b for every b  (sweep counts = Stanley's numbers)
  T7 DICTO's ledger read from P directly (lowest / highest corner of every 2-face): at each i = 2 corner one contact is made, of kind
     colour(R(v)), and one lost, of kind a - colour(R(v)); swaps X -> Y = h_Y; balance X -> Y = Y -> X
  T8 #108's in(X) = N_X - sum_cells c_X(type) + p_X equals h_X for every |X| = 2
  T9 reversal: N_{-u}(b) = N_u(a - b)
Non-simple case (the moved 16-cell of studies/2026-11-13-rosette-balance, Theorem 4, and the regular 16-cell): Stanley's hypothesis
fails (corners in 8 cells, so the polar is not simplicial); the faces new at a corner are not an interval [R, sigma] of a Boolean
lattice; the per-class corner counts are not fixed by the face numbers (rank of the class contribution matrix < number of classes);
the moved one is unbalanced in the direction -3x1 + x4, the regular one balanced in every generic direction tried.
Negative control: a tilted permutohedron with random cell types (not a-balanced): Stanley's h is undefined and the ledger is unbalanced.
Usage: stanley_check.py [pilot|full]   prints PROGRESS lines and FINAL ok / FAIL."""
import sys, os, json, time, itertools, random, importlib.util
from fractions import Fraction as Fr
from collections import Counter
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.join(HERE, '..', '..', '2026-11-13-rosette-balance', 'scripts', 'rosette_balance.py')
spec = importlib.util.spec_from_file_location('rosette_balance', RB); rb = importlib.util.module_from_spec(spec); spec.loader.exec_module(rb)
QF, dot, sub, refl, roots, solve, rank = rb.QF, rb.dot, rb.sub, rb.refl, rb.roots, rb.solve, rb.rank

MODE = sys.argv[1] if len(sys.argv) > 1 else 'pilot'
FULL = MODE == 'full'
T0 = time.time(); OUT = dict(mode=MODE, cases={}); FAILS = []
def log(*a): print(*a, flush=True)
def check(name, ok, info=''):
    if not ok: FAILS.append(f'{name} {info}')
    log(('  ok   ' if ok else '  FAIL ') + name + (f'  {info}' if info else ''))
    return ok

# ---------------------------------------------------------------- Wythoff polytopes, exact
def wythoff(g, lab):
    A = roots(g); nA = [dot(a, a) for a in A]
    G = [[dot(A[i], A[j]) for j in range(4)] for i in range(4)]
    om = []
    for j in range(4):
        c = solve(G, [QF(1 if i == j else 0) for i in range(4)])
        om.append(tuple(sum((c[k] * A[k][t] for k in range(4)), QF(0)) for t in range(len(A[0]))))
    x = tuple(sum((QF(lab[j]) * om[j][t] for j in range(4)), QF(0)) for t in range(len(A[0])))
    def orbit(v0):
        seen = {v0: 0}; L = [v0]; q = [v0]
        while q:
            nq = []
            for v in q:
                for i in range(4):
                    y = refl(A[i], nA[i], v)
                    if y not in seen: seen[y] = len(L); L.append(y); nq.append(y)
            q = nq
        return L
    V = orbit(x)
    cells = []   # (type, normal, offset, frozenset of corners)
    for j in range(4):
        off = dot(om[j], x)
        for n in orbit(om[j]):
            C = frozenset(k for k, v in enumerate(V) if (dot(n, v) - off).sign() == 0)
            if len(C) >= 4 and rank([sub(V[k], V[min(C)]) for k in C]) == 3: cells.append((j + 1, n, off, C))
    return V, cells

def project_A4(V, cells):
    """A4 lives in x1+..+x5 = 15; drop x5 (an affine isomorphism onto R^4)"""
    V4 = [v[:4] for v in V]
    c4 = [(t, tuple(n[i] - n[4] for i in range(4)), off - QF(15) * n[4], C) for (t, n, off, C) in cells]
    return V4, c4

def tilt(V, cells, rng, eps):
    """new facet normals n + random rational eps-vector; corners re-solved; same face lattice checked exactly"""
    nc = [(t, tuple(a + QF(Fr(rng.randint(-1000, 1000), 1000)) * eps for a in n), off, C) for (t, n, off, C) in cells]
    sig = [[ci for ci, c in enumerate(cells) if k in c[3]] for k in range(len(V))]
    NV = []
    for k in range(len(V)):
        F = sig[k]; assert len(F) == 4
        p = tuple(solve([list(nc[ci][1]) for ci in F], [nc[ci][2] for ci in F]))
        for ci, c in enumerate(nc):
            s = (dot(c[1], p) - c[2]).sign()
            if ci in F: assert s == 0
            elif s >= 0: return None                     # combinatorics changed: caller retries
        NV.append(p)
    return NV, nc

# ---------------------------------------------------------------- the translation test for a simple polytope

def fine_h(a, f):
    h = {}
    for b in f:
        s = 0
        for cvec in f:
            if all(ci <= bi for ci, bi in zip(cvec, b)):
                w = 1
                for ai, bi, ci in zip(a, b, cvec): w *= comb(ai - ci, bi - ci)
                s += (-1) ** (sum(b) - sum(cvec)) * w * f[cvec]
        h[b] = s
    return h

def all_b(a): return [tuple(t) for t in itertools.product(*[range(ai + 1) for ai in a])]

def rand_dir(rng, field_sqrt5):
    if field_sqrt5: return tuple(QF(rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6)) for _ in range(4))
    return tuple(QF(rng.randint(-10 ** 6, 10 ** 6)) for _ in range(4))

def simple_case(name, V, cells, ndir, rng, sqrt5=False, expect=None, expect_h=None):
    log(f'== {name}: {len(V)} corners, {len(cells)} cells'); t0 = time.time(); res = dict(corners=len(V), cells=len(cells))
    types = [c[0] for c in cells]; tl = sorted(set(types))
    sig = [frozenset(ci for ci, c in enumerate(cells) if k in c[3]) for k in range(len(V))]
    ok1 = check(f'{name} T1 simple (4 cells at every corner)', all(len(s) == 4 for s in sig))
    if not ok1: return res
    col = lambda T: tuple(Counter(types[i] for i in T).get(t, 0) for t in tl)
    a = col(sig[0]); res['a'] = dict(zip(map(str, tl), a))
    check(f'{name} T3 a-balanced, a = {dict(zip(tl, a))}', all(col(s) == a for s in sig))
    # faces of Delta = all subsets of the corners' cell sets; their corner sets on P
    faces = {}
    for k, s in enumerate(sig):
        for r in range(5):
            for T in itertools.combinations(sorted(s), r): faces.setdefault(frozenset(T), None)
    allc = frozenset(range(len(V)))
    for T in faces:
        C = allc
        for ci in T: C = C & cells[ci][3]
        faces[T] = tuple(sorted(C))
    bad = 0
    for T, C in faces.items():
        if len(T) == 0: continue
        r = rank([sub(V[k], V[C[0]]) for k in C]) if len(C) > 1 else 0
        if r != 4 - len(T): bad += 1
    distinct = len(set(faces.values())) == len(faces)
    check(f'{name} T2 every subset of a corner\'s cells is a face of dimension 4 - |T|; {len(faces)} faces, distinct', bad == 0 and distinct, f'bad {bad}')
    fvec = Counter(len(T) for T in faces); res['f_of_Delta'] = [fvec[i] for i in range(5)]
    f = Counter(col(T) for T in faces)
    for b in all_b(a): f.setdefault(b, 0)
    h = fine_h(a, f)
    res['fine_f'] = {str(b): f[b] for b in sorted(f)}; res['stanley_fine_h'] = {str(b): h[b] for b in sorted(h)}
    sym = all(h[b] == h[tuple(ai - bi for ai, bi in zip(a, b))] for b in h)
    check(f'{name} T4 Stanley fine h symmetric h_b = h_(a-b) and >= 0', sym and all(v >= 0 for v in h.values()),
          ' '.join(f'{b}:{h[b]}' for b in sorted(h) if sum(b) == 2))
    if expect_h: check(f'{name} T4 fine h against the paper\'s numbers', all(h[b] == v for b, v in expect_h.items()), str(expect_h))
    # edges: each 3-subset of a corner's cells is an edge with exactly 2 corners
    nbr = []
    for k, s in enumerate(sig):
        L = []
        for T in itertools.combinations(sorted(s), 3):
            C = faces[frozenset(T)]; assert len(C) == 2 and k in C
            w = C[0] if C[1] == k else C[1]; L.append((w, (s - sig[w])))
        nbr.append(L)
    # 2-faces with kinds, cells by type, for T7 / T8
    two = [T for T in faces if len(T) == 2]
    NX = Counter(col(T) for T in two)
    per_dir = []
    for di in range(ndir):
        u = rand_dir(rng, sqrt5); hts = [dot(u, v) for v in V]
        order = sorted(range(len(V)), key=lambda k: float(hts[k]))
        gen = all((hts[order[i + 1]] - hts[order[i]]).sign() > 0 for i in range(len(order) - 1))
        if not gen: log('  (direction not generic, redrawn)'); continue
        R = []
        for k in range(len(V)):
            Rk = set()
            for w, opp in nbr[k]:
                if (hts[w] - hts[k]).sign() < 0: assert len(opp) == 1; Rk |= opp
            R.append(frozenset(Rk))
        # T5 the line shelling: lowest corner of every face
        # the order is exact: consecutive corners were checked strictly increasing with exact signs above
        rk = {k: i for i, k in enumerate(order)}
        low = {T: min(C, key=lambda k: rk[k]) for T, C in faces.items()}
        bad5 = sum(1 for k, s in enumerate(sig) for r in range(5) for T in itertools.combinations(sorted(s), r)
                   if (low[frozenset(T)] == k) != (R[k] <= frozenset(T)))
        N = Counter(col(Rk) for Rk in R)
        for b in all_b(a): N.setdefault(b, 0)
        # T7 DICTO's ledger read from the 2-faces
        high = {T: max(faces[T], key=lambda k: rk[k]) for T in two}
        made = Counter(); lost = Counter()
        for T in two: made[low[T]] += 1; lost[high[T]] += 1
        swaps = Counter(); bad7 = 0
        for k in range(len(V)):
            if len(R[k]) != 2:
                if len(R[k]) in (1, 3) and (made[k], lost[k]) != ((3, 0) if len(R[k]) == 1 else (0, 3)): bad7 += 1
                continue
            Tm = [T for T in (frozenset(p) for p in itertools.combinations(sorted(sig[k]), 2)) if low[T] == k]
            Tl = [T for T in (frozenset(p) for p in itertools.combinations(sorted(sig[k]), 2)) if high[T] == k]
            if len(Tm) != 1 or len(Tl) != 1 or Tm[0] != R[k] or Tl[0] != sig[k] - R[k]: bad7 += 1; continue
            swaps[(col(Tl[0]), col(Tm[0]))] += 1
        bal = all(swaps[(X, Y)] == swaps[(Y, X)] for (X, Y) in swaps)
        hY = all(c == h[Y] for (X, Y), c in swaps.items())
        # T9 reversal
        Rm = [frozenset(sig[k] - R[k]) for k in range(len(V))]
        Nm = Counter(col(x) for x in Rm)
        rev = all(Nm.get(tuple(ai - bi for ai, bi in zip(a, b)), 0) == N[b] for b in N)
        d = dict(T5_shelling_failures=bad5, N_u={str(b): N[b] for b in sorted(N)}, swaps={f'{X}->{Y}': c for (X, Y), c in sorted(swaps.items())},
                 T7_failures=bad7, balanced=bal, swaps_equal_h=hY, reversal=rev)
        per_dir.append(d)
        check(f'{name} dir {di}: T5 sweep = line shelling of the polar (restriction face R(v))', bad5 == 0, f'failures {bad5}')
        check(f'{name} dir {di}: T6 N_u(b) = Stanley h_b for all b', all(N[b] == h[b] for b in h))
        check(f'{name} dir {di}: T7 ledger from 2-faces: X -> Y = h_Y, balanced', bad7 == 0 and bal and hY,
              ' '.join(f'{X}->{Y}:{c}' for (X, Y), c in sorted(swaps.items())))
        check(f'{name} dir {di}: T9 N_(-u)(b) = N_u(a-b)', rev)
    res['directions'] = per_dir
    # T8 #108's in(X) formula
    bad8 = []
    for X in [b for b in all_b(a) if sum(b) == 2]:
        pX = 1
        for ai, xi in zip(a, X): pX *= comb(ai, xi)
        sc = 0
        for ci, c in enumerate(cells):
            t = tl.index(c[0]); e = [0] * len(a); e[t] = 1
            w = 1
            for ai, xi, ei in zip(a, X, e): w = w * comb(ai - ei, xi - ei) if xi >= ei else 0
            sc += w
        inX = NX[X] - sc + pX
        if inX != h[X]: bad8.append((X, inX, h[X]))
        res.setdefault('in_X', {})[str(X)] = inX
    check(f'{name} T8 #108 in(X) = N_X - sum c_X + p_X equals h_X', not bad8, str(res.get('in_X')))
    res['seconds'] = round(time.time() - t0, 1)
    return res

# ---------------------------------------------------------------- non-simple: the 16-cells
def sixteen(name, V, ndir, rng, special_dir=None):
    log(f'== {name}'); res = {}
    n = 8; pairs = [(0, 1), (2, 3), (4, 5), (6, 7)]
    F0 = [tuple(p[s] for p, s in zip(pairs, ss)) for ss in itertools.product((0, 1), repeat=4)]
    def normal(pts):
        M = [sub(p, pts[0]) for p in pts[1:]]; cof = []
        for k in range(4):
            cols = [c for c in range(4) if c != k]; m = [[M[r][c] for c in cols] for r in range(3)]
            det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                   + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
            cof.append(det if k % 2 == 0 else -det)
        return tuple(cof)
    okf = True
    for F in F0:
        nn = normal([V[i] for i in F]); s = set(dot(nn, sub(V[j], V[F[0]])).sign() for j in range(n) if j not in F)
        okf &= (len(s) == 1 and 0 not in s)
    rc = Counter(tuple(sorted(t)) for F in F0 for t in itertools.combinations(F, 3))
    check(f'{name}: the 16 sign-choice tetrahedra are exactly the facets', okf and set(rc.values()) == {2})
    cellsat = [sum(1 for F in F0 if k in F) for k in range(n)]
    check(f'{name}: NOT simple (cells per corner {set(cellsat)}): the polar is not simplicial, Stanley\'s hypothesis fails', set(cellsat) == {8})
    # faces of P containing corner k, as sets of cells: count vs 2^8
    cells = [frozenset(F) for F in F0]
    nb = lambda k: [j for j in range(n) if j // 2 != k // 2]
    facesP = set()
    for F in F0:
        for r in range(1, 5):
            for S in itertools.combinations(F, r): facesP.add(frozenset(S))
    faces_at0 = [S for S in facesP if 0 in S]
    res['faces_through_a_corner'] = len(faces_at0)
    check(f'{name}: faces through a corner {len(faces_at0)} (a simplicial polar would give 2^8 = 256 cell subsets)', len(faces_at0) != 256)
    def ledger(u):
        hts = [dot(u, v) for v in V]
        if any((hts[a] - hts[b]).sign() == 0 for a in range(n) for b in nb(a)): return None
        H = Counter(); minimal = Counter(); contrib = {}
        for k in range(n):
            D = frozenset(b for b in nb(k) if (hts[b] - hts[k]).sign() < 0); U = frozenset(nb(k)) - D
            newf = [S - {k} for S in faces_at_corner[k] if all((hts[j] - hts[k]).sign() > 0 for j in S - {k})]
            # faces new at k (k their lowest corner), as sets of cells containing them; minimal elements under reverse inclusion
            asc = [frozenset(ci for ci, c in enumerate(cells) if (S | {k}) <= c) for S in newf]
            mins = [c for c in asc if not any(o < c for o in asc)]   # minimal cell sets = maximal new faces
            minimal[len(mins)] += 1
            tri = sum(1 for S in newf if len(S) == 2); tet = sum(1 for S in newf if len(S) == 3); edg = sum(1 for S in newf if len(S) == 1)
            lost = sum(1 for b, c in itertools.combinations(sorted(D), 2) if c // 2 != b // 2)
            dshape = 'T' if len(D) == 3 and lost == 3 else ('Q' if len(D) == 3 else '')
            ev = (len(D), dshape, lost, tri, sum(1 for F in F0 if k in F and set(F) - {k} <= D), tet)
            H[ev] += 1
            contrib[ev] = (1, edg, tri, tet, 1 if len(U) == 6 else 0)
        return H, minimal, contrib
    faces_at_corner = [[S for S in facesP if k in S] for k in range(n)]
    def balanced(H):
        return all(H[ev] == H.get((6 - ev[0], ev[1], ev[3], ev[2], ev[5], ev[4]), 0) for ev in H)
    out = []; allbal = True; contribs = {}
    dirs = ([special_dir] if special_dir else []) + [None] * ndir
    for u in dirs:
        while u is None:
            u = tuple(QF(rng.randint(-10 ** 6, 10 ** 6)) for _ in range(4))
            if ledger(u) is None: u = None
        L = ledger(u)
        H, minimal, contrib = L; contribs.update(contrib); b = balanced(H); allbal &= b
        out.append(dict(direction=[str(c) for c in u], balanced=b, minimal_new_faces=dict(minimal), ledger={str(e): c for e, c in sorted(H.items())}))
    res['sweeps'] = out[:6]; res['n_sweeps'] = len(out); res['n_unbalanced'] = sum(1 for o in out if not o['balanced'])
    M = [list(map(Fr, v)) for v in contribs.values()]
    rk = rank([tuple(QF(x) for x in row) for row in M]) if M else 0
    res['classes_seen'] = len(contribs); res['contribution_rank'] = rk
    res['interval_failures'] = sum(o['minimal_new_faces'].get(2, 0) + sum(c for m, c in o['minimal_new_faces'].items() if m > 2) for o in out)
    return res, out

# ---------------------------------------------------------------- main
cases = [('4D permutohedron (A4 1111)', 'A4', (1, 1, 1, 1), {}), ('bitruncated 24-cell (F4 0110)', 'F4', (0, 1, 1, 0), {})]
if FULL: cases.append(('bitruncated 600-cell (H4 0110)', 'H4', (0, 1, 1, 0), {(2, 0): 601, (1, 1): 964, (0, 2): 601}))
ND = 6 if FULL else 2; NT = 2 if FULL else 1
total = len(cases) * (1 + NT) + 3; done = 0
rng = random.Random(20261115)
for name, g, lab, exp in cases:
    V, cells = wythoff(g, lab)
    if g == 'A4': V, cells = project_A4(V, cells)
    OUT['cases'][name] = simple_case(name, V, cells, ND if g != 'H4' else 3, rng, sqrt5=(g == 'H4'), expect_h=exp or None)
    done += 1; log(f'PROGRESS {done / total:.3f} {name}')
    if g == 'H4': continue
    for t in range(NT):
        for attempt in range(20):
            r = tilt(V, cells, rng, QF(Fr(1, 200)))
            if r: break
        check(f'{name} tilted copy {t}: face lattice kept (exact)', r is not None)
        if r:
            NV, nc = r
            OUT['cases'][f'{name}, tilted {t}'] = simple_case(f'{name}, tilted {t}', NV, nc, ND, rng)
            hs = OUT['cases'][f'{name}, tilted {t}'].get('stanley_fine_h'); h0 = OUT['cases'][name].get('stanley_fine_h')
            check(f'{name} tilted {t}: same Stanley h as the regular copy (no symmetry needed)', hs == h0)
        done += 1; log(f'PROGRESS {done / total:.3f} {name} tilted {t}')

# negative control: tilted permutohedron with random types (not a-balanced)
V, cells = project_A4(*wythoff('A4', (1, 1, 1, 1)))
r = tilt(V, cells, rng, QF(Fr(1, 200)))
NV, nc = r
lab_rng = random.Random(7)
nc2 = [(lab_rng.choice((1, 2)), n, o, C) for (t, n, o, C) in nc]
types = [c[0] for c in nc2]
sig = [[ci for ci, c in enumerate(nc2) if k in c[3]] for k in range(len(NV))]
ms = Counter(tuple(sorted(types[ci] for ci in s)) for s in sig)
check('NEG random types on a tilted permutohedron: not a-balanced (Stanley h undefined)', len(ms) > 1, str(dict(ms)))
unb = 0
for di in range(ND):
    u = rand_dir(rng, False); hts = [dot(u, v) for v in NV]
    swaps = Counter()
    for k, s in enumerate(sig):
        D = []
        for T in itertools.combinations(s, 3):
            C = [j for j in range(len(NV)) if all(j in nc2[ci][3] for ci in T)]
            w = C[0] if C[1] == k else C[1]
            if (hts[w] - hts[k]).sign() < 0: D.append((set(s) - set(T)).pop())
        if len(D) == 2:
            Y = tuple(sorted(types[ci] for ci in D)); X = tuple(sorted(types[ci] for ci in s if ci not in D)); swaps[(X, Y)] += 1
    if not all(swaps[(X, Y)] == swaps.get((Y, X), 0) for (X, Y) in swaps): unb += 1
check(f'NEG random types: ledger unbalanced in {unb} of {ND} directions (expected > 0)', unb > 0)
OUT['negative_control'] = dict(corner_type_multisets={str(k): v for k, v in ms.items()}, unbalanced_directions=unb, directions=ND)
done += 1; log(f'PROGRESS {done / total:.3f} negative control')

# non-simple: the moved 16-cell (rosette-balance Theorem 4) and the regular one
MOVED = [(10, 2, -1, 0), (-10, 1, 0, 1), (1, 8, -2, 0), (1, -10, 1, -1), (0, -2, 10, 2), (-1, 2, -9, -2), (-1, -2, 1, 9), (-2, -1, 1, -8)]
Vm = [tuple(QF(c) for c in v) for v in MOVED]
res, out = sixteen('moved 16-cell', Vm, 200 if FULL else 20, rng, special_dir=(QF(-3), QF(0), QF(0), QF(1)))
first = out[0]
hts = [-30, 31, -3, -4, 2, 1, 12, -2]
check('moved 16-cell: corner heights under -3x1 + x4 are -30, 31, -3, -4, 2, 1, 12, -2', [int(dot((QF(-3), QF(0), QF(0), QF(1)), v).a) for v in Vm] == hts)
check('moved 16-cell: unbalanced in the direction -3x1 + x4 (rosette-balance Theorem 4)', not first['balanced'], str(first['ledger']))
check(f'moved 16-cell: faces new at a corner are not always an interval [R, sigma] (corners with >1 minimal new face: {res["interval_failures"]})', res['interval_failures'] > 0)
check(f'moved 16-cell: class contributions have rank {res["contribution_rank"]} < {res["classes_seen"]} classes: counts not fixed by face numbers',
      res['contribution_rank'] < res['classes_seen'])
check(f'moved 16-cell: unbalanced in {res["n_unbalanced"]} of {res["n_sweeps"]} sweeps (> 0)', res['n_unbalanced'] > 0)
OUT['cases']['moved 16-cell'] = res
done += 1; log(f'PROGRESS {done / total:.3f} moved 16-cell')
Vr = []
for i in range(4):
    for s in (1, -1): v = [QF(0)] * 4; v[i] = QF(10 * s); Vr.append(tuple(v))
res2, out2 = sixteen('regular 16-cell', Vr, 50 if FULL else 10, rng)
check(f'regular 16-cell: balanced in all {res2["n_sweeps"]} generic sweeps (symmetry: Paradigm Thm 10.3)', res2['n_unbalanced'] == 0)
OUT['cases']['regular 16-cell'] = res2
done += 1; log(f'PROGRESS {done / total:.3f} regular 16-cell')

OUT['fails'] = FAILS; OUT['seconds'] = round(time.time() - T0, 1)
json.dump(OUT, open(os.path.join(HERE, '..', 'data', f'stanley-{MODE}.json'), 'w'), indent=1, default=str)
log(f'checks failed: {len(FAILS)}; {OUT["seconds"]} s')
if FAILS: log('FAIL'); [log('  ' + f) for f in FAILS]; sys.exit(1)
log(f'FINAL ok ({MODE}, {OUT["seconds"]} s)')
