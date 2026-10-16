# DICTO OCD Stella seed (DICTO 2026-10-16: "12 around a small icosa filled out like Bodhi ... seed"): the Bodhi seed's pattern with the OCD
# Stella. An outer OCD Stella scaled by K holds 12 OCD Stellas on its 5-fold axes, each pushed out until it touches the outer form; the
# smallest K at which the 12 do not overlap each other closes the seed (neighbours touching). Centre: the largest icosahedron (the crystal's,
# scaled) that meets none of the 12. Reports K, contacts, the gap share and the 12's contact pattern. Float.
# -> data/stella-seed.txt, data/stella-seed.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
R = json.load(open('data/crystal-render.json')); S = np.array(R['stella']['v']); I = np.array(R['ico']['v'])
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
rr = np.linalg.norm(S, axis=1); U = S[rr > rr.max() - 1e-6]; U = U / np.linalg.norm(U, axis=1)[:, None]
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
out = ['DICTO · dictospheres.com', 'DICTO OCD Stella seed (float)',
       f'outer OCD Stella scale K = {K:.6f} (φ² = {((1 + 5 ** .5) / 2) ** 2:.6f}, φ³ = {((1 + 5 ** .5) / 2) ** 3:.6f}); the 12 at distance {t:.5f}; worst overlap {worst:.1e}',
       f'each of the 12 touches the outer form and, face to face, {sorted(set(cnt))} of the others',
       f'centre icosahedron: largest {s:.4f} of the crystal icosahedron',
       f'volumes: outer {vOut:.5f}; 12 OCD Stellas {12 * vS / vOut:.2%}; centre {vI * s ** 3 / vOut:.2%}; gap {gap / vOut:.2%}']
print('\n'.join(out)); open('data/stella-seed.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'stella': R['stella'], 'ico': R['ico'], 'K': K, 'stel': [p.tolist() for p in stel], 'centre_scale': s}, open('data/stella-seed.json', 'w'))
