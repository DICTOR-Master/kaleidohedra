"""The Cleo-Antonius yantra (DICTO 11-08: 'a side of Antonius instead of stella'). Antonius (D65, the golden antiprism; Cleo + Antonius
+ Cleo = the golden rhombohedron) has side faces congruent to the Cleo-Icos's: legs 0.851, base 0.894, apex half-angle atan(1/phi),
slope 1/phi. Pair: Cleo-Icos cone slope 2/phi^2 above, Antonius side slope 1/phi below; product p = 2/phi^3 (viewpoint-invariant).
Perfect member of that family: u v = p, both small triangles on the circle, bindu centred. Also the perfect members for the stella pair
(p = (2/phi^2)/sqrt2) for comparison. Counts are checked after (counts.py)."""
import mpmath as mp, json
from model import solve, all_conditions, order_ok
mp.mp.dps = 60
phi = (1 + mp.sqrt(5)) / 2
def yan(u, v, Q, S):
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root=1)
def inc(t, Q):
    b, w = t['b'], t['w']; m1 = w[1] / (Q - b[1]); h = abs(Q - b[5]); hw = m1 * h; r = hw * h / (hw + mp.sqrt(hw**2 + h**2))
    return b[5] + (r if Q > b[5] else -r)
out = {}
for name, p, u0 in (('Cleo-Antonius (p = 2/phi^3)', 2 / phi**3, 0.69), ('Cleo-Octangula (p = 2/(phi^2 sqrt2))', 2 / phi**2 / mp.sqrt(2), 0.73)):
    def F(u, Q, S):
        v = p / u; t = yan(u, v, Q, S); b, w = t['b'], t['w']
        return [w[1]**2 + b[1]**2 - b[1], w[9]**2 + b[9]**2 - b[9], inc(t, Q) - mp.mpf(1) / 2]
    sol = None
    for du in [x / 100 for x in range(-15, 16, 3)]:
        for Q0 in (0.52, 0.55, 0.58):
            for S0 in (0.88, 0.92, 0.96):
                try:
                    u, Q, S = mp.findroot(F, (u0 + du, Q0, S0), tol=mp.mpf(10)**-50)
                    if isinstance(u, mp.mpc) or u.imag if hasattr(u, 'imag') and u.imag else False: continue
                    t = yan(u, p / u, Q, S)
                    if order_ok(t, mp.mpf(10)**-30) and max(abs(e) for n, e in all_conditions(t)) < mp.mpf(10)**-40: sol = (u, Q, S, t); break
                except Exception: pass
            if sol: break
        if sol: break
    if not sol: print(name, ': no perfect yantra found'); continue
    u, Q, S, t = sol; b, w = t['b'], t['w']; a = {3: mp.mpf(1), 7: mp.mpf(0), 8: b[1], 6: b[2], 9: b[3], 1: b[6], 5: b[7], 4: b[8], 2: b[9]}
    s = lambda x: {'a': mp.nstr(x, 40)}; key = 'GF' + str(len(out) + 1)
    out[key] = {'label': name, 'u': mp.nstr(u, 30), 'v': mp.nstr(p / u, 30), 'b': {str(i): s(b[i]) for i in range(1, 10)}, 'w': {str(i): s(w[i]) for i in range(1, 10)}, 'apex': {str(i): s(a[i]) for i in range(1, 10)}}
    print(f'{key} {name}: perfect member u = {mp.nstr(u, 15)}, v = {mp.nstr(p / u, 15)}, Q = {mp.nstr(Q, 12)}, S = {mp.nstr(S, 12)}', flush=True)
json.dump(out, open('golden_family.json', 'w'), indent=1)
print('FINAL ok' if out else 'FINAL FAIL: no perfect member found')
