# Flat-ended pyramid families (DICTO, 2026-10-14): pyramids with equal side edges 1 on an equiangular 2k-gon with sides 1 and r
# alternating, so that the k long faces are equilateral. Exist for k = 3 (FUJI's family, from the tetrahedron), k = 4 (octahedral,
# from the square pyramid J1) and k = 5 (icosahedral, from the pentagonal pyramid J2). The base is a regular k-gon of side
# s = 1 + r / cos(pi/k) with its corners cut; its long sides are at distance s / (2 tan(pi/k)) from the centre, so the base angle
# on the long sides is cos L = s / (sqrt3 tan(pi/k)). Checks that formula against coordinates, finds the flat member, and the
# member whose base continues the plane of solid X's face across a triangle edge: L + D_X = 180°. DICTO · dictospheres.com
import json, math, os
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
def pyramid(k, r):
    tot = 2 * math.pi / k
    s = 1 + r / math.cos(math.pi / k)                      # the regular k-gon before cutting
    Rk = s / (2 * math.sin(math.pi / k)); P = []
    for i in range(k):
        A = np.array([Rk * math.cos(i * tot), Rk * math.sin(i * tot), 0]); B = np.array([Rk * math.cos((i + 1) * tot), Rk * math.sin((i + 1) * tot), 0])
        u = (B - A) / s; c = r / (2 * math.cos(math.pi / k))
        P += [A + u * c, B - u * c]
    P = np.array(P); R = np.linalg.norm(P[0]); h = math.sqrt(max(0, 1 - R * R))
    return P, h
def cosL_formula(k, r): return (1 + r / math.cos(math.pi / k)) / (math.sqrt(3) * math.tan(math.pi / k))
def cosL_coords(k, r):
    P, h = pyramid(k, r); A, B = P[0], P[1]; apex = np.array([0, 0, h])
    n = np.cross(B - A, apex - A); n /= np.linalg.norm(n); return abs(n[2]) if h > 0 else 1.0
out = {'families': {}}
for k, name in ((3, 'triangular (FUJI)'), (4, 'square (octahedral)'), (5, 'pentagonal (icosahedral)')):
    rflat = brentq(lambda r: cosL_formula(k, r) - 1, 0, 1.5)
    P, h = pyramid(k, 0.0)
    sides = sorted(set(round(float(np.linalg.norm(P[i] - P[(i + 1) % len(P)])), 6) for i in range(len(P))))
    ok = all(abs(cosL_formula(k, r) - cosL_coords(k, r)) < 1e-12 for r in np.linspace(0, rflat * .99, 9))
    L0 = math.degrees(math.acos(cosL_formula(k, 0)))
    out['families'][k] = dict(name=name, flat_r=rflat, L_at_r0=L0, formula_matches_coordinates=ok, base_sides_at_r0=sides)
# face-plane members: dihedral D across a triangle's edge (to the face on the other side)
D = {'octahedron (tri-tri)': math.acos(-1 / 3), 'icosahedron (tri-tri)': math.acos(-5 ** .5 / 3),
     'cuboctahedron (tri-square)': math.acos(-1 / 3 ** .5), 'icosidodecahedron (tri-pentagon)': math.acos(-math.sqrt((5 + 2 * 5 ** .5) / 15)),
     'rhombicuboctahedron (tri-square)': math.acos(-math.sqrt(2 / 3)), 'rhombicosidodecahedron (tri-square)': math.radians(159.0948),
     'snub cube (tri-square)': math.radians(142.9834), 'snub cube (tri-tri)': math.radians(153.2347),
     'snub dodecahedron (tri-pentagon)': math.radians(152.9299), 'snub dodecahedron (tri-tri)': math.radians(164.1754),
     'truncated tetrahedron (tri-hexagon)': math.acos(-1 / 3), 'tetrahedron (tri-tri)': math.acos(1 / 3)}
for n in range(3, 11): D[f'{n}-gonal antiprism (tri-tri)'] = math.acos((1 - 4 * math.cos(math.pi / n)) / 3)
matches = {}
for k in (3, 4, 5):
    rows = []
    for name, d in D.items():
        want = math.cos(math.pi - d)                       # cos L needed
        r = (want * math.sqrt(3) * math.tan(math.pi / k) - 1) * math.cos(math.pi / k)
        if -1e-12 <= r <= out['families'][k]['flat_r'] + 1e-12: rows.append((name, round(r, 6)))
    matches[k] = rows
out['faceMatches'] = matches
json.dump(out, open(os.path.join(ROOT, 'kfamilies.json'), 'w'), indent=1)
for k, f in out['families'].items(): print(k, f)
for k, rows in matches.items(): print(k, rows)
