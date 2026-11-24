# Plate harmony: how the central plates of the Vacuus, the Resonus and other frames can relate (25 November 2026)

DICTO · dictospheres.com · study 2026-11-25-plate-harmony · with Claude (Anthropic).

> **Status box.** Study note, not published. Checks: extract_catalogue.py FINAL ok (logs/extract.log); run_catalogue.py FINAL ok
> (428 arrangements, regions and simplicial flag equal to the catalogue study's in every row); stellation_roots.py FINAL ok
> (controls: H3's 120 regions traced, each π/30; Sunstar 69 plates, 92 corners, 150 edges as in the stellation study);
> four_d.py FINAL ok (control: H4 has exponents 1, 11, 19, 29, 14 400 chambers, simplicial, reflection); yantra.py FINAL ok
> (both yantras certified by the Krawczyk test); make_tables.py FINAL ok. Nothing running. The full tables are `data/tables.md`.

**DICTO's question.** In what other ways can the plates (the central planes) of a Vacuus, a Resonus or another frame relate
harmoniously? Each arrangement of central planes is tested for six properties: (3) equiangular; (4) the planes split into mutually
perpendicular triples; (5) equal emptiness, meaning all regions on the sphere have equal area; (6) every angle between planes is a
rational multiple of π; (7) the characteristic polynomial factors over Z, and freeness; (9) regular pencils, meaning the k planes
through every line are spaced π/k. The study also records whether each arrangement is simplicial and whether it is a reflection
arrangement. Added at DICTO's request (25 Nov): the **Sphericus** crossing measures, and the Tacitus silence of the crossing points.

## Verdict

1. **Theorem 1 (regular pencils are reflections).** A central plane arrangement in R³ has every pencil regular, (9), exactly when it
   is a reflection arrangement. In all 428 catalogue arrangements, and in every other family here, (9) and "reflection" agree.
2. **Theorem 2 (what a reflection arrangement gives).** A reflection arrangement has (5), (6), (9), is simplicial, and is free
   (so (7) holds). In the catalogue, equal area (5) holds **only** for the 57 reflection arrangements. This is an observation, not a
   theorem. The 5-gonal trapezohedron's Vacuus (10 planes) shows why the cheap tests are not enough. All its angles are rational and
   it passes the lune test, yet its 60 regions have three exact areas: π/30, π/15 and π/10, twenty of each.
3. **The most harmonious arrangement is the 3 coordinate planes**, the Resonus of the cube and the Vacuus of the octahedron. It has
   all six properties (score 6/6). It is the only arrangement whose crossings are harmonious: every point has 2 circles, every
   angle is π/2 and every arc is π/2. Next come H3 (15 mirror planes: the Vacuus of every icosahedral Platonic and Catalan
   polyhedron, of the four Kepler–Poinsot stars and of the Dogstar) and B3 (9 planes). Each has 5/6, missing only (3). In 4D, H4
   (60 mirrors) also has 5/6.
4. **The H4 Coxeter plane (Coxeter).** None of the walls of the 4D Queens has a 30-fold pencil. The largest pencil is 5 for H4 and
   6 for the 600-cell's 300 Resonus walls. But the 60 mirrors of H4 cut the Coxeter plane in exactly **30 lines, two mirrors per
   line, forming a regular 30-line pencil**, decided exactly. The 300 walls cut it in 210 lines that are not regular.
5. **The hub (31 planes) is free but not harmonious.** It is simplicial (480 triangles) with χ = (t − 1)(t − 11)(t − 19), and it is
   **free with exponents 1, 11, 19** by Yoshinaga's criterion, computed exactly. It is not a reflection arrangement, and its angles
   are not all rational. The same arrangement is the Resonus of the rhombicosidodecahedron, the truncated icosidodecahedron and J76.
6. **The yantras score 0.** As plane arrangements (cap 60°), both spherical yantras fail all six properties. For the "no" answers
   the certificates are exact or certified within the boxes. χ = (t − 1)(t² − 26t + 266) does not factor, so neither yantra is free
   (Terao). Theorem 3 proves the angle 2 arctan(2u) between the great triangle t7's leg planes is not a rational multiple of π.
7. **Root forms.** The Resonus of every root form lies inside the 31 hub planes: CLEO 4/4, AXE 4/4, FUJI 7/7, Cleo-Icos 4/4 and
   Antonius 4/4 (exact). Their Vacuus about their own centroid leaves the hub: CLEO 3/6, AXE 2/6, FUJI 0/12, Cleo-Icos 3/6 and
   Antonius 0/3. Placed on the φ-ladder, with their dodecahedron as D0:
   - CLEO's corners are one corner of D0 and three of I₋₂.
   - Cleo-Icos is O and a face of I0.
   - AXE has two corners of D0 and two corners on no station.
   - FUJI has one corner of D0.
   - Antonius has three corners of I0 (a, b, c); its other three (a + b, …) lie on no station.
8. **Tacitus of the crossings.** Weighted by the number of circles through each point, the crossing points of every prism Resonus
   and every bipyramid Vacuus with n ≠ 4, and of J12 and J13, are silent in degree 2 beyond their symmetry (exact). The cause is a
   balance: the axis point carries weight n, and that equals the total weight on the equator. No other arrangement checked is silent
   beyond symmetry, but 91 large catalogue arrangements were not run (size cap of 1 000 points).

## Definitions (no new ones)

- **Vacuus** (#110 §2): one plane through the centre O and each edge. **Resonus** (DICTO, 24 Nov): one plane through O parallel
  to each face, with parallel faces sharing one plane. The centres are those of study 2026-11-24-vacuus-resonus-catalogue; Johnson
  polyhedra use both the corner centroid and the volume centroid.
- **Sphericus** is DICTO's name (25 Nov 2026) for the spherical view of a plate set: the network of great circles, one per central
  plate, plus small circles where the construction has them, and how they cross. **Its exact definition will be fixed with DICTO.**
  The working measures used here are:
  - (a) the crossing points and the number of circles through each;
  - (b) the crossing angles at each point (the gaps between neighbouring circles);
  - (c) the arcs between consecutive crossings along each circle;
  - (d) the side counts and areas of the regions.

  "Harmonious crossing" means (a)–(c) each take one value.
- **Tacitus** (study 2026-11-25-tacitus): the set is silent in degree k when every degree-k spherical harmonic averages to zero on
  it. "Beyond symmetry" means silent although the symmetry group of the set has an invariant harmonic of degree k.

## Theorems and proofs

**Theorem 1.** For a central arrangement A of planes in R³ (rank 3), every pencil of A is regular if and only if A is the mirror
arrangement of a finite reflection group.

*Proof.* (⇐) In a finite reflection group W, the planes through a line ℓ are the mirrors of the stabiliser of ℓ, a dihedral
reflection group I₂(k). Its k mirrors are spaced π/k (classical; Coxeter, *Regular Polytopes*).
(⇒) Let every pencil be regular. At a point where k circles meet, every corner angle of a region is π/k ≤ π/2. A spherical
polygon with n sides has angle sum greater than (n − 2)π. With every angle at most π/2 this forces n = 3, so every region C is a
triangle with angles π/p, π/q, π/r. Let C′ share the side e with C, along the plane H. At both ends of e the pencil is regular, so
C′ has the same angles there as C, and it shares the side e. By ASA congruence of spherical triangles, C′ = s_H(C), where s_H is
the reflection in H. The regions are connected through shared sides, so each region is the image of C under a word in the
reflections. The tiling therefore coincides with the Coxeter tiling of the group W generated by the reflections in C's three sides,
and W is finite because the triangle is spherical. The union of the region edges is the union of the mirrors of W, so A is the
mirror arrangement of W. ∎

**Theorem 2.** A reflection arrangement in R³ is simplicial and free, has every angle a rational multiple of π, has all regions of
equal area, and has regular pencils.
*Proof.*
- The regions are the chambers of W. W acts on them simply transitively, so they are congruent triangles with angles π/m (Coxeter).
- Every angle between two mirrors is a rational multiple of π, because the product of the two reflections has finite order.
- Freeness is Saito's and Terao's theorem.
- Regular pencils follow from Theorem 1. ∎

Every reflection arrangement in the data confirms this: the 57 in the catalogue, the 15 mirror planes and the stella frame
(the Vacuus of the stella-octangula yantra frame is A3, 6 planes).

**Theorem 3 (the yantras' angles).** At cap 60° the leg planes of the great triangle t7 meet at θ with
cos θ = (1 − 4u²)/(1 + 4u²), that is θ = 2 arctan(2u). For both the DICTO Yantra and Kulaichev's yantra, θ/π is irrational.
*Proof.*
1. The apex of t7 is the top of the circle, its corners lie at depth R = 1/(1 + u²) with half-width u/(1 + u²), and the gnomonic
   scale is s² = 12. The cross products give the formula; the script checks it against the computed normals.
2. Write c = 2cos 2θ. Then c ∈ Q(u²).
3. u is a root of an even integer polynomial: degree 160 for the DICTO Yantra (sri-yantra study) and degree 348, f348, for
   Kulaichev's (2026-11-15-yantra-uniqueness). So [Q(c):Q] ≤ 80 or 174.
4. If θ = (k/n)π with gcd(k, n) = 1, then c = 2cos(2πk/n) has degree φ(n)/2 (Niven; Conway–Jones). Hence φ(n) ≤ 160 or 348,
   which forces n ≤ 204 813 or n ≤ 968 845.
5. For every such n, the Arb ball of nθ/π, taken from the Krawczyk box of radius 10⁻¹⁰⁰, contains no integer. ∎

**Proposition 4 (the H4 Coxeter plane).** Let W(H4) act on R⁴ with its 60 mirrors, let c = s₁s₂s₃s₄ be a Coxeter element, and let
P be its Coxeter plane (the real plane on which c rotates by 2π/30). Then the mirrors cut P in exactly 30 lines, each the trace of
exactly two mirrors, spaced π/30.
*Proof (exact computation).*
- The simple roots are found exactly as the positive roots whose reflection permutes the other positive roots.
- P is the kernel of c² − 2cos(2π/30)·c + 1 over K = Q(2cos(2π/30)), a field of degree 4 that contains √5 = 2·(2cos(2π/5)) + 1.
- The traces are deduplicated exactly in K.
- Regularity: for every pair of traces at angle α, C₃₀(2cos 2α) = 2 holds in K. This is the Chebyshev identity cos(60α) = 1. ∎

The classical form of this is Coxeter's: the Petrie polygon of the 600-cell is a 30-gon, and the H4 roots project onto the Coxeter
plane in rings of 30. Here the statement is about the mirrors' traces, checked exactly.

## Method

Every equality is decided exactly in a number field Q[x]/(g) (python-flint fmpq_poly) with a certified real root (Arb ball plus an
exact sign change). Balls are used only for orders and for choosing roots.
- **Arrangement counts.** The intersection lines are grouped by exact keys.
- **χ.** χ(t) = (t − 1)(t² − (n − 1)t + b₃) with b₂ = Σ(m_X − 1), from the Möbius function (Orlik–Solomon). The number of regions
  is |χ(−1)| (Zaslavsky). In 4D the full lattice is used: 2-flats from Plücker keys, lines from the 2-flats cut by every other
  hyperplane, all in Z[φ].
- **(6) Rational angles.** Take the minimal polynomial of 2cos 2θ (the characteristic polynomial of multiplication, factored over Z
  by FLINT) and compare it with FLINT's cos_minpoly(n) (Niven; Conway and Jones 1976).
- **(9) Regular pencils.** C_k(2cos 2θ) = 2 for every pair in a k-pencil, exact (Chebyshev).
- **(5) Equal area.** First the lune test, which is exact. Two planes that are neighbours in a pencil bound a lune of area 2α made
  of whole regions, so αR/2π must be an integer. It fails exactly when α/π is irrational. If the lune test passes, a reflection
  arrangement settles it. Otherwise every region is traced and its exact area computed (all corner angles rational).
- **(4) Perpendicular triples.** An exhaustive exact search, capped at 2·10⁶ nodes. It reached the cap only for the 300 4D walls,
  where (4) is left open.
- **(7) Freeness.**
  - If χ does not factor, the arrangement is not free (Terao's factorisation theorem).
  - A reflection arrangement is free (Saito; Terao).
  - A supersolvable arrangement is free (Stanley; Jambu–Terao); the test is a modular line.
  - Otherwise Yoshinaga's criterion (2005) decides it: the arrangement is free exactly when χ factors with the exponents of the
    Ziegler multirestriction to one plane, found by exact linear algebra in the field.

  The multirestriction code was checked on H3 (exponents 5, 9) and B3 (exponents 3, 5).
- **Sphericus.**
  - Crossing points and multiplicities come from the lattice.
  - Angular orders on each circle and at each point are exact (sign of determinants).
  - Arcs are compared by the sign of p·q and the exact (p·q)²/(|p|²|q|²).
  - Crossing angles are compared by the exact cos² class of the two planes and the sign of the cosine.
  - Region areas are exact when every corner angle is rational. Otherwise the table counts the values certified apart, which is a
    lower bound on the number of areas.
- **Tacitus.** This step reuses tacitus.py of study 2026-11-25-tacitus: its energies, its numerical symmetry group and its character
  dimensions.
  - The crossing points include both antipodes, so every odd degree is silent. Even degrees k ≤ 20 are screened in floating point.
  - A silence that the symmetry group does not force is then decided exactly in the field. For even k, P_k(t) is a polynomial in
    t² = (p·q)²/(|p|²|q|²), and t² lies in the field.
  - Two float near-misses were found to be exactly nonzero: the 6-gonal trapezohedron's Resonus and the 8-gonal trapezohedron's
    Vacuus.
  - Sets with more than 1 000 points are not run; there are 91 of them, listed in the data.
  - The symmetry group is found numerically, as in the Tacitus study.
- **Yantras (box data).** Both are rebuilt from the uniqueness studies' systems with #103's construction. construct() and the
  Krawczyk test are copied line for line from the sri-yantra study's breakers_certify.py. Every quantity is an Arb ball in a box
  of radius 10⁻¹⁰⁰.
  - Inequalities are decided by the balls; equalities are seen only as "inside the box".
  - The 32 multiple points found inside the boxes are exactly the defining incidences of a yantra: 18 marmas, 7 apexes on bases and
    6 corner touches (31 triple points), plus the 9 bases meeting at infinity. So they hold exactly, and χ is exact.
  - The ring (the yantra's circle, a small circle of radius 60°) is included in Sphericus. In each yantra it meets the 27 great
    circles in 44 points, 10 of them crossed by two great circles (the corners on the circle).
  - The metric results (3)–(6) and (9) are for cap 60°, as in spherical.py. The incidence results (χ, freeness, simplicial,
    multiplicities) hold for every cap, by projective invariance.
- **Root forms.** CLEO, AXE and FUJI are taken from study 2026-10-14-axe-cleo-fuji (inputs/), identified exactly as (a + bφ)/2 and
  scaled into the stellation frame (their dodecahedron becomes D0; checked). Cleo-Icos is O plus a face of I0. Antonius is the
  middle of the golden rhombohedron spanned by that face's corners. Its shape was checked against the app's floats.
  - Hulls are exact.
  - Hub membership is tested as a direction.
  - The ladder is tested exactly against φᵏI0 and φᵏD0 for −8 ≤ k ≤ 8.
- **Runs.** All runs were on the compute machine through the job runner, under nice: scripts/, logs/, data/.

## Tables (summary; full tables in data/tables.md)

| family | arrangements | reflection | (3) | (4) | (5) | (6) | (7) factors / free | (9) | harmonious crossing | Tacitus beyond |
|---|---|---|---|---|---|---|---|---|---|---|
| catalogue (163 polyhedra, Vacuus and Resonus, Johnson at 2 centres) | 428 | 57 | 20 | 25 | 57 | 59 | 85 / 85 | 57 | 8 (all the 3 coordinate planes) | 22 (weighted, degree 2) |
| stellation cycle: M15, R6, R10, H31, S69 | 5 | M15 | R6 | M15 | M15 | M15 | M15, H31 / both free | M15 | none | none |
| root forms (Vacuus at 1 or 2 centres, Resonus) | 11 | 0 | 0 | 0 | 0 | 0 | 4 / 4 (Vacuus of CLEO, AXE, Cleo-Icos: A3 combinatorics; Antonius: 3 planes in general position) | 0 | none | none |
| 4D Queens: H4, the 300 | 2 | H4 | 0 | H4 (300 open) | H4 | H4 | H4 / H4 | H4 | (not defined in 4D here) | (not run) |
| spherical yantras, stella frame | 3 | stella | 0 | 0 | stella | stella | stella / stella | stella | none | none |

Score distribution over the 428 catalogue arrangements: 6/6 for 8 (all the 3 coordinate planes), 5/6 for 15 (H3 and B3),
4/6 for 34, 2/6 for 1, 1/6 for 42 and 0/6 for 328.

The free arrangements that are not reflection arrangements (observation; all decided exactly):
- the Resonus of CO, TC and TO (7 planes, exponents 1, 3, 3);
- the Resonus of RCO and TCO (13 planes, exponents 1, 5, 7);
- the Resonus of RID, TID and J76 (the hub, 31 planes, exponents 1, 11, 19).

These Resonus arrangements are simplicial, so they belong to Grünbaum's catalogue of simplicial arrangements. Matching them to its
labels is LEAD 1. Further free non-reflection arrangements:
- the Vacuus of the n-gonal trapezohedra for odd n (supersolvable, exponents 1, n − 1, n);
- 13 Johnson cases (data).

Equiangular sets have at most 6 planes (Haantjes; Lemmens–Seidel). The catalogue has 3 (orthogonal), 4 (the tetrahedral axes), 5
(the 5-gonal trapezohedron's Resonus) and 6 (the five-fold axes).

## Which arrangements are most harmonious

Ranked by how many of (3), (4), (5), (6), (7) and (9) hold:
1. **6/6: the 3 coordinate planes.** These are the Resonus of the cube and the Vacuus of the octahedron, the 3-gonal antiprism and
   the 4-gonal bipyramid. They are also the only harmonious Sphericus.
2. **5/6: H3, the 15 mirror planes; B3, 9 planes; H4 in 4D.** Each misses only equiangularity.
   - H3 is the Vacuus of the icosahedron, the dodecahedron, the icosahedral Catalans, the Kepler–Poinsot stars, the Dogstar and J59,
     and the Resonus of the rhombic triacontahedron.
   - B3 is the Vacuus of the octahedral Catalans and the deltoidal icositetrahedron.
   - H4 is the Vacuus of the 600-cell and the Resonus and Vacuus of the 120-cell. Its mirrors meet the Coxeter plane in the regular
     30-line pencil.
3. **4/6: the other reflection arrangements:** A3 (6 planes; the Vacuus of the cube, tetrahedron and rhombic dodecahedron, and the
   stella frame), A1 × I₂(m) and I₂(m).
4. **Free but not regular:** the 7-, 13- and 31-plane Resonus arrangements, including the hub. Only (7) holds; they are simplicial
   and free.
5. **0/6:** both spherical yantras, the Sunstar's 69, R6, R10, and the 600-cell's 300 walls (χ does not factor, so not free).

## Observations (labelled as such)

- (5) ⇒ reflection holds in every arrangement tested. Whether it holds for all central arrangements in R³ is open (LEAD 2).
- The Vacuus of CLEO, AXE and Cleo-Icos about the centroid has the combinatorics of A3 (6 planes, exponents 1, 2, 3; CLEO, AXE, Cleo-Icos)
  without being a reflection arrangement.

## Sources (classical results credited; free routes)

Cited from standard knowledge and the earlier studies. No web search was run in this study (LEAD 3: open each free copy and check
the citations).
- H. Terao, free arrangements and the factorisation theorem (Invent. Math. 63, 1981).
- K. Saito (1980) on free divisors.
- T. Zaslavsky, *Facing up to arrangements* (Mem. AMS 154, 1975).
- P. Orlik and H. Terao, *Arrangements of Hyperplanes* (1992).
- M. Yoshinaga, "On the freeness of 3-arrangements" (Bull. LMS 37, 2005).
- G. Ziegler, multiarrangements (1989).
- R. Stanley (1972) and M. Jambu and H. Terao (1984) on supersolvable arrangements.
- B. Grünbaum, "A catalogue of simplicial arrangements in the real projective plane" (Ars Math. Contemp. 2, 2009; open access).
- M. Cuntz, simplicial arrangements and freeness (arXiv).
- H. S. M. Coxeter, *Regular Polytopes*, and "The product of the generators of a finite group generated by reflections" (Duke
  Math. J. 18, 1951): the Coxeter plane and h = 30.
- I. Niven (1956); J. H. Conway and A. J. Jones (Acta Arith. 30, 1976).
- J. Haantjes (1948); P. Lemmens and J. J. Seidel (1973) on equiangular lines.
- Delsarte, Goethals and Seidel (1977), via the Tacitus study.
- Mosseri and Sadoc (1982) for the tiles t4 and t6 (CLEO and AXE). Mackay (1962) for the icosahedron's face pyramid.
- Studies reused: 2026-11-24-vacuus-resonus-catalogue, 2026-11-25-stellation-cycle, 2026-11-24-resonus-4d,
  2026-11-08-tetra-yantra, 2026-11-08-sri-yantra, 2026-11-15-yantra-uniqueness, 2026-11-15-dicto-yantra-uniqueness,
  2026-10-14-axe-cleo-fuji, 2026-11-25-tacitus; papers/names-audit.md.

## LEADS

1. Match the free non-reflection Resonus arrangements (7, 13, 31 planes) to Grünbaum's labels, and check Cuntz's published
   exponents.
2. Prove or refute that equal area (5) implies a reflection arrangement in R³.
3. Open the free copies of the sources above and confirm the citations.
4. The 600-cell's 300 walls: the perpendicular-triple search hit its cap, so (4) is open. The Sphericus and Tacitus measures of the
   4D arrangements (on S³) are not defined here yet.
5. Run the 91 large catalogue arrangements through the Tacitus test of their crossings, with a group taken from the planes.
6. The yantras at other caps: the metric properties depend on the cap ρ. Is there a ρ at which a yantra angle becomes rational?
7. Sphericus: fix the exact definition with DICTO, including small circles and weights.
