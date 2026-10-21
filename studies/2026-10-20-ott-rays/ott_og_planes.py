# DICTO 2026-10-21: in the frame of #37 (where both are given), the 8 octahedral cuts of the DICTO OTT lie exactly in 8 of the 20 hexagon
# planes of the DICTO OG, so each octahedral ray has the height of a Hex Aktis. Exact in Q(sqrt5): a plane n.x = d of the OTT equals a plane
# m.x = e of the OG iff n x m = 0, n.m > 0 and d (m.m) = e (n.m).   usage: python3 ott_og_planes.py <studies/2026-10-18-ocd-octet/scripts> <cut8-exact.json>
import sys, os, json
sys.path.insert(0, sys.argv[1])
from q5 import *
from exactpoly import planes_of
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
OG = [[q(x) for x in p] for p in json.load(open(os.path.join(sys.argv[1], '..', 'data', 'step1-ocd-exact.json')))['V']]
OTT = [[q(x) for x in p] for p in json.load(open(sys.argv[2]))['V']]
def on(P, n, d): return [p for p in P if dot(n, p) == d]
og_hex = [(n, d) for n, d in planes_of(OG) if len(on(OG, n, d)) == 6]
ott_tri = [(n, d) for n, d in planes_of(OTT) if len(on(OTT, n, d)) == 3 and len({qs_(qm(x, x)) for x in n}) == 1]
same = lambda a, b: all(x == Z for x in cross(a[0], b[0])) and sgn(dot(a[0], b[0])) > 0 and qm(a[1], dot(b[0], b[0])) == qm(b[1], dot(a[0], b[0]))
ok(len(og_hex) == 20 and len(ott_tri) == 8, f'the OG has {len(og_hex)} hexagon planes; the OTT has {len(ott_tri)} octahedral (pole) triangles')
ok(all(sum(same(t, h) for h in og_hex) == 1 for t in ott_tri), 'each of the 8 octahedral triangles of the OTT lies in one hexagon plane of the OG, exactly')
# DICTO 2026-10-21 (referee): in each such plane, the OG hexagon's circumradius equals the OTT triangle's inradius, and three corners of the
# hexagon are exactly the midpoints of the triangle's edges, so the hexagon touches the triangle there (and lies inside it, the OG being inside the OTT).
OGs = [tuple(qs_(x) for x in v) for v in OG]; key = lambda v: tuple(qs_(x) for x in v)
allok, r_eq = True, True
for t in ott_tri:
    h = next(h for h in og_hex if same(t, h)); T3 = on(OTT, *t); H6 = on(OG, *h)
    ctr = [qd(vsum3, qr(3)) for vsum3 in [qa(qa(T3[0][k], T3[1][k]), T3[2][k]) for k in range(3)]]
    side2 = dot(vsub(T3[0], T3[1]), vsub(T3[0], T3[1])); in2 = qd(side2, qr(12))                       # inradius^2 of an equilateral triangle
    circ = {qs_(dot(vsub(p, ctr), vsub(p, ctr))) for p in H6}                                              # hexagon corners' distance^2 to the centre
    r_eq &= circ == {qs_(in2)}
    mids = [[qd(qa(a[k], b[k]), qr(2)) for k in range(3)] for a, b in ((T3[0], T3[1]), (T3[1], T3[2]), (T3[2], T3[0]))]
    allok &= all(key(m) in {key(p) for p in H6} for m in mids)
ok(r_eq, f'in each of the 8 planes the OG hexagon\'s circumradius^2 equals the OTT triangle\'s inradius^2, {qs_(in2)} (exact)')
ok(allok, 'three corners of each such hexagon are exactly the midpoints of the triangle\'s three edges: the hexagon touches the triangle there')
