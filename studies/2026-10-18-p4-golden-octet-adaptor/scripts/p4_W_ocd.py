# DICTO 2026-10-18 "like this last Fable W particularly, and face could be exact imprint of OCD?!" -- W with OCD imprints:
# W_OCD = rhombic dodecahedron round the octet vertex (0,0,R) minus the OCDs biting into it (instead of their envelopes).
# The vertex RDs tile space, so OCD + W_OCD fill space exactly by construction (every point outside the OCDs lies in exactly one vertex RD).
# Checks (dicto-node): one solid? volume (expect cell - OCD), sphericity, centrosymmetric (inversion through the vertex), contact faces.
# usage: python3 p4_W_ocd.py step10-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; L = np.array(D['L'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
v = np.array([0, 0, R])
RD = hull([v + R * np.array(a) for a in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]] + [v + R / 2 * np.array(s) for s in itertools.product((1, -1), repeat=3)])
OCD = hull(V); sh = [np.array(c) @ L for c in itertools.product(range(-2, 3), repeat=3)]
bites = [t for t in sh if np.linalg.norm(t - v) < 2.5 and (RD ^ OCD.translate(t)).volume() > 1e-9]
W = RD - U([OCD.translate(t) for t in bites])
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
inv = W.translate(-v).transform(np.c_[-np.eye(3), np.zeros(3)]).translate(v)
cell = abs(np.linalg.det(L))
me = W.to_mesh()
out = dict(volume=W.volume(), expected=cell - OCD.volume(), parts=len([p for p in W.decompose() if p.volume() > 1e-9]), genus=W.genus(), sphericity=sph(W),
           centrosymmetric=abs((inv ^ W).volume() - W.volume()) < 1e-9, ocds_biting=len(bites),
           v=np.round(np.asarray(me.vert_properties[:, :3], float) - v, 6).tolist(), t=np.asarray(me.tri_verts).tolist())
print({k: out[k] for k in ('volume', 'expected', 'parts', 'genus', 'sphericity', 'centrosymmetric', 'ocds_biting')}); json.dump(out, open(sys.argv[2], 'w'))
