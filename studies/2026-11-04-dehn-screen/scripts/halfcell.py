import math, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
s3 = math.sqrt(3); H = math.sqrt(2/3)
def cell(up, dn):
    nb = [(math.cos(k*math.pi/3), math.sin(k*math.pi/3), 0) for k in range(6)]
    nb += [(math.cos(t)/s3, math.sin(t)/s3, H) for t in up] + [(math.cos(t)/s3, math.sin(t)/s3, -H) for t in dn]
    Hs = np.array([[*n, -np.dot(n, n)/2] for n in map(np.array, nb)])
    return np.unique(np.round(HalfspaceIntersection(Hs, np.zeros(3)).intersections, 10), axis=0)
A = [math.pi/6, 5*math.pi/6, 3*math.pi/2]; B = [t + math.pi/3 for t in A]
RD = cell(A, B); TRD = cell(A, A)
def half(P, top):
    h = ConvexHull(P); Hs = np.vstack([h.equations, [0, 0, -1 if top else 1, 0]])
    return np.unique(np.round(HalfspaceIntersection(Hs, np.array([0, 0, .05 if top else -.05])).intersections, 9), axis=0)
def sig(P):
    D = np.linalg.norm(P[:, None] - P[None], axis=2); return sorted(np.round(D.ravel(), 6))
print("RD", len(RD), round(ConvexHull(RD).volume, 6), "| TRD", len(TRD), round(ConvexHull(TRD).volume, 6))
hs = {}
for n, P in (("RD", RD), ("TRD", TRD)):
    for t in (True, False): hs[f"{n} {'top' if t else 'bottom'}"] = half(P, t)
for a, b in itertools.combinations(hs, 2): print(f"{a:10s} vs {b:10s} congruent:", sig(hs[a]) == sig(hs[b]))
X = hs["RD top"]; h = ConvexHull(X); fs = {}
for eq, s in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 6)), set()).update(s)
print("half-cell:", len(X), "corners, volume", round(h.volume, 6), "faces by size", sorted(len(v) for v in fs.values()))
