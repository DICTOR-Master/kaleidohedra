#!/usr/bin/env python3
"""minimal polynomials of the exact spacings in named.json (compact exact form); 60 s cap each."""
import json, sys, signal
import sympy as sp
d = json.load(open(sys.argv[1])); x = sp.Symbol('x'); out = {}
def alarm(s, f): raise TimeoutError
signal.signal(signal.SIGALRM, alarm)
items = [('H', d['cell']['H_exact'])]
for sec in ['arrangements', 'rings', 'mandala']:
    for a in d[sec]:
        ex = a.get('t_exact') or a.get('period_exact') or a.get('r_exact') or a.get('d_exact')
        items.append((a['name'], ex))
items.append(('volume', d['cell']['volume_exact']))
for k, (name, ex) in enumerate(items):
    e = sp.sympify(ex); signal.alarm(60)
    try:
        mp = sp.minimal_polynomial(e, x); signal.alarm(0); out[name] = dict(minpoly=str(sp.factor(mp)), degree=int(sp.degree(mp, x)), value=str(sp.N(e, 20)))
    except Exception as er:
        signal.alarm(0); out[name] = dict(minpoly=None, value=str(sp.N(e, 20)))
    print(f'PROGRESS {(k + 1) / len(items):.3f} {name}: {out[name]}', flush=True)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print('FINAL ok' if out['H']['minpoly'] else 'FINAL FAIL')
