# Dehn atoms (19 Nov 2026): the list of every single-solid atom of The DICTOnary of Atoms (catalogue D1-D178 + the known atoms),
# with the source of its corners. Reads the two catalogue pages (names and kinds exactly as printed) and joins each atom to an exact
# model file (DICTO Solids dataset; the 17 Nov missing-atoms batches) or to an exact construction (constructions.py); anything else is
# listed with the reason it is skipped. Clusters, structures, networks, compounds, curved bodies, star polyhedra and 4D solids are out
# of scope. Output: data/manifest.json. Usage: manifest.py <k-research root> <dataset dir> <out json>
import csv, html, json, os, re, sys, glob
KR, DS, OUT = sys.argv[1:4]
CAT = os.path.join(KR, 'papers/book-quanta-dictonary')
MISS = [os.path.join(KR, 'studies/2026-11-17-atoms-missing'), os.path.join(KR, 'studies/2026-11-17-atoms-missing-2')]
def rel(p): return os.path.relpath(p, KR) if p.startswith(KR) else 'math-data:' + os.path.relpath(p, os.path.dirname(os.path.dirname(DS)))
def gallery(fn):
    s = open(os.path.join(CAT, fn), encoding='utf8').read(); out = []
    for m in re.finditer(r'<div class="an"><b>(.*?)</b>\s*(.*?)</div><div class="am">(.*?)</div>', s, re.S):
        no, name, am = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in m.groups()]
        kind, _, frm = am.partition('·'); out.append(dict(no=no, name=name, kind=kind.strip(), frm=frm.strip()))
    return out
def tables(fn):
    s = open(os.path.join(CAT, fn), encoding='utf8').read(); out = []
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', s, re.S):
        c = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in re.findall(r'<td[^>]*>(.*?)(?=<td|$)', r, re.S)]
        if len(c) >= 4 and c[0] in ('—', 'J1') or (len(c) >= 4 and re.match(r'D\d+$', c[0])): out.append(dict(no=c[0], name=c[1], kind=c[2], frm=c[3]))
    return out
main = gallery('atoms-catalogue.html') + tables('atoms-catalogue.html')
known = gallery('atoms-catalogue-known.html') + [t for t in tables('atoms-catalogue-known.html')]
# model files: the dataset (via its index) and the two missing-atoms batches (d_number in each file)
files = {}
for r in csv.DictReader(l for l in open(os.path.join(DS, 'index.csv'), encoding='utf8') if not l.startswith('#')):
    if r['dataset_file'] and r['universal_number'].startswith('D'): files.setdefault(r['universal_number'], os.path.join(DS, r['dataset_file']))
pieces = {}
for b in MISS:
    for f in sorted(glob.glob(b + '/models/*.json')):
        d = json.load(open(f)); dn = d.get('d_number') or ''
        if dn.startswith('D'): files.setdefault(dn, f)
    for f in sorted(glob.glob(b + '/models/pieces/*.json')):
        pieces.setdefault(json.load(open(f)).get('d_number') or os.path.basename(f), []).append(f)
DSF = lambda s: os.path.join(DS, 'solids', s + '.json'); KM = lambda s: os.path.join(MISS[1], 'models', s + '.json')
# sets under one number: each piece computed alone (the set file holds several solids side by side)
SETS = {'D72': 'piece-dented-tetrahedron', 'D73': 'piece-dicto-fill-set', 'D74': 'piece-cleo-towers', 'D75': 'piece-polar-cleo-towers'}
SETFILES = {k: sorted(f for f in glob.glob(MISS[0] + '/models/pieces/*.json') if os.path.basename(f).startswith(v)) for k, v in SETS.items()}
SETFILES['D138'] = [KM('piece-diadem'), os.path.join(MISS[1], 'models/pieces/piece-diadem-r.json')]
# atoms with no model file: exact constructions (constructions.py) or the reason they are skipped
CONS = {'D11': ('same', 'D4', 'the DICTO Jewel itself (#18 defines the Hexa Jewels as exact DICTO Jewels; 2026-11-17-atoms-missing, "Not drawn")'),
        'D12': ('ident', 'FUJI', 'studies/2026-10-14-axe-cleo-fuji/nets/pieces.json, identified in Q(sqrt5) by the dehn-words rule (each corner to 2e-9)'),
        'D16': ('cons', 'admiral_cap', "exact definition in the app source (k-mix krp-core edgeRoof.js): two tetrahedra over one edge of the unit icosahedron, apex at the octahedron's corner; checked: volume phi/12, edges 1, sqrt2/2, phi sqrt2/2"),
        'D54': ('cons', 'hex_aktis', 'OG (dataset dicto-ogdoecontahedron) hexagon joined to the centre (build-cleo-towers.py: 20 Hex Aktis + 60 Deltoid Aktis, every apex at the centre)'),
        'D55': ('cons', 'deltoid_aktis', 'OG (dataset dicto-ogdoecontahedron) deltoid joined to the centre (as D54)'),
        'D56': ('cons', 'triaktis', 'OTT (dataset dicto-ott) triangle of the 24-class joined to the centre (studies/2026-10-20-ott-rays: 8 Oktaktis + 24 Triaktis + 6 Tetraktis)'),
        'D57': ('cons', 'tetraktis', 'OTT (dataset dicto-ott) rhombus joined to the centre (as D56)'),
        'D133': ('skip', 'no exact form', '#96 leaves the exact form open (Section 6); no model file'),
        'D134': ('skip', 'no exact form', '#96 leaves the exact form open (Section 6); a family, one per brick size; no model file')}
FLOAT = {'D8': 'k-mix krp-core dodeca13Data.js (registry floats)', 'D10': 'k-mix krp-core hexaData.js (registry floats, about 8 digits)',
         'D13': 'k-mix krp-core kits13.js KIT13_UNITY_VAJRA (6 digits)', 'D17': 'kits13.js KIT13_BODHI_B4 (6 digits)', 'D18': 'kits13.js KIT13_BODHI_B1 (6 digits)',
         'D23': 'studies/2026-10-16-polar-dharma (floats)', 'D24': 'studies/2026-10-15-icosa-star-hollow/data/exact_meshes.json (9-digit floats)',
         'D25': 'studies/2026-10-15-icosa-star-hollow/data/exact_meshes.json (9-digit floats)', 'D26': 'studies/2026-10-15-icosa-star-hollow/data/exact_meshes.json (9-digit floats)',
         'D27': 'studies/2026-10-15-icosa-star-hollow/data/exact_meshes.json (9-digit floats)', 'D65': 'k-mix krp-core cleo-sphere.js ANTONIUS (floats)',
         'D66': 'k-mix krp-core cleo-sphere.js PENTA_CLEO (floats)', 'D102': 'studies/2026-10-29-quanta-atoms/dicto-fallen-humpty.json (16-digit decimals only)'}
# known atoms: catalogue name -> model file or construction
KNOWN = {'dodecahedron stellation 8': ('float', 'k-mix krp-core sunstar.js DOGSTAR (registry floats)'),
         'Mosseri–Sadoc tile t6': ('ident', 'AXE'), 'Mosseri–Sadoc tile t4': ('ident', 'CLEO'),
         'icosahedron face pyramid': ('cons', 'cleo_icos'),
         'truncated octahedron x = φ': ('file', DSF('dicto-icosaxes')), 'truncated octahedron x = 1/φ': ('file', DSF('dicto-unborn-axes')),
         'regular octahedron at the Delian bond': ('file', DSF('dicto-delilah')), "convex hull of Jessen's orthogonal icosahedron": ('file', DSF('dicto-goliath')),
         'tetragonal disphenoid': ('file', DSF('dicto-david')),
         'cell-first section of the 600-cell at height 0': ('file', DSF('dicto-alicia')),
         'cell-first section of the 600-cell at height (3 + √5)/2': ('file', DSF('dicto-unicorn')),
         'cell-first section of the 600-cell at height (5 + 3√5)/4': ('file', DSF('dicto-bandersnatch')),
         'regular-hexagon stage of the icosidodecahedron': ('cons', 'id_stage_third'), 'regular-decagon stage of the icosidodecahedron': ('cons', 'id_stage_golden'),
         'Mosseri–Sadoc tile t3': ('file', KM('known-tricap'), KM('known-cleo-low')), 'Mosseri–Sadoc tile t2': ('file', KM('known-hound-tooth')),
         'pseudoicosahedron': ('file', KM('known-unborn')), 'excavated dodecahedron': ('file', KM('known-inner-eye')),
         'rectified truncated icosahedron': ('file', KM('known-cut-og')), 'augmented cuboctahedron': ('file', KM('known-dicto-13-coa')),
         'half rhombic dodecahedron': ('file', KM('known-hemi-rd')), 'square bipyramid': ('file', KM('known-oct-16')), 'triangular bipyramid': ('file', KM('known-tbp-5')),
         'DICTO all-rhombus block': ('cons', 'all_rhombus_block'), 'DICTO flattened rhombohedron': ('cons', 'flattened_rhombohedron'),
         'Bain disphenoid': ('skip', 'no vertex data found (finding F3; not in the dataset or the app registry)'), 'Bain rhombic dodecahedron': ('cons', 'bain_rd'),
         "Fedorov's elongated dodecahedron with regular hexagons": ('cons', 'regular_hex_ed'),
         'Half octahedron P': ('cons', 'half_octahedron'), "Tetrahedron face pyramid Q and Q'": ('cons', 'tetra_face_pyramid'),
         'A · HexOct 3/8 c-tile, brick of two cubes': ('cons', 'brick'), 'D · HexOct −11/24 h-tile, regular hexagonal prism': ('cons', 'hex_prism')}
IN = ('solid', 'piece', 'piece (a family, one per brick size)')
atoms, out_scope = [], []
def entry(a, book):
    e = dict(no=a['no'], name=a['name'], kind=a['kind'], frm=a['frm'], book=book)
    if a['kind'] not in IN: out_scope.append(e); return
    no = a['no']
    if book == 'new':
        if no in SETFILES: e.update(source='set', files=[rel(f) for f in SETFILES[no]])
        elif no in CONS:
            k, v, note = CONS[no]; e.update(source=k, key=v, note=note)
        elif no in FLOAT: e.update(source='float', note=FLOAT[no])
        elif no in files: e.update(source='file', files=[rel(files[no])])
        else: e.update(source='missing')
    else:
        key = next((k for k in KNOWN if a['name'].startswith(k)), None)
        if key is None: e.update(source='missing')
        else:
            v = KNOWN[key]
            if v[0] == 'file': e.update(source='file', files=[rel(f) for f in v[1:]])
            elif v[0] in ('cons', 'ident'): e.update(source=v[0], key=v[1])
            elif v[0] == 'float': e.update(source='float', note=v[1])
            else: e.update(source='skip', key='no data', note=v[1])
    atoms.append(e)
for a in main: entry(a, 'new')
for a in known: entry(a, 'known')
json.dump(dict(atoms=atoms, out_of_scope=out_scope), open(OUT, 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print('in scope', len(atoms), Counter(a['source'] for a in atoms), 'out of scope', len(out_scope))
for a in atoms:
    if a['source'] == 'missing': print('MISSING', a['no'], a['name'])
