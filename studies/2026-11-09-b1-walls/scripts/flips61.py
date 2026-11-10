"""Name each #61 wall's flip (DICTO 10 Nov): at s = 1/5, just below and just above each wall (-9/40, -19/120 = -(4-s)/24, -1/8 = -5s/8,
-1/40 = -s/8), every power cell of the six words; the pairs of holes that share a face of positive area; which pairs are gained and lost.
Each pair is named by the two roles (oct / tetX / tetY) and the layer offset between them."""
import sys, os
from fractions import Fraction as Fr
from collections import Counter
from validate import Net, Cell, net_for, ROLE_OF
WORDS = ['ABC', 'AC', 'ACBC', 'ACABC', 'ACBCAC', 'ACBABC']; s = Fr(1, 5); d = Fr(1, 1000)
WALLS = [(Fr(-9, 40), '-9s/8'), (Fr(-19, 120), '-(4-s)/24'), (Fr(-1, 8), '-5s/8'), (Fr(-1, 40), '-s/8')]
print(f'START flips at s = {s}, {len(WALLS)} walls', flush=True)
def pairs(lam):
    out = Counter()
    for w in WORDS:
        spec = net_for(w, s); net = Net(w, spec['G'], spec['T'], spec['motif'], spec['w']); n = len(w)
        for i in range(3 * n):
            c = Cell(net, i, (lam,), Fr(12))
            if c.empty: continue
            for k in c.faces():
                h = c.H[k]; j = h['j']; dz = (j // 3 - i // 3) + h['kv'][2] * n      # layer offset (in layers)
                a, b = ROLE_OF[i % 3], ROLE_OF[j % 3]
                out[(w, tuple(sorted([(a, 0), (b, dz)])) if a <= b else tuple(sorted([(b, 0), (a, -dz)])))] += 1
    return out
changed = 0
for t, (lw, name) in enumerate(WALLS):
    lo, hi = pairs(lw - d), pairs(lw + d)
    gain = {k: v - lo.get(k, 0) for k, v in hi.items() if v > lo.get(k, 0)}; lost = {k: v - hi.get(k, 0) for k, v in lo.items() if v > hi.get(k, 0)}
    G = Counter(); Lc = Counter()
    for (w, pr), v in gain.items(): G[pr] += v
    for (w, pr), v in lost.items(): Lc[pr] += v
    changed += 1 if (G or Lc) else 0
    print(f'WALL λ = {lw} ({name}): gained {dict(G)}; lost {dict(Lc)}', flush=True)
    print(f'PROGRESS {(t + 1) / len(WALLS):.2f}', flush=True)
print('FINAL ok' if changed == len(WALLS) else f'FINAL FAIL: only {changed} of {len(WALLS)} walls show a flip')
