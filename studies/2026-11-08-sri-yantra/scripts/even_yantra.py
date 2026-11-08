"""The most even exact yantra (DICTO 11-08: 'that sounds like an answer'). Every yantra of the 4-parameter family (u, v, Q, S) has all
18 marmas exact and both great triangles inscribed (model.py). Among those with the traditional 43 pieces (14, 10, 10, 8, 1) find the
one whose 43 pieces are most nearly equal in area: minimise the coefficient of variation (spread / mean) of the 43 areas. Compare
with the DICTO Yantra (GF1), the Cleo-Octangula (K1), Huet's classical and R1. Nelder-Mead from several starts; the best is then
polished and its own corners-on-circle residuals reported."""
import json, math, sys
import numpy as np
from scipy.optimize import minimize
from model import solve, order_ok
import figure as FG
def yantra(x):
    u, v, Q, S = x
    if not (0.3 < u < 1.5 and 0.3 < v < 1.5 and 0 < Q < 1 and 0 < S < 1): return None
    P = v * v / (1 + v * v); R = 1 / (1 + u * u)
    try:
        t = solve(P, Q, R, S, v / (1 + v * v), u / (1 + u * u), lambda z: math.sqrt(z) if z >= 0 else float('nan'), root=1)
    except (ZeroDivisionError, ValueError): return None
    if any(math.isnan(t['b'][i]) or math.isnan(t['w'][i]) for i in range(1, 10)): return None
    if not order_ok(t, 1e-12): return None
    return t
def pieces(t):
    b = t['b']; w = t['w']; a = t['a']
    segs = FG.segments(b, w, a); pts, fs = FG.faces(segs); out = []
    for f in fs:
        poly = [pts[k] for k in f]; ar = FG.area(poly)
        if ar >= -1e-14: continue
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        cnt = sum(FG.inside_tri((cx, cy), b, w, a, i) for i in range(1, 10))
        if cnt % 2: out.append((abs(ar), cnt, len(FG.corners_of(poly))))
    return out
def score(x):
    t = yantra(x)
    if t is None: return 9.0
    try: P = pieces(t)
    except Exception: return 9.0
    rings = [sum(1 for p in P if p[1] == c) for c in (1, 3, 5, 7, 9)]
    if rings != [14, 10, 10, 8, 1] or any(p[2] != 3 for p in P): return 5.0 + abs(len(P) - 43) * 0.1
    A = np.array([p[0] for p in P]); return float(A.std() / A.mean())
def ref(path, key):
    e = json.load(open(path))[key]; return e
starts = {'DICTO Yantra (GF1)': (0.679318588706775, 0.695014037372934, 0.576510321708, 0.968268607459),
          'Huet classical': (math.sqrt((1 - 0.602) / 0.602), math.sqrt(0.332 / 0.668), 0.537, 0.835)}
for n, x in starts.items(): print(f'{n}: spread/mean of the 43 areas = {score(x):.4f}', flush=True)
best = None; rng = np.random.default_rng(3)
inits = list(starts.values()) + [tuple(np.array(starts['Huet classical']) + rng.normal(0, 0.03, 4)) for _ in range(10)]
for x0 in inits:
    r = minimize(score, x0, method='Nelder-Mead', options={'xatol': 1e-9, 'fatol': 1e-10, 'maxiter': 3000})
    if best is None or r.fun < best.fun: best = r
u, v, Q, S = best.x; t = yantra(best.x)
print(f'MOST EVEN: u = {u:.10f}, v = {v:.10f}, Q = {Q:.10f}, S = {S:.10f}; spread/mean = {best.fun:.5f}')
b, w = t['b'], t['w']
print('  t1 corners off the circle:', round(math.hypot(w[1], b[1] - 0.5) - 0.5, 5), ' t9:', round(math.hypot(w[9], b[9] - 0.5) - 0.5, 5))
P = pieces(t); A = sorted(p[0] for p in P); print(f'  smallest piece / largest piece = {A[0] / A[-1]:.4f}')
s = lambda z: {'a': repr(float(z))}
json.dump({'E1': {'u': u, 'v': v, 'b': {str(i): s(b[i]) for i in range(1, 10)}, 'w': {str(i): s(w[i]) for i in range(1, 10)}, 'apex': {str(i): s(t['a'][i]) for i in range(1, 10)}}}, open('even.json', 'w'), indent=1)
print('FINAL ok' if best.fun < score(starts['DICTO Yantra (GF1)']) and best.fun < 5 else 'FINAL FAIL: no more even 43-piece yantra found')
