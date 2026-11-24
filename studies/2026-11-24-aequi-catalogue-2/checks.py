# Checks for catalogue.csv (prints FINAL ok only if every check passes).
#  1 counts: 3 reserved + (5935 + 336 + 1375 + 1910 - 66 repeats) rows, Nos. 1233.. consecutive, each source die once
#  2 names: by the rule, distinct, every name decodes to exactly its own number; name_shown = "Name (No.N)"
#  3 order: the sort key (group order desc, group, m, N, corners, batch, index) is strictly increasing
#  4 certification: every source die has a certify record with the same label, status certified, or split box ok
#  5 congruence: no two catalogued dice congruent; each die left out congruent to one catalogued earlier; none congruent to a die of 2026-11-19-aequi-complete (4553)
#    or to any of the catalogued 1232; positive control: the dice that post2a.py set aside as congruent to
#    2026-11-19 dice must be found again by this test
#  6 row 95 of 2026-11-20-aequi-two-placements is catalogued already (picker no. 240)
import csv, glob, gzip, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

fails = []
def check(c, msg):
    print(('ok   ' if c else 'FAIL ') + msg)
    if not c: fails.append(msg)

rows = list(csv.DictReader(open(os.path.join(HERE, 'catalogue.csv'))))
batch = {b: load_batch(b) for b in BATCHES}
# 1 counts
check([int(r['No']) for r in rows] == list(range(1233, 1233 + len(rows))), 'Nos. consecutive from 1233 (last %s)' % rows[-1]['No'])
check(len(rows) == 3 + 9556 - 66, 'rows = 3 + 9556 - 66 = %d' % len(rows))
dupids = {(r['batch'], int(r['id'])) for r in csv.DictReader(open(os.path.join(HERE, 'duplicates.csv')))}
for b in BATCHES:
    ids = sorted([int(r['source_id']) for r in rows if r['source_batch'] == b] + [i for bb, i in dupids if bb == b])
    check(len(batch[b]) == EXPECT[b] and ids == list(range(EXPECT[b])), 'batch %s: %d dice, each catalogued once or left out as a repeat' % (b, EXPECT[b]))
res = [r for r in rows if r['source_batch'] == 'reserved']
check([(int(r['No']), r['group'], int(r['m']), int(r['N'])) for r in res] == [t[:4] for t in RESERVED]
      and [r['name'] for r in res] == ['Inimisa', 'Inimiyo', 'Inimigo'], 'Nos. 1233-1235 reserved: Inimisa, Inimiyo, Inimigo')
# 2 names
old_names = list(csv.DictReader(open(os.path.join(NUMB, 'names.csv'))))
check(all(r['name'] == rule(int(r['n'])) and r['name_shown'] == shown(int(r['n'])) for r in old_names) and len(old_names) == 1232,
      'rule reproduces all 1232 names and shown names of names.csv')
check(all(r['name'] == rule(int(r['No'])) for r in rows), 'names follow the rule')
check(all((mt := SHOWN_RE.match(r['name_shown'])) and mt.group(1) == r['name'] and mt.group(2) == r['No'] for r in rows),
      'name_shown is exactly "Name (No.N)"')
allnames = [r['name'] for r in old_names] + [r['name'] for r in rows]
check(len(set(allnames)) == len(allnames), 'all %d names distinct (with the 1232)' % len(allnames))
check(all(parses(r['name']) == [r['No']] for r in rows), 'every name has exactly one parse, its own number')
# 3 order and data agreement
keys = [sort_key(r['source_batch'], int(r['source_id']), batch[r['source_batch']][int(r['source_id'])]) for r in rows[3:]]
check(all(a < b for a, b in zip(keys, keys[1:])), 'order: group order desc, group, m, N, then corners, batch, index')
check(all((lambda d: (d['group'], int(d['m']), int(d['N'])) == (r['group'], int(r['m']), int(r['N'])))(batch[r['source_batch']][int(r['source_id'])])
          for r in rows[3:]), 'group, m, N agree with the source data')
check(all(d['group'] not in WITH_T for b in BATCHES for d in batch[b]),
      'no new die has a full group containing T (so none is one of the 1232 by group alone)')
# 4 certification
acc = {(a['study'], a['sid']): a for a in json.load(open(os.path.join(EXT, 'accidental2a.json')))}
for b in BATCHES:
    cert = {}
    for l in gzip.open(os.path.join(EXT, 'certify%s.jsonl.gz' % b), 'rt'):
        c = json.loads(l); cert[c['sid']] = c
    ok = len(cert) == len(batch[b])
    for i, d in enumerate(batch[b]):
        c = cert.get(i)
        lab = d['group'] + ': ' + ' + '.join(d['orbit_labels'])
        if not c or c['label'] != lab or int(c['N']) != int(d['N']): ok = False; continue
        if c['status'] == 'certified': continue
        a = acc.get((c['study'], i))
        if not (c['status'] == 'accidental' and a and a['split_krawczyk']['ok']): ok = False
    check(ok, 'batch %s: every die certified (labels match; split-box dice: split Krawczyk ok)' % b)

# 5 congruence. Scale-free signature of a die centred at the origin: depths d/min(d), Gram matrix of unit normals.
# Depths are grouped into levels (sorted; a new level where the gap exceeds 1e-7; checked: every gap between levels
# >= 1e-6 and every level narrower than 1e-9, so the levels are stable). For each face: its level, then the sorted
# multiset of (dot rounded to 1e-4, level) over all faces; the multiset of these rows is invariant under every
# orthogonal map (mirror images included) and relabelling of faces. Dots come from the finite set of direction
# pairs; each is checked to lie >= 1e-8 from a rounding boundary. Two dice are congruent candidates when the
# signatures agree AND the sorted depth vectors agree to 1e-6.
dup = list(csv.DictReader(open(os.path.join(HERE, 'duplicates.csv'))))
cat = {(r['source_batch'], int(r['source_id'])): int(r['No']) for r in rows[3:]}
newsig = {}; coll = 0
for r in rows[3:]:
    k = sig_new(batch[r['source_batch']][int(r['source_id'])]); coll += bool(find(newsig, k)); add(newsig, k, int(r['No']))
okd = True
for r in dup:
    b, i = r['batch'], int(r['id']); m = find(newsig, sig_new(batch[b][i]))
    kb, ki = r['kept_batch'], int(r['kept_id'])
    if (b, i) in cat or m != [int(r['kept_No'])] or cat.get((kb, ki)) != int(r['kept_No']) or BATCHES.index(kb) >= BATCHES.index(b): okd = False
check(okd and len(dup) == 66, 'the 66 left out are each congruent to exactly one catalogued die of an earlier batch')
check(len(cat) + len(dup) == 9556 and coll == 0, 'catalogued %d + left out %d = 9556; catalogued dice mutually non-congruent' % (len(cat), len(dup)))
oldsig = {}; nold = 0
for f in glob.glob(os.path.join(OLD, '*.json')):
    o = json.load(open(f)); k = sig(DIRS[[int(x) for x in o['face_directions']]],
                                    np.repeat([float(x) for x in o['depths_60_digits']], [int(x) for x in o['orbit_sizes']]))
    nold += bool(find(oldsig, k)); add(oldsig, k, o['file'])
check(nold == 0 and sum(map(len, oldsig.values())) == 4553, 'study 2026-11-19: 4553 dice, mutually non-congruent by this test')
hit = [(b, i) for b in BATCHES for i, d in enumerate(batch[b]) if find(oldsig, sig_new(d))]
check(not hit, 'no new die congruent to a die of study 2026-11-19-aequi-complete (%d hits)' % len(hit))
P = json.load(open(os.path.join(NUMB, 'src', 'dice.json')))
def sig_pick(e):
    U, dd = [], []
    for k, oi in enumerate(e['o']):
        for j in P['groups'][e['g']][oi]['dirs']: U.append(P['dirs'][j]); dd.append(e['d'][k])
    return sig(U, dd)
picksig = {}; npk = 0
for e in P['dice']:
    k = sig_pick(e); npk += bool(find(picksig, k)); add(picksig, k, e.get('num'))
check(npk == 0 and len(P['dice']) == 1232, 'the catalogued 1232: mutually non-congruent by this test')
hit = [(b, i) for b in BATCHES for i, d in enumerate(batch[b]) if find(picksig, sig_new(d))]
check(not hit, 'no new die congruent to any of the catalogued 1232 (%d hits)' % len(hit))
# positive control: the dice set aside by post2a.py as congruent to 2026-11-19 dice
for b in BATCHES:
    col = json.load(gzip.open(os.path.join(EXT, 'collected%s.json.gz' % b)))['dice']
    newids = {d['sid'] for d in batch[b]}
    aside = [d for d in col if d['centroid_at_origin'] and not d['face_transitive'] and d['group'] not in WITH_T
             and d['sid'] not in newids]
    rep = json.load(gzip.open(os.path.join(EXT, 'aequi%s.json.gz' % b)))['repeats_old']
    found = sum(bool(find(oldsig, sig_new(d))) for d in aside)
    check(len(aside) == len(rep) and found == len(aside), 'positive control %s: %d dice set aside, %d found again in 2026-11-19' % (b, len(aside), found))
check(stat['gmargin'] >= 1e-8 and stat['gap'] >= 1e-6 and stat['width'] < 1e-9,
      'signature stability: dot margin %.1e, smallest level gap %.1e, widest level %.1e' % (stat['gmargin'], stat['gap'], stat['width']))
# 6 row 95
cls = list(csv.DictReader(open(os.path.join(STUDIES, '2026-11-24-aequi-vacuus-scutoids', 'data', 'aequi_classification.csv'))))
r95 = [r for r in cls if r['record'].startswith('0095-Td-D12-D12p-24-RT24-RT24p-24')]
check(len(r95) == 1 and r95[0]['n'] == '240' and old_names[239]['name_shown'] == 'Niyoo (No.240)',
      'row 95 (Td: D12+D12′/24 + RT24+RT24′/24, N = 48) is already catalogued: Niyoo (No.240)')
print('FINAL ok' if not fails else 'FINAL FAIL: %d checks failed' % len(fails))
