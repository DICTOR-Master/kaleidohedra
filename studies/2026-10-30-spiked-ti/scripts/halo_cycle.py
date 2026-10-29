# Star Halo cycle (DICTO 10-30: "run the K cycle first"). Start from the Star Halo K (hull of the 32 tips of the Golden or Double TI Star)
# and treat it as TI was treated: over each of its 60 triangles a spike whose tip is t times the foot of the perpendicular from the centre
# (t = 2: the mirrored face pyramid; t = phi: golden). Check: the hull of the 60 tips (is it the 1/phi^3 core shape, i.e. the polar of K?),
# the nesting K ⊂ Halo Star ⊂ hull ⊂ t·K, and the fills: layer 1 = over each corner of K the pyramid to the tips of its faces, over each
# edge the tetrahedron (edge + 2 tips); layer 2 = the same with the corners and edges of t·K. Volumes and overlaps (separating axis).
import json, itertools, os, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
SRC = os.environ.get('SRC', 'phi'); T = os.environ.get('T', 'phi')
s_src = {'phi': phi, '2': 2.0}[SRC]; t = {'phi': phi, '2': 2.0}[T]
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def facelist(Q):
    hq = ConvexHull(Q); out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(Q) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    return list(out.values())
FT = facelist(P)
K = np.array([s_src * P[ids].mean(0) for _, ids in FT])
KF = facelist(K)
dists = sorted({round(-eq[3], 9) for eq, _ in KF})
tips = [t * (-eq[3]) * eq[:3] for eq, _ in KF]          # t x foot of the perpendicular
TP = np.array(tips)
def pl(Q):
    u = {}
    for eq in ConvexHull(Q).equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
cut = lambda H: (lambda W: W[ConvexHull(W).vertices])(HalfspaceIntersection(H, np.zeros(3)).intersections)
H = TP[ConvexHull(TP).vertices]; HF = facelist(TP)
kinds = {}
for eq, ids in HF: kinds[len(ids)] = kinds.get(len(ids), 0) + 1
# the 1/phi^3 core of the TI Star turn (same s as the source), and the polar of K
pen = np.array([s_src * P[ids].mean(0) for _, ids in FT if len(ids) == 5]); hexa = np.array([s_src * P[ids].mean(0) for _, ids in FT if len(ids) == 6])
core = cut(np.vstack([pl(pen), pl(hexa)]))
def shape(Q):
    V = Q[ConvexHull(Q).vertices]; V = V / np.linalg.norm(V, axis=1).max()
    d = np.linalg.norm(V[:, None] - V[None], axis=2); m = d[d > 1e-9].min()
    return (len(V), tuple(sorted({round(x, 5) for x in d[(d > 1e-9) & (d < 1.6 * m)].ravel()})), tuple(sorted({round(x, 6) for x in np.linalg.norm(V, axis=1)})))
hull_is_core_shape = shape(TP) == shape(core)
scale_to_core = np.linalg.norm(TP, axis=1).max() / np.linalg.norm(core, axis=1).max()
# fills
KV = K; fa = {v: [fi for fi, (_, ids) in enumerate(KF) if v in ids] for v in range(len(KV))}
E = sorted({tuple(sorted(e)) for _, ids in KF for e in itertools.combinations(ids, 2)
            if len([fi for fi, (_, j) in enumerate(KF) if e[0] in j and e[1] in j]) == 2})
vol = lambda Q: ConvexHull(Q).volume
L1 = [np.vstack([KV[v]] + [tips[f] for f in fa[v]]) for v in range(len(KV))] + \
     [np.vstack([KV[a], KV[b]] + [tips[f] for f in fa[a] if f in fa[b]]) for a, b in E]
L2 = [np.vstack([t * KV[v]] + [tips[f] for f in fa[v]]) for v in range(len(KV))] + \
     [np.vstack([t * KV[a], t * KV[b]] + [tips[f] for f in fa[a] if f in fa[b]]) for a, b in E]
spikes = [np.vstack([KV[ids], tips[fi]]) for fi, (_, ids) in enumerate(KF)]
VK = vol(K); VH = vol(TP); star = VK + sum(vol(Q) for Q in spikes)
inside = lambda A, B: bool(np.all(A @ pl(B)[:, :3].T + pl(B)[:, 3] <= 1e-9))
res = dict(source=SRC, t=T, K_face_distances=dists, K_corners=len(K), K_faces=len(KF), K_edges=len(E),
           tips=len(tips), hull_corners=len(H), hull_faces=kinds, hull_is_core_shape=bool(hull_is_core_shape), hull_over_core_scale=scale_to_core,
           volumes_over_K=dict(K=1, halo_star=star / VK, hull=VH / VK, tK=t ** 3),
           star_inside_hull=all(inside(Q, TP) for Q in spikes) and inside(K, TP), hull_inside_tK=inside(TP, t * K),
           layer1=dict(pieces=len(L1), kinds=sorted({round(vol(Q), 9) for Q in L1}), sum=sum(map(vol, L1)), needed=VH - star),
           layer2=dict(pieces=len(L2), kinds=sorted({round(vol(Q), 9) for Q in L2}), sum=sum(map(vol, L2)), needed=t ** 3 * VK - VH))
# overlaps
pieces = [K] + spikes + L1 + L2
def axes(Q):
    hq = ConvexHull(Q); n = [eq[:3] for eq in hq.equations]
    ed = {tuple(sorted((a, b))) for sm in hq.simplices for a, b in [(sm[0], sm[1]), (sm[1], sm[2]), (sm[0], sm[2])]}
    return n, [Q[b] - Q[a] for a, b in ed]
AX = [axes(Q) for Q in pieces]; C = [Q.mean(0) for Q in pieces]; Rr = [np.linalg.norm(Q - Q.mean(0), axis=1).max() for Q in pieces]
def sep(i, j):
    A_, B_ = pieces[i], pieces[j]
    for ax in AX[i][0] + AX[j][0] + [np.cross(u, v) for u in AX[i][1] for v in AX[j][1]]:
        nn = np.linalg.norm(ax)
        if nn < 1e-12: continue
        pa, pb = A_ @ (ax / nn), B_ @ (ax / nn)
        if pa.max() <= pb.min() + 1e-9 or pb.max() <= pa.min() + 1e-9: return True
    return False
bad = [(i, j) for i, j in itertools.combinations(range(len(pieces)), 2) if np.linalg.norm(C[i] - C[j]) <= Rr[i] + Rr[j] + 1e-9 and not sep(i, j)]
res['pieces'] = len(pieces); res['overlaps'] = len(bad)
print(json.dumps(res, indent=1, default=float)); json.dump(res, open(f'data/halo-cycle-{SRC}-{T}.json', 'w'), indent=1, default=float)
