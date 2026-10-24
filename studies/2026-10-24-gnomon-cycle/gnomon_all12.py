# Gnomon table, all twelve stations exact (DICTO 2026-10-24, item A). Adds the two stations without exact volumes in gnomon_table.py:
# rTI (core of the H–O compound) and jtI (hull, = hull(TI ∪ PD), PD = TI's polar in ρ² = 9/4, Progenitors tih_v2_check.py).
# rTI and TI corners from studies/2026-10-16-progenitors/data/full-cycle.json are snapped to a + b√5 (a, b in (1/16)Z, error < 1e-6
# checked); PD's corners are computed exactly as the poles of TI's face planes; volume = exact sum of origin tetrahedra over hull triangles.
# Station order as in the Progenitors render (twelve=1): I ⊂ Cleo star ⊂ D′ ⊂ ID ⊂ O ⊂ rTI ⊂ TI ⊂ H ⊂ jtI ⊂ RT ⊂ M ⊂ I·φ³.
# Cross-check: the same method on TI, H, RT, Ip3 must reproduce gnomon_table.py's exact values (same scale).
import json, itertools, sys, numpy as np
from fractions import Fraction as F
from scipy.spatial import ConvexHull
sys.path.insert(0, __file__.rsplit('/', 1)[0])
class Q:
    def __init__(s, a, b=0): s.a, s.b = F(a), F(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    def __truediv__(s, o): o = o if isinstance(o, Q) else Q(o); n = o.a*o.a - 5*o.b*o.b; return s * Q(o.a / n, -o.b / n)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __float__(s): return float(s.a) + float(s.b) * 5 ** .5
    def __repr__(s): return f'{s.a}' + (f' + {s.b}√5' if s.b else '')
def snap(x):
    best = None
    for b16 in range(-80, 81):
        b = F(b16, 16); a = F(round((x - float(b) * 5 ** .5) * 16), 16); e = abs(float(a) + float(b) * 5 ** .5 - x)
        if best is None or e < best[0] - 1e-12 or (abs(e - best[0]) < 1e-12 and abs(b16) < abs(best[1].b * 16)): best = (e, Q(a, b))
    assert best[0] < 1e-6, (x, best); return best[1]
def det(p, q, r): return p[0]*(q[1]*r[2]-q[2]*r[1]) - p[1]*(q[0]*r[2]-q[2]*r[0]) + p[2]*(q[0]*r[1]-q[1]*r[0])
def exact_volume(V, X=None):
    V = np.array(V); h = ConvexHull(V); X = X or [[snap(c) for c in v] for v in V]; tot = Q(0)
    for s, eq in zip(h.simplices, h.equations):
        a, b, c = (V[i] for i in s)
        if np.dot(np.cross(b - a, c - a), eq[:3]) < 0: s = s[[0, 2, 1]]
        tot = tot + det(*(X[i] for i in s))
    return tot / 6, h.volume
st = json.load(open(__file__.rsplit('/', 3)[0] + '/studies/2026-10-16-progenitors/data/full-cycle.json'))['st']
phi = Q(F(1, 2), F(1, 2)); I = Q(F(-5, 12), F(5, 12))
known = {'TI': Q(F(-35, 4), F(39, 4)), 'H': Q(F(-365, 4), F(189, 4)), 'RT': Q(-135, F(135, 2)), 'Ip3': Q(F(235, 12), F(35, 4))}
ok = []
scale = None
for k, ref in known.items():
    v, fv = exact_volume(st[k]['v']); r = ref / v
    if scale is None: scale = r
    ok.append((f'method check {k}: same scale as the table (ratio {r})', r == scale and abs(float(v) - fv) < 1e-5))
new = {}
v, fv = exact_volume(st['rTI']['v']); new['rTI'] = v * scale; ok.append((f'rTI exact volume agrees with float hull ({float(v):.6f} vs {fv:.6f})', abs(float(v) - fv) < 1e-5))
TV = np.array(st['TI']['v']); TX = [[snap(c) for c in v] for v in TV]; th = ConvexHull(TV); PD = {}
for sx, eq in zip(th.simplices, th.equations):
    key = tuple(np.round(eq, 6))
    if key in PD: continue
    a, b, c = (TX[i] for i in sx); u = [b[i] - a[i] for i in range(3)]; w = [c[i] - a[i] for i in range(3)]
    n = [u[1]*w[2] - u[2]*w[1], u[2]*w[0] - u[0]*w[2], u[0]*w[1] - u[1]*w[0]]; d = n[0]*a[0] + n[1]*a[1] + n[2]*a[2]
    PD[key] = [x * Q(F(9, 4)) / d for x in n]
PD = list(PD.values()); ok.append((f'TI has 32 face planes -> PD has 32 corners ({len(PD)})', len(PD) == 32))
JX = TX + PD; JV = np.array([[float(x) for x in p] for p in JX])
hf = np.array(st['hull']['v']); jh = ConvexHull(JV)
ok.append(('hull(TI ∪ PD) corners = the study\'s jtI corners (float, 1e-5)', len(jh.vertices) == len(hf) and all(np.min(np.linalg.norm(hf - JV[i], axis=1)) < 1e-5 for i in jh.vertices)))
v, fv = exact_volume(JV, JX); new['hull'] = v * scale; ok.append((f'jtI exact volume agrees with float hull ({float(v):.6f} vs {fv:.6f})', abs(float(v) - fv) < 1e-5))
lay = {'I→ID': Q(F(65, 16), F(59, 48)), 'ID→O': Q(F(625, 912), F(289, 912))}
ID = I + lay['I→ID']; O = ID + lay['ID→O']
stations = [('I', I), ('Cleo star', I * 2), ("D′", Q(F(10, 9), F(14, 27))), ('ID', ID), ('OG', O), ('rTI (core)', new['rTI']), ('TI', known['TI']),
            ('H', known['H']), ('jtI (hull)', new['hull']), ('RT', known['RT']), ('M', Q(F(145, 12), F(65, 12))), ('I·φ³', known['Ip3'])]
vals = [float(v) for _, v in stations]
ok.append(('the twelve stations grow strictly in volume in this order', all(a < b for a, b in zip(vals, vals[1:]))))
pw = [Q(1)]
for _ in range(12): pw.append(pw[-1] * phi)
def name(r):
    for k, p in enumerate(pw):
        if r == p: return f'φ^{k}'
    if r.b == 0: return 'rational'
    for k, p in enumerate(pw[1:], 1):
        q = r / p
        if q.b == 0: return f'{q.a}·φ^{k}'
        q = r * p
        if q.b == 0: return f'{q.a}/φ^{k}'
    return ''
print(f'{"station":11s} {"volume (exact)":28s} {"× I":>9s}  {"/ I (exact)":26s} {"form":14s} {"step":>8s}  step form')
prev = None
for nm, V in stations:
    m = V / I; r = V / prev if prev else None
    print(f'{nm:11s} {str(V):28s} {float(m):9.4f}  {str(m):26s} {name(m):14s} ' + (f'{float(r):8.4f}  {name(r)}' if r else ''))
    prev = V
for t, k in ok: print(('PASS ' if k else 'FAIL ') + t)
print('ALL PASS' if all(k for _, k in ok) else 'SOME FAIL')
print('\nall pairs (later / earlier) that are rational, rational·φ^k or rational/φ^k:')
for (n1, v1), (n2, v2) in itertools.combinations(stations, 2):
    f = name(v2 / v1)
    if f: print(f'  {n2} / {n1} = {f}')
print('gnomons (later − earlier) that are rational multiples of I·φ^k:')
for (n1, v1), (n2, v2) in zip(stations, stations[1:]):
    f = name((v2 - v1) / I)
    print(f'  {n2} − {n1} = {f + " · I" if f else "(no neat form)"}  [{float((v2 - v1) / I):.4f} I]')
