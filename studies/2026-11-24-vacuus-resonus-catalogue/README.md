# The Vacuus and the Resonus: the exact catalogue (24 Nov 2026)

DICTO · data study for the paper "The Vacuus and the Resonus" (working title), V SF A project.

> **Status box.** Study note, not published. Every count in this study is exact: number fields, interval or ball arithmetic
> for every sign, no rounding in any decision. All 92 Johnson solids are now exact, J84–J90 included. Nothing remains in
> floating point. Theorems A–D are proved below; the observations state their exact scope (the solids of this catalogue).
> Resume: everything committed; nothing running.

**Conclusion.**
- **Catalogue.** The Vacuus and the Resonus are computed exactly for 163 solids: 5 Platonic, 13 Archimedean, 13 Catalan,
  40 prisms, antiprisms, bipyramids and trapezohedra (n = 3–12), and all 92 Johnson solids about both centres. The table is
  `data/vacuus-resonus-catalogue.md` (and `.csv`), one row per solid.
- **J84–J90 exact.** Each lies in a number field of degree 6, 12, 8, 16, 32, 20 and 24 (in its symmetry frame, edge 1).
  Every face is checked exactly, and the floating-point pilot of the Vacuus study is confirmed for these seven.
- **(i) Theorem A.** A centrally symmetric solid has every Resonus plane carrying two parallel faces. The converse holds when
  parallel faces have equal areas (Minkowski). In the catalogue the converse fails only for the truncated tetrahedron, where each
  triangle is parallel to a hexagon.
- **(ii) Theorem B.** A plane through O is both a Vacuus plate and a Resonus plane exactly when it holds an edge and is
  parallel to a face. In the polar, this happens when an edge of P\* points along a corner ray of P\*. For prisms this happens
  exactly when n ≡ 2 (mod 4); it does in 28 solids (Archimedean, Catalan, prisms and 21 Johnson solids).
- **(iii) Theorem C.** Simplicial arrangements:
  - Near pencils: every prism has a simplicial Resonus, and every bipyramid a simplicial Vacuus.
  - Platonic and non-snub Archimedean solids: the Resonus is the set of planes at right angles to whole classes of rotation axes.
    It is simplicial exactly for the cube and for the seven Archimedean solids CO, TC, TO, RCO, TCO, RID and TID.
  - If every Vacuus plate is a mirror of Td, Oh or Ih, the Vacuus is simplicial. This covers the 5 Platonic and the 11 non-snub
    Catalan solids.
  - Johnson solids: the Resonus is simplicial only for J3, J19 and J76, which have the face directions of CO, RCO and RID.
- **(iv) Theorem D (duality).** By the polar link, Resonus(P\*) is the set of planes at right angles to the corners of P, and
  Vacuus(P\*) is the set of planes at right angles to the edges of P. It follows that:
  - Vacuus(P) ∩ Resonus(P\*) collects the edges AB with a corner C at right angles to both A and B. Among the dual pairs, only
    the octahedron (with the cube) has one.
  - Resonus(P) ∩ Vacuus(P\*) collects the faces that have an edge at right angles to them.
  - Both counts are checked on every dual pair.

## 1. Definitions (no new ones)

- **Vacuus** (#110, Section 2; vacuus-enumeration study, Section 1): one plate through the centre O and each edge. A plate is a
  **full sheet**, **shared sheet** or **single fin**, and the solid is of the **heart**, **inherited heart** or **non-heart**
  kind (DICTO's names).
- **Resonus** (DICTO, 24 Nov; resonus study): one plane through O parallel to each face; parallel faces share one plane. Below,
  a Resonus plane "carries two faces" when it comes from a pair of parallel faces.
- **Mirror**: a mirror of the solid's full symmetry group (exact reflection maps the corner set onto itself).
- **Arrangement on the sphere**: the planes cut the unit sphere into vertices, edges and regions (V/E/regions in the table).
  It is **simplicial** when every region is a triangle. A pencil (all planes through one line) is not simplicial.
- **P\***: the polar of P about O.
- **R\*(P), V\*(P)**: the planes at right angles to the corner lines and to the edge directions of P. By the polar link they are
  the Resonus and the Vacuus of P\* (resonus study, Theorem 1).
- Centres: Platonic, Archimedean, Catalan and prism-family solids use the symmetry centre. Johnson solids use (a) the corner
  centroid and (b) the volume centroid, as DICTO decided.

## 2. Method

Stage 1 (`scripts/j84_90_exact.py`, J84–J90):
- From the registry floats, Gauss–Newton at 4000 digits on the defining equations: edges of length 1, and both diagonals of
  every square of length √2.
- The solid is then placed in its symmetry frame. The axes are two mirror normals and their common axis. For the C2v and Cs
  solids (J86–J89) the origin is the axis point at the level of the largest ring of corners. Centring at the corner centroid
  instead raised the degree, so it is not used here.
- Each coordinate gets its minimal polynomial from PARI's `algdep` (LLL).
- The common field is built exactly. Each coordinate is first tested for membership in the field: a linear relation (`lindep`),
  then an exact check that it is a root of its own polynomial. Otherwise the field is joined with it by `polcompositum`, and the
  numbers only choose the factor (the real embedding). `polredbest` then gives a smaller defining polynomial.
- Exact checks in the field: every edge has squared length 1, and every square has both diagonals of squared length 2 and its
  four corners coplanar.
- The faces are regular and the solid is convex (checked exactly in stage 2). By Cauchy's rigidity theorem the polyhedron is
  then the Johnson solid of that combinatorial type.
- PARI/GP (The PARI Group), via cypari2.

Stage 2 (`scripts/catalogue.py`) reuses the exact code of study 2026-11-24-vacuus-enumeration unchanged: its builders and its
`analyse()`. The only change is that `Fld.sign` is replaced. Additions:
- **Signs.** For the sympy fields, interval arithmetic (mpmath `iv`) around a 10^-60 to 10^-3000 enclosure of the field
  generator; the precision is raised until the interval excludes 0. For J84–J90: python-flint (`fmpq_poly` modulo the defining
  polynomial, F. Johansson's Arb) at a certified real root, isolated by `complex_roots` (real roots come back with exactly zero
  imaginary part).
- **Planes.** The Resonus and Vacuus as exact plane sets, their intersection, mirror flags by exact reflection, and R\*(P) and
  V\*(P).
- **Arrangements.** Counted twice:
  - by the formula f2 = 1 − f0 + f1 on the projective plane (exact intersection lines);
  - by exact face tracing on the sphere. Angular orders come from exact determinant signs, and the trace yields every region's
    number of sides.
  - Simplicial means 2f1 = 3f2, and the run asserts that every region is then a triangle.
- **Independent checks** (asserted for every solid and centre):
  - Euler;
  - every edge lies on exactly one plate;
  - the Resonus has as many planes as faces minus parallel pairs, the pairs found by a zero cross product;
  - Theorem 1(b) of the resonus study on every edge;
  - on every dual pair, Resonus(P\*) = R\*(P) and Vacuus(P\*) = V\*(P) as exact plane sets, both ways;
  - mirror flags recomputed by exact reflection agree with `analyse()`;
  - face tracing agrees with the formula, and Euler holds on the sphere;
  - the Resonus is the same about both centres of a Johnson solid.

Further checks are in `scripts/patterns.py`:
- Mirror counts equal the group's: Td 6, Oh 9, Ih 15, O and I 0, D_nh n + 1, D_nd n.
- Prism-family plate and plane counts equal their closed forms (Section 4).
- For all 92 Johnson solids, mirrors, plates, kind and central symmetry equal the independent floating-point pilot (full group
  by search).
- Control: the truncated icosidodecahedron gives 31 Resonus planes and 480 regions, as in the resonus study.

Floats are used only to propose combinatorics: hull faces, and the cyclic order of a face's corners. Each proposal is then
certified exactly: planar, supporting, every edge equal, every edge on exactly two faces, Euler.

Stage 3:
- `scripts/axis_classes.py`: the 14 arrangements of planes at right angles to unions of axis classes (Oh and Ih, two Ih frames),
  matched exactly to every Platonic, Archimedean and Catalan Resonus and Vacuus.
- `scripts/make_table.py`: the table.
- `scripts/patterns.py`: every theorem checked on every row; every observation's scope listed (`data/patterns.txt`).

Runs: on the compute machine through the job runner, after pilots (logs in `logs/`).

## 3. J84–J90, exact

| J | solid | symmetry | field degree | defining polynomial (polredbest) | corner, volume centroid |
|---|---|---|---|---|---|
| 84 | snub disphenoid | D2d | 6 | x⁶ − 2x⁵ − 2x³ − 2x + 1 | equal |
| 85 | snub square antiprism | D4d | 12 | x¹² − 4x¹¹ − 6x¹⁰ + 56x⁹ − … + 16 (`data/j84_90_exact.json`) | equal |
| 86 | sphenocorona | C2v | 8 | x⁸ − 6x⁶ + 5x⁴ − 150x² + 625 | differ |
| 87 | augmented sphenocorona | Cs | 16 | degree 16 (file) | differ |
| 88 | sphenomegacorona | C2v | 32 | degree 32 (file) | differ |
| 89 | hebesphenomegacorona | C2v | 20 | degree 20 (file) | differ |
| 90 | disphenocingulum | D2d | 24 | degree 24 (file) | equal |

- The coordinates' own degrees are 6, 12, 8, 16, 32, 20 and 24 at most, and the field degree equals the largest of them.
- Among them, the sphenocorona coordinate 0.85272694… has minimal polynomial 60x⁴ − 48x³ − 100x² + 56x + 23.
- Vacuus (exact, both centres): J84 14, J85 36, J86 20, J87 26, J88 24, J89 32, J90 34 plates. J87 is non-heart; the other six
  are inherited heart. This agrees with the floating-point pilot.
- Resonus: 12, 25, 14, 17, 18, 21 and 24 planes. Only J85 has a pair of parallel faces (its two squares).

## 4. Theorems and observations

### (i) The Resonus analogue of "heart iff centrally symmetric"

**Theorem A.** Let P be a convex polytope in R³ and O a point inside it.
(a) The Resonus of (P, O) is the Resonus of (P, O′) moved by O′ − O. Its arrangement does not depend on the centre.
(b) |Resonus| = F − p, where p is the number of pairs of parallel faces. Each plane carries one face or two.
(c) If P is centrally symmetric, every Resonus plane carries two faces, and |Resonus| = F/2.
(d) Suppose every Resonus plane carries two faces, and each two parallel faces have equal areas. Then P is centrally symmetric.
(e) The area condition in (d) cannot be dropped.

*Proof.*
- (a) A face plane a·x = c moves to a·x = c′ under a translation, and its normal a is unchanged. The Resonus plane is
  a·(x − O) = 0.
- (b) Two faces give the same plane through O exactly when their normals are parallel. Two distinct faces of a convex polytope
  cannot have the same outward normal, so parallel faces come in pairs with opposite normals (resonus study, Theorem 1).
- (c) The point reflection maps each face F to a face −F with the opposite normal.
- (d) Assume every face normal u has −u as a face normal, with equal areas. Then −P has the same face normals and face areas
  as P. By Minkowski's uniqueness theorem (a convex polytope is determined up to translation by its face normals and face areas;
  H. Minkowski, "Allgemeine Lehrsätze über die konvexen Polyeder", 1897), −P is a translate of P, so P is centrally symmetric.
- (e) The truncated tetrahedron. ∎

Checked on all 215 solid–centre pairs:
- (b) and (c) hold on every row.
- "Every plane carries two faces and the solid is not centrally symmetric" occurs exactly once: the truncated tetrahedron, whose
  4 triangles are parallel to its 4 hexagons.
- So in this catalogue the Resonus has all its planes double exactly when the Vacuus is of the heart kind (Lemma 1), with that
  one exception.
- The opposite extreme, no two faces parallel (every plane carries one face), occurs in 31 solids:
  - the tetrahedron, triakis tetrahedron, pentagonal icositetrahedron and pentagonal hexecontahedron;
  - bipyramids with n odd and trapezohedra with n even;
  - J1, J2, J7, J9, J10, J12, J13, J14, J16, J17, J64, J84, J86, J87, J88, J89, J90.

### (ii) When the Resonus and the Vacuus share a plane

**Theorem B.** A plane H through O lies in both the Resonus and the Vacuus of (P, O) exactly when H holds an edge of P and is
parallel to a face of P. In the polar this reads: an edge [a_G, a_H] of P\* is parallel to the ray from O to a corner a_F of
P\*.

*Proof.* H is in the Resonus when H is parallel to a face. H is in the Vacuus when H holds an edge; the plate of an edge is
unique because O is not on the edge's line. In the polar, the Resonus plane of F is at right angles to a_F, and the plate of the
edge F ∩ G is at right angles to a_F − a_G (resonus study, Theorem 1). The two planes are equal exactly when these normals are
parallel. ∎

**Proposition B1 (prisms).** For the regular n-gonal prism about its centre, the Resonus and Vacuus share n/2 planes if
n ≡ 2 (mod 4), and none otherwise.

*Proof.*
- The Resonus is the horizontal plane plus vertical planes with normals at angles (2k + 1)π/n.
- A plate through O and a base edge is tilted, because the edge does not meet the axis. So it is neither vertical nor horizontal.
- The plate of the vertical edge at angle 2πj/n is vertical, with normal at angle 2πj/n + π/2.
- The two normals agree modulo π when 2j + n/2 ≡ 2k + 1 (mod n), which is solvable exactly when n/2 is odd. Then all n/2
  vertical-edge plates qualify (opposite vertical edges share a plate). ∎ Exact: n = 6 gives 3 and n = 10 gives 5; all other
  n give 0.

The same mechanism serves any solid with a prism belt about an axis through O, since both centres of a Johnson solid lie on its
axis. Observation (exact scope):
- The pair is nonempty for 28 of the 163 solids:
  - cuboctahedron 4 and icosidodecahedron 6: the hexagon and decagon slices are parallel to the triangles and pentagons;
  - rhombic dodecahedron 6 and rhombic triacontahedron 15: Vacuus = Resonus;
  - truncated octahedron 3: the octagon slices;
  - 6- and 10-gonal prisms (B1);
  - 21 Johnson solids.
- The Johnson solids:
  - with a hexagonal or decagonal prism belt, giving 3 or 5 planes (B1): J18, J20, J21, J35, J36, J38–J43;
  - with an equator of edges in a mirror parallel to an end face (bicupolas and birotundas): J27, J28, J29, J30, J31, J34;
  - the gyrobifastigium J26;
  - the augmented hexagonal prisms J55 and J57, and the biaugmented truncated cube J67.
- The intersection is the same about both centres for every Johnson solid.
- No Platonic, snub, antiprism, bipyramid or trapezohedron shares a plane, and neither does any of J84–J90.

### (iii) Simplicial arrangements

**Theorem C1 (near pencils).** Every prism has a simplicial Resonus, and every bipyramid has a simplicial Vacuus (n ≥ 3).

*Proof.* In both cases the planes are one horizontal plane and m ≥ 2 vertical planes through the axis (prism: m = n or n/2
lateral directions; bipyramid: the equator plate and m vertical plates through the apex edges). This is a near pencil. Every
region is bounded by two consecutive vertical planes and the horizontal plane, so it is a triangle on the sphere. ∎ Exact:
n = 3–12, both families.

**Theorem C2 (planes at right angles to axis classes).**
(a) Classification. Take the 3 four-fold, 4 three-fold and 6 two-fold axes of Oh, and the 6 five-fold, 10 three-fold and 15
two-fold axes of Ih. The planes at right angles to a union of whole classes form a simplicial arrangement exactly for:
- Oh: {4} (3 planes, 8 regions), {2} (6, 24), {4,3} (7, 32), {4,2} (9, 48), {4,3,2} (13, 96). Not for {3} (4 planes, 14
  regions) or {3,2} (10, 72).
- Ih: {2} (15, 120), {5,2} (21, 240), {3,2} (25, 360), {5,3,2} (31, 480). Not for {5} (6, 32), {3} (10, 92) or {5,3} (16, 152).

(b) Resonus of the uniform solids. The Resonus of each Platonic and non-snub Archimedean solid is exactly such a union:
- {4} cube; {3} tetrahedron, octahedron, truncated tetrahedron; {4,3} CO, TC, TO; {4,3,2} RCO, TCO;
- {5} dodecahedron; {3} icosahedron; {5,3} ID, TI, TD; {5,3,2} RID, TID.

So the Resonus is simplicial exactly for the cube, CO, TC, TO, RCO, TCO, RID and TID.

(c) Vacuus. The Vacuus of every Platonic and non-snub Catalan solid, and of the CO and the ID, is also such a union:
- {2} for the tetrahedron, cube, icosahedron, dodecahedron, RD, RT, triakis tetrahedron, tetrakis hexahedron and the 4
  icosahedral non-snub Catalans;
- {4} for the octahedron, {3} for the CO, {5} for the ID;
- {4,2} for the triakis octahedron, deltoidal icositetrahedron and disdyakis dodecahedron.

*Proof.* (a) is the exact computation in `axis_classes.py`. Every region was traced, and it agrees in both icosahedral frames.
(b) and (c) are exact equalities of plane sets, solid by solid, read from the same files. Ultimately, each face of a non-snub
uniform solid is centred on a rotation axis (its face stabiliser contains the rotation of the regular face), and its normal
is that axis. ∎ The snubs and the remaining Catalans are not unions; none of them has a simplicial Resonus.

**Theorem C3 (mirror Vacuus).** Suppose every Vacuus plate of P is a mirror, and the symmetry group of P is Td, Oh or Ih. Then
the Vacuus of P is simplicial.

*Proof.*
- The Vacuus is invariant under the symmetry group, so it is a union of orbits of mirrors.
- The mirror orbits are the {2} class for Td (6 mirrors), the {4} and {2} classes for Oh (3 and 6), and the {2} class for Ih
  (15). Every union of these is simplicial by C2(a).
- The unions are reflection arrangements: A1³, A3, B3 and H3, as Coxeter (1934) showed.
∎ By Proposition 2 of the vacuus-enumeration study this covers all 11 non-snub Catalan solids, and it covers the 5 Platonic
solids (checked: every plate a mirror). Exact: all 16 are simplicial.

Observations (exact scope):
- Johnson Resonus. Simplicial only for J3, J19 and J76. Their face-normal lines are exactly those of CO (7 planes, 32 regions),
  RCO (13, 96) and RID (31, 480):
  - J3 is half of CO;
  - J19 is RCO minus a square cupola, with the octagon parallel to the removed cupola's square;
  - J76 is RID minus a pentagonal cupola, with the decagon parallel to the opposite pentagon.
  In each case every pair of parallel faces of the parent keeps a member, and the Resonus depends only on the set of face-normal
  lines.
- Johnson Vacuus. Simplicial exactly for J1, J2, J12, J13, J15, J26 and J59, about both centres.
- Prism family, besides C1. The Vacuus is simplicial for the odd trapezohedra (n = 3, 5, 7, 9, 11), the cube (n = 4 prism) and
  the octahedron (n = 3 antiprism). The Resonus is simplicial for the cube as the 3-gonal trapezohedron. For the odd
  trapezohedra no proof is given here (LEAD 3).

### (iv) Duality

**Theorem D.** Let P have O inside, with polar P\*.
(a) Resonus(P\*) = R\*(P), the planes at right angles to the corner lines of P, and Vacuus(P\*) = V\*(P), the planes at right
angles to the edge directions of P. So |Resonus(P\*)| = V − (number of antipodal corner pairs), and |Vacuus(P\*)| = the number
of edge directions of P.
(b) Vacuus(P) ∩ Resonus(P\*) consists of the plates of those edges AB for which some corner C has OC ⊥ OA and OC ⊥ OB.
(c) Resonus(P) ∩ Vacuus(P\*) consists of the Resonus planes of those faces F at right angles to which P has an edge.

*Proof.*
- (a) Apply Theorem 1 of the resonus study to P\*, using P\*\* = P. The corners of P are the face normals of P\*, and the
  edge AB of P is dual to an edge of P\* whose plate is at right angles to B − A.
- (b) The plate of AB has normal A × B, and A, B are independent because O is not on the edge line. The Resonus planes of P\*
  have normals C, the corners of P. A × B is parallel to C exactly when C ⊥ A and C ⊥ B.
- (c) The Resonus plane of F has normal n_F. The planes of Vacuus(P\*) have normals B − A, so they are equal exactly when the
  edge AB is parallel to n_F. ∎

Checked:
- (a) holds as exact plane-set equality on all 38 dual pairs: 5 Platonic with their polars, 13 Archimedean–Catalan and 20
  prism-family pairs. The counts from both rows agree. Vacuus(P) ∩ Resonus(P\*) seen from P equals Resonus(P\*) ∩ Vacuus(P\*\*)
  seen from P\*, so each pair gives two numbers.

Observations:
- In every pair at most one of the two numbers is nonzero, and the nonzero ones are:
  - Vacuus(octahedron) ∩ Resonus(cube) = 3. These are the octahedron's 3 square slices, the cube's face-parallel planes; the
    corner (0, 0, 1) is at right angles to both ends of the edge from (1, 0, 0) to (0, 1, 0). The same holds for the 3-gonal
    antiprism and trapezohedron.
  - Vacuus(P\*) ∩ Resonus(P) for P = TC (3), RCO (9), TCO (9), RID (15) and TID (15), where edges run along the axes of the
    octagons and squares.
  - For every prism (Proposition D1).
  - All other pairs give 0 and 0: the tetrahedron and the dodecahedron–icosahedron pair, the other eight Archimedean pairs,
    and every antiprism with n ≥ 4.
- Among Johnson solids (P itself only):
  - Vacuus(P) ∩ R\*(P) is nonempty for J12, J13, J55, J57 and J91;
  - Resonus(P) ∩ V\*(P) is nonempty for 49 of the 92.

**Proposition D1 (prisms).** For the n-gonal prism, |Resonus(P) ∩ Vacuus(P\*)| = n/2 + 1 if 4 | n, and 1 otherwise.

*Proof.*
- The lateral edges are at right angles to the bases, which gives the horizontal plane.
- A lateral face's normal (angle (2j + 1)π/n) is parallel to a base edge (angle (2k + 1)π/n + π/2) exactly when
  π/2 ≡ 2(j − k)π/n (mod π), that is, when 4 | n. Then all n/2 lateral planes qualify. ∎ Exact: n = 4, 8, 12 give 3, 5, 7;
  all other n give 1.

## 5. Johnson solids: the two centres

- The corner centroid and the volume centroid coincide for 40 of the 92: the 37 found exact earlier, and J84, J85, J90, whose
  symmetry fixes a single point.
- Moving the centre changes none of the Vacuus counts in any of the 92: kind, plates, sheets, mirrors, the intersection with
  the Resonus, and the polar intersections.
- The Resonus is the same plane set about both centres (Theorem A(a)).
- Only the arrangement of the Vacuus planes on the sphere changes:
  - In J66 the counts change: 1554/3328/1776 about the corner centroid, against 1586/3376/1792 about the volume centroid.
  - In 23 others (J20, J23, J24, J25, J32, J33, J40, J41, J47, J60, J68, J70, J71, J76–J79, J81–J83, J87–J89) the counts
    are equal, but the crossing points or region shapes differ.
- Exact Johnson kinds (all 92, corner centroid): heart 13, inherited heart 50, non-heart 29.

## 6. The table

`data/vacuus-resonus-catalogue.md` and `.csv`: 163 rows, in the order Platonic (D, I, C, T, O), Archimedean, Catalan, prism
family, Johnson. Columns:
- V, E, F, centrally symmetric, mirrors;
- Vacuus: plates (full + shared + single), kind, plates on mirrors, sphere V/E/regions, simplicial;
- Resonus: planes (carrying 2 faces + 1 face), planes on mirrors, sphere V/E/regions, simplicial;
- R∩V (of which mirrors); Vacuus(P) ∩ Resonus(P\*); Resonus(P) ∩ Vacuus(P\*);
- for Johnson solids, what changes about the volume centroid.

Full per-plate data (slices, classes, point multiplicities, region side counts) are in `data/catalogue-all.json`.

## Sources checked

Studies 2026-11-24-vacuus-enumeration (Lemma 1, Proposition 2, Tables 1–3, the floating-point Johnson pilot) and
2026-11-24-resonus (Theorem 1, the H3 control). Methods credited at point of use:
- Minkowski's uniqueness theorem (1897);
- Cauchy's rigidity theorem (1813);
- Coxeter, "Discrete groups generated by reflections" (Ann. Math. 35, 1934) for simplicial reflection arrangements;
- Zaslavsky (1975) and Grünbaum (2009) for counting regions of arrangements;
- PARI/GP (`algdep`, `lindep`, `polcompositum`, `polredbest`);
- python-flint / Arb (F. Johansson) for certified roots and ball arithmetic;
- sympy and mpmath.

Not opened here: published exact coordinates of J84–J90 (e.g. A. V. Timofeenko's papers on the non-composite polyhedra); see
LEAD 1.

## LEADS

1. Compare the minimal polynomials of J84–J90 with the published ones (Timofeenko; standard references). J86's 60x⁴ − 48x³ −
   100x² + 56x + 23 appears among our coordinates.
2. Theorem B: a structural description of the Johnson cases without a prism belt (J26, J27, J29–J31, J34, J55, J57, J67).
3. Prove that the odd trapezohedra have a simplicial Vacuus (n = 3, …, 11 exact). The planes are n vertical mirrors plus n
   planes at right angles to the lateral edge directions of the antiprism.
4. Theorem C2 for the snubs. Their Resonus is not a union of axis classes (the snub triangles), and none is simplicial. Is
   every Resonus with a face in general position non-simplicial?
5. J66: why its Vacuus arrangement alone changes its counts between the two centres.
6. 4D: the same catalogue for the uniform 4-polytopes. The Resonus of the A4 permutahedron (370 regions) is the control.

## Files

- `scripts/j84_90_exact.py`: stage 1.
- `scripts/merge_stage1.py`.
- `scripts/catalogue.py`: stage 2, reusing `../2026-11-24-vacuus-enumeration/scripts`.
- `scripts/merge_rows.py`: puts the J84–J90 rerun into the catalogue.
- `scripts/axis_classes.py`, `scripts/make_table.py`, `scripts/patterns.py`.
- `data/j84_90_exact.json`: defining polynomial, root to 200 digits, and exact coordinates.
- `data/catalogue-all.json`, `data/axis-classes.json`, `data/patterns.txt`.
- `data/vacuus-resonus-catalogue.{md,csv}`.
- `logs/`.
