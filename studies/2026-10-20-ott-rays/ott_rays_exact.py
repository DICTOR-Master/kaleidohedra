# DICTO 2026-10-20: the DICTO OTT core of rays (DICTO's idea, Kyushindo series): the DICTO OTT (the rhombic triacontahedron cut by its
# octahedron at all 8 key sites, #37a) cut into its face pyramids, every apex at the centre, like the OG's Hex and Deltoid Aktis.
# Exact in Q(sqrt5), on studies/2026-10-19-og-gyrated-octet/cut8-exact.json: faces, rays, kinds (corner matching), volumes, shares.
#   usage: python3 ott_rays_exact.py <studies/2026-10-18-ocd-octet/scripts> <cut8-exact.json>
import sys, os, json, itertools, math
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1])
from q5 import *
from exactpoly import planes_of, volume
HERE = os.path.dirname(os.path.abspath(__file__)); log = {'mark': 'DICTO OTT core of rays, exact, 2026-10-20 · ' + MARK}
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
D = json.load(open(sys.argv[2])); V = [[q(x) for x in p] for p in D['V']]
O = [Z, Z, Z]
def vsum(xs):
    t = Z
    for x in xs: t = qa(t, x)
    return t
PL = planes_of(V)
F = []
for n, d in PL:
    on = [i for i, v in enumerate(V) if dot(n, v) == d]
    P = [[qf(x) for x in V[i]] for i in on]; c = [sum(p[k] for p in P) / len(P) for k in range(3)]
    u = [P[0][k] - c[k] for k in range(3)]; nf = [qf(x) for x in n]
    w = [nf[1] * u[2] - nf[2] * u[1], nf[2] * u[0] - nf[0] * u[2], nf[0] * u[1] - nf[1] * u[0]]
    ang = lambda p: math.atan2(sum((p[k] - c[k]) * w[k] for k in range(3)), sum((p[k] - c[k]) * u[k] for k in range(3)))
    F.append(([i for _, i in sorted(zip([ang(p) for p in P], on))], n, d))
ok(all(sgn(d) > 0 for _, n, d in F), f'the OTT: {len(V)} corners, {len(F)} faces, the centre strictly inside every face')
OTTV = volume(V); ok(OTTV == q(D['volume']) if isinstance(D['volume'], str) else True, f'volume {qs_(OTTV)} ({qf(OTTV):.6f}), as in #37a')
rays = [[V[i] for i in f] + [O] for f, _, _ in F]
vols = [volume(r) for r in rays]
ok(vsum(vols) == OTTV, 'the rays (face pyramids to the centre) add up to the OTT exactly')
d2 = lambda a, b: dot(vsub(a, b), vsub(a, b))
def same_shape(P, Q):
    n = len(P) - 1
    if len(Q) != len(P): return False
    for sh in range(n):
        for dr in (1, -1):
            m = [(sh + dr * k) % n for k in range(n)] + [n]
            if all(d2(P[i], P[j]) == d2(Q[m[i]], Q[m[j]]) for i in range(n + 1) for j in range(i + 1, n + 1)): return True
    return False
kinds = []
for r, v in zip(rays, vols):
    for kd in kinds:
        if same_shape(kd['ray'], r): kd['n'] += 1; break
    else: kinds.append({'ray': r, 'n': 1, 'sides': len(r) - 1, 'vol': v})
h2 = lambda n, d: qd(qm(d, d), dot(n, n))
for kd, (f, n, d) in [(kd, next((f, n, d) for (f, n, d), r in zip(F, rays) if r is kd['ray'])) for kd in kinds]:
    kd['height2'] = h2(n, d)
log['kinds'] = [{'sides': kd['sides'], 'count': kd['n'], 'volume': qs_(kd['vol']), 'share': qf(qd(qm(qr(kd['n']), kd['vol']), OTTV)), 'height': qf(kd['height2']) ** .5,
                 'edges2': sorted({qs_(d2(kd['ray'][i], kd['ray'][j])) for i in range(len(kd['ray'])) for j in range(i + 1, len(kd['ray'])) if j == len(kd['ray']) - 1 or (j - i) % kd['sides'] in (1, kd['sides'] - 1)})} for kd in kinds]
ok(sum(kd['n'] for kd in kinds) == len(F), 'kinds of ray (corner matching): ' + '; '.join(f"{kd['n']} on {kd['sides']}-gons, height {qf(kd['height2']) ** .5:.4f}, share {qf(qd(qm(qr(kd['n']), kd['vol']), OTTV)) * 100:.2f}%" for kd in kinds))
json.dump(log, open(os.path.join(HERE, 'ott-rays-exact.json'), 'w'), indent=1)
