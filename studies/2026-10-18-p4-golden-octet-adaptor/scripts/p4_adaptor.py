# DICTO 2026-10-18 "fusing all as one piece, and as adaptor to any golden envelope solid -- golden octet".
# All the non-envelope pieces of the golden envelope octet belong to the envelope they surround if every point goes to its nearest
# envelope centre: the fcc Voronoi cell, a rhombic dodecahedron (RD) |x|+|y|, |y|+|z|, |z|+|x| <= R. Exact checks: is the envelope (RT)
# inside its RD? which RT corners touch the RD faces? Adaptor = RD - RT, one per envelope; RD + envelope tile space (RDs tile fcc).
# -> data/p4-adaptor.json
import itertools
from exactpoly import *
G = json.load(open(os.path.join(HERE, '..', '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json')))
RT = [[q(x) for x in v] for v in G['RT']]; S1 = json.load(open(os.path.join(HERE, '..', '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json'))); R = q(S1['R'])
ab = lambda x: x if sgn(x) >= 0 else qn(x)
pairs = lambda v: [qa(ab(v[0]), ab(v[1])), qa(ab(v[1]), ab(v[2])), qa(ab(v[0]), ab(v[2]))]
inside = all(sgn(qs(R, s)) >= 0 for v in RT for s in pairs(v))
touch = [v for v in RT if any(s == R for s in pairs(v))]
RD = [[qm(R, qr(a)), qm(R, qr(b)), qm(R, qr(c))] for a, b, c in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]] + \
     [[qm(R, qr(Fr(a, 2))), qm(R, qr(Fr(b, 2))), qm(R, qr(Fr(c, 2)))] for a, b, c in itertools.product((1, -1), repeat=3)]
vRD = volume(RD); vRT = volume(intersect(planes_of(RT)))
cell = q(json.load(open(os.path.join(HERE, '..', '..', '2026-10-18-ocd-octet', 'data', 'step2-octet-frame.json')))['checks']['cell_volume'])
adaptor = qs(vRD, vRT)
checks = dict(RT_inside_RD=inside, RT_corners_on_RD_faces=len(touch), touching_corners=[[qs_(x) for x in v] for v in touch][:6], RD_volume=qs_(vRD), RD_equals_cell=vRD == cell,
              RT_volume=qs_(vRT), adaptor_volume=qs_(adaptor), adaptor_float=qf(adaptor), envelope_share=qf(qd(vRT, vRD)))
print(json.dumps(checks, indent=1)); save('p4-adaptor.json', dict(mark=MARK, step='p4-1', checks=checks))
