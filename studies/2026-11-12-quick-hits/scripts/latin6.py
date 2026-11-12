# latin6.py: independent recomputation (our own code, from the paper's definitions) of the order-six census of "Determinant
# Divisibility of Centered Latin Squares" (aiXiv 2609.03275; repo aconsciousfractal/Determinant-Divisibility-of-Centered-Latin-Squares).
# Definitions (paper §2): L a Latin square with entries 1..n; A_ij = L_ij - L_{i,n-1} (0 <= i, j <= n-2); det(E_std) = n det(A).
# Claims (REPRODUCE.md, order six): 9408 reduced Latin squares; 8832 with 36 | det(E_std), 576 with 18 | det but 36 does not;
# 1252 distinct parity patterns L mod 2; 84 of them with full-rank A mod 2; 0 patterns with mixed outcomes; 80 associative reduced
# squares (group tables), 36 of them with 36 not dividing det(E_std). Theorem (binary criterion, n = 2 mod 4): n^2 | det(E_std)
# <=> rank_F2(A mod 2) < n - 1, checked on every square.
import itertools
from fractions import Fraction
n = 6
def reduced_latin(n):
    """all reduced Latin squares of order n (first row and column 1..n in order), symbols 1..n"""
    out = []; L = [[0] * n for _ in range(n)]
    for j in range(n): L[0][j] = j + 1
    for i in range(n): L[i][0] = i + 1
    cells = [(i, j) for i in range(1, n) for j in range(1, n)]
    def bt(k):
        if k == len(cells): out.append(tuple(tuple(r) for r in L)); return
        i, j = cells[k]
        used = set(L[i][:j]) | {L[r][j] for r in range(i)}
        for s in range(1, n + 1):
            if s not in used: L[i][j] = s; bt(k + 1)
        L[i][j] = 0
    bt(0); return out
def det(M):
    M = [[Fraction(x) for x in r] for r in M]; m = len(M); d = Fraction(1)
    for c in range(m):
        p = next((r for r in range(c, m) if M[r][c] != 0), None)
        if p is None: return 0
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, m):
            f = M[r][c] / M[c][c]
            if f: M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return int(d)
def rank2(M):
    rows = [int(''.join(str(x % 2) for x in r), 2) for r in M]; rk = 0; w = len(M[0])
    for bit in reversed(range(w)):
        piv = next((i for i, r in enumerate(rows) if r >> bit & 1), None)
        if piv is None: continue
        p = rows.pop(piv); rk += 1; rows = [r ^ p if r >> bit & 1 else r for r in rows]
    return rk
def assoc(L):
    op = lambda a, b: L[a - 1][b - 1]
    return all(op(op(a, b), c) == op(a, op(b, c)) for a in range(1, n + 1) for b in range(1, n + 1) for c in range(1, n + 1))
S = reduced_latin(n)
c36 = c18 = 0; patterns = {}; crit_bad = 0; groups = 0; group_cex = 0
for L in S:
    A = [[L[i][j] - L[i][n - 1] for j in range(n - 1)] for i in range(n - 1)]
    dE = n * det(A); assert dE % 18 == 0, 'baseline n^2/2 fails'
    full = dE % 36 == 0
    if full: c36 += 1
    else: c18 += 1
    r = rank2(A)
    if (dE % 36 == 0) != (r < n - 1): crit_bad += 1
    pat = tuple(tuple(x % 2 for x in row) for row in L)
    patterns.setdefault(pat, set()).add((dE % 36 == 0, r == n - 1))
    if assoc(L):
        groups += 1
        if dE % 36: group_cex += 1
mixed = sum(1 for v in patterns.values() if len({a for a, b in v}) > 1)
fullrank_pats = sum(1 for v in patterns.values() if any(b for a, b in v))
print(f'reduced Latin squares {len(S)} (claim 9408)')
print(f'36 | det(E_std): {c36} (claim 8832); 18 | det only: {c18} (claim 576)')
print(f'distinct parity patterns {len(patterns)} (claim 1252); with full-rank A mod 2: {fullrank_pats} (claim 84); mixed outcomes: {mixed} (claim 0)')
print(f'binary criterion violations: {crit_bad} (theorem: 0)')
print(f'associative (group tables): {groups} (claim 80); with 36 not dividing det: {group_cex} (claim 36)')
ok = (len(S), c36, c18, len(patterns), fullrank_pats, mixed, crit_bad, groups, group_cex) == (9408, 8832, 576, 1252, 84, 0, 0, 80, 36)
print('FINAL ok: every order-six claim recomputed and equal' if ok else 'FINAL FAIL: see the lines above')
