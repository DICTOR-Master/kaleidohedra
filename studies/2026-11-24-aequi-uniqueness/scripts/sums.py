# Consistency check of Theorem B against study 2026-11-20-aequi-alexandrov: every orbit set that FAILS Alexandrov's
# condition must have a nonzero vector sum of its face directions. The directions are unit vectors of the frame,
# stored in double precision (each coordinate within 1e-15 of the exact value), so a computed |sum| > 1e-9 proves the
# exact sum is nonzero (N <= 13 terms: total error < 13 * 3e-15).
# usage: python3 sums.py <alexandrov study dir> out.csv
import sys, os, json, csv
import numpy as np
SRC = sys.argv[1]
sys.path.insert(0, os.path.join(SRC, '..', '2026-11-19-aequi-complete', 'scripts'))
from groups import DIRS
assert np.abs(np.linalg.norm(DIRS, axis=1) - 1).max() < 1e-14
VR = list(csv.DictReader(open(os.path.join(SRC, 'data', 'verdicts.csv'))))
# verdicts.csv is keyed by (group, orbit families, N), which repeats for different orbit sets; a set counts as
# 'possibly failing' when any verdict row with its key fails (conservative).
from collections import defaultdict
KEY = defaultdict(set)
for r in VR: KEY[(r['group'], r['orbits'], int(r['N']))].add(r['verdict'].startswith('fails'))
rows = []
for line in open(os.path.join(SRC, 'data', 'sets.jsonl')):
    s = json.loads(line)
    idx = [i for o in s['orbits'] for i in o]
    nrm = float(np.linalg.norm(DIRS[idx].sum(0)))
    name = ' + '.join('+'.join(f) for f in s['fams'])
    k = KEY.get((s['group'], name, s['N']))
    rows.append([s['kind'], s['group'], name, s['N'], '?' if k is None else ('fails' if True in k else 'holds'), nrm])
with open(sys.argv[2], 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['kind', 'group', 'orbits', 'N', 'verdict', 'sum_norm']); w.writerows(rows)
fail = [r for r in rows if r[4].startswith('fails')]
unk = sum(r[4] == '?' for r in rows)
mn = min(r[5] for r in fail)
print(f'sets {len(rows)}, unmatched {unk}, possibly failing {len(fail)}, smallest |sum| among possibly failing {mn:.6g}, '
      f'sets with |sum| < 1e-9: {sum(r[5] < 1e-9 for r in rows)}')
nfv = sum(r['verdict'].startswith('fails') for r in VR)
print(f'verdict rows failing: {nfv}')
if unk == 0 and nfv == 87 and len(fail) >= 87 and mn > 1e-9: print('FINAL ok')
