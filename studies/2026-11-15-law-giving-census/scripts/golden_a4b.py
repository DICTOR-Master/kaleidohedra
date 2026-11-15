#!/usr/bin/env python3
"""Why do the two A4 golden members go silent in two degrees at once?  For every subgroup K of S5 (all 156, by closure of
pairs of permutations) split the corner set into K-orbits and test whether EVERY K-orbit is itself silent in the two degrees
(a piecewise explanation, as the two icosahedra explain Icosaxes).  Tones of a piece Q: sum over pairs of Gegenbauer U_k(cos) (exact)."""
import itertools, sympy as sp
from functools import lru_cache
phi = (1 + sp.sqrt(5))/2
def pts(base):
    P = sorted(set(itertools.permutations(base)), key=str); m = sum(base)/5
    return [tuple(sp.nsimplify(sp.expand(x - m)) for x in p) for p in P]
S5 = list(itertools.permutations(range(5)))
def comp(a, b): return tuple(a[b[i]] for i in range(5))
def closure(gens):
    G = {tuple(range(5))}; fr = [tuple(range(5))]
    while fr:
        nf = []
        for g in fr:
            for h in gens:
                x = comp(h, g)
                if x not in G: G.add(x); nf.append(x)
        fr = nf
    return frozenset(G)
subs = set()
for a in S5:
    for b in S5: subs.add(closure([a, b]))
subs = sorted(subs, key=len); print('subgroups of S5:', len(subs), flush=True)
x = sp.Symbol('x')
U = {k: sp.chebyshevu(k, x) for k in range(1, 11)}
def run(name, base, degs):
    P = pts([sp.nsimplify(sp.expand(b)) for b in base]); idx = {p: i for i, p in enumerate(P)}
    raw = sorted(set(itertools.permutations([sp.nsimplify(sp.expand(b)) for b in base])), key=str)
    nn = sp.nsimplify(sp.expand(sum(a*a for a in P[0])))
    C = [[sp.nsimplify(sp.expand(sum(a*b for a, b in zip(p, q))/nn)) for q in P] for p in P]
    @lru_cache(None)
    def piece_tone(piece, k):
        return sp.nsimplify(sp.expand(sum(U[k].subs(x, C[i][j]) for i in piece for j in piece)))
    m = sum(base)/5
    def act(g, p):   # permute coordinates of the uncentred point
        return p
    # orbits: S5 permutes coordinates; centred points permute the same way
    hits = []
    for K in subs:
        seen = set(); orbs = []
        for i, p in enumerate(P):
            if i in seen: continue
            orb = frozenset(idx[tuple(p[g[c]] for c in range(5))] for g in K); seen |= orb; orbs.append(orb)
        if len(orbs) == 1: continue
        if all(piece_tone(o, k) == 0 for o in orbs for k in degs):
            other = [k for k in range(1, 11) if k not in degs and all(piece_tone(o, k) == 0 for o in orbs)]
            hits.append((len(K), [len(o) for o in orbs], other))
    print(f'{name}: subgroups K whose every orbit is silent in degrees {degs}: {len(hits)}', flush=True)
    for h in sorted(set((a, tuple(b), tuple(c)) for a, b, c in hits)): print(f'   |K| = {h[0]}, piece sizes {list(h[1])}, pieces also silent in {list(h[2])}', flush=True)
    return hits
h1 = run('20 corners o3o3x3x at t = phi', (phi**2, phi**2, phi**2, phi, 0), (5, 7))
h2 = run('30 corners o3x3o3x at t = 1/phi', (phi**2, phi**2, 1, 1, 0), (3, 6))
h3 = run('control 20 corners at t = 2', (3, 3, 3, 2, 0), (5, 7))
print('FINAL ok' if not h3 else 'FINAL FAIL')
