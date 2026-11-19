# Exact existence of the fair dice without central symmetry, by Alexandrov's condition (20 November 2026)

**Verdict: all 956 orbit sets satisfy Alexandrov's condition, so each carries a fair die (and exactly one, up to scale), without numerics: the 94 Td and T dice of the main catalogue (Td 3, T 91) and the 31 O, 91 Td and 740 T dice of the two-icosahedron study, 956 of 956 certified, none undecided. The bound used is the same for all: (H) no open hemisphere holds more than M of the N directions, and here M/N ≤ 0.6875; with (D), the perimeter of a hull is at least twice its diameter, every set A that could fail would need more than N/2 directions within a diameter of at most π(2M − N)/N ≤ 67.5°, and no pair of directions has that many in its lens. The smallest exclusion margin is 0.88 (in the cosine), far above the arithmetic error (1e-14). Controls: on the 87 polar sets that fail the condition (exhaustive, study 2026-11-20-aequi-alexandrov) the test certifies none; of the 232 that hold it certifies 60 and leaves 172 undecided, of the 50 solved controls 45 and 5; it never contradicts the exhaustive verdict. This closes open item (1) of the Aequi draft. Part 2 (below the frame groups): of the 4404 dice of the draft's §5.3, 3104 have their face directions in opposite pairs (Corollary 3, not tested) and the other 1300 (D2 857, D3 344, D5 62, D2d 27, S4 8, D3h 1, D5h 1) are all certified by the same test, none undecided (M/N ≤ 0.75, smallest margin 0.33); so existence is exact for all 4553 dice of study 2026-11-19-aequi-complete. The controls, rerun, give the same verdicts as above, the 87 failing sets again none certified.**

## The condition

A fair die with unit face normals n_1..n_N is, through the polar body, Alexandrov's problem of prescribing the integral Gauss curvature μ = (1/N) Σ δ_{n_k} (A. D. Aleksandrov, C. R. (Dokl.) Acad. Sci. URSS 35 (1942) 131–134; condition, existence and uniqueness as stated by J. Bertrand, Geom. Dedicata 183 (2016) 81–99, arXiv:1505.04821, Theorem 1.2, and by V. Oliker, Adv. Math. 213 (2007) 600–620, arXiv:math/0701398, Theorem 1, the polytope case in Theorems 4 and 6). For equal masses (the draft's Proposition 2, following Bertrand's (18)): the condition fails if and only if some set A of the directions lying in an open hemisphere has

g(A) = 2π(2|A| − N)/N − L(A) ≥ 0,

L(A) the perimeter of the spherical convex hull of A (twice the length for an arc, 0 for a point). Study 2026-11-20-aequi-alexandrov tested this over every subset, possible for N ≤ 13. Here N runs from 10 to 118, so a reduction to finitely many cheap tests is needed.

## The reduction and its proof

Write d for the angle between directions, and for two directions p, q (not opposite) with D = d(p, q) let the lens be S(p, q) = {directions x : d(x, p) ≤ D and d(x, q) ≤ D}. Let M be the largest number of the N directions in one open hemisphere, and M(S) the same for a subset S.

**Lemma.** If some A in an open hemisphere has g(A) ≥ 0, then there are directions p, q in A with N/2 < k_max and d(p, q) ≤ π(2k_max − N)/N, where k_max = min(|S(p, q)|, M(S(p, q)), M).

*Proof.* Let k = |A|. Since L ≥ 0, g(A) ≥ 0 needs 2k > N (the draft's Proposition 2), so k ≥ 2 and A has two points at largest distance; call them p, q and D = d(p, q). Then:

1. A lies in an open hemisphere, so k ≤ M; and p, q are not opposite, so D < π.
2. Every x in A has d(x, p) ≤ D and d(x, q) ≤ D (D is the diameter of A), so A ⊆ S(p, q): k ≤ |S(p, q)|, and as A is in an open hemisphere, k ≤ M(S(p, q)). So k ≤ k_max.
3. L(A) ≥ 2D. Let K be the hull of A, a convex spherical polygon (or an arc) inside an open hemisphere. The great circle through p and q meets K in an arc from a to b on the boundary of K that contains p and q, so d(a, b) ≥ D (the arc is shorter than π, inside the open hemisphere). The boundary of K runs from a to b in two ways, and each way is at least the geodesic distance d(a, b). So L ≥ 2 d(a, b) ≥ 2D. (For an arc K, L is twice its length by definition, which is again ≥ 2D.)
4. g(A) ≥ 0 gives 2D ≤ L(A) ≤ 2π(2k − N)/N ≤ 2π(2k_max − N)/N. ∎

**Certificate.** So if every pair p, q of the directions (not opposite) has k_max ≤ N/2 or d(p, q) > π(2k_max − N)/N, no A fails, Alexandrov's condition holds, and by the draft's Theorem A (Oliker's Theorems 4 and 6 for existence, Alexandrov's uniqueness as stated by Bertrand) the fair die exists and is unique up to scale. If M ≤ N/2 no pair is needed at all: then g(A) ≤ −L(A) ≤ 0 with equality only for |A| = N/2 = 1. The test is a finite list of exact comparisons: N(N − 1)/2 pairs, each a count and one cosine.

The hint's monotone step (that for a fixed hemisphere the worst A is all the directions in it) is not used and not claimed; L grows with A (a convex set inside another has the shorter perimeter), but whether g does depends on the set.

**M exactly.** The count f(v) = #{x : v·x > 0} keeps every strict inequality under a small change of v, so it is largest on an open cell of the arrangement of the great circles x^⊥. Any two great circles meet, so every cell has a vertex w = ±(x_i × x_j)/|x_i × x_j| on its boundary, and near w the cell is {w + εu} with u in an open sector of the circle w^⊥, where f = #{w·x > 0} + #{x on w^⊥ : u·x > 0}. So M = max over vertices w of #{w·x > 0} + h(w), with h(w) the most directions on the circle w^⊥ in one open half-circle (tried at every break angle ± 10⁻⁶ rad). The same routine gives M(S) for a lens.

**Arithmetic.** The directions are built in 50-digit arithmetic from the exact frame coordinates (0, ±1, ±φ, ±1/φ) and rounded once to doubles (error ≤ 1.2 × 10⁻¹⁶ per coordinate; they agree with the studies' float lists to 1.1 × 10⁻¹⁶), so every dot product is within 10⁻¹⁴ of its exact value. Each inequality relied on has a stated margin far above that:
- lens membership is tested inclusively with tolerance 10⁻⁹ (this can only enlarge S, which only makes the certificate harder);
- a pair is excluded by distance only when cos(π(2k_max − N)/N) − p·q > 10⁻⁹; the smallest such margin on the 956 sets is 0.8827;
- in computing M, a sign w·x is classed zero below 10⁻¹² and nonzero above 10⁻⁹ (the run stops if any falls between): the largest zero is 2.6 × 10⁻¹⁶, the smallest nonzero 0.021; the smallest |x_i × x_j| used is 0.188; in the half-circle counts the smallest |cos| is the deliberate tilt 10⁻⁶.

## Method

1. **Sets** (scripts/extract.py, data/sets.jsonl): the 94 Td and T rows of data/catalogue.csv of study 2026-11-20-aequi-catalogue, face directions from the dice files of study 2026-11-19-aequi-complete; the 31 O, 91 Td and 740 T dice of data/aequi.json of study 2026-11-20-aequi-two-placements; as controls the 87 failing, 232 holding and 50 solved polar sets of study 2026-11-20-aequi-alexandrov. Every direction is an index into the 122 directions of the two-placements study, whose first 74 are the 74 of the main study (checked).
2. **Certificate** (scripts/existence.py, data/results.jsonl, data/controls.jsonl): M, then every pair; refinement by M(S) only where a pair is not excluded by min(|S|, M). Per set: M, the bound used, pairs tested, the smallest margin and its pair, the arithmetic margins.
3. **Independent checks** (scripts/check.py, data/check-*.jsonl): they cannot certify, only expose an error. (a) M from 200 000 Fibonacci directions and from every vertex tilted at random by 10⁻⁵: never above the exact M, and equal to it on all 1325 sets. (b) A witness hunt over caps (the k directions nearest a direction, for 3000 Fibonacci directions and every face direction), g by the hull in the gnomonic chart as in alex.py of study 2026-11-20-aequi-alexandrov: it finds g ≥ 0 on all 87 failing sets, and on the 956 main sets its largest g is −3.86.
4. **Summary** (scripts/summarise.py, data/verdicts.csv with one row per set, logs/summary.log).

## Results

| group | sets | N | largest M/N | certified | undecided | bound | smallest margin |
|---|---|---|---|---|---|---|---|
| main catalogue, Td | 3 | 10–22 | 0.6000 | 3 | 0 | H + D | 1.2572 |
| main catalogue, T | 91 | 16–70 | 0.6875 | 91 | 0 | H + D | 0.8827 |
| two icosahedra, O | 31 | 30–98 | 0.5667 | 31 | 0 | H + D | 1.3376 |
| two icosahedra, Td | 91 | 28–118 | 0.6786 | 91 | 0 | H + D | 1.0112 |
| two icosahedra, T | 740 | 24–110 | 0.6250 | 740 | 0 | H + D | 1.2290 |
| **all** | **956** | | | **956** | **0** | | |

No set has M ≤ N/2 (none is centrally symmetric), so every one needed the pairs; none needed the refinement M(S). What decides is simple: an open hemisphere holds at most 68.75% of the directions, so a failing A would have more than half of them within a diameter of at most π(2M − N)/N ≤ 67.5°, and no lens of that size holds more than N/2.

## Controls

| polar sets (study 2026-11-20-aequi-alexandrov, exhaustive) | sets | certified | undecided |
|---|---|---|---|
| condition fails (12 with equality) | 87 | 0 | 87 |
| condition holds | 232 | 60 | 172 |
| solved controls (die known) | 50 | 45 | 5 |

It certifies no failing set, including the 12 with g = 0 exactly (the exclusion is strict), and every set it certifies is one the exhaustive test found to hold. The polar sets are small (N = 4 to 15) and often have most of their directions in one hemisphere (M/N up to 0.92), where the diameter bound is too weak; for them the exhaustive test of the earlier study decides.

## Part 2: the 4404 dice below the frame groups (20 November 2026)

The draft's open question 1: run the certificate on the dice of §5.3, the 4404 Aequi of study 2026-11-19-aequi-complete whose full group is not a frame group (prisms included; the 149 frame-group dice are Part 1 and Corollary 3).

**Method.** (1) scripts/extract_below.py (data/sets-below.jsonl, logs/extract-below.log) reads the 4553 files data/dice/*.json of study 2026-11-19-aequi-complete (each label met once in its data/table.csv), sets aside the 149 of Ih, I, Oh, O, Td, Th, T, and tests each of the other 4404 for opposite pairs (the index set equals its negative, exactly, the frames being centrally symmetric). As Theorem A (b) predicts, a set has opposite pairs exactly when its full group contains the central inversion (no exception among the 4404). (2) existence.py unchanged (data/results-below.jsonl, logs/run-below.log), with every safeguard of Part 1. (3) check.py unchanged on these results (data/check-below.jsonl, logs/check-below.log). (4) The controls rerun with existence.py in the same session (data/controls-rerun.jsonl, logs/controls-rerun.log). (5) scripts/summarise_below.py (data/verdicts-below.csv, one row per tested set, logs/summary-below.log).

**Results.**

| group | dice | opposite pairs (Corollary 3) | tested | N | largest M/N | certified | undecided | smallest margin |
|---|---|---|---|---|---|---|---|---|
| C2h | 888 | 888 | 0 | | | | | |
| D2 | 857 | 0 | 857 | 6–20 | 0.7500 | 857 | 0 | 0.3333 |
| D2h | 848 | 848 | 0 | | | | | |
| S6 | 694 | 694 | 0 | | | | | |
| D3 | 344 | 0 | 344 | 8–24 | 0.6667 | 344 | 0 | 0.9397 |
| Ci | 280 | 280 | 0 | | | | | |
| D3d | 261 | 261 | 0 | | | | | |
| D5d | 112 | 112 | 0 | | | | | |
| D5 | 62 | 0 | 62 | 15–57 | 0.5333 | 62 | 0 | 1.1706 |
| D2d | 27 | 0 | 27 | 6–22 | 0.6667 | 27 | 0 | 0.8090 |
| D4h | 17 | 17 | 0 | | | | | |
| S4 | 8 | 0 | 8 | 8–18 | 0.7500 | 8 | 0 | 0.3333 |
| D6h | 2 | 2 | 0 | | | | | |
| D10h | 1 | 1 | 0 | | | | | |
| D8h | 1 | 1 | 0 | | | | | |
| D3h (triangular prism) | 1 | 0 | 1 | 5 | 0.6000 | 1 | 0 | 1.3090 |
| D5h (pentagonal prism) | 1 | 0 | 1 | 7 | 0.5714 | 1 | 0 | 0.9010 |
| **all** | **4404** | **3104** | **1300** | 5–57 | 0.7500 | **1300** | **0** | 0.3333 |

All 1300 are certified by (H) and (D) alone: no pair needed the refinement M(S), and no set has M ≤ N/2. None is undecided, so the exhaustive test of study 2026-11-20-aequi-alexandrov (planned for undecided sets with N ≤ 13) was not needed. The largest M/N is 0.75 (some D2 and S4 sets), so a failing A would need more than N/2 directions within a diameter of at most 90°. The smallest margin, 0.3333 = 0 − (−1/3), is on 5789-S4-O8-4-RD12-4 (N = 8, M = 6): the bound angle is π(2·6 − 8)/8 = 90°, and the closest pair whose lens holds more than 4 directions is two O8 directions at arccos(−1/3) ≈ 109.5°. It is the closest call of all 2256 certified sets, still far above the arithmetic error (1e-14).

**Arithmetic** (these 1300 sets and the controls rerun): largest |w·x| classed zero 2.6 × 10⁻¹⁶, smallest classed nonzero 0.048, nothing between; smallest |x_i × x_j| used 0.230; smallest |cos| in the half-circle counts the deliberate tilt 10⁻⁶. The exact directions agree with the study's floats to 1.1 × 10⁻¹⁶.

**Controls**, rerun: on the 87 failing polar sets the test certifies none; of the 232 that hold it certifies 60 and leaves 172 undecided, of the 50 solved controls 45 and 5; it never contradicts the exhaustive verdict, and all 369 results (verdict, M and margin) are the same as Part 1's data/controls.jsonl. **Independent checks** on the 1300: M by sampling equals the exact M on all 1300 (never above it); the cap hunt finds no A with g ≥ 0 on any of them (largest g −2.92).

So, with Part 1 and Corollary 3, **existence is exact for all 4553 dice** of study 2026-11-19-aequi-complete: 3104 + 55 by Corollary 3, 1300 + 94 by the diameter certificate.

## LEADS

- For the paper (not edited here): open item (1) closes. Existence is exact for all 149 Aequi of the main catalogue (Corollary 3 for the 55 of Ih, Oh, Th; this certificate for the 94 of Td and T), and for the 31 O, 91 Td and 740 T dice of Proposition 6 (with Corollary 3 for the Oh and Th ones). The sentence "existence rests on the 80-digit solutions" can change to "existence is by Alexandrov's condition, checked exactly (study 2026-11-20-aequi-existence)"; the 80-digit dice remain as the dice themselves.
- The Lemma could stand in the paper as a corollary of Proposition 2, a sufficient condition that needs only pairs: if every pair of directions whose lens holds more than N/2 of them is more than π(2M − N)/N apart, the fair die exists.
- A structural reason for groups fixing only the centre (the paper's open question) is not found here; the data show M/N ≤ 0.6875 on all 956, and the margins are wide, which suggests a proof by bounding M and the lens counts for the T orbits directly.
- For the paper (not edited here): the first half of open question 1 is answered (Part 2). Existence is exact for all 4404 dice of §5.3: 3104 by Corollary 3, the 1300 without opposite pairs (D2 857, D3 344, D5 62, D2d 27, S4 8, D3h 1, D5h 1) by Corollary 3′, none undecided. §5.3 and the proof notes can say existence is exact for all 4553; the question's second half (a structural reason) stays open.
- A structural reason now has more data: on all 2256 sets without opposite pairs (Parts 1 and 2), M/N ≤ 0.75 and every set passes on (H) and (D) alone; the two tightest (4939-D2-O8-4-RT24-4-1 and 5789-S4-O8-4-RD12-4, both N = 8, M = 6, margin 1/3) are where the 90° bound meets two O8 directions at 109.5°.

## Files

scripts/: extract.py, existence.py, check.py, summarise.py (they read groups.py of studies 2026-11-19-aequi-complete and 2026-11-20-aequi-two-placements). data/: sets.jsonl, results.jsonl, controls.jsonl, check-results.jsonl, check-controls.jsonl, verdicts.csv. logs/: extract.log, run.log, controls.log, check-results.log, check-controls.log, summary.log. Part 2: scripts/extract_below.py, summarise_below.py (existence.py and check.py unchanged; they also read the dice files and groups.py of study 2026-11-19-aequi-complete); data/sets-below.jsonl, results-below.jsonl, check-below.jsonl, controls-rerun.jsonl, verdicts-below.csv; logs/extract-below.log, run-below.log, check-below.log, controls-rerun.log, summary-below.log. Computed on a remote host; nothing here depends on the 80-digit dice.

FINAL ok
