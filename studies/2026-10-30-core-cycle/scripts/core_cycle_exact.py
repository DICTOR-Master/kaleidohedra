# Exact (Q(sqrt5)) check of the TI Star core's two-step cycle, with exactlib of the DICTO Solids data set (build/).
# Usage: core_cycle_exact.py <dataset build dir> <stations-exact.json of #78>
import json, os, sys
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1]); from exactlib import *
raw = json.load(open(sys.argv[2])); TI = [tuple(QF(Fr(a), Fr(b), 5) for a, b in v) for v in raw['TI']]
def turn(P, t):
    V, F = hull(P)
    feet = []
    for f in F:
        n = cross(sub(V[f[1]], V[f[0]]), sub(V[f[2]], V[f[0]])); feet.append((len(f), mul(dot(n, V[f[0]]) / dot(n, n), n)))
    tips = [(k, mul(t, p)) for k, p in feet]
    pen = [p for k, p in tips if k == 5]; hexa = [p for k, p in tips if k == 6]
    A, AF = hull(pen); B, BF = hull(hexa)
    core, CF = halfspace_solid(face_planes(A, AF) + face_planes(B, BF))
    r5 = dot(feet[[k for k, _ in feet].index(5)][1], feet[[k for k, _ in feet].index(5)][1]); r3 = dot(feet[[k for k, _ in feet].index(6)][1], feet[[k for k, _ in feet].index(6)][1])
    return V, F, [p for _, p in tips], core, CF, r5 / r3
out = {}
for name, t in [('phi', PHI), ('2', Q(2))]:
    V0, F0, tips0, C, CF, q0 = turn(TI, t)          # q = (pentagon foot distance / hexagon foot distance)^2
    V1, F1, tips1, C2, C2F, q1 = turn(C, t)
    k = t * t * Q(Fr(5, 15), Fr(2, 15))             # predicted two-turn scale t^2 (5 + 2 sqrt5)/15
    S2 = {tuple(x) for x in C2}; ST = {tuple(mul(k, v)) for v in V0}
    # hull of the core's tips vs the polar of TI: same directions (5-fold, 3-fold); shape fixed by (R5/R3)^2
    def ratio(P):
        V, F = hull(P); r = sorted({dot(v, v) for v in V}, key=lambda x: x.f()); return (len(V), r[-1] / r[0] if len(r) == 2 else Q(1))
    pol = polar(V0, F0, Q(1))
    out[name] = dict(q_TI=fmt(q0), q_core=fmt(q1), product=fmt(q0 * q1), product_is_1=(q0 * q1 == Q(1)),
                     next_core_equals_scaled_TI=(S2 == ST), scale=fmt(k),
                     core_tip_hull=[ratio(tips1)[0], fmt(ratio(tips1)[1])], polar_TI=[ratio(pol)[0], fmt(ratio(pol)[1])],
                     core_tip_hull_is_polar_TI_shape=(ratio(tips1)[1] == ratio(pol)[1]))
print(json.dumps(out, indent=1))
