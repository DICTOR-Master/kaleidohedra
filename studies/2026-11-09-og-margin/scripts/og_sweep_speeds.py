# og_sweep.py (from cut_lemma.py), DICTO 11 Nov 2026 ("could we not use anything from permutahedron studies" -> "yes start the pilot").
# The #104 sweep applied to the OG hop. Polar picture as in cut_lemma.py: candidates X_i = corners of X_k = polar(D_k).
# Slider: T_lam = {y : X_j.y <= |X_j|^2 + lam}. Large lam: every candidate is a face; lam = 0: X_{k+1} (faces = ACTIVE candidates).
# Stacked over lam this is ONE convex 4D polyhedron; each facet's lam-range is an interval [lam_i, inf), so faces only DIE going down,
# exactly once: lam_i = min lam s.t. facet i nonempty (one LP). Cut <=> lam_i > 0 (control 1: must equal the hull test of cut_lemma).
# At its death point y_i the TIGHT facets are the faces it dies among (generic: 3; symmetric clusters: more).
# MASS FLOW: every face starts with mass 1; going down in lam, a dying face hands its mass in equal parts to the tight faces that
# outlive it. At lam = 0 all mass sits on active faces: candidates = sum of active masses (control 2: conservation).
# Wanted lemma shape: every active mass < 2  =>  cut < active  =>  at most half the candidates are cut (#43 step A1).
# Records per level: candidates, active, cut, death events, cluster sizes, max/mean active mass, max mass carried by a dying face.
# SPEEDS (DICTO 11-11 'is it possibly a different 4D shadow' / 'a balancing one'): plane j moves at speed s_j = |X_j|^q;
# q = 0 is og_sweep.py; every q has the same bottom (X_{k+1}); the 4D shape and who dies among whom change. Search a balancing one.
# usage: python -u og_sweep_speeds.py <five-fold-octet dir> <kmax> <out.json> <q list, e.g. -2,-1,0,0.5,1>
import sys, os, json, time
import numpy as np
from scipy.spatial import ConvexHull, cKDTree
from scipy.optimize import linprog
OUT = os.path.abspath(sys.argv[3])
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])   # OG (exact), G (60 exact rotations)
KMAX = int(sys.argv[2])
OGf = np.array([[x.f() for x in v] for v in OG]); Gf = np.array([[[x.f() for x in row] for row in M] for M in G])

def faces(V, tol=1e-9):
    h = ConvexHull(V); E = h.equations; n = len(E); par = np.arange(n)
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    roots = np.array([find(i) for i in range(n)]); u, inv = np.unique(roots, return_inverse=True)
    M = np.zeros((len(u), 3)); Dd = np.zeros(len(u)); cnt = np.bincount(inv)
    np.add.at(M, inv, E[:, :3]); np.add.at(Dd, inv, -E[:, 3]); M /= np.linalg.norm(M, axis=1)[:, None]; Dd /= cnt
    return M, Dd, np.unique(h.vertices)

def symmetrise(W):
    X = np.vstack([W @ g.T for g in Gf]); X = X[np.lexsort(X.T[::-1])]
    t = cKDTree(X); groups = {}
    for i, js in enumerate(t.query_ball_point(X, 1e-8)):
        groups.setdefault(min(js), []).append(i)
    return np.array([X[g].mean(0) for g in groups.values()])

def death(X, x2, sp, i):
    """lam_i and the death point: min lam s.t. X_i.y - s_i lam = |X_i|^2, X_j.y - s_j lam <= |X_j|^2 (s = plane speeds)."""
    A = np.hstack([X, -sp[:, None]])
    r = linprog(c=[0, 0, 0, 1], A_ub=A, b_ub=x2, A_eq=A[i:i + 1], b_eq=x2[i:i + 1], bounds=[(None, None)] * 4, method='highs')
    if r.status != 0: raise RuntimeError(f'LP status {r.status} at candidate {i}')
    return r.x[3], r.x[:3]

def analyse(X, x2, act, perms, reps, sp):
    n = len(X); na = int(act.sum())
    top_ok = len(ConvexHull(X / sp[:, None]).vertices) == n                  # CONTROL 0: every face present at the top
    lam = np.full(n, -np.inf); tight = {}; scale = np.abs(x2).max()
    for i in reps:
        li, yi = death(X, x2, sp, i)
        T = np.where(np.abs(X @ yi - li * sp - x2) < 1e-7 * scale)[0]
        for pm in perms:
            j = pm[i]
            if lam[j] == -np.inf: lam[j] = li; tight[j] = pm[T]
    tol = 1e-9 * scale * max(1.0, 1 / sp.min())
    cut_sweep = lam > tol; agree = bool((cut_sweep == ~act).all())        # CONTROL 1
    mass = np.ones(n); orphan = 0
    for i in np.argsort(-lam):
        if not cut_sweep[i]: break
        rec = [j for j in tight[i] if j != i and lam[j] < lam[i] - tol]
        if not rec: orphan += 1; continue
        mass[rec] += mass[i] / len(rec); mass[i] = 0
    cons = abs(mass.sum() - n) < 1e-6 and orphan == 0                        # CONTROL 2
    cstar = 1.0
    if cut_sweep.any():
        from scipy.sparse import csr_matrix
        from scipy.sparse.csgraph import maximum_flow
        Q, BIG = 1000, 10 ** 9; S, Tn = n, n + 1; er, ec = [], []
        for i in np.where(cut_sweep)[0]:
            for j in tight[i]:
                if j != i and lam[j] < lam[i] - tol: er.append(i); ec.append(j)
        def feasible(c):
            r = er + [S] * n + list(np.where(act)[0]); cc = ec + list(range(n)) + [Tn] * na
            cap = [BIG] * len(er) + [Q] * n + [int(c * Q)] * na
            G = csr_matrix((np.array(cap, np.int64), (r, cc)), shape=(n + 2, n + 2))
            return maximum_flow(G, S, Tn).flow_value >= n * Q
        lo, hi = 1.0, float(mass[act].max()) + 0.01
        if feasible(hi):
            while hi - lo > 1e-3:
                mid = (lo + hi) / 2
                if feasible(mid): hi = mid
                else: lo = mid
        else: hi = float('inf')
        cstar = hi
    return dict(top_ok=top_ok, agree=agree, cons=cons, orphans=orphan, eq_max=float(mass[act].max()), cstar=cstar)

QS = [float(q) for q in sys.argv[4].split(',')] if len(sys.argv) > 4 else [0.0]
rows_out = []; ok_all = True; t0 = time.time()
V = OGf; FF = faces(V)
for k in range(KMAX + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    act = np.zeros(len(W), bool); act[cor2] = True
    X = W / np.einsum('ij,ij->i', W, W)[:, None]; x2 = np.einsum('ij,ij->i', X, X); n = len(X); xn = np.sqrt(x2)
    tree = cKDTree(X); perms = [tree.query(X @ g.T)[1] for g in Gf]
    orb = -np.ones(n, int); reps = []
    for i in range(n):
        if orb[i] < 0:
            for pm in perms: orb[pm[i]] = len(reps)
            reps.append(i)
    row = dict(k=k, cand=n, active=int(act.sum()), cut=int((~act).sum()), q={})
    for q in QS:
        r = analyse(X, x2, act, perms, reps, xn ** q); row['q'][str(q)] = r
        ok_all &= r['top_ok'] and r['agree'] and r['cons']
        print(f'k {k:3d} q {q:+.2f}: cut {row["cut"]:6d}/{n:6d} | top all faces {r["top_ok"]} | sweep=hull {r["agree"]} | conserved {r["cons"]} | equal-split max {r["eq_max"]:.3f} | BEST c* {r["cstar"]:.3f} | {time.time() - t0:.0f}s', flush=True)
    print(f'PROGRESS {(k + 1) / (KMAX + 1):.3f} level {k}', flush=True)
    rows_out.append(row); V, FF = W, FN
json.dump({'mark': 'DICTO #43 sweep speeds (balancing 4D shadow), 2026-11-11 · DICTO · dictospheres.com', 'k': rows_out}, open(OUT, 'w'))
for q in QS:
    cs = [r['q'][str(q)]['cstar'] for r in rows_out]
    print(f'q {q:+.2f}: worst c* {max(cs):.3f} | c* < 2 at every level: {all(c < 2 for c in cs)} | by level {[round(c, 2) for c in cs]}')
print('FINAL ok' if ok_all else 'FINAL FAIL: a control failed')
