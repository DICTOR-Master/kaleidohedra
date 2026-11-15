#!/usr/bin/env python3
"""Controls for the hidden-zeros census (exact):
 C1 known points: the golden 20-set and 30-set (census) give zeros {1,2,5,7} and {1,2,3,6}; the 600-cell kills all k <= 20 but 12, 20;
    the 24-cell inside the 600-cell kills exactly the degrees with no F4 invariant.
 C2 random: 3000 random subsets of the 600-cell (sizes 10..60) show no exact zero at any k <= 20.
 C3 wrong mechanism: the rule 'a Galois-self set is silent in every odd degree' must fail on the census sets (data/census-U600.json)."""
import sys, os, json, itertools
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hz_core import *
from hz_universes import *
ok = True
X, A, lab, Lp, Rp, St, sig = h4_ambient(); U = u600(X)
# C1: golden sets via exact Gram-matrix matching: build them in A4 coordinates and compare zero sets computed independently (sympy)
phi = (1 + sp.sqrt(5)) / 2
def golden(base):
    P = sorted(set(itertools.permutations(base)), key=str); m = sum(base) / 5
    return [tuple(sp.nsimplify(sp.expand(x - m)) for x in p) for p in P]
def zeros_sym(P, kmax=20):
    x = sp.Symbol('x'); nn = sp.expand(sum(a * a for a in P[0])); out = []
    for k in range(1, kmax + 1):
        U_ = sp.chebyshevu(k, x)
        tot = sum(U_.subs(x, sp.expand(sum(a * b for a, b in zip(P[0], q)) / nn)) for q in P)
        if sp.nsimplify(sp.expand(tot)) == 0: out.append(k)
    return out
z20 = zeros_sym(golden([phi**2, phi**2, phi**2, phi, 0])); z30 = zeros_sym(golden([phi**2, phi**2, 1, 1, 0]))
print('C1 golden 20-set zeros', z20, ' 30-set zeros', z30, flush=True)
ok &= z20 == [1, 2, 5, 7] and z30 == [1, 2, 3, 6]
# the same zero patterns must occur among the S5-orbits of the 600-cell in H4 coordinates (exact)
d = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'census-U600.json')))
pats = {(s['size'], tuple(s['zeros'])) for s in d['sets'] if s['kind'] == 'orbit'}
c1b = (20, (1, 2, 5, 7)) in pats and (30, (1, 2, 3, 6)) in pats
print('C1 golden patterns present among the 600-cell orbits:', c1b); ok &= c1b
z600 = U.zeros(range(120)); print('C1 600-cell zeros', z600); ok &= z600 == [k for k in range(1, 21) if k not in (12, 20)]
rat = [i for i in range(120) if (X[i, :, 1] == 0).all()]
z24 = U.zeros(rat); f4 = [k for k in range(1, 21) if k not in (6, 8, 12, 14, 16, 18, 20)]
print('C1 24-cell zeros', z24, 'expected (no F4 harmonic invariant)', f4); ok &= z24 == f4
# C2 random subsets
rng = np.random.default_rng(2026); hits = 0
for t in range(3000):
    n = int(rng.integers(10, 61)); S = rng.choice(120, n, replace=False)
    if U.zeros(S): hits += 1
print('C2 random subsets with an exact zero:', hits, 'of 3000'); ok &= hits == 0
# C3 wrong mechanism
gs = [s for s in d['sets'] if s.get('galois_self')]
bad = [s for s in gs if not all(k in s['zeros'] for k in range(1, 21, 2))]
print(f'C3 wrong rule "Galois-self => silent in all odd degrees": {len(bad)} counterexamples among {len(gs)} Galois-self sets (must be > 0)')
ok &= len(bad) > 0
print('FINAL ok' if ok else 'FINAL FAIL')
