# Tables for the README and the build sheet, from ../out/scan.json, ../out/angles.txt and ../out/faces--1_8.json.
# Usage: python3 tables.py  -> stdout (markdown), saved as ../out/tables.md
import json, os, re
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(HERE, '../out')
rows = json.load(open(os.path.join(O, 'scan.json')))
def sig(a): return ' + '.join(f"{v}×{ {'3':'tri','4':'quad','5':'pent','6':'hex','7':'hept','12':'12-gon'}[k] }" for k, v in a['kinds'].items())
# group consecutive weights with the same face kinds for both tiles
groups = []
for r in sorted(rows, key=lambda r: Fr(r['lam'])):
    key = (sig(r['c']), sig(r['h']))
    if groups and groups[-1]['key'] == key: groups[-1]['lams'].append(r)
    else: groups.append(dict(key=key, lams=[r]))
print('| λ | weights tested | c-tile faces | c: ring faces (best) | h-tile faces | h: ring faces (best) |')
print('|---|---|---|---|---|---|')
for g in groups:
    L = [Fr(r['lam']) for r in g['lams']]
    rng = str(L[0]) if len(L) == 1 else f'{L[0]} … {L[-1]}'
    def best(t):
        b = max(g['lams'], key=lambda r: r[t]['ring_ok']); n = b[t]['faces']
        return f"{b[t]['ring_ok']}/{n}" + (f" (at {b['lam']})" if b[t]['ring_ok'] and len(L) > 1 else '')
    print(f"| {rng} | {len(L)} | {g['lams'][0]['c']['faces']}: {g['key'][0]} | {best('c')} | {g['lams'][0]['h']['faces']}: {g['key'][1]} | {best('h')} |")
print()
print('Surface parts (solids joined over area): c', sorted({r['c']['surface_parts'] for r in rows}), ' h', sorted({r['h']['surface_parts'] for r in rows}))
print('Volume check (union = sum of pieces) all true:', all(r[t]['vol_ok'] for r in rows for t in 'ch'), '; side check (every side used by two faces) all true:', all(r[t]['edge_bad'] == 0 for r in rows for t in 'ch'))
print()
F = json.load(open(os.path.join(O, 'faces--1_8.json')))
for t in 'ch':
    kinds = {}
    for f in F[t]:
        k = (len(f['corners']), tuple(sorted(f['sides'])), f['rings']); kinds[k] = kinds.get(k, 0) + 1
    print(f'{t}-tile at λ = -1/8: | corners | sides | count | rings each | rings | shared ring sides inside each face | ties inside |')
    tot = [0, 0, 0]
    for (n, s, r), c in sorted(kinds.items()):
        per = sum(Fr(x) * 2 for x in s); inner = (3 * r - per) / 2
        print(f'| {n} | {", ".join(s)} | {c} | {r} | {c * r} | {inner} | {2 * c * inner} |'); tot[0] += c; tot[1] += c * r; tot[2] += c * inner
    along = Fr(3 * tot[1], 2) - tot[2]
    print(f'| total | | {tot[0]} | | {tot[1]} | {tot[2]} inside faces + {along} on the edges = {tot[2] + along} | {2 * (tot[2] + along)} |')
