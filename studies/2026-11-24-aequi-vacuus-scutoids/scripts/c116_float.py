"""Floating resin (27 Nov 2026; DICTO: "the resin method of exchange: fixed start and end points, floating until best alignment
synchronizes"). With Claude (Anthropic).
Start (C116, its canonical form) and end (Minana #377) are fixed shapes; the core FLOATS (any turn, mirror allowed). The resin settles:
each core face takes the Minana face it faces best (one-to-one: the assignment with the largest total cosine between paired face
directions, Hungarian method), then the core turns to fit that pairing best (Kabsch/Procrustes); repeat until nothing changes.
From many random starting turns, record every settled state: total cosine (how well it synchronizes) and neighbour pairs kept.
Question: does the best-synchronized state find the best alignment (144 of 174 kept, c116_orbitpairs.py) by itself?
No symmetry is imposed or used. Output data/c116/float.json."""
import os, sys, json
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial.transform import Rotation
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json')))
faces, mf, P = d['faces'], d['minana_faces'], np.array(d['P'])
C = []
for f in faces:
    X = P[f]; c = X.mean(0); n = np.linalg.svd(X - c)[2][2]
    C.append(n if n @ c > 0 else -n)
C = np.array(C)
Dm = A.build("aequus-377")
M = np.array([[float(x) for x in u] for u, c in Dm["planes"]]); M /= np.linalg.norm(M, axis=1)[:, None]
def adjset(fl): return {frozenset((a, b)) for a in range(60) for b in range(a + 1, 60) if len(set(fl[a]) & set(fl[b])) == 2}
A0, AM = adjset(faces), adjset(mf)
def kept(sig):
    iv = {v: k for k, v in sig.items()}; return len(A0 & {frozenset(iv[x] for x in e) for e in AM})
def settle(R):
    last = None
    for it in range(200):
        X = C @ R.T; r, c = linear_sum_assignment(-(X @ M.T)); sig = dict(zip(r.tolist(), c.tolist()))
        if sig == last: break
        last = sig
        U, _, Vt = np.linalg.svd(C.T @ M[c]); R = (U @ Vt).T          # best orthogonal map (turn or mirror-turn)
    X = C @ R.T; tot = float(np.sum(X * M[[sig[k] for k in range(60)]]))
    return sig, tot, it
rng = np.random.default_rng(27)
N = int(os.environ.get('NSTART', 4000)); states = {}
for s in range(N):
    R = Rotation.random(random_state=rng).as_matrix()
    if s % 2: R = R @ np.diag([1, 1, -1])
    sig, tot, it = settle(R)
    key = tuple(sig[k] for k in range(60))
    if key not in states: states[key] = dict(total_cos=round(tot, 6), kept=kept(sig), hits=0)
    states[key]['hits'] += 1
    if s % 500 == 0: print(f'PROGRESS {s / N:.2f}  distinct settled states {len(states)}', flush=True)
rows = sorted(states.items(), key=lambda kv: -kv[1]['total_cos'])
print('settled states:', len(rows), flush=True)
print('top 10 by synchronization (total cosine of 60):', flush=True)
for key, r in rows[:10]: print('  ', r, flush=True)
bk = max(r['kept'] for k, r in rows)
print('most neighbour pairs kept by any settled state:', bk, '; best possible (enumeration): 144', flush=True)
top = rows[0][1]
print(f"BEST-SYNCHRONIZED STATE keeps {top['kept']} of 174 (found from {top['hits']} of {N} starts)", flush=True)
from collections import Counter
print('kept counts over settled states:', sorted(Counter(r['kept'] for k, r in rows).items(), reverse=True)[:12], flush=True)
op = json.load(open(os.path.join(HERE, '../data/c116/onefloor.json')))['pairing']
best144 = tuple(int(op[str(k)]) for k in range(60))
print('the 144 pairing itself among settled states:', best144 in states, flush=True)
json.dump([dict(pairing=list(k), **r) for k, r in rows[:200]], open(os.path.join(HERE, '../data/c116/float.json'), 'w'))
print('FINAL ok' if rows else 'FINAL FAIL')
