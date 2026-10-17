# DICTO 2026-10-18 octet study -- STEP 14: do the three Penrose prisms (step 13) fit the middle region in 3D? (float, sampling)
# Each prism = the rhombus footprint run along the five-fold axis a, from the surface of OCD 1 to the surface of OCD 2.
# For a grid of footprint points: does the axis line meet both OCDs (so the column is closed at both ends)? does the column between
# them stay inside the star hull H (the middle region)? does it hit a key? Column volumes vs the middle piece. -> data/step14-fit.json
import itertools, numpy as np
from scipy.spatial import ConvexHull
from q5 import *
S1 = load('step1-ocd-exact.json'); S5 = load('step5-keyed-octet.json'); pe = load('step13-penrose.json'); mesh = load('step10-meshes.json')
V = np.array([[qf(q(x)) for x in v] for v in S1['V']]); R = qf(q(S1['R'])); E_o = ConvexHull(V).equations
r = np.linalg.norm(V, axis=1); i1 = [i for i in range(len(V)) if r[i] > r.max() - 1e-9 and abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
c1 = V[i1]; o = np.array([0, R, R]); a = c1 / np.linalg.norm(c1); ub = np.cross(a, [1, 0, 0]); ub /= np.linalg.norm(ub); wb = np.cross(a, ub)
star = V[sorted({j for f in S1['faces'] if i1 in f for j in f})]; E_h = ConvexHull(np.vstack([star, o - star])).equations
keys = [ConvexHull(np.array([[qf(q(x)) for x in p] for p in K])).equations for K in S5['keys'].values()]
keys = [(E, np.zeros(3)) for E in keys] + [(E, o) for E in keys]
def tspan(x0, Eq, sh):   # t interval of the line x0 + t a inside {n.(x - sh) + d <= 0}
    nA = Eq[:, :3] @ a; b = -(Eq[:, :3] @ (x0 - sh) + Eq[:, 3]); lo, hi = -np.inf, np.inf
    for k in range(len(Eq)):
        if abs(nA[k]) < 1e-14:
            if b[k] < 0: return None
        elif nA[k] > 0: hi = min(hi, b[k] / nA[k])
        else: lo = max(lo, b[k] / nA[k])
    return (lo, hi) if lo < hi else None
rng = np.random.default_rng(2); out = {}; total_vol = 0
for name, Q in pe['patch'].items():
    Q = np.array(Q); e1, e2 = Q[1] - Q[0], Q[3] - Q[0]; area = abs(e1[0] * e2[1] - e1[1] * e2[0]); N = 4000
    UV = rng.random((N, 2)); pts2 = Q[0] + UV[:, :1] * e1 + UV[:, 1:] * e2
    closed = inH = clear = 0; heights = []
    for p2 in pts2:
        x0 = c1 + p2[0] * ub + p2[1] * wb
        s1 = tspan(x0, E_o, np.zeros(3)); s2 = tspan(x0, E_o, o)
        if s1 is None or s2 is None or s2[0] <= s1[1]: continue
        closed += 1; t1, t2 = s1[1], s2[0]; heights.append(t2 - t1)
        ts = np.linspace(t1, t2, 25)[1:-1]; X = x0 + np.outer(ts, a)
        if np.all(X @ E_h[:, :3].T + E_h[:, 3] <= 1e-9): inH += 1
        hit = False
        for Eq, sh in keys:
            sp = tspan(x0, Eq, sh)
            if sp and sp[1] > t1 + 1e-12 and sp[0] < t2 - 1e-12: hit = True; break
        clear += not hit
    vol = area * np.mean(heights) * closed / N if heights else 0; total_vol += vol
    out[name] = dict(footprint_area=area, closed_both_ends=closed / N, column_inside_hull=inH / max(closed, 1), column_clear_of_keys=clear / max(closed, 1),
                     height_min=float(min(heights)) if heights else None, height_max=float(max(heights)) if heights else None, column_volume=vol)
out['all_three_volume'] = total_vol; out['middle_piece_volume'] = mesh['middle']['volume']; out['share_of_middle'] = total_vol / mesh['middle']['volume']
print(json.dumps(out, indent=1)); save('step14-fit.json', dict(mark=MARK, step=14, status='float sampling', fit=out))
