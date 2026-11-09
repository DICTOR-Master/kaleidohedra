"""E1 refined (DICTO 10 Nov 2026). Finding: E1 lies on the edge where t4's right leg meets t5's corner (the three lines of the
rhombus threshold: t4 right leg, t5 base, t6 right leg), to 2e-10 at double precision. So E1 = the most even yantra ON that edge:
C(u, v, Q, S) = 0 fixes S, and the spread of the 43 areas is minimised over (u, v, Q). Here at 40 digits: S from C = 0 by
findroot, gradient and Hessian by central differences, Newton steps. Reports the refined E1, its gradient, the Hessian's
eigenvalues (all > 0: a true minimum on the edge) and the spread. usage: ~/geom/bin/python -u e1_refine.py"""
import sys, json, time
sys.path.insert(0, '.')
import mpmath as mp
from model import solve, order_ok, det3
import figure as FG
mp.mp.dps = 90
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
def tri(u, v, Q, S):
    P = v * v / (1 + v * v); R = 1 / (1 + u * u)
    return solve(P, Q, R, S, v / (1 + v * v), u / (1 + u * u), mp.sqrt, root=1)
def C(u, v, Q, S):
    t = tri(u, v, Q, S); b, w, a = t['b'], t['w'], t['a']
    return det3(((w[4], b[4]), (0, a[4])), ((-w[5], b[5]), (w[5], b[5])), ((w[6], b[6]), (0, a[6])))
Sg = [None]
def Sof(u, v, Q):
    Sg[0] = mp.findroot(lambda S: C(u, v, Q, S), Sg[0], tol=mp.mpf(10)**-85); return Sg[0]
def spread(x):
    u, v, Q = x; S = Sof(u, v, Q); t = tri(u, v, Q, S); b, w, a = t['b'], t['w'], t['a']
    pts, fs = FG.faces(FG.segments(b, w, a)); A = []
    for f in fs:
        poly = [pts[k] for k in f]; ar = FG.area(poly)
        if ar >= -mp.mpf(10)**-60: continue
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        if sum(FG.inside_tri((cx, cy), b, w, a, i) for i in range(1, 10)) % 2: A.append(-ar)
    if len(A) != 43: raise ValueError(f'{len(A)} odd pieces')
    m = sum(A) / 43; return mp.sqrt(sum((x - m)**2 for x in A) / 43) / m
E = json.load(open('even.json'))['E1']
u0, v0 = mp.mpf(E['u']), mp.mpf(E['v']); b6 = mp.mpf(E['b']['6']['a']); Sg[0] = mp.mpf(E['b']['9']['a'])
x = [u0, v0, b6]; say('start spread', mp.nstr(spread(x), 12), 'S', mp.nstr(Sg[0], 12))
h = mp.mpf(10)**-25
for it in range(8):
    f0 = spread(x); g = []; H = mp.matrix(3, 3)
    for i in range(3):
        e = [h if k == i else 0 for k in range(3)]
        fp = spread([x[k] + e[k] for k in range(3)]); fm = spread([x[k] - e[k] for k in range(3)])
        g.append((fp - fm) / (2 * h)); H[i, i] = (fp - 2 * f0 + fm) / h**2
    for i in range(3):
        for j in range(i + 1, 3):
            pp = spread([x[k] + (h if k in (i, j) else 0) for k in range(3)]); mm = spread([x[k] - (h if k in (i, j) else 0) for k in range(3)])
            pm = spread([x[k] + (h if k == i else -h if k == j else 0) for k in range(3)]); mp_ = spread([x[k] + (-h if k == i else h if k == j else 0) for k in range(3)])
            H[i, j] = H[j, i] = (pp - pm - mp_ + mm) / (4 * h * h)
    step = mp.lu_solve(H, mp.matrix(g)); x = [x[k] - step[k] for k in range(3)]
    say(f'iter {it}: spread {mp.nstr(f0, 15)}  |grad| {mp.nstr(mp.norm(mp.matrix(g)), 3)}  |step| {mp.nstr(mp.norm(step), 3)}')
    if mp.norm(step) < mp.mpf(10)**-40: break
ev = mp.eig(H)[0]
u, v, Q = x; S = Sof(u, v, Q)
say('E1 refined: u', mp.nstr(u, 25), 'v', mp.nstr(v, 25), 'Q', mp.nstr(Q, 25), 'S', mp.nstr(S, 25))
say('spread/mean', mp.nstr(spread(x), 15), '; Hessian eigenvalues', [mp.nstr(mp.re(e), 4) for e in ev])
json.dump({'u': str(u), 'v': str(v), 'Q': str(Q), 'S': str(S), 'spread': str(spread(x)), 'hessian_eig': [str(mp.re(e)) for e in ev]}, open('e1-refined.json', 'w'))
print('FINAL ok' if all(mp.re(e) > 0 for e in ev) else 'FINAL FAIL: not a minimum on the edge')
