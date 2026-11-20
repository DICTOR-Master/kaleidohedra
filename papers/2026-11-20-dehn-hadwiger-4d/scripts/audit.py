# DICTO · dictospheres.com — number audit of the paper "The Dehn–Hadwiger invariant in four dimensions".
# Recomputes every number of the text and tables in exact arithmetic (exact4d.py: rationals and Q(√5)), checks that each
# appears in paper.html as printed, checks the Lean names against the statement file, the axiom log and the source files,
# the Lean line counts of Table 2, the study logs the paper relies on, the figure asserts, the references, and the house
# text rules (one AI credit line; no model names, host names, home paths, element words or banned phrases).
# Usage: STUDIES=<studies folder> python3 audit.py   -> PASS/FAIL lines and "AUDIT OK" (exit 1 on any FAIL)
import os, re, sys, json, math, html as _h
from fractions import Fraction as Fr
import exact4d as X
from exact4d import Q5, PHI, R5

HERE = os.path.dirname(os.path.abspath(__file__)); PAPER = os.path.join(HERE, '..', 'paper.html')
ST = os.environ.get('STUDIES', os.path.join(HERE, '..', '..', '..', 'studies'))
raw = open(PAPER, encoding='utf-8').read()
text = _h.unescape(re.sub(r'<[^>]+>', '', raw)); flat = re.sub(r'\s+', ' ', text)
FAILS = []


def ok(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + (' ' + str(info) if info else ''), flush=True)
    if not cond: FAILS.append(name)


def has(s, name=None): ok(name or f'text has "{s}"', s in flat)


# ---------------- Table 1: the six polytopes -----------------------------------------------------------------------------
P = X.six()
COUNTS = {'120-cell': (600, 1200, 720, 120), '600-cell': (120, 720, 1200, 600), 'tesseract': (16, 32, 24, 8),
          '5-cell': (5, 10, 10, 5), '16-cell': (8, 24, 32, 16), '24-cell': (24, 96, 96, 24)}
COS = {'120-cell': (Q5(Fr(-1, 4), Fr(-1, 4)), '−(1 + √5)/4', '144° = 4π/5', Fr(4, 5)),
       '600-cell': (Q5(Fr(-1, 8), Fr(-3, 8)), '−(1 + 3√5)/8', '164.48° = 4π/3 − θ5', None),
       'tesseract': (Q5(0), '0', '90° = π/2', Fr(1, 2)), '5-cell': (Q5(Fr(1, 4)), '1/4', '75.52° = θ5', None),
       '16-cell': (Q5(Fr(-1, 2)), '−1/2', '120° = 2π/3', Fr(2, 3)), '24-cell': (Q5(Fr(-1, 2)), '−1/2', '120° = 2π/3', Fr(2, 3))}
rows = {}
for m in re.finditer(r'<tr[^>]*><td>([^<]+)</td>(.*?)</tr>', raw, re.S):
    rows[m.group(1)] = re.sub(r'\s+', ' ', _h.unescape(re.sub(r'<[^>]+>', '', m.group(2))))
for nm in X.ORDER:
    p = P[nm]; c, cs, ang, rat = COS[nm]
    ok(f'{nm}: counts {COUNTS[nm]} exact', p.counts() == COUNTS[nm], p.counts())
    ok(f'{nm}: dihedral cos {cs} exact', p.cos == c, p.cos)
    deg = math.degrees(math.acos(float(c)))
    ok(f'{nm}: angle {ang}', f'{deg:.2f}' in ang or f'{round(deg)}°' in ang, f'{deg:.6f}°')
    if rat is not None: ok(f'{nm}: angle = {rat}π', abs(deg - 180 * rat) < 1e-9)
    r = rows.get(nm, ''); ok(f'Table 1 row {nm}', ', '.join(map(str, COUNTS[nm])) in r and cs in r and ang in r, r[:90])
# edge lengths and cell types
CELLV = {'120-cell': 20, '600-cell': 4, 'tesseract': 8, '5-cell': 4, '16-cell': 4, '24-cell': 6}
for nm in X.ORDER: ok(f'{nm}: facets have {CELLV[nm]} corners', {len(c) for c in P[nm].cells} == {CELLV[nm]})
# ridge areas of the triangle polytopes: (√3/4) a² each
for nm, n, tot in (('5-cell', 10, '(5√3/2) a²'), ('600-cell', 1200, '300√3 a²')):
    p = P[nm]; a2 = {X.tri_area2(*[p.V[i] for i in sorted(s)]) for s in p.ridges}
    ok(f'{nm}: every ridge a triangle of squared area 3a⁴/16', all(len(s) == 3 for s in p.ridges) and a2 == {Fr(3, 16) * p.a2 * p.a2})
    has(tot)
ok('10 · √3/4 = 5√3/2 and 1200 · √3/4 = 300√3', Fr(10, 4) == Fr(5, 2) and Fr(1200, 4) == 300)
has('10 · (√3/4) a² = (5√3/2) a²'); has('1200 · (√3/4) a² = 300√3 a²')

# ---------------- Proposition 8 and Lemma 7 ---------------------------------------------------------------------------------
c5, c6 = P['5-cell'].cos, P['600-cell'].cos
prod = Q5(Fr(15, 32), Fr(-3, 32))
ok('sin θ5 sin θ600 = (15 − 3√5)/32 (squares, positive)', (1 - c5 * c5) * (1 - c6 * c6) == prod * prod and prod.sign() > 0)
ok('its square (270 − 90√5)/1024', prod * prod == Q5(Fr(270, 1024), Fr(-90, 1024)))
ok('(1 + 3√5)² /64 = (46 + 6√5)/64', Q5(1, 3) * Q5(1, 3) == Q5(46, 6))
ok('cos(θ5 + θ600) = −1/2 exactly', c5 * c6 - prod == Q5(Fr(-1, 2)))
ok('θ5 > π/3 and θ600 > 5π/6', c5 < Q5(Fr(1, 2)) and c6 * c6 > Q5(Fr(3, 4)) and c6.sign() < 0)
t5, t6 = math.acos(0.25), math.acos(float(c6))
ok('θ5 + θ600 = 4π/3 (floats agree)', abs(t5 + t6 - 4 * math.pi / 3) < 1e-14)
for s in ('(15 − 3√5)/32', '(270 − 90√5)/1024', '(46 + 6√5)/64', '−(1 + 3√5)/32', '7π/6', 'cos θ600 < −√3/2'.replace('θ600', 'θ600')):
    has(s)
ok('Lemma 7: 1/4 is not in Niven\'s set {0, ±1/2, ±1}', Fr(1, 4) not in {0, Fr(1, 2), Fr(-1, 2), 1, -1})
ok('Lemma 7 alt: 2cos θ5 = 1/2 is not an algebraic integer', Fr(1, 2).denominator != 1)
has('{0, ±1/2, ±1}')
d240, d315 = math.degrees(t5 + t6), math.degrees(4 * math.pi / 3 + t5)
ok('240° and 315.52°', f'{d240:.0f}' == '240' and f'{d315:.2f}' == '315.52', f'{d240:.6f}, {d315:.6f}'); has('240°'); has('315.52°')
for v, s in ((math.degrees(math.pi - math.acos(1 / 3)), '109.47°'), (math.degrees(math.acos(1 / 3)), '70.53°'), (math.degrees(t5), '75.52°'), (math.degrees(t6), '164.48°')):
    ok(f'angle {s}', f'{v:.2f}°' == s, f'{v:.6f}'); has(s)

# ---------------- Proposition 10: the balance -------------------------------------------------------------------------------
ok('300√3 = (5√3/2) · 120', Fr(5, 2) * 120 == 300)
sols = [p for p in range(1, 200) if 120 % (p * p) == 0]
ok('p² | 120 only for p = 1, 2', sols == [1, 2], sols)
ok('120 = 2³ · 3 · 5', 2 ** 3 * 3 * 5 == 120); has('120 = 2³ · 3 · 5')
ok('p = 2, q odd: n = 120 q²/4 = 30 q², smallest 30', all(120 * q * q // 4 == 30 * q * q for q in (1, 3, 5)))
has('n b² = 120 a²'); has('n = 30, of edge b = 2a'); has('(5√3/2)(n b² − 120 a²)')
# Proposition 11 (iii): 1200 − 4c + 4c·0 ... sum = 10c − 1200, zero iff c = 120
ok('−1200 + 4c + 6c = 0 iff c = 120 (only 4c of the angle 4π/3 drop out)', [c for c in range(0, 601) if -1200 + 10 * c == 0] == [120])
ok('c = 120: 720 old ridges, 480 at 4π/3, 720 cap sides', (1200 - 4 * 120, 4 * 120, 6 * 120) == (720, 480, 720))
has('(10c − 1200)'); has('720 at θ600, 480 at 4π/3, 720 cap sides at θ5')

# ---------------- Theorem 12: the cap orbits -------------------------------------------------------------------------------
p6 = P['600-cell']
ok('600-cell: corners are 2I (closed under the quaternion product)', all(X.qmul(u, v) in set(p6.V) for u in p6.V[:12] for v in p6.V))
ok('600-cell: circumradius 1, edge 1/φ', p6.R2 == Q5(1) and p6.a2 == 1 / (PHI * PHI))
orbs = X.caps(p6); ok('5 orbits of 120', sorted(len(o) for o in orbs) == [120] * 5 and len(set(k for o in orbs for k in o)) == 600)
for i, o in enumerate(orbs):
    f, T = X.cap_checks(p6, o); ok(f'orbit {i}: ' + ', '.join(k for k in f), all(f.values()), f)
cen = [sum((p6.V[i][j] for i in p6.cells[0]), Q5()) / 4 for j in range(4)]
ok('facet centroid |c|² = (7 + 3√5)/16 = φ⁴/8', X.dot(cen, cen) == Q5(Fr(7, 16), Fr(3, 16)) and X.dot(cen, cen) == PHI * PHI * PHI * PHI / 8)
has('(7 + 3√5)/16 = φ⁴/8'); has('(4/φ²) c'); has('|4c/φ²|² = 2')
# (1 + (a√10/4)/|c|) = 4/φ²  <=>  (a√10/4)/|c| = 4/φ² − 1; square both sides: (10 a²/16)/|c|² = (4/φ² − 1)²
a2 = p6.a2; lam = 4 / (PHI * PHI) - 1
ok('tip factor: 1 + (a√10/4)/|c| = 4/φ² (squares, positive)', (Q5(10) * a2 / 16) / X.dot(cen, cen) == lam * lam and lam.sign() > 0)
ok('the 5-cell height over a facet is a√10/4 (5-cell of edge 1)', True)
p5 = P['5-cell']; v0 = p5.V[4]; base = [p5.V[i] for i in range(4)]
bc = [sum((b[j] for b in base), Q5()) / 4 for j in range(4)]; hgt2 = X.dot(X.sub(v0, bc), X.sub(v0, bc))
ok('5-cell height² = 10 a²/16 exactly', hgt2 == Q5(10) * p5.a2 / 16)
has('1440'); has('14400')
log600 = os.path.join(ST, '2026-11-20-600cell-5cell-zero', 'checks', 'dehn600.log')
L = open(log600, encoding='utf-8').read() if os.path.exists(log600) else ''
ok('study log: rotations 1440, reflections 0', re.search(r'rotations 1440\s*,\s*reflections 0', L) is not None)
ok('study log dehn600: FINAL ok, 21 PASS', L.rstrip().endswith('FINAL ok') and L.count('\nPASS ') + L.startswith('PASS ') == 21)
LA = open(os.path.join(ST, '2026-11-20-600cell-5cell-zero', 'checks', 'apexes.log'), encoding='utf-8').read()
ok('study log apexes: all 5 left orbits, mirror relation, FINAL ok', LA.count('PASS left orbit') == 5 and 'mirror image' in LA and LA.rstrip().endswith('FINAL ok'))

# ---------------- Proposition 13: volumes --------------------------------------------------------------------------------
def vol2(p):
    """squared volume / a⁸ by pyramids from the centre: V = (#facets/4) r T, r the inradius, T the facet volume."""
    k = 0; c = sorted(p.cells[k]); n = p.N[k]; vs = [p.V[i] for i in c]
    r2 = X.dot(vs[0], n) * X.dot(vs[0], n) / p.nn                       # inradius²
    assert len(c) == 4; e = [X.sub(vs[i], vs[0]) for i in (1, 2, 3)]
    G = [[X.dot(e[i], e[j]) for j in range(3)] for i in range(3)]
    det = (G[0][0] * (G[1][1] * G[2][2] - G[1][2] * G[2][1]) - G[0][1] * (G[1][0] * G[2][2] - G[1][2] * G[2][0])
           + G[0][2] * (G[1][0] * G[2][1] - G[1][1] * G[2][0]))
    T2 = det / 36; N = len(p.cells)
    return Q5(N * N, 0) / 16 * r2 * T2 / (p.a2 * p.a2 * p.a2 * p.a2)


V600 = Q5(25, 0) / 4 * PHI * PHI * PHI
ok('V(600-cell) = (25/4) φ³ a⁴ = (25/4)(2 + √5) a⁴', vol2(p6) == V600 * V600 and V600 == Q5(Fr(25, 4)) * Q5(2, 1))
ok('V(5-cell) = (√5/96) a⁴', vol2(p5) == (R5 / 96) * (R5 / 96))
tot = V600 + 120 * R5 / 96
ok('total = (25 + 15√5)/2 = 5√5 φ²', tot == Q5(Fr(25, 2), Fr(15, 2)) and tot == 5 * R5 * PHI * PHI)
ok('(5^(3/8)√φ)⁸ = 125 φ⁴ = (5√5 φ²)²', tot * tot == 125 * PHI * PHI * PHI * PHI)
num = {'26.47542': float(V600), '2.79508': float(120 * R5 / 96), '29.27051': float(tot), '2.325989': 5 ** 0.375 * float(PHI) ** 0.5}
for s, v in num.items(): ok(f'value {s}', f'{v:.{len(s.split(".")[1])}f}' == s, v); has(s)
ok('2.32599 (abstract) rounds 2.325989', f'{5 ** 0.375 * float(PHI) ** 0.5:.5f}' == '2.32599'); has('2.32599 a')
ok('cube edge = total^(1/4)', abs(float(tot) ** 0.25 - 5 ** 0.375 * float(PHI) ** 0.5) < 1e-12)
v30 = V600 + 30 * 16 * R5 / 96
ok('n = 30, b = 2a: (25/2 + 45√5/4) a⁴ ≈ 37.65576, cube edge ≈ 2.477182', v30 == Q5(Fr(25, 2), Fr(45, 4)) and f'{float(v30):.5f}' == '37.65576' and f'{float(v30) ** 0.25:.6f}' == '2.477182')
has('(25/2 + 45√5/4) a⁴ ≈ 37.65576 a⁴'); has('≈ 2.477182 a')
# proof of Prop 13: inradius φ³/(2√2) for a = 1 (squares), r·T = φ³/24, V = 600 φ³/96; 5-cell inradius √10/20
r2 = (PHI * PHI) * X.dot(cen, cen)                                   # |c|² scaled to a = 1 (× φ²)
ok('600-cell inradius² (a = 1) = φ⁶/8', r2 == PHI * PHI * PHI * PHI * PHI * PHI / 8)
ok('600 φ³/96 = (25/4) φ³', Fr(600, 96) == Fr(25, 4))
ok('5-cell: 5 · √10/(4 · 6√2 · 20) = √5/96', Fr(5, 4 * 6 * 20) == Fr(1, 96))
ok('(50 + 25√5)/4 + 5√5/4 = (25 + 15√5)/2', Q5(Fr(50, 4), Fr(25, 4)) + Q5(0, Fr(5, 4)) == Q5(Fr(25, 2), Fr(15, 2)))
has('5√5 φ² a⁴ ≈ 29.27051 a⁴'); has('5<sup>3/8</sup>√φ a ≈ 2.325989 a'.replace('<sup>', '').replace('</sup>', ''))

# ---------------- Lean: names, axioms, lines -------------------------------------------------------------------------------
E2 = os.path.join(ST, '2026-11-20-palomar-dehn4d')
CH = open(os.path.join(E2, 'package', 'Challenge', 'DehnHadwiger4D.lean'), encoding='utf-8').read()
AX = open(os.path.join(E2, 'package', 'logs', 'axioms.log'), encoding='utf-8').read()
thms = re.findall(r'^theorem (\S+)', CH, re.M)
ok('Challenge: 14 theorems', len(thms) == 14, thms); ok('Challenge: 300 lines', CH.count('\n') == 300 or len(CH.splitlines()) == 300, len(CH.splitlines()))
axl = re.sub(r'\s+', ' ', AX)
for t in thms:
    ok(f'axioms: {t}', re.search(r"'DehnHadwiger4D\." + re.escape(t) + r"' depends on axioms: \[propext, Classical\.choice, Quot\.sound\]", axl) is not None)
LEAN = os.path.join(E2, 'lean', 'DehnHadwiger'); src = ''
lines = {}
for f in sorted(os.listdir(LEAN)):
    if re.match(r'DH\d+.*\.lean$', f):
        t = open(os.path.join(LEAN, f), encoding='utf-8').read(); src += t; lines[f[:-5]] = len(t.splitlines()) if not t.endswith('\n') else t.count('\n')
ok('15 modules DH1–DH15', len(lines) == 15, sorted(lines))
ok('3,383 lines in all', sum(lines.values()) == 3383, sum(lines.values())); has('3,383 lines')
for m in re.finditer(r'<tr[^>]*><td>([A-Za-z0-9, ]+)</td><td class="n">([\d, ]+)</td>', raw):
    names = [x.strip() for x in m.group(1).split(',')]; nums = [int(x) for x in m.group(2).replace(', ', ' ').replace(',', '').split()]
    if all(n in lines for n in names): ok(f'Table 2 {m.group(1)}', [lines[n] for n in names] == nums, nums)
canon = os.path.join(E2, 'package', 'library', 'Canon')
ok('13 Dehn Canon modules reused', len([f for f in os.listdir(canon) if f.endswith('.lean')]) == 13); has('13 modules of the Dehn Canon')
codes = set(re.findall(r'<code>([A-Za-z_][A-Za-z0-9_\']*)</code>', raw))
lean_names = {c for c in codes if re.match(r'^(dehnHadwiger|similar|arccos_quarter|adj_class|cell600_pair|area_pos|wedgeAngle)', c)}
for c in sorted(lean_names):
    ok(f'Lean name {c} exists', re.search(r'(theorem|lemma|def) ' + re.escape(c) + r'[\s({\[:]', src + CH) is not None)
ok('no sorry / native_decide in the Lean sources', 'sorry' not in re.sub(r'--.*|/-.*?-/', '', src, flags=re.S) and 'native_decide' not in re.sub(r'--.*|/-.*?-/', '', src, flags=re.S))
ok('adj_class: squared length 8, dot −2 + 6φ', 'gdot z w = (-2, 6)' in src and '= 8' in src); has('dot product −2 + 6φ')
ok('−2 + 6φ over 8 = (1 + 3√5)/8 (cos between normals)', (Q5(-2) + 6 * PHI) / 8 == Q5(Fr(1, 8), Fr(3, 8)))
for s in ('Lean v4.35.0-rc2', 'Mathlib v4.35.0-rc2'): has(s)

# ---------------- pre-score logs ---------------------------------------------------------------------------------------------
PS = os.path.join(ST, '2026-11-20-palomar-next-prescore', 'checks')
for f in ('dihedral4d.log', 'rational_pi.log', 'relation_600_5.log'):
    t = open(os.path.join(PS, f), encoding='utf-8').read(); ok(f'pre-score {f}: FINAL ok', t.rstrip().endswith('FINAL ok'))

# ---------------- figures --------------------------------------------------------------------------------------------------
fs = json.load(open(os.path.join(HERE, '..', 'data', 'fig-scenes.json')))
ok('figure asserts all pass', all(c[1] for c in fs['checks']) and len(fs['checks']) >= 26, len(fs['checks']))
for f in ('fig-six.png', 'fig-angles.png', 'fig-caps.png'):
    ok(f'figure {f} present and used', os.path.exists(os.path.join(HERE, '..', 'figures', f)) and f'figures/{f}' in raw)

# ---------------- references and house rules ------------------------------------------------------------------------------
nref = len(re.findall(r'<li>', raw.split('<ol class="refs">')[1]))
body = flat[:flat.rindex('References')]
cited = set()
for m in re.finditer(r'\[([^\[\]]+)\]', body):
    for part in re.split(r'[,;]', m.group(1)):
        if re.fullmatch(r'\d+', part.strip()): cited.add(int(part.strip()))
ok(f'{nref} references, every one cited', set(range(1, nref + 1)) <= cited, sorted(set(range(1, nref + 1)) - cited))
ok('no citation beyond the list', max(cited) <= nref, max(cited))
ok('one AI credit line', flat.count('with Claude (Anthropic)') == 1 and 'Computation, proofs, verification and drafting with Claude (Anthropic).' in flat)
low = flat.lower()
for w in ('opus', 'sonnet', 'fable', 'claude code', 'in plain words', 'football', 'flat-ended',
          'compute-host', '/home/', 'raspberry'):
    ok(f'banned: "{w}"', w not in low)
for w in ('fire', 'water', 'earth', 'aether', 'void', 'wind'):
    ok(f'no element word "{w}"', re.search(r'\b' + w + r'\b', low) is None)
ok('Queens only in the two notes (titles of references aside)', body.count('White Queen') == 1 and body.count('Red Queen') == 1)
ok('DICTO DOI labels', all(m.startswith('DICTO DOI:') for m in re.findall(r'DICTO DOI:[^,.]*', flat)))
ok('status box present (draft)', 'delete this box at publication' in flat)
ok('paper number at publication', 'Paper # (at publication)' in flat)

print('AUDIT OK' if not FAILS else f'AUDIT FAIL ({len(FAILS)}): ' + '; '.join(FAILS))
sys.exit(1 if FAILS else 0)
