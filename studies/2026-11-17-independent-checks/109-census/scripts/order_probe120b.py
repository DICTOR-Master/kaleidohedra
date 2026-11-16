"""Probe 2: hash-order enumerations of the 600 cells (Python set iteration orders), corners named
by the census 600-cell ordering (lexicographic in the sqrt5 basis)."""
import sys, os, json, itertools
from fractions import Fraction as Fr
import numpy as np
from core import *
from worlds import world
CEN = sys.argv[1]
sets = json.load(open(os.path.join(CEN, 'census-U120.json')))['sets']
W = world('120'); W6 = world('600')
def s5(x):
    a, b = Fr(x[0]), Fr(x[1]); return (a + b / 2, b / 2)
order600 = sorted(range(120), key=lambda i: tuple(s5(c) for c in W6.exact[i]))
rank = np.empty(120, int); rank[order600] = np.arange(120)
cellpos = {tuple(sorted(int(rank[x]) for x in c)): i for i, c in enumerate(W.cells)}
lex = sorted(cellpos)
cands = {
  'lex tuples': lex,
  'set of tuples (lex insertion)': list(set(lex)),
  'set of frozensets (lex insertion)': [tuple(sorted(f)) for f in set(frozenset(t) for t in lex)],
  'dict of frozensets': [tuple(sorted(f)) for f in dict.fromkeys(frozenset(t) for t in lex)],
}
# cells grouped by the facet-centre direction: sort by corner-sum in census coordinates is a sort (ruled out)
odd2 = [s['rep'] for s in sets if s['size'] == 2 and all(k in s['zeros'] for k in range(1, 21, 2))]
for nm, lst in cands.items():
    o = np.array([cellpos[t] for t in lst])
    good = sum(1 for s in sets[:400] if W.T.zeros(o[s['rep']]) == s['zeros'])
    print(f'{good:4d}/400  {nm}', flush=True)
rp = np.random.default_rng(1).permutation(600)
print(f'{sum(1 for s in sets[:400] if W.T.zeros(rp[s["rep"]]) == s["zeros"]):4d}/400  random permutation baseline')
