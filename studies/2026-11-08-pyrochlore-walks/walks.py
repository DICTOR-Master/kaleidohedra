"""Closed walks and tailless non-backtracking closed walks per site on the pyrochlore network (the corner-sharing tetrahedra of
spin ice), lengths 1..LMAX, exact integers, computed directly on the network (no formula). Coordinates x4: fcc translations
(0,2,2),(2,0,2),(2,2,0); basis (0,0,0),(0,1,1),(1,0,1),(1,1,0); bonds = squared distance 2. All sites are equivalent.
Closed walks: dynamic programming over every site within LMAX/2 steps. Tailless NB walks: (1/|V|) trace(B^L), B the Hashimoto
(non-backtracking edge) matrix, counted from the site's 6 outgoing edges. Cross-check: the Ihara-Bass formula for a 6-regular
graph (q = 5) turns the closed-walk counts into the NB counts; both must agree for every L. Compares with the study data."""
import sys, itertools
from fractions import Fraction
from math import comb
LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30
B = [(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
def nbrs(p):
    out = []
    for d in itertools.product((-1, 0, 1), repeat=3):
        if sum(x * x for x in d) != 2: continue
        q = tuple(a + b for a, b in zip(p, d))
        # q must be a pyrochlore site: q - basis in the fcc lattice (even coords, even sum/2)
        if any(all((qq - bb) % 2 == 0 for qq, bb in zip(q, b)) and (sum(qq - bb for qq, bb in zip(q, b)) // 2) % 2 == 0 for b in B):
            out.append(q)
    return out
o = (0, 0, 0); assert len(nbrs(o)) == 6 and all(len(nbrs(q)) == 6 for q in nbrs(o))
R = LMAX // 2 + 1
dist = {o: 0}; frontier = [o]
for r in range(1, R + 1):
    nf = []
    for p in frontier:
        for q in nbrs(p):
            if q not in dist: dist[q] = r; nf.append(q)
    frontier = nf
N = {p: [q for q in nbrs(p) if q in dist] for p in dist}
# closed walks
cur = {o: 1}; W = [1]
for L in range(1, LMAX + 1):
    nxt = {}
    for p, c in cur.items():
        if dist[p] > LMAX - L + 1: continue
        for q in N[p]: nxt[q] = nxt.get(q, 0) + c
    cur = nxt; W.append(cur.get(o, 0))
# tailless NB: states = directed edge (a -> b); start on each edge out of o, require return to the same start edge after L steps
NB = [0]
starts = [(o, q) for q in nbrs(o)]
for L in range(1, LMAX + 1): NB.append(0)
for e0 in starts:
    cur = {e0: 1}
    for L in range(1, LMAX + 1):
        # cur holds walks of L edges ending with edge e; count those whose NEXT edge would be e0 (closing NB, cyclically NB)
        NB[L] += sum(c for (a, b), c in cur.items() if b == e0[0] and a != e0[1])
        nxt = {}
        for (a, b), c in cur.items():
            for d in N.get(b, []):
                if d == a: continue
                if dist.get(d, 99) > LMAX: continue
                nxt[(b, d)] = nxt.get((b, d), 0) + c
        cur = nxt
# Ihara-Bass cross-check (per vertex, (q+1)-regular, q = 5), as in A400949's program
def ihara(W, q):
    M = len(W) - 1; c = [Fraction(0)] * (M + 1)
    for k in range(1, M // 2 + 1): c[2 * k] += Fraction(q - 1, 2 * k)
    for j in range(1, M + 1):
        for i in range(j + 1):
            if 2 * j - i <= M: c[2 * j - i] += Fraction(comb(j, i) * W[i] * (-q) ** (j - i), j)
    return [int(m * c[m]) for m in range(1, M + 1)]
IB = ihara(W, 5)
print('closed walks per site, L = 0..%d:' % LMAX, W)
print('tailless NB closed walks per site, L = 1..%d:' % LMAX, NB[1:])
STUDY_W = [1, 0, 6, 12, 78, 300, 1512, 7056, 35214, 176124]
STUDY_NB = [0, 0, 12, 12, 0, 276, 756, 2988, 16104, 64800]
ok = IB == NB[1:] and W[:len(STUDY_W)] == STUDY_W and NB[1:1 + len(STUDY_NB)] == STUDY_NB
print('Ihara-Bass agrees for every L:', IB == NB[1:], '| agrees with the Loop Equality study data:', W[:10] == STUDY_W, NB[1:11] == STUDY_NB)
print('FINAL ok' if ok else 'FINAL FAIL: direct counts, Ihara-Bass and study data disagree')
