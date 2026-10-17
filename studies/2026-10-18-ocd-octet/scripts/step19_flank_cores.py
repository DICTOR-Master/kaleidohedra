# DICTO 2026-10-18 octet study -- STEP 19: the flanking Penrose cores in the keyless full kit (step 18), exactly.
# Flank prism k = the step-13 flank rhombus (one phi-step smaller thick Penrose rhombus at a side corner S) run along the axis a.
# Without keys, M0 = H - OCD1 - OCD2. Flank core = flank prism & H - OCD1 - OCD2 (convex parts, exact). Checks: volumes, both flanks
# equal, the three cores pairwise interior-disjoint (exact), what is left of M0. Writes data/step19-input.json for the node mesh check.
import json as js
from exactpoly import *
S1 = load('step1-ocd-exact.json'); V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R'])
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
i1 = [i for i in five if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]; c1 = V[i1]; o = [Z, R, R]; c2 = vsub(o, c1)
a = c1; aa = dot(a, a); P = lambda v: vsub(v, vmul(a, qd(dot(v, a), aa)))
star = sorted({j for f in S1['faces'] if i1 in f for j in f}); rel = [P(vsub(V[j], c1)) for j in star]
rr = [dot(t, t) for t in rel]; rt = max(rr, key=qf); tips = [t for t, x in zip(rel, rr) if x == rt]
iphi = qinv(PHI); d = P(vsub(c2, c1)); e2 = qm(rt, qm(iphi, qm(iphi, qm(iphi, iphi))))
i, j = [(i, j) for i in range(5) for j in range(i + 1, 5) if all(x == y for x, y in zip(d, vmul(vadd(tips[i], tips[j]), iphi)))][0]
star2 = [vsub(d, t) for t in tips]
def flank(S_, Ta):
    Tb = [T for T in star2 if dot(vsub(T, S_), vsub(T, S_)) == e2][0]
    return [S_, Ta, vsub(vadd(Ta, Tb), S_), Tb]
rhombi = {'central': [[Z, Z, Z], vmul(tips[i], iphi), d, vmul(tips[j], iphi)],
          'flank1': flank(vmul(tips[i], iphi), tips[i]), 'flank2': flank(vmul(tips[j], iphi), tips[j])}
rhombi = {k: [vadd(c1, p) for p in Q] for k, Q in rhombi.items()}
def side_planes(Q):
    cen = [qm(qa(qa(qa(Q[0][k], Q[1][k]), Q[2][k]), Q[3][k]), qr(Fr(1, 4))) for k in range(3)]; out = []
    for k in range(4):
        n = cross(vsub(Q[(k + 1) % 4], Q[k]), a); dd = dot(n, Q[k])
        if sgn(qs(dot(n, cen), dd)) > 0: n = [qn(x) for x in n]; dd = qn(dd)
        out.append((n, dd))
    return out
starpts = [V[jj] for jj in star]; PH = planes_of(starpts + [vsub(o, p) for p in starpts]); PO = planes_of(V); PO2 = shift(PO, o)
vol = {}
for k, Q in rhombi.items():
    sp = side_planes(Q)
    vol[k] = qs(qs(volume(intersect(sp + PH)), volume(intersect(sp + PH + PO))), volume(intersect(sp + PH + PO2)))
pairs = {f'{a_}&{b_}': qs_(volume(intersect(side_planes(rhombi[a_]) + side_planes(rhombi[b_]) + PH))) for a_, b_ in (('central', 'flank1'), ('central', 'flank2'), ('flank1', 'flank2'))}
M0 = qs(qs(volume(intersect(PH)), volume(intersect(PH + PO))), volume(intersect(PH + PO2)))
rest = qs(qs(qs(M0, vol['central']), vol['flank1']), vol['flank2'])
checks = dict(M0=qs_(M0), M0_float=qf(M0), cores={k: qs_(v) for k, v in vol.items()}, cores_float={k: qf(v) for k, v in vol.items()},
              flanks_equal=vol['flank1'] == vol['flank2'], prism_pair_overlaps_in_H=pairs, rest_after_three_cores=qs_(rest), rest_float=qf(rest),
              three_cores_share_of_M0=qf(qa(qa(vol['central'], vol['flank1']), vol['flank2'])) / qf(M0))
print(js.dumps(checks, indent=1))
save('step19-flank-cores.json', dict(mark=MARK, step=19, checks=checks, rhombi={k: [[qs_(x) for x in p] for p in Q] for k, Q in rhombi.items()}))
js.dump(dict(rhombi={k: [[qf(x) for x in p] for p in Q] for k, Q in rhombi.items()}, a=[qf(x) for x in a]), open(os.path.join(DATA, 'step19-input.json'), 'w'))
