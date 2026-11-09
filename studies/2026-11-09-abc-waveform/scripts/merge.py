"""Merge the three scan shards: totals, word-set census, and the candidate list for followup.py.
Key check for the aim: does any design admit patches while excluding BOTH constant words SSSS and TTTT?"""
import json, glob, os, itertools
from collections import Counter
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
res = {}
for f in sorted(glob.glob(os.path.join(D, 'scan-K5-n3-P3-I3-shard*of3.json'))):
    for x in json.load(open(f)): res[(x['design'], x['mode'], x['mirror'])] = x
R = list(res.values()); nd = len({x['design'] for x in R})
print(f"designs {nd} (incl. control), runs {len(R)}")
print('VERDICTS (rule, mirrors, verdict):', sorted(Counter((x['mode'], x['mirror'], x['verdict'].split()[0]) for x in R).items()))
tilers = [x for x in R if x['words']]
print('TILING RUNS by word set:', sorted(Counter(('all16' if len(x['words']) == 16 else ','.join(x['words']) if len(x['words']) <= 2 else f"{len(x['words'])} words") for x in tilers).items()))
both = [x for x in tilers if 'SSSS' not in x['words'] and 'TTTT' not in x['words']]
print(f"runs that tile but exclude both SSSS and TTTT: {len(both)}", [(x['tag'], x['mode'], x['mirror'], x['words']) for x in both][:10])
odd = [x for x in tilers if 1 < len(x['words']) < 16]
for x in odd: print('RESTRICTED', x['tag'], x['mode'], x['mirror'], x['verdict'], 'admitted', x['words'])
cands = [x for x in R if x['verdict'] == 'CANDIDATE']
json.dump(cands, open(os.path.join(D, 'candidates.json'), 'w'))
print(f"candidates {len(cands)}:", [(x['tag'], x['mode'], x['mirror'], len(x['words'])) for x in cands])
ctrl = [x for x in R if x['design'] == 0]
ok = nd == 1944 and all(x['verdict'].startswith('PERIODIC') and len(x['words']) == 16 for x in ctrl)
print('FINAL ok' if ok else f'FINAL FAIL: designs {nd}, control {ctrl}')
