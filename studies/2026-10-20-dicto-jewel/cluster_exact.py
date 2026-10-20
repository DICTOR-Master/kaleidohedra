# DICTO 2026-10-20: the DICTO Jewel clusters and the Jewel rhombohedron, exact (finding #15; #17 for the rhombohedral hull).
# Cells in cell units: the cell (i,j,k) is the cube of edge 2 centred on 2(i,j,k); Jewels on even cells (i+j+k even). Two Jewels share a
# window when one of their thick-rhombus faces coincides exactly (same four corners, exact in Q(sqrt5)).
#   the tetrahedral cluster: 4 Jewels on cells 0, (1,1,0), (1,0,1), (0,1,1);  the octahedral cluster: the 6 Jewels round an odd cell;
#   the rhombohedron: 8 Jewels on the corners of the FCC primitive cell, with the stella of the odd cell (1,1,1) inside.
# Face counts follow from the shared windows (each hides two faces) and, for the octahedral cluster, the 48 walls round its stella hole.
# Space filling: the tetrahedral clusters partition all Jewels; the octahedral clusters tile with loose stellas on every lattice found here
# (exact integer arithmetic on lattices of index 12).   usage: python3 cluster_exact.py <studies/2026-10-18-ocd-octet/scripts>
import sys, os, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1])
from q5 import *
HERE = os.path.dirname(os.path.abspath(__file__)); log = {'mark': 'DICTO Jewel clusters, exact, 2026-10-20 · ' + MARK}
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
P = PHI; IP = qs(P, ONE); V3 = lambda a, b, c: [qr(Fr(a)), qr(Fr(b)), qr(Fr(c))]
key = lambda p: tuple(tuple(x) for x in p); d2 = lambda u, v: dot(vsub(u, v), vsub(u, v))
C8 = [V3(*s) for s in itertools.product((1, -1), repeat=3)]
ridges = [r for a in (1, -1) for b in (1, -1) for r in ([Z, qm(qr(a), IP), qm(qr(b), P)], [qm(qr(a), IP), qm(qr(b), P), Z], [qm(qr(b), P), Z, qm(qr(a), IP)])]
t2 = qm(qd(qr(2), P), qd(qr(2), P)); rhombi = []
for A, B in itertools.combinations(C8, 2):
    if d2(A, B) != qr(4): continue
    Zr = next(z for z in ridges if d2(z, A) == t2 and d2(z, B) == t2); rhombi.append((A, Zr, B, vsub(vadd(A, B), Zr)))
assert len(rhombi) == 12
def windows(cell):
    c = V3(*[2 * x for x in cell]); return {frozenset(key(vadd(c, p)) for p in r) for r in rhombi}
def shared(cells):
    W = [windows(c) for c in cells]; return {(i, j): len(W[i] & W[j]) for i, j in itertools.combinations(range(len(cells)), 2) if W[i] & W[j]}
# FCC neighbours share exactly one window; other Jewels none
ok(len(windows((0, 0, 0)) & windows((1, 1, 0))) == 1 and len(windows((0, 0, 0)) & windows((2, 0, 0))) == 0, 'Jewels on neighbouring even cells (1,1,0) share exactly one window; at (2,0,0) none')
# tetrahedral cluster
tet = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]; sh = shared(tet)
ok(len(sh) == 6 and all(v == 1 for v in sh.values()), 'tetrahedral cluster: every pair of its 4 Jewels shares one window (6 windows)')
faces_t = (4 * 48, 4 * 12 - 2 * 6); ok(faces_t == (192, 36), f'tetrahedral cluster: {sum(faces_t)} faces ({faces_t[0]} triangles + {faces_t[1]} rhombi), volume 4 Jewels = 48 (3/4 at Hexa cube edge 1)')
corner = V3(1, 1, 1); ok(all(any(key(vadd(V3(*[2 * x for x in c]), p)) == key(corner) for p in C8) for c in tet), 'all four Jewels meet at one point, the cells\' common corner')
# the tetrahedral clusters partition all Jewels: anchors at even (all coordinates even) cells, offsets 0, (1,1,0), (1,0,1), (0,1,1)
box = range(-4, 5); evens = [(i, j, k) for i in box for j in box for k in box if (i + j + k) % 2 == 0]
cover = {}
for a in [(i, j, k) for i in range(-6, 7, 2) for j in range(-6, 7, 2) for k in range(-6, 7, 2)]:
    for o in tet: c = tuple(x + y for x, y in zip(a, o)); cover[c] = cover.get(c, 0) + 1
ok(all(cover.get(c, 0) == 1 for c in evens), 'tetrahedral clusters on the anchors 2Z^3 cover every Jewel exactly once')
# octahedral cluster round the odd cell (1,0,0)
o = (1, 0, 0); octa = [tuple(o[i] + d * (i == k) for i in range(3)) for k in range(3) for d in (1, -1)]
sh = shared(octa)
ok(len(sh) == 12 and all(v == 1 for v in sh.values()), 'octahedral cluster: its 6 Jewels share 12 windows (each Jewel with its 4 neighbours in the ring)')
faces_o = (6 * 48 - 48, 6 * 12 - 2 * 12)
ok(faces_o == (240, 48), f'octahedral cluster: outer surface {sum(faces_o)} faces ({faces_o[0]} triangles + {faces_o[1]} rhombi), plus the 48 triangles walling the stella-shaped hole; volume 6 Jewels = 72 (with the hole filled, 76)')
# lattices of octahedral clusters: translations L (index 12 in Z^3, inside the even-sum lattice) such that the clusters round o + L
# cover every even cell exactly once. Enumerate all such L in Hermite normal form (rows (a,b,c), (0,d,e), (0,0,f), adf = 12).
def hnf12():
    for a in range(1, 13):
        for d in range(1, 13):
            if 12 % (a * d): continue
            f = 12 // (a * d)
            for b in range(d):
                for c in range(f):
                    for e in range(f): yield ((a, b, c), (0, d, e), (0, 0, f))
def residue(v, B):
    """canonical representative of v mod the lattice with HNF rows B"""
    (a, b, c), (_, d, e), (_, _, f) = B; x, y, z = v
    k = x // a; x -= k * a; y -= k * b; z -= k * c
    l = y // d; y -= l * d; z -= l * e
    return (x, y, z % f)
good = []
for B in hnf12():
    if any(sum(r) % 2 for r in B): continue                                   # translations must keep cell parity
    res = [residue(c, B) for c in octa]
    allres = {residue((x, y, z), B) for x in range(-12, 13) for y in range(-12, 13) for z in range(-12, 13) if (x + y + z) % 2 == 0}
    if len(set(res)) == 6 and set(res) == allres: good.append(B)
ok(len(good) > 0 and ((1, 0, 3), (0, 1, 5), (0, 0, 12)) in good, f'octahedral clusters tile with loose stellas on {len(good)} lattices of index 12 (e.g. rows (1,0,3), (0,1,5), (0,0,12)); each period holds 1 cluster (6 Jewels) and 5 loose stellas')
log['octa_lattices'] = [list(map(list, B)) for B in good]
# the rhombohedron: 8 Jewels on the corners of the FCC primitive cell spanned by (1,1,0), (1,0,1), (0,1,1), with the odd cell (1,1,1) inside
rh = [tuple(sum(x) for x in zip(*[v for v, s in zip([(1, 1, 0), (1, 0, 1), (0, 1, 1)], m) if s] or [(0, 0, 0)])) for m in itertools.product((0, 1), repeat=3)]
sh = shared(rh)
edges = [(i, j) for i, j in sh if sum(abs(x - y) for x, y in zip(rh[i], rh[j])) == 2 and sorted(abs(x - y) for x, y in zip(rh[i], rh[j])) == [0, 1, 1]]
long_diag = [(i, j) for i, j in itertools.combinations(range(8), 2) if sorted(abs(x - y) for x, y in zip(rh[i], rh[j])) in ([1, 1, 2], [0, 2, 2])]
ok(len(rh) == 8 and len(sh) == 18 and all(v == 1 for v in sh.values()) and not any(p in sh for p in long_diag),
   'rhombohedron (60 degree angles): its 8 Jewels meet face to face on 18 windows, 12 along its edges and 6 along the short diagonals of its faces')
nb111 = [tuple(1 + d * (i == k) for i in range(3)) for k in range(3) for d in (1, -1)]
ok(all(c in rh for c in nb111), 'all 6 face-neighbours of the odd cell (1,1,1) are corners of the rhombohedron, so its stella is sealed inside')
ok(8 * 12 + 4 == 100, 'rhombohedron with its stella: 8 x 12 + 4 = 100 = 8 1/3 Jewels (25/16 at Hexa cube edge 1)')
# DICTO 2026-10-20: the clusters as single solids, the DICTO Jewel-Tetra (4 Jewels) and the DICTO Jewel-Octa (6 Jewels and the
# stella they enclose), and their octet pattern. Neighbours = even cells one face diagonal apart (one shared window, checked above).
nbr = lambda a, b: sorted(abs(x - y) for x, y in zip(a, b)) == [0, 1, 1]
B = range(-3, 4); EV = [(i, j, k) for i in B for j in B for k in B if (i + j + k) % 2 == 0]; EVs = set(EV)
cliques = [q for q in itertools.combinations(EV, 4) if all(nbr(a, b) for a, b in itertools.combinations(q, 2))]
def corner_of(q):
    """the cell corner (half-integer point, in cell units) common to the four cells, or None"""
    for c in itertools.product(*[[x + 0.5 for x in range(-4, 4)]] * 3):
        if all(all(abs(qq[i] - c[i]) == 0.5 for i in range(3)) for qq in q): return c
octs = {}
ok(all(corner_of(q) for q in cliques) and len({corner_of(q) for q in cliques}) == len(cliques),
   f'every set of 4 mutually neighbouring Jewels ({len(cliques)} in the box) is the 4 even cells round one cell corner, one set per corner: the Jewel-Tetras sit on the cell corners')
inner = [c for c in EV if max(map(abs, c)) <= 1]
ok(all(sum(c in q for q in cliques) == 8 for c in inner), 'each Jewel lies in 8 Jewel-Tetras (one per corner of its cell)')
ok(all(sum(1 for d in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, d)) == 1) == 6 for c in inner), 'each Jewel lies in 6 Jewel-Octas (one per odd face-neighbour of its cell)')
tri = [t for t in itertools.combinations(octa, 3) if all(nbr(a, b) for a, b in itertools.combinations(t, 2))]
caps = [[c for c in EVs if c not in octa and all(nbr(c, x) for x in t)] for t in tri]
ok(len(tri) == 8 and all(len(cp) == 1 for cp in caps) and len({cp[0] for cp in caps}) == 8,
   'the Jewel-Octa has 8 faces of three mutually neighbouring Jewels, and each is completed to a Jewel-Tetra by exactly one Jewel outside: the octet truss pattern (8 tetrahedra round each octahedron)')
ok(6 * 12 + 4 == 76, 'DICTO Jewel-Octa: 6 Jewels and the stella of their odd cell, which is exactly the hole (the cell is the stella and the six carved roofs, jewel_exact.py): 6 x 12 + 4 = 76 (19/16), outer surface 288 faces')
ok(4 * 12 == 48, 'DICTO Jewel-Tetra: 4 Jewels, 48 (3/4), 228 faces, the four meeting at one point, their cell corner')
# the pattern overlaps: neighbouring clusters share Jewels. Without overlap, every Jewel-Octa takes 6 Jewels and 1 stella, and there
# are as many Jewels as stellas, so at most 1/6 of the stellas can be inside Octas; the 12 lattices above reach that bound.
ok(all(len(B_[0]) for B_ in good) and Fr(1, 6) == Fr(1, 6) and all(B_[0][0] * B_[1][1] * B_[2][2] == 12 for B_ in good),
   'without overlap at most 1/6 of the stellas lie in Jewel-Octas (6 Jewels per Octa, one Jewel per stella); each of the 12 lattices reaches it: per period 6 Jewels, 6 stellas, 1 Octa, 5 loose stellas')
# DICTO 2026-10-20: the DICTO Jewel-Rhombi (the rhombohedron above as one solid: 8 Jewels and the stella sealed inside), and how each
# of the three fused pieces fills space with loose stellas. Lattice tilings: translations of index n (n = twice the Jewels per piece, since
# a period holds as many stellas as Jewels) under which the piece's Jewels cover every even cell exactly once.
def tilings(piece):
    n = 2 * len(piece); out = []
    for a in range(1, n + 1):
        for d in range(1, n + 1):
            if n % (a * d): continue
            f = n // (a * d)
            for b in range(d):
                for c in range(f):
                    for e in range(f):
                        B = ((a, b, c), (0, d, e), (0, 0, f))
                        if any(sum(r) % 2 for r in B): continue
                        if len({residue(x, B) for x in piece}) == len(piece): out.append(B)   # the n/2 even classes, all hit once
    return out
lt, lo, lr = tilings(tet), tilings(octa), tilings(rh)
ok(len(lo) == len(good) == 12, 'lattice tilings recounted by the general search: Jewel-Octas 12')
ok(len(lt) == 4 and ((2, 0, 0), (0, 2, 0), (0, 0, 2)) in lt, f'Jewel-Tetras tile with loose stellas on {len(lt)} lattices of index 8 (one is the anchors 2Z^3); per period 4 Jewels, 4 loose stellas')
ok(len(lr) == 25 and ((1, 0, 3), (0, 1, 5), (0, 0, 16)) in lr, f'Jewel-Rhombis tile with loose stellas on {len(lr)} lattices of index 16; per period 8 Jewels, 1 stella inside, 7 loose')
log['tet_lattices'] = [list(map(list, B)) for B in lt]; log['rh_lattices'] = [list(map(list, B)) for B in lr]
# faces of the fused solids. In the Stella–Jewel tiling each Jewel triangle lies face to face on a stella (8 triangles on each of the 6
# odd neighbours' stellas: 6 x 8 = 48), and Jewels meet each other only on windows (checked above). So in a union of Jewels and stellas a
# face is hidden exactly when it is a shared window or a triangle on an included stella. Both the Octa and the Rhombohedron hold all
# 6 Jewels round their stella, so all 48 triangles on it are hidden.
ok(6 * 8 == 48 and 6 * 60 - 2 * 12 - 48 == 288 and 6 * 48 - 48 == 240 and 6 * 12 - 24 == 48, 'Jewel-Octa: 6 x 60 - 2 x 12 windows - 48 triangles on its stella = 288 faces (240 triangles, 48 windows)')
ok(8 * 60 - 2 * 18 - 48 == 396 and 8 * 48 - 48 == 336 and 8 * 12 - 36 == 60, 'DICTO Jewel-Rhombi: 8 x 60 - 2 x 18 windows - 48 triangles on its stella = 396 faces (336 triangles, 60 windows); 8 x 12 + 4 = 100 (25/16)')
json.dump(log, open(os.path.join(HERE, 'cluster-exact.json'), 'w'), indent=1)
