# Step 17 (DICTO: frog chorus, "test the spatial version"). Exploratory, float.
# The 20 hexagon directions of the OCD are a dodecahedron's corners; the 5 inscribed cubes are the five voices. Each cube gives a
# bcc packing (joints on that cube's 8 hexagons), all copies in the same orientation. Around a five-fold axis a5 of a central copy,
# space is cut into 5 wedges of 72 deg; wedge k uses cube k's packing (cube k+1 = cube k turned 72 deg about a5), so the whole is
# exactly five-fold symmetric. Collisions across the wedge boundaries (packing test g(x) >= 1 on every pair), scanning the start
# angle of the wedges; contacts across boundaries (hexagon joints or other).
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
N = json.load(open('data/network.json')); O = np.array(N['ocd'])
pl = []
for e in ConvexHull(O).equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
pl = np.array(pl); n_f = pl[:, :3] / np.linalg.norm(pl[:, :3], axis=1)[:, None]; d_f = -pl[:, 3] / np.linalg.norm(pl[:, :3], axis=1)
g = lambda X: np.max((X @ n_f.T) / (2 * d_f), axis=-1)
hexn = [e for e in pl if np.sum(np.abs(O @ e[:3] + e[3]) < 1e-7) == 6]
U = np.array([e[:3] / np.linalg.norm(e[:3]) for e in hexn]); h = -hexn[0][3] / np.linalg.norm(hexn[0][:3])
cubes = []
for S in itertools.combinations(range(20), 8):
    D = U[list(S)] @ U[list(S)].T; off = D[~np.eye(8, dtype=bool)]
    if np.all((np.abs(off - 1 / 3) < 1e-6) | (np.abs(off + 1 / 3) < 1e-6) | (np.abs(off + 1) < 1e-6)): cubes.append(list(S))
assert len(cubes) == 5, len(cubes)
r = np.linalg.norm(O, axis=1); a5 = O[np.argmax(r)]; a5 /= np.linalg.norm(a5)
def rot(axis, ang):
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]]); return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
R72 = rot(a5, 2 * np.pi / 5)
# order the cubes so that cube k+1 = R72 cube k
def same(A, B): return all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-6 for a in A)
order = [0]
while len(order) < 5:
    nxt = next(j for j in range(5) if same(U[cubes[order[-1]]] @ R72.T, U[cubes[j]])); order.append(nxt)
cubes = [cubes[k] for k in order]
def lattice(k, R=3.2):
    t = [2 * h * U[i] for i in cubes[k]]; t4 = []
    for v in t:
        if not any(np.allclose(v, -w) for w in t4): t4.append(v)
    t4 = [v for v in t4][:4]
    # bcc of a cube: integer combinations of the 4 (tetrahedral up to sign) bond vectors
    P = []
    for m in itertools.product(range(-4, 5), repeat=3):
        p = m[0] * (2 * h * U[cubes[k][0]]) + m[1] * (2 * h * U[cubes[k][1]]) + m[2] * (2 * h * U[cubes[k][2]])
        P.append(p)
    P = np.array(P); return P[np.linalg.norm(P, axis=1) < R]
# a basis of the bcc lattice of cube k: three of its bond vectors that are not coplanar; check it generates all 8 bonds
L = []
for k in range(5):
    B = None
    for a, b, c in itertools.combinations(cubes[k], 3):
        M = np.array([U[a], U[b], U[c]]).T * 2 * h
        if abs(np.linalg.det(M)) > 1e-6:
            ok = all(np.allclose(np.round(np.linalg.solve(M, 2 * h * U[i])), np.linalg.solve(M, 2 * h * U[i]), atol=1e-6) for i in cubes[k])
            if ok: B = M; break
    assert B is not None
    P = np.array([B @ np.array(m) for m in itertools.product(range(-6, 7), repeat=3)]); L.append(P[np.linalg.norm(P, axis=1) < 3.0])
# wedge coordinates around a5
e1 = np.cross(a5, [1, 0, 0]); e1 = e1 if np.linalg.norm(e1) > 0.1 else np.cross(a5, [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(a5, e1)
def wedge_of(p, th0):
    ang = (np.arctan2(p @ e2, p @ e1) - th0) % (2 * np.pi); return int(ang // (2 * np.pi / 5)) % 5
best = []
for th0 in np.radians(np.arange(0, 72, 1.0)):
    sites = []
    for k in range(5):
        for p in L[k]:
            if np.linalg.norm(p) < 1e-9 or (np.linalg.norm(p - (p @ a5) * a5) < 1e-9) or wedge_of(p, th0) == k: sites.append((p, k))
    # remove duplicates (the axis and shared sites)
    S = []
    for p, k in sites:
        if not any(np.allclose(p, q) for q, _ in S): S.append((p, k))
    P = np.array([p for p, _ in S]); K = np.array([k for _, k in S])
    inner = np.linalg.norm(P, axis=1) < 2.0
    coll = 0; cross_contacts = 0
    for i in np.where(inner)[0]:
        Dx = P - P[i]; gx = g(Dx); gx[i] = 9
        coll += int(np.sum(gx < 1 - 1e-7)); cross_contacts += int(np.sum((np.abs(gx - 1) < 1e-7) & (K != K[i])))
    best.append((coll, np.degrees(th0), cross_contacts, int(inner.sum())))
best.sort()
out = [f'five voices found and ordered by the 72-degree turn about a five-fold axis: {len(cubes)} cubes',
       f'scan of the wedge start angle (0..71 deg): fewest collisions {best[0][0]} (at {best[0][1]:.0f} deg, {best[0][2]} contacts across boundaries, {best[0][3]} inner copies)',
       f'collision counts over the scan: min {best[0][0]}, max {best[-1][0]}; collision-free angles: {[round(b[1]) for b in best if b[0] == 0]}']
print('\n'.join(out)); open('data/chorus-space.txt', 'w').write('\n'.join(out) + '\n')

# Silent frogs: at the best start angle, remove clashing copies in whole five-fold orbits (so the symmetry stays exact) until no
# collisions remain; report how many copies go silent and where (distance from the axis, along the boundary planes).
th0 = np.radians(best[0][1]); RR = 2.8
S = []
for k in range(5):
    for p in L[k]:
        if np.linalg.norm(p) < RR and (np.linalg.norm(p) < 1e-9 or np.linalg.norm(p - (p @ a5) * a5) < 1e-9 or wedge_of(p, th0) == k):
            if not any(np.allclose(p, q) for q, _ in S): S.append((p, k))
P = np.array([p for p, _ in S]); alive = np.ones(len(P), bool)
def clashes():
    pairs = []
    for i in np.where(alive)[0]:
        Dx = P - P[i]; gx = g(Dx); gx[i] = 9; gx[~alive] = 9
        for j in np.where(gx < 1 - 1e-7)[0]:
            if j > i: pairs.append((i, j))
    return pairs
removed = 0
while True:
    cp = clashes()
    if not cp: break
    # the copy in most clashes, farthest from the centre first; remove its whole five-fold orbit
    cnt = {}
    for i, j in cp: cnt[i] = cnt.get(i, 0) + 1; cnt[j] = cnt.get(j, 0) + 1
    i = max(cnt, key=lambda i: (cnt[i], np.linalg.norm(P[i])))
    for q in [np.linalg.matrix_power(R72, s) @ P[i] for s in range(5)]:
        d = np.linalg.norm(P - q, axis=1); j = int(np.argmin(d))
        if d[j] < 1e-6 and alive[j]: alive[j] = False; removed += 1
inner = np.linalg.norm(P, axis=1) < RR - 0.6
dist = sorted(set(np.round(np.linalg.norm(P[~alive] - np.outer(P[~alive] @ a5, a5), axis=1), 3)))
out2 = [f'silent frogs at start angle {best[0][1]:.0f} deg within radius {RR}: {removed} of {len(P)} copies removed (in whole five-fold orbits) -> collision-free and exactly five-fold symmetric',
        f'   removed copies lie at these distances from the five-fold axis: {dist[:12]}',
        f'   density inside radius {RR - 0.6}: {np.sum(alive & inner)} copies kept of {np.sum(inner)}']
print('\n'.join(out2)); open('data/chorus-space.txt', 'a').write('\n'.join(out2) + '\n')
json.dump({'sites': P[alive].tolist(), 'voice': [int(k) for (p, k), a in zip(S, alive) if a], 'a5': a5.tolist(), 'removed': P[~alive].tolist()}, open('data/chorus-space.json', 'w'))
