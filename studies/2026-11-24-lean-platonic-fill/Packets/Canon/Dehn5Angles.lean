/-
Lean study 5 of the shape-language canon (DICTO, 19 Nov 2026), part O: the angles of the three words
AXE, CLEO, FUJI are combinations of two angles and π.

The four angles: α = arccos(1/√5), β (cos² β = 1/3 − 2√5/15), γ = arccos(√5/3) of study 4, and
ε = arccos((√5 + 1)/√(3(10 − 2√5))) (cos² ε = 1/3 + 2√5/15), the angle at the three short edges of FUJI.

* `wordBeta_eq_gamma_add_eps`: β = γ + ε (so ε = β − γ);
* `wordAlpha_add_wordBeta`: α + β = π − ε;
* `word_angle_relation`: α + 2β − γ = π; `word_angle_sum`: α + β + ε = π.

Method: for each relation, the cosine of the sum is computed with the addition formula from the exact values
of cos and sin (nested square roots; with r = √(3(10 − 2√5)): cos β = (3 − √5)/r, sin β = 4/r,
cos ε = (√5 + 1)/r, sin ε = (2√5 − 2)/r), and the sum lies in [0, π], where arccos ∘ cos is the identity.
The ranges need no comparison of angles: each of α, β, γ, ε lies in [0, π/2] because its cosine is ≥ 0.

Credits: Mathlib `Real.cos_arccos`, `Real.sin_arccos`, `Real.arccos_cos`, `Real.arccos_neg`,
`Real.arccos_le_pi_div_two`, `Real.cos_add`.
No `sorry`.
-/
module

public import Packets.Canon.Dehn4Words

@[expose] public section

open scoped RealInnerProductSpace Real
open Set Module TensorProduct

namespace DehnCanon.Library

/-- r = √(3(10 − 2√5)), the common denominator of cos β, sin β, cos ε, sin ε. -/
noncomputable def wordR : ℝ := √(3 * (10 - 2 * √5))

/-- ε = arccos((√5 + 1)/r) = 37.37…°, cos² ε = 1/3 + 2√5/15: the angle at the three short edges of FUJI. -/
noncomputable def wordEps : ℝ := Real.arccos ((√5 + 1) / wordR)

lemma wordBeta_def : wordBeta = Real.arccos ((3 - √5) / wordR) := rfl

lemma wordR_sq : wordR ^ 2 = 3 * (10 - 2 * √5) :=
  Real.sq_sqrt (by linarith [ten_sub_pos])

lemma wordR_pos : 0 < wordR := Real.sqrt_pos.2 (by linarith [ten_sub_pos])

/-- If `x² + y² = 1` and `y ≥ 0` then `√(1 − x²) = y`. -/
lemma sqrt_one_sub_sq {x y : ℝ} (hy : 0 ≤ y) (h : x ^ 2 + y ^ 2 = 1) : √(1 - x ^ 2) = y := by
  rw [show 1 - x ^ 2 = y ^ 2 by linarith, Real.sqrt_sq hy]

/-- `0 ≤ a / r ≤ 1` when `0 ≤ a` and `a² ≤ r²`. -/
lemma div_wordR_mem {a : ℝ} (ha : 0 ≤ a) (h : a ^ 2 ≤ wordR ^ 2) : 0 ≤ a / wordR ∧ a / wordR ≤ 1 := by
  refine ⟨div_nonneg ha wordR_pos.le, (div_le_one wordR_pos).2 ?_⟩
  exact le_of_sq_le_sq h wordR_pos.le

lemma sq_add_sq_div_wordR {a c : ℝ} (h : a ^ 2 + c ^ 2 = 3 * (10 - 2 * √5)) :
    (a / wordR) ^ 2 + (c / wordR) ^ 2 = 1 := by
  rw [div_pow, div_pow, ← add_div, h, ← wordR_sq]
  exact div_self (pow_ne_zero 2 wordR_pos.ne')

/-! ### cos and sin of the four angles -/

lemma cos_wordAlpha : Real.cos wordAlpha = √5 / 5 := by
  have h1 := one_lt_sqrt5
  have h3 := sqrt5_lt_three
  unfold wordAlpha; rw [Real.cos_arccos] <;> linarith

lemma sin_wordAlpha : Real.sin wordAlpha = 2 * √5 / 5 := by
  have h1 := one_lt_sqrt5
  unfold wordAlpha
  rw [Real.sin_arccos]
  exact sqrt_one_sub_sq (by linarith) (by linear_combination (1 / 5 : ℝ) * sqrt5_sq)

lemma cos_wordGamma : Real.cos wordGamma = √5 / 3 := by
  have h1 := one_lt_sqrt5
  have h3 := sqrt5_lt_three
  unfold wordGamma; rw [Real.cos_arccos] <;> linarith

lemma sin_wordGamma : Real.sin wordGamma = 2 / 3 := by
  unfold wordGamma
  rw [Real.sin_arccos]
  exact sqrt_one_sub_sq (by norm_num) (by linear_combination (1 / 9 : ℝ) * sqrt5_sq)

lemma beta_mem : 0 ≤ (3 - √5) / wordR ∧ (3 - √5) / wordR ≤ 1 := by
  have h3 := sqrt5_lt_three
  apply div_wordR_mem (by linarith)
  rw [wordR_sq]
  nlinarith [sqrt5_sq]

lemma eps_mem : 0 ≤ (√5 + 1) / wordR ∧ (√5 + 1) / wordR ≤ 1 := by
  have h1 := one_lt_sqrt5
  have h3 := sqrt5_lt_three
  apply div_wordR_mem (by linarith)
  rw [wordR_sq]
  nlinarith [sqrt5_sq]

lemma cos_wordBeta : Real.cos wordBeta = (3 - √5) / wordR := by
  rw [wordBeta_def, Real.cos_arccos (by linarith [beta_mem.1]) beta_mem.2]

lemma sin_wordBeta : Real.sin wordBeta = 4 / wordR := by
  rw [wordBeta_def, Real.sin_arccos]
  exact sqrt_one_sub_sq (div_nonneg (by norm_num) wordR_pos.le)
    (sq_add_sq_div_wordR (by linear_combination sqrt5_sq))

lemma cos_wordEps : Real.cos wordEps = (√5 + 1) / wordR := by
  unfold wordEps; rw [Real.cos_arccos (by linarith [eps_mem.1]) eps_mem.2]

lemma sin_wordEps : Real.sin wordEps = (2 * √5 - 2) / wordR := by
  have h1 := one_lt_sqrt5
  unfold wordEps
  rw [Real.sin_arccos]
  exact sqrt_one_sub_sq (div_nonneg (by linarith) wordR_pos.le)
    (sq_add_sq_div_wordR (by linear_combination (5 : ℝ) * sqrt5_sq))

/-! ### Each of the four angles lies in [0, π/2] -/

lemma wordAlpha_mem : 0 ≤ wordAlpha ∧ wordAlpha ≤ π / 2 :=
  ⟨Real.arccos_nonneg _, Real.arccos_le_pi_div_two.2 (by linarith [one_lt_sqrt5])⟩

lemma wordBeta_mem : 0 ≤ wordBeta ∧ wordBeta ≤ π / 2 :=
  ⟨Real.arccos_nonneg _, by rw [wordBeta_def]; exact Real.arccos_le_pi_div_two.2 beta_mem.1⟩

lemma wordGamma_mem : 0 ≤ wordGamma ∧ wordGamma ≤ π / 2 :=
  ⟨Real.arccos_nonneg _, Real.arccos_le_pi_div_two.2 (by linarith [one_lt_sqrt5])⟩

lemma wordEps_mem : 0 ≤ wordEps ∧ wordEps ≤ π / 2 :=
  ⟨Real.arccos_nonneg _, Real.arccos_le_pi_div_two.2 eps_mem.1⟩

/-! ### The relations -/

/-- **β = γ + ε**, that is ε = β − γ. -/
theorem wordBeta_eq_gamma_add_eps : wordBeta = wordGamma + wordEps := by
  have hcos : Real.cos (wordGamma + wordEps) = (3 - √5) / wordR := by
    rw [Real.cos_add, cos_wordGamma, sin_wordGamma, cos_wordEps, sin_wordEps]
    have e : √5 / 3 * ((√5 + 1) / wordR) - 2 / 3 * ((2 * √5 - 2) / wordR) =
        (3 - √5) / wordR + (√5 ^ 2 - 5) / (3 * wordR) := by ring
    rw [e, sqrt5_sq, sub_self, zero_div, add_zero]
  rw [wordBeta_def, ← hcos, Real.arccos_cos (by linarith [wordGamma_mem.1, wordEps_mem.1])
    (by linarith [wordGamma_mem.2, wordEps_mem.2])]

/-- **ε = β − γ.** -/
theorem wordEps_eq : wordEps = wordBeta - wordGamma := by
  rw [wordBeta_eq_gamma_add_eps]; ring

/-- **α + β = π − ε.** -/
theorem wordAlpha_add_wordBeta : wordAlpha + wordBeta = π - wordEps := by
  have hcos : Real.cos (wordAlpha + wordBeta) = -((√5 + 1) / wordR) := by
    rw [Real.cos_add, cos_wordAlpha, sin_wordAlpha, cos_wordBeta, sin_wordBeta]
    have e : √5 / 5 * ((3 - √5) / wordR) - 2 * √5 / 5 * (4 / wordR) =
        -((√5 + 1) / wordR) - (√5 ^ 2 - 5) / (5 * wordR) := by ring
    rw [e, sqrt5_sq, sub_self, zero_div, sub_zero]
  have h := Real.arccos_cos (x := wordAlpha + wordBeta) (by linarith [wordAlpha_mem.1, wordBeta_mem.1])
    (by linarith [wordAlpha_mem.2, wordBeta_mem.2])
  rw [hcos, Real.arccos_neg] at h
  exact h.symm

/-- **α + β + ε = π.** -/
theorem word_angle_sum : wordAlpha + wordBeta + wordEps = π := by
  linarith [wordAlpha_add_wordBeta]

/-- **α + 2β − γ = π.** -/
theorem word_angle_relation : wordAlpha + 2 * wordBeta - wordGamma = π := by
  linarith [wordAlpha_add_wordBeta, wordBeta_eq_gamma_add_eps]

/-- γ = α + 2β − π. -/
theorem wordGamma_eq : wordGamma = wordAlpha + 2 * wordBeta - π := by
  linarith [word_angle_relation]

/-- ε = π − α − β. -/
theorem wordEps_eq' : wordEps = π - wordAlpha - wordBeta := by
  linarith [wordAlpha_add_wordBeta]

end DehnCanon.Library
