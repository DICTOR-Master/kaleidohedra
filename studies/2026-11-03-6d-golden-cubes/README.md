# Does 6D select the Golden Cut Cubes? (study, 2026-11-03)

DICTO proposed that "6D would seem to be a natural home for a cube octahedron": B6 contains the cube's symmetry and Z^6
carries the icosahedral (golden) cut-and-project. Separate study, not part of #89 (paper draft
papers/golden-cuts-beyond-plato; study studies/2026-11-03-golden-cuts-beyond-plato, whose cubes_lib.py is copied here
unchanged). Results note (typeset, 7 pages): `~/Documents/papers-to-read/6d-golden-cubes.pdf` (source `note/paper.html`,
printed on dicto-big-brother with ~/kres-tmp/cw-print/print.mjs, footer "study, not published").

**Answer.** Octahedron side: yes. Cube side: no, for an arithmetic reason (the square's diagonal √2).

Conventions: cube [-1,1]^3; a cut cube has corners = signed permutations of (1, 1, t), t = 1 - 2x (x = #88 unit-edge cut);
it is the cube cut by |x1|+|x2|+|x3| <= mu, mu = 2 + t. Greater t_G = 1/(1 + sqrt2 phi), lesser t_L = 1/(1 + sqrt2/phi).

## Results (exact in Q(sqrt2, sqrt5) unless marked)

**Sanity (s1, 13/13).** Icosahedral projector P = G/2 (Gram entries 1, +-1/sqrt5), P_perp = Galois conjugate; both shadows
of the 6-cube are rhombic triacontahedra (32 corners, 30 rhombi, diagonals phi); central section by physical space = regular
dodecahedron; stabiliser of physical space in B6 has order 120 (I_h), so O_h is not inherited, only T_h. E8: Z-span of the
120 unit icosians, norm 2(a + c) for |q|^2 = a + c sqrt5: rank 8, Gram det 1, even = E8; roots = units and units/phi, H4
shadows = two 600-cells with squared radii 1 and 1/phi^2. All in Q(sqrt5).

**Theorem 1 (s2, 16/16).** Distance field (field of squared-distance ratios; a similarity invariant): Q(sqrt5) for the golden
cut dodecahedra, icosahedra, tetrahedra, octahedra; Q(sqrt2, sqrt5) (degree 4) for both Golden Cut Cubes. For any cut cube it
is Q(t). t_G and t_L share the minimal polynomial z^4 - 8z^3 + 4z - 1: the two Golden Cut Cubes are Galois conjugates.
Reason: #88's c_n = 2cos(pi/n); c_3 = 1, c_5 = phi in Q(sqrt5), c_4 = sqrt2 not.

**Corollary 2 (field obstruction, proof).** Points with coordinates in Q(sqrt5) (orthonormal frame), their sections by
Q(sqrt5)-flats and projections onto Q(sqrt5)-subspaces never contain a similar copy of a Golden Cut Cube's corners. Covers the
icosahedral cut-and-project of Z^6 (shadows, tiles, windows, model sets), E8 -> H4 and its sections, the regular 4D solids at
Q(sqrt5) heights. Same with Q(sqrt2) (octagonal structures).

**Theorem 3 (s2).** Corner modules (Z-span of the corners) have rank 6 for all ten golden cuts (each is a shadow of part of
Z^6). Golden inflation phi^k M in M: k = 3 (D, I, O pairs), k = 6 (T pair); cubes: no real lambda other than an integer
(proof: lambda (2,0,0), lambda (2t,0,0) in M forces t quadratic). So the cubes' 6D lift has a degree-4 slope and no
self-similarity.

**Theorem 4 (s3, proof + exact check).** No 3D section of the 6-cube (any flat, any embedding) or tile of a section of its
honeycomb is a truncated cube: at most 6 face directions, a truncated cube has 7 (checked: 14 faces, {3: 8, 8: 6}, 7
directions). No projection either (zonotope, triangles). Cube x cube with the diagonal B3: invariant flats meeting both halves
trivially are F_mu = {(x, x/mu)} (Schur); graph sections are C cap A^-1 C, <= 6 directions. Example: A = icosahedral
5-fold rotation: 8 corners, 12 triangles, 6 of 48 cube symmetries.

**Cube x octahedron (s3).** C x C* (C* = {|y|_1 <= 1}) cut by F_mu is C cap mu C*: octahedron (1), Unborn Axes
(3 - phi = 1 + 1/phi^2), truncated octahedron (3/2), Icosaxes (phi = 1 + 1/phi), cuboctahedron (2), Greater GCC
(4 + 3/2 sqrt2 - sqrt5 - 1/2 sqrt10 ~ 2.304114), cut cube 2 + 1/phi^2 (octagon ratio phi/sqrt2), truncated cube (1 + sqrt2),
Lesser GCC (4 - 3/2 sqrt2 + sqrt5 - 1/2 sqrt10 ~ 2.533609), cut cube 2 + 1/phi (ratio 1/(sqrt2 phi)), cube (3); all matches
exact (similar(), bijection with one distance factor). Octahedron pair at golden heights between octahedron and cuboctahedron;
golden heights on the cube side are #89's rectified tesseract h = 1/phi^2, 1/phi and are off golden by sqrt2.
mu_G = a + (b - a)/phi^2 (unique with a, b in Q(sqrt2)): a = 1, b = 3 + sqrt2; mu_L: a = 7 - 3 sqrt2, b = 5 - 2 sqrt2.

**Theorem 5 (cut equals shadow; s3 exact, s4 float search + exact confirmation).** Shadow of (m, n) in Z^3 + Z^3 on F_mu is
proportional to m + n/mu (mu = phi: the Fibonacci product, Z^6 -> Z[phi]^3). D6 roots: four diagonal orbits 12+12+12+24;
the 24 mixed roots e_a +- f_b (a != b) cast (1, 1/mu, 0), the section's corners are (1, mu - 1, 0): equal only at mu = phi
(Icosaxes, point for point). Any lattice orbit: the matching condition is a degree <= 2 integer polynomial in mu, so either
a sweep (all mu; shortest norm 3) or mu rational/quadratic; 454 orbit reps of {-2..2}^6 give 38 isolated mu, all degree <= 2,
only phi from norm 2; never mu_G, mu_L. Shortest selecting norms (search {-4..4}^6, exact-confirmed; < 25 are global minima):
Icosaxes 2, truncated cube (Archimedean) 3, cut cube 2 + 1/phi 4, truncated octahedron 5, Unborn Axes 15
(e.g. (-1,-1,0 | 2,3,0)), cut cube 2 + 1/phi^2 44 (box minimum only), Golden Cut Cubes none.

**Octahedron side (s2).** Icosaxes corners = all signed permutations of (phi, 1, 0) = corners of the two pyritohedral twin
icosahedra (compound of two icosahedra, UC46, classical); Unborn Axes corners = signed permutations of (phi^2, 1, 0) = the
24 non-cube corners of the two twin dodecahedra.

**E-series (light).** E8 -> H4 is over Q(sqrt5) (Corollary 2). Coxeter-plane fields of E6, E7, E8 are Q(cos 2pi/h), h = 12, 18,
30; sqrt2 needs 8 | h: none. Natural projections only.

## Prior art (library + light web search, 2026-11-03)
Kramer-Neri 1984, Duneau-Katz 1985, Elser 1985 (Z^6 icosahedral cut-and-project); Elser-Sloane 1987, Moody-Patera 1993
(E8 -> H4, icosians); Baake 1999 and Moody 2000 surveys (library bridges/); Al-Siyabi-Koca-Koca 2020 (icosahedral polyhedra
from D6; library) and Koca et al. 2015 (pyritohedral group); Lifshitz 2002 (square/cubic Fibonacci tilings); Skilling 1976 /
compound of two icosahedra. Field constraints on quasicrystals are standard. Not found: the field obstruction for golden cuts,
the Galois pairing of the Golden Cut Cubes, the cube x octahedron sections with cut-equals-shadow.

## Uncertain / open
- E-series: natural projections only, not all subspaces.
- s4 is a floating-point search in a box (hits confirmed exactly); the norm-44 minimum is a box minimum.
- No structure over Q(sqrt2, sqrt5) in which the golden cube depth is natural was found (Theorem 3 says its lift could not be
  golden-self-similar).

## Files
scripts/: cubes_lib.py (copied from #89 study), sixd_lib.py, s1_sanity_cut_project.py, s2_field_signature.py, s3_six_d.py,
s4_min_norm.py, figs.py. data/: s1-sanity.json (13), s2-field-signature.json (16), s3-six-d.json (24), s4-min-norm.json (8);
every file carries its checks, all pass (61). figures/: fig1-cube-octahedron-6d.png, fig2-cut-and-project.png.
Run on dicto-big-brother from scripts/ with ~/geom/bin/python (each step < 170 s); figs: `python figs.py <out> <logo png>`.
