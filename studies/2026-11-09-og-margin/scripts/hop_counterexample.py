# hop_counterexample.py, DICTO 11 Nov 2026: the smallest convex polytope (origin inside) whose single hop cuts MORE than half of
# its faces. Random search over small polytopes (hull of n random points, n = 5..14, origin placed at a random interior point), keep
# the fewest faces with cut > F/2 and every cut foot point at depth > 1e-3 (relative). Independent check of each cut/active verdict by
# linear programming: foot point p_i is cut iff it is a convex combination of the other foot points (scipy linprog feasibility).
# usage: python -u hop_counterexample.py <seed> <trials> [max points, default 14]
import sys
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
rng = np.random.default_rng(int(sys.argv[1])); TR = int(sys.argv[2]); NMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 14

def planes(V, tol=1e-9):
    E = ConvexHull(V).equations; keep = []
    for e in E:
        if not any(np.abs(e - f).max() < tol for f in keep): keep.append(e)
    E = np.array(keep); return E[:, :3], -E[:, 3]

def lp_cut(P, i):
    others = np.delete(P, i, 0); n = len(others)
    A = np.vstack([others.T, np.ones(n)]); b = np.append(P[i], 1)
    r = linprog(np.zeros(n), A_eq=A, b_eq=b, bounds=[(0, None)] * n, method='highs')
    return r.status == 0

best = None; maxfrac = (0, None)
for t in range(TR):
    n = int(rng.integers(5, NMAX + 1)); V = rng.normal(size=(n, 3)) * rng.uniform(0.2, 3, 3)
    h = ConvexHull(V); w = rng.dirichlet(np.ones(len(h.vertices)) * 0.3); o = w @ V[h.vertices]
    V = V - o
    M, d = planes(V)
    if d.min() < 1e-3 * np.abs(V).max(): continue
    P = M * d[:, None]; F = len(P); cor = ConvexHull(P).vertices; c = F - len(cor)
    if c * 2 <= F: continue
    nc = np.setdiff1d(np.arange(F), cor); E = ConvexHull(P[cor]).equations
    depth = (-(P[nc] @ E[:, :3].T + E[:, 3]).max(1)).min() / np.abs(P).max()
    if depth < 1e-3: continue
    if c / F > maxfrac[0]: maxfrac = (c / F, F)
    if best is None or F < best[0] or (F == best[0] and c > best[1]): best = (F, c, V.copy(), depth)
ok = True
if best:
    F, c, V, depth = best; M, d = planes(V); P = M * d[:, None]
    lp = [lp_cut(P, i) for i in range(F)]; cor = set(ConvexHull(P).vertices.tolist())
    agree = all(lp[i] == (i not in cor) for i in range(F)); ok &= agree and sum(lp) == c
    print(f'smallest found: {len(V)} points, {len(ConvexHull(V).vertices)} corners, {F} faces, {c} cut ({c / F:.3f}), min cut depth {depth:.2e}, LP agrees: {agree}')
    print('corners (origin inside):'); print(np.array2string(V[ConvexHull(V).vertices], precision=4, suppress_small=True))
    print('face distances:', np.array2string(d, precision=4)); print('cut by LP:', [i for i in range(F) if lp[i]])
print(f'largest cut fraction among robust finds: {maxfrac[0]:.3f} (F = {maxfrac[1]})')
print('FINAL ok' if (best and ok) else 'FINAL FAIL: no robust example found or LP disagrees with the hull verdict')
