# Stage 0 for the Stackings World (DICTO 10-26): is the #57 piece census more than the h/c statistics of the stacking?
# Exact (sympy) on #57's appendix.json. Per site and period: each layer owns two tetrahedral pieces of its own type (one in each
# neighbouring gap); each gap owns one octahedral piece, top half from the layer above, bottom half from the layer below.
import json, sympy as sp, itertools, pathlib
lam = sp.Symbol('lam'); A = json.load(open(pathlib.Path(__file__).parent / '../2026-10-25-stackings/appendix.json'))
iv = sorted({tuple(e['stretch']) for e in A}, key=lambda t: sp.Rational(t[0]))
V = {}
for e in A:
    t = e['rule'].replace('top ', '').replace('bottom ', '').replace(' + ', '')  # 'hh','ch','hc','cc' (top,bottom) or 'h','c'
    V[(e['kind'], t, tuple(e['stretch']))] = sp.sympify(e['volume'], locals={'lam': lam})
def v(kind, t, I): return V.get((kind, t, I), sp.Integer(0))  # missing = piece of zero volume on that interval (stop)
ok = True
for I in iv:
    # 1. mean rule: O(top x, bottom y) = (O(x,x) + O(y,y))/2
    for x, y in (('c', 'h'), ('h', 'c')):
        d = sp.simplify(v('oct', x + y, I) - (v('oct', x + x, I) + v('oct', y + y, I)) / 2)
        print('mean rule', I, x + y, 'OK' if d == 0 else d); ok &= d == 0
    # 2. space per layer is the same for c and h (each layer owns 2 tets + one oct-equivalent)
    d = sp.simplify(2 * v('tet', 'c', I) + v('oct', 'cc', I) - 2 * v('tet', 'h', I) - v('oct', 'hh', I))
    print('equal space per layer', I, 'OK' if d == 0 else d); ok &= d == 0
# 3. census of words with the same hexagonality but different order: oct share of space is identical
def share(word, I):
    n = len(word); o = sum(v('oct', word[(k + 1) % n] + word[k], I) for k in range(n)); t = sum(2 * v('tet', s, I) for s in word)
    return sp.simplify(o), sp.simplify(t)
for a, b in (('hhcc', 'hchc'), ('hhhccc', 'hchchc'), ('hhccc', 'hchcc'), ('hcccc', 'chccc')):
    for I in iv:
        d = [sp.simplify(x - y) for x, y in zip(share(a, I), share(b, I))]
        print('same hexagonality', a, b, I, 'OK' if d == [0, 0] else d); ok &= d == [0, 0]
print('ALL PASS' if ok else 'FAIL')
