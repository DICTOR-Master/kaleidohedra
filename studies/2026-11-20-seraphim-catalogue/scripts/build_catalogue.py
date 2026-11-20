# The numbered catalogue of the Seraphim: the 1083 two-icosahedron fair dice of study 2026-11-20-aequi-two-placements.
# usage: build_catalogue.py DICE_DIR OUT_DIR [WORD_LIST]
# Made like the Aequi catalogue (study 2026-11-20-aequi-catalogue, scripts/build_catalogue.py), with the second
# icosahedron placement (B, a quarter turn about z from A) added:
# numbering within each group, groups in the order Oh, O, Td, Th, T; inside a group by m, then N, then the orbit families
# in the order C6, O8, RD12, D12, D12', I12, I12', RT24, RT24' (each die's sorted list of family ranks, compared word by
# word; a joined orbit counts with all its families), then the placement of a split orbit (the orbit whose representative
# has fewer minus signs first), last the study's row number (checked never needed).
import json, sys, os, glob, csv, re
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_EVEN
dice_dir, out = sys.argv[1], sys.argv[2]
P = '′'
GROUPS = ['Oh', 'O', 'Td', 'Th', 'T']
WANT = {'Oh': 53, 'O': 31, 'Td': 91, 'Th': 168, 'T': 740}
FAM = ['C6', 'O8', 'RD12', 'D12', 'D12' + P, 'I12', 'I12' + P, 'RT24', 'RT24' + P]
INIT_ORDER = ['T', 'C', 'O', 'RD', 'D', 'D' + P, 'I', 'I' + P, 'RT', 'RT' + P]   # by face count 4, 6, 8, 12, 12, 20, 30; primed after unprimed
SOLID = {'T': 'tetrahedron', 'C': 'cube', 'O': 'octahedron', 'RD': 'rhombic dodecahedron', 'D': 'dodecahedron',
         'I': 'icosahedron', 'RT': 'rhombic triacontahedron'}
def solid(x):
    return SOLID[x.rstrip(P)] + (' (second placement)' if x.endswith(P) else '')
def size(f):
    return int(re.sub(r'[^0-9]', '', f))
def parts(label):
    """orbit label -> {family: number of directions}. 'D12+D12′/24' -> {D12: 12, D12′: 12};
    'RT24+RT24′/24a' -> {RT24: 12, RT24′: 12}; 'RT24′/12b' -> {RT24′: 12}; 'O8/4a' -> {O8: 4}."""
    m = re.fullmatch(r'([A-Z0-9+′]+?)(?:/(\d+)[ab]?)?', label)
    fams = m.group(1).split('+'); k = int(m.group(2)) if m.group(2) else None
    tot = sum(size(f) for f in fams)
    if k is None or k == tot: return {f: size(f) for f in fams}
    return {f: size(f) * k // tot for f in fams}
def counts(labels):
    n = Counter()
    for l in labels:
        for f, k in parts(l).items(): n[f] += k
    return n
def initial_set(labels):
    """The Aequi rule for each placement: the icosahedron's 20 (O8 + I12 of that placement) is I or I′ whenever all its
    directions are faces, the triacontahedron's 30 (C6 + RT24 of that placement) is RT or RT′ likewise; the 8 and the 6
    are shared by the two placements and are absorbed by every complete solid that uses them. Otherwise each orbit names
    its own source: C6 C, O8 O, O8/4 T, RD12 RD, D12 D, I12 I, RT24 or a half of it RT (primed for placement B)."""
    n = counts(labels); got = set(); usedO = usedC = False
    for p in ('', P):
        if n['O8'] == 8 and n['I12' + p] == 12: got.add('I' + p); n['I12' + p] = 0; usedO = True
        if n['C6'] == 6 and n['RT24' + p] == 24: got.add('RT' + p); n['RT24' + p] = 0; usedC = True
    if n['C6'] and not usedC: got.add('C')
    if n['O8'] == 8 and not usedO: got.add('O')
    elif n['O8'] == 4: got.add('T')
    if n['RD12']: got.add('RD')
    for p in ('', P):
        if n['D12' + p]: got.add('D' + p)
        if n['I12' + p]: got.add('I' + p)
        if n['RT24' + p]: got.add('RT' + p)
    return got
def swap(got):
    return {x[:-1] if x.endswith(P) else (x + P if x in ('D', 'I', 'RT') else x) for x in got}
def bits(got):
    return tuple(int(x in got) for x in INIT_ORDER)
def canonical(got):
    """of the die's two quarter-turned positions, the one in which the first solid (in initials order) that lies in one
    placement only is unprimed: the larger presence word over INIT_ORDER."""
    s = swap(got)
    return (got, False) if bits(got) >= bits(s) else (s, True)
def initials(got):
    seq = [x for x in INIT_ORDER if x in got]
    plain = ''.join(x.rstrip(P) for x in seq)
    if 'DIRT' in plain: return '·'.join(seq)     # DICTO 20 Nov (Aequi): dots where the initials would spell a word
    return ''.join(seq)
def famkey(labels):
    return sorted(tuple(sorted(FAM.index(f) for f in parts(l))) for l in labels)
def repkey(d):
    return sorted((tuple(sorted(FAM.index(f) for f in parts(l))), r.count('-')) for l, r in zip(d['orbits'], d['orbit_representatives']))
def order(d):
    return (d['m'], d['N'], famkey(d['orbits']), repkey(d), d['sid'])
def d12(s):
    return str(Decimal(s).quantize(Decimal('1e-12'), rounding=ROUND_HALF_EVEN))
dice = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(dice_dir, '*.json')))]
rows = []; turned = []; ties = 0
for g in GROUPS:
    L = sorted([d for d in dice if d['group'] == g], key=order)
    ties += sum(1 for a, b in zip(L, L[1:]) if order(a)[:4] == order(b)[:4])
    for i, d in enumerate(L, 1):
        got, t = canonical(initial_set(d['orbits']))
        if t: turned.append(d['sid'])
        ini = initials(got)
        rows.append(dict(group=g, number=i, name='Seraph %s-%d, %s %d' % (ini, d['N'], g, i), short='%s-%d' % (ini, d['N']),
            initials=ini, solids=' + '.join(solid(x) for x in INIT_ORDER if x in got), m=d['m'], N=d['N'],
            mosaicus='yes' if d['m'] >= 4 else 'no', hands=d['hands'], named_turned='yes' if t else 'no',
            orbits=' + '.join('%s %s' % (l, r) for l, r in zip(d['orbits'], d['orbit_representatives'])),
            faces='; '.join(d['faces_by_orbit']), corners=d['corners'],
            depths='; '.join(d12(x) for x in d['depths_60_digits']),
            study_row=d['sid'], source='dice/' + os.path.basename(d['file'])))
F = ['group', 'number', 'name', 'initials', 'solids', 'm', 'N', 'mosaicus', 'hands', 'named_turned', 'orbits', 'faces', 'corners', 'depths', 'study_row', 'source']
with open(os.path.join(out, 'catalogue.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=F, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
H = ['group', 'no.', 'name', 'm', 'N', 'Mosaicus', 'hands', 'orbit set (representative)', 'faces by orbit', 'depths (first orbit = 1; 12 decimals)', 'source']
with open(os.path.join(out, 'catalogue.md'), 'w') as f:
    f.write('# Catalogue of the Seraphim (1083 fair dice on the axes of the cube and both icosahedra)\n\n')
    f.write('Mosaicus = Seraph Mosaicus (m ≥ 4 kinds of face). Orbit labels as in the source study (primed = second icosahedron placement); '
            'a name marked † is read from the quarter-turned position (primes swapped), see the README. Depths in the order of the orbit set; '
            'source = file in study 2026-11-20-aequi-two-placements/data.\n\n')
    f.write('| ' + ' | '.join(H) + ' |\n|' + '---|' * len(H) + '\n')
    for r in rows:
        f.write('| %s | %d | %s%s | %d | %d | %s | %s | %s | %s | %s | %s |\n' % (r['group'], r['number'], r['name'], ' †' if r['named_turned'] == 'yes' else '',
                r['m'], r['N'], r['mosaicus'], 'two' if r['hands'].startswith('two') else 'one', r['orbits'], r['faces'], r['depths'], r['source']))
json.dump(rows, open(os.path.join(out, 'catalogue.json'), 'w'), ensure_ascii=False, indent=0)
# names that rest on a convention not fixed by the Aequi catalogue (listed for DICTO in the README)
def cases(d):
    n = counts(d['orbits']); labels = d['orbits']; c = []
    if n['O8'] == 8 and n['I12'] == 12 and n['I12' + P] == 12: c.append('O8 shared by both complete icosahedra (I and I′)')
    if n['C6'] == 6 and n['RT24'] == 24 and n['RT24' + P] == 24: c.append('C6 shared by both complete triacontahedra (RT and RT′)')
    if any('+' in l for l in labels): c.append('an orbit joining the two placements (named by both, e.g. D12+D12′/24 as D D′)')
    return c
byc = defaultdict(list)
for r, d in ((r, next(x for x in dice if x['sid'] == r['study_row'])) for r in rows):
    for c in cases(d): byc[c].append(r['name'])
with open(os.path.join(out, 'convention-cases.md'), 'w') as f:
    f.write('# Names that rest on a convention not fixed by the Aequi catalogue\n\n')
    for c, L in byc.items():
        print('case: %s: %d dice' % (c, len(L)))
        f.write('- %s (%d): %s\n' % (c, len(L), ', '.join(L)))
    f.write('- named from the quarter-turned position (%d): %s\n' % (len(turned), ', '.join(r['name'] for r in rows if r['named_turned'] == 'yes')))
# checks
ok = True; msg = []
cnt = Counter(r['group'] for r in rows)
if len(rows) != 1083 or dict(cnt) != WANT: ok = False; msg.append('counts %s' % dict(cnt))
for g in GROUPS:
    if [r['number'] for r in rows if r['group'] == g] != list(range(1, WANT[g] + 1)): ok = False; msg.append('numbers not contiguous in ' + g)
if len(set(r['name'] for r in rows)) != 1083: ok = False; msg.append('full names not unique')
if ties: ok = False; msg.append('%d ties after the placement key' % ties)
print('ties after the placement key (study row needed):', ties)
mc = Counter(r['m'] for r in rows); nm = sum(r['mosaicus'] == 'yes' for r in rows)
print('by m', sorted(mc.items()), 'Mosaici', nm)
if [mc[k] for k in range(2, 12)] != [30, 88, 167, 228, 234, 181, 103, 41, 10, 1] or nm != 965: ok = False; msg.append('m counts')
hc = Counter((r['group'], r['hands'].startswith('two')) for r in rows); print('hands', sorted(hc.items()))
if any(two != (g in ('O', 'T')) for g, two in hc): ok = False; msg.append('hands not as the groups')
print('named from the quarter-turned position:', len(turned))
by = defaultdict(list)
for r in rows: by[r['short']].append('%s %d' % (r['group'], r['number']))
shared = {k: v for k, v in by.items() if len(v) > 1}
print('short names shared by more than one die: %d names, %d dice' % (len(shared), sum(len(v) for v in shared.values())))
cross = {k: v for k, v in shared.items() if len(set(x.split()[0] for x in v)) > 1}
print('  of which across groups: %d' % len(cross))
for k, v in sorted(shared.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:15]: print('  %s: %s' % (k, ', '.join(v)))
print('dotted names:', sum('·' in r['initials'] for r in rows))
# other dictionary words in the undotted initials (primes dropped), length >= 3, for DICTO
try:
    W = {w.strip().upper() for w in open(sys.argv[3] if len(sys.argv) > 3 else '/usr/share/dict/words') if w.strip().isalpha() and w.strip().islower() and len(w.strip()) >= 3}
except OSError: W = set()
words = Counter()
for r in rows:
    s = r['initials'].replace(P, '').replace('·', '')
    if '·' in r['initials']: continue
    for i in range(len(s)):
        for j in range(i + 3, len(s) + 1):
            if s[i:j] in W: words[s[i:j]] += 1
print('words in undotted initials:', sorted(words.items(), key=lambda kv: -kv[1]))
print('FINAL ok' if ok else 'FINAL FAIL: ' + '; '.join(msg))
