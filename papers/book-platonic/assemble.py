# Assemble DICTO's Platonic book (working title; the title is DICTO's) from hand-written chapter files and the published papers.
# Plan: papers/plan-book-platonic (11 Nov 2026); DICTO 13 Nov 2026: books first, this is the third.
# Modelled on book-golden-cycle/ and book-star-cores/, with one difference: a chapter here draws on SEVERAL papers. Each chapter is a
# hand-written file chapters/chNN.html (opening, bridges, study results, the chapter's claims and open items) holding include lines
#   <!--INC <paper number> sec=<keys> [lead]-->
# which pull the named sections of the published paper word for word: h2 headings become h3 headings "From #N, §k. title"; the
# paper's own theorem numbers are kept (each block says which paper it is from); figures are copied to figures/chNN/ and renumbered
# through the chapter (references to figures of the paper that are not included read "Figure k of #N"); "this paper" becomes "#N".
# A short list of edits (EDITS) removes the running "DICTO proposed/asked" credit lines (FIRM 11-09: DICTO is the author) and the
# words the house rules ban. Each included paper's prior-art, sources-checked, data and reference sections go to the appendix
# "Sources by chapter". Output: paper.html, typeset by ../print.mjs.
import re, os, shutil, html, json
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE); ROOT = os.path.dirname(P); ST = os.path.join(ROOT, 'studies')
FOLDER = {8: 'ekp', 99: '2026-11-06-five-in-octet', 88: 'golden-truncated-triangles', 90: 'six-dimensions-golden-cubes',
          44: '2026-10-21-aristotles-pyramid', 77: 'face-to-face', 92: '2026-11-04-pyramid-tilings', 87: 'dicto-vacuus',
          107: '2026-11-11-queens-vacuus', 45: '2026-10-21-reuleaux-platonic', 19: '../studies/2026-10-14-axe-cleo-fuji/paper',
          22: 'chain-of-karma', 42: '2026-10-20-dicto-sunstar', 47: '2026-10-22-platonic-mixes', 106: '2026-11-10-one-world',
          41: '2026-10-20-dicto-jewel', 108: '2026-11-11-atlas-chains'}
FILE = {19: 'paper-house.html'}
DOI = {19: '10.5281/zenodo.23351291'}   # #19's meta line gives the DOI without the "DICTO DOI:" label
# chapters: (label, file, part heading or None)
CH = [('1', 'ch01.html', 'Part One. Inside the five'), ('2', 'ch02.html', None), ('3', 'ch03.html', None), ('4', 'ch04.html', None),
      ('5', 'ch05.html', None), ('6', 'ch06.html', 'Part Two. The five fill space'), ('7', 'ch07.html', None), ('8', 'ch08.html', None),
      ('9', 'ch09.html', None), ('10', 'ch10.html', None), ('11', 'ch11.html', 'Part Three. Where the five live'), ('12', 'ch12.html', None),
      ('13', 'ch13.html', None), ('Coda', 'coda.html', None)]
# sections that never go into a chapter body: they go to the appendix
MOVE = r'(\d+\. )?(Reproducibility|Data and reproducibility|Data, scripts and checks|Credits|Naming|References|Sources checked|Sources and sources checked|Sources|Appendix[ AB]*\. The reference library searched|Prior art.*|Relation to known work.*|What is known and what is new|What is new and what is known|In the app|Build it|Remarks)'
EDITS = [  # (old, new): applied to included text only; each was read in its sentence
    ("building the same body on all five Platonic solids, as one family, is DICTO's idea, and the other four did not appear", "built on all five Platonic solids the same body makes one family, and the other four did not appear"),
    ('Aristotle wrote that the pyramid fills space; DICTO proposed that he may have meant one of these.', 'Aristotle wrote that the pyramid fills space; he may have meant one of these.'),
    ('DICTO also proposed the question of how the whole Platonic solids fill space. His earlier exact work answers it for all five:', 'How the whole Platonic solids fill space is answered for all five by DICTO\'s earlier exact work:'),
    ('DICTO proposed that it may have been Bradwardine\'s tetrahedron, the Cleo-Icos.', 'It may have been Bradwardine\'s tetrahedron, the Cleo-Icos.'),
    ('and where DICTO\'s proposal fits', 'and where the face-pyramid reading fits'),
    ('DICTO proposed <i>pyramidise</i> as one operation on any solid', '<i>Pyramidise</i> is one operation on any solid'),
    ('DICTO proposed the Star as the step that turns each centre pyramid out over its own face.', 'The Star is the step that turns each centre pyramid out over its own face.'),
    ('DICTO proposed that the pyramid could be a face pyramid, and in paper #44 [1] we proved Aristotle\'s Pyramid Theorem:', 'Read as a face pyramid, it gives Aristotle\'s Pyramid Theorem, proved in paper #44 [1]:'),
    (' DICTO proposed that he may have meant the Cleo-Icos.', ' he may have meant the Cleo-Icos.'),
    ('The question is DICTO\'s: Aristotle', 'Aristotle'),
    ('DICTO proposed the product of cube and octahedron as the six-dimensional home of the pair:', 'The product of cube and octahedron is the six-dimensional home of the pair:'),
]
BANNED = re.compile(r'football|flat-ended|in plain words|simply put|in short\s*:|DICTO asked|asked by DICTO|DICTO proposed|DICTO chose|DICTO\'s choice|selected by', re.I)

conc = json.load(open(os.path.join(P, 'dicto-concordance', 'concordance.json'), encoding='utf8'))
PAPERS = {}
for k, v in conc['papers'].items():
    if k.isdigit():
        d = str(v.get('doi', '')); d = d if d.startswith('10.') else '10.5281/zenodo.' + d
        PAPERS[int(k)] = (v['title'], d)
INBOOK = {}     # paper number -> chapter label where it is used first
REFERRED = set(); styles = set(); sources = {}; INDEX = {}
INDEX_TERMS = ['Euclid', 'Pacioli', 'Kepler', 'Plato', 'Aristotle', 'Hart', 'Dehn', 'golden ratio', 'golden cut', 'Golden Cut', 'Icosaxes',
               'Unborn Axes', 'Cleo-Icos', 'Antonius', 'AXE', 'CLEO', 'FUJI', 'Lotus seed', 'Chain of Karma', 'Admiral Cap', 'Dogstar',
               'Sunstar', 'Jewel', 'EKP', 'octet', 'Vacuus', 'Angelus', 'Angeli', 'Mirror Law', 'Reuleaux', 'Ogdoecontahedron', 'OG',
               'pentakis dodecahedron', 'stella octangula', 'great stellated dodecahedron', '600-cell', '120-cell', '24-cell',
               'snub 24-cell', 'quasicrystal', 'approximant', 'Galois twin', 'Dodeca-13', 'UNITY', 'Sheriff', 'Lone-star', 'roof']

def copyfig(src, folder, label):
    raw = 'https://raw.githubusercontent.com/DICTOR-Master/kaleidohedra/master/'
    path = os.path.join(ROOT, src[len(raw):]) if src.startswith(raw) else os.path.normpath(os.path.join(P, folder, src))
    if not os.path.exists(path): raise SystemExit(f'FIG MISSING ch{label} {src} ({path})')
    dst = f'figures/ch{label}/{os.path.basename(src)}'
    os.makedirs(os.path.join(HERE, os.path.dirname(dst)), exist_ok=True); shutil.copy(path, os.path.join(HERE, dst)); return dst

def sections(body):
    """split a paper body at its h2 headings: [(heading text, html)]"""
    parts = re.split(r'(<h2[^>]*>.*?</h2>)', body, flags=re.S)
    out = [('__lead__', parts[0])]
    for i in range(1, len(parts), 2):
        out.append((html.unescape(re.sub('<[^>]+>', '', parts[i])).strip(), parts[i + 1]))
    return out

def include(num, keys, lead, label):
    folder = FOLDER[num]; s = open(os.path.join(P, folder, FILE.get(num, 'paper.html')), encoding='utf8').read()
    for st in re.findall(r'<style>(.*?)</style>', s, re.S): styles.add(st.strip())
    doi = DOI.get(num) or re.search(r'DICTO DOI: (10\.5281/zenodo\.\d+)', s).group(1)
    title = PAPERS.get(num, (None,))[0] or html.unescape(re.sub('<[^>]+>', '', re.search(r'<title>(.*?)</title>', s, re.S).group(1)))
    body = s[s.index('<body'):s.rindex('</body>')]
    body = body[body.index('>') + 1:]
    secs = sections(body)
    INBOOK.setdefault(num, label)
    # appendix material of this paper (once)
    if num not in sources:
        app = [f'<h4>{html.escape(h)}</h4>{b}' for h, b in secs[1:] if re.match(MOVE + r'$', h)]
        sources[num] = (title, doi, app, label)
    picked = []
    if lead:
        L = secs[0][1]
        L = re.sub(r'<img class="(watermark|logo)"[^>]*>', '', L)
        L = re.sub(r'<h1.*?</h1>', '', L, flags=re.S); L = re.sub(r'<p class="(sub|version|small)".*?</p>', '', L, flags=re.S)
        for cls in ('meta', 'abstract', 'status'):
            L = re.sub(r'<div class="' + cls + r'">.*?</div>\s*(?=<|$)', '', L, flags=re.S)
        L = re.sub(r'<p class="(meta|status)".*?</p>', '', L, flags=re.S)
        if lead == 'figs': L = ''.join(re.findall(r'<figure.*?</figure>|<div class="figs.*?</div>\s*</figure>', L, re.S))
        picked.append(('', L))
    for k in keys:
        hit = [(h, b) for h, b in secs[1:] if h.split('.')[0].strip() == k or (not k.isdigit() and h.startswith(k))]
        if not hit: raise SystemExit(f'SECTION {k} not found in #{num}: {[h for h, _ in secs]}')
        picked.append(hit[0])
    out = []
    for h, b in picked:
        if h:
            m = re.match(r'(\d+)\. (.*)', h)
            hh = f'#{num} §{m.group(1)}. {m.group(2)}' if m else f'#{num}: {h}'
            out.append(f'<h3 class="from">{html.escape(hh)}</h3>')
        out.append(b)
    blk = ''.join(out)
    blk = re.sub(r'<p class="prec">.*?</p>', '', blk, flags=re.S)
    # figures: copy, renumber through the chapter
    blk = re.sub(r'<img ([^>]*?)src="([^"]+)"', lambda mo: f'<img {mo.group(1)}src="{copyfig(mo.group(2), folder, label)}"', blk)
    caps = re.findall(r'<figcaption[^>]*>\s*(?:<b>)?\s*(Figure|Fig\.|Plate)s? (\d+)(?:[–-](\d+))?', blk)
    fmap = {}
    for kind, a, b in caps:
        for n in range(int(a), int(b or a) + 1): fmap.setdefault(n, f'⟦{num}-{n}⟧')
    def fref(mo):
        word, a, dash, b = mo.group(1), int(mo.group(2)), mo.group(3), mo.group(4)
        w = 'Figure' + ('s' if re.match(r'\w+s ', mo.group(0)) else '')
        if a in fmap and (not b or int(b) in fmap):
            return f'{w} {fmap[a]}' + (f'{dash}{fmap[int(b)]}' if b else '')
        return f'{w} {a}{dash or ""}{b or ""} of #{num}'
    blk = re.sub(r'\b(Figure|Fig\.|Plate)s? (\d+)(?:(–|-|, | and )(\d+))?(?![\d.]\d)', fref, blk)
    for a, b in EDITS: blk = blk.replace(a, b)
    blk = blk.replace('this paper', f'#{num}').replace('This paper', f'Paper #{num}')
    note = (f'<p class="from">The sections below are from #{num}, <i>{html.escape(title)}</i> (DICTO DOI: {doi}), word for word; figures are '
            f'renumbered through the chapter, and numbers in square brackets refer to the references of #{num} (Appendix).</p>')
    return note + f'<div class="inc">{blk}</div>'

def link_text(t):
    def r(mo):
        n = int(mo.group(1))
        if n in INBOOK: return f'<a href="#ch{INBOOK[n]}">#{n}</a>'
        if n in PAPERS: REFERRED.add(n); return f'<a href="https://doi.org/{PAPERS[n][1]}">#{n}</a>'
        return mo.group(0)
    return re.sub(r'(?<![&\w/])#(\d{1,3})\b', r, t)
def link_html(h):
    parts = re.split(r'(<[^>]+>)', h); out = []; inA = 0
    for p in parts:
        if p.startswith('<'):
            if re.match(r'<a\b', p): inA = 1
            if p.startswith('</a'): inA = 0
            out.append(p)
        else: out.append(p if inA else link_text(p))
    return ''.join(out)

# pass 1: read every chapter file, expand includes (records INBOOK before linking)
chapters = []; toc = []
for label, fn, part in CH:
    src = open(os.path.join(HERE, 'chapters', fn), encoding='utf8').read()
    src = re.sub(r'<!--INC (\d+) sec=([\w,]*)( lead| figs)?-->', lambda mo: include(int(mo.group(1)), [k for k in mo.group(2).split(',') if k], (mo.group(3) or '').strip(), label), src)
    order = []
    for cap in re.findall(r'<figcaption[^>]*>.*?</figcaption>', src, re.S):
        head = re.match(r'<figcaption[^>]*>\s*(?:<b>)?\s*Figures? ((?:⟦[^⟧]+⟧(?:–|-|, | and )?)+)', cap)
        if head:
            toks = re.findall(r'⟦[^⟧]+⟧', head.group(1))
            m2 = re.match(r'⟦(\d+)-(\d+)⟧[–-]⟦\1-(\d+)⟧', head.group(1))
            if m2: toks = [f'⟦{m2.group(1)}-{k}⟧' for k in range(int(m2.group(2)), int(m2.group(3)) + 1)]
            for t in toks:
                if t not in order: order.append(t)
    for i, t in enumerate(order, 1): src = src.replace(t, f'{label}.{i}')
    if '⟦' in src: raise SystemExit(f'unnumbered figure in chapter {label}: ' + re.search(r'.{80}⟦[^⟧]+⟧.{20}', src, re.S).group(0))
    title = html.unescape(re.sub('<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', src, re.S).group(1))).strip()
    chapters.append((label, part, src)); toc.append((label, title))
# study figures used by the hand-written text: <img src="study:<folder>/<path>"> is copied to figures/ch<label>/
out = []
for label, part, src in chapters:
    src = re.sub(r'src="study:([^"]+)"', lambda mo: 'src="' + copyfig(os.path.join(ST, mo.group(1)), '', label) + '"', src)
    src = re.sub(r'src="paper:([^"]+)"', lambda mo: 'src="' + copyfig(os.path.join(P, mo.group(1)), '', label) + '"', src)
    plain = re.sub('<[^>]+>', ' ', src)
    for term in INDEX_TERMS:
        if re.search(r'\b' + re.escape(term) + r'(s|es)?\b', plain): INDEX.setdefault(term, []).append(label)
    src = link_html(src)
    if part: out.append(f'<div class="part"><h1 class="partt">{part}</h1></div>')
    out.append(f'<section class="ch" id="ch{label}">{src}</section>')
body = ''.join(out)
front = link_html(open(os.path.join(HERE, 'front.html'), encoding='utf8').read())
epi = link_html(open(os.path.join(HERE, 'epilogue.html'), encoding='utf8').read())
about = open(os.path.join(HERE, 'about.html'), encoding='utf8').read()
refs = open(os.path.join(HERE, 'references.html'), encoding='utf8').read()
for label, fn in [('front', 'front.html'), ('epilogue', 'epilogue.html')]:
    s = open(os.path.join(HERE, fn), encoding='utf8').read()
    s = re.sub(r'src="study:([^"]+)"', lambda mo: 'src="' + copyfig(os.path.join(ST, mo.group(1)), '', label) + '"', s)
    if label == 'front': front = link_html(s)
    else: epi = link_html(s)
# appendix: sources by chapter, in the order the papers are first used
app = ['<section class="app" id="app"><h1 class="chapter">Appendix. Sources by chapter</h1><p>For every paper drawn on, as published with it: '
       'its prior-art and status sections, the sources checked, data and code, and its numbered references (the numbers in square '
       'brackets inside the chapters).</p>']
for num, (title, doi, parts, label) in sorted(sources.items(), key=lambda kv: (CH.index(next(c for c in CH if c[0] == kv[1][3])), kv[0])):
    app.append(f'<h3>#{num} {html.escape(title)} (DICTO DOI: {doi}), used from Chapter {label}</h3>' + ''.join(parts))
app.append('</section>')
apphtml = link_html(''.join(app))
for num in list(REFERRED):
    if num in INBOOK: REFERRED.discard(num)
inbook = ('<section class="app" id="papers"><h1 class="chapter">Papers in this book</h1><table class="toc">' +
          ''.join(f'<tr><td>#{n}</td><td>{html.escape(sources[n][0])}</td><td>Chapter {INBOOK[n]}</td><td><a href="https://doi.org/{sources[n][1]}">{sources[n][1]}</a></td></tr>' for n in sorted(sources)) +
          '</table><h2 id="refs">Papers referred to</h2><p style="font-size:9pt">DICTO\'s papers named in the text that are not drawn on as a source.</p><table class="toc">' +
          ''.join(f'<tr><td>#{n}</td><td>{html.escape(PAPERS[n][0])}</td><td><a href="https://doi.org/{PAPERS[n][1]}">{PAPERS[n][1]}</a></td></tr>' for n in sorted(REFERRED)) +
          '</table></section>')
def nice(t): return re.sub('<[^>]+>', '', t)
idx = ('<section class="app" id="index"><h1 class="chapter">Index</h1><p style="font-size:9pt">Chapters in which each term appears.</p><table class="idx">' +
       ''.join(f'<tr><td>{nice(t)}</td><td>{", ".join(dict.fromkeys(v))}</td></tr>' for t, v in sorted(INDEX.items(), key=lambda kv: kv[0].lower())) + '</table></section>')
tochtml = ('<h2>Contents</h2><table class="toc"><tr><td><a href="#opening">Opening. The Outsider</a></td></tr>' +
           ''.join((f'<tr><td class="tp">{p}</td></tr>' if p else '') + f'<tr><td><a href="#ch{l}">{"Coda" if l == "Coda" else "Chapter " + l}. {html.escape(t.split(". ", 1)[-1] if t.startswith(("Chapter", "Coda")) else t)}</a></td></tr>'
                   for (l, t), (_, _, p) in zip(toc, CH)) +
           '<tr><td><a href="#epilogue">Epilogue. What has been shown</a></td></tr><tr><td><a href="#app">Appendix. Sources by chapter</a></td></tr>'
           '<tr><td><a href="#papers">Papers in this book, and papers referred to</a></td></tr><tr><td><a href="#classical">References</a></td></tr>'
           '<tr><td><a href="#index">Index</a></td></tr><tr><td><a href="#about">About the author</a></td></tr></table>')
css = '\n'.join(sorted(styles)) + '''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font-size:8.3pt;color:#777;margin:1mm 0 2mm;font-family:"DejaVu Sans",sans-serif}
h3.from{font:600 10.5pt "DejaVu Sans",sans-serif;color:#6b5310;margin:10pt 0 3pt;break-after:avoid}
div.inc{border-left:2px solid #e6dcc0;padding-left:3mm;margin:2mm 0 4mm}
.part{break-before:page;height:200mm;display:flex;flex-direction:column;align-items:center;justify-content:center} h1.partt{font-size:26pt;color:#b8962e;text-align:center}
table.toc td{border-bottom:1px dotted #ccc;padding:1.1mm 2mm} table.toc td.tp{font-weight:600;color:#6b5310;border:none;padding-top:3mm} table.toc a, table.idx a{color:inherit;text-decoration:none}
.titlepage{min-height:240mm;display:flex;flex-direction:column;justify-content:flex-start} .titlepage h1{font-size:30pt}
section.epi,section.app,section.about{break-before:page} section.app h3{font-size:10pt;margin-top:5mm} section.app p,section.app li,section.app td{font-size:8.6pt}
.claims{border:0.4pt solid #b9a46a;background:#fbf8ee;padding:2mm 3mm;margin:3mm 0;break-inside:avoid;font-size:9.4pt}
.claims p{margin:1mm 0}
.thmbox{border-left:3px solid #b8962e;background:#faf6ea;padding:2mm 3mm;margin:2mm 0;break-inside:avoid}
figure img{max-width:100%} figure.one img{width:100%;display:block}
span.el{display:inline-block;width:1.15em;text-align:center;font-weight:700;color:#fff;border-radius:2px;font-family:"DejaVu Sans",sans-serif;font-size:0.9em}
span.D{background:#8a5cc4} span.I{background:#3a70cd} span.C{background:#488e48} span.T{background:#cd3e28} span.O{background:#e8c852;color:#222}
.coverph{height:250mm;display:flex;align-items:center;justify-content:center;border:1.5px dashed #b8962e;color:#8a7440;font:16pt "DejaVu Sans",sans-serif;box-sizing:border-box}
body,h1,h2,h3,h4,.sub,.meta,figcaption,table,.status{font-family:"DejaVu Sans","Liberation Sans",sans-serif}
body{font-size:10pt}
table{max-width:100%} td,th{overflow-wrap:anywhere}'''
doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>The Five Solids (working title)</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
{front.replace('__TOC__', tochtml)}
{body}
<section class="epi" id="epilogue">{epi}</section>
{apphtml}
{inbook}
{refs}
{idx}
{about}
</body></html>'''
hits = [doc_m.group(0) for doc_m in BANNED.finditer(re.sub('<[^>]+>', ' ', doc))]
open(os.path.join(HERE, 'paper.html'), 'w', encoding='utf8').write(doc)
print('chapters', len(chapters), 'papers in book', len(sources), 'referred', len(REFERRED), 'figures', sum(len(fs) for _, _, fs in os.walk(os.path.join(HERE, 'figures'))),
      'chars', len(doc), 'BANNED' if hits else 'banned 0', hits[:20])
