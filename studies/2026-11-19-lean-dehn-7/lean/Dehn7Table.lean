/-
Lean study 7 of the shape-language canon (DICTO, 19 Nov 2026), part Z: the canon in one table.

* `IsZeroWord P`: a convex polytope with Dehn invariant zero. `IsNonzeroWord P`: one with invariant not zero.
* The zero words proved in Lean: cube, rhombic dodecahedron, every cube ∩ rhombic dodecahedron solid (the fair
  18-face die among them), rhombic triacontahedron, both golden rhombohedra, truncated octahedron.
* The nonzero words proved in Lean (D·I·C·T·O order for the Platonic ones): dodecahedron, icosahedron,
  tetrahedron, octahedron; every cube ∩ octahedron solid other than the truncated octahedron (Lucky 7 among
  them); the three words CLEO, AXE, FUJI.
* `canon_not_scissorsCongruent`: no similar copy of a nonzero word is scissors congruent to a similar copy of a
  zero word.
* Pairs of nonzero words, each proved separately:
  - over α, β (independent modulo π, study 6): `dod_ico_…`, and the dodecahedron and the icosahedron against
    each of CLEO, AXE, FUJI (`dod_cleo_…`, …, `ico_fuji_…`);
  - over arccos(1/3) with opposite signs: `oct_tetra_…`, `co_oct_…` (3/2 < t < 2, Lucky 7 among them),
    `co_tetra_…` (1 < t < 3/2).
  Pairs with one solid of each family (e.g. the dodecahedron against the octahedron) and pairs over arccos(1/3)
  with the same sign (e.g. Lucky 7 against the tetrahedron) are not decided here (README, Leads).

Credits: study 4's `not_scissorsCongruent_similarCopies`, `dehnSet_similarCopy`; study 5's `not_proportional`,
`not_scissorsCongruent_of_not_proportional`, `dehn_cleo_alpha_beta`, `dehn_axe_alpha_beta`,
`dehn_fuji_alpha_beta`, `edgeTerm_gamma`; study 6's `wordAnglesIndep`; study 2's
`not_scissorsCongruent_of_dehnSet_ne`; Mathlib `TensorProduct.smul_tmul'`, `List.sum_replicate`.
No `sorry`.
-/
import DehnCanon.Dehn7Icosa

open scoped RealInnerProductSpace Real
open Set Module TensorProduct

namespace DehnCanon

/-! ### Two more polytopes -/

theorem isPoly_rd (c : ℝ) : IsPoly (rdSet c) := by
  refine ⟨bounded_of_coords c (fun x hx i => ?_), Fin 12, inferInstance, _, _, rfl⟩
  have H := fun m : Fin 12 => (hx m : ⟪crN (Fin.natAdd 6 m), x⟫ ≤ c)
  have h0 := H 0; have h1 := H 1; have h2 := H 2; have h3 := H 3; have h4 := H 4; have h5 := H 5
  have h6 := H 6; have h7 := H 7; have h8 := H 8; have h9 := H 9; have h10 := H 10; have h11 := H 11
  simp [crN, crZ, inner3, Fin.natAdd] at h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11
  fin_cases i <;> simp only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk] <;> rw [abs_le] <;>
    constructor <;> linarith

lemma phi_mem : 0 ≤ phi ∧ phi ≤ 2 := by
  have h := sqrt5_lt_three; constructor <;> unfold phi <;> [positivity; linarith]

theorem isPoly_goldProlate : IsPoly goldProlateSet := by
  refine ⟨?_, Fin 6, inferInstance, _, _, rfl⟩
  rw [goldProlateSet_eq]
  refine bounded_of_coords 6 (fun x hx i => ?_)
  obtain ⟨a, b, c, ⟨a0, a1⟩, ⟨b0, b1⟩, ⟨c0, c1⟩, rfl⟩ := hx
  obtain ⟨p0, p2⟩ := phi_mem
  rw [abs_le]
  fin_cases i <;> simp [gpU, gpV, gpW] <;> (try constructor) <;>
    nlinarith [mul_nonneg a0 p0, mul_nonneg b0 p0, mul_nonneg c0 p0, mul_le_mul a1 p2 p0 zero_le_one,
      mul_le_mul b1 p2 p0 zero_le_one, mul_le_mul c1 p2 p0 zero_le_one]

theorem isPoly_goldOblate : IsPoly goldOblateSet := by
  refine ⟨?_, Fin 6, inferInstance, _, _, rfl⟩
  rw [goldOblateSet_eq]
  refine bounded_of_coords 6 (fun x hx i => ?_)
  obtain ⟨a, b, c, ⟨a0, a1⟩, ⟨b0, b1⟩, ⟨c0, c1⟩, rfl⟩ := hx
  obtain ⟨p0, p2⟩ := phi_mem
  rw [abs_le]
  fin_cases i <;> simp [goU, goV, goW] <;> (try constructor) <;>
    nlinarith [mul_nonneg a0 p0, mul_nonneg b0 p0, mul_nonneg c0 p0, mul_le_mul a1 p2 p0 zero_le_one,
      mul_le_mul b1 p2 p0 zero_le_one, mul_le_mul c1 p2 p0 zero_le_one]

/-! ### Zero and nonzero words -/

/-- A zero word: a convex polytope whose Dehn invariant is zero. -/
def IsZeroWord (P : Set R3) : Prop := IsPoly P ∧ dehnSet P = 0

/-- A nonzero word: a convex polytope whose Dehn invariant is not zero. -/
def IsNonzeroWord (P : Set R3) : Prop := IsPoly P ∧ dehnSet P ≠ 0

/-- **The zero words of the canon.** -/
theorem zeroWords (s c r : ℝ) (hs : 0 < s) :
    IsZeroWord (cubeSet s) ∧ IsZeroWord (rdSet c) ∧ IsZeroWord (cubeRDSet s c) ∧ IsZeroWord (rtSet r) ∧
    IsZeroWord goldProlateSet ∧ IsZeroWord goldOblateSet ∧ IsZeroWord truncOctSet :=
  ⟨⟨isPoly_cube s, dehnSet_cube s hs⟩, ⟨isPoly_rd c, dehnSet_rd c⟩, ⟨isPoly_cubeRD s c, dehnSet_cubeRD s c⟩,
    ⟨isPoly_rt r, dehnSet_rt r⟩, ⟨isPoly_goldProlate, dehnSet_goldProlate⟩,
    ⟨isPoly_goldOblate, dehnSet_goldOblate⟩, ⟨isPoly_co _, dehnSet_truncOct⟩⟩

/-- **The nonzero words of the canon.** -/
theorem nonzeroWords {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) (ht : t ≠ 3 / 2) :
    IsNonzeroWord dodSet ∧ IsNonzeroWord icoSet ∧ IsNonzeroWord tetraSet ∧ IsNonzeroWord octSet ∧
    IsNonzeroWord (coSet t) ∧ IsNonzeroWord cleoSet ∧ IsNonzeroWord axeSet ∧ IsNonzeroWord fujiSet :=
  ⟨⟨isPoly_dod, dehnSet_dod_ne_zero⟩, ⟨isPoly_ico, dehnSet_ico_ne_zero⟩,
    ⟨isPoly_tetra, dehnSet_tetra_ne_zero⟩, ⟨isPoly_oct, dehnSet_oct_ne_zero⟩,
    ⟨isPoly_co t, dehnSet_co_ne_zero ht1 ht2 ht⟩, ⟨isPoly_cleo, dehnSet_cleo_ne_zero⟩,
    ⟨isPoly_axe, dehnSet_axe_ne_zero⟩, ⟨isPoly_fuji, dehnSet_fuji_ne_zero⟩⟩

/-- **No similar copy of a nonzero word is scissors congruent to a similar copy of a zero word.** -/
theorem canon_not_scissorsCongruent {P Q P' Q' : Set R3} (hP : IsNonzeroWord P) (hQ : IsZeroWord Q)
    (hP' : IsSimilarCopy P P') (hQ' : IsSimilarCopy Q Q') : ¬ ScissorsCongruent P' Q' :=
  not_scissorsCongruent_similarCopies hP.1 hQ.1 hP.2 hQ.2 hP' hQ'

/-! ### Pairs of nonzero words over α and β -/

/-- The dodecahedron over α, β: (−30 (2√5 − 2)) ⊗ α + 0 ⊗ β. -/
lemma dehnSet_dod_ab : dehnSet dodSet =
    (-30 * (2 * √5 - 2)) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      (0 : ℝ) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle) := by
  rw [dehnSet_dod, TensorProduct.zero_tmul, add_zero]; rfl

/-- The icosahedron over α, β: (−120) ⊗ α + (−240) ⊗ β (γ = α + 2β modulo π). -/
lemma dehnSet_ico_ab : dehnSet icoSet =
    (-120 : ℝ) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      (-240 : ℝ) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle) := by
  rw [dehnSet_ico, edgeTerm_gamma, add_assoc, ← edgeTerm_add]
  norm_num; rfl

/-- The three words over α, β, in the same form. -/
lemma dehnSet_cleo_ab : dehnSet cleoSet =
    (3 : ℝ) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      (3 * ((√5 - 1) / 2)) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle) := by
  rw [dehnSet_cleo, dehn_cleo_alpha_beta]; rfl

lemma dehnSet_axe_ab : dehnSet axeSet =
    (1 + (√5 - 1) / 2) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      (6 : ℝ) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle) := by
  rw [dehnSet_axe, dehn_axe_alpha_beta]; rfl

lemma dehnSet_fuji_ab : dehnSet fujiSet =
    (9 - 3 * ((√5 - 1) / 2)) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      (12 - 3 * ((√5 - 1) / 2)) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle) := by
  rw [dehnSet_fuji, dehn_fuji_alpha_beta]; rfl

macro "det_ne" : tactic =>
  `(tactic| (intro h; nlinarith [sqrt5_sq, sqrt5_gt, sqrt5_lt]))

/-- **No dodecahedron is scissors congruent to an icosahedron** (any sizes, any positions). -/
theorem dod_ico_not_scissorsCongruent {D I : Set R3} (hD : IsSimilarCopy dodSet D)
    (hI : IsSimilarCopy icoSet I) : ¬ ScissorsCongruent D I :=
  not_scissorsCongruent_of_not_proportional isPoly_dod isPoly_ico (fun t => by
    rw [dehnSet_dod_ab, dehnSet_ico_ab]
    exact not_proportional wordAnglesIndep.1 wordAnglesIndep.2 (by det_ne) t) hD hI

theorem dod_cleo_not_scissorsCongruent {D C : Set R3} (hD : IsSimilarCopy dodSet D)
    (hC : IsSimilarCopy cleoSet C) : ¬ ScissorsCongruent D C :=
  not_scissorsCongruent_of_not_proportional isPoly_dod isPoly_cleo (fun t => by
    rw [dehnSet_dod_ab, dehnSet_cleo_ab]
    exact not_proportional wordAnglesIndep.1 wordAnglesIndep.2 (by det_ne) t) hD hC

theorem dod_axe_not_scissorsCongruent {D A : Set R3} (hD : IsSimilarCopy dodSet D)
    (hA : IsSimilarCopy axeSet A) : ¬ ScissorsCongruent D A :=
  not_scissorsCongruent_of_not_proportional isPoly_dod isPoly_axe (fun t => by
    rw [dehnSet_dod_ab, dehnSet_axe_ab]
    exact not_proportional wordAnglesIndep.1 wordAnglesIndep.2 (by det_ne) t) hD hA

theorem dod_fuji_not_scissorsCongruent {D F : Set R3} (hD : IsSimilarCopy dodSet D)
    (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent D F :=
  not_scissorsCongruent_of_not_proportional isPoly_dod isPoly_fuji (fun t => by
    rw [dehnSet_dod_ab, dehnSet_fuji_ab]
    exact not_proportional wordAnglesIndep.1 wordAnglesIndep.2 (by det_ne) t) hD hF

theorem ico_cleo_not_scissorsCongruent {I C : Set R3} (hI : IsSimilarCopy icoSet I)
    (hC : IsSimilarCopy cleoSet C) : ¬ ScissorsCongruent I C :=
  not_scissorsCongruent_of_not_proportional isPoly_ico isPoly_cleo (fun t => by
    rw [dehnSet_ico_ab, dehnSet_cleo_ab]
    exact not_proportional wordAnglesIndep.1 wordAnglesIndep.2 (by det_ne) t) hI hC

theorem ico_axe_not_scissorsCongruent {I A : Set R3} (hI : IsSimilarCopy icoSet I)
    (hA : IsSimilarCopy axeSet A) : ¬ ScissorsCongruent I A :=
  not_scissorsCongruent_of_not_proportional isPoly_ico isPoly_axe (fun t => by
    rw [dehnSet_ico_ab, dehnSet_axe_ab]
    exact not_proportional wordAnglesIndep.1 wordAnglesIndep.2 (by det_ne) t) hI hA

theorem ico_fuji_not_scissorsCongruent {I F : Set R3} (hI : IsSimilarCopy icoSet I)
    (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent I F :=
  not_scissorsCongruent_of_not_proportional isPoly_ico isPoly_fuji (fun t => by
    rw [dehnSet_ico_ab, dehnSet_fuji_ab]
    exact not_proportional wordAnglesIndep.1 wordAnglesIndep.2 (by det_ne) t) hI hF

/-! ### Pairs of nonzero words over arccos(1/3) with opposite signs -/

/-- If no positive multiple of the invariant of `P` is the invariant of `Q`, no similar copy of `P` is scissors
congruent to a similar copy of `Q`. -/
theorem not_scissorsCongruent_of_not_pos_proportional {P Q P' Q' : Set R3} (hP : IsPoly P) (hQ : IsPoly Q)
    (h : ∀ t : ℝ, 0 < t → t • dehnSet P ≠ dehnSet Q) (hP' : IsSimilarCopy P P')
    (hQ' : IsSimilarCopy Q Q') : ¬ ScissorsCongruent P' Q' := by
  apply not_scissorsCongruent_of_dehnSet_ne (hP.similarCopy hP') (hQ.similarCopy hQ')
  obtain ⟨a, ha, e1⟩ := dehnSet_similarCopy hP'
  obtain ⟨c, hc, e2⟩ := dehnSet_similarCopy hQ'
  rw [e1, e2]
  intro he
  apply h (c⁻¹ * a) (mul_pos (inv_pos.2 hc) ha)
  rw [mul_smul, he, inv_smul_smul₀ hc.ne']

lemma smul_edgeTerm (t L θ : ℝ) : t • edgeTerm L θ = edgeTerm (t * L) θ := by
  unfold edgeTerm; rw [TensorProduct.smul_tmul', smul_eq_mul]

/-- Two invariants L ⊗ arccos(1/3) and M ⊗ arccos(1/3) with L < 0 < M are not positive multiples of each other. -/
lemma tet_not_pos_proportional {L M : ℝ} (h : L * M < 0) (t : ℝ) (ht : 0 < t) :
    t • edgeTerm L tetDihedral ≠ edgeTerm M tetDihedral := by
  rw [smul_edgeTerm]
  intro he
  have := edgeTerm_inj tetDihedral_not_ratPi he
  rw [← this] at h
  nlinarith [mul_pos ht (mul_self_pos.2 (show L ≠ 0 by rintro rfl; simp at h))]

/-- The tetrahedron of study 3 (edge 2√2): 12√2 ⊗ arccos(1/3). -/
lemma dehnSet_tetra_tet : dehnSet tetraSet = edgeTerm (12 * √2) tetDihedral := by
  rw [dehnSet_tetra, tetrahedron, dehn_const, List.sum_replicate, nsmul_eq_mul]
  congr 1; push_cast; ring

/-- **No octahedron is scissors congruent to a regular tetrahedron** (any sizes, any positions):
the invariants are −12√2 ⊗ arccos(1/3) and +12√2 ⊗ arccos(1/3), of opposite signs. -/
theorem oct_tetra_not_scissorsCongruent {O T : Set R3} (hO : IsSimilarCopy octSet O)
    (hT : IsSimilarCopy tetraSet T) : ¬ ScissorsCongruent O T :=
  not_scissorsCongruent_of_not_pos_proportional isPoly_oct isPoly_tetra (fun t ht => by
    rw [dehnSet_oct, dehnSet_tetra_tet]
    exact tet_not_pos_proportional (by nlinarith [Real.sqrt_pos.2 (show (0 : ℝ) < 2 by norm_num)]) t ht)
    hO hT

/-- **For 3/2 < t < 2 (Lucky 7 among them), no cube ∩ octahedron solid is scissors congruent to an
octahedron.** -/
theorem co_oct_not_scissorsCongruent {t : ℝ} (ht1 : 3 / 2 < t) (ht2 : t < 2) {C O : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hO : IsSimilarCopy octSet O) : ¬ ScissorsCongruent C O :=
  not_scissorsCongruent_of_not_pos_proportional (isPoly_co t) isPoly_oct (fun s hs => by
    rw [dehnSet_co (by linarith) ht2, dehnSet_oct]
    have h2 := Real.sqrt_pos.2 (show (0 : ℝ) < 2 by norm_num)
    exact tet_not_pos_proportional (by nlinarith [mul_pos h2 h2, mul_pos (mul_pos h2 h2) (sub_pos.2 ht1)])
      s hs) hC hO

/-- **For 1 < t < 3/2, no cube ∩ octahedron solid is scissors congruent to a regular tetrahedron.** -/
theorem co_tetra_not_scissorsCongruent {t : ℝ} (ht1 : 1 < t) (ht2 : t < 3 / 2) {C T : Set R3}
    (hC : IsSimilarCopy (coSet t) C) (hT : IsSimilarCopy tetraSet T) : ¬ ScissorsCongruent C T :=
  not_scissorsCongruent_of_not_pos_proportional (isPoly_co t) isPoly_tetra (fun s hs => by
    rw [dehnSet_co ht1 (by linarith), dehnSet_tetra_tet]
    have h2 := Real.sqrt_pos.2 (show (0 : ℝ) < 2 by norm_num)
    exact tet_not_pos_proportional (by nlinarith [mul_pos h2 h2, mul_pos (mul_pos h2 h2) (sub_pos.2 ht2)])
      s hs) hC hT

end DehnCanon
