# TI Star: an exhaustive list of the solids one turn makes, and how they nest (DICTO 10-30: "the cycle has not been exhaustive").
# Point sets: TI corners, the 12 pentagon tips (hull: icosahedron Ip), the 20 hexagon tips (hull: dodecahedron Dh), all 32 tips (hull K),
# s.TI. Solids: TI; TI + 12 pentagonal spikes; TI + 20 hexagonal spikes; the TI Star; Ip; Dh; Ip ∩ Dh; K; s.TI. For each pair: is one
# inside the other? For Ip ∩ Dh: its faces and whether it is a truncated icosahedron of the same shape as TI (scaled).
import json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
h = ConvexHull(P); F = []; seen = set()
for eq in h.equations:
    k = tuple(np.round(eq, 7))
    if k in seen: continue
    seen.add(k); F.append([i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8])
VT = h.volume
def planes(Q):
    hq = ConvexHull(Q); out = {}
    for eq in hq.equations: out.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(out.values()))
def face_kinds(Q):
    hq = ConvexHull(Q); c = {}
    for eq in planes(Q):
        n = sum(1 for p in Q[hq.vertices] if abs(eq[:3] @ p + eq[3]) < 1e-7); c[n] = c.get(n, 0) + 1
    return dict(sorted(c.items()))
res = {}
for name, s in [('2', 2.0), ('phi', phi)]:
    pen = np.array([s * P[f].mean(0) for f in F if len(f) == 5]); hexa = np.array([s * P[f].mean(0) for f in F if len(f) == 6])
    spikes_p = [np.vstack([P[f], s * P[f].mean(0)]) for f in F if len(f) == 5]; spikes_h = [np.vstack([P[f], s * P[f].mean(0)]) for f in F if len(f) == 6]
    Ip, Dh = planes(pen), planes(hexa)
    core = HalfspaceIntersection(np.vstack([Ip, Dh]), np.zeros(3)).intersections; core = core[ConvexHull(core).vertices]
    S = {  # name: list of convex parts (a solid is the union of its parts)
        'TI': [P], 'TI+12 pentagonal spikes': [P] + spikes_p, 'TI+20 hexagonal spikes': [P] + spikes_h, 'TI Star': [P] + spikes_p + spikes_h,
        'Ip ∩ Dh': [core], 'Ip (icosahedron of the 12 pentagon tips)': [pen], 'Dh (dodecahedron of the 20 hexagon tips)': [hexa],
        'K (hull of the 32 tips)': [np.vstack([pen, hexa])], 's·TI': [s * P]}
    convex = {k: (len(v) == 1) for k, v in S.items()}
    def inside(A, B):   # every part of A inside convex B (B must be one convex part)
        Bp = planes(B[0]); return all(np.max(Q @ Bp[:, :3].T + Bp[:, 3]) <= 1e-9 for Q in A)
    names = list(S); rel = []
    for a, b in itertools.permutations(names, 2):
        if convex[b] and inside(S[a], S[b]): rel.append((a, b))
    # direct covers (a inside b with nothing strictly between)
    cover = [(a, b) for a, b in rel if not any((a, c) in rel and (c, b) in rel for c in names if c not in (a, b))]
    # the core: face kinds and whether it is similar to TI
    ck = face_kinds(core); rc = np.linalg.norm(core, axis=1)
    e = sorted({round(np.linalg.norm(core[i] - core[j]), 7) for i, j in itertools.combinations(range(len(core)), 2)})[:3]
    vol = {k: (sum(ConvexHull(Q).volume for Q in v) if len(v) > 1 else ConvexHull(v[0]).volume) / VT for k, v in S.items()}
    vol['TI Star'] = s; vol['TI+12 pentagonal spikes'] = 1 + (s - 1) * 12 * 1.3347684105728597 / ((125 + 43 * 5 ** .5) / 4)
    vol['TI+20 hexagonal spikes'] = 1 + (s - 1) * 20 * 1.9635254915624212 / ((125 + 43 * 5 ** .5) / 4)
    res[name] = dict(volumes_over_TI={k: round(v, 6) for k, v in vol.items()}, nesting_covers=cover,
                     core=dict(corners=len(core), faces=ck, radius_spread=float(np.ptp(rc)), shortest_distances=e,
                               similar_to_TI=bool(ck == {5: 12, 6: 20} and np.ptp(rc) < 1e-7 and abs(e[0] - e[1]) < 1e-7 if len(e) > 1 else False)),
                     K_also_Ip_plus_20_pyramids=inside([hexa], [np.vstack([pen, hexa])]) and bool(np.all([np.max(p @ Ip[:, :3].T + Ip[:, 3]) > 1e-9 for p in hexa])))
print(json.dumps(res, indent=1, ensure_ascii=False)); json.dump(res, open('data/stations-turn.json', 'w'), indent=1, ensure_ascii=False)
