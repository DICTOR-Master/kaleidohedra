# Counting rule check (DICTO 2026-10-27, "do 1 and 2"): in each spacing's windows, the exact ratio hexagonal : cubic and Janus : cubic
# of the octahedral pieces; where it is constant, the pieces shrink together (end of the walk) and the face-count rule predicts it.
import json, glob, os, sympy as sp
from fractions import Fraction as Fr
D = os.path.expanduser('~/kres-tmp/splash/data')
for p in sorted(glob.glob(f'{D}/s_*.json'), key=lambda p: Fr(json.load(open(p))['s'])):
    d = json.load(open(p))
    if int(d['rmin']) != 1: print(d['s'], 'reach 2: skipped'); continue
    out = []
    for w in sorted(d['mix'], key=Fr):
        V = {x['ctx']: sp.sympify(x['volume']) for x in d['mix'][w] if x['role'] == 'oct'}
        if all(k in V for k in ('---', '-+-', '--+')) and V['---'] != 0:
            a, b = sp.cancel(V['-+-'] / V['---']), sp.cancel(V['--+'] / V['---'])
            if not a.free_symbols: out.append(f'λ>{w}: hex/cubic = {a}, Janus/cubic = {b}')
    print(d['s'], '|', '; '.join(out) or 'no constant-ratio window', flush=True)
