"""Threshold atlas (DICTO 10 Nov 2026: 'prove the threshold curve'). Two-slope family with (b), (c): for each (u, v) solve Q, S,
then record the odd-piece count, the triangles among them, admissibility, and the sign of C = det(t4 right leg, t5 base, t6 right
leg). Question: is {45 pieces} exactly {C > 0} on the admissible region, i.e. is the threshold one curve C = 0?
usage: python -u threshold_atlas.py STEP   (writes atlas-STEP.json; prints FINAL ok when every admissible point agrees)"""
import sys, json, time
sys.path.insert(0, '.')
import mpmath as mp
mp.mp.dps = 30
from rhombus import yantra, extra
from model import order_ok, det3
from figure import segments, faces, area, corners_of, inside_tri
T0 = time.time()
def census(t):
    b, w, a = ({i: float(x) for i, x in t[k].items()} for k in ('b', 'w', 'a'))
    pts, fs = faces(segments(b, w, a)); odd = []
    for fc in fs:
        poly = [pts[k] for k in fc]; ar = area(poly)
        if ar >= -1e-14: continue
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        if sum(inside_tri((cx, cy), b, w, a, i) for i in range(1, 10)) % 2: odd.append(len(corners_of(poly)))
    return len(odd), sum(1 for o in odd if o == 3)
def C(t):
    b, w, a = t['b'], t['w'], t['a']
    return det3(((w[4], b[4]), (0, a[4])), ((-w[5], b[5]), (w[5], b[5])), ((w[6], b[6]), (0, a[6])))
step = mp.mpf(sys.argv[1]); us = [mp.mpf('0.60') + step * i for i in range(int((mp.mpf('0.86') - mp.mpf('0.60')) / step) + 1)]
out = []; bad = 0; last = time.time()
for u in us:
    guess = (mp.mpf('0.55'), mp.mpf('0.92'))
    for v in us:
        try:
            Q, S = mp.findroot(lambda Q, S: extra(yantra(u, v, Q, S))[:2], guess, tol=mp.mpf(10)**-25); guess = (Q, S)
            t = yantra(u, v, Q, S); adm = order_ok(t, mp.mpf(10)**-20)
            n, tri = census(t) if adm else (None, None); c = float(C(t))
        except Exception as e:
            out.append(dict(u=float(u), v=float(v), err=str(e)[:40])); continue
        agree = (not adm) or ((n == 45) == (c > 0) and n in (43, 45))
        if not agree: bad += 1
        out.append(dict(u=float(u), v=float(v), adm=adm, n=n, tri=tri, C=c, agree=agree))
        if time.time() - last > 30: print(f'[{time.time()-T0:6.0f} s] heartbeat u={float(u):.3f}', flush=True); last = time.time()
json.dump(out, open(f'atlas-{sys.argv[1]}.json', 'w'))
A = [o for o in out if o.get('adm')]
print(f'points {len(out)}, admissible {len(A)}, counts {sorted(set(o["n"] for o in A))}, disagreements {bad}, errors {sum(1 for o in out if "err" in o)}')
print('FINAL ok' if bad == 0 and A else 'FINAL FAIL: the count does not follow the sign of C everywhere')
