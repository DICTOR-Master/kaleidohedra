#!/usr/bin/env python3
"""Exact recheck in Q(sqrt5) of the walls test. Work in R^5 (sum-zero space). For each 2-face of A and B (found by the float
run, then reconfirmed exactly coplanar), the central plane's normal n in Q(sqrt5)^5 is the nullspace of [face corners; (1,..,1)].
Directions of the 600-cell P (exact closure of X under self-reflection) and its cell centres; parallel = all 2x2 minors 0 exactly."""
import itertools, sympy as sp, numpy as np, runpy, io, contextlib, sys
r5 = sp.sqrt(5); p = (1 + r5) / 2
def orb(b): return [sp.Matrix(t).T for t in sorted(set(itertools.permutations(b)), key=str)]
def cen(S): m = sum(S, sp.zeros(1, 5)) / len(S); return [sp.simplify(v - m) for v in S]
X = cen(orb((p**2, p**2, p**2, p, 0))); F = cen(orb((p**2, p**2, 1, 1, 0)))
key = lambda v: tuple(sp.nsimplify(sp.expand(x)) for x in v)
Pd = {key(v): v for v in X}; grow = True
while grow:
    grow = False; L = list(Pd.values())
    for v in L:
        vv = sp.expand((v * v.T)[0])
        for w in L:
            u = (w - 2 * sp.expand((w * v.T)[0]) / vv * v).applyfunc(sp.radsimp); k = key(u)
            if k not in Pd: Pd[k] = u; grow = True
    assert len(Pd) <= 120, len(Pd)
P = list(Pd.values()); print('exact 600-cell corners:', len(P), flush=True)
def par(a, b): return all(sp.expand(a[i] * b[j] - a[j] * b[i]) == 0 for i in range(5) for j in range(i + 1, 5))
def normal(c):
    M = sp.Matrix.vstack(*c, sp.ones(1, 5)); ns = M.nullspace(); assert len(ns) == 1; return ns[0].T.applyfunc(sp.radsimp)
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(sys.argv[1] if len(sys.argv) > 1 else 'walls.py')
dirsP = []
for v in P:
    if not any(par(v, d) for d in dirsP): dirsP.append(v)
print('mirror directions:', len(dirsP), flush=True)
# cell centres: from the float hull's facets, rebuilt exactly from corner indices
Pf = np.array([[float(x) for x in v] for v in P]); Q = np.linalg.qr(np.vstack([np.ones(5), np.eye(5)[:4]]).T)[0][:, 1:5]
from scipy.spatial import ConvexHull
cells = ConvexHull(Pf @ Q).simplices; cc = []
for s_ in cells:
    v = (P[s_[0]] + P[s_[1]] + P[s_[2]] + P[s_[3]]).applyfunc(sp.radsimp)
    if not any(par(v, d) for d in cc): cc.append(v)
print('cell-centre directions:', len(cc), flush=True)
res = {}
for nm, S in (('A', X), ('B', F)):
    Sf = np.array([[float(x) for x in v] for v in S]) @ Q
    fac, rid = g['faces2'](Sf); r = {}
    for c in rid:
        pts = [S[i] for i in c]
        n = normal(pts[:3]); assert all(sp.expand((q * n.T)[0]) == 0 for q in pts)   # exact coplanarity with the centre
        k = (len(c), any(par(n, d) for d in dirsP), any(par(n, d) for d in cc)); r[k] = r.get(k, 0) + 1
    res[nm] = r; print(nm, '(corners, mirror wall, cell-parallel section):', r, flush=True)
ok = len(P) == 120 and len(dirsP) == 60 and len(cc) == 300 and all(k[1] or k[2] for k in list(res['A']) + list(res['B']))
print('FINAL ok' if ok else 'FINAL FAIL')
