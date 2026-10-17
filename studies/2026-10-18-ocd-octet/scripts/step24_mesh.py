# DICTO 2026-10-18 octet study -- STEP 24 check (dicto-node): outer corner minus the phi^-2 half-octahedron, split into connected parts.
import sys, json, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); RT = np.array(json.load(open(sys.argv[2]))['RT']); R = D['R']
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); env = hull(RT)
octa = hull([[s * R if i == j else 0 for j in range(3)] for i in range(3) for s in (1, -1)])
oc = max((octa - env).decompose(), key=lambda p: np.asarray(p.to_mesh().vert_properties[:, :3])[:, 2].mean())
pyr = octa ^ m3.Manifold.cube([3, 3, 3], True).translate([0, 0, 2 / 3 + 1.5])
left = oc - pyr; parts = sorted(left.decompose(), key=lambda p: -p.volume())
out = dict(outer=oc.volume(), pyramid=pyr.volume(), parts=[dict(volume=p.volume(), corners=np.unique(np.round(np.asarray(p.to_mesh().vert_properties[:, :3]), 6), axis=0).tolist()) for p in parts if p.volume() > 1e-12])
print(json.dumps({k: (v if k != 'parts' else [(round(x['volume'], 7), len(x['corners'])) for x in v]) for k, v in out.items()}))
json.dump(out, open(sys.argv[3], 'w'))
