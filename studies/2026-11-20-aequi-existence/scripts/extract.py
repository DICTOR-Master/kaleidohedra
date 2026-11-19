# List the orbit sets to test (study 2026-11-20-aequi-existence).
#   main  : the 94 Td and T dice of the main catalogue (study 2026-11-20-aequi-catalogue, catalogue.csv, with the
#           face directions from the dice files of study 2026-11-19-aequi-complete);
#   two   : the 31 O, 91 Td and 740 T dice of study 2026-11-20-aequi-two-placements (data/aequi.json);
#   fail / hold / ctrl : the 87 failing and 232 holding polar sets and the 50 solved controls of study
#           2026-11-20-aequi-alexandrov (data/alex.jsonl), as controls.
# Every direction is written as an index into the 122-direction list of study 2026-11-20-aequi-two-placements
# (groups.py), whose first 74 are the 74 directions of study 2026-11-19-aequi-complete (checked here).
# usage: extract.py STUDIES_DIR out.jsonl
import json, sys, csv, os, importlib.util, numpy as np
S, out = sys.argv[1], sys.argv[2]
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m
g74 = load(S + '/2026-11-19-aequi-complete/scripts/groups.py', 'g74')
g122 = load(S + '/2026-11-20-aequi-two-placements/scripts/groups.py', 'g122')
assert len(g74.DIRS) == 74 and len(g122.DIRS) == 122
assert np.abs(g74.DIRS - g122.DIRS[:74]).max() < 1e-15 and list(g74.DFAM) == list(g122.DFAM[:74])
rows = []
for r in csv.DictReader(open(S + '/2026-11-20-aequi-catalogue/data/catalogue.csv')):
    if r['group'] not in ('Td', 'T'): continue
    d = json.load(open(S + '/2026-11-19-aequi-complete/data/' + r['source']))
    rows.append(dict(kind='main', group=r['group'], name=r['name'], label=d['label'], N=d['N'],
                     sizes=d['orbit_sizes'], dirs=d['face_directions']))
for d in json.load(open(S + '/2026-11-20-aequi-two-placements/data/aequi.json')):
    if d['group'] not in ('O', 'Td', 'T'): continue
    rows.append(dict(kind='two', group=d['group'], name='two-placements sid %d' % d['sid'], label=d['label'], N=d['N'],
                     sizes=d['orbit_sizes'], dirs=d['face_directions']))
cnt = {}
for L in open(S + '/2026-11-20-aequi-alexandrov/data/alex.jsonl'):
    a = json.loads(L)
    k = 'ctrl' if a['kind'] == 'control' else 'fail' if a['verdict'].startswith('fails') else 'hold'
    cnt[k] = cnt.get(k, 0) + 1
    rows.append(dict(kind=k, group=a['group'], name='alexandrov %s cls %d subset %s' % (a['kind'], a['cls'], a['subset']),
                     label=' + '.join('+'.join(f) for f in a['fams']), N=a['N'], sizes=a['sizes'], dirs=None,
                     cls=a['cls'], m=a['m'], subset=a['subset'], alex_g=a['g'], alex_verdict=a['verdict']))
# the Alexandrov study stores orbit indices of the study's classes; recover the directions from its sets file
sets = {}
for L in open(S + '/2026-11-20-aequi-alexandrov/data/sets.jsonl'):
    a = json.loads(L); sets[(a['cls'], a['m'], tuple(a['subset']))] = [j for O in a['orbits'] for j in O]
for r in rows:
    if r['dirs'] is None: r['dirs'] = sets[(r['cls'], r['m'], tuple(r['subset']))]
    assert len(r['dirs']) == r['N'] == sum(r['sizes']) == len(set(r['dirs']))
by = {}
for r in rows: by[(r['kind'], r['group'] if r['kind'] in ('main', 'two') else '')] = by.get((r['kind'], r['group'] if r['kind'] in ('main', 'two') else ''), 0) + 1
with open(out, 'w') as fo:
    for r in rows: fo.write(json.dumps(r) + '\n')
print(sorted(by.items()))
ok = by.get(('main', 'Td')) == 3 and by.get(('main', 'T')) == 91 and by.get(('two', 'O')) == 31 and by.get(('two', 'Td')) == 91 \
     and by.get(('two', 'T')) == 740 and cnt == {'fail': 87, 'hold': 232, 'ctrl': 50}
print('FINAL ok' if ok else 'FINAL FAIL: counts')
