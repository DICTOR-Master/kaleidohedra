# Alexandrov's condition for a fair die with given face normals, and a die-finder without a search box.
#
# A fair die with unit face normals n_1..n_N (each face subtends 4π/N from the origin) is Alexandrov's problem for the
# polar body with integral Gauss curvature μ = (1/N) Σ δ_{n_k} (A. D. Aleksandrov 1942; condition and uniqueness as
# stated in J. Bertrand, arXiv:1505.04821, Theorem 1.2; V. Oliker, arXiv:math/0701398). Condition: for every nonempty
# spherical convex ω ≠ S², μ(ω) < σ(ω_{π/2}), σ the uniform probability on S².
#
# Test used here. For a discrete μ only ω = spherical convex hull of a set A of normals in an open hemisphere matters
# (a convex ω not in an open hemisphere contains two antipodal points, so σ(ω_{π/2}) = 1 > μ(ω), the normals bounding a
# solid). Then σ(ω_{π/2}) = 1 − σ(A*), A* = {y : y·a ≤ 0 for all a in A}, and A* is the polar polygon of hull(A), whose
# area is 2π − L(A), L the perimeter of hull(A) (Girard's formula with the polar angles π − side; for one point L = 0,
# for an arc L = twice its length). So the condition FAILS iff some A in an open hemisphere has
#     g(A) = 2π (2|A| − N)/N − L(A) ≥ 0,
# and only |A| > N/2 can fail. Search: A = the k normals nearest a direction v (caps) for many v, then local moves
# (add, remove, swap one normal), and every subset when N ≤ 18. A witness is re-checked in 50-digit arithmetic from the
# exact frame coordinates (0, ±1, ±φ, ±1/φ).
#
# Die-finder (decides the other way, by construction). With ψ_k = log d_k the face met by the ray u maximises
# (n_k·u) e^{−ψ_k}, so Φ(ψ) = ∫ log max_k (n_k·u) e^{−ψ_k} dσ(u) + Σ_k μ_k ψ_k is convex with gradient
# μ_k − Ω_k/4π (the variational form of Alexandrov's problem; Oliker; Bertrand's optimal-transport dual). Φ is
# minimised over one ψ per orbit on a 200 000-point Fibonacci grid (no box: |ψ| ≤ 25), then polished with the study's
# exact solid angles (Van Oosterom and Strackee's triangle formula, study 2026-11-19-aequi-complete, solve.py) by
# scipy's hybrid Powell method. A die is accepted when every face is within 1e-10 of 4π/N.
#
# usage: alex.py sets.jsonl out.jsonl NPROC [time_limit_s]
import json, sys, os, time, itertools, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-19-aequi-complete', 'scripts'))
from groups import DIRS, DFAM
from solve import face_omegas
from scipy.spatial import ConvexHull
from scipy.optimize import linprog, minimize, root
mp.mp.dps = 50
# exact directions (50 digits), matched to the study's float list
PHI = (1 + mp.sqrt(5)) / 2
RAW = {'C6': (1, 0, 0), 'O8': (1, 1, 1), 'RD12': (1, 1, 0), 'D12': (0, PHI, 1), 'I12': (0, 1 / PHI, PHI), 'RT24': (1, PHI, 1 / PHI)}
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

def arc(a, b): return float(np.arctan2(np.linalg.norm(np.cross(a, b)), a @ b))
def hemivec(P):
    v = P.sum(0); nv = np.linalg.norm(v)
    if nv > 1e-12 and (P @ (v / nv)).min() > 1e-9: return v / nv
    k = len(P); c = np.r_[0, 0, 0, -1.0]
    A = np.hstack([-P, np.ones((k, 1))])
    r = linprog(c, A_ub=A, b_ub=np.zeros(k), bounds=[(-1, 1)] * 3 + [(None, 1)])
    if r.status == 0 and -r.fun > 1e-9: v = r.x[:3]; return v / np.linalg.norm(v)
    return None
def hull_cycle(P):
    """indices of the vertices of the spherical convex hull of P (in an open hemisphere), in cyclic order; None if P is
    not in an open hemisphere."""
    v = hemivec(P)
    if v is None: return None
    if len(P) == 1: return [0]
    e1 = np.cross(v, [1, 0, 0] if abs(v[0]) < .9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(v, e1)
    Q = P / (P @ v)[:, None]; xy = np.c_[Q @ e1, Q @ e2]
    try:
        return list(ConvexHull(xy).vertices)
    except Exception:   # collinear in the gnomonic chart: the hull is an arc; its perimeter counts it twice
        d = xy - xy.mean(0); w = np.linalg.svd(d)[2][0]; t = d @ w
        return [int(np.argmin(t)), int(np.argmax(t))]
def perimeter(P, cyc):
    if len(cyc) == 1: return 0.0
    return sum(arc(P[cyc[i]], P[cyc[(i + 1) % len(cyc)]]) for i in range(len(cyc)))

def witness_search(X):
    N = len(X); kmin = N // 2 + 1; cache = {}
    def g(A):
        A = tuple(sorted(A))
        if A not in cache:
            cyc = hull_cycle(X[list(A)])
            cache[A] = -np.inf if cyc is None else 2 * np.pi * (2 * len(A) - N) / N - perimeter(X[list(A)], cyc)
        return cache[A]
    V = [x for x in X]
    for i, j in itertools.combinations(range(N), 2):
        s = X[i] + X[j]
        if np.linalg.norm(s) > 1e-9: V.append(s / np.linalg.norm(s))
    if N <= 40:
        for i, j, k in itertools.combinations(range(N), 3):
            s = X[i] + X[j] + X[k]
            if np.linalg.norm(s) > 1e-9: V.append(s / np.linalg.norm(s))
    M = 2000; z = 1 - (2 * np.arange(M) + 1) / M; t = np.pi * (3 - 5 ** .5) * np.arange(M)
    V += list(np.c_[np.sqrt(1 - z * z) * np.cos(t), np.sqrt(1 - z * z) * np.sin(t), z])
    for v in V:
        d = X @ v; o = np.argsort(-d); npos = int((d > 1e-9).sum())
        for k in range(kmin, npos + 1): g(o[:k])
    if N <= 18:
        for k in range(kmin, N + 1):
            for A in itertools.combinations(range(N), k): g(A)
    # local moves from the ten best
    best = sorted(cache, key=lambda A: -cache[A])[:10]
    for A in best:
        cur = set(A); improved = True
        while improved:
            improved = False; base = g(cur)
            moves = [cur | {j} for j in range(N) if j not in cur] + [cur - {i} for i in cur if len(cur) > kmin]
            moves += [(cur - {i}) | {j} for i in cur for j in range(N) if j not in cur]
            for B in moves:
                if g(B) > base + 1e-15: cur = set(B); improved = True; break
    A = max(cache, key=lambda A: cache[A])
    return list(A), cache[A], len(cache)

def mp_check(idx, A):
    """50-digit g(A) from exact coordinates, with the hull order of the float computation."""
    X = DIRS[idx]; cyc = hull_cycle(X[A]); N = len(idx)
    P = [MPD[idx[a]] for a in A]
    def marc(a, b):
        c = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
        return mp.atan2(mp.sqrt(sum(x * x for x in c)), sum(x * y for x, y in zip(a, b)))
    arcs = [] if len(cyc) == 1 else [marc(P[cyc[i]], P[cyc[(i + 1) % len(cyc)]]) for i in range(len(cyc))]
    L = mp.mpf(0) if len(cyc) == 1 else sum(arcs)
    # the float hull must be the exact hull: every point of A on the inner side of every hull edge (exactly)
    ok = True
    if len(cyc) >= 3:
        for i in range(len(cyc)):
            a, b = P[cyc[i]], P[cyc[(i + 1) % len(cyc)]]
            nrm = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
            sgn = [sum(x * y for x, y in zip(nrm, p)) for p in P]
            if min(sgn) < -mp.mpf(10) ** -40 and max(sgn) > mp.mpf(10) ** -40: ok = False
    gm = 2 * mp.pi * (2 * len(A) - N) / N - L
    return gm, L, ok, len(cyc), [mp.nstr(a * 180 / mp.pi, 20) for a in arcs]

FIB = None
def die_finder(idx, sizes):
    global FIB
    if FIB is None:
        M = 200000; z = 1 - (2 * np.arange(M) + 1) / M; t = np.pi * (3 - 5 ** .5) * np.arange(M)
        FIB = np.c_[np.sqrt(1 - z * z) * np.cos(t), np.sqrt(1 - z * z) * np.sin(t), z]
    X = DIRS[idx]; N = len(idx); m = len(sizes); orb = np.repeat(np.arange(m), sizes)
    S = FIB @ X.T; logS = np.log(np.where(S > 0, S, 1e-300))
    w = np.array(sizes) / N
    def phi(x):
        psi = np.r_[0.0, x]
        L = logS - psi[orb][None, :]; k = np.argmax(L, 1)
        frac = np.bincount(orb[k], minlength=m) / len(FIB)
        return L[np.arange(len(L)), k].mean() + w @ psi, (w - frac)[1:]
    r = minimize(phi, np.zeros(m - 1), jac=True, method='L-BFGS-B', bounds=[(-25, 25)] * (m - 1),
                 options=dict(maxiter=2000, gtol=1e-9))
    x0 = r.x; T = 4 * np.pi / N; cut = np.cumsum([0] + list(sizes))
    out = dict(grid_x=x0.tolist(), grid_at_bound=bool(np.abs(x0).max() > 24.9))
    def F(x):
        if not np.all(np.isfinite(x)) or np.abs(x).max() > 25: return np.full(m - 1, 10.0)
        try: om = face_omegas(X, np.repeat(np.exp(np.r_[0.0, x]), sizes))
        except Exception: return np.full(m - 1, 10.0)
        return np.array([om[cut[k]:cut[k + 1]].mean() - T for k in range(1, m)])
    found = None
    if not out['grid_at_bound']:
        for xs in [x0, x0 * 1.01, x0 + 0.01]:
            try: rr = root(F, xs, method='hybr', options=dict(xtol=1e-14, maxfev=400 * m))
            except Exception: continue
            if not np.all(np.isfinite(rr.x)) or np.abs(rr.x).max() > 25: continue
            try: om = face_omegas(X, np.repeat(np.exp(np.r_[0.0, rr.x]), sizes))
            except Exception: continue
            res = float(np.abs(om - T).max())
            if res < 1e-10: found = dict(depths=np.exp(np.r_[0.0, rr.x]).tolist(), max_residual=res); break
    out['die'] = found
    return out

def work(row):
    t0 = time.time()
    idx = [j for O in row['orbits'] for j in O]; sizes = [len(O) for O in row['orbits']]
    X = DIRS[idx]
    A, gf, ncand = witness_search(X)
    if not np.isfinite(gf):   # no set of more than N/2 normals lies in an open hemisphere: the condition cannot fail
        A = [0]; gm, L, hull_ok, nh, arcs = -mp.inf, mp.mpf(0), False, 0, []
    else:
        gm, L, hull_ok, nh, arcs = mp_check(idx, A)
    fails = bool(gm >= 0 and hull_ok)
    exhaustive = len(idx) <= 18
    # the condition, from the search (decisive when every subset was tried)
    condition = 'fails' if fails else 'holds' if exhaustive else 'no witness found'
    df = die_finder(idx, sizes)
    holds = df['die'] is not None
    equality = bool(fails and abs(gm) < mp.mpf(10) ** -40)   # g = 0 to 40 digits: Alexandrov's inequality is strict, so this fails
    if fails and not holds: verdict = 'fails'
    elif fails and holds and equality: verdict = 'fails (equality: the die-finder approaches a limit with a face at infinity)'
    elif fails and holds: verdict = 'CONFLICT'
    elif holds: verdict = 'holds'
    else: verdict = 'holds; die not found' if exhaustive else 'undecided'
    box = None
    if holds:
        dd = np.array(df['die']['depths']); box = bool(np.all(np.abs(np.log(dd / dd[0])) <= 1.5))
    out = dict(kind=row['kind'], cls=row['cls'], group=row['group'], m=row['m'], subset=row['subset'], N=len(idx),
               fams=row['fams'], sizes=sizes, witness_dirs=[idx[a] for a in A], witness_size=len(A),
               witness_hull_vertices=nh, witness_hull_arcs_deg=arcs, witness_perimeter=mp.nstr(L, 30), g=mp.nstr(gm, 30),
               bound_4pi=mp.nstr(2 * mp.pi * (2 * len(A) - len(idx)) / len(idx), 30),
               sigma_hull_halfpi=mp.nstr(1 - (2 * mp.pi - L) / (4 * mp.pi), 30), mu_hull=mp.nstr(mp.mpf(len(A)) / len(idx), 30),
               hull_exact=hull_ok, candidates=ncand, exhaustive=exhaustive, condition=condition, equality=equality,
               die_finder=df, die_inside_study_box=box,
               study_sols=row['study_sols'], verdict=verdict, secs=round(time.time() - t0, 1))
    return out

if __name__ == '__main__':
    inp, outp, npr = sys.argv[1], sys.argv[2], int(sys.argv[3]); tl = float(sys.argv[4]) if len(sys.argv) > 4 else 270
    rows = [json.loads(L) for L in open(inp)]
    key = lambda r: (r['kind'], r['cls'], r['m'], tuple(r['subset']))
    done = set()
    if os.path.exists(outp):
        for L in open(outp):
            try: done.add(key(json.loads(L)))
            except Exception: pass
    todo = sorted([r for r in rows if key(r) not in done], key=lambda r: -sum(len(O) for O in r['orbits']))
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
