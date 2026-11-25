# The Aequi of the five cubes: the icosahedral frame with the cube in its five placements (25 November 2026)

DICTO · dictospheres.com · study 2026-11-25-aequi-five-cubes · with Claude (Anthropic).

**Verdict: 11 481 new orbit sets searched (14 group classes of Ih; caps below), every one with exactly one fair die (a theorem here,
by Corollary B1, and found by the search). They make 10 768 distinct Aequi (18 face-transitive polyhedra set aside). 8 of them are
congruent to dice of the 9490 (prisms whose directions occur in both frames); none to the 1232 or the 4404. So 10 760 are new,
and all 10 760 are rigorously certified** (Krawczyk in ball arithmetic: 10 745 on a box of constant type, 15 on a split box;
Newton-refined depths within 8.0e-76 of the true fair depths (enclosures in data/certify.jsonl.gz); structural corners exact, 0 failures). Not numbered or named here
(a later batch).

| full group | order | m=2 | m=3 | m=4 | m=5 | m=6 | m=7 | m=8 | m=9 | m=10 | m=11 | new |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ih | 120 | 3 | 3 | 1 |  |  |  |  |  |  |  | 7 |
| Th | 24 | 13 | 35 | 54 | 48 | 25 | 7 |  |  |  |  | 182 |
| D5d | 20 | 36 | 130 | 294 | 441 | 453 | 328 | 164 | 53 | 11 |  | 1 910 |
| D3d | 12 | 69 | 370 | 1 239 |  |  |  |  |  |  |  | 1 678 |
| T | 12 | 18 | 78 | 204 | 354 | 430 | 374 | 232 | 100 | 28 | 4 | 1 822 |
| D5 | 10 | 24 | 127 |  |  |  |  |  |  |  |  | 151 |
| S10 | 10 | 18 | 92 |  |  |  |  |  |  |  |  | 110 |
| D2h | 8 | 37 | 335 |  |  |  |  |  |  |  |  | 372 |
| D3 | 6 | 71 | 619 |  |  |  |  |  |  |  |  | 690 |
| S6 | 6 | 43 | 417 |  |  |  |  |  |  |  |  | 460 |
| C2h | 4 | 161 | 2 334 |  |  |  |  |  |  |  |  | 2 495 |
| D2 | 4 | 50 | 624 |  |  |  |  |  |  |  |  | 674 |
| Ci | 2 |  | 209 |  |  |  |  |  |  |  |  | 209 |
| all | | 543 | 5 373 | 1 792 | 843 | 908 | 709 | 396 | 153 | 39 | 4 | **10 760** |

Every die is counted once, under its full symmetry group, with m = its number of face orbits under that group. Chiral dice
(two hands, counted once): T 1 822, D3 690, D2 674, D5 151. The caps (below) bound m for the groups of order 10 or less, so
the columns above m = 3 or 4 are complete only for Ih, I, Th, T and D5d (and D3d to m = 4). I gives no die of its own: its
orbits on the 122 directions are those of Ih (as with one cube placement, study 2026-11-19).

## Question

DICTO: the Aequi mix icosahedra turned together; have all such combinations been mapped? The cube frame with the two
icosahedron placements is done (studies 2026-11-19-aequi-complete, 2026-11-20-aequi-two-placements,
2026-11-24-aequi-certify-extend). This study does the mirror case: the icosahedral frame, in which the cube (and the
octahedron) sits in **five placements**, the compound of five cubes inscribed in the dodecahedron.

## Directions, exactly (scripts/groups.py, logs/groups.log)

Icosahedron placement A of the earlier studies: vertices (0, ±φ, ±1) cyclic. Its dual dodecahedron has the 20 vertices
(±1, ±1, ±1) and (0, ±1/φ, ±φ) cyclic. The 60 face diagonals of the dodecahedron (length 2) are exactly the 60 edges of
the five inscribed cubes, 12 per cube (checked exactly in Z[φ]). Cube 0 is the coordinate cube; cube k is cube 0 turned
by k fifths of a turn about the vertex axis (0, φ, 1).

| directions of cube k | number | where they lie |
|---|---|---|
| C6_k: face normals | 6 (3 axes) | icosahedral 2-fold axes. The five cubes share out all 15 two-fold axes, 3 each: C6_0 ∪ … ∪ C6_4 = RT30 = C6 + RT24 |
| O8_k: body diagonals | 8 (4 axes) | icosahedral 3-fold axes. Each of the 10 three-fold axes lies in exactly two cubes: O8_0 ∪ … ∪ O8_4 = I20 = O8 + I12 |
| RD12_k: edge midpoints (rhombic dodecahedron face normals) | 12 | **on no icosahedral axis** (every one is at least 0.17 in sup-norm from all 62 axis directions) |

The octahedron dual to cube k has the same three sets (its vertices C6_k, face normals O8_k, edge midpoints RD12_k), so
the five octahedra add nothing beyond the five cubes.

**What is genuinely new.** C6_k and O8_k coincide with icosahedral axes (D12, I20, RT30 are already in the frame), so
the only new directions are the edge midpoints of the four cubes other than cube 0: **48 directions**. Cube 0's RD12 is
the RD12 of the earlier studies. Exactly (unnormalised, each |q|² = 8; a + bφ coordinates):

- **RDa** (24): (1, 2 − φ, 1 + φ) with all signs and cyclic orders, e.g. the midpoint of (1, 1, 1) and (0, −1/φ, φ);
- **RDb** (24): (φ, φ − 1, 2φ − 1) with all signs and cyclic orders, e.g. the midpoint of (0, 1/φ, φ) and (φ, 0, 1/φ).

RD60 = RD12 + RDa + RDb (the edge midpoints of all five cubes) is one orbit of Ih (and of I); RDa and RDb are single
orbits of Th. Union with the frame: 62 + 60 = **122 directions**, permuted by all 120 maps of Ih (asserted).

## Definition

As in the earlier studies: an Aequus has one depth per orbit of a point group G, m ≥ 2 orbits, every face present, and
every face subtends 4π/N from the centre; listed once under its full symmetry group; face-transitive polyhedra excluded.

- **Groups**: every subgroup of Ih with one fixed point, up to conjugation in Ih: Ih, I, Th, T, D5d, D5, S10, D3d, D3,
  S6, D2h, D2, C2h, Ci (14 classes; polar groups C_n, C_nv, C_s left out as before: they give no Aequus).
- **New orbit sets**: those whose RD directions come from **at least two of the five cubes**. A set inside one cube's 74
  directions (62 icosahedral + RD12_k) is an orbit set of study 2026-11-19-aequi-complete after the icosahedral rotation
  that carries cube k to cube 0, so it is not searched again. Sets are reduced by the normaliser in Ih and kept when bounded.
- **Balanced (Theorem B).** Every orbit of a group fixing only the centre sums to zero (largest computed |Σ| over all
  orbits of all 14 classes: 2.5e-16), so every orbit set is balanced. By Corollary B1 of study 2026-11-24-aequi-uniqueness
  (Theorem B with Alexandrov's uniqueness), **every new orbit set carries exactly one fair die**, with one depth per orbit
  and its centroid at the centre. The search finds it and the certification proves it; the count of dice per set is a
  theorem, not an observation.

## Method

The pipeline of studies 2026-11-19-aequi-complete, 2026-11-20-aequi-two-placements and 2026-11-24-aequi-certify-extend,
with their scripts copied and changed only where marked "study 2026-11-25" (scripts/):

1. **Directions and groups** (groups.py, logs/groups.log): the 122 directions; Ih and its 164 subgroups; exact Z[φ] checks
   (cube edges, |q|² = 8, RD60 one Ih orbit, RDa and RDb Th orbits, RD60 off every icosahedral axis).
2. **Orbit sets** (classes.py, logs/classes.log, data/classes.json): the 14 classes with one fixed point; orbits; new
   bounded sets reduced by the normaliser in Ih; the vector-sum check.
3. **Search** (solve.py unchanged, run.sh; data/raw/sol.jsonl.gz, sol-node.jsonl.gz): double precision, first orbit at
   depth 1, the m − 1 equations "mean solid angle of orbit k = 4π/N", hybrid Powell from the same start grids, box e^±1.5,
   acceptance every face within 1e-10 of 4π/N. Solid angles by Van Oosterom and Strackee's triangle formula (1983).
4. **Re-search** (recheck.py, logs/recheck.log): 2 sets had no solution from the first grid (Th: O8 + RD12 + I12 + RDa + RDb;
   T, m = 8). From 2049 Sobol starts (box widened to e^±3) each gave exactly one die, inside the old box (depth ratios
   0.985 to 1); the Jacobians are regular (smallest singular values 0.36 and 0.16). Small basins, not missing dice.
5. **Classification** (collect.py, logs/collect.log): full symmetry group (every isometry fixing the centroid that maps
   the face planes onto themselves), face orbits, repeats removed by congruence. 11 481 solutions → 10 786 distinct polyhedra:
   10 768 Aequi, 18 face-transitive (excluded), 0 with the centroid off the centre.
6. **Comparison with the catalogue** (post.py, logs/post.log, data/repeats.json, data/twins.json): against all 15 192
   catalogued dice (1232 + 4404 + the 9556 records behind the 9490). A repeat needs equal scale-free sorted plane distances
   and corner distances (to 1e-6), the same full group and corner count, and the same Gram signature of the normals (the
   invariant of study 2026-11-24-aequi-catalogue-2, copied). Repeats: 8, all from the 9490 (D6h 2, D3h 3, D2h 3: hexagonal,
   triangular and rectangular prisms whose directions lie in both frames).
7. **Certification** (certify.py, structural.py, accidental.py, summarize.py; logs/certify.log, structural.log,
   accidental.log, summarize.log; data/certify.jsonl.gz, structural.json, accidental.json): exactly the method of study
   2026-11-24-aequi-certify-extend Part 1 (exact Q(√5) normals in arb balls at 320 bits; combinatorial type constant over the
   box, by linear slacks and Balinski's theorem; Krawczyk's test K(X) ⊂ int X, tight run at r = 1e-40 and widest run;
   structural multi-plane corners proved exactly in Q(√5); split box with the hull of the side Jacobians where the fair
   point lies on a wall of type change). The only addition: for two walls in a depth space of dimension above 3 the expected
   number of regions is 4 (two distinct hyperplanes through one point cut R^n into 4 regions), where the copied script had
   no rule for n > 3.

Uniqueness half-widths (largest box with exactly one fair die, depths near 1): 1e-2: 4 097, 1e-3: 2 082, 1e-4: 4 008,
1e-5: 325, 1e-6: 229, 1e-7: 13, 1e-8: 6. Structural corners: 5 344 dice, 6 612 distinct exact checks, 0 failures. Split
box: 15 dice (D5d 10, D3d 3, D2h 1, D3 1), 11 with one wall, 4 with two walls, all pass. Symmetry reduction checked for
all 10 760 (10 with one depth per frame-map orbit).

Credit: the solid-angle formula is Van Oosterom and Strackee's (IEEE Trans. Biomed. Eng. BME-30 (1983) 125–126); fair dice by
equal solid angles 4π/N are Rawlins's construction, and the fixing of one free parameter between two kinds of face is Diaconis
and Keller's (as credited in the earlier studies); Krawczyk's operator (R. Krawczyk, 1969) in arb ball arithmetic
(F. Johansson, python-flint); uniqueness up to scale is Alexandrov's theorem; existence for balanced directions is Theorem B
of study 2026-11-24-aequi-uniqueness; the five cubes in the dodecahedron are the classical compound (Euclid's construction of
the dodecahedron on the cube; the compound of five cubes as in Coxeter's Regular Polytopes).

## Caps (stated; the convention of study 2026-11-24-aequi-certify-extend Part 2(a), raised where cheap)

| class | orbits | new sets in all | searched | m searched |
|---|---|---|---|---|
| Ih | 4 | 7 | 7 | all |
| I | 4 | 7 | 7 | all |
| Th | 8 | 190 | 190 | all |
| T | 12 | 2 014 | 2 014 | all |
| D5d | 11 | 1 916 | 1 916 | all |
| D3d | 15 | 32 249 | 1 678 | m ≤ 4 |
| S10 | 13 | 4 988 | 196 | m ≤ 3 |
| D5 | 14 | 9 020 | 220 | m ≤ 3 |
| D2h | 22 | ≥ 84 771 | 365 | m ≤ 3 |
| S6 | 21 | ≥ 198 651 | 568 | m ≤ 3 |
| D3 | 22 | ≥ 140 472 | 783 | m ≤ 3 |
| C2h | 35 | ≥ 24 450 (m ≤ 4) | 2 566 | m ≤ 3 |
| D2 | 32 | ≥ 37 241 (m ≤ 5) | 702 | m ≤ 3 |
| Ci | 61 | 269 at m = 3 | 269 | m ≤ 3 (m = 2 bounds nothing) |
| **all** | | | **11 481** | |

Every searched set gave exactly one fair die (52 (class, m) stages, plan check: searched = sets in every stage). By
Corollary B1 this is also what must happen, so the counts are exact for the sets searched. A die whose full group is a
capped class can have more orbits than the cap; those are not covered.

## Observations

- **The seven Ih dice** (RD60 = the edge midpoints of all five cubes, with icosahedral axis orbits), depths with the first orbit
  at 1: RD60 + D12 (N = 72, 110 corners, 0.97589); I20 + RD60 (N = 80, 0.98549); RT30 + RD60 (N = 90, 0.98555);
  I20 + RD60 + D12 (N = 92); RT30 + RD60 + D12 (N = 102); RT30 + I20 + RD60 (N = 110); RT30 + I20 + RD60 + D12 (N = 122,
  240 corners, every direction of this study used once). These are the only new dice with full icosahedral symmetry.
- **Twins.** 12 D3 dice here have the same sorted plane distances (to 1e-6) and corner distances as 12 S6 dice of study
  2026-11-19 (each with an orbit RD12+RDa/6 where the S6 die has RD12/6), but they are not congruent: the groups differ and the
  Gram signatures of the normals differ. Distances alone do not identify an Aequus (data/twins.json).
- **Prisms are shared between the frames**: the 8 repeats are prisms (D6h, D3h, D2h) whose few directions occur in the
  cube frame of the two-placement study as well.

## Not covered

- The capped classes above their caps (table above).
- **Icosahedra turned by a free angle about a shared axis** (the next lead below): the two-placement and five-cube cases are
  the two discrete placements that share a whole symmetry group; a free angle gives a continuous family.
- Off-axis face directions (continuous families; study 2026-11-24-aequi-certify-extend Part 2(c)).
- Closed forms: all values are certified enclosures, not closed forms.
- Not numbered or named (a later batch, as asked). Not checked against outside catalogues beyond those named in the earlier
  studies' source lists; nothing here is a priority claim.

## LEADS

1. **Icosahedra turned by a free angle θ about a shared axis** (a 5-fold, 3-fold or 2-fold axis of both): the group kept is
   the axis group (D5d, D3d, D2h and subgroups), and each θ gives a balanced set, so by Corollary B1 one fair die per θ: a
   one-parameter family per orbit set, as for the off-axis faces. Cells (group, orbit types, combinatorial type) are the
   thing to count, with certified tracking of type changes in θ. The two-placement case is θ = 90° about a 2-fold axis.
2. Raise the caps: D3d, S10, D5 complete (32 249 + 4 988 + 9 020 sets; measured cost 30–90 core-seconds per set for m ≥ 4); D2h, S6, D3 to m = 4.
3. The twins: a description of the 12 D3/S6 pairs (same distances, different normals); is there a construction that
   produces such pairs in general?
4. Two placements of the icosahedron AND five placements of the cube together (the union of the 122 directions of each
   frame): the common refinement, under the groups shared by Oh and Ih (Th, T, D2h, D2, S6, D3, C2h, Ci).
5. Catalogue numbers and names for the 10 760 (later batch, DICTO's choice of order).

## Files

scripts/: groups.py, classes.py, solve.py, run.sh, recheck.py, collect.py, exact.py (used for its geometry routines),
post.py, certify.py, structural.py, accidental.py, summarize.py, plan_check.py.
data/: classes.json, stages-*.txt, plan.json, raw/ (search records), collected.json.gz, aequi.json.gz (the 10 760 with
orbits, directions, depths), dice-new.json.gz (certification input), counts.md, repeats.json, twins.json,
certify.jsonl.gz (per die: status, uniqueness half-width, type radius, enclosure), structural.json, accidental.json.
logs/: every step.
