"""LEAD 3 (12 Nov 2026): which yantras sit at the turn u = v (Kulaichev's (a)) AND meet (b), (c), (d)? Full solution set, exact.
Definitions (studies/2026-11-08-sri-yantra, model.py / natural.py): slopes u (t7, from O), v (t3, from T); (b) t1's base corners on the
circle, (c) t9's base corners on the circle, (d) the bindu's incircle centred (centre at depth 1/2). Yantra = model.order_ok (bases
strictly ordered, half-widths > 0, apexes on the correct side, corners in the closed disc).
Reduction (exact, stated in the README): admissible forces 0 < u < 1 at u = v (b3 < b7 <=> P < R <=> u^2 < 1; w7 > 0 <=> u > 0);
(b) with w1 > 0 <=> t1's corner is the circle point (t/(1+t^2), t^2/(1+t^2)) with t > 0; for an admissible yantra the (1,3,8) marma
gives Q = Q(t) (its coefficient vanishes only if b1 = P, b1 = R or w1 = 0); so every admissible (a)(b)(c)(d)-yantra is a real zero of
   G(u, S) = 0  (c),   H(u, t, S) = 0  (closing equation, ALL factors kept),   D(u, t, S) = 0  ((d) squared)     with v = u.
Elimination with every factor kept (Singular via sage, PARI): Res_S of G with each factor of H and of D, all factors, then Res_t of
every pair of t-dependent factors, all factors in u. Every real root in (0, 1) of every u-factor is a candidate; for each, all real
(t > 0, S) solutions are found and the yantra is rebuilt by model.solve; it is kept only if it meets every condition (unsquared (d))
and is admissible. Real roots in u: PARI polrootsreal, each re-isolated in an exact rational interval (polsturm = 1) and refined by
Newton with an exact-interval bracket; t, S at the candidate: mpmath polyroots at 2 DIG + 40 digits; the decision margins are printed
(smallest margin vs the decision threshold 1e-(DIG/3)).
POSITIVE controls: Kulaichev's yantra is found, its u-factor is exactly the stored f348 (figures/kulaichev-minpoly-u.txt), u agrees
with the stored 60 digits, and it is admissible with (d) unsquared. NEGATIVE controls: the 3-4-5 rhombus u = 3/4 is a root of no
u-factor (its (d) misses by 2.4e-5, exact evaluation); without the admissibility test more than one real solution remains (the test
does real work); a perturbed Kulaichev point fails the condition test.
usage: python -u lead3_turn_yantras.py [pilot|full]     (pilot: 60 digits; full: 300 digits)"""
import sys, os, time, json, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
SY = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-08-sri-yantra'))
sys.path.insert(0, os.path.join(SY, 'scripts'))
os.chdir(os.path.join(HERE, '..', 'data'))            # natural.py reads golden_family.json from the working folder
mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
DIG = 60 if mode == 'pilot' else 300
EPSD, MARD = DIG // 3, DIG // 6                       # decision threshold 1e-EPSD; every rejection must exceed 1e-MARD
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
checks = {}
def check(c, msg): checks[msg] = bool(c); say(('ok   ' if c else 'FAIL ') + msg)
with contextlib.redirect_stdout(io.StringIO()):
    import natural as N
import model
import sympy as sp
import mpmath as mp
mp.mp.dps = 2 * DIG + 40                              # headroom for degree-396 evaluations; decisions use 1e-EPSD
eps = mp.mpf(10) ** (-EPSD)
tomp = lambda z: mp.mpf(str(z).replace(' ', ''))
from sage.all__sagemath_singular import QQ, PolynomialRing
import cypari2
pari = cypari2.Pari(); pari.allocatemem(3 * 10**9); pari.set_real_precision(DIG + 20)
Rg = PolynomialRing(QQ, 'u,t,S'); U, Tt, SS = Rg.gens(); Fr = Rg.fraction_field()
R5 = PolynomialRing(QQ, 'u,v,t,S'); V5 = R5.gens()[1]
def to_sage(e):                                      # sympy expression in u, v, t, S -> sage with v = u (the turn)
    F5 = R5(sp.sstr(sp.expand(e)).replace('**', '^'))
    return Rg(F5.subs({V5: R5.gens()[0]}))
Gk = to_sage(N.G); Hk = to_sage(N.H)
say('G, H with v = u: degrees in (u, t, S)', [Gk.degree(x) for x in (U, Tt, SS)], [Hk.degree(x) for x in (U, Tt, SS)])
# (d) squared, the same formulas as stage4_elim.py (yantra audit), case K
Fv = U; one = Fr(1)
Pf = Fv**2 / (1 + Fv**2); Rf = one / (1 + U**2); w3f = Fv / (1 + Fv**2); w7f = U / (1 + U**2)
xWf = w7f * Pf / Rf; k3f = w3f / (1 - Pf)
Qn_, Qd_ = sp.fraction(sp.factor(N.Q)); Qf = Fr(to_sage(Qn_)) / Fr(to_sage(Qd_))
xXf = xWf * (SS - Rf) / (SS - Pf); k9f = xXf / (Rf - Pf)
b1f = Tt**2 / (1 + Tt**2); w1f = Tt / (1 + Tt**2); m1f = w1f / (Qf - b1f)
b5f = (m1f * Qf + k9f * Pf) / (m1f + k9f); hf = Qf - b5f; hwf = m1f * hf; cf = one / 2 - b5f
Dexpr = (hwf**2 + hf**2) * cf**2 - (hwf * hf - hwf * cf)**2
Dk = Rg(Dexpr.numerator())
say('D: degrees in (u, t, S)', [Dk.degree(x) for x in (U, Tt, SS)])
def facs(F): return [(f, m) for f, m in F.factor() if f.degree() > 0]
Gf, Hf, Df = facs(Gk), facs(Hk), facs(Dk)
show = lambda L: [((f.degree(U), f.degree(Tt), f.degree(SS)), m) for f, m in L]
say('factors of G', show(Gf)); say('factors of H', show(Hf)); say('factors of D', show(Df))
# elimination, every factor kept
uonly = []                                            # polynomials in u alone whose roots are candidates
pairs = []                                            # (a, b, tag): t-dependent factors from the H-side and the D-side
for g, _ in Gf:
    if g.degree(SS) == 0:
        uonly.append((g, 'G factor free of S')); continue
    sideH, sideD = [], []
    for h, _ in Hf:
        r = g.resultant(h, SS) if h.degree(SS) > 0 else h
        assert r != 0, 'Res_S(G, H-factor) vanishes identically'
        sideH += [f for f, m in facs(r)]
    for d, _ in Df:
        r = g.resultant(d, SS) if d.degree(SS) > 0 else d
        assert r != 0, 'Res_S(G, D-factor) vanishes identically'
        sideD += [f for f, m in facs(r)]
    for side, nm in ((sideH, 'H'), (sideD, 'D')):
        for f in side:
            if f.degree(Tt) == 0: uonly.append((f, f'{nm}-side factor free of t'))
    for a in {f for f in sideH if f.degree(Tt) > 0}:
        for b in {f for f in sideD if f.degree(Tt) > 0}:
            pairs.append((g, a, b))
say(f'{len(pairs)} (H-side, D-side) factor pairs; {len(uonly)} u-only factors')
cand_polys = []                                       # (u-polynomial in PARI, origin)
gcd_bad = []
for i, (g, a, b) in enumerate(pairs):
    gg = a.gcd(b)
    if gg.degree(Tt) > 0: gcd_bad.append((a, b, gg)); continue
    A = pari(str(a).replace('t', 'z')); B = pari(str(b).replace('t', 'z'))
    r = pari.polresultant(A, B, 'z')
    if r == 0: gcd_bad.append((a, b, None)); continue
    fz = pari.factor(r)
    for j in range(len(fz[0])):
        if pari.poldegree(fz[0][j], 'u') > 0: cand_polys.append((fz[0][j], (g, a, b)))
    print(f'PROGRESS {(i + 1) / max(1, len(pairs)):.3f} resultants', flush=True)
# shared factors = curves of solutions of the polynomial system; each must be one of t = +-u, t = +-1/u (exact obstruction:
# t = u gives b1 = P = b3, t = 1/u gives b1 = R = b7 (bases not strictly ordered), t < 0 gives w1 < 0)
known = {Rg(Tt - U): 't = u: b1 = u^2/(1+u^2) = P = b3 (t1 base on t3 base)', Rg(Tt + U): 't = -u < 0: w1 < 0',
         Rg(U * Tt - 1): 't = 1/u: b1 = 1/(1+u^2) = R = b7 (t1 base on t7 base)', Rg(U * Tt + 1): 't = -1/u < 0: w1 < 0'}
curves = set()
for a, b, gg in gcd_bad:
    for f, m in (gg.factor() if gg is not None else []):
        if f.degree() == 0: continue
        fk = next((k for k in known if f == k or f == -k), None)
        curves.add(str(fk) if fk is not None else 'UNKNOWN ' + str(f))
say('curves of solutions from shared factors:', sorted(curves))
for cu in sorted(curves):
    if not cu.startswith('UNKNOWN'): say(f'   {cu}: {known[Rg(cu)]} -> not admissible (exact)')
check(all(gg is not None for _, _, gg in gcd_bad) and not any(c.startswith('UNKNOWN') for c in curves),
      'every curve of the polynomial system lies on t = +-u or t = +-1/u, none admissible (exact): the admissible solutions are isolated')
# the exact identities behind the obstruction
check(sp.simplify((N.t**2 / (1 + N.t**2)).subs(N.t, N.u) - N.u**2 / (1 + N.u**2)) == 0 and
      sp.simplify((N.t**2 / (1 + N.t**2)).subs(N.t, 1 / N.u) - 1 / (1 + N.u**2)) == 0, 'b1(t = u) = P and b1(t = 1/u) = R at v = u (exact)')
for f, why in uonly:
    if f.degree(U) > 0: cand_polys.append((pari(str(f)), None))
# distinct u-factors
uniq = []
for P_, org in cand_polys:
    P_ = P_ / pari.pollead(P_, 'u')
    if not any(P_ == Q_ for Q_, _ in uniq): uniq.append((P_, org))
say(f'{len(uniq)} distinct u-factors; degrees', sorted(int(pari.poldegree(P_, "u")) for P_, _ in uniq))
f348 = pari(open(os.path.join(SY, 'figures', 'kulaichev-minpoly-u.txt')).read().strip().replace('x', 'u'))
f348 = f348 / pari.pollead(f348, 'u')
check(any(P_ == f348 for P_, _ in uniq), 'POSITIVE: the stored Kulaichev polynomial f348 is one of the u-factors (exact)')
check(all(pari.subst(P_, 'u', pari('3/4')) != 0 for P_, _ in uniq), 'NEGATIVE: the 3-4-5 rhombus u = 3/4 is a root of no u-factor (exact)')
# real roots in (0, 1): PARI polrootsreal, each root re-isolated in an exact rational interval of width 2e-14 (polsturm = 1),
# then refined by Newton and bracketed by a sign change inside it
from fractions import Fraction
roots = []; nisol = [0]
for P_, org in uniq:
    n01 = int(pari.polsturm(P_, [0, 1]))
    if n01 == 0: continue
    rr = pari.polrootsreal(P_, [0, 1])
    cs = [mp.mpf(Fraction(str(c)).numerator) / Fraction(str(c)).denominator for c in list(pari.Vec(P_))]   # highest degree first
    dcs = [c * (len(cs) - 1 - i) for i, c in enumerate(cs[:-1])]
    f_ = lambda z: mp.polyval(cs, z)
    for r in rr:
        r0 = Fraction(str(r).replace(' ', '')).limit_denominator(10**18)
        lo, hi = r0 - Fraction(1, 10**14), r0 + Fraction(1, 10**14)
        cnt = int(pari.polsturm(P_, [pari(f'{lo.numerator}/{lo.denominator}'), pari(f'{hi.numerator}/{hi.denominator}')]))
        assert cnt == 1, 'isolating interval does not hold exactly one root'
        rv = mp.mpf(r0.numerator) / r0.denominator
        for _ in range(60):                           # Newton from the 1e-14 start; quadratic convergence
            step = f_(rv) / mp.polyval(dcs, rv); rv -= step
            if abs(step) < mp.mpf(10) ** (-(DIG + 15)): break
        dl, dh = rv - mp.mpf(10) ** (-(DIG + 5)), rv + mp.mpf(10) ** (-(DIG + 5))
        assert mp.mpf(lo.numerator) / lo.denominator < dl and dh < mp.mpf(hi.numerator) / hi.denominator and f_(dl) * f_(dh) < 0, \
            'refined root not bracketed inside the exact isolating interval'
        if 0 < rv < 1: roots.append((rv, P_, org))
        nisol[0] += 1
say(f'{len(roots)} real roots in (0, 1) (certified isolation, PARI polrootsreal); u-factor degrees involved',
    sorted({int(pari.poldegree(P_, 'u')) for _, P_, _ in roots}))
# exact u = 0, 1 cases and roots at the ends are not admissible (u in (0, 1) open)
Gpari = pari(str(Gk))
Qexpr = sp.factor(N.Q)
def coeffs_in(F, k, vals):                            # sage poly in (u, t, S): coefficients in variable k at the other values
    deg = max(e[k] for e in F.dict()) if F.dict() else 0
    cs = [mp.mpf(0)] * (deg + 1)
    for e, c in F.dict().items():
        term = mp.mpf(int(c.numerator())) / int(c.denominator())
        for j in range(3):
            if j != k and e[j]: term *= vals[j] ** e[j]
        cs[e[k]] += term
    return cs[::-1]                                   # highest degree first (mpmath order)
def real_roots_in(F, k, vals):                        # real roots of F in variable k, at DIG + 20 digits (mpmath polyroots)
    cs = coeffs_in(F, k, vals)
    while len(cs) > 1 and cs[0] == 0: cs = cs[1:]
    if len(cs) <= 1: return []
    rts = mp.polyroots(cs, maxsteps=400, extraprec=4 * DIG, error=False)
    return [mp.re(z) for z in rts if abs(mp.im(z)) < eps]
def rel(F, vals):                                     # relative value of a sage polynomial at (u, t, S)
    tot = mp.mpf(0); size = mp.mpf(0)
    for (eu, et, es), c in F.dict().items():
        term = mp.mpf(int(c.numerator())) / int(c.denominator()) * vals[0]**eu * vals[1]**et * vals[2]**es
        tot += term; size += abs(term)
    return abs(tot) / size if size else mp.mpf(0)
def yantra_at(uu, tt, Sv):
    P = uu**2 / (1 + uu**2); R = 1 / (1 + uu**2); w3 = uu / (1 + uu**2); w7 = uu / (1 + uu**2)
    Qv = sp.N(Qexpr.subs({N.u: sp.Float(mp.nstr(uu, DIG + 15), DIG + 15), N.v: sp.Float(mp.nstr(uu, DIG + 15), DIG + 15),
                          N.t: sp.Float(mp.nstr(tt, DIG + 15), DIG + 15)}), DIG + 10)
    Qv = mp.mpf(str(Qv))
    b1 = tt**2 / (1 + tt**2)
    return model.solve(P, Qv, R, Sv, w3, w7, sqrt=mp.sqrt, b1=b1), Qv
def bindu(tri):                                       # signed: incentre depth of the bindu minus 1/2 (unsquared (d))
    b, w = tri['b'], tri['w']
    m1 = w[1] / (b[6] - b[1]); h = b[6] - b[5]; hw = m1 * h; c_ = mp.mpf(1) / 2 - b[5]
    L = mp.sqrt(hw**2 + h**2); r = hw * h / (hw + L)        # inradius of the bindu (apex at depth Q = b6, base at b5)
    return r - c_, (h, hw)
def margin_admissible(tri):
    b, w, a = tri['b'], tri['w'], tri['a']
    ms = [('base order b%d < b%d' % (i, i + 1), b[i + 1] - b[i]) for i in range(1, 9)]
    ms += [('w%d > 0' % i, w[i]) for i in range(1, 10)]
    ms += [('apex side t%d' % i, (a[i] - b[i]) if i in model.DOWN else (b[i] - a[i])) for i in range(1, 10)]
    ms += [('t%d corners in disc' % i, -(w[i]**2 + b[i]**2 - b[i])) for i in range(1, 10) if i not in (1, 3, 7, 9)]
    worst = min(ms, key=lambda z: z[1])
    return worst
results = []
for k, (uu, P_, org) in enumerate(roots):
    print(f'PROGRESS {(k + 1) / len(roots):.3f} candidates', flush=True)
    Sroots = real_roots_in(Gk, 2, (uu, 0, 0))
    sols = []
    if org is None:
        # u-only factor: search t from H and D directly at each S
        for Sv in Sroots:
            for hfac, _ in Hf:
                for tt in real_roots_in(hfac, 1, (uu, 0, Sv)):
                    if rel(Dk, (uu, tt, Sv)) < eps: sols.append((tt, Sv))
    else:
        g, a, b = org
        tA = real_roots_in(a, 1, (uu, 0, 0))
        for tt in tA:
            if rel(b, (uu, tt, mp.mpf(0))) >= eps: continue
            for Sv in Sroots:
                if rel(Hk, (uu, tt, Sv)) < eps and rel(Dk, (uu, tt, Sv)) < eps: sols.append((tt, Sv))
    if not sols:
        results.append(dict(u=uu, deg=int(pari.poldegree(P_, 'u')), verdict='no real (t, S) with G = H = D = 0 at this u (complex t or S)')); continue
    for tt, Sv in sols:
        row = dict(u=uu, t=tt, S=Sv, deg=int(pari.poldegree(P_, 'u')), P=P_)
        try:
            tri, Qv = yantra_at(uu, tt, Sv)
        except ZeroDivisionError:
            row['verdict'] = 'model.solve divides by zero (degenerate)'; results.append(row); continue
        res_all = max(abs(val) for nm, val in model.all_conditions(tri))
        cb = abs(tri['w'][1]**2 + tri['b'][1]**2 - tri['b'][1]); cc = abs(tri['w'][9]**2 + tri['b'][9]**2 - tri['b'][9])
        dd, (h, hw) = bindu(tri)
        worst = margin_admissible(tri)
        row.update(Q=Qv, res_all=res_all, b=cb, c=cc, d=dd, worst=worst)
        conds = res_all < eps and cb < eps and cc < eps and abs(dd) < eps
        if not conds:
            row['verdict'] = f'squared-form root only: unsquared (d) misses by {mp.nstr(dd, 6)} (or a condition residual {mp.nstr(max(res_all, cb, cc), 3)})'
        elif tt <= 0:
            row['verdict'] = f'meets (a)(b)(c)(d) but NOT admissible: t = {mp.nstr(tt, 8)} < 0, so w1 = t/(1+t^2) < 0 (by {mp.nstr(abs(tri["w"][1]), 6)})'
            row['worst'] = ('w1 > 0', tri['w'][1])
        elif worst[1] <= 0:
            row['verdict'] = f'meets (a)(b)(c)(d) but NOT admissible: {worst[0]} fails by {mp.nstr(worst[1], 6)}'
        else:
            row['verdict'] = f'ADMISSIBLE yantra with (a)(b)(c)(d); smallest admissibility margin {mp.nstr(worst[1], 6)} ({worst[0]})'
        results.append(row)
print()
print('ALL CANDIDATES (u in (0, 1), every u-factor):')
for r in results:
    print(f"  u = {mp.nstr(r['u'], 25)}  (u-factor degree {r['deg']})" + (f", t = {mp.nstr(r['t'], 15)}, S = {mp.nstr(r['S'], 15)}" if 't' in r else '') + f"\n      -> {r['verdict']}")
adm = [r for r in results if r['verdict'].startswith('ADMISSIBLE')]
genuine = [r for r in results if 'worst' in r and r['res_all'] < eps and r['b'] < eps and r['c'] < eps and abs(r['d']) < eps]
ku = mp.mpf('0.750438516022214024406084657051234510340891003639790315415314')
check(len(adm) == 1, f'exactly one admissible yantra with (a)(b)(c)(d) among all {len(results)} candidates')
check(len(adm) == 1 and abs(adm[0]['u'] - ku) < mp.mpf(10) ** -58, 'POSITIVE: it is Kulaichev\'s yantra (u agrees with the stored 60 digits)')
check(len(adm) == 1 and pari.poldegree(adm[0].get('P', f348), 'u') == 348, 'its u-factor has degree 348')
check(len(genuine) > len(adm), f'NEGATIVE: without the admissibility test {len(genuine)} real solutions of (a)(b)(c)(d) remain (the test does real work)')
if adm:
    k0 = adm[0]
    tri, _ = yantra_at(k0['u'] * (1 + mp.mpf('1e-12')), k0['t'], k0['S'])
    pert = max(abs(val) for nm, val in model.all_conditions(tri))
    check(pert > eps or abs(bindu(tri)[0]) > eps or abs(tri['w'][9]**2 + tri['b'][9]**2 - tri['b'][9]) > eps,
          'NEGATIVE: the perturbed Kulaichev point (u + 1e-12 u) fails the condition test')
# margins summary
nonadm = [r for r in results if r not in adm]
mins = [abs(r['worst'][1]) for r in nonadm if 'worst' in r and r['worst'][1] <= 0]
mind = [abs(r['d']) for r in nonadm if 'd' in r and not (r['res_all'] < eps and r['b'] < eps and r['c'] < eps and abs(r['d']) < eps)]
say('smallest failing admissibility margin', mp.nstr(min(mins), 5) if mins else '-', '; smallest unsquared-(d) miss', mp.nstr(min(mind), 5) if mind else '-',
    f'; working precision {DIG} digits, decision threshold 1e-{EPSD}')
check(all(m > mp.mpf(10) ** (-MARD) for m in mins + mind), f'every rejection margin exceeds 1e-{MARD} (far above the 1e-{EPSD} threshold)')
say(f'time {time.time() - T0:.0f} s')
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, c in checks.items() if not c))
