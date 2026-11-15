"""Counts in fixed age windows from a finished run (step 1 events + Lmin 0 frames), for comparing models over a common window.
Light post-processing (JSON only). Usage: python window.py RESULTS_DIR MODEL_RULE [windows like 0-230,230-1000] -> prints JSON"""
import sys, os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts')); sys.path.insert(0, HERE)
from eventlog import Tiling
from swaps import swap_list, persistent

d, mr = sys.argv[1], sys.argv[2]
wins = [tuple(int(x) for x in w.split('-')) for w in (sys.argv[3] if len(sys.argv) > 3 else '0-100,100-200,200-230,0-230').split(',')]
lines = open(os.path.join(d, f'frames_{mr}_L0.jsonl')).read().splitlines()
fr = [Tiling.from_json(l) for l in lines]
lens = [{tuple(p.split('|')): v for p, v in json.loads(l).get('lengths', {}).items()} for l in lines]
rows = json.load(open(os.path.join(d, f'events_{mr}_L0.json')))
sw = swap_list(fr, rows)
out = {}
for lo, hi in wins:
    inw = lambda t0: lo < t0 <= hi
    c = Counter(r['type'] for r in rows if inw(r['t0']))
    s = [x for x in sw if inw(fr[x['iA']].t)]
    p = {f'k{k}_l{l}': persistent(fr, s, k, l, lens)[0] for k in (1, 5) for l in (0, 150)}
    out[f'{lo}-{hi}'] = dict(counts=dict(c), persistent_swaps=p, plates_end=len(fr[[f.t for f in fr].index(lo)].cells) if lo in [f.t for f in fr] else None)
print(json.dumps({mr: out}))
