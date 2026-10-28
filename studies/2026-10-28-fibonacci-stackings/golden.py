# The Fibonacci stacking and the Hexagonality Law (DICTO 10-28). Exact: in the infinite Fibonacci stacking (types c -> ch, h -> c)
# the share of h layers is 1/phi^2 = (3 - sqrt5)/2, and the four kinds of piece (lower type, upper type) occur with frequencies
# cc 1/phi^3, ch 1/phi^2, hc 1/phi^2, hh 0 (h layers never touch). By the law each role then averages exactly
# V(cc) + (V(hh) - V(cc)) (3 - sqrt5)/2 per layer: the golden ratio enters the volumes of a stacking.
import json
from fractions import Fraction as F
from collections import Counter
def fib(n):
    w = 'c'
    while len(w) < n: w = ''.join('ch' if x == 'c' else 'c' for x in w)
    return w[:n]
w = fib(200000); n = len(w); phi = (1 + 5 ** .5) / 2
c = Counter(w[k:k + 2] for k in range(n - 1))
print('share h', w.count('h') / n, ' 1/phi^2 =', 1 / phi ** 2)
print('pairs', {k: round(v / (n - 1), 6) for k, v in c.items()}, ' 1/phi^3 =', round(1 / phi ** 3, 6), ' 1/phi^2 =', round(1 / phi ** 2, 6))
# rock salt / NiAs at lam = 1/3 (exact volumes of #64's run): per-layer averages in Q(sqrt5), written a + b sqrt5
d = json.load(open('/home/dicto/k-research/studies/2026-10-27-splash-rules/run2/out/rocksalt_mix.json'))
lam = F(1, 3); win = next(x for x in d['windows'] if F(x['lo']) < lam < F(x['hi']))
ev = lambda e: eval(e.replace('lam', '(F(1,3))').replace('/', '*F(1,1)/'), {'F': F})
res = {}
for r, name in [('S', 'ball'), ('O', 'octahedral atom'), ('C', 'tetrahedral hole (lower)'), ('Y', 'tetrahedral hole (upper)')]:
    V = {k: ev(e) for k, e in win['roles'][r]['volumes'].items()}
    D = V['hh'] - V['cc']
    a, b = V['cc'] + D * F(3, 2), -D / 2            # V(cc) + D (3 - sqrt5)/2
    res[name] = (str(a), str(b), float(a) + float(b) * 5 ** .5)
    print(f'{name:26s} per layer = {a} + ({b}) sqrt5 = {float(a) + float(b) * 5 ** .5:.9f}')
json.dump(res, open('golden_rocksalt.json', 'w'), indent=1)
