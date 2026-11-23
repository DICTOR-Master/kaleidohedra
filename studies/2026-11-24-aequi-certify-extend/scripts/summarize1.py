# Part 1 summary tables from data/certify-pass1.jsonl, data/accidental.json, data/structural.json
import json, collections, math, csv
R = [json.loads(L) for L in open('data/certify-pass1.jsonl')]
A = {(o['study'], o['sid']): o for o in json.load(open('data/accidental.json'))}
S = json.load(open('data/structural.json'))
rows = []
for r in sorted(R, key=lambda r: (r['study'], r['sid'])):
    a = A.get((r['study'], r['sid']))
    if a:
        st = 'certified (split box)' if a['split_krawczyk']['ok'] and a['tight']['ok'] else 'FAIL'
        wide = a['split_krawczyk']['r']; tr = None
    else:
        st = 'certified' if r['status'] == 'certified' else r['status']; wide = r['wide']['r'] if r.get('wide') else None; tr = r.get('type_radius')
    rows.append(dict(study=r['study'], row=r['sid'], label=r['label'], group=r['group'], m=r['m'], N=r['N'], status=st,
                     uniqueness_halfwidth=wide, type_radius=tr, tight_halfwidth=1e-40, multi_plane_corners=r.get('n_multi_corners', 0),
                     symmetry_ok=r['symmetry_ok']))
with open('data/certify-table.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
c = collections.Counter(x['status'] for x in rows)
L = ['| study | group | dice | certified | split box | failed | smallest uniqueness half-width | median |', '|---|---|---|---|---|---|---|---|']
for st in ['2026-11-19-aequi-complete', '2026-11-20-aequi-two-placements']:
    for g in ['Ih', 'Oh', 'O', 'Td', 'Th', 'T']:
        X = [x for x in rows if x['study'] == st and x['group'] == g]
        if not X: continue
        ws = sorted(x['uniqueness_halfwidth'] for x in X)
        L.append('| %s | %s | %d | %d | %d | %d | %.1e | %.1e |' % (st[:10], g, len(X), sum(x['status'] == 'certified' for x in X),
                 sum(x['status'] == 'certified (split box)' for x in X), sum('FAIL' in x['status'] or x['status'] not in ('certified', 'certified (split box)') for x in X), ws[0], ws[len(ws) // 2]))
L.append('| all | | %d | %d | %d | %d | | |' % (len(rows), c['certified'], c['certified (split box)'], len(rows) - c['certified'] - c['certified (split box)']))
hist = collections.Counter('1e-%d' % round(-math.log10(x['uniqueness_halfwidth'])) if x['uniqueness_halfwidth'] else 'none' for x in rows)
L.append(''); L.append('Uniqueness half-width (nearest power of ten): ' + ', '.join('%s: %d' % kv for kv in sorted(hist.items(), key=lambda kv: -float(kv[0]))))
L.append('Dice with corners where four or more planes meet: %d (structural, proved exactly: %d dice, %d distinct checks, %d failures; accidental: 3)' % (
    sum(1 for x in rows if x['multi_plane_corners']), S['dice_with_structural_corners'], S['distinct_checks'], S['failures']))
open('data/certify-summary.md', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
