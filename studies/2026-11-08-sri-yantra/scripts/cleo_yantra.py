"""The stella yantra (DICTO 11-08: the tetrahedral Sri Yantra spun from the regular stella octangula). Spinning the regular
stella octangula about its 3-fold axis gives two cones whose axial section is a yantra great pair with slopes u = v = 1/sqrt2
(regular tetrahedron in a sphere: base depth 2/3 of the diameter, base circumradius sqrt2/3). Here the yantra on that frame:
u = v = 1/sqrt2 plus the classical conditions (b) t1 and (c) t9 base corners on the circle (Kulaichev's (b), (c)); unknowns Q, S.
Solved to 60 digits; checks every Huet condition, validity, and compares with Huet's classical and Kulaichev's yantras."""
import mpmath as mp
from model import solve, all_conditions, order_ok
mp.mp.dps = 80
u = 2 / ((1 + mp.sqrt(5)) / 2) ** 2   # Cleo-Icos, the icosahedron face pyramid: cone slope 2/phi^2
def yantra(Q, S):
    P = u**2 / (1 + u**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, u / (1 + u**2), u / (1 + u**2), mp.sqrt, root=1)
def eqs(Q, S):
    t = yantra(Q, S); b, w = t['b'], t['w']
    return [w[1]**2 + b[1]**2 - b[1], w[9]**2 + b[9]**2 - b[9]]
best = None
for Q0 in [mp.mpf(x) / 100 for x in range(45, 62, 2)]:
    for S0 in [mp.mpf(x) / 100 for x in range(78, 92, 2)]:
        try:
            Q, S = mp.findroot(eqs, (Q0, S0), tol=mp.mpf(10)**-70)
            t = yantra(Q, S)
            if order_ok(t, mp.mpf(10)**-40): best = (Q, S, t); break
        except Exception: pass
    if best: break
if not best:
    print('no valid stella yantra with t1, t9 corners on the circle near the classical one'); print('FINAL FAIL: none found'); raise SystemExit
Q, S, t = best
print('Cleo yantra u = v = 2/phi^2: Q =', mp.nstr(Q, 40), ' S =', mp.nstr(S, 40))
for i in range(1, 10): print(f'  b{i} = {mp.nstr(t["b"][i], 25)}  w{i} = {mp.nstr(t["w"][i], 25)}')
huet = [mp.mpf(x) for x in ('0.332', '0.537', '0.602', '0.835')]
P = u**2 / (1 + u**2); R = 1 / (1 + u**2)
print('P, Q, R, S =', [mp.nstr(x, 6) for x in (P, Q, R, S)], ' Huet classical:', [str(x) for x in huet])
print('rhombus: diagonal ratio', mp.nstr(u, 8), '(Huet 0.755, Kulaichev 0.7504)')
res = max(abs(x) for x in eqs(Q, S)); cond = max(abs(v) for n, v in all_conditions(t))
ok = res < mp.mpf(10)**-60 and cond < mp.mpf(10)**-60 and order_ok(t, mp.mpf(10)**-40)
print('residuals', mp.nstr(res, 3), mp.nstr(cond, 3), 'valid:', order_ok(t, mp.mpf(10)**-40))
print('FINAL ok' if ok else 'FINAL FAIL stella yantra')
