"""Step 2: is there a lattice "cut equals shadow" selection for the D.I pair, as Icosaxes was selected for C.O?
A. Obstruction (proof + exact check). The 6D product D x D* carries the icosahedral group acting diagonally on V + V
   (V = the 3D rotation representation). An invariant lattice would make the representation rational, so its character
   rational; but the trace of a 5-fold rotation on V is 1 + 2cos72 = phi (checked on the exact matrix), so on V + V it is
   2 phi, irrational. Hence NO lattice in R^6 is invariant under the diagonal icosahedral action, and the flats y = x/mu
   (the only invariant 3-flats meeting both halves trivially, by Schur, as in the 6D study) carry no lattice shadow.
   Every rational representation containing V contains its Galois twin V' (character phi -> 1 - phi), so it has
   dimension >= 6, and in V + V' (the icosahedral Z^6) the only invariant 3-flats are V and V' (V, V' not isomorphic):
   no one-parameter family of symmetric flats at all.
B. What the icosahedral Z^6 does select (exact): with u_1..u_6 the six 5-fold axes (icosahedron corners (0, 1, phi)
   cyclic, one per axis), x = (u_i . y) embeds R^3 isometrically up to one factor (checked: sum u_i u_i^T = c I).
   Central sections by physical space of the Voronoi cells of
     Z^6  {|x_i| <= 1/2}                         -> dodecahedron (the P end)
     D6*  {|x_i| <= 1/2, |x|_1 <= 3/4}            -> icosidodecahedron (the rectified stage)
     D6   {|x_i| + |x_j| <= 1}                   -> rhombic triacontahedron (the hull at the rectified stage)
   and shadows of the shortest shells: Z^6 norm 1 -> icosahedron; D6 roots -> two icosidodecahedra (ratio phi);
   (+-1/2)^6 -> the 32 corners of a rhombic triacontahedron (20 + 12) plus interior points.
usage (dicto-big-brother): ~/geom/bin/python s2_di_lattice.py -> ../data/s2-di-lattice.json
"""
from dp_lib import *          # noqa
out = {}
h = Fr(1, 2)
A5 = [[K(h), -PHI * h, PHI.inv() * h], [PHI * h, PHI.inv() * h, K(-h)], [PHI.inv() * h, K(h), PHI * h]]
tr = A5[0][0] + A5[1][1] + A5[2][2]
def mul(X, Y): return [[sum((X[i][k] * Y[k][j] for k in range(3)), ZERO) for j in range(3)] for i in range(3)]
Pw = A5
for _ in range(4): Pw = mul(Pw, A5)
isI = all(Pw[i][j] == (ONE if i == j else ZERO) for i in range(3) for j in range(3))
check(f'A: 5-fold rotation (A^5 = I: {isI}) has trace {kstr(tr)} = phi, irrational; on V + V the trace 2 phi is irrational, '
      'so no lattice in R^6 is invariant under the diagonal icosahedral action on D x D*', isI and tr == PHI)
# its Galois twin has trace 1 - phi; V + V' has trace 1 (rational)
check('A: on V + V\' (Galois twin) the trace is phi + (1 - phi) = 1, rational (the icosahedral Z^6)', tr + (1 - PHI) == ONE)
out['obstruction'] = 'trace of a 5-fold rotation on V is phi; diagonal action on V+V has irrational character -> no invariant lattice'

# B. icosahedral Z^6
U = [(ZERO, ONE, PHI), (ZERO, ONE, -PHI), (ONE, PHI, ZERO), (ONE, -PHI, ZERO), (PHI, ZERO, ONE), (-PHI, ZERO, ONE)]
G = [[sum((u[a] * u[b] for u in U), ZERO) for b in range(3)] for a in range(3)]
c0 = G[0][0]
check(f'B: the six 5-fold axes form a tight frame: sum u u^T = {kstr(c0)} I', all(G[a][b] == (c0 if a == b else ZERO) for a in range(3) for b in range(3)))
def sec(H):
    return vertices_H(H)
ax = lambda u, s: tuple(K(s) * a for a in u)
Hz6 = [(ax(u, s), K(h)) for u in U for s in (1, -1)]
Sz6 = sec(Hz6)
pl = platonic(); D = pl['dodecahedron'][0]; I = pl['icosahedron'][0]
ok = similar(Sz6, D)[0]; check(f'B: Z^6 Voronoi cell (6-cube) central section = regular dodecahedron ({len(Sz6)} corners)', ok)
Hd6s = Hz6 + [(tuple(sum((K(s[i]) * U[i][k] for i in range(6)), ZERO) for k in range(3)), K(Fr(3, 4)))
              for s in itertools.product((1, -1), repeat=6)]
# drop duplicate / zero normals
Hd6s = [(n, d) for n, d in Hd6s if not all(x.iszero() for x in n)]
Sd6s = sec(Hd6s)
ID = cut_solid(D, K(h))
ok = similar(Sd6s, ID)[0]; check(f'B: D6* Voronoi cell central section = icosidodecahedron ({len(Sd6s)} corners)', ok)
Hd6 = [(tuple(K(s) * U[i][k] + K(t) * U[j][k] for k in range(3)), ONE) for i, j in itertools.combinations(range(6), 2)
       for s in (1, -1) for t in (1, -1)]
Sd6 = sec(Hd6)
Cd6, Fd6 = hull3(Sd6)
sig = signature(Fd6)
check(f'B: D6 Voronoi cell central section = rhombic triacontahedron ({len(Cd6)} corners, faces {sig}: 30 rhombi)', len(Cd6) == 32 and sig == {4: 30})
out['voronoi_sections'] = {'Z6': 'dodecahedron', 'D6*': 'icosidodecahedron', 'D6': 'rhombic triacontahedron'}
# shadows of shells (exact radii classes)
def shadow(v): return tuple(sum((K(v[i]) * U[i][k] for i in range(6)), ZERO) for k in range(3))
def classes(vs):
    cl = {}
    for v in vs:
        p = shadow(v); cl.setdefault(norm2(p).v, []).append(p)
    return {kstr(K(*k)): uniq(ps) for k, ps in cl.items()}
z1 = [tuple(s if j == i else 0 for j in range(6)) for i in range(6) for s in (1, -1)]
c1 = classes(z1); k1 = list(c1)
check(f'B: shadows of the 12 Z^6 vectors of norm 1: one radius class, a regular icosahedron', len(c1) == 1 and similar(list(c1.values())[0], I)[0])
roots = [tuple(s if k == i else t if k == j else 0 for k in range(6)) for i, j in itertools.combinations(range(6), 2) for s in (1, -1) for t in (1, -1)]
c2 = classes(roots)
okc = len(c2) == 2 and all(len(v) == 30 and similar(v, ID)[0] for v in c2.values())
rr = [K(*k) if False else None for k in c2]
r_vals = sorted([float(norm2(v[0])) for v in c2.values()])
check(f'B: shadows of the 60 D6 roots: two icosidodecahedra of 30 corners, squared radii ratio {r_vals[1] / r_vals[0]:.6f} = phi^2', okc and abs(r_vals[1] / r_vals[0] - float(PHI * PHI)) < 1e-12)
half = [tuple(Fr(s, 2) for s in ss) for ss in itertools.product((1, -1), repeat=6)]
c3 = classes(half)
out['half_vector_shadow_classes'] = {k: len(v) for k, v in c3.items()}
print('   (+-1/2)^6 shadow radius classes:', out['half_vector_shadow_classes'], flush=True)
kinds = {k: ('dodecahedron' if len(v) == 20 and similar(v, D)[0] else 'icosahedron' if len(v) == 12 and similar(v, I)[0] else f'{len(v)} points')
         for k, v in c3.items()}
out['half_vector_shadow_kinds'] = kinds; print('   ', kinds, flush=True)
check('B: the 64 vectors (+-1/2)^6 cast only dodecahedra and icosahedra (radius classes), i.e. 3-fold and 5-fold corners',
      all(t in ('dodecahedron', 'icosahedron') for t in kinds.values()))
out['selected_by_Z6'] = 'icosahedron (norm 1), icosidodecahedron (roots; also D6* Voronoi section), dodecahedron (Z^6 Voronoi section), RT (D6 Voronoi section): the ends and the rectified stage only; no golden cut, no continuous mu'
save('s2-di-lattice.json', out)
