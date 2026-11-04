import json, numpy as np, math
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
def det3(a, b, c): return a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def vol(P, simp): return sum(abs(det3(P[a], P[b], P[c])) for a, b, c in simp)/6
def mahler(P):  # exact for Fraction input; centre = corner centroid
    n = len(P); c = tuple(sum(p[i] for p in P)/n for i in range(3)); Q = [sub(p, c) for p in P]
    h = ConvexHull(np.array([[float(x) for x in q] for q in Q])); V = vol(Q, h.simplices)
    fs = {}
    for eq, s in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 8)), s)
    pol = []
    for a, b, d in fs.values():
        nrm = cross(sub(Q[b], Q[a]), sub(Q[d], Q[a])); off = dot(nrm, Q[a]); pol.append(tuple(x/off for x in nrm))
    hp = ConvexHull(np.array([[float(x) for x in q] for q in pol])); return V*vol(pol, hp.simplices)
# h-piece after (x, √3 y, √(3/2) z): corners rational
hp = [(0,0,0),(0,1,Fr(-1,2)),(0,1,0),(Fr(1,2),Fr(-1,2),Fr(-1,2)),(Fr(1,2),Fr(-1,2),0),(Fr(1,2),Fr(1,2),-1),(Fr(1,2),Fr(3,2),0),(1,0,0),(1,1,Fr(-1,2)),(1,1,0)]
hp = [tuple(Fr(x) for x in p) for p in hp]
m = mahler(hp); print('h-piece Mahler exact:', m, '=', float(m))
A = json.load(open('data/admiral-network-pieces.json')); cap = next(p for p in A if p['kind'] == 'A')
P = np.unique(np.round(np.array([v for f in cap['faces'] for v in f]), 12), axis=0)
print('A cap Mahler (float64):', repr(float(mahler([tuple(p) for p in P]))))
