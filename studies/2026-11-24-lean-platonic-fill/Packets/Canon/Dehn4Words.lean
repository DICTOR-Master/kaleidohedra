/-
Lean study 4 of the shape-language canon (DICTO, 19 Nov 2026), part N: two nonzero words, CLEO and AXE.

CLEO and AXE are two of the three pieces AXE, CLEO, FUJI of the study of 14 October 2026; both are tetrahedra
with corners in ℚ(√5) (exact form of the corner data of that study). For each this file proves, from the four
corners and four face normals (`IsTetraData`, part M):

* the solid is the convex hull of its four corners (`cleoSet_eq_convexHull`, `axeSet_eq_convexHull`);
* its Dehn invariant as a set is study 1's edge-list value (`dehnSet_cleo`, `dehnSet_axe`):
  CLEO: three edges of length 1 at α = arccos(1/√5) and three edges of length (√5 − 1)/2 at β;
  AXE: one edge of length (√5 − 1)/2 at α, four edges of length 1 at β, one edge of length 1 at γ = arccos(√5/3);
  β = arccos((3 − √5)/√(3(10 − 2√5))), so cos² β = 1/3 − 2√5/15;
* the invariant is not zero (`dehnSet_cleo_ne_zero`, `dehnSet_axe_ne_zero`);
* so no similar copy of CLEO or AXE is scissors congruent to a cube or to a cube ∩ rhombic dodecahedron solid
  of any size, in any position.

Why "not zero" is cheap for these two. In both, the edges at α have a total length that is not a rational
multiple of the total length of the other edges (1 against (√5 − 1)/2; √5 is irrational). A ℚ-linear map
ℝ → ℚ that kills the other length then leaves a nonzero multiple of α alone, and α is not a rational multiple of
π: cos 2α = −3/5 is rational and not one of 0, ±1/2, ±1 (Niven's theorem). The angles β and γ need not be
understood at all.

Credits: Niven's theorem `niven` (Mathlib `NumberTheory/Niven.lean`); the irrationality of √5
(Mathlib `Nat.Prime.irrational_sqrt`); the polynomial identities over ℚ(√5) are closed by the tactic `grind`.
No `sorry`.
-/
module

public import Packets.Canon.Dehn4Simplex

@[expose] public section

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct

namespace DehnCanon.Library

/-! ### √5 and the three angles -/

lemma sqrt5_sq : (√5 : ℝ) ^ 2 = 5 := Real.sq_sqrt (by norm_num)

lemma one_lt_sqrt5 : (1 : ℝ) < √5 := (Real.lt_sqrt (by norm_num)).2 (by norm_num)

lemma sqrt5_lt_three : (√5 : ℝ) < 3 := (Real.sqrt_lt' (by norm_num)).2 (by norm_num)

lemma irrational_sqrt5 : Irrational (√5 : ℝ) := by
  simpa using Nat.Prime.irrational_sqrt (show Nat.Prime 5 by norm_num)

/-- α = arccos(1/√5) = 63.43…°: the angle at the three long edges of CLEO and at the short edge of AXE. -/
noncomputable def wordAlpha : ℝ := Real.arccos (√5 / 5)

/-- β = 79.18…°, cos² β = 1/3 − 2√5/15: the angle at the three short edges of CLEO and at four edges of AXE. -/
noncomputable def wordBeta : ℝ := Real.arccos ((3 - √5) / √(3 * (10 - 2 * √5)))

/-- γ = arccos(√5/3) = 41.81…°: the angle at one edge of AXE. -/
noncomputable def wordGamma : ℝ := Real.arccos (√5 / 3)

/-- **α is not a rational multiple of π** (Niven's theorem applied to 2α: cos 2α = −3/5). -/
theorem wordAlpha_not_ratPi : wordAlpha ∉ ratPi := by
  rw [mem_ratPi_iff]
  rintro ⟨r, hr⟩
  have h1 := one_lt_sqrt5
  have h3 := sqrt5_lt_three
  have hcos : Real.cos wordAlpha = √5 / 5 := by
    unfold wordAlpha; rw [Real.cos_arccos] <;> linarith
  have h2 : Real.cos (2 * wordAlpha) = -3 / 5 := by
    rw [Real.cos_two_mul, hcos]
    linear_combination (2 / 25) * sqrt5_sq
  have hn := niven (θ := 2 * wordAlpha) ⟨2 * r, by rw [hr]; push_cast; ring⟩
    ⟨-3 / 5, by rw [h2]; norm_num⟩
  rw [h2] at hn
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hn
  norm_num at hn

lemma wordAlpha_class_ne_zero : (Submodule.Quotient.mk wordAlpha : Angle) ≠ 0 := by
  rw [Ne, Submodule.Quotient.mk_eq_zero]; exact wordAlpha_not_ratPi

/-- (√5 − 1)/2 is not a rational multiple of 1, and 1 is not a rational multiple of (√5 − 1)/2. -/
lemma gold_not_rat (q : ℚ) : (q : ℝ) * ((√5 - 1) / 2) ≠ 1 := by
  intro h
  have hq : (q : ℝ) ≠ 0 := by
    intro h0; rw [h0, zero_mul] at h; exact zero_ne_one h
  apply irrational_sqrt5
  refine ⟨1 + 2 / q, ?_⟩
  push_cast
  field_simp
  linarith

lemma rat_ne_gold (q : ℚ) : (q : ℝ) ≠ (√5 - 1) / 2 := by
  intro h
  apply irrational_sqrt5
  refine ⟨2 * q + 1, ?_⟩
  push_cast
  linarith

/-! ### CLEO -/

/-- The four corners of CLEO (exact form of the corner data of the study of 14 October 2026). -/
noncomputable def cleoP : Fin 4 → R3 :=
  ![!₂[-(1 + √5) / 4, -(1 + √5) / 4, -(1 + √5) / 4], !₂[(1 - √5) / 4, 0, -1 / 2],
    !₂[0, -1 / 2, (1 - √5) / 4], !₂[-1 / 2, (1 - √5) / 4, 0]]

/-- Outward normals of the four faces of CLEO; face `m` is opposite the corner `m`. -/
noncomputable def cleoN : Fin 4 → R3 :=
  ![!₂[1, 1, 1], !₂[0, -2, √5 - 1], !₂[-2, √5 - 1, 0], !₂[√5 - 1, 0, -2]]

noncomputable def cleoB : Fin 4 → ℝ := ![-(1 + √5) / 4, (√5 - 1) / 2, (√5 - 1) / 2, (√5 - 1) / 2]

noncomputable def cleoW : Fin 4 → ℝ := ![(√5 - 1) / 2, (√5 + 1) / 4, (√5 + 1) / 4, (√5 + 1) / 4]

/-- **CLEO**, as the intersection of its four face half-spaces. -/
def cleoSet : Set R3 := sol cleoN cleoB

theorem cleo_isTetraData : IsTetraData cleoN cleoP cleoB cleoW where
  w_pos := by
    intro m
    have h1 := one_lt_sqrt5
    fin_cases m <;> simp [cleoW] <;> linarith
  delta := by
    intro m k
    have ht := sqrt5_sq
    fin_cases m <;> fin_cases k <;> simp [cleoW, cleoB, cleoN, cleoP, inner3] <;> grind
  sum_one := by
    intro x
    have ht := sqrt5_sq
    simp [Fin.sum_univ_four, cleoW, cleoB, cleoN, inner3]
    grind
  rebuild := by
    intro x
    have ht := sqrt5_sq
    ext i
    fin_cases i <;> simp [Fin.sum_univ_four, cleoW, cleoB, cleoN, cleoP, inner3] <;> grind

/-- CLEO is the convex hull of its four corners. -/
theorem cleoSet_eq_convexHull : cleoSet = convexHull ℝ (Set.range cleoP) :=
  cleo_isTetraData.eq_convexHull

theorem isPoly_cleo : IsPoly cleoSet := cleo_isTetraData.isPoly

lemma cleo_dist_long (k : Fin 4) (hk : k ≠ 0) : dist (cleoP 0) (cleoP k) = 1 := by
  have ht := sqrt5_sq
  apply dist3 _ _ zero_le_one
  fin_cases k <;> simp [cleoP] at hk ⊢ <;> grind

lemma cleo_dist_short (k l : Fin 4) (hk : k ≠ 0) (hl : l ≠ 0) (hkl : k ≠ l) :
    dist (cleoP k) (cleoP l) = (√5 - 1) / 2 := by
  have ht := sqrt5_sq
  have h1 := one_lt_sqrt5
  apply dist3 _ _ (by linarith)
  fin_cases k <;> fin_cases l <;> simp [cleoP] at hk hl hkl ⊢ <;> grind

lemma ten_sub_pos : (0 : ℝ) < 10 - 2 * √5 := by linarith [sqrt5_lt_three]

/-- The angle value `arccos ((2√5 − 2)/√((10 − 2√5)(10 − 2√5)))` read off from two normals is α. -/
lemma alpha_form : Real.arccos ((2 * √5 - 2) / √((10 - 2 * √5) * (10 - 2 * √5))) = wordAlpha := by
  unfold wordAlpha
  congr 1
  rw [Real.sqrt_mul_self ten_sub_pos.le, div_eq_div_iff ten_sub_pos.ne' (by norm_num)]
  linear_combination (2 : ℝ) * sqrt5_sq

lemma alpha_gram_ne : (10 - 2 * √5) * (10 - 2 * √5) ≠ (2 * √5 - 2) ^ 2 := by
  intro h
  have h3 : (√5 : ℝ) = 3 := by linear_combination (-1 / 32 : ℝ) * h
  linarith [sqrt5_lt_three]

lemma beta_gram_ne : 3 * (10 - 2 * √5) ≠ (3 - √5) ^ 2 := by
  intro h
  have : (16 : ℝ) = 0 := by linear_combination h + sqrt5_sq
  norm_num at this

lemma cleoN_inner_side (i j : Fin 4) (hi : i ≠ 0) (hj : j ≠ 0) :
    ⟪cleoN i, cleoN j⟫ = if i = j then 10 - 2 * √5 else -(2 * √5 - 2) := by
  have ht := sqrt5_sq
  fin_cases i <;> fin_cases j <;> simp [cleoN, inner3, norm3_sq] at hi hj ⊢ <;> grind

lemma cleoN_inner_base (i : Fin 4) (hi : i ≠ 0) :
    ⟪cleoN 0, cleoN 0⟫ = 3 ∧ ⟪cleoN 0, cleoN i⟫ = -(3 - √5) := by
  have ht := sqrt5_sq
  fin_cases i <;> simp [cleoN, inner3, norm3_sq] at hi ⊢ <;> grind

/-- Where two of the three side faces of CLEO meet, the angle class is that of α. -/
lemma cleo_theta_long {A : Set (Fin 4)} {i j : Fin 4} (hA : A = {i, j}) (hi : i ≠ 0) (hj : j ≠ 0)
    (hij : i ≠ j) : theta (cone cleoN A) = (Submodule.Quotient.mk wordAlpha : Angle) := by
  rw [theta_pair_of_gram cleoN hA ten_sub_pos
    (by rw [cleoN_inner_side i i hi hi, ite_eq_left rfl])
    (by rw [cleoN_inner_side j j hj hj, ite_eq_left rfl])
    (by rw [cleoN_inner_side i j hi hj, ite_eq_right hij]) alpha_gram_ne, alpha_form]

/-- Where the base of CLEO meets a side face, the angle class is that of β. -/
lemma cleo_theta_short {A : Set (Fin 4)} {i : Fin 4} (hA : A = {0, i}) (hi : i ≠ 0) :
    theta (cone cleoN A) = (Submodule.Quotient.mk wordBeta : Angle) := by
  rw [theta_pair_of_gram cleoN hA (by norm_num) (cleoN_inner_base i hi).1
    (by rw [cleoN_inner_side i i hi hi, ite_eq_left rfl]) (cleoN_inner_base i hi).2 beta_gram_ne]
  rfl

/-- The edge list of CLEO (length, interior angle). -/
noncomputable def cleoEdges : List (ℝ × ℝ) :=
  [(1, wordAlpha), (1, wordAlpha), (1, wordAlpha), ((√5 - 1) / 2, wordBeta), ((√5 - 1) / 2, wordBeta),
    ((√5 - 1) / 2, wordBeta)]

/-- **The Dehn invariant of CLEO, as a set, is study 1's value of its edge list**: three edges of length 1 at
α and three edges of length (√5 − 1)/2 at β. -/
theorem dehnSet_cleo : dehnSet cleoSet = dehn cleoEdges := by
  unfold cleoSet
  rw [cleo_isTetraData.dehnSet_eq, sum_tetPairs]
  simp only []
  rw [cleo_theta_long (i := 2) (j := 3) (compl_pair_eq (by decide)) (by decide) (by decide) (by decide),
    cleo_theta_long (i := 1) (j := 3) (compl_pair_eq (by decide)) (by decide) (by decide) (by decide),
    cleo_theta_long (i := 1) (j := 2) (compl_pair_eq (by decide)) (by decide) (by decide) (by decide),
    cleo_theta_short (i := 3) (compl_pair_eq (by decide)) (by decide),
    cleo_theta_short (i := 2) (compl_pair_eq (by decide)) (by decide),
    cleo_theta_short (i := 1) (compl_pair_eq (by decide)) (by decide),
    cleo_dist_long 1 (by decide), cleo_dist_long 2 (by decide), cleo_dist_long 3 (by decide),
    cleo_dist_short 1 2 (by decide) (by decide) (by decide),
    cleo_dist_short 1 3 (by decide) (by decide) (by decide),
    cleo_dist_short 2 3 (by decide) (by decide) (by decide)]
  simp only [dehn, cleoEdges, edgeTerm, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
    add_zero, add_assoc]

/-- **CLEO is a nonzero word**: its Dehn invariant is not zero. -/
theorem dehnSet_cleo_ne_zero : dehnSet cleoSet ≠ 0 := by
  rw [dehnSet_cleo]
  have h : dehn cleoEdges = (3 : ℝ) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      (3 * ((√5 - 1) / 2)) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle) := by
    simp only [dehn, cleoEdges, edgeTerm, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
      add_zero]
    rw [show (3 : ℝ) * ((√5 - 1) / 2) = (√5 - 1) / 2 + (√5 - 1) / 2 + (√5 - 1) / 2 by ring,
      show (3 : ℝ) = 1 + 1 + 1 by norm_num, TensorProduct.add_tmul, TensorProduct.add_tmul,
      TensorProduct.add_tmul, TensorProduct.add_tmul]
    abel
  rw [h]
  refine tmul_add_tmul_ne_zero ?_ wordAlpha_class_ne_zero
  rw [Submodule.mem_span_singleton]
  rintro ⟨q, hq⟩
  rw [Rat.smul_def] at hq
  exact gold_not_rat q (by linarith)

/-- **No CLEO is scissors congruent to a cube**: any size, any position of both. -/
theorem cleo_not_scissorsCongruent_cube {C Q : Set R3} (hC : IsSimilarCopy cleoSet C)
    (hQ : IsSimilarCopy (cubeSet 1) Q) : ¬ ScissorsCongruent C Q :=
  not_scissorsCongruent_similarCopies isPoly_cleo (isPoly_cube 1) dehnSet_cleo_ne_zero
    (dehnSet_cube 1 one_pos) hC hQ

/-- No CLEO is scissors congruent to a cube ∩ rhombic dodecahedron solid (the fair 18-face die among them). -/
theorem cleo_not_scissorsCongruent_cubeRD (s c : ℝ) {C Q : Set R3} (hC : IsSimilarCopy cleoSet C)
    (hQ : IsSimilarCopy (cubeRDSet s c) Q) : ¬ ScissorsCongruent C Q :=
  not_scissorsCongruent_similarCopies isPoly_cleo (isPoly_cubeRD s c) dehnSet_cleo_ne_zero
    (dehnSet_cubeRD s c) hC hQ

/-! ### AXE -/

/-- The four corners of AXE (exact form of the corner data of the study of 14 October 2026). -/
noncomputable def axeP : Fin 4 → R3 :=
  ![!₂[-(1 + √5) / 4, -(1 + √5) / 4, -(1 + √5) / 4], !₂[0, -1 / 2, -(3 + √5) / 4],
    !₂[-(1 + √5) / 4, -(1 + √5) / 4, -(5 + √5) / 4], !₂[-1 / 2, -(3 + √5) / 4, -(1 + √5) / 2]]

/-- Outward normals of the four faces of AXE; face `m` is opposite the corner `m`. -/
noncomputable def axeN : Fin 4 → R3 :=
  ![!₂[√5 - 1, 0, -2], !₂[-2, 1 - √5, 0], !₂[1, -1, 1], !₂[1 - √5, 1 + √5, 0]]

noncomputable def axeB : Fin 4 → ℝ := ![(3 + √5) / 2, (3 + √5) / 2, -(1 + √5) / 4, -(1 + √5) / 2]

noncomputable def axeW : Fin 4 → ℝ := ![1 / 2, 1 / 2, 1, 1 / 2]

/-- **AXE**, as the intersection of its four face half-spaces. -/
def axeSet : Set R3 := sol axeN axeB

theorem axe_isTetraData : IsTetraData axeN axeP axeB axeW where
  w_pos := by
    intro m
    fin_cases m <;> simp [axeW]
  delta := by
    intro m k
    have ht := sqrt5_sq
    fin_cases m <;> fin_cases k <;> simp [axeW, axeB, axeN, axeP, inner3] <;> grind
  sum_one := by
    intro x
    have ht := sqrt5_sq
    simp [Fin.sum_univ_four, axeW, axeB, axeN, inner3]
    grind
  rebuild := by
    intro x
    have ht := sqrt5_sq
    ext i
    fin_cases i <;> simp [Fin.sum_univ_four, axeW, axeB, axeN, axeP, inner3] <;> grind

/-- AXE is the convex hull of its four corners. -/
theorem axeSet_eq_convexHull : axeSet = convexHull ℝ (Set.range axeP) :=
  axe_isTetraData.eq_convexHull

theorem isPoly_axe : IsPoly axeSet := axe_isTetraData.isPoly

/-- The Gram numbers of the four normals of AXE. -/
lemma axeN_gram :
    ⟪axeN 0, axeN 0⟫ = 10 - 2 * √5 ∧ ⟪axeN 1, axeN 1⟫ = 10 - 2 * √5 ∧ ⟪axeN 2, axeN 2⟫ = 3 ∧
    ⟪axeN 3, axeN 3⟫ = 12 ∧ ⟪axeN 2, axeN 3⟫ = -(2 * √5) ∧ ⟪axeN 1, axeN 3⟫ = -(6 - 2 * √5) ∧
    ⟪axeN 1, axeN 2⟫ = -(3 - √5) ∧ ⟪axeN 0, axeN 3⟫ = -(6 - 2 * √5) ∧
    ⟪axeN 0, axeN 2⟫ = -(3 - √5) ∧ ⟪axeN 0, axeN 1⟫ = -(2 * √5 - 2) := by
  have ht := sqrt5_sq
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp [axeN, inner3, norm3_sq] <;> grind

lemma beta_form1 : Real.arccos ((3 - √5) / √((10 - 2 * √5) * 3)) = wordBeta := by
  unfold wordBeta; rw [mul_comm (10 - 2 * √5) 3]

lemma beta_form2 : Real.arccos ((6 - 2 * √5) / √((10 - 2 * √5) * 12)) = wordBeta := by
  unfold wordBeta
  congr 1
  rw [show (10 - 2 * √5) * 12 = 2 ^ 2 * (3 * (10 - 2 * √5)) by ring, Real.sqrt_mul (by norm_num),
    Real.sqrt_sq (by norm_num), show (6 - 2 * √5) = 2 * (3 - √5) by ring,
    mul_div_mul_left _ _ two_ne_zero]

lemma gamma_form : Real.arccos (2 * √5 / √(3 * 12)) = wordGamma := by
  unfold wordGamma
  congr 1
  rw [show (3 : ℝ) * 12 = 6 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  ring

lemma beta_gram_ne1 : (10 - 2 * √5) * 3 ≠ (3 - √5) ^ 2 := by
  intro h
  have : (16 : ℝ) = 0 := by linear_combination h + sqrt5_sq
  norm_num at this

lemma beta_gram_ne2 : (10 - 2 * √5) * 12 ≠ (6 - 2 * √5) ^ 2 := by
  intro h
  have : (64 : ℝ) = 0 := by linear_combination h + 4 * sqrt5_sq
  norm_num at this

lemma gamma_gram_ne : (3 : ℝ) * 12 ≠ (2 * √5) ^ 2 := by
  intro h
  have : (16 : ℝ) = 0 := by linear_combination h + 4 * sqrt5_sq
  norm_num at this

/-- The edge list of AXE (length, interior angle), in the order of the corner pairs
(0,1), (0,2), (0,3), (1,2), (1,3), (2,3). -/
noncomputable def axeEdges : List (ℝ × ℝ) :=
  [(1, wordGamma), (1, wordBeta), (1, wordBeta), (1, wordBeta), (1, wordBeta),
    ((√5 - 1) / 2, wordAlpha)]

/-- **The Dehn invariant of AXE, as a set, is study 1's value of its edge list**: one edge of length 1 at γ,
four edges of length 1 at β and one edge of length (√5 − 1)/2 at α. -/
theorem dehnSet_axe : dehnSet axeSet = dehn axeEdges := by
  obtain ⟨g00, g11, g22, g33, g23, g13, g12, g03, g02, g01⟩ := axeN_gram
  have ht := sqrt5_sq
  have h1 := one_lt_sqrt5
  have e01 : theta (cone axeN ({0, 1}ᶜ : Set (Fin 4))) = (Submodule.Quotient.mk wordGamma : Angle) := by
    rw [theta_pair_of_gram axeN (i := 2) (j := 3) (compl_pair_eq (by decide)) (by norm_num) g22 g33 g23
      gamma_gram_ne, gamma_form]
  have e02 : theta (cone axeN ({0, 2}ᶜ : Set (Fin 4))) = (Submodule.Quotient.mk wordBeta : Angle) := by
    rw [theta_pair_of_gram axeN (i := 1) (j := 3) (compl_pair_eq (by decide)) ten_sub_pos g11 g33 g13
      beta_gram_ne2, beta_form2]
  have e03 : theta (cone axeN ({0, 3}ᶜ : Set (Fin 4))) = (Submodule.Quotient.mk wordBeta : Angle) := by
    rw [theta_pair_of_gram axeN (i := 1) (j := 2) (compl_pair_eq (by decide)) ten_sub_pos g11 g22 g12
      beta_gram_ne1, beta_form1]
  have e12 : theta (cone axeN ({1, 2}ᶜ : Set (Fin 4))) = (Submodule.Quotient.mk wordBeta : Angle) := by
    rw [theta_pair_of_gram axeN (i := 0) (j := 3) (compl_pair_eq (by decide)) ten_sub_pos g00 g33 g03
      beta_gram_ne2, beta_form2]
  have e13 : theta (cone axeN ({1, 3}ᶜ : Set (Fin 4))) = (Submodule.Quotient.mk wordBeta : Angle) := by
    rw [theta_pair_of_gram axeN (i := 0) (j := 2) (compl_pair_eq (by decide)) ten_sub_pos g00 g22 g02
      beta_gram_ne1, beta_form1]
  have e23 : theta (cone axeN ({2, 3}ᶜ : Set (Fin 4))) = (Submodule.Quotient.mk wordAlpha : Angle) := by
    rw [theta_pair_of_gram axeN (i := 0) (j := 1) (compl_pair_eq (by decide)) ten_sub_pos g00 g11 g01
      alpha_gram_ne, alpha_form]
  have d01 : dist (axeP 0) (axeP 1) = 1 := dist3 _ _ zero_le_one (by simp [axeP]; grind)
  have d02 : dist (axeP 0) (axeP 2) = 1 := dist3 _ _ zero_le_one (by simp [axeP]; grind)
  have d03 : dist (axeP 0) (axeP 3) = 1 := dist3 _ _ zero_le_one (by simp [axeP]; grind)
  have d12 : dist (axeP 1) (axeP 2) = 1 := dist3 _ _ zero_le_one (by simp [axeP]; grind)
  have d13 : dist (axeP 1) (axeP 3) = 1 := dist3 _ _ zero_le_one (by simp [axeP]; grind)
  have d23 : dist (axeP 2) (axeP 3) = (√5 - 1) / 2 :=
    dist3 _ _ (by linarith) (by simp [axeP]; grind)
  unfold axeSet
  rw [axe_isTetraData.dehnSet_eq, sum_tetPairs]
  simp only []
  rw [e01, e02, e03, e12, e13, e23, d01, d02, d03, d12, d13, d23]
  simp only [dehn, axeEdges, edgeTerm, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
    add_zero, add_assoc]

/-- **AXE is a nonzero word**: its Dehn invariant is not zero. -/
theorem dehnSet_axe_ne_zero : dehnSet axeSet ≠ 0 := by
  rw [dehnSet_axe]
  have h : dehn axeEdges = ((√5 - 1) / 2) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      (1 : ℝ) ⊗ₜ[ℚ] ((Submodule.Quotient.mk wordGamma : Angle) + Submodule.Quotient.mk wordBeta +
        Submodule.Quotient.mk wordBeta + Submodule.Quotient.mk wordBeta +
        Submodule.Quotient.mk wordBeta) := by
    simp only [dehn, axeEdges, edgeTerm, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
      add_zero]
    rw [TensorProduct.tmul_add, TensorProduct.tmul_add, TensorProduct.tmul_add,
      TensorProduct.tmul_add]
    abel
  rw [h]
  refine tmul_add_tmul_ne_zero ?_ wordAlpha_class_ne_zero
  rw [Submodule.mem_span_singleton]
  rintro ⟨q, hq⟩
  rw [Rat.smul_def, mul_one] at hq
  exact rat_ne_gold q hq

/-- **No AXE is scissors congruent to a cube**: any size, any position of both. -/
theorem axe_not_scissorsCongruent_cube {C Q : Set R3} (hC : IsSimilarCopy axeSet C)
    (hQ : IsSimilarCopy (cubeSet 1) Q) : ¬ ScissorsCongruent C Q :=
  not_scissorsCongruent_similarCopies isPoly_axe (isPoly_cube 1) dehnSet_axe_ne_zero
    (dehnSet_cube 1 one_pos) hC hQ

/-- No AXE is scissors congruent to a cube ∩ rhombic dodecahedron solid (the fair 18-face die among them). -/
theorem axe_not_scissorsCongruent_cubeRD (s c : ℝ) {C Q : Set R3} (hC : IsSimilarCopy axeSet C)
    (hQ : IsSimilarCopy (cubeRDSet s c) Q) : ¬ ScissorsCongruent C Q :=
  not_scissorsCongruent_similarCopies isPoly_axe (isPoly_cubeRD s c) dehnSet_axe_ne_zero
    (dehnSet_cubeRD s c) hC hQ

end DehnCanon.Library
