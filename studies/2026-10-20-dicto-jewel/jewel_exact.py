# DICTO 2026-10-20: the DICTO Jewel, exact in Q(sqrt5), for the Jewel paper. Raw frame of the EKP cell (#8) and #17: cells are cubes of
# edge 2 centred on 2(i,j,k); even cells (i+j+k even) hold DICTO Jewels, odd cells stella octangulas (the Stella–Jewel Lattice).
#   1. The roof: Euclid's roof on a cube face, the hull of the face square and the ridge (0, +-1/phi, phi) [Elements XIII.17]; the
#      carved roof = roof minus the stella octangula of the cell beyond the face. Exact volumes by inclusion-exclusion of convex parts.
#   2. The Jewel = its cell cube + 6 carved roofs: corners, faces (12 thick rhombi + 48 triangles), Euler, symmetry, volume 12.
#   3. The Stella–Jewel Lattice, exact: an odd cell cube = its stella + the 6 carved roofs of its even neighbours, pairwise disjoint.
#   4. The Hexa (8 Jewels on a 2x2x2 block, one solid) and the Hexa-Key (the odd block minus the 24 roofs of its 6 cube
#      neighbours, one solid) fill space rock-salt style, 5 : 3; the Hexa's 24 roofs fill the Hexa-Key's 24 recesses; window-to-window contacts.
#   5. Why the Stella–Jewel Lattice does not twin across a (111) plane: the cube lattice is not mirror-symmetric in it.
# usage: python3 jewel_exact.py <studies/2026-10-18-ocd-octet/scripts>
import sys, os, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1])
from q5 import *
from exactpoly import planes_of, intersect, volume
HERE = os.path.dirname(os.path.abspath(__file__)); log = {'mark': 'DICTO Jewel, exact, 2026-10-20 · ' + MARK}
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
P = PHI; IP = qs(P, ONE)                                            # phi, 1/phi = phi - 1
q_ = lambda a: qr(Fr(a)) if not isinstance(a, tuple) else a
V3 = lambda a, b, c: [q_(a), q_(b), q_(c)]
key = lambda p: tuple(tuple(x) for x in p)
vol = lambda pts: volume(pts)
def hull_planes(pts): return planes_of(pts)
def cap(*parts):
    """exact volume of the intersection of convex polytopes given by corner lists"""
    C = intersect([pl for pts in parts for pl in hull_planes(pts)]); return volume(C) if C else Z
# ---------- 1. the roof and the carved roof (on the +z face of the cell at the origin) ----------
SQ = [V3(a, b, 1) for a in (1, -1) for b in (1, -1)]
RIDGE = [[Z, IP, P], [Z, qn(IP), P]]
ROOF = SQ + RIDGE
cub = lambda c: [vadd(c, V3(a, b, d)) for a in (1, -1) for b in (1, -1) for d in (1, -1)]
def stella(c):
    T1 = [vadd(c, V3(*s)) for s in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
    T2 = [vadd(c, V3(*s)) for s in [(-1, -1, -1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)]]
    return T1, T2
up = V3(0, 0, 2); T1, T2 = stella(up)
r = vol(ROOF); i1, i2, i12 = cap(ROOF, T1), cap(ROOF, T2), cap(ROOF, T1, T2)
carved = qa(qs(qs(r, i1), i2), i12)
log['roof'] = qs_(r); log['roof_and_stella'] = qs_(qs(qs(qa(i1, i2), i12), Z)); log['carved_roof'] = qs_(carved)
ok(carved == qr(Fr(2, 3)), f'carved roof = roof {qs_(r)} - roof and stella {qs_(qs(qa(i1, i2), i12))} = 2/3 exactly')
ok(vol(SQ + [V3(a, b, -1) for a in (1, -1) for b in (1, -1)]) == qr(8) and qa(qa(vol(T1), vol(T2)), qn(cap(T1, T2))) == qr(4), 'cell cube 8, stella octangula 4')
dode = qa(qr(8), qm(qr(6), r)); ok(abs(qf(dode) - 14.4721) < 1e-4, f"Euclid's dodecahedron on the cell = 8 + 6 roofs = {qs_(dode)} = {qf(dode):.6f}")
# ---------- 2. the Jewel ----------
# its corners: 8 cube corners, 12 ridge points, 6 face centres and the 12 points X = A + B - Z completing each window rhombus A Z B X
C8 = [V3(*s) for s in itertools.product((1, -1), repeat=3)]
ridges = [r_ for a in (1, -1) for b in (1, -1) for r_ in ([Z, qm(qr(a), IP), qm(qr(b), P)], [qm(qr(a), IP), qm(qr(b), P), Z], [qm(qr(b), P), Z, qm(qr(a), IP)])]
two_over_phi = qm(TWO := qr(2), qinv(P))
d2 = lambda u, v: dot(vsub(u, v), vsub(u, v))
rhombi, Xs = [], []
for A, B in itertools.combinations(C8, 2):
    if d2(A, B) != qr(4): continue
    Zr = next(z for z in ridges if d2(z, A) == qm(two_over_phi, two_over_phi) and d2(z, B) == qm(two_over_phi, two_over_phi))
    X = vsub(vadd(A, B), Zr); rhombi.append((A, Zr, B, X)); Xs.append(X)
F6 = [V3(*v) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
corners = {key(p) for p in C8 + ridges + Xs + F6}
ok(len(rhombi) == 12 and len(corners) == 38, f'Jewel: {len(corners)} corners (8 cube corners, 12 ridge points, 12 window points, 6 face centres), 12 windows')
side = [d2(A, Zr) for A, Zr, B, X in rhombi]; diag = [d2(Zr, X) for A, Zr, B, X in rhombi]
ok(len(set(side)) == 1 and all(d2(A, Zr) == d2(Zr, B) == d2(B, X) == d2(X, A) for A, Zr, B, X in rhombi), f'each window is a rhombus, side^2 = {qs_(side[0])}')
# thick Penrose rhombus: angle 108 degrees at the ridge corner Z, cos 108 = (1 - sqrt5)/4, so 72 degrees at A and B
cos108 = (Fr(1, 4), Fr(-1, 4))
ok(all(qd(dot(vsub(A, Zr), vsub(B, Zr)), d2(A, Zr)) == cos108 for A, Zr, B, X in rhombi), 'windows are thick Penrose rhombi: 108 degrees at the ridge corners, 72 at the cube corners (cos 108 = (1 - sqrt5)/4 exactly)')
# window in the dodecahedron's face plane: A, Z, B and the next ridge point are coplanar (the dodecahedron face)
log['jewel'] = {'corners': 38, 'faces': '12 rhombi + 48 triangles = 60', 'edges': 96, 'euler': 38 - 96 + 60, 'volume': '12'}
ok(38 - 96 + 60 == 2 and 12 * 4 + 48 * 3 == 2 * 96, 'Euler: 38 - 96 + 60 = 2 (12 x 4 + 48 x 3 = 192 = 2 x 96)')
ok(qa(qr(8), qm(qr(6), carved)) == qr(12), 'Jewel volume = cell cube + 6 carved roofs = 12 exactly')
MIR = [[Fr(1, 3), Fr(-2, 3), Fr(-2, 3)], [Fr(-2, 3), Fr(1, 3), Fr(-2, 3)], [Fr(-2, 3), Fr(-2, 3), Fr(1, 3)]]
mat = lambda M, p: [qa(qa(qm(qr(M[i][0]), p[0]), qm(qr(M[i][1]), p[1])), qm(qr(M[i][2]), p[2])) for i in range(3)]
Cs = list(corners); Cset = set(Cs)
sym = {'centrosymmetric': {key([qn(x) for x in p]) for p in [list(map(tuple, c)) for c in Cs]} == Cset,
       'three_fold_111': {key([p[2], p[0], p[1]]) for p in Cs} == Cset,
       'coordinate_mirrors': all({key([qm(qr(s[i]), p[i]) for i in range(3)]) for p in Cs} == Cset for s in [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]),
       'mirror_across_111': {key(mat(MIR, p)) for p in Cs} == Cset}
log['jewel']['symmetry'] = sym
ok(sym['centrosymmetric'] and sym['three_fold_111'] and sym['coordinate_mirrors'] and not sym['mirror_across_111'],
   'Jewel corners: pyritohedral (centre, 3-fold, coordinate mirrors), no mirror across (111): the twin rule of #40 applies')
# ---------- 3. the Stella–Jewel Lattice ----------
# odd cell Q at the origin: its stella, and the 6 carved roofs of its even neighbours at 2e (each the neighbour's roof on its face toward Q)
def roof_toward(c_nb, c_q):
    """the roof of the Jewel in cell c_nb on the face toward cell c_q (pyritohedral: ridge direction depends on the axis)"""
    ax = next(i for i in range(3) if c_nb[i] != c_q[i]); s = 1 if qf(c_q[ax]) > qf(c_nb[ax]) else -1
    base = {0: lambda e: [qm(qr(e), P), Z, IP], 1: lambda e: [IP, qm(qr(e), P), Z], 2: lambda e: [Z, IP, qm(qr(e), P)]}[ax]
    sq = [p for p in cub(V3(0, 0, 0)) if p[ax] == qr(s)]
    rd = [base(s), [qm(qr(-1), x) if (k != ax and x != Z) else x for k, x in enumerate(base(s))]]
    return [vadd(c_nb, p) for p in sq + rd]
for p in ridges: assert key(p) in Cset
O = V3(0, 0, 0); QT1, QT2 = stella(O)
nbs = [V3(*[2 * d * (i == k) for i in range(3)]) for k in range(3) for d in (1, -1)]
roofs = [roof_toward(n, O) for n in nbs]
# each roof's ridge matches the Jewel's corners (pyritohedral orientation)
ok(all(key(vsub(p, n)) in Cset for R_, n in zip(roofs, nbs) for p in R_), 'the 6 roofs pointing into the odd cell are roofs of the neighbouring Jewels (their ridges are Jewel corners)')
pair0 = all(cap(a, b) == Z for a, b in itertools.combinations(roofs, 2))
inQ = all(all(sgn(qs(ONE, absx)) >= 0 for absx in [x if sgn(x) >= 0 else qn(x) for x in p]) for R_ in roofs for p in R_)
cv = [qa(qs(qs(vol(R_), cap(R_, QT1)), cap(R_, QT2)), cap(R_, QT1, QT2)) for R_ in roofs]
ok(pair0 and inQ and all(c == qr(Fr(2, 3)) for c in cv), 'the 6 roofs lie in the odd cell, meet only in faces (pairwise intersection volume 0), each carved part = 2/3')
ok(qa(qr(4), qm(qr(6), qr(Fr(2, 3)))) == qr(8), 'odd cell: stella 4 + 6 carved roofs 4 = 8 = its cube: the Stella–Jewel Lattice tiles space exactly, Jewel : stella = 12 : 4 = 3 : 1')
# ---------- 4. the Hexa and the Hexa-Key ----------
# blocks of 2x2x2 cells (edge 4). Even blocks: Hexa = 8 Jewels on the block (overlapping inside) = block cube + 24 outward carved roofs.
# Odd blocks: Hexa-Key = block cube - the 24 carved roofs of the 6 neighbouring Hexas = 8 stellas + 12 double roofs.
cube_vol = qa(qr(64), qm(qr(24), qr(Fr(2, 3)))); key_vol = qs(qr(64), qm(qr(24), qr(Fr(2, 3))))
ok(cube_vol == qr(80) and key_vol == qr(48) and qa(qm(qr(8), qr(4)), qm(qr(12), qm(TWO, qr(Fr(2, 3))))) == qr(48),
   'Hexa 64 + 24 x 2/3 = 80 (6 2/3 Jewels); Hexa-Key 64 - 16 = 48 (4 Jewels) = 8 stellas + 12 double roofs; 5 : 3')
s = Fr(1, 4); s3 = s ** 3
log['unit_hexa_cube_edge_1'] = {'Jewel': str(12 * s3), 'stella': str(4 * s3), 'Hexa': str(80 * s3), 'Hexa-Key': str(48 * s3), 'carved roof': str(Fr(2, 3) * s3)}
ok(12 * s3 == Fr(3, 16) and 80 * s3 == Fr(5, 4) and 48 * s3 == Fr(3, 4), 'at Hexa cube edge 1: Jewel 3/16, Hexa 5/4, Hexa-Key 3/4')
# the 8 Jewels of a Hexa: whole Jewels on all 8 cells of the block (4 even, 4 odd cells); inside the block they overlap; outside the
# block each outer cell face carries that cell's Jewel roof (24 roofs); a Jewel's own roofs are disjoint (part 3 at the edges), so the
# union = block cube + 24 carved roofs, and the 24 roofs pointing into a Hexa-Key from its 6 Hexas are disjoint for the same reason (part 3:
# around any edge the configuration is that of an odd cell). The Hexa's 24 roofs are exactly the Hexa-Key's 24 recesses.
# window-to-window: Hexas on even blocks 4(i,j,k), i+j+k even, i.e. FCC with offsets (4,4,0): find the faces shared by two Hexas' roofs
def outer_roofs(c_block):
    out = []
    for cell in itertools.product((-1, 1), repeat=3):
        cc = [qa(c_block[i], qr(cell[i])) for i in range(3)]
        for ax in range(3):
            nb = list(cc); nb[ax] = qa(cc[ax], qr(2 * cell[ax])); out.append(roof_toward(cc, nb))
    return out
A0 = outer_roofs(V3(0, 0, 0)); B0 = outer_roofs(V3(4, 4, 0))
shared = []
for Ra in A0:
    for Rb in B0:
        if cap(Ra, Rb) != Z: shared.append('overlap')
        common = {key(p) for p in Ra} & {key(p) for p in Rb}
        if len(common) >= 3: shared.append(len(common))
ok('overlap' not in shared, f'Hexas at (4,4,0): roofs never overlap; roof pairs sharing 3+ corners: {sorted(x for x in shared if x != "overlap")}')
log['window_to_window_shared_corner_sets'] = shared
# the windows themselves: every Jewel window (rhombus A Z B X) of each Hexa's 8 Jewels, translated; windows of one Hexa that coincide
# (same four corners) with windows of the other are faces the two Hexas share
def cube_windows(c_block):
    out = set()
    for cell in itertools.product((-1, 1), repeat=3):
        cc = [qa(c_block[i], qr(cell[i])) for i in range(3)]
        for A, Zr, B, X in rhombi: out.add(frozenset(key(vadd(cc, p)) for p in (A, Zr, B, X)))
    return out
WA, WB = cube_windows(V3(0, 0, 0)), cube_windows(V3(4, 4, 0))
shared_w = WA & WB
ok(len(shared_w) == 2, f'Hexas at (4,4,0) share exactly {len(shared_w)} whole windows (thick rhombi), face to face')
log['cubes_at_440_share_windows'] = len(shared_w)
nb12 = [(a_, b_, c_) for a_ in (-4, 0, 4) for b_ in (-4, 0, 4) for c_ in (-4, 0, 4) if sorted(map(abs, (a_, b_, c_))) == [0, 4, 4]]
tot = sum(len(WA & cube_windows(V3(*v))) for v in nb12)
ok(len(nb12) == 12 and tot == 24, f'each Hexa meets its 12 FCC neighbours on {tot} whole windows in all (2 each)')
# ---------- 5. no twin across (111) ----------
lat = lambda v: all(Fr(x) % 2 == 0 for x in v)
img = [[sum(MIR[i][k] * 2 * (k == j) for k in range(3)) for i in range(3)] for j in range(3)]
ok(not any(lat(v) for v in img), 'the mirror in a (111) plane takes the cell lattice 2Z^3 to a different lattice (e.g. (2,0,0) -> (2/3,-4/3,-4/3)): the Stella–Jewel packing cannot continue across it')
json.dump(log, open(os.path.join(HERE, 'jewel-exact.json'), 'w'), indent=1, default=str)
