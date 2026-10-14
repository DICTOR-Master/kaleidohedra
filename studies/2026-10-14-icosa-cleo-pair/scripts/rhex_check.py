# DICTO 2026-10-14 "check RHex": do the 20 golden rhombohedra on the icosahedron's faces (each Cleo-Icos + Antonius + Cleo-Icos) make the
# rhombic hexecontahedron? Compare with Polyhedraverse's TRANS_BODHI_B2 (Bodhi Seed Kit B, stage 2) after scaling.
import itertools, json, sys
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
phi = (1 + 5 ** .5) / 2
V = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float) / 5 ** .5
E = 2 / 5 ** .5
faces = [t for t in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(V[a] - V[b]) - E) < 1e-9 for a, b in itertools.combinations(t, 2))]
rh = []
for a, b, c in faces:
    u, v, w = V[a], V[b], V[c]; rh.append(np.array([np.zeros(3), u, v, w, u + v, v + w, w + u, u + v + w]))
vols = [ConvexHull(R).volume for R in rh]; cleo = ConvexHull(np.array([np.zeros(3), *rh[0][1:4]])).volume
rng = np.random.default_rng(1); X = rng.uniform(-2.2, 2.2, (400000, 3)); D = [Delaunay(R) for R in rh]
cnt = sum((d.find_simplex(X) >= 0).astype(int) for d in D)
pts = np.unique(np.round(np.vstack(rh), 6), axis=0); r = np.round(np.linalg.norm(pts, axis=1), 3)
ours = sorted(r[r > 1e-6].tolist())
data = json.load(open(sys.argv[1])); P = np.array(data['v'], float); P -= P.mean(0); rp = np.linalg.norm(P, axis=1)
k = max(ours) / rp.max(); theirs = sorted(np.round(rp * k, 3).tolist())
union_vol = (cnt >= 1).mean() * 4.4 ** 3; theirs_vol = ConvexHull(P).volume  # (convex hull only as a sanity bound)
out = dict(rhombohedra=len(rh), each_over_cleo=round(vols[0] / cleo, 9), overlap_points=int((cnt > 1).sum()),
           union_volume_mc=round(union_vol, 3), sum_volumes=round(sum(vols), 4), total_over_cleo=round(sum(vols) / cleo, 6),
           corners_ours=len(ours), corners_bodhi=len(theirs), radius_profile_match=ours == theirs, scale=k,
           radii=sorted(set(ours)), bodhi_faces=len(data['f']))
print(json.dumps(out, indent=1)); json.dump(out, open('studies/2026-10-14-icosa-cleo-pair/rhex-check.json', 'w'), indent=1)
