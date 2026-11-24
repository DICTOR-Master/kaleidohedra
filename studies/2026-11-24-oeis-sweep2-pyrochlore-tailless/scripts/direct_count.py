#!/usr/bin/env python3
"""Closed tailless (cyclically non-backtracking) walks at one site of the pyrochlore network, n = 1..N, by direct
dynamic programming on the network itself (no formula). The pyrochlore network is built as the line graph of diamond:
a site is a diamond bond {p, q}; two sites are adjacent when the bonds share an atom. Diamond (coordinates x4 of the
cubic cell): atoms of sublattice A have x, y, z all even with x + y + z = 0 mod 4; the B atoms are A + (1,1,1); the four
bonds of an A atom go to + (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1). A walk of length n is a sequence of sites
s0 -> s1 -> ... -> sn = s0 with s(i+1) != s(i-1) and also s1 != s(n-1) (no backtrack across the closing point).
Only sites within graph distance n/2 of s0 can lie on a closed walk of length n; states are pruned by that bound."""
import sys, time
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
V = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
def is_A(p): return all(c % 2 == 0 for c in p)
def dnb(p):
    s = 1 if is_A(p) else -1
    return [tuple(p[i] + s * v[i] for i in range(3)) for v in V]
def site_nb(e):
    out = []
    for p in e:
        for q in dnb(p):
            f = frozenset((p, q))
            if f != e: out.append(f)
    return out
s0 = frozenset(((0, 0, 0), (1, 1, 1)))
R = N // 2
dist = {s0: 0}; layer = [s0]; NB = {}
for d in range(1, R + 1):
    nxt = []
    for e in layer:
        NB[e] = site_nb(e)
        for f in NB[e]:
            if f not in dist: dist[f] = d; nxt.append(f)
    layer = nxt
for e in layer: NB[e] = [f for f in site_nb(e)]
print("sites in ball", len(dist), flush=True)
assert len(NB[s0]) == 6
res = []
t0 = time.time()
# for each first step s0 -> f, DP over states (current, previous)
tot = [0] * (N + 1)
for f in NB[s0]:
    cur = {(f, s0): 1}
    for n in range(2, N + 1):
        new = {}
        rem = N - n
        for (c, p), w in cur.items():
            for g in NB.get(c, ()):
                if g == p or g not in dist or dist[g] > rem: continue
                k = (g, c); new[k] = new.get(k, 0) + w
        cur = new
        # closed at length n: current = s0, previous != f (no backtrack across the closing point)
        for (c, p), w in cur.items():
            if c == s0 and p != f: tot[n] += w
print("secs", round(time.time() - t0, 1), flush=True)
print(",".join(str(tot[n]) for n in range(1, N + 1)))
