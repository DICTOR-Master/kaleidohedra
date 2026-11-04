"""Exact Mahler products (affine invariant, about the corner centroid). h-piece: x, y·√3, z·√(3/2) make the corners rational -> exact in Q.
A cap: high-precision float (mpmath, 40 digits) from the network data, then identify in Q(√5)."""
import json, itertools, numpy as np, sympy as sp, mpmath as mp
from scipy.spatial import ConvexHull
def exact_mahler(P):
    P = [sp.Matrix(p) for p in P]; c = sum(P, sp.zeros(3, 1))/len(P); Q = [p - c for p in P]
    h = ConvexHull(np.array([[float(x) for x in q] for q in Q]))
    def vol(pts, simp): return sum(abs(sp.Matrix.hstack(pts[a], pts[b], pts[d]).det()) for a, b, d in simp)/6
    V = vol(Q, h.simplices)
    fs = {}
    for eq, s in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 8)), s)
    pol = []
    for s in fs.values():
        a, b, d = (Q[i] for i in s); n = (b - a).cross(d - a); off = n.dot(a)
        pol.append(n/off)
    hp = ConvexHull(np.array([[float(x) for x in q] for q in pol])); Vp = vol(pol, hp.simplices)
    return sp.nsimplify(sp.simplify(V*Vp))
H = sp.sqrt(sp.Rational(2, 3)); s3 = sp.sqrt(3)
hp = [(0,0,0),(0,1/s3,-H/2),(0,1/s3,0),(sp.Rational(1,2),-1/(2*s3),-H/2),(sp.Rational(1,2),-1/(2*s3),0),(sp.Rational(1,2),1/(2*s3),-H),(sp.Rational(1,2),s3/2,0),(1,0,0),(1,1/s3,-H/2),(1,1/s3,0)]
aff = sp.diag(1, s3, sp.sqrt(sp.Rational(3, 2)))
hp_r = [tuple(sp.nsimplify(sp.simplify(x)) for x in aff*sp.Matrix(p)) for p in hp]
print('h-piece rational corners', hp_r[:3], '...'); print('h-piece Mahler exact =', exact_mahler(hp_r))
A = json.load(open('data/admiral-network-pieces.json')); cap = next(p for p in A if p['kind'] == 'A')
P = np.unique(np.round(np.array([v for f in cap['faces'] for v in f]), 12), axis=0)
phi = (1 + sp.sqrt(5))/2
Pe = [tuple(sp.nsimplify(float(x), [sp.sqrt(5)], tolerance=1e-10) for x in p) for p in P]
print('A cap corners exact', Pe); m = exact_mahler(Pe); print('A cap Mahler exact =', m, '=', sp.N(m, 15))
