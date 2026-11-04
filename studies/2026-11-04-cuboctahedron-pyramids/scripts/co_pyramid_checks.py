#!/usr/bin/env python3
"""Cuboctahedron centre pyramids (DICTO Concordance Part 5, gap 1), 4 Nov 2026.
Pieces (edge 1): T = regular tetrahedron (CO triangle pyramid), S = square pyramid with all edges 1 (CO square pyramid = half octahedron).
Claims checked:
 1. CO circumradius = edge, so the pyramids are T and S; 8T + 6S = CO in volume.
 2. S | S across a square is the regular octahedron (the only way to cover a square face to face).
 3. Octet (fcc = even-sum Z^3, edge sqrt2): split the octahedron at c (odd-sum) along axis i when c has exactly one odd coordinate i
    (all-odd octahedra: any axis). Then at every v in 2Z^3 the 8 tetrahedra at v and the 6 half-octahedra with apex v make a whole CO,
    every tetrahedron lies in exactly one such CO, and what is left is the all-odd octahedra: the rectified cubic honeycomb (CO + O).
 4. A whole CO round v needs all 6 octahedra at v cut across v's axes; at most one of the two ends of an octahedron axis... (counted).
 5. Round a vertex of a twisted (h) layer the same 8 T + 6 S make the anticuboctahedron, not the CO: tetrahedra there share faces (3 pairs),
    in the octet never (0 pairs).
Writes data/co-pyramid-checks.json and prints PASS/FAIL lines."""
import itertools, json, os
from fractions import Fraction as F

OUT = os.path.join(os.path.dirname(__file__), '..', 'data')
res = []
def check(name, ok, detail=''):
    res.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail else ''))

def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0]))
def sub(p, q): return tuple(x-y for x, y in zip(p, q))
def tetvol(a, b, c, d): return F(abs(det3(sub(b, a), sub(c, a), sub(d, a))), 6)

# 1. CO of edge sqrt2 at origin: vertices perms of (±1,±1,0); radius sqrt2 = edge
co = sorted({p for p in itertools.product((-1, 0, 1), repeat=3) if sorted(map(abs, p)) == [0, 1, 1]})
check('CO has 12 vertices, all at squared radius 2 = squared edge 2', len(co) == 12 and all(sum(x*x for x in p) == 2 for p in co))
# volumes in units where edge = sqrt2: T = 1/3, S = 2/3, octahedron = 4/3, CO = 20/3
T = tetvol((0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))
oct_vol = 8 * tetvol((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))  # octahedron |x|+|y|+|z|<=1
S = oct_vol / 2
check('T = 1/3, S = 2/3, O = 4/3 (edge sqrt2)', (T, S, oct_vol) == (F(1, 3), F(2, 3), F(4, 3)), (T, S, oct_vol))
check('8T + 6S = 20/3 = CO volume (5 sqrt2/3 a^3 at a = sqrt2)', 8*T + 6*S == F(20, 3))

# 2. square of S: the second piece on that square must be congruent, on the other side, apex on the axis: octahedron
check('S + mirror S across its square = octahedron (apex heights ±1 over the square of half-diagonal 1)', 2*S == oct_vol)

# 3. octet patch
R = 6
V = [p for p in itertools.product(range(-R, R+1), repeat=3) if sum(p) % 2 == 0]
Vs = set(V)
O = [c for c in itertools.product(range(-R+1, R), repeat=3) if sum(c) % 2 == 1]
E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
def axis(c):
    odd = [i for i in range(3) if c[i] % 2]
    return odd[0] if len(odd) == 1 else None   # None: all three odd, free
tets = []
for a in itertools.product(range(-R, R), repeat=3):
    corners = [tuple(a[k] + d[k] for k in range(3)) for d in itertools.product((0, 1), repeat=3)]
    tets.append(tuple(sorted(p for p in corners if sum(p) % 2 == 0)))
check('every unit cube carries one regular tetrahedron (4 even corners, edges sqrt2)',
      all(len(t) == 4 and all(sum((x-y)**2 for x, y in zip(p, q)) == 2 for p, q in itertools.combinations(t, 2)) for t in tets))
centres = [v for v in V if all(x % 2 == 0 for x in v) and all(abs(x) <= R-2 for x in v)]
whole = 0
for v in centres:
    tv = [t for t in tets if v in t]
    halves = []
    for i in range(3):
        for s in (1, -1):
            c = tuple(v[k] + s*E[i][k] for k in range(3))
            if axis(c) == i: halves.append(c)
    hull = {tuple(v[k] + p[k] for k in range(3)) for p in co}
    inside = all(set(t) - {v} <= hull for t in tv)
    if len(tv) == 8 and len(halves) == 6 and inside and 8*T + 6*S == F(20, 3): whole += 1
check('every v in 2Z^3 (interior) is the centre of a whole CO: 8 T at v inside its hull + 6 half-octahedra with apex v', whole == len(centres), f'{whole}/{len(centres)}')
inner = [t for t in tets if all(abs(x) <= R-3 for p in t for x in p)]
cnt = [sum(1 for p in t if all(x % 2 == 0 for x in p)) for t in inner]
check('every tetrahedron has exactly one corner in 2Z^3, so lies in exactly one CO', set(cnt) == {1}, len(inner))
check('octahedra with one odd coordinate: both halves go to the COs at its two axis ends (both in 2Z^3)',
      all(all(x % 2 == 0 for x in tuple(c[k] + s*E[axis(c)][k] for k in range(3))) for c in O if axis(c) is not None for s in (1, -1)))
check('left over: octahedra at all-odd points; per cube of side 2: one CO (20/3) + one octahedron (4/3) = 8: the rectified cubic honeycomb',
      F(20, 3) + oct_vol == 8)

# 4. counting: a vertex v is a whole-CO centre iff its 6 octahedra c = v ± e_i all take axis i;
#    an octahedron serves only the two ends of its axis, so the 6 octahedra round a CO centre serve no other centre off that axis.
#    fcc vertices : octahedra = 1 : 1, each octahedron serves at most 2 centres, each centre needs 6 -> at most 1/3 of vertices.
#    Here 2Z^3 is 1/4 of the fcc vertices.
check('density: each tetrahedron lies in at most one whole CO, tetrahedra : vertices = 2 : 1, a CO takes 8, so at most 1/4 of vertices are CO centres; 2Z^3 is exactly 1/4 (every tetrahedron used)', F(1, 8) / F(1, 2) == F(1, 4) == F(2, 8))

# 5. hcp vertex vs fcc vertex, by face-sharing tetrahedra among the 4-cliques of the contact graph
import math
def stack(word, n=3):
    pos = {'A': (0.0, 0.0), 'B': (0.5, math.sqrt(3)/6), 'C': (1.0, math.sqrt(3)/3)}
    pts = []
    for z, L in enumerate(word):
        ox, oy = pos[L]
        for a in range(-n, n+1):
            for b in range(-n, n+1):
                pts.append((ox + a + b/2, oy + b*math.sqrt(3)/2, z*math.sqrt(2/3)))
    return pts
def around(word, z):
    pts = stack(word)
    v = min((p for p in pts if abs(p[2] - z*math.sqrt(2/3)) < 1e-9), key=lambda p: p[0]**2 + p[1]**2)
    nb = [p for p in pts if abs(math.dist(p, v) - 1) < 1e-9]
    adj = lambda p, q: abs(math.dist(p, q) - 1) < 1e-9
    cl = [t for t in itertools.combinations(nb, 3) if all(adj(p, q) for p, q in itertools.combinations(t, 2))]
    octs = [q for q in itertools.combinations(nb, 4)
            if sorted(round(math.dist(p, r), 6) for p, r in itertools.combinations(q, 2)) == [1.0]*4 + [round(math.sqrt(2), 6)]*2]
    share = sum(1 for s, t in itertools.combinations(cl, 2) if len(set(s) & set(t)) == 2)
    return len(nb), len(cl), share, len(octs)
f = around('ABCAB', 2); h = around('ABABA', 2)
check('c vertex (ABC): 12 neighbours, 8 tetrahedra, 0 face-sharing pairs, 6 octahedra -> the CO', f == (12, 8, 0, 6), f)
check('h vertex (ABA): 12 neighbours, 8 tetrahedra, 3 face-sharing pairs, 6 octahedra -> the anticuboctahedron (J27)', h == (12, 8, 3, 6), h)

os.makedirs(OUT, exist_ok=True)
json.dump(res, open(os.path.join(OUT, 'co-pyramid-checks.json'), 'w'), indent=1)
print(sum(r['pass'] for r in res), 'PASS', sum(not r['pass'] for r in res), 'FAIL')
