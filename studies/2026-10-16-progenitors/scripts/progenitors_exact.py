# Exact checks for the Progenitors paper (2026-10-16), in Q(sqrt5), Dharma frame:
# (1) the DICTO Palintriacontahedron X (hull of the ID star's tips): icosahedron edge² / dodecahedron edge² = 9/5 exactly, i.e. it is the
#     convex hull of a dodecahedron and an icosahedron with edges in the ratio 3/√5; (2) the Cleo star: D′ = (2/3)·D, and
#     vol(D′) = 20 Cleo-Icos + 20 spikes + 12 inward pyramids + 30 valley tetrahedra exactly (remainder 0); each valley tetrahedron has edges
#     1 × the icosahedron edge, the D′ edge, and four Cleo-Ico side edges. -> data/progenitors-exact.txt
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
from fractions import Fraction as Fr
d2 = lambda a, b: dot([a[i] - b[i] for i in range(3)], [a[i] - b[i] for i in range(3)])
emin = lambda V: min((d2(a, b) for a, b in itertools.combinations(V, 2)), key=lambda q: q.f())
out = ['DICTO · dictospheres.com', 'Progenitors: exact checks (Q(√5))']
# (1) X
ID = C[1][1]; fc = []
for idx in planes(ID): fc.append(([sum((ID[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)], len(idx)))
T3 = [[x * 2 for x in c] for c, n in fc if n == 3]; T5 = [[x * 2 for x in c] for c, n in fc if n == 5]
out.append(f'  (1) X: dodecahedron of the 20 triangle tips, edge² {emin(T3)!r}; icosahedron of the 12 pentagon tips, edge² {emin(T5)!r}; ratio² {(emin(T5) / emin(T3))!r} (9/5 means 3/√5)')
# (2) Cleo star
I = C[0][1]; Dd = true_corners(st['dodecahedron'])
tri = [[I[i] for i in idx] for idx in planes(I)]
tips = [[(t[0][k] + t[1][k] + t[2][k]) * Q(Fr(2, 3)) for k in range(3)] for t in tri]
key = lambda V: frozenset(tuple((x.a, x.b) for x in v) for v in V)
out.append(f'      D′: the 20 tips are (2/3)·D exactly: {key(tips) == key([[x * Q(Fr(2, 3)) for x in v] for v in Dd])}')
O0 = [Q(0)] * 3
def tetvol(a, b, c, d):
    u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]; w = [d[i] - a[i] for i in range(3)]
    x = det3(u, v, w); return (x if x.f() > 0 else -x) / 6
vcore = sum((tetvol(O0, *t) for t in tri), Q(0)); vsp = sum((tetvol(*t, tp) for t, tp in zip(tri, tips)), Q(0))
plD = planes_exact(tips); vpyr = Q(0)
for n, dd in plD:
    base = [v for v in tips if dot(n, v) == dd]; apex = max(I, key=lambda v: dot(n, v).f()); c0 = [sum((b[k] for b in base), Q(0)) / len(base) for k in range(3)]
    # fan the pentagon from its centre: order by angle (float), then exact tetrahedra (apex, centre, consecutive corners)
    import math; cf = np.array([x.f() for x in c0]); nf = np.array([x.f() for x in n]); a0 = np.array([x.f() for x in base[0]]) - cf
    order = sorted(base, key=lambda v: math.atan2(np.cross(a0, np.array([x.f() for x in v]) - cf) @ nf, a0 @ (np.array([x.f() for x in v]) - cf)))
    vpyr = vpyr + sum((tetvol(apex, c0, order[i], order[(i + 1) % 5]) for i in range(5)), Q(0))
e1 = emin(I); vval = Q(0); shapes = set()
for a, b in itertools.combinations(I, 2):
    if d2(a, b) != e1: continue
    two = [tp for t, tp in zip(tri, tips) if any(all(x == y for x, y in zip(v, a)) for v in t) and any(all(x == y for x, y in zip(v, b)) for v in t)]
    vval = vval + tetvol(a, b, two[0], two[1]); P = [a, b] + two
    shapes.add(tuple(sorted((repr(d2(P[i], P[j])) for i, j in itertools.combinations(range(4), 2)))))
vD = volume(tips, np.array([[x.f() for x in v] for v in tips]))
rem = vD - (vcore + vsp + vpyr + vval)
out.append(f'      volumes: core {vcore!r}, spikes {vsp!r}, inward pyramids {vpyr!r}, valleys {vval!r}; D′ {vD!r}; remainder {rem!r}')
out.append(f'      valley tetrahedra: {len(shapes)} shape; squared edges {sorted(next(iter(shapes)))}')
print('\n'.join(out)); open('data/progenitors-exact.txt', 'w').write('\n'.join(out) + '\n')
