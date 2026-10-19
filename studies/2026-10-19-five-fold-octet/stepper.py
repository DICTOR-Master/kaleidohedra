# The UP step as one rule (DICTO 2026-10-19): next solid = faces through every corner of the last, at right angles to that corner's
# direction ("points meeting"); pieces = one convex piece per face of the last solid, cut by planes through the centre and that
# face's edges (an exact partition of the gap). Used for stage 6 on, and to watch the 5/3 rhythm. Float.
import json, sys
from collections import Counter
from scipy.spatial import HalfspaceIntersection
from frame import *

def uniq(P): return P[np.unique(np.round(P, 9), axis=0, return_index=True)[1]]
def nxt(S):
    r = np.linalg.norm(S, axis=1); return uniq(HalfspaceIntersection(np.hstack([S / r[:, None], -r[:, None]]), np.zeros(3)).intersections)
def pieces(S, Snext):
    nS, dS = planes(S); nN, dN = planes(Snext); out = {}; walls = []
    for k in range(len(dS)):
        F = S[np.abs(S @ nS[k] - dS[k]) < 1e-9]; c = F.mean(0); B = np.linalg.svd(F - c)[2][:2]; F = F[np.argsort(np.arctan2((F - c) @ B[1], (F - c) @ B[0]))]
        hs = [np.r_[nN[i], -dN[i]] for i in range(len(dN))] + [np.r_[-nS[k], dS[k]]]; W = []
        for i in range(len(F)):
            m = np.cross(F[i], F[(i + 1) % len(F)]); m /= np.linalg.norm(m); m = m if m @ c > 0 else -m; hs.append(np.r_[-m, 0]); W.append(m)
        V = uniq(HalfspaceIntersection(np.array(hs), c + nS[k] * 1e-3).intersections)
        out.setdefault(f'on {len(F)}-gon', []).append(hv(V)); walls += [int(np.sum(np.abs(V @ m) < 1e-8)) for m in W]
    return out, walls
def describe(S):
    nS, dS = planes(S); fs = Counter(int(np.sum(np.abs(S @ nS[k] - dS[k]) < 1e-7)) for k in range(len(dS)))
    a5 = [float(dS[k]) for k in range(len(dS)) if np.max(np.abs(nS[k] @ u5.T)) > 1 - 1e-9]; a3 = [float(dS[k]) for k in range(len(dS)) if np.max(np.abs(nS[k] @ u3.T)) > 1 - 1e-9]
    c5 = [float(np.linalg.norm(v)) for v in S if np.max(np.abs(v @ u5.T)) / np.linalg.norm(v) > 1 - 1e-9]; c3 = [float(np.linalg.norm(v)) for v in S if np.max(np.abs(v @ u3.T)) / np.linalg.norm(v) > 1 - 1e-9]
    return {'corners': len(S), 'faces': dict(sorted(fs.items())), 'corner_radii': sorted({round(float(x), 6) for x in np.linalg.norm(S, axis=1)}),
            'five_fold': {'corner': c5[0] if c5 else None, 'face': a5[0] if a5 else None}, 'three_fold': {'corner': c3[0] if c3 else None, 'face': a3[0] if a3 else None}}

if __name__ == '__main__':
    RT = np.vstack([u5 * t5, u3 * t3]); S = nxt(nxt(RT))            # stage 4 and 5 again, then go on
    res = {'mark': 'DICTO Universal PiTet (UP) study, stage 6 on, 2026-10-19 (float)', 'stages': []}
    for st in range(6, 6 + int(sys.argv[1]) if len(sys.argv) > 1 else 7):
        N = nxt(S); pc, walls = pieces(S, N)
        res['stages'].append({'stage': st, 'from': describe(S), 'to': describe(N), 'pieces': {k: len(v) for k, v in pc.items()},
                              'volumes': {k: v[0] for k, v in pc.items()}, 'one_kind_each': {k: float(np.ptp(v)) < 1e-9 for k, v in pc.items()},
                              'sum': sum(map(sum, pc.values())), 'gap': hv(N) - hv(S), 'walls_between_pieces': dict(Counter(walls))})
        print(json.dumps(res['stages'][-1], default=float)); S = N
    json.dump(res, open('data/stage6on.json', 'w'), indent=1, default=float)
