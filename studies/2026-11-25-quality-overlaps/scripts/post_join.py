"""Join the 60 open candidate dice with the exact coincidences of study 2026-11-25-stellation-cycle (Theorem 8: the 42 station dice,
depth ratio proved exact; and its list of dice with two orbits of one axis type at equal depth). -> data/candidates.json"""
import gzip, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
S = json.load(open(os.path.join(HERE, '..', 'data', 'aequi-summary.json')))
E42 = json.load(open(os.path.join(ST, '2026-11-25-stellation-cycle', 'data', 'exact42.json')))
A = json.load(open(os.path.join(ST, '2026-11-25-stellation-cycle', 'data', 'aequi.json')))
lab42 = {x['label'] for x in E42}; labeq = {x[2] for x in A['equal_depth_dice']}
D = {(o['part'], o['sid']): o for o in map(json.loads, gzip.open(os.path.join(HERE, '..', 'data', 'aequi-overlaps.jsonl.gz'), 'rt'))}
out = []
for c in S['candidates_open']:
    o = D[(c['part'], c['sid'])]
    out.append(dict(part=c['part'], sid=c['sid'], label=c['label'], No=c.get('No'), RV_proved=o['RV'], resonus=o['resonus'],
                    in_theorem8=c['label'] in lab42, in_equal_depth_list=c['label'] in labeq, n_unresolved=c['n_unresolved'],
                    ratios=sorted({u[4][:22] for u in c['unresolved']})))
json.dump(out, open(os.path.join(HERE, '..', 'data', 'candidates.json'), 'w'), indent=1, ensure_ascii=False)
print('candidates', len(out), '| in Theorem 8 list', sum(x['in_theorem8'] for x in out), '| in equal-depth list', sum(x['in_equal_depth_list'] for x in out),
      '| neither', sum(not x['in_theorem8'] and not x['in_equal_depth_list'] for x in out), '| with RV_proved = 0', sum(x['RV_proved'] == 0 for x in out))
for x in out:
    if not x['in_theorem8'] and not x['in_equal_depth_list']: print('NEITHER', x['part'], x['sid'], x['label'], x['ratios'])
print('ratios seen', sorted({r for x in out for r in x['ratios']}))
print('FINAL ok' if len(out) == len(S['candidates_open']) and out else 'FINAL FAIL')
