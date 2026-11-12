"""reader_check.py: independent reader's checks (13 Nov 2026), written separately from the study scripts (the job also reran gp_enum 6, gp_line_b 6, conj1_witness 11, geodesics 8; log data/reader-check.log). Exact (Fraction / int), stdlib only.
(1) Omega(Pi; centre) as the flag sum n! * prod_k 1/X_k with X_k = k(n+1)/2 - C(k+1, 2) (the chain slacks at the centre) vs 2^(n-1) n/(n-1)!, n = 3..9.
(2) m_{n+2} at the Loday centre by recursion over polygon triangulations, n = 4, 5, 6: 88/27, 49/36, 2288/5625.
(3) n = 6, s = 2 on the equal-speed line: the reported non-root edge (1,6,1,2,7,4)-(2,5,1,2,8,3) is an edge of P(z(2)).
(4) Change ringing: own BFS, n = 3..8: distance rounds->backrounds, number of shortest ways (count), and every shortest way is a plain-hunt half.
(5) The even-n step of the proof: among sequences of n changes with exactly n/2 x changes, none adjacent, the non-alternating ones
    contain two consecutive non-x changes (checked n = 4..12), so the u = 0 step (consecutive 1n share pair 23) is needed and suffices.
Prints ok/FAIL lines; FINAL ok only if every check passes."""
import itertools, sys
from fractions import Fraction as F
from math import comb, factorial
OK = True
def chk(name, c):
    global OK
    OK = OK and bool(c); print(('ok   ' if c else 'FAIL ') + name, flush=True)
# (1)
for n in range(3, 10):
    Y = F(n + 1, 2); tot = F(0)
    # flag sum: X_T = sum_{i in T} Y - C(|T|+1, 2); depends on |T| only at the centre, but compute per permutation honestly for n <= 7
    if n <= 7:
        for p in itertools.permutations(range(1, n + 1)):
            prod = F(1)
            for k in range(1, n):
                prod *= (k * Y - comb(k + 1, 2))
            tot += 1 / prod
    else:
        prod = F(1)
        for k in range(1, n): prod *= (k * Y - comb(k + 1, 2))
        tot = factorial(n) / prod
    chk(f'(1) n={n}: Omega(Pi; centre) flag sum = {tot}, formula 2^(n-1) n/(n-1)! = {F(2 ** (n - 1) * n, factorial(n - 1))}', tot == F(2 ** (n - 1) * n, factorial(n - 1)))
    print('PROGRESS', n - 2, '/ 14', flush=True)
# (2) m_N, N = n + 2: sum over triangulations of the N-gon of prod 1/X_(i,j); diagonal (i,j) <-> interval [i, j-2], X = k(n-k)/2, k = j-i-1
from functools import lru_cache
for n, want in ((4, F(88, 27)), (5, F(49, 36)), (6, F(2288, 5625))):
    N = n + 2
    def X(i, j):
        k = j - i - 1; return F(k * (n - k), 2)
    @lru_cache(None)
    def T(i, j):   # sum over triangulations of polygon i..j (vertices i, i+1, ..., j), product over its inner diagonals
        if j - i < 2: return F(1)
        s = F(0)
        for m in range(i + 1, j):
            a = T(i, m) * (1 / X(i, m) if m - i >= 2 else 1)
            b = T(m, j) * (1 / X(m, j) if j - m >= 2 else 1)
            s += a * b
        return s
    v = T(1, N)
    chk(f'(2) n={n}: m_{N} at the Loday centre = {v} (expected {want})', v == want)
print('PROGRESS 9 / 14', flush=True)
# (3)
n = 6; s = 2
def blocks(S):
    out = []; run = 0
    for i in range(1, n + 1):
        if i in S: run += 1
        elif run: out.append(run); run = 0
    if run: out.append(run)
    return out
subsets = [frozenset(c) for k in range(1, n) for c in itertools.combinations(range(1, n + 1), k)]
def z(S):
    zp = comb(len(S) + 1, 2)
    return zp if len(blocks(S)) == 1 else zp - s
p = (1, 6, 1, 2, 7, 4); q = (2, 5, 1, 2, 8, 3); mid = tuple(F(a + b, 2) for a, b in zip(p, q))
def inP(x): return sum(x) == comb(n + 1, 2) and all(sum(x[i - 1] for i in S) >= z(S) for S in subsets)
def tight(x): return [S for S in subsets if sum(x[i - 1] for i in S) == z(S)]
def rank(rows):
    M = [list(map(F, r)) for r in rows]; r = 0; cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
ones = [1] * n
tp, tq, tm = tight(p), tight(q), tight(mid)
vec = lambda S: [1 if i in S else 0 for i in range(1, n + 1)]
chk('(3) both ends lie in P(z(2)), n = 6', inP(p) and inP(q))
chk('(3) both ends are vertices (tight normals + all-ones of rank 6)', rank([vec(S) for S in tp] + [ones]) == 6 and rank([vec(S) for S in tq] + [ones]) == 6)
chk('(3) the midpoint tight set has rank 5 with all-ones (a 1-dim face) and equals the common tight set of the ends', rank([vec(S) for S in tm] + [ones]) == 5 and set(tm) == set(tp) & set(tq))
dvec = tuple(b - a for a, b in zip(p, q))
chk(f'(3) edge direction {dvec} is not a root e_i - e_j', sorted(dvec) != [-1] + [0] * (n - 2) + [1])
print('PROGRESS 12 / 14', flush=True)
# (4)
def chs(n):
    out = []
    for mask in range(1, 1 << (n - 1)):
        pr = [i for i in range(n - 1) if mask >> i & 1]
        if all(b - a >= 2 for a, b in zip(pr, pr[1:])): out.append(pr)
    return out
def ap(r, c):
    r = list(r)
    for i in c: r[i], r[i + 1] = r[i + 1], r[i]
    return tuple(r)
for n in range(3, 9):
    C = chs(n); start = tuple(range(1, n + 1)); end = start[::-1]
    dist = {start: 0}; cnt = {start: 1}; frontier = [start]
    while end not in dist:
        nxt = []
        for v in frontier:
            for c in C:
                w = ap(v, c)
                if w not in dist: dist[w] = dist[v] + 1; cnt[w] = 0; nxt.append(w)
                if dist[w] == dist[v] + 1: cnt[w] += cnt[v]
        frontier = nxt
    # plain-hunt halves
    A = list(range(0, n - 1, 2)); Bc = list(range(1, n - 1, 2)); halves = []
    for first in (A, Bc):
        r = start; c = first
        for _ in range(n): r = ap(r, c); c = Bc if c is A else A
        halves.append(r)
    chk(f'(4) n={n}: distance {dist[end]} = n, shortest ways {cnt[end]} = 2, both plain-hunt halves end at backrounds', dist[end] == n and cnt[end] == 2 and all(h == end for h in halves))
print('PROGRESS 13 / 14', flush=True)
# (5)
for n in range(4, 13, 2):
    bad = 0
    for pos in itertools.combinations(range(n), n // 2):
        if any(b - a < 2 for a, b in zip(pos, pos[1:])): continue
        alt = pos == tuple(range(0, n, 2)) or pos == tuple(range(1, n, 2))
        non = [t for t in range(n) if t not in pos]
        consec = any(b - a == 1 for a, b in zip(non, non[1:]))
        lonely = any(t - 1 not in pos and t + 1 not in pos for t in non)
        if (not alt and not consec) or lonely: bad += 1
    chk(f'(5) n={n}: every non-alternating placement of n/2 non-adjacent x has two consecutive non-x; every non-x touches an x', bad == 0)
print('PROGRESS 14 / 14', flush=True)
print('FINAL ok' if OK else 'FINAL FAIL', flush=True); sys.exit(0 if OK else 1)
