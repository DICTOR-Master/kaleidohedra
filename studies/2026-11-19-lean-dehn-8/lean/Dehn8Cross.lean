/-
Lean study 8 of the shape-language canon (DICTO, 19 Nov 2026), part AB: the two families of nonzero words
against each other, and the canon table.

* `not_scissorsCongruent_tet_ab`: if the invariant of P is L ⊗ arccos(1/3) with L ≠ 0 and that of Q is
  a ⊗ α + b ⊗ β, no similar copy of P is scissors congruent to a similar copy of Q (any sizes, any positions).
* The fifteen pairs, each by name: each of the octahedron, the tetrahedron and the cube ∩ octahedron solids with
  t ≠ 3/2 (Lucky 7 among them) against each of the dodecahedron, the icosahedron, CLEO, AXE and FUJI
  (`oct_dod_…`, …, `co_fuji_not_scissorsCongruent`).
* `TetFamily`, `ABFamily`: the two families; `canon_cross_not_scissorsCongruent`: the fifteen pairs in one
  statement. `abWord`: the five solids over α, β; `canon_ab_not_scissorsCongruent`: any two different ones are
  not scissors congruent (studies 6 and 7, here in one statement).
* `canon_table`: the canon table: nonzero against zero (study 7), the α–β family pairwise, the two families
  against each other.

Credits: Mathlib `Submodule.exists_dual_map_eq_bot_of_notMem`, `Submodule.mem_map_of_mem`,
`Submodule.subset_span`. This canon: study 2's `not_scissorsCongruent_of_dehnSet_ne`; study 4's
`dehnSet_similarCopy`, `IsPoly.similarCopy`; study 5's `lengthPart`, `lengthPart_tmul`, `lengthPart_smul` (the
method of study 4's `tmul_add_tmul_ne_zero`: a ℚ-linear map on the angle factor), `not_proportional`,
`not_scissorsCongruent_of_not_proportional`; study 6's `wordAnglesIndep`; study 7's `dehnSet_oct`,
`dehnSet_co`, `dehnSet_tetra_tet`, `dehnSet_dod_ab`, `dehnSet_ico_ab`, `dehnSet_cleo_ab`, `dehnSet_axe_ab`,
`dehnSet_fuji_ab`, `IsZeroWord`, `IsNonzeroWord`, `canon_not_scissorsCongruent`; part AA's `tet_not_mem_span`.
No `sorry`.
-/
import DehnCanon.Dehn7Table
import DehnCanon.Dehn8Indep

open scoped RealInnerProductSpace Real
open Set Module TensorProduct

namespace DehnCanon

/-- **The two families apart.** If the invariant of `P` is L ⊗ arccos(1/3) with L ≠ 0 and that of `Q` is
a ⊗ α + b ⊗ β, no similar copy of `P` is scissors congruent to a similar copy of `Q`. -/
theorem not_scissorsCongruent_tet_ab {P Q P' Q' : Set R3} (hP : IsPoly P) (hQ : IsPoly Q) {L a b : ℝ}
    (hL : L ≠ 0) (eP : dehnSet P = edgeTerm L tetDihedral)
    (eQ : dehnSet Q = a ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      b ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle))
    (hP' : IsSimilarCopy P P') (hQ' : IsSimilarCopy Q Q') : ¬ ScissorsCongruent P' Q' := by
  apply not_scissorsCongruent_of_dehnSet_ne (hP.similarCopy hP') (hQ.similarCopy hQ')
  obtain ⟨s, hs, e1⟩ := dehnSet_similarCopy hP'
  obtain ⟨c, -, e2⟩ := dehnSet_similarCopy hQ'
  rw [e1, e2, eP, eQ]
  intro he
  obtain ⟨f, hf, hf0⟩ := Submodule.exists_dual_map_eq_bot_of_notMem tet_not_mem_span inferInstance
  have hz : ∀ x ∈ ({(Submodule.Quotient.mk wordAlpha : Angle), Submodule.Quotient.mk wordBeta} : Set Angle),
      f x = 0 := by
    intro x hx
    have h3 := Submodule.mem_map_of_mem (f := f) (Submodule.subset_span (R := ℚ) hx)
    rw [hf0] at h3
    exact (Submodule.mem_bot ℚ).1 h3
  have e := congrArg (lengthPart f) he
  rw [lengthPart_smul, lengthPart_smul, map_add, edgeTerm, lengthPart_tmul, lengthPart_tmul, lengthPart_tmul,
    hz (Submodule.Quotient.mk wordAlpha) (by simp), hz (Submodule.Quotient.mk wordBeta) (by simp)] at e
  simp only [zero_smul, add_zero, mul_zero, Rat.smul_def] at e
  exact mul_ne_zero hs.ne' (mul_ne_zero (Rat.cast_ne_zero.2 hf) hL) e

lemma oct_L_ne : (-12 * √2 : ℝ) ≠ 0 := by positivity
lemma tetra_L_ne : (12 * √2 : ℝ) ≠ 0 := by positivity
lemma co_L_ne {t : ℝ} (ht : t ≠ 3 / 2) : (12 * √2 * (2 * t - 3) : ℝ) ≠ 0 :=
  mul_ne_zero (by positivity) (by intro h; apply ht; linarith)

/-! ### The fifteen pairs, by name -/

/-- **No octahedron is scissors congruent to a dodecahedron** (any sizes, any positions). -/
theorem oct_dod_not_scissorsCongruent {O D : Set R3} (hO : IsSimilarCopy octSet O)
    (hD : IsSimilarCopy dodSet D) : ¬ ScissorsCongruent O D :=
  not_scissorsCongruent_tet_ab isPoly_oct isPoly_dod oct_L_ne dehnSet_oct dehnSet_dod_ab hO hD

theorem oct_ico_not_scissorsCongruent {O I : Set R3} (hO : IsSimilarCopy octSet O)
    (hI : IsSimilarCopy icoSet I) : ¬ ScissorsCongruent O I :=
  not_scissorsCongruent_tet_ab isPoly_oct isPoly_ico oct_L_ne dehnSet_oct dehnSet_ico_ab hO hI

theorem oct_cleo_not_scissorsCongruent {O C : Set R3} (hO : IsSimilarCopy octSet O)
    (hC : IsSimilarCopy cleoSet C) : ¬ ScissorsCongruent O C :=
  not_scissorsCongruent_tet_ab isPoly_oct isPoly_cleo oct_L_ne dehnSet_oct dehnSet_cleo_ab hO hC

theorem oct_axe_not_scissorsCongruent {O A : Set R3} (hO : IsSimilarCopy octSet O)
    (hA : IsSimilarCopy axeSet A) : ¬ ScissorsCongruent O A :=
  not_scissorsCongruent_tet_ab isPoly_oct isPoly_axe oct_L_ne dehnSet_oct dehnSet_axe_ab hO hA

theorem oct_fuji_not_scissorsCongruent {O F : Set R3} (hO : IsSimilarCopy octSet O)
    (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent O F :=
  not_scissorsCongruent_tet_ab isPoly_oct isPoly_fuji oct_L_ne dehnSet_oct dehnSet_fuji_ab hO hF

/-- **No regular tetrahedron is scissors congruent to a dodecahedron** (any sizes, any positions). -/
theorem tetra_dod_not_scissorsCongruent {T D : Set R3} (hT : IsSimilarCopy tetraSet T)
    (hD : IsSimilarCopy dodSet D) : ¬ ScissorsCongruent T D :=
  not_scissorsCongruent_tet_ab isPoly_tetra isPoly_dod tetra_L_ne dehnSet_tetra_tet dehnSet_dod_ab hT hD

theorem tetra_ico_not_scissorsCongruent {T I : Set R3} (hT : IsSimilarCopy tetraSet T)
    (hI : IsSimilarCopy icoSet I) : ¬ ScissorsCongruent T I :=
  not_scissorsCongruent_tet_ab isPoly_tetra isPoly_ico tetra_L_ne dehnSet_tetra_tet dehnSet_ico_ab hT hI

theorem tetra_cleo_not_scissorsCongruent {T C : Set R3} (hT : IsSimilarCopy tetraSet T)
    (hC : IsSimilarCopy cleoSet C) : ¬ ScissorsCongruent T C :=
  not_scissorsCongruent_tet_ab isPoly_tetra isPoly_cleo tetra_L_ne dehnSet_tetra_tet dehnSet_cleo_ab hT hC

theorem tetra_axe_not_scissorsCongruent {T A : Set R3} (hT : IsSimilarCopy tetraSet T)
    (hA : IsSimilarCopy axeSet A) : ¬ ScissorsCongruent T A :=
  not_scissorsCongruent_tet_ab isPoly_tetra isPoly_axe tetra_L_ne dehnSet_tetra_tet dehnSet_axe_ab hT hA

theorem tetra_fuji_not_scissorsCongruent {T F : Set R3} (hT : IsSimilarCopy tetraSet T)
    (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent T F :=
  not_scissorsCongruent_tet_ab isPoly_tetra isPoly_fuji tetra_L_ne dehnSet_tetra_tet dehnSet_fuji_ab hT hF

/-- **For 1 < t < 2, t ≠ 3/2 (Lucky 7 among them), no cube ∩ octahedron solid is scissors congruent to a
dodecahedron** (any sizes, any positions). -/
theorem co_dod_not_scissorsCongruent {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) (ht : t ≠ 3 / 2) {C D : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hD : IsSimilarCopy dodSet D) : ¬ ScissorsCongruent C D :=
  not_scissorsCongruent_tet_ab (isPoly_co t) isPoly_dod (co_L_ne ht) (dehnSet_co ht1 ht2) dehnSet_dod_ab hC hD

theorem co_ico_not_scissorsCongruent {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) (ht : t ≠ 3 / 2) {C I : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hI : IsSimilarCopy icoSet I) : ¬ ScissorsCongruent C I :=
  not_scissorsCongruent_tet_ab (isPoly_co t) isPoly_ico (co_L_ne ht) (dehnSet_co ht1 ht2) dehnSet_ico_ab hC hI

theorem co_cleo_not_scissorsCongruent {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) (ht : t ≠ 3 / 2) {C C' : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hC' : IsSimilarCopy cleoSet C') : ¬ ScissorsCongruent C C' :=
  not_scissorsCongruent_tet_ab (isPoly_co t) isPoly_cleo (co_L_ne ht) (dehnSet_co ht1 ht2) dehnSet_cleo_ab
    hC hC'

theorem co_axe_not_scissorsCongruent {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) (ht : t ≠ 3 / 2) {C A : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hA : IsSimilarCopy axeSet A) : ¬ ScissorsCongruent C A :=
  not_scissorsCongruent_tet_ab (isPoly_co t) isPoly_axe (co_L_ne ht) (dehnSet_co ht1 ht2) dehnSet_axe_ab hC hA

theorem co_fuji_not_scissorsCongruent {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) (ht : t ≠ 3 / 2) {C F : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent C F :=
  not_scissorsCongruent_tet_ab (isPoly_co t) isPoly_fuji (co_L_ne ht) (dehnSet_co ht1 ht2) dehnSet_fuji_ab hC hF

/-! ### The two families as statements -/

/-- The nonzero words over arccos(1/3): the octahedron, the tetrahedron, and the cube ∩ octahedron solids with
1 < t < 2, t ≠ 3/2. -/
def TetFamily (P : Set R3) : Prop :=
  P = octSet ∨ P = tetraSet ∨ ∃ t : ℝ, 1 < t ∧ t < 2 ∧ t ≠ 3 / 2 ∧ P = coSet t

/-- The five nonzero words over α, β in D·I·C·T·O order and then the three words: dodecahedron, icosahedron,
CLEO, AXE, FUJI. -/
def abWord : Fin 5 → Set R3 := ![dodSet, icoSet, cleoSet, axeSet, fujiSet]

/-- The nonzero words over α, β. -/
def ABFamily (Q : Set R3) : Prop := ∃ i, Q = abWord i

lemma TetFamily.data {P : Set R3} (h : TetFamily P) :
    IsPoly P ∧ ∃ L : ℝ, L ≠ 0 ∧ dehnSet P = edgeTerm L tetDihedral := by
  rcases h with rfl | rfl | ⟨t, ht1, ht2, ht, rfl⟩
  · exact ⟨isPoly_oct, _, oct_L_ne, dehnSet_oct⟩
  · exact ⟨isPoly_tetra, _, tetra_L_ne, dehnSet_tetra_tet⟩
  · exact ⟨isPoly_co t, _, co_L_ne ht, dehnSet_co ht1 ht2⟩

/-- The coefficients of α and β in the invariants of the five. -/
noncomputable def abA : Fin 5 → ℝ :=
  ![-30 * (2 * √5 - 2), -120, 3, 1 + (√5 - 1) / 2, 9 - 3 * ((√5 - 1) / 2)]
noncomputable def abB : Fin 5 → ℝ :=
  ![0, -240, 3 * ((√5 - 1) / 2), 6, 12 - 3 * ((√5 - 1) / 2)]

lemma isPoly_abWord (i : Fin 5) : IsPoly (abWord i) := by
  fin_cases i
  exacts [isPoly_dod, isPoly_ico, isPoly_cleo, isPoly_axe, isPoly_fuji]

lemma dehnSet_abWord (i : Fin 5) : dehnSet (abWord i) =
    abA i ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      abB i ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle) := by
  fin_cases i
  exacts [dehnSet_dod_ab, dehnSet_ico_ab, dehnSet_cleo_ab, dehnSet_axe_ab, dehnSet_fuji_ab]

lemma abWord_det {i j : Fin 5} (h : i ≠ j) : abA i * abB j ≠ abB i * abA j := by
  fin_cases i <;> fin_cases j <;> (try exact absurd rfl h) <;> intro e <;>
    simp only [abA, abB, Fin.isValue, Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.cons_val_four,
      Matrix.head_cons, Matrix.tail_cons] at e <;>
    nlinarith [sqrt5_sq, sqrt5_gt, sqrt5_lt]

/-- **Any two different words over α, β are not scissors congruent** (similar copies, any sizes, any
positions): the dodecahedron, the icosahedron, CLEO, AXE, FUJI. -/
theorem canon_ab_not_scissorsCongruent {i j : Fin 5} (hij : i ≠ j) {P' Q' : Set R3}
    (hP' : IsSimilarCopy (abWord i) P') (hQ' : IsSimilarCopy (abWord j) Q') : ¬ ScissorsCongruent P' Q' :=
  not_scissorsCongruent_of_not_proportional (isPoly_abWord i) (isPoly_abWord j) (fun t => by
    rw [dehnSet_abWord, dehnSet_abWord]
    exact not_proportional wordAnglesIndep.1 wordAnglesIndep.2 (abWord_det hij) t) hP' hQ'

/-- **The two families apart, in one statement**: no similar copy of the octahedron, the tetrahedron or a cube ∩
octahedron solid with t ≠ 3/2 is scissors congruent to a similar copy of the dodecahedron, the icosahedron,
CLEO, AXE or FUJI. -/
theorem canon_cross_not_scissorsCongruent {P Q P' Q' : Set R3} (hP : TetFamily P) (hQ : ABFamily Q)
    (hP' : IsSimilarCopy P P') (hQ' : IsSimilarCopy Q Q') : ¬ ScissorsCongruent P' Q' := by
  obtain ⟨hPp, L, hL, eP⟩ := hP.data
  obtain ⟨i, rfl⟩ := hQ
  exact not_scissorsCongruent_tet_ab hPp (isPoly_abWord i) hL eP (dehnSet_abWord i) hP' hQ'

/-- **The canon table.** For similar copies (any sizes, any positions):
(1) no nonzero word is scissors congruent to a zero word (study 7);
(2) no two different words over α, β are scissors congruent (studies 6 and 7);
(3) no word over arccos(1/3) is scissors congruent to a word over α, β (this study).
Pairs over arccos(1/3) are decided for opposite signs only (study 7's `oct_tetra_…`, `co_oct_…`,
`co_tetra_…`). -/
theorem canon_table :
    (∀ {P Q P' Q' : Set R3}, IsNonzeroWord P → IsZeroWord Q → IsSimilarCopy P P' → IsSimilarCopy Q Q' →
      ¬ ScissorsCongruent P' Q') ∧
    (∀ {i j : Fin 5} {P' Q' : Set R3}, i ≠ j → IsSimilarCopy (abWord i) P' → IsSimilarCopy (abWord j) Q' →
      ¬ ScissorsCongruent P' Q') ∧
    (∀ {P Q P' Q' : Set R3}, TetFamily P → ABFamily Q → IsSimilarCopy P P' → IsSimilarCopy Q Q' →
      ¬ ScissorsCongruent P' Q') :=
  ⟨fun hP hQ hP' hQ' => canon_not_scissorsCongruent hP hQ hP' hQ',
    fun hij hP' hQ' => canon_ab_not_scissorsCongruent hij hP' hQ',
    fun hP hQ hP' hQ' => canon_cross_not_scissorsCongruent hP hQ hP' hQ'⟩

end DehnCanon
