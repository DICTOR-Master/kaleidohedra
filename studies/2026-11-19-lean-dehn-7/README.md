# Lean study 7 of the shape-language canon: the rest of the canon on top of Dehn's theorem (19 November 2026)

**Question (DICTO's canon, continued from studies 1 to 6):** with study 5's edge reading `IsEdgeData.dehnSet_eq`, put the rest of the canon into Lean. In order: (1) the zero words: both golden rhombohedra, the rhombic triacontahedron, the truncated octahedron, the rhombic dodecahedron, the cube; (2) the nonzero words: dodecahedron, icosahedron, octahedron; (3) the fair dice: Lucky 7 (cube ∩ octahedron, 14 faces) and others cheaply in reach; (4) if cheap, a table placing each word in the canon, for proved pairs only.

**Result:** (1), (2) and (3) for Lucky 7 are proved, and (4) for the pairs listed below. Six new Lean files (7,462 lines, most of them generated certificates) compile with Lean v4.35.0-rc2 and the pinned Mathlib, with the twenty-one files of studies 1 to 6 unchanged: no errors, no warnings, no `sorry`, only the three standard axioms (`compile.log`; the whole chain of 27 files was recompiled).

**A correction to the question.** The question says that the golden rhombohedra and the rhombic triacontahedron have dihedral angles that are not all rational multiples of π. They are all rational multiples of π. Every face normal of these three solids is a two-fold axis of the icosahedral group, and any two two-fold axes make an angle of 0°, 36°, 60°, 72°, 90°, 108°, 120°, 144° or 180°. So the dihedral angles are 72° and 108° (prolate rhombohedron), 36° and 144° (oblate rhombohedron) and 144° (triacontahedron). The cheapest Lean route is therefore study 4's `dehnSet_sol_eq_zero_of_rational`. No edge list is needed, and no argument about tiling or parallel edges. The parallel-edge pairing (θ and π − θ on parallel edges of equal length) is also true, but it would need a full edge list for each solid.

## Proved in Lean (theorem names, statements)

### 1. Zero words from rational angles (`lean/Dehn7Gold.lean`, part U)
- `mem_ratPi_of_cos_gold`: if 4c² − 2sc − 1 = 0 with s = ±1 and c = cos θ (so c = (±1 ± √5)/4), then θ is a rational multiple of π. Proof: cos 5θ = ±1 (`cos_five_mul`).
- `rtN`: the 30 two-fold directions, with coordinates in ℤ[√5]: ±4eᵢ, and the cyclic permutations of (±(√5 − 1), ±(√5 + 1), ±2). `rtN_angle`: any two of them make an angle that is a rational multiple of π. This is checked by a Gram table over ℤ[√5] (900 pairs, `decide +kernel`).
- `dehnSet_rtFamily`: **every solid cut out by half-spaces whose normals are two-fold directions of the icosahedral group has Dehn invariant zero**, for any choice of directions and offsets.
```lean
theorem dehnSet_rtFamily {ι : Type} [Finite ι] (f : ι → Fin 30) (b : ι → ℝ) :
    dehnSet (sol (fun i => rtN (f i)) b) = 0
```
- `dehnSet_rt`: the rhombic triacontahedron `rtSet r` (its 30 faces at one distance) is a zero word.
- `goldProlateSet_eq`, `goldOblateSet_eq`: each golden rhombohedron, given as six half-spaces from the 30 directions, **equals the parallelepiped {a u + b v + c w : a, b, c ∈ [0, 1]}** on three five-fold axes u, v, w. These are icosahedron corners of squared length (5 + √5)/2 (`gold_edge_vectors`). For the prolate rhombohedron the three inner products are all φ (pairwise arccos(1/√5)). For the oblate one they are φ, −φ, φ. The proof uses a general lemma `mem_parallelepiped_iff` (dual normals, no common perpendicular direction).
- `dehnSet_goldProlate`, `dehnSet_goldOblate`: both golden rhombohedra are zero words.
- `dehnSet_crFamily`, `dehnSet_rd`: the same for the 18 directions of study 4. The rhombic dodecahedron `rdSet c` (|xᵢ ± xⱼ| ≤ c, 12 faces) is a zero word. The cube is study 3's `dehnSet_cube`.

### 2. The octahedron (`lean/Dehn7Octa.lean`, part V)
- `two_octDelta`: 2 · arccos(1/√3) = π − arccos(1/3). `arccos_neg_third`: arccos(−1/3) = π − arccos(1/3).
- `oct_isEdgeData`: the octahedron |x| + |y| + |z| ≤ 1 (8 faces, 6 corners, 12 edges) satisfies `IsEdgeData`.
- `dehnSet_oct`: **dehnSet octSet = (−12√2) ⊗ arccos(1/3)**. There are twelve edges of length √2, each at π − arccos(1/3).
- `dehnSet_oct_ne_zero`: **the octahedron is a nonzero word**. The proof is Niven's theorem, as for the tetrahedron.

### 3. The cube ∩ octahedron line: the truncated octahedron and Lucky 7 (`lean/Dehn7CubeOct.lean`, part W)
`coSet t` = {|xᵢ| ≤ 1, |x| + |y| + |z| ≤ t}. For 1 < t < 2 it has 6 squares, 8 hexagons, 24 corners (the permutations of (±1, ±(t − 1), 0)) and 36 edges.
- `co_isEdgeData`: `IsEdgeData` for every 1 < t < 2, with t as a variable.
- `dehnSet_co`: **the Dehn invariant of the whole line**:
```lean
theorem dehnSet_co {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) :
    dehnSet (coSet t) = edgeTerm (12 * √2 * (2 * t - 3)) tetDihedral
```
  The 24 square–hexagon edges have length √2 (t − 1) and angle π − arccos(1/√3). The 12 hexagon–hexagon edges have length √2 (2 − t) and angle π − arccos(1/3). By `two_octDelta` the two kinds of edges cancel exactly when their lengths are equal.
- `dehnSet_truncOct`: **the truncated octahedron (t = 3/2, corners the permutations of (±1, ±1/2, 0)) is a zero word**. Its two dihedral angles are not rational multiples of π, so study 4's theorem does not apply. The zero comes from the edge reading and the angle relation.
- `dehnSet_co_ne_zero`: every other member of the line is a nonzero word.
- `dehnSet_luckySeven_ne_zero`: **every member with 7/4 < t < 9/5 is a nonzero word**. The fair 14-face die Lucky 7 is the member t = 1.7566… (from `studies/2026-11-18-fair-32-die/`: corners (1, 0.75658…, 0) in `data/verts-co.json`, bracket (1.75, 1.8) in `data/co.log`). That value is numerical there and was not computed in Lean.

### 4. The dodecahedron (`lean/Dehn7Dodeca.lean`, part X)
- `false_of_comb`: how `cover` is proved for two faces with no common point, by a Farkas certificate a nᵢ + a′ nⱼ = μ₁ n_c₁ + μ₂ n_c₂ + μ₃ n_c₃, μ ≥ 0, Σ μ b_c < a bᵢ + a′ bⱼ.
- `dod_isEdgeData`: the dodecahedron with corners (±2, ±2, ±2) and the cyclic permutations of (0, ±(1 + √5), ±(√5 − 1)) (12 faces, 20 corners, 30 edges of length 2√5 − 2) satisfies `IsEdgeData`.
- `dehnSet_dod`: **dehnSet dodSet = (−30 (2√5 − 2)) ⊗ α**, with α = arccos(1/√5) (study 4's `wordAlpha`). The dihedral angle is arccos(−1/√5) = π − α. This is the α of the three words.
- `dehnSet_dod_ne_zero`: **the dodecahedron is a nonzero word**.

### 5. The icosahedron (`lean/Dehn7Icosa.lean`, part Y)
- `ico_isEdgeData`: the icosahedron with corners the cyclic permutations of (0, ±2, ±(1 + √5)) (20 faces, 12 corners, 30 edges of length 4) satisfies `IsEdgeData`.
- `dehnSet_ico`: **dehnSet icoSet = (−120) ⊗ γ**, with γ = arccos(√5/3) (study 4's `wordGamma`). The dihedral angle is arccos(−√5/3) = π − γ.
- `wordGamma_not_ratPi`: γ is not a rational multiple of π. By study 5, γ = α + 2β − π. By study 6, α and β are independent modulo π.
- `dehnSet_ico_ne_zero`: **the icosahedron is a nonzero word**.

### 6. The table (`lean/Dehn7Table.lean`, part Z)
- `zeroWords`: `IsZeroWord` (convex polytope with invariant 0) holds for the cube, the rhombic dodecahedron, every cube ∩ rhombic dodecahedron solid (the fair 18-face die among them), the rhombic triacontahedron, both golden rhombohedra and the truncated octahedron.
- `nonzeroWords`: `IsNonzeroWord` holds for the dodecahedron, icosahedron, tetrahedron, octahedron (D·I·C·T·O order; there is no cube in this list), every cube ∩ octahedron solid with t ≠ 3/2 (Lucky 7 among them), CLEO, AXE and FUJI.
- `canon_not_scissorsCongruent`: **no similar copy of a nonzero word is scissors congruent to a similar copy of a zero word**.
- Pairs of nonzero words (similar copies, any sizes, any positions; each proved separately):

| pair | why | theorem |
|---|---|---|
| dodecahedron – icosahedron | over α, β: (c, 0) against (−120, −240), independent (study 6) | `dod_ico_not_scissorsCongruent` |
| dodecahedron – CLEO, AXE, FUJI | the same | `dod_cleo_…`, `dod_axe_…`, `dod_fuji_…` |
| icosahedron – CLEO, AXE, FUJI | the same (determinants 720 − 360g, −480 + 240g, 720 − 360g) | `ico_cleo_…`, `ico_axe_…`, `ico_fuji_…` |
| octahedron – tetrahedron | −12√2 and +12√2 times arccos(1/3): opposite signs | `oct_tetra_not_scissorsCongruent` |
| cube ∩ octahedron, 3/2 < t < 2 (Lucky 7) – octahedron | 12√2(2t − 3) > 0 against −12√2 | `co_oct_not_scissorsCongruent` |
| cube ∩ octahedron, 1 < t < 3/2 – tetrahedron | 12√2(2t − 3) < 0 against +12√2 | `co_tetra_not_scissorsCongruent` |

  Together with study 6 (no two of CLEO, AXE, FUJI), the α–β family {dodecahedron, icosahedron, CLEO, AXE, FUJI} is pairwise not scissors congruent.

## Method
- **Rational angles (part U).** Study 4's theorem needs only the pairwise angles of the normals. For the icosahedral directions the Gram numbers lie in ℤ[√5]. The table of 900 pairs is a computation on pairs of integers (`decide +kernel`). The two kinds of entries are closed by study 4's `angle_mem_ratPi_of_gram` (rational cosines) and by the new 36° lemma (cosines (±1 ± √5)/4, where cos 5θ = ±1). The data were checked first in exact arithmetic (`checks/gold_check.py`, output `checks/gold_check.out`). That check confirms the 30 directions, their Gram table, that every cross product of two five-fold axes lies along a two-fold direction (so every zonohedron of the six five-fold axes has its normals among them: argued by hand here, used in Lean only for the three solids above), and the faces of the two rhombohedra.
- **Edge reading (parts V to Y).** Study 5's `IsEdgeData.dehnSet_eq` needs the corner–face table and one `cover` proof for each pair of faces. The Lean text of the tables and of the certificates was written by two generators, `checks/gen_edges.py` (integer normals, corners linear in t, exact fractions) and `checks/gen_edges5.py` (exact ℚ(√5)). Both ran on the compute host and check each fact exactly before writing it. Lean then checks everything again. The pairs of faces are handled as follows:
  - **Edges**, by study 5's `mem_segment_of_tight`: a third face through one corner fixes the position along the edge, and a fourth face bounds it on the other side.
  - **Pairs sharing one corner**, by study 5's `eq_of_tight` (icosahedron: 60 pairs) or by `linarith` on the coordinates (octahedron: 12 pairs).
  - **Pairs with no common point**, by `linarith` (octahedron 4, cube ∩ octahedron 55) or by a Farkas certificate `false_of_comb` (dodecahedron 36, icosahedron 100).

  Identities in ℚ(√5) are proved by `grind` from √5² = 5, signs by `linarith` from 2.236 < √5 < 2.237, and finite tables by `decide`.
- **Angles.** Each edge angle comes from the Gram numbers of the two normals (study 4's `theta_pair_of_gram`). The relations between angles are proved as equalities of real numbers. 2 · arccos(1/√3) = π − arccos(1/3) holds because cos of the left side is −1/3 and arccos(1/√3) ≤ π/2.
- **Not zero.** A single angle class whose angle is not a rational multiple of π is nonzero, by study 1's `edgeTerm_ne_zero`. For arccos(1/3) this is Niven's theorem (study 1). For α it is Niven's theorem on 2α (study 4). For γ it comes from studies 5 and 6.
- **Pairs.** Over α, β: study 5's `not_proportional` with study 6's `wordAnglesIndep`. Over arccos(1/3): two invariants L ⊗ θ and M ⊗ θ with L M < 0 are not positive multiples of each other (`tet_not_pos_proportional`, `not_scissorsCongruent_of_not_pos_proportional`).
- Agreement with the numerical study (`studies/2026-11-19-dehn-words/data/dehn-words.log`): zero for cube, RD, TO, RT and both golden rhombohedra; nonzero for octahedron, icosahedron, dodecahedron and the fair die co (Lucky 7). The printed sizes agree up to the normalisation used there: the octahedron 16.971 = 12√2; the icosahedron 60 = 30 × 2 at edge 2; the dodecahedron 37.082 = 30(√5 − 1) at edge √5 − 1; Lucky 7 17.417 = 24√2 (2t − 3) at t = 1.7566… in units of arccos(1/√3), the same as 12√2 (2t − 3) ⊗ arccos(1/3) here.

## Credits (borrowed lemmas, at the point of use in the files)
Mathlib: `Real.cos_add`, `Real.cos_three_mul`, `Real.sin_three_mul`, `Real.cos_two_mul`, `Real.sin_two_mul`, `Real.cos_arccos`, `Real.arccos_cos`, `Real.arccos_neg`, `Real.arccos_le_pi_div_two`, `Real.sqrt_mul_self`, `Real.lt_sqrt`, `Real.sqrt_lt'`, `InnerProductGeometry.cos_angle`, `norm_eq_sqrt_real_inner`, `Set.pair_eq_pair_iff`, `Finset.sum_ite`, `Finset.sum_const`, `List.sum_replicate`, `TensorProduct.smul_tmul'`; the tactics `grind`, `decide +kernel`, `linarith`, `nlinarith`. Studies 1 to 6 of this canon: `tetDihedral_not_ratPi`, `edgeTerm_ne_zero`, `dehn_const` (1); `not_scissorsCongruent_of_dehnSet_ne` (2); `dehnSet_cube`, `dehnSet_tetra` (3); `dehnSet_sol_eq_zero_of_rational`, `angle_mem_ratPi_of_gram`, `mem_ratPi_of_sin_nat_mul`, `crN_angle`, `theta_pair_of_gram`, `dist3`, `not_scissorsCongruent_similarCopies`, `dehnSet_similarCopy`, `wordAlpha_not_ratPi` (4); `IsEdgeData`, `IsEdgeData.dehnSet_eq`, `mem_segment_of_tight`, `eq_of_tight`, `ind3`, `edgeTerm_angle_add`, `edgeTerm_pi`, `edgeTerm_int`, `edgeTerm_gamma`, `wordGamma_eq`, `not_proportional`, `not_scissorsCongruent_of_not_proportional`, the three words over α, β (5); `word_angles_int_indep`, `wordAnglesIndep` (6). Mathematics: Dehn (1901); Jessen's tensor form; Niven's theorem; the Farkas lemma (only the easy direction is used: a given certificate is checked).

## Sources checked
- Studies 4, 5, 6 of this canon (READMEs and Lean files), and studies 1 to 3 for the names used.
- `studies/2026-11-19-dehn-words/` (README, `data/dehn-words.log`): the numerical calibration and results this study had to match. They agree, as listed under Method.
- `studies/2026-11-18-fair-32-die/data/verts-co.json`, `data/co.log`: the Lucky 7 corners and bracket.
- Pinned Mathlib (grep): Dehn invariant, scissors congruence: not found. Dodecahedron, icosahedron, triacontahedron, rhombohedron as solids: not found (the matches are Coxeter matrices and the octahedral axiom of triangulated categories). A five-fold cosine formula: not found. Farkas' lemma: present (`Analysis/Convex/Cone/`), not used, since the certificates are checked directly.
- No web search was made in this study. A machine-checked Dehn invariant of these solids: not found in the sources checked.

## `#print axioms` (from `compile.log`)
All 41 theorems listed in `lean/Axioms7.lean` print `[propext, Classical.choice, Quot.sound]`. Among them are `dehnSet_rtFamily`, `dehnSet_rt`, `goldProlateSet_eq`, `goldOblateSet_eq`, `dehnSet_goldProlate`, `dehnSet_goldOblate`, `dehnSet_rd`, `dehnSet_oct`, `dehnSet_oct_ne_zero`, `dehnSet_co`, `dehnSet_truncOct`, `dehnSet_luckySeven_ne_zero`, `dehnSet_dod`, `dehnSet_dod_ne_zero`, `dehnSet_ico`, `dehnSet_ico_ne_zero`, `zeroWords`, `nonzeroWords`, `canon_not_scissorsCongruent` and the nine pair theorems. There is no `native_decide` and no added axiom. `grep sorry` over the twenty-seven files of the chain finds only the header lines that say "No `sorry`".

## Limits of what is stated
- As in studies 2 to 6: dimension 3, and the pieces of a scissors congruence are convex polytopes, finitely many, moved by isometries (reflections included). Zero invariant is not shown to imply scissors congruence with a cube (Sydler's direction).
- The solids are given as intersections of half-spaces. For the golden rhombohedra, equality with the parallelepiped is proved. For the octahedron, dodecahedron, icosahedron and the cube ∩ octahedron line, the corners and edges are proved to be those of the solid (`IsEdgeData`: corners in the solid, the open edges are exactly the points on two faces). Equality with the convex hull of the corners is not stated, as for FUJI in study 5.
- The rhombic triacontahedron is the solid of its 30 face planes at one distance. That it is the zonohedron of the six five-fold axes is not stated in Lean.
- Lucky 7: proved for the whole interval 7/4 < t < 9/5 that contains the die. The die's own t is numerical (study of 18 November).
- Only the fair 14-face die is done among the eleven nonzero fair dice of `dehn-words`. The other ten (tc 10, tr 16, td 16, cd 18, or 20, od 20, rdd 24, di 32, dt 42, it 50) are not done here (Leads).

## Files and how to compile
`lean/Dehn7Gold.lean` (part U), `lean/Dehn7Octa.lean` (part V), `lean/Dehn7CubeOct.lean` (part W), `lean/Dehn7Dodeca.lean` (part X), `lean/Dehn7Icosa.lean` (part Y), `lean/Dehn7Table.lean` (part Z), `lean/Axioms7.lean`, `lean/compile_all7.sh`, `compile.log`. In `checks/`: `gold_check.py`, `gen_edges.py`, `gen_edges5.py`, `q5.py` (exact ℚ(√5) arithmetic from study 5), and their outputs `gold_check.out`, `gen_oct.out`, `gen_co.out`, `gen_dod.out`, `gen_ico.out` (counts of faces, corners, edges and pairs; the edge list with lengths and Gram numbers).
The files import study 6 (`DehnCanon.Dehn6Pairs`) and through it studies 1 to 5, all unchanged. They are compiled in the Lean workspace of studies 1 to 6, all files in the folder `DehnCanon/`, by `bash DehnCanon/compile_all7.sh` from the workspace root. The script compiles the twenty-seven files of the chain in dependency order, prints the axioms and greps for `sorry`, `native_decide` and `axiom`. For short runs it takes a part argument (1, 2, 3, check); `compile.log` is the four parts in order. The files on the compute host and the copies here have the same SHA-256.

## Leads
- **The other fair dice.** The generators handle any solid whose corners and normals are exact in ℚ or ℚ(√5), or linear in one parameter. What each die needs is its exact corner data and, for "not zero", the independence of its angle classes. Dice whose angles all reduce to arccos(1/3) (cube and octahedron directions) go through as Lucky 7 did. The others need their own independence argument (study 6's recurrence method).
- **The two families against each other.** Over α, β the canon is decided pairwise; over arccos(1/3) only pairs of opposite sign are. Two cases remain open. First, any pair with one solid from each family needs arccos(1/3) independent of the angles of the other family modulo π. The dodecahedron against the octahedron needs only α against arccos(1/3). That looks within reach of study 6's method at the prime 3: 2 cos 2α = −6/5 is integral at 3, while 2 cos(2 · arccos(1/3)) = −14/9 is not. The icosahedron and the words also involve β, and 2 cos 2β = −(10 + 8√5)/15 is not integral at 3 either, so a different prime or a different argument is needed. This is by hand and not checked. Second, pairs over arccos(1/3) with the same sign, such as Lucky 7 against the tetrahedron, have invariants that are positive multiples of each other. They are decided by comparing invariant and volume at equal volume, and no volume is computed in Lean here.
- **Zonohedra of the five-fold axes.** `dehnSet_rtFamily` already covers every solid whose face normals are two-fold directions. A Lean statement that the rhombic icosahedron and the Bilinski dodecahedron (zonohedra of 5 and 4 five-fold axes) are such solids would make them zero words with no new angle work.
- **Convex hulls.** The equality "solid = convex hull of its corners" for the solids read by edges (here and FUJI) is still open. A general proof of `cover` from it would replace the generated certificates.
- From earlier studies, unchanged: Sydler's converse; one Lean folder for publication (now twenty-seven files).
