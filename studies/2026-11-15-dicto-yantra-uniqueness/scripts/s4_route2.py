"""Step 4 (DICTO Yantra): the independent census, meant for the second compute machine.  Different elimination order, different
elimination method, different root isolator, different interval library from steps 1-3:
  elimination over K = Q(sqrt5), t FIRST, by evaluation and interpolation (direct Res_t(H1, D) over K[u, S] did not finish within the
     5-minute pilot in Singular over K, in Singular over Q[s], in PARI with polmod coefficients or in FLINT, so the eliminant is built from
     values): for integers u0, R3(u0, S) = Res_t(H1(u0), D(u0)) in K[S] (PARI), then E2(u0) = Res_S(R3(u0, S), G(u0, S)) in K.  A point is
     used only if the t-degrees of H1, D, the S-degree of G and the S-degree of R3(u0, S) all equal their generic values, so every value
     is the specialisation of the same formal resultants E2(u) = Res_S(Res_t(H1, D), G).  The u-degree of E2 is at most
     2 deg_u R3 + deg_S R3 deg_u G with deg_u R3 <= deg_t D deg_u H1 + deg_t H1 deg_u D (Sylvester bounds), so that many points plus one
     fix E2 exactly (Lagrange interpolation, PARI); extra points are checked as well.  E2 is factored over K (nffactor); K-factors that
     are lemma factors (data/nz-factors.txt) are dropped; the norms of the rest are factored over Q: the route-2 candidates;
  isolation: every POSITIVE real root of every candidate by exact Sturm bisection (PARI polsturm on dyadic intervals of [0, 2^kb], 2^kb an
     exact Cauchy bound computed here with PARI rationals), refined by exact sign evaluation to width about 2^-900;
  back-solving: mpmath interval arithmetic (iv, outward rounding), not Arb, with sqrt5 = iv.sqrt(5): S from G by the quadratic formula
     (R < S < 1); t by a 1-D branch and bound with the interval Newton test on (0, v), v = c/u, for H1(t); then D at each root; a
     survivor gets the Krawczyk test in (u, t, S) and the admissibility rebuild, in iv.
Input: data/polys-D.json (G, H1, D from step 1, which match #103 up to NZ factors).  FINAL ok iff no candidate is undecided, exactly one
admissible solution is found, it lies in Theorem 9's isolating interval, and the three other real solutions of the system that step 3
found (u = 0.57120, 0.67176, 0.88628; not admissible) are found again (a control that route 2 sees every real solution, not only the
yantra)."""
import json, os, sys, time
sys.set_int_max_str_digits(0)
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = lambda *p: os.path.join(ROOT, *p)
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
from sage.rings.number_field.number_field import QuadraticField
K = QuadraticField(5, 's'); s = K.gen()
RK = PolynomialRing(K, 'u,t,S'); uu, tt, SS = RK.gens()
polys = json.load(open(D('data', 'polys-D.json')))
def from_json(L): return sum((ZZ(int(c[0])) + ZZ(int(c[1])) * s) * uu**e[0] * tt**e[1] * SS**e[2] for e, c in L)
G, H1, Dn = (from_json(polys[k]) for k in ('G', 'H1', 'D'))
NZK = set()
for line in open(D('data', 'nz-factors.txt')):
    if not line.startswith('K '): continue
    f = RK(eval(line[2:].split('#')[0].strip().replace('^', '**'), {'s': s, 'u': uu, 't': tt, 'S': SS})); NZK.add(f / f.lc())
def isnz(f): f = RK(f); return f.degree() > 0 and (f / f.lc()) in NZK
import cypari2
pari = cypari2.Pari(); pari.allocatemem(int(os.environ.get('PARIMEM', 6 * 10**9)))
pari('[u, S, t, s]')                                     # s lowest priority (polmod modulus variable)
MS = pari('Mod(s, s^2 - 5)'); nf = pari.nfinit(pari('s^2 - 5'))
def toP(f): return pari.subst(pari(str(f)), 's', MS)
Gp, Hp, Dp = toP(G), toP(H1), toP(Dn)
dt = (H1.degree(tt), Dn.degree(tt)); du = (H1.degree(uu), Dn.degree(uu), G.degree(uu)); dS = (H1.degree(SS), Dn.degree(SS), G.degree(SS))
R3u = dt[1] * du[0] + dt[0] * du[1]                      # Sylvester bound on deg_u Res_t(H1, D)
say(f'degrees: t {dt}, u (H1, D, G) {du}, S (H1, D, G) {dS}; deg_u R3 <= {R3u}')
def value(u0):
    """E2(u0) in K and the S-degree of R3(u0, S), or None if a degree drops at u0."""
    h = pari.subst(Hp, 'u', u0); d = pari.subst(Dp, 'u', u0); g = pari.subst(Gp, 'u', u0)
    if pari.poldegree(h, 't') != dt[0] or pari.poldegree(d, 't') != dt[1] or pari.poldegree(g, 'S') != dS[2]: return None
    r = pari.polresultant(h, d, 't')
    return pari.polresultant(r, g, 'S'), int(pari.poldegree(r, 'S'))
print('PROGRESS 0.02 E2 by evaluation (pilot of the first points)')
t1 = time.time(); probe = [value(pari(k)) for k in range(1, 6)]
dR3S = max(p_[1] for p_ in probe if p_)
NPT = 2 * R3u + dR3S * du[2] + 1; EXTRA = 8
say(f'deg_S R3 = {dR3S} (generic, from the probes); deg_u E2 <= {NPT - 1}; {NPT} points + {EXTRA} checks; {(time.time() - t1) / 5:.2f} s per point')
X, Y = [], []; k = 0; skipped = []
while len(X) < NPT + EXTRA:
    k += 1; vk = value(pari(k))
    if vk is None or vk[1] != dR3S: skipped.append(k); continue
    X.append(k); Y.append(vk[0])
    if len(X) % 50 == 0: print(f'PROGRESS {0.02 + 0.33 * len(X) / (NPT + EXTRA):.3f} point {len(X)}/{NPT + EXTRA}')
say(f'{len(X)} values (skipped u0 = {skipped}) in {time.time() - t1:.1f} s')
print('PROGRESS 0.36 interpolation')
t1 = time.time()
Ya = [pari.polcoef(pari.lift(y), 0, 's') for y in Y]; Yb = [pari.polcoef(pari.lift(y), 1, 's') for y in Y]
xs = pari(X[:NPT]); Ea = pari.polinterpolate(xs, pari(Ya[:NPT]), 'u'); Eb = pari.polinterpolate(xs, pari(Yb[:NPT]), 'u')
E2 = Ea + pari('s') * Eb
chk = all(pari.subst(Ea, 'u', X[i]) == Ya[i] and pari.subst(Eb, 'u', X[i]) == Yb[i] for i in range(NPT, len(X)))
say(f'E2 interpolated: degree {int(pari.poldegree(E2, "u"))} ({time.time() - t1:.1f} s); the {len(X) - NPT} extra points agree: {chk}')
assert chk and E2 != 0
open(D('data', 'route2-E2.txt'), 'w').write(str(E2) + '\n')
cands = []
print('PROGRESS 0.45 factor E2 over K')
t1 = time.time(); Fz = pari.nffactor(nf, E2); say(f'nffactor: {time.time() - t1:.1f} s')
with open(D('data', 'route2-E2-factors.txt'), 'w') as fh:
    for k_ in range(len(Fz[0])):
        g = Fz[0][k_]; gs = RK(str(pari.liftall(g))); nz = isnz(gs); deg = int(pari.poldegree(g, 'u'))
        fh.write(f'{int(Fz[1][k_])} {"NZ" if nz else "KEEP"} {pari.liftall(g)}\n')
        say(f'   E2 K-factor degree {deg}^{int(Fz[1][k_])}', 'NZ' if nz else 'KEEP', str(pari.liftall(g)) if deg <= 2 else '')
        if nz: continue
        Fq = pari.factor(pari.polresultant(pari.liftall(g), pari('s^2 - 5'), 's'))
        for kk in range(len(Fq[0])):
            q = Fq[0][kk]
            if pari.poldegree(q, 'u') > 0 and not any(q == q2 or q == -q2 for q2 in cands): cands.append(q)
f160 = pari(open(D('inputs', 'f160-u.txt')).read().strip())
has160 = any(pari.poldegree(g, 'u') == 160 and pari.pollead(f160, 'u') * g == pari.pollead(g, 'u') * f160 for g in cands)
say('route 2 candidate rational factor degrees:', [int(pari.poldegree(g, 'u')) for g in cands], '; f160 among them:', has160)
with open(D('data', 'route2-candidates.txt'), 'w') as fh:
    for g in cands: fh.write(f'# degree {pari.poldegree(g, "u")}\n{g}\n')
# ---------------- isolation by exact Sturm bisection on the half-line ----------------
print('PROGRESS 0.55 isolation')
KB = 900
def sturm(g, a, b): return int(pari.polsturm(g, pari(f'[{a}, {b}]')))
def isolate(g):
    cs = pari.Vec(g); lead = cs[0]
    bound = 1 + max(abs(cs[i] / lead) for i in range(1, len(cs)))     # Cauchy bound
    kb = 0
    while pari(2) ** kb < bound: kb += 1
    hi0 = pari(2) ** kb
    out = []; stack = [(pari(0), hi0)]
    if pari.subst(g, 'u', 0) == 0: raise ValueError('root at 0')
    while stack:
        a, b = stack.pop(); n = sturm(g, a, b)
        if n == 0: continue
        if n == 1: out.append((a, b)); continue
        m = (a + b) / 2
        if pari.subst(g, 'u', m) == 0: raise ValueError('rational root')
        stack += [(a, m), (m, b)]
    approx = pari.polrootsreal(g, pari(f'[0, {hi0}]'), precision=3400)
    res = []
    for a, b in out:
        r = [x for x in approx if a < x < b]; assert len(r) == 1
        lo = pari.floor(r[0] * pari(2) ** KB) - 2; hi = lo + 5
        lo, hi = pari.max(lo / pari(2) ** KB, a), pari.min(hi / pari(2) ** KB, b)
        assert pari.sign(pari.subst(g, 'u', lo)) * pari.sign(pari.subst(g, 'u', hi)) < 0
        res.append((lo, hi))
    return sorted(res, key=lambda ab: float(ab[0])), kb
roots = []
for gi, g in enumerate(cands):
    r, kb = isolate(g); say(f'   factor {gi} (degree {int(pari.poldegree(g, "u"))}): {len(r)} positive real roots (Sturm on [0, 2^{kb}])')
    roots += [(gi, ri, a, b) for ri, (a, b) in enumerate(r)]
# ---------------- back-solving in mpmath interval arithmetic ----------------
import mpmath
from mpmath import iv, mp
iv.prec = 1200; mp.prec = 1200
SQ5 = iv.sqrt(iv.mpf(5)); CC = 2 * SQ5 - 4
P_ = {k: [(tuple(e), int(c[0]) + int(c[1]) * SQ5 if int(c[1]) else iv.mpf(int(c[0]))) for e, c in polys[k]] for k in ('G', 'H1', 'D')}
def coeffs_in(p, var, x):
    deg = max(e[var] for e, c in p); out = [iv.mpf(0)] * (deg + 1)
    for e, c in p:
        term = c
        for i in range(3):
            if i != var and e[i]: term = term * x[i] ** e[i]
        out[e[var]] += term
    return out
def horner(cs, x):
    acc = iv.mpf(0)
    for c in reversed(cs): acc = acc * x + c
    return acc
def ev(p, x): return horner(coeffs_in(p, 1, x), x[1])
def has0(I): return I.a <= 0 <= I.b
def frac_iv(a):
    n, d = int(pari.numerator(a)), int(pari.denominator(a))
    return iv.mpf(n) / iv.mpf(d)
def iv_hull(a, b): return iv.mpf([a.a, b.b])
def roots_1d(cs, lo, hi, minw=mpmath.mpf(2) ** -1000):
    """certified real roots of the interval polynomial cs in (lo, hi): intervals each holding exactly one root (interval Newton), or None."""
    dcs = [cs[i] * i for i in range(1, len(cs))]
    out = []
    if has0(horner(cs, lo)) or has0(horner(cs, hi)): return None
    stack = [iv_hull(lo, hi)]
    while stack:
        I = stack.pop()
        if not has0(horner(cs, I)): continue
        dI = horner(dcs, I)
        if not has0(dI):
            m = iv.mpf(I.mid); N = m - horner(cs, m) / dI
            if N.a > I.a and N.b < I.b:
                for _ in range(60):
                    m = iv.mpf(N.mid); N2 = m - horner(cs, m) / horner(dcs, N)
                    N2 = iv.mpf([max(N.a, N2.a), min(N.b, N2.b)])
                    if N2.delta >= N.delta / 2: N = N2; break
                    N = N2
                out.append(N); continue
            if N.b < I.a or N.a > I.b: continue
        if I.delta < minw: return None
        m = I.mid; stack += [iv.mpf([I.a, m]), iv.mpf([m, I.b])]
    return out
def construct(u, t, S):
    v = CC / u; one = iv.mpf(1)
    P = v**2 / (1 + v**2); R = one / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
    b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
    xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
    k3 = w3 / (1 - P); xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
    b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: iv.mpf(0)}
    w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q), 8: xZ * (b8 - b1) / (R - b1), 9: w9}
    return b, w, a
def lt(x, y): return x.b < y.a
def admissible(u, t, S):
    b, w, a = construct(u, t, S); fails, und = [], []
    def need(T, F, lab): (None if T else (fails if F else und).append(lab))
    for i in range(1, 9): need(lt(b[i], b[i + 1]), b[i].a >= b[i + 1].b, f'b{i} < b{i + 1}')
    zero, half = iv.mpf(0), iv.mpf(1) / 2
    for i in range(1, 10): need(lt(zero, w[i]), w[i].b <= 0, f'w{i} > 0')
    for i in range(1, 10):
        if i <= 5: need(lt(b[i], a[i]), a[i].b <= b[i].a, f'apex t{i}')
        else: need(lt(a[i], b[i]), a[i].a >= b[i].b, f'apex t{i}')
    for i in (2, 4, 5, 6, 8):
        p = w[i]**2 + b[i]**2 - b[i]; need(p.b < 0, p.a >= 0, f'corner t{i} inside the disc')
    need(lt(b[5], half), b[5].a >= half.b, 'b5 < 1/2'); need(lt(half, b[6]), b[6].b <= half.a, 'Q > 1/2')
    return fails, und
def deriv(p, var): return [(tuple(e[i] - (i == var) for i in range(3)), c * e[var]) for e, c in p if e[var] > 0]
def evfull(p, x):
    tot = iv.mpf(0)
    for e, c in p: tot += c * x[0] ** e[0] * x[1] ** e[1] * x[2] ** e[2]
    return tot
def krawczyk(x0, rad):
    F = [P_['G'], P_['H1'], P_['D']]; J = [[deriv(f, j) for j in range(3)] for f in F]
    mids = [mpmath.mpf(c.mid) for c in x0]; X = [iv.mpf([m - rad, m + rad]) for m in mids]; y = [iv.mpf(m) for m in mids]
    Jm = mp.matrix([[mpmath.mpf(evfull(J[i][j], y).mid) for j in range(3)] for i in range(3)]); Y = Jm ** -1
    Fy = [evfull(f, y) for f in F]; JX = [[evfull(J[i][j], X) for j in range(3)] for i in range(3)]
    Kk = []
    for i in range(3):
        ki = y[i] - sum(iv.mpf(Y[i, j]) * Fy[j] for j in range(3))
        for j in range(3):
            mij = (iv.mpf(1) if i == j else iv.mpf(0)) - sum(iv.mpf(Y[i, l]) * JX[l][j] for l in range(3))
            ki += mij * (X[j] - y[j])
        Kk.append(ki)
    return all(Kk[i].a > X[i].a and Kk[i].b < X[i].b for i in range(3)), Kk
undec = 0; survivors = []; nr = len(roots)
for n_, (gi, ri, a, b) in enumerate(roots):
    U = iv.mpf([frac_iv(a).a, frac_iv(b).b])
    Gc = coeffs_in(P_['G'], 2, (U, None, None)); assert len(Gc) == 3
    disc = Gc[1] ** 2 - 4 * Gc[2] * Gc[0]
    Rr = iv.mpf(1) / (1 + U ** 2)
    tag = f'factor {gi} root {ri} u = {mpmath.nstr(U.mid, 15)}'
    if disc.b < 0: say(tag, ': REJECT no real S'); print(f'PROGRESS {0.6 + 0.35 * (n_ + 1) / nr:.3f} candidate {n_ + 1}/{nr}'); continue
    if has0(disc) or has0(Gc[2]): say(tag, ': UNDECIDED (S)'); undec += 1; continue
    sq = iv.sqrt(disc); Ss = [(-Gc[1] + sq) / (2 * Gc[2]), (-Gc[1] - sq) / (2 * Gc[2])]
    lines = []
    for Sv in Ss:
        if lt(Sv, Rr) or Sv.a >= 1 or Sv.b <= Rr.a: lines.append(f'S = {mpmath.nstr(Sv.mid, 10)} outside (R, 1)'); continue
        if not (lt(Rr, Sv) and Sv.b < 1): lines.append('UNDECIDED S range'); undec += 1; continue
        ts = roots_1d(coeffs_in(P_['H1'], 1, (U, None, Sv)), iv.mpf(0), CC / U)
        if ts is None: lines.append('UNDECIDED t roots'); undec += 1; continue
        if not ts: lines.append(f'S = {mpmath.nstr(Sv.mid, 10)}: H1 has no root with 0 < t < v'); continue
        for T in ts:
            dv = ev(P_['D'], (U, T, Sv))
            if not has0(dv): lines.append(f'S = {mpmath.nstr(Sv.mid, 10)}, t = {mpmath.nstr(T.mid, 10)}: D = {mpmath.nstr(dv.mid, 4)} != 0'); continue
            lines.append(f'SURVIVOR S = {mpmath.nstr(Sv.mid, 20)}, t = {mpmath.nstr(T.mid, 20)}'); survivors.append((gi, ri, a, b, U, T, Sv))
    say(tag, ':', ' | '.join(lines) if lines else 'REJECT')
    print(f'PROGRESS {0.6 + 0.35 * (n_ + 1) / nr:.3f} candidate {n_ + 1}/{nr}')
st1 = json.load(open(D('inputs', 'stage1-D.json'))); lo40, hi40 = [pari(x) for x in st1['interval40']]
adm = []; others = set()
for gi, ri, a, b, U, T, Sv in survivors:
    okk, Kb = krawczyk((U, T, Sv), mpmath.mpf(10) ** -250)
    f, und = admissible(*Kb) if okk else (['krawczyk'], [])
    in9 = b > lo40 and a < hi40
    say(f'survivor factor {gi} root {ri} u = {mpmath.nstr(U.mid, 12)}: Krawczyk {okk}; admissibility fails {f}, undecided {und}; Theorem 9 interval: {in9}')
    for k_, ref in enumerate((0.571195314832402, 0.671758400623299, 0.886279995315526)):
        if okk and abs(float(U.mid) - ref) < 1e-9 and f: others.add(k_)
    if okk and not f and not und: adm.append(in9)
    if und: undec += 1
say('route 2: undecided', undec, '; admissible solutions', len(adm), '; the three non-admissible solutions of step 3 found again:', sorted(others))
ok = has160 and undec == 0 and adm == [True] and others == {0, 1, 2}
print('FINAL ok' if ok else 'FINAL FAIL: see above')
