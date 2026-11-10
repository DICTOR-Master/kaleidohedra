"""B1 / #61 below s = 1/4, the Hopscotch way (DICTO 10 Nov: "doesnt follow hopscotch"). λ is the slider. In a power diagram every
plane has a fixed normal and an offset affine in λ, every corner is affine in λ, and the combinatorial type changes only where a corner
meets another plane: a root, linear in λ (engine Cell.interval). Walk λ from λ-(c) = -1/4 - s/8 to U(s) = min(1/3 + s/24, 3s/8):
at each hop the next wall is the nearest root over every cell of every word; on the hop every volume is an exact polynomial in λ, and
so is the Swap defect D(λ) per role and outer context. Usage: python swap_walls.py <s> [max_hops]   -> data JSON lines + FINAL"""
import sys, json, itertools, time
from fractions import Fraction as Fr
import sympy as sp
from validate import Net, Cell, net_for, layer_type, ROLE_OF
from engine import cell_volume, LAM
WORDS = ['ABC', 'AC', 'ACBC', 'ACABC', 'ACBCAC', 'ACBABC']
s = Fr(sys.argv[1]); MAXH = int(sys.argv[2]) if len(sys.argv) > 2 else 400
lo_end = -Fr(1, 4) - s / 8; hi_end = min(Fr(1, 3) + s / 24, 3 * s / 8)
nets = []
for w in WORDS:
    spec = net_for(w, s); nets.append((w, Net(w, spec['G'], spec['T'], spec['motif'], spec['w'])))
def hop(sample):
    """cells at the sample: (next wall above, previous wall below, polynomial volumes per key, clashes)"""
    V, clash, hi, lo = {}, [], hi_end, lo_end
    for w, net in nets:
        n = len(w)
        for i in range(3 * n):
            c = Cell(net, i, (sample,), Fr(12)); k = i // 3
            key = (ROLE_OF[i % 3],) + tuple(layer_type(w, k + j) for j in (-1, 0, 1, 2))
            if c.empty: v = sp.Integer(0)
            else:
                a, b = c.interval()
                if a == 'breakpoint': return None
                if b is not None and b < hi: hi = b
                if a is not None and a > lo: lo = a
                v = sp.expand(cell_volume(c, c.faces()) * n)
            if key in V and sp.expand(V[key] - v) != 0: clash.append((key, w))
            V.setdefault(key, v)
    return hi, lo, V, clash
def middle(V, r):
    out = {}
    for a, b in itertools.product('ch', repeat=2):
        ks = [(r, a, x, y, b) for x, y in (('c', 'h'), ('h', 'c'), ('c', 'c'), ('h', 'h'))]
        if all(k in V for k in ks): out[a + b] = sp.factor(sp.expand(V[ks[0]] + V[ks[1]] - V[ks[2]] - V[ks[3]]))
    return out
print(f'START s = {s}: λ from {lo_end} to {hi_end}', flush=True)
cur = lo_end; h = 0; t0 = time.time(); ok = True
while cur < hi_end and h < MAXH:
    eps = min(Fr(1, 400), (hi_end - cur) / 2); res = None
    for _ in range(60):                                    # a sample strictly inside the next hop
        try: res = hop(cur + eps)
        except AssertionError: res = None
        if res is None: eps /= 2; continue
        if res[1] > cur: eps = (res[1] - cur) / 2; res = None; continue     # a wall lies between cur and the sample: move closer
        break
    assert res is not None, f'no clean sample above {cur}'
    hi, lo, V, clash = res
    row = {'s': str(s), 'from': str(cur), 'to': str(hi), 'clashes': len(clash), 'keys': len(V)}
    for r in ('oct', 'tetX', 'tetY'): row[r] = {k: str(v) for k, v in middle(V, r).items()}
    print(json.dumps(row), flush=True)
    print(f'PROGRESS {float((hi - lo_end) / (hi_end - lo_end)):.3f} hop {h + 1} to λ = {hi} ({time.time() - t0:.0f} s)', flush=True)
    cur = hi; h += 1
print('FINAL ok' if cur >= hi_end else f'FINAL FAIL: stopped at hop {h}, λ = {cur}')
