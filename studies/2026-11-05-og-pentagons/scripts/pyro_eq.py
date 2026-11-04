# DICTO 5 Nov 2026: can the regular-triangle (equal-edge) cut OG connect to a pyrochlore network?
# Diamond net: copies at diamond nodes, joined through 4 hexagons in tetrahedral directions; joints at the bond midpoints = pyrochlore sites.
import numpy as np, itertools, math, manifold3d as m3
from scipy.spatial import ConvexHull
V = np.load("equilateral.npy"); V = V - V.mean(0)
def hull(P): return m3.Manifold.hull_points(np.asarray(P, float).tolist())
h = ConvexHull(V); pl = {}
for eq, s in zip(h.equations, h.simplices): pl.setdefault(tuple(np.round(eq, 6)), set()).update(s)
HEX = [sorted(f) for f in pl.values() if len(f) == 6]; print("corners", len(V), "hexagons", len(HEX), flush=True)
cen = [V[f].mean(0) for f in HEX]; u = [c/np.linalg.norm(c) for c in cen]
tet = next(q for q in itertools.combinations(range(len(HEX)), 4) if all(abs(u[a] @ u[b] + 1/3) < 1e-6 for a, b in itertools.combinations(q, 2)))
H = [V[HEX[i]] for i in tet]; T = [cen[i] for i in tet]; d = np.linalg.norm(T[0])
# 1) does a hexagon match its own point reflection (needed for a plain face-to-face diamond join)?
mis = max(min(np.linalg.norm(2*T[0] - p - q) for q in H[0]) for p in H[0]); print(f"hexagon vs its point reflection: worst corner gap {mis:.4f} (0 = plain join works)", flush=True)
A = hull(V); print(f"cut OG volume {A.volume():.6f}, hexagon distance {d:.6f}", flush=True)
for g in (0.0, 0.05, 0.1, 0.2):
    # copy B = point reflection of A through the bond midpoint m; connector = hull of the two hexagons (one turned 60 deg relative to the other)
    def node(c, s): return c + s*V
    tu = [t/np.linalg.norm(t) for t in T]; m = [T[i] + g/2*tu[i] for i in range(4)]
    a1 = [2*m[i] - 2*m[j] for i in range(4) for j in range(4) if i != j]
    Ls = {tuple(np.round(n1*np.array(a1[0]) + n2*np.array(a1[1]) + n3*np.array(a1[5]), 6)) for n1, n2, n3 in itertools.product(range(-1, 2), repeat=3)}
    nodes = [(np.array(c), 1) for c in Ls] + [(np.array(c) + 2*m[0], -1) for c in Ls]
    nodes = [(c, s) for c, s in nodes if np.linalg.norm(c) < 2.2*np.linalg.norm(a1[0])]
    sol = [hull(node(c, s)) for c, s in nodes]; nc = 0
    for (c1, s1), (c2, s2) in itertools.combinations(nodes, 2):
        for i in range(4):
            if s1 == 1 and np.linalg.norm(c2 - (c1 + 2*m[i])) < 1e-6 and g > 0:
                sol.append(hull(np.vstack([c1 + H[i], c2 - H[i]]))); nc += 1
    U = m3.Manifold.batch_boolean(sol, m3.OpType.Add); ov = sum(x.volume() for x in sol) - U.volume()
    print(f"gap {g}: nodes {len(nodes)}, connectors {nc}, overlap volume {ov:.2e}", flush=True)
print("FINAL ok")
