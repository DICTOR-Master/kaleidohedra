# DICTO 2026-10-18 octet study -- STEP 11 (development stage 2: exact pieces). Exact volumes of the middle piece, notched cap and
# notched tetrahedra in Q(sqrt5), by convex pieces only:
#   vol M = vol H - 2 vol(H & OCD) - sum over the 4 keys of vol(H & key)       (H = hull of the two stars; OCDs and keys disjoint)
#   vol(M & octahedron 1) = vol(H & octa1) - vol(H & OCD1)                       (keys lie outside the octahedra)
#   notched cap = cap - 2 vol(M & octa1)   (each octahedron: 12 edges x one share each, over 6 equal caps)
#   notched tet = dented tet - 6 x (vol M - 2 vol(M & octa1)) / 2   (each M: two octahedron shares + two equal tetrahedron shares)
# Checks: the pieces sum exactly to the cell; agree with the step-10 meshes. -> data/step11-exact.json
import numpy as np
from exactpoly import *
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json')
V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R'])
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
i1 = [i for i in five if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]
o = [Z, R, R]; star = [V[j] for j in sorted({j for f in S1['faces'] if i1 in f for j in f})]
Hpts = star + [vsub(o, p) for p in star]
PH = planes_of(Hpts); PO = planes_of(V); PO2 = shift(PO, o)
octa = [[R if (i == j and s > 0) else (qn(R) if i == j else Z) for j in range(3)] for i in range(3) for s in (1, -1)]; Poct = planes_of(octa)
keys = {k: [[q(x) for x in p] for p in K] for k, K in S5['keys'].items()}
vH = volume(intersect(PH)); vHO = volume(intersect(PH + PO)); vHO2 = volume(intersect(PH + PO2))
assert vHO == vHO2, 'inversion symmetry'
vK = {}
for k, K in keys.items():
    for lab, t in (('ocd1', [Z, Z, Z]), ('ocd2', o)):
        c = intersect(PH + shift(planes_of(K), t))
        if c:
            v = volume(c)
            if v != Z: vK[f'{lab} {k}'] = v
vM = qs(qs(vH, qm(qr(2), vHO)), qr(0))
for v in vK.values(): vM = qs(vM, v)
vMoct = qs(volume(intersect(PH + Poct)), vHO)
cap = q(S2['checks']['cap_volume_each']); tetd = q(S5['checks']['piece_tet_with_4_dents']); ocdk = q(S5['checks']['piece_OCD_with_8_keys']); cell = q(S2['checks']['cell_volume'])
cap_n = qs(cap, qm(qr(2), vMoct)); tet_n = qs(tetd, qm(qr(3), qs(vM, qm(qr(2), vMoct))))
total = qa(qa(ocdk, qm(qr(6), cap_n)), qa(qm(qr(6), vM), qm(qr(2), tet_n)))
mesh = load('step10-meshes.json')
checks = dict(hull_H=qs_(vH), H_and_OCD=qs_(vHO), keys_in_H={k: qs_(v) for k, v in vK.items()},
              middle=qs_(vM), middle_float=qf(vM), middle_in_one_octa=qs_(vMoct), middle_in_one_octa_float=qf(vMoct),
              notched_cap=qs_(cap_n), notched_cap_float=qf(cap_n), notched_tet=qs_(tet_n), notched_tet_float=qf(tet_n),
              sum_equals_cell=total == cell,
              mesh_agreement=dict(middle=abs(qf(vM) - mesh['middle']['volume']), cap=abs(qf(cap_n) - mesh['cap']['volume']), tet=abs(qf(tet_n) - mesh['tet_notched']['volume'])))
print(json.dumps(checks, indent=1)); assert total == cell
save('step11-exact.json', dict(mark=MARK, step=11, checks=checks))
