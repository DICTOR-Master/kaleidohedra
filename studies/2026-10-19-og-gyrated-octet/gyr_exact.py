# The gyrated octet, exact in Q(sqrt5) (DICTO 2026-10-20, for the companion paper to #37): the joint hexagon's share of a face (what the
# twin cap is joined across), the twin cap and the bipyramid, the mirror middle piece Mg (exact volume), and the DICTO Belted
# Triacontahedron (DBT) in the gyrated octet: its twin is the DBT turned 60 degrees, and DBTs in every octahedron never overlap.
# Frame of #37: OG at the origin, octahedron |x|+|y|+|z| <= R, R = 2phi/3; twin planes x+y+z = (2k+1)R (every layer boundary, ABAB).
import os, sys, json, itertools
ME = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(ME, '..', '2026-10-18-ocd-octet', 'scripts'))
from q5 import *
from exactpoly import planes_of, intersect, volume
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True)
qstr = lambda x: f'{x[0]} + {x[1]}*sqrt5 = {qf(x):.6f}'
D = json.load(open(os.path.join(ME, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json')))
V = [[q(c) for c in v] for v in D['V']]; R = q(D['R']); THIRD2 = qr(Fr(2, 3))
N1 = [ONE, ONE, ONE]
def mir(v, level=None):   # mirror in x+y+z = level (default R)
    L = R if level is None else level; s = qm(qs(dot(N1, v), L), THIRD2); return [qs(x, s) for x in v]
eqv = lambda a, b: all(x == y for x, y in zip(a, b))
keyv = lambda v: tuple(v)
octv = qm(qr(Fr(4, 3)), qm(R, qm(R, R)))
ok(octv == (Fr(64, 81), Fr(32, 81)), f'octahedron volume {qstr(octv)}')

# 1. the joint hexagon and the faces round it
hexv = [v for v in V if dot(N1, v) == R]
d2 = sorted({dot(vsub(a, b), vsub(a, b)) for a, b in itertools.combinations(hexv, 2)}, key=qf)
s2 = d2[0]; ok(len(hexv) == 6 and sum(1 for a, b in itertools.combinations(hexv, 2) if dot(vsub(a, b), vsub(a, b)) == s2) == 6,
               f'joint hexagon: 6 OG corners on the face, 6 equal sides, side^2 {qstr(s2)}')
ok(d2[1] == qm(s2, qr(3)) and d2[2] == qm(s2, qr(4)), 'regular (short diagonals^2 = 3 side^2, long = 4 side^2)')
a2 = qm(qr(2), qm(R, R)); hshare = qd(qm(qr(6), s2), a2)
print(f'      hexagon / octahedron face = 6 s^2 / a^2 = {qstr(hshare)}; the cap meets its twin across the rest, {qstr(qs(ONE, hshare))}')

# 2. the twin cap and the bipyramid (volumes from the cell kit)
cap = (Fr(277, 1539), Fr(-79, 1539)); OGv = qs(octv, qm(qr(8), cap))
print(f'      OG volume {qstr(OGv)} (octahedron - 8 caps); twin cap = left cap + its mirror (a right cap) = {qstr(qm(qr(2), cap))}')
tet = qm(octv, qr(Fr(1, 4))); print(f'      tetrahedron {qstr(tet)}; triangular bipyramid (two tetrahedra across a twin plane) {qstr(qm(qr(2), tet))}')

# 3. the mirror middle piece Mg at a twin-plane edge: hull of a five-kite star and its mirror image, minus the OG and its twin
r2 = [dot(v, v) for v in V]; top = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == top]
i1 = [i for i in five if sgn(V[i][0]) > 0 and sgn(V[i][1]) > 0 and V[i][2] == Z][0]
star = [V[j] for j in sorted({j for f in D['faces'] if i1 in f for j in f})]
HP = star + [mir(v) for v in star]; PH = planes_of(HP); vH = volume(HP)
OGp = planes_of(V); OGm = [mir(v) for v in V]; OGmp = planes_of(OGm)
c1 = intersect(PH + OGp); c2 = intersect(PH + OGmp); v1, v2 = volume(c1), volume(c2)
ok(v1 == v2, f'the hull meets the OG and its twin in equal volumes {qstr(v1)} (mirror symmetry)')
vMg = qs(qs(vH, v1), v2)
print(f'      hull of the star and its mirror {qstr(vH)}; Mg = {qstr(vMg)} (float run: 0.049215)')

# 4. the DBT in the gyrated octet
B = json.load(open(os.path.join(ME, 'dbt-exact.json'))); DB = [[q(c) for c in v] for v in B['V']]
t = [qm(R, THIRD2)] * 3
F3 = lambda a: qr(Fr(a, 3)); R60 = [[F3(2), F3(-1), F3(2)], [F3(2), F3(2), F3(-1)], [F3(-1), F3(2), F3(2)]]
rot = lambda v: [dot(R60[i], v) for i in range(3)]
tw = {tuple(vsub(mir(v), t)) for v in DB}
ok(tw == {tuple(rot(v)) for v in DB} and tw != {tuple(v) for v in DB}, 'the DBT mirrored in its pole face = the DBT turned 60 degrees about its axis (a true twin, as the OG)')
ok(all(sgn(qs(R, dot(N1, v))) >= 0 and sgn(qa(R, dot(N1, v))) >= 0 for v in DB), 'the DBT lies between its two twin planes x+y+z = -R and +R')
# bodies: layer 0 (centres R(i,j,k), i+j+k = 0) by translation; the layers above and below are its mirror images (gyrated, ABAB)
cents = [[qr(i * 1), qr(j * 1), qr(k * 1)] for i, j, k in itertools.product(range(-2, 3), repeat=3) if i + j + k == 0]
cents = [vmul(c, R) for c in cents]
bodies = []
for c in cents:
    P = [vadd(v, c) for v in DB]
    if not all(x == Z for x in c): bodies.append(('same layer', c, P))
    bodies.append(('layer above (twin)', c, [mir(v) for v in P]))
    bodies.append(('layer below (twin)', c, [mir(v, qn(R)) for v in P]))
P0 = DB; PL0 = planes_of(P0)
def edges(P, PL):
    on = [[k for k, (n, d) in enumerate(PL) if dot(n, v) == d] for v in P]
    return [(P[a], P[b]) for a, b in itertools.combinations(range(len(P)), 2) if len(set(on[a]) & set(on[b])) >= 2]
E0 = edges(P0, PL0)
def gap(axis, A, Bp):   # exact: min over B of axis.x minus max over A of axis.x (>= 0 means separated or touching)
    a = max((dot(axis, v) for v in A), key=qf); b = min((dot(axis, v) for v in Bp), key=qf)
    assert all(sgn(qs(a, dot(axis, v))) >= 0 for v in A) and all(sgn(qs(dot(axis, v), b)) >= 0 for v in Bp); return qs(b, a)
res = {}
for kind, c, P in bodies:
    PL = planes_of(P); sep = None; touch = False
    for n, d in PL0:
        g = gap(n, P0, P)
        if sgn(g) >= 0: sep = 'face plane'; touch = g == Z; break
    if sep is None:
        for n, d in PL:
            g = gap(n, P, P0)
            if sgn(g) >= 0: sep = 'face plane'; touch = g == Z; break
    if sep is None:
        for ea in E0:
            for eb in edges(P, PL):
                ax = cross(vsub(*ea), vsub(*eb))
                if all(x == Z for x in ax): continue
                g = gap(ax, P0, P)
                if sgn(g) < 0: ax = [qn(x) for x in ax]; g = gap(ax, P0, P)
                if sgn(g) >= 0: sep = 'edge axis'; touch = g == Z; break
            if sep: break
    res.setdefault(kind, []).append((sep, touch))
    if sep is None: print('      OVERLAP (or not separated) with', kind, [qf(x) for x in c])
for kind, L in res.items():
    ok(all(s for s, _ in L), f'{kind}: {len(L)} DBTs, none overlaps the central one (exact separating planes)')
