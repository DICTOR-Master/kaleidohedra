# merge.py: sum the shard results of the hopeful-piece hunt (hunt.py K and P parts) into data/summary.json and a printed table.
# usage: merge.py <data dir>
import sys, json, glob, os
D = sys.argv[1]; out = {}; surv = []
for f in sorted(glob.glob(os.path.join(D, '*.json'))):
    if os.path.basename(f) in ('summary.json', 'rules.json'): continue
    r = json.load(open(f)); part = os.path.basename(f).split('_')[0]
    o = out.setdefault(part, dict(candidates=0, counts={}, shards=0)); o['shards'] += 1
    if 'results' in r:                                   # P
        for k, c in r['counts'].items():
            n, v = k.split('|'); o['counts'].setdefault(f'n={n}', {}); o['counts'][f'n={n}'][v] = o['counts'][f'n={n}'].get(v, 0) + c
            o['candidates'] += c
        surv += [['P', P] for n, P, v in r['results'] if v == 'SURVIVOR']
    else:
        o['candidates'] += r['candidates']
        for cl, cv in r['counts'].items():
            o['counts'].setdefault(cl, {})
            for v, c in cv.items(): o['counts'][cl][v] = o['counts'][cl].get(v, 0) + c
        surv += [[part] + s for s in r['survivors']]
json.dump(dict(parts=out, survivors=surv), open(os.path.join(D, 'summary.json'), 'w'), indent=1)
for part, o in out.items():
    print(f'== {part}: {o["candidates"]} candidates, {o["shards"]} shards')
    for cl, cv in sorted(o['counts'].items()): print(f'   {cl}: {dict(sorted(cv.items()))}')
print(f'SURVIVORS {len(surv)}'); [print('  ', s) for s in surv]
