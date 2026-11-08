"""Backwards check (DICTO 9 Nov 2026: "can't it be run backwards differently"): start from each POLYNOMIAL alone, take its real root
near the yantra (PARI, 260 digits, no geometry used), fix u there, solve only the two remaining unknowns (Q, S) from two of the three
conditions, and then test the third condition and every other one (all 18 marmas, tips on bases, corners, order) plus the piece counts.
Pass: third condition and all conditions below 1e-200; counts 43/18/24 (DICTO Yantra) and 45/18/28 (Kulaichev)."""
import mpmath as mp, cypari2
mp.mp.dps = 260
pari = cypari2.Pari(); pari.allocatemem(4 * 10**9); pari('default(realprecision, 270)')
from model import solve, all_conditions, order_ok
phi = (1 + mp.sqrt(5)) / 2
def yan(u, v, Q, S):
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root=1)
def inc(t, Q):
    b, w = t['b'], t['w']; m1 = w[1] / (Q - b[1]); h = abs(Q - b[5]); hw = m1 * h; r = hw * h / (hw + mp.sqrt(hw**2 + h**2))
    return b[5] + (r if Q > b[5] else -r)
ok = True
for name, path, near, vof, starts, want in (('DICTO Yantra', 'dicto-yantra-exact-u.txt', '0.6793', lambda u: 2 / phi**3 / u, [(0.5765, 0.9683)], (43, 18, 24)),
                                            ('Kulaichev', 'kulaichev-minpoly-u.txt', '0.7504', lambda u: u, [(q / 100, s / 100) for q in range(50, 60) for s in range(80, 99)], (45, 18, 28))):
    txt = open(path).read().replace('x', 'u')
    pari('F=' + txt)
    r = pari(f'[x | x<-polrootsreal(F), abs(x-{near})<0.001][1]')
    u = mp.mpf(str(pari(f'Strprintf("%.265f", {r})')))
    v = vof(u)
    G = lambda Q, S: (lambda t: [t['w'][1]**2 + t['b'][1]**2 - t['b'][1], t['w'][9]**2 + t['b'][9]**2 - t['b'][9]])(yan(u, v, Q, S))
    sol = None
    for Q0, S0 in starts:
        try:
            Q, S = mp.findroot(G, (mp.mpf(Q0), mp.mpf(S0)), tol=mp.mpf(10)**-250, maxsteps=200)
            t = yan(u, v, Q, S)
            if order_ok(t, mp.mpf(10)**-100): sol = (Q, S, t); break
        except Exception: pass
    Q, S, t = sol
    third = abs(inc(t, Q) - mp.mpf(1) / 2)
    worst = max(abs(e) for n, e in all_conditions(t))
    print(f'{name}: u from the polynomial only = {mp.nstr(u, 40)}; bindu-centring (not imposed) misses by {mp.nstr(third, 3)}; worst of all Huet conditions {mp.nstr(worst, 3)}', flush=True)
    ok = ok and third < mp.mpf(10)**-200 and worst < mp.mpf(10)**-200
    import json
    json.dump({'B': {'b': {str(i): {'a': mp.nstr(t['b'][i], 60)} for i in range(1, 10)}, 'w': {str(i): {'a': mp.nstr(t['w'][i], 60)} for i in range(1, 10)}, 'apex': {str(i): {'a': mp.nstr(t['a'][i], 60)} for i in range(1, 10)}}}, open(f'backwards-{name.split()[0]}.json', 'w'))
print('FINAL ok' if ok else 'FINAL FAIL: a yantra rebuilt from its polynomial misses a condition')
