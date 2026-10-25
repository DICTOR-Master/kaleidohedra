# #57 appendix data: every piece type of every close-packed stacking (the 16 windows' central gap), on every stretch: exact corner
# functions (affine in λ, coordinates (x, y) in the hexagonal layer basis and z in layer spacings, relative to the site), exact volume
# (polynomial in λ times √2-free factor via the metric determinant), and which pure piece (or halves) it is. Output ../appendix.json.
exec(open('exact_stretch.py').read().split('REFN = ')[0])
import json, sympy as sp
from engine import cell_volume, LAM
seen = {}
for hc in itertools.product('hc', repeat=4):
    hc = ''.join(hc); word = word_for(hc); net, spec = build(word); n = len(word); T = layer_types(word)
    det = sp.sqrt(sp.Matrix(spec['G']).det())
    for lo, hi in STRETCH:
        mid = (lo + hi) / 2; g0 = 2
        for j in range(3):
            i = 3 * g0 + j; k, p = spec['motif'][i]; c = cell(net, i, mid)
            if c is None: continue
            F = c.faces(); sig = (k, len(c.corners), tuple(sorted(len(v) for v in F.values())))
            rule = (T[(g0 + 1) % n] if j == 1 else T[g0 % n]) if k == 'tet' else f'top {T[(g0 + 1) % n]} + bottom {T[g0 % n]}'
            key = (sig, str(lo), str(hi), rule)
            if key in seen: seen[key]['windows'].append(hc); continue
            vol = sp.factor(sp.expand(cell_volume(c, F) * det))
            seen[key] = dict(kind=k, corners=len(c.corners), faces=list(sig[2]), stretch=[str(lo), str(hi)], rule=rule,
                             volume=str(vol), corner_functions=[[[str(a), str(b)] for a, b in f] for f in funcs(c, spec, i, n)], windows=[hc])
data = list(seen.values())
json.dump(data, open('../appendix.json', 'w'), indent=1)
print(f'{len(data)} (piece type, stretch, rule) entries')
for d in data: print(d['kind'], d['corners'], d['faces'], d['stretch'], d['rule'], 'volume', d['volume'][:80])
