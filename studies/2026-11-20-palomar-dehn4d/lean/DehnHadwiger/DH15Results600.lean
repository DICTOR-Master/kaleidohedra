/-
Dehn–Hadwiger study, part 15: the 600-cell against the other regular 4-polytopes (DICTO, 20 Nov 2026).

* `similarCell600_not_scissorsCongruent`: no similar copy of the regular 600-cell is scissors congruent to a similar
  copy of the tesseract, the 16-cell, the 24-cell or the 120-cell.
* `similarCell5_not_scissorsCongruent_similarCell600`: no similar copy of the 5-cell is scissors congruent to a
  similar copy of the 600-cell. Both invariants are non-zero multiples of one tensor (area) ⊗ arccos(1/4), with
  opposite signs, because the 600-cell's dihedral angle is 4π/3 − arccos(1/4) (part 13).
No `sorry`.
-/
import DehnHadwiger.DH14Cell600Area
import DehnHadwiger.DH9Results

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

/-- **The 600-cell against the four regular 4-polytopes with invariant zero**, any size and any position. -/
theorem similarCell600_not_scissorsCongruent {T Q : Set R4} (hT : IsSimilarCopy cell600 T)
    (hQ : IsSimilarCopy tesseract Q ∨ IsSimilarCopy cell16 Q ∨ IsSimilarCopy cell24 Q ∨
      IsSimilarCopy cell120 Q) : ¬ ScissorsCongruent T Q := by
  rcases hQ with h | h | h | h
  · exact not_scissorsCongruent_similarCopies isPoly_cell600 isPoly_tesseract dehnHadwiger_cell600_ne_zero
      dehnHadwiger_tesseract hT h
  · exact not_scissorsCongruent_similarCopies isPoly_cell600 isPoly_cell16 dehnHadwiger_cell600_ne_zero
      dehnHadwiger_cell16 hT h
  · exact not_scissorsCongruent_similarCopies isPoly_cell600 isPoly_cell24 dehnHadwiger_cell600_ne_zero
      dehnHadwiger_cell24 hT h
  · exact not_scissorsCongruent_similarCopies isPoly_cell600 isPoly_cell120 dehnHadwiger_cell600_ne_zero
      dehnHadwiger_cell120 hT h

/-- The area of the ridge points of the 5-cell, as a positive real number. -/
lemma cell5_area_real_pos : 0 < (μH[(finrank ℝ R4 - 2 : ℕ)]
    {x | ridgeAngle cell5 x = Submodule.Quotient.mk (Real.arccos (1 / 4))}).toReal := by
  have hτ : (Submodule.Quotient.mk (Real.arccos (1 / 4)) : Angle) ≠ 0 := by
    rw [Ne, Submodule.Quotient.mk_eq_zero]; exact arccos_quarter_not_ratPi
  have hfin : μH[(finrank ℝ R4 - 2 : ℕ)]
      {x | ridgeAngle cell5 x = Submodule.Quotient.mk (Real.arccos (1 / 4))} ≠ ⊤ := by
    refine ne_top_of_le_ne_top (support_finite fiveN (fun _ => 1) isPoly_cell5.1) (measure_mono ?_)
    intro x hx; rw [mem_ofPred_eq] at hx ⊢; show ridgeAngle cell5 x ≠ 0; rw [hx]; exact hτ
  have hpos := cell5_area_pos
  rw [← finrank_R4_sub] at hpos
  exact ENNReal.toReal_pos hpos.ne' hfin

/-- The area of the ridge points of the 600-cell, as a positive real number. -/
lemma cell600_area_real_pos : 0 < (μH[(finrank ℝ R4 - 2 : ℕ)]
    {x | ridgeAngle cell600 x = Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4))}).toReal := by
  have hτ : (Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4)) : Angle) ≠ 0 := by
    rw [Ne, Submodule.Quotient.mk_eq_zero]; exact angle600_not_ratPi
  have hfin : μH[(finrank ℝ R4 - 2 : ℕ)]
      {x | ridgeAngle cell600 x = Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4))} ≠ ⊤ := by
    refine ne_top_of_le_ne_top (support_finite (fun z : {z // z ∈ cell600Z} => gvec z.1) (fun _ => 1)
      isPoly_cell600.1) (measure_mono ?_)
    intro x hx; rw [mem_ofPred_eq] at hx ⊢; show ridgeAngle cell600 x ≠ 0; rw [hx]; exact hτ
  have hpos := cell600_area_pos
  rw [← finrank_R4_sub] at hpos
  exact ENNReal.toReal_pos hpos.ne' hfin

/-- The class 4π/3 − arccos(1/4) is minus the class of arccos(1/4). -/
lemma angle600_class : (Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4)) : Angle) =
    -Submodule.Quotient.mk (Real.arccos (1 / 4)) := by
  rw [← Submodule.Quotient.mk_neg, Submodule.Quotient.eq]
  have : 4 * Real.pi / 3 - Real.arccos (1 / 4) - -Real.arccos (1 / 4) = (4 / 3 : ℚ) * Real.pi := by
    push_cast; ring
  rw [this, mem_ratPi_iff]
  exact ⟨4 / 3, rfl⟩

/-- **The 5-cell against the 600-cell.** No similar copy of the regular 5-cell is scissors congruent to a similar
copy of the regular 600-cell. -/
theorem similarCell5_not_scissorsCongruent_similarCell600 {T Q : Set R4} (hT : IsSimilarCopy cell5 T)
    (hQ : IsSimilarCopy cell600 Q) : ¬ ScissorsCongruent T Q := by
  intro h
  have hD := dehnHadwiger_eq_of_scissorsCongruent (isPoly_cell5.similarCopy hT) (isPoly_cell600.similarCopy hQ) h
  obtain ⟨a, ha, hTa⟩ := dehnHadwiger_similarCopy hT
  obtain ⟨b, hb, hQb⟩ := dehnHadwiger_similarCopy hQ
  rw [hTa, hQb, dehnHadwiger_cell5_eq, dehnHadwiger_cell600_eq] at hD
  set A := (μH[(finrank ℝ R4 - 2 : ℕ)]
    {x | ridgeAngle cell5 x = Submodule.Quotient.mk (Real.arccos (1 / 4))}).toReal
  set B := (μH[(finrank ℝ R4 - 2 : ℕ)]
    {x | ridgeAngle cell600 x = Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4))}).toReal with hBdef
  have hA : 0 < A := cell5_area_real_pos
  have hB : 0 < B := cell600_area_real_pos
  rw [angle600_class, TensorProduct.tmul_neg, smul_neg, TensorProduct.smul_tmul', TensorProduct.smul_tmul',
    eq_neg_iff_add_eq_zero, ← TensorProduct.add_tmul] at hD
  have hpos : 0 < a • A + b • B := by
    simp only [smul_eq_mul]; positivity
  exact edgeTerm_ne_zero hpos.ne' arccos_quarter_not_ratPi hD

end DehnHadwiger
