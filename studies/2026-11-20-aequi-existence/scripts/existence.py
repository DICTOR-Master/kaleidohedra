# Exact existence of a fair die by Alexandrov's condition, for orbit sets of up to 122 face directions
# (study 2026-11-20-aequi-existence). Alexandrov's condition (A. D. Aleksandrov 1942, as stated by J. Bertrand,
# arXiv:1505.04821, Theorem 1.2, and V. Oliker, arXiv:math/0701398, Theorems 1, 4, 6), in the paper's Proposition 2:
# it fails iff some set A of the N directions lying in an open hemisphere has g(A) = 2π(2|A| − N)/N − L(A) ≥ 0,
# L(A) the perimeter of its spherical convex hull. The exhaustive search over subsets (study 2026-11-20-aequi-alexandrov,
# alex.py) is impossible for N up to 122; this script certifies g(A) < 0 for every A by two necessary conditions:
#
#   (H) |A| ≤ M, M = the largest number of the directions in one open hemisphere (computed exactly, below);
#   (D) L(A) ≥ 2 diam(A): if p, q in A realise the diameter D = d(p, q) (< π, as A is in an open hemisphere), the
#       great circle through p and q meets the hull in an arc containing p and q, whose two ends split the boundary
#       into two paths each at least as long as the arc, so L ≥ 2D. And A lies in the lens S(p, q) = {x : d(x, p) ≤ D,
#       d(x, q) ≤ D}.
# So g(A) ≥ 0 forces a pair p, q with 2D ≤ 2π(2k − N)/N for some k with N/2 < k ≤ min(|S(p, q)|, M). A pair is
# excluded when D > π(2 kmax − N)/N, kmax = min(|S(p, q)|, M) (or kmax ≤ N/2); refinement (R): kmax = min(|S(p, q)|,
# M(S(p, q))), the largest number of directions of the lens in one open hemisphere. If every pair is excluded the
# condition holds and the fair die exists (Theorem A). If M ≤ N/2, (H) alone suffices (L ≥ 0, and g = 0 would need
# |A| = N/2 and L = 0, i.e. N = 2).
#
# M exactly: the count f(v) = #{x : v·x > 0} is lower semicontinuous in v, so its maximum is taken on an open cell of
# the arrangement of the great circles x^⊥; every such cell has a vertex w = ±(x_i × x_j)/|x_i × x_j| in its closure,
# and near w the cell is {w + εu} with u in an open sector of w^⊥, where f = #{w·x > 0} + #{x ∈ w^⊥ : u·x > 0}.
# So M = max over vertices w of #{w·x > 0} + h(w), h(w) the most points of the circle w^⊥ in one open half-circle.
#
# Arithmetic: the directions are built in 50-digit arithmetic from the exact frame coordinates (0, ±1, ±φ, ±1/φ) and
# rounded once to doubles (error ≤ 1.2e-16 per coordinate), so every dot product is within 1e-14 of its exact value.
# Lens membership is tested inclusively with tolerance 1e-9 (only enlarges S: conservative). A pair counts as excluded
# only with margin cos(π(2kmax − N)/N) − p·q > 1e-9. Signs w·x are classified zero below 1e-12 and nonzero above 1e-9
# (the run asserts nothing falls between). Every set is also checked against the study's float directions.
#
# usage: existence.py STUDIES_DIR sets.jsonl out.jsonl NPROC [time_limit_s] [kinds,comma,separated]
import json, sys, os, time, itertools, importlib.util, numpy as np, mpmath as mp
mp.mp.dps = 50
S_DIR = sys.argv[1]
spec = importlib.util.spec_from_file_location('g122', S_DIR + '/2026-11-20-aequi-two-placements/scripts/groups.py')
g122 = importlib.util.module_from_spec(spec); spec.loader.exec_module(g122)
DIRS, DFAM = g122.DIRS, list(g122.DFAM)
PHI = (1 + mp.sqrt(5)) / 2
RAW = {'C6': (1, 0, 0), 'O8': (1, 1, 1), 'RD12': (1, 1, 0), 'D12': (0, PHI, 1), 'I12': (0, 1 / PHI, PHI),
       'RT24': (1, PHI, 1 / PHI), 'D12p': (0, 1, PHI), 'I12p': (0, PHI, 1 / PHI), 'RT24p': (PHI, 1, 1 / PHI)}
MPD = [None] * len(DIRS)
for f, t in RAW.items():
    for s in itertools.product((1, -1), repeat=3):
        q = [a * b for a, b in zip(s, t)]
        for k in range(3):
            v = q[k:] + q[:k]; n = mp.sqrt(sum(x * x for x in v)); v = [x / n for x in v]
            fv = np.array([float(x) for x in v])
            i = int(np.argmin(np.abs(DIRS - fv).max(1)))
            if np.abs(DIRS[i] - fv).max() < 1e-12 and DFAM[i] == f: MPD[i] = v
assert all(v is not None for v in MPD)
XEX = np.array([[float(x) for x in v] for v in MPD])          # exact values rounded once
STUDY_DIFF = float(np.abs(XEX - DIRS).max())
TZ, TNZ, TL, TM = 1e-12, 1e-9, 1e-9, 1e-9

def max_open_hemi(Y, stats):
    """largest number of rows of Y (unit vectors) in one open hemisphere, exactly (see header)."""
    k = len(Y)
    if k <= 1: return k
    W = []
    for i, j in itertools.combinations(range(k), 2):
        c = np.cross(Y[i], Y[j]); n = np.linalg.norm(c)
        if n > 1e-6: W.append(c / n); W.append(-c / n); stats['min_cross'] = min(stats.get('min_cross', 9.0), float(n))
        elif n > 1e-12: raise RuntimeError('near-parallel directions')   # only x and −x may be skipped
    if not W: return 1   # all rows on one line: x and −x (distinct), no open hemisphere holds both
    W = np.array(W); D = W @ Y.T; A = np.abs(D)
    mid = (A >= TZ) & (A <= TNZ)
    if mid.any(): raise RuntimeError('sign classification ambiguous')
    z = A < TZ
    stats['zero_max'] = max(stats.get('zero_max', 0.0), float(A[z].max()) if z.any() else 0.0)
    stats['nonzero_min'] = min(stats.get('nonzero_min', 9.0), float(A[~z].min()) if (~z).any() else 9.0)
    pos = (D >= TZ).sum(1); best = 0
    order = np.argsort(-(pos + z.sum(1)))
    for r in order:
        if pos[r] + z[r].sum() <= best: break
        w = W[r]; C = Y[z[r]]
        e1 = np.cross(w, [1, 0, 0] if abs(w[0]) < .9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(w, e1)
        th = np.arctan2(C @ e2, C @ e1)
        cand = np.concatenate([th + np.pi / 2 + 1e-6, th + np.pi / 2 - 1e-6, th - np.pi / 2 + 1e-6, th - np.pi / 2 - 1e-6])
        cs = np.cos(th[None, :] - cand[:, None])
        stats['semicircle_min'] = min(stats.get('semicircle_min', 9.0), float(np.abs(cs).min()))
        h = int((cs > 0).sum(1).max())
        best = max(best, int(pos[r]) + h)
    return best

def work(row):
    t0 = time.time(); N = row['N']; idx = row['dirs']
    X = XEX[idx]; stats = {}
    M = max_open_hemi(X, stats)
    out = dict(kind=row['kind'], group=row['group'], name=row['name'], label=row['label'], N=N, M=M)
    for k in ('alex_g', 'alex_verdict'):
        if k in row: out[k] = row[k]
    if M <= N / 2:
        out.update(verdict='holds', bound='H (M <= N/2)', pairs=0, refined=0, undecided_pairs=[], min_margin=None)
    else:
        G = X @ X.T
        undec = []; refined = 0; min_margin = 9.0; worst = None; npairs = 0
        for p in range(N):
            q = np.arange(p + 1, N); c = G[p, q]
            q = q[c > -1 + 1e-9]; c = G[p, q]        # an opposite pair is never in one open hemisphere
            npairs += len(q)
            Sm = (G[p][None, :] >= c[:, None] - TL) & (G[q, :] >= c[:, None] - TL)
            s = Sm.sum(1); kmax = np.minimum(s, M)
            thr = np.cos(np.pi * np.clip(2 * kmax - N, 0, N) / N)
            marg = thr - c
            excl = (kmax <= N / 2) | (marg > TM)
            for t in np.nonzero(~excl)[0]:
                # refinement (R): the lens's own open-hemisphere count
                refined += 1
                k2 = min(int(s[t]), max_open_hemi(X[Sm[t]], stats))
                m2 = np.cos(np.pi * min(max(2 * k2 - N, 0), N) / N) - c[t]
                if k2 <= N / 2 or m2 > TM:
                    marg[t] = m2 if k2 > N / 2 else 9.0
                    continue
                undec.append(dict(p=idx[p], q=idx[int(q[t])], D_deg=float(np.degrees(np.arccos(np.clip(c[t], -1, 1)))),
                                  lens=int(s[t]), kmax=k2, margin=float(m2)))
            live = (kmax > N / 2)
            if live.any():
                mm = marg[live].min()
                if mm < min_margin: min_margin = float(mm); worst = dict(p=idx[p], q=idx[int(q[live][np.argmin(marg[live])])])
        out.update(verdict='holds' if not undec else 'undecided', bound='H + D' + (' + R' if refined else ''),
                   pairs=npairs, refined=refined, undecided_pairs=undec[:20], n_undecided_pairs=len(undec),
                   min_margin=min_margin if min_margin < 9 else None, worst_pair=worst)
    out['stats'] = stats; out['secs'] = round(time.time() - t0, 2)
    return out

if __name__ == '__main__':
    inp, outp, npr = sys.argv[2], sys.argv[3], int(sys.argv[4]); tl = float(sys.argv[5]) if len(sys.argv) > 5 else 270
    kinds = sys.argv[6].split(',') if len(sys.argv) > 6 else None
    rows = [json.loads(L) for L in open(inp)]
    if kinds: rows = [r for r in rows if r['kind'] in kinds]
    key = lambda r: (r['kind'], r['name'])
    done = set()
    if os.path.exists(outp):
        for L in open(outp):
            try: done.add(key(json.loads(L)))
            except Exception: pass
    todo = sorted([r for r in rows if key(r) not in done], key=lambda r: -r['N'])
    print('directions: exact vs study floats, max difference %.2e' % STUDY_DIFF, flush=True)
    assert STUDY_DIFF < 1e-14
    print('sets', len(rows), 'done', len(done), 'to do', len(todo), flush=True)
    from multiprocessing import Pool
    t0 = time.time(); n = 0
    with Pool(npr) as pool, open(outp, 'a') as fo:
        it = pool.imap_unordered(work, todo)
        while True:
            left = tl - (time.time() - t0)
            if left <= 0: print('TIME: stopping, rerun to continue', flush=True); pool.terminate(); break
            try: r = it.next(timeout=left)
            except StopIteration: break
            except Exception as e:
                if type(e).__name__ == 'TimeoutError': print('TIME: stopping, rerun to continue', flush=True); pool.terminate(); break
                raise
            fo.write(json.dumps(r) + '\n'); fo.flush(); n += 1
    print('wrote', n, 'in', round(time.time() - t0, 1), 's', flush=True)
    print('FINAL ok' if n + len(done) == len(rows) else 'FINAL PARTIAL: rerun to continue')
