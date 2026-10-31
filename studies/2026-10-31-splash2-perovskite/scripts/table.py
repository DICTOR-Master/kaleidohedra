# Known polytypes table + Ramsdell check from the exact data (light; reads data/splash2_perovskite.json).
import json, sys
from fractions import Fraction as Fr
D = json.load(open(sys.argv[1]))
def ramsdell(letters):
    L = ['ABC'.index(c) for c in letters]; N = len(L)
    if N == 3 and len(set(L)) == 3: return '3C'
    if N % 3 == 0:
        for sh in (1, 2):
            if all(L[(k + N // 3) % N] == (L[k] + sh) % 3 for k in range(N)): return f'{N}R'
    return f'{N}H'
cols = ['face partners per B', 'B with 0 shared faces', 'B with 2 shared faces', 'face-sharing clusters per B (incl. single octahedra)',
        'strings (2 or more octahedra) per B', 'B-B at r2=8/3', 'A neighbours per B (r2=3/2)']
print('| name | c/h | Ramsdell (computed) | examples | h | p_hh | ' + ' | '.join(cols) + ' |')
for k in D['known']:
    print(f"| {k['name']} | ({k['word']}) | {ramsdell(k['letters'])} | {k['compounds']} | {k['stats']['h']} | {k['stats']['p_hh']} | " + ' | '.join(k['Q'][c] for c in cols) + ' |')
