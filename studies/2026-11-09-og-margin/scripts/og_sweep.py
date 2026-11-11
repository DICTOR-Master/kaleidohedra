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
# usage: python -u og_sweep.py <five-fold-octet dir> <kmax> <out.json>
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

def death(X, x2, i):
    """lam_i and the death point: min lam s.t. X_i.y - lam = |X_i|^2, X_j.y - lam <= |X_j|^2."""
    A = np.hstack([X, -np.ones((len(X), 1))])
    r = linprog(c=[0, 0, 0, 1], A_ub=A, b_ub=x2, A_eq=A[i:i + 1], b_eq=x2[i:i + 1], bounds=[(None, None)] * 4, method='highs')
    if r.status != 0: raise RuntimeError(f'LP status {r.status} at candidate {i}')
    return r.x[3], r.x[:3]

rows_out = []; ok_all = True; t0 = time.time()
V = OGf; FF = faces(V)
for k in range(KMAX + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    act = np.zeros(len(W), bool); act[cor2] = True
    X = W / np.einsum('ij,ij->i', W, W)[:, None]; x2 = np.einsum('ij,ij->i', X, X); n = len(X)
    tree = cKDTree(X); perms = [tree.query(X @ g.T)[1] for g in Gf]          # rotation action on candidates
    orb = -np.ones(n, int); reps = []
    for i in range(n):
        if orb[i] < 0:
            for p in perms: orb[p[i]] = len(reps)
            reps.append(i)
    lam = np.full(n, -np.inf); tight = {}                                   # lam only needed for cut candidates (> 0) and ties
    scale = np.abs(x2).max()
    for o, i in enumerate(reps):
        li, yi = death(X, x2, i)
        T = np.where(np.abs(X @ yi - li - x2) < 1e-7 * scale)[0]
        for p, g in zip(perms, Gf):                                         # spread to the orbit
            j = p[i]
            if lam[j] == -np.inf: lam[j] = li; tight[j] = p[T]
    tol = 1e-9 * scale
    cut_sweep = lam > tol
    agree = bool((cut_sweep == ~act).all())                                 # CONTROL 1
    # mass flow, descending lam
    mass = np.ones(n); order = np.argsort(-lam); orphan = 0; carried = 0.0; ev = {}
    for i in order:
        if not cut_sweep[i]: break
        rec = [j for j in tight[i] if j != i and lam[j] < lam[i] - tol]
        key = (round(lam[i] / tol), len(tight[i])); ev[len(tight[i])] = ev.get(len(tight[i]), 0) + 1
        if not rec: orphan += 1; continue
        carried = max(carried, mass[i]); mass[rec] += mass[i] / len(rec); mass[i] = 0
    am = mass[act]; cons = abs(mass.sum() - n) < 1e-6 and orphan == 0          # CONTROL 2
    # BEST FLOW (11-11, after equal split failed): mass may take any route down the sweep (dying face -> faces it dies among that
    # outlive it). c* = least possible maximum active load (max-flow, binary search). c* < 2 at every level => cut < active.
    cstar = 1.0; na = int(act.sum())
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
        lo, hi = 1.0, float(am.max()) + 0.01
        while hi - lo > 1e-3:
            mid = (lo + hi) / 2
            if feasible(mid): hi = mid
            else: lo = mid
        cstar = hi
    print(f'k {k:3d}: BEST FLOW least max active load c* = {cstar:.4f} (mean {n / na:.4f})', flush=True)
    nc, na = int(cut_sweep.sum()), int(act.sum())
    ok_all &= agree and cons
    print(f'PROGRESS {(k + 1) / (KMAX + 1):.3f} level {k}', flush=True)
    print(f'k {k:3d}: cand {n:6d} active {na:6d} cut {nc:6d} ({nc / n:.3f}) | sweep=hull {agree} | mass conserved {cons} (orphans {orphan}) | '
          f'active mass max {am.max():.4f} mean {am.mean():.4f} | max carried by a dying face {carried:.4f} | tight-set sizes at deaths {dict(sorted(ev.items()))} | '
          f'lam range of deaths [{lam[cut_sweep].min() if nc else 0:.3e}, {lam[cut_sweep].max() if nc else 0:.3e}] | {len(reps)} orbit LPs | {time.time() - t0:.0f}s', flush=True)
    rows_out.append(dict(k=k, cand=n, active=na, cut=nc, sweep_equals_hull=agree, mass_conserved=cons, orphans=orphan,
                         mass_max=float(am.max()), cstar=cstar, mass_mean=float(am.mean()), carried_max=carried, tight_sizes=ev,
                         mass_hist=np.histogram(am, bins=[0, 1, 1.5, 2, 3, 5, 1e9])[0].tolist()))
    V, FF = W, FN
json.dump({'mark': 'DICTO #43 sweep pilot, 2026-11-11 · DICTO · dictospheres.com', 'k': rows_out}, open(OUT, 'w'))
under2 = all(r['mass_max'] < 2 for r in rows_out)
print('every level: every active face carries mass < 2 (=> cut < active):', under2)
print('every level: BEST FLOW c* < 2:', all(r['cstar'] < 2 for r in rows_out), '| c* by level', [round(r['cstar'], 3) for r in rows_out])
print('FINAL ok' if ok_all else 'FINAL FAIL: a control failed (sweep vs hull, or mass not conserved)')
