# Platonic book: three floating-point results made exact (13 Nov 2026)

**Conclusion (13 Nov 2026): the crossed-nest cores and all six octet thresholds hold exactly (√5/2, 3/2, φ, 1 + √5/2, φ², 3), but the
neighbouring faces at 1 + √5/2, φ² and 3 meet corner to corner or corner on edge, never edge to edge. Dogstar has NO central disc under
the #87 definition: its 15 planes carry 114 of its 138 edges, but each plane holds two open fans, not a closed disc. No face of the
Dogstar lies on a plane through its centre (the draft says one).**

Asked for by the Platonic book draft (papers/book-platonic: Ch 1 §1.3, Ch 4 Dogstar paragraph, Ch 10 octet paragraph), which marks
these results "floating point". This study does not edit the book. It gives the values the book can cite.

Script `scripts/platonic_exact.py` (log `data/platonic-exact.log`, `data/platonic-exact.json`; pilot `data/pilot.log`,
`data/platonic-exact-pilot.json`). It ran on the compute machine through the job gate (jobs platexact-pilot, platexact): 59 checks,
0 failed, 9 s, FINAL ok. All arithmetic is exact in Q(√5), using the field class of the #87 study
(studies/2026-11-02-dicto-vacuus/scripts/qf.py, executed from its file and not retyped; the script adds only an exact |x|). Floats
appear in only two places: the 6-digit readings printed next to the exact values, and the #87 float apex-angle sum, which is run next
to the exact disc test as a cross-check.

## Float vs exact

| # | claim in the draft (float) | exact result | same? |
|---|---|---|---|
| A0 | stella octangula: 2 tetrahedra on the cube, core = octahedron | regular octahedron | yes |
| A1 | dodecahedron's 20 corners: 5 crossed cubes, core = rhombic triacontahedron | exactly 5 cubes (each is T ∪ −T of two of the 10 tetrahedra, and every inscribed cube has this form); the core has 32 corners on 2 spheres and 60 equal edges, and its faces are 30 congruent rhombi with diagonal² ratio (3 + √5)/2 = φ² | yes |
| A1 | 10 crossed tetrahedra: core = icosahedron of edge 1/φ × the dodecahedron's | regular icosahedron, edge² ratio (3 − √5)/2 = 1/φ², so edge ratio exactly 1/φ; its corners lie on the dodecahedron's face axes (the dual position) | yes |
| A1 | either chiral set of five: the same icosahedron | exactly 2 fives use all 20 corners; both have the same core as the ten | yes |
| A2 | icosahedron's 30 edge midpoints: 5 crossed octahedra, core = icosahedron of edge 1/φ, same orientation | exactly 5 octahedra; core = λ × the icosahedron itself with λ = (√5 − 1)/2 = 1/φ exactly (same orientation): the golden loop shrinks by 1/φ each turn | yes |
| B1 | grown icosahedra first touch at s = 1.118034 = √5/2 | s = √5/2 exactly; the 12 neighbours of shell (1,1,0) touch face to face on a golden face (normal (φ, 1/φ, 0) up to sign), with a 4-cornered overlap | yes |
| B2 | tetrahedral-hole centres reached at s = 3/2 | s = 3/2 exactly; both kinds of hole; 4 cells reach the centre at once (the 4 octahedra that share a face with the hole), each with the centre of a layer face (the 3-fold axis passes through the hole centre) | yes |
| B3 | icosahedra cover all of space at s = φ; the octet's corners are covered last | s = φ exactly; proof below; the octet corners are the ONLY last points | yes |
| B4 | the 8 layer-plane faces: coplanar faces meet "edge to edge" at s = 1 + √5/2 | s = 1 + √5/2 exactly (6 coplanar neighbours meet at once). The contact is a **corner on an edge**: a corner of one face touches the neighbour's edge at (3 − √5)/2 = 1/φ² of its length from the nearer end (a golden point) | value yes; "edge to edge" no |
| B5 | the 12 golden faces meet at s = φ² | s = (3 + √5)/2 = φ² exactly (2 coplanar neighbours); the contact is **corner to corner** | value yes; "edge to edge" no |
| B6 | grown dodecahedra touch at s = 3/2 | s = 3/2 exactly; 12 neighbours touch face to face with a 4-cornered overlap | yes |
| B7 | the dodecahedra's coplanar faces meet at s = 3 | s = 3 exactly (2 coplanar neighbours); the contact is **corner to corner** | value yes; "edge to edge" no |
| C1 | Dogstar: 138 edges on 27 central planes; 12 planes carry 8 edges, 3 carry 6, 12 carry 2 | exact, the same; no edge passes through O | yes |
| C1 | "only one of its 84 faces lies on a plane through the centre" | **0** central faces (60 triangles and 24 quadrilaterals, none on a central plane; the orbit study's own census JSON also has 0, so the README sentence was a transcription slip) | **no** |
| C2 | 114 of 138 edges lie on fifteen central discs (83 %) | 114 of 138 = 19/23 = 82.6 % lie on the 15 central planes carrying ≥ 3 edges (the 11-11 census rule). Under the **#87 definition** (a central disc is a closed flat sheet of fins whose apex angles sum to 2π) the Dogstar has **0 central discs**: every one of the 15 planes carries two opposite **open fans** | **no** under #87 |
| C3 | the 15 planes are the 15 mirror planes of the icosahedral group: 3 coordinate and 12 golden; only the 3 coordinate planes are Dogstar's own mirrors | exact: they are the 15 mirrors of the icosahedral group of the six neighbouring dodecahedra; the 3 coordinate planes carry 6 edges each and the 12 golden planes carry 8 each; exactly the 3 coordinate planes are mirrors of the Dogstar | yes |

## A. Crossed-nest cores (method)
Corners are exact in Q(√5): the cube (±1, ±1, ±1), the dodecahedron (cube ∪ cyclic(0, ±1/φ, ±φ)) and the icosahedron
cyclic(0, ±1, ±φ). The members are found by exact distance tests: regular tetrahedra as 4-sets with six equal distances, cubes as
T ∪ −T, and octahedra as three mutually orthogonal antipodal pairs. The core is the intersection of the members' face half-spaces: every
triple of planes is solved by Cramer's rule, and a point is kept only if it satisfies every half-space. The core is then identified
exactly by its corners, its face sizes, its single edge length and its radii. The search is complete: every regular tetrahedron on a set
of points on a sphere is centred at the sphere's centre, and every inscribed cube is T ∪ −T.

## B. Octet thresholds (method and proofs)
**Scale.** Cube side 2, so the octet edge is √2 (s is scale-free). The sites (octahedral holes) form the fcc lattice L = {integer
vectors with even sum}. Each site holds the octahedron |x|₁ ≤ 1, Pacioli's icosahedron I = cyclic(0, ±1/φ², ±1/φ) (its corners divide
the octahedron's edges in the golden ratio), and the nest's dodecahedron D (the face centres of I). The octet's corners lie at L + e₁ and
the tetrahedral holes at L ± (½, ½, ½). The gauge ‖v‖_K = max over facets N·v (each facet written N·x ≤ 1) is exact.
**Kinds of event, and why there are no others in 0 < s ≤ 3.** Each threshold is a minimum over ALL cells. A norm bound makes the list
finite: ‖v‖_K ≥ |v|/R, where R is the circumradius of K. Any offset that could give a value ≤ 3 is therefore listed, and every value of
each kind in the range is printed:
- *touch* (sK and sK + v meet iff s ≥ ‖v‖_K / 2, since K is centrally symmetric; 176 offsets in the bound). Icosahedra:
  √5/2 (12, shell (1,1,0)), φ (6, (2,0,0)), 2 (24), √5 (12), 3φ/2 (12), ½ + √5 (12), 3 (32). Dodecahedra: 3/2 (12), 3/φ (6),
  3φ/2 (24), 9/(2φ) (12), 3 (20). The first values are the draft's. The later values are contacts with farther cells inside the
  overlap. One coincidence: icosahedra meet their (2,0,0) neighbours exactly at s = φ, at the octet corner between them, which is the
  full-cover threshold.
- *hole centres reached*: only 3/2.
- *full cover*: only φ.
- *coplanar faces meet* (sF and sF + v in one plane meet iff s ≥ ‖v‖ in the gauge of F − F, computed exactly in the plane): each
  family has exactly one value ≤ 3, namely 1 + √5/2 (layer faces), φ² (golden faces) and 3 (dodecahedra). Every one of the 20 + 12
  faces belongs to a family that has coplanar neighbours.
- Contact type: two coplanar translates of a triangle or a pentagon can never share a segment, because neither shape has a pair of
  parallel opposite edges. So "edge to edge" is impossible for these faces. The exact contacts are given in the table above.
**Cover proof at s = φ.** (i) The six octahedron corners have gauge exactly φ, so O ⊂ φI and every octahedron is covered. (ii) Split
each tetrahedral hole into 4 cones from its centre t, one over each face. The cone over a face lies in φI + c, where c is the site
across that face, because its 4 corners do: the face corners have gauge φ and t has gauge 3/2. The octet is octahedra plus tetrahedra
of the two kinds, and the second kind is the point reflection of the first. So φI + L covers space. (iii) The octet corner e₁ has gauge
≥ φ from every site (equality for exactly its 6 neighbouring sites, all sites within the bound checked). So below φ the corners are
uncovered. (iv) The gauge from c is convex. Inside O_c it reaches φ only at points on a facet of φI that holds all the corners of their
carrier face. No two adjacent corners of O share a facet of φI (checked), so only the 6 corners reach φ. Inside a cone the gauge is
< φ, except on its base face, which (iv) has already covered. So the octet corners are the only last points.

## C. Dogstar's discs (method)
Corners: the registry floats (data/dogstar_vacuus.json of studies/2026-11-11-orbit-polytopes), each recognised uniquely as
(a + b√5)/4 with a residual below 1e-9. From then on everything is exact: the 56 corners and 84 faces, each face planar, a closed
oriented surface (each of the 138 edges lies in 2 faces, in opposite directions; V − E + F = 2), and volume exactly φ/2. This volume is
2φ³ − (15 + 7√5)/4: a cube of edge φ minus the six roofs of the neighbouring dodecahedra of edge 1, which identifies the solid. As a
further check, every face lies on a face plane of that cube or of one of the six dodecahedra. Every face cone from O has positive volume,
so the #87 Vacuus is well defined (#87 Theorem 1). Exactly 24 signed permutations keep the solid, the pyritohedral group.
Two definitions are run side by side:
- **11-11 census rule** (vacuus_census.py): a central plane that carries ≥ 3 edges. This gives 15 planes and 114 edges, as in the draft.
- **#87 rule** (vacuus.py): fins O–A–B join into a flat sheet across a shared corner ray when they are coplanar and lie on opposite
  sides of the ray. A central disc is a sheet whose apex angles sum to 2π. Here this is decided exactly: the sheet is one closed cycle
  of corners that winds once round O. The float apex sum agrees on all 54 sheets. The Dogstar has 54 sheets and **0 discs**.
  - On each of the 12 golden planes the 8 edges form two opposite fans of 4 fins. Each fan opens by arccos(−√5/3) = 138.19°, so
    together they sweep 276.38° of the 360°.
  - On each of the 3 coordinate planes the 6 edges form two fans of 3 fins. Each opens by arccos(−1/√5) = 116.57°, sweeping 233.13° in
    all.
  - In the two gaps of each plane, the plane passes through faces, not along edges.
  - The exact opening equals the sum of the fin angles on all 30 fans.

So the Dogstar's Vacuus is concentrated on the 15 icosahedral mirror planes, but as 30 open fans and not as discs. Under the #87 meaning,
the draft's phrase "fifteen central discs" (and "83 % of its edges on discs") should read "fifteen central planes carrying two fans
each".

## Controls (all ok)
POSITIVE: the octahedron has 3 square discs (4 fins each) under both definitions; the cuboctahedron 4 × 6; the icosidodecahedron 6 × 10
(as in #87); the stella octangula's core is the octahedron; every corner of I and D has gauge 1 (gauge machinery).
NEGATIVE: the cube has 0 discs under both definitions (its 6 diagonal planes carry 2 edges each); the dodecahedron has 0.
Faults fixed on the way, over 6 runs: no |x| on the field class (added in the script); a test `None in` list that called the field's
equality; an unbound variable in a diagnostic line; a float tolerance check against a rounded angle. All of these were script faults.
None changed a value.

## LEADS
1. Rerun the 11-11 Vacuus census with the #87 closed-sheet test. The "share of edges on discs" ranking in Ch 4 (Sunstar tetrahedral
   cluster 94 %, Hexa-Key 80 %, ...) uses the ≥ 3-edges-on-a-plane rule. For the convex controls the two rules agree. For non-convex
   solids they need not, as the Dogstar shows.
2. A name for Dogstar's open fans (a "bow-tie" pair per mirror plane) is DICTO's to give.
3. The octet's layer faces meet at the golden point 1/φ² of an edge. Is that point a corner of the EKP-type roof sheet that forms beyond
   s = 1 + √5/2?

## Sources checked
papers/book-platonic chapters ch01, ch04, ch10 (the three passages and their "Claimed, known, open" boxes);
studies/2026-11-06-crossed-nest (README, compounds.py, overlap.py, roofs.py, data-*.txt); studies/2026-11-11-orbit-polytopes (README
Dogstar and census sections, vacuus_census.py, data/dogstar_vacuus.json, data/vacuus_census.json); studies/2026-11-02-dicto-vacuus
(README definition, vacuus.py sheet and disc code, qf.py); Concordance ledger [130], [131]. The reference library was not searched (no
prior-art question: the compounds and their cores are classical, as the draft already says).

DICTO · dictospheres.com
