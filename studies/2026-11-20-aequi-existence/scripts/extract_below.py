# Part 2 of study 2026-11-20-aequi-existence: the 4404 dice below the frame groups (study 2026-11-19-aequi-complete,
# data/dice/*.json, every die whose full group is not one of Ih, I, Oh, O, Td, Th, T; prisms included).
# Each die's face directions are tested for opposite pairs (the set equals its negative): those are Corollary 3 and
# are only counted; the others are written out for the diameter certificate (existence.py), as kind 'below'.
# Cross-checks: 4553 dice, 149 in frame groups, 4404 below, each label in data/table.csv once; and a set has opposite
# pairs exactly when its full group contains the central inversion (Theorem A (b): the full group of the die is the
# symmetry group of its directions).
# usage: extract_below.py STUDIES_DIR out.jsonl
import json, sys, csv, glob, os, collections, importlib.util, numpy as np
S, out = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('g74', S + '/2026-11-19-aequi-complete/scripts/groups.py')
g74 = importlib.util.module_from_spec(spec); spec.loader.exec_module(g74)
DIRS = g74.DIRS; assert len(DIRS) == 74
# index of −x for every direction (the frames are centrally symmetric)
NEG = [int(np.argmin(np.abs(DIRS + x).max(1))) for x in DIRS]
assert all(np.abs(DIRS[NEG[i]] + DIRS[i]).max() < 1e-15 for i in range(74))
FRAME = {'Ih', 'I', 'Oh', 'O', 'Td', 'Th', 'T'}
INV = {'Ci', 'C2h', 'C4h', 'C6h', 'S6', 'S10', 'D2h', 'D4h', 'D6h', 'D8h', 'D10h', 'D3d', 'D5d', 'Th', 'Oh', 'Ih'}
labels = collections.Counter((r['label'], r['group']) for r in csv.DictReader(open(S + '/2026-11-19-aequi-complete/data/table.csv')))
files = sorted(glob.glob(S + '/2026-11-19-aequi-complete/data/dice/*.json'))
n_all = len(files); n_frame = 0; rows = []; cnt = collections.defaultdict(lambda: [0, 0]); mism = []
for f in files:
    d = json.load(open(f))
    assert labels[(d['label'], d['group'])] == 1, d['label']
    if d['group'] in FRAME: n_frame += 1; continue
    idx = d['face_directions']; assert len(idx) == d['N'] == len(set(idx)) == sum(d['orbit_sizes'])
    opp = set(NEG[i] for i in idx) == set(idx)
    if opp != (d['group'] in INV): mism.append(d['label'])
    cnt[d['group']][0 if opp else 1] += 1
    if not opp:
        rows.append(dict(kind='below', group=d['group'], name=os.path.basename(f)[:-5], label=d['label'], N=d['N'],
                         sizes=d['orbit_sizes'], dirs=idx))
with open(out, 'w') as fo:
    for r in rows: fo.write(json.dumps(r) + '\n')
print('dice', n_all, '| frame groups', n_frame, '| below', n_all - n_frame)
print('group: opposite pairs (Corollary 3), without (to test)')
for g in sorted(cnt, key=lambda g: (-sum(cnt[g]), g)): print('  %-5s %4d %4d' % (g, cnt[g][0], cnt[g][1]))
tot = [sum(v[0] for v in cnt.values()), sum(v[1] for v in cnt.values())]
print('  all   %4d %4d' % tuple(tot))
print('opposite pairs disagree with inversion in the group:', len(mism), mism[:5])
print('N of the sets to test: %d..%d' % (min(r['N'] for r in rows), max(r['N'] for r in rows)))
ok = n_all == 4553 and n_frame == 149 and n_all - n_frame == 4404 and not mism and sum(tot) == 4404 and len(rows) == tot[1]
print('FINAL ok' if ok else 'FINAL FAIL')
