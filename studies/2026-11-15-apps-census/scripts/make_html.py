#!/usr/bin/env python3
"""Apps census -> paper/paper.html (DRAFT proposal for DICTO's read).

Usage: python3 scripts/make_html.py <path to dimension-wizard.js>
Reads data/census.json; reads the CURRENT order of the gold DICTO block from the wizard code
(K_WORLDS filtered by DICTO_WORK, then DICTO's lattices), checks that every DICTO world in the
code has exactly one census row and every census row is in the code, and writes the table
current position -> proposed position (ring order, book order, today's order kept inside a book).
Prints FINAL ok / FINAL FAIL.

After the change (DICTO 16 Nov 2026, "apps proposal start work") the wizard holds the gold block's order itself
(DICTO_SHELF, under FIVE_RINGS). Then the script checks the code against the census instead: every census row is on the
shelf exactly once (the DICTO Hex Prism's key there is 'hex'), under its census book, in the proposed order, the two
pyrochlore worlds are DICTO's work, and no other DICTO world is lost; paper/paper.html (the proposal as read) is kept.
"""
import html, json, re, sys
from pathlib import Path

here = Path(__file__).resolve().parent.parent
C = json.loads((here / 'data/census.json').read_text())
src = Path(sys.argv[1]).read_text()
fails = []

if 'const DICTO_SHELF = [' in src:
    # --- after the change: the code's shelf against the census ---
    rows = C['dicto_worlds']
    code_key = lambda k: 'hex' if k == 'dictohex' else k
    shelf_src = src[src.index('const DICTO_SHELF = ['):src.index('];', src.index('const DICTO_SHELF = ['))]
    shelf = [(b, k) for b, ks in re.findall(r"\['(\w+)', \[([^\]]*)\]\]", shelf_src) for k in re.findall(r"'(\w+)'", ks)]
    shelf_keys = [k for _, k in shelf]
    work = set(re.findall(r"'(\w+)'", re.search(r'const DICTO_WORK = new Set\(\[([^\]]*)\]', src).group(1)))
    kw = src[src.index('const K_WORLDS = ['):src.index('// A Kagome hull')]
    worlds = set(re.findall(r"\{ key: '(\w+)'", kw)) | {'stellaJewel', 'sunstar', 'shells', 'golden'}
    lat3 = src[src.index('export const LATTICES_3D = ['):src.index('const OBLIQUE_4D')]
    lat_keys = set(re.findall(r"\{ key: '(\w+)'", lat3))
    rings = re.findall(r"\{ id: '(\w+)', kanji: '(.)', colour: '(#\w+)', books: \[([^\]]*)\] \}", src)
    ring_books = [re.findall(r"'(\w+)'", b) for _, _, _, b in rings]
    if [k for k, _, _, _ in rings] != [r.lower() for r in C['rings']]: fails.append(f'rings in the code {[k for k, *_ in rings]}')
    if ring_books != [R['books'] for R in C['rings'].values()]: fails.append('ring books differ from the census')
    for (rid, kanji, col, _), (rg, R) in zip(rings, C['rings'].items()):
        if kanji != R['kanji']: fails.append(f'{rg}: kanji {kanji}')
    for k, n in ((k, shelf_keys.count(k)) for k in set(shelf_keys)):
        if n != 1: fails.append(f'{k} on the shelf {n} times')
    for r in rows:
        k = code_key(r['key'])
        if r['book']:
            if k not in shelf_keys: fails.append(f'census row {r["key"]} not on the shelf')
            elif dict((kk, b) for b, kk in shelf)[k] != r['book']: fails.append(f'{r["key"]}: book {dict((kk, b) for b, kk in shelf)[k]} in the code, {r["book"]} in the census')
        elif k in shelf_keys: fails.append(f'{r["key"]} has no book in the census but is on the shelf')
        elif k not in work: fails.append(f'{r["key"]} (no book yet) not DICTO work')
    for k in shelf_keys:
        if k not in [code_key(r['key']) for r in rows]: fails.append(f'shelf key {k} has no census row')
        if k != 'hex' and k not in work: fails.append(f'shelf key {k} not in DICTO_WORK')
        if k != 'hex' and k not in worlds | lat_keys: fails.append(f'shelf key {k} is no world or lattice')
    for k in ('breathing', 'bodhiPyro'):
        if k not in work: fails.append(f'{k} not moved into DICTO_WORK')
    # every DICTO world/lattice in the code is listed once: on the shelf, or after the rings (no book yet)
    code_dicto = sorted(k for k in work if k in worlds | lat_keys)
    for k in code_dicto:
        if k not in shelf_keys and not any(code_key(r['key']) == k and not r['book'] for r in rows): fails.append(f'DICTO world {k} neither on the shelf nor a no-book census row')
    listed = len(shelf_keys) + sum(1 for r in rows if not r['book'] and code_key(r['key']) in work)
    if listed != len(rows): fails.append(f'{listed} entries listed, {len(rows)} census rows')
    # the order DICTO approved: Table 1 of the proposal as read (paper/paper.html), row by row
    by_name = {html.escape(r['name'], quote=False): code_key(r['key']) for r in rows}
    t1 = (here / 'paper/paper.html').read_text().split('<h2>2. Table 1')[1].split('<h2>3.')[0]
    approved = [by_name[n] for n in re.findall(r'<tr><td>(.*?)</td>', t1) if n in by_name]
    no_book = [code_key(r['key']) for r in rows if not r['book']]
    if approved != shelf_keys + no_book: fails.append(f'order differs from the proposal as read: {approved}')
    if 'gperm' in work: fails.append('gperm counted as DICTO work')
    print(f'shelf {len(shelf_keys)} + no book yet {listed - len(shelf_keys)} = {listed} entries; census rows {len(rows)}')
    print('order: ' + ' '.join(shelf_keys))
    print('paper/paper.html kept (the proposal as read)')
    for f in fails: print('FAIL', f)
    print('FINAL ' + ('FAIL' if fails else 'ok'))
    sys.exit(1 if fails else 0)

# --- current order, from the code ---
kw = src[src.index('const K_WORLDS = ['):src.index('// A Kagome hull')]
order = []
for m in re.finditer(r"\{ key: '(\w+)'|\[\['(stellaJewel)', '[^']*', '\w+'\], \['(sunstar)'|\['(shells)', '(golden)'\]", kw):
    order += [g for g in m.groups() if g]
work = set(re.findall(r"'(\w+)'", re.search(r'const DICTO_WORK = new Set\(\[([^\]]*)\]', src).group(1)))
gold_worlds = [k for k in order if k in work]
current = {k: i + 1 for i, k in enumerate(gold_worlds)}
n = len(gold_worlds)
current['dictofcc'] = n + 1          # gold block, kind 'lattice', after the worlds
current['dictohex'] = n + 2
lat3 = src[src.index('export const LATTICES_3D = ['):src.index('const OBLIQUE_4D')]
lat_keys = re.findall(r"\{ key: '(\w+)'", lat3)
for k in ('breathing', 'bodhiPyro'):
    if k not in lat_keys: fails.append(f'{k} not in LATTICES_3D')
    if k in work: fails.append(f'{k} already in DICTO_WORK (census says it is not)')

rows = C['dicto_worlds']
keys = [r['key'] for r in rows]
for k in gold_worlds:
    if keys.count(k) != 1: fails.append(f'world {k}: {keys.count(k)} census rows')
for r in rows:
    if r['key'] not in current and r.get('from') != 'lattice': fails.append(f'census row {r["key"]} not in the gold block')
if 'gperm' in work: fails.append('gperm counted as DICTO work')

# --- proposed order: rings, books, then today's order inside a book (moved-in lattices last) ---
book_ix = {b: i for i, b in enumerate(C['books'])}
def sort_key(r):
    b = book_ix.get(r['book'], 99)
    return (b, current.get(r['key'], 1000))
prop_rows = sorted(rows, key=sort_key)
proposed = {r['key']: i + 1 for i, r in enumerate(prop_rows)}

def esc(s): return html.escape(s, quote=False)
def ring_of(book): return C['books'][book][0] if book else ''
def ring_cell(book):
    if not book: return '<i>to place</i>'
    rg = ring_of(book); R = C['rings'][rg]
    return f'<span style="color:{R["colour"]};font-weight:bold">{rg} {R["kanji"]}</span>'

moved = sum(1 for r in rows if current.get(r['key']) != proposed[r['key']])
same = len(rows) - moved
trs, last_book = [], None
for r in prop_rows:
    b = r['book']
    if b != last_book:
        rg = ring_of(b)
        col = C['rings'][rg]['colour'] if rg else '#777'
        label = f'Book {b} · {esc(C["books"][b][1])}' if b else 'Not yet in a book'
        trs.append(f'<tr class="bk"><td colspan="7" style="border-left:3pt solid {col}">{ring_cell(b)} · {label}</td></tr>')
        last_book = b
    cur = current.get(r['key'])
    cur_s = str(cur) if cur else ('lattice blocks' if r.get('from') == 'lattice' else '?')
    mv = ''
    book_s = (b + (' (reading)' if r.get('reading') else '')) if b else '—'
    trs.append(f'<tr><td>{esc(r["name"])}</td><td>{esc(r["shows"])}</td><td>{esc(r["papers"])}</td>'
               f'<td>{book_s}</td><td>{esc(r["also"]) or "—"}</td><td>{cur_s}</td><td{mv}>{proposed[r["key"]]}</td></tr>')

other = ''.join(f'<tr>{"".join(f"<td>{esc(c)}</td>" for c in row)}</tr>' for row in C['other_doors'])

ring_rows = []
for rg, R in C['rings'].items():
    bs = ', '.join(f'{b} ({esc(C["books"][b][1])})' for b in R['books'])
    cnt = sum(1 for r in rows if r['book'] in R['books'])
    ring_rows.append(f'<tr><td><span style="color:{R["colour"]};font-weight:bold">{rg} {R["kanji"]}</span> · {R["solid"]}</td><td>{bs}</td><td>{cnt}</td></tr>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Apps and The Five Orders of Space</title><link rel="stylesheet" href="../paper.css">
<style>table{{border-collapse:collapse;width:100%;font-size:7.9pt;margin:2mm 0;break-inside:auto}} td,th{{border:0.3pt solid #999;padding:0.7mm 1.2mm;vertical-align:top;text-align:left}} th{{background:#eee}} tr{{break-inside:avoid}} tr.bk{{break-after:avoid;page-break-after:avoid}} tr.bk td{{background:#f6f3ea;font-weight:bold}} td.mv{{background:#fff1c9;font-weight:bold}} table.w td:first-child{{width:19%}} table.w td:nth-child(2){{width:30%}} table.w td:nth-child(3){{width:14%}} table.w td:nth-child(4){{width:7%}} table.w td:nth-child(5){{width:16%}} table.w td:nth-child(6){{width:7%}} table.o td:first-child{{width:16%}} table.o td:nth-child(2){{width:38%}} p.s{{font-size:9pt}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>The Apps and The Five Orders of Space<br><span style="font-size:0.72em;font-weight:normal">A census of every world and door, mapped to the eleven books and five rings, with one proposed order</span></h1>
<div class="meta"><b>DICTO</b> · census of 15 November 2026 · PROPOSAL, for DICTO's read</div>
<div class="status">PROPOSAL, for DICTO's read; not for publication. Nothing in any app, the site or a repository was changed. DICTO, 15 November 2026: "maybe we need a census of all apps and whether they need to be reordered in line with The Five Orders of Space headings".
<br><b>How it was counted.</b> The positions are read from the wizard code (Kaleidohedra repository, master of 12 November 2026), not from screenshots; the script that builds this table also checks that every world of DICTO's gold block has exactly one row ({len(gold_worlds)} worlds + 2 lattices + 2 lattices moved in = {len(rows)} rows). The book of each world is the themed book that holds its paper as a chapter (chapter heads of the eleven books, the site's "In the book" labels); Quanta of Space is the home only where no themed book holds it. Two placements are readings, marked: Golden Rhombohedra (Book Nine) and Golamandalas (no book yet).
<br><b>The one pick</b> is Section 3. Regrouping gives every one of the {len(rows)} entries a new number; inside each book today's order is kept. Open points for DICTO are in Section 5.</div>

<h2>1. The census</h2>
<p>All of DICTO's apps are one joined app with three doors, Kaleidohedra, Rhombiverse and Polyhedraverse, each opening the same DICTO wizard; dictospheres.com links the three doors and the papers' "View in app" buttons open single worlds. Inside the wizard's 3D+ list the order is: the <b>gold DICTO block</b> (DICTO's pieces, then {len(gold_worlds)} worlds, then 2 lattices), the Kaleidohedra block, the Rhombiverse block, the Polyhedraverse block. The 1D+, 2D+, 4D, 5D and 6D tabs hold the rest. The gold block is where an order by the books matters; Table 2 covers everything else.</p>
<table><tr><th>ring</th><th>books</th><th>gold-block entries</th></tr>{''.join(ring_rows)}</table>

<h2>2. Table 1: the gold DICTO block, world by world</h2>
<p class="s">Grouped as proposed: ring, then book, then today's order kept inside each book (today's order is already newest first). "Now" is the position in the gold block today; "new" the proposed one. "Also in" names other books that hold the same paper; under the one-place rule the world is listed once, under its home book.</p>
<table class="w"><tr><th>world</th><th>what it shows</th><th>papers</th><th>home book</th><th>also in</th><th>now</th><th>new</th></tr>{''.join(trs)}</table>

<h2>3. The proposal (one pick)</h2>
<p><b>Inside the gold DICTO block, list the worlds under the five rings in book order</b>: Earth (Books One, Two), Water (Three to Five), Fire (Six, Seven), Wind (Eight), Void (Nine to Eleven). Each ring gets one thin heading in its element colour (green, blue, red, yellow, violet); each world's row carries its book number. DICTO's pieces stay first, above Earth, as now. A ring with no world is not shown. Above the rings, one row of five ring buttons jumps to a ring with one tap, so the newest work (now in Fire) is one tap from the top on a phone. The newest world carries a small "new" mark in its row instead of being moved to the top.</p>
<p>Two worlds that are DICTO's but sit today among the classical lattices of both the Kaleidohedra and the Rhombiverse blocks, <b>Golden Breathing Pyrochlore</b> and <b>Golden Bodhi Pyrochlore Networks</b>, move into the gold block under Book One. Everything else outside the gold block stays where it is (Table 2): the Kaleidohedra and Rhombiverse lattices are all Book Two's classical space-fillers in one block each; Polyhedraverse keeps the Platonic solids at the top of its green list; the dimension tabs stay. The DICTO User Guide's world table and the Almanac follow the new order.</p>

<h2>4. Table 2: the other doors and lists</h2>
<table class="o"><tr><th>where</th><th>what</th><th>book</th><th>now</th><th>proposed</th></tr>{other}</table>

<h2>5. For and against, and the rules it meets</h2>
<p><b>For.</b> The apps read as the shelf reads: one work, eleven books, five rings, and a world shows which book explains it (the paper and app pairing rule, made visible). Book Two's worlds (Jewel, Sunstar, the thirteens, the octet networks) sit together, as the book's Part II; the Platonic book's worlds come together (the EKP cell at 26 and Studies at 30 join Every Mix, Reuleaux and Aristotle's Pyramid at 11 to 13). Visitors who know one book find its worlds in one place.</p>
<p><b>Against, and how the pick meets each rule.</b></p>
<ul>
<li><b>New work at the top</b> (DICTO, 8 Oct). Ring order puts the newest worlds, the Bitruncated 600-cell and The 4D Permutohedron (Book Seven), at 28 and 29 instead of 2 and 3, Golamandalas (8 Nov) from 4 to the end, and DICTONIC, placed first by DICTO on 23 Oct, at 16. This is the main cost. The pick answers it with the ring buttons (one tap) and the "new" mark; DICTO may prefer instead to keep a top row of the newest one or two worlds, which would list them twice.</li>
<li><b>One place only</b> (DICTO, 10 Oct). Kept: each world is listed once, under its home book; where a world's papers sit in more than one book (column "also in"), the other books show only as book numbers in its row. The two pyrochlore worlds now appear twice (Kaleidohedra and Rhombiverse blocks); the move ends that.</li>
<li><b>Mobile first.</b> Five headings and one button row add about six rows to a long list; the jump row shortens the scroll to any ring.</li>
<li><b>Nothing unnecessary shown.</b> Empty rings are hidden; Book Eleven has no world yet, so the Void shows Books Nine and Ten only.</li>
<li><b>Polyhedraverse's order</b> (Platonic at the top of the green list, DICTO 9 Oct) is untouched.</li>
</ul>
<p><b>Open points for DICTO</b> (one line each): (1) Golamandalas: paper #103 is in no book yet; it is listed last until DICTO names its book. (2) Golden Rhombohedra (the Ammann–Kramer tiles, not DICTO's) is in the gold block today; Book Nine is a reading; it could instead move to the Kaleidohedra block. (3) Targets and Shells have no paper (pairing rule). (4) Generalized Permutohedra stays in the Kaleidohedra block, as not DICTO's mathematics, with a Fire chip for Book Seven.</p>
<p><b>Found on the way, outside the apps.</b> The site's book shelf puts Quanta of Space first and HexOct second (DICTO's rule of 31 Oct), while the series makes HexOct Book Six; the shelf order is DICTO's to decide and is not changed by this proposal. Several "In the book" labels on the site's paper cards name Quanta of Space for papers that are now also chapters of Space-Fillers (#17, #18, #41, #42), and #104, #105 and #107, chapters of the Paradigm, carry no book label yet.</p>
</body></html>
'''
(here / 'paper/paper.html').write_text(page)
for f in fails: print('FAIL', f)
print(f'gold worlds in code {len(gold_worlds)}; rows {len(rows)}; moved {moved}')
print('FINAL ' + ('FAIL' if fails else 'ok'))
sys.exit(1 if fails else 0)
