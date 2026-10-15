"""Exact check: our 60 tetrahedra (triacontahedron -> GSD layer) against Hafner's (2007),
each 1/6 of a prolate golden rhombohedron on the triacontahedron's edge.
Chain scale (polar in the unit sphere). Both volumes are positive, so equal squares prove equality.
Writes data/polar-hafner-exact.txt."""
from fractions import Fraction as F
import math, os

class Q:  # a + b*sqrt5, exact
    def __init__(s, a, b=0): s.a, s.b = F(a), F(b)
    def __mul__(s, o): return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    def __sub__(s, o): return Q(s.a - o.a, s.b - o.b)
    def f(s): return float(s.a) + float(s.b)*math.sqrt(5)
    def __repr__(s): return f'{s.a} + {s.b}*sqrt5'

a2 = Q(130, -58)                    # triacontahedron edge squared (snapped from data/reversed-chain.json, checked below)
ours = Q(F(188, 3), -28)            # our tetrahedron (paper section 5, polar_gsd_pieces)
phi2 = Q(F(3, 2), F(1, 2))
c2 = Q(F(2, 5), F(2, 25))           # prolate golden rhombohedron: V^2 = a^6 * (1 - 3c^2 + 2c^3), c = 1/sqrt5
hafner_sq = a2*a2*a2*c2*Q(F(1, 36))  # (V/6)^2
diff = ours*ours - phi2*phi2*hafner_sq

import json, itertools
pts = dict(json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'reversed-chain.json'))))['rhombic triacontahedron']
edge2 = min(math.dist(p, q) for p, q in itertools.combinations(pts, 2))**2
lines = [
  f'triacontahedron edge^2: exact {a2} = {a2.f():.12f}; measured from chain data {edge2:.12f}',
  f'ours: {ours} = {ours.f():.12f}',
  f'Hafner tetrahedron (1/6 prolate rhombohedron on that edge): sqrt({hafner_sq}) = {math.sqrt(hafner_sq.f()):.12f}',
  f'ours^2 - (phi^2 * Hafner)^2 = {diff}  (EXACT 0: ours = phi^2 x Hafner)',
]
assert diff.a == 0 and diff.b == 0 and abs(edge2 - a2.f()) < 1e-9
open(os.path.join(os.path.dirname(__file__), '..', 'data', 'polar-hafner-exact.txt'), 'w').write('DICTO · dictospheres.com\n' + '\n'.join(lines) + '\n')
print('\n'.join(lines))
