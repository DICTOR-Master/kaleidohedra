"""DICTO 11-08: the DICTO Yantra seems best 'because there are more hidden triangles from overlaps that aren't possible on other
figures'. Count EVERY triangle the 27 sides make (any three sides meeting pairwise at three distinct points, composite triangles
included), for each yantra. A triple whose three sides meet in ONE point (a marma) makes no triangle. Huet's classical from model.py."""
import json, math, itertools
from fractions import Fraction
from model import solve
def load(f, k):
    e = json.load(open('../figures/' + f))[k]; g = lambda d: {int(i): float(v['a']) if isinstance(v, dict) else float(v) for i, v in d.items()}
    return g(e['b']), g(e['w']), g(e['apex'])
def huet():
    P, R = 0.332, 0.602; t = solve(P, 0.537, R, 0.835, math.sqrt(P * (1 - P)), math.sqrt(R * (1 - R)), math.sqrt, root=1)
    return t['b'], t['w'], t['a']
def segs(b, w, a):
    S = []
    for i in range(1, 10):
        L, Rr, A = (-w[i], b[i]), (w[i], b[i]), (0.0, a[i]); S += [(L, Rr), (L, A), (Rr, A)]
    return S
def meet(s, t, eps=1e-9):
    (x1, y1), (x2, y2) = s; (x3, y3), (x4, y4) = t
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-14: return None
    u = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d; v = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    if -eps <= u <= 1 + eps and -eps <= v <= 1 + eps: return (x1 + u * (x2 - x1), y1 + u * (y2 - y1))
    return None
def count(b, w, a):
    S = segs(b, w, a); n = len(S); M = {}
    for i, j in itertools.combinations(range(n), 2):
        p = meet(S[i], S[j])
        if p: M[i, j] = p
    c = 0
    for i, j, k in itertools.combinations(range(n), 3):
        if (i, j) in M and (i, k) in M and (j, k) in M:
            p, q, r = M[i, j], M[i, k], M[j, k]
            if abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) > 1e-10: c += 1
    return c
cases = [('DICTO Yantra (GF1)', load('golden_family.json', 'GF1')), ('most even E1', load('even.json', 'E1')),
         ('middle way E2', load('even2.json', 'E2')), ('Cleo-Octangula K1', load('kites.json', 'K1')),
         ('Cleo rhombus (45 pieces)', load('cleo-yantra.json', 'Cleo')), ('perfect stella PF2', load('perfect.json', 'PF2')),
         ('Huet classical (approx.)', huet())]
res = []
for name, (b, w, a) in cases:
    c = count(b, w, a); res.append(c); print(f'{name:28s} all triangles: {c}', flush=True)
print('FINAL ok' if all(c > 43 for c in res) else 'FINAL FAIL: a count below the 43 pieces')
