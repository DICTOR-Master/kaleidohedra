# Can the cut OG (rectified truncated icosahedron) be made with ALL edges equal and flat faces? (DICTO 5 Nov 2026)
import json, numpy as np, math
from scipy.spatial import ConvexHull
from scipy.optimize import least_squares
from fractions import Fraction as F
s5 = math.sqrt(5); D = json.load(open("step1-ocd-exact.json"))
q = lambda x: (lambda a, b: float(F(a)) + float(F(b))*s5)(*x.split("|")) if isinstance(x, str) else float(x)
V = np.array([[q(x) for x in p] for p in D["V"]]); V -= V.mean(0); P0 = V[np.linalg.norm(V, axis=1) < .69]
h = ConvexHull(P0); pl = {}
for eq, s in zip(h.equations, h.simplices): pl.setdefault(tuple(np.round(eq, 6)), set()).update(s)
FS = [sorted(f) for f in pl.values()]
import itertools
E = [(a, b) for a, b in itertools.combinations(range(len(P0)), 2) if sum(a in f and b in f for f in FS) == 2]
print("edges", len(E))
def res(x):
    P = x.reshape(-1, 3); L = np.array([np.linalg.norm(P[a] - P[b]) for a, b in E])
    r = list(L - 1)
    for f in FS:
        if len(f) > 3:
            Q = P[f] - P[f].mean(0); r += list(np.linalg.svd(Q)[1][-1:]*3)   # flatness
    r += list(P.mean(0))                                                       # fix translation
    return np.array(r)
x0 = (P0/np.mean([np.linalg.norm(P0[a] - P0[b]) for a, b in E])).ravel()
s = least_squares(res, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
P = s.x.reshape(-1, 3); R = np.abs(res(s.x)).max(); print("max residual", R)
hh = ConvexHull(P); print("convex (all corners on hull):", len(hh.vertices) == len(P))
print("radii spread", np.ptp(np.linalg.norm(P - P.mean(0), axis=1)).round(6), sorted(set(np.round(np.linalg.norm(P - P.mean(0), axis=1), 5))))
for n in (5, 6):
    f = next(f for f in FS if len(f) == n); c = P[f].mean(0); nrm = np.linalg.svd(P[f] - c)[2][-1]; e1 = P[f[0]] - c
    o = sorted(f, key=lambda i: math.atan2(np.cross(nrm, e1) @ (P[i] - c), e1 @ (P[i] - c)))
    ang = [math.degrees(math.acos(np.clip((P[o[i-1]] - P[o[i]]) @ (P[o[(i+1) % n]] - P[o[i]]), -1, 1))) for i in range(n)]
    print(n, "-gon angles", np.round(ang, 3))
np.save("equilateral.npy", P)
