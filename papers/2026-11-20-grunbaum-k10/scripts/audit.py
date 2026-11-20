# DICTO · dictospheres.com — number audit for the paper on Grünbaum's zone question at k = 10: every number and quoted
# phrase of the text is checked against the data of the studies (STUDIES env, default ../../../studies) and against
# ../data/get-exact.json (written by get_exact.py); any mismatch is listed and the audit fails.
import ast, json, os, re, subprocess
from math import comb
H = os.path.dirname(os.path.abspath(__file__))
ST = os.environ.get('STUDIES', os.path.join(H, '..', '..', '..', 'studies'))
LIB = os.environ.get('LIBRARY', os.path.join(os.path.expanduser('~'), 'kaleidohedra-references'))
raw = open(os.path.join(H, '..', 'paper.html'), encoding='utf-8').read()
txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', raw)).replace('&amp;', '&')
bad = []
NEEDS = []
def need(s, why):
    NEEDS.append(s)
    if s not in txt: bad.append(f'missing "{s}" ({why})')
def ok(c, why):
    if not c: bad.append('FAIL ' + why)
def rd(*p): return open(os.path.join(ST, *p), encoding='utf-8').read()
K = '2026-11-15-grunbaum-k10'
X = json.load(open(os.path.join(H, '..', 'data', 'get-exact.json')))
ok(open(os.path.join(H, '..', 'data', 'get-exact.log')).read().rstrip().endswith('FINAL ok'), 'get_exact.py ended FINAL ok')
zs = lambda u: (f'{u[0]} + {u[1]}φ' if u[0] else f'{u[1]}φ')

# ---- the solids (get-exact.json) ----
for n in ('GET A', 'GET B', 'candidate 2'):
    r = X[n]; st = r['stats']
    ok((st['F'], st['V'], st['E'], st['chi']) == (30, 32, 60, 2), f'{n} F V E χ'); ok(r['zones'] == [10] * 6, f'{n} zones')
    ok(st['coplanar_adjacent'] == 0 and set(st['normal_angles']) <= {36, 72, 108}, f'{n} normals'); ok(r['neighbours'] == 14 and r['lambda_index'] == 1, f'{n} λ')
    ok(r['removed_types'] == ['015', '023', '124', '345'], f'{n} removed types')
for n in ('GET A', 'GET B'):
    r = X[n]; ok(tuple(r['volume']) == tuple(r['covolume']) == (20, 32), f'{n} volume'); ok((r['prolate'], r['oblate']) == (10, 6), f'{n} cells')
    ok(r['missing'] == ['015', '023', '124', '345'], f'{n} missing')
    for p, t in r['cells'] + r['removed']: need(f'({"".join(map(str, p))}; {"".join(map(str, t))})', f'{n} cell')
need('20 + 32φ', 'volume'); need('015, 023, 124 and 345', 'missing types')
ok(zs(X['T']['prolate_volume']) == '2 + 2φ' and zs(X['T']['oblate_volume']) == '2φ' and zs(X['T']['volume']) == '20 + 40φ', 'cell volumes')
need('prolate (volume 2 + 2φ) or oblate (volume 2φ)', 'cell volumes'); need('volume 20 + 40φ', 'T volume')
ok(X['basis'] == [[1, 0, 0, -1, 0, -1], [0, -1, 0, 0, 1, -1], [0, 0, 1, 1, 1, 0]], 'basis')
for b in ['(1, 0, 0, −1, 0, −1)', '(0, −1, 0, 0, 1, −1)', '(0, 0, 1, 1, 1, 0)']: need(b, 'basis')
ok(X['symmetries'] == {'GET A': [2, 2], 'GET B': [3, 0], 'candidate 2': [12, 0]}, 'symmetries'); ok(all(v == [0, 0] for v in X['congruences'].values()), 'no congruences')
need('4 symmetries (2 rotations and 2 reflections)', 'A sym'); need('GET B has 3 (rotations about one axis)', 'B sym'); need('order 12, all rotations', 'C sym')
need('120 symmetries of the six-axis star', '120'); need('(60 of them rotations)', '60')
ok(X['shared_removed_cells'] == {'GET A, GET B': 3, 'GET B, candidate 2': 3, 'GET A, candidate 2': 2}, 'shared cells')
need('GET A and GET B have three removed cells in common, GET B and the indented triacontahedron three, GET A and the indented triacontahedron two', 'shared')
for n, k in [('GET A', 'square face'), ('GET B', 'three neighbours'), ('candidate 2', 'regular tetrahedron')]: ok(k in X[n]['dimple_kind'], f'{n} dimple kind')
ok(comb(20, 8) == 125970, 'C(20,8)'); need('125,970', 'cube search')
nb = {tuple(v) for v in X['GET A']['neighbour_vectors']}
for v in [(-1, -1, -1, 0, 0, 0), (-1, 0, 0, 1, 0, 1), (0, -1, 0, 0, 1, -1)]:
    ok(v in nb, f'figure 4 vector {v}'); need('(' + ', '.join(str(c).replace('-', '−') for c in v) + ')', 'figure 4 vector')
fs = open(os.path.join(H, '..', 'data', 'fig-scenes.log')).read()
ok('FINAL ok' in fs and 'lattice index 1' in fs, 'fig_scenes.py asserts passed')

# ---- the study of 15 November ----
t12 = rd(K, 'data', 'tile12.log'); ok(t12.count('tiles=True translates=14') == 2, 'tile12: both tile, 14 translates'); need('14 translates within reach', 'tile check')
T12 = json.load(open(os.path.join(ST, K, 'data', 'tile12.json')))
R = {r['index']: r for r in T12['results']}
ok(all(R[i]['det'] == [14, 20] for i in (3, 4, 5, 6)) and R[7]['det'] == [8, 16], 'undecided volumes'); need('four of volume 14 + 20φ and one of volume 8 + 16φ', 'undecided')
v = rd(K, 'data', 'verify.log'); ok(v.count("'coverage_counts': {1: 200000}") == 2, 'verify 200000'); need('200,000 random points', 'verify')
c6 = [ast.literal_eval(l) for l in rd(K, 'data', 'cover6.log').splitlines() if l.startswith('{')]
ok(all(c['points'] == 20000 and c['all_once'] for c in c6 if c['index'] >= 3), 'cover6'); need('covers 20,000 of 20,000 random points exactly once', 'cover6')
s6 = rd(K, 'data', 'search6.log')
ok('depth=3 states=10 ' in s6 and 'depth=4 states=29 ' in s6 and 'depth=4 states=29 in_class=29 noncoplanar=29 rank<=3=3' in s6, 'search depths 3, 4')
ok('states=4827 rank_hist={6: 4578, 5: 241, 3: 8}' in s6, 'search totals')
need('depth 3 gives 10 classes', 's6'); need('depth 4 gives 29 classes, exactly three with rank 3', 's6'); need('4,827 classes, 8 of them with rank 3', 's6')
vc = rd(K, 'data', 'vclass3.log')
ok("n=5: {'subspaces': 729, 'zone_words_ok': 192, 'pair_consistent': 192, 'rank3': 192, 'coherent_golden': 5, 'coherent_twin': 3}" in vc, 'vclass3 n=5')
ok("n=6: {'subspaces': 19683, 'zone_words_ok': 768, 'pair_consistent': 768, 'rank3': 768, 'coherent_golden': 5, 'coherent_twin': 3}" in vc, 'vclass3 n=6')
ok(3 ** 9 == 19683 and 3 ** 6 == 729, '3^9, 3^6')
for s in ['729', '192', '19,683', '768', '5 / 3', 'All 19,683 such X', 'The 8 sign-coherent survivors, 5 for the golden star and 3']: need(s, 'Table 2')
g = rd(K, 'data', 'gnomon.log')
ok("'sources': 18, 'paths': 19048" in g and "'distinct': 23255" in g and "'rank_hist': {6: 22093, 5: 1145, 3: 17}" in g, 'gnomon')
ok('rhombic icosahedron + one zone layer gives the triacontahedron: True' in g, 'gnomon control')
for s in ['18 surfaces', '19,048 cut paths', '23,255 distinct', '6 (22,093), 5 (1,145) and 3 (17)']: need(s, 'gnomon')
cg = [ast.literal_eval(l) for l in rd(K, 'data', 'cover-gnomon.log').splitlines() if l.startswith('{')]
ok(len(cg) == 17 and sum('why' in c for c in cg) == 6 and sum(c.get('all_once') is False for c in cg) == 8 and sum(c.get('all_once') is True for c in cg) == 3, 'gnomon 6/8/3')
gs = [ast.literal_eval(l) for l in rd(K, 'data', 'gnomon-sources.log').splitlines() if l.startswith('{')]
ok(len(gs) == 18 and sum(bool(x['reaches']) for x in gs) == 2 and all(x['k8_face_pair_rank'] == 3 for x in gs if x['reaches']), 'gnomon sources')
need('Exactly two of the 18 sources reach them', 'gnomon sources')
RK = rd(K, 'README.md')
ok('exactly two tilers (D1/D2 type) at depth 2' in RK, 'C(5) two tilers'); need('exactly two tilers, of the type of Grünbaum', 'C(5)')
# ---- Hall, Kostick, Inchbald, mixing, echo ----
Hc = json.load(open(os.path.join(ST, '2026-11-20-hall-2016-check', 'data', 'hall_check.json')))
ok(Hc['tetrahedra'] == 10 and sum(sum(h['candidate 2 (Inchbald)'].values()) == 12 for h in Hc['hall']) == 10, 'Hall 10 sets, 12 maps')
ok(sorted(h['candidate 2 (Inchbald)']['same_hand_maps'] > 0 for h in Hc['hall']).count(True) == 5, 'Hall 5 + 5 hands')
need('each of the 10 regular tetrahedra', 'Hall'); need('five in one hand and five in the other, by 12 maps each', 'Hall')
HR = rd('2026-11-20-hall-2016-check', 'README.md')
HM = re.sub(r'\s+', ' ', json.dumps(json.load(open(os.path.join(ST, '2026-11-20-hall-2016-check', 'sources', 'hall-sketchfab-metadata.json'))), ensure_ascii=False).replace('\\n', ' ')).lower()
for q in ['result from removing one golden rhombohedron from each of four vertices having tetrahedral symmetry', 'the DRT is chiral', 'fourteen such DRTs will completely enclose one in their center']:
    ok(q.lower() in HM, f'Hall quote "{q}" in the Sketchfab metadata'); need(f'"{q}"', 'Hall quote')
kc = rd('2026-11-20-hall-2016-check', 'data', 'kostick_cells.log')
ok('"distinct_panels": 354' in kc and "(4, False, 'GET A (same hand)')\": 19" in kc and '[26, 6, 4]' in kc and '[25, 6, 4]' in kc, 'Kostick concavo')
for s in ['354 panels', '19 cells, each showing 25 or 26 of its 30 faces']: need(s, 'Kostick')
for q in ['dimples oriented about z-axis, so as to fill space in a directional way', 'a set of 3 parallel zones indicated as blue bands']:
    ok(q in HR or q in rd('2026-11-20-palomar-grunbaum', 'README.md') or q in rd(K, 'README.md'), f'Kostick quote {q}'); need(q, 'Kostick quote')
IR = rd('2026-11-17-inchbald-check', 'README.md'); ok('160 tilings' in IR and '0: 4, 1: 92, 2: 60, 3: 4' in IR, 'Inchbald 160'); need('160 tilings of T', 'Inchbald')
ok('31 Mar 2022' in IR and '23 Mar 2023' in IR, 'Inchbald archive dates')
MR = rd('2026-11-17-get-mixing', 'README.md')
ok('the 17 cells of a fine tiling of T' in MR and 'the exact overlap volume with each of its 14 lattice translates within 2R is 0' in MR, 'mixing exact tiling')
need('17 cells of a tiling of T less one corner cell', 'mixing'); need('each of its 14 lattice translates within reach is 0', 'mixing')
ER = rd('2026-11-15-echo-shapes', 'README.md')
ok('40,052 paths and 42,805 valid surfaces' in ER and '450,172 have every zone of exactly 14 faces' in ER and 'Lemmens–Seidel 1973' in ER, 'echo')
need('42,805 valid surfaces', 'echo'); need('450,172 surfaces', 'echo')
# ---- Lean (study 2026-11-20-palomar-grunbaum) ----
PG = '2026-11-20-palomar-grunbaum'; PR = rd(PG, 'README.md')
ok('The library is the 23 modules of `lean-B/GET`, 3,806 lines' in PR and '435 cone-separation normals' in PR and 'c₀ = (0, φ, 1 + φ)' in PR, 'Lean README facts')
for s in ['23 modules and 3,806 lines', '435 normals', '(0, φ, 1 + φ)', '46,286 declarations', 'Your solution is okay!']: need(s, 'Lean')
lg = os.path.join(ST, PG, 'package', 'logs')
ok(open(os.path.join(lg, 'axioms.log')).read().count('[propext, Classical.choice, Quot.sound]') == 4, 'axioms of the four theorems')
ok('Your solution is okay!' in open(os.path.join(lg, 'comparator-judge-lean.log')).read(), 'comparator')
ok('accepted 46286 declarations' in open(os.path.join(lg, 'comparator-kernel-conron.log')).read(), 'con-ron')
CH = open(os.path.join(ST, PG, 'package', 'Challenge', 'GrunbaumK10.lean'), encoding='utf-8').read()
for frag in ['IsSphericalPolyhedron P F ∧ IsRhombicMonohedral F ∧ (∀ i, (F i).IsGoldenRhombus) ∧', 'EveryZoneHas F 10 ∧ LinearIndependent ℝ b ∧ TilesByTranslates P (lattice b) ∧',
             'IsSphericalPolyhedron P F ∧ IsRhombicMonohedral F ∧ EveryZoneHas F 10 ∧ IsParallelohedron P']:
    ok(frag in CH, f'Challenge has "{frag}"'); need(frag, 'Lean statement as printed')
ok(len(os.listdir(os.path.join(ST, PG, 'package', 'lean-B', 'GET'))) == 23, '23 modules on disk')
# ---- Grünbaum's words, against the library copy of his author's version (when present) ----
pdf = os.path.join(LIB, 'Grunbaum-2010-Bilinski-dodecahedron-v2-3-10.pdf')
Q = [('11', 'polyhedra with surface homeomorphic to a sphere and adjacent faces not coplanar'),
     ('15', 'None of the other isozonohedra obtainable by indentation of F or T seem to be parallelohedra.'),
     ('17', 'Given an even integer k ≥ 4, is there a rhombic monohedral parallelohedron such that every zone has exactly k faces?'),
     ('17', 'The cube has k = 4, the rhombic dodecahedra K and B have k = 6, and the doubly indented icosahedra D1 and D2 are examples with k = 8. No information is available for any k ≥ 10.')]
for pg, q in Q:
    need(q.rstrip('.') if q.endswith('parallelohedra.') else q, 'Grünbaum quote')
    if os.path.exists(pdf):
        page = re.sub(r'\s+', ' ', subprocess.run(['pdftotext', '-f', pg, '-l', pg, pdf, '-'], capture_output=True, text=True).stdout)
        ok(q in page, f'Grünbaum p. {pg}: "{q[:40]}…"')
    else: bad.append('library copy of Grünbaum 2010 not found: quotes unchecked')

# ---- further facts of the text (added 20 Nov 2026) ----
GL = open(os.path.join(H, '..', 'data', 'get-exact.log'), encoding='utf-8').read()
ok('T: F, V, E = 30, 32, 60; corners of valence [3, 5]; six zones of 10; 20 cell types, 10 prolate (volume 2 + 2φ) and 10 oblate (2φ)' in GL, 'T facts')
need('32 corners (20 where three faces meet, 12 where five meet) and six zones of 10', 'T corners'); need('10 prolate and 10 oblate', 'T cells')
ok('side² = φ + 2, diagonals 2 and 2φ, for all 15 pairs of axes' in GL, 'rhombus'); need('side √(φ + 2) and diagonals 2 and 2φ', 'rhombus')
ok('symmetries of the six-axis star: 120 (60 rotations)' in GL, '120 / 60')
ok(GL.count('T + t keeps 18 faces') == 3, '18 faces kept'); need('keeps 18 of its faces', '18 kept')
ok(GL.count('14 face neighbours') == 3, '14 neighbours'); need('There are 14 such neighbour vectors', '14')
ok('T has 5 inscribed cubes on its 20 three-valent corners' in GL, '5 cubes'); need('one of the five cubes inscribed in T on its 20 three-face corners', 'cubes')
for n in ('GET A', 'GET B'):
    ok(sorted(set(X[n]['stats']['normal_angles'])) == [36, 72, 108], f'{n} angles 36 72 108')
need('meet at 36°, 72° or 108°, never at 0°', 'angles')
ok(sorted(X['GET A']['cell_types'] + X['GET A']['missing']) == sorted(''.join(map(str, c)) for c in __import__('itertools').combinations(range(6), 3)), '16 + 4 = 20 types')
ok(all(sum(str(a) in t for t in X['GET A']['missing']) == 2 for a in range(6)), 'every axis in two missing types'); need('every axis occurs in exactly two of these types', 'axes')
# Theorem 10: every sign-coherent survivor has |p| = 1 on 16 types and 0 on four types that are oblate (in its own star)
VC = json.load(open(os.path.join(ST, K, 'data', 'vclass3.json')))
P2 = lambda a, b: (a[0] * b[0] + a[1] * b[1], a[0] * b[1] + a[1] * b[0] + a[1] * b[1])   # (x + yφ)(u + vφ), φ² = φ + 1
def det3(M):
    t = (0, 0)
    for (i, j, k), sg in [((0, 1, 2), 1), ((1, 2, 0), 1), ((2, 0, 1), 1), ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 0, 2), -1)]:
        q = P2(P2(M[0][i], M[1][j]), M[2][k]); t = (t[0] + sg * q[0], t[1] + sg * q[1])
    return t
AX = [[(1, 0), (0, 1), (0, 0)], [(-1, 0), (0, 1), (0, 0)], [(0, 0), (1, 0), (0, 1)], [(0, 0), (-1, 0), (0, 1)], [(0, 1), (0, 0), (1, 0)], [(0, -1), (0, 0), (1, 0)]]
tw = lambda z: (z[0] + z[1], -z[1])                      # √5 → −√5: φ → 1 − φ
import itertools as IT
def oblate(t, twin):
    # |det| of the three axes (of the twin star for twin survivors: tw rewrites each coordinate x + yφ as x + yφ', back in
    # the basis 1, φ); used only to tell the two volumes of a star apart (the smaller is the oblate one)
    d = det3([[tw(z) if twin else z for z in AX[i]] for i in map(int, t)])
    return abs(d[0] + d[1] * (1 + 5 ** .5) / 2)
nsurv = 0
for sv in VC['6']['survivors']:
    cells = sv.get('golden_cells') if sv.get('golden') else sv.get('twin_cells'); twin = not sv.get('golden')
    if cells is None: continue
    nsurv += 1; types = [''.join(map(str, c)) for c in IT.combinations(range(6), 3)]
    miss = [t for t in types if not cells.get(t)]
    vols = {t: oblate(t, twin) for t in types}; small = min(vols.values())
    ok(len(cells) == 16 and set(cells.values()) == {1} and len(miss) == 4, 'Theorem 10: 16 types, count 1')
    ok(all(abs(vols[t] - small) < 1e-9 for t in miss), 'Theorem 10: the four missing types are oblate in their star')
ok(nsurv == 8, 'Theorem 10: 8 survivors read')
# dates and other facts of the sources
for q in ['28 June 2016', '3 April 2022']: need(q, 'source dates')
ok('published 28 June 2016' in HR and '3 April 2022' in HR, 'Hall and Kostick dates in the Hall study')
ok('updated 6 December 2024' in rd(PG, 'package', 'palomar', 'formalization.yaml'), 'Inchbald update date'); need('updated 6 December 2024', 'Inchbald')
ok('These five are his only dimpled-triacontahedron models' in HR, 'Hall five models'); need("Hall's five dimpled models", 'Hall five')
ok(PR.count('rejected') >= 1 and '(a) `EveryZoneHas F 10` → `12`' in PR and '(c) the proof of `grunbaum_k10` replaced by `sorry`' in PR, 'three altered copies'); need('Three altered copies, with 12 in place of 10', 'negative controls')
ok('NanoDa:** run directly' in PR and 'Result: **accepts**' in PR, 'NanoDa accepts')
ok(len(re.findall(r'^theorem ', CH, re.M)) == 4 and 'cube_everyZoneHas' in CH and 'rhombicDodecahedron_everyZoneHas' in CH, 'four theorems, two calibrations'); need('The four theorems depend only on the axioms', 'four'); need('two calibration theorems', 'calibration')
ok('depth=12' in s6, 'search depth 12'); need('To depth 12 there are 4,827 classes', 'depth 12')
ok('no surface with every zone of 12 faces arises in up to 3 layers' in ER and '450,172 surfaces have every zone of 14 faces' in ER and 'k = 14 in up to 2 layers' in ER, 'echo layers')
need('in up to 3 layers (42,805 valid surfaces', 'echo'); need('in up to 2 layers 450,172 surfaces', 'echo')
ok('cos = 1/√5' in ER, 'echo cos'); need('cos = 1/√5', 'echo')
SUP = 'however, multiple indentations lead to a considerable number of polyhedra, which have not been examined in detail'
need('"multiple indentations lead to a considerable number of polyhedra, which have not been examined in detail" [2]', 'Supplement quote')
ok(SUP in open(os.path.join(H, '..', 'data', 'supplement-quote.txt'), encoding='utf-8').read(), 'Supplement quote in the extracted sentence (data/supplement-quote.txt)')


need('absent on 31 March 2022 and present on 23 March 2023', 'Inchbald archive dates')
ok('for all 15 pairs of axes' in GL and all(len(X[n]['neighbour_vectors']) == 14 for n in ('GET A', 'GET B')), '15 pair types, 14 neighbours')
need('each of the 15 pair types ij occurs on exactly two faces', '15 pairs'); need('the 15 vectors generate Λ (index 1)', '15 vectors')
ok(RK.startswith('# Grünbaum\'s zone question at k = 10 (15 November 2026)') and '(20 November 2026)' in HR.splitlines()[0], 'search dates 15 to 20 November')
need('(15 to 20 November 2026; free routes only)', 'search dates')
# ---- sweep: every number of the body (abstract to the end of §12, tables and captions included) must sit inside a checked
# string above, or be a year or page of a cited source (checked against the reference list) ----
body = re.sub(r'<h2>\d+\. ', '<h2>', raw[raw.index('<div class="abstract">'):raw.index('<h2>Data and reproducibility')])
bt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body)).replace('&amp;', '&')
bt = re.sub(r'(Theorems?|Lemmas?|Propositions?|Corollary|Figures?|Table|§|Ch\.|Chapter|k =|n =|pp?\.)\s*\d+(\s*\([a-z]+\))?((,| and|–)\s*\d+(\s*\([a-z]+\))?)*', ' ', bt)
bt = re.sub(r'\[[\d, –]+\]', ' ', bt); bt = re.sub(r'20\d\d-\d\d-\d\d-[\w-]+', ' ', bt)
refs = raw[raw.index('<h2>References'):]
YEARS = {'1885', '1954', '1960', '1972', '1973', '1976', '1980', '1984', '2004', '2009', '2010', '2016', '2022', '2023', '2024', '2025', '2026'}
pool = ' | '.join(NEEDS)
for m in re.finditer(r'(?<![\w.,])\d+(?:,\d{3})*(?![\w])', bt):
    tok = m.group(0)
    if re.search(r'(?<![\d,])' + re.escape(tok) + r'(?![\d,])', pool): continue
    if tok in YEARS and tok in refs + txt[:txt.find('References')]: continue
    bad.append(f'number not checked: "{tok}" in "…{bt[max(0, m.start() - 40):m.end() + 20]}…"')

print('\n'.join(bad) if bad else 'AUDIT OK: every number and quote checked against the studies\' data')
