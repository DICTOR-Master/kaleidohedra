"""The rhombus yantra without the two tiny extra pieces (DICTO 10 Nov 2026: 'compute the exact slope').
Family: u = v (equal great triangles, DICTO's rhombus) with (b), (c) (t1's and t9's base corners on the circle). At u = 1/sqrt2
(stella) the yantra has 43 odd pieces, at Kulaichev's u = 0.75044 and at 3/4 it has 45. Between them three lines that bound
the tiny piece become concurrent: that slope u* is where the tiny pieces are born. Find the three lines, solve u* to 50 digits,
check the counts on both sides, report (d) and admissibility there.  usage: python rhombus_threshold.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import mpmath as mp
from rhombus import yantra, extra
from model import order_ok, det3
from figure import segments, faces, area, corners_of, inside_tri
mp.mp.dps = 60
guess = [mp.mpf('0.55'), mp.mpf('0.92')]
def solved(k):
    Q, S = mp.findroot(lambda Q, S: extra(yantra(k, k, Q, S))[:2], tuple(guess), tol=mp.mpf(10)**-50)
    guess[:] = [Q, S]; return yantra(k, k, Q, S), Q, S
def lines(t):
    b, w, a = t['b'], t['w'], t['apex'] if 'apex' in t else t['a']
    L = {}
    for i in range(1, 10):
        L[('base', i)] = ((-w[i], b[i]), (w[i], b[i]))
        L[('right', i)] = ((w[i], b[i]), (0, a[i])); L[('left', i)] = ((-w[i], b[i]), (0, a[i]))
    return L
def census(t):
    b, w, a = ({i: float(x) for i, x in t[k].items()} for k in ('b', 'w', 'apex' if 'apex' in t else 'a'))
    pts, fs = faces(segments(b, w, a)); odd = []
    for f in fs:
        poly = [pts[k] for k in f]; ar = area(poly)
        if ar >= -1e-14: continue
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        if sum(inside_tri((cx, cy), b, w, a, i) for i in range(1, 10)) % 2: odd.append((corners_of(poly), -ar, cx, cy))
    return odd
def onl(p, l):
    (x1, y1), (x2, y2) = l
    return abs((x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)) / float(mp.hypot(x2 - x1, y2 - y1))
# 1. the three lines of the tiny right-hand piece at u = 3/4
t, Q, S = solved(mp.mpf(3) / 4)
odd = census(t); tiny = min((o for o in odd if o[2] > 0), key=lambda o: o[1])
L = lines(t); V = tiny[0]
three = [k for k, l in L.items() if sum(onl(p, tuple((float(c[0]), float(c[1])) for c in l)) < 1e-9 for p in V) >= 2]
print('odd pieces at u = 3/4:', len(odd), '; tiny piece area', tiny[1], 'bounded by', three)
assert len(three) == 3
F = lambda k: det3(*(lines(solved(k)[0])[n] for n in three))
lo, hi = 1 / mp.sqrt(2), mp.mpf(3) / 4
print('sign at stella 1/sqrt2:', mp.sign(F(lo)), ' at 3/4:', mp.sign(F(hi)))
guess[:] = [mp.mpf('0.55'), mp.mpf('0.92')]; F(lo)
# scan for the sign change (continuation from the stella end)
ks = [lo + (hi - lo) * j / 200 for j in range(201)]; vals = []
for k in ks: vals.append(F(k))
ch = [j for j in range(200) if mp.sign(vals[j]) != mp.sign(vals[j + 1])]
print('sign changes between stella and 3/4 at steps', ch)
j = ch[-1]; a_, b_ = ks[j], ks[j + 1]; guess[:] = [solved(a_)[1], solved(a_)[2]]
us = mp.findroot(F, (a_, b_), solver='anderson', tol=mp.mpf(10)**-55)
t, Q, S = solved(us)
print('u* =', mp.nstr(us, 50)); print('   Q =', mp.nstr(Q, 30), ' S =', mp.nstr(S, 30))
print('   apex angle 2 atan u* =', mp.nstr(2 * mp.degrees(mp.atan(us)), 15), 'deg; admissible:', order_ok(t, mp.mpf(10)**-40))
print('   (d) bindu centre offset:', mp.nstr(extra(t)[2], 8), '(Kulaichev 0, Rh345 2.36e-5)')
for k in (us - mp.mpf(10)**-4, us + mp.mpf(10)**-4):
    guess[:] = [Q, S]; tt = solved(k)[0]; o = census(tt)
    print(f'   u = u* {"-" if k < us else "+"} 1e-4: {len(o)} odd pieces, {sum(len(x[0]) == 3 for x in o)} triangles')
oc = census(t); print('   at u* itself:', len(oc), 'odd pieces (three lines meet: a 19th triple point)')
import json; json.dump({'u_star': str(us), 'Q': str(Q), 'S': str(S), 'lines': [list(x) for x in three]}, open('../data/rhombus-threshold.json', 'w'))
print('FINAL ok' if ch and order_ok(t, mp.mpf(10)**-40) else 'FINAL FAIL')
