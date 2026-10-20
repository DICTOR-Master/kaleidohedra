# DICTO 2026-10-20: the numbers of the family table (the OG's family), exact in Q(sqrt5), each from exact corners in the #37 frame:
# volumes, corner and face counts, shares of the octet cell / the OCD's bcc cell; and the octet's phi^-2 corner cuboctahedron (#37 step 24).
import os, sys, json, itertools
ME = os.path.dirname(os.path.abspath(__file__)); GY = os.path.join(ME, '..', '2026-10-19-og-gyrated-octet'); OC = os.path.join(ME, '..', '2026-10-18-ocd-octet')
sys.path.insert(0, os.path.join(OC, 'scripts'))
from q5 import Fr, Z, ONE, qr, qa, qs, qm, qd, qf, qn, q, qs_, dot
from exactpoly import planes_of, intersect, volume
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True)
qstr = lambda x: f'{x[0]} + {x[1]}*sqrt5 = {qf(x):.6f}'
R = (Fr(1, 3), Fr(1, 3)); R3 = qm(R, qm(R, R))
octc = qm(qr(Fr(2)), R3);   # octahedron 4R^3/3 + 2 tetrahedra R^3/3
bccc = qm(qr(Fr(32, 27)), R3)   # the OCD's bcc cell
ok(octc == (Fr(32, 27), Fr(16, 27)) and bccc == (Fr(512, 729), Fr(256, 729)), f'octet cell {qstr(octc)}; bcc cell {qstr(bccc)}')
L = lambda f: [[q(c) for c in v] for v in json.load(open(f))['V']]
OG = L(os.path.join(OC, 'data', 'step1-ocd-exact.json')); DB = L(os.path.join(GY, 'dbt-exact.json')); OT = L(os.path.join(GY, 'cut8-exact.json'))
SO = json.load(open(os.path.join(ME, 'stella-octa-exact.json'))); ST = [[q(c) for c in v] for v in SO['stella_V']]
PD = planes_of(DB)
# the RT = the DBT without its two pole planes (normals along (1,1,1))
par = lambda n: n[0] == n[1] and n[1] == n[2]
RTP = [(n, d) for n, d in PD if not par(n)]
RT = intersect(RTP)
rows = []
def row(name, V, cell=None, cellname=''):
    P = planes_of(V); v = volume(V); rows.append((name, len(V), len(P), v)); s = f'{name}: {len(V)} corners, {len(P)} faces, volume {qstr(v)}'
    if cell: sh = qd(v, cell); s += f'; {qstr(sh)} of the {cellname}'
    print('      ' + s); return v
vOG = row('OG', OG, bccc, 'bcc cell (hexagon-joined packing)')
ok(vOG == (Fr(-1000, 1539), Fr(1240, 1539)), 'OG volume as #37')
vS = row('OCD Stella', ST, bccc, 'bcc cell'); ok(vS == (Fr(-4064, 729), Fr(2240, 729)), 'OCD Stella as #31a')
vRT = row('golden envelope (rhombic triacontahedron)', RT, octc, 'octet cell'); ok(vRT == (Fr(-320, 27), Fr(160, 27)) and qd(vRT, octc) == (Fr(90), Fr(-40)), 'golden envelope 10/phi^6 = 90 - 40sqrt5 of the octet (#37)')
vD = row('DBT', DB, octc, 'octet cell'); vT = row('OTT', OT, octc, 'octet cell')
a = qm(R, (Fr(3, 2), Fr(-1, 2)))   # R / phi^2
CU = []
for p in set(itertools.permutations((1, 1, 0))) | set(itertools.permutations((1, -1, 0))) | set(itertools.permutations((-1, -1, 0))):
    CU.append([qm(a, qr(x)) for x in p])
CU = [list(v) for v in {tuple(v) for v in CU}]
vC = row('phi^-2 corner cuboctahedron', CU, octc, 'octet cell')
ok(len(CU) == 12 and vC == qd(vRT, qr(3)), f'the octet\'s phi^-2 corner cuboctahedron is exactly one third of the golden envelope: {qstr(vC)}')
ok(qd(vC, octc) == (Fr(30), Fr(-40, 3)), 'and 30 - 40sqrt5/3 of the octet cell (one per cell)')
# its 14 parts: 6 square pyramids (octahedron corners scaled by phi^-2) and 8 tetrahedron corners (scaled by phi^-2)
octv = qm(qr(Fr(4, 3)), R3); tetv = qm(octv, qr(Fr(1, 4))); p2 = qm((Fr(3, 2), Fr(-1, 2)), qm((Fr(3, 2), Fr(-1, 2)), (Fr(3, 2), Fr(-1, 2))))   # phi^-6
pyr = qm(qm(octv, qr(Fr(1, 2))), p2)   # the corner of the octahedron down to its equator is half of it
tc = qm(tetv, p2)
ok(qa(qm(qr(6), pyr), qm(qr(8), tc)) == vC, f'6 pyramids {qstr(pyr)} + 8 tetrahedron corners {qstr(tc)} = the cuboctahedron')
ok(pyr == (Fr(-32, 81), Fr(16, 81)), 'each pyramid (-32 + 16sqrt5)/81, as #37 step 24')
json.dump(dict(mark='DICTO · dictospheres.com', rows=[dict(name=n, corners=c, faces=f, volume=qs_(v)) for n, c, f, v in rows], cubocta=qs_(vC), pyramid=qs_(pyr), tet_corner=qs_(tc)),
          open(os.path.join(ME, 'family-exact.json'), 'w'), indent=1, ensure_ascii=False)
print('saved family-exact.json')
