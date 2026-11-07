# Assemble DICTO's book "Star Cores: Spikes, Halos and Cycles" (Cycles of Growth, Part II) from the published paper sources (DICTO
# 2026-11-01; version 1 published 2 November 2026, concept DOI 10.5281/zenodo.23867732). Modelled on book-golden-cycle/assemble.py: each paper becomes a chapter (title, abstract, sections, theorems, tables and
# figures kept word for word); the meta line goes; "Sources checked", "Data and code" and "Sources"/"References" move to one appendix by
# chapter; figures are copied into figures/ch<n>/ and renumbered per chapter. #85 is its latest published version (v3, record 23866680), with the sloping bases at the six convex pieces as ordinary text. Front matter,
# plates, closing chapter and About from front.html, plates.html, epilogue.html, about.html (by hand); the cards are built here from the
# study data (cards.py pictures, studies/2026-11-01-star-cores-book). Output: paper.html (typeset by ../print.mjs).
import re, os, shutil, html, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE); ROOT = os.path.dirname(P); ST = os.path.join(ROOT, 'studies')
CH = [('1', 'spiked-ti', 78), ('2', 'star-cores-a', 79), ('3', 'star-cores-b', 81), ('4', 'star-cores-c', 80), ('5', 'star-cores-d', 85)]
PART = {'1': 'Part I. The TI Star', '2': 'Part II. The star of every solid', '5': 'Part III. Eccentric pieces'}
CORR = [('and asked whether such factors form a series.', 'and proposed that such factors might form a series.'),
        ('DICTO asked whether his sloping bases also stop the six convex pieces.', 'DICTO proposed his sloping bases for the six convex pieces as well.')]
INDEX_TERMS = ['TI Star', 'Star Halo', 'TI Star core', 'truncated icosahedron', 'icosahedron', 'dodecahedron', 'icosidodecahedron',
    'rhombic triacontahedron', 'pentakis dodecahedron', 'Platonic', 'Archimedean', 'Catalan', 'polar', 'polar spikes', 'halo', 'core',
    'star chain', 'growth rule', 'Universal PiTet', 'gnomon', 'Cleo star', 'golden ratio', 'golden spike', 'doubling', 'Conway', 'join',
    'Kleetope', 'Coxeter', 'Euler', 'Dehn', 'valley rule', 'valley law', 'sloping bases', 'dihedral angle', 'gain', 'norm', 'primes',
    'Ogdoecontahedron', 'Hecatodihedron', 'GTI', 'FPD', 'Palintriacontahedron', 'Metaxyhexecontahedron', 'Tweedledum', 'Tweedledee',
    'Samson', 'Sonsam', 'Lahdeli', 'Chucky', 'Fang', 'Triskelion Tetrahedron', 'Dodeca-13 Wedge', 'Dodeca-13 Needle', 'Kagemusha',
    'Maedate', 'Kuwagata', 'OCD Stella', 'Belted Triacontahedron', 'OTT', 'KRE', 'PHE', 'TPP', 'DPHP', 'Icosaxes', 'Unborn Axes', 'David',
    'Delilah', 'Alice', 'White Rabbit', 'Red King', 'Red Knight', 'White Knight', 'Queens', 'Jewel', 'Ganesha', 'Golden TI Star',
    'Cube Pearl', 'Golden Clasp', 'Hamlet', 'Ophelia', 'Polyhedraverse', 'quasicrystal', 'Stewart', 'antipedal']
INDEX = {}
styles = set(); chapters = []; sources = []; toc = []
cw = open(os.path.join(P, 'collected', 'paper.html'), encoding='utf8').read()
PAPERS = {int(m.group(1)): (html.unescape(re.sub('<[^>]+>', '', m.group(2))), m.group(3)) for m in re.finditer(r'<tr><td class="n">#(\d+)</td><td><b>(.*?)</b>.*?DICTO DOI: (10\.5281/zenodo\.\d+)', cw, re.S)}
PAPERS.update({76: ('Between the Queens', '10.5281/zenodo.23780068'), 77: ('Face to Face', '10.5281/zenodo.23779962'),
               78: ('The Truncated Icosahedron Star (TI Star)', '10.5281/zenodo.23782577'), 79: ("Star Cores of DICTO's Solids", '10.5281/zenodo.23822905'),
               80: ("The Gains of DICTO's Growth Rule", '10.5281/zenodo.23822907'), 81: ('Core Cycles', '10.5281/zenodo.23846772'),
               85: ('Eccentric Pieces', '10.5281/zenodo.23850490')})
INBOOK = {num: lab for lab, _, num in CH}
# Part I of the series, The Golden Cycle (v3, concept DOI 10.5281/zenodo.23752452): its chapters by paper number (book-golden-cycle/assemble.py)
PARTI = {22: 1, 23: 2, 24: 3, 27: 4, 29: 5, 32: 6, 33: 7, 34: 8, 35: 9, 38: 10, 39: 11, 43: 12, 54: 14}
SEEN_PARTI = set()
REFERRED = set()
def link_text(t):
    def r(mo):
        n = int(mo.group(1))
        if n in INBOOK: return f'<a href="#ch{INBOOK[n]}">#{n}</a>'
        if n in PARTI and n not in SEEN_PARTI:
            SEEN_PARTI.add(n); REFERRED.add(n)
            return f'<a href="https://doi.org/{PAPERS[n][1]}">#{n}</a> (Part I, Chapter {PARTI[n]})'
        if n in PAPERS: REFERRED.add(n); return f'<a href="https://doi.org/{PAPERS[n][1]}">#{n}</a>'
        return mo.group(0)
    return re.sub(r'(?<![&\w])#(\d{1,2})\b', r, t)
def link_html(h):
    parts = re.split(r'(<[^>]+>)', h); out = []; inA = False
    for p in parts:
        if p.startswith('<'):
            if re.match(r'<a\b', p): inA = True
            if p.startswith('</a'): inA = False
            out.append(p)
        else: out.append(p if inA else link_text(p))
    return ''.join(out)
MOVESEC = r'(\d+\. )?(Reproducibility|Data and reproducibility|Data, scripts and checks|Credits|Appendix[ AB]*\. The reference library searched)'
for label, folder, num in CH:
    s = open(os.path.join(P, folder, 'paper.html'), encoding='utf8').read()
    for st in re.findall(r'<style>(.*?)</style>', s, re.S): styles.add(st.strip())
    doi = re.search(r'DICTO DOI: (10\.5281/zenodo\.\d+)', s).group(1)
    ver = re.search(r'Paper #\d+ · Version (\d+)', s).group(1)
    body = s[s.index('<h1'):s.rindex('</body>')]
    title = html.unescape(re.sub('<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1))).strip()
    body = re.sub(r'<div class="meta">.*?</div>', '', body, count=1, flags=re.S)
    out = [m.group(0) for m in re.finditer(r'<p class="prec">.*?</p>', body, re.S)]
    body = re.sub(r'<p class="prec">.*?</p>', '', body, flags=re.S)
    for m in list(re.finditer(r'<h2>(' + MOVESEC + r'|References)</h2>(.*?)(?=<h2|$)', body, re.S)):
        out.append('<h4>' + m.group(1) + '</h4>' + m.group(4)); body = body.replace(m.group(0), '')
    def fig(mo):
        src = mo.group(1); dst = f'figures/ch{label}/{os.path.basename(src)}'; path = os.path.join(P, folder, src)
        if not os.path.exists(path): raise SystemExit(f'FIG MISSING ch{label} {src}')
        os.makedirs(os.path.join(HERE, os.path.dirname(dst)), exist_ok=True); shutil.copy(path, os.path.join(HERE, dst)); return f'<img src="{dst}"'
    body = re.sub(r'<img src="([^"]+)"', fig, body)
    body = re.sub(r'\bFigure (\d+)', lambda mo: f'Figure {label}.{mo.group(1)}', body)
    body = re.sub(r'\bFig\. (\d+)', lambda mo: f'Fig. {label}.{mo.group(1)}', body)
    for a, b in CORR: body = body.replace(a, b)
    body = body.replace('this paper', 'this chapter').replace('This paper', 'This chapter')
    SEEN_PARTI.clear(); body = link_html(body)
    plain = re.sub('<[^>]+>', ' ', body)
    for term in INDEX_TERMS:
        if re.search(r'\b' + re.escape(term) + r'(s|es)?\b', plain): INDEX.setdefault(term, []).append(label)
    head = f'Chapter {label}. '
    body = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 class="chapter" id="ch{label}">{head}{title}</h1>', body, count=1, flags=re.S)
    note = f' (version {ver})'
    body = body.replace('</h1>', f'</h1>\n<p class="from">From paper #{num}{note}, DICTO DOI {doi}</p>', 1)
    if label in PART: chapters.append(f'<div class="part"><h1 class="partt">{PART[label]}</h1></div>')
    chapters.append(f'<section class="ch">{body}</section>')
    if num == 85: chapters.append('__ECCENTRIC_CARDS__')
    toc.append((head + title, label, num, doi)); sources.append(f'<h3>{head}{html.escape(title)} (#{num}, DICTO DOI {doi})</h3>' + ''.join(out))

# ------------------------------------------------------------------ the cards ------------------------------------------------------------
import cards_data as CD
cards_main, cards_ecc, card_names, summary = CD.build(ST, HERE)
for name, D, anchor in card_names:
    for term in INDEX_TERMS:
        if term.lower() in name.lower(): INDEX.setdefault(term, []).append(f'<a href="#{anchor}">card {D}</a>')
ecc = ('<div class="part" id="ecc-cards"><h1 class="partt">Cards of the eccentric pieces</h1><p class="partsub">The seven pieces of Chapter 5 and DICTO\'s two notch '
       'pieces, one page each</p></div>' + ''.join(cards_ecc))
chapters = [c if c != '__ECCENTRIC_CARDS__' else ecc for c in chapters]
catalogue = ('<section class="cathead" id="catalogue"><h1 class="partt">Part IV. The catalogue of star cores</h1><p class="partsub">One card for every '
             'shape, in the order of DICTO\'s numbers</p>' + open(os.path.join(HERE, 'cards-intro.html'), encoding='utf8').read() + '</section>' + ''.join(cards_main))

def short_core(c):
    m = re.match(r'period two (at once|from turn \d)', c)
    if m: sc = re.search(r'by (t\S*(?: \S+)*?) in length', c); return f"2, {m.group(1).replace('from turn', 'turn')}" + (f"; {sc.group(1)}" if sc else '')
    return re.sub(r' \(.*', '', c).replace('no core at turn', 'no core, turn').replace('not run: Chapter 3 treats the convex shapes', '–')
def short_chain(c):
    if c.startswith('period four, radius gain'): return 'period 4, gain ' + c.split('radius gain ')[1].split(' ≈')[0].split(' (')[0]
    if c.startswith('period four'): return 'period 4'
    if c.startswith('step five') or c.startswith('step six') or c.startswith('the chain of the Ogdoecontahedron'): return 'OG chain, open (9 steps)'
    if c.startswith('the chain of T runs TQHD'): return 'into the OG chain'
    if not c: return '–'
    return {'not closed in eight steps (screened)': 'open (8 steps)', 'not run: no centre fixed by every symmetry': 'no centre', 'not run': '–'}.get(c, c[:40])
def short_valley(c):
    m = re.search(r'three: (.*?) at t = φ, (.*?) at t = 2', c)
    return (m.group(1) + ' / ' + m.group(2)) if m else ('not run' if 'not run' in c else '')
glance = ('<section class="app" id="glance"><h1 class="chapter">Every shape at a glance</h1><p style="font-size:9pt">The cards in one table, in the order of '
          'DICTO\'s numbers. Group: the centre rule of Chapter 2 (A–D). Core: period, turn at which the cycle is entered, and the two-turn length scale '
          '(Chapter 3). Chain of T: Chapter 4, or the screening of Chapter 2, Table 3. Valley: volume added over steps two and three, t = φ / t = 2 '
          '(Chapter 2, Section 7). Rows D106–D109 and the notch pieces come from the book\'s own runs.</p><table class="glance"><tr><th>D</th><th>shape</th><th>group</th><th>core</th><th>chain of T</th><th>valley</th></tr>' +
          ''.join(f'<tr><td><a href="#card-{D}">{D}</a></td><td>{html.escape(n)}</td><td>{g}</td><td>{short_core(c)}</td><td>{short_chain(ch)}</td><td>{short_valley(v)}</td></tr>' for _, D, n, g, c, ch, v in summary) +
          '<tr><td>Notch 1</td><td>Maedate</td><td>–</td><td>decagonal prism, then none (study)</td><td>–</td><td>keeps growing (Chapter 5)</td></tr>'
          '<tr><td>Notch 2</td><td>Kuwagata</td><td>–</td><td>decagonal prism, then none (study)</td><td>–</td><td>stops at step three, t = 2, exactly (Chapter 5; exact: the book\'s own runs)</td></tr></table></section>')
front = open(os.path.join(HERE, 'front.html'), encoding='utf8').read()
epi = open(os.path.join(HERE, 'epilogue.html'), encoding='utf8').read().replace('__NEW4__', open(os.path.join(HERE, 'new4.html'), encoding='utf8').read())
plates = open(os.path.join(HERE, 'plates.html'), encoding='utf8').read()
for t in INDEX_TERMS:
    if re.search(r'\b' + re.escape(t) + r'(s|es)?\b', re.sub('<[^>]+>', ' ', epi)): INDEX.setdefault(t, []).append('Closing')
refhtml = ('<section class="app"><h1 class="chapter" id="refs">Papers referred to, not in this book</h1><table>' +
           ''.join(f'<tr><td>#{n}</td><td>{html.escape(PAPERS[n][0])}{(" (Part I, The Golden Cycle, Chapter " + str(PARTI[n]) + ")") if n in PARTI else ""}</td><td><a href="https://doi.org/{PAPERS[n][1]}">{PAPERS[n][1]}</a></td></tr>' for n in sorted(REFERRED)) +
           '</table></section>')
def nice(t): return re.sub('<[^>]+>', '', t)
def refs(v):
    seen = []; [seen.append(x) for x in v if x not in seen]
    return ', '.join(x if x.startswith('<a') or x == 'Closing' else f'<a href="#ch{x}">{x}</a>' for x in seen)
def two_col(items):
    h = (len(items) + 1) // 2; L, R = items[:h], items[h:] + [('', '')] * (2 * h - len(items))
    return '<table class="idx">' + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td class="gap"></td><td><b>{c}</b></td><td>{d}</td></tr>' for (a, b), (c, d) in zip(L, R)) + '</table>'
idxhtml = ('<section class="app"><h1 class="chapter" id="index">Index</h1><p style="font-size:9pt">Chapters, the closing chapter and the cards in which each term appears.</p>' +
           two_col([(nice(t), refs(v)) for t, v in sorted(INDEX.items(), key=lambda kv: nice(kv[0]).lower())]) +
           '<h2>The cards by name</h2>' + two_col([(html.escape(n), f'<a href="#{a}">{D}</a>') for n, D, a in sorted(card_names, key=lambda x: x[0].lower())]) + '</section>')
tochtml = ('<h2>Contents</h2><table class="toc">' + ''.join(f'<tr><td><a href="#ch{tag}">{html.escape(t)}</a></td><td>#{n}</td></tr>' for t, tag, n, d in toc) +
           '<tr><td><a href="#ecc-cards">Cards of the eccentric pieces (9)</a></td><td></td></tr>'
           '<tr><td><a href="#plates">Plates</a></td><td></td></tr><tr><td><a href="#catalogue">Part IV. The catalogue of star cores (' + str(len(cards_main)) + ' cards)</a></td><td></td></tr>'
           '<tr><td><a href="#glance">Every shape at a glance</a></td><td></td></tr><tr><td><a href="#closing">Closing. Spikes, halos and cycles</a></td><td></td></tr><tr><td><a href="#app">Appendix. Sources by chapter</a></td><td></td></tr>'
           '<tr><td><a href="#refs">Papers referred to, not in this book</a></td><td></td></tr><tr><td><a href="#index">Index</a></td><td></td></tr></table>')
css = '\n'.join(sorted(styles)) + '''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font-size:8.5pt;color:#777;margin:-2mm 0 4mm}
.part{break-before:page;height:200mm;display:flex;flex-direction:column;align-items:center;justify-content:center} h1.partt{font-size:26pt;color:#b8962e;text-align:center} p.partsub{font-size:11pt;color:#555}
table.toc td{border-bottom:1px dotted #ccc;padding:1.2mm 2mm} table.toc a, table.idx a{color:inherit;text-decoration:none}
.titlepage{min-height:240mm;display:flex;flex-direction:column;justify-content:flex-start} .titlepage h1{font-size:30pt}
section.epi,section.app{break-before:page} section.app h3{font-size:10pt;margin-top:5mm} section.app p,section.app li{font-size:8.6pt}
figure img{width:100%;display:block}
.added{border:1.5px solid #2bb3a3;background:#f1fbf9;padding:2mm 4mm;margin:4mm 0} .added p.addk{font-weight:600;color:#1d7f74;font-size:9pt}
section.plate{break-before:page;break-inside:avoid} section.plate>img{display:block;width:100%;height:auto;margin:0 auto}
.pcap h2{margin:3mm 0 1mm;font-size:14pt} .pcap p.pkey{font-size:9.6pt;color:#555;margin:0 0 2mm} .pcap ul{margin:0;padding-left:5mm} .pcap li{font-size:10.5pt;line-height:1.4;margin:0 0 1.2mm}
section.card{break-before:page;break-inside:avoid} section.card h2.cardt{font-size:15pt;margin:0 0 1mm;color:#222} section.card h2.cardt span.dn{color:#b8962e;margin-right:2mm}
section.card p.pkey{font-size:9pt;color:#444;margin:0 0 1mm} section.card figure{margin:0 0 1mm}
section.card table.cd{font-size:8.5pt;line-height:1.28;margin:0;width:100%} section.card table.cd th{width:34mm;font-weight:600;color:#6b5310;padding:0.6mm 1.5mm 0.6mm 0}
section.card table.cd td{padding:0.8mm 0} section.card p.cnote{font-size:7.6pt;color:#555;margin:1mm 0 0}
section.cathead{break-before:page;padding-top:30mm} section.cathead h1.partt{margin-bottom:2mm} section.cathead p.partsub{text-align:center;margin-bottom:14mm}
div.idx2{column-count:2;column-gap:8mm;font-size:8.6pt;line-height:1.35} div.idx2 div{break-inside:avoid;margin:0 0 .5mm} div.idx2 a{color:inherit;text-decoration:none}
table.glance{break-inside:auto;width:100%} table.glance tr{break-inside:avoid} table.glance td,table.glance th{font-size:7.6pt;padding:0.3mm 1.5mm;border-bottom:1px dotted #ddd} table.glance a{color:inherit;text-decoration:none}
table.idx{width:100%} table.idx td{padding:0.3mm 1.5mm;font-size:8.4pt;border-bottom:1px dotted #ddd} table.idx td.gap{width:6mm;border:none}
/* DICTO 10-29: neutral sans-serif for the whole book, as in HexOct */
body,h1,h2,h3,h4,.sub,.meta,figcaption,table,.status,ol.refs{font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",sans-serif}
body{font-size:10pt}'''
doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Star Cores</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
{front.replace('__TOC__', tochtml)}
{''.join(chapters)}
{plates}
{catalogue}
{glance}
<section class="epi" id="closing">{epi}</section>
<section class="app" id="app"><h1 class="chapter">Appendix. Sources by chapter</h1><p>Each chapter's own list of sources checked, data and code, as published with its paper.</p>{''.join(sources)}
<h3>The cards and plates</h3><p>Pictures: studies/2026-11-01-star-cores-book, scripts/cards.py and plates.py (painter and constructions imported from figs_paper_a.py, star_core.py and star_valley.py of study 2026-10-30-star-cores, and the notch pieces as in kagemusha_variants.py of study 2026-11-01-star-cores-d), rendered on dicto-big-brother at 300 dpi. Card data: DICTO Solids v7 (dataset concept DOI 10.5281/zenodo.23606967, version 10.5281/zenodo.23850845); star-cores.json, polar-spikes.json, sloping-bases.json, star-valley.json (study 2026-10-30-star-cores); study2b.json and gains (study 2026-10-30-star-cores-exact); valley-law-predict.json, kagemusha-variants.json, kuwagata-cycle.json and sloping-six (study 2026-11-01-star-cores-d); the treatment of Cube Pearl, Golden Clasp, Hamlet and Ophelia (scripts/new4.py, run_new4.sh of the book study).</p></section>
{refhtml}
{idxhtml}
{open(os.path.join(HERE, 'about.html'), encoding='utf8').read()}
</body></html>'''
open(os.path.join(HERE, 'paper.html'), 'w', encoding='utf8').write(doc)
imgs = re.findall(r'<img[^>]+src="([^"]+)"', doc); missing = [i for i in imgs if not os.path.exists(os.path.normpath(os.path.join(HERE, i)))]
print('chapters', len(toc), 'cards', len(cards_main), '+', len(cards_ecc), 'referred', len(REFERRED), 'index terms', len(INDEX), 'images', len(imgs), 'MISSING', missing, 'chars', len(doc))
