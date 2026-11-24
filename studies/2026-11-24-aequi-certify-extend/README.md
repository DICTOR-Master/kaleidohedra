# Certifying and extending the Aequi (24 November 2026)

DICTO · dictospheres.com · study 2026-11-24-aequi-certify-extend · with Claude (Anthropic).

**Verdict, Part 1: all 1232 Aequi are rigorously certified.** For each die, ball arithmetic proves that exactly one fair depth vector lies in an explicit box around the published depths, and that the published 60-digit depths are within 5e-60 of it. The face structure is proved constant over the box. 1229 dice pass on a box where the combinatorial type does not change; the other 3 sit exactly where the type changes, and they pass with a split box. There are no failures. **Aequus CIRT-30, T 26:** its C6 and RT24/12a faces are at equal depth to within 2.2e-78 (rigorous). The exact equality is reduced to one identity along the line d(C6) = d(RT24/12a): 2Ω(RT24/12a face) − Ω(C6 face) = 4π/30 for every depth of the I12 faces. That identity holds to 1e-93 at six points but is **not yet proved**, so "exactly equal" is not claimed. One of the other two split-box dice, Td: D12+D12′/24 + RT24+RT24′/24, is settled exactly: its depth ratio is cos 18° = √(10+2√5)/4, and it is fair because its faces project onto the 48 triangles of the cube's symmetry.

**Part 2:** (a) Both icosahedron placements under the 16 other subgroup classes of Oh with one fixed point: 6 924 orbit sets searched (all m = 2; m = 3 for groups of order ≥ 6; m = 4 for D3d), every set with exactly one fair die, giving **5 935 new Aequi, all rigorously certified**. (b) Widening the depth box to e^±3 for the seven frame groups (234 sets) found the same single die in every set, and nothing new; raising the caps (D3d and C2h with 9 orbits completed to every m; D3 and S6 at m = 5) searched 2 141 more sets, again with exactly one fair die per set, and gave **1 711 more new Aequi (336 + 1 375), all certified**. D2h (16 orbits) m = 5 is checkpointed at 1 426 of 1 455 sets. (c) the pilot of faces off the symmetry axes: along every one-parameter family tried (9 families, 5 groups) there is **exactly one fair die for every value of the parameter**, so these dice come as **continuous families**, not as isolated dice. The enumeration problem is therefore one of counting cells (group, orbit types, combinatorial type), not dice. It is defined below.

**Part 3:** none of the 1232 (nor the new dice of Part 2) appears in the catalogues checked (sources listed below). The method of fixing one free parameter between two kinds of face (fair by continuity) is credited to Diaconis and Keller. Fair dice built by setting every face's solid angle to 4π/N are credited to Rawlins.

Fairness model throughout (as in the earlier studies): every face subtends the solid angle 4π/N from the centroid. For all dice here the centroid is the centre, by symmetry: every group involved fixes only that point.

## Part 1. Certification of the 1232

The 1232 are the 149 frame-group Aequi of study 2026-11-19-aequi-complete (Ih 4, Oh 4, Td 3, Th 47, T 91) and the 1083 of study 2026-11-20-aequi-two-placements (Oh 53, O 31, Td 91, Th 168, T 740).

### Method (scripts/certify.py, accidental.py, structural.py, line504.py)

1. **Exact data.** Every face normal is an exact vector over Q(√5): one of 9 patterns, with signs and cyclic orders. It is turned into a ball vector at 320 bits (arb, python-flint).
2. **Symmetry reduction.** Each die is described by one depth per face orbit of its full group, with the first orbit at depth 1. We check that each listed orbit is one orbit of the frame maps that preserve the die's labelled face set. The frame maps are exact matrices over Q(√5), and their images are matched within a finite set of directions at least 0.1 apart. Then, for any depth vector with one depth per orbit, all faces of an orbit are congruent. So fairness is the m − 1 equations F_k = Ω(one face of orbit k) − 4π/N = 0, for k = 2..m (the sum of all Ω is 4π). Each solid angle is a sum of Van Oosterom–Strackee triangle angles, 2 atan2(det, |a||b||c| + (a·b)|c| + (a·c)|b| + (b·c)|a|), over a fan from one corner of the face.
3. **Combinatorial type over a box.** A corner is where three planes meet (solved by Cramer's rule), so its coordinates are *linear* in the depths. The slack of every other plane at every corner is therefore a linear function of the depths, and its minimum over a box is exact: centre value − r·Σ|coefficients|. We certify that every slack stays positive over the box. Each face's corners are put in order from the edge graph, not from angles. Each corner must close up into one cycle of edges, with at most two corners per pair of planes. This makes the type constant over the box, by the following argument. Each listed corner remains a vertex. Each of its edges, which depend only on the planes through it, leads to a listed neighbour. So the listed graph is a union of components of the polytope's graph. That graph is connected (Balinski), so the listed corners and faces are all of them.
4. **Corners with more than three planes.** 189 dice have such corners at their fair depths.
   - **Structural corners:** in 188 dice the extra planes pass through the corner for *every* depth vector with that orbit structure. This is proved exactly in Q(√5) by scripts/structural.py. Each offset coefficient Σ|q_i|(q_f·w_i)/det − [orbit]|q_f| is split by the radical |q| ∈ {1, √2, √3, √(φ+2)}, and every part is zero. There were 1662 distinct checks and 0 failures. Such a corner is one vertex of the type, and the argument of step 3 holds with its cone of edges. The cone depends only on the normals.
   - **Accidental corners:** in 3 dice the extra planes meet in one point only on a hyperplane h = 0 of depth space, and the fair point lies on that hyperplane to 60 digits. These are treated in step 6.
5. **Krawczyk's test.** Take x̃ = the 60-digit depths (exact binary midpoints) and the box X = x̃ ± r. Let J(X) enclose the Jacobian of F over X, computed by forward differentiation in ball arithmetic. Let C be the inverse of mid J. If K = x̃ − C F(x̃) + (I − C J(X))(X − x̃) lies inside the interior of X, then F has exactly one zero in X. Two runs:
   - a *tight* run at r = 1e-40. Every die passes, with |K − x̃| ≤ 5.0e-60, so the published 60-digit depths are within 5e-60 of the true fair depths (largest |F(x̃)| = 8.2e-59);
   - a *wide* run: the largest r in {1e-2, 3.2e-3, 1e-3, …, 1e-12} below the type radius for which the test passes. This is the uniqueness half-width reported for each die (relative to depths near 1).
6. **Split box for the 3 accidental dice** (scripts/accidental.py). The types T+ (h > 0) and T− (h < 0) are read at the 60-digit point moved 1e-6 to either side. Each is certified on its closed half-box: every slack is positive except slacks that are exact multiples of h, which vanish only on h = 0. A fan triangle that shrinks to a segment on h = 0 is allowed while its denominator is positive. F is continuous and piecewise smooth, so F(x) − F(y) ∈ hull(J+(X), J−(X))(x − y), and Krawczyk's test with the hull proves exactly one zero in X. The two Jacobians agree to 1e-6 (F is C¹ across h = 0).

### Results (data/certify-summary.md, data/certify-table.csv: every die with its name where it has one, uniqueness half-width, type radius, multi-plane corners)

| study | group | dice | certified | split box | failed | smallest uniqueness half-width | median |
|---|---|---|---|---|---|---|---|
| 2026-11-19 | Ih | 4 | 4 | 0 | 0 | 3.2e-04 | 1.0e-02 |
| 2026-11-19 | Oh | 4 | 4 | 0 | 0 | 3.2e-03 | 1.0e-02 |
| 2026-11-19 | Td | 3 | 3 | 0 | 0 | 3.2e-03 | 1.0e-02 |
| 2026-11-19 | Th | 47 | 47 | 0 | 0 | 1.0e-05 | 1.0e-03 |
| 2026-11-19 | T | 91 | 90 | 1 | 0 | 1.0e-05 | 3.2e-04 |
| 2026-11-20 | Oh | 53 | 53 | 0 | 0 | 1.0e-05 | 3.2e-04 |
| 2026-11-20 | O | 31 | 31 | 0 | 0 | 3.2e-06 | 3.2e-04 |
| 2026-11-20 | Td | 91 | 89 | 2 | 0 | 1.0e-05 | 3.2e-04 |
| 2026-11-20 | Th | 168 | 168 | 0 | 0 | 1.0e-06 | 1.0e-04 |
| 2026-11-20 | T | 740 | 740 | 0 | 0 | 3.2e-08 | 1.0e-04 |
| all | | 1232 | 1229 | 3 | 0 | | |

Uniqueness half-width (nearest power of ten): 1e-2: 89, 1e-3: 104, 1e-4: 952, 1e-5: 56, 1e-6: 29, 1e-7: 1, 1e-8: 1
Dice with corners where four or more planes meet: 189 (structural, proved exactly: 188 dice, 1662 distinct checks, 0 failures; accidental: 3)

- The largest uniqueness boxes are ±1e-2 (89 dice); the smallest is ±3.2e-8 (one T die of the two-placement study). The smallest type radius is 3.8e-6.
- Every die's face structure (corners, faces, sides) is certified constant over its box. In particular, the corner counts recorded in the earlier studies are confirmed for all 1232.

### The three dice on a hyperplane of type change

| die | hyperplane h = 0 | uniqueness box | where the fair point lies |
|---|---|---|---|
| Aequus CIRT-30, T 26: T: C6 + I12 + RT24/12 (study 2026-11-19 row 504) | d(C6) = d(RT24/12a) | ±3.2e-3 | \|h\| < 2.2e-78 (rigorous) |
| Td: D12+D12′/24 + RT24+RT24′/24 (two-placement row 95; N = 48, 26 corners) | d(RT) = cos 18° · d(D) | ±1e-2 | **exactly on h = 0** (proof below) |
| Td: O8/4a + O8/4b + D12+D12′/24 + RT24+RT24′/24 (two-placement row 124; N = 56) | d(RT) = cos 18° · d(D) | ±3.2e-4 | \|h\| < 2.3e-77 (rigorous) |

**Row 95, exact.** Take the depth ratio d(RT)/d(D) = cos 18° = √(10+2√5)/4. Exact arithmetic (sympy, structural.py) shows three things. All 26 corners lie on the 26 cube axes (6 C6, 8 O8, 12 RD12). Every one of the 48 triangular faces has one corner on each kind of axis. Those three axes are mutually nearest (angles 54.74°, 45°, 35.26°). So each face projects from the centre onto an Oh fundamental triangle, with angles π/2, π/3, π/4 and area π/12 = 4π/48. The die is fair exactly at this ratio, and by the certified uniqueness box it is the catalogue die. Its projection has the full symmetry Oh, while the solid has only Td.

**Aequus CIRT-30, T 26.** scripts/line504.py:
- On the line d(C6) = d(RT24/12a) = 1, the four-plane corners are structural, and Krawczyk in the one variable t = d(I12) proves exactly one t* in ±1e-2 with Ω(I12 face) = 4π/30. Its value is t* = 1.014935802739769241603950729393898891237 ± 5e-40.
- Along the line, 2Ω(RT) − Ω(C6) − 4π/30 evaluates to [± 1.7e-93] at t = 1, 1.005, 1.01, 1.02, 1.03 and to [± 1e-38] at t*. If this identity holds for every t near t*, then at t* all three orbits are fair (from 6Ω_C + 12Ω_R + 12Ω_I = 4π), so the line carries a fair die. By the certified uniqueness in the 2-D box, that die is CIRT-30, and its C6 and RT24/12a depths are **exactly** equal.
- **Status:** the identity is observed, not proved, so exact equality is **not claimed**. What is proved is |d(C6) − d(RT24/12a)| < 2.2e-78.
- **Likely mechanism (not a proof):** the I12 faces come in threes around the O8 axes. Each Ih mirror through such an axis carries the three I12 directions to themselves and swaps the nearby C6 and RT24/12a directions (all those within 69° of the axis; the I12 faces reach 57.8°). This suggests that the I12 faces take equal area from C6 and from RT24/12a as t varies. Writing the proof is LEAD 1. (Study 2026-11-24-aequi-vacuus-scutoids is running an independent exact algebraic certificate for this die. Nothing here depends on it.)

**Row 124:** it has the same hyperplane as row 95, but its projection has only the symmetry Td, so the mechanism there is not yet identified (LEAD 2).

## Part 2. Extensions

### (a) Both icosahedron placements under the other subgroups of Oh

**Search (scripts/classes2a.py, solve.py, run2a.sh, plan_check.py; logs/classes2a.log, logs/job-aequi-2a.log; 22 cores on a compute host).** We took every subgroup of Oh with one fixed point that does not contain T (orbit sets of Oh, O, Td, Th, T were covered by study 2026-11-20-aequi-two-placements), up to conjugation in Oh: D4h, D3d, C4h, D4, D2d (two classes), D2h (two classes), S6, D3, S4, C2h (two classes), D2 (two classes), Ci. These are 16 classes, acting on all 122 directions of both placements. Groups with a fixed line or plane (C_n, C_nv, C_s, C_1) are left out: in study 2026-11-19-aequi-complete their fair solids never had the centroid at the centre. We searched every orbit set using both placements (some orbit with a D12/I12/RT24 direction and some with a D12′/I12′/RT24′ direction), reduced by the normaliser in Oh and bounded. Solver, start grids and box (e^±1.5) are those of the earlier studies.

**Coverage (what is complete, what is capped).**
- m = 2 for every class: 1 328 sets. Ci has none, since two antipodal pairs do not bound a solid.
- m = 3 for every class of order ≥ 6: D4h 350, D3d 276, C4h 527, D4 425, D2d 470 + 786, D2h 668 + 207, S6 403, D3 774.
- m = 4 for D3d: 710 sets.
- In all, 6 924 sets, every one searched (plan_check: searched = sets for all 26 stages). **Every set gave exactly one fair die** (0 sets with none, 0 with two or more).
- Not searched (the caps of this part): m = 3 for S4, C2h, D2; m ≥ 4 for all classes except D3d; m ≥ 5 for D3d. The class enumeration gives the counts: D4h has 16 333 sets in all (m up to 14), D3d 8 151 (m up to 13), and the low groups have many thousands.

**Classification (collect.py, post2a.py; logs/collect2a.log, logs/post2a.log).**
- The 6 924 solutions are 5 977 distinct solids. Of these, 35 are face-transitive (excluded), none has its centroid off the centre, and **5 942 are Aequi**.
- 7 of them have the full symmetry Oh. Their face sets are unions of T orbits, so they are repeats of the two-placement study.
- The other 5 935 have a full group not containing T. None is congruent to any of the 4553 of study 2026-11-19-aequi-complete (checked by scale-free plane distances and corner distances, mirror images included, against every die of the same N, group and corner count).
- So there are **5 935 new Aequi**, by full symmetry group and number of face orbits m:

| group | m=2 | m=3 | m=4 | total |
|---|---|---|---|---|
| D6h | 1 | 1 |  | 2 |
| D4h | 89 | 352 |  | 441 |
| D3h | 1 | 2 |  | 3 |
| D3d | 64 | 273 | 704 | 1041 |
| D2d | 156 | 1051 |  | 1207 |
| D4 | 39 | 240 |  | 279 |
| D2h | 87 | 775 |  | 862 |
| C4h | 50 | 401 |  | 451 |
| D3 | 101 | 740 |  | 841 |
| S6 | 28 | 364 |  | 392 |
| C2h | 243 |  |  | 243 |
| D2 | 96 |  |  | 96 |
| S4 | 77 |  |  | 77 |
| all | 1032 | 4199 | 704 | 5935 |

D6h and D3h are prisms, as in the earlier study (symmetry outside the frame maps).

**Certification (certify.py with Newton refinement from the double-precision depths; accidental.py; structural.py; summarize2a.py; logs/certify2a.log, accidental2a.log, structural2a.log, summarize2a.log).** **All 5 935 are rigorously certified**, with the same method as Part 1:
- 5 924 on a box of constant type. For 6 of these (D4h dice whose full group is a turned copy of D4h, not made of frame maps) the system was certified with one depth per frame-map orbit, a larger system that contains the die.
- 11 on a split box. 5 have one wall, 5 have two walls (D4h, 4 regions each), and one has ten walls (D3d: D12+D12′/12 + RT24+RT24′/12a + RT24+RT24′/12b + RT24+RT24′/12c, 36 regions; the count of regions is checked by Euler's formula on the sphere).
- Tight boxes place the fair depths within 5.2e-76 of the refined values.
- Uniqueness half-widths: 1e-2: 3574, 1e-3: 1501, 1e-4: 838, 1e-5: 14, 1e-6: 6, 1e-7: 1, 1e-8: 1.
- Structural corners: 3983 dice, 8318 exact checks, 0 failures.

**Dice on walls with simple ratios.** These are the same phenomenon as row 95 of Part 1: the fair point lies on the wall to 1e-75, and their exact status is open, except where a proof as for row 95 applies (LEAD 3).
- D2h: D12+D12′/8 + RT24+RT24′/8 (two dice): d(RT) = cos 18° d(D).
- D2h: I12+I12′/8 + RT24+RT24′/8: d(RT) = cos 30° d(I).
- S6: D12/6 + D12′/6 and S6: I12/6 + I12′/6: the two orbits at equal depth, so all 12 faces are at one depth.

**Data.** data/collected2a.json.gz (all solids), data/aequi2a.json.gz (the 5 935 with orbits, depths, corners, groups), data/dice2a-new.json (input to certification), data/certify2a.jsonl.gz, data/accidental2a.json, data/structural2a.json, data/raw/sol-2a.jsonl.gz.

### (b) Caps raised and the depth box widened

**Wider depth box (scripts/solve_wide.py, run2b.sh, compare2b.py; data/raw/sol-2b.jsonl, data/compare2b.json; a small compute host).** Every orbit set of the seven frame groups (one placement, as in study 2026-11-19-aequi-complete: 234 sets, m = 2 to 8) was searched again with the depth box widened from e^±1.5 to e^±3 (depth ratios 0.050 to 20.1) and denser starts: 41 starts for m = 2; 11², 7³, 5⁴ grids for m = 3 to 5; 512 Sobol points for m ≥ 6 (about 75 000 starts in all). Result: **every set again has exactly one fair die, the same one as before** (depths agree to 1e-6 in all 234 sets; 0 sets with none, 0 with two or more). All depth ratios lie in 0.888 to 1.193, so the old box was never close to binding for these groups. This is still a search inside a box, not a proof of "one die per set".

**Raised caps (scripts/solve1.py = the study-1 solver unchanged, run2b.sh with SOLVER=solve1.py, collect1.py, post2a.py with prefix 2caps; logs/job-aequi-2capsb.log, collect2caps.log, post2caps.log, certify2caps.log, structural2caps.log).** One placement, study-1 box e^±1.5. The run started on the small compute host. It was stopped after 122 of the 126 D3d m = 5 sets because that host was too slow for the time before the power cut, and it was resumed from the same file on the larger host.

*Batch 1: D3d (9 orbits) and C2h (9 orbits), completed to every m.* These had been capped at m ≤ 4. Now m = 5..9 are searched: D3d 126 + 84 + 36 + 9 + 1 sets, C2h 76 + 52 + 24 + 7 + 1 sets (416 sets). **Every set has exactly one fair die.** The 416 solutions are 396 distinct Aequi:
- 8 have a group containing T (Ih 4, Oh 4) and were met before;
- 52 are congruent to dice of study 2026-11-19-aequi-complete;
- **336 are new**, all rigorously certified (Krawczyk on constant-type boxes; structural corners in 107 dice, 236 exact checks, 0 failures; uniqueness half-widths 1e-2: 20, 1e-3: 94, 1e-4: 209, 1e-5: 12, 1e-6: 1).

| group | m=5 | m=6 | m=7 | m=8 | total |
|---|---|---|---|---|---|
| D3d | 125 | 83 | 35 | 9 | 252 |
| C2h | 45 | 29 | 9 | 1 | 84 |
| all | 170 | 112 | 44 | 10 | 336 |

So the classes D3d (9 orbits) and C2h (9 orbits) are now complete for every m, like the classes that study 2026-11-19 completed.

*Batch 2: D3 (12 orbits) and S6 (13 orbits) at m = 5.* These had been capped at m ≤ 4. 438 D3 sets and 1 287 S6 sets were searched, and **every set has exactly one fair die**. The 1 725 solutions are 1 489 distinct Aequi:
- 6 have a group containing T (Th 5, Oh 1) and were met before;
- 108 are congruent to dice of study 2026-11-19-aequi-complete;
- **1 375 are new**: S6 1000, D3 354, D3d 21, all with m = 5 under their full group. All are rigorously certified (Krawczyk on constant-type boxes, no multi-plane corners; uniqueness half-widths 1e-2: 32, 1e-3: 590, 1e-4: 731, 1e-5: 14, 1e-6: 7, 1e-8: 1).

*Batch 3 (resumed after the power cut, 24 Nov afternoon): D2h (16 orbits) m = 5 and D3 (12 orbits) m = 6, now complete.* All 1 455 D2h sets and all 508 D3 sets were searched (plan_check2: searched = sets), and **every set has exactly one fair die**. collect1.py, post2a.py (prefix 2caps3), certify.py and structural.py (logs/collect2caps3.log, post2caps3.log, certify2caps3.log, structural2caps3.log): 1 963 solutions, 1 962 distinct solids, 1 961 Aequi (one is face-transitive). 1 has a group containing T (Ih, met before), 50 are congruent to dice of study 2026-11-19-aequi-complete, and **1 910 are new** (D2h 1 449, D3 416, D3d 45). **All 1 910 are rigorously certified** (status certified 1 910 of 1 910; symmetry and face-graph checks pass for all). Structural corners: 1 116 dice, 824 distinct exact checks, 0 failures. Data: data/collected2caps3.json.gz, aequi2caps3.json.gz, dice2caps3-new.json, certify2caps3.jsonl.gz, structural2caps3.json, counts2caps3.md.

New Aequi in Part 2(b) caps, all three batches: 1 711 + 1 910 = 3 621. With Part 2(a): 5 935 + 3 621 = 9 556 new certified Aequi.

Data: data/counts2caps.md, counts2caps2.md, aequi2caps*.json.gz, certify2caps*.jsonl.gz, structural2caps*.json, collected2caps*.json.gz, raw/sol-2caps*.jsonl.gz.

### (c) Pilot: faces off the symmetry axes (scripts/pilot2c.py, data/pilot2c.json, logs/pilot2c.log)

**Family.** A direction v(s) = normalise((1 − s)a + s b) moves along an arc of a mirror plane of G, from axis a to axis b. Its G-orbit (|G|/2 directions) joins one axis orbit at depth 1. There is one fairness equation in one unknown depth, and all roots with depth ratio in [e^−1.5, e^1.5] are found by sign changes on 121 points, then bisection. s runs over 59 values in (0, 1). Double precision: this is a pilot only.

| family | s ranges with one combinatorial type: corners, full group, sides (axis face, moving face) |
|---|---|
| Oh: C6 + 24 on the arc C6 → RD12 (N = 30) | 0.02–0.98: 32, Oh, (4, 4) |
| Oh: C6 + 24 on the arc C6 → O8 (N = 30) | 0.02–0.98: 44, Oh, (4, 5) |
| Oh: O8 + 24 on the arc O8 → RD12 (N = 32) | 0.02–0.98: 30, Oh, (3, 4) |
| Oh: RD12 + 24 on the arc C6 → O8 (N = 36) | 0.02–0.22: 62, (8, 4) · 0.23–0.77: 62, (4, 6) · 0.78–0.98: 62, (8, 4) |
| Td: O8/4 + 12 on the arc O8/4 → C6 (N = 16) | 0.02–0.98: 16, Td, (3, 4) |
| Td: C6 + 12 on the arc (1,1,1) → (1,1,−2) (N = 18) | five types; Oh at s = 1/3 (the arc passes RD12); at s = 2/3 it passes O8 |
| Th: C6 + 12 pyritohedral (1, s′, 0) (N = 18) | 0.02–0.98: 32, Th, (4, 6); Oh at the midpoint (RD12); passes Aequus CD-18, Th 1 where the moving direction is D12 |
| Th: O8 + 12 pyritohedral (N = 20) | 24 / 36 / 30 (Oh, midpoint) / 36 / 24 corners |
| Ih: D12 + 60 on the arc D12 → RT30 (N = 72) | 0.02–0.75: 110 corners, (5, 5) · 0.77–0.98: 140 corners, (10, 5) |

**What the pilot shows.**
- (1) Every s gave **exactly one** fair depth in the range: 531 values, 0 with none and 0 with two or more. So each family is a continuous curve of fair dice, and its symmetry is the group G except at isolated s.
- (2) The combinatorial type is constant on intervals and changes at isolated s, where a corner of four or more planes forms.
- (3) Where the moving direction passes a frame axis, the family passes through a catalogue die or a die with larger symmetry (Oh at the midpoints, CD-18 on the pyritohedral arc).
- (4) Counting explains (1): m orbits give m − 1 equations, and the free parameters are the m − 1 depth ratios plus the position parameters of the off-axis orbits (1 for an orbit on a mirror arc, 2 for a general orbit). So the fair dice with p position parameters form a p-dimensional set (generically).

**The enumeration problem, defined (for DICTO).** Fix a finite point group G with one fixed point. An *orbit type* is a choice of k orbits of directions, each either an axis orbit (fixed), a mirror orbit (1 parameter on a mirror arc), or a general orbit (2 parameters), together with the arcs or regions they range over. A *fair cell* is a connected set of fair dice of one orbit type with constant combinatorial type and constant full symmetry group. The questions are:
- (E1) for each G and each orbit type with p parameters, list the fair cells, with their dimension (p generically), their boundaries (type changes, symmetry jumps, faces vanishing), and the catalogue dice on their closures;
- (E2) the *combinatorially distinct* fair dice: the number of combinatorial types (with symmetry) met by the cells, which is finite for bounded face count N.

The axis-only catalogue (the 1232 and the 4553) is the p = 0 layer. The pilot shows 1 to 5 types per one-parameter family. A full enumeration is a search over (G, orbit types, N ≤ bound) that tracks type changes along each family, as done here for nine families.

## Part 3. Prior art (sources checked)

- **Diaconis and Keller, "Fair dice", Amer. Math. Monthly 96 (1989) 337–339.** Fair by symmetry means the symmetry group acts transitively on the faces (isohedra). They also give fair dice that are not face-transitive, obtained by adjusting one parameter between two kinds of face (for example a prism or a "coin" of the right thickness); in our memory they call this fair by continuity, but the full text was not re-read today. None of the 1232 is face-transitive (one-orbit solids were excluded by definition). The idea of tuning depths between face orbits is theirs; our dice are new instances of it, under the solid-angle model.
- **Rawlins, US patent 11033806** (methods for mathematically fair N-sided dice): sets every face's solid angle to 4π/N and solves for proportions when there are several face shapes (for example a 7-sided die with three shapes). This is the same fairness model; its examples are prisms and bipyramid-type dice, not frame-axis polyhedra.
- **Isohedra catalogues** (MathWorld "Isohedron" and "Fair Die"; Wikipedia "Isohedral figure"; Sherman's loki3 fair-dice page, which also lists polyisohedra and dice built from equal sets of faces): face-transitive solids only, or equal-face constructions. None of ours appears.
- Checked on 20 Nov for the paper outline (papers/2026-11-20-aequi/outline.md) and still valid: McCooey's polyhedron catalogue, Michon's Numericana page on dice, Taniguchi and Uehara arXiv:1810.12108, Irving and Patel. None has these dice.
- **Known among ours:** the prisms of study 2026-11-19 (outside the 1232) are known in idea (Diaconis–Keller; Goucher's fair triangular prism). The twelve two-orbit dice of Equanimity (paper #111 draft) are DICTO's earlier work and are included in the 149. **No die of the 1232 was found in any earlier catalogue checked.** This is a search record, not a priority claim.
- Methods credited at their point of use: Van Oosterom and Strackee (IEEE Trans. Biomed. Eng. BME-30 (1983) 125–126) for solid angles; Krawczyk's operator (Krawczyk 1969; Moore) for the existence and uniqueness tests; arb ball arithmetic (Johansson) through python-flint; Balinski's theorem (a 3-polytope's graph is 3-connected) for the type argument.

## LEADS

1. A written proof of the CIRT-30 identity 2Ω(RT24/12a) − Ω(C6) = 4π/30 along d(C6) = d(RT24/12a). The candidate proof is the mirror through the O8 axes swapping C6 and RT24/12a near each triple of I12 faces, plus the split of the twelve missing RT24/12b cells between C6 and RT24/12a. This would turn |h| < 2.2e-78 into equality.
2. Row 124 (Td, N = 56): the same hyperplane d(RT) = cos 18° d(D) as row 95, but no projection symmetry. Find the mechanism.
3. "Fair by projection": a die whose central projection has more symmetry than the solid (row 95: Td solid, Oh projection). Search the catalogue for more.
4. Off-axis families: run E1 for all mirror orbits of Oh, Td, Th, Ih (one parameter), then general orbits (two parameters), with certified tracking of type changes.
5. Remaining caps: both placements at m ≥ 4 (m ≥ 5 for D3d) under the subgroups of Oh, and m = 3 for S4, C2h, D2; one placement: D2 (20 orbits) and C2h (23 orbits) above m = 4 and m = 3, Ci above m = 3. Every set searched so far (6 924 + 416 + 1 725 + 234 re-searched) has exactly one fair die. A proof of "one fair die per orbit set" for groups with one fixed point would make all these counts exact.
6. The new dice of Part 2 (5 935 + 336 + 1 375) are certified but not yet drawn: renders and Vacuus sheets, as in the earlier studies.

## Questions for DICTO

1. Off-axis dice come in continuous families. Should a family count as one Aequus (one name per fair cell), or should only special members get names (where the family meets an axis, or where its symmetry rises)?
2. Row 95 (Td: D12+D12′/24 + RT24+RT24′/24, N = 48) is fair because its projection is the disdyakis dodecahedron. Should it get a name now? It is among the 1083 waiting for numbers.
3. Do the new Aequi of Part 2 (both placements under the subgroups of Oh; dice above the old caps) go into the numbered catalogue, or stay a dataset below the frame groups like the 4553?

## Files

- scripts/:
  - certify.py (Part 1 certifier), accidental.py (split box), structural.py (exact zero proofs; row 95), line504.py (CIRT-30 on its line), summarize1.py;
  - classes2a.py, solve.py, run2a.sh, plan_check.py, collect.py, exact.py, post2a.py (Part 2a; solve/collect/exact are copies from study 2026-11-20-aequi-two-placements);
  - solve_wide.py, run2b.sh, plan_check2.py, compare2b.py, solve1.py, collect1.py (Part 2b);
  - pilot2c.py (Part 2c);
  - groups.py (122 directions, copy).
- data/:
  - Part 1: certify-pass1.jsonl, certify-table.csv, certify-summary.md, accidental.json, structural.json;
  - Part 2: classes2a.json, plan2a-stages.txt, raw/ (double-precision solutions), counts2a.md, aequi2a.json.gz, dice2a-new.json, certify2a.jsonl.gz, classes-study1.json, plan2b-stages.txt, compare2b.json, plan2caps*-stages.txt, counts2caps*.md, aequi2caps*.json.gz, certify2caps*.jsonl.gz, structural2caps*.json, pilot2c.json.
- logs/: certify, accidental, structural, line504, classes2a, pilot2c, and the Part 2 job logs.

Software: python-flint 0.9.0 (arb), scipy, sympy, mpmath.
- 2026-11-24 compute job aequi-2b finished OK; read and recorded in its study README (closed by coordinator).

## Decisions (24 Nov; DICTO: "make decisions instead of questions")
1. Off-axis families: one Aequus per fair cell (one name per family); special members (meeting an axis, or with higher symmetry) are listed under it, not named apart.
2. Row 95 is named in the next numbering batch.
3. The new Aequi of Part 2 enter the numbered catalogue from no. 1233, in one ordered batch after the D2h/D3 resume ends: the three permutahedron duals first (1233-1235), then by group order and m.
