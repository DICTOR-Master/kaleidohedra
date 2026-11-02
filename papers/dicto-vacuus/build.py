# Paper #87 DICTO Vacuus Solids (DRAFT): builds paper.html and figures/ from the two studies.
# Usage: python3 build.py   (then print with print.mjs on dicto-big-brother, ~/kres-tmp/cw-print)
import json, html, os, shutil, math
HERE = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(HERE, '../../studies/2026-11-02-dicto-vacuus')
OR = os.path.join(HERE, '../../studies/2026-11-02-vacuus-origami')
FIG = os.path.join(HERE, 'figures'); os.makedirs(FIG, exist_ok=True)
E = html.escape
C = json.load(open(os.path.join(ST, 'data/vacuus-census.json'))); ROWS = C['rows']
BY = {r['src'][:-5]: r for r in ROWS}

def short(n):
    n = n.replace('DICTO ', '').split(' (')[0]
    return {'Truncated-Icosahedral Hecatodihedron': 'DICTO Hecatodihedron', 'GTI': 'DICTO GTI', 'Ogdoecontahedron': 'DICTO Ogdoecontahedron (OG)'}.get(n, n)

# ---------- the one table ----------
TAB = [('dodecahedron', 'Dodecahedron'), ('icosahedron', 'Icosahedron'), ('cube', 'Cube'), ('tetrahedron', 'Tetrahedron'), ('octahedron', 'Octahedron'),
       ('cuboctahedron', 'Cuboctahedron'), ('dicto-shadow-17', 'Kagemusha'), ('dicto-lion', 'Lion'), ('dicto-david', 'David'), ('dicto-delilah', 'Delilah'),
       ('dicto-ogdoecontahedron', 'DICTO Ogdoecontahedron (OG)'), ('dicto-cube-pearl', 'Cube Pearl'), ('dicto-golden-clasp', 'Golden Clasp'),
       ('dicto-ti-star-core', 'TI Star core'), ('dicto-gti', 'DICTO GTI'), ('dicto-goliath', 'Goliath'), ('dicto-icosaxes', 'Icosaxes'),
       ('dicto-unborn-axes', 'Unborn Axes'), ('dicto-white-knight', 'White Knight'), ('dicto-blockhead', 'Blockhead'), ('dicto-dodecaxes', 'Dodecaxes'),
       ('dicto-lotus-hexa', 'Lotus Hexa')]
def pif(x):
    p, q = x.split('/')
    return ('π' if p == '1' else p + 'π') + '/' + q
def notes(r):
    f = []
    if not r['well_defined']: f.append(f'not defined: O outside {r["faces_O_not_inside"]} face planes')
    if r['all_congruent']: f.append('Isofin')
    if r['central_discs']: f.append('Disc: ' + ', '.join(f'{v} × {k}-fin disc' for k, v in r['central_discs'].items()))
    if r['family'] == 'DICTO Solids v7' and r['strut_lengths'] == 1 and r['well_defined']: f.append('One-Strut')
    if r['apex_rational']: f.append('apex ' + ', '.join(pif(x) for x in r['apex_rational']) + ('' if r['exact'] else ' (float64)'))
    if r['right']: f.append('right-angled fins')
    if r['convex'] is False: f.append('non-convex')
    return '; '.join(f)
rows = ''
for slug, nm in TAB:
    r = BY[slug]; ap = r['apex_deg']
    aps = f'{ap[0]:.2f}' if len(ap) == 1 else f'{ap[0]:.2f}–{ap[-1]:.2f}'
    fld = {'Q': 'Q', 'Q(sqrt(5))': 'Q(√5)', 'Q(sqrt(2))': 'Q(√2)', 'Q(sqrt(3))': 'Q(√3)'}.get(r['field'], 'float64')
    D = (r['D'] or '').replace('U5; W2', '')
    rows += (f"<tr><td>{E(nm)}</td><td>{E(D)}</td><td>{fld}</td><td class=n>{r['E']}</td><td class=n>{r['fin_classes']}</td><td class=n>{aps}</td>"
             f"<td class=n>{r['V']}</td><td class=n>{r['strut_lengths']}</td><td class=n>{r['edge_lengths']}</td><td class=n>{r['frame_lengths']}</td><td>{notes(r)}</td></tr>")

# ---------- plates ----------
PL = [('dodecahedron', 'Dodecahedron'), ('icosahedron', 'Icosahedron'), ('cube', 'Cube'), ('tetrahedron', 'Tetrahedron'), ('octahedron', 'Octahedron'),
      ('dicto-shadow-17', 'Kagemusha (D86)'), ('dicto-lion', 'Lion (D87)'), ('dicto-ogdoecontahedron', 'DICTO Ogdoecontahedron (OG, D28)'),
      ('dicto-cube-pearl', 'Cube Pearl (D106)'), ('dicto-golden-clasp', 'Golden Clasp (D107)'), ('dicto-ti-star-core', 'TI Star core (D105)')]
def sw(c): return f'<span class=sw style="background:{c}"></span>'
plates = ''
for i, (slug, nm) in enumerate(PL, 1):
    r = BY[slug]; col = json.load(open(os.path.join(ST, 'renders', slug + '.colours.json')))
    shutil.copy(os.path.join(ST, 'renders', slug + '.png'), os.path.join(FIG, 'plate-' + slug + '.png'))
    fins = '; '.join(f"{sw(col['fin_colours'][j])}{c['count']} × apex {c['apex_deg']:.2f}°" + (f" (= {pif(c['apex_rational_pi'])})" if c['apex_rational_pi'] else '')
                     + (f", right angle at {'O' if c['right_angle'] == ['O'] else 'a corner'}" if c['right_angle'] else '') for j, c in enumerate(r['classes']))
    Lmax = max(math.sqrt(s['L2']) for s in r['strut_classes'])
    st = '; '.join(f"{sw(col['strut_colours'][j])}{s['count']} × {math.sqrt(s['L2']) / Lmax:.4f} R" for j, s in enumerate(r['strut_classes']))
    ex = ''
    if r['central_discs']: ex = ' Central discs: ' + ', '.join(f'{v} flat disc{"s" if v > 1 else ""} of {k} fins' for k, v in r['central_discs'].items()) + '.'
    plates += (f'<figure class=pl><img src="figures/plate-{slug}.png" alt="{E(nm)}: Vacuus as sheets and as struts"><figcaption><b>Plate {i}. {E(nm)}</b>: {r["E"]} fins, {r["V"]} struts.'
               f' Left, SHEETS: {fins}. Right, STRUTS: {st} (R = the longest strut); grey: the {r["E"]} edges of the solid in {r["edge_lengths"]} length{"s" if r["edge_lengths"] > 1 else ""}.{ex}</figcaption></figure>\n')
for slug in ['cube', 'dicto-shadow-17']:
    shutil.copy(os.path.join(OR, 'renders', slug + '.png'), os.path.join(FIG, 'origami-' + slug + '.png'))

n_all = len(ROWS); n_d = sum(r['family'] == 'DICTO Solids v7' for r in ROWS)
assert (n_all, n_d) == (100, 69)
one_strut = [short(r['name']) for r in ROWS if r['family'] == 'DICTO Solids v7' and r['strut_lengths'] == 1]
frame3 = [short(r['name']) for r in ROWS if r['family'] == 'DICTO Solids v7' and r['frame_lengths'] <= 3]
iso = [r['name'] for r in ROWS if r['all_congruent']]
assert len(one_strut) == 12 and len(frame3) == 9 and len(iso) == 21, (one_strut, frame3, iso)
assert [r['name'] for r in ROWS if r['frame_lengths'] == 1] == ['Cuboctahedron']
assert [r['name'] for r in ROWS if not r['well_defined']] == ['Lotus Hexa']
assert sum(r['exact'] for r in ROWS) == 92

T = open(os.path.join(HERE, 'paper.src.html')).read()
T = T.replace('{{ROWS}}', rows).replace('{{PLATES}}', plates).replace('{{ONE_STRUT}}', ', '.join(sorted(one_strut))).replace('{{FRAME3}}', ', '.join(sorted(frame3)))
open(os.path.join(HERE, 'paper.html'), 'w').write(T); print('paper.html', len(T))
