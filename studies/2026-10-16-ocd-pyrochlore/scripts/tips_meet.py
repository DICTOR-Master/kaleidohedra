# Step 15 (DICTO: the little X-shaped holes; "tips or tendrils meeting each other" instead of Dogstar holes). Exploratory, float.
# At each square-face centre four free hexagons face inward (two from each of the two copies on that cube axis). Each carries a
# Cleo-Ico tip (step 11); the tips collide. Trim each tip where it meets the others: keep the part closer to its own hexagon
# centre than to the other three (the symmetric cut). Shapes of the trimmed tips and of the faces where they meet.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
C = [np.array(P) for P in json.load(open('data/cleo-adapter.json'))]
R = json.load(open('data/network-render.json')); cube = np.array(R['cube']); G = json.load(open('data/gaps.json')); V = np.array(G['V'])
a_half = np.abs(V @ cube[0]).max()
best = None
for k in range(3):
    site = cube[k] * a_half; L = 2 * site
    mine = [P for P in C if np.linalg.norm(P[:3].mean(0) - site) < np.linalg.norm(P[:3].mean(0) + site)]   # tips on our side facing it
    mine = sorted(mine, key=lambda P: np.linalg.norm(P[3] - site))[:2]
    other = [P + L for P in C if np.linalg.norm(P[:3].mean(0) + site) < np.linalg.norm(P[:3].mean(0) - site)]
    other = sorted(other, key=lambda P: np.linalg.norm(P[3] - site))[:2]
    tips = mine + other; best = (site, tips); break
site, tips = best
bases = [P[:3].mean(0) for P in tips]
def trimmed(i):
    H = list(ConvexHull(tips[i]).equations)
    for j in range(4):
        if j != i:   # closer to base i than base j:  (b_j - b_i).x <= (|b_j|^2 - |b_i|^2)/2
            n = bases[j] - bases[i]; H.append(np.r_[n, -(bases[j] @ bases[j] - bases[i] @ bases[i]) / 2])
    H = np.array(H); nrm = np.linalg.norm(H[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    return np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0)
T = [trimmed(i) for i in range(4)]
def faces(P):
    h = ConvexHull(P); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    out = []
    for e in pl:
        Q = P[np.abs(P @ e[:3] + e[3]) < 1e-7]; c = Q.mean(0); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        Q = Q[np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]; L_ = [np.linalg.norm(Q[i] - Q[(i + 1) % len(Q)]) for i in range(len(Q))]
        kind = f'{len(Q)}-gon'
        if len(Q) == 4 and max(L_) - min(L_) < 1e-7:
            d = sorted([np.linalg.norm(Q[0] - Q[2]), np.linalg.norm(Q[1] - Q[3])]); kind = 'golden rhombus' if abs(d[1] / d[0] - 1.6180339887) < 1e-6 else 'rhombus'
        out.append(kind)
    return out
v0 = ConvexHull(tips[0]).volume
out = [f'four Cleo-Ico tips at a square-face centre; original volume {v0:.6f} each; tips collide pairwise: '
       + str(sum(1 for a, b in itertools.combinations(range(4), 2) if ConvexHull(np.vstack([tips[a], tips[b]])).volume < ConvexHull(tips[a]).volume + ConvexHull(tips[b]).volume - 1e-12)) + ' pairs (by hull test)']
for i, P in enumerate(T):
    fs = faces(P); out.append(f'   trimmed tip {i}: {len(P)} corners, volume {ConvexHull(P).volume:.6f} ({100 * ConvexHull(P).volume / v0:.1f}% kept), faces: ' + ', '.join(f'{fs.count(k)} {k}' for k in sorted(set(fs))))
# do the trimmed tips meet face to face (shared faces) and fill the X between them?
shared = 0
for a, b in itertools.combinations(range(4), 2):
    fa = ConvexHull(T[a]).equations; fb = ConvexHull(T[b]).equations
    if any(np.allclose(x[:3], -y[:3], atol=1e-7) and abs(x[3] + y[3]) < 1e-7 for x in fa for y in fb): shared += 1
out.append(f'pairs of trimmed tips meeting face to face: {shared} of 6')
print('\n'.join(out)); open('data/tips-meet.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'tips': [P.tolist() for P in tips], 'trimmed': [P.tolist() for P in T], 'site': site.tolist()}, open('data/tips-meet.json', 'w'))
