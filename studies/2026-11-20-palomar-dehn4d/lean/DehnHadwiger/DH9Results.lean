/-
Dehn–Hadwiger study, part 9: the four-dimensional non-congruence results (DICTO, 20 Nov 2026).

* `similarCell5_not_scissorsCongruent`: no similar copy of the regular 5-cell is scissors congruent to a similar
  copy of the tesseract, the 16-cell, the 24-cell or the 120-cell (their invariant is zero, the 5-cell's is not).
  The 4-dimensional analogue of Dehn's tetrahedron-versus-cube theorem; in this form it is classical (any
  dimension: the regular simplex is not scissors congruent to the cube).
No `sorry`.
-/
import DehnHadwiger.DH8Cell120

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

/-- **The 5-cell against the four regular 4-polytopes with invariant zero**, any size and any position. -/
theorem similarCell5_not_scissorsCongruent {T Q : Set R4} (hT : IsSimilarCopy cell5 T)
    (hQ : IsSimilarCopy tesseract Q ∨ IsSimilarCopy cell16 Q ∨ IsSimilarCopy cell24 Q ∨
      IsSimilarCopy cell120 Q) : ¬ ScissorsCongruent T Q := by
  rcases hQ with h | h | h | h
  · exact not_scissorsCongruent_similarCopies isPoly_cell5 isPoly_tesseract dehnHadwiger_cell5_ne_zero
      dehnHadwiger_tesseract hT h
  · exact not_scissorsCongruent_similarCopies isPoly_cell5 isPoly_cell16 dehnHadwiger_cell5_ne_zero
      dehnHadwiger_cell16 hT h
  · exact not_scissorsCongruent_similarCopies isPoly_cell5 isPoly_cell24 dehnHadwiger_cell5_ne_zero
      dehnHadwiger_cell24 hT h
  · exact not_scissorsCongruent_similarCopies isPoly_cell5 isPoly_cell120 dehnHadwiger_cell5_ne_zero
      dehnHadwiger_cell120 hT h

end DehnHadwiger
