# Swap Rule proof, sharpness (DICTO 2026-10-27): outside the proved range the halves identity itself fails. Engine only (whole
# stackings, exact): each half of each piece is compared with the same half of the same-role piece of the pure stacking of that
# layer's type (ABC for c, AC for h), same s and lam (exact fingerprints, as in swap_cut.py). A FAIL = a half that is not the pure half.
# Usage: python sharp.py <s> <lam,...> [words]
import sys, os
from fractions import Fraction as Fr
from validate import Net, Cell, net_for, half, fp, layer_type, ROLE_OF
s = Fr(sys.argv[1]); lams = [Fr(x) for x in sys.argv[2].split(',')]
words = sys.argv[3].split(',') if len(sys.argv) > 3 else ['ACBC', 'ACABC', 'ACBCAC', 'ACBABC']
def build(w): spec = net_for(w, s); return Net(w, spec['G'], spec['T'], spec['motif'], spec['w'])
def halves(net, w, lam):
    n = len(w); out = {}
    for k in range(n):
        for jr in range(3):
            i = 3 * k + jr; c = Cell(net, i, (lam,), Fr(12)); zc = (k + Fr(1, 2)) / n
            out[(k, jr)] = tuple(tuple(fp(net.G, half(c, lam, zc, up))) if not c.empty else () for up in (False, True))
    return out
tot_ok = tot_bad = 0
for lam in lams:
    ref = {'c': halves(build('ABC'), 'ABC', lam), 'h': halves(build('AC'), 'AC', lam)}
    R = {(t, jr, up): ref[t][(0, jr)][up] for t in 'ch' for jr in range(3) for up in (0, 1)}
    bad = []
    for w in words:
        H = halves(build(w), w, lam); n = len(w)
        for (k, jr), (lo, hi) in H.items():
            for up, e in ((0, lo), (1, hi)):
                t = layer_type(w, k + up)
                if e == R[(t, jr, up)]: tot_ok += 1
                else: tot_bad += 1; bad.append(f'{w} gap {k} {ROLE_OF[jr]} {"upper" if up else "lower"} half (layer type {t})')
    print(f's={s} lam={lam}: {len(bad)} halves differ from the pure half; e.g. {bad[:4]}', flush=True)
print(f'TOTAL s={s}: {tot_ok} halves equal to the pure half, {tot_bad} differ')
