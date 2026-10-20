# DICTO 2026-10-20: the Sunstar clusters and the Hexa twin, exact in Q(sqrt5) (raw frame of sunstar_exact.py: cells of edge 2 on 2(i,j,k)).
#   contacts: two dodecahedra on neighbouring even cells (one face diagonal apart) touch on exactly one thick Penrose rhombus (the Jewel's
#     window), found by clipping each face of one by the other (exact); none two cells apart along an axis.
#   Sunstar-Tetra (4 dodecahedra round a cell corner), Sunstar-Octa (6 round an odd cell + its Dogstar), Sunstar-Rhombi (8 on the corners
#     of the face-centred cubic cell + the Dogstar inside): contacts, the Dogstar filling the hole exactly, volumes. Their tilings with loose
#     Dogstars are those of the Jewel clusters (#41, cluster_exact.py): the same cells, so the same lattices (4, 12, 25; 2, 1, 9 up to symmetry).
#   Sunstar-Hexa and Sunstar-Hexa-Key (DICTO's names, the twins of the Hexa and Hexa-Key): 8 whole dodecahedra on a 2 x 2 x 2 block (one solid) and the space between such blocks (one solid): volumes, make-up, contacts.
#   Dogstar inside its own cell's stella octangula (so Dogstars can sit in every cell).
#   usage: python3 sunstar_clusters.py <studies/2026-10-18-ocd-octet/scripts>
import sys, os, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1])
from q5 import *
from exactpoly import planes_of, intersect, volume
HERE = os.path.dirname(os.path.abspath(__file__)); log = {'mark': 'DICTO Sunstar clusters, exact, 2026-10-20 · ' + MARK}
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
P = PHI; IP = qs(P, ONE)
V3 = lambda a, b, c: [x if isinstance(x, tuple) else qr(Fr(x)) for x in (a, b, c)]
key = lambda p: tuple(tuple(x) for x in p)
def cap(*pls):
    C = intersect([pl for p in pls for pl in p]); return volume(C) if C else Z
def vsum(xs):
    t = Z
    for x in xs: t = qa(t, x)
    return t
C8 = [V3(*s) for s in itertools.product((1, -1), repeat=3)]
RID = [r for a in (1, -1) for b in (1, -1) for r in ([Z, qm(qr(a), IP), qm(qr(b), P)], [qm(qr(a), IP), qm(qr(b), P), Z], [qm(qr(b), P), Z, qm(qr(a), IP)])]
DOD = C8 + RID; DP0 = planes_of(DOD)
at = lambda cell: V3(*[2 * x for x in cell])
dod = lambda cell: [vadd(at(cell), p) for p in DOD]
dplanes = lambda cell: [(n, qa(d, dot(n, at(cell)))) for n, d in DP0]
def roof(c_nb, c_q):
    ax = next(i for i in range(3) if c_nb[i] != c_q[i]); sg = 1 if c_q[ax] > c_nb[ax] else -1
    return [vadd(at(c_nb), p) for p in [p for p in C8 if p[ax] == qr(sg)] + [p for p in RID if p[ax] == qm(qr(sg), P)]]
D = volume(DOD); r = volume(roof((1, 0, 0), (0, 0, 0))); dog = qs(qr(8), qm(qr(6), r))
# ---------- contacts: exact clipping of coplanar faces ----------
def faces(cell):
    V = dod(cell); out = []
    for n, d in dplanes(cell):
        pts = [p for p in V if dot(n, p) == d]
        c = [sum(qf(p[i]) for p in pts) / len(pts) for i in range(3)]; nf = [qf(x) for x in n]
        import numpy as np
        u = np.array([qf(x) for x in vsub(pts[0], [qr(Fr(0))] * 3)]) - c; u /= np.linalg.norm(u); w = np.cross(nf, u)
        pts.sort(key=lambda p: np.arctan2(np.dot(np.array([qf(x) for x in p]) - c, w), np.dot(np.array([qf(x) for x in p]) - c, u)))
        out.append((n, d, pts))
    return out
def clip(poly, n, d):
    """the part of a convex polygon (exact points) with n.x <= d"""
    out = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        va, vb = qs(dot(n, a), d), qs(dot(n, b), d)
        if sgn(va) <= 0: out.append(a)
        if sgn(va) * sgn(vb) < 0:
            t = qd(va, qs(va, vb)); out.append(vadd(a, vmul(vsub(b, a), t)))
    return out
def area2(poly):
    s = [Z, Z, Z]
    for a, b in zip(poly, poly[1:] + poly[:1]): s = vadd(s, cross(a, b))
    return dot(s, s)
def contacts(c1, c2):
    pl2 = dplanes(c2); res = []
    for n, d, pts in faces(c1):
        if not any(all(x == Z for x in cross(n, n2)) and sgn(dot(n, n2)) < 0 and all(dot(n2, p) == d2 for p in pts) for n2, d2 in pl2): continue   # opposite face, same plane
        poly = pts
        for n2, d2 in pl2: poly = clip(poly, n2, d2) if poly else poly
        if len(poly) >= 3 and area2(poly) != Z: res.append(poly)
    return res
ct = contacts((0, 0, 0), (1, 1, 0))
win = None
if len(ct) == 1:
    poly = ct[0]; sides = {qs_(dot(vsub(a, b), vsub(a, b))) for a, b in zip(poly, poly[1:] + poly[:1])}
    win = len(poly) == 4 and len(sides) == 1
ok(cap(dplanes((0, 0, 0)), dplanes((1, 1, 0))) == Z and len(ct) == 1 and win and contacts((0, 0, 0), (2, 0, 0)) == [],
   'dodecahedra on neighbouring even cells do not overlap and touch on exactly one rhombus of equal sides (the Jewel window); two cells apart along an axis they do not touch')
JW = {key(p) for p in C8} | {key(p) for p in RID}
# Fable referee 2026-10-20: the rhombus is the whole contact (two convex solids that do not overlap meet only in one common face
# plane, and clipping the coplanar faces finds all of it); and it is a thick Penrose rhombus: 108 degrees at the ridge point.
poly = ct[0]; zi = next(i for i, p in enumerate(poly) if key(p) in {key(q) for q in RID})
A_, Z_, B_ = poly[zi - 1], poly[zi], poly[(zi + 1) % 4]
cosZ = qd(dot(vsub(A_, Z_), vsub(B_, Z_)), dot(vsub(A_, Z_), vsub(A_, Z_)))
ok(cosZ == (Fr(1, 4), Fr(-1, 4)), 'the contact rhombus has 108 degrees at the ridge point (cos = (1 - sqrt5)/4) and so 72 at the cube corners: a thick Penrose rhombus')
ok(sum(1 for p in ct[0] if key(p) in JW) == 3, 'the contact rhombus has three corners of the dodecahedron at the origin (two cube corners and a ridge point) and its fourth inside that face, as the Jewel window')
# ---------- the three clusters ----------
tet = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
octa = [(2, 1, 1), (0, 1, 1), (1, 2, 1), (1, 0, 1), (1, 1, 2), (1, 1, 0)]
rh = [tuple(sum(x) for x in zip(*[v for v, s in zip([(1, 1, 0), (1, 0, 1), (0, 1, 1)], m) if s] or [(0, 0, 0)])) for m in itertools.product((0, 1), repeat=3)]
def touch(cells):
    pairs = [(a, b) for a, b in itertools.combinations(cells, 2)]
    return sum(len(contacts(a, b)) for a, b in pairs), all(cap(dplanes(a), dplanes(b)) == Z for a, b in pairs)
nt, gt = touch(tet); no, go = touch(octa); nr, gr = touch(rh)
ok(gt and nt == 6 and go and no == 12 and gr and nr == 18, f'Sunstar-Tetra / -Octa / -Rhombi: dodecahedra pairwise without overlap, meeting on {nt} / {no} / {nr} whole rhombi (as the Jewel clusters)')
corner = V3(1, 1, 1); ok(all(any(key(vadd(at(c), q)) == key(corner) for q in C8) for c in tet), 'the 4 dodecahedra of the Sunstar-Tetra share one corner, the cells\' common corner')
# the Dogstar of the odd cell (1,1,1) fills the hole of the Sunstar-Octa exactly: the odd cell = Dogstar + the 6 roofs of exactly these 6
oc = (1, 1, 1); nb6 = [tuple(oc[i] + d * (i == k) for i in range(3)) for k in range(3) for d in (1, -1)]
ok(sorted(nb6) == sorted(octa) and all(c in rh for c in nb6), 'the 6 dodecahedra whose roofs fill the odd cell round the Dogstar are exactly the Sunstar-Octa\'s, and all are corners of the Sunstar-Rhombi: the Dogstar fills each hole exactly')
log['volumes_raw'] = {'dodecahedron': qs_(D), 'Dogstar': qs_(dog), 'Sunstar-Tetra': qs_(qm(qr(4), D)), 'Sunstar-Octa': qs_(qa(qm(qr(6), D), dog)), 'Sunstar-Rhombi': qs_(qa(qm(qr(8), D), dog))}
ok(qa(qm(qr(6), D), dog) == (Fr(66), Fr(10)) and qa(qm(qr(8), D), dog) == (Fr(86), Fr(14)), f"volumes (cells of edge 2): Sunstar-Tetra 4 D = 40 + 8 sqrt5, Sunstar-Octa 6 D + Dogstar = 66 + 10 sqrt5, Sunstar-Rhombi 8 D + Dogstar = 86 + 14 sqrt5")
# the Sunstar itself: a dodecahedron and the Dogstars of its 6 face-neighbour cells (disjoint pieces of the tiling)
sun = qa(D, qm(qr(6), dog)); log['volumes_raw']['Sunstar'] = qs_(sun)
ok(sun == (Fr(46), Fr(-10)), 'the Sunstar (a dodecahedron and its 6 face Dogstars) = 46 - 10 sqrt5 (cells of edge 2)')
# the paper's unit, as #41: the 2 x 2 x 2 block of cells (the Sunstar-Hexa's cube) has edge 1, so volumes / 64
u = lambda x: qd(x, qr(64))
U = {'dodecahedron': (Fr(5, 32), Fr(1, 32)), 'Dogstar': (Fr(3, 32), Fr(-1, 32)), 'Sunstar': (Fr(23, 32), Fr(-5, 32)), 'Sunstar-Tetra': (Fr(5, 8), Fr(1, 8)),
     'Sunstar-Octa': (Fr(33, 32), Fr(5, 32)), 'Sunstar-Rhombi': (Fr(43, 32), Fr(7, 32)), 'Sunstar-Hexa': (Fr(9, 8), Fr(1, 8)), 'Sunstar-Hexa-Key': (Fr(7, 8), Fr(-1, 8))}
RAW = {'dodecahedron': D, 'Dogstar': dog, 'Sunstar': sun, 'Sunstar-Tetra': qm(qr(4), D), 'Sunstar-Octa': qa(qm(qr(6), D), dog), 'Sunstar-Rhombi': qa(qm(qr(8), D), dog),
       'Sunstar-Hexa': qa(qr(64), qm(qr(24), r)), 'Sunstar-Hexa-Key': qs(qr(64), qm(qr(24), r))}
ok(all(u(RAW[k]) == U[k] for k in U), 'at Sunstar-Hexa cube edge 1: dodecahedron (5 + sqrt5)/32, Dogstar (3 - sqrt5)/32, Sunstar (23 - 5 sqrt5)/32, Sunstar-Tetra (5 + sqrt5)/8, Sunstar-Octa (33 + 5 sqrt5)/32, Sunstar-Rhombi (43 + 7 sqrt5)/32, Sunstar-Hexa (9 + sqrt5)/8, Sunstar-Hexa-Key (7 - sqrt5)/8')
log['unit_hexa_cube_edge_1'] = {k: qs_(v) for k, v in U.items()}
# ---------- the Sunstar-Hexa and Sunstar-Hexa-Key ----------
blk = list(itertools.product((0, 1), repeat=3))
outer = [(c, tuple(c[i] + (1 if c[i] == 1 else -1) * (i == k) for i in range(3))) for c in blk for k in range(3)]
ROOFS = [planes_of(roof(a, b)) for a, b in outer]
ok(len(outer) == 24 and all(cap(a, b) == Z for a, b in itertools.combinations(ROOFS, 2)), 'Sunstar-Hexa: the 8 whole dodecahedra of a 2 x 2 x 2 block reach out of it by 24 roofs, pairwise without overlap (inner roofs stay in the block)')
hexa = qa(qr(64), qm(qr(24), r)); key_ = qs(qr(64), qm(qr(24), r))
ok(hexa == (Fr(72), Fr(8)) and key_ == (Fr(56), Fr(-8)) and qa(qm(qr(8), dog), qm(qr(24), r)) == key_,
   'Sunstar-Hexa = block 64 + 24 roofs = 72 + 8 sqrt5; the Sunstar-Hexa-Key (a block with the 24 roofs of its 6 neighbours taken out) = 56 - 8 sqrt5 = 8 Dogstars + 12 double roofs')
ok(qa(hexa, key_) == qr(128) and sgn(qs(qm(hexa, qr(11)), qm(key_, (Fr(17), Fr(4))))) == 0, 'they fill space, block for block; volume ratio (17 + 4 sqrt5)/11 = 2.358..., irrational (the Jewel Hexa and Hexa-Key: 5 : 3)')
# Fable referee 2026-10-20, the Key's make-up: a Key cell is the cube minus the 3 roofs through its outer faces = (cube minus all 6 roofs
# of its face-neighbours, the Dogstar) plus the 3 roofs on its inner faces; and across each of the 12 inner faces the two roofs share
# their base square, so they pair up base to base: 8 Dogstars and 12 double roofs.
inner = [(a, b) for a, b in itertools.permutations(blk, 2) if sorted(abs(x - y) for x, y in zip(a, b)) == [0, 0, 1]]
base = lambda a, b: frozenset(key(p) for p in roof(a, b)[:4])
ok(len(inner) == 24 and all(base(a, b) == base(b, a) for a, b in inner), 'the 24 inner roofs of a block pair up base to base across its 12 inner faces (double roofs); with the Dogstars they make the Key')
# into a key block: each of its 8 cells receives 3 roofs (through its 3 outer faces), a subset of the 6 into an odd cell, so disjoint
# contacts between neighbouring twins: rhombi between dodecahedra of the two blocks
def blk_contacts(off):
    B2 = [tuple(c[i] + off[i] for i in range(3)) for c in blk]
    return sum(len(contacts(a, b)) for a in blk for b in B2 if sorted(abs(x - y) for x, y in zip(a, b)) == [0, 1, 1])
nb12 = [o for o in itertools.product((-2, 0, 2), repeat=3) if sorted(map(abs, o)) == [0, 2, 2]]
tot12 = sum(blk_contacts(o) for o in nb12)
noov = all(cap(dplanes(a), dplanes(tuple(b[i] + o[i] for i in range(3)))) == Z for o in nb12 for a in blk for b in blk)
ok(len(nb12) == 12 and tot12 == 24 and noov, f'each Sunstar-Hexa meets its 12 neighbours on {tot12} whole rhombi in all, and no two overlap')
c440 = blk_contacts((2, 2, 0))
ok(c440 == 2, f'neighbouring Sunstar-Hexas (blocks one face diagonal apart) touch on exactly {c440} whole rhombi, as the Jewel Hexas')
# ---------- Dogstar inside its own cell's stella octangula ----------
T1 = [V3(*s) for s in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]; T2 = [[qn(x) for x in p] for p in T1]
cub = planes_of(C8); R6 = [planes_of(roof(n, (0, 0, 0))) for n in [tuple(d * (i == k) for i in range(3)) for k in range(3) for d in (1, -1)]]
def dog_in(Tp): return qs(cap(cub, Tp), vsum(cap(rp, Tp) for rp in R6))
T1p, T2p = planes_of(T1), planes_of(T2); T12 = T1p + T2p
inst = qs(qa(dog_in(T1p), dog_in(T2p)), dog_in(T12))
ok(inst == dog, 'the Dogstar lies wholly inside its own cell\'s stella octangula (volume met in full), so a Dogstar fits every cell, eight tips at each cube corner')
json.dump(log, open(os.path.join(HERE, 'sunstar-clusters.json'), 'w'), indent=1)
