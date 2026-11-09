"""Natural cap for the spherical yantra (DICTO 11-08: 'leaning towards Cleos'): choose the cap so the upper great triangle t7 is as
near as possible a face of the spherical icosahedron (the Cleo-Icos seen from its centre: equilateral, angles 72, sides 63.4349).
Yantra: the perfect one (viewpoint.json V1). For cap angular radius RHO, compute t7's spherical angles and sides; show that no cap gives tip angle 72 (the root search of 8 Nov had no sign change)."""
import json, math
import numpy as np
from scipy.optimize import brentq
V = json.load(open('viewpoint.json'))['V1']; f = lambda d: {int(k): float(v['a']) for k, v in d.items()}
b, w, a = f(V['b']), f(V['w']), f(V['apex'])
def tri(i, rho):
    sc = math.tan(rho) / 0.5
    P = lambda x, d: (lambda q: q / np.linalg.norm(q))(np.array([x * sc, (0.5 - d) * sc, 1.0]))
    return P(-w[i], b[i]), P(w[i], b[i]), P(0, a[i])
def ang(A, B, C):          # spherical angle at A between arcs AB and AC
    n1 = np.cross(A, B); n2 = np.cross(A, C)
    return math.degrees(math.acos(np.clip(np.dot(n1, n2) / np.linalg.norm(n1) / np.linalg.norm(n2), -1, 1)))
def side(A, B): return math.degrees(math.acos(np.clip(np.dot(A, B), -1, 1)))
def report(rho, i=7):
    L, R, A = tri(i, rho); return ang(A, L, R), ang(L, A, R), side(A, L), side(L, R)
ICO_SIDE = math.degrees(math.atan(2))          # 63.4349 deg: arc between adjacent icosahedron vertices
# Finding (paper #103 sec. 11): no cap works. Scan cap radii 0.01..89 deg: the tip angle starts above 72 (flat limit = flat tip angle)
# and only grows, and tip minus base angle keeps one sign, so t7 is never an exact spherical icosahedron face.
flat_tip = math.degrees(2 * math.atan(w[7] / (a[7] - b[7]) if a[7] > b[7] else w[7] / (b[7] - a[7])))
rows = [(r,) + report(math.radians(r)) for r in np.linspace(0.01, 89, 8901)]
tips = [t for _, t, *_ in rows]; diffs = [t - bs for _, t, bs, *_ in rows]
print(f'flat tip angle of t7 {flat_tip:.4f} deg; over caps 0.01..89 deg: tip angle from {min(tips):.4f} to {max(tips):.4f}')
print(f'tip minus base angle from {min(diffs):.4f} to {max(diffs):.4f} (one sign: never equal)')
mono = all(t2 >= t1 - 1e-12 for t1, t2 in zip(tips, tips[1:]))
ok = min(tips) > 72 and mono and (min(diffs) > 0 or max(diffs) < 0) and abs(min(tips) - flat_tip) < 1e-2
json.dump({'flat_tip_deg': flat_tip, 'tip_min': min(tips), 'tip_max': max(tips), 'monotone': mono}, open('cleo-cap.json', 'w'))
print('FINAL ok: no cap makes t7 an icosahedron face' if ok else 'FINAL FAIL: scan does not support the claim')
