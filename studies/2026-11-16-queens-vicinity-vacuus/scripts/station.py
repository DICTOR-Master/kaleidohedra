#!/usr/bin/env python3
"""The cross-wall station of the truncated-600-cell hop (found by study1.py part stations): seed lambda3:lambda4 = 1/phi.
Exact description: where its corners sit on the 600-cell's edges, its two edge lengths, faces per wall, and its place on
the Hopscotch line (mu) against the stations already known there (pds-hopscotch-line: 19-design mu* = 0.924138673,
canonical-form silence mu_Omega = 0.921449634, turn fixed point r = phi^2/(2 sqrt2) = 0.925615). FINAL ok on its checks."""
import itertools
from qv_lib import *   # noqa: F401,F403
import study1 as S1

checks = []
lam = (ZERO, ZERO, IPHI, ONE)
x0 = tuple(sum((l * OMEGA[i][k] for i, l in enumerate(lam)), ZERO) for k in range(4))
V = orbit(x0)
checks.append(len(V) == 1440)
# corners on the 600-cell's edges: scale so that the corner lies on the 600-cell's boundary between two adjacent corners
# p (the 600-cell corner along omega_4) and q (its neighbour across alpha_4): x0 = s((1-t) p + t q)
w4 = OMEGA[3]
p = next(v for v in V600 if dot(v, w4).sign() > 0 and dot(v, w4) * dot(v, w4) == dot(v, v) * dot(w4, w4))
q = reflect(p, ALPHA[3])
# solve x0 = a p + b q exactly (x0 lies in span(p, q): check) ; t = b / (a + b)
a_, b_ = None, None
M = [[p[i], q[i]] for i in range(4)]
# least-squares-free exact solve from two independent coordinates
for i, j in itertools.combinations(range(4), 2):
    det = M[i][0] * M[j][1] - M[i][1] * M[j][0]
    if not det.iszero():
        a_ = (x0[i] * M[j][1] - M[i][1] * x0[j]) / det
        b_ = (M[i][0] * x0[j] - x0[i] * M[j][0]) / det
        break
checks.append(all((a_ * p[k] + b_ * q[k] - x0[k]).iszero() for k in range(4)))
t = b_ / (a_ + b_)
print('corner on the 600-cell edge pq at fraction t =', q5str(t), '=', float(t), '(uniform truncation: 1/3; rectification: 1/2)')
# edge lengths
Vf = np.array([fl(v) for v in V])
d2 = sorted({round(float(dot(sub(V[0], v), sub(V[0], v))), 9) for v in V[1:]})[:3]
e = [x for x in d2][:2]
print('two shortest distances from a corner (edge lengths squared, float):', e, 'ratio of lengths', (e[1] / e[0]) ** .5)
r = vacuus4(V, 'station truncated 600-cell')
print(r)
checks.append(r['plates'] == 360 and r['plates_mirror'] == 60 and r['plates_cross'] == 300 and r['plates_none'] == 0)
print('triangles per cross wall:', r['ridges_cross'] / r['plates_cross'], '; hexagons per mirror wall:', r['ridges_mirror'] / r['plates_mirror'])
mu = S1.mu_of(x0)
print('mu =', q5str(mu), '=', float(mu), '; mu* (19-design) 0.924138673, mu_Omega 0.921449634, turn r 0.925615: all differ')
checks.append(mu == Q5(Fr(1, 2), Fr(1, 5)))
print('checks', checks)
print('FINAL ok' if all(checks) else 'FINAL FAIL')
