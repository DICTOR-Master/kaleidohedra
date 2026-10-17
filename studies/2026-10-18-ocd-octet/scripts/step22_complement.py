# DICTO 2026-10-18 octet study -- STEP 22 (dicto-node, manifold3d): the space the golden envelopes leave in the octet (1 - 10/phi^6).
# Is it one connected web or separate pieces? If separate: how many kinds per cell, their volumes, sphericity, and are they convex?
# usage: python3 step22_complement.py step10-input.json step22-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); RT = np.array(json.load(open(sys.argv[2]))['RT']); L = np.array(D['L']); R = D['R']
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
env = hull(RT); sh = [np.array(c) @ L for c in itertools.product(range(-3, 4), repeat=3)]
allenv = U([env.translate(s) for s in sh if np.linalg.norm(s) < 3.6])
# a box round one lattice vertex v = (0,0,R) and round a tetrahedron centre, both well inside the envelope cloud
out = {}
for name, centre in (('vertex', np.array([0, 0, R])), ('tet_centre', np.array([R / 2, R / 2, R / 2])), ('edge_mid', np.array([0, R / 2, R / 2]))):
    box = m3.Manifold.cube([1.2 * R] * 3, True).translate(centre)
    comp = box - allenv; parts = comp.decompose()
    inner = [p for p in parts if all(np.all(np.abs(np.asarray(p.to_mesh().vert_properties[:, :3]) - centre) < 0.6 * R - 1e-6, axis=1))]
    out[name] = dict(parts_in_box=len(parts), parts_not_touching_box=len(inner),
                     inner=[dict(volume=p.volume(), sphericity=np.pi ** (1 / 3) * (6 * p.volume()) ** (2 / 3) / p.surface_area(),
                                 convex=abs(p.volume() - hull(np.asarray(p.to_mesh().vert_properties[:, :3])).volume()) < 1e-9,
                                 centre=np.asarray(p.to_mesh().vert_properties[:, :3]).mean(0).round(4).tolist()) for p in inner])
    print(name, out[name], flush=True)
json.dump(out, open(sys.argv[3], 'w'))
# the outer corner piece: the octahedron's +z corner region minus the envelope
corner = hull([[0, 0, 0], [0, 0, R], [R/2, 0, R/2], [-R/2, 0, R/2], [0, R/2, R/2], [0, -R/2, R/2]] + [[a*R/3, b*R/3, R/3] for a in (1, -1) for b in (1, -1)])
oc = corner - env; P = np.asarray(oc.to_mesh().vert_properties[:, :3])
Tp = np.array(D['Tp']); dt = hull(Tp) - allenv
for nm, p in (('outer_corner', oc), ('dented_tet', dt)):
    Pp = np.asarray(p.to_mesh().vert_properties[:, :3])
    out[nm] = dict(volume=p.volume(), parts=len([x for x in p.decompose() if x.volume() > 1e-9]), convex=abs(p.volume() - hull(Pp).volume()) < 1e-9,
                   sphericity=np.pi ** (1 / 3) * (6 * p.volume()) ** (2 / 3) / p.surface_area(), corners=len(np.unique(np.round(Pp, 7), axis=0)))
    print(nm, out[nm], flush=True)
out['envelope'] = dict(volume=env.volume(), sphericity=np.pi ** (1 / 3) * (6 * env.volume()) ** (2 / 3) / env.surface_area())
print('envelope', out['envelope'])
json.dump(out, open(sys.argv[3], 'w'))
out['outer_corner']['part_volumes'] = sorted([x.volume() for x in oc.decompose()], reverse=True)
out['outer_corner']['part_centres'] = [np.asarray(x.to_mesh().vert_properties[:, :3]).mean(0).round(4).tolist() for x in sorted(oc.decompose(), key=lambda x: -x.volume())][:4]
print('outer corner parts', out['outer_corner']['part_volumes'][:5], out['outer_corner']['part_centres'])
json.dump(out, open(sys.argv[3], 'w'))
# natural outer pieces: the octahedron minus the envelope, by connected parts (no cone cuts)
octa = hull([[s * R if i == j else 0 for j in range(3)] for i in range(3) for s in (1, -1)]); rest_o = octa - env
parts = sorted(rest_o.decompose(), key=lambda x: -x.volume())
out['octa_minus_envelope'] = dict(parts=len(parts), volumes=[x.volume() for x in parts], sphericity=[np.pi ** (1 / 3) * (6 * x.volume()) ** (2 / 3) / x.surface_area() for x in parts],
                                 convex=[abs(x.volume() - hull(np.asarray(x.to_mesh().vert_properties[:, :3])).volume()) < 1e-9 for x in parts])
print('octa minus envelope', {k: (np.round(v, 6).tolist() if k != 'convex' else v) for k, v in out['octa_minus_envelope'].items()})
json.dump(out, open(sys.argv[3], 'w'))
