# A cell-local kit (exact): each octahedron = OG + 8 caps (the octahedron minus the OG, cut by the planes through the centre and the
# octahedron's edges: one cap under each face); each tetrahedron whole. No piece crosses a cell face, so the kit fills the octet AND the
# gyrated octet (any stacking of the layers). Checks: the 8 caps have one volume, they and the OG fill the octahedron; which caps are
# mirror images of which (the octahedron's 8 faces under the OG's symmetry, which has no mirror through a face's axis).
import os, sys
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check.py')).read().split("n = (Q5(1), Q5(1), Q5(1))")[0])
from exact_inner import hullH
Rv = R
O6 = []
for j in range(3):
    for sgn in (1, -1):
        v = [Q5(0)] * 3; v[j] = Rv * sgn; O6.append(tuple(v))
vO, vOG = hullH(O6)['V'], hullH(V)['V']
caps = (vO - vOG) / 8
print('octahedron volume', vO, '| OG', vOG, '| each cap (octahedron - OG)/8 =', caps, '≈', round(caps.f(), 6), '| OG fills', round((vOG / vO).f() * 100, 2), '% of its octahedron')
# per face: the OG corners on it (the joint hexagon) for every face: all 8 faces carry a hexagon
faces = [(sx, sy, sz) for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)]
cnt = [sum(1 for v in V if (sx * v[0] + sy * v[1] + sz * v[2]) == Rv) for sx, sy, sz in faces]
print('joint-hexagon corners on each of the 8 faces:', cnt)
