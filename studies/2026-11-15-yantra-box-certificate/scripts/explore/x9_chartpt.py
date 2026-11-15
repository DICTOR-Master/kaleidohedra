"""Exploration: values of the chart tests at a chart point."""
import json, sys
from fractions import Fraction as Fq
d = json.load(open(sys.argv[1])); pt = [Fq(x) for x in sys.argv[2:5]]
def ev(P): return sum(int(c) * pt[0]**e[0] * pt[1]**e[1] * pt[2]**e[2] for e, c in P)
print('F:', {k: float(ev(v)) for k, v in d['F'].items()})
for k, v in d['tests'].items():
    n, dd = ev(v['N']), ev(v['D'])
    tag = 'VIOLATED' if n * dd < 0 else ('0' if n * dd == 0 else 'holds')
    print(f'  {k}: N={float(n):.4g} D={float(dd):.4g} {tag}')
