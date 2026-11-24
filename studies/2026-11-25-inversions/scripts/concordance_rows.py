"""Append this study's settled items to concordance.json gaps.waiting and its new open gaps to gaps.loose (indent=2, ensure_ascii=False)."""
import json, os, sys
P = os.path.expanduser('~/k-research/papers/dicto-concordance/concordance.json')
D = json.load(open(P)); W = D['gaps']['waiting']; L = D['gaps']['loose']
keysW = list(W[-1].keys()); keysL = list(L[-1].keys())
S = 'studies/2026-11-25-inversions'
rows = json.load(open(sys.argv[1]))
done = {(r.get('study'), r.get('result')) for r in W}
for r in rows['waiting']:
    r = dict(date='2026-11-25', study=S, **r); assert list(r.keys()) == keysW or set(r.keys()) == set(keysW), r.keys()
    if (r['study'], r['result']) not in done: W.append({k: r[k] for k in keysW})
doneL = {(r.get('src'), r.get('what')) for r in L}
for r in rows['loose']:
    r = dict(src='study 2026-11-25-inversions', **r); assert set(r.keys()) == set(keysL)
    if (r['src'], r['what']) not in doneL: L.append({k: r[k] for k in keysL})
json.dump(D, open(P, 'w'), indent=2, ensure_ascii=False)
print('waiting', len(W), 'loose', len(L))
