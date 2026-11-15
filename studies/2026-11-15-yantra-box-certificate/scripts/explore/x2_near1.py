"""Exploration: on the G = 0 branch (t9 corner on the circle, S > R), which admissibility inequalities fail as u -> 1, for all t?"""
import math, sys
sys.path.insert(0, '.')
from x1_admregion import construct
def Sbranch(u):
    s = (-(1 - u**4) + math.sqrt((1 - u**4)**2 + 4 * u**8)) / (2 * u**3); return 1 / (1 + s * s)
def ineqs(u, t, S):
    b, w, a = construct(u, t, S); out = {}
    for i in range(1, 9): out[f'b{i+1}-b{i}'] = b[i+1] - b[i]
    for i in range(1, 10): out[f'w{i}'] = w[i]
    for i in range(1, 10): out[f'apex{i}'] = (a[i] - b[i]) if i <= 5 else (b[i] - a[i])
    for i in (2, 4, 5, 6, 8): out[f'disc{i}'] = -(w[i]**2 + b[i]**2 - b[i])
    out['1/2-b5'] = 0.5 - b[5]; out['Q-1/2'] = b[6] - 0.5
    return out
for u in (0.9, 0.94, 0.95, 0.96, 0.98, 0.99, 0.999):
    S = Sbranch(u); R = 1/(1+u*u)
    worst = {}
    nt = 400
    for k in range(1, nt):
        t = u * k / nt
        try: q = ineqs(u, t, S)
        except ZeroDivisionError: continue
        fails = [n for n, v in q.items() if v <= 0]
        for n in fails: worst[n] = worst.get(n, 0) + 1
    always = [n for n, c in worst.items() if c == nt - 1]
    print(f'u={u}: S-R={S-R:.4g}; inequalities failing for ALL t: {always}; some t: {sorted(set(worst)-set(always))}')
