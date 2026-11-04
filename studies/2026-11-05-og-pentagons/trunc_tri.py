# DICTO 5 Nov 2026: make all 20 hexagons TRUNCATED TRIANGLES (all angles 120°, sides alternating long/short).
# With mirrors (full Ih) every hexagon side is equal, so this needs the rotation group I only: a chiral (left/right) family.
import json, numpy as np, math, itertools
from scipy.spatial import ConvexHull
from scipy.optimize import least_squares
from fractions import Fraction as F
s5 = math.sqrt(5); D = json.load(open("step1-ocd-exact.json"))
q = lambda x: (lambda a, b: float(F(a)) + float(F(b))*s5)(*x.split("|")) if isinstance(x, str) else float(x)
V = np.array([[q(x) for x in p] for p in D["V"]]); V -= V.mean(0); C = V[np.linalg.norm(V, axis=1) < .69]
h = ConvexHull(C); pl = {}
for eq, s in zip(h.equations, h.simplices): pl.setdefault(tuple(np.round(eq, 6)), set()).update(s)
FS = [sorted(f) for f in pl.values()]; HEX = [f for f in FS if len(f) == 6]
deg = np.array([sum(i in f for f in FS) for i in range(len(C))])
on6 = np.array([sum(i in f for f in HEX) for i in range(len(C))])      # q: in 2 hexagons; p: in 1
Pidx = np.where(on6 == 1)[0]; Qidx = np.where(on6 == 2)[0]
# rotation group I: proper orthogonal maps permuting C
R = []
for a, b in itertools.product(range(len(C)), repeat=2):
    pass
A = C[Pidx[0]], C[Pidx[1]]
base = np.array([C[Pidx[0]], C[Qidx[0]], np.cross(C[Pidx[0]], C[Qidx[0]])]).T
for j, k in itertools.product(Pidx, Qidx):
    T = np.array([C[j], C[k], np.cross(C[j], C[k])]).T
    if abs(np.linalg.det(T)) < 1e-9: continue
    M = T @ np.linalg.inv(base)
    if np.allclose(M @ M.T, np.eye(3), atol=1e-6) and np.linalg.det(M) > 0:
        img = C @ M.T
        if all(np.min(np.linalg.norm(C - x, axis=1)) < 1e-6 for x in img): R.append(M)
print("rotations", len(R))
p0, qd = C[Pidx[0]], C[Qidx[0]] / np.linalg.norm(C[Qidx[0]])
def build(x):
    p = p0 + x[:3]; qq = qd * x[3]; P = C.copy()
    for M in R:
        for src, idx in ((p, Pidx), (qq, Qidx)):
            y = M @ (C[Pidx[0]] if idx is Pidx else C[Qidx[0]]); i = idx[np.argmin(np.linalg.norm(C[idx] - y, axis=1))]
            P[i] = M @ src
    return P
def hexinfo(P, f):
    c = P[f].mean(0); n = np.linalg.svd(P[f] - c)[2][-1]; e1 = P[f[0]] - c
    o = sorted(f, key=lambda i: math.atan2(np.cross(n, e1) @ (P[i] - c), e1 @ (P[i] - c)))
    ang = [math.degrees(math.acos(np.clip((P[o[i-1]] - P[o[i]]) @ (P[o[(i+1) % 6]] - P[o[i]]) / np.linalg.norm(P[o[i-1]] - P[o[i]]) / np.linalg.norm(P[o[(i+1) % 6]] - P[o[i]]), -1, 1))) for i in range(6)]
    sides = [np.linalg.norm(P[o[i]] - P[o[(i+1) % 6]]) for i in range(6)]
    return np.linalg.svd(P[f] - c)[1][-1], ang, sides
def flat(P, f): return np.linalg.svd(P[f] - P[f].mean(0))[1][-1]
out = []
for t in np.linspace(0, .3, 7):              # t = how far the sides split: (long - short)/(long + short)
    def res(x):
        P = build(x); fl, ang, sd = hexinfo(P, HEX[0])
        r = [fl, ang[0] - 120, ang[1] - 120, (max(sd) - min(sd))/(max(sd) + min(sd)) - t, np.linalg.norm(P[Qidx[0]]) - np.linalg.norm(C[Qidx[0]])]
        r += [flat(P, f) for f in FS if len(f) == 5][:1] + [flat(P, f) for f in HEX[1:3]]
        return np.array(r)
    s = least_squares(res, np.r_[0, 0, 0, np.linalg.norm(C[Qidx[0]])] if not out else out[-1][1], xtol=1e-14, ftol=1e-14)
    P = build(s.x); fl, ang, sd = hexinfo(P, HEX[0]); hh = ConvexHull(P)
    tri = [f for f in FS if len(f) == 3][0]; ts = sorted(np.linalg.norm(P[a] - P[b]) for a, b in itertools.combinations(tri, 2))
    maxflat = max(flat(P, f) for f in FS if len(f) > 3)
    print(f"split {t:.2f}: residual {np.abs(res(s.x)).max():.1e}, faces flat {maxflat:.1e}, convex {len(hh.vertices) == len(P)}, hexagon sides {min(sd):.4f}/{max(sd):.4f} angles {np.round(ang, 2).tolist()}, triangle sides {np.round(ts, 4).tolist()}")
    out.append((t, s.x))
np.save("trunc-tri-family.npy", np.array([o[1] for o in out]))
# save left (computed) and right (mirror) at split 0.30 for rendering
P = build(out[6][1]); np.save("trunc-tri-left.npy", P); np.save("trunc-tri-right.npy", P * np.array([-1, 1, 1]))
