# DICTO 2026-10-18 octet study -- STEP 15: the Penrose core = central thick Penrose prism (step 13) trimmed to the middle piece.
# Exact: prism side planes contain the axis a and the rhombus edges (all in Q(sqrt5)); core = prism & H - OCD1 - OCD2 (keys clear, step 14,
# checked exactly here), so vol core = vol(prism & H) - vol(prism & H & OCD1) - vol(prism & H & OCD2). -> data/step15-core.json
# Also writes data/step15-input.json (float) for the mesh split on dicto-node (step15_mesh.py).
import json as js, numpy as np
from exactpoly import *
S1 = load('step1-ocd-exact.json'); S5 = load('step5-keyed-octet.json')
V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R'])
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
i1 = [i for i in five if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]; c1 = V[i1]; o = [Z, R, R]; c2 = vsub(o, c1)
a = c1; aa = dot(a, a); P = lambda v: vsub(v, vmul(a, qd(dot(v, a), aa)))
star = sorted({j for f in S1['faces'] if i1 in f for j in f}); rel = [P(vsub(V[j], c1)) for j in star]
rr = [dot(t, t) for t in rel]; rt = max(rr, key=qf); tips = [t for t, x in zip(rel, rr) if x == rt]
iphi = qinv(PHI); d = P(vsub(c2, c1))
i, j = [(i, j) for i in range(5) for j in range(i + 1, 5) if all(x == y for x, y in zip(d, vmul(vadd(tips[i], tips[j]), iphi)))][0]
rh = [c1, vadd(c1, vmul(tips[i], iphi)), vadd(c1, d), vadd(c1, vmul(tips[j], iphi))]          # rhombus corners in the plane through c1
cen = [qm(qa(qa(qa(rh[0][k], rh[1][k]), rh[2][k]), rh[3][k]), qr(Fr(1, 4))) for k in range(3)]
side = []
for k in range(4):
    n = cross(vsub(rh[(k + 1) % 4], rh[k]), a); dd = dot(n, rh[k])
    if sgn(qs(dot(n, cen), dd)) > 0: n = [qn(x) for x in n]; dd = qn(dd)
    side.append((n, dd))
starpts = [V[jj] for jj in star]; PH = planes_of(starpts + [vsub(o, p) for p in starpts]); PO = planes_of(V)
vPH = volume(intersect(side + PH)); vPHO1 = volume(intersect(side + PH + PO)); vPHO2 = volume(intersect(side + PH + shift(PO, o)))
keyhit = [k for k, K in S5['keys'].items() for t in ([Z, Z, Z], o) if volume(intersect(side + PH + shift(planes_of([[q(x) for x in p] for p in K]), t))) != Z]
core = qs(qs(vPH, vPHO1), vPHO2)
mid = q(load('step11-exact.json')['checks']['middle'])
checks = dict(prism_and_hull=qs_(vPH), core=qs_(core), core_float=qf(core), keys_inside_core=keyhit, rest_of_middle=qs_(qs(mid, core)), rest_float=qf(qs(mid, core)),
              core_share_of_middle=qf(core) / qf(mid), core_symmetric=vPHO1 == vPHO2)
print(js.dumps(checks, indent=1))
save('step15-core.json', dict(mark=MARK, step=15, rhombus=[[qs_(x) for x in p] for p in rh], axis=[qs_(x) for x in a], checks=checks))
f = lambda v: [qf(x) for x in v]
js.dump(dict(rh=[f(p) for p in rh], a=f(a)), open(os.path.join(DATA, 'step15-input.json'), 'w'))
