import numpy as np, itertools
from scipy.optimize import least_squares
src = open('/tmp/claude-1000/-home-dicto-Downloads-pet-bottle-rhombiverse/7eb40546-e88a-4dc6-81d1-ac55e6f94c23/scratchpad/kres/studies/2026-10-21-b1nr-bent/b1nr_bent.py').read()
exec(src[:src.index('def mvc')])
V0 = V.copy()
# vertex orbit by J51 edge type: 0 = end-triangle edge (6), 1 = lateral prism edge (3), 2 = apex edge (12)
def etype(i, j):
    if i >= 6 or j >= 6: return 2
    return 1 if abs(J[i][2] - J[j][2]) > .5 else 0
vt = [etype(i, j) for i, j in E]
ecls = {}
for a, b in edges: ecls.setdefault(tuple(sorted((vt[a], vt[b]))), []).append((a, b))
print('edge classes', {k: len(v) for k, v in ecls.items()})
def planar(X, f):
    Q = X[f] - X[f].mean(0); return np.linalg.svd(Q)[1][-1]
def run(name, eq_classes, w_reg=None):
    def res(x):
        X = x.reshape(-1, 3); r = [planar(X, f) * 10 for k, f in faces]
        for c in eq_classes:                       # each listed class: all its edges length 1
            r += [np.linalg.norm(X[a] - X[b]) - 1 for a, b in ecls[c]]
        for c in ecls:                             # free classes: equal within the class only
            if c not in eq_classes:
                ls = [np.linalg.norm(X[a] - X[b]) for a, b in ecls[c]]; r += list(np.array(ls) - np.mean(ls))
        r += [X.mean(0)[k] for k in range(3)]
        if not eq_classes: r.append(np.linalg.norm(X[edges[0][0]] - X[edges[0][1]]) - 1)
        return np.array(r)
    s = least_squares(res, V0.ravel() + 1e-3 * np.random.default_rng(1).normal(size=V0.size), xtol=1e-14, ftol=1e-14, gtol=1e-14)
    X = s.x.reshape(-1, 3); pl = max(planar(X, f) for k, f in faces)
    lens = {c: np.round(sorted({round(np.linalg.norm(X[a] - X[b]), 5) for a, b in ecls[c]}), 5).tolist() for c in ecls}
    print(f'{name}: max out-of-plane {pl:.2e} | edge lengths by class {lens}')
    return X
XA = run("A all edges 1 + flat", list(ecls)); np.save("XA.npy", XA)
from scipy.spatial import ConvexHull
X = XA - XA.mean(0); H = ConvexHull(X)
print('corners on hull', len(H.vertices), 'of 21')
def angles(f):
    P = X[f]; n = len(P); return [round(np.degrees(np.arccos(np.clip((P[i-1]-P[i])@(P[(i+1)%n]-P[i]),-1,1))),2) for i in range(n)]
for k in ('sq', 'pent'):
    for kind, f in faces:
        if kind == k: print(k, angles(f), 'sum', round(sum(angles(f)),2))
# convex: every face plane has all points on one side
bad = 0
for kind, f in faces:
    P = X[f]; n = np.linalg.svd(P - P.mean(0))[2][-1]; d = (X - P.mean(0)) @ n
    if d.max() > 1e-5 and d.min() < -1e-5: bad += 1
print('faces with points on both sides (non-convex):', bad)
# symmetry: count distinct distances from centre
print('radii', sorted({round(float(np.linalg.norm(p)), 4) for p in X}))
