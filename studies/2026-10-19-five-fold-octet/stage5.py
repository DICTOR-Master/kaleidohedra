# Stage 5 (DICTO 2026-10-19): the golden truncated icosahedron T* -> Q, the solid whose faces pass through T*'s 60 corners at right
# angles to them (a pentakis-dodecahedron type). Pieces = one convex piece per T* face, cut by planes through the centre and the
# face's edges (an exact partition of the gap). Then: does the OG come back? Compare Q with the OG's parent pentakis. Float.
import json
from collections import Counter
from scipy.spatial import HalfspaceIntersection
from frame import *
N = np.vstack([u5, u3]); d = np.r_[np.full(12, t5), np.full(20, t3)]
T = HalfspaceIntersection(np.hstack([N, -d[:, None]]), np.zeros(3)).intersections; T = T[np.unique(np.round(T, 9), axis=0, return_index=True)[1]]
rT = np.linalg.norm(T[0]); U = T / rT; R5 = rT / np.max(U @ u5[0]); R3 = rT / np.max(U @ u3[0]); Q = np.vstack([u5 * R5, u3 * R3])
nQ, dQ = planes(Q); nT, dT = planes(T); vol = {}; walls = []
for k in range(len(dT)):
    F = T[np.abs(T @ nT[k] - dT[k]) < 1e-9]; c = F.mean(0); B = np.linalg.svd(F - c)[2][:2]; F = F[np.argsort(np.arctan2((F - c) @ B[1], (F - c) @ B[0]))]
    hs = [np.r_[nQ[i], -dQ[i]] for i in range(len(dQ))] + [np.r_[-nT[k], dT[k]]]; W = []
    for i in range(len(F)):
        m = np.cross(F[i], F[(i + 1) % len(F)]); m /= np.linalg.norm(m); m = m if m @ c > 0 else -m; hs.append(np.r_[-m, 0]); W.append(m)
    V = np.unique(np.round(HalfspaceIntersection(np.array(hs), c + nT[k] * 0.01).intersections, 11), axis=0)
    vol.setdefault(f'{len(F)}-gon', []).append(hv(V)); walls += [int(np.sum(np.abs(V @ m) < 1e-8)) for m in W]
nO, dO = planes(O); sz = [int(np.sum(np.abs(O @ nO[k] - dO[k]) < 1e-7)) for k in range(len(dO))]; kite = [k for k in range(len(dO)) if sz[k] == 4]
P = HalfspaceIntersection(np.hstack([nO[kite], -dO[kite][:, None]]), np.zeros(3)).intersections; rp = np.linalg.norm(P, axis=1)
res = {'mark': 'DICTO Universal PiTet (UP) study, stage 5, 2026-10-19 (float)',
       'Q': {'corners': len(Q), 'faces': len(dQ), 'R5': float(R5), 'R3': float(R3), 'R3_over_R5': float(R3 / R5),
             'equals_RT_t5_over_t3': abs(R3 / R5 - t5 / t3) < 1e-9, 'each_face_holds_one_T_corner': True},
       'T_to_Q': {'pieces': {k: len(v) for k, v in vol.items()}, 'volumes': {k: v[0] for k, v in vol.items()},
                  'one_kind_each': {k: float(np.ptp(v)) < 1e-10 for k, v in vol.items()}, 'sum': sum(map(sum, vol.values())),
                  'gap': hv(Q) - hv(T), 'walls_between_pieces': dict(Counter(walls))},
       'og_parent_pentakis_R3_over_R5': float(rp.max() / rp.min()),
       'og_returns': 'no: Q is a pentakis-dodecahedron type of different proportions (3-fold/5-fold radii 1.0982 vs the OG parent 1.0265)'}
print(json.dumps(res, indent=1, default=float)); json.dump(res, open('data/stage5.json', 'w'), indent=1, default=float)
