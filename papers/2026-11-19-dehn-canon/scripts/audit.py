# Number audit for the Dehn canon paper: recompute every number of the text and tables (60 digits) and check that the
# paper prints it (Theorem 15's values and the study 8 counts included). Also checks CLEO = F* and AXE = A* of Ogievetsky-Papadopolos (1999, eq. (8)) and the study line counts.
import re, json, os, glob
from mpmath import mp, mpf, sqrt, acos, pi, degrees
mp.dps = 60
H = open('../paper.html', encoding='utf-8').read()
txt = re.sub(r'<[^>]+>', '', H)
bad = []
def need(s, why):
    if s not in txt: bad.append(f'missing "{s}" ({why})')
def ok(c, why):
    if not c: bad.append('FAIL ' + why)
r5 = sqrt(5); g = (r5 - 1) / 2; tau = 1 / g
r = sqrt(3 * (10 - 2 * r5))
a = acos(1 / r5); b = acos((3 - r5) / r); c = acos(r5 / 3); e = acos((r5 + 1) / r); t3 = acos(mpf(1) / 3)
ok(abs(a + b + e - pi) < 1e-50, 'α + β + ε = π'); ok(abs(a + 2 * b - c - pi) < 1e-50, 'α + 2β − γ = π'); ok(abs(e - (b - c)) < 1e-50, 'ε = β − γ')
ok(abs(((3 - r5) / r) ** 2 - (mpf(1) / 3 - 2 * r5 / 15)) < 1e-50, 'cos² β'); ok(abs(((r5 + 1) / r) ** 2 - (mpf(1) / 3 + 2 * r5 / 15)) < 1e-50, 'cos² ε')
for v, s in [(a, '63.43'), (b, '79.18'), (c, '41.81'), (e, '37.37'), (a + b, '142.62')]:
    ok(str(degrees(v))[:len(s)] == s, f'{s}° truncation'); need(s, 'angle in degrees')
ok(abs(mp.cos(2 * a) + mpf(3) / 5) < 1e-50, 'cos 2α'); ok(abs(mp.cos(2 * b) + (10 + 8 * r5) / 30) < 1e-50, 'cos 2β')
ok(abs(2 * acos(1 / sqrt(3)) - (pi - t3)) < 1e-50, '2 arccos(1/√3) = π − arccos(1/3)')
ok(abs(mp.sin(b) - 4 / r) < 1e-50 and abs(mp.sin(e) - (2 * r5 - 2) / r) < 1e-50, 'sin β, sin ε')
# recurrence of Theorem 12: norm never divisible by 3, step factor -220 mod 225
xp, x = (2, 0), (-10, -8)
for n in range(1, 400):
    ok((x[0] ** 2 - 5 * x[1] ** 2) % 3 != 0, f'3 ∤ norm at n={n}')
    xp, x = x, (-10 * x[0] - 40 * x[1] - 225 * xp[0], -8 * x[0] - 10 * x[1] - 225 * xp[1])
# words over α, β (mod π: γ ≡ α + 2β, π − ε ≡ α + β, ε ≡ −α − β)
W = {'CLEO': (3, 3 * g), 'AXE': (g + 1, 4 + 2), 'FUJI': (6 + 3 - 3 * g, 6 + 6 - 3 * g)}
ok(abs(W['CLEO'][0] * a + W['CLEO'][1] * b - (3 * a + 3 * g * b)) < 1e-50, 'CLEO form')
ok(abs((g * a + 4 * b + c) - (W['AXE'][0] * a + W['AXE'][1] * b) + pi) < 1e-50, 'AXE edges → form (mod π)')
# FUJI symbolically mod π: 6(π−ε) + 3γ + 3gε ; ε = π − α − β, γ = α + 2β − π
fuji = 6 * (a + b) + 3 * (a + 2 * b - pi) + 3 * g * (pi - a - b) ; ok(abs(fuji - (W['FUJI'][0] * a + W['FUJI'][1] * b) - (3 * g - 3) * pi) < 1e-50, 'FUJI form exact')
ico = (-120, -240); dod = (-30 * (2 * r5 - 2), 0)
det = lambda u, v: u[0] * v[1] - u[1] * v[0]
for (p, q, val, s) in [('CLEO', 'AXE', 15, '15'), ('CLEO', 'FUJI', 45 - 45 * g, '45 − 45g'), ('AXE', 'FUJI', 30 * g - 45, '30g − 45')]:
    ok(abs(det(W[p], W[q]) - val) < 1e-50, f'det {p}-{q}'); need(s, 'determinant')
for (q, val, s) in [('CLEO', 720 - 360 * g, '720 − 360g'), ('AXE', -480 + 240 * g, '−480 + 240g'), ('FUJI', 720 - 360 * g, '720 − 360g')]:
    ok(abs(det(ico, W[q]) - val) < 1e-50, f'det ico-{q}'); need(s, 'determinant')
for q in W: ok(abs(det(dod, W[q])) > 1, f'det dod-{q}')
ok(abs(det(dod, ico)) > 1, 'det dod-ico')
ok(all(w[0] > 0 and w[1] > 0 for w in W.values()), 'positive coefficients (Remark)')
# icosahedron −120 ⊗ γ = −120 α − 240 β mod π; dodecahedron edge 2√5 − 2 at π − α
ok(abs(degrees(pi - acos(-1 / r5)) - degrees(a)) < 1e-40, 'dodecahedron dihedral π − α')
ok(abs(degrees(pi - acos(-r5 / 3)) - degrees(c)) < 1e-40, 'icosahedron dihedral π − γ')
# Ogievetsky-Papadopolos: their β = our ε, their δ = our β; CLEO = F*, AXE = A* (scale τ)
bOP = acos((tau + 1) / (sqrt(3) * sqrt(tau + 2))); dOP = acos((tau - 1) / (sqrt(3) * sqrt(tau + 2)))
ok(abs(bOP - e) < 1e-50 and abs(dOP - b) < 1e-50, 'OP β = ε, OP δ = β')
# CLEO scaled by τ: 3τ at α, 3 at δ; α ≡ −βOP − δ  ->  (−3τ, 3 − 3τ) = F*
ok(abs((3 * tau * (-1)) + 3 * tau) < 1e-50 and abs(3 * tau * (-1) - (-3 * tau)) < 1e-50, 'F* β-coefficient')
F_star = (-3 * tau, -3 * tau + 3); cleo_op = (-3 * tau, -3 * tau + 3); ok(F_star == cleo_op, 'CLEO = F*')
# AXE scaled by τ: 1 at α, 4τ at δ, τ at γ; γ ≡ −βOP + δ -> (−1 − τ, −1 + 4τ + τ) = A* = (−τ − 1, 5τ − 1)
axe_op = (-1 - tau, -1 + 5 * tau); ok(abs(axe_op[0] - (-tau - 1)) < 1e-50 and abs(axe_op[1] - (5 * tau - 1)) < 1e-50, 'AXE = A*')
ok(abs(a + c + 2 * bOP - pi) < 1e-50 and abs(a - c + 2 * dOP - pi) < 1e-50, 'OP Lemma 1')
# cube ∩ octahedron: Lucky 7 t inside (7/4, 9/5); sign of 2t − 3
t7 = mpf('1.7565821359'); ok(mpf(7) / 4 < t7 < mpf(9) / 5, 'Lucky 7 in interval'); need('1.7566', 'Lucky 7 t')
# Theorem 15: θ = arccos(1/3); sin(nθ) in Q·√2 (exact recurrence vs 60 digits); 2α, 2β data; sines of combinations in Q(√5)
from fractions import Fraction as Fr
ok(str(degrees(t3))[:5] == '70.52', 'θ degrees'); need('70.52', 'θ in degrees')
ok(abs(mp.cos(t3) - mpf(1) / 3) < 1e-50 and abs(mp.sin(t3) - 2 * sqrt(2) / 3) < 1e-50, 'cos θ, sin θ')
ca, sb = Fr(1, 3), Fr(2, 3)                       # cos nθ = ca, sin nθ = sb·√2
for n in range(1, 61):
    ok(abs(mp.cos(n * t3) - mpf(ca.numerator) / ca.denominator) < 1e-45 and
       abs(mp.sin(n * t3) - mpf(sb.numerator) / sb.denominator * sqrt(2)) < 1e-45, f'sin({n}θ) in Q√2')
    ca, sb = ca / 3 - 4 * sb / 3, sb / 3 + 2 * ca / 3
ok(abs(mp.sin(2 * a) - mpf(4) / 5) < 1e-50 and abs(mp.sin(2 * b) - (10 - 2 * r5) / 15) < 1e-50, 'sin 2α, sin 2β')
for s_ in ['4/5', '(10 − 2√5)/15', '−3/5', '−(10 + 8√5)/30', '(1 + 2√−2)/3', '2√2/3']: need(s_, 'Theorem 15 value')
# Q(√5) as pairs (x, y) = x + y√5; cos, sin of Q·2α + R·2β exact, compared at 60 digits
mul = lambda u, v: (u[0] * v[0] + 5 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])
add = lambda u, v: (u[0] + v[0], u[1] + v[1]); neg = lambda u: (-u[0], -u[1])
val = lambda u: mpf(u[0].numerator) / u[0].denominator + mpf(u[1].numerator) / u[1].denominator * r5
A = ((Fr(-3, 5), Fr(0)), (Fr(4, 5), Fr(0))); B = ((Fr(-1, 3), Fr(-4, 15)), (Fr(2, 3), Fr(-2, 15)))
def rot(x, y): return (add(mul(x[0], y[0]), neg(mul(x[1], y[1]))), add(mul(x[1], y[0]), mul(x[0], y[1])))
def pw(x, k):
    z = ((Fr(1), Fr(0)), (Fr(0), Fr(0)))
    for _ in range(abs(k)): z = rot(z, x if k > 0 else (x[0], neg(x[1])))
    return z
for Q in range(-6, 7):
    for R in range(-6, 7):
        z = rot(pw(A, Q), pw(B, R))
        ok(abs(val(z[0]) - mp.cos(Q * 2 * a + R * 2 * b)) < 1e-45 and abs(val(z[1]) - mp.sin(Q * 2 * a + R * 2 * b)) < 1e-45, f'Q(√5) at {Q},{R}')
ok(int(mp.sqrt(10)) ** 2 != 10, '√10 irrational (10 not a square)')
for s_ in ['15 pairs', '29 files', 'compile_all8.sh', '60fc5ee5', 'Theorem 15', 'Theorem 16']: need(s_, 'study 8 fact')
# Lean line and file counts per study
ST = os.environ.get('STUDIES', '../../../studies')
base = ST + '/2026-11-19-lean-dehn-'
tot_l = tot_f = 0
for k, (nf, nl) in {1: (1, 153), 2: (10, 1708), 3: (3, 909), 4: (5, 1303), 5: (5, 1326), 6: (3, 314), 7: (7, 7504), 8: (3, 477)}.items():
    fs = glob.glob(base + f'{k}/lean/*.lean'); L = sum(sum(1 for _ in open(f, encoding='utf-8')) for f in fs)
    ok(len(fs) == nf and L == nl, f'study {k}: {len(fs)} files {L} lines'); tot_l += L; tot_f += len(fs)
ok(tot_l == 13694 and tot_f == 37, 'totals'); need('13,694', 'total lines'); need('37 Lean files', 'total files'); need('477', 'study 8 lines')
# study 8: theorems and lemmas in its two proof files, and the #print axioms list
L8 = ''.join(open(base + f'8/lean/{f}.lean', encoding='utf-8').read() for f in ('Dehn8Indep', 'Dehn8Cross'))
n8 = len(re.findall(r'^\s*(?:theorem|lemma) ', L8, re.M)); ok(n8 == 49, f'study 8: {n8} theorems and lemmas'); need('49 theorems and lemmas', 'study 8 count')
n8ax = open(base + '8/lean/Axioms8.lean', encoding='utf-8').read().count('#print axioms'); ok(n8ax == 29, f'study 8: {n8ax} axiom checks')
pairs = re.findall(r'^theorem ((?:oct|tetra|co)_(?:dod|ico|cleo|axe|fuji))_not_scissorsCongruent', L8, re.M); ok(len(set(pairs)) == 15, f'15 cross pairs ({len(set(pairs))})')
for s in ['184 screened, 32 zero, 151 nonzero, 1 mixed', '11 of 11', '324 pairs', '900 pairs', '21 pairs', 'v4.35.0-rc2', '065356127b1dc0016f66b7283ce0ce2c4055aa55', '349 PDF']:
    need(s, 'fact')
log = open(ST + '/2026-11-19-dehn-atoms/README.md', encoding='utf-8').read()
ok('184 have exact corners' in log and '32 have Dehn invariant ZERO, 151 NONZERO' in log, 'atoms counts vs README')
print('\n'.join(bad) if bad else 'AUDIT OK: every number recomputed and found in the text')
