# Fable, pass 5: independent check of the counting step (2026-10-17)

DICTO · dictospheres.com

Checks the counting claims in GBP §6 ("No one-size fill", "No face-to-face fill of any sizes", "Not face to face", "The best builds"). Exact means exact in ℚ(√5); |v| is the five-fold vector; λ is the rhombohedron edge; g is the volume of G′ per bcc cell; d_O is the oblate volume at edge |v|.

## Verdict

| Claim | Verdict |
|---|---|
| (a) One size, face to face: 66 prolate, −30 oblate per cell at λ = φ\|v\|/9 (k³ times at φ\|v\|/(9k)), so no such tiling, periodic or not | **Holds.** The homotopy step is valid; a complete proof is given below. One small correction: the conclusion holds for every λ in ℚφ·\|v\|, not only φ\|v\|/(9k). |
| (b) Face to face, any sizes | **Holds**, given that the interior of G′ is connected. That is checked in float only (pass 1: 99.8% of the free voxels in one component; the rest are 1–2-voxel slivers in the 36° wedges). |
| (c) Periodic, any arrangement, all edges in ℚφ·\|v\|: the oblate part must be −10/243 per cell | **Holds.** It is elementary (linear independence of 1 and φ over ℚ) and needs no homotopy. It needs periodicity. For non-periodic fills that are not face to face, nothing is proved. |
| (d) At least 90 Mudras or 20 Crown Jewels per cell at edge φ\|v\|/9 | **Holds with a correction.** The numbers are right, but only if every piece has its scale in ℚφ·\|v\|. A piece at a scale in ℚ·\|v\| (for example the φ-smaller oblate of pass 1, or a Vajra at \|v\|/9) can also have a negative part. Precise form: Σ_Mudra (s/λ)³/90 + Σ_CrownJewel (s/λ)³/20 ≥ 1 per cell, where s is each piece's scale. |

## Numbers (exact, re-derived)

- g = φ³ d_O · (X + Yφ) with X + Yφ = 1/243 + (11/243)√5 (from `data/gbpc-periodic-count.txt`). Since √5 = 2φ − 1, this gives Y = 22/243 and X = 1/243 − 11/243 = −10/243.
- Prolate volume = φ × oblate volume (exact: (−232 + 104√5) = φ(376 − 168√5)).
- At λ = rφ|v| one tile has oblate volume r³φ³d_O, so the counts are o = X/r³ and p = Y/r³. At r = 1/9: o = −10·729/243 = **−30** and p = 22·729/243 = **66**. At r = 1/(9k) both are multiplied by k³.
- **Mudra:** volume (1/2 − √5/6) prolate blocks = (−1/3 + φ/3) oblate units, so X = −1/3. At r = 1/9 it contributes −1/(3·729), and 10/243 ÷ 1/2187 = **90**.
- **Crown Jewel:** X = −3/2, and 10/243 ÷ (3/(2·729)) = **20**. The Vajra, Chatra and Diadem have X = 1/6, 1/2, 1/3 > 0.
- A scale s = r|v| (not times φ) multiplies a piece's (X, Y) by φ⁻³ = 2φ − 3, which turns (X, Y) into (−3X + 2Y, 2X − Y).
  - Oblate (1, 0) → (−3, 2): this is pass 1's small oblate.
  - Vajra (1/6, 1/6) → (−1/6, 1/6): also negative. This is why (d) needs its qualifier.

## Proof of (a)

**Setting.** We have a face-to-face tiling of G′ by golden rhombohedra of one edge λ. Write a, b for the two five-fold directions in a wall's plane.

1. **Walls are grids.** Faces lying in one wall are all translates of the parallelogram λa × λb. Face to face, they meet edge to edge. A convex corner of the wall must be a face vertex. So the faces covering the wall form a patch of the grid c + λℤa + λℤb through a wall corner c. All wall corners lie on that grid. Their coordinates differ by rational multiples of φ, so λ ∈ ℚφ·|v|. (This is the wall test, in its face-to-face form.)
2. **The map F.** Tile vertices differ by vectors in λM, where M is the rank-6 ℤ-module of the five-fold vectors. Let σ* be the additive map on λM that is coordinatewise conjugation σ (a + b√5 ↦ a − b√5). Set F(v) = σ̃(c₀) + σ*(v − c₀) at the vertices, where c₀ is a wall corner, and extend F affinely over each tile.
   - F is continuous, because the tiling is face to face.
   - On each tile, det DF = σ(vol T)/vol T.
   - On each wall, F is the affine map c + sλa + tλb ↦ F(c) + sσ̃(λa) + tσ̃(λb). By step 1 it depends only on G′ and λ.
3. **The deviation H is bounded.** Let A be the ℝ-linear map with Aℓ = σ̃(ℓ) on the bcc lattice L. Here L ⊂ λM, by the module test. Put H = F − A·x.
   - On the walls, H is periodic: F(x + ℓ) = F(x) + Aℓ there. So H is bounded on the walls.
   - Every point of G′ lies within a fixed distance R₀ of a wall, because the triacontahedron union is periodic.
   - A segment of length ≤ R₀ crosses a bounded number of tiles, since tile volume is bounded below.
   - DH is bounded, since there are finitely many tile orientations.
   - So |H| ≤ C on all of G′, for any such tiling. **This is the point the sketch left implicit, and it holds.**
4. **The count.** Let U_N be the union of the tiles assigned to N³ cells.
   - Σ_T σ(vol T) = ∫ det(A + DH) = det(A)·vol U_N + ∮_{∂U_N} (null-Lagrangian terms in H and its tangential derivatives). On a closed surface, integration by parts removes every factor of A·x, so the terms involve H only.
   - The wall part of ∂U_N gives N³Φ + O(N²), where Φ is a fixed per-cell constant from the periodic wall data.
   - The rest of ∂U_N has area O(N²), and the integrand there is bounded by step 3.
   - Hence p_N σ(v_P) + o_N σ(v_O) = N³S + O(N²), with S = det(A)·g + Φ. Together with the real equation p_N v_P + o_N v_O = N³g + O(N²), and the determinant φ − σ(φ) = √5 ≠ 0, this gives o_N = N³·o + O(N²).
5. **S = σ(g).** This is now a theorem; pass 1 only checked it numerically.
   - Take any periodic triangulation of G′ whose vertices lie in ℚ(√5)³ and whose vertices on walls have rational (s, t). Such a triangulation exists: perturb any triangulation, since the validity conditions are open and both point sets are dense.
   - Let F̃ = σ̃ at the vertices, extended piecewise affinely. Then F̃ = F on the walls, and F̃ − A·x is periodic.
   - So F̃ gives the same S by step 4. Its tile sum is Σσ(vol simplex) = σ(g).
   - Pass 1's exact value 704/81 + 928√5/243 agrees.
6. **Conclusion.** The densities are the unique rational solution of o + pφ = g/v_O(λ), which is o = X/r³ < 0 for every λ = rφ|v|. **No face-to-face one-size tiling of G′ exists, periodic or not.** The counting step is now checked independently.

**Remark.** The method reproduces the Ammann–Kramer ratio only for tilings with bounded H, such as cut-and-project tilings. In all of space, without walls, H can grow, and the ratio is not forced. Here the walls of G′ are what force H to stay bounded.

## Suggested wording for §6 (replaces "The computations are exact; … not yet checked independently.")

> The computations are exact, and the counting step has now been checked independently (FABLE-GBPC-COUNT-CHECK.md). In a face-to-face tiling the conjugation extends to a continuous piecewise-affine map whose deviation from a linear map is fixed on the walls and therefore bounded, since every point of G′ is near a wall. This bounds the error by O(N²) and forces the same counts as a periodic tiling would; the negative oblate count holds for every edge length in ℚφ·|v|.

In "No face-to-face fill of any sizes", replace "(exact; the counting step is a proof sketch)" with "(exact; uses that G′ is connected, checked in float)".

In "The best builds", replace "at least 90 Mudras or 20 Crown Jewels per cell at edge φ|v|/9 (exact)" with "when every piece has its edge in ℚφ·|v|, at least 90 Mudras or 20 Crown Jewels per cell at edge φ|v|/9 (exact); pieces at other scales, such as φ-smaller oblates, can also carry a negative part".
