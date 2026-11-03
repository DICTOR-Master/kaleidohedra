"""Step 1, sanity: known cut-and-project facts, exact in K = Q(sqrt2, sqrt5).
A. Icosahedral embedding of Z^6: six axes a_i of the icosahedron (one per +- pair of corners), |a_i|^2 = 2 + phi.
   Gram G_ij = a_i.a_j / (2 + phi) has entries 1 and +-1/sqrt5; P_par = G/2 is the orthogonal projector of R^6 onto
   physical space (sum a_i a_i^T = 2(2 + phi) I_3), and P_perp = I - P_par is its Galois conjugate (sqrt5 -> -sqrt5).
B. Projections of the 6-cube {0,1}^6: physical and internal shadows are rhombic triacontahedra (32 corners, 30 faces,
   all rhombi with diagonals in ratio phi).
C. Central section of the 6-cube by physical space: {x : |x.a_i| <= 1} = a regular dodecahedron (20 corners).
D. Stabiliser of physical space in B6 (signed permutations g with g P_par = P_par g): order 120 (= I_h);
   O_h (order 48) is therefore not inherited; the largest cube subgroup is the pyritohedral T_h (order 24).
E. E8 -> H4: the icosian ring (Z-span of the 120 unit icosians) with the norm F(q) = a + c, |q|^2 = a + c sqrt5, is an
   even unimodular lattice of rank 8 after doubling (Gram det 1) = E8; its 240 roots are the units and the units / phi,
   i.e. two 600-cells of radii 1 and 1/phi (Elser-Sloane 1987, Moody-Patera 1993). All coordinates lie in Q(sqrt5).
usage (dicto-big-brother): ~/geom/bin/python s1_sanity_cut_project.py -> ../data/s1-sanity.json
"""
from sixd_lib import *          # noqa
from collections import Counter
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form

out = {}
# ---------------------------------------------------------------- A. projector
A6 = [(ZERO, ONE, PHI), (ZERO, -ONE, PHI), (ONE, PHI, ZERO), (-ONE, PHI, ZERO), (PHI, ZERO, ONE), (-PHI, ZERO, ONE)]
n2 = 2 + PHI
check('|a_i|^2 = 2 + phi for all six axes', all(dot(a, a) == n2 for a in A6))
G = [[dot(a, b) / n2 for b in A6] for a in A6]
offd = {G[i][j].v for i in range(6) for j in range(6) if i != j}
check('Gram off-diagonal entries are +-1/sqrt5', offd == {K(0, 0, Fr(1, 5)).v, K(0, 0, Fr(-1, 5)).v})
S = [[sum((A6[k][i] * A6[k][j] for k in range(6)), ZERO) for j in range(3)] for i in range(3)]
check('sum a_i a_i^T = 2(2 + phi) I_3 (tight frame)', all(S[i][j] == (2 * n2 if i == j else ZERO) for i in range(3) for j in range(3)))
P = [[G[i][j] / 2 for j in range(6)] for i in range(6)]
PP = [[sum((P[i][k] * P[k][j] for k in range(6)), ZERO) for j in range(6)] for i in range(6)]
check('P_par^2 = P_par, symmetric, trace 3', all(PP[i][j] == P[i][j] and P[i][j] == P[j][i] for i in range(6) for j in range(6))
      and sum((P[i][i] for i in range(6)), ZERO) == 3)
check('P_perp = I - P_par is the Galois conjugate of P_par', all(((ONE if i == j else ZERO) - P[i][j]) == P[i][j].conj5()
                                                               for i in range(6) for j in range(6)))

# ---------------------------------------------------------------- B. shadows of the 6-cube
def shadow(axes, y): return tuple(sum((axes[i][k] * y[i] for i in range(6)), ZERO) for k in range(3))
Aperp = [tuple(c.conj5() for c in a) for a in A6]
for lab, axes in (('physical', A6), ('internal', Aperp)):
    pts = [shadow(axes, y) for y in itertools.product((0, 1), repeat=6)]
    c0 = shadow(axes, (Fr(1, 2),) * 6); pts = [vsub(p, c0) for p in pts]
    V, F = hull3(pts)
    rh = all(len(f) == 4 for f in F)
    ratios = set()
    for f in F:
        q = [V[i] for i in f]
        # order the rhombus: diagonals join the two pairs at the larger distance
        ds = sorted(((d2(q[0], q[k]), k) for k in (1, 2, 3)), key=lambda t: float(t[0]))
        opp = ds[-1][1]; others = [k for k in (1, 2, 3) if k != opp]
        dA, dB = d2(q[0], q[opp]), d2(q[others[0]], q[others[1]])
        big, small = (dA, dB) if dA > dB else (dB, dA)
        ratios.add((big / small).v)
        sides = {d2(q[0], q[k]).v for k in others} | {d2(q[opp], q[k]).v for k in others}
        rh = rh and len(sides) == 1
    check(f'{lab} shadow of the 6-cube: {len(V)} corners, {len(F)} faces, all rhombi with diagonal ratio phi '
          f'(rhombic triacontahedron)', len(V) == 32 and len(F) == 30 and rh and ratios == {(PHI * PHI).v})
    out[f'shadow_{lab}'] = {'corners': len(V), 'faces': len(F)}

# ---------------------------------------------------------------- C. central section = dodecahedron
H = [(a, ONE) for a in A6] + [(vscale(-ONE, a), ONE) for a in A6]
V = vertices_H(H)
r = {dot(v, v).v for v in V}
m = min(d2(a, b) for a, b in itertools.combinations(V, 2))
deg = Counter(sum(1 for b in V if d2(a, b) == m) for a in V)
Vd, Fd = hull3(V)
check(f'central section of the 6-cube by physical space: {len(V)} corners on one sphere, 3 edges at each, 12 regular '
      f'pentagon faces (regular dodecahedron)', len(V) == 20 and len(r) == 1 and deg == Counter({3: 20})
      and len(Fd) == 12 and all(len(f) == 5 for f in Fd))
out['central_section'] = {'corners': len(V), 'R2': kstr(K(*r.pop()))}

# ---------------------------------------------------------------- D. stabiliser of physical space in B6
stab = []
for g in signed_perms(6):
    p, s = g
    if all(P[p[i]][p[j]] * (s[i] * s[j]) == P[i][j] for i in range(6) for j in range(6)): stab.append(g)
# its action on physical space: x -> sum ... ; check it maps the 12 icosahedron corners to themselves
check(f'stabiliser of physical space in B6 (order 46080) has order {len(stab)} = |I_h|', len(stab) == 120)
out['stabiliser_order'] = len(stab)

# ---------------------------------------------------------------- E. E8 from icosians
U = v600()
def F(q):  # F(q) = a + c where |q|^2 = a + c sqrt5 (and no sqrt2 part)
    n = dot(q, q); assert n.v[1] == 0 and n.v[3] == 0; return n.v[0] + n.v[2]
def ratcoords(q):  # 8 rationals: each coordinate a + c sqrt5 -> (a, c)
    return [x for c in q for x in (c.v[0], c.v[2])]
units_phi = [vscale(PHI.inv(), u) for u in U]
gens = [ratcoords(q) for q in U]
M = sp.Matrix([[sp.Integer(4) * sp.Rational(x) for x in g] for g in gens]).T     # columns = generators, scaled by 4
Hn = hermite_normal_form(M)
check('Z-span of the 120 unit icosians has rank 8', Hn.shape[1] == 8)
Bas = Hn.T / 4                                   # rows: basis in rational coords
def fr(r): r = sp.Rational(r); return Fr(int(r.p), int(r.q))
def from_rat(row): return tuple(K(fr(row[2 * k]), 0, fr(row[2 * k + 1])) for k in range(4))
basis = [from_rat(list(Bas.row(i))) for i in range(8)]
def Bf(x, y): return (F(vadd(x, y)) - F(x) - F(y))       # = 2 * bilinear form of F
Gram = sp.Matrix([[sp.Rational(Bf(x, y).numerator, Bf(x, y).denominator) for y in basis] for x in basis])
even = all(Gram[i, i] % 2 == 0 for i in range(8))
check(f'icosian lattice with the norm 2F: Gram determinant {Gram.det()}, even, integral (E8)',
      Gram.det() == 1 and even and all(x.is_integer for x in Gram))
# units / phi lie in the lattice and have F = 1, like the units
def inlat(q): c = Bas.T.solve(sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in ratcoords(q)])); return all(x.is_integer for x in c)
check('the 240 vectors {u, u/phi} lie in the lattice and all have F = 1 (2F = 2: the 240 roots of E8)',
      all(inlat(q) for q in U + units_phi) and all(F(q) == 1 for q in U + units_phi))
rad = Counter(kstr(dot(q, q)) for q in U + units_phi)
check(f'their H4 shadows: two 600-cells, squared radii {dict(rad)} (ratio phi^2), coordinates in Q(sqrt5)',
      set(rad) == {kstr(ONE), kstr(PHI.inv() * PHI.inv())} and all(in_q5(c) for q in U + units_phi for c in q))
out['E8'] = {'gram_det': int(Gram.det()), 'shadow_radii2': dict(rad)}
dump('s1-sanity.json', out)
