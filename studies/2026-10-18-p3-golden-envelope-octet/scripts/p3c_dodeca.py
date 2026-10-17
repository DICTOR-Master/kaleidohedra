# DICTO 2026-10-18 Project 3c (cuboctahedron + dodecahedron set) -- step 1, exact: the central dodecahedron of the cut-down tetrahedron
# (largest cell of octet step 26: 20 corners, 12 pentagons) -- exact corners, faces, edge lengths, symmetry (rotations / mirrors of T+),
# and volume. Writes data/p3c-dodeca.json (exact + float corners for the node split).
import sys, os, itertools, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '2026-10-18-ocd-octet', 'scripts'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '2026-10-18-ocd-octet', 'scripts'))
src = open('step26_tet_plane_trick.py').read().split('summary = [')[0]
exec(src)
OUT = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0] if sys.argv[0] else '.')), '..', 'data')
big, vb = max(kept, key=lambda cv: qf(cv[1]))
Cf = np.array([[qf(x) for x in p] for p in big]); hh = ConvexHull(Cf)
faces = []
for e in np.unique(np.round(hh.equations, 9), axis=0):
    idx = [i for i in range(len(big)) if abs(Cf[i] @ e[:3] + e[3]) < 1e-9]
    c = Cf[idx].mean(0); u = Cf[idx[0]] - c; w = np.cross(e[:3], u); idx = [idx[k] for k in np.argsort(np.arctan2((Cf[idx] - c) @ w, (Cf[idx] - c) @ u))]
    faces.append(idx)
edges2 = sorted({qs_(dot(vsub(big[f[k]], big[f[(k + 1) % len(f)]]), vsub(big[f[k]], big[f[(k + 1) % len(f)]]))) for f in faces for k in range(len(f))}, key=lambda s: qf(q(s)))
def ang(f, k):
    a, b, c = big[f[k - 1]], big[f[k]], big[f[(k + 1) % len(f)]]; u, w = vsub(a, b), vsub(c, b)
    return round(math.degrees(math.acos(qf(dot(u, w)) / math.sqrt(qf(dot(u, u)) * qf(dot(w, w))))), 3)
angles = sorted({ang(f, k) for f in faces for k in range(len(f))})
cen = vmul(vadd(vadd(Tp[0], Tp[1]), vadd(Tp[2], Tp[3])), qr(Fr(1, 4)))
rel = [vsub(p, cen) for p in big]; relf = np.array([[qf(x) for x in p] for p in rel])
def has(M): return all(np.min(np.linalg.norm(relf - (M @ x), axis=1)) < 1e-9 for x in relf)
ax = (Cf.mean(0) - np.array([qf(x) for x in cen]))
rots = [np.array(Pm) * np.array(s)[:, None] for Pm in itertools.permutations(np.eye(3)) for s in itertools.product((1, -1), repeat=3)]
sym = [M for M in rots if has(M)]
checks = dict(corners=len(big), faces=len(faces), face_sizes=sorted({len(f) for f in faces}), edge_lengths2=edges2, edge_lengths=[round(qf(q(s)) ** .5, 6) for s in edges2],
              face_angles=angles, volume=qs_(vb), volume_float=qf(vb), centred_at_tet_centre=bool(np.allclose(ax, 0)),
              cube_symmetries_kept=len(sym), proper=sum(1 for M in sym if np.linalg.det(M) > 0), improper=sum(1 for M in sym if np.linalg.det(M) < 0))
print(json.dumps(checks, indent=1))
json.dump(dict(mark=MARK, step='p3c-1', checks=checks, corners=[[qs_(x) for x in p] for p in big], corners_float=Cf.tolist(), faces=faces),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)) if False else '/home/dicto/kaleidohedra/studies/2026-10-18-p3-golden-envelope-octet/data', 'p3c-dodeca.json'), 'w'), indent=1)
