# Volume form of the Swap Rule below s0 (check only, DICTO 2026-10-27): exact engine volumes of every piece, grouped by role and the
# types of its two layers; consistency (one volume per group) and V(c|h) + V(h|c) = V(c|c) + V(h|h) per role. Usage: s lam,...
import sys
from fractions import Fraction as Fr
import sympy as sp
from validate import Net, Cell, net_for, layer_type, ROLE_OF
from engine import cell_volume, LAM
s = Fr(sys.argv[1])
for lam in [Fr(x) for x in sys.argv[2].split(',')]:
    V = {}; clash = 0
    for w in ['ABC', 'AC', 'ACBC', 'ACABC', 'ACBCAC', 'ACBABC']:
        spec = net_for(w, s); net = Net(w, spec['G'], spec['T'], spec['motif'], spec['w']); n = len(w)
        for i in range(3 * n):
            c = Cell(net, i, (lam,), Fr(12)); k = i // 3
            v = 0 if c.empty else sp.Rational(cell_volume(c, c.faces()).subs(LAM, sp.Rational(lam))) * n   # per unit cell height -> x n
            key = (ROLE_OF[i % 3], layer_type(w, k), layer_type(w, k + 1))
            if key in V and V[key] != v: clash += 1
            V.setdefault(key, v)
    for r in ('oct', 'tetX', 'tetY'):
        g = {k[1:]: v for k, v in V.items() if k[0] == r}
        if len(g) == 4: print(f's={s} lam={lam} {r}: V(c|h)+V(h|c)-V(c|c)-V(h|h) = {g[("c","h")] + g[("h","c")] - g[("c","c")] - g[("h","h")]}  (clashes so far {clash})', flush=True)
