"""Natural cap for the spherical yantra (DICTO 11-08: 'leaning towards Cleos'): choose the cap so the upper great triangle t7 is as
near as possible a face of the spherical icosahedron (the Cleo-Icos seen from its centre: equilateral, angles 72, sides 63.4349).
Yantra: the perfect one (viewpoint.json V1). For cap angular radius RHO, compute t7's spherical angles and sides; solve tip angle = 72."""
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
rho = brentq(lambda r: report(r)[0] - 72, math.radians(5), math.radians(89))
tip, base, s1, s2 = report(rho)
print(f'cap angular radius {math.degrees(rho):.6f} deg: t7 tip angle {tip:.6f}, base angles {base:.6f}, sides {s1:.6f} and base {s2:.6f}  (icosahedron face: 72, 72, {ICO_SIDE:.4f})')
L3, R3, A3 = tri(3, rho); print(f'  lower great triangle t3 there: tip {ang(A3, L3, R3):.4f}, base angles {ang(L3, A3, R3):.4f}, sides {side(A3, L3):.4f}, base {side(L3, R3):.4f}')
json.dump({'rho_deg': math.degrees(rho)}, open('cleo-cap.json', 'w'))
print('FINAL ok' if abs(tip - 72) < 1e-9 else 'FINAL FAIL: tip angle not 72')
