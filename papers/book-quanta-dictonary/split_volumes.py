# Split Quanta of Space into two volumes (DICTO 2026-11-03: "yes split it with that title"). Run from k-research/papers.
#   Volume I  (book-quanta-of-space/paper.html): "Quanta of Space: A Manifesto", version 2.0, same concept DOI 10.5281/zenodo.23754454:
#             front matter, Introduction, Chapters 1-6 with their narrative entries, Findings and apps (narrative: Kaleidohedra and the
#             data set told as entries), About the author. Where the catalogue stood at the end of Chapter 1: a short pointer.
#   Volume II (book-quanta-dictonary/paper.html): "Quanta of Space II: The DICTOnary of Atoms", new book, DOI to be reserved:
#             cover, title page, how to read an entry, contents, the catalogue of all the atoms (with Not drawn here and the clusters,
#             structures and networks), the data work by work (A.xx), the known and rediscovered shapes, About the author.
# Source: the v1.5 draft (git 8b71279c). Cross-references: "Data: Appendix A.n" -> "Data: Volume II, A.n" in Volume I; every catalogue
# entry and every A.n section of Volume II names the chapter of Volume I that tells its work (atoms.py, told() here).
# Usage: python3 book-quanta-dictonary/split_volumes.py   (runs atoms.py for the catalogue blocks; checks every reference at the end)
import re, subprocess, sys, os, html
SRC = subprocess.run(['git', 'show', '8b71279c:papers/book-quanta-of-space/paper.html'], capture_output=True, text=True, check=True).stdout
V1, V2 = 'book-quanta-of-space/paper.html', 'book-quanta-dictonary/paper.html'
ATOMS = '../studies/2026-10-29-quanta-atoms'
DATE = '3 November 2026'
DOI1 = '10.5281/zenodo.23754454'
T2 = '<i>Quanta of Space II: The DICTOnary of Atoms</i>'
n_sub = 0
def rep(t, a, b, n=1):
    global n_sub
    c = t.count(a); assert c == n, (a[:80], c); n_sub += c
    return t.replace(a, b)
def cut(t, a, b):
    """the text from marker a to marker b inclusive."""
    i, j = t.index(a), t.index(b) + len(b); return t[i:j]

# ------------------------------------------------------------------ Volume I
v1 = SRC
head_end = v1.index('</style></head>') + len('</style></head>')
STYLE = v1[:head_end]
# status box: one box under the meta line, the open items of this version
box1 = f'''<div class="status" style="text-align:left;margin-top:5mm;break-inside:avoid"><b>DRAFT, Volume I, Version 2.0, {DATE}, for DICTO's reading. Not published.</b> Delete this box at publication.
<ul style="margin:1mm 0 0;padding-left:5mm">
<li>Works #79 to #87 are not yet told in short in this book: they come in the next version (DICTO, 3 November 2026), and their new shapes then join the catalogue in Volume II.</li>
<li><b>Volume II</b>, {T2}: its front cover is a DRAFT for DICTO's approval (in the style of this cover: the same DICTO square, the title below; see Volume II's status box). Its DICTO DOI is to be reserved; then it is named on this title page, in the pointer at the end of Chapter 1 and in this record (related identifier isSupplementedBy).</li>
<li>D·I·C·T·O order: set in the #44 lead and the A.45 lists (now in Volume II); left as they are because they follow a picture or an order in space: the captions of Figures 44 (panel order) and 47 (bottom to top), Plato's elements, nesting orders and tables of the published papers.</li>
</ul></div>'''
i = v1.index('<p class="small" style="margin-top:8mm">Book · Version 1.5'); j = v1.index('</ul></div>', i) + len('</ul></div>')
v1 = v1[:i] + f'''<p class="small" style="margin-top:8mm">Book · Volume I · Version 2.0 · {DATE} · DICTO DOI: {DOI1}</p>
<p class="small" style="margin-top:2mm">Volume II: {T2}, the catalogue of all the atoms, the data work by work and the known and rediscovered shapes (DICTO DOI to be reserved).</p>
''' + box1 + v1[j:]
n_sub += 2
# contents
v1 = rep(v1, '73 works: 71 papers in six chapters, with the catalogue of all the atoms, then the Kaleidohedra findings and the data set (numbers are the paper numbers on dictospheres.com)<br>Appendix: the data, work by work</p>',
         f'73 works: 71 papers in six chapters, then the Kaleidohedra findings and the data set (numbers are the paper numbers on dictospheres.com)<br>In Volume II, {T2}: the catalogue of all the atoms, the data work by work, and the known and rediscovered shapes</p>')
v1 = rep(v1, "<li><b>—</b>All the atoms: DICTO's 123 new shapes, and his new clusters and networks</li>",
         "<li><b>—</b>All the atoms: the catalogue is Volume II</li>")
v1 = rep(v1, '<li><b>—</b>At the end: known and rediscovered shapes in the work</li>',
         '<li><b>—</b>Known and rediscovered shapes in the work: in Volume II</li>')
# introduction
v1 = rep(v1, "where every DICTO solid has a permanent D-number; the chapter closes with the catalogue of all the atoms, 123 new shapes of DICTO's and the known shapes the work builds with.</p>",
         f"where every DICTO solid has a permanent D-number. The catalogue of all the atoms, 123 new shapes of DICTO's and the known shapes the work builds with, is Volume II, {T2}.</p>")
# #88 short entry, then the pointer where the catalogue stood
v1 = rep(v1, 'and stand in the catalogue that follows.', 'and stand in the catalogue of Volume II.')
v1 = rep(v1, '<!--E88 START-->\n<section class="shortch" style="break-before:page;break-after:page">', '<!--E88 START-->\n<section class="shortch" style="break-before:page;break-after:auto">')
a, b = v1.index('<!--ATOMS START-->'), v1.index('<!--ATOMS END-->') + len('<!--ATOMS END-->')
POINTER = f'''<!--ATOMS POINTER START (the catalogue is Volume II since version 2.0)-->
<section class="shortch" style="break-before:auto;break-after:page">
<div class="se"><h2>All the atoms</h2>
<p>The catalogue of all the atoms, which closed this chapter up to version 1.4, is now a book of its own: Volume II, {T2}. It lists every named shape of the work, one quantum of space each: DICTO's 123 new shapes with their D-numbers, his 31 new clusters, structures and networks, and the known and rediscovered shapes the work builds with, each with its picture, data and source. It also holds the data, work by work, cited in this volume as “Data: Volume II, A.n”.</p></div>
</section>
<!--ATOMS POINTER END-->'''
v1 = v1[:a] + POINTER + v1[b:]
# data references
v1, k = re.subn(r'Data: Appendix (A\.[0-9A-Za-z]+)', r'Data: Volume II, \1', v1); n_sub += k; n_data = k
# appendix and known shapes out (they are Volume II); About the author stays
a = v1.index('<!-- ============ APPENDIX ============ -->'); b = v1.index('<!--KNOWN END-->') + len('<!--KNOWN END-->')
v1 = v1[:a] + v1[b:]
ABOUT_OLD = "and to six books: <i>Quanta of Space: A Manifesto</i> (this one), "
v1 = rep(v1, ABOUT_OLD, f"and to seven books: <i>Quanta of Space: A Manifesto</i> (this one) and its second volume, {T2}, ")
v1 = rep(v1, '<title>Quanta of Space: A Manifesto</title>', '<title>Quanta of Space: A Manifesto (Volume I)</title>')
open(V1, 'w', encoding='utf8').write(v1)

# ------------------------------------------------------------------ catalogue blocks for Volume II (needs Volume I written)
r = subprocess.run([sys.executable, f'{ATOMS}/scripts/atoms.py', f'{ATOMS}/index.csv', 'book-quanta-dictonary/figures/atoms',
                    'book-quanta-dictonary/atoms-catalogue.html', V1], capture_output=True, text=True); print(r.stdout, r.stderr)
assert r.returncode == 0
cat = open('book-quanta-dictonary/atoms-catalogue.html', encoding='utf8').read()
known = open('book-quanta-dictonary/atoms-catalogue-known.html', encoding='utf8').read()
m = re.search(r'new (\d+) new clusters (\d+) other (\d+)', r.stdout); NNEW, NCL, NKN = map(int, m.groups())
assert (NNEW, NCL) == (123, 31), (NNEW, NCL)   # the counts written in Volume I

# Volume I chapters (same reading as atoms.py)
sys.path.insert(0, f'{ATOMS}/scripts')
def vol1_chapters(t):
    ch = {}
    last = None
    for sec in re.findall(r'<section[^>]*>(.*?)</section>', t, re.S):
        mk = re.search(r'chapter-mark">([^<]*)<', sec)   # a short section with no chapter line belongs to the chapter before it
        if mk: last = mk
        elif last: mk = last
        else: continue
        c = re.match(r'Chapter (\d)', mk.group(1))
        name = 'Chapter ' + c.group(1) if c else ('Findings and apps' if mk.group(1).startswith('Findings and apps') else None)
        if not name: continue
        keys = ['#' + x for x in re.findall(r'#(\d+[a-z]?)\b', mk.group(1)) + re.findall(r'<span class="n">#(\d+[a-z]?)</span>', sec)]
        if name == 'Findings and apps': keys += [mk.group(1)]
        if 'Bonds · closing' in mk.group(1): keys += ['A.DB']
        for k in keys: ch.setdefault(k, []).append(name) if name not in ch.get(k, []) else None
    return ch
CH = vol1_chapters(v1)
CHNAME = {'Chapter 1': 'Atoms', 'Chapter 2': 'Bonds', 'Chapter 3': 'Shells', 'Chapter 4': 'Cycles', 'Chapter 5': 'Stacking', 'Chapter 6': 'Four dimensions', 'Findings and apps': ''}
def told_a(code):
    """A.18 -> 'Chapter 1'; A.DB -> Chapter 2 (closing section); A.K, A.D -> Findings and apps."""
    if code == 'A.DB': return CH['A.DB'][0]
    if code in ('A.K', 'A.D'): return 'Findings and apps'
    return CH['#' + code[2:]][0]

# ------------------------------------------------------------------ Volume II
app = cut(SRC, '<!-- ============ APPENDIX ============ -->', '</section>\n<!--KNOWN START-->')[:-len('\n<!--KNOWN START-->')]
app = rep(app, '<p class="chapter-mark">Appendix</p>', '<p class="chapter-mark">The DICTOnary · the data</p>')
app = rep(app, '<p>One section per work, with the exact values, volumes, proof sketches and checks as published in its paper.',
          '<p>One section per work, with the exact values, volumes, proof sketches and checks as published in its paper, in the order of the chapters of Volume I; under each title, the chapter of Volume I that tells the work.')
sections = []   # (code, title, chapter) for the contents
def add_told(mm):
    code, title = mm.group(2), mm.group(3).strip(); ch = told_a(code); sections.append((code, title, ch))
    where = 'Volume I, ' + ch + (' · ' + CHNAME[ch] if CHNAME.get(ch) else '')
    return mm.group(0) + f'\n<p class="told">Told in {where}.</p>'
app, n_told = re.subn(r'<h2( class="first")?>(A\.[0-9A-Za-z]+) ([^<]*)<span[^>]*>\([^)]*\)</span></h2>', add_told, app)
assert n_told == app.count('<h2'), (n_told, app.count('<h2'))
n_sub += n_told

about = cut(SRC, '<!--ABOUT START-->', '<!--ABOUT END-->')
about = rep(about, ABOUT_OLD, f"and to seven books: <i>Quanta of Space: A Manifesto</i> and its second volume, {T2} (this one), ")

style2 = STYLE.replace('<title>Quanta of Space: A Manifesto</title>', '<title>Quanta of Space II: The DICTOnary of Atoms</title>')
style2 = style2.replace('</style></head>', '''.appendix p.told { font: italic 8.8pt "Nimbus Sans", "Liberation Sans", sans-serif; color: #6b5310; margin: -1pt 0 4pt; }
.howto dt { font-weight: 600; color: #6b5310; margin-top: 6pt; } .howto dd { margin: 1pt 0 0 6mm; }
.contents ul.app { list-style: none; padding: 0; margin: 0 0 4pt; columns: 2; column-gap: 8mm; font: 8.8pt/1.45 "DejaVu Sans", sans-serif; }
.contents ul.app li { break-inside: avoid; margin: 0 0 1.5pt; padding-left: 11mm; text-indent: -11mm; } .contents ul.app li b { display: inline-block; width: 11mm; text-indent: 0; color: #6b5310; }
</style></head>''')
box2 = f'''<div class="status" style="text-align:left;margin-top:5mm;break-inside:avoid"><b>DRAFT, Volume II, Version 1.0, {DATE}, for DICTO's reading. Not published.</b> Delete this box at publication.
<ul style="margin:1mm 0 0;padding-left:5mm">
<li><b>Cover (DRAFT, for DICTO's approval):</b> the front cover is made as Volume I's: the same DICTO square, the title panel below in the same letters and colours (QUANTA OF SPACE II gold, THE DICTONARY OF ATOMS white with the five letters of DICTO at the initial size so the coinage shows, ◆ DICTO ◆ red). One option to tell the volumes apart at a glance: the same five by five square drawn with each Platonic solid's Greater Golden Cut solid of #88 in its place (same letters, colours and order), so Volume I shows the solids and Volume II their first new atoms. Keep the square as it is, or take this option?</li>
<li>Works #79 to #87 are not yet told in short in Volume I, and their new shapes are not yet in this catalogue: next version (DICTO, 3 November 2026).</li>
<li><b>DICTO DOI to be reserved</b> for this book (new record, type Book, isSupplementTo Volume I's concept DOI {DOI1}); then named on this title page, in the footer and in Volume I.</li>
<li>The pictures of the 16 golden cut solids are drawn from the construction of #88 and #89 (floating point); they are not yet model files in DICTO Solids (next data set version).</li>
<li>D·I·C·T·O order: set in the A.45 lists; left as they are where they follow a picture or an order in space, as in Volume I.</li>
</ul></div>'''
title2 = f'''<!-- ============ COVER ============ -->
<section class="page coverpage" style="height:252mm;display:flex;justify-content:center;align-items:center">
<img src="figures/cover/dictonary-cover-front.png" alt="Cover: Quanta of Space II, The DICTOnary of Atoms, DICTO, under the DICTO square of the five Platonic solids of DICTO's name, D I C T O" style="height:248mm;display:block">
</section>
<section class="page titlepage">
<img class="big" src="../dicto-logo.png" alt="DICTO">
<h1>Quanta of Space II</h1>
<p class="sub">The DICTOnary of Atoms</p>
<p class="by">DICTO</p>
<p class="small">artist, Osaka, Japan · contact@dictospheres.com · https://dictospheres.com<br>
All works, findings and names are DICTO's. Computation, checking and drafting with Claude (Anthropic).<br>
Licence CC BY-SA 4.0</p>
<p class="small" style="margin-top:8mm">Book · Volume II · Version 1.0 · {DATE} · DICTO DOI: to be reserved</p>
<p class="small" style="margin-top:2mm">Volume I: <i>Quanta of Space: A Manifesto</i> (DICTO DOI: {DOI1}), the manifesto and the works told in six chapters. This volume holds their atoms and their data.</p>
{box2}
</section>
'''
howto = f'''<!-- ============ HOW TO READ AN ENTRY ============ -->
<section class="page intro howto">
<img class="logo" src="../dicto-logo.png" alt="DICTO">
<p class="chapter-mark">Introduction</p>
<h1>How to read an entry</h1>
<p class="lead">This is a dictionary of the atoms of space: every named shape of DICTO's geometric work, one quantum of space each. Volume I, <i>Quanta of Space: A Manifesto</i>, tells the works in six chapters; this volume holds their shapes and their numbers. The name is DICTO's: the DICTOnary.</p>
<p>Each entry is read like an entry in a dictionary.</p>
<dl>
<dt>Headword: the D-number and the name</dt>
<dd>D1, D2 … are DICTO's permanent numbers for his new single solids and pieces, given in order of first publication and never reused. A known shape keeps the number its first maker gave it (Johnson, uniform, Wenninger, Hart, Mosseri–Sadoc). Clusters, structures and networks built from the pieces carry no number (—).</dd>
<dt>Definition: the picture, the data and the source</dt>
<dd><b>Picture.</b> Drawn from the exact model file in the data set <i>DICTO Solids: Exact Geometry</i>, all in one pose: gold for DICTO's new shapes, silver for known ones. A shape with no model file yet is listed in a table under “Not drawn here”.<br>
<b>Data.</b> Its kind (solid, piece, cluster, structure, network, compound or curved body) and the status found by the prior-art search. “Not found” means only that the sources searched did not show it; it is not proof of novelty. The exact values of each work, its volumes, proof sketches and checks, are in “The data, work by work”, one section per work: A.18 is the data of paper #18.<br>
<b>Source.</b> The paper by its number (#41) or the Kaleidohedra finding (F1), linked to its DICTO DOI, and the chapter of Volume I that tells it (Volume I, Chapter 1).</dd>
</dl>
<h3>The parts of this volume</h3>
<p><b>All the atoms:</b> DICTO's {NNEW} new shapes, then his {NCL} new clusters, structures and networks, then those not drawn yet. <b>The data, work by work:</b> the sections A.8 to A.51, with A.DB for the DICTONIC SOLIDS and BONDS, A.K for the Kaleidohedra findings and A.D for the data set. <b>Known and rediscovered shapes:</b> the {NKN} shapes the work builds with that were made first by others. Every value can be rebuilt and checked from the data set, whose checker re-proves it from the data files alone.</p>
<p class="credit">Shapes, names and D-numbers by DICTO; catalogue and data built and checked with Claude (Anthropic). Licence CC BY-SA 4.0.</p>
</section>
'''
# contents: the catalogue's parts, then the data sections grouped by the chapter of Volume I that tells them
groups = []
for code, title, ch in sections:
    if not groups or groups[-1][0] != ch: groups.append((ch, []))
    groups[-1][1].append((code, title))
lis = ''
for ch, items in groups:
    lab = ch + (' · ' + CHNAME[ch] if CHNAME.get(ch) else '')
    lis += f'<h3 style="margin:6pt 0 2pt;font-size:9.5pt">Told in Volume I, {lab}</h3>\n<ul class="app">\n' + '\n'.join(f'<li><b>{c}</b>{t}</li>' for c, t in items) + '\n</ul>\n'
contents = f'''<!-- ============ CONTENTS ============ -->
<section class="page contents">
<img class="logo" src="../dicto-logo.png" alt="DICTO" style="width:22mm">
<h1>Contents</h1>
<p style="font: 9.5pt 'DejaVu Sans', sans-serif;">How to read an entry</p>
<h2>All the atoms</h2><p class="chap">The catalogue: every named shape of the work, with its picture, data and source.</p>
<ol>
<li><b>—</b>DICTO's new atoms: {NNEW} new shapes, D1 to D123</li>
<li><b>—</b>DICTO's new clusters, structures and networks: {NCL}</li>
<li><b>—</b>Not drawn here: the shapes with no model file yet</li>
</ol>
<h2>The data, work by work</h2><p class="chap">One section per work, as published in its paper.</p>
{lis}<h2>Known and rediscovered shapes in the work</h2><p class="chap">The {NKN} shapes made first by others, or rediscovered by DICTO.</p>
<h2>About the author</h2>
</section>
'''
v2 = (style2 + '<body>\n<img class="watermark" src="../dicto-logo.png" alt="">\n\n' + title2 + howto + contents +
      '<!--ATOMS START-->\n' + cat + '<!--ATOMS END-->\n' + app + '\n<!--KNOWN START-->\n' + known + '<!--KNOWN END-->\n' + about + '\n</body></html>\n')
open(V2, 'w', encoding='utf8').write(v2)
assert 'D1 to D123' in v2 and re.search(r'<b>D123</b>', v2) and 'D—' not in v2

# ------------------------------------------------------------------ checks: no dangling references
codes2 = set(re.findall(r'<h2[^>]*>(A\.[0-9A-Za-z]+) ', v2))
refs1 = re.findall(r'Volume II, (A\.(?:\d+[a-z]?|DB|K|D)\b)', v1)
dang = [x for x in refs1 if x not in codes2]
assert not dang, dang
assert 'Appendix A.' not in v1 and 'catalogue that follows' not in v1 and 'end of the book' not in v1
inner2 = re.findall(r'\(see (A\.[0-9A-Za-z]+)\)', v2); assert all(x in codes2 for x in inner2), inner2
for k in re.findall(r'Told in Volume I, (Chapter \d|Findings and apps)', v2):
    assert (k.startswith('Chapter') and f'chapter-mark">{k} ' in v1) or (k == 'Findings and apps' and 'chapter-mark">Findings and apps' in v1), k
n_cat = len(re.findall(r'<div class="av">Volume I, ', v2)) + len(re.findall(r'<td>Volume I, ', v2))
print(f'Volume I: {n_data} data references to Volume II A.n (all found); Volume II: {n_told} A.n sections and {n_cat} catalogue rows name their Volume I chapter; '
      f'{len(inner2)} internal see-A.n; substitutions {n_sub}')
