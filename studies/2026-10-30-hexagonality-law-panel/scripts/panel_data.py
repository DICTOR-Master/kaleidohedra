# The Hexagonality Law panel's data (DICTO 2026-10-29 "all recommended": decisions 1A-5A). One entry per paper of the law, the
# same charts as the site cards and papers, values copied unchanged from each paper's own figure script and study files:
#  #66 studies/2026-10-27-splash-rules/run2/out/rocksalt_mix.json via 2026-10-28-halves-physics/scripts/card_figs.py
#  #68 2026-10-28-measured-polytypes/fig68.py   #70 2026-10-28-pressure/pressure.json + fig70.py
#  #71 2026-10-28-law-in-alloys/fig71.py        #72 2026-10-28-perovskites-cathodes/fig72.py
#  #73 2026-10-28-ice-diamond-nanowires/fig73.py (energies from the ANNNI parameters there)   #74 2026-10-28-pyrochlore-kagome/fig74.py
# A point carries a stacking word only where the source names the stacking (or it is a standard polytype); only those build.
# Writes ~/k-mix/src/app/hexlaw-data.js.
import json, os
from fractions import Fraction as F
S = os.path.expanduser('~/k-research/studies')
STD = {'3C': 'ABC', '2H': 'AB', '4H': 'ABAC', '6H': 'ABCACB', '9R': 'ABACACBCB', '15R': 'ABCACBCABACABCB'}
def hx(w): n = len(w); return sum(w[i - 1] == w[(i + 1) % n] for i in range(n)) / n
def pt(label, h, y, word=None):
    if word is None and label in STD: word = STD[label]
    if word: assert abs(hx(word) - h) < 1e-9, (label, word, h)
    return {'label': label, 'h': round(h, 6), 'y': round(y, 6), **({'word': word} if word else {})}
C = []
# #66
d = json.load(open(f'{S}/2026-10-27-splash-rules/run2/out/rocksalt_mix.json')); lam = F(1, 3)
w = next(w for w in d['windows'] if F(w['lo']) < lam < F(w['hi']))
V = {k: eval(e.replace('lam', '(F(1,3))').replace('/', '*F(1,1)/'), {'F': F}) for k, e in w['roles']['O']['volumes'].items()}
a, b = V['cc'], V['hh']
W66 = [('3C', 'ABC'), ('6H', 'ABCACB'), ('10H', 'ABACB'), ('4H', 'ABCB'), ('6H', 'ABCBAB'), ('2H', 'AB')]
C.append({'paper': 66, 'key': 'c66', 'x': 'h', 'series': [{'name': 'NaCl / NiAs', 'line': [[0, float(a)], [1, float(b)]],
          'points': [pt(f'{n} {wd}', hx(wd), float(a + F(hx(wd)).limit_denominator(30) * (b - a)), wd) for n, wd in W66]}]})
# #68
S68 = {'SiC': {0: 7.542/3*3.079**2, 1/3: 15.113/6*3.077**2, .4: 37.800/15*3.076**2, .5: 10.085/4*3.076**2, 1: 5.059/2*3.074**2},
       'Si': {0: 40.152, 1/3: 40.106, .5: 40.095, 1: 40.109}, 'Ge': {0: 45.596, 1/3: 45.535, .5: 45.516, 1: 45.493}}
NAME = {0: '3C', 1/3: '6H', .4: '15R', .5: '4H', 1: '2H'}
ser = []
for m, dd in S68.items():
    y = {h: 100 * (v / dd[0] - 1) for h, v in dd.items()}
    ser.append({'name': m, 'line': [[0, 0], [1, y[1]]], 'points': [pt(NAME[h], h, y[h]) for h in sorted(y)]})
C.append({'paper': 68, 'key': 'c68', 'x': 'h', 'series': ser})
# #70 (against pressure, not h: no stacking dots, no own-stacking marker)
p = json.load(open(f'{S}/2026-10-28-pressure/pressure.json'))
ser = []
for m, key, ptr in (('SiC', 'SiC (GGA+vdW, Kawanishi-Mizoguchi)', None), ('Si', 'Si (PBEsol, Keller et al.)', 11.0), ('Ge', 'Ge (PBEsol, Keller et al.)', 10.0)):
    e, v, _ = p[key]['margins']['3C vs 6H']
    ser.append({'name': m, 'line': [[0, e], [30, e + v * 30]], 'until': ptr, 'points': []})
C.append({'paper': 70, 'key': 'c70', 'x': 'P', 'xmax': 30, 'mark': 4.5, 'series': ser})
# #71
H = [(0, '3C'), (1, '2H'), (1/2, '4H'), (1/3, '6H'), (3/5, 'Mg 10H'), (5/7, 'Mg 14H')]
C.append({'paper': 71, 'key': 'c71a', 'x': 'h', 'series': [
    {'name': '2 − h', 'line': [[0, 2], [1, 1]], 'points': [pt(n, h, 2 - h) for h, n in H]},
    {'name': 'h', 'line': [[0, 0], [1, 1]], 'points': [pt(n, h, h) for h, n in H]},
    {'name': '1', 'line': [[0, 1], [1, 1]], 'points': [pt(n, h, 1) for h, n in H]}]})
FE = [('3C', 0, 106), ('6H₁', 1/3, 80, 'ABCACB'), ('4H', 1/2, 82), ('10H', 3/5, 60), ('6H₂', 2/3, 59, 'ABCBAB'), ('2H', 1, 27)]
C.append({'paper': 71, 'key': 'c71b', 'x': 'h', 'series': [{'name': 'Fe', 'line': [[0, 106], [1, 27]], 'points': [pt(*q) for q in FE]}]})
# #72
C.append({'paper': 72, 'key': 'c72a', 'x': 'h', 'series': [
    {'name': 'BaRuO₃', 'line': [[0, 64.25], [0.72, 64.25 + 6.82 * 0.72]], 'points': [pt(k, h, v) for k, (h, v) in {'3C': (0, 64.28), '6H': (1/3, 65.88), '4H': (1/2, 67.51), '9R': (2/3, 68.91)}.items()]},
    {'name': 'BaMnO₃', 'line': [[0, 61.9], [1, 71.0]], 'points': [pt(k, h, v) for k, (h, v) in {'3C': (0, 61.9), '4H': (1/2, 66.1), '2H': (1, 71.0)}.items()]}]})
C.append({'paper': 72, 'key': 'c72b', 'x': 'o1', 'series': [{'name': 'LiₓCoO₂', 'line': [[0, 4.81], [1, 4.24]],
          'points': [{'label': 'O3, x = 0.35', 'h': 0, 'y': 4.81}, {'label': 'H1-3, x = 0.12', 'h': 0.5, 'y': 4.52}, {'label': 'O1, x = 0', 'h': 1, 'y': 4.24}, {'label': 'O3, x = 1', 'h': 0, 'y': 4.68}]}]})
# #73
HH = [(0, '3C'), (1/3, '6H'), (1/2, '4H'), (1, '2H')]
EC = {'GaAs': [0, 56, 77, 149], 'GaSb': [0, 50, 70, 146], 'InP': [0, 50, 77, 183], 'InAs': [0, 34, 58, 126], 'InSb': [0, 39, 59, 113]}
CF = {'GaAs': [0, .052, .071, .129], 'GaSb': [0, .057, .076, .148], 'InP': [0, .029, .039, .062], 'InAs': [0, .034, .055, .095], 'InSb': [0, .036, .061, .113], 'GaP': [0, .021, .027, .045]}
C.append({'paper': 73, 'key': 'c73a', 'x': 'h', 'series': [
    {'name': 'ΔEc', 'line': [[0, 0], [1, 1]], 'points': [pt(f'{n} {k}', h, v[i] / v[-1]) for k, v in EC.items() for i, (h, n) in enumerate(HH)]},
    {'name': 'Δcf', 'line': None, 'points': [pt(f'{n} {k}', h, v[i] / v[-1]) for k, v in CF.items() for i, (h, n) in enumerate(HH)]}]})
POLY = {'3C': 'ABC', '6H': 'ABCACB', '15R': 'ABCACBCABACABCB', '4H': 'ABAC', '9R': 'ABABCBCAC', '2H': 'AB'}
def spins(q):
    P = {'A': 0, 'B': 1, 'C': 2}; n = len(q); return [1 if (P[q[(i + 1) % n]] - P[q[i]]) % 3 == 1 else -1 for i in range(n)]
def En(q, J):
    s = spins(q); n = len(s); return -sum(J[m - 1] * s[i] * s[(i + m) % n] for i in range(n) for m in (1, 2, 3)) / n
J = {'Sn': (15.178, -.222, -.045), 'Ge': (16.816, -1.054, -.344), 'C': (25.448, -3.435, -.337), 'Si': (10.587, -2.593, -.766), 'SiC': (2.735, -2.424, -.396)}
ser = [{'name': k, 'line': [[0, 0], [1, 1]] if k == 'Sn' else None, 'joined': True,
        'points': [pt(n, hx(q), (En(q, j) - En(POLY['3C'], j)) / (En(POLY['2H'], j) - En(POLY['3C'], j)), q) for n, q in sorted(POLY.items(), key=lambda x: hx(x[1]))]} for k, j in J.items()]
C.append({'paper': 73, 'key': 'c73b', 'x': 'h', 'series': ser})
# #74
C.append({'paper': 74, 'key': 'c74', 'x': 'h', 'series': [{'name': 'Mn₃X', 'line': [[0, 4], [1, 1]],
          'points': [pt(k, h, 1 + 3 * (1 - h)) for k, h in (('3C', 0), ('6H', 1/3), ('4H', 1/2), ('9R', 2/3), ('2H', 1))]}]})
for c in C: c['label'] = {'c71a': '(a)', 'c71b': '(b)', 'c72a': '(a)', 'c72b': '(b)', 'c73a': '(a)', 'c73b': '(b)'}.get(c['key'], '')
out = os.path.expanduser('~/k-mix/src/app/hexlaw-data.js')
open(out, 'w').write('// The Hexagonality Law panel\'s charts (DICTO 2026-10-29, decisions 1A-5A), generated by k-research\n'
    '// studies/2026-10-30-hexagonality-law-panel/scripts/panel_data.py from the papers\' own study files (values unchanged).\n'
    'export const LAW_CHARTS = ' + json.dumps(C, ensure_ascii=False) + ';\nexport default LAW_CHARTS;\n')
print(len(C), 'charts', sum(len(s['points']) for c in C for s in c['series']), 'points', sum('word' in q for c in C for s in c['series'] for q in s['points']), 'buildable')
