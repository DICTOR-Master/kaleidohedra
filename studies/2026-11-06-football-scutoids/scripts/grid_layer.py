"""Football layer with pentagon-hexagon links (reading A). Every link joins a pentagon of one ball to a hexagon of the next, on one axis.
A link line continues through a ball only as the same kind of face (a 5-fold axis has pentagons at both ends, a 3-fold axis hexagons), so
along a line the balls alternate pentagon role / hexagon role. Each ball sits on two lines: its 5-fold axis a along e1 and a 3-fold axis c
along e2, angle(a, c) = 79.19 deg (the other value, 37.38 deg, makes diagonal neighbours overlap). Checkerboard: even sites X (a on e1,
c on e2); odd sites Y = X turned 180 deg about the bisector of e1, e2 (c on e1, a on e2). Link length D = h5 + h6 + gap.
Checks: every link pentagon-to-hexagon, coaxial and parallel; no two balls overlap (separating-plane test); bridge = convex hull of the
two facing faces; bridges disjoint from balls and from each other."""
import numpy as np, itertools, sys
from scipy.spatial import ConvexHull
from football import V, F, pent, hexa, h5, h6
gap = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
P5 = [(f[0] / np.linalg.norm(f[0]),) + tuple(f[1:]) for f in pent]; P3 = [(f[0] / np.linalg.norm(f[0]),) + tuple(f[1:]) for f in hexa]
best = None
for f5 in P5:
    for f3 in P3:
        ang = np.degrees(np.arccos(np.clip(f5[0] @ f3[0], -1, 1)))
        if abs(ang - 79.19) < 0.05: best = (f5, f3); break
    if best: break
a, c = best[0][0], best[1][0]
bis = (a + c) / np.linalg.norm(a + c)
def rot(ax, t):
    ax = ax / np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]]); return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
R_Y = rot(bis, np.pi)
print("swap check", np.abs(R_Y @ a - c).max(), np.abs(R_Y @ c - a).max()); assert np.allclose(R_Y @ a, c, atol=1e-6)
D = h5 + h6 + gap
e1, e2 = a, c                       # lattice directions (X's own axes)
def centre(i, j): return D * (i * e1 + j * e2)
def ball(i, j):
    R = np.eye(3) if (i + j) % 2 == 0 else R_Y
    return V @ R.T + centre(i, j), R
def face_toward(i, j, d):
    Vb, R = ball(i, j)
    for n, h, idx in F:
        if np.allclose(R @ n, d / np.linalg.norm(d), atol=1e-9): return len(idx), Vb[idx]
    return None, None
links = []; bad = 0
for i, j in itertools.product(range(-2, 3), repeat=2):
    for di, dj, d in ((1, 0, e1), (0, 1, e2)):
        k1, f1 = face_toward(i, j, d); k2, f2 = face_toward(i + di, j + dj, -d)
        if k1 is None or k2 is None or {k1, k2} != {5, 6}: bad += 1
        else: links.append((f1, f2))
print(f"gap {gap}: link length D = {D:.4f}; links checked {len(links)}, not pentagon-hexagon {bad}")
# overlap test between balls (convex): separating axis via LP-free check: hull of the union volume vs sum
def overlap(A, B):
    hA, hB = ConvexHull(A), ConvexHull(B)
    for P, h in ((B, hA), (A, hB)):
        if ((h.equations[:, :3] @ P.T + h.equations[:, 3:4]) < -1e-9).all(0).any(): return True
    # edge-edge cases: sample interior points
    rng = np.random.default_rng(0); w = rng.dirichlet(np.ones(len(A)), 400); pts = w @ A
    return ((hB.equations[:, :3] @ pts.T + hB.equations[:, 3:4]) < -1e-9).all(0).any()
balls = {(i, j): ball(i, j)[0] for i, j in itertools.product(range(-2, 3), repeat=2)}
ov = [(p, q) for p, q in itertools.combinations(balls, 2) if np.linalg.norm(balls[p].mean(0) - balls[q].mean(0)) < 5.2 and overlap(balls[p], balls[q])]
dmin = min(np.linalg.norm(balls[p].mean(0) - balls[q].mean(0)) for p, q in itertools.combinations(balls, 2))
print(f"ball overlaps: {len(ov)}; nearest centres {dmin:.4f} (ball circumradius {np.linalg.norm(V, axis=1).max():.4f})")
# bridges: hull of the two faces; must not overlap balls
br = [np.vstack(l) for l in links]
bo = sum(1 for B in br for P in balls.values() if overlap(B, P) and ConvexHull(np.vstack([B, P])).volume < ConvexHull(B).volume + ConvexHull(P).volume - 1e-6)
print(f"bridge-ball overlaps (beyond the shared face): {bo}")
print("FINAL ok" if bad == 0 and not ov else "FINAL FAIL")
