# DICTO 2026-10-20: the revised DBT, the rhombic triacontahedron cut the same way at all 8 key sites (its three-fold corners on the
# octahedron's face normals), exact in Q(sqrt5). It is the RT (or the DBT) intersected with the octahedron |x|+|y|+|z| <= R.
# Checks: corners, faces and edges; no new corners; volume = RT - 8 keys; each octahedron face holds the DBT's pole triangle;
# pyritohedral symmetry (the OG's), not full octahedral; the OG lies inside; share of space; the 6 corner spaces.
import os, sys, json, itertools
ME = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(ME, '..', '2026-10-18-ocd-octet', 'scripts'))
from q5 import *
from exactpoly import planes_of, intersect, volume
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True)
qstr = lambda x: f'{x[0]} + {x[1]}*sqrt5 = {qf(x):.6f}'
D = json.load(open(os.path.join(ME, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json')))
V = [[q(c) for c in v] for v in D['V']]; R = q(D['R'])
B = json.load(open(os.path.join(ME, 'dbt-exact.json'))); DB = [[q(c) for c in v] for v in B['V']]
OCT = [[R if (i == j and s > 0) else (qn(R) if i == j else Z) for j in range(3)] for i in range(3) for s in (1, -1)]
PO = planes_of(OCT); PD = planes_of(DB)
C = intersect(PD + PO); key = lambda v: tuple(v)
ok(len(C) == 24, f'{len(C)} corners')
ok({key(v) for v in C} <= {key(v) for v in DB}, 'no new corners: every corner is a corner of the DBT (so of the triacontahedron)')
P = planes_of(C)
on = lambda pl: [v for v in C if dot(pl[0], v) == pl[1]]
kinds = {}
for pl in P:
    k = len(on(pl)); kinds[k] = kinds.get(k, 0) + 1
E = sum(len(on(pl)) for pl in P) // 2
ok(len(P) == 38 and kinds == {4: 6, 3: 32} and len(C) - E + len(P) == 2, f'{len(P)} faces {kinds} (4 = whole rhombi, 3 = triangles), {E} edges, Euler 2')
tri = [pl for pl in P if len(on(pl)) == 3]
octf = [pl for pl in tri if any(all(dot(n, v) == d for v in on(pl)) for n, d in PO)]   # all 3 corners on an octahedron face plane
s2 = (Fr(8, 3), Fr(-8, 9))
def sides(pl): Q = on(pl); return sorted([dot(vsub(a, b), vsub(a, b)) for a, b in itertools.combinations(Q, 2)], key=qf)
ok(len(octf) == 8 and all(all(x == s2 for x in sides(pl)) for pl in octf), 'each of the 8 octahedron faces holds an equilateral triangle, side^2 8/3 - 8sqrt5/9 (the DBT pole triangle)')
half = [pl for pl in tri if pl not in octf]
rh = [pl for pl in P if len(on(pl)) == 4]
ok(len(half) == 24, '24 half-rhombus triangles (rhombi cut along the long diagonal)')
vol = volume(C); RTv = (Fr(-320, 27), Fr(160, 27)); keyv = (Fr(-44, 81), Fr(20, 81))
ok(vol == qs(RTv, qm(qr(8), keyv)) and vol == (Fr(-608, 81), Fr(320, 81)), f'volume {qstr(vol)} = triacontahedron - 8 keys')
DBv = (Fr(-872, 81), Fr(440, 81)); ok(vol == qs(DBv, qm(qr(6), keyv)), 'and = DBT - its 6 remaining keys')
S = {key(v) for v in C}
def img(A, v): return tuple(dot(A[i], v) for i in range(3))
I3 = lambda p, s: [[qr(s[i]) if j == p[i] else Z for j in range(3)] for i in range(3)]
Th = [I3(p, s) for p in [(0, 1, 2), (1, 2, 0), (2, 0, 1)] for s in itertools.product((1, -1), repeat=3)]
ok(all({img(A, v) for v in C} == S for A in Th), 'symmetric under the 24 operations of the pyritohedral group Th (the OG\'s symmetry)')
ok({img(I3((1, 0, 2), (1, 1, 1)), v) for v in C} != S, 'not under the swap x <-> y (so Th, not the full octahedral group)')
ok(all(sgn(qs(d, dot(n, v))) >= 0 for v in V for n, d in P), 'the OG lies inside')
octv = qm(qr(Fr(4, 3)), qm(R, qm(R, R))); cell = qm(qr(Fr(3, 2)), octv)   # octahedron + 2 tetrahedra = 3/2 octahedron
share = qd(vol, cell); ok(True, f'share of space {qstr(share)} (DBT (493 - 219sqrt5)/6 = {qf((Fr(493, 6), Fr(-219, 6))):.6f})')
corner = qm(qs(octv, vol), qr(Fr(1, 6))); ok(corner == (Fr(112, 81), Fr(-48, 81)), f'octahedron - solid = 6 corner spaces of {qstr(corner)} (as for the DBT)')
ok(True, f'per cell left over: 6 corner spaces + 2 whole tetrahedra = {qstr(qs(cell, vol))}')
json.dump(dict(mark='DICTO · dictospheres.com', solid='triacontahedron cut at all 8 key sites (RT & octahedron)', V=[[qs_(x) for x in v] for v in C],
               volume=qs_(vol), share=qs_(share)), open(os.path.join(ME, 'cut8-exact.json'), 'w'), indent=1, ensure_ascii=False)
print('saved cut8-exact.json')
