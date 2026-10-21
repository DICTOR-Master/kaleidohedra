# DICTO 2026-10-21: do the ribbons return? At every solid of the OG's downward family where a two-fold axis passes through the inside of an
# edge (the "edge stations" of axis_words.py), EXACT in Q(sqrt5): the two faces that meet at that edge, their shapes, and whether they form a
# ribbon as on the TQH: two congruent isosceles trapezoids sharing their shorter parallel side, with every face of that kind paired so
# (30 ribbons, two per two-fold axis). Solids from golden-long-solids.pkl (exact, built by golden_exact_long.py). The pkl holds all foot points;
# the solid is their hull, so corners are taken from the hull (polytope), and the axis word (corner / face / edge on each axis, as in
# axis_words.py) is recomputed here from the hull corners, for every solid.
#   usage: python3 ribbons_return.py <studies/2026-10-19-five-fold-octet>
import sys, os, json, pickle
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
# The solid is the hull of the exact points S, so its corners are the points of S that lie on three face planes with independent
# normals (all exact), and each face is the corners on one face plane (ordered round the face by float angle only); closure and Euler
# are checked. This avoids the float corner guessing of the #38 helper, which fails on the large solids (down 9).
import numpy as np
from collections import Counter
from exact_shells import det3v
def hull_polytope(S):
    H = solid(S); C = []
    for v in S:
        on = [n for n, d in H if dot(n, v) == d]
        if any(det3v(a, b, c) != Q5(0) for i, a in enumerate(on) for j, b in enumerate(on[i + 1:], i + 1) for c in on[j + 1:]): C.append(v)
    faces = []
    for i, (n, d) in enumerate(H):
        f = [j for j, v in enumerate(C) if dot(n, v) == d]
        pts = np.array([[x.f() for x in C[j]] for j in f]); c = pts.mean(0); B = np.linalg.svd(pts - c)[2][:2]
        faces.append(([f[k] for k in np.argsort(np.arctan2((pts - c) @ B[1], (pts - c) @ B[0]))], i))
    edges = Counter(frozenset(e) for o, _ in faces for e in zip(o, o[1:] + o[:1]))
    assert all(m == 2 for m in edges.values()) and len(C) - len(edges) + len(faces) == 2
    return C, faces
FROM = int(os.environ.get('FROM', '0'))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
D = pickle.load(open(os.path.join(HERE, 'golden-long-solids.pkl'), 'rb'))
names = ['OG', 'TPH', 'TQH', 'TQP', 'TQHD'] + [f'down {k}' for k in range(5, 13)]
Z0 = Q5(0); a2 = (Z0, Z0, Q5(1)); AX = {'5-fold': (Z0, Q5(1), PHI), '3-fold': (Q5(1), Q5(1), Q5(1)), '2-fold': a2}
zero = lambda u: all(x == Z0 for x in u)
d2 = lambda a, b: dot(sub(a, b), sub(a, b))
par = lambda a, b, c, d: zero(cross(sub(b, a), sub(d, c)))
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
for k, S in enumerate(D):
    if k >= len(names): break
    if k < FROM: continue
    C, Fc = hull_polytope(S); faces = [tuple(C[j] for j in o) for o, _ in Fc]
    word = {}
    for an, ax in AX.items():
        word[an] = 'corner' if any(zero(cross(v, ax)) and dot(v, ax).sign() > 0 for v in C) else 'face' if any(zero(cross(n, ax)) and dot(n, ax).sign() > 0 for n, d in solid(S)) else 'edge'
    ok(True, f"{names[k]}: {len(S)} foot points, hull {len(C)} corners, {len(faces)} faces; axis word " + ', '.join(f'{an}: {w}' for an, w in word.items()))
    res[names[k]] = {'foot_points': len(S), 'corners': len(C), 'faces': len(faces), 'word': word}
    if word['2-fold'] != 'edge': continue
    hit = None
    for f in faces:
        for a, b in zip(f, f[1:] + f[:1]):
            m = tuple(x + y for x, y in zip(a, b))
            if zero(cross(m, a2)) and dot(m, a2).sign() > 0 and not zero(cross(sub(b, a), a2)): hit = (a, b)
    if hit is None: print(f'{names[k]}: the two-fold axis does not pass through an edge'); continue
    two = [f for f in faces if hit[0] in f and hit[1] in f]; shp = [shape(list(f)) for f in two]
    sides = [sorted(repr(d2(f[i], f[(i + 1) % len(f)])) for i in range(len(f))) for f in two]
    info = res[names[k]]; info.update({'faces_at_axis_edge': shp, 'congruent_sides': sides[0] == sides[1]})
    rib = False
    if all(s == 'isosceles trapezoid' for s in shp) and sides[0] == sides[1]:
        f = two[0]; s4 = [d2(f[i], f[(i + 1) % 4]) for i in range(4)]; r = 0 if par(f[0], f[1], f[3], f[2]) else 1
        short = min(s4[r], s4[r + 2], key=lambda q: q.f()); longp = max(s4[r], s4[r + 2], key=lambda q: q.f()); rib = d2(*hit) == short
        info['axis_edge_is'] = 'shorter parallel side' if d2(*hit) == short else 'longer parallel side' if d2(*hit) == longp else 'leg'
        tz = [g for g in faces if len(g) == 4 and sorted(repr(d2(g[i], g[(i + 1) % 4])) for i in range(4)) == sides[0]]; info['trapezoids_of_that_kind'] = len(tz)
        if rib:                                        # every trapezoid of the solid paired across its shorter side, 30 pairs
            tz = [g for g in faces if len(g) == 4 and shape(list(g)) == 'isosceles trapezoid' and sorted(repr(d2(g[i], g[(i + 1) % 4])) for i in range(4)) == sides[0]]
            E = {}
            for i, g in enumerate(tz):
                for j in range(4): E.setdefault(frozenset((g[j], g[(j + 1) % 4])), []).append(i)
            sh = [e for e, v in E.items() if len(v) == 2 and d2(*tuple(e)) == short]
            rib = len(tz) == 60 and len(sh) == 30 and sorted(x for e in sh for x in E[e]) == list(range(60))
            info['trapezoids_of_that_kind'] = len(tz); info['pairs_across_shorter_side'] = len(sh)
    info['ribbon'] = rib
    ok(True, f"{names[k]} ({len(C)} corners): at the two-fold axis edge meet {shp[0]} + {shp[1]}" + (' (congruent)' if info['congruent_sides'] else '') +
       (': a ribbon as on the TQH (60 congruent isosceles trapezoids in 30 pairs across their shorter parallel sides)' if rib else f": not a ribbon (the axis edge is their {info.get('axis_edge_is', '-')}; {info.get('trapezoids_of_that_kind', 0)} faces of that kind)"))
json.dump(res, open(os.path.join(HERE, f'ribbons-return{"-from-%d" % FROM if FROM else ""}.json'), 'w'), indent=1)
