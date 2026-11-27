import json, numpy as np
from scipy.spatial import ConvexHull
A = json.load(open('/tmp/all_stars.json'))
want = [('D77','2',4),('D71','2',1),('D3','phi',1),('D77','phi',5),('D77','2',1),('D99','phi',2),('D96','2',2),('D97','2',2),('D95','2',5),('D99','2',2),('D71','2',4),('D77','2',3)]
for D, t, tn in want:
    sh = next(s for s in A if s['D'] == D and s['t'] == t); T = sh['turns'][tn - 1]
    V = np.array(T['solid']['vertices']); F = T['solid']['faces']; tips = np.array(T['tips']); c0 = V.mean(0); V -= c0; tips -= c0
    star = ConvexHull(V).volume + sum(ConvexHull(np.vstack([V[f], [tp]])).volume for f, tp in zip(F, tips))
    P = np.vstack([V, tips]); h = ConvexHull(P); fs = {}
    for eq, sm in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 8)), set()).update(sm)
    Sp = []
    for f in F:
        X = V[f]; n = np.cross(X[1] - X[0], X[2] - X[0]); n /= np.linalg.norm(n); n = n if n @ X[0] > 0 else -n; Sp.append((n, n @ X[0]))
    depth = []
    for k in fs:
        n = np.array(k[:3]); n /= np.linalg.norm(n); d = -k[3]; s = min(dd / (m @ n) for m, dd in Sp if m @ n > 1e-12); depth.append(1 - s / d)
    print(f"{D} {sh['name'][:22]:22s} t={t:3s} turn {tn}: star / hull volume {star / h.volume:.3f}; pit depth (share of the face distance) "
          f"min {min(depth):.3f} max {max(depth):.3f}")
