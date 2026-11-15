#!/usr/bin/env python3
"""E8 follow-up: is each OPEN 120-root set S (stabiliser 576 or 144 in the diagonal H4) the image of a 600-cell shell under W(E8)?
Search: an orthogonal map w sending a basis of shell 1 onto points of S with the same exact Gram values (B-form classes), such that w
maps all of shell 1 onto S (exact signature match); then w (float matrix) must map all 240 roots onto roots (so w is in Aut(E8) = W(E8)).
Control: a random 120-subset of the roots is not such an image."""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
HZ = os.path.join(HERE, '..', '..', '2026-11-15-hidden-zeros-h4')
sys.path.insert(0, os.path.join(HZ, 'scripts'))
from hz_core import *
from hz_universes import *
X = cell600()
P8, ipB, Yf = e8_from(X)
U = Universe('E8 roots', P8, 8, Yf, ipfun=ipB)
IM = U.IM
sh = list(range(120)); basis = span_basis(Yf, sh)
nv = int(IM.max()) + 1
def enc(M):
    k = np.zeros(M.shape[0], dtype=np.int64)
    for c in range(M.shape[1]): k = k * nv + M[:, c]
    return k
ref = enc(IM[np.ix_(sh, basis)])
def iso(S, cap=2_000_000):
    S = np.array(sorted(S)); calls = [0]
    def rec(ys):
        calls[0] += 1
        if calls[0] > cap: return None
        i = len(ys)
        if i == len(basis):
            sig = enc(IM[np.ix_(S, ys)])
            return ys if sorted(sig.tolist()) == sorted(ref.tolist()) else None
        cand = S
        for j, y in enumerate(ys): cand = cand[IM[cand, y] == IM[basis[i], basis[j]]]
        for c in cand:
            if c in ys: continue
            r = rec(ys + [int(c)])
            if r: return r
        return None
    return rec([])
d = json.load(open(os.path.join(HZ, 'data', 'census-E8.json')))
cases = [s for s in d['sets'] if 4 in s['OPEN'] and s['stab_order'] in (576, 144)]
ok = True; out = []
for s in cases:
    ys = iso(s['rep'])
    if ys is None:
        print(f'stab {s["stab_order"]}: no isometry from shell 1 found', flush=True); ok = False; out.append(False); continue
    W = np.linalg.solve(Yf[basis], Yf[ys]).T          # w Yf[b] = Yf[y]
    img = Yf @ W.T
    dist = np.min(np.linalg.norm(img[:, None, :] - Yf[None, :, :], axis=2), axis=1)
    inW = dist.max() < 1e-9
    onto = set(np.argmin(np.linalg.norm(img[:120, None, :] - Yf[None, :, :], axis=2), axis=1).tolist()) == set(s['rep'])
    orth = np.abs(W @ W.T - np.eye(8)).max() < 1e-9
    print(f'stab {s["stab_order"]}: w orthogonal {orth}, maps shell 1 onto S {onto}, maps the 240 roots to roots (w in W(E8)) {inW}', flush=True)
    ok &= orth and onto and inW; out.append(bool(orth and onto and inW))
rng = np.random.default_rng(7)
R = sorted(rng.choice(240, 120, replace=False).tolist())
neg = iso(R, cap=200000) is None
print(f'control: random 120-subset of the roots is not an isometric image of a shell: {neg}', flush=True)
json.dump({'cases': [{'stab': s['stab_order'], 'w_in_WE8_maps_shell_onto_S': o} for s, o in zip(cases, out)], 'control_random_not_image': neg},
          open(os.path.join(HERE, '..', 'data', 'e8-shell-images.json'), 'w'), indent=1)
print('FINAL ok' if ok and neg and len(cases) == 4 else 'FINAL FAIL')
