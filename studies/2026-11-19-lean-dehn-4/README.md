# Lean study 4 of the shape-language canon: our own solids on top of Dehn's theorem (19 November 2026)

**Question (DICTO's canon, continued from studies 1 to 3):** study 3 proved Dehn's theorem for one model tetrahedron and the cubes [−s, s]³. (A) Tidy, and state it for every size and position. (B) Put the zero word in Lean: the fair 18-face die, cube ∩ rhombic dodecahedron. (C) Put a nonzero word in Lean: one of AXE, CLEO, FUJI.

**Result:** (A) and (B) are proved, (B) for the whole cube ∩ rhombic dodecahedron line. (C) is proved for two of the three words, CLEO and AXE. FUJI is not done; the exact obstruction is below. Four new Lean files (1,279 lines) compile with Lean v4.35.0-rc2 and the pinned Mathlib, with the eleven files of studies 1 to 3 unchanged: no errors, no warnings, no `sorry`, only the three standard axioms (`compile.log`).

## Proved in Lean (theorem names, statements)

### A. Any size, any position (`lean/Dehn4Similar.lean`)
1. `dehnSet_smul_set`: for a > 0 and every set P, `dehnSet (a • P) = a • dehnSet P`. Scaling multiplies every edge length by a and keeps every angle; a acts on the length factor of ℝ ⊗[ℚ] (ℝ/ℚπ).
2. `IsSimilarCopy P Q`: Q = g '' (a • P) for some a > 0 and some isometry g of the space (rotation, translation, reflection). `dehnSet_similarCopy`: then `dehnSet Q = a • dehnSet P`. `dehnSet_similarCopy_eq_zero_iff`: zero for Q exactly when zero for P.
3. `similarTetra_not_scissorsCongruent_similarCube` (**Dehn's theorem, any size and position**):
```lean
theorem similarTetra_not_scissorsCongruent_similarCube {T Q : Set R3}
    (hT : IsSimilarCopy tetraSet T) (hQ : IsSimilarCopy (cubeSet 1) Q) : ¬ ScissorsCongruent T Q
```
Here "a regular tetrahedron" and "a cube" mean a similar copy of study 3's two models. That every regular tetrahedron in another description is such a copy is not a Lean statement here.

### B. The zero word (`lean/Dehn4Rational.lean`)
4. `dehnSet_sol_eq_zero_of_rational`: a solid cut out by finitely many half-spaces whose normals make, two by two, angles that are rational multiples of π has `dehnSet = 0`, for all offsets of the half-spaces. Any number of faces may pass through an edge or a corner; no edge list is needed and the solid need not be bounded.
5. `cubeRDSet s c`: the points with |xᵢ| ≤ s and |xᵢ ± xⱼ| ≤ c (`mem_cubeRDSet`), 18 half-spaces. `isPoly_cubeRD`.
6. `dehnSet_cubeRD` (**the zero word**): `dehnSet (cubeRDSet s c) = 0` for all real s, c: the whole line of cuts (for c ≥ 2s the solid is the cube and for c ≤ s the rhombic dodecahedron; these two descriptions are not separate Lean statements). `dehnSet_fairDie18`: the fair 18-face die is the member s = 1, c = μ√2 with μ = 1.03125… (study of 18 November); the statement holds for every μ, so the value of μ is not needed. `dehnSet_cubeRD_eq_cube`: the same invariant as every cube.

Not claimed: that these solids are scissors congruent to a cube. That is the converse direction (Sydler 1965, Jessen), which is not in Lean here. Proved is only: invariant zero, the same as the cube's.

### C. Two nonzero words (`lean/Dehn4Simplex.lean`, `lean/Dehn4Words.lean`)
7. `IsTetraData n p b w` and `IsTetraData.dehnSet_eq`: for a tetrahedron given by four corners and four face normals (with the finitely many identities that make the face functionals barycentric coordinates), `dehnSet` = the sum over the six edges of (distance of the two corners) ⊗ (angle class of the two faces through the edge). `IsTetraData.eq_convexHull`: the solid is the convex hull of the four corners. `theta_pair_of_gram`: the angle of two faces from the Gram numbers of their normals.
8. `tmul_add_tmul_ne_zero`: L₁ ⊗ θ₁ + L₂ ⊗ θ₂ ≠ 0 when L₁ is not a rational multiple of L₂ and θ₁ is not a rational multiple of π, whatever θ₂ is.
9. `wordAlpha_not_ratPi`: α = arccos(1/√5) = 63.43…° is not a rational multiple of π (Niven's theorem on 2α: cos 2α = −3/5).
10. CLEO: `cleoSet_eq_convexHull` (CLEO is the convex hull of its four corners, exact ℚ(√5) form of the corner data of the study of 14 October), `dehnSet_cleo`: `dehnSet cleoSet = dehn cleoEdges`, three edges of length 1 at α and three edges of length (√5 − 1)/2 at β = 79.18…° (cos² β = 1/3 − 2√5/15). `dehnSet_cleo_ne_zero` (**CLEO is a nonzero word**).
11. AXE: `axeSet_eq_convexHull`, `dehnSet_axe`: `dehnSet axeSet = dehn axeEdges`, one edge of length (√5 − 1)/2 at α, four edges of length 1 at β, one edge of length 1 at γ = arccos(√5/3) = 41.81…°. `dehnSet_axe_ne_zero` (**AXE is a nonzero word**).
12. `cleo_not_scissorsCongruent_cube`, `axe_not_scissorsCongruent_cube`: no similar copy of CLEO or of AXE is scissors congruent to a similar copy of the cube. `cleo_not_scissorsCongruent_cubeRD`, `axe_not_scissorsCongruent_cubeRD`: nor to a similar copy of any cube ∩ rhombic dodecahedron solid, the fair 18-face die among them.

## Method
- **Scaling.** The cone of directions at a point is unchanged by scaling about the origin, so the angle class is unchanged; lengths scale by Mathlib's `MeasureTheory.Measure.hausdorffMeasure_smul₀`.
- **Zero word.** At a point, the angle class is that of the cone of the tight constraints (study 2). All their normals lie in the plane across the edge. If the cone has interior, it is the cone of two of the constraints (`two_extreme`: every normal is a combination with coefficients ≥ 0 of two extreme ones; three vectors of a plane are dependent, then a sign count), and `theta_pair` of study 3 gives π minus the angle of those two normals. If it has no interior, its area, and so its angle, is 0. For the 18 normals of cube ∩ rhombic dodecahedron, written in whole numbers, the relation 4(nᵢ·nⱼ)² = k|nᵢ|²|nⱼ|² with k ∈ {0, 1, 2, 3, 4} is checked for all 324 pairs by `decide +kernel` (kernel evaluation, no added axiom); then cos² of the angle is k/4 and the angle is a rational multiple of π (double and triple angle formulas, no case list of angles).
- **Why CLEO and AXE, and why they are cheap.** Exact edge data of the three words (ℚ(√5) arithmetic on the corner data; run on the compute host):

| word | faces | edges: length at angle |
|---|---|---|
| CLEO | 4 | 3 × 1 at α; 3 × (√5−1)/2 at β |
| AXE | 4 | 1 × (√5−1)/2 at α; 4 × 1 at β; 1 × 1 at γ |
| FUJI | 7 | 6 × 1 at π − ε; 3 × 1 at γ; 3 × (√5−1)/2 at ε = 37.37…° (cos² ε = 1/3 + 2√5/15) |

  In CLEO and AXE the edges at α have a total length that is not a rational multiple of the total length of the other edges (1 against (√5−1)/2, and √5 is irrational). A ℚ-linear map ℝ → ℚ that kills the other length leaves a nonzero multiple of α, and α needs only Niven's theorem, because cos 2α is rational. β and γ are evaluated for the statement of the invariant but are not needed for "not zero"; no independence of two angles is needed. Both are tetrahedra, so one evaluation lemma serves both; CLEO was chosen first (three-fold symmetry), AXE followed at little extra cost.
- The polynomial identities over ℚ(√5) (16 corner-face values, the barycentric identities, lengths, Gram numbers) are closed by the tactic `grind` from √5² = 5.

## Not done: FUJI, and what would unlock it
(Done in study 5, `studies/2026-11-19-lean-dehn-5/`: the edge reading for a solid that is not a tetrahedron, the angle relations, and FUJI nonzero.)
1. **Geometry (the real obstruction).** FUJI has 7 faces and 12 edges; six faces meet at one corner and the seventh is a hexagon. `IsTetraData` is for four faces. Needed: an evaluation lemma for a solid given by corners and half-spaces that is not a tetrahedron, namely for each edge "the points of the solid where exactly its two faces are tight are the open segment between its two corners", and that no other set of tight faces has a line as direction space. Cutting FUJI into tetrahedra and using additivity does not avoid this: the cut edges then need their own angle evaluations.
2. **Arithmetic.** Dehn(FUJI) = 1 ⊗ (3γ − 6ε) + ((√5−1)/2) ⊗ 3ε modulo π. The cheap test needs ε ∉ ℚπ. cos 2ε = (4√5 − 5)/15 is irrational, so Niven's theorem in its rational form does not apply. Two ways to unlock it, neither done here:
   - Mathlib has `Real.isIntegral_two_mul_cos_rat_mul_pi` (2 cos of a rational multiple of π is an algebraic integer; found in `NumberTheory/Niven.lean`). Missing lemma: 2 cos 2ε = (8√5 − 10)/15, a root of 45y² + 60y − 44, is not an algebraic integer.
   - Or prove the angle identity ε + α + β = π (it holds to double precision, see Leads); then FUJI is a combination of α and β and the test of item 8 applies with α alone.

## Credits (borrowed lemmas, at the point of use in the files)
Mathlib: `niven` (Niven's theorem, `NumberTheory/Niven.lean`), `Nat.Prime.irrational_sqrt`, `MeasureTheory.Measure.hausdorffMeasure_smul₀`, `MeasureTheory.hausdorffMeasure_segment`, `smul_finsum`, `TensorProduct.smul_tmul'`, `Submodule.exists_dual_map_eq_bot_of_notMem`, `Module.forall_dual_apply_eq_zero_iff`, `InnerProductGeometry.cos_angle_mul_norm_mul_norm`, `Real.cos_three_mul`, `Real.sin_eq_zero_iff`, `Fintype.not_linearIndependent_iff`, `LinearIndependent.fintype_card_le_finrank`, `LinearIndependent.pair_iff'`, `MeasureTheory.Measure.addHaar_submodule`, `Convex.sum_mem`, `convexHull_min`; the tactic `grind`. Studies 1 to 3 of this canon: `dehnSet_image`, `dehnSet_eq_dehn_edgeList`, `not_scissorsCongruent_of_dehnSet_ne`, `theta_pair`, `pair_of_finrank_one`, `dehnSet_cube`, `dehnSet_tetra`. Mathematics: Dehn (1901); Jessen's tensor form; Niven's theorem; that every space-filler has Dehn invariant zero is Debrunner (1980), not used here.

## Sources checked
- Data: corners of AXE, CLEO, FUJI from `studies/2026-10-14-axe-cleo-fuji/nets/pieces.json` (9 digits), identified in ℚ(√5) and then checked exactly (planar faces, edge lengths, cos² of every dihedral angle); the fair 18-face die from `studies/2026-11-18-fair-32-die/data/verts-cr.json` (corners (±1, ±0.4584…, ±0.4584…) and (±0.7292…)(1,1,1), so s = 1, c = 1.4584… = μ√2). The numerical results of `studies/2026-11-19-dehn-words/` (AXE, CLEO nonzero; die cr zero) agree with what is proved here.
- Pinned Mathlib (grep): Hausdorff measure under scaling, Niven's theorem and the algebraic-integer form `Real.isIntegral_two_mul_cos_rat_mul_pi` are there; a Dehn invariant or scissors congruence of polytopes is not (as in study 2).
- Prior Lean work: as listed in study 2's README (FormalBook PR #157). No web search was made in this study. A machine-checked Dehn invariant of a cube ∩ rhombic dodecahedron solid, or of these two tetrahedra: not found in the sources checked.

## `#print axioms` (from `compile.log`)
All 23 theorems listed in `lean/Axioms4.lean` print `[propext, Classical.choice, Quot.sound]`, among them `dehnSet_smul_set`, `similarTetra_not_scissorsCongruent_similarCube`, `dehnSet_sol_eq_zero_of_rational`, `dehnSet_cubeRD`, `dehnSet_fairDie18`, `IsTetraData.dehnSet_eq`, `wordAlpha_not_ratPi`, `dehnSet_cleo`, `dehnSet_cleo_ne_zero`, `cleo_not_scissorsCongruent_cube`, `dehnSet_axe`, `dehnSet_axe_ne_zero`, `axe_not_scissorsCongruent_cube`. No `native_decide`, no added axioms. `grep sorry` over the fifteen files of the chain finds only the header lines that say "No `sorry`".

## Limits of what is stated
Dimension 3. Pieces of a scissors congruence are convex polytopes, finitely many, moved by isometries (reflections included). "Similar copy" allows reflections. CLEO and AXE are the solids with the corners written in `Dehn4Words.lean`. The fair cut μ of the 18-face die is not defined in Lean; the theorem covers every cut. Zero invariant is not shown to imply scissors congruence with a cube.

## Tidy
`studies/2026-11-19-lean-dehn-2/lean/DehnCanon2Gaps.lean` is deleted (here and in the Lean workspace; no file imported it). Study 2's README has a line pointing to study 3.

## Files and how to compile
`lean/Dehn4Similar.lean` (part K), `lean/Dehn4Rational.lean` (part L), `lean/Dehn4Simplex.lean` (part M), `lean/Dehn4Words.lean` (part N), `lean/Axioms4.lean`, `lean/compile_all4.sh`, `compile.log`.
The files import study 3 (`DehnCanon.Dehn3Solids`) and through it studies 1 and 2, all unchanged. Compiled in the Lean workspace of studies 1 to 3, all files in the folder `DehnCanon/`, by `bash DehnCanon/compile_all4.sh` from the workspace root: it compiles the fifteen files of the chain in dependency order, prints the axioms and greps for `sorry`, `native_decide` and `axiom`. The files on the compute host and the copies here have the same SHA-256.

## Leads
- **FUJI**: the evaluation lemma for a solid that is not a tetrahedron (item 1 above) is the one missing piece; it would also give the octahedron, the dodecahedron, the icosahedron and the other fair dice.
- **All three words in two angles (numerical, not proved).** To double precision α + 2β − γ = π and ε = β − γ, so ε + α + β = π. If proved (addition formulas for cos and sin), then modulo π, with g = (√5−1)/2: CLEO = 3 ⊗ α + 3g ⊗ β, AXE = (1 + g) ⊗ α + 6 ⊗ β, FUJI = (9 − 3g) ⊗ α + (12 − 3g) ⊗ β. This is the start of the question of the dehn-words study: which sums of the words cancel.
- Are α and β independent modulo π over ℚ? Needed to decide which combinations of the words are zero; this is beyond Niven's theorem (two angles) and would use `Real.isIntegral_two_mul_cos_rat_mul_pi` or a norm argument in ℚ(√5).
- The rational-normals theorem (item 4) gives Dehn-zero at once for every solid whose face normals come from a family with rational angles: truncated octahedron, rhombic dodecahedron and their cuts. Each needs only its table of normals.
- Does the fair 18-face die fill space? Dehn zero is necessary only (lead of the dehn-words study, unchanged).
- The converse (Sydler): zero invariant and equal volume imply scissors congruent. Not in Lean in the sources checked; a large project.
- For publication: merge the fifteen files into one Lean folder; `two_extreme`, `tmul_add_tmul_ne_zero` and `dehnSet_smul_set` are general.
