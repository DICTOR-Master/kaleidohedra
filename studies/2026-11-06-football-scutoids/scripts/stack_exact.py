"""Football scutoid study, step 3a (DICTO 11-07 "move to step 3 exact geometry"): the closest stacking of the pentagon-hexagon layers,
found continuously and with the BRIDGES included (step 2a used balls only and a 9 x 9 grid of shifts).
Bodies of a layer cell: ball X, ball Y and four bridges (hull of the two facing faces). The upper layer is the base moved by
T = h n + a P1 + b P2. Bodies A (base) and B (upper, extra lattice shift L) overlap iff T lies inside the Minkowski difference
M = A - B - L (a convex polytope). For a shift (a, b) the forbidden heights are open intervals; h(a, b) = the least h > 0 outside all.
Minimise h over (a, b); then report the active contacts (facets of the M's the optimum T lies on) for the exact solve (step 3a, part 2)."""
import itertools, sys, json, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
sys.argv = [sys.argv[0], '0.6']
exec(open('grid_layer.py').read().split('# overlap test')[0].replace('print(', '(lambda *a, **k: None)('))
n = np.cross(e1, e2); n /= np.linalg.norm(n)
P1, P2 = 2 * D * e1, D * (e1 + e2)
# bodies of the cell (0,0): balls (0,0) X and (1,0) Y; bridges (0,0)->(1,0), (0,0)->(0,1), (1,0)->(2,0), (1,0)->(1,1)
bodies, names = [], []
for i, j in ((0, 0), (1, 0)):
    bodies.append(ball(i, j)[0]); names.append(f"ball {'XY'[i]}")
for i, j in ((0, 0), (1, 0)):
    for di, dj, d in ((1, 0, e1), (0, 1, e2)):
        k1, f1 = face_toward(i, j, d); k2, f2 = face_toward(i + di, j + dj, -d)
        bodies.append(np.vstack([f1, f2])); names.append(f"bridge {'XY'[i]}{'+e1' if di else '+e2'}")
# Minkowski differences for all pairs and nearby lattice shifts; keep those that can meet a vertical line within reach
Ms = []
for A, B in itertools.product(range(len(bodies)), repeat=2):
    diff = (bodies[A][:, None, :] - bodies[B][None, :, :]).reshape(-1, 3)
    H = ConvexHull(diff); pts = diff[H.vertices]
    for p, q in itertools.product(range(-3, 4), repeat=2):
        L = p * P1 + q * P2; Q = pts - L
        # coordinates of Q in the basis (P1, P2, n)
        C = np.linalg.solve(np.array([P1, P2, n]).T, Q.T).T
        if C[:, 2].max() <= 0: continue                 # entirely below the base plane: never forbids h > 0
        Ms.append(dict(A=A, B=B, p=p, q=q, eq=ConvexHull(Q).equations, C=C))
print(f"bodies {len(bodies)} ({', '.join(names)}); Minkowski pieces kept {len(Ms)}")
def intervals(a, b):
    """open forbidden h-intervals on the line T = h n + a P1 + b P2"""
    out = []
    base = a * P1 + b * P2
    for k, M in enumerate(Ms):
        if not (M['C'][:, 0].min() - 1e-9 < a < M['C'][:, 0].max() + 1e-9 and M['C'][:, 1].min() - 1e-9 < b < M['C'][:, 1].max() + 1e-9): continue
        eq = M['eq']; s = eq[:, :3] @ n; r = eq[:, :3] @ base + eq[:, 3]    # inside iff r + s h < 0 for all facets
        if (r[np.abs(s) < 1e-14] >= 0).any(): continue
        pos, neg = s > 1e-14, s < -1e-14
        hi = (-r[pos] / s[pos]).min() if pos.any() else np.inf
        lo = (-r[neg] / s[neg]).max() if neg.any() else -np.inf
        if lo < hi - 1e-12 and hi > 0: out.append((lo, hi, k))
    return out
def hmin(ab):
    a, b = ab; I = sorted(intervals(a, b)); h = 0.0
    changed = True
    while changed:
        changed = False
        for lo, hi, k in I:
            if lo < h + 1e-12 < hi: h = hi; changed = True
    return h
# coarse scan, then local refinement (Nelder-Mead; h is piecewise smooth)
G = 40
best = min(((hmin((a, b)), a, b) for a, b in itertools.product(np.arange(G) / G, repeat=2)))
print(f"grid {G}x{G}: h {best[0]:.6f} at ({best[1]:.4f}, {best[2]:.4f})")
cands = sorted(((hmin((a, b)), a, b) for a, b in itertools.product(np.arange(G) / G, repeat=2)))[:12]
res = []
for h0, a0, b0 in cands:
    r = minimize(hmin, [a0, b0], method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-13, maxiter=4000))
    res.append((r.fun, r.x[0] % 1, r.x[1] % 1))
res.sort()
h, a, b = res[0]
print("best local optima (h, a, b):"); [print(f"  {x[0]:.10f}  ({x[1]:.8f}, {x[2]:.8f})") for x in res[:6]]
T = h * n + a * P1 + b * P2
act = []
for k, M in enumerate(Ms):
    d = M['eq'][:, :3] @ T + M['eq'][:, 3]
    if d.max() > -1e-6 and d.max() < 1e-6:   # T on the boundary of M
        on = [int(i) for i in np.where(np.abs(d) < 1e-6)[0]]
        act.append(dict(k=k, A=names[M['A']], B=names[M['B']], p=M['p'], q=M['q'], facets=len(on)))
print(f"optimum h = {h:.10f}, shift ({a:.8f}, {b:.8f}); contacts (T on the boundary of a Minkowski piece): {len(act)}")
for c in act: print(f"  {c['A']} (base) touches {c['B']} (upper, lattice +({c['p']},{c['q']})) on {c['facets']} facet(s)")
cellvol = abs(np.linalg.det(np.array([P1, P2, T])))
vb = ConvexHull(bodies[0]).volume; vbr = sum(ConvexHull(B).volume for B in bodies[2:])
print(f"balls fill {2 * vb / cellvol:.6f}, bridges {vbr / cellvol:.6f}, gap {1 - (2 * vb + vbr) / cellvol:.6f}")
old = 3.6224
print(f"step 2a value h = {old} at (0, 0.444): with bridges included that stacking is " + ("FREE" if hmin((0.0, 0.444)) <= old + 1e-4 else f"BLOCKED (needs h = {hmin((0.0, 0.444)):.4f})"))
json.dump(dict(h=h, a=a, b=b, contacts=act), open('../data-stack-exact.json', 'w'), indent=1)
print("FINAL ok" if len(act) >= 3 and abs(hmin((a, b)) - h) < 1e-9 else "FINAL FAIL (optimum not held by at least three contacts)")