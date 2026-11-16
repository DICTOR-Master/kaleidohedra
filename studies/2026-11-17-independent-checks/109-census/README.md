# Independent cross-check of the Paper #109 census (17 November 2026)

Reviewer's request: re-derive the census with an independent implementation, not a re-run of the
existing scripts. This study covers the census (§6, Table 3a). The X and F core was checked
separately in the paper's own folder and is not repeated here.

**Independence.** All code in `scripts/` was written from scratch. No census, study or paper script
was opened. For definitions we read only the paper (§2, §6, Table 3a) and the Method section (§0) of
the hidden-zeros study README. The census outputs (`census-*.json`) were opened only after our own
enumeration, zeros and Table 3a spot-check had been written to `logs/` (build, canon, merge and
spot3a logs).

## Method

- **Points, exact.** The 600-cell is the 120 unit icosians, with doubled coordinates in Z[φ] stored as
  integer pairs a + bφ. The 120-cell is the 600 cell centroids, found as 4-cliques of the edge graph.
  The 24-cell is 2T and the snub 24-cell is 2I ∖ 2T. The E8 roots are the units together with φ⁻¹ times
  the units, with B(x, y) = a + b when ⟨x, y⟩ = a + b√5. The check asserts B ∈ {0, ±½, ±1}.
- **Tones, exact.** We build the Gram matrix as codes into the distinct cosines, which are exact in
  Q(φ). For a set S we form the histogram of cosines over S × S, then
  T_k = |S|⁻² Σ n_c G_k(c)/G_k(1). G_k is U_k by recurrence in Q(φ) on S³, and C_k^(3) over the
  rationals on S⁷. A zero means exactly (0, 0).
- **Groups.** H4 is the 14400 maps x ↦ l x r̄ and l x̄ r̄. F4 is the 1152 maps with l, r in 2O that
  preserve 2T. The snub group is the 576 elements of H4 that preserve 2T. Each group becomes exact
  permutations by matching images to points.
- **Subgroup catalogue** (our reading of §0):
  - every two-generated subgroup ⟨g, h⟩, with g a conjugacy-class representative and h running over
    the orbits of C(g) (H4: 34 classes and 33,528 pairs; F4: 25 and 3,316; snub: 23 and 1,876);
  - every reflection subgroup up to conjugacy (H4: 16, F4: 36, snub: 7);
  - [L × R], [L × L].2 and diag(L).2 for all subgroup classes L and R of 2I (or 2O). For the snub,
    these are taken up to 2T-conjugacy;
  - the graph groups {x ↦ a x α(a)⁻¹} for every subgroup L and every automorphism α. Their orbits are
    the twisted classes;
  - each of these closed under −I and under taking the rotation part (by Schreier generators).
- **Sets.** Every orbit; every union of two orbits of the same group; and unions of twisted classes
  (all unions when there are at most 9 classes, otherwise unions of at most 3). In the snub we use
  twisted classes of 2I-subgroups that lie inside the snub. We count sets up to the polytope's symmetry
  group. The canonical form is the exact lexicographically least image; for the 120-cell and E8 it is
  a 128-bit min-hash, which gave exactly the same 9,696 classes as the exact form on the 600-cell
  (`hashcheck-600.log`).

## Results

| item | result |
|---|---|
| Validation (`v1_validate.log`) | **MATCH.** The 600-cell rings only at 12 and 20. X in R⁵ is silent exactly at {1, 2, 5, 7} and F exactly at {1, 2, 3, 6}. The twisted classes of 2I are 20, 20, 20, 30, 30: X and −X give {1, 2, 5, 7}, F and −F give {1, 2, 3, 6}, and R gives 2 and all odd degrees. |
| (c) Zeros of every stored census set, recomputed | **MATCH:** 600-cell 808/808, 24-cell 144/144, snub 257/257, E8 541/541. The point orderings were identified independently: the coordinates sorted in the √5 basis, and for E8 the units first, then φ⁻¹ times the units. A wrong ordering fails on about 40% of the sets. **120-cell: NOT DONE set by set.** The JSON stores no coordinates, and its 120-cell order is not a coordinate sort (`order_probe120*.log`, `compare-120-wrong-ordering-probe.log`). |
| 120-cell, without the ordering (`compare120_inv.log`) | **MATCH (invariant level).** For all 1482 census sets, the triple (size, exact zero list, stabiliser order) occurs among our classes, and no triple occurs more often in the census than among our classes. |
| (a) Census sets in our family | 24-cell 144/144, snub 257/257, E8 541/541. 600-cell 721/808: all 177 orbits and 198 unions, and 346/433 twisted sets. The other 87 twisted sets are unions of **4–7** twisted classes from partitions with 15–62 classes. That is outside the "at most 3 when more than 9" rule in §0, but each of the 87 is still a union of our independently computed twisted classes (`diag_tw-600.log`). |
| Orbits, both directions | **MATCH.** Every single orbit of our larger catalogue is in the census: 600-cell 181/181, 24-cell 34/34, snub 94/94, E8 356/356; 120-cell 1058/1058 by invariant triple. |
| (b) Set counts 808 / 1482 / 144 / 257 / 541 (3232) | **NOT REPRODUCED.** Up to symmetry our family has 9,696 / 52,291 / 476 / 13,099 / 9,363 classes. All of the excess is unions: our union rule (every pair of orbits of every subgroup in our larger catalogue) is wider than the census's 179/221/71-class catalogue, and §0 does not say which unions are kept. The census sets are distinct up to symmetry in the four polytopes where we could test it (808, 144, 257, 541). |
| Table 3a, 600-cell, degree 8 (`spot3a.log`) | **MATCH.** Exactly four 30-point classes, zeros {1, 3, 4, 8}, stabilisers 15, 15, 50, 50. Exactly four 60-point classes, zeros all odd, 4 and 8, stabilisers 60, 60, 200, 200. They are unions of two orbits of [C3 × C5], [C5 × C5], [C3 × C10] (= [C10 × C6]) and [C5 × C5].2 (= [C10 × C10].2); these are equal up to ±1 and side swap. |
| Table 3a, 120-cell, 240 points | **MATCH.** Two classes (a mirror pair) with zeros 1–5, 7–11, 13, 15, 17, 19 and stabiliser 120, each a union of two [2T × C10] orbits (the paper's [C5 × 2T] up to ±1 and side swap). |
| Table 3a, E8, 120 roots | **MATCH.** Shells 96 + 24 with stabiliser 576, and 72 + 48 with stabiliser 144, each with zeros 4 and all odd degrees. Both single shells kill 4 as well (bizonal, §6). |
| Explanation mechanisms (G, X, ZONAL, TW, SPAN, GAL, RES) | **NOT DONE** (not in scope). We check zeros, not whether they are explained. |

Note: our 120-cell family also has degree-8 zeros in 30-, 60- and 120-point sets. Table 3a lists only
the 240-point one as unexplained, so the others must be explained by the census mechanisms; we did not
check that.

## Not covered

- The 120-cell census was compared by invariants only, not set by set.
- The exact count of 3232 sets is a property of the census's own catalogue and union rule, and we did
  not reproduce it.
- The explanation mechanisms, the kernels N_k, the linkage tables and the controls were not
  recomputed.
- Our catalogue is complete up to conjugacy for two-generated and reflection subgroups (pairs are
  taken up to simultaneous conjugacy). The quaternion families come from subgroup classes, so it is
  not a list of all subgroups.

## Rerun (from a clean checkout, on the compute host; 24 cores; each step under 5 minutes)

```
cd scripts
PY=python3   # needs numpy and scipy
$PY v1_validate.py
for w in 600 24 snub E8 120; do $PY build.py $w; done
$PY canon.py 600 0 340000; $PY canon.py 600 340000 700000
$PY canon.py 24; $PY canon.py snub; $PY canon.py E8
$PY canon.py 120 0 600000; $PY canon.py 120 600000 1200000; $PY canon.py 120 1200000 1800000
HASH=1 $PY canon.py 600          # optional: hash canonical form vs exact
for w in 600 24 snub E8 120; do $PY merge.py $w; done
$PY spot3a.py
# comparison (CEN = the hidden-zeros study's data folder)
for w in 600 24 snub E8; do $PY compare.py $CEN $w; done
$PY diag_tw.py $CEN 600; $PY compare120_inv.py $CEN
```

Outputs: `data/indep-<world>.json` lists each class with its size, representative indices, exact
zeros and provenance. The intermediate pickles are rebuilt by the scripts and are not kept.

Computation with Claude (Anthropic).
