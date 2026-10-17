# Builds src/app/ocd-octet-data.js for two networks of the DICTO Icosahedral Octet world (DICTO 2026-10-18; research branch
# studies/2026-10-18-ocd-octet): the Ogdoecontahedron (OCD) in the octahedron of its 8 joint hexagons (|x|+|y|+|z| = 2phi/3, exact),
# with regular tetrahedra as the octet truss.
#   ocdOctet   "Octet with OCD": OCD + its 8 golden-envelope corners as keys (DICTO's choice), 6 caps, tetrahedra with 4 key dents
#              (3 shapes; the two tetrahedra are the same piece). Exact, study steps 1-5.
#   ocdPenrose "Octet with OCD and Penrose cores" (DICTO's name): + a middle piece on every octahedron edge between two facing five-fold
#              stars, trimmed round the keys, split into the Penrose core (thick Penrose rhombus prism) and the rest; caps and tetrahedra
#              notched; left and right tetrahedra. Exact volumes, study steps 6-15.
# Cells are in the octet world's frame (octahedra at (a/2)n, a = phi^2): scale 3phi/4. Each piece: [role, vertices, triangles, outline]
# (outline = its edges between faces that are not flat, so the triangulation does not show).
# Inputs (research checkout): studies/2026-10-18-ocd-octet/data/{step10-input,step15-input}.json. Needs manifold3d (dicto-node).
# Usage: python3 <this> <research checkout> <out.js>
import sys, json, itertools, numpy as np, manifold3d as m3
ROOT = sys.argv[1].rstrip('/') + '/studies/2026-10-18-ocd-octet/data/'
D = json.load(open(ROOT + 'step10-input.json')); C = json.load(open(ROOT + 'step15-input.json'))
PHI = (1 + 5 ** 0.5) / 2; K = 3 * PHI / 4
V = np.array(D['V']); R = D['R']; L = np.array(D['L']); Tp = np.array(D['Tp'])
assert abs(R * K - PHI ** 2 / 2) < 1e-12
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
OCD = hull(V); keyed = U([OCD] + [hull(Kp) for Kp in D['keys'].values()])
r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
shifts = [np.array(ijk) @ L for ijk in itertools.product(range(-2, 3), repeat=3)]
def Mi(i):
    c = V[i]; o = R * np.sign(np.where(np.abs(c) < 1e-9, 0, c)); star = V[sorted({j for f in D['faces'] if i in f for j in f})]
    return hull(np.vstack([star, o - star])) - keyed - keyed.translate(o)
Mb = {i: Mi(i) for i in five}; Mall = U([Mb[i].translate(s) for s in shifts if np.linalg.norm(s) < 2.3 for i in five])
allkeys = U([keyed.translate(s) for s in shifts if np.linalg.norm(s) < 2.3])
corner = hull([[0, 0, 0], [0, 0, R], [R/2, 0, R/2], [-R/2, 0, R/2], [0, R/2, R/2], [0, -R/2, R/2]] + [[a*R/3, b*R/3, R/3] for a in (1, -1) for b in (1, -1)])
capPlain = corner - OCD; capNotched = capPlain - Mall
T = hull(Tp); tetDent = T - allkeys; tetNotch = tetDent - Mall
i1 = [i for i in five if abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
rh = np.array(C['rh']); ax = np.array(C['a']); ax /= np.linalg.norm(ax); prism = hull(np.vstack([rh - ax, rh + ax]))
core1 = Mb[i1] ^ prism; rest1 = Mb[i1] - prism
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        G = np.zeros((3, 3))
        for i in range(3): G[i, pm[i]] = sg[i]
        ops.append(G)
tf = lambda mf, G: mf.transform(np.c_[G, np.zeros(3)])
caps = lambda cap: [tf(cap, next(G for G in ops if np.allclose(G @ [0, 0, 1], d))) for d in [s * e for e in np.eye(3) for s in (1, -1)]]
canon = [i for i in five if next(x for x in V[i] if abs(x) > 1e-9) > 0]
def at_corner(mf, i): return tf(mf, next(G for G in ops if np.allclose(G @ V[i1], V[i])))
def part(role, mf, centre):
    mesh = mf.to_mesh(); P = (np.asarray(mesh.vert_properties[:, :3], float) - centre) * K; Tr = np.asarray(mesh.tri_verts)
    n = np.cross(P[Tr[:, 1]] - P[Tr[:, 0]], P[Tr[:, 2]] - P[Tr[:, 0]]); area = np.linalg.norm(n, axis=1); keep = area > 1e-10
    Tr, n = Tr[keep], n[keep] / area[keep, None]
    edges = {}
    for t, nn in zip(Tr, n):
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])): edges.setdefault((min(a, b), max(a, b)), []).append(nn)
    outline = [list(map(int, e)) for e, ns in edges.items() if len(ns) != 2 or ns[0] @ ns[1] < 0.99999]
    used = sorted({int(x) for x in Tr.ravel()}); idx = {u: k for k, u in enumerate(used)}
    return [role, np.round(P[used], 5).tolist(), [[idx[int(x)] for x in t] for t in Tr], [[idx[a], idx[b]] for a, b in outline]]
z3 = np.zeros(3); ct = Tp.mean(0)
cells = {
    'ocdOct': [part('ocdKeyed', keyed, z3)] + [part('ocdCapPlain', c, z3) for c in caps(capPlain)],
    'ocdTet': [part('ocdTet', tetDent, ct)],
    'ocdOctPenrose': [part('ocdKeyed', keyed, z3)] + [part('ocdCap', c, z3) for c in caps(capNotched)]
                     + [part('penroseCore', at_corner(core1, i), z3) for i in canon] + [part('midRest', at_corner(rest1, i), z3) for i in canon],
    'ocdTetPenrose': [part('ocdTetL', tetNotch, ct)],
}
vols = dict(keyed=keyed.volume(), capPlain=capPlain.volume(), capNotched=capNotched.volume(), tetDent=tetDent.volume(), tetNotch=tetNotch.volume(),
            core=core1.volume(), rest=rest1.volume())
print({k: round(v, 6) for k, v in vols.items()})   # study (exact): 1.223113, 0.086940, 0.058072, 0.382754, 0.249486, 0.010129, 0.063162
for k, v in cells.items(): print(k, [(p[0], len(p[1]), len(p[2]), len(p[3])) for p in v][:4], len(v))
open(sys.argv[2], 'w').write('// Generated by scripts/build-ocd-octet-data.py (OCD octet, DICTO 2026-10-18; research studies/2026-10-18-ocd-octet). Do not edit.\n'
                             'export default ' + json.dumps({'scale': K, 'cells': cells}, separators=(',', ':')) + ';\n')
