# Other splits of the pieces between layers (task step 4). A two-tile system needs each layer's tile to depend on that layer's
# letter (c/h) alone. The pieces of the gap between layers g and g+1 are: the octahedral piece (cut at mid-plane by the Rule of
# Halves), the tetrahedral piece with its base on layer g (tip at g+1) and the one with its base on layer g+1. Exact test: for
# every gap in words covering all contexts, the shape of each whole piece (up to lattice symmetry about its site, z kept or
# flipped) is recorded with the types (T[g], T[g+1]); a piece can be given to a layer only if its shape is fixed by that layer's
# type alone. Usage: ~/geom/bin/python split_check.py <lam> ...
import itertools, sys
from fractions import Fraction as Fr
from engine import Cell
from tiles import build, types, corners, SYM, ctx_words

def shape(X, site, n):
    Y = [(p[0] - site[0], p[1] - site[1], (p[2] - site[2]) * n) for p in X]; best = None
    for (a, b, c, d), fl in itertools.product(SYM, (1, -1)):
        k = tuple(sorted((a * p[0] + b * p[1], c * p[0] + d * p[1], fl * p[2]) for p in Y))
        best = k if best is None or k < best else best
    return best

if __name__ == '__main__':
    W = sorted({w for w, L in ctx_words().values()})
    for s in sys.argv[1:]:
        lam = Fr(s); rec = {}
        for w in W:
            net, spec = build(w); n = len(w); T = types(w); m = spec['motif']
            for g in range(n):
                for off, name in ((0, 'oct'), (1, 'tet tip-down (base on g+1)'), (2, 'tet tip-up (base on g)')):
                    i = 3 * g + off; c = Cell(net, i, (lam,), Fr(12))
                    if c.empty: continue
                    X = corners(c, lam); key = shape(X, m[i][1], n)
                    rec.setdefault(name, {}).setdefault((T[g], T[(g + 1) % n]), set()).add(key)
        print(f'λ={s}')
        for name, d in rec.items():
            allk = {k for v in d.values() for k in v}
            by_lo = {a: set().union(*[v for (x, y), v in d.items() if x == a]) for a in 'ch'}
            by_hi = {b: set().union(*[v for (x, y), v in d.items() if y == b]) for b in 'ch'}
            f = lambda D: all(len(v) <= 1 for v in D.values())
            print(f'  {name}: {len(allk)} shapes over type pairs {sorted(d)}; fixed by lower layer type: {f(by_lo)}; '
                  f'by upper layer type: {f(by_hi)}', flush=True)
