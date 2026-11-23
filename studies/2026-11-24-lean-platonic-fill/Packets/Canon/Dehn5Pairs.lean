/-
Lean study 5 of the shape-language canon (DICTO, 19 Nov 2026), part R: can two of the three words be scissors
congruent to each other (similar copies, any sizes)? A conditional answer.

Over the two angles α, β the three words are (part Q, g = (√5 − 1)/2)
CLEO = 3 ⊗ α + 3g ⊗ β, AXE = (1 + g) ⊗ α + 6 ⊗ β, FUJI = (9 − 3g) ⊗ α + (12 − 3g) ⊗ β.

`WordAnglesIndep`: modulo π, α is not a rational multiple of β and β is not a rational multiple of α
(equivalently: α, β, π are linearly independent over ℚ). THIS IS A HYPOTHESIS HERE; it is not proved in Lean.

* `not_proportional`: if θ₁, θ₂ are independent in this sense and `a d ≠ b c`, then no real multiple of
  `a ⊗ θ₁ + b ⊗ θ₂` equals `c ⊗ θ₁ + d ⊗ θ₂`.
* `cleo_axe_not_proportional`, `cleo_fuji_not_proportional`, `axe_fuji_not_proportional`: under
  `WordAnglesIndep`, no real multiple of the invariant of one word is the invariant of another.
* `cleo_axe_not_scissorsCongruent`, `cleo_fuji_not_scissorsCongruent`, `axe_fuji_not_scissorsCongruent`: under
  `WordAnglesIndep`, no similar copy of one word is scissors congruent to a similar copy of another.

Without the hypothesis nothing is decided: if β were a rational multiple of α modulo π, all three invariants
would be real multiples of 1 ⊗ α, and so proportional.

Credits: Mathlib `Submodule.exists_dual_map_eq_bot_of_notMem`, `TensorProduct.lift`,
`TensorProduct.inductionOn`, `TensorProduct.smul_tmul'`; the method (a ℚ-linear map on the angle factor) is
that of study 4's `tmul_add_tmul_ne_zero`.
No `sorry`.
-/
module

public import Packets.Canon.Dehn5Fuji

@[expose] public section

open scoped RealInnerProductSpace Real
open Set Module TensorProduct

namespace DehnCanon.Library

/-- The ℚ-linear map `L ⊗ θ ↦ f θ • L` from the Dehn space to the lengths, for a ℚ-linear `f` on angle
classes. -/
noncomputable def lengthPart (f : Module.Dual ℚ Angle) : DehnSpace →ₗ[ℚ] ℝ :=
  TensorProduct.lift ((LinearMap.lsmul ℚ ℝ).comp f).flip

lemma lengthPart_tmul (f : Module.Dual ℚ Angle) (L : ℝ) (θ : Angle) :
    lengthPart f (L ⊗ₜ[ℚ] θ) = f θ • L := by
  simp [lengthPart]

/-- `lengthPart f` respects multiplication of the lengths by a real number. -/
lemma lengthPart_smul (f : Module.Dual ℚ Angle) (t : ℝ) (x : DehnSpace) :
    lengthPart f (t • x) = t * lengthPart f x := by
  induction x using TensorProduct.inductionOn with
  | tmul L θ =>
    rw [TensorProduct.smul_tmul', lengthPart_tmul, lengthPart_tmul, smul_eq_mul, mul_smul_comm]
  | add x y hx hy => rw [smul_add, map_add, map_add, hx, hy, mul_add]

/-- **Two invariants over two independent angles are proportional only if their coefficients are.** -/
theorem not_proportional {a b c d : ℝ} {θ₁ θ₂ : Angle} (h1 : θ₁ ∉ Submodule.span ℚ {θ₂})
    (h2 : θ₂ ∉ Submodule.span ℚ {θ₁}) (hdet : a * d ≠ b * c) (t : ℝ) :
    t • (a ⊗ₜ[ℚ] θ₁ + b ⊗ₜ[ℚ] θ₂) ≠ (c ⊗ₜ[ℚ] θ₁ + d ⊗ₜ[ℚ] θ₂ : DehnSpace) := by
  intro h
  obtain ⟨f, hf, hf0⟩ := Submodule.exists_dual_map_eq_bot_of_notMem h1 inferInstance
  have hf2 : f θ₂ = 0 := by
    have h3 : f θ₂ ∈ (Submodule.span ℚ {θ₂}).map f :=
      Submodule.mem_map_of_mem (Submodule.mem_span_singleton_self _)
    rw [hf0] at h3
    exact (Submodule.mem_bot ℚ).1 h3
  obtain ⟨g, hg, hg0⟩ := Submodule.exists_dual_map_eq_bot_of_notMem h2 inferInstance
  have hg1 : g θ₁ = 0 := by
    have h3 : g θ₁ ∈ (Submodule.span ℚ {θ₁}).map g :=
      Submodule.mem_map_of_mem (Submodule.mem_span_singleton_self _)
    rw [hg0] at h3
    exact (Submodule.mem_bot ℚ).1 h3
  have e1 := congrArg (lengthPart f) h
  rw [lengthPart_smul, map_add, map_add, lengthPart_tmul, lengthPart_tmul, lengthPart_tmul,
    lengthPart_tmul, hf2, zero_smul, zero_smul, add_zero, add_zero, Rat.smul_def, Rat.smul_def] at e1
  have e2 := congrArg (lengthPart g) h
  rw [lengthPart_smul, map_add, map_add, lengthPart_tmul, lengthPart_tmul, lengthPart_tmul,
    lengthPart_tmul, hg1, zero_smul, zero_smul, zero_add, zero_add, Rat.smul_def, Rat.smul_def] at e2
  have e1' : t * a = c :=
    mul_left_cancel₀ (Rat.cast_ne_zero.2 hf : ((f θ₁ : ℚ) : ℝ) ≠ 0) (by linear_combination e1)
  have e2' : t * b = d :=
    mul_left_cancel₀ (Rat.cast_ne_zero.2 hg : ((g θ₂ : ℚ) : ℝ) ≠ 0) (by linear_combination e2)
  apply hdet
  rw [← e1', ← e2']
  ring

/-- The hypothesis of this part: modulo π, α is not a rational multiple of β, and β is not a rational multiple
of α. Not proved in Lean. -/
def WordAnglesIndep : Prop :=
  (Submodule.Quotient.mk wordAlpha : Angle) ∉ Submodule.span ℚ {(Submodule.Quotient.mk wordBeta : Angle)} ∧
  (Submodule.Quotient.mk wordBeta : Angle) ∉ Submodule.span ℚ {(Submodule.Quotient.mk wordAlpha : Angle)}

theorem cleo_axe_not_proportional (h : WordAnglesIndep) (t : ℝ) :
    t • dehnSet cleoSet ≠ dehnSet axeSet := by
  rw [dehnSet_cleo, dehnSet_axe, dehn_cleo_alpha_beta, dehn_axe_alpha_beta]
  exact not_proportional h.1 h.2 (by intro h'; nlinarith [sqrt5_sq]) t

theorem cleo_fuji_not_proportional (h : WordAnglesIndep) (t : ℝ) :
    t • dehnSet cleoSet ≠ dehnSet fujiSet := by
  rw [dehnSet_cleo, dehnSet_fuji, dehn_cleo_alpha_beta, dehn_fuji_alpha_beta]
  exact not_proportional h.1 h.2 (by intro h'; nlinarith [sqrt5_sq, sqrt5_lt_three]) t

theorem axe_fuji_not_proportional (h : WordAnglesIndep) (t : ℝ) :
    t • dehnSet axeSet ≠ dehnSet fujiSet := by
  rw [dehnSet_axe, dehnSet_fuji, dehn_axe_alpha_beta, dehn_fuji_alpha_beta]
  exact not_proportional h.1 h.2 (by intro h'; nlinarith [sqrt5_sq, sqrt5_lt_three]) t

/-- If no real multiple of the invariant of `P` is the invariant of `Q`, no similar copy of `P` is scissors
congruent to a similar copy of `Q`. -/
theorem not_scissorsCongruent_of_not_proportional {P Q P' Q' : Set R3} (hP : IsPoly P) (hQ : IsPoly Q)
    (h : ∀ t : ℝ, t • dehnSet P ≠ dehnSet Q) (hP' : IsSimilarCopy P P') (hQ' : IsSimilarCopy Q Q') :
    ¬ ScissorsCongruent P' Q' := by
  apply not_scissorsCongruent_of_dehnSet_ne (hP.similarCopy hP') (hQ.similarCopy hQ')
  obtain ⟨a, -, e1⟩ := dehnSet_similarCopy hP'
  obtain ⟨c, hc, e2⟩ := dehnSet_similarCopy hQ'
  rw [e1, e2]
  intro he
  apply h (c⁻¹ * a)
  rw [mul_smul, he, inv_smul_smul₀ hc.ne']

/-- **Conditional**: if α and β are independent modulo π, no CLEO is scissors congruent to an AXE
(any sizes, any positions). -/
theorem cleo_axe_not_scissorsCongruent (h : WordAnglesIndep) {C A : Set R3}
    (hC : IsSimilarCopy cleoSet C) (hA : IsSimilarCopy axeSet A) : ¬ ScissorsCongruent C A :=
  not_scissorsCongruent_of_not_proportional isPoly_cleo isPoly_axe (cleo_axe_not_proportional h) hC hA

/-- **Conditional**: if α and β are independent modulo π, no CLEO is scissors congruent to a FUJI. -/
theorem cleo_fuji_not_scissorsCongruent (h : WordAnglesIndep) {C F : Set R3}
    (hC : IsSimilarCopy cleoSet C) (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent C F :=
  not_scissorsCongruent_of_not_proportional isPoly_cleo isPoly_fuji (cleo_fuji_not_proportional h) hC hF

/-- **Conditional**: if α and β are independent modulo π, no AXE is scissors congruent to a FUJI. -/
theorem axe_fuji_not_scissorsCongruent (h : WordAnglesIndep) {A F : Set R3}
    (hA : IsSimilarCopy axeSet A) (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent A F :=
  not_scissorsCongruent_of_not_proportional isPoly_axe isPoly_fuji (axe_fuji_not_proportional h) hA hF

end DehnCanon.Library
