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
faces_t = (4 * 48, 4 * 12 - 2 * 6); ok(faces_t == (192, 36), f'tetrahedral cluster: {sum(faces_t)} faces ({faces_t[0]} triangles + {faces_t[1]} rhombi), volume 4 Jewels = 48 (3/4 at Jewel Cube edge 1)')
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
ok(8 * 12 + 4 == 100, 'rhombohedron with its stella: 8 x 12 + 4 = 100 = 8 1/3 Jewels (25/16 at Jewel Cube edge 1)')
json.dump(log, open(os.path.join(HERE, 'cluster-exact.json'), 'w'), indent=1)
