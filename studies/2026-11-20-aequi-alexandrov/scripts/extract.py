# List the orbit sets to test: the 319 polar orbit sets of study 2026-11-19-aequi-complete with no fair die about the
# frame centre in its search box, and a control of 50 polar orbit sets where that search found one (spread evenly over
# the solved polar records in file order).
# usage: extract.py ../../2026-11-19-aequi-complete out.jsonl
import json, sys
src, out = sys.argv[1], sys.argv[2]
cls = json.load(open(src + '/data/classes.json'))
recs = {}
for f in ['sol-big.jsonl', 'sol-node.jsonl']:
    for L in open(src + '/data/raw/' + f):
        r = json.loads(L); recs[(r['cls'], r['m'], tuple(r['subset']))] = r
plan = {tuple(p) for p in json.load(open(src + '/data/plan.json'))}
none, solved = [], []
for (ci, m, S), r in sorted(recs.items()):
    if (ci, m) not in plan or not cls[ci]['polar']: continue
    orbs = cls[ci]['orbits']
    row = dict(cls=ci, group=cls[ci]['name'], m=m, subset=list(S), orbits=[orbs[i] for i in S], N=r['N'],
               fams=r['fams'], study_sols=r['sols'])
    (solved if r['sols'] else none).append(row)
step = len(solved) / 50
ctrl = [solved[int(i * step)] for i in range(50)]
with open(out, 'w') as fo:
    for r in none: r['kind'] = 'nosol'; fo.write(json.dumps(r) + '\n')
    for r in ctrl: r['kind'] = 'control'; fo.write(json.dumps(r) + '\n')
print('polar sets with no die in the box', len(none), '| solved polar sets', len(solved), '| controls', len(ctrl))
print('FINAL ok' if len(none) == 319 and len(ctrl) == 50 else 'FINAL FAIL: expected 319 and 50')
