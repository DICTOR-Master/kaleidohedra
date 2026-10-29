# The star chain (DICTO 10-30: "run the core next"). S0 = TI; S(n+1) = hull of the tips of the spikes of S(n), each tip t times the foot of
# the perpendicular from the centre to a face of S(n) (t = phi or 2). S1 = Star Halo, S2 = the 1/phi^3 core shape. For n = 0..6:
# corners, faces, radius ratio (outer/inner corners), edge-length ratio, shape match with every earlier member (up to scale), the
# volumes of the star and the hull, and the exact fill of both layers (corner pyramids over the tips of the faces at each corner, edge
# tetrahedra) with an overlap test.
import json, itertools, os, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2; T = os.environ.get('T', 'phi'); t = {'phi': phi, '2': 2.0}[T]; N = int(os.environ.get('N', '6'))
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def facelist(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    return V, list(out.values())
def shape(V):
    W = V / np.linalg.norm(V, axis=1).max(); d = np.linalg.norm(W[:, None] - W[None], axis=2); m = d[d > 1e-9].min()
    return (len(W), tuple(sorted({round(x, 5) for x in d[(d > 1e-9) & (d < 1.7 * m)].ravel()})), tuple(sorted({round(x, 6) for x in np.linalg.norm(W, axis=1)})))
def axes(Q):
    hq = ConvexHull(Q); n = [eq[:3] for eq in hq.equations]
    ed = {tuple(sorted((a, b))) for sm in hq.simplices for a, b in [(sm[0], sm[1]), (sm[1], sm[2]), (sm[0], sm[2])]}
    return n, [Q[b] - Q[a] for a, b in ed]
def overlaps(pieces):
    AX = [axes(Q) for Q in pieces]; C = [Q.mean(0) for Q in pieces]; Rr = [np.linalg.norm(Q - Q.mean(0), axis=1).max() for Q in pieces]
    bad = 0
    for i, j in itertools.combinations(range(len(pieces)), 2):
        if np.linalg.norm(C[i] - C[j]) > Rr[i] + Rr[j] + 1e-9: continue
        ok = False
        for ax in AX[i][0] + AX[j][0] + [np.cross(u, v) for u in AX[i][1] for v in AX[j][1]]:
            nn = np.linalg.norm(ax)
            if nn < 1e-12: continue
            pa, pb = pieces[i] @ (ax / nn), pieces[j] @ (ax / nn)
            if pa.max() <= pb.min() + 1e-9 or pb.max() <= pa.min() + 1e-9: ok = True; break
        bad += not ok
    return bad
vol = lambda Q: ConvexHull(Q).volume
S = P; rows = []; shapes = []
for n in range(N + 1):
    V, FL = facelist(S); sh = shape(V)
    kinds = {}
    for eq, ids in FL: kinds[len(ids)] = kinds.get(len(ids), 0) + 1
    match = [m for m, s2 in enumerate(shapes) if s2 == sh]; shapes.append(sh)
    tips = [t * (-eq[3]) * eq[:3] for eq, _ in FL]; TP = np.array(tips)
    fa = {v: [fi for fi, (_, ids) in enumerate(FL) if v in ids] for v in range(len(V))}
    E = sorted({tuple(sorted(e)) for _, ids in FL for e in itertools.combinations(ids, 2)
                if sum(1 for _, j in FL if e[0] in j and e[1] in j) == 2 and np.linalg.norm(V[e[0]] - V[e[1]]) > 1e-9})
    # keep only true edges: pairs adjacent on the boundary of both faces (consecutive corners)
    def is_edge(a, b):
        fs = [fi for fi in fa[a] if fi in fa[b]]
        if len(fs) != 2: return False
        m = (V[a] + V[b]) / 2; return all(abs(FL[f][0][:3] @ m + FL[f][0][3]) < 1e-8 for f in fs)
    E = [e for e in E if is_edge(*e)]
    spikes = [np.vstack([V[ids], tips[fi]]) for fi, (_, ids) in enumerate(FL)]
    star = vol(V) + sum(vol(Q) for Q in spikes); VH = vol(TP)
    L1 = [np.vstack([V[v]] + [tips[f] for f in fa[v]]) for v in range(len(V))] + [np.vstack([V[a], V[b]] + [tips[f] for f in fa[a] if f in fa[b]]) for a, b in E]
    L2 = [np.vstack([t * V[v]] + [tips[f] for f in fa[v]]) for v in range(len(V))] + [np.vstack([t * V[a], t * V[b]] + [tips[f] for f in fa[a] if f in fa[b]]) for a, b in E]
    s1, s2 = sum(map(vol, L1)), sum(map(vol, L2))
    ov = overlaps([V] + spikes + L1 + L2) if n <= 3 else None
    r = np.linalg.norm(V, axis=1)
    rows.append(dict(step=n, corners=len(V), faces=dict(sorted(kinds.items())), edges=len(E), radius_ratio=round(r.max() / r.min(), 9),
                     same_shape_as_steps=match, star_over_S=round(star / vol(V), 9), hull_over_S=round(VH / vol(V), 9),
                     layer1_exact=abs(s1 - (VH - star)) < 1e-9 * VH, layer2_exact=abs(s2 - (t ** 3 * vol(V) - VH)) < 1e-9 * VH,
                     pieces=1 + len(spikes) + len(L1) + len(L2), overlaps=ov, hull_scale_vs_S=round(np.linalg.norm(TP, axis=1).max() / r.max(), 9)))
    S = TP
print(json.dumps(rows, indent=1)); json.dump(rows, open(f'data/star-chain-{T}.json', 'w'), indent=1)
