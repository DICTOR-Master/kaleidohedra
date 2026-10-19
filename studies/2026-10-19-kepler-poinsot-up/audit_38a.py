# Number audit for paper #38a (DICTO 2026-10-19, "get all details exact"): every computed statement in the paper, re-derived exactly here
# in Q(sqrt5) and compared with the text. Any FAIL blocks publishing.
import os, sys, re, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '2026-10-19-five-fold-octet'))
exec(open(os.path.join(HERE, 'exact_kp.py')).read().split('def shell(')[0])
from exact_shells import cross
from exact_inner import piece
paper = open(os.path.join(HERE, '..', '..', 'papers', '2026-10-19-kepler-poinsot-pitet', 'paper.html')).read()
res = []
def check(name, ok, in_text=None):
    t = True if in_text is None else (in_text in paper)
    res.append((name, ok and t)); print(('PASS' if ok and t else 'FAIL'), name, '' if t else f'  [text missing: {in_text!r}]')
p2 = PHI * PHI; p3 = p2 * PHI
d2 = lambda a, b: dot(sub(a, b), sub(a, b))
emin = lambda S: min((d2(a, b) for a, b in itertools.combinations(S, 2)), key=lambda q: q.f())
check('I has edge 1', emin(I) == Q5(1), 'icosahedron I of edge 1')
check('D1 has edge phi', emin(D1) == p2, 'dodecahedral hull of edge φ')
check('hull of small star has edge phi^3', emin(I2) == p3 * p3, 'icosahedral hull of edge φ³')
check('I2 = phi^3 I', log['I2_is_phi3_I'])
vI = hullH(I)['V']; vD1 = hullH(D1)['V']
sp = [piece(F + [t]) for F, t in gsd]; ss = [piece(F + [t]) for F, t in ssd]
check('20 spikes, 12 spires', len(sp) == 20 and len(ss) == 12, '20 spikes')
check('each spike = I/10', all(p['V'] * 10 == vI for p in sp), 'each spike = I/10')
check('great star = 3 x I', vI + sum((p['V'] for p in sp), Q5(0)) == 3 * vI, '3 (each spike = I/10)')
check('small star = sqrt5 x D1', vD1 + sum((p['V'] for p in ss), Q5(0)) == Q5(0, 1) * vD1, '√5 (12 spires = (√5 − 1)·D1)')
check('12 spires = (sqrt5-1) D1', sum((p['V'] for p in ss), Q5(0)) == Q5(-1, 1) * vD1)
check('spike volume 1/8 + sqrt5/24', sp[0]['V'] == Q5(Fr(1, 8), Fr(1, 24)), '1/8 + √5/24')
check('spire volume 5/3 + 3sqrt5/4', ss[0]['V'] == Q5(Fr(5, 3), Fr(3, 4)), '5/3 + 3√5/4')
import json
kp = json.load(open(os.path.join(HERE, 'exact_kp.json')))
g, s_ = kp['great stellated shell: volumes'], kp['small stellated shell: volumes']
check('cap 5/8 + 7sqrt5/24', g['inward_pyramid'] == '5/8+7/24r5', '5/8 + 7√5/24')
check('AXE 1/6 + sqrt5/12', g['valley_tet'] == '1/6+1/12r5', '1/6 + √5/12')
check('small inward 29/24 + 13sqrt5/24', s_['inward_pyramid'] == '29/24+13/24r5', '29/24 + 13√5/24')
check('small tet 3/4 + sqrt5/3', s_['valley_tet'] == '3/4+1/3r5', '3/4 + √5/3')
check('fills exact, no overlap (both shells)', all(kp[k]['sum_equals_gap'] and kp[k]['pairs_not_separated'] == 0 for k in kp if 'valleys' in k))
# spire heights and the reciprocal pairs
def ratio2(F, apex):
    c = cent(F); n = cross(sub(F[1], F[0]), sub(F[2], F[0])); hn = dot(sub(apex, c), n); return hn * hn / dot(n, n) / d2(F[0], c)
check('spike (h/r)^2 = phi^4 = 7/2+3sqrt5/2', ratio2(*gsd[0]) == p2 * p2, '7/2 + 3√5/2 = φ⁴')
check('spire (h/r)^2 = phi^2', ratio2(*ssd[0]) == p2, '3/2 + √5/2 = φ²')
HD = hullH(D1); o, i = HD['F'][0]; F = [HD['C'][j] for j in o]; n, d = HD['H'][i]; c = max(I, key=lambda v: dot(n, v).f())
check('cap (h/r)^2 = phi^-2', ratio2(F, c) * p2 == Q5(1), '3/2 − √5/2 = φ⁻²')
HI2 = hullH(I2); o, i = HI2['F'][0]; F = [HI2['C'][j] for j in o]; n, d = HI2['H'][i]; c = max(D1, key=lambda v: dot(n, v).f())
check('small inward (h/r)^2 = phi^-4', ratio2(F, c) * p2 * p2 == Q5(1), '7/2 − 3√5/2 = φ⁻⁴')
# the spikes' sides lie in 12 planes (the pentagram planes)
pl = set()
for F, t in gsd:
    for a, b in itertools.combinations(F, 2):
        n = cross(sub(b, a), sub(t, a)); dd = dot(n, a)
        if dd.sign() < 0: n, dd = tuple(-x for x in n), -dd
        k = n[0] if n[0] != Q5(0) else (n[1] if n[1] != Q5(0) else n[2]); pl.add((tuple(repr(x / k) for x in n), repr(dd / k)))
check('great-star spike sides fall into 12 planes', len(pl) == 12, 'twelve pentagram planes')
# figure 1 caption: a fourth turn inward is 1/phi^9 ~ 1/76 of the outer size
check('fourth turn inward = 1/phi^9 ~ 1/76', abs(1 / ((1 + 5 ** .5) / 2) ** 9 - 1 / 76.013) < 1e-4, '1/76')
print('ALL PASS' if all(ok for _, ok in res) else f'{sum(not ok for _, ok in res)} FAIL')
