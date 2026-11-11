# generic_hop.py, DICTO 11 Nov 2026 ("figure out if this may be an expression of a new law"): is "cut fraction < 1/2" a law of the
# hop for EVERY convex polytope, or special to the OG family?  Hop: D -> P(D) = hull of the foot points h_i n_i of D's face planes
# (= polar of T(polar D)). Candidate = face of D; CUT = foot point not a corner of P(D). Mean load = candidates / active = 1/(1 - cut).
# Start classes (origin inside):  S  near-sphere points, radial noise s;  I  same, closed under the 60 icosahedral rotations;
#   H  random half-spaces (unit normals, offsets uniform in [1 - s, 1]);  E  points on an ellipsoid with origin moved off centre.
# Every hop with cut > F/2 and F <= 1000 is re-checked candidate by candidate by LP (in hull of the others?).
# Shallow cuts (depth < 1e-6 of the size) are reported but not counted in the robust maximum.
# Check per hop: Euler for P(D) in the form F' = 2(F - c) - 4 - e'  (e' = sum over faces of P(D) of (corners - 3)), and every
#   face distance > 0 (origin strictly inside). Records max cut fraction per run.
# ROUNDNESS VERSION (roundness_hop.py, DICTO 11-11 'run the cut fraction vs roundness test'): per hop also the roundness of D:
#   R/r (largest corner distance / smallest face distance, from O) and t = t_min(D) = least t with D inside t.P(D) (#43's quantity).
#   Question: is there g with cut fraction <= g(t), g(3/phi^2) < 1/2?  Many seeds, noise levels spread continuously.
# usage: python -u roundness_hop.py <seed0> <nseeds> <out.json> [quick]
import sys, json, time
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
SEED0, NSEED, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; QUICK = len(sys.argv) > 4; rng = np.random.default_rng(SEED0)
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
        if kind == 'I': W = symmetrise(W)
        nfoot = len(W); W = dedupe(W); dup = nfoot - len(W)
        FN = faces(W); M2, D2, cor2, deg2 = FN
        F = len(W); c = F - len(cor2)
        depth = robust_depth(W, cor2)
        C = V[cor]; Rr = float(np.linalg.norm(C, axis=1).max() / Dd.min())
        t = float(((C @ M2.T) / D2[None, :]).max())          # t_min(D): D inside t.P(D)
        e2 = sum(len(d) - 3 for d in deg2.values()); ok &= len(M2) == 2 * (F - c) - 4 - e2 and dup == 0 and t >= 1 - 1e-9
        out.append(dict(kind=kind, n=n, s=s, k=k, F=F, cut=c, frac=c / F, Rr=Rr, t=t, depth=depth))
        V, FF = W, FN
        if len(M2) > FCAP: break
    return out, ok

PHI2 = 3 / phi ** 2
rows = []; allok = True; t0 = time.time()
kinds = ('S', 'I', 'H', 'E')
for seed in range(SEED0, SEED0 + NSEED):
    rng = np.random.default_rng(seed)
    for kind in kinds:
        n = int(rng.choice([60, 120, 300, 600] if kind == 'I' else [30, 60, 150, 400]))
        s = float(rng.uniform(0.005, 0.4)) if kind != 'E' else float(rng.uniform(0.05, 1.0))
        if kind == 'H': s = float(rng.uniform(0.05, 0.9))
        o, ok = run(kind, n, s, 6 if QUICK else 8); allok &= ok; rows += o
    print(f'PROGRESS {(seed - SEED0 + 1) / NSEED:.3f} seed {seed} hops so far {len(rows)} {time.time() - t0:.0f}s', flush=True)
rob = [r for r in rows if r['cut'] == 0 or r['depth'] > 1e-6]
json.dump(rows, open(OUT, 'w'))
print(f'hops: {len(rows)} (robust {len(rob)})')
for lab, key, edges in (('t = t_min(D)', 't', [1, 1.02, 1.05, 1.1, PHI2, 1.2, 1.3, 1.5, 2, 3, 1e9]), ('R/r', 'Rr', [1, 1.02, 1.05, 1.1, 1.15, 1.2, 1.3, 1.5, 2, 3, 1e9])):
    print(f'max cut fraction by {lab} (bin: max cut, hops):')
    for a, b in zip(edges, edges[1:]):
        sel = [r['frac'] for r in rob if a <= r[key] < b]
        if sel: print(f'   [{a:.4f}, {b:.4f}): max {max(sel):.3f}  mean {np.mean(sel):.3f}  hops {len(sel)}')
g = [r['frac'] for r in rob if r['t'] <= PHI2]
print(f'KEY: hops with t <= 3/phi^2 = {PHI2:.4f}: {len(g)}, max cut fraction {max(g) if g else float("nan"):.3f}, above 1/2: {sum(1 for x in g if x > 0.5)}')
gr = [r for r in rob if r['frac'] > 0.5]
if gr: print('roundest over-half hop: t', round(min(r['t'] for r in gr), 4), 'R/r', round(min(r['Rr'] for r in gr), 4))
print('FINAL ok' if allok else 'FINAL FAIL: Euler identity, origin, duplicate or t >= 1 check failed')
