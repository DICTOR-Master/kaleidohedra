"""Second dual sweep CO ∩ mu·RD (README units of 2026-11-04-co-rd-sweep): CO = {|x_i| <= 1, |x|+|y|+|z| <= 2},
RD = polar of CO in the unit sphere = {|x_i|+|x_j| <= 1}. Exact in Q(sqrt2). Birds 1, 2 on this line."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweeplib as L
from sweeplib import F, Q, ZERO, ONE
import drive
import sympy as sp
L.set_field(2)
logf = open(os.path.join(os.path.dirname(__file__), '..', 'data', 's1_co_rd.log'), 'w')
def log(s): print(s); logf.write(s + '\n'); logf.flush()
pl = []
for i in range(3):
    for s in (1, -1):
        e = [F(0)] * 3; e[i] = F(s); pl.append((e, F(1), ZERO, 'cube'))
for s in itertools.product((1, -1), repeat=3):
    pl.append(([F(x) for x in s], F(2), ZERO, 'oct'))
for i, j in itertools.combinations(range(3), 2):
    for a, b in itertools.product((1, -1), repeat=2):
        e = [F(0)] * 3; e[i] = F(a); e[j] = F(b); pl.append((e, ZERO, F(1), 'rhomb'))
sw = L.Sweep(pl)
checks = []
R = drive.run_line(sw, Q(1, 2), log, 'CO-RD')
ws = [w['mu'] for w in R['walls']]
fw = [f['mu'] for f in R['feet']]
checks.append(('walls of S are 1, 4/3, 3/2, 2', ws == [F(1), F(Q(4, 3)), F(Q(3, 2)), F(2)]))
checks.append(('every wall determinant linear in mu, root at the wall', all(w['dets_ok'] for w in R['walls'])))
checks.append(('Euler 2 on both sides of every wall', all(w['kind']['euler'] == (2, 2) for w in R['walls'])))
# turn tests
c = ws[0] * ws[-1]
log(f'turn test: c = first*last wall = {c}; walls symmetric under mu -> c/mu: {drive.symmetric_under(ws, c)}')
checks.append(('walls of S symmetric under mu -> 2/mu', drive.symmetric_under(ws, F(2))))
ev = sorted(set(ws) | set(fw), key=float)
log(f'all events (S walls + foot walls): {ev}; symmetric under 2/mu: {drive.symmetric_under(ev, F(2))}')
# midsphere value of c: (rho_CO / rho_RD)^2 = (3/2)/(2/3) = 9/4
log(f'midsphere c = (rho_CO/rho_RD)^2 = 9/4: walls symmetric under 9/4: {drive.symmetric_under(ws, F(Q(9, 4)))}')
# antipol: S^v(mu) has cube at 1, oct at 3/2, rhomb at 2/mu: is it S(2/mu)? is it TO ∩ (2/mu)RD?
plTO = [(a, (F(Q(3, 2)) if f == 'oct' else b0), b1, f) for a, b0, b1, f in pl]
swTO = L.Sweep(plTO)
def same(A, B):
    A = sorted(tuple(float(c) for c in x) for x, _ in A); B = sorted(tuple(float(c) for c in x) for x, _ in B)
    return len(A) == len(B) and all(abs(a - b) < 1e-12 for u, v in zip(A, B) for a, b in zip(u, v))
on_line, on_to = [], []
for mu in [Q(11, 10), Q(5, 4), Q(7, 5), Q(29, 20), Q(8, 5), Q(9, 5)]:
    st = sw.structure(F(mu))
    Sv = L.Sweep(sw.antipol_planes(st, F(mu))).vertices(ZERO)
    on_line.append(same(Sv, sw.vertices(F(2) / F(mu))))
    ref = swTO if mu > Q(4, 3) else L.Sweep([p for p in pl if p[3] != 'oct'])
    on_to.append(same(Sv, ref.vertices(F(2) / F(mu))))
log(f'antipol S^v(mu) = S(2/mu) at 6 sample mu: {on_line}')
log(f'antipol S^v(mu) = TO ∩ (2/mu)RD for mu > 4/3 (TO = cube ∩ (3/2)oct), = cube ∩ (2/mu)RD for mu < 4/3, at 6 sample mu: {on_to}')
checks.append(('antipol leaves the line: S^v(mu) != S(2/mu) at all samples', not any(on_line)))
checks.append(('antipol = TO ∩ (2/mu)RD (mu > 4/3), cube ∩ (2/mu)RD (mu < 4/3)', all(on_to)))
# t_min envelope and its maximum
res = drive.tmin_envelope(sw, ev, log, 'CO-RD')
best = max(res, key=lambda r: r['fvalue'])
log(f'max t_min on (1, 2): {best["value"]} (~{best["fvalue"]:.12f}) at mu = {best["argmax"]} (~{float(best["argmax"]):.12f})')
t2, _, _ = sw.tmin(F(0, 1))
log(f't_min at the fixed point sqrt2: {t2} (~{float(t2):.12f})')
for mu in [Q(1), Q(2), Q(1, 2), Q(3)]:
    t, _, _ = sw.tmin(F(mu)); log(f't_min({mu}) = {t}')
checks.append(('t_min peak is NOT at sqrt2', abs(float(best['argmax']) - 2 ** .5) > 1e-6))
# flag radii of the CO: face centres (cube 1, triangle 4/3), edge midpoint (1,1/2,1/2): 3/2, vertex (1,1,0): 2
flags = [F(1), F(Q(4, 3)), F(Q(3, 2)), F(2)]
log(f'squared flag radii of the CO (square centre, triangle centre, edge midpoint, corner): {flags}')
checks.append(('walls = squared flag radii of the CO', ws == flags))
checks.append(('flag radii: R^2 h_sq^2 = rho^2 h_tri^2 = 2 (why the walls are 2/mu-symmetric)', flags[0] * flags[3] == flags[1] * flags[2] == F(2)))
# the interior maximum of t_min sits at the geometric mean of the jump wall and the foot wall next to it
checks.append(('interior t_min max at sqrt(3/2 * 8/5) = sqrt(12/5)', any(r['interior'] and sp.simplify(r['argmax'] - sp.sqrt(sp.Rational(12, 5))) == 0 for r in res)))
for n, ok in checks: log(('ok   ' if ok else 'FAIL ') + n)
allok = all(ok for _, ok in checks)
log('FINAL ok' if allok else 'FINAL FAIL: ' + '; '.join(n for n, ok in checks if not ok))
