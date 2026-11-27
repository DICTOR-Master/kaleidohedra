import json, sys, numpy as np
from scipy.spatial import ConvexHull
D = json.load(open(sys.argv[1]))
for T in D['turns'][2:]:
    V = np.array(T['solid']['vertices']); F = T['solid']['faces']; tips = np.array(T['tips']); c0 = V.mean(0); V = V - c0; tips = tips - c0
    vS = ConvexHull(V).volume; vsp = sum(ConvexHull(np.vstack([V[f], [tp]])).volume for f, tp in zip(F, tips)); star = vS + vsp
    P = np.vstack([V, tips]); h = ConvexHull(P); vH = h.volume
    fs = {}
    for eq, sm in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 8)), set()).update(sm)
    # where do the hull's corners come from: tips only, or also S corners?
    hv = set(h.vertices); ntip = sum(1 for i in hv if i >= len(V)); nS = len(hv) - ntip
    # the Vacuus-Solid of the hull at the size whose pits reach S: pit bottom = the S point deepest on the axis = smallest radius where the
    # axis meets S's boundary (S convex): s* = min over S planes of d_S / (n_S . n_F)
    Sp = []
    for f in F:
        X = V[f]; n = np.cross(X[1] - X[0], X[2] - X[0]); n /= np.linalg.norm(n); n = n if n @ X[0] > 0 else -n; Sp.append((n, n @ X[0]))
    pv = 0
    for k, idx in fs.items():
        n = np.array(k[:3]); n /= np.linalg.norm(n); s = min(d / (m @ n) for m, d in Sp if m @ n > 1e-12)
        pv += ConvexHull(np.vstack([P[list(idx)], [s * n]])).volume
    print(f"turn {T['turn']}: hull corners {len(hv)} ({ntip} tips, {nS} corners of S); star volume {star:.6f}; hull {vH:.6f}; "
          f"hull minus pits reaching S {vH - pv:.6f}; star / that = {star / (vH - pv):.4f}")
print('FINAL ok' if len(D['turns']) >= 3 else 'FINAL FAIL (fewer than three turns)')
