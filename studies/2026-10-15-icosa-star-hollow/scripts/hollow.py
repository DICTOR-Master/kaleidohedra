# DICTO-ICOSA star, hollow (DICTO 2026-10-15: "check the hollow first"): centre icosidodecahedron (edge 1) removed, a pyramid with
# all edges 1 pointing inward on each of its 32 faces, core icosahedron on the 12 pentagonal-pyramid tips. Exact + separating axes.
import itertools, numpy as np
from scipy.spatial import ConvexHull
g = (1 + 5 ** .5) / 2
# icosidodecahedron of edge 1: (0,0,±φ) and (±1/2, ±φ/2, ±φ²/2), cyclic
V = []
for s in (1, -1):
    for i in range(3):
        v = [0, 0, 0]; v[i] = s * g; V.append(v)
for sx, sy, sz in itertools.product((1, -1), repeat=3):
    b = [sx * .5, sy * g / 2, sz * g * g / 2]
    for k in range(3): V.append(b[k:] + b[:k])
ID = np.array(V); assert len(ID) == 30
edges = sorted(set(round(np.linalg.norm(a - b), 9) for a, b in itertools.combinations(ID, 2)))[:1]; assert abs(edges[0] - 1) < 1e-9
H = ConvexHull(ID); F = []
for e in H.equations:
    idx = tuple(sorted(i for i in range(30) if abs(ID[i] @ e[:3] + e[3]) < 1e-9))
    if idx not in [f for f, _ in F]: F.append((idx, e))
assert len(F) == 32
def pyramid(idx, e):
    Q = ID[list(idx)]; c = Q.mean(0); h = np.sqrt(1 - np.linalg.norm(Q[0] - c) ** 2); return np.vstack([Q, c - e[:3] * h])
pyr = [(len(i), pyramid(i, e)) for i, e in F]
tips5 = np.array([P[-1] for n, P in pyr if n == 5]); tips3 = np.array([P[-1] for n, P in pyr if n == 3])
r5 = np.linalg.norm(tips5, axis=1); r3 = np.linalg.norm(tips3, axis=1)
core_edge = min(np.linalg.norm(a - b) for a, b in itertools.combinations(tips5, 2))
print('pentagon tips radius', r5.min(), r5.max(), ' triangle tips radius', r3.min(), r3.max())
print('core icosahedron edge', core_edge, ' 2/sqrt5 =', 2 / 5 ** .5)
# core icosahedron = hull of the 12 tips; its insphere vs the triangle tips (3-fold axes point at core face centres)
CI = ConvexHull(tips5); core_in = min(-e[3] for e in CI.equations)
print('core inradius', core_in, ' triangle-tip radius', r3.min(), ' gap along 3-fold axis', r3.min() - core_in)
# separating-axis overlap test between convex solids
def axes(P):
    h = ConvexHull(P); A = [e[:3] for e in h.equations]
    E = [P[j] - P[i] for s in h.simplices for i, j in itertools.combinations(s, 2)]
    return A, E
def overlap(P, Q, tol=1e-9):
    a1, e1 = axes(P); a2, e2 = axes(Q); cand = a1 + a2
    for u in e1[:60]:
        for w in e2[:60]:
            c = np.cross(u, w)
            if np.linalg.norm(c) > 1e-9: cand.append(c / np.linalg.norm(c))
    for n in cand:
        p, q = P @ n, Q @ n
        if p.max() <= q.min() + tol or q.max() <= p.min() + tol: return False
    return True
bad = [(i, j) for (i, (_, P)), (j, (_, Q)) in itertools.combinations(enumerate(pyr), 2) if overlap(P, Q)]
print('inward pyramid pairs overlapping:', len(bad), 'of', 32 * 31 // 2)
core = tips5
bad_core = [i for i, (_, P) in enumerate(pyr) if overlap(P, core)]
print('pyramids overlapping the core icosahedron:', len(bad_core))
# exact values
print('volumes: ID', (45 + 17 * 5 ** .5) / 6, ' 12 J2', 12 * (5 + 5 ** .5) / 24, ' 20 tets', 20 * 2 ** .5 / 12, ' core', 5 * (3 + 5 ** .5) / 12 * core_edge ** 3)

# can the core turn in place? rotate it about each kind of axis and find the first angle where it hits a pyramid
def rot(axis, t):
    a = np.array(axis, float); a /= np.linalg.norm(a); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
for name, ax in [('5-fold', tips5[0]), ('3-fold', tips3[0]), ('2-fold', tips5[0] + tips5[np.argsort(np.linalg.norm(tips5 - tips5[0], axis=1))[1]]), ('random', [0.3, 0.7, 0.2])]:
    hit = None
    for deg in np.arange(0.05, 36.01, 0.05):
        C = core @ rot(ax, np.radians(deg)).T
        if any(overlap(P, C, tol=1e-7) for _, P in pyr): hit = deg; break
    print(f'core turned about a {name} axis: first contact at {hit} degrees')
