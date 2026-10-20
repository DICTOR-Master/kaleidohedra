# DICTO 2026-10-20: the Sunstar Lattice, exact in Q(sqrt5), for the Sunstar paper (the dodecahedral twin of the Jewel paper, #41).
# Raw frame as #8 and #41: cells are cubes of edge 2 centred on 2(i,j,k); regular dodecahedra (Euclid's cube + 6 roofs) on the even cells,
# Dogstars on the odd cells (DICTO's name; the solid is G. W. Hart's 1996 stellation 8 of the dodecahedron, also Walser, Polyhedra-World).
#   1. The Dogstar = odd cube minus the 6 roofs of its neighbours' dodecahedra; with the dodecahedra it tiles space; volume.
#   2. The Dogstar is exactly a partial stellation of the dodecahedron 1/phi^3 the cell's (same centre, same orientation): which cells.
#   3. Star Chain Reaction (#12): the great stellated dodecahedron of that core has the cell dodecahedron's 20 corners; a whole Sunstar
#      1/phi^3 the size (the core and its 6 Dogstars) lies inside it, and no larger copy does.
#   usage: python3 sunstar_exact.py <studies/2026-10-18-ocd-octet/scripts>
import sys, os, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1])
from q5 import *
from exactpoly import planes_of, intersect, volume
HERE = os.path.dirname(os.path.abspath(__file__)); log = {'mark': 'DICTO Sunstar Lattice, exact, 2026-10-20 · ' + MARK}
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
P = PHI; IP = qs(P, ONE)
V3 = lambda a, b, c: [x if isinstance(x, tuple) else qr(Fr(x)) for x in (a, b, c)]
key = lambda p: tuple(tuple(x) for x in p)
def cap(*parts_planes):
    C = intersect([pl for pls in parts_planes for pl in pls]); return volume(C) if C else Z
def vsum(xs):
    t = Z
    for x in xs: t = qa(t, x)
    return t
# ---------- the dodecahedron (Euclid: cube + 6 roofs) and the roofs ----------
C8 = [V3(*s) for s in itertools.product((1, -1), repeat=3)]
RID = [r for a in (1, -1) for b in (1, -1) for r in ([Z, qm(qr(a), IP), qm(qr(b), P)], [qm(qr(a), IP), qm(qr(b), P), Z], [qm(qr(b), P), Z, qm(qr(a), IP)])]
DOD = C8 + RID
def roof(c_nb, c_q, s=ONE):
    """the roof of the dodecahedron in cell c_nb (cells of edge 2s) on its face toward cell c_q"""
    ax = next(i for i in range(3) if c_nb[i] != c_q[i]); sg = 1 if qf(c_q[ax]) > qf(c_nb[ax]) else -1
    sq = [p for p in C8 if p[ax] == qr(sg)]; rd = [p for p in RID if p[ax] == qm(qr(sg), P)]
    return [vadd(c_nb, vmul(p, s)) for p in sq + rd]
cube = lambda c, s=ONE: [vadd(c, vmul(p, s)) for p in C8]
O = V3(0, 0, 0); E = [V3(*[d * (i == k) for i in range(3)]) for k in range(3) for d in (1, -1)]
nbs = lambda c, s=ONE: [vadd(c, vmul(e, qm(qr(2), s))) for e in E]
dvol = volume(DOD); rvol = volume(roof(V3(2, 0, 0), O))
ok(dvol == qa(qr(8), qm(qr(6), rvol)) and rvol == (Fr(1, 3), Fr(1, 3)), f'dodecahedron = cube 8 + 6 roofs of (1 + sqrt5)/3: {qs_(dvol)}')
# ---------- 1. the Dogstar ----------
R6 = [roof(n, O) for n in nbs(O)]; R6p = [planes_of(r) for r in R6]; CUBEp = planes_of(cube(O))
ok(all(cap(a, b) == Z for a, b in itertools.combinations(R6p, 2)) and all(cap(rp, CUBEp) == rvol for rp in R6p),
   'the 6 roofs reaching into an odd cell lie in it and meet only in faces (pairwise volume 0)')
dog = qs(qr(8), qm(qr(6), rvol)); log['dogstar_raw'] = qs_(dog)
ok(dog == (Fr(6), Fr(-2)), f'Dogstar = cube - 6 roofs = 6 - 2 sqrt5 = {qf(dog):.6f}; each even cell lies in its dodecahedron, whose roofs go into odd cells without overlap, so dodecahedra and Dogstars tile space')
edge = qd(qr(2), P)                                              # the dodecahedron's edge on cells of edge 2
k = qd(ONE, qm(edge, qm(edge, edge)))                            # volume factor to dodecahedron edge 1
ok(qm(dog, k) == qd(P, qr(2)), 'Dogstar volume at dodecahedron edge 1 = phi/2 exactly')
ok(qa(dvol, dog) == qr(16), 'dodecahedron + Dogstar = 16 = two cells; packing density of the dodecahedra (5 + sqrt5)/8')
def dogstar_meet(cell_planes, c=O, s=ONE):
    """exact volume of (Dogstar at c, scale s) intersected with a convex cell: cube part minus the 6 roof parts"""
    cu = planes_of(cube(c, s)); v = cap(cell_planes, cu)
    if v == Z: return Z
    for n in nbs(c, s): v = qs(v, cap(cell_planes, planes_of(roof(n, c, s))))
    return v
# ---------- 2. the stellation cells of the core dodecahedron 1/phi^3 ----------
s3 = qd(ONE, qm(P, qm(P, P)))
CORE = [vmul(p, s3) for p in DOD]; CP = planes_of(CORE); assert len(CP) == 12
BOX = [(V3(*[d * (i == k) for i in range(3)]), qr(10)) for k in range(3) for d in (1, -1)]
cells = []
for sig in itertools.product((1, -1), repeat=12):
    pl = [(n, d) if g == 1 else ([qn(x) for x in n], qn(d)) for (n, d), g in zip(CP, sig)]
    C = intersect(pl + BOX)
    if not C or any(any(abs(qf(x)) > 9.99 for x in p) for p in C): continue
    v = volume(C)
    if sgn(v) > 0: cells.append({'layer': sig.count(-1), 'planes': pl, 'corners': C, 'vol': v})
layers = [sum(1 for c in cells if c['layer'] == L) for L in range(4)]
ok(len(cells) == 63 and layers == [1, 12, 30, 20], f'the 12 face planes of the core cut space into 63 bounded cells: core 1, pyramids 12, wedges 30, spikes 20 ({layers})')
memb = []
for c in cells:
    m = dogstar_meet(c['planes']); memb.append(m)
    c['in'] = 1 if m == c['vol'] else (0 if m == Z else None)
ok(all(c['in'] is not None for c in cells), 'every stellation cell lies wholly inside the Dogstar or wholly outside it')
inl = [sum(1 for c in cells if c['layer'] == L and c['in']) for L in range(4)]
ok(inl == [1, 12, 24, 8] and vsum(c['vol'] for c in cells if c['in']) == dog,
   f'Dogstar = core + 12 pyramids + 24 of 30 wedges + 8 of 20 spikes ({inl}), volumes adding up to 6 - 2 sqrt5: an exact partial stellation of the core 1/phi^3')
miss_w = [c for c in cells if c['layer'] == 2 and not c['in']]; spk = [c for c in cells if c['layer'] == 3 and c['in']]
far = lambda C: max(C, key=lambda p: qf(dot(p, p)))
cen = lambda C: [qd(vsum(p[i] for p in C), qr(len(C))) for i in range(3)]
ok(len(miss_w) == 6 and all(sum(1 for x in cen(c['corners']) if x == Z) == 2 for c in miss_w) and {key(far(c['corners'])) for c in spk} == {key(p) for p in C8},
   'the 6 missing wedges lie on the cube axes; the tips of the 8 spikes kept are the 8 cube corners')
# ---------- 3. Star Chain Reaction ----------
gsd_tips = {key(far(c['corners'])) for c in cells if c['layer'] == 3}
ok(gsd_tips == {key(p) for p in DOD}, "the great stellated dodecahedron of the core (all 63 cells) has exactly the cell dodecahedron's 20 corners: it is the EKP cell's great star")
s = s3; small_dogs = [vmul(e, qm(qr(2), s)) for e in E]
GV = vsum(c['vol'] for c in cells)
dv_s = qm(dog, qm(s, qm(s, s)))
met = [vsum(dogstar_meet(c['planes'], sd, s) for c in cells) for sd in small_dogs]
ok(all(m == dv_s for m in met), 'each of the 6 Dogstars of the Sunstar 1/phi^3 (round the core) lies wholly inside the great star (its volume met in full)')
# no larger copy: a corner p of the small Sunstar on the great star's boundary leaves it under any enlargement about the centre
def leaves(p):
    for c in cells:
        vals = [qs(dot(n, p), d) for n, d in c['planes']]
        if any(sgn(v) > 0 for v in vals): continue                       # p strictly outside this cell: stays outside nearby
        if not any(v == Z and sgn(d) > 0 for v, (n, d) in zip(vals, c['planes'])): return False
    return True
tips = [vadd(sd, vmul(q, s)) for sd in small_dogs for q in C8]
ttop = [p for p in tips if leaves(p)]
ok(len(ttop) > 0, f'{len(ttop)} spike tips of the small Dogstars lie on the great star and leave it under any enlargement: the fit is tight, scale exactly 1/phi^3')
log['tight_tips'] = len(ttop)
log['gsd_cells_float'] = [[[qf(x) for x in p] for p in c['corners']] for c in cells]   # for the figures only
log['dogstar_cells'] = [i for i, c in enumerate(cells) if c['in']]
json.dump(log, open(os.path.join(HERE, 'sunstar-exact.json'), 'w'), indent=1)
