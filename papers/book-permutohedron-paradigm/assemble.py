# Assemble DICTO's book "The Permutohedron Paradigm" (Book Seven of THE FIVE ORDERS OF SPACE, the Fire ring) from its sources:
# front.html (cover, title page with the series line, status box, contents), chapters/NN-key.html (the Opening and fifteen
# chapters, in the order of the arc agreed with DICTO on 13 November 2026, PROPOSAL.html), epilogue.html, references.html,
# about.html, and the shared series page ../series-five-orders/series-page.html.
# Every number is assigned here, in reading order: {{S:key}} declares a statement (Theorem, Lemma, Proposition, Corollary,
# Remark share one counter per chapter), {{F:key}} a figure, {{T:key}} a table, <h2 data-k="key"> a numbered section;
# {{s:key}}, {{f:key}}, {{t:key}}, {{sec:key}}, {{ch:key}} refer to them anywhere in the book; {D:n} prints "#n (DICTO DOI: ...)".
# An unknown key stops the build. Keys oN.M are the labels of the 70-page draft (tools/migrate_v1.py), kept so that every
# cross-reference of the draft follows its statement to its new place. Output: paper.html, typeset by ../print.mjs (build.sh).
import re, os, html, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
PARTS = {'three': ('Part One. The swap builds solids', 'One swap of neighbouring values draws the hexagon; with four values the swaps build Kelvin\'s cell, the slider and the bonds, until the edges stop being swaps.'),
         'scut3': ('Part Two. Swaps inside cells: DICTO\'s scutoid tissues', 'The centre of the book. In a slice a swap is a scutoid; one dimension up the permutohedron of five values is the web of swaps; swept, it and every simple 4-polytope are tissues of swaps, counted and balanced; crowded swaps make rosettes, and the walls of close packing are 4D scutoids.'),
         'everyn': ('Part Three. Swaps in every dimension', 'The Vacuus and the sweep counted for every number of values, and the golden slice of the 4D filling.'),
         'family': ('Part Four. The summit', 'Slide the walls instead of the values: every solid of the climb lies in one family, every edge a swap.'),
         'bells': ('Part Five. The return', 'Ringers may only swap neighbours: the first hexagon heard.')}
CHMAP = {'o1': 'three', 'o2': 'slider', 'o3': 'bonds', 'o4': 'rd', 'o5': 'scut3', 'o6': 'web', 'o7': 'centre2', 'o8': 'rosettes', 'o9': 'walls',
         'o10': 'web', 'o11': 'everyn', 'o12': 'golden', 'o13': 'bells', 'o14': 'family'}

# DICTO's papers: the Collected Works table, plus the papers newer than it
cw = open(os.path.join(P, 'collected', 'paper.html'), encoding='utf8').read()
PAPERS = {int(m.group(1)): (html.unescape(re.sub('<[^>]+>', '', m.group(2))), m.group(3)) for m in re.finditer(r'<tr><td class="n">#(\d+)</td><td><b>(.*?)</b>.*?DICTO DOI: (10\.5281/zenodo\.\d+)', cw, re.S)}
PAPERS.update({104: ('Scutoid Tissues in Four Dimensions', '10.5281/zenodo.24111864'),
               105: ('DICTO 1:2 Truncated Octahedron: The 4D Vacuus of the Permutohedron', '10.5281/zenodo.24121177'),
               107: ('The Vacuus of the Queens', '10.5281/zenodo.24126800'),
               108: ('The Atlas of the Chains', '10.5281/zenodo.24126802')})

CHECKS = {
 'open': 'No new checks: the Opening retells the chapters. Figure 0.2: figs_book.py (studies/2026-11-13-paradigm-expansion), drawn from the six orders of 1, 2, 3.',
 'three': 'studies/2026-11-11-paradigm-ch1: key_lemma.py (exact, symbolic; the faces of the solids of Section 1.3 computed from their hulls; log kept; FINAL ok), fig_three.py (Figure 1.1). Commit d79c1d1f; checked independently on 11 November 2026, all findings fixed. Figure 1.3: studies/2026-11-13-paradigm-expansion (figs_book.py; side lengths computed from the values).',
 'kelvin': 'studies/2026-11-13-paradigm-expansion: figs_book.py (Figure 2.1: the 24 orders of 1, 2, 3, 4 and the 36 edges, each edge classed by the pair of values it swaps, 12 per pair; Euler 24 − 36 + 14 = 2 checked). The Dehn test and the TO-13 block: #100 and #26, with their own studies.',
 'slider': 'studies/2026-11-11-paradigm-ch2: symmetry.py (the full symmetry group of the corners for four symmetric and three non-symmetric spacings; exact; FINAL ok). Commit becdcba3. The identification of T(x): #105, Theorem 4 (dictonic_family.py in studies/2026-11-10-permutohedron). The silent station: #94 (studies/2026-11-04-harmonic-fingerprint); Figure 3.3 recomputes Q₄ along the slider from the closed form of #94 (figs_book.py), with the zero at a = 1/φ.',
 'bonds': 'studies/2026-11-11-paradigm-ch3: weight_map.py (exact, corner by corner, at d = −1/3, 0, 1/τ³, 1/3, 2/7, and every site within ±8 at six weights; FINAL ok), fig_slider.py (Figure 4.1). Commit d79c1d1f; checked independently on 11 November 2026, all findings fixed. Figure 4.2: figs_book.py (the two cells as half-space intersections at d = −1/3, 0, 1/3; their volumes add to the lattice cell).',
 'rd': 'studies/2026-11-11-hemi-rd-build: analyse_build.py (DICTO\'s world export; float geometry, the first reading of the build), fill_test.py (a numerical first test), exact_fill.py (Theorem 5.3 in rational arithmetic: 487 pairs separated by exact planes, densities 15 + 1 = 16; FINAL ok). Commit 52b55686. studies/2026-11-13-paradigm-exact: hemi_exact.py (Theorem 5.1 in rational arithmetic: the stored transforms read as exact rotations and tenths, 91 + 99 pairs separated by exact planes, hull = Z + c exactly, 14 + 6 · ⅙ = 15; FINAL ok; log data/hemi-exact.log). studies/2026-11-11-paradigm-ch4: fig_ch4.py (Figure 5.1; FINAL ok), commit 7f2c451e.',
 'scut3': 'Theorem 6.1: the draft Scutoids: Layers, Shells and Cycles (commit e932cb55) and its studies of 17 October and 6–10 November 2026 (faces flat to 10<sup>−13</sup>, volumes adding up). Theorems 6.2 and 6.3: studies/2026-11-13-paradigm-exact, scutoid_exact.py (exact in ℚ(√5): polars, folds, mirror planes, the flip shells at five-fold radii 1, 1.55 and 155/86, the scutoid shells at circumradii 1, 1.18, 1.42, 1.499, 71/45 with 2 × 2016 pairs of half-cells separated by exact planes and volumes adding exactly; FINAL ok; log data/scutoid-exact.log). Proposition 6.4: the study of 6–7 November 2026 (layer spacing solved from exact contact planes, corners to 400 digits; h written exactly in ℚ(2 cos 6°), FINAL ok).',
 'web': 'studies/2026-11-10-permutohedron (the study of #105; commit 3f41e5b3): the 65 slices and their shapes in exact rational arithmetic, every face confirmed exactly, Euler number 2 for every shape; web_of_bonds.py (the classical facts of Section 7.1 recounted exactly); the six corners of Theorem 7.2 confirmed against all 150 faces. The Mirror Law sections: studies/2026-11-11-orbit-polytopes (commit c5fb794d): mirror_law.py (228 cases, no disagreement), mirror_check.py (Corollary 7.4), vacuus_queens.py (under all 14 400 symmetries), vacuus_middles.py. Figures 7.1 and 7.2: figs_book.py (studies/2026-11-13-paradigm-expansion), the slices recomputed from their normals.',
 'centre1': 'Proposition 8.1: studies/2026-11-11-paradigm-ch5, swap_orderings.py (all 120 orderings for three directions; exact; FINAL ok), commit bc0c7781. Theorem 8.2: #104 and its studies. The warm-up and Figures 8.1 to 8.3: figs_book.py (studies/2026-11-13-paradigm-expansion): the events of each frame counted from the corners, 1, 11, 11, 1 for Kelvin\'s cell and 1, 26, 66, 26, 1 for the 4D permutohedron in the direction drawn. The self-reverse event: studies/2026-11-13-swaps-and-fixed-points, check K8 (exact, d = 2 to 7).',
 'centre2': 'The studies named in #104 (sweeps of the 120-cell, the truncated 120-cell and the bitruncated 600-cell in nine generic directions; the 5-cube, the 5D permutohedron and three random simple 4-polytopes, predictions first). The balance law in every chain: #108. Figure 9.4: figs_book.py, the h-vectors from the f-vectors by the Dehn–Sommerville relations.',
 'rosettes': 'studies/2026-11-11-paradigm-ch8: simple_rule.py (the edge count of Theorem 10.1 against the measured degree of all 81 polytopes of the Atlas; FINAL ok), commit c5fb794d; the Atlas data of #108 (studies/2026-11-11-orbit-polytopes). Section 10.2: studies/2026-11-13-rosette-balance, rosette_balance.py and invariants.py (exact: rationals, ℚ(√5) for H<sub>4</sub>; the ledgers of all 34 rosette rows, the moved 16-cell, 8000 + 60 moved sweeps; FINAL ok), commit d8331af2. Figures 10.1 to 10.3: figs_book.py; the edge counts of Figure 10.2 recomputed from Theorem 10.1.',
 'walls': 'studies/2026-11-09-b1-walls: cells61.py with the five cell logs data/cells2-D24/ (35,561,184 exact sign checks, each ending FINAL ok); rerun from a clean checkout on 11 November 2026 with identical logs, commit 2467d60f. Re-run: cd studies/2026-11-09-b1-walls/scripts &amp;&amp; D2=24 python -u cells61.py (about 45 minutes, five cells in parallel). The Boulder: the B1 logs of studies/2026-11-09-b1-walls (tower-c.log, tower-h.log) and studies/2026-11-13-paradigm-exact/data/b1-logs (the cube and dodecahedron chains, each exact run ending FINAL ok). Cones of heights: the proof in the text (no computation).',
 'everyn': 'studies/2026-11-10-permutohedron: vacuus_general.py (Theorem 12.1 by brute force over every ridge, n = 3 to 9, exact elimination), vacuus3d_12.py (the 15 cards of Figure 12.1, exact). studies/2026-11-11-paradigm-ch11: sweep_all_n.py (Proposition 12.2, n = 3 to 7; FINAL ok), commit 2ec0ae43. Figure 12.2: figs_book.py (ridges, slices and Eulerian numbers from their formulas, checked against the table).',
 'golden': 'studies/2026-11-11-paradigm-ch12: golden_types.py (corner heights exact in ℤ[φ]; types by graph isomorphism; FINAL ok), commit 9ecafe40. The float slice test of 10 November 2026 is superseded. Theorem 13.2 and the correction to Theorem 13.1 (i): studies/2026-11-13-golden-slice-window, slice_window.py (exact in ℚ(φ): Lawrence volumes per band, the window tiling on a patch of radius 50, the period plane; 40 checks, FINAL ok), commit 6ba577f5. Figures 13.1 to 13.3: figs_book.py (heights exact in ℤ[φ]; the plane sections of the slices in floating point, for the picture only).',
 'family': 'studies/2026-11-12-permutohedron-associahedron-line: gp_line.py (Theorem 14.1, the table, n = 4, 5, exact), gp_enum.c and gp_line_b.py (the equal-speed line, n = 4, 5, 6), conj1_witness.py (the point of the proof of (iii), n = 3 to 13) and reader_check.py (an independent recheck); commits ee6fd4e7, b7c4891a. studies/2026-11-12-abhy-associahedron: abhy.py (Proposition 14.2, 48 checks). studies/2026-11-12-permutohedron-equal-edges: coxeter.py, gp_setup.py, gp_enum.c, gp_analyse.py, gp_tables.py (Theorem 14.3, exact over ℚ(√2) and ℚ(√5)); render_a316.py and vacuus_a316.py (the 13-COA and its Vacuus; the Vacuus in floating point); PRIOR-ART.md (13 November 2026, commit 7f9b1dd5: the sources checked for the atoms). The road, the one-cone map, Fedorov\'s five rendered and the 13-COA re-rendered: figs_book.py (studies/2026-11-13-paradigm-expansion). The #89 reading: check89.py there (exact, sympy; FINAL ok).',
 'bells': 'studies/2026-11-12-change-ringing, commit 52adaaef (Theorem 15.7 proved for every n on 13 November 2026, after an independent reader closed one gap; breadth-first search for n = 7, 8 rerun by the reader with the same result). Figures 15.5 and 15.6: figs_book.py (studies/2026-11-13-paradigm-expansion), the rows generated from the place notation and checked to be 120 distinct rows, each step a change.'}

def D(n): return f'#{n} (DICTO DOI: {PAPERS[n][1]})'
def link_text(t, tag, PAPER_CH):
    def r(mo):
        n = int(mo.group(1))
        if n in PAPERS:
            PAPER_CH.setdefault(n, set()).add(tag); return f'<a href="https://doi.org/{PAPERS[n][1]}">#{n}</a>'
        if n > 3: print('UNKNOWN PAPER #', n, 'in', tag)
        return mo.group(0)
    t = re.sub(r'(?<![&\w])#(\d{1,3})\b', r, t)
    t = re.sub(r'\b(Chapters?) (\d{1,2})\b', lambda mo: f'{mo.group(1)} <a href="#ch{mo.group(2)}">{mo.group(2)}</a>' if 1 <= int(mo.group(2)) <= 15 else mo.group(0), t)
    return t
def link_html(h, tag, PAPER_CH):
    out = []; inA = False
    for p in re.split(r'(<[^>]+>)', h):
        if p.startswith('<'):
            if re.match(r'<a\b', p): inA = True
            if p.startswith('</a'): inA = False
            out.append(p)
        else: out.append(p if inA else link_text(p, tag, PAPER_CH))
    return ''.join(out)

# ---- read the chapters, assign numbers in reading order
files = sorted(glob.glob(os.path.join(HERE, 'chapters', '*.html')))
CH = []
for f in files:
    s = open(f, encoding='utf8').read()
    m = re.match(r'<!--META (\{.*?\})-->\n', s, re.S); meta = json.loads(m.group(1)); body = s[m.end():]
    if '<!--NEW' in body: raise SystemExit(f'unwritten NEW marker left in {os.path.basename(f)}')
    CH.append((meta, body))
NUM = {'ch': {}, 's': {}, 'f': {}, 't': {}, 'sec': {}}
for i, (meta, body) in enumerate(CH):
    NUM['ch'][meta['key']] = '0' if meta['key'] == 'open' else str(i)
for k, v in CHMAP.items(): NUM['ch'][k] = NUM['ch'][v]
assert len(CH) == 16 and CH[0][0]['key'] == 'open', [m['key'] for m, b in CH]
for meta, body in CH:
    c = NUM['ch'][meta['key']]; cnt = {'S': 0, 'F': 0, 'T': 0, 'sec': 0}
    for mo in re.finditer(r'\{\{([SFT]):([^}]+)\}\}|<h2 data-k="([^"]+)">', body):
        if mo.group(3):
            cnt['sec'] += 1; key = mo.group(3); kind = 'sec'; val = f'{c}.{cnt["sec"]}'
        else:
            kind = mo.group(1).lower(); key = mo.group(2); cnt[mo.group(1)] += 1; val = f'{c}.{cnt[mo.group(1)]}'
        if key in NUM[kind]: raise SystemExit(f'duplicate {kind} key {key}')
        NUM[kind][key] = val
def resolve(h, where):
    def r(mo):
        kind, key = mo.group(1), mo.group(2)
        k = kind.lower() if kind in 'SFT' else kind
        if key not in NUM[k]: raise SystemExit(f'unknown {kind} key {key} in {where}')
        return NUM[k][key]
    h = re.sub(r'\{\{(S|F|T|s|f|t|sec|ch):([^}]+)\}\}', r, h)
    h = re.sub(r'\{D:(\d+)\}', lambda mo: D(int(mo.group(1))), h)
    return h
def numsec(body, c):
    k = [0]
    def r(mo):
        k[0] += 1; return f'<h2 id="sec{c}-{k[0]}">{c}.{k[0]} '
    return re.sub(r'<h2 data-k="[^"]+">', r, body)

INDEX_TERMS = ['permutohedron', 'swap', 'truncated triangle', 'elongated hexagon', 'truncated octahedron', 'DICTO 1:2 Truncated Octahedron', 'DICTO 2:1 Truncated Octahedron',
    'Kelvin', 'Weaire', 'golden loop', 'golden bond', 'golden cut', 'Icosaxes', 'Unborn Axes', 'DICTONIC', 'silent station', 'harmonic', 'Dehn invariant', 'web of bonds', 'power diagram', 'rhombic dodecahedron', 'Hemi RD',
    'chamfered cube', 'zonohedron', 'cube pyramid', 'scutoid', 'T1', 'Eulerian', 'h-vector', 'g-theorem', 'Vacuus', 'majorization', 'Mirror Law', 'braid relation',
    'Queens', '600-cell', '120-cell', 'bitruncated 600-cell', 'truncated 600-cell', 'runcinated 5-cell', 'balance law', 'rosette', 'Swap Rule', 'chamber map', 'secondary fan', 'switch theorem',
    'Coxeter', 'Wythoff', 'Atlas', 'generalized permutohedra', 'deformation cone', 'Minkowski sum', 'associahedron', 'canonical form', 'augmented cuboctahedron', '13-COA', 'parallelohedra', 'Fedorov', 'graphical zonotope', 'Stretching Theorem', 'Boulder', 'golden slice', 'quasicrystal', 'change ringing', 'extent', 'plain hunt', 'Plain Bob', 'Stedman', 'Grandsire', 'Kyushindo', 'Fibonacci', 'Stanley', 'self-reverse']
PAPER_CH = {}; INDEX = {}; chapters = []; toc = []; checks = []
for meta, body in CH:
    key = meta['key']; c = NUM['ch'][key]; tag = 'Opening' if key == 'open' else c
    body = resolve(numsec(body, c), key)
    body = link_html(body, tag, PAPER_CH)
    for src in re.findall(r'src="([^"]+)"', body):
        if not os.path.exists(os.path.join(HERE, src)): raise SystemExit(f'missing figure {src} in {key}')
    plain = re.sub('<[^>]+>', ' ', body)
    for term in INDEX_TERMS:
        if re.search(r'\b' + re.escape(term) + r'(s|es)?\b', plain): INDEX.setdefault(term, []).append(tag)
    head = 'Opening. ' if key == 'open' else f'Chapter {c}. '
    if key in PARTS:
        pt, pi = PARTS[key]; chapters.append(f'<div class="part"><h1 class="partt">{pt}</h1><p class="parti">{pi}</p></div>')
    fromline = f'<p class="from">{link_html(resolve(meta["from"], key), tag, PAPER_CH)}</p>' if meta.get('from') else ''
    chapters.append(f'<section class="ch"><h1 class="chapter" id="ch{"0" if key == "open" else c}">{head}{html.escape(meta["title"])}</h1>\n<p class="sub">{resolve(meta["sub"], key)}</p>\n{fromline}\n{body}</section>')
    toc.append((head + meta['title'], '0' if key == 'open' else c, PARTS.get(key, ('',))[0]))
    checks.append(f'<h3>{head}{html.escape(meta["title"])}</h3><p>{link_html(resolve(CHECKS[key], key), tag, PAPER_CH)}</p>')

front = resolve(open(os.path.join(HERE, 'front.html'), encoding='utf8').read(), 'front')
epi = resolve(open(os.path.join(HERE, 'epilogue.html'), encoding='utf8').read(), 'epilogue')
refs = resolve(open(os.path.join(HERE, 'references.html'), encoding='utf8').read(), 'references')
front = link_html(front, 'front', PAPER_CH); epi = link_html(epi, 'Epilogue', PAPER_CH); refs = link_html(refs, 'refs', {})
tochtml = '<h2>Contents</h2><table class="toc">' + ''.join((f'<tr><td colspan="2"><b>{p}</b></td></tr>' if p else '') + f'<tr><td><a href="#ch{l}">{html.escape(t)}</a></td><td></td></tr>' for t, l, p in toc) + \
    '<tr><td><a href="#epilogue">Epilogue. What has been shown</a></td><td></td></tr><tr><td><a href="#checks">Appendix. Checks and data by chapter</a></td><td></td></tr><tr><td><a href="#papers">Papers referred to</a></td><td></td></tr><tr><td><a href="#references">References</a></td><td></td></tr><tr><td><a href="#index">Index</a></td><td></td></tr><tr><td><a href="#about">About the author</a></td><td></td></tr><tr><td><a href="#five-orders">The Five Orders of Space</a></td><td></td></tr></table>'
front = front.replace('__TOC__', tochtml)
def chs(v):
    v = [str(x) for x in v]
    return ', '.join(sorted(set(v), key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else 0, x)))
papers = '<section class="app" id="papers"><h1 class="chapter">Papers referred to</h1><p style="font-size:9pt">DICTO\'s papers named in this book, with their DICTO DOIs (concept DOIs: they resolve to the latest version) and where they are named.</p><table class="plist"><tr><th>#</th><th>title</th><th>DICTO DOI</th><th>named in</th></tr>' + \
    ''.join(f'<tr><td>#{n}</td><td>{html.escape(PAPERS[n][0])}</td><td><a href="https://doi.org/{PAPERS[n][1]}">{PAPERS[n][1]}</a></td><td>{chs(PAPER_CH[n]).replace("front", "title page")}</td></tr>' for n in sorted(PAPER_CH)) + '</table></section>'
idx = '<section class="app" id="index"><h1 class="chapter">Index</h1><p style="font-size:9pt">Chapters in which each term appears.</p><table class="idx">' + \
    ''.join(f'<tr><td>{t}</td><td>{chs(v)}</td></tr>' for t, v in sorted(INDEX.items(), key=lambda kv: kv[0].lower())) + '</table></section>'
SERIES = os.path.join(P, 'series-five-orders', 'series-page.html')
if os.path.exists(SERIES):
    series = open(SERIES, encoding='utf8').read().replace('<section class="five-orders"', '<section class="five-orders" id="five-orders"', 1)
else:
    print('HOOK: the shared series page ../series-five-orders/series-page.html is missing; the book is built without it')
    series = '<section class="app" id="five-orders"><h1 class="chapter">The Five Orders of Space</h1><p>[the shared series page goes here at release]</p></section>'
css = open(os.path.join(HERE, 'book.css'), encoding='utf8').read() + '''
h1.chapter{break-before:page;font-size:19pt;margin-top:0} p.from{font:8.6pt/1.4 "DejaVu Sans",sans-serif;color:#6b5310;border-left:2px solid #b8962e;padding-left:2.5mm;margin:0 0 4mm}
section.ch > p.sub{font-size:10.5pt;margin:-1mm 0 2.5mm}
.part{break-before:page;height:230mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center} h1.partt{font-size:26pt;color:#b8962e} p.parti{max-width:120mm;font-size:11pt;color:#444}
table.toc{width:100%} table.toc td{border:none;border-bottom:1px dotted #ccc;padding:1.0mm 2mm} table.toc a,table.plist a{color:inherit;text-decoration:none}
.titlepage{min-height:240mm;display:flex;flex-direction:column;justify-content:flex-start} .titlepage h1{font-size:30pt}
p.series{font:600 11pt "Nimbus Sans","Liberation Sans","DejaVu Sans",sans-serif;color:#cd3e28;letter-spacing:.02em;margin:-2mm 0 4mm}
section.app{break-before:page} section.app h3{font-size:10pt;margin:4mm 0 1mm} section.app p,section.app li{font-size:8.6pt}
h3.srch{font:600 10pt "DejaVu Sans",sans-serif;color:#6b5310;margin:5mm 0 1mm} p.src{font-size:8.6pt;color:#333}
table.claims td:first-child{width:6mm} table.claims td:last-child{width:46mm} table.plist td:first-child{width:9mm;white-space:nowrap} table.idx td:first-child{width:62mm}
figure img{max-width:100%} a{color:#6b5310;text-decoration:none}
h3{break-after:avoid} table.claims,table.plist,table.idx{break-inside:auto} table.claims tr,table.plist tr,table.idx tr{break-inside:avoid}
p.opener{font-size:10.5pt;line-height:1.5;border-left:3px solid #cd3e28;padding-left:3mm;margin:0 0 4mm}
div.worked{border:1px solid #d9c9a0;background:#fbf8ef;padding:2mm 3mm;margin:3mm 0;font-size:9.6pt} div.worked b.wt{color:#6b5310}
p.handoff{font-style:italic;color:#333;border-top:1px solid #e3d7b5;padding-top:2mm;margin-top:5mm}
p.pointer{font-size:9pt;color:#444}
.two{display:flex;gap:4mm} .two figure{flex:1}
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
{series}
</body></html>'''
left = re.findall(r'\{\{[^}]*\}\}|\{D:\d+\}', doc)
if left: raise SystemExit(f'unresolved: {left[:5]}')
open(os.path.join(HERE, 'paper.html'), 'w', encoding='utf8').write(doc)
nfig = len(re.findall(r'<figure', doc))
print('chapters', len(toc), 'figures', nfig, 'papers referred', len(PAPER_CH), 'index terms', len(INDEX), 'chars', len(doc))
