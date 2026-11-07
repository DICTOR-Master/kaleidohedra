# Assemble The Golden Ladder (version 2 onwards; version 6: errata and two Concordance results, see ADD and V1CORR) (DICTO 11-05: keep v1, add the remaining chapters as new versions; DICTO 11-06 "continue chapters").
# Opening: Map of the Ladder (golden-ladder-map). Chapters 1-2: as published in v1 (this folder's paper.html at v1, kept as v1.html).
# Chapters 3-8: DICTO's published papers set word for word (#20 + #48, #88, #65, #89, #90, #91); meta line replaced by a "From paper" line,
# figures copied to figures/ch<n>/ and numbered per chapter. Chapter 9: the closing chapter (golden-ladder-closing). Status boxes removed
# from all sources; one status box for the draft at the top. Output: paper.html (typeset by ../print.mjs).
import re, os, shutil, html, json
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE); ROOT = os.path.dirname(P)
V1 = os.path.join(HERE, 'v1.html')
if not os.path.exists(V1): shutil.copy(os.path.join(HERE, 'paper.html'), V1)
v1 = open(V1, encoding='utf8').read()
FUJI = os.path.join(ROOT, 'studies', '2026-10-14-fuji-family', 'paper', 'paper-house.html')
# (label, source html, paper number, published version, concept DICTO DOI)
CH = [('3A', FUJI, 20, 5, '10.5281/zenodo.23357896'),
      ('3B', os.path.join(P, '2026-10-23-golden-split', 'paper.html'), 48, None, None),
      ('4', os.path.join(P, 'golden-truncated-triangles', 'paper.html'), 88, 2, None),
      ('5', os.path.join(P, 'red-queen-120', 'paper.html'), 65, None, None),
      ('6', os.path.join(P, 'golden-cuts-beyond-plato', 'paper.html'), 89, None, None),
      ('7', os.path.join(P, 'six-dimensions-golden-cubes', 'paper.html'), 90, None, None),
      ('8', os.path.join(P, 'dual-pairs-dimensions', 'paper.html'), 91, None, None)]
styles = set()
# Book corrections (DICTO's term rule 11-02: 'truncated triangle', never 'flat-ended'; banned label 'In short.')
CORR = [('the term &quot;flat-ended triangle&quot; and the names', 'the names'), ('the term "flat-ended triangle" and the names', 'the names'),
        ('flat-ended-triangle hexagons', 'truncated-triangle hexagons'), ('flat-ended or isogonal', 'truncated-triangle (then called flat-ended) or isogonal'.replace('flat-ended', 'flat‑ended')),
        ('Flat-ended', 'Truncated'), ('flat-ended', 'truncated'), ('<b>In short.</b> ', ''), ('In short. ', '')]
# Version 6 (7 November 2026): two results routed to the book by the Concordance (waiting items 5 and 47), added after an anchor in their chapter
ADD = {'7': ('cuboctahedron (2) and cube (3).</p>', '''
<div class="thm"><b>Theorem 1A (the other golden pairs under the same swap; added in the book, Version 6).</b> Write the golden cuts of #88 as x<sub>1</sub> = φ/(k + 2φ) (greater) and x<sub>2</sub> = 1/(φk + 2) (lesser), with k = 1 for the triangle-faced solids, √2 for the cube and φ for the dodecahedron, and let σ be the swap √2 ↦ −√2, √5 ↦ −√5 of Theorem 1, DICTO's Double Vision. (a) Cube: σ(x<sub>1</sub>) = x<sub>2</sub>, the Galois twins of Theorem 1. (b) Dodecahedron: x<sub>1</sub> = 1/3, so the Greater Golden Cut Dodecahedron is its own twin; σ(x<sub>2</sub>) = (7 + √5)/22 ≈ 0.419821 is a real cut, whose new corner sides are φ<sup>3</sup> times what remains of the old sides: the twin of the Lesser Golden Cut Dodecahedron is the φ<sup>3</sup>-cut dodecahedron. (c) Tetrahedron, octahedron, icosahedron: σ(x<sub>1</sub>) = φ<sup>2</sup> and σ(x<sub>2</sub>) = 1/2 + √5/10 ≈ 0.723607 both exceed 1/2, so the corner triangles would overlap and neither twin is a solid. (d) The φ<sup>3</sup>-cut dodecahedron is not a station of the golden cycle: as a section D ∩ μD* at midsphere 1, where the icosidodecahedron is μ = 1, it sits at μ = (65 − 19√5)/22 ≈ 1.023396, against 13/6 − √5/2 ≈ 1.048633 for the greater and 35/22 − 5√5/22 ≈ 1.082712 for the lesser golden cut, and no station of the cycle (I, Cleo star, D′, ID, OG, rTI, TI, H, jtI, RT, M, I·φ<sup>3</sup>) is a truncated dodecahedron.</div>
<p><b>Proof.</b> σ(φ) = −1/φ. (a) σ turns kx = φ(1 − 2x) with k = √2 into √2x = (1 − 2x)/φ, the equation of x<sub>2</sub>. (b) With k = φ, x<sub>1</sub> = φ/(3φ) = 1/3, fixed by σ. σ(x<sub>2</sub>) = 1/(1/φ<sup>2</sup> + 2) = φ<sup>2</sup>/(2φ<sup>2</sup> + 1) = (7 + √5)/22. A pentagon cut at x keeps 1 − 2x of each side and gains corner sides φx, and φ(7 + √5)/(8 − 2√5) = 2 + √5 = φ<sup>3</sup>. (c) With k = 1, x<sub>1</sub> = φ/(1 + 2φ) = 1/φ<sup>2</sup> and x<sub>2</sub> = 1/(φ + 2); σ gives φ<sup>2</sup> and 1/(2 − 1/φ) = φ/√5 = 1/2 + √5/10. (d) At midsphere 1 the dodecahedron's corners lie at √3/φ and the icosahedron's faces at φ/√3, so a corner cut at x lies at μ = 3/φ<sup>2</sup> − 2x(3/φ<sup>2</sup> − 1) = (9 − 3√5)/2 − x(7 − 3√5), which is 1 at x = 1/2; x = 1/3, 1/(φ<sup>2</sup> + 2) and (7 + √5)/22 give the three values. The stations are those of the cycle's table (studies/2026-10-24-gnomon-cycle, gnomon-all12.txt). □</p>
<p>So the swap pairs the cube's two golden cuts with each other, fixes the dodecahedron's greater cut, sends its lesser cut to a cut with sides in the ratio φ<sup>3</sup>, and gives the triangle-faced solids no partner. The φ<sup>3</sup> of that cut and the φ<sup>3</sup> step of the golden cycle (#54) share the number only. Exact, from the study 2026-11-04-golden-twins, rechecked for this version.</p>'''),
       '8': ('and the source is credited.</p>', '''
<p><b>The Golden OGs and their prior art (added in the book, Version 6).</b> The Lesser and Greater Golden OG have the face pattern of OG: 102 corners, 180 edges and 80 faces, 20 regular hexagons and 60 kites. That pattern is known, as for OG itself: it is the dual of L0 applied to the dodecahedron in the operator notation of Rossiter's Antiprism software, and it is in McCooey's catalogue (#31, §4 and §7). The golden metric forms, at μ = √5 and μ = (13 + 6√5)/11, were not found in the sources checked (6 November 2026): Wikipedia's table of near-misses to the Johnson solids, and a web search for “polyhedron 20 regular hexagons 60 kites 102 vertices”. Like OG, the Golden OGs keep a known face pattern and are new as solids within these checks.</p>''')}
# Version 6: chapters 1-2 are set from v1.html as published; corrections applied here (Concordance erratum 24)
V1CORR = [('The Pell multiplets (0, P<sub>n</sub>, P<sub>n+1</sub>) of SO(7) converge',
           'The Pell multiplets (0, P<sub>n</sub>, Q<sub>n</sub>) of SO(7), with P<sub>n</sub> = 1, 2, 5, 12, … the Pell numbers and Q<sub>n</sub> = P<sub>n</sub> + P<sub>n−1</sub> = 1, 3, 7, 17, … (OEIS A001333), converge')]
def strip_status(b): return re.sub(r'<div class="status">.*?</div>\s*', '', b, flags=re.S)
def chapter(label, src, num, ver, doi):
    s = open(src, encoding='utf8').read(); d = os.path.dirname(src)
    for st in re.findall(r'<style>(.*?)</style>', s, re.S): styles.add(st.strip())
    zs = os.path.join(d, 'zenodo-state.json')
    if doi is None and os.path.exists(zs): doi = '10.5281/zenodo.' + str(json.load(open(zs))['conceptrecid'])
    if doi is None: doi = re.search(r'DICTO DOI: (10\.5281/zenodo\.\d+)', s).group(1)
    if ver is None:
        m = re.search(r'[Vv]ersion (\d+)', re.search(r'<div class="meta">.*?</div>', s, re.S).group(0)); ver = int(m.group(1)) if m else 1
    body = s[s.index('<h1'):s.rindex('</body>')]
    body = re.sub(r'<img class="(watermark|logo)"[^>]*>', '', body)
    title = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1)
    title = re.sub(r'<br>.*', '', title, flags=re.S).strip()
    body = re.sub(r'<div class="meta">.*?</div>', '', body, count=1, flags=re.S)
    body = strip_status(body)
    def fig(mo):
        f = mo.group(1); path = os.path.normpath(os.path.join(d, f))
        if not os.path.exists(path): raise SystemExit(f'FIG MISSING ch{label} {f}')
        dst = f'figures/ch{label}/{os.path.basename(f)}'
        os.makedirs(os.path.join(HERE, os.path.dirname(dst)), exist_ok=True); shutil.copy(path, os.path.join(HERE, dst)); return f'<img src="{dst}"'
    body = re.sub(r'<img src="([^"]+)"', fig, body)
    body = re.sub(r'\b(Figure|Fig\.|Table) (\d+)', lambda mo: f'{mo.group(1)} {label}.{mo.group(2)}', body)
    body = body.replace('this paper', 'this chapter').replace('This paper', 'This chapter')
    for x, y in CORR: body = body.replace(x, y)
    if label in ADD:
        a, add = ADD[label]; assert body.count(a) == 1, (label, a); body = body.replace(a, a + add)
    body = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 id="ch{label}">Chapter {label} · {title}</h1>', body, count=1, flags=re.S)
    m = re.search(r'</h1>\s*(<p class="sub">.*?</p>)?', body, re.S)
    body = body[:m.end()] + f'\n<p class="from">From paper #{num}, version {ver} · DICTO DOI: {doi}</p>\n' + body[m.end():]
    return f'<div class="chapter">{body}</div>', re.sub('<[^>]+>', '', title), num, doi
def own(folder, label, newtitle=None):
    s = open(os.path.join(P, folder, 'paper.html'), encoding='utf8').read()
    for st in re.findall(r'<style>(.*?)</style>', s, re.S): styles.add(st.strip())
    body = s[s.index('<h1'):s.rindex('</body>')]
    body = re.sub(r'<img class="(watermark|logo)"[^>]*>', '', body)
    body = re.sub(r'<div class="meta">.*?</div>', '', body, count=1, flags=re.S); body = strip_status(body)
    def fig(mo):
        f = mo.group(1); path = os.path.normpath(os.path.join(P, folder, f)); dst = f'figures/ch{label}/{os.path.basename(f)}'
        os.makedirs(os.path.join(HERE, os.path.dirname(dst)), exist_ok=True); shutil.copy(path, os.path.join(HERE, dst)); return f'<img src="{dst}"'
    body = re.sub(r'<img src="([^"]+)"', fig, body)
    t = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1)
    main = re.sub('<[^>]+>', '', re.sub(r'<br>.*', '', t, flags=re.S)).strip()
    sub = re.search(r'<span[^>]*>(.*?)</span>', t, re.S); sub = sub.group(1).split(' · ')[0] if sub else ''
    head = (f'Chapter {label} · ' if label else '') + (newtitle or main) + (f': {sub}' if sub and 'Ladder' not in sub else '')
    if label: body = re.sub(r'\b(Figure|Fig\.) (\d+)', lambda mo: f'{mo.group(1)} {label}.{mo.group(2)}', body)
    body = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 id="{"ch"+label if label else "map"}">{head}</h1>', body, count=1, flags=re.S)
    return body, head
# v1 chapters 1-2 as published
v1ch = re.findall(r'<div class="chapter">.*?(?=<div class="chapter">|</body>)', v1, re.S)
assert len(v1ch) == 2, len(v1ch)
v1ch = [c.replace('<h1>Chapter 1 ·', '<h1 id="ch1">Chapter 1 ·').replace('<h1>Chapter 2 ·', '<h1 id="ch2">Chapter 2 ·') for c in v1ch]
for x, y in V1CORR:
    assert sum(c.count(x) for c in v1ch) == 1, x[:60]; v1ch = [c.replace(x, y) for c in v1ch]
for st in re.findall(r'<style>(.*?)</style>', v1, re.S): styles.add(st.strip())
mapbody, _ = own('golden-ladder-map', '')
closing, closing_head = own('golden-ladder-closing', '9')
built = [chapter(*c) for c in CH]
toc = [('1', 'One Triangle, Three Numbers', 'opening chapter'), ('2', 'Silence Is Golden', 'chapter')]
toc += [(lab, t, f'#{n}') for (lab, *_), (_, t, n, _d) in zip(CH, built)]
toc.append(('9', re.sub(r'^Chapter 9 · ', '', closing_head), 'closing chapter'))
tochtml = '<h2>Contents</h2><table class="toc">' + '<tr><td><a href="#map">Map of the Ladder</a></td><td>opening</td></tr>' + ''.join(
    f'<tr><td><a href="#ch{l}">Chapter {l} · {html.escape(t)}</a></td><td>{n}</td></tr>' for l, t, n in toc) + '</table>'
ch3div = ('<div class="chapter"><h1 id="ch3">Chapter 3 · The Truncated Triangle and the Golden Bond</h1><p class="sub">The 2D rung, in two papers: '
          'the truncated triangle enters with the FUJI Family (#20, Chapter 3A), and the golden bond with the Golden Split (#48, Chapter 3B)</p></div>')
css = '\n'.join(sorted(styles)) + '''
.chapter{break-before:page} .chapter h1{margin-top:0} p.from{font-size:8.5pt;color:#777;margin:-1mm 0 4mm}
table.toc td{border-bottom:1px dotted #ccc;padding:1.2mm 2mm} table.toc a{color:inherit;text-decoration:none}
figure img, .figs img{max-width:100%}
body,h1,h2,h3,h4,.sub,.meta,figcaption,table,.status,ol.refs{font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",sans-serif}'''
status = '''<div class="status"><b>Draft of Version 6: corrections and additions (delete this box at publication; set status = '' in assemble.py).</b><ul>
<li>Erratum 24 (Chapter 2): the Pell multiplets are (0, P<sub>n</sub>, Q<sub>n</sub>) with Q = A001333, as the printed dimensions 112, 4 928, 905 520, 411 098 688 and μ = 7/3, 17/7, 41/17, 99/41 are; the printed (0, P<sub>n</sub>, P<sub>n+1</sub>) would give 378, 19 656, … and the limit 2.547, not 1 + √2 (recomputed by the Weyl dimension formula of SO(7)).</li>
<li>Concordance waiting item 5 (Chapter 7, new Theorem 1A after Theorem 1): the Galois twins of the other golden cuts: the dodecahedron's greater cut is its own twin, its lesser cut's twin is the φ³-cut dodecahedron, which is not a station of the golden cycle; the triangle-faced solids have no twin solid (study 2026-11-04-golden-twins, every number recomputed).</li>
<li>Concordance waiting item 47 (Chapter 8, prior art of #91): the Golden OGs keep OG's known face pattern (Rossiter, McCooey); their golden metric forms were not found in the sources checked.</li>
</ul></div>'''   # v5 released 7 November 2026; this box is the v6 draft's
doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>The Golden Ladder</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<div class="coverpage" style="height:252mm;display:flex;justify-content:center;align-items:center;break-after:page">
<img src="figures/cover/golden-ladder-cover-front.png" alt="Cover: The Golden Ladder, DICTO, a ladder whose rungs are golden shapes from 2D to 8D" style="height:248mm;display:block"></div>
<img class="watermark" src="../dicto-logo.png" alt="">
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>The Golden Ladder<br><span style="font-size:0.72em;font-weight:normal">Golden Cuts from Plato to the Eighth Dimension</span></h1>
<div class="meta"><b>DICTO</b> (artist, Osaka, Japan) · contact@dictospheres.com · https://dictospheres.com · ORCID 0009-0001-2620-2036<br>
Book · Version 6 · 7 November 2026 · DICTO DOI: 10.5281/zenodo.23966554 · Licence CC BY-SA 4.0 · Part of DICTO: Collected Geometric Works (DICTO DOI: 10.5281/zenodo.23345699)<br>Cover by DICTO: a ladder of golden rails whose rungs climb the dimensions: the truncated triangle with sides in the golden ratio (2D); Icosaxes and Unborn Axes (3D); the 120-cell (4D); and E8 as two 600-cells, one φ times the other, in the Coxeter plane (8D).</div>
{status}
{tochtml}
<div class="chapter">{mapbody}</div>
{''.join(v1ch)}
{ch3div}
{''.join(b for b, *_ in built)}
<div class="chapter">{closing}</div>
</body></html>'''
open(os.path.join(HERE, 'paper.html'), 'w', encoding='utf8').write(doc)
imgs = re.findall(r'<img[^>]+src="([^"]+)"', doc); missing = [i for i in imgs if not os.path.exists(os.path.normpath(os.path.join(HERE, i)))]
print('chapters', len(toc), 'images', len(imgs), 'MISSING', missing, 'chars', len(doc))
