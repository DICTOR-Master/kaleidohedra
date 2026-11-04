#!/usr/bin/env python3
"""Census of Dehn-zero truncated tetrahedra (Concordance 6.1, next gap; DICTO 4 Nov "combinatory approach").
T(n) minus corner tetrahedra of sizes k1..k4: Dehn = 6(n - Σk)⊗α, and (tetrahedra - 2·octahedra) = n - Σk (second differences of C(·,3)), so Dehn zero <=> octet 2:1 ratio
<=> Σk = n. Every such piece is a union of octet cells. For each multiset k (k_i <= n-1, k_i + k_j <= n), n <= NMAX:
 (a) local patch test round one piece (exact cover of a ball of cells, cell-aligned): if it fails, no cell-aligned tiling;
 (b) periodic exact cover on tori fcc/L of index m·(cells/3), m = 1..MMAX (all HNF sublattices), stop at the first found.
Calibration: (1,1,1,1) at n = 4 must tile (known, Damasceno–Engel–Glotzer 2012)."""
import sys, itertools, json, time, numpy as np
A = sys.argv; SAT = '--sat' in A; A = [a for a in A if a != '--sat']; sys.argv, NMAX, MMAX, NCAP = A[:1], int(A[1]), int(A[2]), int(A[3])
ONLY = json.loads(A[4]) if len(A) > 4 else None; OUT = A[5] if len(A) > 5 else 'data/census.json'
exec(open('scripts/tile_octet.py').read().split("if __name__")[0])
V = np.array([(0,0,0),(1,1,0),(1,0,1),(0,1,1)], float)
def piece(n, k):
    Vn = V*n; Mi = np.linalg.inv(np.vstack([Vn.T, np.ones(4)]))
    out = []
    for kind, p in cells(n + 2):
        lam = Mi @ np.array([*p, 1.0])
        if np.any(lam <= 1e-9): continue
        if any(lam[i] > 1 - k[i]/n + 1e-9 for i in range(4)): continue
        out.append((kind, p))
    return out
def orients_of(cl):
    kinds = [c[0] for c in cl]; pts = np.array([c[1] for c in cl]); seen = set(); res = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3))
            for i in range(3): M[i, perm[i]] = sg[i]
            Q = pts @ M.T
            key_ = frozenset((kd, tuple(np.round(q - Q.min(0), 6))) for kd, q in zip(kinds, Q))
            if key_ not in seen: seen.add(key_); res.append((kinds, Q))
    return res
def patch(orients, R):
    kinds, P0 = orients[0]; cen = P0.mean(0)
    def ck(kd, p): return (kd, tuple(np.round(np.asarray(p)*2).astype(int)))
    ball = {ck(kd, p) for kd, p in cells(int(R + abs(cen).max()) + 3) if np.linalg.norm(np.array(p) - cen) <= R}
    rad = max(np.linalg.norm(P0 - cen, axis=1)) + 1
    rows = set(); span = int(R + rad) + 3
    for kd, Q in orients:
        qc = Q.mean(0)
        for v in itertools.product(range(-span, span + 1), repeat=3):
            s = B @ np.array(v, float); c = qc + s
            if np.linalg.norm(c - cen) > R + rad: continue
            r = tuple(sorted(ck(a, q + s) for a, q in zip(kd, Q)))
            if any(x in ball for x in r): rows.add(r)
    rows = list(rows); base = tuple(sorted(ck(a, q) for a, q in zip(kinds, P0)))
    allc = sorted({c for r in rows for c in r}); idx = {c: i for i, c in enumerate(allc)}
    rws = [tuple(idx[c] for c in r) for r in rows]; prim = {idx[c] for c in ball}
    if SAT:
        from pysat.solvers import Cadical153
        from pysat.card import CardEnc, EncType
        cov = {}
        for i, r in enumerate(rws):
            for j in r: cov.setdefault(j, []).append(i + 1)
        cnf = []; top = len(rws)
        for j, lits in cov.items():
            am = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, am.nv); cnf += am.clauses
            if j in prim: cnf.append(lits)
        b = rows.index(base) + 1; cnf.append([b])
        t0 = time.time()
        with Cadical153(bootstrap_with=cnf) as S:
            ok = S.solve()
        return ok, round(time.time() - t0, 1), len(ball)
    X = {j: set() for j in range(len(allc))}
    for i, r in enumerate(rws):
        for j in r: X[j].add(i)
    def sel(i):
        cols = []
        for j in rws[i]:
            for kk in X[j]:
                for l in rws[kk]:
                    if l != j: X[l].discard(kk)
            cols.append(X.pop(j))
        return cols
    def desel(i, cols):
        for j in reversed(rws[i]):
            X[j] = cols.pop()
            for kk in X[j]:
                for l in rws[kk]:
                    if l != j: X[l].add(kk)
    nodes = [0]; t0 = time.time()
    def rec():
        nodes[0] += 1
        if time.time() - t0 > 900: raise TimeoutError
        Pm = [j for j in X if j in prim]
        if not Pm: return True
        j = min(Pm, key=lambda c: (len(X[c]), np.linalg.norm(np.array(allc[c][1])/2 - cen)))
        for i in list(X[j]):
            cols = sel(i)
            if rec(): return True
            desel(i, cols)
        return False
    sel(rows.index(base))
    try: ok = rec()
    except TimeoutError: ok = 'timeout'
    return ok, nodes[0], len(ball)
res = []
JOBS = [(n, tuple(k)) for n, k in ONLY] if ONLY else [(n, k) for n in range(2, NMAX + 1) for k in sorted({tuple(sorted(c, reverse=True)) for c in itertools.product(range(n), repeat=4) if sum(c) == n})]
for n, k in JOBS:
    if True:
        if any(k[i] + k[j] > n for i, j in itertools.combinations(range(4), 2)): continue
        cl = piece(n, k); kinds = [c[0] for c in cl]; nO, nT = kinds.count('O'), kinds.count('T')
        assert nT == 2*nO, (n, k, nT, nO)
        ors = orients_of(cl); R = 1.6*n + 4
        ok, nodes, nb = patch(ors, R)
        rec_ = {'n': n, 'k': k, 'cells': len(cl), 'O': nO, 'T': nT, 'orientations': len(ors), 'patch_R': R, 'patch': ok, 'patch_nodes': nodes}
        if ok is True:
            found = None; per = len(cl)//3
            for m in range(1, MMAX + 1):
                N = m*per
                if N > NCAP: rec_['periodic_note'] = f'stopped: N > {NCAP}'; break
                cnt = 0
                for H in hnf(N):
                    cnt += 1; s = try_torus(ors, H)
                    if s and s != 'bad torus': found = (N, H.tolist()); break
                rec_[f'tori_N{N}'] = cnt
                if found: break
            rec_['periodic'] = found
        print(json.dumps(rec_), flush=True); res.append(rec_)
json.dump(res, open(OUT, 'w'), indent=1)
