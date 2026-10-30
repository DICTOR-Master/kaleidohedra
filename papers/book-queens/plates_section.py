# The Plates section of 'Alicia in Wonderland' version 3 (DICTO 2026-10-31: "full page cards/plates" to give the shapes room).
# One page per shape: the picture (plates/*.png, made on dicto-big-brother by plates/render_plates.py) and a few exact facts, all
# read from plates/plates.json (written by the same script from the DICTO solids dataset v6 and the 600-cell source model) or
# from the book's own Chapters 6 and 8. Called by assemble.py; the section sits after Chapter 8, before the epilogue.
import json, os, re, html
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(HERE, 'plates', 'plates.json'), encoding='utf8'))
CLEO = json.load(open(os.path.join(HERE, '..', '..', 'studies', '2026-10-27-white-queen-600', 'data', 'cleo_shells.json')))['shells']
DATASET_DOI = '10.5281/zenodo.23790799'
SIDES = {3: 'triangles', 4: 'four-sided faces', 5: 'pentagons', 6: 'hexagons', 7: 'seven-sided faces', 8: 'eight-sided faces',
         9: 'nine-sided faces', 10: 'decagons'}
SIDES1 = {3: 'triangle', 4: 'four-sided face', 5: 'pentagon', 6: 'hexagon', 7: 'seven-sided face', 8: 'eight-sided face',
          9: 'nine-sided face', 10: 'decagon'}


def q5(t):
    """'a + b√5' in the dataset's and the study's spellings -> (a, b) as Fractions."""
    t = t.replace('sqrt5', '√5').replace('−', '-').replace(' ', '')
    a = b = Fr(0)
    for sgn, term in re.findall(r'([+-]?)([^+-]+)', t):
        s = -1 if sgn == '-' else 1
        if '√5' in term:
            c = term.replace('√5', '')
            if c.startswith('/'): c = '1' + c          # √5/2
            b += s * (Fr(c) if c else Fr(1))
        else:
            a += s * Fr(term)
    return a, b


def q5fmt(a, b):
    """(p + q√5)/r with one denominator, as the book's tables write heights."""
    if b == 0:
        return str(a).replace('-', '−')
    r = (a.denominator * b.denominator) // __import__('math').gcd(a.denominator, b.denominator)
    p, q = int(a * r), int(b * r)
    qs = ('' if abs(q) == 1 else str(abs(q))) + '√5'
    num = (f'{p} {"+" if q > 0 else "−"} {qs}' if p else ('−' if q < 0 else '') + qs).replace('-', '−')
    return num if r == 1 else (f'({num})/{r}' if p else f'{num}/{r}')


def faces_text(fbs):
    items = sorted(((int(k), v) for k, v in fbs.items()))
    return ', '.join(f'{v} {SIDES[k] if v != 1 else SIDES1[k]}' for k, v in items)


CH = {'#63': ('6', 'The White Queen', '600-cell'), '#65': ('8', 'The Red Queen', '120-cell')}


def slice_plate(n, s):
    ch, queen, poly = CH[s['paper']]
    m = re.search(r'at height (.+?) along the ([a-z-]+) direction', s['scale_note'])
    a, b = q5(m.group(1)); direction = m.group(2)
    cut = f'{direction}, at height {q5fmt(a, b)}'
    if a == 0 and b == 0: cut += ': the central slice'
    if 'midpoint of its gap' in s['scale_note']: cut += ': in a gap between two layers of corners, cut at its midpoint'
    fv = s['f_vector']; sym = s['symmetry']
    note = re.sub(r'^[WR]\d+: ', '', s['note'])
    if s['name'] == 'Humpty Dumpty':          # the dataset row carries its correction history; the book's own words (Chapter 6)
        note = ('one of the sections drawn by Alicia Boole Stott (1900, cell-first series through the corner layers); the exact '
                'solid and the name are #63\'s and DICTO\'s; D85 is kept, as D-numbers are never reused; forced to equal edges it '
                'becomes Fallen Humpty (D102)')
    note = note[0].upper() + note[1:]
    rows = [('Cut', f'The {poly} cut {cut}'),
            ('Corners, edges, faces', f'{fv["vertices"]}, {fv["edges"]}, {fv["faces"]}'),
            ('Faces', faces_text(s['faces_by_sides'])),
            ('Symmetry', f'{sym["schoenflies"]}, order {sym["order"]}; {"convex" if s["convex"] else "non-convex"}'),
            ('Record', note + ('' if note.endswith(')') or note.endswith('.') else '') ),
            ('Source', f'Chapter {ch} (#{s["paper"][1:]}); exact model: DICTO solids dataset v6 (DICTO DOI {DATASET_DOI}), '
                       f'{s["file"]}')]
    badge = s['D'] or 'no D-number'
    return plate(n, f'{queen} · slices', ch, f'plates/slice-{s["slug"]}.png', s['name'], badge, rows,
                 f'{s["name"]}, a slice of the {poly}')


def shell_plate(n, s):
    k = s['shell']
    name = 'Cleo core' if k == 0 else ('Outer wrap' if k == 14 else f'Shell {k}')
    ex = CLEO[k]                              # the exact height from the study (cleo_shells.py), checked against the drawing's
    assert ex['cells'] == s['cells']; a, b = q5(ex['height'])
    assert abs(float(a) + float(b) * 5 ** 0.5 - s['centre_height']) < 1e-6
    what = ('Twenty Cleo-Icos filling a regular icosahedron: the 20 cells at the corner v' if k == 0 else
            'The 20 cells at the corner opposite v, wrapping all the others' if k == 14 else
            f'{s["cells"]} regular tetrahedra of the 600-cell')
    rows = [('Cells', f'{what}; all one kind as seen (by exact edge lengths, Chapter 6)'),
            ('Centre height', f'{q5fmt(a, b)} along v, in units where v stands at height 2'),
            ('So far', f'{s["so_far"]} of the 600 cells, from the core out' + ('' if k == 0 else f' (core and shells 1 to {k})' if k < 14 else ' (all)')),
            ('View', 'Perspective from an eye at height −21/10, just beyond the opposite corner; drawn at its own scale; '
                     'grey: the shells inside'),
            ('Source', 'Chapter 6, Figure 6.3 (#63)')]
    return plate(n, 'The White Queen · Cleo shells', '6', f'plates/wq-shell-{k:02d}.png', name, f'{s["cells"]} cells', rows,
                 f'{name} of the 600-cell round one corner')


WQ_HEIGHTS = {2.0: (Fr(2), Fr(0)), 1.618033989: (Fr(1, 2), Fr(1, 2)), 1.0: (Fr(1), Fr(0)), 0.618033989: (Fr(-1, 2), Fr(1, 2)), 0.0: (Fr(0), Fr(0))}


def layer_plate(n, s):
    k = s['layer']; c = s['cells']
    name = 'Core' if k == 0 else f'Layer {k}'
    h = s['centre_height']; a, b = WQ_HEIGHTS[abs(h)]
    if h < 0: a, b = -a, -b
    dod = 'dodecahedron' if c == 1 else 'dodecahedra'
    what = (f'1 regular dodecahedron of the 120-cell; cut from its centre it gives Aristotle\'s twelve pentagonal pyramids (Figure 8.1)'
            if k == 0 else f'{c} regular {dod} of the 120-cell; all one kind as seen (Chapter 8)')
    where = ('the White Queen\'s corner v' if k == 0 else 'the White Queen\'s corner opposite v' if k == 8 else
             f'the White Queen\'s {c} corners at height {q5fmt(a, b)} along v (v at height 2)')
    rows = [('Cells', what),
            ('Where', f'Round {where}: each of her corners becomes one dodecahedron, its 20 corners the centres of her 20 cells there'),
            ('So far', f'{s["so_far"]} of the 120 dodecahedra, from the core out'),
            ('View', 'Perspective from just beyond the opposite dodecahedron; drawn at its own scale; grey: the layers inside'),
            ('Source', 'Chapter 8, Figure 8.1 (#65)')]
    return plate(n, 'The Red Queen · layers of dodecahedra', '8', f'plates/rq-layer-{k}.png', name, f'{c} {dod}', rows,
                 f'{name} of the 120-cell round one dodecahedron')


def plate(n, group, ch, img, name, badge, rows, alt):
    tr = ''.join(f'<tr><td>{html.escape(k)}</td><td>{link(html.escape(v))}</td></tr>' for k, v in rows)
    return (f'<section class="plate" id="plate{n}"><div class="ph"><span>Plate {n} · {group}</span>'
            f'<span><a href="#ch{ch}">Chapter {ch}</a></span></div>'
            f'<img src="{img}" alt="{html.escape(alt)}">'
            f'<div class="pn"><h2>{html.escape(name)}</h2><span class="dn">{html.escape(badge)}</span></div>'
            f'<table class="pf">{tr}</table></section>')


def link(t):
    t = re.sub(r'#(6[35])\b', lambda m: f'<a href="#ch{"6" if m.group(1) == "63" else "8"}">#{m.group(1)}</a>', t)
    return re.sub(r'(?<![/\w])(Chapter|Chapters) (\d)\b', lambda m: f'{m.group(1)} <a href="#ch{m.group(2)}">{m.group(2)}</a>', t)


def plates_html():
    W = [s for s in F['slices'] if s['paper'] == '#63']; R = [s for s in F['slices'] if s['paper'] == '#65']
    out, toc, n = [], [], 0
    for kind, items, fn in (('wslice', W, slice_plate), ('shell', F['shells'], shell_plate), ('rslice', R, slice_plate),
                            ('layer', F['layers'], layer_plate)):
        for s in items:
            n += 1; out.append(fn(n, s))
            lab = (s['name'] + (f' ({s["D"]})' if s['D'] else '') if 'name' in s else
                   ('White Queen: ' + ('Cleo core' if s['shell'] == 0 else 'outer wrap' if s['shell'] == 14 else f'shell {s["shell"]}')) if kind == 'shell' else
                   ('Red Queen: ' + ('core' if s['layer'] == 0 else f'layer {s["layer"]}')))
            toc.append(f'<li><a href="#plate{n}">{n}</a>&ensp;{html.escape(lab)}</li>')
    nW, nS, nR, nL = len(W), len(F['shells']), len(R), len(F['layers'])
    a1, a2, a3, a4 = 1, 1 + nW, 1 + nW + nS, 1 + nW + nS + nR
    intro = f'''<section class="app plates-open"><h1 class="chapter" id="plates">Plates</h1>
<p>The plates give the shapes of Chapters 6 and 8 a page each. Plates {a1}–{a2 - 1} are the named slices of the White Queen, the 600-cell (Chapter 6); Plates {a2}–{a3 - 1} her fifteen Cleo shells (Figure 6.3); Plates {a3}–{a4 - 1} the named slices of the Red Queen, the 120-cell (Chapter 8); Plates {a4}–{a4 + nL - 1} her nine layers of dodecahedra (Figure 8.1).</p>
<p>Each slice is drawn from its exact model in the DICTO solids dataset, version 6 (DICTO DOI {DATASET_DOI}), with its faces coloured by their number of sides as in the atlases of Figures 6.1 and 8.3: triangles ivory, four-sided faces blue, pentagons red, hexagons amber, seven-sided faces green, eight-sided faces violet, nine-sided faces teal, decagons pink. Heights are measured along each direction's own vector, as in the atlases, so they compare within one direction only. The names are DICTO's, after Lewis Carroll; the D-numbers are the permanent numbers of DICTO's catalogue. Alicia, the Unicorn and the Bandersnatch, sections in Alicia Boole Stott's series of 1900, carry none; Humpty Dumpty, also one of hers, keeps the D85 it was given before this was known.</p>
<p>The shells and layers are seen in perspective, as in Figures 6.3 and 8.1, each drawn at its own scale, with the shells or layers inside the one shown in grey.</p>
<ol class="platelist">{''.join(toc)}</ol></section>'''
    return link(intro) + ''.join(out)


PLATES_CSS = '''
section.plate{break-before:page;break-inside:avoid}
.plate .ph{display:flex;justify-content:space-between;font-size:8.5pt;color:#8a7440;border-bottom:0.6pt solid #b8962e;padding-bottom:1.5mm;margin-bottom:4mm}
.plate .ph a{color:#8a7440;text-decoration:none}
.plate img{display:block;width:170mm;height:170mm;margin:0 auto}
.plate .pn{display:flex;align-items:baseline;justify-content:space-between;margin:4.5mm 0 2mm}
.plate .pn h2{font-size:22pt;margin:0;color:#111;font-weight:600}
.plate .dn{font-size:14pt;color:#b8962e;font-weight:600}
.plate table.pf{width:100%;border-collapse:collapse;font-size:9pt;line-height:1.32}
.plate table.pf td{padding:0.9mm 2mm 0.9mm 0;vertical-align:top;border-top:0.4pt solid #e4dccb}
.plate table.pf td:first-child{width:38mm;color:#6b5310;font-weight:600}
ol.platelist{list-style:none;padding:0;columns:2;column-gap:10mm;font-size:9pt;margin-top:5mm} ol.platelist li{break-inside:avoid;padding:0.5mm 0;border-bottom:1px dotted #ddd}
'''
