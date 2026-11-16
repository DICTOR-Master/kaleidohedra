"""Control 4 check (job sun-tilt-poly): each sweep must give exactly the #104 h-vector counts and pass every frame."""
import json, sys
R = sys.argv[1]
want = {'red': {'birth': 116, 'swap': 366, 'death': 116}, 'trunc120': {'birth': 716, 'swap': 966, 'death': 716},
        'bitruncated': {'birth': 716, 'swap': 2166, 'death': 716}}
n = 0
for st, w in want.items():
    for sd in (13, 17, 19):
        try:
            r = json.load(open(f'{R}/sweep_{st}_{sd}.json')); s = r['steps']['1']
            good = s['counts'] == w and s['ok'] is True
            print(st, sd, s['counts'], 'frames ok', s['ok'], 'negative control caught', r.get('neg_control_caught'), 'MATCH' if good else 'DIFFERS'); n += good
        except Exception as e:
            print(st, sd, 'missing', e)
print('MATCH', n)
