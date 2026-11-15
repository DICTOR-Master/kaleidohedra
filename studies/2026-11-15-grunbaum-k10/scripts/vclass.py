#!/usr/bin/env python3
"""Necessary condition for a FACE-TO-FACE lattice tiling in class C(n) (n zone directions among the six 5-fold axes, one zone per
direction, every two zones crossing exactly twice, so F = n(n-1) faces and every zone has k = 2(n-1) faces).
Lemma (walking along zones; README section 'The face-pair lemma'): the vector lambda_ab in Z^n from one (a,b) face to the other has
coordinates a and b equal to 0 and every other coordinate in {0, +-1, +-2}; in a face-to-face lattice tiling all 15 (or 10) of them lie
in one rank-3 sublattice L of Z^n. Write V = L (x) Q = row space of a 3 x n matrix M with columns m_i, Plucker coordinates
p_ijk = det(m_i, m_j, m_k). If m_a, m_b are independent, the only vectors of V vanishing at a and b are multiples of (p_abc)_c, so the
nonzero values |p_abc| (c not a, b) must all be t or 2t for one t. Some p_T != 0 (rank 3); relabel T = {1,2,3} (the condition is
symmetric in the labels), M = [I | X]; then the pairs {1,2},{1,3},{2,3} force every entry of X into {0, +-1/2, +-1, +-2}. We enumerate
all 7^(3(n-3)) such X (scaled by 2 to integers) and keep the V where every pair passes (pairs with m_a || m_b are kept unconditionally).
Output: survivors with their scaled lambda vectors. Prints PROGRESS and FINAL."""
import sys, json, itertools, time
import numpy as np
t0 = time.time()
OUT = sys.argv[1]
S = np.array([0, 1, -1, 2, -2, 4, -4], dtype=np.int64)       # 2 * {0, 1/2, -1/2, 1, -1, 2, -2}
def minors(Mbatch, n):
    T = list(itertools.combinations(range(n), 3)); P = {}
    for t in T:
        A = Mbatch[:, :, list(t)]
        P[t] = (A[:, 0, 0]*(A[:, 1, 1]*A[:, 2, 2] - A[:, 1, 2]*A[:, 2, 1]) - A[:, 0, 1]*(A[:, 1, 0]*A[:, 2, 2] - A[:, 1, 2]*A[:, 2, 0])
                + A[:, 0, 2]*(A[:, 1, 0]*A[:, 2, 1] - A[:, 1, 1]*A[:, 2, 0]))
    return P
def key(t): return tuple(sorted(t))
def run(n):
    m = 3*(n - 3); total = 7**m; chunk = 7**min(m, 7); keep = []; ndeg = 0
    pairs = list(itertools.combinations(range(n), 2))
    for start in range(0, total, chunk):
        idx = np.arange(start, min(total, start + chunk), dtype=np.int64)
        digits = np.stack([(idx // 7**j) % 7 for j in range(m)], axis=1)
        X = S[digits].reshape(-1, 3, n - 3)
        M = np.concatenate([np.broadcast_to(2*np.eye(3, dtype=np.int64), (len(idx), 3, 3)), X], axis=2)
        P = minors(M, n); ok = np.ones(len(idx), bool); deg = np.zeros(len(idx), bool)
        for a, b in pairs:
            vals = np.stack([np.abs(P[key((a, b, c))]) for c in range(n) if c not in (a, b)], axis=1)
            nz = vals > 0; anynz = nz.any(1); deg |= ~anynz
            big = np.where(nz, vals, 0).max(1); small = np.where(nz, vals, np.iinfo(np.int64).max).min(1)
            good = np.all(~nz | (vals == small[:, None]) | (vals == 2*small[:, None]), axis=1)
            ok &= good | ~anynz
        ndeg += int((ok & deg).sum())
        for i in np.nonzero(ok)[0]:
            Mi = M[i]; lam = {}
            Pi = {t: int(P[t][i]) for t in P}
            for a, b in pairs:
                v = [0]*n
                for c in range(n):
                    if c not in (a, b): v[c] = Pi[key((a, b, c))]*(1 if (a < b < c or b < c < a or c < a < b) else 1)
                # sign of p_abc for the ordered triple (a,b,c)
                for c in range(n):
                    if c in (a, b): continue
                    srt = sorted((a, b, c)); perm = [srt.index(x) for x in (a, b, c)]
                    sg = 1 if perm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]) else -1
                    v[c] = sg*Pi[key((a, b, c))]
                nzv = [abs(x) for x in v if x]
                if nzv:
                    t = min(nzv); v = [x//t if x % t == 0 else x/t for x in v]
                lam[f'{a}{b}'] = v
            keep.append({'X_times_2': Mi[:, 3:].tolist(), 'degenerate_pair': bool(deg[i]), 'lambda_scaled': lam})
        print(f'PROGRESS {min(total, start+chunk)/total:.4f} n={n} survivors={len(keep)} t={time.time()-t0:.0f}s', flush=True)
    return {'n': n, 'enumerated': total, 'survivors': len(keep), 'with_degenerate_pair': ndeg, 'list': keep[:2000]}
res = {}
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for n in range(4, NMAX + 1):
    res[n] = run(n); print(f'n={n}: enumerated {res[n]["enumerated"]}, survivors {res[n]["survivors"]} (with a degenerate pair {res[n]["with_degenerate_pair"]})', flush=True)
json.dump(res, open(OUT, 'w'), indent=0)
print('RESULT survivors', {k: v['survivors'] for k, v in res.items()}, f'| {time.time()-t0:.0f}s')
print('FINAL ok' if res[5]['survivors'] > 0 and res[4]['survivors'] > 0 else 'FINAL FAIL: positive controls (n=4 Bilinski, n=5 D1/D2) need survivors')
