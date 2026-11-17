# Independent exact cross-check of Paper #110, "Walls of Silence" (for Version 2)

Computation with Claude (Anthropic).

All code in `scripts/` was written from scratch for this check. No script of the
paper or of its studies was opened, imported or copied. The definitions and claims
come from the paper's text only. The studies' outputs were compared only after these
logs were written (see the end of this file).

## Method

* **Exact arithmetic.** Every number lies in Z[φ], stored as an integer pair (a, b) = a + bφ.
  Products, dot products, 4×4 determinants and equality tests are exact integer
  arithmetic. Signs are decided exactly: by float only when |a + bφ| > 0.01 with
  |a|, |b| < 2^50, otherwise by exact integer comparison. Hyperplanes are compared by an
  exact projective key: the primitive integer vector after making the first coordinate
  rational. Floats appear only (i) as a sort/filter step that is then re-checked
  exactly, and (ii) in the zero-area side of the "whole or not at all" test in item 6
  (stated there).
* **Coordinates.** These are the paper's. The 600-cell P0 is the union of the five S5-orbits
  A, B, C3, −A, −B in the sum-zero space of R^5, stored as 5x − (Σx)·1. Its 120 corners are
  checked to be closed under the reflection in each corner (an H4 root system), and the
  reflections generate a group of order 14400 that contains −1. All group work uses these
  exact permutations. The 120-cell Q has as corners the 600 cell centres of P0 (sums of
  the 4 corners of each cell).
* **Hulls.** Facets are found by testing every 4-subset of corners exactly as a supporting
  hyperplane. The result is certified closed: each 2-face lies in exactly two facets, and
  Euler's relation holds. 2-faces are the intersections of two facets with ≥ 3 corners.
  A plate is the hyperplane through the centre and the face; its normal is an exact
  generalised cross product.

## Rerun

From a clean copy of this folder: `PY=/path/to/python ./run_all.sh`. It needs numpy, scipy,
ortools, highspy and python-sat. Each step takes under 5 minutes on the compute host (24 cores).
`cache/` (group tables, about 50 MB) is rebuilt by `s0_base.py` and is not kept.

## Results

| # | Item | Verdict | Numbers |
|---|------|---------|---------|
| 1 | Cross walls = central sections of the 25 inscribed 24-cells | **MATCH (exact)** | 25 24-cells (every D4 simple system among the corners, closed under reflection); each corner in 5. Each has 24 octahedral facets and so 12 cell axes. Each section holds 12 corners of its 24-cell and exactly 12 corners of the 600-cell. The 300 sections are distinct and are exactly the 300 cross walls (`data/crosswalls_24cells.csv`). |
| 2 | Theorem A | **MATCH (exact)** | A has f = (20, 40, 30, 10) and 30 plates, one face each: 20 edge triangles and 10 hexagons, all on mirrors. B has f = (30, 90, 80, 20) and 80 plates, one face each: 10 edge triangles and 30 golden rectangles on mirrors, 40 radius triangles on cross walls. A and B share exactly 10 mirrors (= the S5 mirrors) and together use all 60. C3 has f = (20, 60, 70, 30), with 70 faces on 5 cross walls, 14 each. (The f-vectors reversed give the paper's A*, B*, C3* f-vectors in B′(b).) |
| 3 | Lemma 3 (a)–(c), exact transitivity | **MATCH (exact)** | 1200 edge triangles, 20 per mirror. 720 pentagons of Q, 12 per mirror. 1800 golden rectangles, all on mirrors, 30 per mirror. 2400 radius triangles, all on cross walls, 8 per cross wall. The exact W(H4) orbit of one face is the whole class for triangles, rectangles and radius triangles. |
| 4 | Theorem B (a)–(d) | **MATCH (exact)** | (a) 24 corners at 36° per corner, in two icosahedral 12-sets. 10 inscribed 600-cells, each exactly reflection-closed. Every corner lies in 2. Two states of 5, disjoint within a state; across states every meeting is 24 corners forming a 24-cell (25 of them). (b) A complete search over ordered 4-tuples of Q's corners, with no symmetry used, finds 1200 A, 1200 B and 600 C3 copies, each inside exactly one P_i: 120/120/60 per P_i and 40/60/20 through each corner. Stabilisers are 12, 12, 24. (c) 1560 walls = M 60 + X 300 + N 1200. Hosts: M is a cross wall of all 10; X is a mirror of exactly the 2 P_i through that axis; N is a cross wall of exactly 2. Each P_i has 60 X-mirrors and 60 M + 240 N cross walls. All 1200 A copies are hidden in Q and use only X (all 300). B uses 60/300/1200 and C3 uses 60/0/1200; none of them is hidden in Q, and all are hidden in their own P_i. (d) In every P_i each triangle is a face of exactly 2 A copies and 1 B copy. |
| 5 | Proposition 5 | **MATCH (exact)**, with one wording note | 60 S5s in each 600-cell, each of order 120, with orbits 20, 20, 20, 30, 30. The orbits are exactly the copies of item 4. Every S5 of every 600-cell splits its 5 shared 24-cells as (0, 12, 12) once and (10, 2, 12) four times. 90,000 cases give **18** patterns of (kind in first state, kind in second). In **1500** cases every corner has the same kind; in exactly the same 1500 cases the two S5s cut the 24-cell into the same pieces, and for each (pair, first S5) exactly 1 of 60 matches. Copies across states: A–A share ≤ 5 corners and ≥ 2 walls; A–B ≤ 3 corners, ≥ 1 wall; B–B ≤ 6 corners, ≥ 5 walls. Data: `data/prop5_cases.csv.gz` (all 90,000 rows) and `data/prop5_patterns.txt` (pattern table). **Note:** "share at most 6 corners" holds for A and B copies. Two C3 copies from the two states can share **12** corners and 0 walls. |
| 6 | Theorem B′ (d) covers | **MATCH**: coverage exact except one float side; minimum **16 / 16 / 22 proved by two solvers** | See below. |
| 7 | No exact cover | **MATCH (proved twice)** | CP-SAT (equalities) and an Algorithm X written here both find none, complete, for A*, B*, C3* and for all 300 dual copies together. |

### Item 6 in detail

* **Coverage.** The fin over the ridge of X* dual to the edge ab of X is the normal cone of ab. That
  cone does not depend on r² or on the scale of P, so coverage was computed with P0 (P is a
  positive multiple of P0).
  * Each copy covers exactly **60** pentagons whole: A* 120 copies with 10 per pentagon, B* 120
    copies with 10 per pentagon, C3* 60 copies with 5 per pentagon.
  * No (copy, pentagon) pair is covered in part.
  * Each copy has 10 plates, all on Q's mirrors.
  * Every edge of Q lies whole in a single fin, for every family.
* **What "covered whole" means.** The pentagon must lie in the **union** of the copy's fins on
  its plate. That union is needed:
  * One fin alone holds only 30 of B*'s 60 pentagons and **none** of C3*'s.
  * With "one fin" as the reading, B* and C3* would not reach 60.
  * The paper's "covers a pentagon whole" should say that several fins of one copy together
    cover it.
* **Exactness of the coverage test.**
  * Regions where one corner maximises: they are pruned exactly by ranks. Each region of
    positive area is certified by an exact witness point checked in Z[φ]; all were certified.
  * Zero area of the remaining regions: decided by a float LP. This is the one non-exact step.
* **(i) Explicit covers.** 16 A*, 16 B* and 22 C3* are in `data/cover_*.json`. Each was re-checked
  as a set union of all 720 pentagons. The multiplicities are A* 540/120/60 (as in the paper's
  Figure 7), B* 576/72/48/24 and C3* 280/288/144/8.
* **(ii) No smaller cover.** No symmetry breaking was used in any of these runs.

| question | HiGHS MIP (minimise) | OR-tools CP-SAT, objective given (`cpsatmin`) | CaDiCaL (pysat, totalizer ≤ K) |
|---|---|---|---|
| A* ≤ 15? | Optimal 16, dual bound 16, 1247 nodes, 12.7 s | INFEASIBLE, 12.5 s | **NOT DONE**: no answer in 260 s; also no answer in 260 s with copy 0 forced, which is justified by transitivity |
| B* ≤ 15? | Optimal 16, dual bound 16, 1199 nodes, 9.6 s | INFEASIBLE, 9.4 s | not run (A* already timed out) |
| C3* ≤ 21? | Optimal 22, dual bound 22, 27461 nodes, 16.3 s | INFEASIBLE, 42.4 s | not run |

Pure CP-SAT feasibility (no objective) also gave no answer in 270 s for A*.
`logs/s7_cover_A_cpsat_le15.log` therefore ends `FINAL FAIL … UNKNOWN`, as do the two
CaDiCaL logs. These are timeouts, not contradictions.

* **Short human-checkable bound (s9): none reaches the optimum.**
  * The LP relaxation is exactly 12, so the fractional bound is the counting bound.
  * Packing bound: the largest set of pentagons with no two on one copy has 10 (A*, B*) and
    11 (C3*).
  * Mirror double counting: every copy meets exactly 10 of the 60 mirrors (6 pentagons on
    each). Each mirror's 12 pentagons need ≥ 2 copies (A*, B*) or ≥ 3 copies (C3*). This gives
    ≥ 12 for A* and B*, and ≥ **18** for C3*. The C3* figure is the best short argument found;
    it is short except that "≥ 3 per mirror" rests on a 12-pentagon ILP.
  * The dodecahedron, corner and edge families give less.
  * The optimality of 16/16/22 rests on the two solvers, and is now certified: DRAT proofs of "no cover of 15, 15, 21" checked by drat-trim (`cert/README.md`, 17 Nov).

## Not covered

* Theorem B′ (a), (b) (only the f-vectors via item 2), (e) and (f).
* Theorem C and Proposition 6.
* Tables 1 and 4.
* The quaternion hand computations in the proof of Lemma 3. The same facts were checked
  in the paper's R^5 coordinates instead.
* A third solver proof of the covers. CaDiCaL timed out.

## Comparison with the studies' outputs (done after the logs above)

`2026-11-16-redqueen-cats/data` agrees on everything compared:
* the 18 half-cat patterns;
* the shared-corner and shared-wall extremes (A–A 5 corners and 2 walls, A–B 3 and 1, B–B 6 and 5);
* "6 pentagons on each of 10 mirrors";
* the minimum covers 16/16/22 by HiGHS, with the same A* and C3* multiplicities.

The studies' meeting counts do not include C3 copies.
