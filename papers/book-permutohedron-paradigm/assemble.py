# Assemble DICTO's book "The Permutohedron Paradigm" (working title; the title is DICTO's) from its chapter drafts
# papers/paradigm-ch01 ... paradigm-ch13 and paradigm-coda (DICTO 13 Nov 2026: one book, not chapter by chapter).
# Modelled on book-golden-cycle/assemble.py and book-star-cores/assemble.py. Each chapter keeps its text, theorems, proofs,
# tables and figures; the meta line and the per-chapter status box go (the book has one status box, front.html); labels,
# figures, tables and sections are numbered by chapter; every edit beyond that is listed in EDITS below and must apply
# exactly once (the script stops otherwise). "Further reading" moves to the one References list (references.html), the
# per-chapter check notes and Chapter 13's "Data and methods" to the appendix Checks and data. Figures are copied into
# figures/ch<N>/; figures-fixed/ (made by fix_figures.py) overrides them. Output: paper.html, typeset by ../print.mjs (build.sh).
import re, os, shutil, html
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
CH = [(str(i), f'paradigm-ch{i:02d}') for i in range(1, 14)] + [('Coda', 'paradigm-coda')]
PART = {'1': ('Part One. Three dimensions', 'The permutohedra of three and four values: the truncated triangle, Kelvin\'s cell, the golden loop and the web of bonds; then a build of DICTO\'s that leads out of the family, and the scutoid.'),
        '6': ('Part Two. Four dimensions', 'The permutohedron of five values: its Vacuus and its heart, its sweep as a tissue, the rosettes, the walls of the Swap Rule and the mirrors of the Queens.'),
        '11': ('Part Three. Every dimension', 'The Vacuus and the sweep counted for every number of values, the golden slice of the 4D filling, and change ringing on the permutohedra of three to eight values.')}

# DICTO's papers: the Collected Works table, plus the papers newer than it
cw = open(os.path.join(P, 'collected', 'paper.html'), encoding='utf8').read()
PAPERS = {int(m.group(1)): (html.unescape(re.sub('<[^>]+>', '', m.group(2))), m.group(3)) for m in re.finditer(r'<tr><td class="n">#(\d+)</td><td><b>(.*?)</b>.*?DICTO DOI: (10\.5281/zenodo\.\d+)', cw, re.S)}
PAPERS.update({104: ('Scutoid Tissues in Four Dimensions', '10.5281/zenodo.24111864'),
               105: ('DICTO 1:2 Truncated Octahedron: The 4D Vacuus of the Permutohedron', '10.5281/zenodo.24121177'),
               107: ('The Vacuus of the Queens', '10.5281/zenodo.24126800'),
               108: ('The Atlas of the Chains', '10.5281/zenodo.24126802')})
def D(n): return f'#{n} (DICTO DOI: {PAPERS[n][1]})'

# the line under each chapter title: where the chapter comes from, with the DICTO DOIs of its original papers
FROM = {
 '1': f'Retold from {D(88)} and {D(20)}, with #48 and #105. Lemma 1.1 and its reading of DICTO\'s solids as gap ratios are new in this book.',
 '2': f'Retold from {D(48)}, {D(105)} and {D(93)}. Proposition 2.1 and the reading of the golden loop as symmetric spacings are new in this book.',
 '3': f'Retold from {D(52)}, {D(53)} and {D(90)}, with #105. The reading of the weight as the spacing, d = (g − m)/(g + m), is new in this book.',
 '4': f'New in this book, from DICTO\'s Hemi RD build in Polyhedraverse (11 November 2026); background in {D(58)} and {D(87)}.',
 '5': f'Re-edited from DICTO\'s draft Scutoids: Layers, Shells and Cycles (10 November 2026, not published) and {D(104)}. Section 5.1 is new in this book.',
 '6': f'Re-edited from {D(105)}, Sections 1–3. Section 6.4 comes from {D(107)} and {D(108)}.',
 '7': f'Re-edited from {D(104)}, Section 1. Sections 7.2 and 7.3 come from Chapter 5 and {D(108)}.',
 '8': f'New in this book, from {D(104)}, Lemma 5, and the Atlas of {D(108)}.',
 '9': f'Re-edited from {D(104)}, Sections 2 and 3, which prove below s = 1/4 the Swap Rule of {D(61)}.',
 '10': f'Re-edited from {D(107)}, Sections 1–5 and Figure 1. Section 10.6 is new in this book.',
 '11': f'Re-edited from {D(105)}, Section 4, and {D(104)}, Theorem 1′. Proposition 11.2 for every n is new in this book.',
 '12': f'New in this book. It answers the second lead of {D(105)}.',
 '13': f'New in this book. It reads the three principles of Kyushindo, as {D(43)} gives them, in English change ringing.',
 'Coda': f'Re-edited from {D(105)}, Section 6, with a closing paragraph on what the book added.'}

# checks and data, by chapter (from each chapter draft's status box; studies under studies/ of the research branch)
CHECKS = {
 '1': 'studies/2026-11-11-paradigm-ch1: key_lemma.py (exact, symbolic; the faces of the solids of Section 1.3 computed from their hulls; log kept; FINAL ok), fig_three.py (Figure 1.1). Commit d79c1d1f; checked independently on 11 November 2026, all findings fixed.',
 '2': 'studies/2026-11-11-paradigm-ch2: symmetry.py (the full symmetry group of the corners for four symmetric and three non-symmetric spacings; exact; FINAL ok). Commit becdcba3. The identification of T(x): #105, Theorem 4 (dictonic_family.py in studies/2026-11-10-permutohedron).',
 '3': 'studies/2026-11-11-paradigm-ch3: weight_map.py (exact, corner by corner, at d = −1/3, 0, 1/τ³, 1/3, 2/7, and every site within ±8 at six weights; FINAL ok), fig_slider.py (Figure 3.1). Commit d79c1d1f; checked independently on 11 November 2026, all findings fixed.',
 '4': 'studies/2026-11-11-hemi-rd-build: analyse_build.py (DICTO\'s world export with exact transforms; float geometry: the hull matched to 10<sup>−9</sup>, volumes to 10<sup>−6</sup>, the six pyramids found empty by sampling), fill_test.py (a numerical first test), exact_fill.py (Theorem 4.3 in rational arithmetic: 487 pairs separated by exact planes, densities 15 + 1 = 16; FINAL ok). Commit 52b55686. studies/2026-11-11-paradigm-ch4: fig_ch4.py (Figure 4.1; FINAL ok), commit 7f2c451e.',
 '5': 'studies/2026-11-11-paradigm-ch5: swap_orderings.py (all 120 orderings for three directions; exact; FINAL ok), commit bc0c7781. Theorems 5.2–5.4: the draft Scutoids: Layers, Shells and Cycles (commit e932cb55) and its studies of 17 October and 6–10 November 2026 (faces flat to 10<sup>−13</sup>, volumes adding up). Proposition 5.5: the study of 6–7 November 2026 (layer spacing solved from exact contact planes, corners to 400 digits; h written exactly in ℚ(2 cos 6°), FINAL ok).',
 '6': 'studies/2026-11-10-permutohedron (the study of #105; commit 3f41e5b3): the 65 slices and their shapes in exact rational arithmetic, every face confirmed exactly, Euler number 2 for every shape; web_of_bonds.py (the classical facts of Section 6.1 recounted exactly); the six corners of Theorem 6.2 confirmed against all 150 faces. Section 6.4: #107 and #108 (studies/2026-11-11-orbit-polytopes).',
 '7': 'The studies named in #104 (sweeps of the 120-cell, the truncated 120-cell and the bitruncated 600-cell in nine generic directions; the 5-cube, the 5D permutohedron and three random simple 4-polytopes, predictions first). Section 7.3: #108.',
 '8': 'studies/2026-11-11-paradigm-ch8: simple_rule.py (the edge count of Theorem 8.1 against the measured degree of all 81 polytopes of the Atlas; FINAL ok), commit c5fb794d; the Atlas data of #108 (studies/2026-11-11-orbit-polytopes).',
 '9': 'studies/2026-11-09-b1-walls: cells61.py with the five cell logs data/cells2-D24/ (35,561,184 exact sign checks, each ending FINAL ok); rerun from a clean checkout on 11 November 2026 with identical logs, commit 2467d60f. Re-run: cd studies/2026-11-09-b1-walls/scripts &amp;&amp; D2=24 python -u cells61.py (about 45 minutes, five cells in parallel).',
 '10': 'studies/2026-11-11-orbit-polytopes (commit c5fb794d): mirror_law.py (228 cases, no disagreement), mirror_check.py (Corollary 10.2), vacuus_queens.py (Section 10.3, under all 14 400 symmetries), vacuus_middles.py (Section 10.4).',
 '11': 'studies/2026-11-10-permutohedron: vacuus_general.py (Theorem 11.1 by brute force over every ridge, n = 3 to 9, exact elimination), vacuus3d_12.py (the 15 cards of Figure 11.1, exact). studies/2026-11-11-paradigm-ch11: sweep_all_n.py (Proposition 11.2, n = 3 to 7; FINAL ok), commit 2ec0ae43.',
 '12': 'studies/2026-11-11-paradigm-ch12: golden_types.py (corner heights exact in ℤ[φ]; types by graph isomorphism; FINAL ok), commit 9ecafe40. The float slice test of 10 November 2026 is superseded.',
 '13': 'studies/2026-11-12-change-ringing, commit 52adaaef (Theorem 13.7 proved for every n on 13 November 2026, after an independent reader closed one gap; breadth-first search for n = 7, 8 rerun by the reader with the same result).',
 'Coda': 'No new checks.'}

# edits beyond numbering: (old, new); each must occur exactly once
EDITS = {
 '1': [('<b>Lemma 1.</b>', '<b>Lemma 1.1.</b>'), ('<b>Corollary 2.</b>', '<b>Corollary 1.2.</b>'),
       ('right, the orderings of 1, 2, 4, 5, the DICTO 1:2 Truncated Octahedron. From #105.</figcaption>',
        'right, the orderings of 1, 2, 4, 5, the DICTO 1:2 Truncated Octahedron, five of which make the heart of the 4D Vacuus (Chapter 6). From #105. (Permutohedra labelled by orderings, edges by exchanges, are a standard picture: T. Piesk, Wikimedia Commons, 2020; D. Eppstein.)</figcaption>')],
 '4': [('<p>The rhombic dodecahedron is a cube with a square pyramid', '<p>Chapters 1 to 3 found DICTO\'s solids among the permutohedra. This chapter follows one of his builds that leads out of the family. The rhombic dodecahedron is a cube with a square pyramid'),
       ('its hull matches Z to 10<sup>−9</sup>; the missing volume 1 = 6 · ⅙ is the six pyramids, each found empty under its square (analyse_build.py). ∎',
        'its hull matches Z to 10<sup>−9</sup>; the missing volume 1 = 6 · ⅙ is the six pyramids, each found empty under its square (analyse_build.py). This identification of the build is numerical (hull to 10<sup>−9</sup>, volumes to 10<sup>−6</sup>, the empty pyramids by sampling); the volume of Z is exact, and an exact reading of the build in rational coordinates is open. Theorem 4.3 is stated for Z and the cube pyramids and is exact. ∎')],
 '5': [('<p>A scutoid is a cell whose outline changes', '<p>Chapter 4 found where the permutohedron stops. This chapter returns to its edges, the exchanges of neighbours, and follows them into the cells of living tissue. A scutoid is a cell whose outline changes'),
       ('figures/football-slices.png', 'figures/ti-crystal-slices.png'),
       ('<figure><img src="figures/ti-crystal-slices.png"', '</div>\n<figure><img src="figures/ti-crystal-slices.png"'),
       ('Slices through the crystal of Proposition 5.5: the cells change neighbours twice per layer.</figcaption></figure></div>', 'Slices through the crystal of Proposition 5.5: the cells change neighbours twice per layer.</figcaption></figure>')],
 '6': [('(#105, Theorem 6.1)', '(#105, Theorem 1)'), ('(#105, Theorem 6.2)', '(#105, Theorem 2)'),
       ('(for an even number of values there is one more coincidence, Theorem 3)', '(for an even number of values there is one more coincidence, Theorem 11.1)'),
       ('These five are the heart of the Vacuus (Figure 3).', 'These five are the heart of the Vacuus (Figure 6.2; the orderings of 1, 2, 4, 5 on the solid are drawn in Figure 1.2).'),
       ('<figcaption>Close up: into the hollow centre', '<figcaption><b>Figure 6.1.</b> Close up: into the hollow centre'),
       ('<b>Figure 3.</b> One of the five central slices', '<b>Figure 6.2.</b> One of the five central slices')],
 '7': [('<b>Theorem 1.</b> In a generic sweep', '<b>Theorem 7.1</b> (#104, Theorem 1). In a generic sweep'),
       ('then Theorem 1. <i>Confirmation:</i>', 'then Theorem 7.1. <i>Confirmation:</i>'),
       ('the balance law, Theorem 7.4; and Sections 2 and 3.', 'the balance law, Theorem 7.4; and the walls of Chapter 9.')],
 '8': [('<h2>8.2 Open</h2>\n<p>A rosette at a corner with e edges is a bistellar move on more than four cells at once. Which of its exchanges balance, and whether a rosette tissue has a balance law of its own, is open; the Atlas',
        '<h2>8.2 Open</h2>\n<div class="box"><b>Open question 8.2.</b> Which exchanges of a rosette balance, and does a rosette tissue have a balance law of its own?</div>\n<p>A rosette at a corner with e edges is a bistellar move on more than four cells at once. The Atlas')],
 '9': [('We propose the name <i>4D scutoid</i> for such a 4-cell whose 3D slices change neighbours at a wall where cells stop touching and others start.',
        'Such a 4-cell, whose 3D slices change neighbours at a wall where cells stop touching and others start, is a <i>4D scutoid</i> (#104).')],
 '10': [('<p>Take a solid and look for its <i>Vacuus</i>', '<p>Chapter 6 found the Vacuus of the permutohedron and its heart. This chapter asks the same question of the Queens and of every polytope built from a reflection group. Take a solid and look for its <i>Vacuus</i>'),
        ('This paper answers it', 'This chapter answers it'), ('<b>Corollary 4.</b>', '<b>Corollary 10.4.</b>'),
        ('(#105, Figure 4)', '(Figure 11.1; #105, Figure 4)'), ('the H<sub>4</sub> row repeats Section 3 as a control', 'the H<sub>4</sub> row repeats Section 10.3 as a control')],
 '12': [('<p>The 4D permutohedra fill four-dimensional space', '<p>Chapter 11 followed the permutohedron into every dimension. This chapter cuts its four-dimensional filling. The 4D permutohedra fill four-dimensional space'),
        ('This is the permutohedron\'s own version of the passage from crystal to quasicrystal: a finite set of kinds, never repeating. Whether the 35 kinds can be cut down to finitely many <i>shapes</i> by the projection (window) method that gives Penrose-type tilings is open.</p>',
         'This is the permutohedron\'s own version of the passage from crystal to quasicrystal: a finite set of kinds, never repeating.</p>\n<div class="box"><b>Open question 12.2.</b> Can the 35 kinds be cut down to finitely many <i>shapes</i> by the projection (window) method that gives Penrose-type tilings?</div>')],
 '13': [('<p>In English change ringing a band rings', '<p>Part Three ends with the oldest walk through all the orders of a set. In English change ringing a band rings')],
 'Coda': [('This paper joins the two:', '#105 joined the two:')],
}
FIGMAP = {'6': {}, '9': {4: '9.1', 5: '9.2', 6: '9.3'}, '11': {4: '11.1'}}   # chapter figure numbers that are not 1, 2, 3, … in order
RENAME = {'football-slices.png': 'ti-crystal-slices.png'}
INDEX_TERMS = ['permutohedron', 'truncated triangle', 'elongated hexagon', 'truncated octahedron', 'DICTO 1:2 Truncated Octahedron', 'DICTO 2:1 Truncated Octahedron',
    'Kelvin', 'golden loop', 'golden bond', 'golden cut', 'Icosaxes', 'Unborn Axes', 'DICTONIC', 'web of bonds', 'power diagram', 'rhombic dodecahedron', 'Hemi RD',
    'chamfered cube', 'zonohedron', 'cube pyramid', 'scutoid', 'exchange of neighbours', 'Eulerian', 'h-vector', 'Vacuus', 'majorization', 'Mirror Law',
    'Queens', '600-cell', '120-cell', 'bitruncated 600-cell', 'truncated 600-cell', 'runcinated 5-cell', 'balance law', 'rosette', 'Swap Rule', 'chamber map',
    'Coxeter', 'Wythoff', 'Atlas', 'golden slice', 'quasicrystal', 'change ringing', 'extent', 'plain hunt', 'Plain Bob', 'Stedman', 'Grandsire', 'Kyushindo', 'Fibonacci', 'Stanley']

PAPER_CH = {}; INDEX = {}
def link_text(t, tag):
    def r(mo):
        n = int(mo.group(1))
        if n in PAPERS:
            PAPER_CH.setdefault(n, set()).add(tag); return f'<a href="https://doi.org/{PAPERS[n][1]}">#{n}</a>'
        if n > 3: print('UNKNOWN PAPER #', n, 'in', tag)
        return mo.group(0)
    t = re.sub(r'(?<![&\w])#(\d{1,3})\b', r, t)
    t = re.sub(r'\b(Chapters?) (\d{1,2})\b', lambda mo: f'{mo.group(1)} <a href="#ch{mo.group(2)}">{mo.group(2)}</a>' if 1 <= int(mo.group(2)) <= 13 else mo.group(0), t)
    return t
def link_html(h, tag):
    out = []; inA = False
    for p in re.split(r'(<[^>]+>)', h):
        if p.startswith('<'):
            if re.match(r'<a\b', p): inA = True
            if p.startswith('</a'): inA = False
            out.append(p)
        else: out.append(p if inA else link_text(p, tag))
    return ''.join(out)
def renum_figs(body, label):
    fmap = dict(FIGMAP.get(label, {}))
    k = [0]
    def cap(mo):
        n = int(mo.group(1)); k[0] += 1
        fmap.setdefault(n, f'{label}.{n}'); return f'<b>Figure {fmap[n]}.</b>'
    body = re.sub(r'<b>Figure (\d+)\.</b>', cap, body)
    def txt(seg):   # in-text references, not inside the Sources paragraphs, not after a paper number (#105, Figure 4)
        def r(mo):
            if '#' in seg[max(0, mo.start() - 14):mo.start()]: return mo.group(0)
            a = int(mo.group(2)); out = f'{mo.group(1)} {fmap.get(a, f"{label}.{a}")}'
            if mo.group(5): out += mo.group(4) + fmap.get(int(mo.group(5)), f'{label}.{mo.group(5)}')
            return out
        return re.sub(r'\b(Figures?) (\d+)\b(?!\.\d)((–|, | and )(\d+)\b)?', r, seg)
    parts = re.split(r'(<p class="src">.*?</p>|<b>Figure [\d.]+\.</b>|<[^>]+>)', body, flags=re.S)
    return ''.join(p if (p.startswith('<p class="src">') or p.startswith('<b>Figure') or p.startswith('<')) else txt(p) for p in parts)

chapters = []; toc = []; checks = []; styles = set()
for label, folder in CH:
    s = open(os.path.join(P, folder, 'paper.html'), encoding='utf8').read()
    for st in re.findall(r'<style>(.*?)</style>', s, re.S): styles.add(st.strip())
    body = s[s.index('<h1'):s.rindex('</body>')]
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1)
    title = html.unescape(re.sub('<[^>]+>', '', h1.split('<br>')[0])).strip().replace('Coda: ', '')
    sub = re.search(r'<span[^>]*>(.*?)</span>', h1, re.S).group(1)
    sub = re.sub(r'^The Permutohedron Paradigm(, Chapter \d+)?: ', '', sub)
    sub = sub[:1].upper() + sub[1:]
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body, count=1, flags=re.S)
    body = re.sub(r'<div class="meta">.*?</div>', '', body, count=1, flags=re.S)
    body = re.sub(r'<div class="status">.*?</div>', '', body, count=1, flags=re.S)
    for a, b in EDITS.get(label, []):
        if body.count(a) != 1: raise SystemExit(f'EDIT not found exactly once in {label}: {a[:70]!r} ({body.count(a)})')
        body = body.replace(a, b)
    if label == '6':   # the figure of the orderings is Figure 1.2 already; Chapter 6 points to it
        body, n = re.subn(r'<figure><img src="figures/fig-orderings\.png".*?</figure>\n?', '', body, flags=re.S)
        assert n == 1
    if label == '13':
        body = re.sub(r'\bTable (\d)\b', r'Table 13.\1', body)
        m = re.search(r'<h2>Data and methods</h2>\s*(<p class="src">.*?</p>)', body, re.S)
        CHECKS['13'] += ' ' + re.sub(r'^<p class="src">|</p>$', '', m.group(1)).replace('(Figures 1–4,', '(Figures 13.1–13.4,'); body = body.replace(m.group(0), '')
    body = re.sub(r'<p class="src"><b>Further reading\.</b>.*?</p>', '', body, flags=re.S)
    body = re.sub(r'<h2>Sources</h2>', '<h3 class="srch">Sources</h3>', body)
    body = re.sub(r'<h2>(\d+)\. ', lambda mo: f'<h2>{label}.{mo.group(1)} ', body)
    if label != 'Coda': body = renum_figs(body, label)
    body = body.replace('The Permutohedron Paradigm, Chapter', 'Chapter').replace('this paper', 'this chapter').replace('This paper', 'This chapter')
    def fig(mo):
        src = mo.group(1); name = RENAME.get(os.path.basename(src), os.path.basename(src)); dst = f'figures/ch{label}/{name}'
        path = os.path.join(P, folder, src)
        os.makedirs(os.path.join(HERE, os.path.dirname(dst)), exist_ok=True)
        fixed = os.path.join(HERE, 'figures-fixed', f'ch{label}', name)
        shutil.copy(fixed if os.path.exists(fixed) else path, os.path.join(HERE, dst)); return f'src="{dst}"'
    body = re.sub(r'src="(figures/[^"]+)"', fig, body)
    tag = label
    body = link_html(body, tag)
    plain = re.sub('<[^>]+>', ' ', body)
    for term in INDEX_TERMS:
        if re.search(r'\b' + re.escape(term) + r'(s|es)?\b', plain): INDEX.setdefault(term, []).append(tag)
    head = 'Coda. ' if label == 'Coda' else f'Chapter {label}. '
    fromline = link_html(FROM[label], tag)
    if label in PART:
        pt, pi = PART[label]; chapters.append(f'<div class="part"><h1 class="partt">{pt}</h1><p class="parti">{pi}</p></div>')
    chapters.append(f'<section class="ch"><h1 class="chapter" id="ch{label}">{head}{html.escape(title)}</h1>\n<p class="sub">{sub}</p>\n<p class="from">{fromline}</p>\n{body}</section>')
    toc.append((head + title, label))
    checks.append(f'<h3>{head}{html.escape(title)}</h3><p>{link_html(CHECKS[label], tag)}</p>')

front = open(os.path.join(HERE, 'front.html'), encoding='utf8').read()
epi = open(os.path.join(HERE, 'epilogue.html'), encoding='utf8').read()
refs = open(os.path.join(HERE, 'references.html'), encoding='utf8').read()
front = link_html(front, 'front'); epi = link_html(epi, 'Epilogue')
partrow = {k: v[0] for k, v in PART.items()}
tochtml = '<h2>Contents</h2><table class="toc">' + ''.join((f'<tr><td colspan="2"><b>{partrow[l]}</b></td></tr>' if l in partrow else '') + f'<tr><td><a href="#ch{l}">{html.escape(t)}</a></td><td></td></tr>' for t, l in toc) + \
    '<tr><td><a href="#epilogue">Epilogue. What has been shown</a></td><td></td></tr><tr><td><a href="#checks">Appendix. Checks and data by chapter</a></td><td></td></tr><tr><td><a href="#papers">Papers referred to</a></td><td></td></tr><tr><td><a href="#references">References</a></td><td></td></tr><tr><td><a href="#index">Index</a></td><td></td></tr><tr><td><a href="#about">About the author</a></td><td></td></tr></table>'
front = front.replace('__TOC__', tochtml)
def chs(v): return ', '.join(sorted(v, key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else 0, x)))
papers = '<section class="app" id="papers"><h1 class="chapter">Papers referred to</h1><p style="font-size:9pt">DICTO\'s papers named in this book, with their DICTO DOIs (concept DOIs: they resolve to the latest version) and where they are named.</p><table class="plist"><tr><th>#</th><th>title</th><th>DICTO DOI</th><th>named in</th></tr>' + \
    ''.join(f'<tr><td>#{n}</td><td>{html.escape(PAPERS[n][0])}</td><td><a href="https://doi.org/{PAPERS[n][1]}">{PAPERS[n][1]}</a></td><td>{chs(PAPER_CH[n]).replace("front", "opening")}</td></tr>' for n in sorted(PAPER_CH)) + '</table></section>'
idx = '<section class="app" id="index"><h1 class="chapter">Index</h1><p style="font-size:9pt">Chapters in which each term appears.</p><table class="idx">' + \
    ''.join(f'<tr><td>{t}</td><td>{", ".join(v)}</td></tr>' for t, v in sorted(INDEX.items(), key=lambda kv: kv[0].lower())) + '</table></section>'
css = '\n'.join(sorted(styles)) + '''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font:8.6pt/1.4 "DejaVu Sans",sans-serif;color:#6b5310;border-left:2px solid #b8962e;padding-left:2.5mm;margin:0 0 4mm}
section.ch > p.sub{font-size:10.5pt;margin:-1mm 0 2.5mm}
.part{break-before:page;height:230mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center} h1.partt{font-size:26pt;color:#b8962e} p.parti{max-width:120mm;font-size:11pt;color:#444}
table.toc{width:100%} table.toc td{border:none;border-bottom:1px dotted #ccc;padding:1.2mm 2mm} table.toc a,table.plist a{color:inherit;text-decoration:none}
.titlepage{min-height:240mm;display:flex;flex-direction:column;justify-content:flex-start} .titlepage h1{font-size:30pt}
section.app{break-before:page} section.app h3{font-size:10pt;margin:4mm 0 1mm} section.app p,section.app li{font-size:8.6pt}
h3.srch{font:600 10pt "DejaVu Sans",sans-serif;color:#6b5310;margin:5mm 0 1mm} p.src{font-size:8.6pt;color:#333}
table.claims td:first-child{width:6mm} table.claims td:last-child{width:46mm} table.plist td:first-child{width:9mm;white-space:nowrap} table.idx td:first-child{width:62mm}
figure img{max-width:100%} a{color:#6b5310;text-decoration:none}
h3{break-after:avoid} table.claims,table.plist,table.idx{break-inside:auto} table.claims tr,table.plist tr,table.idx tr{break-inside:avoid}
img[src$="hero-fill.png"]{width:58%;display:block;margin:0 auto} img[src$="perm4-close.png"]{width:85%} img[src$="cut-heart.png"]{width:85%}
body,h1,h2,h3,h4,.sub,.meta,figcaption,table,.status,ol.refs,p.from{font-family:"Nimbus Sans","Liberation Sans","DejaVu Sans",sans-serif}
body{font-size:10pt}'''
doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>The Permutohedron Paradigm</title>
<link rel="stylesheet" href="../paper.css"><style>{css}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt="">
{front}
{''.join(chapters)}
<section class="epi">{epi}</section>
<section class="app" id="checks"><h1 class="chapter">Appendix. Checks and data by chapter</h1><p>The study behind each chapter's checks, in the folder studies/ of the research branch of https://github.com/DICTOR-Master/kaleidohedra (branch research-fig3), with the commit at which it was last changed. FINAL ok marks a script whose log ends with every check passed.</p>{''.join(checks)}</section>
{papers}
{refs}
{idx}
{open(os.path.join(HERE, 'about.html'), encoding='utf8').read()}
</body></html>'''
open(os.path.join(HERE, 'paper.html'), 'w', encoding='utf8').write(doc)
print('chapters', len(toc), 'papers referred', len(PAPER_CH), 'index terms', len(INDEX), 'figures', sum(len(fs) for r, _, fs in os.walk(os.path.join(HERE, 'figures')) if 'figures-fixed' not in r), 'chars', len(doc))
