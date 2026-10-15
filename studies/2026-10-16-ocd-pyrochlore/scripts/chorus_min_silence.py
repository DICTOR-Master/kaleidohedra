# Fable check 2026-10-16 (light, float clash graph): is the greedy orbit silencing of step 22 minimal? Same sites as
# chorus_exact_big.py (radius 5, start angle 59 deg). ILP minimum over five-fold orbits, uniqueness, and the minimum without symmetry.
import sys, numpy as np
src = open('scripts/chorus_exact_big.py').read(); src = src[:src.index('removed = 0')]
sys.argv = ['x', '5.0']; exec(src)
n = len(P); orb = -np.ones(n, int); no = 0
for i in range(n):
    if orb[i] >= 0: continue
    for s in range(5):
        q = np.linalg.matrix_power(R72, s) @ P[i]; dd = np.linalg.norm(P - q, axis=1); j = int(np.argmin(dd))
        if dd[j] < 1e-6: orb[j] = no
    no += 1
sizes = np.bincount(orb); print('sites', n, 'orbits', no, 'orbit sizes', dict(zip(*np.unique(sizes, return_counts=True))))
E = set()
for i in range(n):
    gx = g(P - P[i]); gx[i] = 9
    for j in np.where(gx < 1 - 1e-9)[0]:
        a, b = sorted((orb[i], orb[j])); E.add((a, b))
selfclash = [a for a, b in E if a == b]; E2 = [(a, b) for a, b in E if a != b]
print('clashing orbit pairs', len(E2), 'orbits clashing with themselves', len(selfclash))
from scipy.optimize import milp, LinearConstraint, Bounds
c = sizes.astype(float)                      # minimise number of silenced copies
A = np.zeros((len(E2), no)); 
for r, (a, b) in enumerate(E2): A[r, a] = A[r, b] = 1
lb = np.zeros(no); 
for a in selfclash: lb[a] = 1
res = milp(c, constraints=[LinearConstraint(A, 1, np.inf)], integrality=np.ones(no), bounds=Bounds(lb, 1))
x = np.round(res.x).astype(int); print('ILP status', res.status, 'min silenced copies', int(c @ x), 'in', int(x.sum()), 'orbits')
res2 = milp(np.ones(no), constraints=[LinearConstraint(A, 1, np.inf)], integrality=np.ones(no), bounds=Bounds(lb, 1))
print('min number of orbits', int(round(res2.fun)))
# compare with the greedy result in data/chorus-exact-big.json
import json; G = np.array(json.load(open('data/chorus-exact-big.json'))['silenced'])
gs = set(orb[int(np.argmin(np.linalg.norm(P - q, axis=1)))] for q in G); print('greedy silenced orbits', len(gs), 'copies', len(G))
sil = P[np.repeat(x, 1)[orb] == 1]
rho = np.linalg.norm(sil - np.outer(sil @ a5, a5), axis=1)
print('optimal: silenced distances from axis', sorted(set(np.round(rho, 3))))
alive = x[orb] == 0; rr = np.linalg.norm(P - np.outer(P @ a5, a5), axis=1)
print('optimal kept fraction <1,<2,<3,<4:', [round(float(np.mean(alive[rr < r0])), 2) for r0 in (1, 2, 3, 4)])
# angular position of silenced copies relative to the nearest wedge boundary (degrees)
def ang(p): return np.degrees((np.arctan2(p @ e2, p @ e1) - th0) % (2 * np.pi / 5))
ab = [min(ang(p), 72 - ang(p)) for p in sil if np.linalg.norm(p - (p @ a5) * a5) > 1e-6]
print('optimal: angular distance of silenced copies to nearest boundary (deg):', sorted(np.round(ab, 1)))
# perpendicular distance from the nearest boundary half-plane
def pd(p):
    out = []
    for k in range(5):
        t = th0 + k * 2 * np.pi / 5; u = np.cos(t) * e1 + np.sin(t) * e2; w = np.cross(a5, u)
        if p @ u > 0: out.append(abs(p @ w))
        else: out.append(np.linalg.norm(p - (p @ a5) * a5))
    return min(out)
print('optimal: distance of silenced copies from nearest boundary half-plane:', sorted(np.round([pd(p) for p in sil], 3)))
print('wedge-site distance-to-boundary for comparison, median', round(float(np.median([pd(p) for p in P])), 3))
# misorientation of voice 0 vs voice 1 (the two cubes) as a rotation about a shared 3-fold axis
c0 = U[cubes[0]]; c1 = U[cubes[1]]; sh = [u for u in c0 if np.min(np.linalg.norm(c1 - u, axis=1)) < 1e-6]
print('shared directions', len(sh))
ax = sh[0]; v0 = [u for u in c0 if abs(u @ ax) < 0.5 and abs(u@ax)>0.2][0]
best = min(np.degrees(np.arccos(np.clip(v0 @ w - (v0@ax)*(w@ax), -1, 1) / (1 - (v0@ax)**2))) for w in c1 if abs(w@ax - v0@ax) < 1e-6)
print('rotation about shared 3-fold axis taking a cube-0 corner to nearest cube-1 corner (deg):', round(best, 4))
gx_ = list(gs); row = np.zeros(no); row[gx_] = 1
r3 = milp(np.ones(no), constraints=[LinearConstraint(A, 1, np.inf), LinearConstraint(row, -np.inf, len(gx_) - 1)], integrality=np.ones(no), bounds=Bounds(lb, 1))
print('another 16-orbit solution different from greedy?', r3.status == 0 and round(r3.fun) == 16, 'fun', r3.fun)
# per-copy minimum, symmetry not imposed
EE = set()
for i in range(n):
    gx = g(P - P[i]); gx[i] = 9
    for j in np.where(gx < 1 - 1e-9)[0]: EE.add(tuple(sorted((i, int(j)))))
B = np.zeros((len(EE), n))
for r, (a, b) in enumerate(EE): B[r, a] = B[r, b] = 1
r4 = milp(np.ones(n), constraints=[LinearConstraint(B, 1, np.inf)], integrality=np.ones(n), bounds=Bounds(0, 1))
print('clashing copy pairs', len(EE), '; min silenced copies without imposing five-fold symmetry:', round(r4.fun))
