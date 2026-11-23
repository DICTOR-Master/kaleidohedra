# Part 2(b): the wide-box re-search against the study-1 search (same sets): solutions per set, and each wide-box
# solution matched (depths to 1e-6) with the study-1 solution of the same set.  usage: compare2b.py
import json, glob, collections
W = [json.loads(L) for L in open('data/raw/sol-2b.jsonl')]
old = {}
for f in glob.glob('../2026-11-19-aequi-complete/data/raw/sol-*.jsonl'):
    for L in open(f):
        try: r = json.loads(L)
        except Exception: continue
        old[(r['cls'], r['m'], tuple(r['subset']))] = r
hist = collections.Counter(len(r['sols']) for r in W); same = 0; diff = []; missing_old = 0
for r in W:
    o = old.get((r['cls'], r['m'], tuple(r['subset'])))
    if o is None: missing_old += 1; continue
    ok = len(r['sols']) == len(o['sols']) and all(any(max(abs(a - b) for a, b in zip(x, y)) < 1e-6 for y in o['sols']) for x in r['sols'])
    same += ok
    if not ok: diff.append(dict(set=(r['cls'], r['m'], r['subset']), wide=r['sols'], old=o['sols']))
lo = min(min(x[1:]) for r in W for x in r['sols'] if len(x) > 1); hi = max(max(x[1:]) for r in W for x in r['sols'] if len(x) > 1)
print('sets', len(W), 'solutions per set', dict(hist), '| same single die as study 1:', same, '| differing:', len(diff), '| not in study-1 raw:', missing_old)
print('depth ratios of all solutions: %.4f .. %.4f (box e^-3 .. e^3 = 0.0498 .. 20.09)' % (lo, hi))
for d in diff[:10]: print(d)
json.dump(dict(hist=dict(hist), same=same, diff=diff), open('data/compare2b.json', 'w'), indent=1)
print('FINAL ok' if not diff and missing_old == 0 else 'FINAL: differences listed')
