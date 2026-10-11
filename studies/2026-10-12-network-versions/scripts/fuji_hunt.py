# DICTO (2026-10-12): in the dodecahedral Lotus seed "it's a FUJI that fits between them, maybe at a different angle, sides going
# from the six-sided triangle to the vertices of the dodecahedron". Search: on every 3-fold axis, flat-ended triangles (hexagons,
# all angles 120°, sides alternating) made of corners of the solids (outer dodecahedron, the 20 corner copies, the centre), square
# to the axis and centred on it, joined to a dodecahedron corner on the same axis; keep the pyramids that lie in the gap (outside
# every solid, inside the outer form). Reports each kind: count, edges, volume, the slopes of its faces to the base, gap share.
import sys, itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open(__file__.replace('fuji_hunt.py', 'network_screen.py')).read().split('def sat_overlap')[0])
X = sys.argv[1] if len(sys.argv) > 1 else 'D'
Xv = ref[X]; outer = Xv * PHI ** 2; centre = Xv / PHI
copies = []
for y in Xv:
    d = y / np.linalg.norm(y); j = np.argmax(Xv @ d); copies.append(Xv + (y * PHI ** 2 - Xv[j]))
solids = [ConvexHull(c).equations for c in copies] + [ConvexHull(centre).equations]
OUT = ConvexHull(outer).equations
pts = np.unique(np.round(np.vstack([outer, centre] + copies), 9), axis=0)
Dcorners = np.unique(np.round(np.vstack([centre] + copies + [outer]), 9), axis=0) if X == 'D' else pts
gapvol = ConvexHull(outer).volume - len(copies) * ConvexHull(Xv).volume - ConvexHull(centre).volume
D_ = ref['D']; axes3 = [v / np.linalg.norm(v) for v in D_]          # dodecahedron corners point along the 3-fold axes
def clear(P):          # pyramid P (convex) outside every solid and inside the outer form (sampled interior test)
    H = ConvexHull(P); w = np.random.default_rng(0).dirichlet(np.ones(len(P)), 400) @ P
    if not np.all(w @ OUT[:, :3].T + OUT[:, 3] <= 1e-9): return False
    for E in solids:
        if np.any(np.all(w @ E[:, :3].T + E[:, 3] < -1e-9, axis=1)): return False
    return True
found = {}
for u in axes3:
    h = np.round(pts @ u, 7); r = np.linalg.norm(pts - np.outer(pts @ u, u), axis=1)
    on_axis = pts[r < 1e-7]
    for level in np.unique(h):
        ring = pts[(np.abs(h - level) < 1e-7) & (r > 1e-6)]
        if len(ring) < 6: continue
        # a flat-ended triangle centred on the 3-fold axis is {p, Rp, R^2 p, q, Rq, R^2 q} (R = 120° turn about the axis)
        K = np.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]]); R1 = np.eye(3) + np.sin(2 * np.pi / 3) * K + (1 - np.cos(2 * np.pi / 3)) * K @ K
        has = lambda x: np.min(np.linalg.norm(ring - x, axis=1)) < 1e-6
        triples = []
        for p in ring:
            if has(p @ R1.T) and has(p @ R1.T @ R1.T): triples.append(np.array([p, p @ R1.T, p @ R1.T @ R1.T]))
        for t1, t2 in itertools.combinations(triples, 2):
            if np.min(np.linalg.norm(t1[0] - t2, axis=1)) < 1e-6: continue
            Q = np.vstack([t1, t2]); c = Q.mean(0)
            # order round the axis and test 120° corners, alternating sides
            ex = Q[0] - c; ex /= np.linalg.norm(ex); ey = np.cross(u, ex)
            ang = np.arctan2((Q - c) @ ey, (Q - c) @ ex); Q = Q[np.argsort(ang)]
            sides = [np.linalg.norm(Q[i] - Q[(i + 1) % 6]) for i in range(6)]
            angles = []
            for i in range(6):
                a_, b_ = Q[i - 1] - Q[i], Q[(i + 1) % 6] - Q[i]
                angles.append(np.degrees(np.arccos(np.clip(a_ @ b_ / np.linalg.norm(a_) / np.linalg.norm(b_), -1, 1))))
            if not np.allclose(angles, 120, atol=1e-4): continue
            if not (np.isclose(sides[0], sides[2]) and np.isclose(sides[2], sides[4]) and np.isclose(sides[1], sides[3]) and np.isclose(sides[3], sides[5])): continue
            for A in on_axis:
                P = np.vstack([Q, A])
                if abs((A - c) @ u) < 1e-6 or not clear(P): continue
                hgt = abs((A - c) @ u); vol = ConvexHull(P).volume
                slopes = sorted({round(np.degrees(np.arctan2(hgt, abs(np.linalg.norm(np.cross(Q[(i + 1) % 6] - Q[i], c - Q[i])) / np.linalg.norm(Q[(i + 1) % 6] - Q[i])))), 3) for i in range(6)})
                k = (round(sides[0], 5), round(sides[1], 5), round(hgt, 5))
                found.setdefault(k, {'n': 0, 'vol': vol, 'slopes': slopes})['n'] += 1
print(f'{X} Lotus seed analog: gap volume {gapvol:.6f}')
for (s1, s2, hgt), v in sorted(found.items(), key=lambda kv: -kv[1]['n']):
    print(f'  FUJI-like pyramid x{v["n"]}: base sides {s1} / {s2}, height {hgt}, volume {v["vol"]:.6f}, face slopes {v["slopes"]} deg; '
          f'all of them fill {v["n"] * v["vol"] / gapvol:.1%} of the gap')
if not found: print('  none found')
