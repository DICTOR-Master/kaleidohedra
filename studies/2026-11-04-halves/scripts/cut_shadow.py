"""Central band test (DICTO 4 Nov): a band (prism) between the halves keeps every twist convex iff the central cut equals the solid's shadow along the
axis ("cut equals shadow", #90). For each space-filler and axis: area of the central section vs area of the projection (shadow)."""
import math, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
def perms(v):
    return list({tuple(s*v[p[i]] for i, s in enumerate(sg)) for p in itertools.permutations(range(3)) for sg in itertools.product((1, -1), repeat=3)})
phi = (1 + 5**.5)/2; s3 = math.sqrt(3)
S = {'rhombic dodecahedron': perms((1, 0, 0)) + perms((.5, .5, .5)), 'truncated octahedron': perms((0, 1, 2)), 'cube': perms((1, 1, 1)),
     'B3 permutohedron': perms((1, 2, 3)), 'hexagonal prism': [(math.cos(k*math.pi/3), math.sin(k*math.pi/3), z) for k in range(6) for z in (-.5, .5)],
     'elongated dodecahedron': perms((1, 0, 0)) and [p for p in perms((.5, .5, .5))] + [(x, y, z + (0.5 if z > 0 else -0.5 if z < 0 else 0)) for x, y, z in perms((1, 0, 0))] + [(x, y, z + .5) for x, y, z in perms((.5, .5, .5)) if z > 0] + [(x, y, z - .5) for x, y, z in perms((.5, .5, .5)) if z < 0],
     '60° rhombohedron': [tuple(np.array(a)*i + np.array(b)*j + np.array(c)*k) for i in (0, 1) for j in (0, 1) for k in (0, 1) for a, b, c in [((1, 0, 0), (.5, s3/2, 0), (.5, 1/(2*s3), math.sqrt(2/3)))]]}
AX = {'2-fold (1,1,0)': (1, 1, 0), '3-fold (1,1,1)': (1, 1, 1), '4-fold (0,0,1)': (0, 0, 1)}
for name, V in S.items():
    P = np.unique(np.round(np.array(V, float), 9), axis=0); P = P - P[ConvexHull(P).vertices].mean(0); h = ConvexHull(P)
    out = []
    for an, a in AX.items():
        a = np.array(a, float)/np.linalg.norm(a); u = np.cross(a, [1, 0, 0] if abs(a[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(a, u)
        sh = ConvexHull(np.c_[P @ u, P @ w]).volume
        Hs = np.vstack([h.equations, [*a, 0], [*(-a), 0]])   # section: the polygon h ∩ {a·x = 0}
        try:
            X = HalfspaceIntersection(np.vstack([h.equations, [*a, -1e-9], [*(-a), -1e-9]]), np.zeros(3)).intersections
            sec = ConvexHull(np.c_[X @ u, X @ w]).volume
        except Exception: sec = float('nan')
        out.append(f"{an}: cut/shadow {sec/sh:.4f}{'  = CUT EQUALS SHADOW' if abs(sec/sh - 1) < 1e-6 else ''}")
    print(f"{name:26s} " + ' | '.join(out))
