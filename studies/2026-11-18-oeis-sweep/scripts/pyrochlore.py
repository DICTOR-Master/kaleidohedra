"""Pyrochlore network (spin ice; #102 Corollary 2): closed walks and closed tailless non-backtracking walks per site.

Method A (this script, new): the pyrochlore network is the line graph L(G) of the diamond network G (sites = bonds of diamond,
two sites joined when their bonds share an atom). For a d-regular graph, the adjacency spectrum of L(G) is {lambda + d - 2 :
lambda in spec(G)} together with -2 for the remaining |E| - |V| eigenvalues. Diamond is 4-regular with |E| = 2|V|, so per site
    W(m) = (1/2) * sum_i C(m,i) 2^(m-i) D(i)  +  (1/2) (-2)^m,
with D(i) = closed i-step walks per diamond atom = Domb number A002895(i/2) for i even, 0 for i odd.
Tailless NB walks: Ihara-Bass for a 6-regular graph (q = 5), the same transform as in A400949's program.

Method B (independent, study 2026-11-08-pyrochlore-walks/walks.py, FINAL ok): direct dynamic programming on the network itself
for L <= 30 (closed walks) and direct Hashimoto edge-walk count (tailless NB). Its outputs are pasted below and compared.
Run: python pyrochlore.py  (prints terms to L = 40 and the comparison)."""
from math import comb
from fractions import Fraction

LMAX = 40
def domb(n): return sum(comb(n, k) ** 2 * comb(2 * k, k) * comb(2 * n - 2 * k, n - k) for k in range(n + 1))
D = [domb(i // 2) if i % 2 == 0 else 0 for i in range(LMAX + 1)]
W = []
for m in range(LMAX + 1):
    s = sum(comb(m, i) * 2 ** (m - i) * D[i] for i in range(m + 1)) + (-2) ** m
    assert s % 2 == 0
    W.append(s // 2)

def ihara(W, q):  # per vertex of a (q+1)-regular graph; returns tailless NB closed walks for lengths 1..M
    M = len(W) - 1; c = [Fraction(0)] * (M + 1)
    for k in range(1, M // 2 + 1): c[2 * k] += Fraction(q - 1, 2 * k)
    for j in range(1, M + 1):
        for i in range(j + 1):
            if 2 * j - i <= M: c[2 * j - i] += Fraction(comb(j, i) * W[i] * (-q) ** (j - i), j)
    out = [m * c[m] for m in range(1, M + 1)]
    assert all(x.denominator == 1 for x in out)
    return [int(x) for x in out]
NB = ihara(W, 5)

# Method B data (walks.py direct counts, data-walks-30.txt)
B_W = [1, 0, 6, 12, 78, 300, 1512, 7056, 35214, 176124, 902496, 4679136, 24590208, 130560768, 699729792, 3779987712, 20562988878, 112547448924, 619346672208, 3424664011776, 19018122975768, 106021551258096, 593110987716000, 3328539189498432, 18733818892838688, 105717847936756800, 598035541490454528, 3390631479921169920, 19263561414031164672, 109655484361799852544, 625322550966187133952]
B_NB = [0, 0, 12, 12, 0, 276, 756, 2988, 16104, 64800, 278916, 1286352, 5738928, 25845036, 118098612, 540178572, 2482501704, 11470845192, 53186644596, 247472898972, 1155354197016, 5409675441324, 25398322598892, 119545910744592, 563987677987800, 2666471876270592, 12632008967689620, 59953672872323256, 285045170715444144, 1357431489995004156]

print('closed walks per pyrochlore site, L = 0..%d:' % LMAX); print(','.join(map(str, W)))
print('tailless NB closed walks per pyrochlore site, L = 1..%d:' % LMAX); print(','.join(map(str, NB)))
okW = W[:31] == B_W; okNB = NB[:30] == B_NB
print('closed walks: line-graph formula == direct count (L = 0..30):', okW)
print('tailless NB: Ihara-Bass(formula) == direct Hashimoto count (L = 1..30):', okNB)
print('FINAL ok' if okW and okNB else 'FINAL FAIL')
