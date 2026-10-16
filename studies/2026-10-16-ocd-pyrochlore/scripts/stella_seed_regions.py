# DICTO OCD Stella seed: a principled kit attempt (float). Each body gets a region of the outer form φ²S bounded by separating planes:
# copy i vs centre: x·v̂_i = |v|/φ (supports both, at the corner contact v_i/φ); copy i vs touching copy j: the face plane where they meet
# (gauge 1); copy vs outer: the outer form itself. Centre region: x·v̂_i ≤ |v|/φ for all i. Test: do the 13 regions tile the outer form
# (volumes sum, pairwise no overlap, each holds its body)? If so, region − body splits into convex cone pieces from the body's centre.
# -> data/stella-seed-regions.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
R = json.load(open('data/stella-seed.json')); S = np.array(R['stella']['v']); PHI = (1 + 5 ** .5) / 2
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-8) for q in P): P.append(e)
    return np.array(P)
PS = planes(S); rr = np.linalg.norm(S, axis=1); far = S[rr > rr.max() - 1e-9]; L = np.linalg.norm(far[0])
def interior(H):
    A, b = H[:, :3], -H[:, 3]; r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    return (r.x[:3], r.x[3]) if r.success else (None, 0)
def poly(H):
    x, r = interior(H)
    return HalfspaceIntersection(H, x).intersections if r > 1e-9 else None
OUT = np.c_[PS[:, :3], PS[:, 3] * PHI ** 2]
reg = []
cen = np.vstack([OUT] + [np.r_[v / L, -L / PHI] for v in far])          # x·v̂ ≤ |v|/φ
reg.append(cen)
for i, v in enumerate(far):
    H = [OUT, np.r_[-v / L, L / PHI][None, :]]                              # x·v̂_i ≥ |v|/φ
    for j, w in enumerate(far):
        if i == j: continue
        x = PHI * (v - w) / 2; g = max((PS[:, :3] @ x) / (-PS[:, 3]))
        if abs(g - 1) > 1e-6: continue                                       # only touching neighbours
        k = int(np.argmax((PS[:, :3] @ x) / (-PS[:, 3])))                      # face of copy i facing copy j: normal n with n·(w − v) < 0 ...
        n = PS[k, :3]; d = -PS[k, 3]
        # the contact plane: face of copy j with normal n at n·x = d + n·φw ... copy i is on the side n·x ≥ n·φw + d? use the midpoint side
        c = n @ (PHI * (v + w) / 2)
        side = 1 if n @ (PHI * v) > c else -1
        H.append((np.r_[-side * n, side * c])[None, :])
    reg.append(np.vstack(H))
vols = []; bodies = [S / PHI] + [S + PHI * v for v in far]
for H, B in zip(reg, bodies):
    V = poly(H); vols.append(ConvexHull(V).volume if V is not None else 0)
inside = [bool(np.all(B @ H[:, :3].T + H[:, 3] <= 1e-7)) for H, B in zip(reg, bodies)]
over = 0.0
for a, b in itertools.combinations(range(13), 2):
    x, r = interior(np.vstack([reg[a], reg[b]])); over = max(over, r)
vO = ConvexHull(S * PHI ** 2).volume
out = ['DICTO · dictospheres.com', 'OCD Stella seed: regions by separating planes (float)',
       f'region volumes: centre {vols[0]:.6f}, copies {min(vols[1:]):.6f}..{max(vols[1:]):.6f}; sum {sum(vols):.6f} vs outer {vO:.6f}',
       f'each region holds its body: {all(inside)}; deepest overlap between regions {over:.2e}',
       f'tiles the outer form: {abs(sum(vols) - vO) < 1e-6 and over < 1e-7}']
print('\n'.join(out)); open('data/stella-seed-regions.txt', 'w').write('\n'.join(out) + '\n')
