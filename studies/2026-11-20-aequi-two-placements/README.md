# The Aequi with both icosahedron placements under Th and T (20 November 2026)

**Verdict: every orbit set of Th and T that uses both icosahedron placements was searched (224 Th sets, 1088 T sets), and every one gave exactly one fair die within the search box. They make 1083 Aequi** (Oh 53, O 31 in two hands each, Td 91, Th 168, T 740 in two hands each), none congruent to any of the 4553 of study 2026-11-19-aequi-complete. By number of face orbits: m = 2: 30, m = 3: 88, m = 4: 167, m = 5: 228, m = 6: 234, m = 7: 181, m = 8: 103, m = 9: 41, m = 10: 10, m = 11: 1. Every one is confirmed to 80 digits (largest |Ω − 4π/N| = 1.4e-100). All controls pass: the pilot's 7 cross-placement sets reappear with their depths to 9 digits, and sets using one placement only are not counted again.

This closes the lead "the two icosahedron placements together under Th and T" of study 2026-11-19-aequi-complete (its README, "Not covered").

Aequi by full symmetry group and m (every die counted once, under its full symmetry group; a chiral die counts once for its two hands):

| group | order | m=2 | m=3 | m=4 | m=5 | m=6 | m=7 | m=8 | m=9 | m=10 | m=11 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Oh | 48 | 12 | 19 | 15 | 6 | 1 |  |  |  |  |  | 53 |
| O | 24 | 5 | 10 | 10 | 5 | 1 |  |  |  |  |  | 31 |
| Td | 24 | 8 | 21 | 28 | 22 | 10 | 2 |  |  |  |  | 91 |
| Th | 24 | 3 | 18 | 42 | 51 | 36 | 15 | 3 |  |  |  | 168 |
| T | 12 | 2 | 20 | 72 | 144 | 186 | 164 | 100 | 41 | 10 | 1 | 740 |
| all | | 30 | 88 | 167 | 228 | 234 | 181 | 103 | 41 | 10 | 1 | 1083 |

## Definition (as in study 2026-11-19-aequi-complete, with the second placement added)

- **Directions**: the study's 74 (cube axes C6, O8, RD12; icosahedron axes of placement A: D12 (0, ±φ, ±1), I12 (0, ±1/φ, ±φ), RT24 (±1, ±φ, ±1/φ), all cyclic, with C6 and O8) plus placement B, which is placement A turned a quarter turn about z: **D12′** (0, ±1, ±φ), **I12′** (0, ±φ, ±1/φ), **RT24′** (±φ, ±1, ±1/φ), all cyclic. C6, O8 and RD12 are unchanged by the quarter turn, so these three families are the only directions not already in the 74. Union: 122 directions (scripts/groups.py checks that the quarter turn carries each family of A onto its primed family and that every Oh map permutes all 122).
- **Groups**: Th (pyritohedral, order 24) and T (order 12). Th has 9 orbits on the 122 (C6, O8, RD12, D12, I12, RT24, D12′, I12′, RT24′); T has 12 (O8, RT24 and RT24′ each split in two).
- **Orbit sets searched**: every set of m ≥ 2 orbits containing at least one orbit of placement A (D12, I12, RT24) and at least one of placement B (D12′, I12′, RT24′), any cube orbits allowed, reduced by the normaliser: all 48 maps of Oh normalise Th and T, so a set and its quarter-turned (or mirrored) image count once. Sets with one placement only are excluded: they are exactly the 57 Th sets and 153 T sets searched in the earlier study (scripts/classes.py counts them and checks the numbers).
- **Aequus, full symmetry group, hands, labels**: as in the earlier study. A label X+Y/k is an orbit of the die's full group with k directions from both X and Y: under Oh, O and Td the quarter turns and diagonal mirrors carry D12 onto D12′, so D12+D12′/24 is one orbit (all 24 orders of (0, ±1, ±φ)), and likewise I12+I12′/24 and RT24+RT24′/48 (or /24 under O and Td).

## Method

The earlier study's pipeline, unchanged except for the direction list and the both-placement filter (scripts/ are copies with those edits):

1. **Orbits and sets** (scripts/classes.py, logs/classes.log, data/classes.json).
2. **Double precision** (scripts/solve.py, scripts/run.sh): first orbit at depth 1, the m − 1 equations "mean solid angle of orbit k = 4π/N" in the m − 1 log-depths, scipy's hybrid Powell from the same start grids (21 starts for m = 2; 9², 6³, 4⁴, 3⁵ grids plus the centre for m = 3..6; 256 Sobol points plus the centre for m ≥ 7), box e^±1.5, acceptance every face within 1e-10 of 4π/N. Solid angles by Van Oosterom and Strackee's triangle formula (1983) on a fan from the face centre. Raw results data/raw/sol-1.jsonl, sol-2.jsonl (two compute hosts, short chunks).
3. **Re-search of empty sets** (scripts/recheck.py, logs/recheck.log, data/raw/sol-recheck.jsonl): one set had no solution from its 257 starts (T, m = 8: D12 + I12 + both RT24/12 + D12′ + I12′ + both RT24′/12). From 2049 Sobol starts (seed 2) with a larger evaluation limit, 4 starts converged, all to one solid: the Oh die D12+D12′/24 + I12+I12′/24 + RT24+RT24′/48, already met under Th; the Jacobian there is regular (smallest singular value 0.60). Its basin is small, not singular.
4. **Classification** (scripts/collect.py, logs/collect.log): centroid, full symmetry group (every isometry fixing the centroid that maps the face planes onto themselves), face orbits; repeats removed by congruence. 1312 solutions → 1088 distinct solids: 1083 Aequi, 5 face-transitive (excluded), 0 with the centroid off the centre.
5. **80 digits** (scripts/exact.py, scripts/run_exact.sh, logs/exact-summary.log, data/raw/exact.jsonl.gz): mpmath findroot at 100 working digits, corners by Cramer's rule; every face |Ω − 4π/N| < 1e-50 (largest 1.4e-100), every corner on its planes and inside the others to 1e-50 (largest residual 1.5e-100); group, corner count and orbit count recomputed from the refined depths: 0 mismatches.
6. **Tables and controls** (scripts/make_table.py, logs/make_table.log): data/table.csv, data/table.md (all 1083 with representative directions, faces by orbit, corners, depths), data/aequi.json, data/dice/*.json (one file per die, depths to 60 digits), data/counts.md, data/search-status.json, data/controls.log.
7. **Pictures** (scripts/render.py): for each die the solid (neutral label tones per face orbit; colours are labels only) and its Vacuus (one plate from the centre to each edge; slate = sloping, pale sand = on a mirror plane of the die's own group). Contact sheets by group, 40 dice a page, 30 sheets: figures/sheet-Oh-p1..p2.png, sheet-O.png, sheet-Td-p1..p3.png, sheet-Th-p1..p5.png, sheet-T-p1..p19.png. The 2166 single-die images (data/figures/, 25 MB) are not in git (.gitignore); render.py remakes them from data/raw/exact.jsonl.gz.

Credit: the solid-angle formula is Van Oosterom and Strackee's (IEEE Trans. Biomed. Eng. BME-30 (1983) 125–126); the fairness model, the orbit-depth construction and the exact-check pattern are Equanimity's (paper #111 draft, after Rawlins and Diaconis–Keller as cited there); the pipeline is study 2026-11-19-aequi-complete's.

## Search coverage

| group | orbits | m searched | both-placement sets | one-placement sets (excluded) | sets with 0 fair dice | sets with 2 or more |
|---|---|---|---|---|---|---|
| Th | 9 | 2–9 (all) | 224 | 57 | 0 | 0 |
| T | 12 | 2–12 (all) | 1088 | 153 | 0 (1 after the first grid, see Method 3) | 0 |

Th sets by m: 6, 27, 54, 63, 46, 21, 6, 1. T sets by m: 7, 38, 109, 200, 252, 228, 150, 72, 25, 6, 1.

Orbit sets of Oh, O and Td on the 122 directions need no search of their own: each of their orbits is a union of T orbits, so each of their orbit sets is a T orbit set (searched here when it uses both placements, in the earlier study when it uses one), and its die was met there with its full symmetry.

## Controls (data/controls.log)

- **The pilot's 7 cross-placement sets** (study 2026-11-19-aequi-three-families, run1.log; its D12 is D12′ here). Each reappears, as its quarter-turned image (D12 with I12′ and RT24′), with the pilot's depths to 9 digits: C6+D12+I12 (1.035081866, 1.008326858) → Th: C6 + D12 + I12′ (1.03508186623, 1.00832685841); C6+D12+RT24 (0.968371571, 0.978746466) → Th: C6 + D12 + RT24′; O8+D12+I12 (0.976386131, 0.980845617) → Th: O8 + D12 + I12′; O8+D12+RT24 (1.025156621, 1.021400472) → Th: O8 + D12 + RT24′; RD12+D12+I12 (0.977791453, 0.982791948) → Th: RD12 + D12 + I12′; RD12+D12+RT24 (0.995037734, 1.008212282) → Th: RD12 + D12 + RT24′; D12+I12+RT24 (1.008451630, 1.019765250) → Th: D12 + I12′ + RT24′. All PASS.
- **One placement not counted again**: the excluded one-placement sets number Th 57 and T 153, exactly the earlier study's; the sets searched here number Th 224 and T 1088, exactly the both-placement sets; none of the 1083 dice is congruent (scale-free plane distances and corner distances to 1e-6, mirror images included) to any of the earlier study's 4553 Aequi. PASS.
- **Refinement**: group, corners and orbit count from the 80-digit depths agree with the double-precision classification for all 1083. PASS.

## What stood out

- **Symmetries O and Td appear.** With one placement the earlier study found no die with symmetry exactly O (and Td only on the cube axes). Here the quarter turns and diagonal mirrors carry placement A onto B, so a set using both can be invariant under them: 31 O dice (chiral, two hands) and 91 Td dice.
- **O: 31 = 2⁵ − 1.** Every O die has exactly one chiral orbit RT24+RT24′/24 (the 48 directions of RT24 and RT24′ split under O into two mirror-image orbits of 24; using both gives an Oh set), joined to any nonempty choice of the five Oh orbits C6, O8, RD12, D12+D12′/24, I12+I12′/24: 5, 10, 10, 5, 1 by m.
- **Td by m equals the earlier study's T by m** (8, 21, 28, 22, 10, 2; 91 each). Td on the 122 directions has 8 orbits (C6, O8/4 twice, RD12, D12+D12′/24, I12+I12′/24, RT24+RT24′/24 twice), and the inversion permutes them as it permutes the 8 T orbits of one placement (swapping the two O8/4 and the two 24-direction orbits). With one die per set, the dice with exactly the base symmetry are the sets the inversion does not fix, so the two counts agree m by m.
- **Oh 53**: every Oh orbit set with m ≥ 2 that uses at least one of the three placement-mixing Oh orbits (2⁶ − 2³ − 3 = 53). Each self-conjugate Th set (56) gave an Oh die or one of three face-transitive solids; each of the other 168 Th sets gave a Th die.
- **Five face-transitive solids met** (excluded): Oh D12+D12′/24 (N = 24), Oh I12+I12′/24 (N = 24), Oh RT24+RT24′/48 (N = 48), O RT24+RT24′/24 (N = 24), Td RT24+RT24′/24 (N = 24).
- **Equal depths across the two studies.** Th: O8 + D12 + RT24′ here and Th: O8 + I12 + RT24 of the earlier study have the same RT24 : O8 depth ratio, 1.02140047185008282050793373959299607810 (equal in all 38 digits compared). In both dice the 8 triangles of O8 meet only RT24 (or RT24′) planes, so their fairness alone fixes that ratio, whatever the third orbit is.
- **One basin was small**: the single set where the first grid of 257 starts found nothing (Method 3). Its die exists and was met under Th; the dense re-search found that one solid and no other. "One die per set" stays an observation inside the search box, not a proof.

## Not covered

- Subgroups of Oh other than Th and T with both placements (D2h, D3d, D4h, D2d, S6, D3, D2, C2h, S4, ...): not searched.
- Other rotations of the icosahedron frame (only these two placements keep the 2-fold axes on the coordinate axes).
- Dice with depth ratios outside e^±1.5 of the first orbit; more than one fair die per set outside the start grids.
- Closed forms: values are numerical to 80 digits.
- Whether any of these dice appears in earlier catalogues was not checked here; nothing here is a priority claim.

## LEADS

1. Both placements under the subgroups of Oh (D4h, D2d, D3d, D2h, S4, ... ): the next layer of the same sweep, with the caps of the earlier study.
2. The fixed-ratio law: when an orbit's faces meet only one other orbit, its fairness fixes that one depth ratio regardless of the rest (seen above across the two studies). A table of all such shared ratios over the 5636 dice of both studies would show how many dice are determined orbit by orbit.
3. Uniqueness: a denser start grid on every set (as the re-search did for one) would test "one die per set" further; a proof is open.
4. The O dice (31, chiral, two hands) and the Td dice (91): the counting correspondence with the one-placement T dice suggests a direct geometric correspondence; not checked.
5. Closed forms for the simplest dice (m = 2: Oh 12, O 5, Td 8, Th 3, T 2).

## Files

scripts/: groups.py (122 directions, placements, quarter-turn check, both-placement filter), classes.py, solve.py + run.sh, recheck.py, collect.py, exact.py + run_exact.sh, make_table.py, render.py. data/: classes.json, plan.json, search-status.json, table.csv, table.md, aequi.json, counts.md, controls.log, dice/ (1083 files), raw/ (double-precision solutions, re-search, 80-digit records). figures/: 30 contact sheets. logs/: classes, collect, recheck, exact-summary, make_table.
