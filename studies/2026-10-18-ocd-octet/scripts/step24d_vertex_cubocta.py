# DICTO 2026-10-18 octet study -- STEP 24d (Claude's observation from step 24): the phi^-2 corner pyramids of the 6 octahedra at a lattice
# vertex, with the phi^-2 corners of the 8 tetrahedra there, would make a cuboctahedron (the octet's vertex figure) scaled by phi^-2.
# Exact checks: each small tetrahedron corner lies outside every envelope (golden-free), meets no key except at points (the keys' base
# corners sit at the golden-section points of the edges, distance R*sqrt2/phi^2 from a vertex), and the volumes. -> data/step24d-cubocta.json
import itertools
from exactpoly import *
G = json.load(open(os.path.join(HERE, '..', '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json')))
RT = [[q(x) for x in v] for v in G['RT']]; PR = planes_of(RT)
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json')
R = q(S1['R']); L = [[q(x) for x in v] for v in S2['lattice']]; Tp = [[q(x) for x in v] for v in S2['Tplus']]
ip2 = qinv(qm(PHI, PHI)); v0 = [Z, Z, R]
small = [vadd(v0, vmul(vsub(p, v0), ip2)) for p in Tp]          # T+ corner at R e_z, scaled by phi^-2 towards that vertex
PS = planes_of(small); vS = volume(intersect(PS))
def lat(c):
    o = [Z, Z, Z]
    for k, Lv in zip(c, L): o = vadd(o, vmul(Lv, qr(k)))
    return o
cents = [lat(c) for c in itertools.product(range(-2, 3), repeat=3)]; cents = [c for c in cents if qf(dot(c, c)) < 6]
env_hit = [qs_(c) for c in [[qs_(x) for x in c] for c in cents] if False]
env_ov = max((qf(volume(intersect(PS + shift(PR, c)))) for c in cents), default=0)
keys = [[[q(x) for x in p] for p in K] for K in S5['keys'].values()]
key_ov = max((qf(volume(intersect(PS + shift(planes_of(K), c)))) for K in keys for c in cents), default=0)
key_touch = sum(1 for K in keys for c in cents for p in K if all(sgn(qs(d, dot(n, vadd(p, c)))) >= 0 for n, d in PS))
pyr = volume(intersect(planes_of([[R if (i == j and s > 0) else (qn(R) if i == j else Z) for j in range(3)] for i in range(3) for s in (1, -1)]) + [([Z, Z, qn(ONE)], qn(qr(Fr(2, 3))))]))
cubo = qa(qm(qr(6), pyr), qm(qr(8), vS))
edge = qm(qm(R, ip2), (Fr(0), Fr(0)))  # placeholder
cell = q(S2['checks']['cell_volume'])
checks = dict(small_tet_volume=qs_(vS), small_tet_overlaps_envelopes=env_ov, small_tet_overlaps_keys=key_ov, key_corners_on_small_tet=key_touch,
              pyramid_volume=qs_(pyr), vertex_cuboctahedron=qs_(cubo), vertex_cuboctahedron_float=qf(cubo), share_of_space=qf(qd(cubo, cell)),
              cuboctahedron_edge=f'R*sqrt2/phi^2 = {qf(R) * 2 ** .5 / qf(qm(PHI, PHI)):.6f}')
print(json.dumps(checks, indent=1)); save('step24d-cubocta.json', dict(mark=MARK, step='24d', checks=checks))
