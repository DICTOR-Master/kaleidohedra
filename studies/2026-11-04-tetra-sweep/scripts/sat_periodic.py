#!/usr/bin/env python3
"""Periodic test by SAT: for each piece (n, k) and m = 1..MMAX, every HNF torus of index N = m·cells/3; exact cover (each cell exactly once) by CaDiCaL.
Stops at the first torus found. A piece whose patches close but with no torus up to MMAX is an APERIODIC-CLUE candidate (clue checklist, open-work 11-04)."""
import sys, json, time, itertools, numpy as np
ARGS = list(sys.argv)
sys.argv = [ARGS[0], '0', '0', '0', '[]']; exec(open('scripts/census.py').read().split("\nres = []\n")[0])
MMAX = int(ARGS[1]); JOBS = json.loads(ARGS[2]); OUT = ARGS[3]
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def torus_sat(orients, H):
    L = B @ H; Li = np.linalg.inv(L)
    def key(kind, x): z = Li @ np.asarray(x, float); return (kind, tuple(np.round(z - np.floor(z + 1e-9), 6) % 1))
    reps = [B @ np.array(v, float) for v in itertools.product(*[range(int(H[k, k])) for k in range(3)])]
    base = [('O', (1, 0, 0)), ('T', (.5, .5, .5)), ('T', (-.5, -.5, -.5))]
    idx = {c: i for i, c in enumerate(sorted({key(k, np.array(p) + r) for r in reps for k, p in base}))}
    rows = set()
    for kinds, P in orients:
        for r in reps:
            ks = [idx.get(key(k, p + r)) for k, p in zip(kinds, P)]
            if None in ks or len(set(ks)) != len(ks): continue
            rows.add(tuple(sorted(ks)))
    rows = sorted(rows); cov = {}
    for i, r in enumerate(rows):
        for j in r: cov.setdefault(j, []).append(i + 1)
    if len(cov) < len(idx): return False
    cnf = []; top = len(rows)
    for lits in cov.values():
        e = CardEnc.equals(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, e.nv); cnf += e.clauses
    with Cadical153(bootstrap_with=cnf) as S: return S.solve()
res = []
for n, k in JOBS:
    k = tuple(k); cl = piece(n, k); ors = orients_of(cl); per = len(cl)//3; rec = {'n': n, 'k': k, 'orientations': len(ors)}; t0 = time.time(); found = None
    for m in range(1, MMAX + 1):
        N = m*per; cnt = 0
        for H in hnf(N):
            cnt += 1
            if torus_sat(ors, H): found = (N, H.tolist()); break
        rec[f'tori_N{N}'] = cnt
        if found: break
    rec['periodic'] = found; rec['seconds'] = round(time.time() - t0, 1); print(json.dumps(rec), flush=True); res.append(rec)
json.dump(res, open(OUT, 'w'), indent=1)
