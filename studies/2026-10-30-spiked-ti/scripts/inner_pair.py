# TI Star: the inner Platonic pair of each turn. D_TI = the dodecahedron of the 12 pentagon planes of TI, I_TI = the icosahedron of
# its 20 hexagon planes; TI = D_TI ∩ I_TI. Check their place among the solids of the turn (TI, TI Star, core, Ip, Dh, K, s·TI) and that
# the growth rule applied to Ip and Dh gives s·D_TI and s·I_TI.
import json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
h = ConvexHull(P); planes = {}
for eq in h.equations: planes.setdefault(tuple(np.round(eq, 7)), eq)
EQ = np.array(list(planes.values())); VT = h.volume
nper = [sum(1 for p in P if abs(eq[:3] @ p + eq[3]) < 1e-8) for eq in EQ]
cut = lambda H: (lambda W: W[ConvexHull(W).vertices])(HalfspaceIntersection(H, np.zeros(3)).intersections)
D_TI = cut(EQ[[n == 5 for n in nper]]); I_TI = cut(EQ[[n == 6 for n in nper]])
def pl(Q):
    u = {}
    for eq in ConvexHull(Q).equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
def rel(A, B):
    d = A @ pl(B)[:, :3].T + pl(B)[:, 3]
    if np.all(d <= 1e-9): return 'inside'
    d2 = B @ pl(A)[:, :3].T + pl(A)[:, 3]
    if np.all(d2 <= 1e-9): return 'contains'
    return 'crosses'
def grow(Q):
    V = Q[ConvexHull(Q).vertices]; r = np.linalg.norm(V, axis=1); return cut(np.hstack([V / r[:, None], -r[:, None]]))
out = {}
for SCN, s in [('phi', phi), ('2', 2.0)]:
    F = []; seen = set()
    for eq in h.equations:
        k = tuple(np.round(eq, 7))
        if k in seen: continue
        seen.add(k); F.append([i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    tips = [s * P[f].mean(0) for f in F]
    pen = np.array([t for t, f in zip(tips, F) if len(f) == 5]); hexa = np.array([t for t, f in zip(tips, F) if len(f) == 6])
    core = cut(np.vstack([pl(pen), pl(hexa)])); K = np.vstack([pen, hexa]); star_pts = np.vstack([P] + tips)
    S = {'TI': P, 'D_TI': D_TI, 'I_TI': I_TI, 'core': core, 'Ip': pen, 'Dh': hexa, 'K': K, 's·TI': s * P}
    rels = {f'{a} vs {b}': rel(S[a], S[b]) for a, b in itertools.combinations(S, 2)}
    g1 = grow(pen); g2 = grow(hexa)
    same = lambda A, B: abs(ConvexHull(A).volume - ConvexHull(B).volume) < 1e-9 * ConvexHull(B).volume and rel(A, B) == 'inside'
    out[SCN] = dict(volumes={k: round(ConvexHull(v).volume / VT, 6) for k, v in S.items()}, relations=rels,
                    rule_Ip_is_sD_TI=bool(same(g1, s * D_TI)), rule_Dh_is_sI_TI=bool(same(g2, s * I_TI)),
                    TI_is_D_TI_and_I_TI=bool(abs(ConvexHull(cut(np.vstack([pl(D_TI), pl(I_TI)]))).volume - VT) < 1e-9),
                    D_TI_corners=len(D_TI), I_TI_corners=len(I_TI),
                    spikes_tips_vs_D_TI=int(np.sum(np.max(np.array(tips) @ pl(D_TI)[:, :3].T + pl(D_TI)[:, 3], axis=1) > 1e-9)))
print(json.dumps(out, indent=1, ensure_ascii=False)); json.dump(out, open('data/inner-pair.json', 'w'), indent=1, ensure_ascii=False)
