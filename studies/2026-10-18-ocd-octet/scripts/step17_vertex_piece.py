# DICTO 2026-10-18 octet study -- STEP 17 (dicto-node, manifold3d): merge caps with middle rests into one vertex piece per octet vertex,
# then score every piece's chunkiness by sphericity psi = pi^(1/3) (6V)^(2/3) / A.
# usage: python3 step17_vertex_piece.py step10-input.json step15-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2]))
V = np.array(D['V']); R = D['R']; L = np.array(D['L']); Tp = np.array(D['Tp']); hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
OCD = hull(V); keyed = U([OCD] + [hull(K) for K in D['keys'].values()])
r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
shifts = [np.array(ijk) @ L for ijk in itertools.product(range(-2, 3), repeat=3)]
def Mi(i):
    c = V[i]; o = R * np.sign(np.where(np.abs(c) < 1e-9, 0, c)); star = V[sorted({j for f in D['faces'] if i in f for j in f})]
    return hull(np.vstack([star, o - star])) - keyed - keyed.translate(o)
Mb = {i: Mi(i) for i in five}; Mall = U([Mb[i].translate(s) for s in shifts if np.linalg.norm(s) < 2.3 for i in five])
corner = hull([[0, 0, 0], [0, 0, R], [R/2, 0, R/2], [-R/2, 0, R/2], [0, R/2, R/2], [0, -R/2, R/2]] + [[a*R/3, b*R/3, R/3] for a in (1, -1) for b in (1, -1)])
cap = corner - OCD - Mall
i1 = [i for i in five if abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]; o1 = np.array([0, R, R]); m = o1 / 2
rh = np.array(C['rh']); a = np.array(C['a']); a /= np.linalg.norm(a); prism = hull(np.vstack([rh - a, rh + a]))
M1 = Mb[i1]; core = M1 ^ prism; rest = M1 - prism
allkeys = U([keyed.translate(s) for s in shifts if np.linalg.norm(s) < 2.3]); T = hull(Tp) - allkeys - Mall
# Th ops (cyclic permutations x sign flips) as 3x3 matrices
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        G = np.zeros((3, 3))
        for i in range(3): G[i, pm[i]] = sg[i]
        ops.append(G)
def place(mf, G, t): return mf.transform(np.c_[G, t])
def is_lattice(t): x = np.linalg.solve(L.T, t); return np.allclose(x, np.round(x), atol=1e-9)
v = np.array([0, 0, R])
# the 6 caps at v: octahedron centres v -+ R e_i, cap pointing from centre c to v
caps = []
for c in [v - R * e for e in np.eye(3)] + [v + R * e for e in np.eye(3)]:
    dvec = (v - c) / R; G = next(G for G in ops if np.allclose(G @ [0, 0, 1], dvec) and is_lattice(c - G @ np.zeros(3)))
    caps.append(place(cap, G, c))
# the 12 half-rests at v: edges (v, v + w), w = R(+-1, +-1, 0) perms; rest at base edge (0,R,0)-(0,0,R), midpoint m, direction (0,1,-1)
halves = []; base_dir = np.array([0, 1, -1.0])
for w in {tuple(R * np.array(p) * s) for p in ([1, 1, 0], [1, -1, 0], [1, 0, 1], [1, 0, -1], [0, 1, 1], [0, 1, -1]) for s in (1, -1)}:
    w = np.array(w); p = v + w / 2; found = None
    for G in ops:
        gd = G @ base_dir
        if np.allclose(np.abs(gd), np.abs(w / R)) and (np.allclose(gd, w / R) or np.allclose(gd, -w / R)):
            t = p - G @ m
            if is_lattice(t): found = (G, t); break
    assert found, w
    G, t = found; piece = place(rest, G, t)
    n = (v - p) / np.linalg.norm(v - p); half = piece.trim_by_plane(n.tolist(), float(n @ p))   # keep the side towards v
    halves.append(half)
vertex = U(caps + halves)
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
out = {}
for k, mf in (('keyed_OCD', keyed), ('vertex_piece', vertex), ('penrose_core', core), ('tetrahedron', T), ('old_cap', cap), ('old_middle_rest', rest), ('bare_OCD', OCD)):
    parts = sorted([p.volume() for p in mf.decompose()], reverse=True)
    out[k] = dict(volume=mf.volume(), area=mf.surface_area(), sphericity=sph(mf), parts=len([p for p in parts if p > 1e-9]))
    print(f"{k:16s} V {mf.volume():.6f}  psi {sph(mf):.3f}  parts {out[k]['parts']}", flush=True)
mesh = vertex.to_mesh(); out['vertex_mesh'] = dict(v=np.round(mesh.vert_properties[:, :3] - v, 6).tolist(), t=mesh.tri_verts.tolist())
out['check_vertex_volume'] = dict(expected=6 * cap.volume() + 6 * rest.volume(), got=vertex.volume())
json.dump(out, open(sys.argv[3], 'w'))
