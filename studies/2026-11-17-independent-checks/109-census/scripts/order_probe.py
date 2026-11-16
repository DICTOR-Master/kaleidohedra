"""Probe: which point ordering does the census JSON use? (No census code is read; we test
natural orderings of the 600-cell against the stored zero lists with our own tone routine.)"""
import json, sys, os, itertools
import numpy as np
from core import *
from universes import build_2I

CEN = sys.argv[1]
d = json.load(open(os.path.join(CEN, 'census-U600.json')))
D, U, mul, conj = build_2I()
cand = {}
cand['sorted exact (a,b) pairs'] = list(range(120))
cand['sorted floats'] = sorted(range(120), key=lambda i: tuple(U[i]))
cand['sorted floats desc'] = sorted(range(120), key=lambda i: tuple(-U[i]))
cand['sorted exact (b,a)'] = sorted(range(120), key=lambda i: tuple((c[1], c[0]) for c in D[i]))
cand['sorted exact sqrt5 basis'] = sorted(range(120), key=lambda i: tuple((Fr(2*c[0] + c[1], 2), Fr(c[1], 2)) for c in D[i]))
from fractions import Fraction as Fr
cand['sorted exact sqrt5 basis'] = sorted(range(120), key=lambda i: tuple((Fr(2*c[0] + c[1], 2), Fr(c[1], 2)) for c in D[i]))
codes, cosv = exact_gram_codes(D)
E = ToneEngine(codes, cosv, 'S3')
sets = d['sets']
# cosine list order as a fingerprint: first appearance scanning the Gram row by row
for name, order in cand.items():
    o = np.array(order)
    seen = []
    for i in range(120):
        for j in range(120):
            c = cosv[codes[o[i], o[j]]]
            if c not in seen: seen.append(c)
    fp = [qfloat(c) for c in seen]
    good = sum(1 for s in sets[:200] if E.zeros(o[s['rep']]) == s['zeros'])
    print(f'{name:28s} zeros match on first 200 sets: {good}   first-appearance cosines: {[round(x,3) for x in fp]}')
print('census cosine list:', d['cosines'])
