# DICTO's infinite expansion, basic premise: can phi^2 * (AXE, FUJI, CLEO) be filled by the Lotus family at edge scale 1
# (icosahedron I, small icosahedron i, AXE, FUJI, CLEO)? Necessary conditions: volume and Dehn invariant, exactly.
import json, sys, itertools, numpy as np, mpmath as mp
from scipy.optimize import milp, LinearConstraint, Bounds
mp.mp.dps = 15
P = json.load(open(sys.argv[1])); PHI = (1 + 5 ** .5) / 2; R5 = 5 ** .5
def vol(V, F):
    V = np.array(V); c = V.mean(0); s = 0
    for f in F:
        for i in range(1, len(f) - 1): s += abs(np.dot(V[f[0]] - c, np.cross(V[f[i]] - c, V[f[i + 1]] - c))) / 6
    return s
def edges(V, F):
    V = np.array(V); c = V.mean(0); nrm = []
    for f in F:
        n = np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]); n /= np.linalg.norm(n); nrm.append(n if n @ (V[f[0]] - c) > 0 else -n)
    E = {}
    for fi, f in enumerate(F):
        for k in range(len(f)):
            a, b = sorted((f[k], f[(k + 1) % len(f)])); E.setdefault((a, b), []).append(fi)
    out = []
    for (a, b), fs in E.items():
        if len(fs) != 2: continue
        ang = np.pi - np.arccos(np.clip(nrm[fs[0]] @ nrm[fs[1]], -1, 1))
        if abs(ang - np.pi) < 1e-9: continue                      # flat (coplanar split): no contribution
        out.append((float(np.linalg.norm(V[a] - V[b])), ang))
    return out
types = {}
for p in P:
    r = p['role']; v = vol(p['vertices'], p['faces'])
    key = r if r != 'ico' else ('I' if v > 1 else 'i')
    types.setdefault(key, (p['vertices'], p['faces'], v))
def qs5(x):                                                      # x = (a + b sqrt5) / den
    for den in (1, 2, 3, 4, 6, 8, 12, 24, 48):
        for b in range(-400, 401):
            a = x * den - b * R5
            if abs(a - round(a)) < 2e-6: return (round(a), b, den)
    raise ValueError(x)
# distinct dihedral angles and their rational relations with pi
angs = sorted({round(a, 6) for t in types.values() for _, a in edges(t[0], t[1])})
print('distinct dihedral angles (deg):', [round(np.degrees(a), 4) for a in angs])
# the two independent angles (Dehn basis of this family): 37.3774 and arccos(sqrt5/3) = 41.8103 degrees
basis = [a for a in angs if abs(np.degrees(a) - 37.3774) < 1e-3 or abs(np.degrees(a) - 41.8103) < 1e-3]
coord = {}
for a in angs:
    rel = mp.pslq([mp.mpf(a), mp.mpf(basis[0]), mp.mpf(basis[1]), mp.pi], maxcoeff=12, maxsteps=10 ** 5, tol=mp.mpf(10) ** -5)
    assert rel and rel[0] != 0, a
    coord[round(a, 6)] = [mp.mpf(-rel[1]) / rel[0], mp.mpf(-rel[2]) / rel[0]]
    print(f'  {np.degrees(a):.4f} = {coord[round(a,6)][0]} x 37.38 + {coord[round(a,6)][1]} x 41.81 (mod 180)')
print('angle basis (deg):', [round(np.degrees(b), 4) for b in basis])
# Dehn vector of each type: for each basis angle, sum length*coeff, written as (a + b sqrt5) -> 2 reals
def dehn(V, F, scale=1.0):
    D = np.zeros((len(basis), 2))
    for L, a in edges(V, F):
        c = coord[round(a, 6)]
        for j, cj in enumerate(c):
            if cj == 0: continue
            q = qs5(L * scale); val = float(cj)
            D[j] += np.array([q[0], q[1]]) / q[2] * val
    return D.ravel()
names = list(types)
for k in names: print(f'  {k}: volume = {qs5(types[k][2])}  (a,b,den of (a+b√5)/den)')
cols = np.array([[types[k][2]] + list(dehn(types[k][0], types[k][1])) for k in names]).T
for target in ('I', 'axe', 'fuji', 'cleo'):
    V, F, v = types[target]
    rhs = np.array([v * PHI ** 6] + list(dehn(V, F, PHI ** 2)))
    n = len(names)
    res = milp(c=np.ones(n), constraints=LinearConstraint(cols, rhs - 1e-6, rhs + 1e-6), integrality=np.ones(n), bounds=Bounds(0, 400))
    print(f'phi^2 x {target}: ' + ('counts ' + str(dict(zip(names, np.round(res.x).astype(int)))) if res.success else 'NO whole-number solution (volume + Dehn)'))
    # volume only, for comparison
    res2 = milp(c=np.ones(n), constraints=LinearConstraint(cols[:1], rhs[:1] - 1e-7, rhs[:1] + 1e-7), integrality=np.ones(n), bounds=Bounds(0, 400))
    print(f'    volume only: ' + (str(dict(zip(names, np.round(res2.x).astype(int)))) if res2.success else 'none'))
# sanity: the Lotus seed's actual counts must satisfy the phi^2 x I equations
cnt = {'I': 12, 'i': 1, 'axe': 60, 'fuji': 20, 'cleo': 20}
lhs = cols @ np.array([cnt[k] for k in names]); V, F_, v = types['I']; rhs = np.array([v * PHI ** 6] + list(dehn(V, F_, PHI ** 2)))
print('Lotus seed check (should be ~0):', np.abs(lhs - rhs).max())
print('Dehn vectors:', {k: np.round(dehn(types[k][0], types[k][1]), 4).tolist() for k in names})
