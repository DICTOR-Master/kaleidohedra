import math, itertools, sys, numpy as np
from collections import Counter
from scipy.spatial import ConvexHull, HalfspaceIntersection
sys.argv = [sys.argv[0], 'x', '8', '300']; exec(open('scripts/dehn.py').read().split("if __name__")[0])
P0 = np.array(sorted({tuple(s*v for s, v in zip(sg, p)) for p in itertools.permutations((1, 2, 3)) for sg in itertools.product((1, -1), repeat=3)}), float)
a = np.array([1, 1, 1])/math.sqrt(3); z = np.array([0, 0, 1.]); v = np.cross(a, z); K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); Rz = np.eye(3) + K + K @ K*((1 - a @ z)/np.linalg.norm(v)**2)
P = P0 @ Rz.T; h = ConvexHull(P)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
def half(top):
    Hs = np.vstack([h.equations, [0, 0, -1 if top else 1, 0]]); return HalfspaceIntersection(Hs, np.array([0, 0, 1e-3 if top else -1e-3])).intersections
T, B = half(True), half(False)
sec = np.unique(np.round(T[np.abs(T[:, 2]) < 1e-7], 6), axis=0); print('cut section corners', len(sec), 'side lengths', sorted({round(float(np.linalg.norm(p - q)), 4) for p, q in itertools.combinations(sec, 2)})[:3])
for nm, U in (('permutohedron', P), ('twisted permutohedron', np.unique(np.round(np.vstack([T, B @ rz(math.pi/3).T]), 6), axis=0))):
    hu = ConvexHull(U); X = U[hu.vertices]; X, F = hull_faces(X)
    # merge coplanar facets robustly: hull_faces groups by rounded plane
    conv = abs(hu.volume - h.volume) < 1e-6*h.volume
    rows = dehn(X, F, rows_only=True); angs = Counter(round(math.degrees(t), 3) for L, t in rows); d = dehn(X, F)
    print(f'{nm}: convex {conv}, corners {len(X)}, faces {sorted(Counter(len(f) for f in F).items())}, dihedrals {dict(sorted(angs.items()))}, Dehn zero {d["dehn_zero"]}')
