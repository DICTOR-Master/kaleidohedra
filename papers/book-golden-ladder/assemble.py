# Assemble The Golden Ladder, version 2 (DICTO 11-05: keep v1, add the remaining chapters as new versions; DICTO 11-06 "continue chapters").
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
status = ''   # deleted at release (v4 released 6 November 2026 after DICTO's read ok: Figure 3A.1 photographs cleaned)
doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>The Golden Ladder</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<div class="coverpage" style="height:252mm;display:flex;justify-content:center;align-items:center;break-after:page">
<img src="figures/cover/golden-ladder-cover-front.png" alt="Cover: The Golden Ladder, DICTO, a ladder whose rungs are golden shapes from 2D to 8D" style="height:248mm;display:block"></div>
<img class="watermark" src="../dicto-logo.png" alt="">
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>The Golden Ladder<br><span style="font-size:0.72em;font-weight:normal">Golden Cuts from Plato to the Eighth Dimension</span></h1>
<div class="meta"><b>DICTO</b> (artist, Osaka, Japan) · contact@dictospheres.com · https://dictospheres.com · ORCID 0009-0001-2620-2036<br>
Book · Version 5 · 7 November 2026 · DICTO DOI: 10.5281/zenodo.23966554 · Licence CC BY-SA 4.0 · Part of DICTO: Collected Geometric Works (DICTO DOI: 10.5281/zenodo.23345699)<br>Cover by DICTO: a ladder of golden rails whose rungs climb the dimensions: the truncated triangle with sides in the golden ratio (2D); Icosaxes and Unborn Axes (3D); the 120-cell (4D); and E8 as two 600-cells, one φ times the other, in the Coxeter plane (8D).</div>
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
