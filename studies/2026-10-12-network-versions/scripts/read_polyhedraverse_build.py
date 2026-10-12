import json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.transform import Rotation
S = json.load(open('shapes.json')); B = json.load(open(sys.argv[1]))['stores']['worldpoly']['nodes']
PHI = (1 + 5 ** .5) / 2
def place(n):
    V = np.array(S[n['shape']]); q = n['transform']['quaternion']
    return Rotation.from_quat(q).apply(V) + np.array(n['transform']['position'])
P = [(n['shape'].replace('GOLDEN_RHOMBOHEDRON_', '').replace('RHOMBIC_TRIACONTAHEDRON', 'RT'), place(n)) for n in B]
el = lambda W: min(np.linalg.norm(W[0] - w) for w in W[1:])
print('edges:', {k: round(el(W), 6) for k, W in P})
def axes(W):
    H = ConvexHull(W); F = H.equations[:, :3]; E = []
    for s in H.simplices:
        for a, b in itertools.combinations(s, 2): E.append(W[a] - W[b])
    return F, E
def overlap(A, B_):
    FA, EA = axes(A); FB, EB = axes(B_); ax = list(FA) + list(FB)
    dirs = {tuple(np.round(e / np.linalg.norm(e), 6)) for e in EA + EB}
    dirs = [np.array(d) for d in dirs]
    for u, v in itertools.combinations(dirs, 2):
        w = np.cross(u, v)
        if np.linalg.norm(w) > 1e-6: ax.append(w / np.linalg.norm(w))
    depth = 1e9
    for a in ax:
        p, q = A @ a, B_ @ a
        d = min(p.max() - q.min(), q.max() - p.min())
        if d <= 1e-6: return 0.0
        depth = min(depth, d)
    return depth
ov = [(i, j, round(overlap(P[i][1], P[j][1]), 4)) for i, j in itertools.combinations(range(len(P)), 2)]
ov = [o for o in ov if o[2] > 0]
print('overlapping pairs:', len(ov)); [print('  ', P[i][0], i, P[j][0], j, 'depth', d) for i, j, d in ov[:20]]
RT = [W for k, W in P if k == 'RT']; C = np.array([W.mean(0) for W in RT]); c0 = C.mean(0)
r = np.linalg.norm(C - c0, axis=1); print('12 RT centres: distance from their middle', np.round(np.sort(r), 4), '; Bodhi value phi^2 =', round(PHI ** 2, 4))
d = np.linalg.norm(C[:, None] - C[None], axis=2); print('nearest RT-RT centre distances:', np.round(np.sort(d + np.eye(12) * 99, axis=1)[:, :5], 3)[:3])
rh = [(k, W) for k, W in P if k != 'RT']
inside = [k for k, W in rh if np.linalg.norm(W.mean(0) - c0) < r.mean() - 0.5]
print('rhombohedra:', len(rh), '; with centre nearer the middle than the RTs:', len(inside), {k: inside.count(k) for k in set(inside)})
print('their volume', round(sum(ConvexHull(W).volume for k, W in rh if np.linalg.norm(W.mean(0) - c0) < r.mean() - 0.5), 4))
print('--- with the misplaced RT left out')
idx = [i for i, (k, W) in enumerate(P) if k == 'RT']; bad = 26
good = [P[i][1].mean(0) for i in idx if i != bad]
# the Bodhi middle: point equidistant (phi) from the 11 good centres, least squares
from scipy.optimize import least_squares
G = np.array(good); m = least_squares(lambda x: np.linalg.norm(G - x[:3], axis=1) - x[3], np.r_[G.mean(0), 1.6]).x
print('11 RT centres: distance from the fitted middle', np.round(np.linalg.norm(G - m[:3], axis=1), 5), '(Bodhi: phi =', round(PHI, 5), 'in app units, edge 1/phi)')
dirs = (G - m[:3]) / np.linalg.norm(G - m[:3], axis=1)[:, None]
miss = -dirs.sum(0); print('missing 12th direction (sum of the 11, reversed), length', round(np.linalg.norm(miss), 4), '; RT 26 centre offset from middle', np.round(P[bad][1].mean(0) - m[:3], 4), 'should be', np.round(miss / np.linalg.norm(miss) * PHI, 4))
rh_in = [(k, i, W) for i, (k, W) in enumerate(P) if k != 'RT' and np.linalg.norm(W.mean(0) - m[:3]) < 1.2]
print('rhombohedra within 1.2 of the middle:', len(rh_in), {k: sum(1 for kk, _, _ in rh_in if kk == k) for k in ('PROLATE', 'OBLATE')}, 'volume', round(sum(ConvexHull(W).volume for _, _, W in rh_in), 4),
      '; enclosed space in app units = 15.27..15.29 / phi^3 =', round(15.28 / PHI ** 3, 3))
