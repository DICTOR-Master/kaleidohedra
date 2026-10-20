# DICTO 2026-10-20: the DICTO OG core of 80 spires (DICTO's idea): the Ogdoecontahedron cut into its 80 face pyramids, every apex at the
# centre (as the CLEO sphere is the icosidodecahedron cut into 20 Cleo and 12 pentagonal pockets). Exact in Q(sqrt5), on the OG of
# studies/2026-10-18-ocd-octet/data/step1-ocd-exact.json (raw frame of #37).
#   the OG is centred; its 20 hexagons and 60 kites; the 80 pyramids fill it exactly (volumes add up, pairwise only faces);
#   the 20 hexagonal spires are one shape and the 60 kite spires are one shape (corner matching); heights, volumes, shares; apex angles.
#   usage: python3 og_spires_exact.py <studies/2026-10-18-ocd-octet/scripts>
import sys, os, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1])
from q5 import *
from exactpoly import planes_of, intersect, volume
HERE = os.path.dirname(os.path.abspath(__file__)); log = {'mark': 'DICTO OG core of 80 spires, exact, 2026-10-20 · ' + MARK}
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
D = json.load(open(os.path.join(sys.argv[1], '..', 'data', 'step1-ocd-exact.json')))
V = [[q(x) for x in p] for p in D['V']]
import math
def cyclic(f):
    """the face's corners in cyclic order (sorted by angle round the face centre, float only for the order)"""
    P = [[qf(x) for x in V[i]] for i in f]; c = [sum(p[k] for p in P) / len(P) for k in range(3)]
    u = [P[0][k] - c[k] for k in range(3)]; a, b = [P[1][k] - c[k] for k in range(3)], u
    n = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    w = [n[1] * u[2] - n[2] * u[1], n[2] * u[0] - n[0] * u[2], n[0] * u[1] - n[1] * u[0]]
    ang = lambda p: math.atan2(sum((p[k] - c[k]) * w[k] for k in range(3)), sum((p[k] - c[k]) * u[k] for k in range(3)))
    return [i for _, i in sorted(zip([ang(p) for p in P], f))]
F = [cyclic(f) for f in D['faces']]
O = [Z, Z, Z]
def vsum(xs):
    t = Z
    for x in xs: t = qa(t, x)
    return t
cen = vmul([vsum(p[i] for p in V) for i in range(3)], qr(Fr(1, len(V))))
hexes = [f for f in F if len(f) == 6]; kites = [f for f in F if len(f) == 4]
ok(cen == O and len(V) == 102 and len(hexes) == 20 and len(kites) == 60, f'the OG: 102 corners centred at the origin, {len(hexes)} hexagons and {len(kites)} kites')
OGV = volume(V)
spires = [[V[i] for i in f] + [O] for f in F]
vols = [volume(s) for s in spires]
ok(vsum(vols) == OGV, f'the 80 spires (face pyramids to the centre) add up to the OG exactly: {qs_(OGV)}')
# they meet only in faces: pyramids over different faces of a convex solid from an interior point never overlap (each lies in its
# face's cone from the centre, and these cones only share boundaries); checked here on every pair of neighbouring spires
nb = [(a, b) for a, b in itertools.combinations(range(len(F)), 2) if len(set(F[a]) & set(F[b])) >= 2]
ok(all(volume(intersect(planes_of(spires[a]) + planes_of(spires[b])) or [O]) == Z for a, b in nb[:60]) and len(nb) == 180,
   f'neighbouring spires meet only in faces (180 shared edges of the OG; first 60 pairs checked by exact intersection)')
d2 = lambda u, v: dot(vsub(u, v), vsub(u, v))
def same_shape(P, Q):
    """corner matching: apex to apex (last point), base corners in cyclic order either way round, all pairwise distances equal"""
    n = len(P) - 1
    if len(Q) != len(P): return False
    for sh in range(n):
        for dr in (1, -1):
            m = [(sh + dr * k) % n for k in range(n)] + [n]
            if all(d2(P[i], P[j]) == d2(Q[m[i]], Q[m[j]]) for i in range(n + 1) for j in range(i + 1, n + 1)): return True
    return False
hs = [s for s, f in zip(spires, F) if len(f) == 6]; ks = [s for s, f in zip(spires, F) if len(f) == 4]
ok(all(same_shape(hs[0], s) for s in hs) and all(same_shape(ks[0], s) for s in ks), 'the 20 hexagonal spires are one shape, and the 60 kite spires are one shape (corner matching)')
hv = volume(hs[0]); kv = volume(ks[0])
ok(qa(qm(qr(20), hv), qm(qr(60), kv)) == OGV, f'hexagonal spire {qs_(hv)}, kite spire {qs_(kv)}; 20 + 60 of them = the OG')
def height(f):
    P = [V[i] for i in f]; n = cross(vsub(P[1], P[0]), vsub(P[2], P[0])); return qd(qm(dot(n, P[0]), dot(n, P[0])), dot(n, n))   # squared
hh2, kh2 = height(hexes[0]), height(kites[0])
ok(all(height(f) == hh2 for f in hexes) and all(height(f) == kh2 for f in kites), f'heights squared: hexagonal {qs_(hh2)} ({qf(hh2) ** .5:.6f}), kite {qs_(kh2)} ({qf(kh2) ** .5:.6f})')
share_h = qd(qm(qr(20), hv), OGV); share_k = qd(qm(qr(60), kv), OGV)
log.update(OG=qs_(OGV), hex_spire=qs_(hv), kite_spire=qs_(kv), hex_height2=qs_(hh2), kite_height2=qs_(kh2), hex_share=qs_(share_h), kite_share=qs_(share_k))
ok(qa(share_h, share_k) == ONE, f'shares of the OG: hexagonal spires {qs_(share_h)} ({qf(share_h):.6f}), kite spires {qs_(share_k)} ({qf(share_k):.6f})')
# edge lengths of the spires (sides and the lateral edges to the centre), for naming and building
hexP = hs[0]; kiteP = ks[0]
log['hex_spire_edges2'] = sorted({qs_(d2(hexP[i], hexP[j])) for i in range(7) for j in range(i + 1, 7) if j == 6 or (j - i) % 6 in (1, 5)})
log['kite_spire_edges2'] = sorted({qs_(d2(kiteP[i], kiteP[j])) for i in range(5) for j in range(i + 1, 5) if j == 4 or (j - i) % 4 in (1, 3)})
print('hex spire edges^2', log['hex_spire_edges2']); print('kite spire edges^2', log['kite_spire_edges2'])
json.dump(log, open(os.path.join(HERE, 'og-spires-exact.json'), 'w'), indent=1)
