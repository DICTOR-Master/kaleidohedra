"""Loop Equality (#74) as a theorem (paper #102): numerical re-verification on many stackings, exact integers.
Usage: python3 loop_checks.py [L_WALK L_NB L_PYRO L_CP [PART]] > data-loop-checks.txt
  (compute-host: 30 24 14 12 tetra, about 2.5 min; 30 24 14 12 other, about 1 min)
Graphs: the tetrahedral (diamond-type) network of a stacking, with the bond rule of loops2.py / oeis_checks.py
(bilayer k = lower atom u=0 and upper atom u=1 at the in-plane position of letter seq[k]; the upper atom of bilayer k bonds
to the three lower atoms of bilayer k+1 at in-plane distance 1/sqrt3); its line graph, the pyrochlore network (#60);
and the close-packed sphere packing of a stacking. Each graph is built on a finite window: N x N in-plane cells, periodic,
with N > L so that no walk can wrap round, and enough bilayers above and below the tested sites that no walk reaches the
window's top or bottom. The tested sites are the sites of a whole period (or 12 consecutive bilayers if aperiodic).
Checks, at EVERY tested site:
  W  closed walks, lengths 0..L_WALK                          = diamond (3C) values = Domb numbers A002895
  F  the chain formula W_2n = sum_a c(n,a) H(a), H = A002893  (proof of Theorem 1, Section 2)
  B  walks between the two ends of every bond                 = 3C value (Lemma 2)
  D  walks between the two ends of every path of two bonds    = 3C value (Lemma 2)
  T  closed tailless non-backtracking walks, lengths 1..L_NB  = Ihara-Bass value from the Domb numbers (oeis_checks.py C1)
  P  pyrochlore network: closed walks and tailless NB walks per site = 3C pyrochlore values
  S  close-packed spheres: closed walks and tailless NB walks per sphere = fcc values (A002899)
"""
import sys, time, random
import numpy as np
from math import comb, factorial
from fractions import Fraction as Fr
from scipy.sparse import csr_matrix
TSTART = time.time()
LW, LN, LP, LC = [int(x) for x in sys.argv[1:5]] if len(sys.argv) > 4 else (30, 24, 14, 12)
PART = sys.argv[5] if len(sys.argv) > 5 else 'all'   # 'tetra' = W F B D T (+ shells); 'other' = P S and control; 'all'
out = lambda *a: print(*a, flush=True)
a1 = np.array([1, 0.]); a2 = np.array([.5, 3 ** .5 / 2]); SH = {'A': 0, 'B': 1, 'C': 2}
def offs(lo, hi, sign):
    r = [(di, dj) for di in range(-2, 3) for dj in range(-2, 3)
         if abs(np.hypot(*(sign * (di * a1 + dj * a2) + (hi - lo) * (a1 + a2) / 3)) - 1 / np.sqrt(3)) < 1e-9]
    assert len(r) == 3; return r
OFF = {(lo, hi): offs(lo, hi, -1) for lo in range(3) for hi in range(3) if lo != hi}    # as oeis_checks.py
OFFS = {(lo, hi): offs(lo, hi, 1) for lo in range(3) for hi in range(3) if lo != hi}
INP = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]

def domb(n): return sum(comb(n, j) ** 2 * comb(2 * j, j) * comb(2 * n - 2 * j, n - j) for j in range(n + 1))
def ihara(c, q, M):   # per vertex tailless NB closed walks from closed-walk moments c (as oeis_checks.py)
    coef = [Fr(0)] * (M + 1)
    for j in range(1, M + 1):
        for i in range(j + 1):
            d = 2 * j - i
            if d <= M: coef[d] -= Fr(comb(j, i) * c[i] * (-q) ** (j - i), j)
    N = []
    for m in range(M + 1):
        L = (Fr(q - 1, 2) * Fr(2, m) if m and m % 2 == 0 else 0) - coef[m]
        x = L * m; assert x.denominator == 1; N.append(int(x))
    return N
DOMB = [domb(k // 2) if k % 2 == 0 else 0 for k in range(LW + 1)]
NBD = ihara(DOMB, 3, LW)

# ---------- F: the chain formula ----------
# level line: levels 2k (lower atoms) and 2k+1 (upper atoms); gap (2k,2k+1) intra (one bond), gap (2k+1,2k+2) inter.
# c(n,a) = closed level paths of length 2n from level 0 with exactly a upward inter crossings.  H(a) = sum (a!/(i!j!k!))^2.
def H(a): return sum((factorial(a) // (factorial(i) * factorial(j) * factorial(a - i - j))) ** 2 for i in range(a + 1) for j in range(a + 1 - i))
cpoly = {0: {0: 1}}; okF = True
for step in range(LW):
    nxt = {}
    for lev, pol in cpoly.items():
        for d in (1, -1):
            inter = (lev % 2 == 1 and d == 1) or (lev % 2 == 0 and d == -1)
            tgt = nxt.setdefault(lev + d, {})
            for a, c in pol.items():
                a2_ = a + (1 if inter and d == 1 else 0); tgt[a2_] = tgt.get(a2_, 0) + c
    cpoly = nxt
    if (step + 1) % 2 == 0:
        n = (step + 1) // 2; okF &= sum(c * H(a) for a, c in cpoly.get(0, {}).items()) == domb(n)
out(f'F chain formula sum_a c(n,a) H(a) = Domb(n) for n = 0..{LW // 2}: {okF}')

# ---------- stackings ----------
def letters_from_ch(ch, n):   # Jagodzinski: at a c layer keep the direction of the step, at an h layer reverse it
    s = [1]; pos = [0, 1]
    for k in range(1, n - 1):
        s.append(s[-1] if ch[k % len(ch)] == 'c' else -s[-1]); pos.append((pos[-1] + s[-1]) % 3)
    return ''.join('ABC'[p] for p in pos)
def fib_word(n):
    w = 'c'
    while len(w) < n: w = ''.join('ch' if x == 'c' else 'c' for x in w)
    return w
def random_periodic(p, rng):
    while True:
        s = [rng.randrange(3)]
        for _ in range(p - 1): s.append(rng.choice([x for x in range(3) if x != s[-1]]))
        if s[-1] != s[0]: return ''.join('ABC'[x] for x in s)
rng = random.Random(20261107)
STK = [('3C', 'ABC', 3), ('2H', 'AB', 2), ('4H', 'ABAC', 4), ('6H', 'ABCACB', 6), ('9R', 'ABABCBCAC', 9)]
for t in range(30):
    p = rng.randint(4, 12); STK.append((f'rand{t:02d}-p{p}', random_periodic(p, rng), p))
for F in (3, 5, 8, 13, 21):   # Fibonacci approximant: the first F letters of the c/h Fibonacci word, repeated
    STK.append((f'fib-approx-{F}', ('ch', fib_word(F)[:F]), F))
STK.append(('fib-infinite', ('ch', fib_word(600)), 12))   # the aperiodic Fibonacci stacking itself
w = [0]
for _ in range(599): w.append(rng.choice([x for x in range(3) if x != w[-1]]))
STK.append(('rand-aperiodic', ''.join('ABC'[x] for x in w), 12))
def window(spec, ntest, L):   # letters of a window and the bilayers to test (ntest consecutive bilayers in the middle)
    m = L // 2 + 3; K = ntest + 2 * m
    if isinstance(spec, tuple): seq = letters_from_ch(spec[1], 240 + K)[240:240 + K]
    elif len(spec) > 100: seq = spec[200:200 + K]
    else: seq = (spec * (K // len(spec) + 2))[:K]
    assert all(seq[k] != seq[k + 1] for k in range(K - 1))
    return seq, list(range(m, m + ntest))
def hexagonality(seq, ks): return sum(seq[k - 1] == seq[k + 1] for k in ks) / len(ks)

# ---------- graphs ----------
def tetra(seq, N):
    K = len(seq); idx = lambda k, i, j, u: ((k * N + i % N) * N + j % N) * 2 + u
    E = []
    for k in range(K):
        for i in range(N):
            for j in range(N):
                E.append((idx(k, i, j, 0), idx(k, i, j, 1)))
                if k + 1 < K:
                    lo, hi = SH[seq[k]], SH[seq[k + 1]]
                    for di, dj in OFF[(lo, hi)]: E.append((idx(k, i, j, 1), idx(k + 1, i - di, j - dj, 0)))
    pos = lambda v: ((v // 2 // N) % N) * a1 + (v // 2 % N) * a2 + SH[seq[v // 2 // (N * N)]] * (a1 + a2) / 3
    for (x, y) in E[::97]:   # geometric check on a sample of bonds: slanted bonds 1/sqrt3 apart in plane, vertical bonds 0
        d = pos(y) - pos(x); best = min(np.hypot(*(d + p * N * a1 + q * N * a2)) for p in (-1, 0, 1) for q in (-1, 0, 1))
        assert abs(best - (0 if x // 2 == y // 2 else 1 / np.sqrt(3))) < 1e-9
    return K * N * N * 2, E, idx
def adj(V, E):
    r = [x for x, y in E] + [y for x, y in E]; c = [y for x, y in E] + [x for x, y in E]
    return csr_matrix((np.ones(len(r), dtype=np.int64), (r, c)), shape=(V, V))
def nb_matrix(V, E):   # Hashimoto matrix, M[f, e] = 1 if the step e -> f does not turn back
    D = E + [(y, x) for x, y in E]; oute = [[] for _ in range(V)]
    for t, (x, y) in enumerate(D): oute[x].append(t)
    r, c = [], []
    for t, (x, y) in enumerate(D):
        for f in oute[y]:
            if D[f][1] != x: r.append(f); c.append(t)
    return csr_matrix((np.ones(len(r), dtype=np.int64), (r, c)), shape=(len(D), len(D))), oute
def walks(A, starts, L, extra):   # closed walks at each start, and walks from each start to the targets extra[c]
    X = np.zeros((A.shape[0], len(starts)), dtype=np.int64); X[starts, range(len(starts))] = 1
    cl = [[1] * len(starts)]; ex = [[[int(X[y, c]) for y in extra[c]] for c in range(len(starts))]]
    for _ in range(L):
        X = A @ X
        cl.append([int(X[s, c]) for c, s in enumerate(starts)])
        ex.append([[int(X[y, c]) for y in extra[c]] for c in range(len(starts))])
    return cl, ex
def tailless(M, edges_of_site, L, chunk=48):   # per site: sum over its outgoing edges e of (B^m)_{ee}, m = 0..L
    cols = [e for es in edges_of_site for e in es]; res = np.zeros((L + 1, len(cols)), dtype=np.int64)
    for c0 in range(0, len(cols), chunk):
        cc = cols[c0:c0 + chunk]; Y = np.zeros((M.shape[0], len(cc)), dtype=np.int64); Y[cc, range(len(cc))] = 1
        for m in range(1, L + 1):
            Y = M @ Y; res[m, c0:c0 + len(cc)] = Y[cc, range(len(cc))]
    per = []; t = 0
    for es in edges_of_site: per.append(res[:, t:t + len(es)].sum(axis=1)); t += len(es)
    return per
def tetra_checks(spec, ntest):
    L = max(LW, LN); seq, ks = window(spec, ntest, L); N = L + 2
    V, E, idx = tetra(seq, N); A = adj(V, E)
    starts = [idx(k, 0, 0, u) for k in ks for u in (0, 1)]
    nbrs = [[int(z) for z in A[s].indices] for s in starts]
    d2 = [sorted({int(z) for y in nb for z in A[y].indices if z != s}) for s, nb in zip(starts, nbrs)]
    assert all(len(n) == 4 for n in nbrs) and all(len(d) == 12 for d in d2)
    cl, ex = walks(A, starts, LW, [nb + d for nb, d in zip(nbrs, d2)])
    M, oute = nb_matrix(V, E)
    shells = []
    for s in starts:   # coordination sequence of each tested site, n = 0..8 (control: these DO depend on the site)
        seen = {s}; fr = {s}; cs = [1]
        for _ in range(8):
            nx = {int(z) for v in fr for z in A[v].indices if z not in seen}; seen |= nx; fr = nx; cs.append(len(nx))
        shells.append(cs)
    return seq, ks, cl, ex, tailless(M, [oute[s] for s in starts], LN), shells

out(f'Loop Equality checks: closed walks to length {LW}, tailless NB to {LN}, pyrochlore to {LP}, close-packed spheres to {LC}')
seq, ks, cl, ex, T, _ = tetra_checks('ABC', 3)
REF_B = [ex[L][0][0] for L in range(LW + 1)]; REF_D = [ex[L][0][4] for L in range(LW + 1)]
assert [cl[L][0] for L in range(LW + 1)] == DOMB
out('reference 3C bond walks W(a,b), L = 1,3,..,21:', REF_B[1:22:2])
out('reference 3C two-bond walks W(a,c), L = 2,4,..,22:', REF_D[2:23:2])
out('reference tailless NB per site (Ihara-Bass from Domb), L = 6,8,..:', NBD[6:LN + 1:2])
allok = True
for name, spec, p in (STK if PART in ('all', 'tetra') else []):
    t0 = time.time(); seq, ks, cl, ex, T, shells = tetra_checks(spec, min(p, 12)); S = range(len(cl[0]))
    okW = all(cl[L][c] == DOMB[L] for L in range(LW + 1) for c in S)
    okB = all(ex[L][c][j] == REF_B[L] for L in range(LW + 1) for c in S for j in range(4))
    okD = all(ex[L][c][j] == REF_D[L] for L in range(LW + 1) for c in S for j in range(4, 16))
    okT = all(int(t[m]) == NBD[m] for t in T for m in range(1, LN + 1))
    ok = okW and okB and okD and okT; allok &= ok
    out(f'{name:15s} bilayers {seq[ks[0]:ks[-1] + 1]:12s} h={hexagonality(seq, ks):.3f} sites {2 * len(ks):2d}: '
        f'W {okW} B {okB} D {okD} T {okT} ({time.time() - t0:.1f} s)')
    out(f'  shells n=3..8 per site: ' + ' '.join(','.join(map(str, c[3:])) for c in shells))
    out(f'  per site NB L={LN} / closed L={LW}: ' + ' '.join(f'{int(t[LN])}/{cl[LW][c]}' for c, t in enumerate(T)))
if PART in ('all', 'tetra'): out('TETRA all', len(STK), 'stackings, every tested site:', allok)
if PART == 'tetra': out(f'FINAL {"ok" if allok and okF else "FAIL"} part tetra ({time.time() - TSTART:.0f} s)'); sys.exit()

# ---------- pyrochlore network = line graph of the tetrahedral network ----------
def pyro_checks(spec, ntest, L):
    seq, ks = window(spec, ntest, 2 * L + 2); N = L + 3
    V, E, idx = tetra(seq, N)
    inc = [[] for _ in range(V)]
    for t, (x, y) in enumerate(E): inc[x].append(t); inc[y].append(t)
    PE = sorted({(min(s, t), max(s, t)) for v in range(V) for s in inc[v] for t in inc[v] if s != t})
    A = adj(len(E), PE)
    starts = sorted({t for k in ks for u in (0, 1) for t in inc[idx(k, 0, 0, u)]})
    assert all(len(A[t].indices) == 6 for t in starts)
    cl, _ = walks(A, starts, L, [[] for _ in starts])
    M, oute = nb_matrix(len(E), PE)
    return cl, tailless(M, [oute[s] for s in starts], L), len(starts)
cl0, T0p, _ = pyro_checks('ABC', 3, LP)
PW = [cl0[L][0] for L in range(LP + 1)]; PT = [int(T0p[0][m]) for m in range(LP + 1)]
assert all(cl0[L][c] == PW[L] for L in range(LP + 1) for c in range(len(cl0[0])))
out(f'pyrochlore (3C) closed walks per site, L = 0..{LP}:', PW)
out(f'pyrochlore (3C) tailless NB per site, L = 1..{LP}:', PT[1:])
SUB = STK[1:13] + STK[-7:]
okP = True
for name, spec, p in SUB:
    t0 = time.time(); cl, T, ns = pyro_checks(spec, min(p, 12), LP)
    ok = all(cl[L][c] == PW[L] for L in range(LP + 1) for c in range(ns)) and all(int(t[m]) == PT[m] for t in T for m in range(1, LP + 1))
    okP &= ok; out(f'PYRO {name:15s} sites {ns:3d}: {ok} ({time.time() - t0:.1f} s)')
out('PYRO all', len(SUB), 'tested stackings, every tested site:', okP)

# ---------- close-packed spheres ----------
def cp_checks(spec, ntest, L):
    seq, ks = window(spec, ntest, 2 * L); N = L + 2; K = len(seq)
    idx = lambda k, i, j: (k * N + i % N) * N + j % N
    E = set()
    for k in range(K):
        for i in range(N):
            for j in range(N):
                v = idx(k, i, j)
                for a, b in INP: x = idx(k, i + a, j + b); E.add((min(v, x), max(v, x)))
                if k + 1 < K:
                    for a, b in OFFS[(SH[seq[k]], SH[seq[k + 1]])]: E.add((v, idx(k + 1, i + a, j + b)))
    E = sorted(E); V = K * N * N; A = adj(V, E)
    starts = [idx(k, 0, 0) for k in ks]; assert all(len(A[s].indices) == 12 for s in starts)
    cl, _ = walks(A, starts, L, [[] for _ in starts])
    M, oute = nb_matrix(V, E)
    return cl, tailless(M, [oute[s] for s in starts], L)
cl0, T0c = cp_checks('ABC', 3, LC)
CW = [cl0[L][0] for L in range(LC + 1)]; CT = [int(T0c[0][m]) for m in range(LC + 1)]
out(f'fcc closed walks per sphere (A002899), L = 0..{LC}:', CW)
out(f'fcc tailless NB per sphere, L = 1..{LC}:', CT[1:])
okS = True
for name, spec, p in SUB:
    t0 = time.time(); cl, T = cp_checks(spec, min(p, 12), LC)
    ok = all(cl[L][c] == CW[L] for L in range(LC + 1) for c in range(len(cl[0]))) and all(int(t[m]) == CT[m] for t in T for m in range(1, LC + 1))
    okS &= ok; out(f'SPHERES {name:15s} spheres {len(cl[0]):2d}: {ok} ({time.time() - t0:.1f} s)')
out('SPHERES all', len(SUB), 'tested stackings, every tested sphere:', okS)

# ---------- control: the networks do differ (coordination sequences 3C vs 2H, A008253 / A008264) ----------
def coord(spec, R=6):
    seq, ks = window(spec, 1, 2 * R); N = 2 * R + 3; V, E, idx = tetra(seq, N); A = adj(V, E)
    s = idx(ks[0], 0, 0, 0); seen = {s}; fr = {s}; cs = [1]
    for _ in range(R):
        nx = {int(z) for v in fr for z in A[v].indices if z not in seen}; seen |= nx; fr = nx; cs.append(len(nx))
    return cs
c3, c2 = coord('ABC'), coord('AB')
out('control coordination sequences 3C', c3, ' 2H', c2)
assert c3 == [1, 4, 12, 24, 42, 64, 92] and c2 == [1, 4, 12, 25, 44, 67, 96]
out(f'FINAL {"ok" if allok and okP and okS and okF else "FAIL"} part {PART} ({time.time() - TSTART:.0f} s)')
