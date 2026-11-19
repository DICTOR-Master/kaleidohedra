# Number audit for "Fair Dice — The Aequi": every count and bound in the text and tables is read from the study data
# files and checked against the paper (and Table 3 row by row against the catalogue). Ends with "AUDIT OK" or a list.
# Usage: STUDIES=<folder holding the studies> python3 audit.py   (needs numpy for the study's groups.py)
import os, re, csv, json, sys, subprocess
from collections import Counter
S = os.environ.get('STUDIES', '../../../studies')
C, A, K, T2 = (os.path.join(S, d) for d in ('2026-11-19-aequi-complete', '2026-11-20-aequi-alexandrov',
                                            '2026-11-20-aequi-catalogue', '2026-11-20-aequi-two-placements'))
HERE = os.path.dirname(os.path.abspath(__file__))
H = open(os.path.join(HERE, '..', 'paper.html'), encoding='utf-8').read()
txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', H))
bad = []
def need(s, why):
    if s not in txt: bad.append(f'missing "{s}" ({why})')
def ok(c, why):
    if not c: bad.append('FAIL ' + why)
def sci(x, d=1):   # 6.86e-100 -> "6.9 × 10⁻¹⁰⁰"
    m, e = f'{x:.{d}e}'.split('e'); sup = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    return f'{m} × 10{str(int(e)).translate(sup)}'

# ---- main catalogue (catalogue study) ----
cat = list(csv.DictReader(open(os.path.join(K, 'data/catalogue.csv'), encoding='utf-8')))
ok(len(cat) == 149, '149 rows'); need('149', 'main catalogue')
g = Counter(r['group'] for r in cat)
for grp, n in [('Ih', 4), ('Oh', 4), ('Td', 3), ('Th', 47), ('T', 91)]:
    ok(g[grp] == n, f'{grp} {n}'); need(f'{grp} {n}', 'group count')
ok(set(g) == {'Ih', 'Oh', 'Td', 'Th', 'T'}, 'no O, no I')
mc = Counter(int(r['m']) for r in cat)
want = {2: 26, 3: 41, 4: 42, 5: 27, 6: 11, 7: 2}
ok(dict(mc) == want, f'by m {dict(mc)}')
for m, n in want.items(): need(f'{n} (m = {m})', 'count by m')
mos = [r for r in cat if int(r['m']) >= 4]
ok(len(mos) == 82 and all(r['mosaicus'] == 'yes' for r in mos), '82 Mosaici'); need('82 Aequi Mosaici', 'Mosaici')
mg = Counter(r['group'] for r in mos); ok(mg['Th'] == 20 and mg['T'] == 62, 'Mosaici Th 20, T 62'); need('20 of them in Th and 62 in T', 'Mosaici by group')
ok(g['Ih'] + g['Oh'] + g['Th'] == 55 and g['Td'] + g['T'] == 94, '55 / 94'); need('55 dice of Ih, Oh and Th', '55'); need('94 dice of Td and T', '94')
ok(all(r['hands'].startswith('two') == (r['group'] == 'T') for r in cat), 'two hands exactly for T')
Ds = sorted(r['D'] for r in cat if r['D']); ok(Ds == [f'D{i}' for i in range(179, 192)], 'D179–D191'); need('D179–D191', 'D-numbers')
rdi = [r for r in cat if r['D'] == 'D191'][0]; ok(rdi['name'] == 'Aequus RDI-32, Th 17', 'D191 = RDI-32, Th 17'); need('Aequus RDI-32, Th 17', 'D191')
ohs = [r['name'].split(',')[0].replace('Aequus ', '') for r in cat if r['group'] == 'Oh']
ok(ohs == ['CO-14', 'CRD-18', 'ORD-20', 'CORD-26'], 'Oh names'); need('CO-14, CRD-18 and ORD-20 of Equanimity and CORD-26', 'Oh names')
irt = [r for r in cat if r['group'] == 'Th' and r['number'] == '24'][0]
ok(irt['name'] == 'Aequus IRT-44, Th 24' and irt['orbits'].startswith('O8 (1, 1, 1) + I12') and 'RT24' in irt['orbits'], 'IRT-44 = O8 + I12 + RT24')
need('Aequus IRT-44, Th 24', '§5.2')
# Table 3 row by row
rows = re.findall(r'<tr><td class="n">(\w+) (\d+)</td><td>([^<]*)</td><td class="n">(\d+)</td><td class="n">(\d+)</td><td>([^<]*)</td><td>([^<]*)</td></tr>',
                  H.split('<!--CATALOGUE-->')[1].split('<!--/CATALOGUE-->')[0])
ok(len(rows) == 149, f'Table 3 has {len(rows)} rows')
for (grp, num, name, m, N, fc, D), r in zip(rows, cat):
    ok((grp, num, m, N, D) == (r['group'], r['number'], r['m'], r['N'], r['D']) and r['name'] == f'Aequus {name}, {grp} {num}'
       and fc == ', '.join(p.strip().replace('-gon', '') for p in r['faces'].split(';')), f'Table 3 row {grp} {num}')
# residuals of the 149 and central symmetry (Corollary 3) from the 60-digit die files
sys.path.insert(0, os.path.join(C, 'scripts')); import numpy as np; from groups import DIRS, DFAM
rs = ri = 0
for r in cat:
    d = json.load(open(os.path.join(C, 'data', r['source']), encoding='utf-8'))
    rs = max(rs, float(d['residual_solid_angle'])); ri = max(ri, float(d['residual_incidence']))
    V = DIRS[d['face_directions']]; ok(len(V) == int(r['N']), f'N of {r["name"]}')
    sym = all(np.abs(V + v).max(axis=1).min() < 1e-9 for v in V)
    ok(sym == (r['group'] in ('Ih', 'Oh', 'Th')), f'opposite pairs exactly for Ih/Oh/Th: {r["name"]}')
ok(ri < 1e-100, 'corners on planes to 1e-100'); need(sci(rs), 'face residual of the 149'); need('to 10⁻¹⁰⁰', 'incidence')

# ---- search (complete study) ----
st = json.load(open(os.path.join(C, 'data/search-status.json')))
fx = [x for x in st if not x['polar']]; po = [x for x in st if x['polar']]
nfx = sum(x['searched'] for x in fx); npo = sum(x['searched'] for x in po)
hfx = Counter(); hpo = Counter()
for x in fx: hfx.update({k: v for k, v in x['sols_hist'].items()})
for x in po: hpo.update({k: v for k, v in x['sols_hist'].items()})
ok(nfx == 6684 and dict(hfx) == {'1': 6684}, 'one die on each of 6684'); need('6684', 'fixed-point sets')
ok(npo == 4938 and hpo['1'] == 4619 and hpo['0'] == 319, 'polar 4938 = 4619 + 319')
for s in ('4938', '4619', '319'): need(s, 'polar sets')
ok(nfx + npo == 11622, '11 622 sets'); need('11 622', 'all sets')
fg = Counter()
for x in st:
    if x['group'] in ('Ih', 'I', 'Oh', 'O', 'Td', 'Th', 'T'): fg[x['group']] += x['searched']
ok(dict(fg) == {'Ih': 4, 'I': 4, 'Oh': 4, 'O': 4, 'Td': 8, 'Th': 57, 'T': 153}, f'frame-group sets {dict(fg)}')
need('4 sets for Ih, 4 for I, 4 for Oh, 4 for O, 8 for Td, 57 for Th and 153 for T, 234 in all', 'frame sets'); ok(sum(fg.values()) == 234, '234')
na = Counter(r['why'] for r in csv.DictReader(open(os.path.join(C, 'data/not-aequi.csv'), encoding='utf-8')))
ok(na['fair about the frame centre only (centroid elsewhere)'] == 3554, '3554 off-centre'); need('3554', 'off-centre')
need('6.1 × 10⁻⁵', 'smallest offset'); ok('smallest offset 6.1e-5' in open(os.path.join(C, 'README.md'), encoding='utf-8').read(), 'offset 6.1e-05 in study')
# counts of all 4553
cnt = {}
for line in open(os.path.join(C, 'data/counts.md'), encoding='utf-8'):
    p = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(p) == 9 and p[-1].isdigit(): cnt[p[0]] = int(p[-1])
ok(cnt['all'] == 4553 and sum(v for k, v in cnt.items() if k != 'all') == 4553, '4553'); need('4553', 'all Aequi')
ok(4553 - 149 == 4404, '4404'); need('4404', 'below frames')
for k, v in [('C2h', 888), ('D2', 857), ('D2h', 848), ('S6', 694)]: ok(cnt[k] == v, f'{k} {v}'); need(f'{k} {v}', 'largest classes')
ok(sorted(cnt, key=lambda k: -cnt[k])[1:5] == ['C2h', 'D2', 'D2h', 'S6'], 'largest four classes')
ok(sum(cnt[k] for k in ('D3h', 'D5h', 'D6h', 'D8h', 'D10h')) == 6, 'six prisms'); need('Six of them are prisms', 'prisms')
ex = open(os.path.join(C, 'logs/exact-summary.log'), encoding='utf-8').read()
m_ = re.search(r'refined (\d+) dice; all exact_ok: True; max \|Omega - 4pi/N\| = ([\d.e+-]+)', ex)
ok(m_ and int(m_.group(1)) == 4553, 'exact 4553'); need(sci(float(m_.group(2))), 'residual of 4553')

# ---- Alexandrov study ----
v = list(csv.DictReader(open(os.path.join(A, 'data/verdicts.csv'), encoding='utf-8')))
ns = [r for r in v if r['kind'] == 'nosol']; ct = [r for r in v if r['kind'] != 'nosol']
fails = [r for r in ns if r['verdict'].startswith('fails')]; holds = [r for r in ns if r['verdict'] == 'holds']
ok(len(ns) == 319 and len(fails) == 87 and len(holds) == 232, '319 = 87 + 232'); need('87 fail', '87'); need('other 232', '232')
gk = 'g=2pi(2|A|-N)/N-L'
eq = [r for r in fails if abs(float(r[gk])) < 1e-40]   # 0 to 1e-50 in the 50-digit re-check; ok(len(eq) == 12, f'12 equalities ({len(eq)})'); need('12 of them fail with equality', '12')
pos = min(float(r[gk]) for r in fails if float(r[gk]) > 1e-40); ok(f'{pos:.4f}' == '0.0329', f'smallest margin {pos}'); need('g = 0.0329', 'margin')
ok(all(int(r['witness_size']) == int(r['N']) - 1 for r in fails), 'witness N − 1 in all 87')
ok(all(r['die_80_digits'] == 'True' for r in holds), '232 confirmed')
dr = [float(r['die_depth_ratio_max']) for r in holds]; ok(f'{min(dr):.2f}' == '4.53' and f'{max(dr):.1f}' == '116.4', f'ratios {min(dr)} {max(dr)}')
need('from 4.53 to 116.4', 'depth ratios')
co = [float(r['die_centroid_offset']) for r in holds]; ok(f'{min(co):.2f}' == '0.21' and f'{max(co):.2f}' == '1.02', f'offsets {min(co)} {max(co)}')
need('from 0.21 to 1.02', 'offsets'); ok(all(int(r['N']) <= 13 for r in ns), 'N ≤ 13'); need('N ≤ 13', 'exhaustive')
ok(len(ct) == 50 and all(r['verdict'] == 'holds' for r in ct), '50 controls'); need('50 polar sets', 'controls')
sm = open(os.path.join(A, 'logs/summary.log'), encoding='utf-8').read()
ok('largest relative depth difference from the study die 1.2e-12' in sm, 'control 1.2e-12'); need('1.2 × 10⁻¹²', 'controls')
ok(abs(2.718281828459045 ** 1.5 - 4.4817) < 1e-3, 'e^1.5'); need('e<sup>1.5</sup> = 4.48'.replace('<sup>', '').replace('</sup>', ''), 'box')

# ---- two placements ----
t2 = {}
for line in open(os.path.join(T2, 'data/counts.md'), encoding='utf-8'):
    p = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(p) == 13 and p[-1].isdigit(): t2[p[0]] = [int(c) if c else 0 for c in p[2:]]
ok(t2['all'][-1] == 1083, '1083'); need('1083', 'two-icosahedron dice')
for grp, lab in [('Oh', 'Oh'), ('O', 'O (two hands)'), ('Td', 'Td'), ('Th', 'Th'), ('T', 'T (two hands)'), ('all', 'all')]:
    m = re.search(r'<tr(?: class="hd")?><td>' + re.escape(lab) + r'</td>(.*?)</tr>', H)
    cells = [int(c) if c else 0 for c in re.findall(r'<td[^>]*>(\d*)</td>', m.group(1))] if m else None
    ok(cells == t2[grp], f'Table 4 row {grp}: {cells} vs {t2[grp]}')
ok(t2['O'][-1] == 2 ** 5 - 1 and t2['Oh'][-1] == 2 ** 6 - 2 ** 3 - 3, '31 and 53'); need('2⁵ − 1 = 31', '31'); need('2⁶ − 2³ − 3 = 53', '53')
al = t2['all']; ok(al[0] == 30 and al[1] == 88 and sum(al[2:10]) == 965, '30 / 88 / 965'); need('965 are Aequi Mosaici', '965')
s2 = json.load(open(os.path.join(T2, 'data/search-status.json')))
n2 = Counter(); h2 = Counter()
for x in s2: n2[x['group']] += x['searched']; h2.update(x['sols_hist'])
ok(n2['Th'] == 224 and n2['T'] == 1088 and dict(h2) == {'1': 1312}, f'224 + 1088 sets, one die each {dict(n2)} {dict(h2)}')
need('Th (224 sets) and T (1088 sets)', 'two-placement sets')
e2 = open(os.path.join(T2, 'logs/exact-summary.log'), encoding='utf-8').read()
m2 = re.search(r'max \|Omega - 4pi/N\| = ([\d.e+-]+)', e2); need(sci(float(m2.group(1))), 'residual of 1083')
rd = open(os.path.join(T2, 'README.md'), encoding='utf-8').read()
ok('its 257 starts' in rd and 'From 2049 Sobol starts' in rd, '257 / 2049'); need('257 starts', 're-search'); need('2049 more', 're-search')
ok(4553 + 1083 == 5636, '5636'); need('5636', 'all dice')
# fixed ratio of §5.2 from the 60-digit depths of both dice
d1 = json.load(open(os.path.join(C, 'data', irt['source']), encoding='utf-8'))
fn = [f for f in os.listdir(os.path.join(T2, 'data/dice')) if f.endswith('-Th-O8-D12-RT24p.json')]
ok(len(fn) == 1, 'two-placement die O8 + D12 + RT24′'); d2 = json.load(open(os.path.join(T2, 'data/dice', fn[0]), encoding='utf-8'))
ok(d1['orbits'] == ['O8', 'I12', 'RT24'] and d2['orbits'][0] == 'O8' and d2['orbits'][-1].startswith('RT24'), f'orbit order {d1["orbits"]} {d2["orbits"]}')
from decimal import Decimal, getcontext; getcontext().prec = 70
r1 = Decimal(d1['depths_60_digits'][2]) / Decimal(d1['depths_60_digits'][0]); r2 = Decimal(d2['depths_60_digits'][-1]) / Decimal(d2['depths_60_digits'][0])
s38 = '1.02140047185008282050793373959299607810'
ok(str(r1)[:40] == str(r2)[:40] == s38[:40], f'fixed ratio {r1} {r2}'); need(s38, 'fixed ratio')
# Figure 1 angle
out = subprocess.run([sys.executable, os.path.join(HERE, 'fig_polar.py')], capture_output=True, text=True).stdout
a = re.search(r'face 0: ([\d.]+) deg; normal angle at the polar corner: ([\d.]+) deg', out)
ok(a and a.group(1) == a.group(2), 'Figure 1 angles agree'); need(a.group(1) + '°', 'Figure 1 angle')

if bad: print('\n'.join(bad)); print(f'AUDIT FAILED: {len(bad)}'); sys.exit(1)
print('AUDIT OK: 149 catalogue rows, group and m counts, 55/94 split, search sets, 87/232, 4553, 1083 split, residual bounds, fixed ratio, Figure 1')
