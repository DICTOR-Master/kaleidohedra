# DICTO 2026-10-18 octet study -- STEP 19 meshes (dicto-node, manifold3d): keyless middle piece M0 split into the three Penrose cores
# and the rest. Checks: volumes vs the exact values, is the rest one solid (and its genus), sphericity of each piece, and are the two
# flanking cores the same piece or mirror images (search for a proper rotation taking one onto the other, Kabsch on vertex triples).
# usage: python3 step19_mesh.py step10-input.json step19-input.json OUT.json
import sys, json, itertools, numpy as np, manifold3d as m3
D = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2]))
V = np.array(D['V']); R = D['R']; hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
OCD = hull(V); r = np.linalg.norm(V, axis=1)
i1 = [i for i in range(len(V)) if r[i] > r.max() - 1e-9 and abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
o = np.array([0, R, R]); star = V[sorted({j for f in D['faces'] if i1 in f for j in f})]
M0 = hull(np.vstack([star, o - star])) - OCD - OCD.translate(o)
ax = np.array(C['a']); ax /= np.linalg.norm(ax)
cores = {k: M0 ^ hull(np.vstack([np.array(Q) - ax, np.array(Q) + ax])) for k, Q in C['rhombi'].items()}
rest = M0
for k in cores: rest = rest - cores[k]
sph = lambda mf: np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
out = {}
for k, mf in list(cores.items()) + [('rest', rest), ('M0', M0)]:
    parts = sorted([p.volume() for p in mf.decompose()], reverse=True)
    out[k] = dict(volume=mf.volume(), sphericity=sph(mf), parts=len([p for p in parts if p > 1e-9]), genus=mf.genus())
    print(k, {x: round(y, 6) if isinstance(y, float) else y for x, y in out[k].items()}, flush=True)
def verts(mf):
    P = np.asarray(mf.to_mesh().vert_properties[:, :3], float); return np.unique(np.round(P, 7), axis=0)
def proper_match(A, B, tol=1e-5):
    ca, cb = A.mean(0), B.mean(0); A0, B0 = A - ca, B - cb
    if len(A) != len(B): return False
    i0 = np.argsort(-np.linalg.norm(A0, axis=1))[:3]; a = A0[i0]
    da = [np.linalg.norm(a[0] - a[1]), np.linalg.norm(a[0] - a[2]), np.linalg.norm(a[1] - a[2])]
    for p in itertools.permutations(range(len(B0)), 3):
        b = B0[list(p)]
        if abs(np.linalg.norm(b[0]) - np.linalg.norm(a[0])) > tol: continue
        if any(abs(x - y) > tol for x, y in zip(da, [np.linalg.norm(b[0] - b[1]), np.linalg.norm(b[0] - b[2]), np.linalg.norm(b[1] - b[2])])): continue
        H_ = a.T @ b; U, S_, Wt = np.linalg.svd(H_); Rm = Wt.T @ U.T
        if np.linalg.det(Rm) < 0: continue
        AR = A0 @ Rm.T
        if all(np.min(np.linalg.norm(B0 - x, axis=1)) < tol for x in AR): return True
    return False
f1, f2 = verts(cores['flank1']), verts(cores['flank2'])
out['flanks_same_piece_by_rotation'] = proper_match(f1, f2)
out['flank1_mirror_matches_flank2'] = proper_match(f1 * np.array([-1, 1, 1]), f2)
print('flanks same by rotation:', out['flanks_same_piece_by_rotation'], ' flank1 mirrored matches flank2:', out['flank1_mirror_matches_flank2'])
json.dump(out, open(sys.argv[3], 'w'))
