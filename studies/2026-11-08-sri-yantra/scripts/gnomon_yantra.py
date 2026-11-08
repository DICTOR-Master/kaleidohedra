"""Gnomon yantra (DICTO 11-08, option A: a gnomon that grows the yantra into larger copies of itself). If the incircle of the
innermost triangle (the bindu triangle: legs of t1, base of t5) is centred on the yantra's centre (Kulaichev's condition (d)), a copy
of the whole yantra scaled to that incircle fits it exactly and concentrically: the yantra minus that disc is a gnomon, and the
yantras nest without end at ratio k = (incircle radius) / (outer radius). Keep the Cleo-Octangula (u = 2/phi^2 above, v = 1/sqrt2
below) and impose (d) together with ONE of (b) t1 corners on the circle or (c) t9 corners on the circle. Report validity, k, and
write the data for the counts (43 triangles, 18 marmas, 24 sandhis)."""
import mpmath as mp, json
from model import solve, all_conditions, order_ok
mp.mp.dps = 60
phi = (1 + mp.sqrt(5)) / 2; u = 2 / phi**2; v = 1 / mp.sqrt(2)
def yan(Q, S):
    P = v**2 / (1 + v**2); R = 1 / (1 + u**2)
    return solve(P, Q, R, S, v / (1 + v**2), u / (1 + u**2), mp.sqrt, root=1)
def cond_b(t): return t['w'][1]**2 + t['b'][1]**2 - t['b'][1]
def cond_c(t): return t['w'][9]**2 + t['b'][9]**2 - t['b'][9]
def incircle(t, Q):
    b, w = t['b'], t['w']; m1 = w[1] / (Q - b[1])      # t1 legs: x = m1 (Q - d), apex at depth Q; t5 base at depth b5
    # incircle centre on the axis at depth c: distance to base = c - b5... base is ABOVE or BELOW? use the inradius formula of the
    # isosceles triangle with apex depth Q, base depth b5, half-width at base hw = m1*|Q - b5|
    h = abs(Q - b[5]); hw = m1 * h; side = mp.sqrt(hw**2 + h**2); r = hw * h / (hw + side)
    c = b[5] + (r if Q > b[5] else -r)                  # centre depth: r from the base towards the apex
    return c, r
def cond_d(t, Q): c, r = incircle(t, Q); return c - mp.mpf(1) / 2
out = {}
for label, other in (('(b) t1 corners on circle + (d) centred bindu', cond_b), ('(c) t9 corners on circle + (d) centred bindu', cond_c)):
    sol = None
    for Q0 in [mp.mpf(x) / 100 for x in range(48, 62, 2)]:
        for S0 in [mp.mpf(x) / 100 for x in range(80, 97, 2)]:
            try:
                Q, S = mp.findroot(lambda Q, S: [other(yan(Q, S)), cond_d(yan(Q, S), Q)], (Q0, S0), tol=mp.mpf(10)**-50)
                t = yan(Q, S)
                if order_ok(t, mp.mpf(10)**-30) and max(abs(x) for n, x in all_conditions(t)) < mp.mpf(10)**-40: sol = (Q, S, t); break
            except Exception: pass
        if sol: break
    if not sol: print(label, ': no valid yantra'); continue
    Q, S, t = sol; c, r = incircle(t, Q); k = r / (mp.mpf(1) / 2)
    b, w = t['b'], t['w']; a = {3: mp.mpf(1), 7: mp.mpf(0), 8: b[1], 6: b[2], 9: b[3], 1: b[6], 5: b[7], 4: b[8], 2: b[9]}
    s = lambda x: {'a': mp.nstr(x, 40)}
    name = 'G' + str(len(out) + 1)
    out[name] = {'label': label, 'k': mp.nstr(k, 30), 'b': {str(i): s(b[i]) for i in range(1, 10)}, 'w': {str(i): s(w[i]) for i in range(1, 10)}, 'apex': {str(i): s(a[i]) for i in range(1, 10)}}
    print(f'{name} {label}: valid; Q = {mp.nstr(Q, 12)}, S = {mp.nstr(S, 12)}; nesting ratio k = {mp.nstr(k, 15)} (1/k = {mp.nstr(1/k, 12)}); other circle condition misses by {mp.nstr(cond_c(t) if other is cond_b else cond_b(t), 4)}')
json.dump(out, open('gnomon.json', 'w'), indent=1)
print('FINAL ok' if out else 'FINAL FAIL: no gnomon yantra on the Cleo-Octangula')
