# Independent checks of existence.py's results (study 2026-11-20-aequi-existence); they can only expose an error, they
# certify nothing.
#  (1) M by sampling: for 200 000 Fibonacci directions v and for the vertices w = ±(x_i × x_j)/|.| tilted at random by
#      1e-5, count #{x : v·x > 1e-12}; the largest count must not exceed the exact M (and is expected to equal it).
#  (2) Witness hunt: for caps A = the k directions nearest a direction v (v over 3000 Fibonacci directions and every
#      face direction; N/2 < k, A in an open hemisphere), g(A) = 2π(2|A| − N)/N − L(A) with the hull perimeter by the
#      gnomonic chart (as in study 2026-11-20-aequi-alexandrov, alex.py). A certified set must have every g < 0.
# usage: check.py STUDIES_DIR sets.jsonl results.jsonl out.jsonl NPROC
import json, sys, numpy as np, importlib.util
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
spec = importlib.util.spec_from_file_location('ex', __file__.replace('check.py', 'existence.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
XEX = ex.XEX
def fib(M):
    z = 1 - (2 * np.arange(M) + 1) / M; t = np.pi * (3 - 5 ** .5) * np.arange(M)
    return np.c_[np.sqrt(1 - z * z) * np.cos(t), np.sqrt(1 - z * z) * np.sin(t), z]
F200, F3 = fib(200000), fib(3000)
def hemivec(P):
    v = P.sum(0); nv = np.linalg.norm(v)
    if nv > 1e-12 and (P @ (v / nv)).min() > 1e-9: return v / nv
    k = len(P); r = linprog(np.r_[0, 0, 0, -1.0], A_ub=np.hstack([-P, np.ones((k, 1))]), b_ub=np.zeros(k),
                            bounds=[(-1, 1)] * 3 + [(None, 1)])
    if r.status == 0 and -r.fun > 1e-9: v = r.x[:3]; return v / np.linalg.norm(v)
    return None
def perim(P):
    v = hemivec(P)
    if v is None: return None
    e1 = np.cross(v, [1, 0, 0] if abs(v[0]) < .9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(v, e1)
    Q = P / (P @ v)[:, None]; xy = np.c_[Q @ e1, Q @ e2]
    try: cyc = list(ConvexHull(xy).vertices)
    except Exception:
        d = xy - xy.mean(0); w = np.linalg.svd(d)[2][0]; t = d @ w; cyc = [int(np.argmin(t)), int(np.argmax(t))]
    arc = lambda a, b: float(np.arctan2(np.linalg.norm(np.cross(a, b)), a @ b))
    return sum(arc(P[cyc[i]], P[cyc[(i + 1) % len(cyc)]]) for i in range(len(cyc)))
def work(a):
    row, res = a; X = XEX[row['dirs']]; N = len(X); rng = np.random.default_rng(1)
    m1 = int(((F200 @ X.T) > 1e-12).sum(1).max())
    W = []
    for i in range(N):
        for j in range(i + 1, N):
            c = np.cross(X[i], X[j]); n = np.linalg.norm(c)
            if n > 1e-6: W += [c / n, -c / n]
    W = np.array(W); W = W + 1e-5 * rng.standard_normal(W.shape); W /= np.linalg.norm(W, axis=1)[:, None]
    m2 = int(((W @ X.T) > 1e-12).sum(1).max())
    gmax = -np.inf; ntried = 0; seen = set()
    for v in np.vstack([F3, X]):
        d = X @ v; o = np.argsort(-d); npos = int((d > 1e-9).sum())
        for k in range(N // 2 + 1, npos + 1):
            A = tuple(sorted(o[:k]))
            if A in seen: continue
            seen.add(A); L = perim(X[list(A)]); ntried += 1
            if L is not None: gmax = max(gmax, 2 * np.pi * (2 * k - N) / N - L)
    return dict(kind=row['kind'], name=row['name'], N=N, M=res['M'], M_sampled=max(m1, m2),
                M_ok=max(m1, m2) <= res['M'], M_equal=max(m1, m2) == res['M'], caps_tried=ntried,
                g_max_caps=None if gmax == -np.inf else float(gmax), verdict=res['verdict'],
                contradiction=bool(res['verdict'] == 'holds' and gmax >= 0))
if __name__ == '__main__':
    S, sets, results, outp, npr = sys.argv[1:6]
    rows = {(r['kind'], r['name']): r for r in map(json.loads, open(sets))}
    res = [json.loads(L) for L in open(results)]
    from multiprocessing import Pool
    with Pool(int(npr)) as pool, open(outp, 'w') as fo:
        out = pool.map(work, [(rows[(r['kind'], r['name'])], r) for r in res], chunksize=4)
        for o in out: fo.write(json.dumps(o) + '\n')
    bad = [o for o in out if not o['M_ok'] or o['contradiction']]
    print('sets', len(out), '| M sampled = exact', sum(o['M_equal'] for o in out), '| M sampled > exact', sum(not o['M_ok'] for o in out),
          '| certified with a cap g >= 0', sum(o['contradiction'] for o in out))
    print('FINAL ok' if not bad else 'FINAL FAIL')
