"""The 3D Vacuus of the DICTO 1:2 Truncated Octahedron (DICTO 11 Nov: "the shots aren't vacuus at all"): the planes through its centre
spanned by its edges (each edge with the centre spans one plane), and each plane's card = the solid cut by that plane (a central polygon).
Exact (fractions) in the sum-zero 3-space of the permutohedron of (-2,-1,1,2); exported in ordinary 3D by the isometry of #105 Theorem 4.
Prints the planes, how many edges each card carries, each card's corner count, and FINAL ok if every edge is carried exactly once."""
import itertools, json, sys
from fractions import Fraction as F
from collections import Counter, defaultdict
vals = (-2, -1, 1, 2)
V = sorted(set(itertools.permutations(vals)))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def adjacent(p, q):   # an edge: swap of two values neighbouring in the sorted list (-2,-1), (-1,1), (1,2)
    d = [i for i in range(4) if p[i] != q[i]]
    return len(d) == 2 and p[d[0]] == q[d[1]] and p[d[1]] == q[d[0]] and abs(vals.index(p[d[0]]) - vals.index(p[d[1]])) == 1
E = [(p, q) for p, q in itertools.combinations(V, 2) if adjacent(p, q)]
assert len(V) == 24 and len(E) == 36
def cross_normal(a, b):   # normal in sum-zero space of the plane through 0, a, b: solve n.1 = n.a = n.b = 0
    import itertools as it
    M = [[1, 1, 1, 1], list(a), list(b)]
    # null vector of 3x4 integer matrix via 3x3 minors
    n = []
    for k in range(4):
        cols = [c for c in range(4) if c != k]
        m = [[M[r][c] for c in cols] for r in range(3)]
        det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        n.append((-1) ** k * det)
    from math import gcd
    g = gcd(*n); n = [x // g for x in n]; s = next(x for x in n if x); return tuple(x if s > 0 else -x for x in n)
planes = defaultdict(list)
for p, q in E: planes[cross_normal(p, q)].append((p, q))
H = [[F(1, 2), F(1, 2), F(-1, 2), F(-1, 2)], [F(1, 2), F(-1, 2), F(1, 2), F(-1, 2)], [F(1, 2), F(-1, 2), F(-1, 2), F(1, 2)]]
to3 = lambda y: [float(sum(h[i] * y[i] for i in range(4))) for h in H]
cards = []
for n, es in planes.items():
    pts = set(tuple(F(x) for x in v) for v in V if dot(n, v) == 0)
    for p, q in E:
        a, b = dot(n, p), dot(n, q)
        if a * b < 0: t = F(a, a - b); pts.add(tuple(F(x) + t * (F(y) - F(x)) for x, y in zip(p, q)))
    cards.append({'normal': list(n), 'edges_carried': len(es), 'corners': len(pts), 'pts3': [to3(p) for p in pts],
                  'edges3': [[to3(p), to3(q)] for p, q in es]})
kinds = Counter((c['corners'], c['edges_carried']) for c in cards)
print(f'{len(planes)} central planes carry the 36 edges; cards (corners, edges carried): {dict(kinds)}')
for c in sorted(cards, key=lambda c: (-c['corners'], c['normal'])): print('  normal', c['normal'], 'corners', c['corners'], 'edges', c['edges_carried'])
solid = {'pts3': [to3(v) for v in V], 'edges3': [[to3(p), to3(q)] for p, q in E]}
json.dump({'cards': cards, 'solid': solid}, open(sys.argv[1] if len(sys.argv) > 1 else 'vacuus3d_12.json', 'w'))
print('FINAL ok' if sum(c['edges_carried'] for c in cards) == 36 else 'FINAL FAIL')
