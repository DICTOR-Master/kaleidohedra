"""Step 4: the independent census (second route), meant for the second compute machine.  Different elimination order, different
root isolator, different interval library from steps 1-3:
  elimination: R3 = Res_t(H1, D) first (Singular), NZ factors dropped (same lemma, data/nz-factors.txt), then E2 = Res_S(R3_k, G)
     for every kept factor R3_k (PARI), factored (PARI);
  isolation: every real root in (0, 1) of every kept factor of E2 by exact Sturm bisection (PARI polsturm on dyadic intervals),
     refined by exact sign evaluation (PARI, rational arithmetic) to width 2^-900;
  back-solving: mpmath interval arithmetic (iv, outward rounding), not Arb: S from G by the quadratic formula (R < S < 1);
     t by a 1-D branch and bound with the interval Newton test on (0, u) for H1(t) (each root certified unique in its interval);
     then D at each root; a survivor gets the Krawczyk test in (u, t, S) and the admissibility rebuild, in iv.
Input: data/polys-K.json (G, H1, D from step 1, which match #103 up to NZ factors).  FINAL ok iff no candidate is undecided,
exactly one admissible solution is found, it lies in Theorem 10's isolating interval, and step 3's other real solution of the system
(u = 0.66866, not admissible) is found again (a control that the second route sees every real solution, not only the yantra)."""
import json, os, sys, time
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = lambda *p: os.path.join(ROOT, *p)
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
Rg = PolynomialRing(QQ, 'u,t,S'); uu, tt, SS = Rg.gens()
polys = json.load(open(D('data', 'polys-K.json')))
def from_json(L): return sum(ZZ(int(c)) * uu**e[0] * tt**e[1] * SS**e[2] for e, c in L)
G, H1, Dn = (from_json(polys[k]) for k in ('G', 'H1', 'D'))
NZ = set()
for line in open(D('data', 'nz-factors.txt')):
    f = Rg(line.split('#')[0].strip().replace('^', '**')); NZ.add(f / f.lc())
print('PROGRESS 0.02 Res_t(H1, D)')
t1 = time.time(); R3 = H1.resultant(Dn, tt); say(f'R3 = Res_t(H1, D): degrees (u, S) = ({R3.degree(uu)}, {R3.degree(SS)}), {time.time() - t1:.1f} s')
assert R3 != 0
print('PROGRESS 0.30 factor R3')
t1 = time.time(); fl = R3.factor(); say(f'factored in {time.time() - t1:.1f} s')
keep = []
for f, m in fl:
    if f.degree() == 0: continue
    nz = (f / f.lc()) in NZ
    say(f'   R3 factor degrees (u, S) = ({f.degree(uu)}, {f.degree(SS)})^{m}', 'NZ' if nz else 'KEEP', str(f) if len(str(f)) < 50 else '')
    if not nz: keep.append(f)
open(D('data', 'route2-R3-factors.txt'), 'w').write(''.join(f'{m} {"NZ" if (f / f.lc()) in NZ else "KEEP"} {f}\n' for f, m in fl if f.degree() > 0))
import cypari2
pari = cypari2.Pari(); pari.allocatemem(6 * 10**9)
cands = []
print('PROGRESS 0.45 Res_S(R3_k, G)')
for f in keep:
    if f.degree(SS) == 0:
        cands.append(pari(str(f))); continue
    E2 = pari.polresultant(pari(str(f)), pari(str(G)), 'S'); assert E2 != 0
    Fz = pari.factor(E2)
    for k in range(len(Fz[0])):
        g = Fz[0][k]; gs = Rg(str(g)); nz = (gs / gs.lc()) in NZ
        say(f'   E2 factor degree {int(pari.poldegree(g, "u"))}^{int(Fz[1][k])}', 'NZ' if nz else 'KEEP', str(g) if pari.poldegree(g, 'u') <= 2 else '')
        if not nz: cands.append(g)
f348 = pari(open(D('inputs', 'kulaichev-minpoly-u.txt')).read().strip().replace('x', 'u'))
has348 = any(pari.poldegree(g, 'u') == 348 and pari.pollead(f348, 'u') * g == pari.pollead(g, 'u') * f348 for g in cands)
say('route 2 candidate factor degrees:', [int(pari.poldegree(g, 'u')) for g in cands], '; f348 among them:', has348)
with open(D('data', 'route2-candidates.txt'), 'w') as fh:
    for g in cands: fh.write(f'# degree {pari.poldegree(g, "u")}\n{g}\n')
# ---------------- isolation by exact Sturm bisection ----------------
print('PROGRESS 0.55 isolation')
KB = 900
def sturm(g, a, b): return int(pari.polsturm(g, pari(f'[{a}, {b}]')))
def isolate(g):
    out = []; stack = [(pari(0), pari(1))]
    if pari.subst(g, 'u', 0) == 0 or pari.subst(g, 'u', 1) == 0: raise ValueError('root at 0 or 1')
    while stack:
        a, b = stack.pop(); n = sturm(g, a, b)
        if n == 0: continue
        if n == 1: out.append((a, b)); continue
        m = (a + b) / 2
        if pari.subst(g, 'u', m) == 0: raise ValueError('rational root')
        stack += [(a, m), (m, b)]
    # refinement: PARI polrootsreal at 1000 digits seeds a dyadic interval of width ~2^-KB inside each Sturm interval;
    # two exact sign evaluations at its ends certify it (the Sturm interval holds exactly one root)
    approx = pari.polrootsreal(g, pari('[0, 1]'), precision=3400)
    res = []
    for a, b in out:
        r = [x for x in approx if a < x < b]; assert len(r) == 1
        lo = pari.floor(r[0] * pari(2) ** KB) - 2; hi = lo + 5
        lo, hi = pari.max(lo / pari(2) ** KB, a), pari.min(hi / pari(2) ** KB, b)
        assert pari.sign(pari.subst(g, 'u', lo)) * pari.sign(pari.subst(g, 'u', hi)) < 0
        res.append((lo, hi))
    return sorted(res, key=lambda ab: float(ab[0]))
roots = []
for gi, g in enumerate(cands):
    r = isolate(g); say(f'   factor {gi} (degree {int(pari.poldegree(g, "u"))}): {len(r)} real roots in (0, 1) (Sturm)')
    roots += [(gi, ri, a, b) for ri, (a, b) in enumerate(r)]
# ---------------- back-solving in mpmath interval arithmetic ----------------
import mpmath
from mpmath import iv, mp
iv.prec = 1200; mp.prec = 1200
P_ = {k: [(tuple(e), int(c)) for e, c in polys[k]] for k in ('G', 'H1', 'D')}
def coeffs_in(p, var, x):
    deg = max(e[var] for e, c in p); out = [iv.mpf(0)] * (deg + 1)
    for e, c in p:
        term = iv.mpf(c)
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
def iv_of(a, b): return iv.mpf([mpmath.mpf(pari.numerator(a).__int__()) / mpmath.mpf(pari.denominator(a).__int__()),
                                 mpmath.mpf(pari.numerator(b).__int__()) / mpmath.mpf(pari.denominator(b).__int__())])
def frac_iv(a):                                            # exact rational -> tiny enclosing interval
    n, d = int(pari.numerator(a)), int(pari.denominator(a))
    return iv.mpf(n) / iv.mpf(d)
def iv_hull(a, b): return iv.mpf([a.a, b.b])
def roots_1d(cs, lo, hi, minw=mpmath.mpf(2) ** -1000):
    """certified real roots of the interval polynomial cs in the open interval (lo, hi): list of intervals, each holding exactly one
    root (interval Newton), or None if undecided."""
    dcs = [cs[i] * i for i in range(1, len(cs))]
    out = []; stack = [iv.mpf([lo.b, hi.a])]   # start strictly inside (lo, hi)
    # the ends themselves: the polynomial must be nonzero at t = lo and t = hi (else undecided)
    if has0(horner(cs, lo)) or has0(horner(cs, hi)): return None
    stack = [iv_hull(lo, hi)]
    while stack:
        I = stack.pop()
        if not has0(horner(cs, I)): continue
        dI = horner(dcs, I)
        if not has0(dI):
            m = iv.mpf(I.mid); N = m - horner(cs, m) / dI
            if N.a > I.a and N.b < I.b:
                for _ in range(60):                      # interval Newton contraction: the root stays inside, width shrinks
                    m = iv.mpf(N.mid); N2 = m - horner(cs, m) / horner(dcs, N)
                    N2 = iv.mpf([max(N.a, N2.a), min(N.b, N2.b)])
                    if N2.delta >= N.delta / 2: N = N2; break
                    N = N2
                out.append(N); continue
            if N.b < I.a or N.a > I.b: continue
        if I.delta < minw: return None
        m = I.mid; stack += [iv.mpf([I.a, m]), iv.mpf([m, I.b])]
    # roots must lie strictly inside (lo, hi): the end values are nonzero, so a root interval meeting an end is impossible
    return out
def construct(u, t, S):
    v = u; one = iv.mpf(1)
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
def lt(x, y): return x.b < y.a                             # certified x < y
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
    K = []
    for i in range(3):
        ki = y[i] - sum(iv.mpf(Y[i, j]) * Fy[j] for j in range(3))
        for j in range(3):
            mij = (iv.mpf(1) if i == j else iv.mpf(0)) - sum(iv.mpf(Y[i, l]) * JX[l][j] for l in range(3))
            ki += mij * (X[j] - y[j])
        K.append(ki)
    return all(K[i].a > X[i].a and K[i].b < X[i].b for i in range(3)), K
undec = 0; survivors = []; nr = len(roots)
for n_, (gi, ri, a, b) in enumerate(roots):
    U = iv.mpf([frac_iv(a).a, frac_iv(b).b])
    Gc = coeffs_in(P_['G'], 2, (U, None, None)); assert len(Gc) == 3
    disc = Gc[1] ** 2 - 4 * Gc[2] * Gc[0]
    Rr = iv.mpf(1) / (1 + U ** 2)
    tag = f'factor {gi} root {ri} u = {mpmath.nstr(U.mid, 15)}'
    if disc.b < 0: say(tag, ': REJECT no real S'); continue
    if has0(disc) or has0(Gc[2]): say(tag, ': UNDECIDED (S)'); undec += 1; continue
    sq = iv.sqrt(disc); Ss = [(-Gc[1] + sq) / (2 * Gc[2]), (-Gc[1] - sq) / (2 * Gc[2])]
    lines = []
    for Sv in Ss:
        if lt(Sv, Rr) or Sv.a >= 1 or Sv.b <= Rr.a: lines.append(f'S = {mpmath.nstr(Sv.mid, 10)} outside (R, 1)'); continue
        if not (lt(Rr, Sv) and Sv.b < 1): lines.append('UNDECIDED S range'); undec += 1; continue
        ts = roots_1d(coeffs_in(P_['H1'], 1, (U, None, Sv)), iv.mpf(0), U)
        if ts is None: lines.append('UNDECIDED t roots'); undec += 1; continue
        if not ts: lines.append(f'S = {mpmath.nstr(Sv.mid, 10)}: H1 has no root with 0 < t < u'); continue
        for T in ts:
            dv = ev(P_['D'], (U, T, Sv))
            if not has0(dv): lines.append(f'S = {mpmath.nstr(Sv.mid, 10)}, t = {mpmath.nstr(T.mid, 10)}: D = {mpmath.nstr(dv.mid, 4)} != 0'); continue
            lines.append(f'SURVIVOR S = {mpmath.nstr(Sv.mid, 20)}, t = {mpmath.nstr(T.mid, 20)}'); survivors.append((gi, ri, a, b, U, T, Sv))
    say(tag, ':', ' | '.join(lines) if lines else 'REJECT')
    print(f'PROGRESS {0.6 + 0.35 * (n_ + 1) / nr:.3f} candidate {n_ + 1}/{nr}')
st1 = json.load(open(D('inputs', 'stage1-K.json'))); lo40, hi40 = [pari(x) for x in st1['interval40']]
adm = []; other = False
for gi, ri, a, b, U, T, Sv in survivors:
    okk, K = krawczyk((U, T, Sv), mpmath.mpf(10) ** -250)
    f, und = admissible(*K) if okk else (['krawczyk'], [])
    in10 = b > lo40 and a < hi40
    say(f'survivor factor {gi} root {ri}: Krawczyk {okk}; admissibility fails {f}, undecided {und}; Theorem 10 interval: {in10}')
    if okk and abs(float(U.mid) - 0.668656315401935) < 1e-9: other = True
    if okk and not f and not und: adm.append(in10)
    if und: undec += 1
say('route 2: undecided', undec, '; admissible solutions', len(adm), '; non-admissible solution at u = 0.66866 found again:', other)
ok = has348 and undec == 0 and adm == [True] and other
print('FINAL ok' if ok else 'FINAL FAIL: see above')
