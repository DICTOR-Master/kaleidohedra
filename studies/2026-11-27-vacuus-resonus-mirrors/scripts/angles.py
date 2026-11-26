"""Step 6 (27 Nov 2026; DICTO yes): the pieces in one mirror chamber and their solid angles, for the five simplest pairs. With Claude
(Anthropic). The chamber (a spherical triangle) is split exactly by every other plane of the pair (K arithmetic: a corner of a piece
is the cross product of two plane normals). Solid angle of each piece: mpmath at 60 digits (Van Oosterom-Strackee fan), then
identified as a rational multiple of 4 pi when it is one (denominator <= 10^4, residual < 1e-45). Check: the pieces' angles sum
to the chamber's, 4 pi / |G|, to 1e-50. Output angles.json: per pair, per piece: corners (floats), solid angle / (4 pi), exact
fraction if any. Next (step 7): fair dice from unions of pieces."""
import os, sys, json
from fractions import Fraction
import mpmath as mp
mp.mp.dps = 60
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pieces.py')).read()
exec(src[:src.index('PAIRS = ')])
def chamber(mir, one):
    g = (one * 1000003, one * 2000029 + one * 17 / 31, one * 3700019 + one * 5 / 7)
    gs = [sg(dot(m, g)) for m in mir]; cor = []
    for i in range(len(mir)):
        for j in range(i + 1, len(mir)):
            d = cross(mir[i], mir[j])
            for dd in (d, scl(-1, d)):
                if all(sg(dot(m, dd)) in (0, s) for m, s in zip(mir, gs)) and not any(same_dir(dd, c) and sg(dot(dd, c)) > 0 for c in cor):
                    cor.append(dd)
    assert len(cor) == 3
    # order corners counterclockwise seen from outside
    a, b, c = cor
    if sg(dot(cross(sub(b, a), sub(c, a)), a)) < 0: cor = [a, c, b]
    return cor
def split(poly, p):
    s = [sg(dot(p, v)) for v in poly]
    if all(x >= 0 for x in s) or all(x <= 0 for x in s): return [poly]
    A, B = [], []
    for i in range(len(poly)):
        u, v = poly[i], poly[(i + 1) % len(poly)]; su, sv = s[i], s[(i + 1) % len(poly)]
        if su >= 0: A.append(u)
        if su <= 0: B.append(u)
        if su * sv < 0:
            w = cross(p, cross(u, v))           # on plane p and on the great circle through u, v
            if sg(dot(w, u)) < 0 or sg(dot(w, v)) < 0: w = scl(-1, w)
            A.append(w); B.append(w)
    return [A, B]
def mpv(v): return [mp.mpf(x.a.numerator) / x.a.denominator + mp.mpf(x.b.numerator) / x.b.denominator * mp.sqrt(x.r) for x in v]
def solid_angle(poly):
    P = [mpv(v) for v in poly]; P = [[x / mp.sqrt(sum(y * y for y in v)) for x in v] for v in P]
    tot = mp.mpf(0); a = P[0]
    for i in range(1, len(P) - 1):
        b, c = P[i], P[i + 1]
        num = a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
        den = 1 + sum(x * y for x, y in zip(a, b)) + sum(x * y for x, y in zip(b, c)) + sum(x * y for x, y in zip(c, a))
        tot += 2 * mp.atan2(abs(num), den)
    return tot
PAIRS5 = [('cube', 'octahedron'), ('cuboctahedron', 'rhombic dodecahedron'), ('tetrahedron', 'tetrahedron (dual)'),
          ('icosidodecahedron', 'rhombic triacontahedron'), ('dodecahedron', 'icosahedron')]
SD = dict(SOL); SD['tetrahedron (dual)'] = [scl(-1, v) for v in SD['tetrahedron']]
G = {6: 24, 9: 48, 15: 120}; out = []; allok = True
for a, b in PAIRS5:
    Va, Vb = SD[a], SD[b]; mir = mirrors_of(Va); pa, pb = planes_of(Va), planes_of(Vb)
    allp = []
    for p in pa[0] + pa[1] + pb[0] + pb[1]: add(allp, p)
    one = Va[0][0] * 0 + 1
    polys = [chamber(mir, one)]
    for p in allp:
        if any(same_dir(p, m) for m in mir): continue
        polys = [q for P in polys for q in split(P, p)]
    polys = [P for P in polys if len(P) >= 3]
    ch = 4 * mp.pi / G[len(mir)]; angs = [solid_angle(P) for P in polys]
    ok = abs(sum(angs) - ch) < mp.mpf(10) ** -50; allok &= ok
    rec = []
    for P, w in zip(polys, angs):
        f = w / (4 * mp.pi); fr = Fraction(str(mp.nstr(f, 50))).limit_denominator(10 ** 4)
        exact = abs(f - mp.mpf(fr.numerator) / fr.denominator) < mp.mpf(10) ** -45
        rec.append(dict(corners=[[float(x) for x in v] for v in P], sides=len(P), frac_of_sphere=mp.nstr(f, 58),
                        exact=str(fr) if exact else None))
    out.append(dict(pair=f'{a} + {b}', group_order=G[len(mir)], pieces=rec))
    print(f'{a} + {b}: {len(polys)} pieces per chamber (sum check {ok}); fractions of the sphere:', flush=True)
    for r in rec: print(f'   {r["sides"]}-sided  {r["frac_of_sphere"][:22]}  ' + (f'= {r["exact"]} exactly' if r['exact'] else '(not a rational multiple, small denominators)'), flush=True)
exp = [2, 2, 3, 4, 12]
cnt = [len(r['pieces']) for r in out]
print('control: piece counts equal step 2 (2, 2, 3, 4, 12):', cnt == exp)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../angles.json'), 'w'), indent=1)
print('FINAL ok' if allok and cnt == exp else 'FINAL FAIL')
