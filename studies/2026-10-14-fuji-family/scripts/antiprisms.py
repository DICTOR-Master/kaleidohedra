# FUJI(r) and the antiprisms (DICTO, 2026-10-14): the r at which FUJI(r)'s base continues the plane of an n-gonal antiprism's
# triangles (base angle + the antiprism's triangle-triangle dihedral = 180) is r = 2 cos(pi/n) - 1, checked for n = 3..12.
# DICTO · dictospheres.com
import math, numpy as np
from scipy.optimize import brentq
def L(r):
    R = math.sqrt((1 + r + r * r) / 3); h = math.sqrt(1 - R * R); a = 2 * math.asin(1 / (2 * R)); return math.degrees(math.atan2(h, R * math.cos(a / 2)))
def tritri(n):
    R = 1 / (2 * math.sin(math.pi / n)); H = math.sqrt(1 - (2 * R * math.sin(math.pi / (2 * n))) ** 2)
    t = [np.array([R * math.cos(2 * math.pi * k / n), R * math.sin(2 * math.pi * k / n), H / 2]) for k in range(n)]
    b = [np.array([R * math.cos(2 * math.pi * k / n + math.pi / n), R * math.sin(2 * math.pi * k / n + math.pi / n), -H / 2]) for k in range(n)]
    def nrm(p, q, s):
        v = np.cross(q - p, s - p); return v / np.linalg.norm(v) * (1 if v @ ((p + q + s) / 3) > 0 else -1)
    return 180 - math.degrees(math.acos(nrm(t[0], b[0], t[1]) @ nrm(t[0], b[-1], b[0])))
worst = 0
for n in range(4, 13):
    r = brentq(lambda r: L(r) - (180 - tritri(n)), 0, 1 - 1e-12, xtol=1e-15)
    worst = max(worst, abs(r - (2 * math.cos(math.pi / n) - 1))); print(n, round(tritri(n), 6), r)
print('n = 3: octahedron, r = 0 (tetrahedron):', abs(L(0) - (180 - tritri(3))) < 1e-9)
print('worst |r - (2cos(pi/n) - 1)| for n = 4..12:', worst)
