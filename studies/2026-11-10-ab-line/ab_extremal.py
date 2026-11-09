"""Aim 1, step 2 (DICTO 10 Nov 2026): what is extremal at the turn on the AB line? Claim, from the window areas of the four
complementary pairs: per window area 1 + 4t + 2t^2, squares (0/90 deg) 1, squares (45/135 deg) 2t^2, each rhombus type t. Hence
edges in the four directions are in the ratio (1+2t) : (2t+2t^2) : (1+2t) : (2t+2t^2), equal only at t = 1/sqrt2, and the number of
squares per rhombus (1+2t^2)/(4t) is smallest exactly at t = 1/sqrt2 (value 1/sqrt2: the AB ratio 1 : sqrt2), symmetric under the turn.
Check against the actual tilings: edge-direction frequencies counted from the vertex stars (raw, not reduced) of T(t), exact rationals,
for many t on both sides of 1/sqrt2. usage: python3 ab_extremal.py"""
import sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-09-ab-turn', 'scripts'))
from zono import zonogon, arrangement, area
def edge_dirs(t):
    Ev = [(-t, t), (Fr(1), Fr(0)), (-t, -t), (Fr(0), Fr(1))]; W = zonogon(Ev); A = area(W); e = [Fr(0)] * 4
    for P, st in arrangement(W, Ev):
        f = area(P) / A
        for d in range(8):
            if st[d]: e[d % 4] += f
    return e
ok = True; rows = []
for t in [Fr(11, 20), Fr(3, 5), Fr(2, 3), Fr(7, 10), Fr(5, 7), Fr(12, 17), Fr(17, 24), Fr(7, 10), Fr(3, 4), Fr(4, 5), Fr(9, 10)]:
    e = edge_dirs(t)
    want = [1 + 2*t, 2*t + 2*t*t, 1 + 2*t, 2*t + 2*t*t]
    ratio_ok = all(e[k] * want[0] == e[0] * want[k] for k in range(4))
    sq_per_rh = (1 + 2*t*t) / (4*t)
    ok &= ratio_ok
    rows.append((float(t), [float(x / e[0]) for x in e], ratio_ok, float(sq_per_rh)))
for r in rows: print(f't = {r[0]:.4f}: edge directions (relative to 0 deg) {[round(x, 6) for x in r[1]]}  matches formula: {r[2]}  squares per rhombus {r[3]:.6f}')
# exact extremum of squares per rhombus: f(t) = 1/(4t) + t/2, f'(t) = -1/(4t^2) + 1/2 = 0  <=>  t^2 = 1/2; f(1/(2t)) = f(t)
print('squares per rhombus is smallest at t = 1/sqrt2 (value 1/sqrt2 = 0.707107); every sampled t gives more:', all(r[3] > 2**-0.5 for r in rows))
print('FINAL ok' if ok and all(r[3] > 2**-0.5 for r in rows) else 'FINAL FAIL')
