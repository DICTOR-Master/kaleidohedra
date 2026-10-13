# The dictosphere's facets (DICTO, 2026-10-14): 6 squares (cube directions) and 8 flat-ended triangles (octahedron directions),
# triangles meeting short side to short side: the intersection of a cube |x|,|y|,|z| <= 1 with an octahedron |x|+|y|+|z| <= s,
# 1.5 < s < 2. Hexagon sides: sqrt2 (s - 1) against the squares, sqrt2 (2 - s) against the other hexagons.
# When all 14 faces touch one sphere, s = sqrt3 and r = (sqrt3 - 1)/2, the cuboctahedral FUJI member. Compares with DICTO's
# measurements (long 4 cm, short 1.5 cm, sphere about 7.5 cm across). DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def solid(s):
    H = [list(n) + [-1.0] for n in np.vstack([np.eye(3), -np.eye(3)])]
    H += [list(np.array(sg)) + [-s] for sg in itertools.product((1, -1), repeat=3)]
    hs = HalfspaceIntersection(np.array(H, float), np.zeros(3)); return hs.intersections
def hexagon(s):
    V = solid(s); n = np.ones(3) / math.sqrt(3); on = V[np.abs(V @ n - s / math.sqrt(3)) < 1e-9]
    c = on.mean(0); a = on[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
    P = on[np.argsort(np.arctan2((on - c) @ b, (on - c) @ a))]
    return sorted(np.linalg.norm(P[i] - P[(i + 1) % len(P)]) for i in range(len(P)))
s = math.sqrt(3); sides = hexagon(s)
out = dict(s=s, octaPlaneDistance=s / math.sqrt(3), cubePlaneDistance=1.0, allFacesTangentToOneSphere=abs(s / math.sqrt(3) - 1) < 1e-12,
           hexSides=[round(x, 9) for x in sides], r=sides[0] / sides[-1], rExact=(3 ** .5 - 1) / 2)
out['rMatches'] = bool(abs(out['r'] - out['rExact']) < 1e-12)
# scale to DICTO's sphere: the long side 4 cm fixes the inradius
k = 4 / sides[-1]; out['inradiusFromLongSide_cm'] = k; out['predictedShortSide_cm'] = sides[0] * k
out['predictedInsphereDiameter_cm'] = 2 * k
# DICTO's measured r -> s
r = 1.5 / 4; out['measured_r'] = r; out['measured_s'] = (2 + r) / (1 + r); out['sqrt3'] = s
json.dump(out, open(os.path.join(ROOT, 'dictosphere.json'), 'w'), indent=1)
for k_, v in out.items(): print(k_, v)
# ports: a 3 cm port centred on each face (DICTO): clearance to the nearest edge of each face
port = 3.0
sq_half = sides[-1] * k / 2                       # square: half its side
hexR = 1 * k                                       # hexagon: distances from its centre to its long and short sides
nh = np.ones(3) / math.sqrt(3); V = solid(s); on = V[np.abs(V @ nh - s / math.sqrt(3)) < 1e-9]; c = on.mean(0)
def apothems(P, c):
    P = P[np.argsort(np.arctan2(*(np.c_[(P - c) @ np.cross(nh, (P[0] - c) / np.linalg.norm(P[0] - c)), (P - c) @ ((P[0] - c) / np.linalg.norm(P[0] - c))].T)))]
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]; t = (b - a) / np.linalg.norm(b - a); v = c - a; out.append((np.linalg.norm(b - a), np.linalg.norm(v - (v @ t) * t)))
    return out
ap = apothems(on, c)
res = dict(portDiameter_cm=port, squareClearance_cm=sq_half - port / 2,
           hexClearanceToLongSides_cm=min(d for L, d in ap if L > sides[0] * 1.5) * k - port / 2,
           hexClearanceToShortSides_cm=min(d for L, d in ap if L < sides[0] * 1.5) * k - port / 2)
json.dump({**out, **res}, open(os.path.join(ROOT, 'dictosphere.json'), 'w'), indent=1)
for k_, v in res.items(): print(k_, round(v, 3))
