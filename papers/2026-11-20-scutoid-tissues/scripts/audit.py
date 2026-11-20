# Audit: every number in the body of paper.html (abstract to the end of "Data and reproducibility") must lie inside a span
# that is either (1) checked here against the study data or texts, or computed exactly, or (2) structural (section, theorem,
# figure and reference numbers, years and identifiers of cited works, mathematics of the statements and proofs).
# Also checks the #104 DOIs against the Concordance. Exit 1 on any unmatched number or failed check; last line FINAL ok.
# Usage: python3 scripts/audit.py STUDIES_DIR CONCORDANCE_JSON      (run from the paper folder)
import sys, re, json, html, math, os

ST, CONC = sys.argv[1], sys.argv[2]
raw = open('paper.html', encoding='utf-8').read()
FAIL = []
NCHK = [0]


def ok(name, cond, info=''):
    NCHK[0] += 1
    if not cond:
        FAIL.append(name + ' ' + str(info))
    print(('PASS ' if cond else 'FAIL ') + name + (' ' + str(info) if info else ''), flush=True)


def rd(rel):
    return open(os.path.join(ST, rel), encoding='utf-8').read()


def has(rel, text):
    return text in rd(rel)


def jl(rel):
    return json.load(open(os.path.join(ST, rel)))


# ---------------------------------------------------------------- body text
body = raw[raw.index('<p class="abstract">'):raw.index('<h2>References')]
body = re.sub(r'<sub>(.*?)</sub>', r'\1', body)
body = re.sub(r'<sup>(.*?)</sup>', r'^\1', body)
body = html.unescape(re.sub(r'<[^>]+>', ' ', body))
body = re.sub(r'[ \t\n]+', ' ', body)
cover = [False] * len(body)


def span(rx, why, need=1):
    """mark every match of rx as covered; require at least `need` matches"""
    n = 0
    for m in re.finditer(rx, body):
        n += 1
        for i in range(m.start(), m.end()):
            cover[i] = True
    if need:
        ok('text has: ' + why, n >= need, rx)


def data(rx, why, cond):
    ok(why, cond)
    span(rx, why)


# ---------------------------------------------------------------- data and exact checks
TN = '2026-11-15-tissue-null-models/'
SW = jl(TN + 'data/sweep.json')
chk = {c[0]: c[1] for c in SW['checks']}
poly = {(p['family'], p['rings']): p for p in SW['polytopes']}
c120, t120, b600 = poly[('H4', '1000')], poly[('H4', '1100')], poly[('H4', '0110')]
trip = lambda p: (p['h1'], p['h2'], p['h1'])
data(r'116 / 366 / 116', '120-cell 116/366/116 (sweep.json)', trip(c120) == (116, 366, 116) and chk['120-cell (116,366)'])
data(r'716 / 966 / 716', 'truncated 120-cell 716/966/716', trip(t120) == (716, 966, 716))
data(r'716 / 2166 / 716', 'bitruncated 600-cell 716/2166/716', trip(b600) == (716, 2166, 716))
data(r'116 births, 366 swaps and 116 deaths', '120-cell in words', True)
data(r'716, 966, 716', 'truncated 120-cell in words', True)
data(r'716, 2166, 716', 'bitruncated 600-cell in words', True)
EL = rd('2026-11-15-event-logger/README.md')
ok('logger returns the #104 counts in two directions', 'in two directions, all frames passing' in EL and '716 / 2166 / 716 (bitruncated 600-cell)' in EL)
SG = rd('2026-11-15-sun-granulation/README.md')
ok('three further directions, 9 of 9 exact', 'three more directions' in SG and '9 of 9 exact' in SG)
data(r'f0 − 2f3 \+ 6', 'closed swaps = f0 - 2 f3 + 6 (120-cell: 600 - 240 + 6 = 366)', c120['f0'] - 2 * c120['f3'] + 6 == 366)
data(r'f3 − 4', 'closed births = f3 - 4 (120 - 4 = 116)', c120['f3'] - 4 == 116)
pv = 24 * math.pi ** 2 / 35 - 2
data(r'24π²/35 − 2 = 4\.7677', '24 pi^2/35 - 2 = 4.7677', abs(pv - 4.7677) < 5e-5)
data(r'4\.7669 ± 0\.0006', 'PV simulation 4.7669 +- 0.0006 (sweep.json check)', chk.get('PV 3D contact changes per birth 4.7669 +- 0.0006 vs 24pi^2/35 - 2 = 4.7677') is True)
span(r'4\.7677', 'PV value repeated')
data(r'96π²/35 corners', 'typical PV cell corners 96 pi^2/35 (THEORY section 3)', '96π²/35' in rd(TN + 'THEORY.md'))
data(r'2 \+ 48π²/35 walls', 'walls = 2 + 48 pi^2/35, and (walls)/2 - 3 = 24 pi^2/35 - 2',
     abs((2 + 48 * math.pi ** 2 / 35) / 2 - 3 - pv) < 1e-12 and '2 + 48π²/35' in rd(TN + 'THEORY.md'))
rs = {r['cells']: r for r in SW['random_simple_polytopes']}
data(r'4\.76291 at n = 300000', 'random simple 4-polytope 4.76291 at n = 300000', round(rs[300000]['h2_over_h1'], 5) == 4.76291)
LOG = rd(TN + 'data/sweep.log')
data(r'14/2 − 3 = 4', 'bcc 14 walls -> 4', 14 / 2 - 3 == 4 and 'control bcc (truncated octahedra) swaps per birth = 4 exactly' in LOG)
data(r'gives exactly 4', 'perturbed bcc sweep exactly 4', 'swaps per birth = 4 exactly' in LOG)
data(r'with 14 walls', 'truncated octahedron 14 walls', True)
data(r'4 swaps per birth', 'bcc 4 swaps per birth', True)
data(r'15 space-time Poisson–Voronoi blocks, swept in 15 directions each', '15 blocks x 15 directions', '15 blocks (seeds 1 to 5 x seed time scales' in SG and '15 directions each' in SG)
data(r'any of the 225 block-directions', '225 block-directions, no index 0 or 4', 'no corner of index 0 or 4 in any of the 225' in SG)
data(r'at most 2\.7%', 'swaps within 2.7%', 'by at most 2.7% in every block' in SG)
span(r'within 2\.7%', 'summary 2.7%')
data(r'tilt of 45 degrees births and deaths are 13 to 20% of the swaps', 'moving Voronoi 13 to 20% at 45 degrees', '13 to 20% at 45 degrees' in SG)
data(r'differ over the tilts by 1\.2 to 3\.6 times', 'Sun tilts 1.2 to 3.6 x PV spread', '1.2 to 3.6 times the Poisson-Voronoi spread' in SG and 'NOT CONFIRMED, as predicted' in SG)
CV = rd('2026-11-15-cosmic-voids/README.md')
data(r'30,758 contact changes', 'toy foams 30,758 events', '30,758 events in three generic motions' in CV)
data(r'time floor of 1e-9', '0 simultaneous at 1e-9', '0 simultaneous changes at a 1e-9 time floor' in CV)
span(r'30,758 events', 'summary 30,758')
GR = rd('2026-11-15-grains-polycrystals/README.md')
data(r'13\.65 to 13\.85', 'grain model <F> 13.65 to 13.85', 'steady-state mean faces 13.65 to 13.85' in GR)
data(r'13\.766', 'Mason <F> 13.766', 'Mason et al. 13.766' in GR)
data(r'3\.883', '13.766/2 - 3 = 3.883', abs(13.766 / 2 - 3 - 3.883) < 1e-12 and '3.883' in GR)
SZ = rd('2026-11-17-sun-step-zero/README.md')
data(r'criteria passed in 0 of 13 settings', 'step zero: 0 of 13 settings', 'passes the\ncriteria C1 to C5 in 0 of 13 settings' in SZ or 'C1 to C5 in 0 of 13 settings' in SZ.replace('\n', ' '))
NC = rd('2026-11-18-sun-net-change/README.md')
data(r'frame-rate free in 16 of 16 settings', 'net change frame-rate free 16 of 16', 'frame-rate free: passes in 16 of 16 settings' in NC and 'NOT CONFIRMED as a natural rung' in NC)
ND = rd('2026-11-18-sun-net-vs-d/README.md')
data(r'the 16 settings collapse', 'net vs D: 16 settings', 'the 16 settings come within 15% of one curve' in ND.replace('\n', ' '))
data(r'falls from 0\.73 to 0\.60', 'net vs D ratio 0.73 to 0.60', '(0.73 to 0.60)' in ND and 'No candidate rung' in ND)
LN = rd('2026-11-18-sun-lineage/README.md')
data(r'spread of 51 to 73%', 'lineage spread 51 to 73%', 'spread of 51 to 73% at matched D' in LN)
data(r'rising from 0\.95 to 1\.26', 'lineage ratio 0.95 to 1.26', 'rises from 0.95 to 1.26' in LN and 'NOT CONFIRMED as a natural rung' in LN)
AS = rd('2026-11-15-atmosphere-seaice/README.md')
data(r'0\.03 to 0\.15 per cell-hour', 'clouds 0.03 to 0.15', '(0.03 to 0.15)' in AS)
data(r'0\.245 ± 0\.011', 'law-built froth 0.245 +- 0.011', '0.245 +- 0.011' in EL)
data(r'0\.53 ± 0\.05', 'Rutenberg-McCurdy 0.53 +- 0.05', '0.53 +- 0.05' in EL)
EP = rd('2026-11-15-earth-plates/README.md')
ok('earth: agreement does NOT carry over', 'does NOT carry over to an' in EP)
# figure facts from the figure script's own output
FJ = json.load(open('data/fig-tube.json'))
fchk = {c[0]: c[1] for c in FJ['checks']}
d1, d2 = FJ['directions']
data(r'\(12 in one direction, 14 in the other\)', 'figure: 12 and 14 swaps', d1['counts']['swap'] == 12 and d2['counts']['swap'] == 14)
data(r'its 18 other corners', 'figure: 18 middle corners', sum(d1['counts'].values()) - 2 == 18)
data(r'\(1, 116, 366, 116, 1\)', 'figure: corner indices of the whole sweep', fchk.get('direction 1: corner indices (1, 116, 366, 116, 1)') and fchk.get('direction 2: corner indices (1, 116, 366, 116, 1)'), )
data(r'600 corners and 1200 edges', 'figure: 600 corners, 1200 edges', fchk.get('120-cell: 600 corners') and fchk.get('1200 edges, four at every corner'))
data(r'\(20 checks, all passing\)', 'figure: 20 checks all passing', len(FJ['checks']) == 20 and all(c[1] for c in FJ['checks']))
data(r'whose 20 checks', 'figure: 20 checks (data section)', len(FJ['checks']) == 20)
data(r'from 3 at birth to 3 at death', 'figure: sides 3 to 3', d1['sides'][0] == d1['sides'][-1] == 3 == d2['sides'][0] == d2['sides'][-1])
src = open('scripts/fig_tube.py').read()
data(r'10, 30, 50, 70 and 90%', 'figure: sections at 10..90%', 'FR = (0.1, 0.3, 0.5, 0.7, 0.9)' in src)
data(r'1, 116, 366, 116, 1 corners of index 0 to 4', 'section 4: whole-sweep indices (figure json)', fchk.get('direction 1: corner indices (1, 116, 366, 116, 1)'))
# the rendered figures: facts from fig_scenes.py's output, the study data and the Sun faces
FS = json.load(open('data/fig-scenes.json')); fsc = {c[0]: c[1] for c in FS['checks']}; G = FS['figures']
ok('figures: every check of fig_scenes.py passes', all(c[1] for c in FS['checks']))
data(r'with 43 checks', 'figures: 43 checks (data section)', len(FS['checks']) == 43)
data(r'its section has 5 sides on the lower plane and 6 on the upper', 'Figure 1: 5 and 6 sides',
     G['fig1'] == {'bottom_sides': 5, 'top_sides': 6} and fsc.get('Figure 1: the scutoid has 5 sides at the bottom and 6 at the top'))
g2 = G['fig2']
data(r'86 cells, 211 corners, 36 births, 147 swaps and 28 deaths', 'Figure 2: block counts',
     (g2['cells'], g2['corners'], g2['births'], g2['swaps'], g2['deaths']) == (86, 211, 36, 147, 28))
data(r'147 = 211 − 36 − 28', 'Figure 2: swaps = corners - births - deaths', 147 == 211 - 36 - 28 and fsc.get('Figure 2: swaps = corners - births - deaths'))
data(r'14 walls, 6 squares and 8 hexagons', 'Figure 5: bcc cells 14 walls, 6 squares, 8 hexagons', fsc.get('Figure 5: every whole bcc cell has 14 walls (6 squares, 8 hexagons)'))
data(r'\(100 to 300000', 'Figure 5: random polytopes from 100 to 300000 cells', min(rs) == 100 and max(rs) == 300000)
csrc = open('scripts/fig_compose.py').read()
data(r'2nd and 98th percentiles', 'Figure 6: colour ramp percentiles', 'np.percentile(allv, 2), np.percentile(allv, 98)' in csrc)
import numpy as np
SF = np.load('data/sun-faces.npz'); NS = int(SF['crop'][2]); TS = SF['front'].shape[0]
data(r'a 12 Mm square', 'Figure 6: 12 Mm square', round(NS * float(SF['dx'])) == 12)
data(r'40 minutes of the same square \(242 frames, 10 s apart\)', 'Figure 6: 242 frames, 10 s apart, 40 minutes',
     TS == 242 and float(SF['dt']) == 10.0 and round((TS - 1) * 10 / 60) == 40)
data(r'0\.1 Mm below the surface in the Bifrost run en024048_hion', 'Figure 6: run and depth (study text)', 'en024048_hion' in SG and '0.1 Mm below tau = 1' in SG)
# #104 DOIs against the Concordance
C = json.load(open(CONC))['papers']['104']
ok('#104 concept DOI ' + C['doi'], '10.5281/zenodo.%s (all versions; Version 3: 10.5281/zenodo.%s)' % (C['doi'], C['doi_v3']) in raw)
ok('#104 is Version 3', C['version'] == 3 and 'Version 3, 11 November 2026' in raw)

# ---------------------------------------------------------------- structure and mathematics
S = [
    (r'#104', 'paper number'), (r'Theorems? \d[\d′, and]*', 'theorem numbers'), (r'Lemma \d', 'lemma'), (r'Corollary \d', 'corollary'),
    (r'Figure \d', 'figure'), (r'Fig\. \d', 'figure'), (r'Sections? \d( to \d)?', 'section'), (r'§+\d+(–\d+)?', 'section'),
    (r'\b\d+\. [A-Z]', 'section heading'), (r'paper #104', 'paper'), (r'h[123]', 'h-vector entries'), (r'f[03]', 'f-vector entries'),
    (r'R\d', 'regions R1, R2'), (r'2-2 move', 'name of the move'), (r'T1', 'name of the move'), (r'\b[23]D\b', 'dimension'),
    (r'three-dimensional|four-dimensional', 'words'), (r'\d+ November 2026', 'date'), (r'arXiv:[\w./]+', 'arXiv id'),
    (r'\b(19[5-9]\d|20[0-2]\d)\b', 'year of a cited work'), (r'd ≥ 4', '#104 Theorem 1′ range'), (r'600-cell|120-cell', 'polytope names'),
    (r'⟨F⟩/2 − 3', 'the formula'), (r'corners − 2 × cells', 'the formula'), (r'K − 2C', 'the formula'), (r'K/C − 2', 'formula'),
    (r'⟨F⟩/2 − 1', 'formula'), (r'2F − 4', 'Euler, simple polytope'), (r'4K = Σ\(2F − 4\)', 'formula'), (r'3Kcell = 2Ecell', 'Euler'),
    (r'4 − 6 \+ 4 = 2', 'Euler on the link'), (r'4 · 3 / 2 = 6', 'arcs of the link'), (r'2 · 6 = 12', 'sides of the link'),
    (r'index(es)? [0-4](, [0-4])*( or [0-4])?( and [0-4])?|index of [0-4] or [0-4]|indices? (\d to \d|\d, \d or \d)', 'corner indices 0 to 4'),
    (r'\(index [0-4]\)', 'corner index'), (r'i = [0-4]', 'index cases'), (r'e[1-4]|C[1-4]|Cj|ej', 'edge and cell labels'),
    (r'e1, …, ei', 'labels'), (r'(index|indices) 1, 2 or 3', 'indices'), (r'1, 2 or 3', 'indices'),
    (r'tetrahedral section, so births = deaths = f3 − 4 \(four cells', 'closed sweep'), (r'The −4 and \+6', 'closed corrections'),
    (r'Rn', 'regions'), (r'tend to 1', 'limit'), (r'by at most 1 and S = K − B − D by at most 2', 'bound'),
    (r'(x, y, v t)|\(x, y, t\)', 'coordinates'), (r'Version 3', 'version'), (r'Phil\. Mag\.|Nat\. Commun\.', 'journal'),
    (r'with five or more cells', 'words'), (r'\[\d+(, \d+)*\]', 'citation numbers'), (r'4-polytopes?', 'name'),
    (r'step 0', 'time step 0 (limit)'), (r'\[\d+, Theorems? \d( and \d)?\]', 'citation with theorem'),
    (r'index cannot be 0|index is 1', 'proof cases'), (r'Python 3', 'software'), (r'fig_tube', 'file name'), (r'render3d', 'file name'),
    (r'Figures \d( to \d)?', 'figures'), (r'24π²/35 − 2', 'the Poisson–Voronoi value as a formula'), (r'Theorem 1\(\w\)', 'theorem part'), (r'Lemma 5', 'lemma of #104'), (r'1′', 'theorem prime'),
]
for rx, why in S:
    span(rx, why, need=0)

left = []
for m in re.finditer(r'\d+', body):
    if not all(cover[i] for i in range(m.start(), m.end())):
        left.append(body[max(0, m.start() - 40):m.end() + 25])
ok('every number in the body is checked or structural', not left, '%d unmatched' % len(left))
for x in left:
    print('   UNMATCHED: ...' + x + '...')
print('%d checks, %d failed' % (NCHK[0], len(FAIL)))
print('FINAL ok' if not FAIL else 'FINAL FAIL')
sys.exit(1 if FAIL else 0)
