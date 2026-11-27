import json, numpy as np
from scipy.spatial import ConvexHull
A = json.load(open('/tmp/all_stars.json'))
for tn in (1, 4):
    sh = next(s for s in A if s['D'] == 'D71' and s['t'] == '2'); T = sh['turns'][tn - 1]
    V = np.array(T['solid']['vertices']); F = T['solid']['faces']; tips = np.array(T['tips']); c0 = V.mean(0); V -= c0; tips -= c0
    star = ConvexHull(V).volume + sum(ConvexHull(np.vstack([V[f], [tp]])).volume for f, tp in zip(F, tips))
    P = np.vstack([V, tips]); h = ConvexHull(P); fs = {}
    for eq, sm in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 8)), set()).update(sm)
    hv = set(h.vertices)
    pv = 0; offaxis = []; kinds = []
    for k, idx in fs.items():
        n = np.array(k[:3]); n /= np.linalg.norm(n); d = -k[3]; Fc = P[list(idx)]
        # S corners whose central projection onto the face plane falls inside the face: the deepest such corner is the pit apex
        cand = []
        for j, c in enumerate(V):
            if c @ n <= 1e-12: continue
            y = c * (d / (c @ n))
            cen = Fc.mean(0); e1 = Fc[0] - cen; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
            P2 = np.c_[(Fc - cen) @ e1, (Fc - cen) @ e2]; P2 = P2[np.argsort(np.arctan2(P2[:, 1], P2[:, 0]))]; q = np.array([(y - cen) @ e1, (y - cen) @ e2])
            inside = all((P2[(i + 1) % len(P2)][0] - P2[i][0]) * (q[1] - P2[i][1]) - (P2[(i + 1) % len(P2)][1] - P2[i][1]) * (q[0] - P2[i][0]) >= -1e-9 for i in range(len(P2)))
            if inside: cand.append((c @ n, j))
        if not cand: continue
        _, j = min(cand); c = V[j]
        if abs(c @ n - d) < 1e-9 * d: continue          # a corner of S on the hull face: no pit there
        pv += ConvexHull(np.vstack([Fc, [c]])).volume
        offaxis.append(float(np.linalg.norm(np.cross(c / np.linalg.norm(c), n)))); kinds.append(len(idx))
    print(f"Samson turn {tn}: S {len(V)} corners / {len(F)} faces; hull {len(fs)} faces (sizes {sorted(set(kinds))}); star volume {star:.6f}; "
          f"hull minus pits to S's corners {h.volume - pv:.6f}; ratio {star / (h.volume - pv):.6f}; pit tips off the face axis: max sin {max(offaxis):.4f}")
