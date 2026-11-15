#!/usr/bin/env python3
"""Part C2b: the k = 14 growth from GET by parallel zone layers (m <= 2), every surface with all zones = 14 streamed through the strong
filters (no coplanar adjacent faces, faces of each pair type balanced in outward sides, exact partial embedding); survivors kept and
classified up to the 120 symmetries of the six-axis star and translation. Usage: g14.py out.json budget_seconds"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gnomon12 as GN
from zsurf import signed_perms, canon
OUT = sys.argv[1]; BUD = float(sys.argv[2])
D = json.load(open(os.path.join(GN.HERE, '..', '..', '2026-11-15-grunbaum-k10', 'data', 'search6.json')))
starts = {}
for idx, nm in ((0, 'GET A'), (1, 'GET B'), (2, 'candidate 2')):
    starts[nm] = {(tuple(p), a, b): s for p, a, b, s in D['candidates_rank_le_3'][idx]['faces']}
st, hits = GN.general_search(starts, 14, 2, BUD)
print('GENERAL K=14 M=2', st, flush=True)
syms = signed_perms(GN.G); classes = {}
for h in hits:
    S = {(tuple(p), a, b): s for p, a, b, s in h['faces']}
    k = canon(GN.G, S, syms)
    classes.setdefault(k, h)
print(f'strong hits {len(hits)}, classes up to symmetry {len(classes)}', flush=True)
json.dump({'stats': st, 'strong_hits': len(hits), 'classes': list(classes.values())[:200], 'n_classes': len(classes)}, open(OUT, 'w'))
print('FINAL ok' if not GN.FAILS else 'FINAL FAIL')
