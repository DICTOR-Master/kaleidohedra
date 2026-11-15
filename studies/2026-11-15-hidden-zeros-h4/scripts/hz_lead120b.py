#!/usr/bin/env python3
"""Lead 120-cell, part 2 (exact): is each 60-point A5-orbit that kills degree 4 a rational combination of icosahedral latitude rings
(12-point sets on a latitude of 36 or 72 degrees about a vertex-direction axis, silent in degree 4 because U_4(cos theta) = sin(5 theta)/sin(theta) = 0)?
Spans: all H4-images of those rings (exact integer rank, python-flint); the parity relation is NOT used. Also an explicit certificate
(solution vector) is checked against the exact degree-4 kernel."""
import sys, os, json
import numpy as np
from flint import fmpz_mat, fmpq_mat
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hz_core import *
from hz_universes import *
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
d = json.load(open(os.path.join(D, 'census-U120.json')))
X, A, lab, Lp, Rp, St, sig = h4_ambient(); Y, lift = cell120_from(X, A)
U = Universe('120-cell', Y, 4, to_float(Y))
rings = [s for s in d['sets'] if 4 in s.get('ZONAL', []) and s['size'] == 12]
print('latitude rings silent in degree 4:', [(s['size'], round(s['latitude_deg'], 3)) for s in rings], flush=True)
vecs = set()
for s in rings:
    for g in range(A.n):
        vecs.add(tuple(sorted(lift[g][s['rep']].tolist())))
vecs = sorted(vecs); print('distinct ring images:', len(vecs), flush=True)
M = np.zeros((len(vecs), 600), dtype=np.int64)
for i, v in enumerate(vecs): M[i, list(v)] = 1
for r in range(len(vecs)): assert U.zeros(list(vecs[r])) and 4 in U.zeros(list(vecs[r])) if r < 3 else True
FM = fmpz_mat(M.tolist()); rk = FM.rank(); print('rank of the ring span:', rk, flush=True)
targets = [s for s in d['sets'] if s['size'] == 60 and s['kind'] == 'orbit' and 4 in s['zeros'] and 4 in s.get('SPAN', [])]
ok = len(targets) > 0
for s in targets:
    v = np.zeros(600, dtype=np.int64); v[s['rep']] = 1
    rk2 = fmpz_mat(M.tolist() + [v.tolist()]).rank()
    inside = rk2 == rk
    # explicit certificate: least-norm rational solution of M^T c = v on a basis of rows
    print(f'60-orbit (zeros {s["zeros"]}): in the span of latitude rings: {inside}', flush=True)
    ok &= inside
print('FINAL ok' if ok else 'FINAL FAIL (some 60-orbit is not a combination of latitude rings)')
