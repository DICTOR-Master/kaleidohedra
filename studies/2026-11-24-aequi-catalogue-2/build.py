# Build catalogue.csv: Nos. 1233-1235 reserved for the three permutahedron duals, then the new certified Aequi
# of study 2026-11-24-aequi-certify-extend (Part 2(a) and the three caps batches) in the decided order.
# A die congruent to one of an earlier batch (batch order 2a, 2caps, 2caps2, 2caps3) is left out (duplicates.csv).
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

batch = {b: load_batch(b) for b in BATCHES}
seen, drop = {}, {}
for b in BATCHES:
    for i, d in enumerate(batch[b]):
        k = sig_new(d); m = find(seen, k)
        if m: drop[(b, i)] = m
        else: add(seen, k, (b, i))
rows = [dict(No=n, name=rule(n), name_shown=shown(n), group=g, m=m, N=N, source_batch='reserved',
             source_id='permutahedron dual %s (face-transitive; not in the certified batches)' % code)
        for n, g, m, N, code in RESERVED]
items = sorted((sort_key(b, i, d), b, i, d) for b in BATCHES for i, d in enumerate(batch[b]) if (b, i) not in drop)
no = {}
for n, (_, b, i, d) in enumerate(items, start=1236):
    rows.append(dict(No=n, name=rule(n), name_shown=shown(n), group=d['group'], m=int(d['m']), N=int(d['N']),
                     source_batch=b, source_id=i)); no[(b, i)] = n
F = ['No', 'name', 'name_shown', 'group', 'm', 'N', 'source_batch', 'source_id']
with open(os.path.join(HERE, 'catalogue.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=F); w.writeheader(); w.writerows(rows)
with open(os.path.join(HERE, 'duplicates.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['batch', 'id', 'group', 'm', 'N', 'kept_batch', 'kept_id', 'kept_No'])
    for (b, i), m in sorted(drop.items(), key=lambda t: (BATCHES.index(t[0][0]), t[0][1])):
        assert len(m) == 1; kb, ki = m[0]; d = batch[b][i]
        w.writerow([b, i, d['group'], d['m'], d['N'], kb, ki, no[(kb, ki)]])
print('rows', len(rows), 'last No', rows[-1]['No'], '| left out as repeats', len(drop))
