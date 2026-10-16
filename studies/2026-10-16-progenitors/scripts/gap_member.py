# DICTO 2026-10-16: "one more should fit in the space between RT and the icosahedron" -> the member of the dodecahedron–icosahedron
# hull family (pentakis-type) that touches both: hull of the RT's 12 five-fold corners and the 20 face centres of I·φ³ (a dodecahedron).
# Exact in Q(√5): the two squared radii, the squared edge ratio I/D, whether every RT corner lies inside it and every corner of it inside
# I·φ³ (touching = equality), and its face count. -> data/gap-member.txt
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
from fractions import Fraction as Fr
S = dict(C); RT = S['RT']; IP = S['I·φ³']
sq = lambda v: dot(v, v)
r = sorted({sq(v).f() for v in RT}); R5 = max((v for v in RT), key=lambda v: sq(v).f()); RI2 = sq(R5)
icoRT = [v for v in RT if sq(v) == RI2]
fc = []
for idx in planes(IP):
    fc.append([sum((IP[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)])
RD2 = sq(fc[0]); assert all(sq(c) == RD2 for c in fc) and len(fc) == 20 and len(icoRT) == 12
M = icoRT + fc
phi2 = Q(Fr(3, 2), Fr(1, 2))
# e_I² = 8 R_I² / (5 + √5); e_D² = 4 R_D² / (3 φ²)  ->  ratio² = 8 R_I² · 3 φ² / ((5 + √5) · 4 R_D²)
ratio2 = RI2 * 6 * phi2 / (Q(5, 1) * RD2)
def sgn(q):  # exact sign of a + b√5
    a, b = q.a, q.b
    if b == 0: return (a > 0) - (a < 0)
    if a == 0: return (b > 0) - (b < 0)
    if (a > 0) == (b > 0): return 1 if a > 0 else -1
    big = (a * a > 5 * b * b) - (a * a < 5 * b * b)  # which term dominates
    return (1 if a > 0 else -1) * big
le = lambda x, y: sgn(y - x) >= 0
Mf = np.array([[x.f() for x in v] for v in M])
pl = planes_exact(M)
inside_RT = all(le(dot(n, v), d) for n, d in pl for v in RT)
touch_RT = sum(1 for v in RT if any(dot(n, v) == d for n, d in pl))
plI = planes_exact(IP)
inside_I = all(le(dot(n, v), d) for n, d in plI for v in M)
touch_I = sum(1 for v in M if any(dot(n, v) == d for n, d in plI))
out = ['DICTO · dictospheres.com', 'The gap member between RT and I·φ³ (exact, Q(√5))',
       f'  R_I² (RT five-fold corners) = {RI2!r};  R_D² (I·φ³ face centres) = {RD2!r}',
       f'  squared edge ratio (icosahedron / dodecahedron) = {ratio2!r} = {ratio2.f():.12f}  (ratio {ratio2.f() ** .5:.12f})',
       f'  faces {len(pl)};  RT inside: {inside_RT}, RT corners on its faces: {touch_RT};  inside I·φ³: {inside_I}, its corners on I·φ³ faces: {touch_I}']
print('\n'.join(out)); open('data/gap-member.txt', 'w').write('\n'.join(out) + '\n')
