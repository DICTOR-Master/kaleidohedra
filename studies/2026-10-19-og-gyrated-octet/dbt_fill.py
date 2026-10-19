# DICTO 2026-10-20: fill the space the DBT leaves in the gyrated octet (DBT unchanged). As #37 step 27 for the golden envelope:
# give every leftover point to its nearest site, piece = Voronoi region of the site minus the DBTs. Two choices of site:
#   tet  the tetrahedron centres (two per cell)          bip  the bipyramid centres = twin-plane face centres (one per cell)
# Float (manifold3d, dicto-node): volume, parts, sphericity, mirror-symmetric or not, congruence between sites.
import json, itertools, math, numpy as np, manifold3d as m3
from scipy.spatial import HalfspaceIntersection
H = '/home/dicto/dbt-exact/2026-10-19-og-gyrated-octet/'
fq = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
DB = np.array([[fq(c) for c in v] for v in json.load(open(H + 'dbt-exact.json'))['V']])
R = fq(json.load(open(H + '../2026-10-18-ocd-octet/data/step1-ocd-exact.json'))['R'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
sph = lambda mf: math.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
MIR = np.eye(3) - 2 / 3 * np.ones((3, 3)); mir = lambda k: (MIR, 2 * k * R / 3 * np.ones(3))
comp = lambda a, b: (a[0] @ b[0], a[0] @ b[1] + a[1])
LM = {0: (np.eye(3), np.zeros(3))}
for k in range(1, 4):
    for s in (1, -1): j = s * k; LM[j] = comp(mir(2 * j - s), LM[j - s])
cent0 = [np.array(c) * R for c in itertools.product(range(-4, 5), repeat=3) if sum(c) == 0]
pts = [np.array(c) * R for c in itertools.product(range(-2, 3), repeat=3) if sum(c) % 2]
e2 = 2 * R * R; T0 = []
sl = [p for p in pts if abs(abs(p.sum()) - R) < 1e-9]
for q in itertools.combinations(range(len(sl)), 4):
    Q = [sl[i] for i in q]
    if all(abs(np.dot(a - b, a - b) - e2) < 1e-9 for a, b in itertools.combinations(Q, 2)): T0.append(np.mean(Q, 0))
U1, U2 = np.array([1, -1, 0]) * R, np.array([0, 1, -1]) * R
tc0 = []   # layer-0 tetrahedron centres, repeated in the layer
for c in T0:
    for i in range(-4, 5):
        for j in range(-4, 5): tc0.append(c + i * U1 + j * U2)
tc0 = np.unique(np.round(tc0, 9), axis=0)
dbts, tets = [], []
for k, m in LM.items():
    for c in cent0:
        cc = m[0] @ c + m[1]
        if np.linalg.norm(cc) < 4.2 * R: dbts.append(hull(DB @ m[0].T + cc))
    for c in tc0:
        cc = m[0] @ c + m[1]
        if np.linalg.norm(cc) < 3.6 * R: tets.append(cc)
tets = np.unique(np.round(tets, 9), axis=0)
ALL = m3.Manifold.batch_boolean(dbts, m3.OpType.Add)
n1 = np.ones(3) / 3 ** .5
def layer_plane(p): return round((p.sum() / R - 1) / 2) * 2 + 1   # nearest odd k: the twin plane x+y+z = kR
bips = []
for t in tets:   # bipyramid centre: the tetrahedron's face centre on a twin plane
    k = layer_plane(t); f = t + ((k * R - t.sum()) / 3) * np.ones(3)
    if abs(f.sum() - k * R) < 1e-9 and abs(abs(t.sum() - k * R) - R / 2) < 1e-6: bips.append(f)
bips = np.unique(np.round(bips, 9), axis=0)
print('DBTs', len(dbts), 'tetrahedron centres', len(tets), 'bipyramid centres', len(bips))
def vor(S, i):
    c = S[i]; d = np.linalg.norm(S - c, axis=1); nb = S[(d > 1e-9) & (d < 2.6 * R)]
    hs = [np.r_[(p - c) / np.linalg.norm(p - c), -((p - c) / np.linalg.norm(p - c)) @ (p + c) / 2] for p in nb]
    return hull(HalfspaceIntersection(np.array(hs), c).intersections)
def mirror_sym(mf, c):   # mirror-symmetric in a plane through c? try the twin-plane mirror and the 3 vertical mirrors of the layer
    best = 1
    for n in [n1] + [np.cross(n1, e) / np.linalg.norm(np.cross(n1, e)) for e in np.eye(3)] + [np.cross(n1, np.cross(n1, e)) / np.linalg.norm(np.cross(n1, np.cross(n1, e))) for e in np.eye(3)]:
        A = np.eye(3) - 2 * np.outer(n, n); t = c - A @ c
        best = min(best, (mf.volume() - (mf.transform(np.hstack([A, t[:, None]])) ^ mf).volume()) / mf.volume())
    return best
for name, S in (('tet', tets), ('bip', bips)):
    i0 = int(np.argmin(np.linalg.norm(S, axis=1))); res = []
    for i in sorted(range(len(S)), key=lambda i: np.linalg.norm(S[i]))[:4]:
        P = vor(S, i) - ALL; parts = [p for p in P.decompose() if p.volume() > 1e-7]
        res.append((S[i], P, parts))
    for c, P, parts in res:
        print(f'{name} site {np.round(c / R, 3)}: piece {P.volume():.6f}, parts {len(parts)} {[round(p.volume(), 6) for p in parts]}, sphericity {sph(max(parts, key=lambda q: q.volume())):.3f}, mirror defect {mirror_sym(P, c):.4f}')
    a, b = res[0][1], res[1][1]
    print(f'  {name}: Voronoi cell {vor(S, i0).volume():.6f}; leftover per cell 1.129153 / {2 if name == "tet" else 1} = {1.129153 / (2 if name == "tet" else 1):.6f}')
    json.dump({'v': np.asarray(res[0][1].to_mesh().vert_properties[:, :3]).round(6).tolist(), 't': np.asarray(res[0][1].to_mesh().tri_verts).tolist(), 'c': res[0][0].tolist()}, open(H + f'dbt-fill-{name}.json', 'w'))
