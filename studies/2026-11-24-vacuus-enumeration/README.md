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

## Resume notes (work in progress, 24 Nov)

- Milestone 1 (done): DICTO's three decisions in the text; the Aequus wording and the rolling-law proposition updated.
- Milestone 2 (running): an exact Johnson table with both centres (scripts/johnson_exact.py). Plan: build J1–J83, J91 and J92 exactly from exact uniform pieces (caps, prisms, antiprisms, pyramid and cupola augmentations, gyrations by half-turns), match each one to the registry by its pairwise-distance invariant, check exactly that it has regular faces and is convex, then analyse it about (a) the corner centroid and (b) the volume centroid. J84–J90 stay floating point (their coordinates are roots of systems of higher degree).
- Milestone 3 (queued): the 4D pilot (scripts/four_d.py): the six regular polytopes and the omnitruncations of A4, B4 and H4. Plates are the hyperplanes through O spanned by the 2-faces; for each one: ridges carried, sheet kind, and whether it is a mirror.
### Table 1. Platonic, Archimedean, Catalan (exact)

Edge plates: count × edges on the plate, sheet kind, slice (the solid cut by the plate). Face plates: count × [sides of the faces parallel to it], slice. Mirror = the plate is a mirror of the solid's full symmetry group.

| solid | group | mirrors | centr. symm. | kind | edge plates | edge-plate classes | on mirrors | face plates | face-plate classes |
|---|---|---|---|---|---|---|---|---|---|
| tetrahedron | Td | 6 | no | **non-heart** | 6 | 6×1 single, 3-gon (2 side lengths) (mirror) | 6 | 4 | 4×[3], regular 3-gon |
| cube | Oh | 9 | yes | **heart** | 6 | 6×2 full, 4-gon (2 side lengths) (mirror) | 6 | 3 | 3×[4+4], regular 4-gon (mirror) |
| octahedron | Oh | 9 | yes | **heart** | 3 | 3×4 full, regular 4-gon (mirror) | 3 | 4 | 4×[3+3], regular 6-gon |
| dodecahedron | Ih | 15 | yes | **heart** | 15 | 15×2 full, 6-gon (2 side lengths) (mirror) | 15 | 6 | 6×[5+5], regular 10-gon |
| icosahedron | Ih | 15 | yes | **heart** | 15 | 15×2 full, 6-gon (2 side lengths) (mirror) | 15 | 10 | 10×[3+3], 12-gon (1 side length) |
| truncated tetrahedron | Td | 6 | no | **non-heart** | 18 | 12×1 single, 4-gon (3 side lengths); 6×1 single, 5-gon (3 side lengths) (mirror) | 6 | 4 | 4×[3+6], 6-gon (2 side lengths) |
| triakis tetrahedron | Td | 6 | no | **inherited heart** | 6 | 6×3 shared, 5-gon (3 side lengths) (mirror) | 6 | 12 | 12×[3], 8-gon (4 side lengths) |
| cuboctahedron | Oh | 9 | yes | **heart** | 4 | 4×6 full, regular 6-gon | 0 | 7 | 4×[3+3], regular 6-gon; 3×[4+4], regular 4-gon (mirror) |
| rhombic dodecahedron | Oh | 9 | yes | **heart** | 6 | 6×4 full, 6-gon (2 side lengths) (mirror) | 6 | 6 | 6×[4+4], 6-gon (2 side lengths) (mirror) |
| truncated cube | Oh | 9 | yes | **heart** | 18 | 12×2 full, 6-gon (2 side lengths); 6×2 full, 8-gon (3 side lengths) (mirror) | 6 | 7 | 4×[3+3], regular 6-gon; 3×[8+8], regular 4-gon (mirror) |
| triakis octahedron | Oh | 9 | yes | **heart** | 9 | 6×4 full, 8-gon (2 side lengths) (mirror); 3×4 full, regular 4-gon (mirror) | 9 | 12 | 12×[3+3], 12-gon (3 side lengths) |
| truncated octahedron | Oh | 9 | yes | **heart** | 15 | 12×2 full, 6-gon (2 side lengths); 3×4 full, 8-gon (2 side lengths) (mirror) | 3 | 7 | 4×[6+6], regular 6-gon; 3×[4+4], 8-gon (2 side lengths) (mirror) |
| tetrakis hexahedron | Oh | 9 | yes | **heart** | 6 | 6×6 full, 6-gon (2 side lengths) (mirror) | 6 | 12 | 12×[3+3], 10-gon (3 side lengths) |
| rhombicuboctahedron | Oh | 9 | yes | **heart** | 24 | 24×2 full, 8-gon (3 side lengths) | 0 | 13 | 6×[4+4], 8-gon (3 side lengths) (mirror); 4×[3+3], 12-gon (2 side lengths); 3×[4+4], regular 8-gon (mirror) |
| deltoidal icositetrahedron | Oh | 9 | yes | **heart** | 9 | 6×4 full, 8-gon (2 side lengths) (mirror); 3×8 full, regular 8-gon (mirror) | 9 | 12 | 12×[4+4], 8-gon (2 side lengths) |
| truncated cuboctahedron | Oh | 9 | yes | **heart** | 36 | 24×2 full, 8-gon (3 side lengths); 12×2 full, 12-gon (4 side lengths) | 0 | 13 | 6×[4+4], 8-gon (3 side lengths) (mirror); 4×[6+6], 12-gon (2 side lengths); 3×[8+8], 8-gon (2 side lengths) (mirror) |
| disdyakis dodecahedron | Oh | 9 | yes | **heart** | 9 | 6×8 full, 8-gon (2 side lengths) (mirror); 3×8 full, 8-gon (1 side length) (mirror) | 9 | 24 | 24×[3+3], 18-gon (9 side lengths) |
| icosidodecahedron | Ih | 15 | yes | **heart** | 6 | 6×10 full, regular 10-gon | 0 | 16 | 10×[3+3], regular 6-gon; 6×[5+5], regular 10-gon |
| rhombic triacontahedron | Ih | 15 | yes | **heart** | 15 | 15×4 full, 8-gon (3 side lengths) (mirror) | 15 | 15 | 15×[4+4], 8-gon (3 side lengths) (mirror) |
| truncated icosahedron | Ih | 15 | yes | **heart** | 45 | 30×2 full, 10-gon (3 side lengths); 15×2 full, 10-gon (3 side lengths) (mirror) | 15 | 16 | 10×[6+6], 18-gon (2 side lengths); 6×[5+5], regular 10-gon |
| pentakis dodecahedron | Ih | 15 | yes | **heart** | 15 | 15×6 full, 10-gon (3 side lengths) (mirror) | 15 | 30 | 30×[3+3], 20-gon (5 side lengths) |
| truncated dodecahedron | Ih | 15 | yes | **heart** | 45 | 30×2 full, 10-gon (3 side lengths); 15×2 full, 10-gon (3 side lengths) (mirror) | 15 | 16 | 10×[3+3], regular 6-gon; 6×[10+10], regular 10-gon |
| triakis icosahedron | Ih | 15 | yes | **heart** | 15 | 15×6 full, 10-gon (3 side lengths) (mirror) | 15 | 30 | 30×[3+3], 24-gon (6 side lengths) |
| rhombicosidodecahedron | Ih | 15 | yes | **heart** | 60 | 30×2 full, 12-gon (4 side lengths); 30×2 full, 16-gon (5 side lengths) | 0 | 31 | 15×[4+4], 12-gon (3 side lengths) (mirror); 10×[3+3], 12-gon (2 side lengths); 6×[5+5], 20-gon (2 side lengths) |
| deltoidal hexecontahedron | Ih | 15 | yes | **heart** | 15 | 15×8 full, 12-gon (3 side lengths) (mirror) | 15 | 30 | 30×[4+4], 14-gon (3 side lengths) |
| truncated icosidodecahedron | Ih | 15 | yes | **heart** | 90 | 60×2 full, 12-gon (4 side lengths); 30×2 full, 20-gon (6 side lengths) | 0 | 31 | 15×[4+4], 12-gon (3 side lengths) (mirror); 10×[6+6], 12-gon (2 side lengths); 6×[10+10], 20-gon (2 side lengths) |
| disdyakis triacontahedron | Ih | 15 | yes | **heart** | 15 | 15×12 full, 12-gon (3 side lengths) (mirror) | 15 | 60 | 60×[3+3], 30-gon (14 side lengths) |
| snub cube | O | 0 | no | **inherited heart** | 48 | 24×1 single, 12-gon (11 side lengths); 12×1 single, 13-gon (7 side lengths); 12×2 shared, 10-gon (6 side lengths) | 0 | 31 | 24×[3], 15-gon (9 side lengths); 4×[3+3], 18-gon (3 side lengths); 3×[4+4], 12-gon (2 side lengths) |
| pentagonal icositetrahedron | O | 0 | no | **inherited heart** | 48 | 24×1 single, 9-gon (8 side lengths); 12×1 single, 9-gon (5 side lengths); 12×2 shared, 8-gon (4 side lengths) | 0 | 24 | 24×[5], 9-gon (6 side lengths) |
| snub dodecahedron | I | 0 | no | **non-heart** | 150 | 60×1 single, 17-gon (17 side lengths); 60×1 single, 20-gon (19 side lengths); 30×1 single, 21-gon (11 side lengths) | 0 | 76 | 60×[3], 21-gon (21 side lengths); 10×[3+3], 18-gon (3 side lengths); 6×[5+5], 30-gon (3 side lengths) |
| pentagonal hexecontahedron | I | 0 | no | **non-heart** | 150 | 60×1 single, 13-gon (13 side lengths); 60×1 single, 15-gon (14 side lengths); 30×1 single, 17-gon (9 side lengths) | 0 | 60 | 60×[5], 15-gon (15 side lengths) |

### Table 2. Prisms, antiprisms (regular faces, unit circumradius base) and their duals, n = 3 to 12 (exact)

| solid | mirrors | centr. symm. | kind | edge plates | edge-plate classes | face plates |
|---|---|---|---|---|---|---|
| 3-gonal prism | 4 | no | **non-heart** | 9 | 6×1 single, 4-gon (3 side lengths); 3×1 single, 4-gon (2 side lengths) (mirror) | 4 |
| 3-gonal bipyramid | 4 | no | **inherited heart** | 4 | 3×2 shared, 4-gon (2 side lengths) (mirror); 1×3 shared, regular 3-gon (mirror) | 6 |
| 3-gonal antiprism | 9 | yes | **heart** | 3 | 3×4 full, regular 4-gon (mirror) | 4 |
| 3-gonal trapezohedron | 9 | yes | **heart** | 6 | 6×2 full, 4-gon (2 side lengths) (mirror) | 3 |
| 4-gonal prism | 9 | yes | **heart** | 6 | 6×2 full, 4-gon (2 side lengths) (mirror) | 3 |
| 4-gonal bipyramid | 9 | yes | **heart** | 3 | 3×4 full, regular 4-gon (mirror) | 4 |
| 4-gonal antiprism | 4 | no | **non-heart** | 16 | 8×1 single, 5-gon (3 side lengths); 8×1 single, 6-gon (4 side lengths) | 9 |
| 4-gonal trapezohedron | 4 | no | **inherited heart** | 12 | 8×1 single, 5-gon (3 side lengths); 4×2 shared, 4-gon (2 side lengths) (mirror) | 8 |
| 5-gonal prism | 6 | no | **non-heart** | 15 | 10×1 single, 6-gon (4 side lengths); 5×1 single, 4-gon (2 side lengths) (mirror) | 6 |
| 5-gonal bipyramid | 6 | no | **inherited heart** | 6 | 5×2 shared, 4-gon (2 side lengths) (mirror); 1×5 shared, regular 5-gon (mirror) | 10 |
| 5-gonal antiprism | 5 | yes | **heart** | 10 | 5×2 full, 4-gon (2 side lengths); 5×2 full, 6-gon (2 side lengths) | 6 |
| 5-gonal trapezohedron | 5 | yes | **heart** | 10 | 5×2 full, 4-gon (2 side lengths) (mirror); 5×2 full, 6-gon (2 side lengths) | 5 |
| 6-gonal prism | 7 | yes | **heart** | 9 | 6×2 full, 6-gon (2 side lengths); 3×2 full, 4-gon (2 side lengths) (mirror) | 4 |
| 6-gonal bipyramid | 7 | yes | **heart** | 4 | 3×4 full, 4-gon (1 side length) (mirror); 1×6 full, regular 6-gon (mirror) | 6 |
| 6-gonal antiprism | 6 | no | **non-heart** | 24 | 12×1 single, 10-gon (6 side lengths); 12×1 single, 5-gon (3 side lengths) | 13 |
| 6-gonal trapezohedron | 6 | no | **inherited heart** | 18 | 12×1 single, 7-gon (4 side lengths); 6×2 shared, 4-gon (2 side lengths) (mirror) | 12 |
| 7-gonal prism | 8 | no | **non-heart** | 21 | 14×1 single, 8-gon (5 side lengths); 7×1 single, 4-gon (2 side lengths) (mirror) | 8 |
| 7-gonal bipyramid | 8 | no | **inherited heart** | 8 | 7×2 shared, 4-gon (2 side lengths) (mirror); 1×7 shared, regular 7-gon (mirror) | 14 |
| 7-gonal antiprism | 7 | yes | **heart** | 14 | 7×2 full, 10-gon (3 side lengths); 7×2 full, 4-gon (2 side lengths) | 8 |
| 7-gonal trapezohedron | 7 | yes | **heart** | 14 | 7×2 full, 4-gon (2 side lengths) (mirror); 7×2 full, 8-gon (3 side lengths) | 7 |
| 8-gonal prism | 9 | yes | **heart** | 12 | 8×2 full, 8-gon (3 side lengths); 4×2 full, 4-gon (2 side lengths) (mirror) | 5 |
| 8-gonal bipyramid | 9 | yes | **heart** | 5 | 4×4 full, 4-gon (1 side length) (mirror); 1×8 full, regular 8-gon (mirror) | 8 |
| 8-gonal antiprism | 8 | no | **non-heart** | 32 | 16×1 single, 14-gon (8 side lengths); 16×1 single, 5-gon (3 side lengths) | 17 |
| 8-gonal trapezohedron | 8 | no | **inherited heart** | 24 | 16×1 single, 9-gon (5 side lengths); 8×2 shared, 4-gon (2 side lengths) (mirror) | 16 |
| 9-gonal prism | 10 | no | **non-heart** | 27 | 18×1 single, 10-gon (6 side lengths); 9×1 single, 4-gon (2 side lengths) (mirror) | 10 |
| 9-gonal bipyramid | 10 | no | **inherited heart** | 10 | 9×2 shared, 4-gon (2 side lengths) (mirror); 1×9 shared, regular 9-gon (mirror) | 18 |
| 9-gonal antiprism | 9 | yes | **heart** | 18 | 9×2 full, 14-gon (4 side lengths); 9×2 full, 4-gon (2 side lengths) | 10 |
| 9-gonal trapezohedron | 9 | yes | **heart** | 18 | 9×2 full, 10-gon (3 side lengths); 9×2 full, 4-gon (2 side lengths) (mirror) | 9 |
| 10-gonal prism | 11 | yes | **heart** | 15 | 10×2 full, 10-gon (3 side lengths); 5×2 full, 4-gon (2 side lengths) (mirror) | 6 |
| 10-gonal bipyramid | 11 | yes | **heart** | 6 | 5×4 full, 4-gon (1 side length) (mirror); 1×10 full, regular 10-gon (mirror) | 10 |
| 10-gonal antiprism | 10 | no | **non-heart** | 40 | 20×1 single, 18-gon (10 side lengths); 20×1 single, 5-gon (3 side lengths) | 21 |
| 10-gonal trapezohedron | 10 | no | **inherited heart** | 30 | 20×1 single, 11-gon (6 side lengths); 10×2 shared, 4-gon (2 side lengths) (mirror) | 20 |
| 11-gonal prism | 12 | no | **non-heart** | 33 | 22×1 single, 12-gon (7 side lengths); 11×1 single, 4-gon (2 side lengths) (mirror) | 12 |
| 11-gonal bipyramid | 12 | no | **inherited heart** | 12 | 11×2 shared, 4-gon (2 side lengths) (mirror); 1×11 shared, regular 11-gon (mirror) | 22 |
| 11-gonal antiprism | 11 | yes | **heart** | 22 | 11×2 full, 18-gon (5 side lengths); 11×2 full, 4-gon (2 side lengths) | 12 |
| 11-gonal trapezohedron | 11 | yes | **heart** | 22 | 11×2 full, 12-gon (4 side lengths); 11×2 full, 4-gon (2 side lengths) (mirror) | 11 |
| 12-gonal prism | 13 | yes | **heart** | 18 | 12×2 full, 12-gon (4 side lengths); 6×2 full, 4-gon (2 side lengths) (mirror) | 7 |
| 12-gonal bipyramid | 13 | yes | **heart** | 7 | 6×4 full, 4-gon (1 side length) (mirror); 1×12 full, regular 12-gon (mirror) | 12 |
| 12-gonal antiprism | 12 | no | **non-heart** | 48 | 24×1 single, 22-gon (12 side lengths); 24×1 single, 5-gon (3 side lengths) | 25 |
| 12-gonal trapezohedron | 12 | no | **inherited heart** | 36 | 24×1 single, 13-gon (7 side lengths); 12×2 shared, 4-gon (2 side lengths) (mirror) | 24 |

### Table 3. The 92 Johnson solids (FLOAT PILOT, not exact; O = corner centroid)

Symmetry centre: 'point' when the full symmetry group fixes only O; 'axis/plane' when it fixes a line or plane (C_nv, C_s), so O is fixed only by the corner-centroid convention. Classes: count × edges per plate, sheet, slice sides (M = on a mirror).

| J | solid | group order | mirrors | symmetry centre | kind | edge plates | classes |
|---|---|---|---|---|---|---|---|
| 1 | square pyramid | 8 | 4 | axis/plane | **inherited heart** | 6 | 4×1 single 4-gon; 2×2 shared 3-gon M |
| 2 | pentagonal pyramid | 10 | 5 | axis/plane | **non-heart** | 10 | 5×1 single 5-gon; 5×1 single 3-gon M |
| 3 | triangular cupola | 6 | 3 | axis/plane | **non-heart** | 15 | 9×1 single 4-gon; 6×1 single 6-gon |
| 4 | square cupola | 8 | 4 | axis/plane | **non-heart** | 20 | 8×1 single 8-gon; 8×1 single 5-gon; 4×1 single 4-gon |
| 5 | pentagonal cupola | 10 | 5 | axis/plane | **non-heart** | 25 | 10×1 single 10-gon; 10×1 single 4-gon; 5×1 single 6-gon |
| 6 | pentagonal rotunda | 10 | 5 | axis/plane | **non-heart** | 35 | 25×1 single 6-gon; 10×1 single 10-gon |
| 7 | elongated triangular pyramid | 6 | 3 | axis/plane | **inherited heart** | 9 | 3×1 single 5-gon; 3×2 shared 5-gon M; 3×1 single 3-gon |
| 8 | elongated square pyramid | 8 | 4 | axis/plane | **inherited heart** | 10 | 4×1 single 6-gon; 4×1 single 4-gon; 2×4 shared 5-gon M |
| 9 | elongated pentagonal pyramid | 10 | 5 | axis/plane | **inherited heart** | 15 | 5×1 single 7-gon; 5×2 shared 5-gon M; 5×1 single 5-gon |
| 10 | gyroelongated square pyramid | 8 | 4 | axis/plane | **inherited heart** | 18 | 12×1 single 6-gon; 4×1 single 7-gon; 2×2 shared 5-gon M |
| 11 | gyroelongated pentagonal pyramid | 10 | 5 | axis/plane | **non-heart** | 25 | 10×1 single 8-gon; 10×1 single 7-gon; 5×1 single 5-gon M |
| 12 | triangular bipyramid | 12 | 4 | point | **inherited heart** | 4 | 3×2 shared 4-gon M; 1×3 shared 3-gon M |
| 13 | pentagonal bipyramid | 20 | 6 | point | **inherited heart** | 6 | 5×2 shared 4-gon M; 1×5 shared 5-gon M |
| 14 | elongated triangular bipyramid | 12 | 4 | point | **inherited heart** | 9 | 6×1 single 5-gon; 3×3 shared 6-gon M |
| 15 | elongated square bipyramid | 16 | 5 | point | **heart** | 6 | 4×2 full 4-gon; 2×6 full 6-gon M |
| 16 | elongated pentagonal bipyramid | 20 | 6 | point | **inherited heart** | 15 | 10×1 single 7-gon; 5×3 shared 6-gon M |
| 17 | gyroelongated square bipyramid | 16 | 4 | point | **inherited heart** | 20 | 16×1 single 7-gon; 4×2 shared 6-gon M |
| 18 | elongated triangular cupola | 6 | 3 | axis/plane | **inherited heart** | 24 | 9×1 single 8-gon; 6×1 single 6-gon; 6×1 single 7-gon; 3×2 shared 6-gon |
| 19 | elongated square cupola | 8 | 4 | axis/plane | **inherited heart** | 32 | 8×1 single 10-gon; 8×1 single 8-gon; 8×1 single 7-gon; 4×2 shared 6-gon; 4×1 single 6-gon |
| 20 | elongated pentagonal cupola | 10 | 5 | axis/plane | **inherited heart** | 40 | 15×1 single 8-gon; 10×1 single 12-gon; 10×1 single 10-gon; 5×2 shared 6-gon |
| 21 | elongated pentagonal rotunda | 10 | 5 | axis/plane | **inherited heart** | 50 | 25×1 single 8-gon; 10×1 single 10-gon; 10×1 single 12-gon; 5×2 shared 8-gon |
| 22 | gyroelongated triangular cupola | 6 | 3 | axis/plane | **non-heart** | 33 | 18×1 single 7-gon; 6×1 single 9-gon; 6×1 single 10-gon; 3×1 single 8-gon |
| 23 | gyroelongated square cupola | 8 | 4 | axis/plane | **non-heart** | 44 | 20×1 single 8-gon; 8×1 single 13-gon; 8×1 single 14-gon; 8×1 single 7-gon |
| 24 | gyroelongated pentagonal cupola | 10 | 5 | axis/plane | **non-heart** | 55 | 10×1 single 17-gon; 10×1 single 7-gon; 10×1 single 9-gon; 10×1 single 18-gon; 10×1 single 8-gon; 5×1 single 12-gon |
| 25 | gyroelongated pentagonal rotunda | 10 | 5 | axis/plane | **non-heart** | 65 | 45×1 single 10-gon; 10×1 single 9-gon; 10×1 single 15-gon |
| 26 | gyrobifastigium | 8 | 2 | point | **inherited heart** | 7 | 4×2 shared 4-gon; 2×1 single 5-gon M; 1×4 shared 4-gon |
| 27 | triangular orthobicupola | 12 | 4 | point | **inherited heart** | 7 | 6×3 shared 6-gon; 1×6 shared 6-gon M |
| 28 | square orthobicupola | 16 | 5 | point | **heart** | 13 | 12×2 full 6-gon; 1×8 full 8-gon M |
| 29 | square gyrobicupola | 16 | 4 | point | **inherited heart** | 17 | 8×2 shared 6-gon; 8×1 single 8-gon; 1×8 shared 8-gon |
| 30 | pentagonal orthobicupola | 20 | 6 | point | **inherited heart** | 21 | 10×2 shared 6-gon; 10×1 single 8-gon; 1×10 shared 10-gon M |
| 31 | pentagonal gyrobicupola | 20 | 5 | point | **heart** | 11 | 5×4 full 6-gon; 5×2 full 6-gon; 1×10 full 10-gon |
| 32 | pentagonal orthocupolarotunda | 10 | 5 | axis/plane | **non-heart** | 50 | 25×1 single 10-gon; 25×1 single 8-gon |
| 33 | pentagonal gyrocupolarotunda | 10 | 5 | axis/plane | **non-heart** | 50 | 40×1 single 10-gon; 10×1 single 9-gon |
| 34 | pentagonal orthobirotunda | 20 | 6 | point | **inherited heart** | 11 | 10×5 shared 10-gon; 1×10 shared 10-gon M |
| 35 | elongated triangular orthobicupola | 12 | 4 | point | **inherited heart** | 27 | 12×1 single 8-gon; 6×1 single 10-gon; 6×2 shared 6-gon; 3×2 shared 8-gon |
| 36 | elongated triangular gyrobicupola | 12 | 3 | point | **heart** | 18 | 9×2 full 8-gon; 6×2 full 6-gon; 3×2 full 10-gon |
| 37 | elongated square gyrobicupola | 16 | 4 | point | **inherited heart** | 36 | 16×1 single 9-gon; 12×2 shared 8-gon; 8×1 single 10-gon |
| 38 | elongated pentagonal orthobicupola | 20 | 6 | point | **inherited heart** | 45 | 20×1 single 9-gon; 10×1 single 12-gon; 10×2 shared 10-gon; 5×2 shared 8-gon |
| 39 | elongated pentagonal gyrobicupola | 20 | 5 | point | **heart** | 30 | 25×2 full 10-gon; 5×2 full 8-gon |
| 40 | elongated pentagonal orthocupolarotunda | 10 | 5 | axis/plane | **inherited heart** | 65 | 40×1 single 12-gon; 10×1 single 11-gon; 10×1 single 10-gon; 5×2 shared 10-gon |
| 41 | elongated pentagonal gyrocupolarotunda | 10 | 5 | axis/plane | **inherited heart** | 65 | 25×1 single 12-gon; 15×1 single 14-gon; 10×1 single 13-gon; 10×1 single 10-gon; 5×2 shared 10-gon |
| 42 | elongated pentagonal orthobirotunda | 20 | 6 | point | **inherited heart** | 65 | 30×1 single 14-gon; 20×1 single 12-gon; 10×2 shared 10-gon; 5×2 shared 12-gon |
| 43 | elongated pentagonal gyrobirotunda | 20 | 5 | point | **heart** | 40 | 15×2 full 14-gon; 15×2 full 12-gon; 10×2 full 10-gon |
| 44 | gyroelongated triangular bicupola | 6 | 0 | point | **non-heart** | 42 | 18×1 single 11-gon; 12×1 single 10-gon; 12×1 single 9-gon |
| 45 | gyroelongated square bicupola | 8 | 0 | point | **non-heart** | 56 | 32×1 single 11-gon; 16×1 single 15-gon; 8×1 single 9-gon |
| 46 | gyroelongated pentagonal bicupola | 10 | 0 | point | **non-heart** | 70 | 30×1 single 11-gon; 20×1 single 19-gon; 15×1 single 13-gon; 5×1 single 9-gon |
| 47 | gyroelongated pentagonal cupolarotunda | 5 | 0 | axis/plane | **non-heart** | 80 | 35×1 single 13-gon; 25×1 single 15-gon; 10×1 single 14-gon; 10×1 single 18-gon |
| 48 | gyroelongated pentagonal birotunda | 10 | 0 | point | **non-heart** | 90 | 30×1 single 15-gon; 20×1 single 14-gon; 20×1 single 19-gon; 20×1 single 13-gon |
| 49 | augmented triangular prism | 4 | 2 | axis/plane | **inherited heart** | 11 | 4×1 single 4-gon; 4×1 single 5-gon; 2×2 shared 4-gon; 1×1 single 5-gon M |
| 50 | biaugmented triangular prism | 4 | 2 | axis/plane | **non-heart** | 17 | 12×1 single 6-gon; 4×1 single 5-gon; 1×1 single 4-gon M |
| 51 | triaugmented triangular prism | 12 | 4 | point | **inherited heart** | 15 | 6×1 single 6-gon; 6×2 shared 6-gon; 3×1 single 5-gon M |
| 52 | augmented pentagonal prism | 4 | 2 | axis/plane | **inherited heart** | 17 | 8×1 single 7-gon; 4×1 single 4-gon; 2×1 single 6-gon; 2×2 shared 6-gon; 1×1 single 5-gon M |
| 53 | biaugmented pentagonal prism | 4 | 2 | axis/plane | **non-heart** | 23 | 10×1 single 8-gon; 8×1 single 7-gon; 2×1 single 6-gon; 2×1 single 4-gon; 1×1 single 4-gon M |
| 54 | augmented hexagonal prism | 4 | 2 | axis/plane | **inherited heart** | 20 | 6×1 single 8-gon; 4×1 single 6-gon; 4×1 single 7-gon; 4×1 single 4-gon; 2×2 shared 5-gon |
| 55 | parabiaugmented hexagonal prism | 8 | 3 | point | **heart** | 11 | 4×2 full 8-gon; 2×2 full 6-gon; 2×2 full 4-gon; 2×4 full 6-gon; 1×2 full 4-gon M |
| 56 | metabiaugmented hexagonal prism | 4 | 2 | axis/plane | **non-heart** | 26 | 8×1 single 7-gon; 6×1 single 8-gon; 4×1 single 9-gon; 4×1 single 4-gon; 2×1 single 6-gon; 2×1 single 10-gon |
| 57 | triaugmented hexagonal prism | 12 | 4 | point | **inherited heart** | 15 | 6×2 shared 8-gon; 6×2 shared 5-gon; 3×2 shared 4-gon |
| 58 | augmented dodecahedron | 10 | 5 | axis/plane | **inherited heart** | 25 | 15×1 single 6-gon; 5×1 single 8-gon; 5×3 shared 7-gon M |
| 59 | parabiaugmented dodecahedron | 20 | 5 | point | **heart** | 15 | 10×2 full 6-gon; 5×4 full 8-gon M |
| 60 | metabiaugmented dodecahedron | 4 | 2 | axis/plane | **inherited heart** | 36 | 14×1 single 8-gon; 8×1 single 6-gon; 4×1 single 10-gon; 4×1 single 7-gon; 4×1 single 9-gon; 1×2 shared 6-gon M; 1×4 shared 8-gon M |
| 61 | triaugmented dodecahedron | 6 | 3 | axis/plane | **inherited heart** | 39 | 18×1 single 8-gon; 6×1 single 11-gon; 6×1 single 7-gon; 3×3 shared 7-gon M; 3×1 single 12-gon; 3×1 single 10-gon |
| 62 | metabidiminished icosahedron | 4 | 2 | axis/plane | **inherited heart** | 19 | 14×1 single 6-gon; 4×1 single 5-gon; 1×2 shared 6-gon M |
| 63 | tridiminished icosahedron | 6 | 3 | axis/plane | **non-heart** | 15 | 9×1 single 4-gon; 3×1 single 6-gon; 3×1 single 5-gon M |
| 64 | augmented tridiminished icosahedron | 6 | 3 | axis/plane | **inherited heart** | 15 | 9×1 single 6-gon; 3×1 single 4-gon; 3×2 shared 6-gon M |
| 65 | augmented truncated tetrahedron | 6 | 3 | axis/plane | **non-heart** | 27 | 21×1 single 6-gon; 3×1 single 7-gon M; 3×1 single 8-gon |
| 66 | augmented truncated cube | 8 | 4 | axis/plane | **inherited heart** | 46 | 24×1 single 8-gon; 8×1 single 9-gon; 4×1 single 6-gon; 4×1 single 10-gon; 4×1 single 12-gon; 2×2 shared 10-gon M |
| 67 | biaugmented truncated cube | 16 | 5 | point | **heart** | 30 | 16×2 full 10-gon; 4×2 full 8-gon; 4×2 full 6-gon; 4×2 full 14-gon; 2×2 full 12-gon M |
| 68 | augmented truncated dodecahedron | 10 | 5 | axis/plane | **inherited heart** | 100 | 40×1 single 12-gon; 25×1 single 10-gon; 10×1 single 14-gon; 10×1 single 13-gon; 10×1 single 11-gon; 5×2 shared 12-gon M |
| 69 | parabiaugmented truncated dodecahedron | 20 | 5 | point | **heart** | 60 | 35×2 full 14-gon; 20×2 full 10-gon; 5×2 full 14-gon M |
| 70 | metabiaugmented truncated dodecahedron | 4 | 2 | axis/plane | **inherited heart** | 116 | 38×1 single 14-gon; 26×1 single 12-gon; 16×1 single 13-gon; 12×1 single 15-gon; 10×1 single 10-gon; 4×1 single 18-gon; 4×1 single 11-gon; 2×2 shared 14-gon; 2×1 single 16-gon; 1×2 shared 10-gon M; 1×2 shared 14-gon M |
| 71 | triaugmented truncated dodecahedron | 6 | 3 | axis/plane | **inherited heart** | 132 | 30×1 single 14-gon; 24×1 single 12-gon; 18×1 single 15-gon; 15×1 single 16-gon; 12×1 single 13-gon; 12×1 single 11-gon; 6×1 single 20-gon; 6×1 single 18-gon; 6×1 single 17-gon; 3×2 shared 12-gon M |
| 72 | gyrate rhombicosidodecahedron | 10 | 5 | axis/plane | **inherited heart** | 75 | 20×2 shared 16-gon; 20×1 single 15-gon; 15×2 shared 12-gon; 10×2 shared 13-gon; 5×1 single 14-gon; 5×1 single 18-gon |
| 73 | parabigyrate rhombicosidodecahedron | 20 | 5 | point | **heart** | 60 | 35×2 full 16-gon; 15×2 full 12-gon; 10×2 full 14-gon |
| 74 | metabigyrate rhombicosidodecahedron | 4 | 2 | axis/plane | **inherited heart** | 88 | 36×1 single 15-gon; 12×2 shared 16-gon; 12×2 shared 13-gon; 10×1 single 18-gon; 6×2 shared 12-gon; 6×1 single 14-gon; 4×1 single 16-gon; 2×2 shared 14-gon |
| 75 | trigyrate rhombicosidodecahedron | 6 | 3 | axis/plane | **inherited heart** | 99 | 42×1 single 15-gon; 15×1 single 18-gon; 15×1 single 16-gon; 12×2 shared 13-gon; 6×2 shared 16-gon; 6×1 single 14-gon; 3×2 shared 14-gon |
| 76 | diminished rhombicosidodecahedron | 10 | 5 | axis/plane | **non-heart** | 105 | 25×1 single 12-gon; 25×1 single 14-gon; 15×1 single 10-gon; 10×1 single 16-gon; 10×1 single 15-gon; 10×1 single 13-gon; 10×1 single 18-gon |
| 77 | paragyrate diminished rhombicosidodecahedron | 10 | 5 | axis/plane | **non-heart** | 105 | 30×1 single 14-gon; 25×1 single 12-gon; 10×1 single 18-gon; 10×1 single 13-gon; 10×1 single 11-gon; 10×1 single 15-gon; 10×1 single 16-gon |
| 78 | metagyrate diminished rhombicosidodecahedron | 2 | 1 | axis/plane | **non-heart** | 105 | 25×1 single 14-gon; 18×1 single 12-gon; 18×1 single 13-gon; 16×1 single 16-gon; 9×1 single 18-gon; 9×1 single 10-gon; 8×1 single 15-gon; 2×1 single 11-gon |
| 79 | bigyrate diminished rhombicosidodecahedron | 2 | 1 | axis/plane | **non-heart** | 105 | 26×1 single 14-gon; 20×1 single 13-gon; 18×1 single 16-gon; 13×1 single 12-gon; 10×1 single 15-gon; 10×1 single 18-gon; 6×1 single 10-gon; 2×1 single 11-gon |
| 80 | parabidiminished rhombicosidodecahedron | 20 | 5 | point | **heart** | 45 | 15×2 full 12-gon; 10×2 full 16-gon; 10×2 full 10-gon; 10×2 full 8-gon |
| 81 | metabidiminished rhombicosidodecahedron | 4 | 2 | axis/plane | **inherited heart** | 88 | 24×1 single 10-gon; 16×1 single 12-gon; 12×1 single 13-gon; 12×1 single 11-gon; 8×1 single 15-gon; 6×1 single 8-gon; 4×1 single 14-gon; 4×1 single 16-gon; 2×2 shared 12-gon |
| 82 | gyrate bidiminished rhombicosidodecahedron | 2 | 1 | axis/plane | **inherited heart** | 88 | 16×1 single 10-gon; 14×1 single 13-gon; 14×1 single 11-gon; 14×1 single 14-gon; 13×1 single 12-gon; 4×1 single 15-gon; 4×1 single 16-gon; 4×1 single 9-gon; 3×1 single 8-gon; 2×2 shared 13-gon |
| 83 | tridiminished rhombicosidodecahedron | 6 | 3 | axis/plane | **non-heart** | 75 | 39×1 single 10-gon; 12×1 single 8-gon; 9×1 single 12-gon; 6×1 single 11-gon; 6×1 single 13-gon; 3×1 single 6-gon |
| 84 | snub disphenoid | 8 | 2 | point | **inherited heart** | 14 | 8×1 single 6-gon; 4×1 single 5-gon; 2×3 shared 5-gon M |
| 85 | snub square antiprism | 16 | 4 | point | **inherited heart** | 36 | 24×1 single 10-gon; 8×1 single 11-gon; 4×2 shared 6-gon M |
| 86 | sphenocorona | 4 | 2 | axis/plane | **inherited heart** | 20 | 8×1 single 7-gon; 8×1 single 6-gon; 2×1 single 8-gon; 1×3 shared 5-gon M; 1×1 single 5-gon M |
| 87 | augmented sphenocorona | 2 | 1 | axis/plane | **non-heart** | 26 | 10×1 single 8-gon; 9×1 single 7-gon; 4×1 single 9-gon; 2×1 single 6-gon; 1×1 single 6-gon M |
| 88 | sphenomegacorona | 4 | 2 | axis/plane | **inherited heart** | 24 | 10×1 single 8-gon; 4×1 single 7-gon; 4×1 single 9-gon; 4×1 single 6-gon; 1×5 shared 7-gon M; 1×1 single 5-gon M |
| 89 | hebesphenomegacorona | 4 | 2 | axis/plane | **inherited heart** | 32 | 16×1 single 9-gon; 12×1 single 8-gon; 2×1 single 10-gon; 1×2 shared 7-gon M; 1×1 single 6-gon M |
| 90 | disphenocingulum | 8 | 2 | point | **inherited heart** | 34 | 20×1 single 9-gon; 12×1 single 11-gon; 2×3 shared 7-gon M |
| 91 | bilunabirotunda | 8 | 3 | point | **heart** | 9 | 6×2 full 6-gon; 2×6 full 6-gon; 1×2 full 8-gon M |
| 92 | triangular hebesphenorotunda | 6 | 3 | axis/plane | **non-heart** | 36 | 12×1 single 8-gon; 12×1 single 10-gon; 6×1 single 7-gon; 6×1 single 9-gon |
