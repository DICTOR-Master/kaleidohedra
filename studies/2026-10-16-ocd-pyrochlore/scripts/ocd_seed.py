# DICTO OCD off-joints study, part 1 (DICTO 2026-10-17: Ogdoecontahedra placed off their hexagon joints): does the OCD itself form the
# Bodhi seed pattern, as the OCD Stella does? An outer OCD scaled by K holds 12 OCDs on its 5-fold axes, each pushed out to touch the outer
# form; the smallest K with no overlap closes the seed. Centre: the largest OCD (scaled) meeting none of the 12. Float.
# -> data/ocd-seed.txt, data/ocd-seed.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
S = np.array(json.load(open('data/network.json'))['ocd']); S = S - S.mean(axis=0); I = S
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
PS, PI = planes(S), planes(I)
sc = lambda P, s: np.c_[P[:, :3], P[:, 3] * s]
def depth(PA, a, PB, b):
    H = np.vstack([np.c_[PA[:, :3], PA[:, 3] - PA[:, :3] @ a], np.c_[PB[:, :3], PB[:, 3] - PB[:, :3] @ b]]); A = H[:, :3]; bb = -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=bb, bounds=[(None, None)] * 3 + [(0, None)])
    return r.x[3] if r.success else 0
def bisect(bad, lo, hi, n=40):
    for _ in range(n):
        m = (lo + hi) / 2
        if bad(m): lo = m
        else: hi = m
    return hi
HX = []   # hexagon normals (3-fold axes) -> their hull's 12 pentagon planes are the 5-fold axes
for e in PS:
    if np.sum(np.abs(S @ e[:3] + e[3]) < 1e-7) == 6: HX.append(e[:3] / np.linalg.norm(e[:3]))
HX = np.array(HX); assert len(HX) == 20
U = planes(HX)[:, :3]; U = U / np.linalg.norm(U, axis=1)[:, None]; assert len(U) == 12
def push(K):   # distance along u at which S + d*u just fits inside K*S (largest d with S+d u inside)
    u = U[0]; return min(((-e[3]) * K - (S @ e[:3]).max()) / (u @ e[:3]) for e in PS if u @ e[:3] > 1e-9)
i, j = next((i, j) for i, j in itertools.combinations(range(12), 2) if U[i] @ U[j] > 0.4)
K = bisect(lambda k: depth(PS, push(k) * U[i], PS, push(k) * U[j]) > 1e-6, 1.5, 6.0)
t = push(K); stel = [t * u for u in U]
worst = max(depth(PS, a, PS, b) for a, b in itertools.combinations(stel, 2))
def touching(a, b):
    X = S + b; Ha = np.c_[PS[:, :3], PS[:, 3] - PS[:, :3] @ a]
    return max(int(np.sum(np.abs(X @ e[:3] + e[3]) < 1e-4)) for e in Ha)
cnt = [sum(1 for j in range(12) if j != i and depth(PS, stel[i], PS, stel[j]) < 1e-6 and touching(stel[i], stel[j]) >= 3) for i in range(12)]
s = bisect(lambda m: not (max(depth(sc(PI, m), np.zeros(3), PS, p) for p in stel) > 1e-6), 0.01, 2.0) * 0.999
vS = ConvexHull(S).volume; vI = ConvexHull(I).volume; vOut = vS * K ** 3
gap = vOut - 12 * vS - vI * s ** 3
out = ['DICTO · dictospheres.com', 'DICTO OCD seed, off-joints study part 1 (float)',
       f'outer OCD scale K = {K:.6f} (φ² = {((1 + 5 ** .5) / 2) ** 2:.6f}, φ³ = {((1 + 5 ** .5) / 2) ** 3:.6f}); the 12 at distance {t:.5f}; worst overlap {worst:.1e}',
       'each of the 12 touches the outer form; contacts between the 12 not counted (the plane test counts far copies)',
       f'centre OCD: largest {s:.4f} of the OCD (1/φ = 0.618034)',
       f'volumes: outer {vOut:.5f}; 12 OCDs {12 * vS / vOut:.2%}; centre {vI * s ** 3 / vOut:.2%}; gap {gap / vOut:.2%}']
print('\n'.join(out)); open('data/ocd-seed.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'ocd': S.tolist(), 'K': K, 'stel': [p.tolist() for p in stel], 'centre_scale': s}, open('data/ocd-seed.json', 'w'))
