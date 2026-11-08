"""Self-similar yantras (DICTO 11-08: the gnomon should give the simple formula). Is an inner pair of triangles an exact scaled copy
of the great pair (t3 apex down, t7 apex up)? A scaling about a point (0, c) on the axis with ratio r (r < 0 flips: up <-> down) maps a
triangle (apex depth a, base depth b, half-width w) to (c + r(a - c), c + r(b - c), |r| w). Require t3 -> X and t7 -> Y exactly: six
equations; unknowns u, v, Q, S (the yantra) and c, r: isolated solutions. Every pairing (X, Y) with the right orientations is tried
from many starts; valid yantras are reported with r, c and the traditional counts."""
import mpmath as mp, itertools, json
from model import solve, all_conditions, order_ok
mp.mp.dps = 50
def yan(u, v, Q, S):
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root=1)
def apexes(t):
    b = t['b']; return {3: mp.mpf(1), 7: mp.mpf(0), 8: b[1], 6: b[2], 9: b[3], 1: b[6], 5: b[7], 4: b[8], 2: b[9]}
DOWN, UP = [1, 2, 4, 5], [6, 8, 9]
pairs = [(X, Y, 1) for X in DOWN for Y in UP] + [(X, Y, -1) for X in UP for Y in DOWN]
found = {}
for X, Y, sg in pairs:
    def F(u, v, Q, S, c, r):
        t = yan(u, v, Q, S); a = apexes(t); b, w = t['b'], t['w']
        return [c + r * (a[3] - c) - a[X], c + r * (b[3] - c) - b[X], abs(r) * w[3] - w[X],
                c + r * (a[7] - c) - a[Y], c + r * (b[7] - c) - b[Y], abs(r) * w[7] - w[Y]]
    seen = []
    for k in range(60):
        rng = mp.rand
        x0 = (mp.mpf(0.55) + 0.4 * mp.rand(), mp.mpf(0.55) + 0.4 * mp.rand(), mp.mpf(0.45) + 0.2 * mp.rand(), mp.mpf(0.75) + 0.2 * mp.rand(), mp.mpf(0.3) + 0.4 * mp.rand(), sg * (mp.mpf(0.1) + 0.6 * mp.rand()))
        try:
            sol = mp.findroot(F, x0, tol=mp.mpf(10)**-40, maxsteps=60)
        except (Exception, ZeroDivisionError): continue
        if any(abs(mp.im(x)) > mp.mpf(10)**-30 for x in sol): continue
        u, v, Q, S, c, r = [mp.re(x) for x in sol]; sol = (u, v, Q, S, c, r)
        if not (0.2 < u < 3 and 0.2 < v < 3): continue
        try: t = yan(u, v, Q, S)
        except Exception: continue
        if not order_ok(t, mp.mpf(10)**-25) or max(abs(e) for n, e in all_conditions(t)) > mp.mpf(10)**-30: continue
        if any(abs(r - s[5]) < 1e-20 for s in seen): continue
        seen.append(sol)
        key = f't3->t{X}, t7->t{Y}'
        b, w = t['b'], t['w']; a = apexes(t); s = lambda x: {'a': mp.nstr(x, 40)}
        found[key + f' #{len(seen)}'] = {'u': mp.nstr(u, 25), 'v': mp.nstr(v, 25), 'r': mp.nstr(r, 25), 'c': mp.nstr(c, 25),
            'b': {str(i): s(b[i]) for i in range(1, 10)}, 'w': {str(i): s(w[i]) for i in range(1, 10)}, 'apex': {str(i): s(a[i]) for i in range(1, 10)}}
        print(f'{key}: u = {mp.nstr(u, 12)}, v = {mp.nstr(v, 12)}, scale r = {mp.nstr(r, 15)}, centre depth c = {mp.nstr(c, 12)}', flush=True)
json.dump(found, open('selfsimilar.json', 'w'), indent=1)
print('valid self-similar yantras:', len(found))
print('FINAL ok' if found else 'FINAL FAIL: no self-similar yantra found')
