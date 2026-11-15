#!/usr/bin/env python3
"""Which candidates are the same solid? Canonical forms (translation + the 120 symmetries of the six-axis star) of: the flip-search
rank-3 candidates, the gnomon rank-3 surfaces, and tilers A, B; plus the number of distinct neighbours (+-lambda) of each, which counts
the patches in Grunbaum's 2010 patch-pair conjecture (Geombinatorics 19, p. 105). Usage: compare.py search6.json gnomon.json tile12.json cover6.json cover-gnomon.json"""
import sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from zsurf import *
G = Geo(6); syms = signed_perms(G)
s6, gn, t12, c6, cg = [json.load(open(p)) for p in sys.argv[1:6]]
def surf(faces): return {(tuple(f[0]), f[1], f[2]): f[3] for f in faces}
items = []
for i, c in enumerate(s6['candidates_rank_le_3']): items.append((f'flip{i}', surf(c['faces'])))
for i, f in enumerate(gn['rank_le_3_surfaces']): items.append((f'gnomon{i}', surf(f)))
keys = {}; out = {}
for name, S in items:
    k = canon(G, S, syms); keys.setdefault(k, []).append(name)
    info, _ = analyse(G, S); lam = face_pair_vectors(G, S, info)
    nb = len(set(tuple(v) for v in lam.values())) if lam else None
    out[name] = {'class': None, 'distinct_lambda': nb, 'volume3': volume3(G, S)}
for ci, (k, names) in enumerate(keys.items()):
    for nm in names: out[nm]['class'] = ci
tiles = {f'flip{r["index"]}': r.get('tiles') for r in t12['results']}
cov = {f'flip{r["index"]}': r.get('all_once') for r in c6}; cov.update({f'gnomon{r["index"]}': r.get('all_once') for r in cg})
for nm in out: out[nm]['exact_tiles'] = tiles.get(nm); out[nm]['covered_once_float'] = cov.get(nm)
for nm, v in out.items(): print(nm, v)
print('classes:', {ci: names for ci, (k, names) in enumerate(keys.items())})
json.dump(out, open('data/compare.json', 'w'), indent=1, default=str)
ok = out['flip0']['class'] != out['flip1']['class']
print('FINAL ok' if ok else 'FINAL FAIL: control (A and B distinct) not met')
