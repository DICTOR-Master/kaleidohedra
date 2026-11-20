/-
Dehn–Hadwiger study, part 5: size and position (DICTO, 20 Nov 2026).

`dehnHadwiger_smul_set`: scaling a set by `a > 0` multiplies its invariant by `a ^ (n - 2)` (the ridge measure
scales, the angles do not). With rigid motions (part 3) this gives the invariant of every similar copy
(`DehnCanon.IsSimilarCopy`, reused: it does not depend on the dimension). The Canon's `tcone_smul_set` and
`IsPoly.smul_set`, `IsPoly.similarCopy` are reused.
Credits: Mathlib `MeasureTheory.Measure.hausdorffMeasure_smul₀`.
No `sorry`.
-/
import DehnHadwiger.DH4Pair
import DehnCanon.Dehn4Similar

open scoped RealInnerProductSpace Pointwise
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

lemma ridgeAngle_smul_set {a : ℝ} (ha : 0 < a) (P : Set E) (x : E) :
    ridgeAngle (a • P) (a • x) = ridgeAngle P x := by
  unfold ridgeAngle; rw [tcone_smul_set ha]

/-- **Scaling.** The invariant of `P` scaled by `a > 0` is `a ^ (n - 2)` times the invariant of `P`. -/
theorem dehnHadwiger_smul_set {a : ℝ} (ha : 0 < a) (P : Set E) :
    dehnHadwiger (a • P) = (a ^ (finrank ℝ E - 2)) • dehnHadwiger P := by
  unfold dehnHadwiger
  rw [smul_finsum]
  apply finsum_congr; intro θ
  have h : {y | ridgeAngle (a • P) y = θ} = a • {x | ridgeAngle P x = θ} := by
    ext y; constructor
    · intro hy
      refine ⟨a⁻¹ • y, ?_, smul_inv_smul₀ ha.ne' y⟩
      show ridgeAngle P (a⁻¹ • y) = θ
      rw [← ridgeAngle_smul_set ha P, smul_inv_smul₀ ha.ne']; exact hy
    · rintro ⟨x, hx, rfl⟩
      show ridgeAngle (a • P) (a • x) = θ
      rw [ridgeAngle_smul_set ha]; exact hx
  rw [h, Measure.hausdorffMeasure_smul₀ (Nat.cast_nonneg _) ha.ne', TensorProduct.smul_tmul']
  congr 1
  rw [NNReal.rpow_natCast, ENNReal.toReal_smul, NNReal.smul_def, NNReal.coe_pow, coe_nnnorm,
    Real.norm_eq_abs, abs_of_pos ha]

/-- The invariant of a similar copy: that of the original times a positive number. -/
theorem dehnHadwiger_similarCopy {P Q : Set E} (h : IsSimilarCopy P Q) :
    ∃ c : ℝ, 0 < c ∧ dehnHadwiger Q = c • dehnHadwiger P := by
  obtain ⟨a, ha, g, rfl⟩ := h
  exact ⟨a ^ (finrank ℝ E - 2), pow_pos ha _, by rw [dehnHadwiger_image, dehnHadwiger_smul_set ha]⟩

/-- A similar copy has invariant zero exactly when the original has. -/
theorem dehnHadwiger_similarCopy_eq_zero_iff {P Q : Set E} (h : IsSimilarCopy P Q) :
    dehnHadwiger Q = 0 ↔ dehnHadwiger P = 0 := by
  obtain ⟨a, ha, hQ⟩ := dehnHadwiger_similarCopy h
  rw [hQ]
  constructor
  · intro h0
    have h1 := congrArg (fun D => a⁻¹ • D) h0
    simpa [inv_smul_smul₀ ha.ne'] using h1
  · intro h0; rw [h0, smul_zero]

/-- Convex polytopes one of which has invariant zero and the other not are not scissors congruent, and the
same holds for all their similar copies. -/
theorem not_scissorsCongruent_similarCopies {P Q P' Q' : Set E}
    (hP : IsPoly P) (hQ : IsPoly Q) (hPne : dehnHadwiger P ≠ 0) (hQ0 : dehnHadwiger Q = 0)
    (hP' : IsSimilarCopy P P') (hQ' : IsSimilarCopy Q Q') : ¬ ScissorsCongruent P' Q' := by
  apply not_scissorsCongruent_of_dehnHadwiger_ne (hP.similarCopy hP') (hQ.similarCopy hQ')
  rw [(dehnHadwiger_similarCopy_eq_zero_iff hQ').2 hQ0]
  exact fun h => hPne ((dehnHadwiger_similarCopy_eq_zero_iff hP').1 h)

end DehnHadwiger
