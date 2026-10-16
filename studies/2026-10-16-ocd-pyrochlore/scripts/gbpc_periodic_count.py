# Fable, GBPC pass 3 (2026-10-16): exact count for PERIODIC tilings of G' whose tile edges are all rational multiples of phi|v|
# (any number of sizes, face to face or not). Exact in Q(sqrt5).
import sys, os
from fractions import Fraction as Fr
class Q:
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): return Q(s.a + o.a, s.b + o.b)
    def __mul__(s, o): return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def __truediv__(s, o): n = o.a * o.a - 5 * o.b * o.b; return s * Q(o.a / n, -o.b / n)
    def __repr__(s): return f'{s.a} + {s.b}*sqrt5'
phi = Q(Fr(1, 2), Fr(1, 2))
dO = Q(376, -168)                          # oblate spanned by three five-fold vectors (edge |v|), exact (gbpc_two_size.py)
VG = Q(Fr(704, 81), Fr(-928, 243))         # G' per bcc cell (pass 1)
x = VG / (dO * phi * phi * phi)            # = X + Y*phi, X = sum of r^3 over oblates, Y over prolates (edge r*phi|v|), both rational
X, Y = x.a - x.b, 2 * x.b
lines = ['DICTO · dictospheres.com',
         f"G' per cell / (phi^3 * oblate volume at edge |v|) = {x!r} = X + Y*phi with X = {X} (sum of r^3 over oblates), Y = {Y} (over prolates)",
         'tile edges r*phi|v| with r rational: oblate volume r^3 phi^3 dO, prolate r^3 phi^4 dO = r^3 phi^3 dO * phi; 1 and phi independent over Q,',
         f'so a periodic tiling (finitely many tiles per period) needs X = {X} >= 0: ' + ('IMPOSSIBLE' if X < 0 else 'possible')]
print('\n'.join(lines)); open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'gbpc-periodic-count.txt'), 'w').write('\n'.join(lines) + '\n')
