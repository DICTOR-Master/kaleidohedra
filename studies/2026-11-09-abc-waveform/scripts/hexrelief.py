"""The literal reading of DICTO's wave: a relief ONLY on the top/underside surface (the hexagon of Narcissus), reciprocal underneath.
Relief = a height level 0/1/2 (trough / middle / crest) at each of the 6 hexagon corners, the corners being the B and C seat points
round the piece's own seat A; across an interface the two reliefs must be complementary (crest into trough: levels sum to 2).
Every relief up to the symmetry of N, mirror copies yes/no: which stacking words of K slabs admit a filling of the n-patch?
Claim tested (the pair-isolation lemma): the admitted words are exactly all words over the set of admitted single bits, because a
hexagon contact joins one down-N and one up-N and neither has a second hexagon.
Usage: hexrelief.py K n"""
import sys, os, itertools, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave_lib as W
t0 = time.time(); K, NP = int(sys.argv[1]), int(sys.argv[2])
HEX = [i for i, f in enumerate(W.BF) if len(f[2]) == 6][0]
S_ = {''.join(w): W.Structure(''.join(w), NP) for w in itertools.product('ST', repeat=K - 1)}
def sigs(S, rel):
    out = []
    for i, Q in enumerate(S.Ps):
        si = []
        for k, (R, t, det, inv) in enumerate(S.pl[i]):
            sk = []
            for fi, (u, c, idx) in enumerate(S.wf[i]):
                if len(idx) != 6: sk.append(frozenset()); continue
                lv = {tuple(np.round(Q[x], 5)): rel[inv[x]] for x in idx}
                up = u[2] > 0   # hexagon on top of this piece -> show levels, below -> show complements
                sk.append(frozenset((p, v if up else 2 - v) for p, v in lv.items()))
            si.append(sk)
        out.append(si)
    return out
SR = W.SYM
seen = set(); rels = []
for rel in itertools.product(range(3), repeat=6):
    full = list(rel) + [0] * 4
    key = min(tuple(full[p[x]] for x in range(6)) for p in SR)   # relabel by symmetry (hexagon corners map to hexagon corners)
    if key not in seen: seen.add(key); rels.append(list(key) + [0] * 4)
print(f"reliefs up to symmetry: {len(rels)}; K={K} n={NP}", flush=True)
from collections import Counter
stats = Counter(); bad = []
for ri, rel in enumerate(rels):
    for mirror in (True, False):
        words = {w for w, S in S_.items() if W.solve(S, sigs(S, rel), mirror)}
        bits = {b for b in 'ST' if b * (K - 1) in words or any(b in w for w in words)}
        prod = {''.join(w) for w in itertools.product(sorted(bits), repeat=K - 1)} if words else set()
        ok = words == prod
        stats[(mirror, ''.join(sorted(bits)) if words else 'none', ok)] += 1
        if not ok: bad.append((rel[:6], mirror, sorted(words)))
    if ri % 20 == 0: print(f"HEARTBEAT {time.time()-t0:.0f}s relief {ri}/{len(rels)}", flush=True)
print("RESULT (mirrors, admitted bits, words == all words over those bits): count", sorted(stats.items()), flush=True)
print("counterexamples", bad[:5], flush=True)
print('FINAL ok' if not bad and len(rels) > 50 else f'FINAL FAIL: {len(bad)} reliefs break the product law', f'{time.time()-t0:.0f}s')
