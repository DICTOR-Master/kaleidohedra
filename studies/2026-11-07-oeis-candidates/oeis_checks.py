"""OEIS candidates (2026-11-07): recompute every sequence in papers/oeis-candidates-2026-11-07.md, exact integers.
Usage: python3 oeis_checks.py > data-oeis-terms.txt   (about 1 minute on the Pi; numpy only)"""
import itertools, numpy as np
from fractions import Fraction as Fr
from math import comb, isqrt
from collections import defaultdict
out = print
# ---------- 1. Ihara-Bass: cyclically non-backtracking closed walks per vertex from closed-walk moments ----------
def ihara(c, q, M):
    """per vertex: sum_m N_m u^m/m = ((q-1)/2) sum_k u^{2k}/k - E[log(1 - lam u + q u^2)], E[lam^i] = c[i]"""
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
def domb(n): return sum(comb(n, j) ** 2 * comb(2 * j, j) * comb(2 * n - 2 * j, n - j) for j in range(n + 1))  # A002895
M = 60
cd = [domb(k // 2) if k % 2 == 0 else 0 for k in range(M + 1)]
nb = ihara(cd, 3, M)
out('C1 NB closed walks per diamond vertex, length 2n, n=1..30:', ','.join(str(nb[2 * n]) for n in range(1, 31)))
dicto = [24, 48, 480, 3432, 25704, 194256, 1509072, 11820000, 93722376, 750276792, 6056400480, 49241424120, 402912569544,
         3315331754256, 27416593190640]   # studies/2026-10-28-pyrochlore-kagome/loops2.out, L = 6..34
assert [nb[L] for L in range(6, 35, 2)] == dicto; out('C1 check: equals loops2.out (direct count, five stackings) for L = 6..34')
# ---------- 2. tetrahedral close-packed stackings (3C, 2H, 4H, 6H): closed walks per site, coordination sequences ----------
a1 = np.array([1, 0.]); a2 = np.array([.5, 3 ** .5 / 2]); SH = {'A': 0, 'B': 1, 'C': 2}
def offs(lo, hi, sign):
    r = [(di, dj) for di in range(-2, 3) for dj in range(-2, 3)
         if abs(np.hypot(*(sign * (di * a1 + dj * a2) + (hi - lo) * (a1 + a2) / 3)) - 1 / np.sqrt(3)) < 1e-9]
    assert len(r) == 3; return r
OFF = {(lo, hi): offs(lo, hi, -1) for lo in range(3) for hi in range(3) if lo != hi}
def tetra_nbrs(seq):   # site (k,i,j,u): bilayer k, cell (i,j), u = 0 lower / 1 upper atom; same rule as loops2.py
    p = len(seq)
    def f(v):
        k, i, j, u = v
        if u == 0:
            lo, hi = SH[seq[(k - 1) % p]], SH[seq[k % p]]
            return [(k, i, j, 1)] + [(k - 1, i + di, j + dj, 1) for di, dj in OFF[(lo, hi)]]
        lo, hi = SH[seq[k % p]], SH[seq[(k + 1) % p]]
        return [(k, i, j, 0)] + [(k + 1, i - di, j - dj, 0) for di, dj in OFF[(lo, hi)]]
    return f
def closed_walks(f, v0, L):
    vec = {v0: 1}; r = [1]
    for _ in range(L):
        nv = defaultdict(int)
        for v, c in vec.items():
            for w in f(v): nv[w] += c
        vec = nv; r.append(vec.get(v0, 0))
    return r
def coordseq(f, v0, R):
    seen = {v0}; fr = {v0}; cs = [1]
    for _ in range(R):
        nx = {w for v in fr for w in f(v) if w not in seen}; seen |= nx; fr = nx; cs.append(len(nx))
    return cs
STK = [('3C', 'ABC'), ('2H', 'AB'), ('4H', 'ABAC'), ('6H', 'ABCACB')]
for name, seq in STK:
    f = tetra_nbrs(seq); ok = True
    for k in range(len(seq)):
        for u in (0, 1):
            r = closed_walks(f, (k, 0, 0, u), 30); ok &= all(r[l] == cd[l] for l in range(31))
    out(f'C2 {name}: closed walks of length 0..30 at every site equal the Domb numbers A002895: {ok}')
for name, seq in STK:
    f = tetra_nbrs(seq); p = len(seq); seen = {}
    for k in range(p):
        for u in (0, 1):
            cs = tuple(coordseq(f, (k, 0, 0, u), 60))
            jag = 'h' if seq[(k - 1) % p] == seq[(k + 1) % p] else 'c'
            if cs not in seen:
                seen[cs] = (k, u, jag); out(f'C3 {name} site (bilayer {k} [{seq[k]}, {jag}], atom {u}):', ','.join(map(str, cs)))
# ---------- 2b. close-packed spheres (fcc ABC, hcp AB, dhcp ABAC): closed walks per sphere ----------
INP = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
OFFS = {(lo, hi): offs(lo, hi, 1) for lo in range(3) for hi in range(3) if lo != hi}
def cp_nbrs(seq):
    p = len(seq)
    def f(v):
        k, i, j = v; o = [(k, i + a, j + b) for a, b in INP]
        for dk in (1, -1):
            o += [(k + dk, i + a, j + b) for a, b in OFFS[(SH[seq[k % p]], SH[seq[(k + dk) % p]])]]
        return o
    return f
fccw = closed_walks(cp_nbrs('ABC'), (0, 0, 0), 12)
for name, seq in [('hcp', 'AB'), ('dhcp', 'ABAC')]:
    f = cp_nbrs(seq)
    out(f'C2b {name}: closed walks 0..12 at every sphere equal fcc (A002899):',
        all(closed_walks(f, (k, 0, 0), 12) == fccw for k in range(len(seq))))
out('C2b fcc closed walks 0..12:', ','.join(map(str, fccw)))
# ---------- 1b. fcc: NB closed walks per sphere (Ihara-Bass, q = 11) from fcc closed walks (A002899) ----------
st = [v for v in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, v)) == 2]
vec = {(0, 0, 0): 1}; cf = [1]
for _ in range(24):
    nv = defaultdict(int)
    for (x, y, z), c in vec.items():
        for a, b, d in st: nv[(x + a, y + b, z + d)] += c
    vec = nv; cf.append(vec.get((0, 0, 0), 0))
nbf = ihara(cf, 11, 24)
out('C1b NB closed walks per fcc sphere, length 3..24:', ','.join(map(str, nbf[3:])))
# ---------- 4. Poincare dodecahedral space: invariant harmonics of degree k = (k+1) * Molien coefficient of 2I ----------
m = [0] * 121
for a in range(11):
    for b in range(7):
        for e in (0, 30):
            d = 12 * a + 20 * b + e
            if d <= 120: m[d] += 1
out('C4 PDS multiplicities, k = 0,2,...,120:', ','.join(str((k + 1) * m[k]) for k in range(0, 121, 2)))
try:
    import json
    rows = json.load(open('../2026-11-04-pds-modes/data/pds-modes.json'))['rows']
    out('C4 check: equals pds-modes.json (icosian character average) at all', len(rows), 'degrees:', all(r[1] == (r[0] + 1) * m[r[0]] for r in rows))
except FileNotFoundError: pass
# ---------- 5. Fibonacci stacking: letters A,B,C = 0,1,2 and steps ----------
w = 'c'
while len(w) < 400: w = ''.join('ch' if x == 'c' else 'c' for x in w)
s = [1]
for t in w[1:]: s.append(s[-1] if t == 'c' else -s[-1])
pos = [0]
for x in s[:-1]: pos.append((pos[-1] + x) % 3)
assert all(('h' if pos[k - 1] == pos[k + 1] else 'c') == w[k] for k in range(1, 390))   # Jagodzinski recheck
A085002 = [((n + isqrt(5 * n * n)) // 2) % 2 for n in range(450)]
assert all((s[k] == 1) == (A085002[k + 2] == 1) for k in range(390))
out('C5 Fibonacci stacking letters (A,B,C = 0,1,2), layers 0..104:', ','.join(map(str, pos[:105])))
out('C5 check: step s_k = +1 exactly when A085002(k+2) = 1 (k < 390); Jagodzinski types recovered')
# ---------- 6. multiplet ladders (Weyl dimension formula) ----------
def su4(a, b, c): return (a + 1) * (b + 1) * (c + 1) * (a + b + 2) * (b + c + 2) * (a + b + c + 3) // 12
def Bn(dyn):
    n = len(dyn); lam = [sum(dyn[i:n - 1]) + Fr(dyn[-1], 2) for i in range(n)]; rho = [Fr(2 * (n - i) - 1, 2) for i in range(n)]
    l = [lam[i] + rho[i] for i in range(n)]; d = Fr(1)
    for i in range(n):
        d *= l[i] / rho[i]
        for j in range(i + 1, n): d *= (l[i] ** 2 - l[j] ** 2) / (rho[i] ** 2 - rho[j] ** 2)
    assert d.denominator == 1; return int(d)
assert (su4(1, 0, 0), su4(0, 1, 0), su4(1, 0, 1), Bn([1, 0, 0]), Bn([0, 1, 0]), Bn([0, 0, 1]), Bn([1, 0, 0, 0]), Bn([0, 0, 0, 1])) == (4, 6, 15, 7, 21, 8, 9, 16)
F = [0, 1]; P = [0, 1]; Q = [1, 1]
for _ in range(40): F.append(F[-1] + F[-2]); P.append(2 * P[-1] + P[-2]); Q.append(2 * Q[-1] + Q[-2])
out('C6a SU(4) (F(n+1),F(n),F(n+1)), n=1..15:', ','.join(str(su4(F[n + 1], F[n], F[n + 1])) for n in range(1, 16)))
out('C6b SU(4) (F(n),F(n+1),F(n)), n=1..15:', ','.join(str(su4(F[n], F[n + 1], F[n])) for n in range(1, 16)))
out('C6c SO(7) (0,P(n),Q(n)) [Q = A001333], n=1..12:', ','.join(str(Bn([0, P[n], Q[n]])) for n in range(1, 13)))
out('    (paper writes (0,P(n),P(n+1)); that would give', ','.join(str(Bn([0, P[n], P[n + 1]])) for n in range(1, 5)), '... not the printed 112, 4928, ...)')
out('C6d SO(9) (0,F(n),F(n+1),0), n=1..12:', ','.join(str(Bn([0, F[n], F[n + 1], 0])) for n in range(1, 13)))
out('C6e SO(9) (0,F(n+1),F(n),0), n=1..12:', ','.join(str(Bn([0, F[n + 1], F[n], 0])) for n in range(1, 13)))
# ---------- 7. approximant ladder: tiles per conventional cubic cell ----------
out('C7 rung F(n+1)/F(n), conventional cubic cell, n=1..12: prolate 4F(3n+2):', ','.join(str(4 * F[3 * n + 2]) for n in range(1, 13)))
out('   oblate 4F(3n+1):', ','.join(str(4 * F[3 * n + 1]) for n in range(1, 13)), ' total 4F(3n+3):', ','.join(str(4 * F[3 * n + 3]) for n in range(1, 13)))
prim = [16, 136, 576, 1220, 10336, 43784, 92736, 785672, 3328160, 7049156, 59721408]   # exact_counts.py, rungs 1/1..144/89 (run 2026-11-07 on compute-host)
out('C7 check: primitive-cell counts = 4F(3n+3), halved exactly when F(n) and F(n+1) are both odd (n = 1 mod 3):',
    all(prim[n - 1] == 4 * F[3 * n + 3] // (2 if n % 3 == 1 else 1) for n in range(1, 12)))
out('FINAL ok')
