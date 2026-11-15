"""Event counts restricted to steps whose two frames both pass every check (Euler, and triple formulas where all junctions are
triple). Usage: python clean_steps.py SERIES_PREFIX  (e.g. results/plates/plates_series_muller2016_1)"""
import json, sys
from collections import Counter, defaultdict
from eventlog import Tiling, check_tiling
P = sys.argv[1]
frames = [Tiling.from_json(l) for l in open(P + '_frames.jsonl')]
good = {F.t: check_tiling(F)['ok'] for F in frames}
rows = json.load(open(P + '_events.json'))
steps = list(zip([F.t for F in frames], [F.t for F in frames][1:]))
clean = {(a, b) for a, b in steps if good[a] and good[b]}
c, per = Counter(), defaultdict(Counter)
for r in rows:
    if (r['t0'], r['t1']) in clean:
        c[r['type']] += 1; b = int((r['t0'] - 1e-9) // 100) * 100; per[f'{b}-{b + 100} Ma'][r['type']] += 1
out = dict(frames=len(frames), frames_ok=sum(good.values()), steps=len(steps), clean_steps=len(clean),
           clean_counts=dict(c), clean_per100={k: dict(v) for k, v in sorted(per.items())},
           clean_clumps=dict(Counter(r['pattern'] for r in rows if (r['t0'], r['t1']) in clean and r['type'] == 'clump')))
print(json.dumps(out, indent=1)); json.dump(out, open(P + '_clean.json', 'w'), indent=1)
