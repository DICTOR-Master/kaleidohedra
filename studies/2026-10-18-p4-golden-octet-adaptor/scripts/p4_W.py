# DICTO 2026-10-18 -- Fable's glue W (fable-review-2, I1) for the 3D page: the rhombic dodecahedron round the octet vertex v = (0,0,R)
# minus the golden envelopes biting into it (dicto-node, manifold3d). usage: python3 p4_W.py step22-input.json step10-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
RT = np.array(json.load(open(sys.argv[1]))['RT']); D = json.load(open(sys.argv[2])); R = D['R']; L = np.array(D['L'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
v = np.array([0, 0, R])
RD = hull([v + R * np.array(a) for a in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]] + [v + R / 2 * np.array(s) for s in itertools.product((1, -1), repeat=3)])
env = hull(RT); sh = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
W = RD - U([env.translate(t) for t in sh if np.linalg.norm(t - v) < 2.5])
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
me = W.to_mesh()
out = dict(volume=W.volume(), parts=len([p for p in W.decompose() if p.volume() > 1e-9]), sphericity=sph(W),
           v=np.round(np.asarray(me.vert_properties[:, :3], float) - v, 6).tolist(), t=np.asarray(me.tri_verts).tolist())
print({k: out[k] for k in ('volume', 'parts', 'sphericity')}); json.dump(out, open(sys.argv[3], 'w'))
