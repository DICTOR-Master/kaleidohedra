# Paper A (sheared space-fillers), exact volumes in Q(√5) of DICTO's skewed rhombic dodecahedron (#1) and the two DICTO skewed elongated
# dodecahedra (#7), from the Gram matrix of their unit edge directions (dot products ±1/2, ±φ/2, ±1/(2φ); read off the app's
# DICTO_DIRECTIONS, src/krp-core/src/geometry-extensions/dicto-fcc.js). A zonohedron's volume is the sum over every 3 of its zones of
# |det|, and det² is the Gram determinant of the three; each det² is shown to be a square in Q(√5) (the root checked by squaring).
# -> data/exact-volumes.txt
import itertools, sys
from fractions import Fraction as Fr
S5 = 5 ** .5
class Q:
    """a + b·√5 with a, b rational."""
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def _c(s, o): return o if isinstance(o, Q) else Q(o)
    def __add__(s, o): o = s._c(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = s._c(o); return Q(s.a - o.a, s.b - o.b)
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): o = s._c(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __eq__(s, o): o = s._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * S5
    def __repr__(s): return f'{s.a}' if s.b == 0 else (f'{s.b}√5' if s.a == 0 else f'{s.a} {"+" if s.b > 0 else "-"} {abs(s.b)}√5')
h = Q(Fr(1, 2)); p2 = Q(Fr(1, 4), Fr(1, 4)); q2 = Q(Fr(-1, 4), Fr(1, 4))   # 1/2, φ/2, 1/(2φ)
one = Q(1)
# Gram matrix of d1..d4, e16, e18 (signs as in the app)
G = [[one, -h, -h, -q2, h, -p2],
     [-h, one, -q2, -h, h, p2],
     [-h, -q2, one, q2, -p2, q2],
     [-q2, -h, q2, one, -p2, -q2],
     [h, h, -p2, -p2, one, Q(0)],
     [-p2, p2, q2, -q2, Q(0), one]]
def det3(M): return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                     + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
def sqrtQ(x):
    # find r = a + b√5 with r² = x and r ≥ 0: a² + 5b² = x.a, 2ab = x.b ; try b from the float value
    import math
    if x == Q(0): return Q(0)
    f = math.sqrt(x.f())
    for den in range(1, 400):
        for bn in range(-4000, 4001):
            b = Fr(bn, den)
            a = Fr(round((f - float(b) * 5 ** .5) * den), den)
            r = Q(a, b)
            if r * r == x and r.f() > 0: return r
    raise ValueError(f'no root in Q(√5) for {x!r}')
def vol(idx):
    tot = Q(0); parts = []
    for t in itertools.combinations(idx, 3):
        g = det3([[G[a][b] for b in t] for a in t])
        r = sqrtQ(g); tot = tot + r; parts.append(r)
    return tot, parts
out = ['DICTO · dictospheres.com', 'Paper A: exact volumes (Q(√5)), edge 1']
phi = Q(Fr(1, 2), Fr(1, 2))
for name, idx, claim in (('DICTO skewed RD (#1)', [0, 1, 2, 3], phi * phi), ('DICTO skewed ED #16 (#7)', [0, 1, 2, 3, 4], phi * phi + 2),
                         ('DICTO skewed ED #18 (#7)', [0, 1, 2, 3, 5], phi * phi * phi + Q(Fr(1, 2)))):
    v, parts = vol(idx)
    out.append(f'  {name}: volume {v!r} = {v.f():.9f}; claimed {claim!r}: {v == claim}')
# line angles among d1..d4
import math
ang = sorted(round(math.degrees(math.acos(abs(G[a][b].f()))), 6) for a, b in itertools.combinations(range(4), 2))
out.append(f'  #1 line angles between its four directions: {ang}')
print('\n'.join(out)); open('data/exact-volumes.txt', 'w').write('\n'.join(out) + '\n')
