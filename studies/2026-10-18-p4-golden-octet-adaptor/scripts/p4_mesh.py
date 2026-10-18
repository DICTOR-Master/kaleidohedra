# DICTO 2026-10-18 golden octet adaptor -- mesh (dicto-node, manifold3d): adaptor = rhombic dodecahedron minus the golden envelope.
# One solid? genus (holes), sphericity; symmetry check of the inversion (achiral). usage: python3 p4_mesh.py step22-input.json R OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
RT = np.array(json.load(open(sys.argv[1]))['RT']); R = float(sys.argv[2])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
RD = hull([[R * a, R * b, R * c] for a, b, c in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]] + [[R * a / 2, R * b / 2, R * c / 2] for a, b, c in itertools.product((1, -1), repeat=3)])
env = hull(RT); ad = RD - env
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
inv = ad.transform(np.c_[-np.eye(3), np.zeros(3)])
me = ad.to_mesh(); e = env.to_mesh(); r = RD.to_mesh()
out = dict(volume=ad.volume(), parts=len([p for p in ad.decompose() if p.volume() > 1e-9]), genus=ad.genus(), sphericity=sph(ad), rd_sphericity=sph(RD),
           centrosymmetric=abs((inv ^ ad).volume() - ad.volume()) < 1e-9,
           adaptor=dict(v=np.round(np.asarray(me.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(me.tri_verts).tolist()),
           envelope=dict(v=np.round(np.asarray(e.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(e.tri_verts).tolist()))
print({k: v for k, v in out.items() if k not in ('adaptor', 'envelope')}); json.dump(out, open(sys.argv[3], 'w'))
# the adaptor is a closed shell round the envelope (genus -1: a cavity). To assemble it must open: split by the mirror plane z = 0 into two
# halves (congruent: the half-turn about the x axis maps one onto the other, a symmetry of the envelope frame).
top = ad.trim_by_plane([0, 0, 1], 0.0); bot = ad.trim_by_plane([0, 0, -1], 0.0)
out['halves'] = dict(top_volume=top.volume(), bottom_volume=bot.volume(), top_parts=len([p for p in top.decompose() if p.volume() > 1e-9]),
                     top_sphericity=sph(top), congruent_by_half_turn=abs((top.transform(np.c_[np.diag([1, -1, -1]), np.zeros(3)]) ^ bot).volume() - bot.volume()) < 1e-9)
tm = top.to_mesh(); out['half'] = dict(v=np.round(np.asarray(tm.vert_properties[:, :3], float), 6).tolist(), t=np.asarray(tm.tri_verts).tolist())
print('halves', out['halves']); json.dump(out, open(sys.argv[3], 'w'))
