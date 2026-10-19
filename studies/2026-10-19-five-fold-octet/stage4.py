# Stage 4 (DICTO 2026-10-19: "keep going outwards, but there may be missing transitional solids"): RT -> the solid whose faces
# pass through the RT's 32 corners at right angles to their axes (points meeting again). Pieces = one convex piece per RT rhombus,
# cut by the planes through the centre and the rhombus edges (an exact partition of the gap). Float.
import json
from collections import Counter
from scipy.spatial import HalfspaceIntersection
from frame import *
RT = np.vstack([u5 * t5, u3 * t3]); N = np.vstack([u5, u3]); d = np.r_[np.full(12, t5), np.full(20, t3)]
T = np.unique(np.round(HalfspaceIntersection(np.hstack([N, -d[:, None]]), np.zeros(3)).intersections, 12), axis=0)
nT, dT = planes(T); nR, dR = planes(RT)
E = sorted({round(float(np.linalg.norm(a - b)), 9) for a, b in itertools.combinations(T, 2)})
res = {'mark': 'DICTO five-fold octet study, stage 4, 2026-10-19 (float)',
       'next_solid': {'corners': len(T), 'faces': dict(Counter(int(np.sum(np.abs(T @ nT[k] - dT[k]) < 1e-7)) for k in range(len(dT)))),
                      'edges_short_long': E[:2], 'long_over_short_is_phi': abs(E[1] / E[0] - PHI) < 1e-9,
                      'corner_radius': float(np.linalg.norm(T[0])), 'pentagon_plane': float(t5), 'hexagon_plane': float(t3)}}
vols, walls = [], []
for k in range(len(dR)):
    q = RT[np.abs(RT @ nR[k] - dR[k]) < 1e-9]; c = q.mean(0); B = np.linalg.svd(q - c)[2][:2]
    q = q[np.argsort(np.arctan2((q - c) @ B[1], (q - c) @ B[0]))]
    hs = [np.r_[nT[i], -dT[i]] for i in range(len(dT))] + [np.r_[-nR[k], dR[k]]]; W = []
    for i in range(4):
        m = np.cross(q[i], q[(i + 1) % 4]); m /= np.linalg.norm(m); m = m if m @ c > 0 else -m; hs.append(np.r_[-m, 0]); W.append(m)
    V = np.unique(np.round(HalfspaceIntersection(np.array(hs), c + nR[k] * 0.02).intersections, 12), axis=0); vols.append(hv(V))
    walls += [int(np.sum(np.abs(V @ m) < 1e-8)) for m in W]
res['rt_to_next'] = {'pieces': 30, 'sum': sum(vols), 'gap': hv(T) - hv(RT), 'one_kind': float(np.ptp(vols)) < 1e-10,
                     'piece_volume': vols[0], 'volume_is_1_over_2phi2': abs(vols[0] - 1 / (2 * PHI ** 2)) < 1e-10,
                     'walls_between_pieces': dict(Counter(walls)),
                     'piece': 'rhombus below; on top 2 quadrilaterals (pentagon planes) and 2 pentagons (hexagon planes); 4 triangular walls'}
print(json.dumps(res, indent=1, default=float)); json.dump(res, open('data/stage4.json', 'w'), indent=1, default=float)
