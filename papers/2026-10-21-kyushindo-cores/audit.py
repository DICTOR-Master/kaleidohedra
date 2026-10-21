# DICTO 2026-10-21: number audit of the Kyushindo Cores paper against the exact logs and data of the four studies, and arithmetic.
#   python3 audit.py <kres/studies>
import sys, os, re, json
from fractions import Fraction as F
from math import lcm
from decimal import Decimal, getcontext
getcontext().prec = 60
S = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'paper.src.html')).read(); txt = re.sub(r'<[^>]+>', ' ', src); import html as _h; txt = _h.unescape(re.sub(r'\s+', ' ', txt))
rd = lambda p: open(os.path.join(S, p)).read(); js = lambda p: json.load(open(os.path.join(S, p)))
bad = 0
def chk(c, m):
    global bad; print(('PASS ' if c else 'FAIL ') + m); bad += (not c)
def parse(s):
    if '|' in s: a, b = s.split('|')
    else: a, b = s[:-2].rsplit('+', 1)
    return F(a), F(b)
def val(s): a, b = parse(s); return Decimal(a.numerator) / a.denominator + Decimal(b.numerator) / b.denominator * Decimal(5).sqrt()
def ex(s):
    a, b = parse(s); d = lcm(a.denominator, b.denominator); A, B = int(a * d), int(b * d)
    if B == 0: core = f'{A}'.replace('-', '−'); return core if d == 1 else f'{core}/{d}'
    t = f'{A} {"+" if B > 0 else "−"} {abs(B) if abs(B) != 1 else ""}√5'.replace('-', '−')
    return t if d == 1 else f'({t})/{d}'
fl = lambda s, n: f'{val(s):.{n}f}'
inn = lambda s: s in txt
TS, PO, GO = 'tower-shells-exact', 'polar-exact', 'golden-exact'
L = {k: rd(p) for k, p in [('t', '2026-10-20-cleo-towers/tower-shells-exact.log'), ('p', '2026-10-20-cleo-towers/polar-exact.log'), ('o', '2026-10-20-og-spires/og-spires-exact.log'),
     ('r', '2026-10-20-ott-rays/ott-rays-exact.log'), ('q', '2026-10-20-ott-rays/ott-og-planes.log'), ('g', '2026-10-21-og-turned-out/golden-exact.log'),
     ('b', '2026-10-21-og-turned-out/golden-orbits.log'), ('c8', '2026-10-19-og-gyrated-octet/cut8-exact.log')]}
# 1. the logs and the PASS counts quoted in Data and reproducibility
want = {'t': 6, 'p': 8, 'o': 7, 'r': 5, 'q': 4, 'b': 6}
for k, n in want.items(): chk(L[k].count('PASS') == n and 'FAIL' not in L[k], f'log {k}: {n} PASS, no FAIL')
chk(L['g'].count('PASS') == 15 and L['g'].count('FAIL') == 1 and 'FAIL shell phi TPH -> phi^2 TQH' in L['g'], 'golden-exact.log: 15 PASS + the one FAIL line (shell 2, one shape per kind)')
for s in ['6 PASS', '8 PASS', '7 PASS', '5 PASS', '4 PASS', '15 PASS and one FAIL line']: chk(inn(s), f'text quotes "{s}"')
# 2. Cleo Towers: Table 1 from tower-shells-exact.json
T = js('2026-10-20-cleo-towers/tower-shells-exact.json')
chk(T['beats'] == [1, 1, 2, 3, 5] and 'one turn of four beats returns the icosidodecahedron exactly 10/phi^4 larger' in L['t'], 'beats 1,1,2,3,5; one turn = c x ID')
chk(abs(Decimal(35) - 15 * Decimal(5).sqrt() - Decimal(10) / ((1 + Decimal(5).sqrt()) / 2) ** 4) < Decimal('1e-40') and inn('c = 10/φ⁴ = 35 − 15√5 ≈ 1.459'), 'c = 10/phi^4 = 35 - 15 sqrt5')
cnt = [sum(s['pieces'].values()) for s in T['shells']]
chk(cnt == [32, 30, 32, 32, 60] and sum(cnt) == 186 and inn('32, 30, 32, 32 and 60 towers, 186 in all'), f'Cleo tower counts {cnt}')
short = lambda s: len(ex(s)) < 30   # longer exact values are given as floats, exact in the json
for i, s in enumerate(T['shells']):
    chk(s['sum_equals_gap_exactly'] and s['one_volume_per_kind'] and all(s['one_symmetry_orbit_per_kind'].values()), f'Cleo shell {i + 1}: exact sum, one shape per kind')
    g = s['gap']; chk(inn(('' if not short(g) else ex(g) + ' ') + '≈ ' + fl(g, 4)), f'Cleo shell {i + 1} volume {fl(g, 4)}' + (f' = {ex(g)}' if short(g) else ''))
    for k, (v,) in s['exact_volumes'].items():
        chk(inn(f"{s['pieces'][k]} on") and inn(('' if not short(v) else ex(v) + ' ') + '≈ ' + fl(v, 6)), f'Cleo shell {i + 1} tower {k}: {fl(v, 6)}' + (f' = {ex(v)}' if short(v) else ''))
chk(T['shells'][2]['pieces'] == {'on 6-gon': 20, 'on 5-gon': 12} and T['shells'][4]['pieces'] == {'on 3-gon': 60}, 'shell 3 on GTI hexagons/pentagons, shell 5 on FPD triangles')
c = (35 - 15 * Decimal(5).sqrt()); chk(f'{c ** 3:.2f}' == '3.11' and inn('c³ ≈ 3.11'), 'c^3 = 3.11')
# 3. Polar Cleo Towers
P = js('2026-10-20-cleo-towers/polar-exact.json')
chk(P['rho2'] == '15+-5r5' and inn('ρ² = 15 − 5√5 = c·φ²') and "= (10/phi^4) * phi^2" in L['p'], 'rho^2 = 15 - 5 sqrt5 = c phi^2')
chk(P['polar'] == {'ID': 'RT c^1', 'RT': 'ID c^1', 'GTI': 'FPD', 'FPD': 'GTI', 'ID c^1': 'RT', 'RT c^1': 'ID'}, 'polar(beat k) = beat 5 - k, k = 0..5')
chk("0 | 1 | 2 | 4 | 7 | 12 go to -7 | -2 | 1 | 3 | 4 | 5" in L['p'] and inn('0 | 1 | 2 | 4 | 7 | 12') and inn('5 | 4 | 3 | 1 | −2 | −7') and inn('5, 3, 2, 1 and 1 beats'), 'Fibonacci boundaries and their polar')
cnt = [sum(s['pieces'].values()) for s in P['shells']]
chk(cnt == [30, 32, 30, 60, 32] and sum(cnt) == 184 and inn('30, 32, 30, 60 and 32 towers, 184 in all'), f'polar tower counts {cnt}')
for i, s in enumerate(P['shells']):
    chk(s['sum_equals_gap_exactly'] and s['one_volume_per_kind'] and all(s['one_symmetry_orbit_per_kind'].values()), f'polar shell {i + 1}: exact sum, one shape per kind')
    g = s['gap']; chk(inn(ex(g) + ' ≈ ' + fl(g, 4)), f'polar shell {i + 1} volume {ex(g)}')
    for k, (v,) in s['exact_volumes'].items(): chk(inn(ex(v) + ' ≈ ' + fl(v, 6)), f'polar shell {i + 1} tower {k}: {ex(v)}')
c3 = (F(35), F(-15)); m = lambda x, y: (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]); c3 = m(m(c3, c3), c3)
for k in ['on 3-gon', 'on 5-gon']:
    a = parse(T['shells'][0]['exact_volumes'][k][0]); b = parse(P['shells'][4]['exact_volumes'][k][0]); chk(m(a, c3) == b, f'polar shell 5 tower {k} = c^3 x Cleo shell 1 tower, exactly')
chk(P['shells'][3]['gap'] == '1557500/9+-696500/9r5', 'polar shell 4 = the FPD -> ID c shell of #38 (gap (1557500 - 696500 sqrt5)/9, as in #38 Table 2)')
# 4. OG core of 80 Aktis
O = js('2026-10-20-og-spires/og-spires-exact.json')
for key, n in [('OG', 6), ('hex_spire', 6), ('kite_spire', 6)]: chk(inn(ex(O[key]) + ' ≈ ' + fl(O[key], n)), f'{key} {ex(O[key])}')
for key in ['hex_height2', 'kite_height2']: chk(inn(f'√({ex(O[key])})') and inn(f'≈ {val(O[key]).sqrt():.6f}'), f'{key}: sqrt({ex(O[key])}) = {val(O[key]).sqrt():.6f}')
chk(inn(ex(O['hex_share']) + ' ≈ 52.99%') and inn(ex(O['kite_share']) + ' ≈ 47.01%') and f"{val(O['hex_share']) * 100:.2f}" == '52.99' and f"{val(O['kite_share']) * 100:.2f}" == '47.01', 'shares 52.99% / 47.01%')
chk('102 corners' in L['o'] and '20 hexagons and 60 kites' in L['o'] and '180 shared edges' in L['o'] and 'first 60 pairs' in L['o'] and 'one shape' in L['o'], 'OG 102 corners, 20 + 60, 180 neighbours, 60 checked, one shape each')
chk(val(O['kite_height2']) > val(O['hex_height2']), 'Deltoid Aktis taller than Hex Aktis')
# 5. OTT core
R = js('2026-10-20-ott-rays/ott-rays-exact.json')
chk('24 corners, 38 faces' in L['r'] and 'volume -608/81|320/81 (1.327676), as in #37a' in L['r'] and inn('(−608 + 320√5)/81 ≈ 1.327676'), 'OTT 24 corners, 38 faces, volume')
chk('38 faces {3: 32, 4: 6}' in L['c8'] and '24 half-rhombus triangles' in L['c8'] and 'pyritohedral group Th' in L['c8'] and 'the OG lies inside' in L['c8'], 'OTT faces 8 + 24 + 6, Th, the OG inside (cut8-exact.log)')
for kd, nm in zip(R['kinds'], ['Oktaktis', 'Triaktis', 'Tetraktis']):   # DICTO's names
    chk(inn(f"{kd['count']} {nm}") and inn(ex(kd['volume']) + ' ≈ ' + fl(kd['volume'], 6)) and inn(f"{kd['height']:.4f}") and inn(f"{kd['share'] * 100:.2f}%"),
        f"{kd['count']} {nm}: {ex(kd['volume'])}, height {kd['height']:.4f}, {kd['share'] * 100:.2f}%")
chk([(k['count'], k['sides']) for k in R['kinds']] == [(8, 3), (24, 3), (6, 4)] and R['octahedral_ray_is_cleo_icos'] and 'are Cleo-Icos (similar exactly)' in L['r'], 'kinds 8/24/6; Oktaktis are Cleo-Icos')
chk(inn('The Oktaktis are Cleo-Icos') and inn('Tetraktis (four-sided, on the whole rhombi)') and not inn('triangle ray') and not inn('octahedral ray'), 'OTT ray names used throughout')
chk('lies in one hexagon plane of the OG, exactly' in L['q'] and abs(val(O['hex_height2']).sqrt() - Decimal(R['kinds'][0]['height'])) < Decimal('1e-12'), 'OTT octahedral cuts in OG hexagon planes; heights equal')
# 6. OG turned out
G = js('2026-10-21-og-turned-out/golden-exact.json')
nm = ['OG', 'phi TPH', 'phi^2 TQH', 'phi^3 TQP', 'phi^4 TQHD']
chk([G['solids'][k]['corners'] for k in nm] == [102, 80, 132, 140, 162] and all(G['solids'][k]['symmetric'] for k in nm), 'corners 102, 80, 132, 140, 162; symmetric')
for k in nm: chk(inn(', '.join(f'{r:.6f}' for r in G['solids'][k]['corner_radii_float'])), f'{k} radii {G["solids"][k]["corner_radii_float"]}')
chk(L['g'].count('lies inside') == 4 and L['g'].count('corners = the flipped spire tips (phi x foot points) exactly') == 4, 'each solid inside the next; corners = flipped tips (4 + 4)')
rm = [max(G['solids'][k]['corner_radii_float']) for k in nm]; ratios = [f'{b / a:.2f}' for a, b in zip(rm, rm[1:])]
chk(ratios == ['1.52', '1.53', '1.61', '1.51'] and inn('1.52, 1.53, 1.61 and 1.51'), f'outer radius ratios {ratios}')
cnt = [sum(s['pieces'].values()) for s in G['shells']]
chk(cnt == [80, 132, 140] and inn('80, 132 and 140 towers') and inn('2, 3 and 3 shapes'), f'golden towers {cnt}')
chk(all(s['sum_equals_gap_exactly'] for s in G['shells']), 'golden shells: sums exact')
for i, s in enumerate(G['shells']):
    chk(inn(fl(s['gap'], 4)), f"golden shell {i + 1} volume {fl(s['gap'], 4)}")
    for k, vs in s['exact_volumes'].items():
        for v in vs: chk(inn(fl(v, 6)), f'golden shell {i + 1} tower {k} {fl(v, 6)}')
chk(inn(ex(G['shells'][0]['exact_volumes']['on 6-gon'][0])), 'shell 1 hexagon tower exact in text')
B = js('2026-10-21-og-turned-out/golden-orbits.json')
chk([(o['sides'], o['faces'], len(o['volumes'])) for o in B['orbits']] == [(3, 60, 1), (3, 60, 1), (5, 12, 1)] and B['gap'] == G['shells'][1]['gap'], 'shell 2: orbits 60 + 60 + 12, one volume each (3 shapes)')
chk(sorted(f"{o['volume_float'][0]:.6f}" for o in B['orbits'][:2]) == sorted(fl(v, 6) for v in G['shells'][1]['exact_volumes']['on 3-gon']), 'orbit volumes = the two triangle volumes')
fj = js('2026-10-21-og-turned-out/flip-float.json')
chk([b['corners'] for b in fj[:5]] == [102, 80, 132, 140, 162] and inn('102, 80, 132, 140 and 162 corners at beats 0–4'), 'full flip (float): same corner counts beats 0-4')
fr = [fj[i + 1]['r_max'] / fj[i]['r_max'] for i in range(4)]; chk(all(1.85 < x < 2.0 for x in fr) and inn('about 1.9 per beat'), f'full flip radius ratios {[round(x, 3) for x in fr]}')
chk(inn('(pending)') and not re.search(r'beats? 5[–-]|corners at beat [5-9]', txt), 'shells 4-5 marked pending, no numbers for beats 5+')
# 6b. surface patterns and lines (section 7)
RB, SP, SL = rd('2026-10-21-og-turned-out/golden-ribbons.log'), rd('2026-10-21-og-turned-out/surface-patterns.log'), rd('2026-10-21-og-turned-out/surface-lines.log')
for nmL, lg, n in [('golden-ribbons', RB, 14), ('surface-patterns', SP, 28), ('surface-lines', SL, 12)]:
    chk(lg.count('PASS') == n and 'FAIL' not in lg and inn(f'{nmL}.log, {n} PASS'), f'{nmL}.log: {n} PASS, no FAIL, quoted')
SPJ = js('2026-10-21-og-turned-out/surface-patterns.json')['solids']; SLJ = js('2026-10-21-og-turned-out/surface-lines.json')['solids']
row = lambda nm: re.search(r'<tr><td>' + nm + r'</td><td>(.*?)</td><td>(.*?)</td></tr>', src)
ax = {5: 'five-fold', 3: 'three-fold', 2: 'two-fold'}
for nm, s in SPJ.items():
    r = row(nm); chk(r is not None, f'Table 5 row {nm}')
    faces, lines = re.sub(r'<[^>]+>', '', r.group(1)), re.sub(r'<[^>]+>', '', r.group(2))
    for k in s['kinds']:
        shp = 'rhombi' if k['shape'] == 'rhombus' else k['shape'] + 's'
        if k['groups'] == 1 and k['count'] > 1: want = f"{k['count']} {shp}, all joined"
        elif k['group_size'] == [1]: want = f"{k['count']} {shp}, apart" + (f", on the {ax[k['group_axis']]} axes" if k['group_axis'] > 1 else '')
        else: want = f"{k['count']} {shp} in {k['groups']} " + ('ribbons' if nm == 'TQH' and 'trapez' in shp else 'rings of 5' if 'trapez' in shp else 'pairs' if k['group_size'] == [2] else f"groups of {k['group_size'][0]}") + f" on the {ax[k['group_axis']]} axes"
        chk(want in faces, f'{nm}: "{want}"')
    l = SLJ[nm]; chk(lines.startswith(f"{l['edges']}; {l['directions']} directions") and l['straight_runs'] == 0, f"{nm}: {l['edges']} edges, {l['directions']} directions, no straight runs")
    fam = dict(l['family_sizes']); al = l['families_along_axes']
    for size, n in fam.items(): chk(f'{n} of {size}' in lines or f'{n} directions of {size}' in lines or (n == 15 and f'directions of {size}' in lines) or f'{l["directions"]} directions of {size}' in lines, f'{nm}: {n} families of {size}')
    chk((al.get('2', 0) == 15 and 'two-fold' in lines) or (al.get('5', 0) == 6 and 'five-fold' in lines) or ('none along an axis' in lines and set(al) == {'0'}), f'{nm}: families along axes {al}')
    chk((l['central_belts'] == 6 and '6 central belts of 10' in lines) or (l['central_belts'] == 0 and 'belt' not in lines), f"{nm}: central belts {l['central_belts']}")
chk(SPJ['OG']['kind_edges'].get('0-1') == 120 and SPJ['TQH']['kind_edges'].get('1-2') == 120, 'hexagons bordered on all six edges (OG by kites, TQH by trapezoids)')
for t in ['(38367 + 17019√5)/13448', '(6615 + 2925√5)/3362', '2.3839 and 1.9781', '0.4343', '62.15° and 117.85°', '0.3840', '23.28°']: chk(inn(t), f'ribbon value {t}')
chk('30 shared trapezoid-trapezoid edges' not in RB and 'pair up across their shorter parallel sides: 30 pairs' in RB and 'two per axis' in RB and '23.281 deg' in RB and '38367/13448+17019/13448r5 and 6615/3362+2925/3362r5 (2.3839, 1.9781), legs^2 1269/13448+567/13448r5 (0.4343), angles [62.15, 117.85], height 0.3840' in RB, 'ribbons: log facts')
chk(RB.count("each trapezoid meets [2] others; 12 groups of [5]") == 2 and "{'shorter parallel side': 0, 'longer parallel side': 0, 'leg': 60}" in RB, 'TQP, TQHD: rings of 5 joined along the legs')
chk('exactly the trapezoids\' parallel sides' in SL and 'two seams with opposite midpoints' in SL, 'TQH two-fold families = ribbon lines, two ribbons per axis')
# 6c. referee fixes (Fable, 2026-10-21)
KC = rd('2026-10-21-og-turned-out/kyushindo-checks.log')
chk(KC.count('PASS') == 13 and 'FAIL' not in KC and inn('kyushindo-checks.log, 13 PASS'), 'kyushindo-checks.log: 13 PASS')
for nm in ['ID', 'RT', 'GTI', 'FPD', 'OG', 'TPH', 'TQH', 'TQHD']: chk(f'(1) {nm}: corners cut off by T: 0 of' in KC, f'w.v <= w.w holds on {nm}')
chk('(1) TQP: corners cut off by T: 60 of 140' in KC and inn('60 of the 140 corners would be cut off') and inn('w·v ≤ w·w for every corner w of S'), 'TQP: 60 of 140 cut; condition stated')
chk(KC.count('fixed by all 60 rotations') == 3 and inn('the inner and the outer solid of every shell are each fixed by all 60 rotations'), 'all shells: inner and outer solids fixed by the 60 rotations')
chk('circumradius^2 equals the OTT triangle\'s inradius^2, 2/9|-2/27' in L['q'] and 'midpoints of the triangle\'s three edges' in L['q'] and inn('(squared, (6 − 2√5)/27)') and ex('2/9|-2/27') == '(6 − 2√5)/27', 'hexagon circumradius = triangle inradius; touching at the 3 edge midpoints')
chk(inn('60 on trapezoids') and not inn('quadrilaterals<'), 'Table 4: trapezoids')
chk(inn('DICTO noticed that the Oktaktis looks like a Cleo-Icos') and '"looks tetrahedral or Cleo-Icos"' in rd('2026-10-20-ott-rays/ott_rays_exact.py'), 'Cleo-Icos observation credited to DICTO (script comment)')
chk(all(float(r) < 1.618 for r in ratios) and inn('a little less than φ per beat'), 'growth per beat below phi')
chk(inn('261 entries') and inn('90 have a local file') and inn('13 page images') and inn('about 170 link-only entries were not searched'), 'library counts stated')
chk(inn('as convexity requires') and not inn('checked exactly; in a convex'), 'straight runs: a remark')
chk(inn('and trapezoid rings of five on the five-fold axes (TQHD), which repeat the rings of the TQP'), 'faces: TQHD repeats TQP rings')
chk(not inn('hexagonal spire') and not inn('kite spire'), 'no "hexagonal/kite spire" left in the text')
# 6d. theorems, Proposition 1, Proposition 5 / Table 6 (restructure, 2026-10-21)
NF = rd('2026-10-21-og-turned-out/nest-feet.log'); RR = rd('2026-10-21-og-turned-out/ribbons-return.log'); AH = rd('2026-10-21-og-turned-out/axis-hull.log')
AW10 = rd('2026-10-21-og-turned-out/axis-words-10.log')
PL = rd('2026-10-21-og-turned-out/polar-turned.log')
chk('30 4-gons, 60 4-gons, 60 5-gons, 12 5-gons' in PL and inn('90 four-sided faces in two kinds, 30 and 60, and 72 pentagons in two kinds, 60 and 12') and '60 3-gons, 30 4-gons, 12 5-gons' in PL, 'polar S4 and Hecatodihedron face kinds')
chk('FAIL' not in NF and 'FAIL' not in RR and 'FAIL' not in AH, 'nest-feet, ribbons-return, axis-hull logs: no FAIL')
nm_ = ['OG', 'TPH', 'TQH', 'TQP', 'TQHD'] + [f'down {k}' for k in range(5, 13)]
turned = {k: f'lies inside phi^{k} {nm_[k]} (turned out, exact)' in NF for k in range(1, 13)}
K = max(k for k in turned if turned[k]); chk(K == 8 and all(turned[k] for k in range(1, K + 1)) and inn(f'checked directly in ℚ(√5) for k ≤ {K}'), f'Corollary 1: nesting also checked exactly for k = 1..{K}')
dn = {k: re.search(rf'downward: {re.escape(nm_[k])} inside {re.escape(nm_[k - 1])}: (True|False)', NF).group(1) == 'True' for k in range(1, K + 1)}
yes = [k for k in dn if dn[k]]; chk(yes == [1, 2, 4] and inn(f'only for k = 1, 2 and 4 among k ≤ {K}'), f'downward nesting only at {yes}')
TM = json.load(open(os.path.join(S, '2026-10-21-nesting-proof/tmin-exact.json')))['k']; TL = rd('2026-10-21-nesting-proof/tmin-exact.log')
phi_ = (1 + 5 ** .5) / 2
chk(all(TM[str(k)]['t_min_le_phi_exact'] and TM[str(k)]['t_min'] < phi_ for k in range(9)) and max(TM[str(k)]['t_min'] for k in range(9)) == TM['3']['t_min'] and abs(TM['3']['t_min'] - 3 / phi_ ** 2) < 1e-12 and TM['3']['t_min_exact'] == '9/2+-3/2r5', 't_min(D_k) <= phi, k = 0..8; max at k = 3 = 3/phi^2 = (9 - 3 sqrt5)/2')
for k in range(9):
    e = TM[str(k)]; chk(inn(f"{e['t_min']:.6f}") and inn(f"+{e['phi_minus_t_min']:.4f}") and f'PASS t_min(D_{k}) =' in TL, f'Table 7 row {k}: {e["t_min"]:.6f}')
chk(abs(15 - 6 * 5 ** .5 - 1.583592) < 1e-6 and 841 < 845 and 29 ** 2 == 841 and 13 ** 2 * 5 == 845 and inn('15 − 6√5 ≈ 1.583592 &lt; φ'.replace('&lt;', '<')) and inn('29 < 13√5 (841 < 845)'), '15 - 6 sqrt5 < phi (29 < 13 sqrt5)')
CL = rd('2026-10-21-nesting-proof/covering-lemma.log')
chk('altitude from A2 onto the longest side 18.0000 deg' in CL and 'kite argument WORKS' in CL and 'A3A5 37.3774' in CL and inn('37.377°') and inn('sin 18°') and 'kite argument FAILS' in CL and inn('more than 54.74°'), 'covering lemma: 18 deg altitude, 37.377 deg, octahedral kite fails')
chk(all(f'(1.134, 1.117, 1.103, 1.146, 1.042, 1.087, 1.026, 1.060, 1.138)' in txt for _ in [0]) and [round(TM[str(k)]['t_min'], 3) for k in range(9)] == [1.134, 1.117, 1.103, 1.146, 1.042, 1.087, 1.026, 1.06, 1.138], 'Conjecture 1 evidence values')
PT = rd('2026-10-21-og-turned-out/polar-turned.log'); PJ = js('2026-10-21-og-turned-out/polar-turned.json')
chk(PT.count('PASS') == 13 and 'FAIL' not in PT and inn('polar-turned.log, 13 PASS'), 'polar-turned.log: 13 PASS')
chk(all(f'polar(S_{k}) = phi^-{k} T^{k}(Hecatodihedron) exactly' in PT for k in range(5)) and all(f'polar(S_{k}) lies inside polar(S_{k - 1})' in PT for k in range(1, 5)), 'Corollary 2 built: k <= 4 exact, nested inward')
cs = [PJ['solids'][f'polar S{k}']['corners'] for k in range(5)]; fs = [PJ['solids'][f'polar S{k}']['faces'] for k in range(5)]
chk(cs == [80, 132, 140, 162, 200] and fs == [102, 80, 132, 140, 162] and inn('80, 132, 140, 162 and 200 corners and 102, 80, 132, 140 and 162 faces'), f'polar solids corners {cs} faces {fs}')
tw = [x['towers'] for x in PJ['shells']]; shp = [len(x['orbits']) for x in PJ['shells']]
chk(tw == [80, 132, 162] and shp == [2, 3, 4] and all(x['sum_equals_gap_exactly'] and x['one_volume_per_orbit'] for x in PJ['shells']) and inn('80, 132 and 162 in 2, 3 and 4 shapes') and inn('hold 80, 132 and 162 towers of 2, 3 and 4 shapes'), 'polar towers 80/132/162 in 2/3/4 shapes')
for x in PJ['shells']:
    chk(inn(f"{x['gap_float']:.4f}") and all(inn(f"{o['volume_float']:.6f}") for o in x['orbits']), f"Table 8 shell {x['shell']}")
chk(inn('192 of 252') and inn('260 of 320') and inn('312 of 402') and "NOTE: 60 listed points are not corners of the hull" in TL and "NOTE: 90 listed points are not corners" in TL and 'D_9: 500 corners (500 listed points), 732 faces' in TL, 'Remark: hull corners vs listed points; D_9 732 faces')
chk(inn('D<sub>10</sub> has 662 faces against 732 for D<sub>9</sub>'.replace('<sub>', '').replace('</sub>', '')) or inn('has 662 faces against 732'), 'Remark: 662 < 732')
for nm, frag in [('OG', '60 x 4-point face, foot inside; 20 x 6-point face, foot inside'), ('TPH', '120 x 3-point face, foot inside; 12 x 5-point face, foot inside'),
                 ('TQH', '60 x 3-point face, foot inside; 60 x 4-point face, foot outside; 20 x 6-point face, foot inside'),
                 ('TQP', '60 x 3-point face, foot on the boundary; 90 x 4-point face, foot inside; 12 x 5-point face, foot inside'),
                 ('TQHD', '120 x 3-point face, foot inside; 60 x 4-point face, foot outside; 20 x 6-point face, foot inside')]:
    chk(f'(a) {nm}: {frag}' in NF, f'Proposition 1: feet on {nm}')
chk(inn('On the TQH the foot points of the 60 trapezoids, the 30 ribbons of §8, lie outside their faces') and inn('On the TQP the feet of the 60 triangles lie on the edges of their faces'), 'Proposition 1 text')
W = {}
for line in (RR + AH).splitlines():
    m = re.match(r'PASS (\S+(?: \d+)?): \d+ (?:foot )?points, hull (\d+) corners, (\d+) faces; (?:axis word )?5-fold: (\w+), 3-fold: (\w+), 2-fold: (\w+)', line)
    if m: W[m.group(1)] = (int(m.group(2)), m.group(4), m.group(5), m.group(6))
KAX = max(i for i, n in enumerate(nm_) if n in W); chk(all(nm_[i] in W for i in range(KAX + 1)), f'axis words on the hull for OG..{nm_[KAX]}')
t6 = re.search(r'<table><tr><th>Axis</th>(.*?)</table>', src, re.S).group(1)
rows = {r[0]: r[1:] for r in [re.findall(r'<td>(?:<b>)?(.*?)(?:</b>)?</td>', tr) for tr in re.findall(r'<tr>(.*?)</tr>', t6)] if r}
for ax_i, axn in [(1, 'five-fold'), (2, 'three-fold'), (3, 'two-fold')]:
    chk([rows[axn][i] for i in range(KAX + 1)] == [W[nm_[i]][ax_i] for i in range(KAX + 1)], f'Table 6 {axn} row = hull words OG..{nm_[KAX]}')
w2 = [W[nm_[i]][3] for i in range(KAX + 1)]
chk(w2[:8] == ['corner', 'edge', 'edge', 'face'] * 2 and w2[8] == 'edge' and inn('for two full periods, the OG to the TQP and the TQHD to down 7') and inn('at down 8 it reads edge'), 'Observation 1: period 4 OG..down 7, edge at down 8')
chk(all(W[nm_[i]][1] == ('corner' if i % 2 == 0 else 'face') and W[nm_[i]][2] == ('face' if i % 2 == 0 else 'corner') for i in range(KAX + 1)), 'five/three-fold alternate on every solid with a hull word')
chk('down 8 (312 corners): at the two-fold axis edge meet isosceles trapezoid + isosceles trapezoid (congruent): a ribbon as on the TQH' in RR and 'down 8: 402 points, hull 312 corners' in AH and 'sharing their shorter parallel side: a ribbon as on the TQH' in AH and inn('So the ribbons of the TQH return exactly at down 8 and at down 9') and 'down 9: 500 points, hull 500 corners, 732 faces; 5-fold: face, 3-fold: corner, 2-fold: edge; at the two-fold edge: isosceles trapezoid + isosceles trapezoid (congruent), sharing their shorter parallel side: a ribbon as on the TQH' in AH, 'ribbons return at down 8 and 9')
chk('down 6 (192 corners): at the two-fold axis edge meet isosceles trapezoid + isosceles trapezoid (congruent): not a ribbon (the axis edge is their longer parallel side' in RR and inn('at down 6, two congruent isosceles trapezoids across their longer parallel sides'), 'down 6: trapezoids across their longer sides')
chk(RR.count('isosceles triangle + isosceles triangle (congruent)') == 2 and inn('At the two-fold edges of the TPH and down 5 two congruent isosceles triangles meet'), 'TPH, down 5: triangle pairs')
chk('252 foot points, hull 192 corners' in RR and '320 foot points, hull 260 corners' in RR and '402 foot points, hull 312 corners' in RR and inn('192 of 252') and inn('260 of 320') and inn('312 of 402'), 'foot points vs hull corners, down 6-8')
chk('down 10   732 corners  5-fold: corner  3-fold: face    2-fold: face' in AW10, 'axis-words-10.log: down 10 three-fold face, two-fold face')
# 7. library appendix
rows = open(os.path.join(HERE, 'lib-rows.html')).read().count('<tr>'); chk(rows == 77 and inn('77 library sources') and inn('77 distinct sources with a text layer'), f'library rows {rows}')
# 8. DOIs of earlier DICTO papers (as on the Collected Works, v17)
for d in ['23463305', '23488944', '23404688', '23457016', '23484012', '23351291', '23357896', '23345699']: chk(inn('DICTO DOI: 10.5281/zenodo.' + d), f'DOI {d}')
chk('proposal' not in txt.lower() and 'proposed' not in txt.lower(), 'no "proposal"/"proposed"')
print('ALL PASS' if bad == 0 else f'{bad} FAIL')
