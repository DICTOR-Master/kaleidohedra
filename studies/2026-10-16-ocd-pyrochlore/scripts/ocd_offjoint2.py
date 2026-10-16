# DICTO OCD off-joints study, part 2 (DICTO 2026-10-17): the golden analysis of §6 of the GBP paper, redone for the densest lattice
# packing found (78.93%, Step 14, off the hexagon joints) and checked on the bcc packing (77.43%) as the known case.
# Each copy's golden envelope is its rhombic triacontahedron (the 30 golden planes, normals on the 2-fold axes, pushed in to touch the
# OCD). G' is space minus the union of the envelopes (10.22% for bcc, exact, paper §6). Reports, float:
#   the G' fraction (voxel sampling); the envelope overlaps per copy (how many, their volume, corners and faces: golden rhombohedra?);
#   whether any point is in three envelopes; and whether the densest lattice's basis looks golden (coordinates a + b√5, small rationals).
# -> data/ocd-offjoint2.txt
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
S = np.array(json.load(open('data/network.json'))['ocd']); S = S - S.mean(axis=0)
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
PS = planes(S)
HX = np.array([e[:3] / np.linalg.norm(e[:3]) for e in PS if np.sum(np.abs(S @ e[:3] + e[3]) < 1e-7) == 6]); assert len(HX) == 20
U = planes(HX)[:, :3]; U /= np.linalg.norm(U, axis=1)[:, None]; assert len(U) == 12          # 5-fold axes
N2 = []                                                                                        # 2-fold axes: midpoints of icosahedron edges
for i, j in itertools.combinations(range(12), 2):
    if abs(U[i] @ U[j] - 1 / 5 ** .5) < 1e-6:
        n = (U[i] + U[j]) / np.linalg.norm(U[i] + U[j]); N2 += [n, -n]
N2 = np.unique(np.round(N2, 12), axis=0); assert len(N2) == 30, len(N2)
H = (S @ N2.T).max(axis=0)                                                                     # support: RT = {x : N2 x <= H}
RTV = HalfspaceIntersection(np.c_[N2, -H], np.zeros(3)).intersections; VRT = ConvexHull(RTV).volume
VOCD = ConvexHull(S).volume
N = json.load(open('data/network.json')); D = json.load(open('data/densest.json'))
lat = {'bcc (hexagon joints)': np.array(N['T'])[:3], 'densest lattice (off the joints)': np.array(D['B'])}
out = ['DICTO · dictospheres.com', 'DICTO OCD off-joints study, part 2: golden envelopes in two packings (float)',
       f'OCD volume {VOCD:.6f}; envelope (rhombic triacontahedron) volume {VRT:.6f}']
rng = np.random.default_rng(1)
for name, B in lat.items():
    det = abs(np.linalg.det(B)); M = np.array(list(itertools.product(range(-3, 4), repeat=3))); T = M @ B
    T = T[np.linalg.norm(T, axis=1) < 2 * np.linalg.norm(RTV, axis=1).max() + np.abs(B).sum()]
    # overlaps of envelope 0 with envelope t
    ov = []
    for t in T:
        if np.linalg.norm(t) < 1e-9: continue
        hs = np.vstack([np.c_[N2, -H], np.c_[N2, -H - N2 @ t]])
        c = t / 2
        if np.any(hs[:, :3] @ c + hs[:, 3] > -1e-9): continue                                  # midpoint not strictly inside both: no overlap
        P = HalfspaceIntersection(hs, c).intersections; hull = ConvexHull(P)
        corners = np.unique(np.round(P, 7), axis=0); fac = len(planes(corners))
        ov.append((round(hull.volume, 6), len(corners), fac))
    # voxel sampling of G' and triple cover
    n = 400000; f = rng.random((n, 3)); X = f @ B; cover = np.zeros(n, dtype=int)
    for t in T:
        cover += ((X - t) @ N2.T <= H).all(axis=1)
    gp = np.mean(cover == 0); tri = np.mean(cover >= 3)
    out += [f'-- {name}: density {VOCD / det:.6f}',
            f'   envelope overlaps per copy: {len(ov)}; (volume, corners, faces): {sorted(set(ov))}',
            f'   G\' (space outside every envelope): {gp:.4%} of space (±{(gp * (1 - gp) / n) ** .5:.2%}); points in 3 or more envelopes: {tri:.4%}']
# is the densest basis golden? each coordinate as (A + Bn√5)/q with small integers
s5 = 5 ** .5; B = np.array(D['B']); res = []
for x in B.ravel():
    best = None
    for q in range(1, 61):
        bn = np.arange(-200, 201); A = np.round(q * x - bn * s5); err = np.abs(A + bn * s5 - q * x) / q
        k = np.argmin(err)
        if err[k] < 1e-9 and abs(A[k]) <= 400: best = (int(A[k]), int(bn[k]), q); break
    res.append(best)
out += [f'densest basis coordinates as (A + B√5)/q, |A| <= 400, |B| <= 200, q <= 60, error < 1e-9: {res}',
        'None = no such simple form found (the basis is a float optimum, good to about 1e-9, so this test can only suggest, not prove).']
print('\n'.join(out)); open('data/ocd-offjoint2.txt', 'w').write('\n'.join(out) + '\n')
