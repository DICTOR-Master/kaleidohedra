# Six equal hexagonal wheels (DICTO, 2026-10-14: "six wheels all the same size", built with DeltaZips long ago). Model: six regular
# hexagonal wheels of circumradius 1 centred together, in the six planes square to the icosahedron's five-fold axes (where six
# equal great circles cross most evenly). Two wheels meet along the line where their planes cross; with flat rigid wheels each rim
# reaches that line at its own distance (between the hexagon's apothem 0.866 and its corner 1). Each wheel may turn in its plane;
# we find the turns that make the wheels meet as nearly as possible, i.e. the smallest bending a flexible ring needs.
# DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
N = [v / np.linalg.norm(v) for v in ico if v @ np.array([1e-3, 2e-3, 3e-3]) > 0]
def frame(n):
    a = np.cross(n, [0.3, 0.5, 0.8]); a /= np.linalg.norm(a); return a, np.cross(n, a)
F = [frame(n) for n in N]
def rim_distance(phi_angle):      # distance from centre to a regular hexagon (circumradius 1) along direction at angle phi
    x = (phi_angle % (math.pi / 3)) - math.pi / 6; return (math.sqrt(3) / 2) / math.cos(x)
pairs = list(itertools.combinations(range(6), 2))
lines = {}
for i, j in pairs:
    d = np.cross(N[i], N[j]); lines[(i, j)] = d / np.linalg.norm(d)
def mismatch(th):
    err = []
    for (i, j), d in lines.items():
        di = rim_distance(math.atan2(d @ F[i][1], d @ F[i][0]) - th[i]); dj = rim_distance(math.atan2(d @ F[j][1], d @ F[j][0]) - th[j]); err.append(di - dj)
    return np.array(err)
best = None
rng = np.random.default_rng(5)
for _ in range(400):
    x0 = rng.uniform(0, math.pi / 3, 6)
    r = minimize(lambda t: (mismatch(t) ** 2).sum(), x0, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-14, maxiter=20000))
    if best is None or r.fun < best.fun: best = r
e = mismatch(best.x)
out = dict(turns_deg=[round(math.degrees(t) % 60, 4) for t in best.x], worst_gap=float(abs(e).max()), rms_gap=float(math.sqrt((e ** 2).mean())),
           note='gaps are differences in rim distance (circumradius 1) where two wheels cross; a flexible ring closes them by bending')
# compare: the four-wheel cuboctahedron (zero gap) and six circles (zero gap)
json.dump(out, open(os.path.join(ROOT, 'six-wheels.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
