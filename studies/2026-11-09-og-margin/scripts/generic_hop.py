# generic_hop.py, DICTO 11 Nov 2026 ("figure out if this may be an expression of a new law"): is "cut fraction < 1/2" a law of the
# hop for EVERY convex polytope, or special to the OG family?  Hop: D -> P(D) = hull of the foot points h_i n_i of D's face planes
# (= polar of T(polar D)). Candidate = face of D; CUT = foot point not a corner of P(D). Mean load = candidates / active = 1/(1 - cut).
# Start classes (origin inside):  S  near-sphere points, radial noise s;  I  same, closed under the 60 icosahedral rotations;
#   H  random half-spaces (unit normals, offsets uniform in [1 - s, 1]);  E  points on an ellipsoid with origin moved off centre.
# Every hop with cut > F/2 and F <= 1000 is re-checked candidate by candidate by LP (in hull of the others?).
# Shallow cuts (depth < 1e-6 of the size) are reported but not counted in the robust maximum.
# Check per hop: Euler for P(D) in the form F' = 2(F - c) - 4 - e'  (e' = sum over faces of P(D) of (corners - 3)), and every
#   face distance > 0 (origin strictly inside). Records max cut fraction per run.
# usage: python -u generic_hop.py <seed> <out.json> [quick]
import sys, json, time
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
rng = np.random.default_rng(int(sys.argv[1])); OUT = sys.argv[2]; QUICK = len(sys.argv) > 3
FCAP = 40000

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
    # corners of each merged face (distinct hull corners on it)
    fc = {}
    for t, s in enumerate(h.simplices):
        fc.setdefault(inv[t], set()).update(s.tolist())
    return M, Dd, h.vertices, fc

def rot(axis, ang):
    a = np.asarray(axis, float); a /= np.linalg.norm(a); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
phi = (1 + 5 ** .5) / 2
G = [np.eye(3)]; gens = [rot([0, 1, phi], 2 * np.pi / 5), rot([1, 1, 1], 2 * np.pi / 3)]
while True:
    new = [g @ s for g in G for s in gens]
    add = [m for m in new if min(np.abs(m - x).max() for x in G) > 1e-9]
    uniq = []
    for m in add:
        if not uniq or min(np.abs(m - x).max() for x in uniq) > 1e-9: uniq.append(m)
    if not uniq: break
    G += uniq
assert len(G) == 60, len(G)

from scipy.spatial import cKDTree
def symmetrise(W):
    X = np.vstack([W @ g.T for g in G]); t = cKDTree(X); groups = {}
    for i, js in enumerate(t.query_ball_point(X, 1e-8)): groups.setdefault(min(js), []).append(i)
    return np.array([X[g].mean(0) for g in groups.values()])
def dedupe(W, tol=1e-9):
    t = cKDTree(W); groups = {}
    for i, js in enumerate(t.query_ball_point(W, tol * np.abs(W).max())): groups.setdefault(min(js), []).append(i)
    return np.array([W[g].mean(0) for g in groups.values()])
def robust_depth(W, cor):
    """smallest distance (relative to the diameter scale) from a non-corner foot point to the boundary of the hull of the corners."""
    nc = np.setdiff1d(np.arange(len(W)), cor)
    if len(nc) == 0: return float('inf')
    E = ConvexHull(W[cor]).equations
    return float((-(W[nc] @ E[:, :3].T + E[:, 3]).max(1)).min() / np.abs(W).max())
from scipy.optimize import linprog
def lp_inside(P, i):
    others = np.delete(P, i, 0); n = len(others)
    r = linprog(np.zeros(n), A_eq=np.vstack([others.T, np.ones(n)]), b_eq=np.append(P[i], 1), bounds=[(0, None)] * n, method='highs')
    return r.status == 0
def unit(n): x = rng.normal(size=(n, 3)); return x / np.linalg.norm(x, axis=1)[:, None]

def start(kind, n, s):
    if kind == 'S': return unit(n) * (1 + s * rng.uniform(-1, 1, (n, 1)))
    if kind == 'I':
        P = unit(max(1, n // 60)) * (1 + s * rng.uniform(-1, 1, (max(1, n // 60), 1)))
        return np.vstack([P @ g.T for g in G])
    if kind == 'H':
        N = unit(n); h = rng.uniform(1 - s, 1, n)
        hs = HalfspaceIntersection(np.hstack([N, -h[:, None]]), np.zeros(3)); return hs.intersections
    if kind == 'E':
        P = unit(n) * np.array([1, 1 + 2 * s, 1 + 6 * s]); return P - np.array([0, 0, (1 + 6 * s) * 0.6])

def run(kind, n, s, hops):
    V = start(kind, n, s); FF = faces(V); out = []; ok = True
    for k in range(hops):
        M, Dd, cor, _ = FF
        if Dd.min() <= 1e-9: ok = False; break
        W = M * Dd[:, None]
        if kind == 'I': W = symmetrise(W)                  # as in the OG runs: orbit closure + merge kills float drift
        nfoot = len(W); W = dedupe(W); dup = nfoot - len(W)  # near-equal foot points = one face split by rounding
        FN = faces(W); M2, D2, cor2, deg2 = FN
        F = len(W); c = F - len(cor2)
        depth = robust_depth(W, cor2)                     # how deep the shallowest cut candidate sits (relative to size)
        ok &= dup == 0
        lpv = None
        if c * 2 > F and F <= 1000:                        # independent LP verdict for every candidate of an over-half hop
            lpv = all(lp_inside(W, i) == (i not in set(cor2.tolist())) for i in range(F)); ok &= lpv
        e2 = sum(len(d) - 3 for d in deg2.values())         # face excess of P(D): sum (corners - 3)
        ok &= len(M2) == 2 * (F - c) - 4 - e2
        out.append(dict(k=k, F=F, cut=c, frac=c / F, load=F / (F - c), excess=e2, dup=dup, depth=depth, lp=lpv))
        V, FF = W, FN
        if len(M2) > FCAP: break
    return out, ok

configs = []
for kind in ('S', 'I', 'H', 'E'):
    for n, s in ((100, .01), (100, .2), (500, .05), (500, .2), (2000, .01), (2000, .1)):
        if kind == 'H': s = {0.01: 0.2, 0.05: 0.4, 0.1: 0.6, 0.2: 0.8}[s]
        if kind == 'E': s = {0.01: 0.1, 0.05: 0.3, 0.1: 0.5, 0.2: 1.0}[s]
        configs.append((kind, n, s))
if QUICK: configs = configs[::6]
res = []; allok = True; t0 = time.time()
for kind, n, s in configs:
    hops = 8 if n <= 500 else 5
    o, ok = run(kind, n, s, hops); allok &= ok
    mf = max(r['frac'] for r in o); mfr = max([r['frac'] for r in o if r['cut'] == 0 or r['depth'] > 1e-6] + [0]); ml = max(r['load'] for r in o)
    res.append(dict(kind=kind, n=n, s=s, ok=bool(ok), hops=o, max_frac=mf, max_frac_robust=mfr, max_load=ml))
    print(f"{kind} n {n:5d} s {s:.2f} | hops {len(o)} F {o[0]['F']}->{o[-1]['F']} | cut fractions " +
          ' '.join(f"{r['frac']:.3f}" for r in o) + f" | min cut depth {min(r['depth'] for r in o):.1e} dups {sum(r['dup'] for r in o)}" + f" | max {mf:.3f} (robust hops, cut depth > 1e-6: {mfr:.3f}) load {ml:.2f} | euler {ok} | {time.time() - t0:.0f}s", flush=True)
json.dump(res, open(OUT, 'w'))
worst = max(res, key=lambda r: r['max_frac_robust'])
print(f"worst robust: {worst['kind']} n {worst['n']} s {worst['s']} max cut fraction {worst['max_frac_robust']:.3f}; above 1/2 anywhere: {worst['max_frac_robust'] > 0.5}")
for kd in 'SIHE': print(kd, 'max robust cut fraction', max(r['max_frac_robust'] for r in res if r['kind'] == kd), 'max mean load', max(r['max_load'] for r in res if r['kind'] == kd))
print('over-half hops LP-verified (F <= 1000):', sum(1 for r in res for h in r['hops'] if h['lp']), 'all agree' if allok else '')
print('FINAL ok' if allok else 'FINAL FAIL: Euler identity, origin or duplicate-foot-point check failed')
