import json, numpy as np
from scipy.spatial import ConvexHull
from collections import Counter
A = json.load(open('/tmp/all_stars.json'))
for t in ('2', 'phi'):
    sh = next(s for s in A if s['D'] == 'D71' and s['t'] == t)
    for tn in (2, 3):
        T = sh['turns'][tn - 1]; V = np.array(T['solid']['vertices']); V -= V.mean(0); F = T['solid']['faces']
        sizes = Counter(len(f) for f in F)
        E = {}
        for f in F:
            for i in range(len(f)):
                a, b = sorted((f[i], f[(i + 1) % len(f)])); E[(a, b)] = float(np.linalg.norm(V[a] - V[b]))
        L = sorted(set(round(x, 9) for x in E.values())); r = np.linalg.norm(V, axis=1)
        # edges of the triangles vs the hexagon-only edges
        tri_e = {tuple(sorted((f[i], f[(i + 1) % 3]))) for f in F if len(f) == 3 for i in range(3)}
        lt = sorted(set(round(E[e], 9) for e in tri_e)); lh = sorted(set(round(v, 9) for e, v in E.items() if e not in tri_e))
        print(f"Samson t={t} turn {tn}: faces {dict(sizes)}; corners {len(V)}; triangle edges {lt}; other hexagon edges {lh}; "
              f"ratio {lh[0] / lt[0] if lh and lt else None:.6f}; corner radius / triangle edge {r.mean() / lt[0]:.6f} (spread {np.ptp(r):.1e})")
print("the four-tetrahedra truncated tetrahedron: ratio 2/3 = 0.666667, corner radius / triangle edge = 1")
