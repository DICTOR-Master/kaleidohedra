# DICTO Jewel twinning (DICTO 2026-10-19), float Monte Carlo first look. Stella-Jewel Lattice in raw units (cube edge 2): Jewels on even
# cells 2(i,j,k), i+j+k even (an fcc of Jewels), stella octangulas on odd cells. Twin: keep every piece whose centre has x+y+z >= 0 and
# replace the rest by the mirror images (in the plane x+y+z = 0, a (111) layer of Jewels) of the pieces with x+y+z > 0: the stacking
# ...C B A B C..., the hcp-type fault. Count how many pieces cover each sample point near the plane: 1 = filled, 0 = gap, 2+ = overlap.
import numpy as np, itertools
PHI = (1 + 5 ** .5) / 2; s = (1, -1)
roofs = [r for a in s for b in s for r in ([0, a / PHI, b * PHI], [a / PHI, b * PHI, 0], [b * PHI, 0, a / PHI])]
C8 = [np.array(c, float) for c in itertools.product(s, s, s)]; verts, faces = [], []
def at(p):
    for i, q in enumerate(verts):
        if np.linalg.norm(p - q) < 1e-9: return i
    verts.append(np.array(p, float)); return len(verts) - 1
for A, B in itertools.combinations(C8, 2):
    if abs(np.linalg.norm(A - B) - 2) > 1e-9: continue
    Z = next(np.array(r) for r in roofs if all(abs(np.linalg.norm(np.array(r) - c) - 2 / PHI) < 1e-9 for c in (A, B))); X = A + B - Z
    faces.append([at(A), at(Z), at(B), at(X)]); m = (A + B) / 2
    for ax in range(3):
        if abs(A[ax] - B[ax]) > 1e-9: continue
        F = np.zeros(3); F[ax] = A[ax]; P = Z if (Z - m) @ F > 0 else X
        faces += [[at(A), at(P), at(F)], [at(P), at(B), at(F)]]
V = np.array(verts); T = np.array([[f[0], f[k], f[k + 1]] for f in faces for k in range(1, len(f) - 1)])
TA, TB, TC = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
RAY = np.array([0.5772, 0.3311, 0.7462]); RAY /= np.linalg.norm(RAY)   # a generic direction: no corner or edge hit
E1, E2 = TB - TA, TC - TA; H = np.cross(RAY, E2); DET = np.einsum('tk,tk->t', E1, H)
def parity(P):                                 # ray casting: odd number of crossings = inside (needs no face winding)
    S = P[:, None] - TA[None]; u = np.einsum('ptk,tk->pt', S, H) / DET
    Qv = np.cross(S, E1[None]); v = np.einsum('k,ptk->pt', RAY, Qv) / DET; t = np.einsum('tk,ptk->pt', E2, Qv) / DET
    return ((u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0)).sum(1) % 2 == 1
in_jewel = parity
def in_stella(P):
    x, y, z = P.T
    tp = (x + y + z >= -1) & (x - y - z >= -1) & (-x + y - z >= -1) & (-x - y + z >= -1)
    tm = (-x - y - z >= -1) & (-x + y + z >= -1) & (x - y + z >= -1) & (x + y - z >= -1)
    return tp | tm
n = np.ones(3) / 3 ** .5; mirror = lambda P: P - 2 * (P @ n)[:, None] * n[None]
cells = [np.array(c) for c in itertools.product(range(-5, 6), repeat=3)]
def cover(P, twin):
    k = np.zeros(len(P), int)
    for c in cells:
        ctr = 2.0 * c; sm = c.sum(); test = in_jewel if sm % 2 == 0 else in_stella
        for Q, use in ((P, (not twin) or sm >= 0), (mirror(P) if twin else None, twin and sm > 0)):
            if not use: continue
            near = np.linalg.norm(Q - ctr, axis=1) < 3 ** .5 + 1e-9
            if near.any(): k[np.where(near)[0][test(Q[near] - ctr)]] += 1
    return k
rng = np.random.default_rng(1); P = rng.uniform(-3, 3, (60000, 3)); P = P[np.abs(P @ n) < 2.0]
print('Jewel corners', len(V), 'triangles', len(T), '| centre inside:', parity(np.zeros((1, 3)))[0], '| volume (MC, expect 12):', round(np.mean(parity(rng.uniform(-2, 2, (200000, 3)))) * 64, 3))
for twin in (False, True):
    k = cover(P, twin); u, c = np.unique(k, return_counts=True)
    print('twinned' if twin else 'baseline', dict(zip(u.tolist(), c.tolist())), ' of', len(P), 'points (|distance to plane| < 2)')
    if twin:
        bad = P[k != 1]; d = bad @ n
        print('  defects: gap fraction', round(np.mean(k == 0), 4), 'overlap fraction', round(np.mean(k > 1), 4), '| distance from the plane: ', np.round(np.percentile(d, [0, 50, 100]), 3) if len(d) else '-')
