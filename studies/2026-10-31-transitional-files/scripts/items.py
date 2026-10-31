import os, subprocess, json
INV = os.path.dirname(os.path.abspath(__file__))
H = '/home/dicto'
KR = H + '/k-research'

def tsv(name, key=0, val=2):
    d = {}
    for l in open(os.path.join(INV, name)):
        f = l.rstrip('\n').split('\t')
        if len(f) > max(key, val):
            d[f[key]] = f[val]
    return d

node_sz = {k: int(v) for k, v in tsv('node.tsv', 0, 2).items() if v.isdigit()}
dbb_kres = {k: int(v) for k, v in tsv('dbb-kres-sz.tsv', 0, 1).items() if v.isdigit()}
dbb_top = {}
for l in open(os.path.join(INV, 'dbb-top.tsv')):
    s, p = l.split()
    dbb_top[p] = int(s)
node_extra = {}
for l in open(os.path.join(INV, 'node-extra.tsv')):
    s, p = l.rstrip('\n').split('\t')
    node_extra[p if p.startswith('/') else H + '/' + p] = int(s)

def du_local(p):
    r = subprocess.run(['du', '-sk', '--', p], capture_output=True, text=True)
    return int(r.stdout.split()[0]) if r.returncode == 0 and r.stdout else 0

items = []  # dict(machine, conf, path, kb, why, where, kind)
gone = []
def add(machine, conf, path, why, where, kb=None, kind='rm'):
    if machine == 'pi' and not os.path.exists(path):
        gone.append(path); return
    if kb is None:
        if machine == 'pi':
            kb = du_local(path)
        elif machine == 'node':
            rel = path[len(H) + 1:]
            kb = node_extra.get(path, node_sz.get(rel, 0))
        else:
            rel = path[len(H) + 1:]
            kb = dbb_kres.get(rel, dbb_top.get(rel, 0))
    items.append(dict(machine=machine, conf=conf, path=path, kb=kb, why=why, where=where, kind=kind))

# ---------------- Pi ----------------
add('pi', 'SAFE', H + '/k-dshells', 'app worktree of branch dictonic-shells; merged into master, working tree clean', 'git: branch dictonic-shells 8d0703cc is in master', kind='worktree')

drafts = '''papers/2026-10-19-universal-pitet/dicto-universal-pitet-v3-draft.pdf
papers/2026-10-20-dicto-jewel/dicto-jewel-draft.pdf
papers/2026-10-20-dicto-sunstar/dicto-sunstar-draft.pdf
papers/2026-10-20-og-family-both-ways/dicto-og-family-draft.pdf
papers/2026-10-20-og-gyrated-octet/dicto-gyrated-octet-v3-draft.pdf
papers/2026-10-20-og-gyrated-octet/dicto-gyrated-octet-v4-draft.pdf
papers/2026-10-20-og-polytypes/dicto-og-polytypes-draft.pdf
papers/2026-10-21-aristotles-pyramid/aristotles-pyramid-draft.pdf
papers/2026-10-21-aristotles-pyramid/aristotles-pyramid-v2-draft.pdf
papers/2026-10-21-kyushindo-cores/kyushindo-cores-draft.pdf
papers/2026-10-21-reuleaux-platonic/reuleaux-platonic-draft.pdf
papers/2026-10-21-reuleaux-platonic/reuleaux-platonic-v2-draft.pdf
papers/2026-10-22-platonic-mixes/platonic-mixes-draft.pdf
papers/2026-10-22-platonic-mixes/platonic-mixes-v2-draft.pdf
papers/2026-10-22-swept-dodecahedra/swept-dodecahedra-draft.pdf
papers/2026-10-22-swept-dodecahedra/swept-dodecahedra-v2-draft.pdf
papers/2026-10-23-exact-vs-dissection/exact-vs-dissection-draft.pdf
papers/2026-10-23-golden-split/golden-split-draft.pdf
papers/2026-10-24-delian-bond/delian-bond-draft.pdf
papers/2026-10-25-david-goliath/david-goliath-draft.pdf
papers/2026-10-25-david-goliath/david-goliath-v2.pdf
papers/2026-10-25-gnomon-polar/gnomon-polar-draft.pdf
papers/2026-10-25-gnomon-polar/gnomon-polar-draft-v2.pdf
papers/2026-10-25-gnomon-polar/gnomon-polar-draft-v3.pdf
papers/2026-10-25-gnomon-polar/gnomon-polar-draft-v4.pdf
papers/2026-10-25-gnomon-polar/gnomon-polar-54-v5.pdf
papers/2026-10-25-gnomon-polar/gnomon-polar-v5b.pdf
papers/2026-10-25-gnomon-polar/gnomon-polar-final-candidate.pdf
papers/2026-10-25-keyed-switch/keyed-switch-56-draft.pdf
papers/2026-10-25-keyed-switch/keyed-switch-56-v2.pdf
papers/2026-10-25-relay-census/relay-census-draft.pdf
papers/2026-10-25-web-of-bonds/web-of-bonds-draft.pdf
papers/2026-10-25-web-of-bonds/web-of-bonds-draft-v2.pdf
papers/2026-10-25-web-of-bonds/web-of-bonds-draft-v3.pdf
papers/2026-10-26-rule-of-halves/rule-of-halves-57-draft.pdf
papers/2026-10-26-rule-of-halves/rule-of-halves-57-v2.pdf
papers/book-laws-of-stacking/SCOPE-laws-of-stacking.pdf
papers/book-laws-of-stacking/dicto-the-laws-of-stacking.pdf
papers/book-laws-of-stacking/dicto-hexoct-laws-of-stacking.pdf
papers/book-quanta-of-space/book-draft.pdf
papers/collected/dicto-collected-geometric-works-v16-draft.pdf
papers/collected/dicto-collected-geometric-works-v17-draft.pdf
papers/collected/dicto-collected-geometric-works-v19-draft.pdf
papers/collected/dicto-collected-geometric-works-v20-draft.pdf
papers/collected/dicto-collected-geometric-works-v30-draft.pdf
papers/intro-solids/ocd-stella/dicto-ocd-stella-v3-draft.pdf'''.split()
for r in drafts:
    nm = os.path.basename(r)
    if 'laws-of-stacking.pdf' in nm and 'SCOPE' not in nm:
        why = 'earlier book PDF; replaced by dicto-hexoct-hexagonality-law.pdf (Zenodo 23823003)'
    elif nm == 'book-draft.pdf':
        why = 'Quanta of Space draft; replaced by dicto-quanta-of-space.pdf (Zenodo 23789970)'
    else:
        why = 'superseded draft; the published PDF sits beside it'
    add('pi', 'SAFE', KR + '/' + r, why, 'git (tracked in k-research; history keeps it)', kind='tracked')

pdfs = json.load(open(os.path.join(INV, 'pdfs.json')))
for x in pdfs:
    r = x['rel']
    if r.startswith('papers/collected/v') and '/v48/' not in r and r.endswith('dicto-collected-geometric-works.pdf'):
        z = x['zen']
        add('pi', 'SAFE', x['path'], 'earlier Collected Works version; v48 is current',
            'Zenodo, each on its own version record (md5 match)' if z else 'git (tracked)', kind='tracked' if x['tracked'] else 'rm')
add('pi', 'SAFE', KR + '/papers/white-queen-600/v2/dicto-the-white-queen-600-cell.pdf', 'White Queen v2 PDF; v3 is current', 'Zenodo 23702910 (md5 match)')
add('pi', 'SAFE', KR + '/papers/swap-rule/dicto-the-swap-rule.pdf', 'Swap Rule v1 PDF; v2 is current', 'Zenodo 23682597 (md5 match); git', kind='tracked')
add('pi', 'SAFE', KR + '/papers/random-stackings-faults/v2/dicto-random-stackings-and-stacking-faults.pdf', 'v2 PDF, identical to the root copy; v3 is current', 'Zenodo 23718814 (md5 match); git', kind='tracked')

zips = [('datasets/2026-10-24-dicto-solids/dicto-solids-exact-geometry-v5-7f2d9385.zip', '23718094'),
        ('datasets/2026-10-24-dicto-solids/dicto-solids-exact-geometry-v6-584e90a3.zip', '23790799'),
        ('papers/4d-shadows/4d-shadows-study-b5f49873.zip', '23687224'),
        ('papers/real-materials-3/real-materials-3-study-d9c29049.zip', '23726065'),
        ('papers/swap-rule/swap-rule-study-c5033201.zip', '23682597'),
        ('papers/swap-rule/v2/swap-rule-study-76ddf347.zip', '23683033'),
        ('papers/white-queen-600/white-queen-600-study-fc1cbd4f.zip', '23690857'),
        ('papers/white-queen-600/v2/white-queen-600-study-fc1cbd4f.zip', '23702910')]
for r, z in zips:
    add('pi', 'SAFE', KR + '/' + r, 'untracked source zip, already uploaded', 'Zenodo %s (md5 match)' % z)
for r in ['star-square.png', 'star-square-opp.png', 'star-square-initials.png', 'star-square-initials-opp.png', 'star-cores-cover-front-initials.png']:
    add('pi', 'SAFE', KR + '/studies/2026-10-31-star-cores-cover/' + r, 'untracked cover variant, not chosen (chosen front committed)', 'rebuildable by scripts/star_square.py + cover_title.py (31b01473)')
for p in [H + '/kaleidohedra/dist', H + '/k-mix/dist', H + '/rhombiverse/dist']:
    add('pi', 'SAFE', p, 'build output (ignored)', 'rebuildable by npm run build')
add('pi', 'SAFE', H + '/.npm/_cacache', 'npm download cache', 'refilled by npm on demand')
add('pi', 'SAFE', H + '/.cache/thumbnails', 'desktop thumbnail cache', 'refilled on demand')
add('pi', 'SAFE', H + '/__pycache__', 'Python bytecode cache', 'rebuilt on import')
for s in ['ff9ee5b8-e526-41f8-8f5b-c551bab3dbbe', 'ddbf200a-bb62-4bd6-b8d7-210cc531c23f']:
    add('pi', 'SAFE', '/tmp/claude-1000/-home-dicto-Downloads-pet-bottle-rhombiverse/' + s, 'scratch of a finished session (RAM disk)', 'none needed: scratch')

# Pi CHECK
add('pi', 'CHECK', H + '/k-mix-star-step', 'worktree of star-step; merged into master and clean, but committed today before the 12:00 ship', 'git: star-step 3c9bcc44 is in master', kind='worktree')
add('pi', 'CHECK', KR + '/papers/real-materials-2/real-materials-2-study-643846bf.zip', 'untracked source zip', 'NOT on Zenodo record 23723566 (only the PDF there); study folder committed')
add('pi', 'CHECK', KR + '/papers/two-tiles/two-tiles-study-0814812a.zip', 'untracked source zip', 'NOT on Zenodo record 23756591 (only the PDF there); study folder committed')
add('pi', 'CHECK', KR + '/studies/2026-10-31-star-cores-cover/kdp-cover-star-cores.pdf', 'current KDP wrap (provisional spine), untracked', 'rebuildable by scripts/kdp_cover.py; commit or keep until assembly')
add('pi', 'CHECK', KR + '/studies/2026-10-31-star-cores-cover/kdp-cover-star-cores-guides.png', 'KDP wrap preview with guides, untracked', 'rebuildable by scripts/kdp_cover.py')
for f in ['kdp-cover-quanta.png', 'kdp-cover-quanta-guides.png', 'kdp-cover-quanta-guides.pdf']:
    add('pi', 'CHECK', KR + '/studies/2026-10-30-quanta-cover/' + f, 'untracked Quanta cover render', 'kdp-cover-quanta.pdf identical in papers-to-read/amazon-kdp-quanta; rebuildable by the cover script')
ptr = H + '/Documents/papers-to-read/'
for f in ['queen-davinci-red.png', 'queen-davinci-white.png', 'queen-geode-red.png', 'queen-geode-white.png', 'queen-geodes-sheet.png']:
    add('pi', 'CHECK', ptr + f, 'Queen Geodes round 4 preview: delete once DICTO has looked', 'git: k-research 2f6a39f6 studies/2026-10-31-queen-geodes/out (identical)')
for f in ['cards-79-80-desktop.png', 'cards-79-80-phone.png', 'dicto-rcp-phone.png', 'dicto-rcp-pv-120.png', 'dicto-rcp-pv-600.png', 'dicto-rcp-queens.png', 'queens-lens-phone.png', 'rhombi-choice-desktop.png', 'rhombi-choice-phone.png', 'star-step-desktop.png', 'star-step-phone.png', 'star-step-phone-star.png', 'star-step-vs-kp.png', 'star-cores-cover-wrap.png']:
    add('pi', 'CHECK', ptr + f, 'app or cover screenshot shown for a decision', 'rebuildable from the app / cover script')
for d in ['amazon-kdp', 'amazon-kdp-alicia', 'amazon-kdp-golden', 'amazon-kdp-quanta']:
    add('pi', 'CHECK', ptr + d, 'interim KDP set, held until all four books settle (DICTO 10-30)', 'interiors identical to k-research working copies (golden also committed)')
add('pi', 'CHECK', H + '/kaleidohedra/node_modules', 'second node_modules (k-mix has its own)', 'rebuildable by npm ci')
add('pi', 'CHECK', H + '/Pictures/Screenshots', 'desktop screenshots 10-18 to 10-30', 'none: looked at')
add('pi', 'CHECK', H + '/Downloads/dictoroids_round5_test.ARCHIVED-2026-07-29', 'archived July test', 'unknown')
add('pi', 'CHECK', H + '/Downloads/pbr-patches', 'old patch files (September)', 'likely applied in rhombiverse git')
add('pi', 'CHECK', '/tmp/claude-1000/-home-dicto-Downloads-pet-bottle-rhombiverse/998f9583-0bbe-48af-a44e-674289f2a28d/scratchpad', 'scratch of the running session (RAM disk; holds these scripts)', 'clears at reboot; delete after this session')

# Pi KEEP
proj = H + '/.claude/projects/-home-dicto-Downloads-pet-bottle-rhombiverse/'
for p in ['Downloads/sculpture-photos.zip', 'Downloads/sculpture-photos-only.zip', 'Downloads/KPR-photos']:
    add('pi', 'KEEP', H + '/' + p, "DICTO's own photos", 'no other copy found: move to LaCie')

# ---------------- dicto-node ----------------
N = H
node_safe = {
 'k-mix-lens': 'test copy of branch queens-lens (merged); every file in Pi git',
 'k-mix-old': 'old test copy of k-mix; every file in Pi git',
 'k-golden': 'test copy (golden-split); every file in Pi git',
 'k-axe': 'test copy (k-axe); every file in Pi git',
 'k-wq': 'test copy (white queen); every file in Pi git',
 'k-view49': 'test copy; every file in Pi git',
 'k-merge': 'test copy; every file in Pi git',
 'k-master-base': 'test copy of master 10-20; every file in Pi git',
 'k-master-test': 'test copy of master 10-20; every file in Pi git',
 'k-bull': 'copy; every file in Pi git',
 'kjoin': 'copy; every file in Pi git',
 'papersv2': 'print copy; every file in Pi git',
 'rhombiverse': 'copy; every file in Pi git',
 'kgbp': 'copy; every file in Pi git (one empty probe)',
 'kgbp-papers': 'print copy; every file in Pi git',
 'fusedpaper': 'print copy; every file in Pi git',
 'fprint': 'print copy; every file in Pi git',
 'site-check': 'site test copy; every file in Pi git',
 'rhombiverse-head': 'copy; every file in Pi git',
 'scratch': 'scratch copy; every file in Pi git',
 'kaleidohedra-studies': 'copy; every file in Pi git (one 1 KB shot script)',
 'kfig': 'copy; every file in Pi git (one empty script)',
 'ot-check': 'test copy; every file in Pi git',
 'pv-lang': 'Polyhedraverse language test copy; only build logs differ',
 'k-soft': 'test copy; only extra files are Fuji JSONs identical on the Pi',
 'scratch-soft-reuleaux': 'test copy; only extra files are Fuji JSONs identical on the Pi',
 'kaleidohedra-check': 'test copy; only extra files are Fuji JSONs identical on the Pi',
 'fujifam': 'Fuji paper copy; extra JSONs identical on the Pi, two small test PNGs',
 'ffprint': 'Fuji print copy; extra JSONs identical on the Pi',
 'ds-check': 'site test copy; coast.npz and .env.local identical on the Pi',
 'dictospheres-preview': 'site preview copy; coast.npz and .env.local identical on the Pi',
 'dicto-site-test': 'site test copy; coast.npz and .env.local identical on the Pi',
 'ds-preview': 'site preview copy; coast.npz identical on the Pi, plus 5 preview PNGs',
 'scratch-ms-tiles': 'test copy plus test screenshots (10-23)',
 'scratch-view49': 'test copy plus 4 test screenshots (10-23)',
 'rl-shots': 'test screenshots 10-21',
 'up-shots': 'test screenshots 10-19',
 'antiprism-build': 'Antiprism 0.29 build tree (installed copy in ~/antiprism)',
 'kjoin-rdist': 'old dist build (10-08)',
 'kjoin-kdist': 'old dist build (10-08)',
 'rv-dist': 'old Rhombiverse dist build (09-26)',
 'rhombiverse-dist': 'old Rhombiverse dist build (09-24)',
 'up-figs': 'figure scratch; extras are vendored three.js files',
}
where_for = lambda n: ('rebuildable: npm run build' if 'dist' in n else
                       'rebuildable: antiprism-0.29.tar.gz (public source)' if n == 'antiprism-build' else
                       'none needed: screenshots, rebuildable by the shot scripts' if 'shots' in n else
                       'git on the Pi (every file hashed and found)')
for n, why in node_safe.items():
    add('node', 'SAFE', N + '/' + n, why, where_for(n))
add('node', 'SAFE', N + '/audit-lh/node_modules', 'node_modules of a 10-10 audit', 'rebuildable by npm ci')
for s in ['new', 'old', 'p']:
    add('node', 'SAFE', N + '/sa-batch/' + s, 'Zenodo batch staging (10-20): PDFs before and after', 'Zenodo: all 78 PDFs md5-matched to record versions')
add('node', 'SAFE', N + '/.npm/_cacache', 'npm download cache', 'refilled by npm on demand')
add('node', 'SAFE', N + '/.npm/_npx', 'npx cache', 'refilled on demand')
add('node', 'SAFE', N + '/.cache/pip', 'pip download cache', 'refilled on demand')
for p, kb in node_extra.items():
    if p.startswith(N + '/k-research/'):
        add('node', 'SAFE', p, 'print draft in the node print copy; superseded', 'final PDF on the Pi / Zenodo; drafts rebuildable from git', kb=kb)

node_check = {
 'k-mix': ('test copy of master (two probe scripts extra); main rsync target', 'git on the Pi'),
 'k-rcp4': ('test copy used today (RCP v4)', 'git on the Pi (every file found)'),
 'k-mix-credits': ('test copy used today (credits)', 'git on the Pi (every file found)'),
 'k-mix-rhombi': ('test copy used today (rhombi-choice)', 'git on the Pi (every file found)'),
 'k-mix-star-step': ('test copy used today (star-step)', 'git on the Pi (every file found)'),
 'k-mix-dicto-rcp': ('test copy used today; i18n.js and two changelogs differ from Pi git', 'compare with ~/k-mix-dicto-rcp on the Pi'),
 'kcheck': ('old test copy (10-11); render.js differs from git', 'unknown: an uncommitted render.js variant'),
 'kgold': ('old test copy (10-10); rhombis/i18n.js differs from git', 'unknown'),
 'kaleidohedra': ('old copy (10-20); all in git except a raw 255 MB stella-seed-cells.json and chorus data', 'raw JSON rebuildable by studies/2026-10-16-ocd-pyrochlore/scripts/stella_seed_cells.py; summary .txt committed'),
 'k-research': ('print copy; rest matches git; book DRAFT PDFs listed as SAFE', 'git on the Pi; two book scripts differ (plates_section.py, assemble.py)'),
 'kaleidohedra-papers': ('print copy (10-24); 5 files not in git (briefing.pdf, cmp-test.pdf)', 'mostly git'),
 'pi-scratch-archive': ('archived Pi session scratchpads (to 10-16)', 'no other copy; contains downloaded references'),
 'og-poly': ('OG renders 10-20 to 10-22: scene HTML up to 100 MB, shots, pkl snapshots', 'figures in k-research; renders rebuildable by the scripts; 30 MB of pkl only here'),
 'ico13': ('Icosa-13 study data (10-12), 24 MB not in git', 'no other copy of the raw data'),
 'dodeca13': ('Dodeca-13 study data (10-09), npy/pkl not in git', 'no other copy of the raw data'),
 'sa-batch/k': ('source copy used for the batch; 16 unstamped PDFs', 'git on the Pi for the rest'),
 'libpdf': ('8 Wikipedia PDFs; 7 identical in the reference library', 'Carbon-nano-onion PDF is not in the library: add it first'),
 'audit-lh': ('Lighthouse audit JSONs of 10-10 (after node_modules)', 'no other copy; results reported 10-10'),
 'polyhedraverse': ('old Polyhedraverse clone, 5 modified and 69 untracked files', 'HEAD in GitHub main; local changes unknown'),
 'pv-proj': ('old Polyhedraverse clone, 3 modified files, 760 MB node_modules/.next', 'HEAD in GitHub main'),
 'krp-core-check': ('krp-core clone, 5 modified files', 'HEAD in GitHub main'),
 'dictospheres': ('site checkout, 14 untracked files (11 MB)', 'HEAD in git'),
 'dictosite': ('old site checkout, 2 modified files', 'HEAD in dictospheres main'),
 'fusedenv': ('Python venv last used 10-14', 'rebuildable by pip; plotenv is the current one'),
 'ap-check': ('Antiprism conway output files (10-16)', 'rebuildable by antiprism'),
 'fuji-model': ('Fuji kit renders (10-14), 118 files not in git', 'probably rebuildable'),
 'cleo-hold': ('held scratch (10-18): chorus-exact.json, scutoid tiles', 'chorus-exact.json also in node kaleidohedra copy'),
 'pp': ('page sheets of papers (10-11)', 'rebuildable from the PDFs'),
}
for n, (why, where) in node_check.items():
    add('node', 'CHECK', N + '/' + n, why, where, kb=node_extra.get(N + '/' + n) if '/' in n else None)
add('node', 'KEEP', N + '/dicto-notes', 'git repo with no copy on the Pi or GitHub found', 'move to LaCie')
add('node', 'KEEP', N + '/dphotos', "DICTO's photos (IMG_*.jpeg)", 'no other copy found: move to LaCie')

# ---------------- dicto-big-brother ----------------
B = H
dbb_safe = {
 'k-mix': 'test copy (10-27); every file in Pi git',
 'k-dshells': 'test copy (10-25); every file in Pi git',
 'k-census': 'test copy (10-25); every file in Pi git',
 'k-census-run': 'test copy (10-25); every file in Pi git',
 'k-axe': 'test copy (10-24); every file in Pi git (one empty probe)',
 'kaleidohedra-check': 'test copy (10-24); every file in Pi git',
 'ds-v3-check': 'dataset v3 check copy; every file in Pi git',
 'k-research': 'small copy (10-28); every file in Pi git',
 'series-wob': 'copy; every file in Pi git',
 'k-dshells-shots': 'test screenshots 10-25',
 'gw-shots': 'test screenshots 10-25',
 'prev57': 'card preview 10-26',
 'ffprint': 'three tiny open scripts',
}
for n, why in dbb_safe.items():
    add('dbb', 'SAFE', B + '/' + n, why, 'none needed: screenshots' if 'shots' in n or n == 'prev57' else 'git on the Pi (every file hashed and found)')
add('dbb', 'SAFE', B + '/.cache/pip', 'pip download cache', 'refilled on demand')
kres_safe = {
 'k57': 'copy for #57 (10-26); in git; extra arXiv PDF is in the library',
 'papers': 'print copy (10-29); extras are drafts and zips verified on Zenodo',
 'series': 'series print copy (10-30); extras are drafts, a Zenodo zip, page PNGs',
 'book': 'Quanta book print (10-25); book-draft.pdf also in git',
 'web-of-bonds': 'print copy; every file in git', 'keyed-switch': 'print copy; in git', 'rule-of-halves': 'print copy; in git',
 'gnomon-polar-print': 'print copy; in git', 'relay-census': 'print copy; in git', 'david-goliath': 'print copy; in git',
 'quanta-atoms': 'run copy; in git', 'dataset-v3': 'dataset build copy; in git', 'dataset-v4': 'dataset build copy; in git',
 'dataset-v5': 'dataset build copy; in git', 'dataset-v6': 'dataset build copy; in git', '4d-shadows-study': 'run copy; in git',
 'census': 'run copy; in git', 'spiked-ti': 'run copy; in git', 'gnomon-polar': 'run copy; in git', 'esc': 'run copy; in git',
 'cw24': 'print copy; in git', 'cw-print': 'print copy; in git', 'ti-pyramids': 'run copy; in git', 'swap': 'run copy; in git',
 'studies-gnomon': 'copy; in git', 'st57': 'copy; in git', 'naming': 'copy; in git', 'keyed-hexoct': 'run copy; in git',
 'hexoct-k-clock': 'run copy; in git', 'gnplan': 'copy; in git', 'gnomon-shapes': 'copy; in git', 'fig70src': 'figure copy; in git',
 'fig70': 'figure copy; in git', 'fig68': 'figure copy; in git', 'fig67': 'figure copy; in git', 'dg-checks': 'copy; in git',
 'core-cycle': 'run copy; in git', 'cards': 'copy; in git', 'site-test': 'site test copy; coast.npz and .env.local identical on the Pi',
 'kmix-dist': 'dist build (10-30)', 'stk-shots': 'test screenshots', 'stk-shots2': 'test screenshots', 'stk-shots3': 'test screenshots',
 'golden-cover': 'cover render copy; extras are preview PNG/PDF', 'wonder-cover': 'cover render copy; extras are preview PNG/PDF',
 'parity': 'two probe scripts', 'old-methods': 'empty helper script', 'focus': 'print scratch',
}
for n, why in kres_safe.items():
    add('dbb', 'SAFE', B + '/kres-tmp/' + n, why,
        'rebuildable: npm run build' if 'dist' in n else 'none needed: screenshots' if 'shots' in n else 'git on the Pi; Zenodo for zips' if n in ('papers', 'series') else 'rebuildable by committed cover scripts' if 'cover' in n else 'git on the Pi (every file hashed and found)')
kres_check = {
 'pyramids': ('raw search data (10-30): f2f-deep-level5.pkl 71 MB, q2 results', 'no other copy of the raw data; results in k-research?'),
 'ico-hexa': ('17 MB part renders (10-27)', 'probably rebuildable'),
 '4d': ('4D run data (10-30): solids.pkl, eig/solve JSON', 'no other copy of the raw data'),
 'kmix-stk': ('test copy (10-27); i18n.js differs from git', 'likely an older i18n.js'),
 'star-cores-cover': ('cover renders (today), same names as the Pi untracked files', 'Pi copy'),
 'star-cores-exact': ('exact runs (today), 106 small result files not in git', 'check against the study commit'),
 'star-cores': ('run logs (10-30); the same logs are untracked on the Pi', 'Pi copy'),
 'star-cores-figs': ('figure run (today)', 'git'),
 'queen-geodes': ('render run (today) plus probe.py', 'git'),
 'plates': ('plates run (today)', 'git'),
 'alicia-plates': ('plates run (today); render_atlas.py differs', 'check'),
 'figc': ('figure run (today)', 'git'),
 'hexoct-cover': ('cover renders; cover_title.py differs (2 KB)', 'check the script'),
 's56': ('#56 figure run: OBJ meshes and logs', 'rebuildable'),
 'splash': ('figure OBJ meshes', 'rebuildable'),
 'splash2': ('splash run output JSONs', 'rebuildable'),
 'pyro': ('columns.png and patch OBJs', 'rebuildable'),
 'pvp': ('25 piece JSONs not in git', 'check PV builders'),
 'pieces29': ('5 empty piece JSONs', 'none'),
 'endless': ('proof output and two scripts not in git', 'check'),
 'japanese': ('Japanese sample drafts and logs', 'check'),
 'bloom-joined': ('joined pieces JSON and join.py', 'check'),
 'fallen': ('fallen-exact.json and recognise.py', 'check'),
 'dg-fig': ('make_figure.py not in git', 'check'),
 'fig69': ('fibonacci-tower.png', 'check'),
 'libidx': ('library index print (INDEX.pdf)', 'rebuildable from library-index'),
 'priorart': ('three Hales arXiv PDFs + text', 'not in the library under these names'),
 'studies': ('study scratch', 'check'),
 'out': ('empty', 'none'),
 'print': ('empty', 'none'),
}
for n, (why, where) in kres_check.items():
    add('dbb', 'CHECK', B + '/kres-tmp/' + n, why, where)
for n, why, where in [
    ('og-poly', 'Heikegani renders (10-24): 3 scene HTML of 27 MB + shots', 'in the nightly LaCie backup; the stylings PDF was delivered'),
    ('runs', 'scale-anomalies sources (IAEA, NIST PDFs) and test renders', 'sources: add to library first'),
    ('study-runs', 'study run outputs 10-25/26 (68 PNGs not in git)', 'check'),
    ('studies', 'swept and changeover scratch (9 files not in git)', 'in the nightly LaCie backup'),
    ('kaleidohedra-papers', 'dataset reading-copy prints (10-24)', 'superseded by dataset v6'),
    ('.cache/ms-playwright', 'Playwright browsers (revision 1248, in use)', 'keep unless tests move'),
]:
    add('dbb', 'CHECK', B + '/' + n, why, where)

json.dump(items, open(os.path.join(INV, 'items.json'), 'w'), indent=0)
json.dump(gone, open(os.path.join(INV, 'gone.json'), 'w'))
print(len(items), 'gone', gone)
