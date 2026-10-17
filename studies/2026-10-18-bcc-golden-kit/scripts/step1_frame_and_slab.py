# DICTO 2026-10-18 "golden kit for the bcc packing" -- STEP 1: the frame, exactly. OCDs on the bcc lattice (hexagon to hexagon), each in
# its golden envelope RT (same frame, gbpc-geom-exact.json). Questions: (a) the slab between second neighbours: is the neighbour's
# face directly opposite (a right prism over the RT face) or offset? (b) does the RT face match a face of the lambda/phi oblate or the
# lambda/phi^2 prolate golden rhombohedron (the two pieces that stack to the slab height, slab-cover study)? -> data/step1-frame.json
import itertools
from exactpoly import *
G = json.load(open(os.path.join(HERE, '..', '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json')))
RT = [[q(x) for x in v] for v in G['RT']]; LB = [[q(x) for x in v] for v in G['LB']]; AX5 = [[q(x) for x in v] for v in G['AX5']]
nbs = []
for c in itertools.product(range(-2, 3), repeat=3):
    if c == (0, 0, 0): continue
    o = [Z, Z, Z]
    for k, Lv in zip(c, LB): o = vadd(o, vmul(Lv, qr(k)))
    nbs.append(o)
d2 = sorted({qs_(dot(o, o)) for o in nbs}, key=lambda s: qf(q(s)))[:3]
first = [o for o in nbs if qs_(dot(o, o)) == d2[0]]; second = [o for o in nbs if qs_(dot(o, o)) == d2[1]]; third = [o for o in nbs if qs_(dot(o, o)) == d2[2]]
PR = planes_of(RT)
o = second[0]
# the RT face facing o: plane n.x = d with n parallel to o
fa = [(n, d) for n, d in PR if all(x == Z for x in cross(n, o)) and sgn(dot(n, o)) > 0]
n, d = fa[0]
FA = [v for v in RT if dot(n, v) == d]
FB = [vsub(o, v) for v in FA]                  # the neighbour's facing face (RT is centrosymmetric)
offset = [vsub(b, a) for a, b in zip(FA, FB)]
perp = lambda w: vsub(w, vmul(n, qd(dot(w, n), dot(n, n))))
opposite = any(all(x == Z for x in perp(vsub(b, FA[0]))) for b in FB)
gap = qs(qd(dot(o, n), qr(1)), qm(qr(2), d))   # in units of |n|
edge2 = lambda P: sorted({qs_(dot(vsub(P[i], P[j]), vsub(P[i], P[j]))) for i in range(len(P)) for j in range(i + 1, len(P))}, key=lambda s: qf(q(s)))
PHI_ = PHI; lam = qm(PHI_, qr(Fr(1, 9))); iphi = qinv(PHI_)
ax_len2 = dot(AX5[0], AX5[0])
sizes = {'lambda/phi': qm(lam, iphi), 'lambda/phi^2': qm(qm(lam, iphi), iphi)}
rt_edge2 = q(edge2(FA)[0])
match = {k: qs_(qd(rt_edge2, qm(qm(s, s), ax_len2))) for k, s in sizes.items()}   # (RT edge / rhombohedron edge)^2
checks = dict(first_neighbours=len(first), second_neighbours=len(second), third_neighbours=len(third), dist2=d2,
              slab_face_corners=len(FA), neighbour_face_directly_opposite=opposite, slab_gap_times_n=qs_(gap), slab_gap=qf(gap) / qf(dot(n, n)) ** .5,
              rt_face_edge=qf(rt_edge2) ** .5, rt_edge_over_rhombohedron_edge_squared=match)
print(json.dumps(checks, indent=1)); save('step1-frame.json', dict(mark=MARK, step=1, checks=checks))
