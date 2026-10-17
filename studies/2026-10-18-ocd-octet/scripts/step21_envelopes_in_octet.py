# DICTO 2026-10-18 octet study -- STEP 21 (stage 3: toward a minimal golden kit; DICTO: "develop the octet toward a minimal golden kit").
# First question: where is the octet already golden? Put each OCD's golden envelope (RT, same frame) into the keyless octet, exactly:
# does it stay inside its octahedron + the 8 tetrahedra round it (keys = its corners in the tetrahedra), do neighbouring envelopes overlap,
# and how much of each piece (cap, tetrahedron, middle piece) lies inside some envelope (golden region) vs outside. -> data/step21-envelopes.json
import itertools
from exactpoly import *
G = json.load(open(os.path.join(HERE, '..', '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json')))
RT = [[q(x) for x in v] for v in G['RT']]; PR = planes_of(RT)
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S11 = load('step11-exact.json')['checks']; S19 = load('step19-flank-cores.json')['checks']
V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R']); L = [[q(x) for x in v] for v in S2['lattice']]; PO = planes_of(V)
def lat(c):
    o = [Z, Z, Z]
    for k, Lv in zip(c, L): o = vadd(o, vmul(Lv, qr(k)))
    return o
cells = [lat(c) for c in itertools.product(range(-2, 3), repeat=3)]
near = [c for c in cells if qf(dot(c, c)) < 4.5 and c != [Z, Z, Z]]
vRT = volume(intersect(PR))
ov = {}
for c in near:
    v = volume(intersect(PR + shift(PR, c)))
    if v != Z: ov[qs_(dot(c, c))] = qs_(v)
octa = [[R if (i == j and s > 0) else (qn(R) if i == j else Z) for j in range(3)] for i in range(3) for s in (1, -1)]; POC = planes_of(octa)
vRT_in_octa = volume(intersect(PR + POC)); vOCD = q(S2['checks']['ocd_volume'])
Tp = [[q(x) for x in v] for v in S2['Tplus']]; PT = planes_of(Tp)
# envelope inside T+ : the 4 envelopes of the octahedra round T+ (centres at the T+ face neighbours), each contributes its key
tcent = [c for c in [[Z, Z, Z]] + near if volume(intersect(PR + shift(PT, [qn(x) for x in c]))) != Z] if False else None
vT = q(S2['checks']['tet_volume']); envT = Z; nT = 0
for c in [[Z, Z, Z]] + near:
    v = volume(intersect(shift(PR, c) + PT))
    if v != Z: envT = qa(envT, v); nT += 1
cell = q(S2['checks']['cell_volume'])
env_share = qd(qs(vRT, Z), cell)
checks = dict(RT_volume=qs_(vRT), RT_overlaps_with_neighbour_envelopes=ov, RT_inside_own_octahedron=qs_(vRT_in_octa),
              RT_outside_octahedron=qs_(qs(vRT, vRT_in_octa)), key_volume=load('step3-key-candidate.json')['checks']['key_volume'],
              envelope_shell_in_octahedron=qs_(qs(vRT_in_octa, vOCD)), caps_outside_envelope_total=qs_(qs(qs(qm(qr(4), qd(R, ONE)) if False else q(S2['checks']['octa_volume']), vRT_in_octa), Z)),
              envelopes_touching_Tplus=nT, envelope_inside_Tplus=qs_(envT), Tplus_outside_envelopes=qs_(qs(vT, envT)),
              envelope_share_of_space=qf(env_share), envelope_share_exact=qs_(env_share))
print(json.dumps(checks, indent=1)); save('step21-envelopes.json', dict(mark=MARK, step=21, checks=checks))
