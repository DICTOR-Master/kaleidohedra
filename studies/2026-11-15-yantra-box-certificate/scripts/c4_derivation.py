"""Step 2 of the Lean plan: the data that ties the stored polynomials to the geometry.  Writes data/lean-deriv.json, read by
c5_deriv_lean.py, which writes the Lean files.

1. The construction table.  Quantities V_0..V_24 in the base point (u, t, S) of studies/2026-11-15-yantra-uniqueness: the bases
   u, t, S, then each quantity by a relation V_i * d_i = n_i (d_i, n_i expressions in earlier quantities), exactly the lines of
   s1_system.py with the leg slopes named (k7 = k3 = u).  For each step: the reduced fraction (N_i, D_i) and the cancelled
   factor K_i, with D_i K_i = A_i and N_i K_i = B_i for the unreduced fraction A_i / B_i of n_i / d_i (Frac.step_inv).
2. The three equations: (c) Gr = w9^2 + S^2 - S, marma (1,4,6) E146 = k1 (Q - b4) - k6 (b4 - b2), (d) squared
   Dq = (1 - 2 b5)^2 ((Q - b1)^2 + w1^2) - w1^2 (2Q - 1)^2.  The numerator of each (unreduced, as the kernel computes it) is
   c * F * prod g_j^m_j with F the system polynomial (G, H1, D of inputs/system-K.txt); each g_j has a witness: an expression
   that is nonzero at every admissible yantra whose numerator is g_j * h_j.
3. The pull-back of G, H1, D to (u, tau, rho) (t = u tau, S = (1 + rho (1 - u) u^2) / (1 + u^2)): substH(F) = c * F~ * prod of
   factors positive on the open box, F~ the stored main-chart polynomial.
4. The 36 admissibility tests as expressions; for each, substH(Num) = alpha N G E1 and substH(Den) = beta D G E2 with (N, D) the
   stored main-chart pair, G the common factor, E1, E2 products of factors positive on the open box (E1 may hold even powers).
5. The charts: F~ o map = alpha p^k q^m F_c for the used equations, and N o map = alpha' N_c E_N, D o map = beta' D_c E_D for the
   used tests, with F_c, N_c, D_c the stored chart polynomials (unrescaled).
Usage: c4_derivation.py   FINAL ok iff every identity and factorisation holds exactly."""
import json, os, sys, time
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(HERE, *p)
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
R3 = PolynomialRing(QQ, 'u,t,S'); U, T, S = R3.gens()
ok = True
# ---------------- expressions ----------------
class E:
    def __init__(s, op, *a): s.op, s.a = op, a
    def __add__(s, o): return E('add', s, E.c(o))
    def __radd__(s, o): return E('add', E.c(o), s)
    def __sub__(s, o): return E('sub', s, E.c(o))
    def __rsub__(s, o): return E('sub', E.c(o), s)
    def __mul__(s, o): return E('mul', s, E.c(o))
    def __rmul__(s, o): return E('mul', E.c(o), s)
    @staticmethod
    def c(o): return o if isinstance(o, E) else E('c', int(o))
def v(i): return E('v', i)
def lean(e):
    if e.op == 'v': return f'(.v {e.a[0]})'
    if e.op == 'c': return f'(.c ({e.a[0]}))'
    return f'(.{e.op} {lean(e.a[0])} {lean(e.a[1])})'
def maxidx(e):
    if e.op == 'v': return e.a[0]
    if e.op == 'c': return -1
    return max(maxidx(e.a[0]), maxidx(e.a[1]))
TAB = []   # (N, D) reduced, polynomials in R3
def frac(e):
    """the kernel's unreduced fraction"""
    if e.op == 'v': return TAB[e.a[0]]
    if e.op == 'c': return (R3(e.a[0]), R3(1))
    (a, b), (c, d) = frac(e.a[0]), frac(e.a[1])
    if e.op == 'add': return (a + c, b) if b == d else (a * d + c * b, b * d)
    if e.op == 'sub': return (a - c, b) if b == d else (a * d - c * b, b * d)
    return (a * c, b * d)
u, t, Sv = v(0), v(1), v(2)
NAMES = ['u', 't', 'S']; TAB += [(U, R3(1)), (T, R3(1)), (S, R3(1))]
STEPS = []
def step(name, d, n):
    d, n = E.c(d), E.c(n)
    i = len(TAB); assert maxidx(d) < i and maxidx(n) < i, name
    (Nd, Dd), (Nn, Dn) = frac(d), frac(n)
    A, B = Nd * Dn, Nn * Dd
    g = A.gcd(B)
    Dq, Nq = A // g, B // g
    # normalise the sign so that the leading coefficient of Dq is positive
    if Dq.lc() < 0: Dq, Nq, g = -Dq, -Nq, -g
    assert Dq * g == A and Nq * g == B
    TAB.append((Nq, Dq)); NAMES.append(name)
    STEPS.append({'i': i, 'name': name, 'd': lean(d), 'n': lean(n), 'K': g})
    return v(i)
R = step('R', 1 + u * u, 1); P = step('P', 1 + u * u, u * u); w7 = step('w7', 1 + u * u, u)
b1 = step('b1', 1 + t * t, t * t); w1 = step('w1', 1 + t * t, t)
k2 = step('k2', Sv - P, u * P); k9 = step('k9', R - P, k2 * (Sv - R)); w9 = step('w9', 1, k9 * (Sv - P))
k8 = step('k8', R - b1, u * (1 - R))
c138 = w1 * (R - b1) - u * (1 - R) * (P - b1)
Q = step('Q', c138, w1 * P * (R - b1) - u * (1 - R) * b1 * (P - b1))
k1 = step('k1', Q - b1, w1); b8 = step('b8', u + k9, u + k9 * P); k4 = step('k4', b8 - Q, k9 * (Q - P))
w6 = step('w6', 1, k2 * (Sv - Q)); b2 = step('b2', k1 + u, k1 * Q); b4 = step('b4', k4 + k8, k4 * b8 + k8 * b1)
k6 = step('k6', Q - b2, w6); b5 = step('b5', k1 + k9, k1 * Q + k9 * P); w5 = step('w5', 1, k6 * (b5 - b2))
w2 = step('w2', 1, k2 * (Sv - b2)); w4 = step('w4', 1, k4 * (b8 - b4)); w8 = step('w8', 1, k8 * (b8 - b1))
h1 = step('h1', 1, k1 * (Q - b4)); h2 = step('h2', 1, k6 * (b4 - b2))   # helpers: keep the (1,4,6) fraction small
say('table:', [(NAMES[i], len(N.monomials()), len(D.monomials())) for i, (N, D) in enumerate(TAB)])
NT = len(TAB)
# ---------------- nonzero witnesses ----------------
WIT = {  # name -> expression nonzero at every admissible yantra (the Lean proof of nonvanishing is in Deriv.lean)
 'u': u, 't': t, '1+u2': 1 + u * u, '1+t2': 1 + t * t, 'S-P': Sv - P, 'R-P': R - P, 'R-b1': R - b1, 'c138': c138,
 'Q-b1': Q - b1, 'u+k9': u + k9, 'b8-Q': b8 - Q, 'k1+u': k1 + u, 'k4+k8': k4 + k8, 'Q-b2': Q - b2, 'k1+k9': k1 + k9,
 'P-b1': P - b1, 'S-R': Sv - R, '1-S': 1 - Sv, 'Q-P': Q - P, 'R-Q': R - Q, 'b2-b1': b2 - b1, 'b4-b2': b4 - b2,
 'b5-b2': b5 - b2, 'b8-b4': b8 - b4, 'b8-b1': b8 - b1, 'S-Q': Sv - Q, 'k1': k1, 'k9': k9, 'k2': k2, 'k8': k8, 'k4': k4,
 'k6': k6, 'w1': w1, 'w6': w6, 'S': Sv, 'R': R, 'P': P, 'b1': b1, 'Q': Q, 'b2-u2': b2, 'S-b2': Sv - b2}
WN = {k: frac(e)[0] for k, e in WIT.items()}
def witness(g):
    for k, Nw in WN.items():
        if Nw != 0 and Nw % g == 0: return k, Nw // g
    return None
# ---------------- the three equations ----------------
src = {}
for line in open(D_('inputs', 'system-K.txt')):
    if ' = ' in line: k, e = line.split(' = ', 1); src[k.strip()] = R3(e.strip().replace('^', '**'))
FINALS = {'G': w9 * w9 + Sv * Sv - Sv, 'H1': h1 - h2,
          'D': (1 - 2 * b5) * (1 - 2 * b5) * ((Q - b1) * (Q - b1) + w1 * w1) - w1 * w1 * (2 * Q - 1) * (2 * Q - 1)}
FIN = {}
for k, e in FINALS.items():
    Num = frac(e)[0]; F = src[k]
    qq = Num // F; assert qq * F == Num, k
    fl = qq.factor(); c = fl.unit(); facs = []
    for g, m in fl:
        w = witness(g)
        if w is None: ok = False; say('NO WITNESS for factor', g, 'of', k); continue
        facs.append({'g': g, 'm': int(m), 'w': w[0], 'h': w[1]})
    FIN[k] = {'e': lean(e), 'c': c, 'facs': facs, 'F': F}
    say(f'final {k}: numerator {len(Num.monomials())} terms = {c} * {k} * {[(str(f["g"])[:30], f["m"], f["w"]) for f in facs]}')
# ---------------- pull-back to (u, tau, rho) ----------------
Rm = PolynomialRing(QQ, 'u,tau,rho'); um, tm, rm = Rm.gens()
main = json.load(open(D_('data', 'polys-utr.json')))
def decm(p, gens): return sum(QQ(c) * gens[0]**e[0] * gens[1]**e[1] * gens[2]**e[2] for e, c in p)
Snum = 1 + rm * (1 - um) * um**2; Sden = 1 + um**2
def substH(f, d):
    return sum(QQ(c) * um**a * (um * tm)**b * Snum**e * Sden**(d - e) for (a, b, e), c in f.dict().items())
POSF = {'u': um, '1-u': 1 - um, '1+u': 1 + um, 'tau': tm, '1-tau': 1 - tm, 'rho': rm, '1+u2': 1 + um**2}
def posfactors(q, strict):
    """q (polynomial in Rm) as c * prod f^m with f positive on the open box; returns (c, list) or None"""
    fl = q.factor(); c = fl.unit(); out = []
    for g, m in fl:
        nm = next((k for k, f in POSF.items() if f == g), None)
        if nm is None and -g in POSF.values(): nm = next(k for k, f in POSF.items() if f == -g); c *= (-1)**m
        if nm is not None: out.append({'g': POSF[nm], 'm': int(m), 'kind': nm}); continue
        if g.degree() > 0 and all(cc > 0 for cc in g.coefficients()): out.append({'g': g, 'm': int(m), 'kind': 'pos'}); continue
        if g.degree() > 0 and all(cc < 0 for cc in g.coefficients()): out.append({'g': -g, 'm': int(m), 'kind': 'pos'}); c *= (-1)**m; continue
        if strict and m % 2 == 0: out.append({'g': g, 'm': int(m), 'kind': 'even'}); continue
        return None
    return c, out
PULL = {}
for k in ('G', 'H1', 'D'):
    F = src[k]; d = F.degree(S); Fm = decm(main['F'][k], (um, tm, rm))
    q = substH(F, d) / Fm
    assert q.denominator() == 1, k
    pf = posfactors(Rm(q.numerator()) * (1 if q.denominator() == 1 else 1), False)
    if pf is None: ok = False; say('pull-back factor not positive for', k); continue
    PULL[k] = {'d': int(d), 'c': pf[0], 'facs': pf[1], 'Fm': Fm}
    say(f'pull-back {k}: c = {pf[0]}, factors {[(f["kind"], f["m"]) for f in pf[1]]}')
# ---------------- the 36 tests ----------------
Bv = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: Sv}
Av = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: Sv, 3: E.c(1), 7: E.c(0)}
Wv = {1: w1, 2: w2, 3: w7, 4: w4, 5: w5, 6: w6, 7: w7, 8: w8, 9: w9}
TESTS = {}
for i in range(1, 9): TESTS[f'b{i} < b{i + 1}'] = Bv[i + 1] - Bv[i]
for i in range(1, 10): TESTS[f'w{i} > 0'] = Wv[i]
for i in range(1, 10): TESTS[f'apex t{i}'] = (Av[i] - Bv[i]) if i <= 5 else (Bv[i] - Av[i])
for i in (2, 4, 5, 6, 8, 9): TESTS[f'corner t{i} in disc'] = Bv[i] * (1 - Bv[i]) - Wv[i] * Wv[i]
TESTS['b9 < 1'] = 1 - Sv; TESTS['b3 < b6'] = Q - P; TESTS['b5 < 1/2'] = 1 - 2 * b5; TESTS['Q > 1/2'] = 2 * Q - 1
assert list(TESTS) == list(main['tests']), (list(TESTS), list(main['tests']))
TD = {}
for k, e in TESTS.items():
    strict = 'in disc' not in k
    Num, Den = frac(e)
    d = max(Num.degree(S), Den.degree(S), 0)
    Nm = decm(main['tests'][k]['N'], (um, tm, rm)); Dm = decm(main['tests'][k]['D'], (um, tm, rm))
    sN, sD = substH(Num, d), substH(Den, d)
    # sN / sD = (alpha/beta) (E1/E2) N / D ; find G = gcd(sN / N, sD / D) after removing N, D
    if sN == 0: ok = False; say('test numerator vanishes', k); continue
    qn, rn = sN.quo_rem(Nm); qd, rd = sD.quo_rem(Dm)
    if rn != 0 or rd != 0: ok = False; say('test', k, 'N or D does not divide'); continue
    G = qn.gcd(qd); e1 = qn // G; e2 = qd // G
    p1 = posfactors(e1, strict); p2 = posfactors(e2, False)
    if p1 is None or p2 is None: ok = False; say('test', k, 'cofactor not positive:', str(e1.factor())[:200], '|', str(e2.factor())[:200]); continue
    if p1[0] * p2[0] < 0: ok = False; say('test', k, 'negative constant'); continue
    say(f'test {k}: num {len(Num.monomials())} den {len(Den.monomials())} G {len(G.monomials())}')
    TD[k] = {'e': lean(e), 'd': int(d), 'G': G, 'a': p1[0], 'E1': p1[1], 'b': p2[0], 'E2': p2[1], 'N': Nm, 'D': Dm, 'strict': strict}
say('tests: all', len(TD), 'of', len(TESTS), 'factorised')
# ---------------- charts ----------------
Rc = PolynomialRing(QQ, 'p,q,r'); p, q, r = Rc.gens()
CH = {'A': (1 - p, 1 - p * q, r), 'B': (1 - p * q, 1 - p, r), 'C1': (p, p**4 * q, r), 'C2': (p * q, p**4, r),
      'W': (p, p**4 * (1 + p**4 * (q - 4)), 1 + p + p**2 * (r - 4)),
      'Wt+': (p * q, (p * q)**4 * (1 + 4 * p**4), 1 + p * q + 4 * p**2 * (r - 1)),
      'Wt-': (p * q, (p * q)**4 * (1 - 4 * p**4), 1 + p * q + 4 * p**2 * (r - 1)),
      'Wr+': (p * q, (p * q)**4 * (1 + 4 * p**4 * (r - 1)), 1 + p * q + 4 * p**2),
      'Wr-': (p * q, (p * q)**4 * (1 + 4 * p**4 * (r - 1)), 1 + p * q - 4 * p**2)}
PPOS = {'p': p, 'q': q, 'r': r}
def parfactors(x, strict):
    fl = x.factor(); c = fl.unit(); out = []
    for g, m in fl:
        nm = next((k for k, f in PPOS.items() if f == g), None)
        if nm: out.append({'g': g, 'm': int(m), 'kind': nm}); continue
        if g.degree() > 0 and all(cc > 0 for cc in g.coefficients()) and g.constant_coefficient() > 0:
            out.append({'g': g, 'm': int(m), 'kind': 'pos'}); continue
        if g.degree() > 0 and all(cc < 0 for cc in g.coefficients()) and g.constant_coefficient() < 0:
            out.append({'g': -g, 'm': int(m), 'kind': 'pos'}); c *= (-1)**m; continue
        if m % 2 == 0: out.append({'g': g, 'm': int(m), 'kind': 'even'}); continue
        return None
    return c, out
CHD = {}
for ch, mp in CH.items():
    cert = json.load(open(D_('data', f'bnb-{ch}.json'))); cd = json.load(open(D_('data', f'polys-utr-{ch}.json')))
    usedF = [k for k in cd['F'] if any(l[6] == 'F' and l[7] == k for l in cert['leaves'])]
    usedT = [k for k in cd['tests'] if any(l[6] == 'T' and l[7] == k for l in cert['leaves'])]
    out = {'map': mp, 'F': {}, 'T': {}}
    for k in usedF:
        Fc = decm(cd['F'][k], (p, q, r)); comp = Rc(PULL[k]['Fm'](*mp))
        x = comp / Fc; assert x.denominator() == 1
        pf = parfactors(Rc(x.numerator()), False)
        if pf is None or any(f['kind'] in ('r', 'even') for f in pf[1]): ok = False; say(ch, k, 'chart factor', x.factor()); continue
        out['F'][k] = {'c': pf[0], 'facs': pf[1], 'Fc': Fc}
    for k in usedT:
        Nc = decm(cd['tests'][k]['N'], (p, q, r)); Dc = decm(cd['tests'][k]['D'], (p, q, r))
        xn = Rc(TD[k]['N'](*mp)) / Nc; xd = Rc(TD[k]['D'](*mp)) / Dc
        assert xn.denominator() == 1 and xd.denominator() == 1, (ch, k)
        pn = parfactors(Rc(xn.numerator()), True); pd = parfactors(Rc(xd.numerator()), True)
        if pn is None or pd is None: ok = False; say(ch, k, 'test factors', xn.factor(), '|', xd.factor()); continue
        if not TD[k]['strict'] and any(f['kind'] in ('even', 'r') for f in pn[1]): ok = False; say(ch, k, 'closed test with vanishing factor'); continue
        out['T'][k] = {'a': pn[0], 'EN': pn[1], 'b': pd[0], 'ED': pd[1], 'Nc': Nc, 'Dc': Dc}
    CHD[ch] = out
    say(f'chart {ch}: F {[(k, [(f["kind"], f["m"]) for f in v["facs"]]) for k, v in out["F"].items()]}; '
        f'T {[(k, [(f["kind"], f["m"]) for f in v["EN"]], [(f["kind"], f["m"]) for f in v["ED"]]) for k, v in out["T"].items()]}')
# ---------------- write ----------------
def enc(f):
    f = f if f.parent() in (R3, Rm, Rc) else f
    return [[list(map(int, e)), str(ZZ(c)) if QQ(c).denominator() == 1 else str(c)] for e, c in f.dict().items()]
def encf(lst): return [{'g': enc(x['g']), 'm': x['m'], 'kind': x.get('kind', ''), **({'w': x['w'], 'h': enc(x['h'])} if 'w' in x else {})} for x in lst]
J = {'names': NAMES, 'table': [{'N': enc(N), 'D': enc(D)} for N, D in TAB],
     'steps': [{**s_, 'K': enc(s_['K'])} for s_ in STEPS],
     'wit': {k: lean(e) for k, e in WIT.items()},
     'finals': {k: {'e': v_['e'], 'c': str(v_['c']), 'facs': encf(v_['facs']), 'F': enc(v_['F'])} for k, v_ in FIN.items()},
     'pull': {k: {'d': v_['d'], 'c': str(v_['c']), 'facs': encf(v_['facs']), 'Fm': enc(v_['Fm'])} for k, v_ in PULL.items()},
     'tests': {k: {'e': v_['e'], 'd': v_['d'], 'G': enc(v_['G']), 'a': str(v_['a']), 'E1': encf(v_['E1']), 'b': str(v_['b']),
                   'E2': encf(v_['E2']), 'N': enc(v_['N']), 'D': enc(v_['D']), 'strict': v_['strict']} for k, v_ in TD.items()},
     'charts': {ch: {'map': [enc(Rc(x)) for x in v_['map']],
                     'F': {k: {'c': str(w['c']), 'facs': encf(w['facs']), 'Fc': enc(w['Fc'])} for k, w in v_['F'].items()},
                     'T': {k: {'a': str(w['a']), 'EN': encf(w['EN']), 'b': str(w['b']), 'ED': encf(w['ED']), 'Nc': enc(w['Nc']),
                               'Dc': enc(w['Dc'])} for k, w in v_['T'].items()}} for ch, v_ in CHD.items()}}
json.dump(J, open(D_('data', 'lean-deriv.json'), 'w'))
say('wrote data/lean-deriv.json')
print('FINAL ok' if ok else 'FINAL FAIL')
