# Apply the Zenodo metadata audit of 20 November 2026 (DICTO 2026-11-21: "read ok — act on all"; the audit is
# ZENODO-METADATA-AUDIT.md in his reading folder). METADATA ONLY: the latest version of each flagged record is edited in place
# (POST draft -> PUT draft -> publish, the zen_applink.py / zen_fixdesc.py pattern); no new versions, files untouched.
# Kinds acted on: (f) add isPartOf the Collected Works concept; (b) put the missing "Version N …" line, taken from the paper's own
# text or the record's own version note, as the first paragraph; (c) names; (d) stale counts/claims; (e) one AI credit line only.
# The Collected Works record is skipped (v52 comes separately); records the audit lists as clean or pending are not touched.
# Usage: zen_auditfix.py --dry | --apply  [--only RID,RID…] [--start K] [--budget SECONDS]
#   --dry prints every proposed change (before -> after); --apply publishes them. Each run stops starting new records after
#   --budget seconds (default 250) and prints the --start value to resume with. Ends with a FINAL line.
import json, urllib.request, socket, os, sys, re, html, time
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
H = {'Authorization': f'Bearer {T}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.inveniordm.v1+json'}
def req(url, method='GET', body=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), method=method, headers=H), timeout=120))
P = os.path.dirname(os.path.abspath(__file__))
BAN = re.compile(re.search(r'const BAN = /(.*?)/gi;', open(f'{P}/print.mjs').read()).group(1), re.I)
CW = '10.5281/zenodo.23345699'
ISPARTOF = {'identifier': CW, 'scheme': 'doi', 'relation_type': {'id': 'ispartof', 'title': {'de': 'Ist Teil von', 'en': 'Is part of'}}}

# ---- the audit's flagged records (latest version ids; checked against /versions/latest at run time) ----
# value: (paper, kinds, version-line source). Source: 'notes' = the record's own version note; a folder = that paper's paper.html.
REC = {
 '23483430': ('#8', 'bf', 'notes'), '23483429': ('#13', 'bf', 'notes'), '23483420': ('#14', 'bf', 'notes'),
 '23483454': ('#17', 'bf', 'notes'), '23483437': ('#18', 'bf', 'notes'), '23483495': ('#19', 'b', 'notes'),
 '23483498': ('#20', 'bcf', 'notes'), '23483408': ('#22', 'bcf', 'notes'), '23483476': ('#23', 'bf', 'notes'),
 '23483403': ('#24', 'bf', 'notes'), '23483477': ('#25', 'bf', 'notes'), '23483484': ('#26', 'bf', 'notes'),
 '23483490': ('#27', 'bf', 'notes'), '23483485': ('#28', 'bdf', 'notes'), '23484406': ('#29', 'bf', 'notes'),
 '23484410': ('#30', 'be', 'notes'), '23968833': ('#31', 'bde', 'notes'), '23486753': ('#31a', 'bf', 'notes'),
 '23484388': ('#32', 'be', 'notes'), '23484383': ('#33', 'be', 'notes'), '23484401': ('#34', 'bef', 'notes'),
 '23483440': ('#34a', 'bf', 'notes'), '23483469': ('#35', 'bef', 'notes'), '23483446': ('#35a', 'bf', 'notes'),
 '23483451': ('#35b', 'bf', 'notes'), '23969651': ('#36', 'bf', 'notes'), '24091154': ('#37', 'bef', '2026-10-18-bull-horns'),
 '23969696': ('#37a', 'bf', 'notes'), '23488955': ('#38', 'bf', 'notes'), '23483398': ('#38a', 'bf', 'notes'),
 '24037758': ('#39', 'f', None), '23490115': ('#40', 'f', None), '23496354': ('#41', 'f', None), '23497703': ('#42', 'f', None),
 '24153218': ('#43', 'f', None), '23930107': ('#44', 'bf', 'notes'), '23550371': ('#45', 'bf', 'notes'),
 '23567586': ('#49', 'b', 'notes'), '24091187': ('#54', 'b', '2026-10-25-gnomon-polar'),
 '24091619': ('#57', 'b', '2026-10-26-rule-of-halves'), '23665945': ('#58', 'f', None), '24091680': ('#59', 'bf', 'icosaxes-hexa'),
 '23678751': ('#60', 'f', None), '23683033': ('#61', 'f', None), '23687224': ('#62', 'f', None), '23717227': ('#63', 'f', None),
 '23709754': ('#64', 'f', None), '23717292': ('#65', 'f', None), '23717731': ('#66', 'f', None), '23718814': ('#67', 'f', None),
 '23719276': ('#68', 'f', None), '23723070': ('#69', 'f', None), '23723566': ('#70', 'f', None), '23726065': ('#71', 'f', None),
 '23728288': ('#72', 'f', None), '23728922': ('#73', 'f', None), '24038200': ('#74', 'bf', 'magnets'),
 '24091361': ('#75', 'bf', 'two-tiles'), '24384410': ('#76', 'f', None), '24091292': ('#77', 'bf', 'face-to-face'),
 '23897414': ('#78', 'f', None), '24091337': ('#79', 'bf', 'star-cores-a'), '24091353': ('#80', 'bf', 'star-cores-c'),
 '24091347': ('#81', 'bf', 'star-cores-b'), '24247023': ('#83', 'f', None), '24091144': ('#84', 'bf', 'window-law'),
 '23866680': ('#85', 'bf', None), '24091198': ('#86', 'bf', '2026-11-02-hexoct-family'), '24123971': ('#87', 'f', None),
 '24123978': ('#88', 'ef', None), '24091298': ('#89', 'bf', 'golden-cuts-beyond-plato'),
 '24091327': ('#90', 'bf', 'six-dimensions-golden-cubes'), '24091287': ('#91', 'bf', 'dual-pairs-dimensions'),
 '24091376': ('#92', 'bf', '2026-11-04-pyramid-tilings'), '24123981': ('#93', 'f', None),
 '24091207': ('#94', 'bf', '2026-11-04-harmonic-fingerprint'), '24029393': ('#95', 'bc', 'notes'),
 '23969511': ('#96', 'b', 'notes'), '24015400': ('#99', 'be', 'notes'), '24091212': ('#100', 'b', '2026-11-07-dehn-tilers'),
 '24241321': ('#102', 'e', None), '24383315': ('#112', 'c', None),
 '24383095': ('Alicia in Wonderland (book)', 'f', None), '24091643': ('DICTONIC Bonds (book)', 'bf', 'book-bonds'),
 '24395996': ('DICTOnary v1.5 (book)', 'df', None), '24091462': ('Golden Cycle (book)', 'bf', 'book-golden-cycle'),
 '24091415': ('HexOct (book)', 'bf', 'book-laws-of-stacking'), '24386728': ('Quanta of Space (book)', 'df', None),
 '24091436': ('Star Cores (book)', 'bf', 'book-star-cores'), '24238023': ('Concordance', 'f', None),
 '24047765': ('DICTO Solids (dataset)', 'f', None),
}
SKIPPED = {  # flagged by the audit but not acted on here (the record's other kinds still go ahead)
 '24069796': 'Collected Works: all kinds skipped; CW v52 comes separately',
 '23866680:b': '#85 Version 3: neither the paper nor the record says what Version 3 changed; no version line invented',
 '24385357': 'DICTOnary v1.4 is no longer the latest; its fixes go to v1.5 (24395996)',
}

# ---- (c), (d), (e): exact text edits (old -> new, each old must occur exactly once) ----
QUANTA_NEW_BODY = (
 '<p>Is space smooth all the way down, like water? Or is it built from pieces, the way a wall is built from stones? People have asked '
 'this for two and a half thousand years. This book takes the question literally. It looks for exact sets of solid pieces that fit '
 'together with no gaps, into shells, into cycles and into the whole of space.</p>'
 '<p>This is Book One, Volume I, of <i>The Five Orders of Space</i>: one work by DICTO in eleven books and twelve volumes, in five orders. '
 'The road starts here, with the oldest question about space, what are its smallest exact pieces and how do they join, and with seven '
 'postulates. In the cube order the pieces fill space: very few alone, all five Platonic solids together with a small kit of helpers, '
 'some held by their shape alone. In the icosahedron order they join in bonds that hand over along a line, and close round a core in '
 'golden shells and cycles, star and core turning into each other. In the tetrahedron order every close packing comes down to a finite '
 'catalogue of pieces that change only by swapping, every count a straight line in one number, and the smallest swap, two neighbours '
 'changing places, becomes the unit of a whole paradigm. In the octahedron order the five solids of the old schools are taken apart: '
 'nested in one cell, cut into Aristotle\'s pyramids, rounded, and each cut golden in exactly two ways. In the dodecahedron order the '
 'same pieces reach beyond three dimensions, as slices and shadows of the solids of four dimensions, and come back. The book ends on the '
 'road through the cycle to its last book, <i>A Brief Geometry of Space</i>.</p>'
 '<p>Postulate 1. Space is built from pieces. Postulate 2. Every piece must be exact: a shape you could make and hold, checked to the '
 'last corner. Postulate 3. A small kit is enough: a handful of shapes builds shells and spaces without end. Postulate 4. The golden '
 'ratio decides when shells close. Postulate 5. Pieces join in bonds, and the web of bonds is as real as the pieces. Postulate 6. '
 'Repeating and never-repeating order meet in the pieces. Postulate 7. Everything is open: the apps, the data and the papers, free to '
 'use and to build on.</p>'
 '<p>Volume II: <i>The DICTOnary of Atoms: Quanta of Space II</i>, the catalogue of all the atoms, the data work by work and the known '
 'and rediscovered shapes.</p>')
QUANTA_OLD = (
 '<p>DICTO\'s manifesto and the overview of his geometric works: is space smooth, or built from exact pieces that fit with no gaps? '
 'From the atoms of Democritus and Plato\'s kit of solids to the quanta of modern physics, the book follows that question through 73 works, '
 '71 papers in six chapters: Atoms, Bonds, Shells, Cycles, Stacking and Four dimensions, with the Kaleidohedra findings and the data set.</p>'
 '<p>Its centre is the Rule of Halves: however equal balls are stacked in close-packed layers, the space between them is shared out into '
 'pieces of only finitely many kinds, every one borrowed whole or in half from the two pure stackings, a finite catalogue of quanta for '
 'every close packing, which closes into two tiles, HexOct. The catalogue of all the atoms, DICTO\'s 134 new shapes and his 37 new '
 'clusters, structures and networks, with the known and rediscovered shapes the work builds with and the data work by work, is Volume II, '
 'The DICTOnary of Atoms: Quanta of Space II.</p>'
 '<p>The works from #52 on are told in short; the books HexOct: The Laws of Stacking, The Golden Cycle and Alicia in Wonderland: The Red '
 '&amp; White Queens hold them in full. For my father, Alan Baker.')
QUANTA_BLAKE = '(William Blake, <i>Auguries of Innocence</i>)</p>'
EDITS = {
 '23483498': [  # #20 (c)
  ('Its base is a <b>flat-ended triangle</b>:', 'Its base is a <b>truncated triangle</b>:'),
  ('Put an apex over a flat-ended triangle with sides', 'Put an apex over a truncated triangle with sides'),
  ('the kagome hexagons are flat-ended triangles,', 'the kagome hexagons are truncated triangles,')],
 '23483408': [  # #22 (c)
  ('on a flat-ended (truncated) triangle with sides', 'on a truncated triangle with sides'),
  ('on a flat-ended triangle (sides', 'on a truncated triangle (sides')],
 '23483485': [('its 60 coplanar triangle pairs merged into 30 rhombi', 'its 30 coplanar triangle pairs merged into 30 rhombi')],  # #28 (d)
 '23484410': [('checking with Claude (Anthropic); independent pre-publication checks by Claude Fable.', 'checking with Claude (Anthropic).')],  # #30 (e)
 '23968833': [  # #31 (d), (e): the paper's current wording
  ('The polar of the Hecatodihedron is new, and DICTO named it',
   'The polar of the Hecatodihedron is not a classical solid and was not found named in the sources checked (Version 2: it is the '
   'canonical pentakis dodecahedron cut at the hexagon planes), and DICTO named it'),
  ('checking with Claude (Anthropic); an independent pre-publication check by Claude Fable.', 'checking with Claude (Anthropic).')],
 '23484388': [('checking with Claude (Anthropic); an independent pre-publication check by Claude Fable.', 'checking with Claude (Anthropic).')],  # #32
 '23484383': [('checking with Claude (Anthropic); two independent pre-publication reviews by Claude Fable.', 'checking with Claude (Anthropic).')],  # #33
 '23484401': [('checking with Claude (Anthropic); scope and publishing order advised by Claude Fable;', 'checking with Claude (Anthropic);')],  # #34
 '23483469': [('checking with Claude (Anthropic); scope and publishing order advised by Claude Fable;', 'checking with Claude (Anthropic);')],  # #35
 '24091154': [  # #37 (e): one AI line, the same credits
  ('computation, exact arithmetic and renders were done with Claude (Anthropic) as a research assistant; the independent exact proofs, '
   'the vertex glue W, the identification of the tetartoid and the keyed-glue design are by Claude Fable.',
   'computation, exact arithmetic and renders, the independent exact proofs, the vertex glue W, the identification of the tetartoid '
   'and the keyed-glue design were done with Claude (Anthropic) as a research assistant.')],
 '24123978': [  # #88 (e)
  ('Computation, proofs, exact checks and drafting with Claude (Anthropic); an independent review by Fable (Anthropic) checked every theorem and number.',
   'Computation, proofs, exact checks, an independent review of every theorem and number, and drafting with Claude (Anthropic).')],
 '24029393': [('the midpoints of the edges of a football,', 'the midpoints of the edges of a truncated icosahedron,')],  # #95 (c), the paper's wording
 '24015400': [  # #99 (e): folded into the one credit line
  ('Computation, proofs and drafting with Claude (Anthropic); an independent review (Claude) checked the prior art and supplied the proofs of Theorem 3.',
   'Computation, proofs (among them those of Theorem 3), an independent review of the prior art and drafting with Claude (Anthropic).')],
 '24241321': [('surfaced, unexpected by DICTO or Claude, in the loop counts', 'surfaced, unexpected, in the loop counts')],  # #102 (e)
 '24383315': [('there are 1083 more (among them', 'there are 1083 more, the Seraphim (among them')],  # #112 (c): DICTO's name, 20 Nov
 '24395996': [  # DICTOnary v1.5 (d): the paper's own wording for the two volumes
  ('Volume I, Quanta of Space: A Manifesto, tells the works in six chapters, Atoms, Bonds, Shells, Cycles, Stacking and Four dimensions; '
   'this volume holds their shapes and their numbers.',
   'Volume I, Quanta of Space: A Manifesto, gives the Postulates; this volume is the Definitions of the whole work, The Five Orders of '
   'Space: its atoms and their data, each with its home in the series.')],
}

def text(s): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()

def version_line(meta, src, N):
    """The 'Version N …' line, from the record's own version note or the paper's own text; None if neither states it."""
    if src == 'notes':
        for a in meta.get('additional_descriptions', []):
            d = re.sub(r'^\s*<p>|</p>\s*$', '', a.get('description', '').strip())
            m = re.search(rf'Version {re.escape(N)}\b', d)
            if not m: continue
            d = d[m.start():]
            cut = re.search(r'\s(Version (?!' + re.escape(N) + r'\b)\d+[ (:.]|Companion:)', d)   # stop at an older version's note
            d = d[:cut.start()].strip() if cut else d.strip()
            # the 20 Oct notes quote the retired wording; the line keeps the note without the quotation (banned phrase)
            return d.replace(' ("DICTO proposed …" in place of "DICTO asked …")', '')
        return None
    s = open(f'{P}/{src}/paper.html').read()
    for m in re.finditer(r'<p\b[^>]*>(.*?)</p>', s, re.S):
        inner = m.group(1).strip()
        if re.match(rf'(<[^>]+>\s*)*Version {re.escape(N)} (corrects|adds|states|redraws|removes|names)\b', inner):
            inner = re.sub(r'\s+', ' ', inner)
            sents = re.split(r'(?<=\.)\s+(?=[A-Z])', inner)          # the version sentence(s): up to "No result changes."
            out = [sents[0]]
            for x in sents[1:]:
                if x.startswith(('No result', 'The mathematics', 'The results')): out.append(x)
                else: break
            return re.sub(r'</?(b|strong)>', '', ' '.join(out))   # plain paragraph, as in recent records
    return None

def transform(rid, meta):
    """Returns (new description, new related_identifiers, list of change notes, list of problems)."""
    paper, kinds, src = REC[rid]
    desc = meta.get('description', ''); new = desc; notes = []; probs = []
    for old, rep in EDITS.get(rid, []):
        n = new.count(old)
        if n != 1: probs.append(f'edit text found {n} times: {old[:70]}…'); continue
        new = new.replace(old, rep); notes.append(('edit', old, rep))
    if rid == '24386728':   # Quanta of Space v3.0 (d): the v2 body under the v3.0 paragraph -> the book's current opening text
        if new.count(QUANTA_OLD) != 1 or new.count(QUANTA_BLAKE) != 1: probs.append('Quanta: stale body or Blake line not found once')
        else:
            new = new.replace(QUANTA_OLD, '<p>For my father, Alan Baker.')
            new = new.replace(QUANTA_BLAKE, QUANTA_BLAKE + QUANTA_NEW_BODY)
            notes.append(('edit', QUANTA_OLD, '(moved up, under the Blake lines:) ' + QUANTA_NEW_BODY + ' … For my father, Alan Baker.'))
    if 'b' in kinds and f'{rid}:b' not in SKIPPED and src:
        N = str(meta.get('version', '')).lstrip('v')
        line = version_line(meta, src, N)
        if not line: probs.append(f'no source states what Version {N} added')
        elif text(new).startswith(text(line)[:60]): notes.append(('info', 'version line already first', ''))
        else:
            new = f'<p>{line}</p>' + new; notes.append(('version line', '', line))
    rel = list(meta.get('related_identifiers', []))
    if 'f' in kinds:
        if any(r.get('identifier') == CW and r.get('relation_type', {}).get('id') == 'ispartof' for r in rel): notes.append(('info', 'isPartOf CW already there', ''))
        else: rel = rel + [ISPARTOF]; notes.append(('isPartOf', '', CW))
    # guards on the new text
    added = text(new)
    if len(BAN.findall(added)) > len(BAN.findall(text(desc))): probs.append('banned wording added: ' + ', '.join(BAN.findall(added)))
    if 'e' in kinds:
        if 'Fable' in new: probs.append('a model name (Fable) is still in the description')
        if len(re.findall(r'Claude', new)) > 1: probs.append(f'Claude named {len(re.findall("Claude", new))} times')
    return new, rel, notes, probs

def show(rid, notes):
    for kind, old, rep in notes:
        if kind == 'edit': print(f'   EDIT   before: {old}\n          after:  {rep}')
        elif kind == 'version line': print(f'   VERSION LINE (top): {rep}')
        elif kind == 'isPartOf': print(f'   ADD isPartOf {rep}')
        else: print(f'   ({old})')

apply = '--apply' in sys.argv
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
only = set(arg('--only', '').split(',')) - {''}
start = int(arg('--start', 0)); budget = float(arg('--budget', 250)); t0 = time.time()
ids = [r for r in REC if not only or r in only]
done = bad = 0; stopped = None
print(f'{"APPLY" if apply else "DRY RUN"}: {len(ids)} records; skipped: ' + ' · '.join(f'{k} ({v})' for k, v in SKIPPED.items()), flush=True)
for i, rid in enumerate(ids):
    if i < start: continue
    if time.time() - t0 > budget: stopped = i; break
    paper, kinds, src = REC[rid]
    rec = req(f'https://zenodo.org/api/records/{rid}')
    latest = str(req(f'https://zenodo.org/api/records/{rec["parent"]["id"]}/versions/latest')['id'])
    if latest != rid: print(f'[{i}] {paper} {rid}: NOT THE LATEST VERSION (latest {latest}); left alone', flush=True); bad += 1; continue
    new, rel, notes, probs = transform(rid, rec['metadata'])
    changed = new != rec['metadata'].get('description', '') or rel != rec['metadata'].get('related_identifiers', [])
    print(f'[{i}] {paper} {rid} v{rec["metadata"].get("version")} kinds {kinds}' + ('' if changed else '  (nothing to change)'), flush=True)
    show(rid, notes)
    if probs:
        bad += 1; print('   PROBLEM: ' + ' | '.join(probs) + '  -> left alone', flush=True); continue
    if not changed or not apply: done += changed; continue
    d = req(f'https://zenodo.org/api/records/{rid}/draft', 'POST')
    new2, rel2, _, probs2 = transform(rid, d['metadata'])
    if probs2 or new2 != new: print('   DRAFT DIFFERS from the published record; left as an open draft for a look', flush=True); bad += 1; continue
    d['metadata']['description'] = new2; d['metadata']['related_identifiers'] = rel2
    req(f'https://zenodo.org/api/records/{rid}/draft', 'PUT', {k: d[k] for k in ('metadata', 'files', 'access', 'pids', 'custom_fields') if k in d})
    p = req(f'https://zenodo.org/api/records/{rid}/draft/actions/publish', 'POST')
    ok = p['metadata'].get('description') == new2 and (('f' not in kinds) or any(r.get('identifier') == CW for r in p['metadata'].get('related_identifiers', [])))
    print('   saved' if ok else '   NOT SAVED', flush=True); done += ok; bad += not ok
    time.sleep(0.3)
print(f'{"changed" if apply else "would change"}: {done}; problems: {bad}' + (f'; budget reached, resume with --start {stopped}' if stopped is not None else ''))
print('FINAL ok' if bad == 0 and stopped is None else ('FINAL partial: resume with --start %d' % stopped if bad == 0 else 'FINAL FAIL: see PROBLEM lines'))
