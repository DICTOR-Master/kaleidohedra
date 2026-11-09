# B1 / #61: the Swap Rule below s = 1/4, exact. Engine volumes (census engine of #57, validate.py of the Swap Rule proof) of every
# hole piece in every stacking word given, keyed by role and the types of the FOUR layers round its gap (t-, t, t', t+);
# consistency (one volume per key) and the middle second difference
#   D(t-, t+) = V(t-,c,h,t+) + V(t-,h,c,t+) - V(t-,c,c,t+) - V(t-,h,h,t+)
# (the Swap Rule with the outer layers held fixed; for s >= 1/4 V does not depend on t-, t+ and D = 0 is #61's Theorem 2).
# Usage: python swap4.py <s> <lam,lam,...> [words]  -> prints; last line FINAL
import sys, json, itertools
from fractions import Fraction as Fr
import sympy as sp
from validate import Net, Cell, net_for, layer_type, ROLE_OF
from engine import cell_volume, LAM
WORDS = ['ABC', 'AC', 'ACBC', 'ACABC', 'ACBCAC', 'ACBABC']   # the six words of #61's map: all 16 four-layer contexts
def table(s, lam, words=WORDS):
    V = {}; clash = []
    for w in words:
        spec = net_for(w, s); net = Net(w, spec['G'], spec['T'], spec['motif'], spec['w']); n = len(w)
        for i in range(3 * n):
            c = Cell(net, i, (lam,), Fr(12)); k = i // 3
            v = 0 if c.empty else sp.Rational(cell_volume(c, c.faces()).subs(LAM, sp.Rational(lam))) * n
            key = (ROLE_OF[i % 3],) + tuple(layer_type(w, k + j) for j in (-1, 0, 1, 2))
            if key in V and V[key] != v: clash.append((key, w))
            V.setdefault(key, v)
    return V, clash
def middle(V, r):
    out = {}
    for a, b in itertools.product('ch', repeat=2):
        ks = [(r, a, x, y, b) for x, y in (('c', 'h'), ('h', 'c'), ('c', 'c'), ('h', 'h'))]
        if all(k in V for k in ks): out[a + b] = V[ks[0]] + V[ks[1]] - V[ks[2]] - V[ks[3]]
    return out
if __name__ == '__main__':
    s = Fr(sys.argv[1]); lams = [Fr(x) for x in sys.argv[2].split(',')]
    res = []; ok = True
    for lam in lams:
        V, clash = table(s, lam)
        row = dict(s=str(s), lam=str(lam), keys=len(V), clashes=len(clash))
        for r in ('oct', 'tetX', 'tetY'): row[r] = {k: str(v) for k, v in middle(V, r).items()}
        ok &= not clash and len(V) == 48
        res.append(row); print(json.dumps(row), flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL: clashes or missing contexts (4-layer key not enough or words too few)')
