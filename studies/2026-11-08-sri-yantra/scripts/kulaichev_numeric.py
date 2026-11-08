"""Kulaichev-Rao-Pustynski yantra: Huet's conditions plus the four extra conditions
(a) t3 = t7 congruent (P = 1 - R), (b) t1 base corners on the circle, (c) t9 base corners on the circle,
(d) incircle of the innermost triangle (legs of t1, base of t5) concentric with the circle.
Solved to 60 digits with mpmath; checked against Pustynski 2014, Table 1 (15 figures)."""
import mpmath as mp
from model import solve, all_conditions, order_ok
mp.mp.dps = 80


def yantra(u, Q, S):
    v = u                                  # (a): slopes of t3 and t7 legs equal -> P = 1 - R
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root=1)


def eqs(u, Q, S):
    t = yantra(u, Q, S); b, w, a = t['b'], t['w'], t['a']
    m1 = w[1] / (Q - b[1])
    return [w[1]**2 + b[1]**2 - b[1],                                   # (b)
            w[9]**2 + b[9]**2 - b[9],                                   # (c)
            m1**2 * (Q - mp.mpf(1)/2)**2 - (mp.mpf(1)/2 - b[5])**2 * (1 + m1**2)]   # (d)


# start from Pustynski's Table 1 (unit circle, y up) converted to depth d = (1 - y)/2
Dy = mp.mpf('0.279461220861835'); Ay = mp.mpf('-0.101410465950899'); zy = mp.mpf('-0.840120291819195')
P0 = (1 - Dy) / 2; u0 = mp.sqrt(P0 / (1 - P0)); Q0 = (1 - Ay) / 2; S0 = (1 - zy) / 2
sol = mp.findroot(lambda u, Q, S: eqs(u, Q, S), (u0, Q0, S0), tol=mp.mpf(10)**-70)
u, Q, S = sol
t = yantra(u, Q, S)
pust = {1: '0.793459849383596', 2: '0.476362922107536', 3: '0.279461220861835', 4: '0.173533168477376',
        5: '0.057031219725571', 6: '-0.101410465950899', 7: '-0.279461220861835', 8: '-0.498053404254090',
        9: '-0.840120291819195'}
print('Kulaichev-Rao-Pustynski yantra, depth from top, diameter 1 (60 digits):')
dev = 0
for i in range(1, 10):
    y = 1 - 2 * t['b'][i]
    dev = max(dev, abs(y - mp.mpf(pust[i])))
    print(f' b{i} = {mp.nstr(t["b"][i], 60)}   w{i} = {mp.nstr(t["w"][i], 60)}   (unit-circle y = {mp.nstr(y, 18)}; Pustynski {pust[i]})')
print(' slope u = v =', mp.nstr(u, 60))
res = max(abs(x) for x in eqs(u, Q, S)); cond = max(abs(v) for n, v in all_conditions(t))
print(f'max residual extra conditions {mp.nstr(res, 5)}; max residual Huet conditions {mp.nstr(cond, 5)}')
print(f'max deviation from Pustynski Table 1 (unit-circle y): {mp.nstr(dev, 5)}; configuration valid: {order_ok(t, mp.mpf(10)**-60)}')
ok = res < mp.mpf(10)**-60 and cond < mp.mpf(10)**-60 and dev < mp.mpf(10)**-13
print('FINAL ok' if ok else 'FINAL FAIL kulaichev numeric')
