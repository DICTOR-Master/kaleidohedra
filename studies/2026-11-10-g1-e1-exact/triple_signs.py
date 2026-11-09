"""Threshold proof, feasibility (DICTO 10 Nov 2026: 'prove the threshold curve'). Over the two-slope family with (b), (c) on a grid
of (u, v) in [0.60, 0.86]^2, evaluate every triple of the 27 lines (concurrency determinant) and list the triples whose sign
CHANGES somewhere (besides those identically zero). If only the threshold triple (t4 right leg, t5 base, t6 right leg) and its
mirror change sign, a certified proof can use 'no other degeneracy'; otherwise each extra crossing must be handled.
usage: python -u triple_signs.py STEP"""
import sys, itertools, json, time
sys.path.insert(0, '.')
import mpmath as mp
mp.mp.dps = 30
from rhombus import yantra, extra
from model import det3
step = mp.mpf(sys.argv[1]); grid = [mp.mpf('0.60') + step * i for i in range(int(mp.mpf('0.26') / step) + 1)]
def lines(t):
    b, w, a = t['b'], t['w'], t['a']; L = {}
    for i in range(1, 10):
        L[f'B{i}'] = ((-w[i], b[i]), (w[i], b[i])); L[f'R{i}'] = ((w[i], b[i]), (0, a[i])); L[f'L{i}'] = ((-w[i], b[i]), (0, a[i]))
    return L
names = None; signs = {}; mins = {}
T0 = time.time()
for u in grid:
    guess = (mp.mpf('0.55'), mp.mpf('0.92'))
    for v in grid:
        Q, S = mp.findroot(lambda Q, S: extra(yantra(u, v, Q, S))[:2], guess, tol=mp.mpf(10)**-25); guess = (Q, S)
        L = lines(yantra(u, v, Q, S)); names = names or sorted(L)
        for tr in itertools.combinations(names, 3):
            d = det3(L[tr[0]], L[tr[1]], L[tr[2]])
            if abs(d) < mp.mpf(10)**-20: signs.setdefault(tr, set()).add(0); continue
            # where do the lines meet nearly? use the meeting of the first two; count only if it lies on all three drawn segments
            (p1, p2), (q1, q2) = L[tr[0]], L[tr[1]]
            den = (p2[0]-p1[0])*(q2[1]-q1[1]) - (p2[1]-p1[1])*(q2[0]-q1[0])
            if abs(den) < mp.mpf(10)**-20: continue
            lam = ((q1[0]-p1[0])*(q2[1]-q1[1]) - (q1[1]-p1[1])*(q2[0]-q1[0])) / den
            X = (p1[0] + lam*(p2[0]-p1[0]), p1[1] + lam*(p2[1]-p1[1]))
            def on(seg, tol=mp.mpf('0.02')):
                (a1, a2) = seg; vx, vy = a2[0]-a1[0], a2[1]-a1[1]; L2 = vx*vx + vy*vy
                tt = ((X[0]-a1[0])*vx + (X[1]-a1[1])*vy) / L2
                dist = abs((X[0]-a1[0])*vy - (X[1]-a1[1])*vx) / mp.sqrt(L2)
                return -tol <= tt <= 1 + tol and dist < mp.mpf('0.01')
            if not all(on(L[n]) for n in tr): continue
            signs.setdefault(tr, set()).add(1 if d > 0 else -1); mins[tr] = min(mins.get(tr, 1), abs(d))
    print(f'[{time.time()-T0:5.0f} s] u = {float(u):.3f}', flush=True)
ident = [tr for tr, ss in signs.items() if ss == {0}]
change = [tr for tr, ss in signs.items() if {1, -1} <= ss]
touch = [tr for tr, ss in signs.items() if 0 in ss and ss != {0} and not ({1, -1} <= ss)]
print('identically zero (Huet conditions, parallels):', len(ident))
print('sign changes inside the region:', len(change), change)
print('touch zero without changing sign:', len(touch), touch[:10])
json.dump({'change': change, 'touch': touch, 'ident': len(ident)}, open('triple-signs.json', 'w'))
print('FINAL ok' if change else 'FINAL FAIL: no sign change found (expected at least the threshold triple)')
