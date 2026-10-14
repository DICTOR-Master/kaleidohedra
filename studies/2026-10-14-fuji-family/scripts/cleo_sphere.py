# Twenty CLEOs pointing inwards (DICTO, 2026-10-14). The icosidodecahedron of edge 1/phi has circumradius exactly 1. Join its centre
# to each of its 20 triangles: each piece has an equilateral base of edge 1/phi and three side edges 1, which is exactly CLEO. Join
# the centre to its 12 pentagons: 12 tall pentagonal pyramids (side edges 1, base edge 1/phi). Together they fill the
# icosidodecahedron, and the walls between them are the six decagonal wheels' golden triangles (centre + one edge). The icosahedral
# twin of the four hexagonal wheels cutting the cuboctahedron into 8 regular tetrahedra + 6 square pyramids. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
E = [(a, b) for a, b in itertools.combinations(range(12), 2) if abs(np.linalg.norm(ico[a] - ico[b]) - 2) < 1e-9]
V = np.array([(ico[a] + ico[b]) / 2 for a, b in E])
edge = min(np.linalg.norm(V[0] - V[i]) for i in range(1, 30)); V *= (1 / phi) / edge
H = ConvexHull(V); faces = []
for e in np.unique(np.round(H.equations, 9), axis=0):
    on = np.where(np.abs(V @ e[:3] + e[3]) < 1e-7)[0]; c = V[on].mean(0); a = V[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
    faces.append([int(i) for i in on[np.argsort(np.arctan2((V[on] - c) @ b, (V[on] - c) @ a))]])
R = np.linalg.norm(V, axis=1)
tri = [f for f in faces if len(f) == 3]; pen = [f for f in faces if len(f) == 5]
cleo_vol = (math.sqrt(5) - 1) / 24
vol_t = sum(ConvexHull(np.vstack([V[f], [0, 0, 0]])).volume for f in tri); vol_p = sum(ConvexHull(np.vstack([V[f], [0, 0, 0]])).volume for f in pen)
side = sorted({round(float(r), 9) for r in R}); base = sorted({round(float(np.linalg.norm(V[f[i]] - V[f[(i + 1) % len(f)]])), 9) for f in faces for i in range(len(f))})
out = dict(circumradius=side, edge=base, triangles=len(tri), pentagons=len(pen), CLEO_volume_each=vol_t / 20, CLEO_volume_exact=cleo_vol,
           pentagonal_pyramid_volume_each=vol_p / 12, total=vol_t + vol_p, icosidodecahedron_volume=H.volume,
           pentagonal_pyramid_height=float(np.linalg.norm(V[pen[0]].mean(0))))
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(ROOT, 'cleo-sphere.json'), 'w'), indent=1)
verts, F, T = [], [], []
for kind, L in (('w1', tri), ('w0', pen)):
    for f in L:
        P = np.vstack([V[f], [0, 0, 0]]); c = V[f].mean(0); Y = P + c * 0.45; base_i = len(verts); verts += Y.tolist(); k = len(f)
        F.append([base_i + i for i in range(k)][::-1]); T.append(kind)
        for i in range(k): F.append([base_i + i, base_i + (i + 1) % k, base_i + k]); T.append(kind)
json.dump({'cleo_sphere': dict(v=verts, f=F, t=T)}, open(os.path.join(ROOT, 'paper', 'figures', 'cleo-sphere.json'), 'w'))
