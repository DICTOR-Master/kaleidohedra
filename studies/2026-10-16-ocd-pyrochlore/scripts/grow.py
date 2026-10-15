# Step 9 (DICTO: "grow golden rhombohedra from the rhombi"). Exploratory, float.
# Golden rhombohedra (prolate and oblate) have only golden-rhombus faces. On a golden rhombus with edge vectors e1, e2 from its
# acute corner (e1.e2 = s^2/sqrt5), a third edge e3 of the same length with e3.e1 and e3.e2 each = +-s^2/sqrt5 gives a golden
# rhombohedron (prolate or oblate). Grow greedily from the two golden-rhombus faces of each conflict zone, outward, accepting a
# brick only if it overlaps nothing (OCDs, zones, bricks already placed); limbs are left out (the zone stands for their crossing).
import json, itertools, numpy as np, sys
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/_lib'); import geomcheck as gc
N = json.load(open('data/network.json')); T = np.array(N['T']); O = np.array(N['ocd']); Z = np.array(json.load(open('data/conflict.json'))['zone'])
C = json.load(open('/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma/data/reversed-chain.json')) if False else None
ax5 = gc.icosa_axes(np.array([v for v in O if abs(np.linalg.norm(v) - np.linalg.norm(O, axis=1).max()) < 1e-9]))['5'] if False else None
# five-fold axes of the OCD: its 12 outer corners
r = np.linalg.norm(O, axis=1); A5 = O[np.abs(r - r.max()) < 1e-9]; A5 = A5 / np.linalg.norm(A5, axis=1)[:, None]
def rhombi(P):
    h = ConvexHull(P); pl = []; out = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-7) for q in pl): continue
        pl.append(e); Q = P[np.abs(P @ e[:3] + e[3]) < 1e-7]
        if len(Q) != 4: continue
        c = Q.mean(0); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); Q = Q[np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]
        L = [np.linalg.norm(Q[i] - Q[(i + 1) % 4]) for i in range(4)]
        if max(L) - min(L) < 1e-7:
            d = sorted([np.linalg.norm(Q[0] - Q[2]), np.linalg.norm(Q[1] - Q[3])])
            if abs(d[1] / d[0] - (1 + 5 ** .5) / 2) < 1e-6: out.append((Q, e))
    return out
R0 = rhombi(Z); assert len(R0) == 2
s = np.linalg.norm(R0[0][0][1] - R0[0][0][0])
on5 = [max(abs(A5 @ ((Q[(i + 1) % 4] - Q[i]) / s))) for Q, e in R0 for i in range(4)]
print(f'zone rhombus edge {s:.6f}; edges along five-fold axes: {all(abs(x - 1) < 1e-7 for x in on5)} (best |cos| {min(on5):.6f})', flush=True)
cells = []
for m in itertools.product(range(-2, 3), repeat=4):
    p = sum(k * t for k, t in zip(m, T))
    if np.linalg.norm(p) < 2.6 and not any(np.allclose(p, c) for c in cells): cells.append(p)
EO = ConvexHull(O).equations
site = Z.mean(0)
obst = [EO - np.c_[np.zeros((len(EO), 3)), EO[:, :3] @ c] for c in cells if np.linalg.norm(c - site) < 1.6]
zones = [ConvexHull(Z).equations]
def free(P):
    EP = ConvexHull(P).equations
    for E in obst + zones + bricks_eq:
        H = np.vstack([EP, E]); nrm = np.linalg.norm(H[:, :3], axis=1)
        rr = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
        if rr.status == 0 and rr.x[3] > 1e-9: return False
    return True
def candidates(Q, e):
    """bricks on rhombus Q (outward normal e[:3]): third edge e3 from the acute corner with e3.e1, e3.e2 = +-s^2/sqrt5"""
    ang = [np.dot(Q[i - 1] - Q[i], Q[(i + 1) % 4] - Q[i]) for i in range(4)]; i0 = int(np.argmax(ang))   # acute corner
    p0 = Q[i0]; e1 = Q[(i0 + 1) % 4] - p0; e2 = Q[i0 - 1] - p0; n = e[:3]; k = s * s / 5 ** .5; out = []
    M = np.array([e1, e2])
    for s1, s2 in itertools.product((1, -1), repeat=2):
        # e3 = x e1 + y e2 + z n with e3.e1 = s1 k, e3.e2 = s2 k, |e3| = s, z > 0 (outward)
        G = M @ M.T; xy = np.linalg.solve(G, [s1 * k, s2 * k]); inplane = xy @ M; z2 = s * s - inplane @ inplane
        if z2 <= 1e-12: continue
        e3 = inplane + np.sqrt(z2) * n
        P = np.array([p0, p0 + e1, p0 + e2, p0 + e1 + e2]); P = np.vstack([P, P + e3])
        kind = 'prolate' if abs(np.linalg.det(np.array([e1, e2, e3])) - s ** 3 * 0.7608) < 1e-3 * s ** 3 else 'oblate'
        out.append((kind, P))
    return out
bricks, bricks_eq, queue = [], [], [(Q, e) for Q, e in R0]
seen = []
while queue and len(bricks) < 300:
    Q, e = queue.pop(0)
    for kind, P in candidates(Q, e):
        if np.linalg.norm(P.mean(0) - site) > 0.9: continue
        if any(np.allclose(np.sort(P, axis=0), np.sort(B, axis=0), atol=1e-9) for _, B in bricks): continue
        if free(P):
            bricks.append((kind, P)); bricks_eq.append(ConvexHull(P).equations)
            for Q2, e2 in rhombi(P):
                if not any(np.allclose(np.sort(Q2, axis=0), np.sort(Qs, axis=0), atol=1e-9) for Qs in seen): seen.append(Q2); queue.append((Q2, e2))
            break
vol = sum(ConvexHull(P).volume for _, P in bricks)
from collections import Counter
out = [f'grown from one conflict zone: {len(bricks)} golden rhombohedra ({dict(Counter(k for k, _ in bricks))}), volume {vol:.6f}; '
       f'stopped because {"no face could take a brick" if not queue else "the cap of 300 bricks was reached"}',
       f'rhombohedron edge {s:.6f} (the OCD hexagon edge is 0.237881, {0.237881 / s:.4f} times longer)']
print('\n'.join(out)); open('data/grow.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'bricks': [[k, P.tolist()] for k, P in bricks], 'zone': Z.tolist()}, open('data/grow.json', 'w'))
