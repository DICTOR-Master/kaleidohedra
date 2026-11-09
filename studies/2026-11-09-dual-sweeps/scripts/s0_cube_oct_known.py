"""Known case first: the cube-octahedron line P_mu = [-1,1]^3 ∩ {|x|+|y|+|z| <= mu} (2026-11-09-hopscotch-rows).
Expect: face-structure walls 1, 2, 3 (linear 4x4 determinants), antipol S^v(mu) = S(3/mu), t_min = min(mu, 3/mu, 5 - mu - 3/mu)
on (1, 3), maximum 5 - 2 sqrt3 at the turn's fixed point sqrt3. Exact in Q(sqrt3)."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweeplib as L
from sweeplib import F, Q, ZERO
L.set_field(3)
pl = []
for i in range(3):
    for s in (1, -1):
        e = [F(0)] * 3; e[i] = F(s); pl.append((e, F(1), ZERO, 'cube'))
for s in itertools.product((1, -1), repeat=3):
    pl.append(([F(x) for x in s], ZERO, F(1), 'oct'))
sw = L.Sweep(pl)
checks = []
walls = sw.walk(Q(1, 2))
ws = [w['mu'] for w in walls]
print('walls', ws)
checks.append(('walls 1,2,3', ws == [F(1), F(2), F(3)]))
for w in walls:
    quad = tuple(sorted(set(w['hits'][0][1]) | {w['hits'][0][2]}))
    d0, d1, lin, root = sw.wall_det(quad)
    c = L.classify(sw, w['below'], w['above'])
    print(f"wall {w['mu']}: det planes {[sw.P[k][3] for k in quad]} = {d0} + {d1} mu, linear {lin}, root {root}; {c['kinds']}; "
          f"faces born {c['born']} died {c['died']} bonds lost {c['bonds_lost']} gained {c['bonds_gained']}; census {c['census_below']} -> {c['census_above']}")
    checks.append((f'det linear, root = wall {w["mu"]}', lin and root == w['mu']))
# antipol = S(3/mu)
for mu in [Q(6, 5), Q(3, 2), Q(7, 4), Q(2), Q(5, 2), Q(13, 5)]:
    st = sw.structure(F(mu))
    Sv = L.Sweep(sw.antipol_planes(st, F(mu)))
    A = sorted(tuple(float(c) for c in x) for x, _ in Sv.vertices(ZERO))
    B = sorted(tuple(float(c) for c in x) for x, _ in sw.vertices(F(3) / F(mu)))
    ok = len(A) == len(B) and all(abs(a - b) < 1e-12 for u, v in zip(A, B) for a, b in zip(u, v))
    checks.append((f'antipol of S({mu}) = S({Q(3) / mu})', ok))
# t_min closed form at 43 rationals
bad = 0
for i in range(43):
    mu = Q(1) + Q(2 * (i + 1), 44)
    t, _, _ = sw.tmin(F(mu))
    f = min(mu, 3 / mu, 5 - mu - 3 / mu)
    if t != F(f): bad += 1; print('mismatch', mu, t, f)
checks.append(('t_min = min(mu, 3/mu, 5-mu-3/mu) at 43 rationals', bad == 0))
r3 = F(0, 1)
t, _, _ = sw.tmin(r3)
print('t_min(sqrt3) =', t)
checks.append(('t_min(sqrt3) = 5 - 2 sqrt3', t == F(5, -2)))
# foot walls (walls of S^v, i.e. of the foot-point hull P(S)) on (1,3): expected at mu = 3/2 (image of the wall 2)
st = sw.structure(F(2) - F(Q(1, 10)))
fs = L.foot_sweep(sw, st['facets'])
fw = [w for w in fs.walk(Q(1, 3) + Q(1, 100), top=F(1)) if w['mu'] < F(1)]
print('foot walls in nu=1/mu inside (1/3, 1):', [w['mu'] for w in fw], '-> mu =', [F(1) / w['mu'] for w in fw])
checks.append(('foot walls on (1,3): mu = 3/2 only', [F(1) / w['mu'] for w in fw] == [F(Q(3, 2))]))
for n, ok in checks: print(('ok  ' if ok else 'FAIL') + ' ' + n)
allok = all(ok for _, ok in checks)
print('FINAL ok' if allok else 'FINAL FAIL: ' + '; '.join(n for n, ok in checks if not ok))
