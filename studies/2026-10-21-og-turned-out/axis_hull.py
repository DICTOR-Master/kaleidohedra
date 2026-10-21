# DICTO 2026-10-21: what each symmetry axis leaves the solid through, on the HULL of each solid of the OG's downward family, EXACT in
# Q(sqrt5), fast enough for the large solids (down 8 to 11). The solid is the hull of the points D_k (golden-long-solids.pkl), with exact
# face planes H = solid(D_k). Along an axis a, the solid ends at t* a, t* = min d/(n.a) over the planes with n.a > 0; the planes reaching
# that minimum decide: one plane square to a -> a face; a hull corner at t* a (a point of D_k lying on three planes with independent normals)
# -> a corner; otherwise exactly two planes -> the inside of an edge. At a two-fold edge, the two faces there (their corners: the hull corners
# on each plane), their shapes, and the ribbon test of ribbons_return.py, using the 60 rotations: the pair is a ribbon when both faces are
# congruent isosceles trapezoids sharing their shorter parallel side and the trapezoid's orbit has 60 faces (so 30 such pairs).
# Cross-check: down 8 (also done by ribbons_return.py with full face lists).   usage: python3 axis_hull.py <five-fold-octet>  (env KS=8,9,10)
import sys, os, json, pickle
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
from exact_shells import det3v
import numpy as np
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
D = pickle.load(open(os.path.join(HERE, 'golden-long-solids.pkl'), 'rb'))
KS = [int(x) for x in os.environ.get('KS', '8,9,10').split(',')]
names = ['OG', 'TPH', 'TQH', 'TQP', 'TQHD'] + [f'down {k}' for k in range(5, 13)]
Z0 = Q5(0); one = Q5(1)
AX = {'5-fold': (Z0, one, PHI), '3-fold': (one, one, one), '2-fold': (Z0, Z0, one)}
zero = lambda u: all(x == Z0 for x in u)
d2 = lambda a, b: dot(sub(a, b), sub(a, b))
par = lambda a, b, c, d: zero(cross(sub(b, a), sub(d, c)))
def corner(v, H):
    on = [n for n, d in H if dot(n, v) == d]
    return any(det3v(a, b, c) != Z0 for i, a in enumerate(on) for j, b in enumerate(on[i + 1:], i + 1) for c in on[j + 1:])
def face_of(n, d, S, H):
    F = [v for v in S if dot(n, v) == d and corner(v, H)]
    P = np.array([[x.f() for x in v] for v in F]); c = P.mean(0); B = np.linalg.svd(P - c)[2][:2]
    return [F[k] for k in np.argsort(np.arctan2((P - c) @ B[1], (P - c) @ B[0]))]
def shape(P):
    n = len(P); s = [d2(P[i], P[(i + 1) % n]) for i in range(n)]; eq = len({repr(x) for x in s})
    if n == 3: return 'equilateral triangle' if eq == 1 else 'isosceles triangle' if eq == 2 else 'scalene triangle'
    if n == 4:
        p02, p13 = par(P[0], P[1], P[3], P[2]), par(P[1], P[2], P[0], P[3])
        if p02 and p13: return 'rhombus' if eq == 1 else 'parallelogram'
        if p02 or p13:
            r = 0 if p02 else 1; return 'isosceles trapezoid' if s[r + 1] == s[(r + 3) % 4] else 'trapezoid'
        return 'kite' if (s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0]) else 'quadrilateral'
    return f'{n}-gon'
res = {}
for k in KS:
    S = D[k]; H = solid(S); row = {}
    for an, a in AX.items():
        cand = [(d / dot(n, a), n, d) for n, d in H if dot(n, a).sign() > 0]
        t = min(cand, key=lambda x: x[0].f())[0]; t = min((x[0] for x in cand), key=lambda q: q.f())
        assert all((x[0] - t).sign() >= 0 for x in cand)
        top = [(n, d) for tt, n, d in cand if tt == t]; p = tuple(t * x for x in a)
        if any(zero(cross(n, a)) for n, _ in top): row[an] = 'face'
        elif any(v == p for v in S) and corner(p, H): row[an] = 'corner'
        else:
            assert len(top) == 2; row[an] = 'edge'
            if an == '2-fold':
                F1, F2 = [face_of(n, d, S, H) for n, d in top]; sh = [shape(F1), shape(F2)]
                same = sorted(repr(d2(F1[i], F1[(i + 1) % len(F1)])) for i in range(len(F1))) == sorted(repr(d2(F2[i], F2[(i + 1) % len(F2)])) for i in range(len(F2)))
                shared = [v for v in F1 if v in F2]; rib = False; which = '-'
                if sh == ['isosceles trapezoid'] * 2 and same and len(shared) == 2:
                    s4 = [d2(F1[i], F1[(i + 1) % 4]) for i in range(4)]; r = 0 if par(F1[0], F1[1], F1[3], F1[2]) else 1
                    lo, hi = sorted([s4[r], s4[r + 2]], key=lambda q: q.f()); e = d2(*shared)
                    which = 'shorter parallel side' if e == lo else 'longer parallel side' if e == hi else 'leg'
                    orbit = {frozenset(app(M, v) for v in F1) for M in G}
                    rib = which == 'shorter parallel side' and len(orbit) == 60
                row['2-fold edge'] = {'faces': sh, 'congruent': same, 'shared_edge': which, 'ribbon': rib}
    nc = sum(1 for v in S if corner(v, H))
    res[names[k]] = {'points': len(S), 'corners': nc, 'faces': len(H), 'word': row}
    e = row.get('2-fold edge')
    ok(True, f"{names[k]}: {len(S)} points, hull {nc} corners, {len(H)} faces; " + ', '.join(f'{an}: {row[an]}' for an in AX) +
       (f"; at the two-fold edge: {e['faces'][0]} + {e['faces'][1]}" + (' (congruent)' if e['congruent'] else '') + (f", sharing their {e['shared_edge']}" if e['shared_edge'] != '-' else '') + (': a ribbon as on the TQH' if e['ribbon'] else ': not a ribbon') if e else ''))
    json.dump(res, open(os.path.join(HERE, 'axis-hull.json'), 'w'), indent=1)
