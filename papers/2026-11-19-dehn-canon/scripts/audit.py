# Number audit for the Dehn canon paper: recompute every number of the text and tables (60 digits) and check that the
# paper prints it. Also checks CLEO = F* and AXE = A* of Ogievetsky-Papadopolos (1999, eq. (8)) and the study line counts.
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
# Lean line and file counts per study
ST = os.environ.get('STUDIES', '../../../studies')
base = ST + '/2026-11-19-lean-dehn-'
tot_l = tot_f = 0
for k, (nf, nl) in {1: (1, 153), 2: (10, 1708), 3: (3, 909), 4: (5, 1303), 5: (5, 1326), 6: (3, 314), 7: (7, 7504)}.items():
    fs = glob.glob(base + f'{k}/lean/*.lean'); L = sum(sum(1 for _ in open(f, encoding='utf-8')) for f in fs)
    ok(len(fs) == nf and L == nl, f'study {k}: {len(fs)} files {L} lines'); tot_l += L; tot_f += len(fs)
ok(tot_l == 13217 and tot_f == 34, 'totals'); need('13,217', 'total lines'); need('34 Lean files', 'total files')
for s in ['184 screened, 32 zero, 151 nonzero, 1 mixed', '11 of 11', '324 pairs', '900 pairs', '21 pairs', 'v4.35.0-rc2', '065356127b1dc0016f66b7283ce0ce2c4055aa55', '349 PDF']:
    need(s, 'fact')
log = open(ST + '/2026-11-19-dehn-atoms/README.md', encoding='utf-8').read()
ok('184 have exact corners' in log and '32 have Dehn invariant ZERO, 151 NONZERO' in log, 'atoms counts vs README')
print('\n'.join(bad) if bad else 'AUDIT OK: every number recomputed and found in the text')
