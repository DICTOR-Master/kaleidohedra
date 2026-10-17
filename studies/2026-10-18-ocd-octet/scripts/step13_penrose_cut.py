# DICTO 2026-10-18 octet study -- STEP 13: a Penrose-rhombus cut of the middle region, seen down the five-fold axis (picture first).
# Proposal (Claude): the thick Penrose rhombus whose long diagonal is c1 -> c2 (projected); its edges run along the star spokes.
# Then on each side corner S a smaller thick rhombus (edge / phi) reaching one tip of each star. Exact checks on projected vectors
# (projection perpendicular to the axis a = c1 is exact in Q(sqrt5)). -> data/step13-penrose.json (+ 2D coords for the drawing)
import numpy as np
from q5 import *
S1 = load('step1-ocd-exact.json'); V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R'])
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
i1 = [i for i in five if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]; c1 = V[i1]; o = [Z, R, R]; c2 = vsub(o, c1)
a = c1; aa = dot(a, a); P = lambda v: vsub(v, vmul(a, qd(dot(v, a), aa)))
star = sorted({j for f in S1['faces'] if i1 in f for j in f}); rel = [P(vsub(V[j], c1)) for j in star]
rr = [dot(t, t) for t in rel]; rt = max(rr, key=qf); tips = [t for t, x in zip(rel, rr) if x == rt]
iphi = qinv(PHI); d = P(vsub(c2, c1))
# A: d = (t_a + t_b)/phi for a pair of tips (the rhombus edges c1->S1, c1->S2 lie along those spokes, length r/phi)
pairA = [(i, j) for i in range(5) for j in range(i + 1, 5) if all(x == y for x, y in zip(d, vmul(vadd(tips[i], tips[j]), iphi)))]
i, j = pairA[0]; S_1 = vmul(tips[i], iphi); S_2 = vmul(tips[j], iphi)               # side corners (relative to c1, projected)
# the thick rhombus angle at c1: cos = t_i.t_j / r^2 -> must be cos 72 (Penrose thick: 72 at c1, 108 at S)
cos_c1 = qd(dot(tips[i], tips[j]), rt); thick = qm(cos_c1, cos_c1) == (Fr(3, 8), Fr(-1, 8)) and sgn(cos_c1) > 0
# B: star 2 tips (relative to c1) = d - t_k ; flanking rhombus at S_1: edges S_1 -> tip_i of star 1 and S_1 -> a tip of star 2, both r/phi^2
T1 = tips[i]; star2_tips = [vsub(d, t) for t in tips]
e2 = qm(rt, qm(iphi, qm(iphi, qm(iphi, iphi))))       # (r/phi^2)^2
cand = [T for T in star2_tips if dot(vsub(T, S_1), vsub(T, S_1)) == e2]
flank_ok = len(cand) == 1 and dot(vsub(T1, S_1), vsub(T1, S_1)) == e2
if flank_ok:
    u, w = vsub(T1, S_1), vsub(cand[0], S_1); cs = qd(dot(u, w), e2); flank_thick = qm(cs, cs) == (Fr(3, 8), Fr(-1, 8)) and sgn(cs) < 0
else: flank_thick = False
checks = dict(diagonal_c1c2_equals_sum_of_two_spokes_over_phi=bool(pairA), central_rhombus_is_Penrose_thick=thick,
              edge_central=qf(rt) ** .5 / qf(PHI), flank_edges_reach_one_tip_of_each_star=flank_ok, flank_rhombus_is_Penrose_thick_108_at_S=flank_thick,
              edge_flank=qf(e2) ** .5)
print(checks)
af = np.array([qf(x) for x in a]); af /= np.linalg.norm(af); ub = np.cross(af, [1, 0, 0]); ub /= np.linalg.norm(ub); wb = np.cross(af, ub)
f2 = lambda v: [float(np.array([qf(x) for x in v]) @ ub), float(np.array([qf(x) for x in v]) @ wb)]
patch = dict(central=[f2([Z, Z, Z]), f2(S_1), f2(d), f2(S_2)])
if flank_ok:
    for nm, S_, T_a in (('flank1', S_1, T1), ('flank2', S_2, tips[j])):
        Tb = [T for T in star2_tips if dot(vsub(T, S_), vsub(T, S_)) == e2][0]
        patch[nm] = [f2(S_), f2(T_a), f2(vsub(vadd(T_a, Tb), S_)), f2(Tb)]
save('step13-penrose.json', dict(mark=MARK, step=13, proposal='Claude, for DICTO', checks=checks, patch=patch))
