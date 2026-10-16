# Fable, pass 4: pushing the exact fill of G′ (2026-10-16)

DICTO · dictospheres.com

The goal of this pass was to push the exact, overlap-free fill of G′ (the golden region minus the 24 GBPCs per bcc cell) past 46.5%, test the Bodhi pieces, and measure what is left.

Everything is exact in ℚ(√5) unless marked FLOAT. All searches ran on dicto-node as logged background jobs (`~/gbpc4/logs`). The full body lists stay on the node (`~/gbpc4/data/search-*.json`, 0.2–0.5 MB each). λ = φ|v|/9, the length of the 36° convex edges.

## Results first

1. **Best fill: 66.85% of G′, using rhombohedra and Bodhi pieces** (search RB-22, exact).
   - Per cell: Mudra 135 at scale λ and 255 at λ/2; Vajra 15 + 46; Diadem 14 + 59; oblates 32 and prolates 11 at λ/4.
   - Filled volume: (173711 − 76891√5)/17496.
   - Gap: (−21647 + 10075√5)/17496 = 0.0504 per cell.
2. **Best with rhombohedra only: 63.12%**, at sizes λ, λ/2 and λ/4 (search R-11, exact).
   - Per cell: 13 oblates at λ; 146 oblates and 24 prolates at λ/2; 628 oblates and 101 prolates at λ/4.
   - Gap: 77545/5832 − 1279√5/216 = 0.0561 per cell.
   - Pass 3 reached 46.5% with λ and λ/2 only.
3. **Adding the sizes λ/φ and λ/φ² gives 63.24%** (RX). These two sizes are not rational multiples of φ|v|. So by the pass-3 wall theorem, no tile of these sizes can have a face on a wall in a complete tiling. In a partial fill they are allowed anyway.
4. **The full-size tiles: the "12" is not a maximum.** The number of edge-λ rhombohedra per cell varies by build: 3–16 over the 12 rhombohedron builds. The most was 16 (RX, restart 0).
   - Big-first ("staged") builds hold 12–16 and fill best.
   - Random-order builds hold 3–10 and fill 54–59%.
5. **Proved: rhombohedra of edges in ℚφ·|v| (any number of such sizes) can never complete a periodic fill of G′.** The pass-3 count requires the oblate part X = −10/243 per cell. Our R builds are periodic, so their stall is forced, not just a weakness of the search.
   - This also holds for the leftover: the gap of the R-11 build has X = −379/3888 < 0 (exact).
6. **Proved: among the Bodhi pieces, only Mudra and Crown Jewel can pay that deficit** (exact; `data/gbpc-periodic-bodhi.txt`). Per r³φ³·oblate volume, at edge scale rφ|v|:

| Piece | X | Y |
|---|---|---|
| Vajra | 1/6 | 1/6 |
| Chatra | 1/2 | 5/6 |
| Mudra | **−1/3** | 1/3 |
| Crown Jewel | **−3/2** | 7/2 |
| Diadem | 1/3 | 0 |

   - Rhombohedra all have X ≥ 0.
   - A periodic fill at scale λ therefore needs at least 90 Mudras or at least 20 Crown Jewels per cell, or a mix.
   - The RB-22 build uses 135 Mudras at λ. Its leftover gap has X = 349/17496 > 0 and Y > 0 (exact). **So for this build, the count no longer forbids finishing the fill.**
7. **The leftover gap is one connected, non-convex network, not separate pockets** (FLOAT, 80³ grid; `data/gbpc-gap-R-11.txt`, `data/gbpc-gap-RB-22.txt`).
   - In each build, 93.5% of the gap is a single component that wraps the cell. Its volume/hull ratio is 0.03 (R-11) and 0.05 (RB-22), so it is far from convex.
   - The rest is a few small components plus voxel-scale slivers: 905 in R-11, 667 in RB-22.
   - No component is a known golden piece. The largest small component in RB-22 is near-convex (ratio 0.97), but its volume is 0.0002, too small to identify at this resolution.
8. **Fill checks.**
   - Exact: every placement passed an exact separating-axis test, with ties decided in ℚ(√5).
   - FLOAT, independent: 0 points covered twice and 0 body points inside an envelope, in both builds. Covered fractions: 63.7% (R-11) and 67.1% (RB-22), matching the exact volumes.

## Method

**Search.** `scripts/gbpc_search.py` uses numpy and fractions only.
- **Bodies:** rhombohedra (20 orientations, 3–5 sizes) and the five Bodhi pieces (120 orientations, sizes λ and λ/2).
- **Exact Bodhi data:** rebuilt from the exact block coordinates p + qφ in `studies/2026-10-12-bodhi-pieces/data/bodhi-B*-raw.json`. They reproduce the stored floats to 7e-16. The exact volumes match the Bodhi study.
- **Overlap test:** separating axes are the 15 golden normals plus every cross product of the edge directions in play. All Bodhi edges lie on symmetry axes (checked), so the axis set is complete and the test is exact.
- **Strategy:** randomised restarts in two kinds:
  - staged: largest size first, over all anchors, then the next size;
  - mixed: largest size that fits at each anchor.
  At each anchor the search keeps the placement with the most face contacts, breaking ties at random.

**Not done within the cap.** We did not run backtracking or beam search. The two-pass cap ran out before the Bodhi runs were long enough to justify it.

**Run status.** RB-21 ran restarts 0–2: 66.62% staged, 59.42% mixed, 66.64% staged. Restart 3 (mixed) was stopped unfinished, at the coordinator's instruction. RB-21 kept no body list, only its log (`data/gbpc-search-RB-21.log`). The gap analysis uses RB-22, the best Bodhi build.

| Run | Restarts | Best fill | Edge-λ rhombohedra per restart |
|---|---|---|---|
| R-11 (rhombohedra λ, λ/2, λ/4) | 4 | 63.12% | 13, 3, 15, 6 |
| R-12 | 4 | 62.69% | 12, 5, 14, 10 |
| RX (+ λ/φ, λ/φ²) | 4 | 63.24% | 16, 6, 13, 7 |
| RB-22 (+ Bodhi) | 1 | **66.85%** | 0 (Bodhi pieces took those places) |
| RB-21 (+ Bodhi) | 3 of 4 (restart 3 stopped) | 66.64% | 0 |

## Proved vs found

**Proved (exact):**
- G′ has no face-to-face tiling by golden rhombohedra (passes 1–2).
- Every tile with a face on a wall has its edge in ℚφ·|v| (pass 3).
- No periodic fill uses only rhombohedra with edges in ℚφ·|v| (passes 3–4).
- Only Mudra and Crown Jewel carry the negative part that a periodic fill needs (this pass).
- The Hadwiger edge invariant vanishes (pass 3).

**Found (exact constructions, not optimal):**
- Fills of 63.1% (rhombohedra only) and 66.9% (with Bodhi pieces).
- In both, the leftover is one connected non-convex network (FLOAT).

**Open:** whether any fill (periodic or not, with Mudra or Crown Jewel) closes G′ completely.

## Paragraph for GBP Draft 3, §6

We pushed the exact fill of G′ with a randomised search over golden rhombohedra and the five Bodhi pieces. Every placement is checked by an exact separating-axis test in ℚ(√5). With rhombohedra of edges φ|v|/9, φ|v|/18 and φ|v|/36, the best periodic build fills 63.1% of G′. Adding the Bodhi pieces raises this to 66.9%, mostly with Mudras. The leftover gap is a single connected, non-convex network per cell, not a set of pockets (float check). Two statements are proved exactly:
- No periodic fill by golden rhombohedra with edges in ℚφ·|v| can be complete: the oblate part of the volume count would have to be −10/243 per cell.
- Among the Bodhi pieces, only the Mudra and the Crown Jewel have the negative part needed to pay that deficit: at least 90 Mudras or 20 Crown Jewels per cell at edge φ|v|/9.

In the best Bodhi build the deficit is already paid, so the count no longer rules out completing it. Whether G′ can be closed completely remains open.
