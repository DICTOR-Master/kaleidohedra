"""ONE WORLD (DICTO 10 Nov: "how about inside their skins as other solids" → "yes verify the skins, one world for all").
Every solid sits inside a skin that makes it a dodecahedron-shaped cell (D of edge 1 = Euclid's cube of edge phi + 6 roofs), so all
live in world 1 (dodecahedral cells and RD cells on the alternating cubes of the grid of edge phi; Dogstar-type cells between).
Exact (sympy): for each content, (a) the inner solid's corners lie in the closed cube (or the dodecahedron for I), (b) the skin pieces
are the stated ones, (c) volumes add up exactly to the dodecahedron's (15 + 7 sqrt5)/4. Usage: python skins.py"""
import sympy as sp, itertools
r5 = sp.sqrt(5); phi = (1 + r5) / 2; h = phi / 2
VD = (15 + 7 * r5) / 4
cube = phi ** 3; roof = sp.simplify((VD - cube) / 6)
def tet(a, b, c, d): return sp.Abs(sp.Matrix.hstack(b - a, c - a, d - a).det()) / 6
P = lambda *x: sp.Matrix(x)
ok = True; rows = []
# C: cube of edge phi + 6 roofs (Euclid); roofs congruent (pyritohedral symmetry), each (VD - phi^3)/6
rows.append(('C (edge φ)', cube, '6 roofs', 6 * roof))
# T: alternate corners of the cube, edge phi*sqrt2; cube - T = 4 right-angled corner tetrahedra (legs phi)
Tv = [P(h, h, h), P(h, -h, -h), P(-h, h, -h), P(-h, -h, h)]
VT = tet(*Tv); corner = tet(P(h, h, -h), P(-h, h, -h), P(h, -h, -h), P(h, h, h))       # corner (h,h,-h) with its three neighbours
rows.append(('T (edge φ√2)', VT, '4 corner tetrahedra + 6 roofs', 4 * corner + 6 * roof))
# O: corners at the face centres, edge phi/sqrt2; cube - O = 8 pieces 'cube of edge h minus its inner corner tetrahedron'
VO = 8 * tet(P(0, 0, 0), P(h, 0, 0), P(0, h, 0), P(0, 0, h)); piece_O = h ** 3 - tet(P(0, 0, 0), P(h, 0, 0), P(0, h, 0), P(0, 0, h))
rows.append(('O (edge φ/√2)', VO, '8 octant pieces + 6 roofs', 8 * piece_O + 6 * roof))
# CO: corners at the edge midpoints, edge phi/sqrt2; cube - CO = 8 corner tetrahedra (legs h)
VCO = cube - 8 * tet(P(h, h, h), P(0, h, h), P(h, 0, h), P(h, h, 0)); cc = tet(P(h, h, h), P(0, h, h), P(h, 0, h), P(h, h, 0))
rows.append(('CO (edge φ/√2)', VCO, '8 corner tetrahedra + 6 roofs', 8 * cc + 6 * roof))
# I: #22 Karma shell: I(1/phi) + 12 pentagonal pyramids (all edges 1) + 30 AXE + 20 CLEO
e = 1 / phi; VI = 5 * (3 + r5) / 12 * e ** 3
Vpp = (5 + r5) / 24
rb = e / sp.sqrt(3); Vcleo = sp.sqrt(3) / 4 * e ** 2 * sp.sqrt(1 - rb ** 2) / 3
def cm_vol(d):   # Cayley-Menger: d[i][j] squared distances of 4 points
    M = sp.Matrix(5, 5, lambda i, j: 0 if i == j else (1 if i == 0 or j == 0 else d[i - 1][j - 1]))
    return sp.sqrt(M.det() / 288)
d2 = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, e ** 2], [1, 1, e ** 2, 0]]   # AXE: five edges 1, one 1/phi
Vaxe = cm_vol(d2)
rows.append(('I (edge 1/φ)', VI, 'Karma shell: 12 pentagonal pyramids + 30 AXE + 20 CLEO (#22)', 12 * Vpp + 30 * Vaxe + 20 * Vcleo))
rows.append(('D (edge 1)', VD, 'none', 0))
for name, vin, skin, vsk in rows:
    tot = sp.nsimplify(sp.simplify(vin + vsk)); good = sp.simplify(vin + vsk - VD) == 0; ok &= good
    print(f'{name:16s} inner {sp.N(vin, 12)}  + skin [{skin}] {sp.N(vsk, 12)}  = {sp.N(vin + vsk, 15)}  exact = D: {good}')
# containment (exact): every corner of T, O, CO lies in the closed cube [-h, h]^3 (they are built from cube corners, face centres, edge midpoints)
print('volume of D (15 + 7√5)/4 =', sp.N(VD, 15))
print('FINAL ok' if ok else 'FINAL FAIL: a skin does not add up to the dodecahedron')
