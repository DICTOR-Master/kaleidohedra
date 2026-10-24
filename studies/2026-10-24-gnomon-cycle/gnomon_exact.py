# Gnomon rule for the twelve-station golden cycle (#35 Vajrayana), DICTO 2026-10-24 (idea from Júlia Pimentel's square-root method,
# (n+1)² = n² + n + (n+1): what does each step add?). Exact volumes from studies/2026-10-16-progenitors (cleo-star.txt, gap-pieces-exact.txt).
from fractions import Fraction as F
class Q:
    def __init__(s, a, b=0): s.a, s.b = F(a), F(b)
    def __mul__(s, o): return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __repr__(s): return f'{s.a} + {s.b}√5'
phi = Q(F(1, 2), F(1, 2)); I = Q(F(-5, 12), F(5, 12)); star = Q(F(-5, 6), F(5, 6)); M = Q(F(145, 12), F(65, 12)); Ip3 = Q(F(235, 12), F(35, 4))
pw = lambda k: (lambda r: r)(eval('*'.join(['phi'] * k)) if k else Q(1))
ok = [('the Cleo star is twice the icosahedron (the 20 spikes add one icosahedron)', star == I * Q(2)),
      ('the last step multiplies by φ: I·φ³ = φ·M', phi * M == Ip3),
      ('M = φ⁸·I', M == pw(8) * I), ('one turn: I·φ³ = φ⁹·I', Ip3 == pw(9) * I)]
for t, k in ok: print(('PASS ' if k else 'FAIL ') + t)
print('ALL PASS' if all(k for _, k in ok) else 'SOME FAIL')
