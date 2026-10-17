# DICTO 2026-10-18 "could five lobed patterns on ocd surface be built into penrose prisms to connect with each other" -- STEP 4:
# the two facing five-kite stars in the octet, seen down the five-fold axis. Exact: the neighbour's corner c2 = R(0,1,1) - c1;
# project both stars on the plane perpendicular to a = c1 and test whether c2 lands exactly on a star-1 corner.
# -> data/step4-stars.json (exact checks + 2D float coords for the drawing)
import numpy as np
from q5 import *
S1 = load('step1-ocd-exact.json'); V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R'])
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf)
F = [i for i, v in enumerate(V) if r2[i] == rmax]
i1 = [i for i in F if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]; c1 = V[i1]
o = [Z, R, R]; c2 = [qs(o[k], c1[k]) for k in range(3)]             # neighbour OCD's antiparallel corner
a = c1; aa = dot(a, a)
def perp(p): t = qd(dot(p, a), aa); return [qs(p[k], qm(t, a[k])) for k in range(3)], t
star1 = sorted({j for f in S1['faces'] if i1 in f for j in f})
nb_star = [[qs(o[k], V[j][k]) for k in range(3)] for j in star1]   # star 2 = point reflection of star 1 through o/2
d_perp, d_ax = perp(vsub(c2, c1))
hits = [j for j in star1 if perp(vsub(V[j], c1))[0] == d_perp]
radius2 = max((dot(perp(vsub(V[j], c1))[0], perp(vsub(V[j], c1))[0]) for j in star1), key=qf)
checks = dict(corner_c1=[qs_(x) for x in c1], neighbour_centre='R(0,1,1)', star_corners=len(star1),
              offset_along_axis=qf(d_ax) * qf(aa) ** .5, offset_sideways=qf(dot(d_perp, d_perp)) ** .5, star_radius=qf(radius2) ** .5,
              c2_over_star1_corner_exact=bool(hits), sideways_equals_star_radius_exact=dot(d_perp, d_perp) == radius2)
print(checks)
# 2D drawing coords: basis u, w perpendicular to a
af = np.array([qf(x) for x in a]); af /= np.linalg.norm(af); u = np.cross(af, [1, 0, 0]); u /= np.linalg.norm(u); w = np.cross(af, u)
c1f = np.array([qf(x) for x in c1])
P2 = lambda p: [float((np.array([qf(x) for x in p]) - c1f) @ u), float((np.array([qf(x) for x in p]) - c1f) @ w)]
H = lambda p: float((np.array([qf(x) for x in p]) - c1f) @ af)
kites1 = []; kites2 = []
for f in S1['faces']:
    if i1 in f:
        P = np.array([[qf(x) for x in V[j]] for j in f]); c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n = n if n @ c > 0 else -n
        uu = P[0] - c; ww = np.cross(n, uu); order = [f[k] for k in np.argsort(np.arctan2((P - c) @ ww, (P - c) @ uu))]
        kites1.append([P2(V[j]) for j in order]); kites2.append([P2([qs(o[k], V[j][k]) for k in range(3)]) for j in order])
# second ring (faces touching star 1 corners) for context
ring1 = []; ring2 = []
for f in S1['faces']:
    if i1 not in f and any(j in star1 for j in f):
        P = np.array([[qf(x) for x in V[j]] for j in f]); c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n = n if n @ c > 0 else -n
        if n @ af < 0.2: continue
        uu = P[0] - c; ww = np.cross(n, uu); order = [f[k] for k in np.argsort(np.arctan2((P - c) @ ww, (P - c) @ uu))]
        ring1.append([P2(V[j]) for j in order]); ring2.append([P2([qs(o[k], V[j][k]) for k in range(3)]) for j in order])
save('step4-stars.json', dict(mark=MARK, step=4, checks=checks, c1=P2(c1), c2=P2(c2), height_c2=H(c2), kites1=kites1, kites2=kites2, ring1=ring1, ring2=ring2,
     star1_heights=[H(V[j]) for j in star1]))
