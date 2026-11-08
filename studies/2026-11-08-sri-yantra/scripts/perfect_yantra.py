"""Perfect yantras (DICTO 11-08: can we split them to get perfection?): all three of (b) t1 corners on the circle, (c) t9 corners on
the circle, (d) centred bindu (so the gnomon nesting is exact), with ONE great triangle exactly a solid of the Cleo-Octangula and the
other slope free: (1) u = 2/phi^2 (Cleo-Icos above) exact, v free; (2) v = 1/sqrt2 (stella below) exact, u free. Unknowns: the free
slope, Q, S. Writes perfect.json for the counts."""
import mpmath as mp, json
from model import solve, all_conditions, order_ok
mp.mp.dps = 60
phi = (1 + mp.sqrt(5)) / 2; CLEO = 2 / phi**2; STELLA = 1 / mp.sqrt(2)
def yan(u, v, Q, S):
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root=1)
def inc(t, Q):
    b, w = t['b'], t['w']; m1 = w[1] / (Q - b[1]); h = abs(Q - b[5]); hw = m1 * h; r = hw * h / (hw + mp.sqrt(hw**2 + h**2))
    return b[5] + (r if Q > b[5] else -r), r
def F(u, v, Q, S):
    t = yan(u, v, Q, S); b, w = t['b'], t['w']
    return [w[1]**2 + b[1]**2 - b[1], w[9]**2 + b[9]**2 - b[9], inc(t, Q)[0] - mp.mpf(1) / 2]
out = {}
for label, fix in (('Cleo-Icos above exact, lower slope free', 'u'), ('stella below exact, upper slope free', 'v')):
    sol = None
    for x0 in [mp.mpf(x) / 100 for x in range(66, 86, 2)]:
        for Q0 in [mp.mpf(x) / 100 for x in range(50, 60, 2)]:
            for S0 in [mp.mpf(x) / 100 for x in range(86, 96, 2)]:
                try:
                    if fix == 'u': g = lambda x, Q, S: F(CLEO, x, Q, S)
                    else: g = lambda x, Q, S: F(x, STELLA, Q, S)
                    x, Q, S = mp.findroot(g, (x0, Q0, S0), tol=mp.mpf(10)**-50)
                    u, v = (CLEO, x) if fix == 'u' else (x, STELLA)
                    t = yan(u, v, Q, S)
                    if 0.5 < x < 1.2 and order_ok(t, mp.mpf(10)**-30) and max(abs(e) for n, e in all_conditions(t)) < mp.mpf(10)**-40: sol = (u, v, Q, S, t); break
                except Exception: pass
            if sol: break
        if sol: break
    if not sol: print(label, ': no valid yantra', flush=True); continue
    u, v, Q, S, t = sol; c, r = inc(t, Q); k = 2 * r
    b, w = t['b'], t['w']; a = {3: mp.mpf(1), 7: mp.mpf(0), 8: b[1], 6: b[2], 9: b[3], 1: b[6], 5: b[7], 4: b[8], 2: b[9]}
    s = lambda x: {'a': mp.nstr(x, 40)}; name = 'PF' + str(len(out) + 1)
    out[name] = {'label': label, 'u': mp.nstr(u, 30), 'v': mp.nstr(v, 30), 'k': mp.nstr(k, 30), 'b': {str(i): s(b[i]) for i in range(1, 10)}, 'w': {str(i): s(w[i]) for i in range(1, 10)}, 'apex': {str(i): s(a[i]) for i in range(1, 10)}}
    print(f'{name} {label}: u = {mp.nstr(u, 12)} (Cleo 0.763932), v = {mp.nstr(v, 12)} (stella 0.707107), Q = {mp.nstr(Q, 10)}, S = {mp.nstr(S, 10)}, nesting k = {mp.nstr(k, 10)}', flush=True)
json.dump(out, open('perfect.json', 'w'), indent=1)
print('FINAL ok' if out else 'FINAL FAIL: no perfect yantra with one exact solid')
