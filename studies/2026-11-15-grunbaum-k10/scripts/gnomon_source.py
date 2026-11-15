#!/usr/bin/env python3
"""Which k = 8 sources does the zone-layer gnomon turn into GET A, GET B (and flip2)? Re-runs gnomon.py's insertion on every class C(5)
source up to flip depth 3 and records, for each source, whether it is a D1/D2-type tiler and which target classes it reaches."""
import sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import gnomon_lib as gl
from zsurf import *
s6 = json.load(open('data/search6.json'))
targets = {}
for i in (0, 1, 2):
    S = {(tuple(f[0]), f[1], f[2]): f[3] for f in s6['candidates_rank_le_3'][i]['faces']}
    targets[gl.canon(gl.G6, S, gl.syms6)] = ['GET A', 'GET B', 'flip2'][i]
G5 = gl.G5; out = []
for d, S in gl.bfs5():
    info, _ = analyse(G5, S); lam = face_pair_vectors(G5, S, info)
    rk = rank_Q([list(v) for v in lam.values()]) if lam else -1
    hits = set()
    for cyc in gl.cycles(S):
        for side in (True, False):
            T = gl.insert(S, cyc, side)
            if T is None: continue
            k = gl.canon(gl.G6, T, gl.syms6)
            if k in targets: hits.add(targets[k])
    rec = {'depth': d, 'k8_face_pair_rank': rk, 'reaches': sorted(hits)}; out.append(rec); print(rec, flush=True)
json.dump(out, open('data/gnomon-sources.json', 'w'), indent=1)
print('FINAL ok' if len(out) > 0 else 'FINAL FAIL: no sources')
