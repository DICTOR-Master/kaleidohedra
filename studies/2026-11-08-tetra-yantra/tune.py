"""Tune the sphere of twenty yantras with harmonics (DICTO 11-08, option A). Points: the 18 marmas of each yantra (360 on the
sphere; cap = icosahedron face incircle). Settings: each yantra's turn psi_f about its face centre. Fingerprint: Steinhardt
Q_l = sqrt(4 pi/(2l+1) sum_m |q_lm|^2), q_lm = mean over points of Y_lm. Icosahedral patterns can only ring at l = 0, 6, 10, 12, ...;
tuning target: silence l in BAD = 1..5, 7, 8, 9, keep Q6, Q10. Compare: all yantras pointing at a face corner (untuned), random turns,
and the tuned turns (many starts, Nelder-Mead then Powell)."""
import json, math, itertools
import numpy as np
from scipy.optimize import minimize
try:
    from scipy.special import sph_harm_y as SH; Y = lambda l, m, th, ph: SH(l, m, th, ph)
except ImportError:
    from scipy.special import sph_harm as SH; Y = lambda l, m, th, ph: SH(m, l, ph, th)
V = json.load(open('viewpoint.json'))['V1']; f = lambda d: {int(k): float(v['a']) for k, v in d.items()}
b, w, a = f(V['b']), f(V['w']), f(V['apex'])
# the 18 marmas of the flat yantra (x, depth), from the triple points of its sides
segs = []
for i in range(1, 10):
    L, R, A = (-w[i], b[i]), (w[i], b[i]), (0.0, a[i]); segs += [(L, R), (L, A), (R, A)]
def inter(s, t):
    (x1, y1), (x2, y2) = s; (x3, y3), (x4, y4) = t; den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-14: return None
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den; py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    on = lambda p, q: min(p[0], q[0]) - 1e-9 <= px <= max(p[0], q[0]) + 1e-9 and min(p[1], q[1]) - 1e-9 <= py <= max(p[1], q[1]) + 1e-9
    return (round(px, 9), round(py, 9)) if on(*s) and on(*t) else None
cnt = {}
for s, t in itertools.combinations(segs, 2):
    q = inter(s, t)
    if q: cnt.setdefault(q, set()).update({segs.index(s), segs.index(t)})
corn = {(round(x, 9), round(y, 9)) for i in range(1, 10) for (x, y) in [(-w[i], b[i]), (w[i], b[i]), (0, a[i])]}
M = [q for q, s in cnt.items() if len(s) >= 3 and q not in corn]
assert len(M) == 18, len(M)
phi = (1 + 5 ** .5) / 2
I = [np.array(p, float) for c in [(0, 1, phi), (1, phi, 0), (phi, 0, 1)] for p in itertools.product(*[(x, -x) if x else (0,) for x in c])]
I = [v / np.linalg.norm(v) for v in I]; E = min(np.linalg.norm(I[i] - I[j]) for i, j in itertools.combinations(range(12), 2))
faces = [t for t in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(I[x] - I[y]) - E) < 1e-9 for x, y in itertools.combinations(t, 2))]
RHO = math.radians(20.905157447889)
sc = math.tan(RHO) / 0.5
FR = []
for t in faces:
    cen = sum(I[k] for k in t); cen /= np.linalg.norm(cen)
    up = I[t[0]] - np.dot(I[t[0]], cen) * cen; up /= np.linalg.norm(up); FR.append((cen, up, np.cross(up, cen)))
LOC = np.array([[x * sc, (0.5 - dd) * sc] for x, dd in M])
def points(psi):
    P = []
    for (cen, up, rt), ps in zip(FR, psi):
        c, s = math.cos(ps), math.sin(ps); u2 = c * up + s * rt; r2 = -s * up + c * rt
        Q = cen[None, :] + LOC[:, 0:1] * r2[None, :] + LOC[:, 1:2] * u2[None, :]
        P.append(Q / np.linalg.norm(Q, axis=1)[:, None])
    return np.vstack(P)
def Ql(P, l):
    th = np.arccos(np.clip(P[:, 2], -1, 1)); ph = np.arctan2(P[:, 1], P[:, 0])
    return math.sqrt(4 * math.pi / (2 * l + 1) * sum(abs(np.mean(Y(l, m, th, ph)))**2 for m in range(-l, l + 1)))
BAD = [1, 2, 3, 4, 5, 7, 8, 9]; SHOW = list(range(1, 13))
cost = lambda psi: sum(Ql(points(psi), l)**2 for l in BAD)
def fp(psi): P = points(psi); return {l: Ql(P, l) for l in SHOW}
rng = np.random.default_rng(7)
res = {'pointing at a corner (untuned)': np.zeros(20), 'random turns': rng.uniform(0, 2 * math.pi, 20)}
best = None
for k in range(12):
    x0 = rng.uniform(0, 2 * math.pi, 20)
    r = minimize(cost, x0, method='Powell', options={'maxiter': 4000, 'xtol': 1e-6, 'ftol': 1e-12})
    if best is None or r.fun < best.fun: best = r
res['tuned'] = best.x
print('l:      ' + ' '.join(f'{l:>7d}' for l in SHOW))
for name, psi in res.items():
    q = fp(psi); print(f'{name[:30]:30s} ' + ' '.join(f'{q[l]:7.4f}' for l in SHOW))
print('silence (sum of Q_l^2 over l = 1..5, 7, 8, 9):', {n: f'{cost(p):.3e}' for n, p in res.items()})
json.dump({'turns_deg': [float(math.degrees(x) % 360) for x in best.x], 'cost': float(best.fun)}, open('tuned-turns.json', 'w'), indent=1)
print('FINAL ok' if best.fun < cost(res['pointing at a corner (untuned)']) else 'FINAL FAIL: tuning did not improve')
