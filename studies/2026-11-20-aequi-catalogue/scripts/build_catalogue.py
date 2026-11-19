# The numbered main catalogue of the Aequi: the 149 dice of the seven frame groups (study 2026-11-19-aequi-complete).
# usage: build_catalogue.py DICE_DIR OUT_DIR
# Numbering (DICTO, 20 Nov): within each group, groups in the order Ih, Oh, Td, Th, T; inside a group by m, then N,
# then the orbit families in the order C6, O8, RD12, D12, I12, RT24 (each die's sorted list of orbit family ranks,
# compared lexicographically), then the placement of a split orbit (the orbit whose representative has fewer minus signs
# first: the half RT24/12 through (phi, 1/phi, 1) before the half through (phi, 1/phi, -1)), last the study's row number.
import json, sys, os, glob, csv, re
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_EVEN
dice_dir, out = sys.argv[1], sys.argv[2]
GROUPS = ['Ih', 'Oh', 'Td', 'Th', 'T']
FAM = ['C6', 'O8', 'RD12', 'D12', 'I12', 'RT24']
INIT_ORDER = ['T', 'C', 'O', 'RD', 'D', 'I', 'RT']          # source solids by face count: 4, 6, 8, 12, 12, 20, 30
SOLID = {'T': 'tetrahedron', 'C': 'cube', 'O': 'octahedron', 'RD': 'rhombic dodecahedron', 'D': 'dodecahedron',
         'I': 'icosahedron', 'RT': 'rhombic triacontahedron'}
def parts(label):
    """orbit label -> {family: number of directions}; 'C6+RT24/30' -> {C6: 6, RT24: 24}; 'O8/4a' -> {O8: 4}."""
    m = re.fullmatch(r'([A-Z0-9+]+?)(?:/(\d+)[ab]?)?', label)
    fams = m.group(1).split('+'); k = m.group(2)
    if len(fams) > 1: return {f: int(re.sub(r'^[A-Z]+', '', f)) for f in fams}
    f = fams[0]; return {f: int(k) if k else int(re.sub(r'^[A-Z]+', '', f))}
def initials(labels):
    """source-solid initials. The icosahedron's 20 = O8 + I12 and the triacontahedron's 30 = C6 + RT24 count as I and RT
    whenever all their directions are faces (as one orbit or split, as in D191 RDI-32); otherwise each orbit names its own
    source: C6 C, O8 O, O8/4 T (a tetrahedron, as in TC-10), RD12 RD, D12 D, I12 I, RT24 or a half of it RT."""
    n = Counter()
    for l in labels:
        for f, k in parts(l).items(): n[f] += k
    got = set()
    if n['O8'] == 8 and n['I12'] == 12: got.add('I'); n['O8'] = n['I12'] = 0
    if n['C6'] == 6 and n['RT24'] == 24: got.add('RT'); n['C6'] = n['RT24'] = 0
    if n['C6']: got.add('C')
    if n['O8'] == 8: got.add('O')
    elif n['O8'] == 4: got.add('T')
    if n['RD12']: got.add('RD')
    if n['D12']: got.add('D')
    if n['I12']: got.add('I')
    if n['RT24']: got.add('RT')
    return ''.join(x for x in INIT_ORDER if x in got), got
def famkey(labels):
    return sorted(tuple(sorted(FAM.index(f) for f in parts(l))) for l in labels)
def repkey(d):
    return sorted((tuple(sorted(FAM.index(f) for f in parts(l))), r.count('-')) for l, r in zip(d['orbits'], d['orbit_representatives']))
def order(d):
    return (d['m'], d['N'], famkey(d['orbits']), repkey(d), d['sid'])
def d12(s):
    return str(Decimal(s).quantize(Decimal('1e-12'), rounding=ROUND_HALF_EVEN))
# settled names (book atoms D179-D191, Equanimity and study 2026-11-19-aequus-rd-ico): group, orbit labels, name
SETTLED = [(179, 'Td', ['C6', 'O8/4'], 'TC-10'), (180, 'Oh', ['C6', 'O8'], 'CO-14'), (181, 'Td', ['O8/4', 'RD12'], 'TRD-16'),
           (182, 'T', ['O8/4', 'D12'], 'TD-16'), (183, 'Oh', ['C6', 'RD12'], 'CRD-18'), (184, 'Th', ['C6', 'D12'], 'CD-18'),
           (185, 'Oh', ['O8', 'RD12'], 'ORD-20'), (186, 'Th', ['O8', 'D12'], 'OD-20'), (187, 'Th', ['RD12', 'D12'], 'RDD-24'),
           (188, 'Ih', ['O8+I12/20', 'D12'], 'DI-32'), (189, 'Ih', ['C6+RT24/30', 'D12'], 'DRT-42'),
           (190, 'Ih', ['C6+RT24/30', 'O8+I12/20'], 'IRT-50'), (191, 'Th', ['O8', 'RD12', 'I12'], 'RDI-32')]
dice = []
for p in sorted(glob.glob(os.path.join(dice_dir, '*.json'))):
    d = json.load(open(p))
    if d['group'] in GROUPS: dice.append(d)
rows = []
for g in GROUPS:
    L = sorted([d for d in dice if d['group'] == g], key=order)
    for i, d in enumerate(L, 1):
        ini, got = initials(d['orbits'])
        if 'DIRT' in ini: ini = '·'.join(x for x in INIT_ORDER if x in got)   # DICTO 20 Nov: dots where the initials would spell a word
        dn = [s for s in SETTLED if s[1] == g and sorted(s[2]) == sorted(d['orbits'])]
        rows.append(dict(group=g, number=i, name='Aequus %s-%d, %s %d' % (ini, d['N'], g, i), short='%s-%d' % (ini, d['N']),
            initials=ini, solids=' + '.join(SOLID[x] for x in INIT_ORDER if x in got), m=d['m'], N=d['N'],
            mosaicus='yes' if d['m'] >= 4 else 'no', hands=d['hands'],
            orbits=' + '.join('%s %s' % (l, r) for l, r in zip(d['orbits'], d['orbit_representatives'])),
            faces='; '.join(d['faces_by_orbit']), corners=d['corners'],
            depths='; '.join(d12(x) for x in d['depths_60_digits']),
            D=('D%d' % dn[0][0]) if dn else '', settled=dn[0][3] if dn else '',
            study_row=d['sid'], source='dice/' + os.path.basename(d['file'])))
F = ['group', 'number', 'name', 'initials', 'solids', 'm', 'N', 'mosaicus', 'hands', 'orbits', 'faces', 'corners', 'depths', 'D', 'study_row', 'source']
with open(os.path.join(out, 'catalogue.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=F, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
H = ['group', 'no.', 'name', 'm', 'N', 'Mosaicus', 'orbit set (representative)', 'faces by orbit', 'depths (first orbit = 1; 12 decimals)', 'D', 'source']
with open(os.path.join(out, 'catalogue.md'), 'w') as f:
    f.write('# Main catalogue of the Aequi (149 dice of the seven frame groups)\n\n')
    f.write('Mosaicus = Aequus Mosaicus (m ≥ 4 kinds of face). D = number among the book atoms. Depths in the order of the orbit set; source = file in study 2026-11-19-aequi-complete/data.\n\n')
    f.write('| ' + ' | '.join(H) + ' |\n|' + '---|' * len(H) + '\n')
    for r in rows:
        f.write('| %s | %d | %s | %d | %d | %s | %s | %s | %s | %s | %s |\n' % (r['group'], r['number'], r['name'], r['m'], r['N'],
                r['mosaicus'], r['orbits'], r['faces'], r['depths'], r['D'], r['source']))
json.dump(rows, open(os.path.join(out, 'catalogue.json'), 'w'), ensure_ascii=False, indent=0)
# names that rest on a convention not fixed by a settled name (listed for DICTO in the README)
def cases(labels):
    n = Counter()
    for l in labels:
        for f, k in parts(l).items(): n[f] += k
    one = len(labels) == len(set(labels)) and not any('+' in l for l in labels)
    c = []
    if n['O8'] == 8 and n['I12'] == 12 and 'O8+I12/20' not in labels: c.append('I from O8 + I12 in separate orbits')
    if n['C6'] == 6 and n['RT24'] == 24 and 'C6+RT24/30' not in labels: c.append('RT from C6 + RT24 in separate orbits')
    if n['I12'] == 12 and n['O8'] != 8: c.append('I12 without the 8 (I for 12 of the icosahedron faces)')
    if n['RT24'] and not (n['C6'] == 6 and n['RT24'] == 24): c.append('RT24 or its halves without C6 (RT for %d of the triacontahedron faces)' % n['RT24'])
    if n['O8'] == 4 and n['I12'] == 12: c.append('one tetrahedron with I12 (T + I, not a partial icosahedron)')
    if n['O8'] == 8 and len([l for l in labels if l.startswith('O8/4')]) == 2 and n['I12'] != 12: c.append('O from the two tetrahedra O8/4a + O8/4b')
    if n['C6'] == 6 and 0 < n['RT24'] < 24: c.append('C6 with half of RT24 (C + RT)')
    return c
byc = defaultdict(list)
for g in GROUPS:
    for d in sorted([d for d in dice if d['group'] == g], key=order):
        for c in cases(d['orbits']): byc[c].append(d['sid'])
name_of = {r['study_row']: '%s %d' % (r['group'], r['number']) for r in rows}
with open(os.path.join(out, 'convention-cases.md'), 'w') as f:
    f.write('# Names that rest on a convention not fixed by a settled name\n\n')
    for c, L in byc.items():
        print('case: %s: %d dice' % (c, len(L)))
        f.write('- %s (%d): %s\n' % (c, len(L), ', '.join(next(r['name'] for r in rows if r['study_row'] == s) for s in L)))
# checks
ok = True; msg = []
cnt = Counter(r['group'] for r in rows); want = {'Ih': 4, 'Oh': 4, 'Td': 3, 'Th': 47, 'T': 91}
if len(rows) != 149 or dict(cnt) != want: ok = False; msg.append('counts %s' % dict(cnt))
for g in GROUPS:
    if [r['number'] for r in rows if r['group'] == g] != list(range(1, want[g] + 1)): ok = False; msg.append('numbers not contiguous in ' + g)
if len(set(r['name'] for r in rows)) != 149: ok = False; msg.append('full names not unique')
for dn, g, labs, nm in SETTLED:
    hit = [r for r in rows if r['D'] == 'D%d' % dn]
    if len(hit) != 1 or hit[0]['short'] != nm: ok = False; msg.append('D%d %s not reproduced: %s' % (dn, nm, [h['short'] for h in hit]))
    else: print('settled D%d %s -> %s' % (dn, nm, hit[0]['name']))
mc = Counter(r['m'] for r in rows); print('by m', sorted(mc.items()), 'Mosaici', sum(r['mosaicus'] == 'yes' for r in rows))
if sum(r['mosaicus'] == 'yes' for r in rows) != 82: ok = False; msg.append('Mosaici count')
by = defaultdict(list)
for r in rows: by[r['short']].append('%s %d' % (r['group'], r['number']))
shared = {k: v for k, v in by.items() if len(v) > 1}
print('short names shared by more than one die: %d names, %d dice' % (len(shared), sum(len(v) for v in shared.values())))
for k, v in sorted(shared.items(), key=lambda kv: (-len(kv[1]), kv[0])): print('  %s: %s' % (k, ', '.join(v)))
print('single-initial names:', [r['name'] + ' [' + r['orbits'] + ']' for r in rows if r['solids'].count('+') == 0])
print('FINAL ok' if ok else 'FINAL FAIL: ' + '; '.join(msg))
