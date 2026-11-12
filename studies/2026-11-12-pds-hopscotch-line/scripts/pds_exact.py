"""Aim 2 paper, closing item (12 Nov 2026, late): EXACT root isolation for every station of the 600-cell (Queens') line, replacing the
40-digit root location of pds_line.py in the two inner hops and for the silent point mu_Omega.
(a) Corners: in each of the three hops the corner x(mu) = x0 + mu x1 (exact, LH.chamber of pds_line.py at the same sample mu) gives
    P12(x(mu)), a degree-12 polynomial over Q(sqrt5); its zeros in the open hop are counted EXACTLY with the counter of canon_unique.py
    (norm over Q, exact real-root isolation in rational intervals of width < 1e-40, sign of gcd(A, F) over Q(sqrt5) at the rational
    endpoints); P12 is evaluated exactly at the walls.
(b) Canonical form: B(mu), the order-12 tone of Omega (exact, from data/pds-line.json; integrity checked against the logged values),
    numerator counted the same way per hop; exact signs at a rational point of each inner hop and at the walls.
(c) Order and the turn: the isolating intervals of mu_Omega, mu* and r = sqrt(r^2) are compared exactly (squares in Q(sqrt5)).
Controls: (P1) the known degree-20 station mu* = 0.924138673238867458601238076667 is re-isolated in the truncated-600-cell hop with its
minimal polynomial; (P2) the counter's own synthetic controls (2 distinct roots incl. a double one; a conjugate root not counted);
(P3) mu_Omega agrees with pds_line's 30 digits; B's logged end signs and B(r) agree; (N1) B - B(q) at a rational q inside each inner
hop has a root there (the counter does see roots in those hops); (N2) P12 corner polynomial of one hop does not vanish on the corners of
the other hops' sample (the three corner orbits differ).
Usage: python -u pds_exact.py [pilot]   (pilot = counter controls + the truncated-600-cell hop only)"""
import sys, os, time, json
T0 = time.time()
PIL = len(sys.argv) > 1 and sys.argv[1] == 'pilot'
here = os.path.dirname(os.path.abspath(__file__))
import sympy as sp
from fractions import Fraction as Fr
# ---- the exact counter of canon_unique.py (same code, not retyped) ----
cu = open(os.path.join(here, '..', '..', '2026-11-10-canonical-sweep', 'scripts', 'canon_unique.py')).read()
s5 = sp.sqrt(5)
ns = {'sp': sp, 's5': s5}
exec(cu[cu.index('# ---------- exact arithmetic in Q(sqrt5) ----------'):cu.index('ok_all = True')], ns)
count_roots, sgn5, split5 = ns['count_roots'], ns['sgn5'], ns['split5']
ok = True
OUT = {}
def check(name, cond):
    global ok; ok &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)
x = sp.Symbol('x')
r_ = count_roots((x - (1 + s5) / 8) * (x - sp.Rational(3, 7)) ** 2 * (x ** 2 - 2), x, sp.Integer(0), sp.Integer(1), 'P2')
check(f'(P2) counter: (x-(1+sqrt5)/8)(x-3/7)^2(x^2-2) on (0,1) has {len(r_)} distinct roots (expect 2)', len(r_) == 2)
r_ = count_roots(x - (3 + s5) / 4, x, sp.Integer(0), sp.Integer(1), 'P2n')
check(f'(P2) counter: x-(3+sqrt5)/4 on (0,1): {len(r_)} roots (expect 0; conjugate (3-sqrt5)/4 inside, not counted)', len(r_) == 0)
print(f'PROGRESS 0.05 counter controls ({time.time() - T0:.0f} s)', flush=True)

# ---- H4 data and the line from pds_line.py (same code, not retyped; its Silent Queens degree-12 Red Queen check is skipped here) ----
src = open(os.path.join(here, 'pds_line.py')).read()
g = {'__name__': 'pds_line_defs'}
exec(src[:src.index('# ================= CONTROL 1')], g)
g['PILOT'] = True                                   # only skips the heavy Red Queen degree-12 check and design k > 4 in the H4 block
exec(src[src.index('# ================= H4 data'):src.index('# ================= the H4 line')], g)
K, Line, W, V, P12e, y, fr, r2 = g['K'], g['Line'], g['W'], g['V'], g['P12e'], g['y'], g['fr'], g['r2']
LH = Line('H4', W, V)
ks = lambda k: sp.Rational(k.a.numerator, k.a.denominator) + sp.Rational(k.b.numerator, k.b.denominator) * s5
walls = [ks(w) for w in fr]                         # 1, (5+sqrt5)/8, 1/2+sqrt5/6, r^2
R2 = ks(r2)
check(f'walls exact: {walls}', walls == [1, (5 + s5) / 8, sp.Rational(1, 2) + s5 / 6, (7 + 3 * s5) / 16] or
      all(sp.expand(sp.radsimp(a - b)) == 0 for a, b in zip(walls, [1, (5 + s5) / 8, sp.Rational(1, 2) + s5 / 6, (7 + 3 * s5) / 16])))
hops = [('truncated 600-cell hop', walls[1], walls[0], Fr(3809, 4000)),
        ('middle hop', walls[2], walls[1], Fr(88859, 100000)),
        ('truncated 120-cell hop', R2, walls[2], Fr(10809, 12500))]
if PIL: hops = hops[:1]
m = sp.Symbol('m'); mu = sp.Symbol('mu')
J = json.load(open(os.path.join(here, '..', 'data', 'pds-line.json')))
MIN20 = sp.Poly(sp.sympify(J['hops']['truncated 600-cell hop']['design19_stations'][0][1], locals={'m': m}), m)
MUSTAR = sp.Float('0.924138673238867458601238076667', 40)
MUOM = sp.Float(J['hops']['truncated 600-cell hop']['B_zeros'][0], 40)
def interval_vs_r(a, b):                            # exact: is r = sqrt(r^2) strictly outside the positive rational interval [a, b]?
    return 'below r' if sgn5(R2 - b * b) > 0 else ('above r' if sgn5(a * a - R2) > 0 else 'contains r')

corner_polys = {}; ivals = {}
for k, (hname, lo, hi, mu0) in enumerate(hops):
    t1 = time.time()
    faces, simp, fv, mm = LH.chamber(mu0)
    x0, x1 = next(iter(faces.values()))
    xm = [ks(p) + ks(q) * m for p, q in zip(x0, x1)]
    A = sp.expand(sp.radsimp(sp.expand(P12e.subs(dict(zip(y, xm)), simultaneous=True))))
    corner_polys[hname] = A
    print(f'== {hname} ({float(lo):.9f}, {float(hi):.9f}): {len(faces)} corners; P12(x(mu)) degree {sp.Poly(A, m).degree()} over Q(sqrt5) '
          f'({time.time() - t1:.0f} s)', flush=True)
    for wname, w in (('lower wall', lo), ('upper wall', hi)):
        check(f'{hname}: P12(corner) != 0 at the {wname} (exact)', sgn5(sp.expand(A.subs(m, w))) != 0)
    st = count_roots(A, m, lo, hi, hname + ' P12')
    for F, (a, b), f in st:
        print(f'   19-design station mu = {sp.N(f, 30)} (interval width {float(b - a):.1e}); norm factor degree {sp.Poly(F, m).degree()}', flush=True)
    if k == 0:
        check('(P1) truncated-600-cell hop: exactly one station, mu* = 0.924138673238867458601238076667, factor = the degree-20 minimal polynomial',
              len(st) == 1 and abs(sp.N(st[0][2], 40) - MUSTAR) < 1e-28 and
              sp.expand(sp.Poly(st[0][0], m).monic().as_expr() - MIN20.monic().as_expr()) == 0)
        if st: ivals['mu*'] = st[0][1]
    else:
        check(f'{hname}: no 19-design station (exact; was 40-digit root location)', len(st) == 0)
    # (b) B(mu) of this hop
    Bs = J['hops'][hname]['B']
    B = sp.sympify(Bs, locals={'mu': mu})
    num = sp.expand(sp.radsimp(sp.numer(sp.together(B)))); den = sp.denom(sp.together(B))
    print(f'   B = numerator (degree {sp.Poly(num, mu).degree()} over Q(sqrt5)) / {den}', flush=True)
    for wname, w in (('lower wall', lo), ('upper wall', hi)):
        check(f'{hname}: B != 0 at the {wname} (exact)', sgn5(sp.expand(num.subs(mu, w))) != 0)
    sgn_ends = [sgn5(sp.expand(num.subs(mu, w))) for w in (lo, hi)]
    check(f'(P3) {hname}: exact signs of B at the hop ends {sgn_ends} = pds_line log {J["hops"][hname]["B_sign_at_ends"]}',
          [str(s) for s in sgn_ends] == J['hops'][hname]['B_sign_at_ends'])
    bz = count_roots(num, mu, lo, hi, hname + ' B')
    for F, (a, b), f in bz:
        print(f'   B = 0 at mu = {sp.N(f, 30)} (interval width {float(b - a):.1e}); minimal polynomial over Q (norm factor, degree '
              f'{sp.Poly(F, mu).degree()}): {sp.Poly(F, mu).as_expr()}', flush=True)
    q = sp.Rational(mu0.numerator, mu0.denominator)
    if k == 0:
        check('(P3) truncated-600-cell hop: B has exactly one zero, mu_Omega, equal to pds_line\'s 30 digits',
              len(bz) == 1 and abs(sp.N(bz[0][2], 40) - MUOM) < 1e-28)
        if bz:
            ivals['mu_Omega'] = bz[0][1]
            F = sp.Poly(bz[0][0], mu)
            OUT['mu_Omega'] = {'value': str(sp.N(bz[0][2], 30)), 'minpoly_Q': str(F.as_expr()), 'degree': F.degree(),
                               'interval': [str(bz[0][1][0]), str(bz[0][1][1])]}
            check('mu_Omega is not a root of the fixed point\'s minimal polynomial 64m^4 - 56m^2 + 1 nor of mu*\'s (exact)',
                  sp.gcd(F.as_expr(), 64 * mu ** 4 - 56 * mu ** 2 + 1) == 1 and sp.gcd(F.as_expr(), MIN20.as_expr().subs(m, mu)) == 1)
        Br = sp.N(B.subs(mu, sp.sqrt(R2)), 30)
        check(f'(P3) B(r) = {Br} agrees with the log {J["hops"][hname]["B_at_fixed_point"][:14]}',
              abs(Br - sp.Float(J['hops'][hname]['B_at_fixed_point'], 30)) < 1e-20)
    else:
        check(f'{hname}: B has no zero (exact; was 40-digit root location)', len(bz) == 0)
        check(f'{hname}: B > 0 at mu = {q} (exact), hence B > 0 on the whole hop', sgn5(sp.expand(num.subs(mu, q))) * sgn5(sp.expand(den.subs(mu, q))) > 0)
        nb = count_roots(sp.expand(num - num.subs(mu, q)), mu, lo, hi, hname + ' N1')
        check(f'(N1) {hname}: B_num - B_num({q}) has {len(nb)} root(s) in the hop (>= 1: the counter sees roots here)', len(nb) >= 1)
    print(f'PROGRESS {0.1 + 0.3 * (k + 1):.2f} {hname} done ({time.time() - T0:.0f} s)', flush=True)

# (N2) the three corner polynomials differ
if not PIL:
    names = list(corner_polys)
    check('(N2) the three hops have three different corner polynomials P12(x(mu))',
          all(sp.expand(corner_polys[a] - corner_polys[b]) != 0 for i, a in enumerate(names) for b in names[i + 1:]))
# (c) order on the line, the fixed point and the turn, exactly
if 'mu*' in ivals and 'mu_Omega' in ivals:
    (a1, b1), (a2, b2) = ivals['mu_Omega'], ivals['mu*']
    check(f'exact order: mu_Omega < mu* (disjoint isolating intervals, {float(b1):.12f} < {float(a2):.12f})', b1 < a2)
    p1, p2 = interval_vs_r(a1, b1), interval_vs_r(a2, b2)
    check(f'exact: mu_Omega {p1}, mu* {p2}; so r is neither, and B(r) != 0, P12(corner(r)) != 0 exactly', p1 == 'below r' and p2 == 'below r')
    # B(r) < 0 exactly: B has one simple sign change in the hop, at mu_Omega < r, and B(1) < 0
    check('exact: B(r) < 0 (B changes sign only at mu_Omega < r and B < 0 at the upper wall mu = 1)',
          J['hops']['truncated 600-cell hop']['B_sign_at_ends'][1] == '-1' and p1 == 'below r')
    # turn images r^2/mu lie in the same hop and differ from mu (mu != r); by uniqueness they are not stations
    for nm, (a, b) in (('mu_Omega', (a1, b1)), ('mu*', (a2, b2))):
        ti = (sgn5(R2 / b - walls[1]) > 0, sgn5(walls[0] - R2 / a) > 0)
        check(f'exact: turn image r^2/{nm} lies in the truncated-600-cell hop ({float(R2 / b):.6f}..{float(R2 / a):.6f}) and is not {nm} '
              f'(since {nm} != r); by the uniqueness above it is not a station of the same kind', all(ti))
json.dump(OUT, open(os.path.join(here, '..', 'data', 'pds-exact-pilot.json' if PIL else 'pds-exact.json'), 'w'), indent=1)
print(f'THEOREM: on the whole 600-cell line P12(corner) has exactly one zero (mu*) and B has exactly one zero (mu_Omega); exact'
      if ok and not PIL else ('pilot controls held' if ok else 'not proved'), flush=True)
print(f'time {time.time() - T0:.0f} s', flush=True)
print('FINAL ok: all controls held' if ok else 'FINAL FAIL')
