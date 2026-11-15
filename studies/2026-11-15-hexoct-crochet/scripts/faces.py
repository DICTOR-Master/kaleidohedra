#!/usr/bin/env python3
"""Exact faces of Narcissus (HexOct h-piece, lambda >= 3/8) and the cube (c-piece), ball spacing a = 1.
Narcissus corners as in paper #98 (Narcissus and Covenant). Writes data/faces.json: every face with side lengths as sqrt of exact rational squares (checked to 1e-12) and corner angles."""
import json, math, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
r3 = math.sqrt(3); H = math.sqrt(2/3); h = 0.5
N = [(0,0,0),(0,1/r3,-H/2),(0,1/r3,0),(h,-1/(2*r3),-H/2),(h,-1/(2*r3),0),(h,1/(2*r3),-H),(h,r3/2,0),(1,0,0),(1,1/r3,-H/2),(1,1/r3,0)]
e = 1/math.sqrt(2); C = list(itertools.product((0, e), repeat=3))

def faces(P):
    X = np.array([[float(c) for c in p] for p in P]); hull = ConvexHull(X); fs = {}
    for eq, s in zip(hull.equations, hull.simplices): fs.setdefault(tuple(np.round(eq, 9)), set()).update(s)
    out = []
    for k, idx in fs.items():
        n = np.array(k[:3]); idx = list(idx); c = X[idx].mean(0); u = X[idx[0]] - c; w = np.cross(n, u)
        idx.sort(key=lambda i: math.atan2((X[i]-c) @ w, (X[i]-c) @ u)); m = len(idx)
        sq = [Fr(float(np.sum((X[idx[(j+1) % m]] - X[idx[j]])**2))).limit_denominator(1000) for j in range(m)]
        assert all(abs(float(q) - np.sum((X[idx[(j+1) % m]] - X[idx[j]])**2)) < 1e-12 for j, q in enumerate(sq))
        sides = ['sqrt(%s)' % q for q in sq]
        ang = []
        for j in range(m):
            a = X[idx[j-1]] - X[idx[j]]; b = X[idx[(j+1) % m]] - X[idx[j]]
            ang.append(round(math.degrees(math.acos(a @ b/np.linalg.norm(a)/np.linalg.norm(b))), 4))
        out.append({'normal': [round(float(x), 6) for x in n], 'corners': [int(i) for i in idx], 'sides': [str(s) for s in sides],
                    'sides_f': [round(math.sqrt(q), 6) for q in sq], 'angles_deg': ang})
    return out, hull.volume, X

res = {}
for name, P in (('Narcissus', N), ('cube', C)):
    F, vol, X = faces(P)
    res[name] = {'corners': None, 'corners_f': X.round(6).tolist(), 'faces': F, 'volume': vol}
    print(name, 'faces', len(F), 'volume', round(vol, 6))
    for f in F: print('  ', len(f['corners']), 'sides', f['sides'], 'angles', f['angles_deg'])
print('check Narcissus volume = sqrt2/4:', abs(res['Narcissus']['volume'] - math.sqrt(2)/4) < 1e-12,
      '| cube volume = sqrt2/4:', abs(res['cube']['volume'] - math.sqrt(2)/4) < 1e-12)
json.dump(res, open('data/faces.json', 'w'), indent=1)
