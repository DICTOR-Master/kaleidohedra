"""DICTO 11-08: 'would viewpoint have helped the circle missing on the most artistic one?' A viewpoint keeps inside as inside, so it
cannot bring E1's corners onto the circle. Instead: the most even exact yantra WITH t1 and t9 corners on the circle (penalty), to see
what evenness the circle costs. Compare E1 (0.614, corners inside) and the DICTO Yantra (0.866)."""
import math, numpy as np
from scipy.optimize import minimize
from even_yantra import yantra, score
def off(x):
    t = yantra(x)
    if t is None: return 1.0, 1.0
    b, w = t['b'], t['w']
    return math.hypot(w[1], b[1] - .5) - .5, math.hypot(w[9], b[9] - .5) - .5
def f(x):
    r1, r9 = off(x); return score(x) + 200 * (r1 * r1 + r9 * r9) ** .5
best = None
for x0 in [(0.679318588706775, 0.695014037372934, 0.576510321708, 0.968268607459), (0.7777407207, 0.7434588452, 0.5415589952, 0.8719616408)]:
    r = minimize(f, x0, method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 4000})
    if best is None or r.fun < best.fun: best = r
r1, r9 = off(best.x); sc = score(best.x)
print('ON-CIRCLE MOST EVEN: u,v,Q,S =', [round(v, 10) for v in best.x], ' spread/mean =', round(sc, 4), ' corners off:', f'{r1:.1e} {r9:.1e}')
print('FINAL ok' if abs(r1) < 1e-6 and abs(r9) < 1e-6 and sc < 5 else 'FINAL FAIL: no 43-piece yantra with both corners on the circle found')
