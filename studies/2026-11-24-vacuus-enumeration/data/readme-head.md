# Vacuus enumeration, row V of the V SF A map (24 Nov 2026)

DICTO · study for the V SF A project (Vacuus, Scutoid Frusta, Aequus), row V: the Vacuus alone.

**Decisions of DICTO (24 Nov).** (1) The Vacuus is the edge-plate definition of #110. The face-parallel planes are a separate construction, not the Vacuus; their tables are kept and labelled as such. (2) Aequus is widened to include face-transitive dice, so the three permutahedron duals are Aequi. (3) Johnson solids: both centres, (a) corner centroid and (b) volume centroid, are computed and compared.

**Conclusion.** Exactly computed (number fields, no rounding in any decision): the Vacuus of all 5 Platonic, 13 Archimedean and 13 Catalan solids and of the prisms, antiprisms, bipyramids and trapezohedra for n = 3 to 12 (71 rows); the 92 Johnson solids as a floating-point pilot (clear margins, not yet exact). A solid is of the **heart** kind exactly when it is centrally symmetric (Lemma 1). The Vacuus of the dodecahedral permutahedron has **90 plates** (60 + 30, all full sheets, none a mirror). The statement 31 = 15 + 10 + 6 (the 15 mirrors of H3; the 6 = the icosidodecahedron's Vacuus) holds for its **face-parallel planes**, a separate construction, not for its Vacuus. The three permutahedra and their dual dice pass every exact check of the rolling law (Section 4).

Status: exact for Tables 1 and 2 and Section 4; Table 3 (Johnson) is a float pilot, to be made exact before any release.

## 1. Definitions used (no new ones)

From Walls of Silence (#110, Section 2), which widens #87 (fins to the edges) and #105 (central slices carrying two-faces): for a convex polytope X with centre O, each edge (a ridge, in 3D) spans with O a plane through O, its **plate**; the Vacuus is the set of plates, each with the edges on it. A plate is a **full sheet** if with each edge e it carries the opposite edge −e, a **shared sheet** if it carries two or more edges but is not full, a **single fin** if it carries one. The Vacuus is of the **heart** kind when every plate is a full sheet, **non-heart** when every plate is a single fin, **inherited heart** otherwise (DICTO's names).

**Face-parallel planes (a separate construction, not the Vacuus).** The planes through O parallel to a face, one per pair of parallel faces (or per face). Called "face plates" in the tables and data files; they are not plates of the Vacuus. They coincide with the Vacuus plates only for the rhombic dodecahedron and the rhombic triacontahedron.

The centre O is the corner centroid (#87); for Tables 1 and 2 it is the centre of the symmetry group. The **slice** of a plate is the polygon the plate cuts from the solid (corners of the solid on the plate plus crossings of edges); "regular" means equal sides and equal radii, both checked exactly.

## 2. Method

- `scripts/vacuus_exact.py`: coordinates exactly in Q(√2), Q(√5), Q(t) (tribonacci, snub cube), Q(ξ) (ξ³ − 2ξ = φ, snub dodecahedron, degree 6), and Q(cos π/2n, h) for the prism family (degree up to 16). The convex hull from floats is checked exactly: every face's corners coplanar, every other corner strictly inside, Euler, all edges equal for the uniform solids. Catalan solids are the polars (corner = face normal / support value). Plates are grouped by exact canonical normals; mirrors are found as the planes whose exact reflection maps the corner set to itself. Signs of nonzero field elements come from an 80-digit evaluation of the exact element.
- The snub dodecahedron is the orbit of one listed vertex, −(2α, 2, 2β), under the 60 rotations that permute an icosahedron's corners (built exactly; of the two golden orientations, one gives 60 corners with 150 equal edges and was kept, the other failed the equal-edge check, as logged).
- `scripts/perm_checks.py`: the permutahedron and dual-die checks of Section 4 (exact 3×3 matrices, group closure).
- `scripts/johnson_pilot.py`: the same definitions in floating point on the app registry's 92 Johnson solids; full symmetry group by search; every merge decision has defect ≤ 8.1e-13, every separation ≥ 6.9e-3 (per-solid values in `data/johnson-pilot.json`).
- `scripts/coincidences.py`: equal plate systems between solids (exact keys in a shared field), and the CSV. `scripts/make_tables.py`: the tables below.
- Prior art and sources: Archimedean solids (Archimedes; complete list Kepler 1619), Catalan solids (Catalan 1865), Johnson solids (Johnson 1966; completeness Zalgaller 1967), permutahedron (Schoute 1911), reflection groups (Coxeter 1934), Matsumoto's theorem (Matsumoto 1964; Tits 1969). The Vacuus reading of each shape is DICTO's.

## 3. Results

**Lemma 1 (heart = centrally symmetric).** The Vacuus of (X, O) is of the heart kind exactly when X is centrally symmetric about O. Proof: if X = −X, the plate through O and edge e contains −e, so every plate is full. Conversely, if every plate is full, every edge e has −e as an edge, so the corner set, hence X, is centrally symmetric. ∎ Every row of Tables 1 to 3 agrees.

**Counts.** Exact (71 rows; the cube and octahedron recur as the n = 3, 4 prism-family members): heart 44, inherited heart 13, non-heart 14. Johnson pilot (92): heart 13, inherited heart 50, non-heart 29.

**Proposition 2 (the Catalan Vacuus lies in the mirrors).** If every edge of a solid P has its two ends swapped by a reflection of P (all Platonic and Archimedean solids except the two snubs), then every edge plate of the polar P* is a mirror. Proof: the edge of P* dual to the edge AB of P joins (multiples of) the normals n₁, n₂ of the two faces at AB. Both faces contain AB, so n₁ and n₂ are at right angles to B − A, that is, both lie in the plane x·(B − A) = 0 through O. That plane is the mirror of the reflection swapping A and B (|A| = |B|), a symmetry by assumption, and since n₁ ≠ ±n₂ it is the plate through O, n₁, n₂. ∎ Checked exactly: every edge plate of all 11 non-snub Catalan solids and all bipyramids is a mirror; for the trapezohedra (duals of antiprisms, whose side edges are swapped by a half-turn, not a reflection) only n of the plates are mirrors.

**Inherited heart without central symmetry** comes two ways in these tables: a mirror carrying several edges (the bipyramids' equator, the C_nv Johnson solids), or a plate holding a 2-fold axis, so that the half-turn carries one edge onto a second edge on the same plate (snub cube and pentagonal icositetrahedron: 12 shared plates of 2 edges, no mirrors at all; snub disphenoid J84). The snub dodecahedron and its dual are non-heart: 150 single fins.

**Coincidences** (equal plate systems, exact; full list in `data/coincidences.txt`, 53 lines). Among them:
- edge plates = face plates in one solid: rhombic dodecahedron (6), rhombic triacontahedron (15), and no other solid.
- the 6 mirrors through the cube's face diagonals carry the edge plates of tetrahedron, cube, triakis tetrahedron, rhombic dodecahedron and tetrakis hexahedron; the 9 mirrors of Oh carry those of triakis octahedron, deltoidal icositetrahedron and disdyakis dodecahedron; the 15 mirrors of Ih carry those of dodecahedron, icosahedron and all 6 icosahedral non-snub Catalans.
- the octahedron's 3 square plates = the cube's face plates; the cuboctahedron's 4 hexagon plates = the face plates of tetrahedron, octahedron and truncated tetrahedron; the icosidodecahedron's 6 decagon plates = the dodecahedron's face plates.
- face plates shared by a solid and its truncations: cuboctahedron, truncated cube, truncated octahedron (7); rhombicuboctahedron and truncated cuboctahedron (13); icosidodecahedron and truncated dodecahedron (16); rhombicosidodecahedron and truncated icosidodecahedron (31).
- prism family: the 3-gonal antiprism (octahedron) edge plates = the 3-gonal trapezohedron (cube) face plates; for n = 4, 8, 12 the prism's face plates = the bipyramid's edge plates.

**Johnson solids with no symmetry centre.** 56 of the 92 have a symmetry group fixing a whole line or plane, so no point is singled out by symmetry; O is then only the corner centroid: J1–J11, J18–J25, J32, J33, J40, J41, J47, J49, J50, J52–J54, J56, J58, J60–J66, J68, J70–J72, J74–J79, J81–J83, J86–J89, J92. The other 36 have a unique symmetry centre (question 2).

## 4. The three permutahedra and their dice (exact)

| | truncated octahedron (A3) | truncated cuboctahedron (B3) | truncated icosidodecahedron (H3) |
|---|---|---|---|
| corners = order of W | 24 | 48 | 120 |
| Coxeter mirrors (mirrors carrying no corner) | 6 | 9 | 15 |
| corners one per chamber; W transitive | yes | yes | yes |
| each edge crosses exactly one Coxeter mirror, whose reflection swaps its ends | yes | yes | yes |
| each 2m-gon face crosses the m mirrors through its axis, each twice; (st)^m = 1 | yes (m = 2, 3) | yes (2, 3, 4) | yes (2, 3, 5) |
| Vacuus plates (edge plates) | 15: 12 hexagon slices + 3 octagon slices (the 3 on mirrors) | 36, none on a mirror | 90 (60 + 30), none on a mirror |
| face-parallel planes (not the Vacuus) | 7 = 3 (square, mirror) + 4 (hexagon) | 13 = 6 (square, mirror) + 4 (hexagon) + 3 (octagon, mirror) | 31 = 15 (square, mirror) + 10 (hexagon) + 6 (decagon) |
| face-parallel planes that are Coxeter mirrors | 0 (its 3 mirror face plates are the coordinate mirrors of B3, not of A3) | 9 = all | 15 = all |

**The dodecahedral permutahedron check (V SF A item 1).** Its Vacuus has 90 plates, none a mirror. The statement holds for the face-parallel planes (not the Vacuus): 31 = 15 parallel to the 30 squares + 10 parallel to the 20 hexagons + 6 parallel to the 12 decagons. The 15 square plates are exactly the 15 mirrors of H3 (each square is crossed by a 2-fold axis, and since −1 is in H3 the plane through O at right angles to a 2-fold axis is a mirror). The 120 corners lie one in each of the 120 chambers. Each of the 180 edges crosses exactly one square plate. The 6 decagon plates are exactly the 6 edge plates of the icosidodecahedron (its Vacuus, 6 regular decagons). The slices are not squares or decagons: a square plate cuts a 12-gon, a hexagon plate a 12-gon, a decagon plate a 20-gon. So V SF A item 1 should read: "the face-parallel planes of the dodecahedral permutahedron …"; its Vacuus is the 90 edge plates.

The 12 hexagon-slice and 3 octagon-slice edge plates of the truncated octahedron are #105's "15 central cards, three of them octagons in the coordinate planes", recomputed.

**The dice.** Tetrakis hexahedron (24 faces), disdyakis dodecahedron (48), disdyakis triacontahedron (120), checked exactly:
- face-transitive under W (6, 9, 15 Coxeter mirrors; W of order 24, 48, 120);
- each face is one chamber: its corners lie on two or more mirrors, inside the closure of one chamber, and the faces fill the 24, 48, 120 chambers once each;
- rolling across any edge is one reflection, in the mirror holding that edge, and that reflection carries one face onto the other;
- the wall types (three per face, carried from face to face by the rolls) are consistent, and round every corner two types alternate, k each, with (st)^k = 1 for k minimal: corners of valence 4, 6 (tetrakis hexahedron, k = 2, 3), 4, 6, 8 (disdyakis dodecahedron, k = 2, 3, 4), 4, 6, 10 (disdyakis triacontahedron, k = 2, 3, 5).

**Aequi (widened definition).** With face-transitive dice admitted (DICTO, 24 Nov), the three are Aequi. Being fair by symmetry, they belong to the classical isohedral dice: a die is fair by symmetry exactly when it is face-transitive (Diaconis and Keller, "Fair dice", Amer. Math. Monthly 96 (1989) 337–339). They are not in the #111/#112 catalogue, which required two or more kinds of face and face directions along symmetry axes. Their codes are DICTO's to name; placeholders: Aequus A3-24 (tetrakis hexahedron), Aequus B3-48 (disdyakis dodecahedron), Aequus H3-120 (disdyakis triacontahedron).

**The rolling law (proposition for DICTO).** Let W be a finite reflection group of rank 3 (A3, B3 or H3) with simple reflections s₁, s₂, s₃, and let m_ij be the order of s_i s_j. Let A be the Aequus of W: the polar of the W-permutahedron (tetrakis hexahedron, disdyakis dodecahedron, disdyakis triacontahedron). Then:
1. **Faces are the group.** The faces of A are the chambers of the mirrors of W, one each, so they correspond one to one with the elements of W. Each face has three edges of the three types 1, 2, 3.
2. **One roll is one reflection.** Rolling A across an edge of type i takes the face of w to the face of w·s_i. As a motion of space it is the reflection in the mirror that holds that edge.
3. **Corner relation.** A corner where edges of types i and j meet has valence 2·m_ij. Rolling once round it alternates the types i, j, and returns to the start: (s_i s_j)^m_ij = 1.
4. **Shortest rolls.** The fewest rolls from face u to face v equals the number of mirrors separating the two faces, which is the length of u⁻¹v in the generators s₁, s₂, s₃.
5. **Matsumoto's theorem.** Any two shortest roll sequences between the same two faces can be turned into one another by corner moves alone. A corner move replaces m_ij alternating rolls i, j, i, … by the m_ij rolls j, i, j, … that go round the same corner the other way.

Items 1 to 3 are checked exactly here for A3, B3 and H3 (Section 4). Items 4 and 5 are standard theorems on reflection groups (Coxeter 1934; Matsumoto 1964; Tits 1969) and are not recomputed. The reading of them as rolling an Aequus is DICTO's.

## 5. LEADS

1. Make Table 3 exact (Johnson coordinates in number fields; J84–J90 need cubic and higher fields).
2. The trapezohedra: find the rule for which of their plates are mirrors (exactly n here); more broadly, the edge plates of a polar P* are mirrors exactly at the edges of P whose ends a reflection swaps.
3. Inherited heart without central symmetry: test whether every shared sheet is forced by a mirror or a 2-fold axis in the plate (true in all rows here).
4. Face plates as their own object: they are shared along truncation families (7, 13, 16, 31 above); is the face-plate system of an omnitruncation always the full mirror set plus the plates of its rank-2 faces?
5. 4D pilot, not run (cost): the omnitruncations of A4, B4, H4 with the same exact checks (A4 Vacuus already in #105: 65 plates); the 600-cell and 120-cell are in #110.
6. V + A: the Vacuus of every Aequus (running elsewhere) can reuse `vacuus_exact.py` directly.

## 6. Questions for DICTO

1. (Answered 24 Nov: the Vacuus is the edge-plate definition.) Do the face-parallel planes need a name of their own?
2. (Answered 24 Nov: compute both the corner centroid and the volume centroid.)
3. (Answered 24 Nov: Aequus widened to face-transitive dice.) Codes for the three: the placeholders above, or names of your choice.
4. "Plate shape": reported here as the slice polygon the plate cuts. Did you mean the slice, or the face the plate is parallel to?

## Files

`scripts/` (vacuus_exact.py, perm_checks.py, johnson_pilot.py, coincidences.py, make_tables.py) · `data/exact-uniform.json`, `data/exact-prisms.json`, `data/johnson-pilot.json`, `data/vacuus-enumeration.csv`, `data/coincidences.txt`, `data/tables.md`, logs `data/*.log`, Johnson source coordinates `data/johnson-float-source.json`.

## Tables
