# Which FUJI(r) complete a face with which solid? FUJI(r)'s base meets each equilateral side face at L(r) along a long side.
# A solid X with unit-edge triangles whose dihedral across that triangle's edge is D_X continues the base plane when
# L(r) + D_X = 180 degrees (as the icosahedron does for FUJI in the Lotus seed: 41.81 + 138.19). Solves for r per solid.
# DICTO · dictospheres.com
import math, json, os
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
def angles(r):
    R = math.sqrt((1 + r + r * r) / 3); h = math.sqrt(1 - R * R)
    a = 2 * math.asin(1 / (2 * R))
    dL = R * math.cos(a / 2); dS = R * math.cos((2 * math.pi / 3 - a) / 2)   # apothems of long and short sides
    return math.degrees(math.atan2(h, dL)), math.degrees(math.atan2(h, dS))
D = {  # dihedral across an edge of a unit triangle face (degrees), with what is on the other side
    'tetrahedron (tri-tri)': math.degrees(math.acos(1 / 3)),
    'octahedron (tri-tri)': math.degrees(math.acos(-1 / 3)),
    'icosahedron (tri-tri)': math.degrees(math.acos(-5 ** .5 / 3)),
    'cuboctahedron (tri-square)': math.degrees(math.acos(-1 / 3 ** .5)),
    'icosidodecahedron (tri-pentagon)': math.degrees(math.acos(-math.sqrt((5 + 2 * 5 ** .5) / 15))),
    'truncated tetrahedron (tri-hexagon)': math.degrees(math.acos(-1 / 3)),
    'triangular prism (tri-square)': 90.0,
    'square antiprism (tri-tri)': 127.5516,
    'square antiprism (tri-square)': 103.8362,
    'pentagonal antiprism (tri-tri)': 138.1897,
    'snub cube (tri-tri)': 153.2347,
    'snub cube (tri-square)': 142.9834,
    'snub dodecahedron (tri-tri)': 164.1754,
    'snub dodecahedron (tri-pentagon)': 152.9299,
    'rhombicuboctahedron (tri-square)': 144.7356,
    'rhombicosidodecahedron (tri-square)': 159.0948,
}
rows = []
for name, d in D.items():
    want = 180 - d
    if not (0 < want < angles(0)[0]): rows.append(dict(solid=name, dihedral=d, r=None)); continue
    r = brentq(lambda r: angles(r)[0] - want, 0, 1 - 1e-12, xtol=1e-14)
    rows.append(dict(solid=name, dihedral=round(d, 4), baseAngle=round(want, 4), r=r, shortSideAngle=round(angles(r)[1], 4)))
json.dump(dict(credit='DICTO · dictospheres.com', rows=rows), open(os.path.join(ROOT, 'gaps.json'), 'w'), indent=1)
for x in rows: print(x)
print('1/phi', 1 / phi)
