# A, icosahedral (DICTO 2026-10-27: "the Hexa was the inspiration, not the shape; icosahedral was the idea"; "render the 20 corner
# version"): 20 Icosaxes, one on each corner of a dodecahedron, each turned by the icosahedral rotation that carries (1,1,1) there
# (its hexagon then faces straight out, as each Jewel of the Hexa faces a corner of the cube). Distance from the centre d: from first
# touch inward, so neighbours pass into each other. Reports overlaps and the joined solid; writes T<k>-union.obj for render depths.
import json, itertools, numpy as np, manifold3d as mf, trimesh
PHI = (1 + 5 ** .5) / 2
I0 = np.array(json.load(open('H2.json'))[0]['vertices'])                  # the Icosaxes at the origin (golden-split frame)
ICO = np.array([p for s in itertools.product([1, -1], repeat=2) for p in [(0, s[0] * .5, s[1] * PHI / 2), (s[0] * .5, s[1] * PHI / 2, 0), (s[1] * PHI / 2, 0, s[0] * .5)]])
def rotations():                                                           # all 60 rotations taking the icosahedron to itself
    a, b = ICO[0], next(q for q in ICO if abs(np.linalg.norm(q - ICO[0]) - 1) < 1e-9)
    out = []
    for A in ICO:
        for B in ICO:
            if abs(np.linalg.norm(A - B) - 1) > 1e-9: continue
            M = np.array([A, B, np.cross(A, B)]).T @ np.linalg.inv(np.array([a, b, np.cross(a, b)]).T)
            if abs(np.linalg.det(M) - 1) < 1e-6 and all(np.min(np.linalg.norm(ICO - M @ p, axis=1)) < 1e-6 for p in ICO): out.append(M)
    return out
R = rotations(); assert len(R) == 60, len(R)
u = np.ones(3) / 3 ** .5; sites = {}
for M in R:
    key = tuple(np.round(M @ u, 6))
    sites.setdefault(key, M)                                                # the 3-fold turn about u keeps the Icosaxes, so one per corner
assert len(sites) == 20
def pieces(d): return [mf.Manifold.hull_points(I0 @ M.T + d * (M @ u)) for M in sites.values()]
def stats(d):
    P = pieces(d); v1 = P[0].volume()
    ov = [(P[i] ^ P[j]).volume() for i, j in itertools.combinations(range(20), 2)]
    U = mf.Manifold.batch_boolean(P, mf.OpType.Add)
    return P, U, v1, sum(o for o in ov if o > 1e-7), sum(o > 1e-7 for o in ov)
lo, hi = 0.5, 6.0                                                           # first touch: the largest d with an overlap
for _ in range(40):
    mid = (lo + hi) / 2
    if stats(mid)[3] > 1e-7: lo = mid
    else: hi = mid
touch = hi; print(f'first touch at d = {touch:.6f} (piece volume {stats(touch)[2]:.6f})')
rows = []
for k, f in enumerate([1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6]):
    d = touch * f; P, U, v1, ov, n = stats(d)
    T = U.to_mesh(); t = trimesh.Trimesh(T.vert_properties[:, :3], T.tri_verts); t.merge_vertices()
    hollow = U.genus(), len(U.decompose())
    print(f'T{k} d={d:.4f} ({f:.2f} of touch): overlapping pairs {n}, overlap {ov:.4f}, joined volume {U.volume():.4f}, genus {U.genus()}, '
          f'parts {len(U.decompose())}, closed {t.is_watertight}, flat faces {len(t.facets) + len(t.faces) - sum(len(x) for x in t.facets)}, '
          f'centre filled {(U ^ mf.Manifold.cube([0.02] * 3, True)).volume() > 1e-9}')
    t.export(f'T{k}-union.obj')
