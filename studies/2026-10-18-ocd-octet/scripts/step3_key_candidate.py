# DICTO 2026-10-18 octet study -- STEP 3 (candidate key, NOT adopted until DICTO chooses): the golden envelope's own corner.
# The OCD's golden envelope (RT, gbpc-geom-exact.json, same frame) pokes through each joint plane |x|+|y|+|z| = R as a small
# tetrahedron: its 3-fold corner + the 3 RT corners that lie exactly on the plane. Exact: those 3 lie on the octahedron's EDGES
# (base triangle inscribed in the face), the cap fits inside T+, volume. -> data/step3-key-candidate.json
import json, numpy as np
from q5 import *
G = json.load(open('../../2026-10-16-ocd-pyrochlore/data/gbpc-geom-exact.json')); RT = [[q(x) for x in v] for v in G['RT']]
S1 = load('step1-ocd-exact.json'); R = q(S1['R']); S2 = load('step2-octet-frame.json'); Tp = [[q(x) for x in v] for v in S2['Tplus']]
s = lambda v: qa(qa(v[0], v[1]), v[2])
top = max(RT, key=lambda v: qf(s(v))); base = [v for v in RT if s(v) == R and all(sgn(x) >= 0 for x in v)]
key = [top] + base
on_edges = all(any(x == Z for x in v) for v in base)
# inside T+: all 4 key corners on the inner side of each T+ face plane (exact)
def inside_tet(p, T):
    for i in range(4):
        F = [T[j] for j in range(4) if j != i]; n = cross(vsub(F[1], F[0]), vsub(F[2], F[0]))
        if sgn(dot(n, vsub(T[i], F[0]))) < 0: n = [qn(x) for x in n]
        if sgn(dot(n, vsub(p, F[0]))) < 0: return False
    return True
fits = all(inside_tet(p, Tp) for p in key)
d = det3(vsub(key[1], key[0]), vsub(key[2], key[0]), vsub(key[3], key[0])); vol = qm(d if sgn(d) > 0 else qn(d), qr(Fr(1, 6)))
height = qs(s(top), R)   # times 1/sqrt3 along the normal
checks = dict(base_corners=len(base), base_on_octa_edges=on_edges, key_inside_Tplus=fits, key_volume=qs_(vol), key_volume_float=qf(vol),
              apex_height_float=qf(height) / 3 ** .5, apex_l1=qs_(s(top)))
print(checks); print('key corners', [[qf(x) for x in v] for v in key])
save('step3-key-candidate.json', dict(mark=MARK, step=3, status='candidate, awaiting DICTO', key=[[qs_(x) for x in v] for v in key], checks=checks))
