# Progenitors step 4 (DICTO: "could FUJI, Cleo or other pieces generate suitable progenitor solids?"): the icosidodecahedron is a common core of
# both progenitors (O wraps it, its 30 corners on O's faces; Theaetetus grows it through Cleo-Icos to H). Put O on the Dharma's own ID (scale
# lambda = 3φ²/4, the middle toggle of Double Vision) and test the golden cycle with O in D's place: I ⊂ ID ⊂ O ⊂ TI ⊂ H ⊂ RT ⊂ I·φ³.
# Exact in Q(sqrt5): nesting, touching, layer volumes, closure. -> data/o-dharma.txt
exec(open('scripts/pair_chain.py').read().split("s, ts = contain(H, O)")[0])
lam = Q(Fr(9, 8), Fr(3, 8)) if False else None
from fractions import Fraction as Fr
lam = Q(Fr(9, 8), Fr(3, 8))
IDd = true_corners(st['icosidodecahedron']); IDr = true_corners(polar(true_corners(st['rhombic triacontahedron'])))
key = lambda V: frozenset(tuple((x.a, x.b) for x in v) for v in V)
assert key([[x * lam for x in v] for v in IDr]) == key(IDd), 'O does not sit on the Dharma ID at 3φ²/4'
O2 = [[x * lam for x in v] for v in O]
C = [('I', true_corners(st['icosahedron'])), ('ID', IDd), ('O', O2), ('TI', true_corners(st['truncated icosahedron'])), ('H', H),
     ('RT', true_corners(st['rhombic triacontahedron'])), ('I·φ³', true_corners(st['icosahedron (phi^3)']))]
out = ['DICTO · dictospheres.com', 'Progenitors step 4: O on the Dharma ID (scale 3φ²/4, exact), the cycle I ⊂ ID ⊂ O ⊂ TI ⊂ H ⊂ RT ⊂ I·φ³']
for (n1, A), (n2, B) in zip(C, C[1:]):
    pl = planes_exact(B); side = [[(dot(n, v) - d) for n, d in pl] for v in A]
    ok = all(not (s.f() > 1e-15) for row in side for s in row) and all(not (s.f() > 0 and s != 0) for row in side for s in row)
    touch = sum(1 for row in side if any(s == 0 for s in row))
    out.append(f'  {n1} ⊂ {n2}: inside {ok}; {touch} of {len(A)} corners of {n1} on faces of {n2}')
vol = lambda V: volume(V, np.array([[x.f() for x in v] for v in V]))
vs = [vol(V) for n, V in C]
out.append('  layer volumes: ' + '; '.join(f'{C[i][0]}→{C[i + 1][0]} {(vs[i + 1] - vs[i])!r} = {(vs[i + 1] - vs[i]).f():.6f}' for i in range(6)))
out.append(f'  closure I·φ³ / I in volume: {(vs[-1] / vs[0])!r} (φ⁹ = 38 + 17√5)')
dd = true_corners(st['dodecahedron']); plO = planes_exact(O2); plD = planes_exact(dd)
out.append(f'  O and D: D inside O {all(not ((dot(n, v) - d).f() > 1e-15) for v in dd for n, d in plO)}, O inside D {all(not ((dot(n, v) - d).f() > 1e-15) for v in O2 for n, d in plD)} (they cross: alternatives, as H and 3·I are)')
print('\n'.join(out)); open('data/o-dharma.txt', 'w').write('\n'.join(out) + '\n')
