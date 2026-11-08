"""DICTO's rhombus (DICTO proposed, 8 Nov 2026: "seems to be a big upright rhombus in the construction").
The two legs of t7 (apex O = top of the circle) and the two legs of t3 (apex T = bottom) are the four
longest lines of the yantra.  Extended to meet, they bound the quadrilateral O, E+, T, E- with
   E+- = (+- u v/(u+v), v/(u+v))     (u = slope of the t7 legs, v = slope of the t3 legs, |dx/dd|).
Sides: |OE| = v sqrt(1+u^2)/(u+v), |TE| = u sqrt(1+v^2)/(u+v).  It is a kite in general and a
RHOMBUS exactly when u = v, i.e. when t3 and t7 are congruent (Kulaichev's extra condition (a));
then E+- = (+-u/2, 1/2), diagonals 1 (vertical) and u (horizontal), angle at O and T = 2 atan u.
Part 1: the kite/rhombus in the classical and exact yantras.
Part 2: special rhombi u = v = k as an extra condition, completed by t1 and t9 base corners on the circle
        (Kulaichev's (b), (c)); solved to 50 digits, admissibility and Kulaichev's (d) residual reported."""
import mpmath as mp
from fractions import Fraction as Fr
from model import solve, order_ok, all_conditions
mp.mp.dps = 60


def kite(u, v):
    u, v = mp.mpf(u), mp.mpf(v)
    ex, ed = u * v / (u + v), v / (u + v)
    angO = 2 * mp.degrees(mp.atan(u)); angT = 2 * mp.degrees(mp.atan(v))
    angE = (360 - angO - angT) / 2
    return dict(E=(ex, ed), angO=angO, angT=angT, angE=angE, ratio=2 * ex / 1,
                sideO=ed * mp.sqrt(1 + u**2), sideT=(1 - ed) * mp.sqrt(1 + v**2))


def yantra(u, v, Q, S):
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    for root in (1, 0):
        t = solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root)
        if order_ok(t, mp.mpf(10)**-40): return t
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, 1)


def extra(t):
    b, w, Q = t['b'], t['w'], t['b'][6]
    m1 = w[1] / (Q - b[1])
    cb = w[1]**2 + b[1]**2 - b[1]; cc = w[9]**2 + b[9]**2 - b[9]
    # (d): incircle of the innermost triangle (legs of t1, base of t5): its centre depth minus 1/2
    sn = m1 / mp.sqrt(1 + m1**2)                      # sin of the half apex angle of t1
    r = (Q - b[5]) * sn / (1 + sn); centre = b[5] + r
    return cb, cc, centre - mp.mpf(1) / 2


def sv(P): return mp.sqrt(P / (1 - P))   # slope of t3 legs from its base depth P
def su(R): return mp.sqrt((1 - R) / R)   # slope of t7 legs from its base depth R


CASES = [
    ('Huet classical (Chiodo eq.)', su(mp.mpf('0.602')), sv(mp.mpf('0.332'))),
    ('Kaivalyasrama 48-grid', su(mp.mpf(30) / 48), sv(mp.mpf(17) / 48)),
    ('Kavi Mahesh 2023', su(mp.mpf(3) / 5), sv(mp.mpf(1) / 3)),
    ('Kulaichev-Rao-Pustynski', mp.mpf('0.750438516022214024406084657051234510340891003639790315415314'),
     mp.mpf('0.750438516022214024406084657051234510340891003639790315415314')),
    ('R1 rational (this study)', mp.mpf(19) / 24, mp.mpf(2) / 3),
    ('Q1 quadratic (this study)', mp.mpf(13) / 16, mp.mpf(12) / 17),
    ('Q2 quadratic (this study)', mp.mpf(4) / 5, mp.mpf(7) / 10),
]

if __name__ == '__main__':
    print('Part 1. DICTO\'s rhombus (kite O-E-T-E) in known yantras  [angles in degrees; ratio = horizontal/vertical diagonal]')
    for name, u, v in CASES:
        k = kite(u, v)
        print(f'  {name:30s} u={mp.nstr(u, 8):>11s} v={mp.nstr(v, 8):>11s}  angle O {mp.nstr(k["angO"], 7):>9s}  T {mp.nstr(k["angT"], 7):>9s}'
              f'  E {mp.nstr(k["angE"], 7):>9s}  diag ratio {mp.nstr(k["ratio"], 7):>9s}  sides |OE|/|TE| = {mp.nstr(k["sideO"] / k["sideT"], 7)}'
              + ('  RHOMBUS' if u == v else '  kite'))
    phi = (1 + mp.sqrt(5)) / 2
    SPECIAL = [('golden rhombus, diagonals 1 : phi', 1 / phi), ('60/120 rhombus (60 deg at O and T)', 1 / mp.sqrt(3)),
               ('3-4-5 rhombus, diagonals 3 : 4', mp.mpf(3) / 4), ('square', mp.mpf(1))]
    print('\nPart 2. Special rhombus u = v = k, completed by t1 and t9 base corners on the circle:')
    ok_any = False; res345 = None
    for name, k in SPECIAL:
        P = k**2 / (1 + k**2); R = 1 / (1 + k**2)
        if not P < R:
            print(f'  {name}: k = {mp.nstr(k, 10)}, P = R = {mp.nstr(P, 5)}: the bases of t3 and t7 coincide, no yantra'); continue
        try:
            Q, S = mp.findroot(lambda Q, S: extra(yantra(k, k, Q, S))[:2], (mp.mpf('0.55'), mp.mpf('0.92')), tol=mp.mpf(10)**-50)
            t = yantra(k, k, Q, S); adm = order_ok(t, mp.mpf(10)**-40)
            cb, cc, dd = extra(t); huet = max(abs(c) for _, c in all_conditions(t))
            print(f'  {name}: k = {mp.nstr(k, 12)}  Q = {mp.nstr(Q, 20)}  S = {mp.nstr(S, 20)}  admissible: {adm}  '
                  f'Huet residual {mp.nstr(huet, 3)}; (d) incircle centre offset {mp.nstr(dd, 6)}')
            print('      depths x48:', ' '.join(mp.nstr(48 * t['b'][i], 5) for i in range(1, 10)))
            if adm and huet < mp.mpf(10)**-45: ok_any = True
            if k == mp.mpf(3) / 4: res345 = (Q, S, t)
        except Exception as e:
            print(f'  {name}: k = {mp.nstr(k, 10)}: no admissible solution near the classical one ({type(e).__name__})')
    if res345:
        Q, S, t = res345
        print('\n3-4-5 rhombus yantra (50 digits): Q =', mp.nstr(Q, 50), ' S =', mp.nstr(S, 50), ' b1 =', mp.nstr(t['b'][1], 50))
        import json
        d = lambda z: {'a': mp.nstr(z, 50, min_fixed=-5, max_fixed=5), 'b': '0'}
        json.dump({'Rh345': {'u': '3/4', 'v': '3/4', 'Q': mp.nstr(Q, 30), 'S': mp.nstr(S, 30),
                             'note': '3-4-5 rhombus yantra; exact field of degree 20 (rhombus345_exact.py); 50-digit values',
                             'b': {i: d(t['b'][i]) for i in range(1, 10)}, 'w': {i: d(t['w'][i]) for i in range(1, 10)},
                             'apex': {i: d(t['a'][i]) for i in range(1, 10)}}},
                  open('../data/rhombus345-coordinates.json', 'w'), indent=1)
    print('FINAL ok' if ok_any and res345 else 'FINAL FAIL no admissible special-rhombus yantra')
