# Lean study 9 of the shape-language canon: the same-sign pairs over arccos(1/3), by adding volumes (19 November 2026)

**Question (DICTO's canon, continued from study 8):** the only undecided pairs of nonzero words in the canon were those over θ = arccos(1/3) whose invariants have the same sign (Lucky 7 against the tetrahedron; a cube ∩ octahedron solid with t < 3/2 against the octahedron). Decide them by adding volumes: compute the volumes in Lean, prove that scissors congruence keeps volume, and state the theorem in the form that is meaningful for similar copies.

**Result:** every such pair is decided, with no exceptional t. With study 8's `canon_table`, every pair of different nonzero words in the canon is now decided (`canon_complete`). Two new Lean files (809 lines) compile with Lean v4.35.0-rc2 and the pinned Mathlib. The twenty-nine files of studies 1 to 8 are unchanged. There are no errors, no warnings and no `sorry`, and only the three standard axioms appear (`compile.log`; the whole chain of 31 files was recompiled).

## The argument on paper (worked out first)
Let dehn P = a ⊗ θ and dehn Q = b ⊗ θ. A similar copy of P at scale s has invariant (s a) ⊗ θ, because the invariant is linear in lengths. Its volume is s³ vol P. If a copy sP is scissors congruent to a copy s′Q, both invariants agree. Because θ ∉ ℚπ (study 1), this gives s a = s′ b. Both volumes agree too, so s³ vol P = s′³ vol Q. Eliminating s and s′ gives a³ vol Q = b³ vol P. For a fixed pair of sizes, equal invariant and equal volume are both needed. For similarity classes the meaningful quantity is the scale-free number a³ / vol, which is the same for every similar copy. **So no similar copy of P is scissors congruent to a similar copy of Q as soon as a³ vol Q ≠ b³ vol P**, that is, (a/b)³ ≠ vol P / vol Q. (When the two numbers agree, Sydler (1965) gives scissors-congruent copies. That direction is not used, and it does not occur below.)

The canon over θ (invariants from studies 3 and 7, volumes from this study):

| solid | a (coefficient of θ) | volume | a³ / vol, in units of 2592√2 |
|---|---|---|---|
| tetrahedron (edge 2√2) | 12√2 | 8/3 | 1/2 |
| octahedron \|x\|+\|y\|+\|z\| ≤ 1 | −12√2 | 4/3 | −1 |
| cube ∩ octahedron, 1 < t < 2 | 12√2 (2t − 3) | (4/3)(t³ − 3(t − 1)³) | g(t) = (2t − 3)³ / (t³ − 3(t − 1)³) |

With x = 2t − 3 ∈ (−1, 1), g = 4x³ / (12 + 9x − x³). Its derivative has the sign of 9(2t − 1)(2t − 3)² ≥ 0, so g increases strictly from g(1) = −1 (at t = 1 the solid is the octahedron) to g(2) = 1/5 (the cuboctahedron). Therefore:
- **Against the tetrahedron (1/2):** g < 1/5 < 1/2 on the whole line. Exactly: 2(2t − 3)³ − (t³ − 3(t − 1)³) = −3 + 9(t − 1)(t − 2)(2t − 3), and |(t − 1)(t − 2)(2t − 3)| < 1/3 on (1, 2).
- **Against the octahedron (−1):** g = −1 only at t = 1, the octahedron itself. Exactly: (2t − 3)³ + t³ − 3(t − 1)³ = 3(t − 1)(2t² − 7t + 8) > 0 for t > 1.
- **Two members of the line:** x³(12 + 9y − y³) − y³(12 + 9x − x³) = (x − y)(12(x² + xy + y²) + 9xy(x + y)), and the second factor is positive on (−1, 1)² apart from (0, 0). For xy ≥ 0 it is ≥ 6(x − y)² + 6x² + 6y². For xy < 0 it is ≥ 12(x + y)² − 3xy, because |x + y| < 1.
- **Lucky 7** (t = 1.756582…, the value `mu_f` in `studies/2026-11-18-fair-32-die/data/co.log`): g = 0.0328 (floats), far from the tetrahedron's 1/2. It is covered by its interval 7/4 < t < 9/5 and also by every t in (1, 2).

**No exceptional t exists:** within the family, the scale-free number a³/vol separates every two different solids.

## Proved in Lean (theorem names, statements)

### 1. Volumes (`lean/Dehn9Vol.lean`, part AC)
- `volume_iUnion_poly`: **volume is additive over a dissection into convex polytopes** with pairwise disjoint interiors. The boundary of a convex set is null (Mathlib `Convex.addHaar_frontier`), so each piece has the volume of its interior. The interiors are disjoint open sets.
- `volume_image_isometry`, `volume_eq_of_scissorsCongruent`: **scissors congruence (study 2's definition) keeps volume.** Study 2's definition already has the two conditions needed, convex pieces and disjoint interiors, so this came cheaply.
- `volume_similar`: volume (g '' (a • P)) = a³ · volume P.
- `volume_oct`: **volume octSet = 4/3**.
- `volume_tetra`: **volume tetraSet = 8/3**.
- `volume_co`: **for 1 ≤ t < 2, volume (coSet t) = (4/3)(t³ − 3(t − 1)³)**.
```lean
theorem volume_co {t : ℝ} (ht1 : 1 ≤ t) (ht2 : t < 2) :
    volume (coSet t) = ENNReal.ofReal (4 / 3 * (t ^ 3 - 3 * (t - 1) ^ 3))
```

### 2. The pairs (`lean/Dehn9Same.lean`, part AD)
```lean
theorem not_scissorsCongruent_of_cube_ne {P Q P' Q' : Set R3} {a b V W : ℝ}
    (hP : IsPoly P) (hQ : IsPoly Q)
    (ha : dehnSet P = edgeTerm a tetDihedral) (hb : dehnSet Q = edgeTerm b tetDihedral)
    (hV : volume P = ENNReal.ofReal V) (hW : volume Q = ENNReal.ofReal W) (hV0 : 0 ≤ V) (hW0 : 0 ≤ W)
    (hne : a ^ 3 * W ≠ b ^ 3 * V)
    (hP' : IsSimilarCopy P P') (hQ' : IsSimilarCopy Q Q') : ¬ ScissorsCongruent P' Q'
```
- `co_tetra_not_scissorsCongruent'`: **every cube ∩ octahedron solid, 1 < t < 2, against the tetrahedron.** Study 7 covered only t < 3/2.
- `co_oct_not_scissorsCongruent'`: **every one, 1 < t < 2, against the octahedron.** Study 7 covered only t > 3/2.
- `co_co_not_scissorsCongruent`: **two different members s ≠ t of the line.**
- `luckySeven_tetra_not_scissorsCongruent`: **Lucky 7 (7/4 < t < 9/5) against the tetrahedron**, the pair named in study 8's Leads.
- `oct_tetra_not_scissorsCongruent'`: the octahedron against the tetrahedron again, now by volume (study 7 used the signs).
- `canon_tet_not_scissorsCongruent`: **any two different solids of study 8's `TetFamily`**, for similar copies in any sizes and positions.
- `canon_complete`: **study 8's `canon_table` with a fourth part.** For similar copies: nonzero against zero; the α–β family pairwise; θ against α–β; and now θ against θ. Every pair of different nonzero words in the canon is decided.
- The arithmetic lemmas: `cond_co_tetra`, `cond_co_oct`, `cond_oct_tetra`, `line_factor_pos`, `cond_co_co`.

## Method
- **Volumes: the cheapest route.** Mathlib has no volume of a simplex or a convex hull. It does have the volume of the unit ball of the ℓᵖ norm in ℝⁿ (`volume_sum_rpow_le`, `volume_sum_rpow_lt`, through the Gamma function). For p = 1 and n = 3 this is the octahedron, (4/3) r³. Everything else is cut from it, using only measure-preserving coordinate maps and null planes:
  - *Half by symmetry* (`vol_half`): reflecting one coordinate keeps volume (`measurePreserving_pi` with `Measure.measurePreserving_neg`), and a coordinate plane is null (`Measure.pi_hyperplane`). So a set that is symmetric in that coordinate has half its volume on each side.
  - *Corner simplex* (`vol_corner`): three halvings of the open ball of radius 2 give {u ≥ 0, u₀ + u₁ + u₂ < 2}, with volume 4/3.
  - *Tetrahedron:* the cube [−1, 1]³ (`Real.volume_Icc_pi`, volume 8) less four corner simplices. Each is the simplex above under x ↦ (1 − vⱼ xⱼ), which keeps volume (`measurePreserving_sub_left`, `measurePreserving_add_left`). The result is 8 − 16/3 = 8/3.
  - *Cube ∩ octahedron:* the ball of radius t less six caps {±xᵢ > 1}. For t < 2 the caps are disjoint. Each cap is a translate (`measurePreserving_sub_right`) or a reflection of half a ball of radius t − 1. The result is (4/3) t³ − 6 · (2/3)(t − 1)³.
  - Sets in 3-space (`EuclideanSpace ℝ (Fin 3)`) are moved to `Fin 3 → ℝ` by `PiLp.volume_preserving_ofLp`. Each half-space solid of studies 2, 3 and 7 is shown equal to its coordinate description (|x|+|y|+|z| ≤ 1, and so on) from its normals.
- **Volume of a scissors congruence.** Each piece is a closed convex polytope. Its boundary is null (`Convex.addHaar_frontier`), and the interiors are pairwise disjoint and open (`measure_iUnion`). An affine isometry is a linear isometry (`LinearIsometryEquiv.measurePreserving`) followed by a translation (`measure_preimage_add_right`).
- **Similar copies.** Study 4's `dehnSet_smul_set` and study 2's `dehnSet_image`, Mathlib's `Measure.addHaar_smul`, and study 1's `edgeTerm_inj` (θ ∉ ℚπ) give s a = s′ b. Then a single `linear_combination` gives s′³ (a³ W − b³ V) = 0.
- **Checks first** (`checks/vol_check.py`, output `checks/vol_check.out`, exact fractions, run on the compute host). The script computes volumes from corners and face planes for the tetrahedron (8/3), the octahedron (4/3) and the line at six rational t (all equal to the formula). It checks the four polynomial identities and K > 0 on a 99 × 99 grid. It also prints g(1) = −1, g(3/2) = 0 and g(2) = 1/5, the values 1/2 and −1 for the tetrahedron and octahedron, g increasing on a grid of 1001 points, and the Lucky 7 values as floats.

## Credits (borrowed lemmas, at the point of use in the files)
Mathlib: `MeasureTheory.volume_sum_rpow_le`, `MeasureTheory.volume_sum_rpow_lt` (volume of the ℓᵖ ball), `Real.Gamma_two`, `Real.Gamma_nat_eq_factorial`, `Measure.pi_hyperplane`, `measurePreserving_pi`, `Measure.measurePreserving_neg`, `Measure.measurePreserving_sub_left`, `measurePreserving_add_left`, `measurePreserving_sub_right`, `measure_preimage_add_right`, `Set.image_add_right`, `Real.volume_Icc_pi`, `PiLp.volume_preserving_ofLp`, `measure_iUnion`, `measure_iUnion_null`, `measure_inter_add_sdiff`, `Convex.addHaar_frontier`, `closure_eq_interior_union_frontier`, `LinearIsometryEquiv.measurePreserving`, `LinearIsometryEquiv.image_eq_preimage_symm`, `AffineIsometryEquiv.map_vadd`, `Measure.addHaar_smul`, `finrank_euclideanSpace_fin`, `ENNReal.ofReal_eq_ofReal_iff`; the tactics `linear_combination`, `nlinarith`, `fin_cases`. Studies 1 to 8 of this canon: `edgeTerm`, `edgeTerm_inj`, `tetDihedral_not_ratPi` (1); `ScissorsCongruent`, `dehnSet_eq_of_scissorsCongruent`, `IsPoly`, `dehnSet_image`, `IsPoly.image`, `tetraSet`, `inner3` (2); `dehnSet_tetra` (3); `dehnSet_smul_set`, `IsPoly.smul_set`, `IsSimilarCopy` (4); `octSet`, `oct_ineqs`, `dehnSet_oct`, `coSet`, `co_ineqs`, `dehnSet_co`, `isPoly_co`, `smul_edgeTerm`, `dehnSet_tetra_tet` (7); `TetFamily`, `ABFamily`, `abWord`, `canon_table` (8). Mathematics: Dehn (1901), with volume as the second invariant (classical); Sydler (1965), quoted and not used.

## Sources checked
- First, DICTO's own papers and their reference lists: `papers/2026-11-19-dehn-canon/paper.html` (§7 Proposition 14, §10, references [1]–[19]: Dehn, Sydler, Jessen, Conway–Radin–Sadun, Ogievetsky–Papadopolos, Debrunner, Lagarias–Moews, Calegari); studies 1 to 8 of this canon (READMEs and Lean files); `studies/2026-11-18-fair-32-die/data/co.log` (Lucky 7's t).
- Our reference library (349 PDF files, file names searched for Sydler, Dehn, Hadwiger, Boltianskii, Jessen, scissors, equidecomposition). Hits: Conway–Radin–Sadun 1999 (text searched for volume and Sydler: they cite the Dehn–Sydler criterion and apply it to Archimedean solids, but give no volume comparison of this kind); Ogievetsky–Papadopolos 1999 (volumes and Dehn invariants of their golden tetrahedra, on another family); Papadopolos–Ogievetsky (inflation rules); Baumbach 2025 (canonical form and scissors congruence, not about this question).
- Pinned Mathlib (grep): the volume of a simplex or of a convex hull was not found. `Equidecomp` exists only for group actions, not for measure. The ℓᵖ-ball volume is present and used. `Convex.addHaar_frontier` is present and used.
- One web search (a Lean or Mathlib formalisation of polytope volume or of volume under scissors congruence). Results: [Hilbert's 3rd Problem and invariants of 3-manifolds](https://arxiv.org/pdf/math/9712226), [The canonical form, scissors congruence and adjoint degrees of polytopes](https://arxiv.org/html/2508.04275v1), [MIT 18.701 notes](https://ocw.mit.edu/courses/res-18-011-algebra-i-student-notes-fall-2021/mit18_701f21_lec35.pdf), [Encyclopedia of Mathematics, Dehn invariant](https://encyclopediaofmath.org/wiki/Dehn_invariant), [Wikipedia, Hilbert's third problem](https://Www.Wikipedia.org/wiki/Scissors-congruent). These are background only, with no formal proof.
- In the sources checked, none of the following was found: a machine-checked proof that scissors congruence keeps volume, the volumes of these solids in Lean, or these same-sign non-congruences.

## `#print axioms` (from `compile.log`)
All 21 theorems in `lean/Axioms9.lean` print `[propext, Classical.choice, Quot.sound]`. Among them are `volume_eq_of_scissorsCongruent`, `volume_oct`, `volume_tetra`, `volume_co`, `not_scissorsCongruent_of_cube_ne`, `co_tetra_not_scissorsCongruent'`, `co_oct_not_scissorsCongruent'`, `co_co_not_scissorsCongruent`, `luckySeven_tetra_not_scissorsCongruent`, `canon_tet_not_scissorsCongruent` and `canon_complete`. There is no `native_decide` and no added axiom. `grep sorry` over the thirty-one files of the chain finds only the header lines that say "No `sorry`".

## Limits of what is stated
- As in studies 2 to 8: dimension 3. The pieces of a scissors congruence are convex polytopes, finitely many, moved by isometries (reflections included). The solids are the half-space solids of studies 2, 3 and 7. Zero invariant is not shown to imply scissors congruence (Sydler's direction).
- `volume_co` is proved for 1 ≤ t < 2 (the caps are disjoint only for t < 2). The cuboctahedron at t = 2 is outside it and is not in the canon.
- Lucky 7's t is numerical (study of 18 November). The theorems hold for every t in (1, 2), and for the interval (7/4, 9/5).

## Files and how to compile
`lean/Dehn9Vol.lean` (part AC), `lean/Dehn9Same.lean` (part AD), `lean/Axioms9.lean`, `lean/compile_all9.sh`, `compile.log`; `checks/vol_check.py` and `checks/vol_check.out`. The files import study 8 (`DehnCanon.Dehn8Cross`) and through it studies 1 to 8, all unchanged. They are compiled in the Lean workspace of studies 1 to 8, with all files in the folder `DehnCanon/`, by `bash DehnCanon/compile_all9.sh` from the workspace root. For short runs the script takes a part argument (1, 2, 3, 4, 5, check). `compile.log` is the six runs in order. The files on the compute host and the copies here have the same SHA-256.

## LEADS
- **The paper.** §10's last open pair class closes. In Figure 2 the θ family can be joined pairwise. Proposition 14 becomes "the arccos(1/3) family is pairwise apart" (`canon_tet_not_scissorsCongruent`), with the scale-free number a³/vol and the table above. Not done here: the paper is outside this study's scope.
- **Volume for the other solids.** The same route (ℓ¹ ball, halving, corner simplices, translates) gives every solid of the cube and octahedron directions. A general Lean volume for convex polytopes (a fan from an interior point) would reach the α–β family. That family is already decided without volume.
- **The ten other fair dice** (from earlier studies): over θ, each needs only its invariant and volume to join this table. The scale-free number a³/vol decides it against all the solids here.
- From earlier studies, unchanged: convex hulls; Sydler's converse; one Lean folder for publication (now thirty-one files).
