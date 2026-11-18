# Lean study 5 of the shape-language canon: the three words finished (19 November 2026)

**Question (DICTO's canon, continued from studies 1 to 4):** study 4 proved that CLEO and AXE are nonzero words and left FUJI open, with a numerical lead: α + 2β − γ = π and ε = β − γ. (1) Prove the angle relations. (2) Write the three words over the two angles α, β. (3) An edge reading for a solid that is not a tetrahedron. (4) FUJI's Dehn invariant is not zero. (5) Bonus: can two of the words be scissors congruent to each other?

**Result:** (1) to (4) are proved. The numerical lead is right. (5) is proved only under a stated hypothesis (α and β independent modulo π), which is not proved in Lean. Four new Lean files (1,297 lines) compile with Lean v4.35.0-rc2 and the pinned Mathlib, with the fifteen files of studies 1 to 4 unchanged: no errors, no warnings, no `sorry`, only the three standard axioms (`compile.log`).

## Proved in Lean (theorem names, statements)

### 1. The angle relations (`lean/Dehn5Angles.lean`)
α = arccos(1/√5) = 63.43…°, β = 79.18…° (cos² β = 1/3 − 2√5/15), γ = arccos(√5/3) = 41.81…° as in study 4; ε = arccos((√5 + 1)/√(3(10 − 2√5))) = 37.37…° (cos² ε = 1/3 + 2√5/15).
- `wordBeta_eq_gamma_add_eps`: β = γ + ε. `wordEps_eq`: **ε = β − γ**.
- `wordAlpha_add_wordBeta`: α + β = π − ε. `word_angle_sum`: α + β + ε = π.
- `word_angle_relation`: **α + 2β − γ = π**.

These are equalities of real numbers, not only modulo π.

### 2. The three words over α and β (`lean/Dehn5Fuji.lean`)
With g = (√5 − 1)/2, in ℝ ⊗ (ℝ/ℚπ):
- `dehn_cleo_alpha_beta`: CLEO = 3 ⊗ α + 3g ⊗ β.
- `dehn_axe_alpha_beta`: AXE = (1 + g) ⊗ α + 6 ⊗ β.
- `dehn_fuji_alpha_beta`: FUJI = (9 − 3g) ⊗ α + (12 − 3g) ⊗ β.

The three forms of the lead of study 4 are correct as written there.

### 3. The edge reading for a solid that is not a tetrahedron (`lean/Dehn5Edges.lean`)
- `IsEdgeData n b p fi fj vk vl`: faces (normals n, offsets b), corners p, and a list of edges, each with its two faces and its two corners. The conditions are finite facts about the table "which face passes through which corner", and one fact about points, `cover`: a point of the solid on two different faces lies on the closed segment of an edge with these two faces, or is a corner.
- `IsEdgeData.faceSet_edge`: for each edge, the points of the solid where exactly its two faces are tight are the open segment between its two corners.
- `IsEdgeData.faceSet_subset_corners`: any other set of faces whose common direction space is a line is tight only at corners. So there are no other wedge points.
- `IsEdgeData.dehnSet_eq` (**the edge reading**):
```lean
theorem IsEdgeData.dehnSet_eq [Fintype ι] [Nonempty ι] [Finite κ] [Fintype ε]
    (h : IsEdgeData n b p fi fj vk vl) :
    dehnSet (sol n b) = ∑ e, dist (p (vk e)) (p (vl e)) ⊗ₜ[ℚ] theta (cone n ({fi e, fj e} : Set ι))
```
- Two lemmas prove `cover` for a concrete solid. `mem_segment_of_tight` (the two faces of an edge): a third face through the second corner only, whose normal is independent of the two, gives the position along the line of the two faces; a fourth face through the first corner only bounds it on the other side. `eq_of_tight` (two faces that share only a corner P): if two more faces c, c′ through P satisfy n_c + μ n_c′ = a n_i + a′ n_j with μ > 0, then P is the only point of the solid on both faces.

The solid need not be simple: any number of faces may meet at a corner, and three faces with dependent normals are allowed.

**Choice made, and why.** Study 4's `IsTetraData` was not generalised. It rests on barycentric coordinates, one face opposite each corner, which only a simplex has. The new structure does the same job edge by edge, with a coordinate along each edge. `IsTetraData` and its two uses (CLEO, AXE) are kept unchanged.

### 4. FUJI (`lean/Dehn5Fuji.lean`)
- `fujiSet`: FUJI as the intersection of its seven face half-spaces; corners and normals in ℚ(√5), exact form of the corner data of the study of 14 October. `fuji_isEdgeData`: its 7 corners, 7 faces and 12 edges satisfy `IsEdgeData`. `fuji_faceSet_edge`: its twelve open edges. `isPoly_fuji`.
- `dehnSet_fuji`: `dehnSet fujiSet = dehn fujiEdges`: six edges of length 1 at α + β (the six edges at the apex; α + β = π − ε), three edges of length 1 at γ and three edges of length g at ε (the hexagon, alternating).
- `dehnSet_fuji_ne_zero` (**FUJI is a nonzero word**).
- `fuji_not_scissorsCongruent_cube`, `fuji_not_scissorsCongruent_cubeRD`: no similar copy of FUJI is scissors congruent to a similar copy of the cube, nor of any cube ∩ rhombic dodecahedron solid, the fair 18-face die among them.
```lean
theorem fuji_not_scissorsCongruent_cube {C Q : Set R3} (hC : IsSimilarCopy fujiSet C)
    (hQ : IsSimilarCopy (cubeSet 1) Q) : ¬ ScissorsCongruent C Q
```
No independence of α and β is needed for "not zero": 9 − 3g is not a rational multiple of 12 − 3g (`fuji_lengths_indep`, from √5 irrational), so study 4's `tmul_add_tmul_ne_zero` applies with α alone, and α needs only Niven's theorem (study 4's `wordAlpha_not_ratPi`).

### 5. Two words against each other: conditional (`lean/Dehn5Pairs.lean`)
- `WordAnglesIndep` (a hypothesis, **not proved in Lean**): modulo π, α is not a rational multiple of β and β is not a rational multiple of α. Equivalently α, β, π are linearly independent over ℚ.
- `not_proportional`: for two angle classes independent in this sense and a d ≠ b c, no real multiple of a ⊗ θ₁ + b ⊗ θ₂ equals c ⊗ θ₁ + d ⊗ θ₂.
- `cleo_axe_not_proportional`, `cleo_fuji_not_proportional`, `axe_fuji_not_proportional`: under `WordAnglesIndep`, no real multiple of the invariant of one word is the invariant of another (the three determinants are 15, 45 − 45g, 30g − 45, none zero).
- `cleo_axe_not_scissorsCongruent`, `cleo_fuji_not_scissorsCongruent`, `axe_fuji_not_scissorsCongruent`: under `WordAnglesIndep`, no similar copy of one word is scissors congruent to a similar copy of another.

Without the hypothesis nothing is decided: if β were a rational multiple of α modulo π, the three invariants would all be real multiples of 1 ⊗ α. So the answer to the bonus question is not a theorem here. It is "no two are compatible" exactly if the hypothesis holds; see Leads for an argument by hand that it does.

## Method
- **Angles.** With r = √(3(10 − 2√5)): cos β = (3 − √5)/r, sin β = 4/r, cos ε = (√5 + 1)/r, sin ε = (2√5 − 2)/r; cos α = √5/5, sin α = 2√5/5; cos γ = √5/3, sin γ = 2/3. The addition formula gives cos(γ + ε) = cos β and cos(α + β) = −cos ε. Each of the four angles lies in [0, π/2] because its cosine is ≥ 0, so both sums lie in [0, π], where arccos ∘ cos is the identity. No comparison of two angles is needed. Before the proof the relations were checked to 120 digits (`checks/angles_check.py`, square roots only).
- **Edge reading.** Study 2 gives the invariant as a sum over all sets A of faces: (length of the set of points where exactly the faces of A are tight) ⊗ (angle class of their cone), and the term is zero unless the common direction space of A is a line. Then A has two different faces; by `cover` the points concerned lie on an edge segment or are corners; the points inside the segment have exactly the two faces of that edge tight; finitely many corners have length zero.
- **FUJI.** The table of the 49 values b_m − ⟨n_m, p_k⟩ (zero or positive) is proved by `grind` and `linarith`; from it all finite conditions are `decide` on a table of Booleans. `cover` is 21 cases, one for each pair of faces: the 12 pairs of an edge by `mem_segment_of_tight`, the 9 pairs of triangles that share only the apex by `eq_of_tight`. Three triples of normals are dependent (two opposite triangles and the hexagon); the certificates avoid them. Boundedness: each coordinate is bounded by a combination with coefficients ≥ 0 of three face inequalities. The angles of the three kinds of edges come from the Gram numbers of the normals (study 4's `theta_pair_of_gram`).
- The certificate numbers (third and fourth face for each edge, determinants, the relations for the nine apex pairs, the bounding combinations) were computed exactly in ℚ(√5) on the compute host (`checks/fuji2.py`, exact fractions, no floating point in the certificates) and are all checked by Lean.
- **Not zero.** As in study 4: a ℚ-linear map ℝ → ℚ on lengths that kills 12 − 3g and not 9 − 3g leaves a nonzero multiple of α.

Exact edge data of FUJI (from `checks/fuji1.out`): faces 0, 3, 5 are triangles with sides 1, 1, 1, faces 1, 2, 4 triangles with sides 1, 1, g, face 6 the hexagon with sides 1, g, 1, g, 1, g.

| edges | number | length | angle |
|---|---|---|---|
| at the apex, between two neighbouring triangles | 6 | 1 | α + β = π − ε = 142.62…° |
| hexagon with a triangle 1, 1, 1 | 3 | 1 | γ = 41.81…° |
| hexagon with a triangle 1, 1, g | 3 | g | ε = 37.37…° |

## Credits (borrowed lemmas, at the point of use in the files)
Mathlib: `Real.cos_arccos`, `Real.sin_arccos`, `Real.arccos_cos`, `Real.arccos_neg`, `Real.arccos_le_pi_div_two`, `Real.cos_add`, `mem_openSegment_of_ne_left_right`, `Set.Finite.measure_zero`, `Finset.sum_subset`, `Finset.sum_image`, `List.sum_ofFn`, `TensorProduct.smul_tmul'`, `TensorProduct.lift`, `TensorProduct.inductionOn`, `Submodule.exists_dual_map_eq_bot_of_notMem`, `Nat.Prime.irrational_sqrt`, `convexHull_min`; the tactic `grind`. Studies 1 to 4 of this canon: `dehnSet_eq_dehn_edgeList`, `finrank_linCone_ne_one_of_subsingleton`, `theta_pair_of_gram`, `hausdorff_openSegment`, `dehnSet_eq_sum_faceSet`, `tmul_add_tmul_ne_zero`, `wordAlpha_not_ratPi` (Niven's theorem `niven`), `not_scissorsCongruent_similarCopies`, `dehnSet_cube`, `dehnSet_cubeRD`, `dehnSet_cleo`, `dehnSet_axe`. Mathematics: Dehn (1901); Jessen's tensor form; Niven's theorem.

## Sources checked
- Data: corners and faces of FUJI from `studies/2026-10-14-axe-cleo-fuji/nets/pieces.json` (9 digits), identified in ℚ(√5) (`checks/fuji1.py`), then checked exactly: planar faces, all corners on the inner side of all faces, edge lengths, Gram numbers. The numerical result of `studies/2026-11-19-dehn-words/` and the table of study 4 (FUJI: 6 × 1 at π − ε, 3 × 1 at γ, 3 × g at ε) agree with what is proved here.
- Pinned Mathlib (grep): a Dehn invariant or scissors congruence: not found. Polytopes appear only in `Analysis/Convex/Exposed.lean`, `Analysis/Normed/Affine/Convex.lean`, `Order/Grade.lean` and Coxeter matrices; an edge list or face lattice of a polytope given by half-spaces: not found. Independence over ℚ of arccos values and π: not found (`NumberTheory/Niven.lean` has Niven's theorem and `isIntegral_two_mul_cos_rat_mul_pi`).
- No web search was made in this study. A machine-checked Dehn invariant of this solid, or these angle relations in Lean: not found in the sources checked.

## `#print axioms` (from `compile.log`)
All 28 theorems listed in `lean/Axioms5.lean` print `[propext, Classical.choice, Quot.sound]`, among them `word_angle_relation`, `wordEps_eq`, `IsEdgeData.dehnSet_eq`, `fuji_isEdgeData`, `dehnSet_fuji`, `dehn_cleo_alpha_beta`, `dehn_axe_alpha_beta`, `dehn_fuji_alpha_beta`, `dehnSet_fuji_ne_zero`, `fuji_not_scissorsCongruent_cube`, `fuji_not_scissorsCongruent_cubeRD`, and the conditional theorems of part 5 (their hypothesis `WordAnglesIndep` is an explicit argument, not an axiom). No `native_decide`, no added axioms. `grep sorry` over the nineteen files of the chain finds only the header lines that say "No `sorry`".

## Limits of what is stated
- Dimension 3; pieces of a scissors congruence are convex polytopes, finitely many, moved by isometries (reflections included), as in studies 2 to 4.
- FUJI is the solid cut out by the seven half-spaces written in `Dehn5Fuji.lean`. Proved: the seven corners lie in it (`convexHull_fujiP_subset`), and its edges are exactly the twelve segments. Not proved as a Lean statement: that it equals the convex hull of the seven corners.
- Part 5 is conditional on `WordAnglesIndep`.
- Zero invariant is not shown to imply scissors congruence with a cube (Sydler's direction), as before.

## Files and how to compile
`lean/Dehn5Angles.lean` (part O), `lean/Dehn5Edges.lean` (part P), `lean/Dehn5Fuji.lean` (part Q), `lean/Dehn5Pairs.lean` (part R), `lean/Axioms5.lean`, `lean/compile_all5.sh`, `compile.log`; `checks/` (the exact computations and their outputs; `gen_cover_lemmas.py` wrote the text of the 21 independence lemmas and the 21 cover lemmas from those numbers).
The files import study 4 (`DehnCanon.Dehn4Words`) and through it studies 1 to 3, all unchanged. Compiled in the Lean workspace of studies 1 to 4, all files in the folder `DehnCanon/`, by `bash DehnCanon/compile_all5.sh` from the workspace root: it compiles the nineteen files of the chain in dependency order, prints the axioms and greps for `sorry`, `native_decide` and `axiom`. The files on the compute host and the copies here have the same SHA-256.

## Leads
- **Independence of α and β modulo π (by hand, not machine-checked).** e^{2iα} = (−3 + 4i)/5 and e^{2iβ} = (−(5 + 4√5) + (10 − 2√5)i)/15 lie in ℚ(√5, i) (sin 2β = (10 − 2√5)/15 is checked by the values of part 1). 2 cos 2β = −(10 + 8√5)/15 is not integral at 3 (3 stays prime in ℚ(√5), and 10 + 8√5 is not divisible by 3), so e^{2iβ} has nonzero valuation at a prime above 3, while e^{2iα} is a unit there. A relation mα + nβ ∈ ℚπ then forces n = 0, and Niven's theorem forces m = 0. If this is put in Lean (valuations in a biquadratic field, or a norm argument), `WordAnglesIndep` becomes a theorem and part 5 is unconditional: no two of the three words, in any sizes, are scissors congruent.
- **Which sums of words cancel** (the question of the dehn-words study). With independence, a combination x CLEO + y AXE + z FUJI of similar copies (scale factors x, y, z > 0) has invariant zero exactly if 3x + (1 + g)y + (9 − 3g)z = 0 and 3g x + 6y + (12 − 3g)z = 0. All six coefficients are positive, so no combination of positive copies cancels; the words alone cannot build a solid of invariant zero. This is a remark by hand, not a Lean statement here.
- The edge reading `IsEdgeData.dehnSet_eq` is ready for the octahedron, the dodecahedron, the icosahedron and the fair dice: each needs its corner-face table and one certificate for each pair of faces.
- A general proof of `cover` from the corner-face table alone (so that the 21 cases are not written out) would need "the solid is the convex hull of its corners"; not done.
- From study 4, unchanged: the rational-normals theorem for more solids; Sydler's converse; one Lean folder for publication (now nineteen files).
