# Exact-to-float check of H1/H2: piece volumes, every pairwise overlap (convex intersection), contacts (shared face area).
import json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
def hs(P): h = ConvexHull(P); return h.equations
def inter(P, Q):
    H = np.vstack([hs(P), hs(Q)]); c = (P.mean(0) + Q.mean(0)) / 2
    # interior point: try the midpoint, else no overlap of positive volume
    if not (H[:, :3] @ c + H[:, 3] < -1e-9).all(): return 0.0
    try: return ConvexHull(HalfspaceIntersection(H, c).intersections).volume
    except Exception: return 0.0
for name in sys.argv[1:]:
    J = json.load(open(name + '.json')); P = [np.array(p['vertices']) for p in J]
    vols = [ConvexHull(p).volume for p in P]; ov = {}
    for i, j in itertools.combinations(range(len(P)), 2):
        v = inter(P[i], P[j])
        if v > 1e-9: ov[(i, j)] = v
    print(name, 'pieces', [J[k]['role'] for k in range(len(J))].count('icosaxes'), 'Icosaxes; volumes', sorted(set(round(v, 6) for v in vols)),
          '| sum', round(sum(vols), 6), '| overlapping pairs', len(ov), 'total overlap', round(sum(ov.values()), 6), sorted(set(round(v, 6) for v in ov.values())))
# The joined solid (manifold3d): volume, closed, genus, faces after merging coplanar triangles; written as <name>-union.obj.
import manifold3d as mf, trimesh
for name in sys.argv[1:]:
    J = json.load(open(name + '.json')); U = None
    for p in J:

        m = mf.Manifold.hull_points(np.array(p['vertices']))
        U = m if U is None else U + m
    M = U.to_mesh(); t = trimesh.Trimesh(M.vert_properties[:, :3], M.tri_verts)
    t.merge_vertices(); facets = len(t.facets) + (len(t.faces) - sum(len(f) for f in t.facets))
    print(name, 'joined: volume', round(U.volume(), 6), '| closed', t.is_watertight, '| genus', U.genus(), '| flat faces', facets, '| corners', len(t.vertices))
    t.export(name + '-union.obj')
