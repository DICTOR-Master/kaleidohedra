"""Step 2: certified isolation of every POSITIVE real root of each candidate factor (data/polys-D.json, from s1_system.py: the rational
factors of the norms of the kept K-factors of E(u)), by three independent methods, which must agree.  Unlike the Kulaichev census, u is
not confined to (0, 1) here (b3 < b7 only says u v < 1, true for every u since u v = 2/phi^3), so the whole half-line u > 0 is covered:
an exact Cauchy bound 1 + max|a_i/a_n| <= 2^k bounds every root, and the census runs on f(2^k x), x in (0, 1).  u = 2^k x keeps the
intervals dyadic.  Methods:
  (V) Vincent-Collins-Akritas bisection (Descartes' rule of signs on Moebius-transformed polynomials), pure Python integers,
      written here; each output interval (a, b) with a, b dyadic holds exactly one root (one sign variation);
  (P) PARI/GP polsturm (exact Sturm counts) on the same dyadic grid, and polrootsreal for the root count in (0, 1);
  (F) FLINT/Arb (python-flint fmpz_poly.complex_roots): certified complex root enclosures; the real roots in (0, 1) are those whose
      enclosures meet the real axis and no other enclosure's conjugate (so the root is its own conjugate).
Then each root is refined to a dyadic interval of width about 2^-1400 (seeded by FLINT, certified by exact endpoint signs inside the VCA interval) and written to
data/roots-D.json.  FINAL ok iff the three methods give the same number of positive roots for every factor, every FLINT enclosure
lies in exactly one VCA interval and vice versa, PARI's Sturm count is 1 on each VCA interval and 0 on each gap, and the positive
control holds: Theorem 9's isolating interval (audit stage 1, case D) contains exactly one of the f160 roots.  Negative control: the
perturbed polynomial f160 + a0/10^10 (a0 = its constant term) must NOT have a root in that interval (or the census would not separate them)."""
import json, os, sys, time
sys.set_int_max_str_digits(0)                          # scaled coefficients exceed the default 4300-digit limit
from fractions import Fraction
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = lambda *p: os.path.join(ROOT, *p)
polys = json.load(open(D('data', 'polys-D.json')))
cands = [(c['origin'], c['is_f160'], [int(x) for x in c['coeffs']]) for c in polys['candidates']]   # coeffs: constant term first

def taylor_shift1(a):                                   # a(x) -> a(x + 1), coefficients low to high
    a = a[:]; n = len(a)
    for i in range(n):
        for j in range(n - 2, i - 1, -1): a[j] += a[j + 1]
    return a
def variations(a):
    s = [x for x in a if x]; return sum(1 for i in range(1, len(s)) if (s[i] > 0) != (s[i - 1] > 0))
def vca01(f):
    """roots of f in (0, 1) as dyadic intervals (num/2^k, (num+1)/2^k) with exactly one root, plus exact dyadic roots."""
    out, exact = [], []
    # work with g(x) = f on [c/2^k, (c+1)/2^k] via g_k,c(x) = 2^(k n) f((c + x)/2^k); start k = 0, c = 0
    stack = [(0, 0, f[:])]
    while stack:
        k, c, g = stack.pop()
        # roots of g in (0,1): transform x -> 1/(1+y) : y^n g(1/(1+y)) has coefficients reversed then shifted
        if g[0] == 0: pass
        r = taylor_shift1(g[::-1]); var = variations(r)
        if var == 0: continue
        if var == 1: out.append((k, c)); continue
        # bisect: left half h(x) = 2^n g(x/2), right half h(x) = 2^n g((x+1)/2)
        n = len(g) - 1
        left = [g[i] * (1 << (n - i)) for i in range(n + 1)]
        right = taylor_shift1(left)
        if right[0] == 0: exact.append((k + 1, 2 * c + 1)); right = right  # midpoint is a root (handled: never for irreducible deg > 1)
        stack.append((k + 1, 2 * c, left)); stack.append((k + 1, 2 * c + 1, right))
    return sorted(out, key=lambda kc: Fraction(kc[1], 1 << kc[0])), exact
def sign_at(f, p, k):                                   # exact sign of f(p / 2^k)
    n = len(f) - 1
    # f(p/2^k) * 2^(k n) = sum f_i p^i 2^(k (n - i)); Horner in p with powers of 2^k
    acc = f[n]
    for i in range(n - 1, -1, -1): acc = acc * p + f[i] * (1 << (k * (n - i)))
    return (acc > 0) - (acc < 0)
def refine(f, k, c, bits):
    a, b = c, c + 1                                     # interval (a/2^k, b/2^k)
    sa, sb = sign_at(f, a, k), sign_at(f, b, k)
    assert sa * sb < 0, 'endpoint signs do not differ'
    while k < bits:
        a, b, k = 2 * a, 2 * b, k + 1; m = a + 1
        sm = sign_at(f, m, k); assert sm != 0
        if sm == sa: a = m
        else: b = m
    return k, a
import cypari2
pari = cypari2.Pari(); pari.allocatemem(4 * 10**9)
import flint
flint.ctx.prec = 2000
ok = True; census = []
st1 = json.load(open(D('inputs', 'stage1-D.json'))); lo40, hi40 = [Fraction(x) for x in st1['interval40']]
for idx, (origin, is348, f0) in enumerate(cands):
    n = len(f0) - 1
    # exact Cauchy bound: every complex root has |u| < 1 + max|a_i/a_n| <= 2^kb
    kb = 0
    while (1 << kb) < 1 + max(abs(Fraction(a, f0[-1])) for a in f0[:-1]): kb += 1
    f = [a << (kb * i) for i, a in enumerate(f0)]          # f(x) = f0(2^kb x): roots u in (0, 2^kb) <-> x in (0, 1)
    say(f'factor {idx}: degree {n} ({origin}{", f160" if is348 else ""}); Cauchy bound 2^{kb}')
    assert f0[0] != 0, 'u = 0 is a root'
    V, exact = vca01(f); assert not exact
    say(f'   VCA: {len(V)} roots in (0, 2^{kb})')
    # PARI
    pf = pari('Pol(' + str(f[::-1]) + ', x)')
    sturm01 = int(pari.polsturm(pf, pari('[0, 1]')))
    nreal = len(pari.polrootsreal(pari('Pol(' + str(f0[::-1]) + ', x)'), pari('[0, +oo]')))   # unscaled, whole half-line
    pv = [int(pari.polsturm(pf, pari(f'[{c}/2^{k}, {c + 1}/2^{k}]'))) for k, c in V]
    gaps = []
    for (k1, c1), (k2, c2) in zip(V, V[1:]):
        gaps.append(int(pari.polsturm(pf, pari(f'[{c1 + 1}/2^{k1}, {c2}/2^{k2}]'))))
    if V:
        gaps.append(int(pari.polsturm(pf, pari(f'[0, {V[0][1]}/2^{V[0][0]}]')))); gaps.append(int(pari.polsturm(pf, pari(f'[{V[-1][1] + 1}/2^{V[-1][0]}, 1]'))))
    p_ok = sturm01 == len(V) == nreal and all(x == 1 for x in pv) and all(x == 0 for x in gaps)
    say(f'   PARI: polsturm on [0,1] (scaled) = {sturm01}, polrootsreal on [0,+oo] (unscaled) = {nreal}; Sturm 1 on every VCA interval: {all(x == 1 for x in pv)}; 0 on gaps: {all(x == 0 for x in gaps)}')
    # FLINT
    roots = [r for r, m in flint.fmpz_poly(f0).complex_roots()]       # unscaled: roots u themselves
    assert len(roots) == n
    real01 = []
    for i, r in enumerate(roots):
        if not r.imag.contains(0): continue
        conj = flint.acb(r.real, -r.imag)
        if any(j != i and conj.overlaps(roots[j]) for j in range(n)): ok = False; say('   FLINT: ambiguous enclosure', r); continue
        x = r.real
        if x < 0: continue                               # arb comparisons are certified: True only if true for the whole ball
        if not (x > 0): ok = False; say('   FLINT: enclosure meets 0', x); continue
        real01.append(x / (1 << kb))                     # to the scaled coordinate x = u / 2^kb
    match = len(real01) == len(V) and all(sum(1 for (k, c) in V if flint.arb(flint.fmpq(c, 1 << k)) < x and x < flint.arb(flint.fmpq(c + 1, 1 << k))) == 1 for x in real01)
    say(f'   FLINT: {len(real01)} positive real roots; each in exactly one VCA interval: {match}')
    ok = ok and p_ok and match
    # refinement: seed from the FLINT enclosure, then certify by exact signs at the two dyadic endpoints (inside the VCA interval,
    # which holds exactly one root, a sign change pins the root between them)
    refined = []
    K = 1400
    for k, c in V:
        x = [x for x in real01 if flint.arb(flint.fmpq(c, 1 << k)) < x and x < flint.arb(flint.fmpq(c + 1, 1 << k))][0]
        lo = (x.lower() * (1 << K)).floor().unique_fmpz(); hi = (x.upper() * (1 << K)).ceil().unique_fmpz()
        lo, hi = int(lo) - 1, int(hi) + 1
        lo = max(lo, c << (K - k)); hi = min(hi, (c + 1) << (K - k))
        assert sign_at(f, lo, K) * sign_at(f, hi, K) < 0, 'refined endpoints do not bracket the root'
        refined.append([K - kb, str(lo), str(hi)])         # u in [lo / 2^(K - kb), hi / 2^(K - kb)]
    census.append({'index': idx, 'origin': origin, 'is_f160': is348, 'degree': n, 'coeffs': [str(x) for x in f0], 'cauchy_log2': kb,
                   'roots01': refined, 'roots01_vca_coarse': [[k, str(c)] for k, c in V]})
    if is348:
        inside = [i for i, (k, a, b) in enumerate(refined) if Fraction(int(a), 1 << k) < hi40 and Fraction(int(b), 1 << k) > lo40]
        ctl = len(inside) == 1 and sign_at(f, 0, 0) != 0
        say(f'   positive control: Theorem 9 interval meets exactly one root (index {inside}): {len(inside) == 1}')
        fneg = f0[:]; fneg[0] += abs(f0[0]) // 10**10 # constant term moved by 1e-10 of itself (f160's coefficients have ~200 digits, so + 1 moves no root out of a 1e-40 interval)
        q = pari('Pol(' + str(fneg[::-1]) + ', x)')
        neg = int(pari.polsturm(q, pari(f'[{lo40.numerator}/{lo40.denominator}, {hi40.numerator}/{hi40.denominator}]')))
        say(f'   negative control: f160 + a0/10^10 has {neg} roots in that interval (expected 0)')
        ok = ok and ctl and neg == 0
        census[-1]['theorem9_root_index'] = inside[0] if inside else None
    print(f'PROGRESS {(idx + 1) / len(cands):.2f} factor {idx} isolated')
json.dump(census, open(D('data', 'roots-D.json'), 'w'))
say('total candidate u values (u > 0):', sum(len(c['roots01']) for c in census))
print('FINAL ok' if ok else 'FINAL FAIL: the three isolations disagree or a control failed')
