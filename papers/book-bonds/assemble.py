# Assemble a first DRAFT of DICTO's book on the bond papers "DICTONIC Bonds: from the Octet to the Rule of Halves"
# (title named by DICTO, 3 November 2026), from the published paper sources (DICTO's idea, 26 October 2026: "the bond papers are really ONE SERIES building
# to the rule of halves"). Modelled on book-laws-of-stacking/assemble.py and book-star-cores/assemble.py (chapter corrections as there, see CORR):
# each published paper becomes a chapter word for word (title, abstract, sections, theorems, tables and figures); the meta line goes;
# "Sources checked", "Data and code"/"Data and reproducibility"/"Methods and data", the reference-library appendices and "References"
# move to one appendix by chapter; figures are copied into figures/ch<n>/ and renumbered per chapter (Figure 3 -> Figure 5.3); paper
# numbers link to the chapter when the paper is in the book, else to its DICTO DOI. Front matter, epilogue and About from front.html,
# epilogue.html, about.html (by hand). pages.json (written after a first print, from the PDF) fills the page numbers of the contents.
# Output: paper.html, typeset on dicto-big-brother with ../print.mjs:  node print.mjs book-bonds <pdf> "DICTONIC Bonds" "–" "–"
import re, os, shutil, html, json
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
# Order: DICTO's own sequence of 26 October 2026 (the series building to the Rule of Halves); part names are placeholders.
# #49 The Polyhedral Stretching Theorem left out (DICTO, 3 November 2026: it goes into the future Laws book).
CH = [('1', '2026-10-22-platonic-mixes', 47), ('2', '2026-10-23-exact-vs-dissection', 50),
      ('3', '2026-10-23-golden-split', 48), ('4', '2026-10-24-delian-bond', 51),
      ('5', '2026-10-25-web-of-bonds', 52), ('6', '2026-10-25-relay-census', 53),
      ('7', '2026-10-25-david-goliath', 55), ('8', '2026-10-25-keyed-switch', 56), ('9', 'icosaxes-hexa', 59),
      ('10', 'series-web-of-bonds', 58), ('11', '2026-10-26-rule-of-halves', 57)]
PART = {'1': ('Part I. Filling', 'Chapters 1 and 2'), '3': ('Part II. The bonds', 'Chapters 3 and 4'),
        '5': ('Part III. The web', 'Chapters 5 and 6'), '7': ("Part IV. The weight walk's bonds", 'Chapters 7 to 9'),
        '10': ('Part V. The law', 'Chapters 10 and 11')}
# Corrections inside the chapters, as in book-star-cores (current practice; the published papers stay the record):
# "DICTO asked" -> "DICTO proposed"; the banned opening label "In short." dropped (the sentence kept); "this paper" -> "this chapter"
# where it means the chapter itself (KEEP lists the places where it means the published paper or its build).
CORR = [('DICTO asked for the same move with icosahedral symmetry.', 'DICTO proposed the same move with icosahedral symmetry.'),
        ('<b>In short.</b> ', ''), ('<b>Plain words:</b> ', '')]
KEEP = ['when this paper is built', 'of the proof and of this paper']
# Appendix letters after the move: old letter -> new letter, or None when that appendix moved to the book's Appendix
# (in-text pointers to it then name the book's Appendix and the chapter). Numbered sections renumbered where one moved.
APPMAP = {'2026-10-22-platonic-mixes': {'B': None}, '2026-10-23-exact-vs-dissection': {'B': None}, '2026-10-23-golden-split': {'A': None, 'B': 'A'},
          '2026-10-24-delian-bond': {'A': None, 'B': 'A'}, '2026-10-25-web-of-bonds': {'A': None, 'B': 'A'},
          '2026-10-25-relay-census': {'A': None, 'B': 'A', 'C': 'B'}}
SECMAP = {'icosaxes-hexa': {'9': '8'}}
def remap(t, folder, label, inbody):
    m = APPMAP.get(folder, {})
    def r(mo):
        old = mo.group(1)
        if old not in m: return mo.group(0)
        if m[old] is None: return mo.group(0) if not inbody else f'the Appendix under Chapter {label}'
        return 'Appendix ' + m[old]
    parts = re.split(r'(<[^>]+>)', t)
    return ''.join(p if p.startswith('<') else re.sub(r'\bAppendix ([A-C])\b', r, p) for p in parts)
INDEX_TERMS = ['DICTONIC', 'bond', 'web of bonds', 'Icosaxes', 'Unborn Axes', 'Unborn', 'AXE', 'Lotus Jewel Axes', 'Dodecaxes', 'Samson', 'Delilah',
    'Sonsam', 'Lahdeli', 'Ian Dury', 'Blockhead', 'David', 'Goliath', 'Jessen', 'Icosaxes Hexa', 'Icosaxes Bloom', 'Icosaxes Bud', 'Icosaxes Seed',
    'Keyaxes', 'Janus', 'Chucky', 'Fang', 'rule of halves', 'octet', 'twinned octet', 'golden point', 'golden ratio', 'Delian', 'power diagram',
    'weighted Voronoi', 'Delaunay', 'Kelvin', 'Kepler', 'rhombic dodecahedron', 'truncated octahedron', 'Bilinski', 'elongated dodecahedron',
    'rhombohedron', 'Admiral Caps', 'Dogstar', 'Sunstar', 'Euclid', 'Pacioli', 'Platonic', 'stretched', 'Fedorov', 'Kaleidohedra',
    'caesium chloride', 'fluorite', 'zinc blende', 'rock salt', 'A15', 'C15', 'Pauling', 'close-packed', 'stacking', 'Ogdoecontahedron']
styles = set(); chapters = []; sources = []; toc = []; INDEX = {}
cw = open(os.path.join(P, 'collected', 'paper.html'), encoding='utf8').read()
PAPERS = {int(m.group(1)): (html.unescape(re.sub('<[^>]+>', '', m.group(2))), m.group(3)) for m in re.finditer(r'<tr><td class="n">#(\d+)</td><td><b>(.*?)</b>.*?DICTO DOI: (10\.5281/zenodo\.\d+)', cw, re.S)}
INBOOK = {num: lab for lab, _, num in CH}
REFERRED = set()
def link_text(t):
    def r(mo):
        n = int(mo.group(1))
        if n in INBOOK: return f'<a href="#ch{INBOOK[n]}">#{n}</a>'
        if n in PAPERS: REFERRED.add(n); return f'<a href="https://doi.org/{PAPERS[n][1]}">#{n}</a>'
        return mo.group(0)
    return re.sub(r'(?<![&\w])#(\d{1,2})\b', r, t)
def link_html(h):
    parts = re.split(r'(<[^>]+>)', h); out = []; inA = False; inStyle = False
    for p in parts:
        if p.startswith('<'):
            if re.match(r'<a\b', p): inA = True
            if p.startswith('</a'): inA = False
            if re.match(r'<(style|svg)\b', p): inStyle = True
            if re.match(r'</(style|svg)', p): inStyle = False
            out.append(p)
        else: out.append(p if (inA or inStyle) else link_text(p))
    return ''.join(out)
# sections that move to the appendix: references, data/code statements and the lists of sources checked
MOVESEC = r'(?:\d+\. )?(?:References|Data and reproducibility|Methods and data|Appendix [A-C]\. The reference library searched|Appendix [A-C]\. Sources checked for prior work)'
for label, folder, num in CH:
    s = open(os.path.join(P, folder, 'paper.html'), encoding='utf8').read()
    for st in re.findall(r'<style>(.*?)</style>', s, re.S): styles.add(st.strip())
    doi = re.search(r'DICTO DOI: (10\.5281/zenodo\.\d+)', s).group(1)
    ver = re.search(r'Version (\d+) · ', s).group(1)
    body = s[s.index('<h1'):s.rindex('</body>')]
    title = html.unescape(re.sub('<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1))).strip()
    body = re.sub(r'<div class="meta">.*?</div>', '', body, count=1, flags=re.S)
    out = []
    for m in re.finditer(r'<p class="prec">.*?</p>', body, re.S):
        if re.sub('<[^>]+>', '', m.group(0)).lstrip().startswith('Precisely'): continue   # #58: part of the telling, stays
        out.append(m.group(0)); body = body.replace(m.group(0), '', 1)
    for m in list(re.finditer(r'<h2[^>]*>(' + MOVESEC + r')</h2>(.*?)(?=<h2|$)', body, re.S)):
        out.append('<h4>' + m.group(1) + '</h4>' + m.group(2)); body = body.replace(m.group(0), '', 1)
    body = remap(body, folder, label, True); out = [remap(o, folder, label, False) for o in out]
    for a, b in SECMAP.get(folder, {}).items():
        body = re.sub(r'(<h2[^>]*>)' + a + r'\. ', r'\g<1>' + b + '. ', body); body = re.sub(r'§' + a + r'\b', '§' + b, body)
    for a, b in CORR: body = body.replace(a, b)
    for i, k in enumerate(KEEP): body = body.replace(k, f'@KEEP{i}@')
    body = body.replace('this paper', 'this chapter').replace('This paper', 'This chapter')
    for i, k in enumerate(KEEP): body = body.replace(f'@KEEP{i}@', k)
    def fig(mo):
        src = mo.group(2); dst = f'figures/ch{label}/{os.path.basename(src)}'; path = os.path.join(P, folder, src)
        if not os.path.exists(path): raise SystemExit(f'FIG MISSING ch{label} {src}')
        os.makedirs(os.path.join(HERE, os.path.dirname(dst)), exist_ok=True); shutil.copy(path, os.path.join(HERE, dst)); return f'{mo.group(1)}{dst}"'
    body = re.sub(r'(<img\b[^>]*?\bsrc=")((?!\.\./)[^"]+)"', fig, body)
    body = re.sub(r'\bFigure (\d+)', lambda mo: f'Figure {label}.{mo.group(1)}', body)
    body = re.sub(r'\bFigures (\d+)', lambda mo: f'Figures {label}.{mo.group(1)}', body)
    body = re.sub(r'\bFig\. (\d+)', lambda mo: f'Fig. {label}.{mo.group(1)}', body)
    body = link_html(body)
    plain = re.sub('<[^>]+>', ' ', body)
    for term in INDEX_TERMS:
        if re.search(r'\b' + re.escape(term) + r'(s|es)?\b', plain): INDEX.setdefault(term, []).append(label)
    head = f'Chapter {label}. '
    body = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 class="chapter" id="ch{label}">{head}{html.escape(title)}</h1>', body, count=1, flags=re.S)
    body = body.replace('</h1>', f'</h1>\n<p class="from">From paper #{num} (version {ver}), DICTO DOI {doi}</p>', 1)
    if label in PART: chapters.append(f'<div class="part" id="part{label}"><h1 class="partt">{PART[label][0]}</h1><p class="partsub">{PART[label][1]}</p></div>')
    chapters.append(f'<section class="ch">{body}</section>')
    toc.append((head + title, label, num, doi))
    sources.append(f'<h3>{head}{html.escape(title)} (#{num}, DICTO DOI {doi})</h3>' + (''.join(out) or '<p>The paper has no separate list of sources, data or references; it names the papers it tells, which are the chapters of this book.</p>'))

PG = json.load(open(os.path.join(HERE, 'pages.json'))) if os.path.exists(os.path.join(HERE, 'pages.json')) else {}
def pg(k): return str(PG.get(k, ''))
front = open(os.path.join(HERE, 'front.html'), encoding='utf8').read()
epi = open(os.path.join(HERE, 'epilogue.html'), encoding='utf8').read()
for t in INDEX_TERMS:
    if re.search(r'\b' + re.escape(t) + r'(s|es)?\b', re.sub('<[^>]+>', ' ', epi)): INDEX.setdefault(t, []).append('E')
refhtml = ('<section class="app"><h1 class="chapter" id="refs">Papers referred to, not in this book</h1><table>' +
           ''.join(f'<tr><td>#{n}</td><td>{html.escape(PAPERS[n][0])}</td><td><a href="https://doi.org/{PAPERS[n][1]}">{PAPERS[n][1]}</a></td></tr>' for n in sorted(REFERRED)) +
           '</table></section>')
def refs(v):
    seen = []; [seen.append(x) for x in v if x not in seen]
    return ', '.join('<a href="#epilogue">E</a>' if x == 'E' else f'<a href="#ch{x}">{x}</a>' for x in seen)
items = [(t, refs(v)) for t, v in sorted(INDEX.items(), key=lambda kv: kv[0].lower())]
h = (len(items) + 1) // 2; L, R = items[:h], items[h:] + [('', '')] * (2 * h - len(items))
idxhtml = ('<section class="app"><h1 class="chapter" id="index">Index</h1><p style="font-size:9pt">Chapters (E = Epilogue) in which each term appears.</p>'
           '<table class="idx">' + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td class="gap"></td><td><b>{c}</b></td><td>{d}</td></tr>' for (a, b), (c, d) in zip(L, R)) + '</table></section>')
rows = []
for t, tag, n, d in toc:
    if tag in PART: rows.append(f'<tr class="tp"><td colspan="3"><a href="#part{tag}">{PART[tag][0]}</a></td></tr>')
    rows.append(f'<tr><td><a href="#ch{tag}">{html.escape(t)}</a></td><td>#{n}</td><td class="pg">{pg("ch" + tag)}</td></tr>')
for anchor, name in [('epilogue', 'Epilogue. From the walk to the law'), ('app', 'Appendix. Sources by chapter'), ('refs', 'Papers referred to, not in this book'), ('index', 'Index'), ('about', 'About the author')]:
    rows.append(f'<tr><td><a href="#{anchor}">{name}</a></td><td></td><td class="pg">{pg(anchor)}</td></tr>')
tochtml = '<h2>Contents</h2><table class="toc">' + ''.join(rows) + '</table>'
css = '\n'.join(sorted(styles)) + '''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font-size:8.5pt;color:#777;margin:-2mm 0 4mm}
.part{break-before:page;height:200mm;display:flex;flex-direction:column;align-items:center;justify-content:center} h1.partt{font-size:26pt;color:#b8962e;text-align:center} p.partsub{font-size:11pt;color:#555}
table.toc{width:100%} table.toc td{border-bottom:1px dotted #ccc;padding:1.1mm 2mm} table.toc td.pg{text-align:right;width:12mm} table.toc tr.tp td{font-weight:600;color:#8a6d1f;padding-top:3mm} table.toc a, table.idx a{color:inherit;text-decoration:none}
.titlepage{height:235mm;display:flex;flex-direction:column;justify-content:center} .titlepage h1{font-size:30pt}
.statusbox{border:1.5px solid #b8962e;background:#fbf7ec;padding:3mm 5mm;margin:8mm 0 0;font-size:9pt;line-height:1.4} .statusbox p{margin:0 0 1.5mm}
section.epi,section.app{break-before:page} section.app h3{font-size:10pt;margin-top:5mm} section.app p,section.app li{font-size:8.6pt}
figure img{width:100%;display:block} h2,h3,h4{break-after:avoid}
table.idx{width:100%} table.idx td{padding:0.3mm 1.5mm;font-size:8.4pt;border-bottom:1px dotted #ddd} table.idx td.gap{width:6mm;border:none}
body,h1,h2,h3,h4,.sub,.meta,figcaption,table,.status,ol.refs{font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",sans-serif}
body{font-size:10pt}'''
doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>DICTONIC Bonds: from the Octet to the Rule of Halves</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
{front.replace('__TOC__', tochtml)}
{''.join(chapters)}
<section class="epi" id="epilogue">{epi}</section>
<section class="app" id="app"><h1 class="chapter">Appendix. Sources by chapter</h1><p>Each chapter's own list of sources checked, its data and code, and its references, as published with its paper.</p>{''.join(sources)}</section>
{refhtml}
{idxhtml}
{open(os.path.join(HERE, 'about.html'), encoding='utf8').read()}
</body></html>'''
open(os.path.join(HERE, 'paper.html'), 'w', encoding='utf8').write(doc)
imgs = re.findall(r'<img[^>]+src="([^"]+)"', doc); missing = [i for i in imgs if not os.path.exists(os.path.normpath(os.path.join(HERE, i)))]
print('chapters', len(toc), 'referred', sorted(REFERRED), 'index terms', len(INDEX), 'images', len(imgs), 'MISSING', missing, 'chars', len(doc))
