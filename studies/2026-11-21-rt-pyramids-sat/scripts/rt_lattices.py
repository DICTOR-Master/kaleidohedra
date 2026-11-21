"""period lattices for the RT search: Lambda spanned by three module vectors of 6D norm^2 <= NMAX2 (module = n in Z^6, all n_i of one parity),
with N = vol(Lambda)/vol(RT pyramid) a positive integer <= NMAXT. Classed up to change of basis (Hermite normal form) and the 120 icosahedral
symmetries (signed permutations of the six 5-fold vectors). Writes data/rt_lattices.json"""
import itertools, json, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from geom import *
NMAX2 = int(sys.argv[1]) if len(sys.argv) > 1 else 8; NMAXT = int(sys.argv[2]) if len(sys.argv) > 2 else 24
E = ico_basis(); G = ico_group_signed_perms(E)
vecs = [v for v in itertools.product(range(-3, 4), repeat=6) if len({x % 2 for x in v}) == 1 and 0 < sum(x*x for x in v) <= NMAX2]
vecs = [v for v in vecs if next(x for x in v if x != 0) > 0]          # one of +-v
V = np.array(vecs, dtype=np.int64); X = to3(V, E); print('vectors', len(V), flush=True)
VOL6 = np.array([32, 64]); 
def hnf(M):
    A = [list(map(int, r)) for r in M]; rows, cols = len(A), len(A[0]); r = 0
    for c in range(cols):
        if r == rows: break
        while True:
            nz = [i for i in range(r, rows) if A[i][c] != 0]
            if not nz: break
            p = min(nz, key=lambda i: abs(A[i][c])); A[r], A[p] = A[p], A[r]
            if A[r][c] < 0: A[r] = [-x for x in A[r]]
            done = True
            for i in range(r + 1, rows):
                q = A[i][c] // A[r][c]; A[i] = [x - q*y for x, y in zip(A[i], A[r])]
                if A[i][c] != 0: done = False
            if done: break
        if any(A[i][c] for i in range(r, rows)) or A[r][c]:
            for i in range(r):
                q = A[i][c] // A[r][c]; A[i] = [x - q*y for x, y in zip(A[i], A[r])]
            r += 1
    return tuple(tuple(x) for x in A)
def act(g, M):
    perm, sg = g; out = np.zeros_like(M)
    for l in range(6): out[:, perm[l]] = sg[l]*M[:, l]
    return out
found = {}
n = len(V); cnt = 0
for i in range(n):
    for j in range(i + 1, n):
        cij = zcross(X[i], X[j])
        d = zdot(cij[None], X[j + 1:])                       # dets with all k > j
        for kk in np.where(np.any(d != 0, axis=1))[0]:
            k = j + 1 + kk; dd = d[kk] if zsign(d[kk]) > 0 else -d[kk]
            r = (zf(6*dd))/zf(VOL6); N = int(round(r))
            if N < 1 or N > NMAXT or not np.array_equal(VOL6*N, 6*dd): continue
            M = V[[i, j, k]]
            key = min(hnf(act(g, M)) for g in G)
            if key not in found: found[key] = N
    if i % 20 == 0: print(f'PROGRESS {i/n:.3f} lattices so far {len(found)}', flush=True)
out = [{'N': N, 'basis': [list(r) for r in key], 'norms2': sorted(sum(x*x for x in r) for r in key)} for key, N in sorted(found.items(), key=lambda kv: (kv[1], kv[0]))]
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'rt_lattices_n{NMAX2}_N{NMAXT}.json'), 'w'), indent=0)
from collections import Counter; print('lattices by N:', dict(Counter(o['N'] for o in out)))
