# Step 3, the rule of halves: every O and Y void cut at its gap's mid-height (k + 1/2) H into a bottom half (layer k) and a top half
# (layer k+1); S whole (its own layer), C whole (nearest layer k+1). Rule: every piece equals the piece of the same kind in the pure
# stacking (3C if its layer is c, 2H if h). Checked on 4H, 6H, 9R, 15R at several weights a (b = c = 0).
import numpy as np, itertools, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0]); from pyro import H, A1, A2, layer_types
import cells
def pieces(word, W):
    S = cells.sites(word); out = []
    n = len(word)
    for i, (t, k, p) in enumerate(S):
        if t in 'SC':
            h = cells.cell(word, i, W); out.append((t, (k if t == 'S' else (k + 1) % n), h.volume if h else 0.0))
            continue
        mid = (k + .5) * H - p[2]                                     # the mid-plane, relative to the site
        for half, sgn, layer in (('bot', 1, k), ('top', -1, (k + 1) % n)):
            h = cells.cell_cut(word, i, W, sgn, mid); out.append((t + half, layer, h.volume if h else 0.0))
    return out
def pure(W):
    ref = {}
    for ty, w in (('c', 'ABC'), ('h', 'AB')):
        for t, k, v in pieces(w, W): ref.setdefault((t, ty), set()).add(round(v, 7))
    return ref
for a in (-0.25, -0.2, -0.1, 0.0, 0.1):
    W = {'S': a, 'C': a, 'O': 0, 'Y': 0}; ref = pure(W); bad = 0; n = 0
    for name, w in (('4H', 'ABAC'), ('6H', 'ABCACB'), ('9R', 'ABACACBCB'), ('15R', 'ABCACBCABACABCB')):
        ty = layer_types(w)
        for t, layer, v in pieces(w, W):
            n += 1
            if round(v, 7) not in ref[(t, ty[layer])]: bad += 1; print(f'  a={a} {name}: {t} of layer {layer} ({ty[layer]}) {v:.7f} not in {ref[(t, ty[layer])]}')
    print(f'a = {a}: {n} pieces checked, {bad} off the rule;', 'pure values', {f'{k[0]}/{k[1]}': sorted(v) for k, v in ref.items()})
