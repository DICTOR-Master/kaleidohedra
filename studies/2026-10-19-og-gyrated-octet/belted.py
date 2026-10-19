# The belted envelope (DICTO 2026-10-19: a shape of its own): the golden envelope (rhombic triacontahedron of inradius 2/3 round the OG,
# #37 frame) cut flat by the two octahedron faces x+y+z = +-R (R = 2phi/3) on one three-fold axis; float description first.
import numpy as np, itertools, json
from scipy.spatial import ConvexHull, HalfspaceIntersection
PHI = (1 + 5 ** .5) / 2; R = 2 * PHI / 3
D = json.load(open('../2026-10-18-ocd-octet/data/step1-ocd-exact.json'))
q = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
V = np.array([[q(c) for c in v] for v in D['V']]); r = np.linalg.norm(V, axis=1); u5 = V[r > r.max() - 1e-9]; u5 /= np.linalg.norm(u5, axis=1)[:, None]
ang = np.max(u5[0] @ u5[1:].T); E = [(i, j) for i, j in itertools.combinations(range(12), 2) if abs(u5[i] @ u5[j] - ang) < 1e-9]
N = np.array([(u5[i] + u5[j]) / np.linalg.norm(u5[i] + u5[j]) for i, j in E]); n3 = np.ones(3) / 3 ** .5
H = np.vstack([np.hstack([N, -np.full((30, 1), 2 / 3)]), [*n3, -R / 3 ** .5], [*-n3, -R / 3 ** .5]])
P = HalfspaceIntersection(H, np.zeros(3)).intersections; P = np.unique(np.round(P, 10), axis=0)
h = ConvexHull(P); RTv = ConvexHull(HalfspaceIntersection(H[:30], np.zeros(3)).intersections).volume
faces = {}
for k, eq in enumerate(H):
    on = np.where(np.abs(P @ eq[:3] + eq[3]) < 1e-9)[0]
    if len(on) >= 3: faces[k] = on
kinds = {}
for k, on in faces.items(): kinds[len(on)] = kinds.get(len(on), 0) + 1
nE = sum(len(on) for on in faces.values()) // 2
print('corners', len(P), '| faces', len(faces), 'by corner count', kinds, '| edges', nE, '| Euler', len(P) - nE + len(faces))
tri = P[faces[30]]; sides = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(tri, 2))
RTedge = None
apex = P[np.argmax(P @ n3)] if False else None
print('volume', round(h.volume, 6), '| envelope', round(RTv, 6), '| cut off', round(RTv - h.volume, 6), '(2 keys = 0.017812)')
print('pole triangle sides', np.round(sides, 6))
# where the cut meets the envelope's edges: fraction along the edge from the three-fold corner
Hf = HalfspaceIntersection(H[:30], np.zeros(3)).intersections; Hf = np.unique(np.round(Hf, 10), axis=0); top = Hf[np.argmax(Hf @ n3)]
nb = [p for p in Hf if abs(np.linalg.norm(p - top) - np.min([np.linalg.norm(x - top) for x in Hf if np.linalg.norm(x - top) > 1e-9])) < 1e-9]
edge = np.linalg.norm(nb[0] - top); t = (top @ n3 - R / 3 ** .5) / ((top - nb[0]) @ n3)
print('envelope edge', round(edge, 6), '| cut at fraction', round(t, 6), 'of each edge from the pole corner; 1/phi^4 =', round(PHI ** -4, 6), ' 1/phi^3 =', round(PHI ** -3, 6), ' 1/(2phi^2)=', round(1 / (2 * PHI * PHI), 6))
print('sphericity', round(np.pi ** (1 / 3) * (6 * h.volume) ** (2 / 3) / h.area, 4), '| height pole to pole', round(2 * R / 3 ** .5, 6), 'width (5-fold corner span)', round(2 * np.max(np.linalg.norm(P - np.outer(P @ n3, n3), axis=1)), 6))
