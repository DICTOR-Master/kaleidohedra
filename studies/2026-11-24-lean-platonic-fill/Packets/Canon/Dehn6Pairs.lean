/-
Lean study 6 of the shape-language canon (DICTO, 19 Nov 2026), part T: no two of the three words AXE, CLEO,
FUJI are scissors congruent to each other, in any sizes. No hypothesis.

* `wordAnglesIndep`: the hypothesis `WordAnglesIndep` of study 5 (part R) is a theorem.
* `Unconditional.cleo_axe_not_proportional`, `Unconditional.cleo_fuji_not_proportional`,
  `Unconditional.axe_fuji_not_proportional`: no real multiple of the Dehn invariant of one word is the
  invariant of another.
* `Unconditional.cleo_axe_not_scissorsCongruent`, `Unconditional.cleo_fuji_not_scissorsCongruent`,
  `Unconditional.axe_fuji_not_scissorsCongruent`: no similar copy of one word is scissors congruent to a
  similar copy of another.

The six statements are the conditional theorems of study 5 (same names, there with the hypothesis as an
argument) applied to `wordAnglesIndep`; they are placed in the namespace `Unconditional` so that study 5 stays
unchanged.

Credits: Mathlib `Submodule.mem_span_singleton`, `Submodule.Quotient.eq`, `Submodule.smul_mem`,
`Rat.mul_den_eq_num`; study 5 of this canon for the conditional theorems; part S (`word_angles_int_indep`).
No `sorry`.
-/
module

public import Packets.Canon.Dehn5Pairs
public import Packets.Canon.Dehn6Indep

@[expose] public section

open scoped RealInnerProductSpace Real
open Set Module TensorProduct

namespace DehnCanon.Library

/-- **The hypothesis of study 5 holds**: modulo π, α is not a rational multiple of β and β is not a rational
multiple of α. -/
theorem wordAnglesIndep : WordAnglesIndep := by
  constructor
  · intro h
    obtain ⟨r, hr⟩ := Submodule.mem_span_singleton.1 h
    rw [← Submodule.Quotient.mk_smul, Submodule.Quotient.eq] at hr
    have hrr : (r : ℝ) * r.den = r.num := by exact_mod_cast Rat.mul_den_eq_num r
    have h2 := ratPi.smul_mem (r.den : ℚ) hr
    have e : ((-(r.den : ℤ) : ℤ) : ℝ) * wordAlpha + (r.num : ℝ) * wordBeta =
        (r.den : ℚ) • (r • wordBeta - wordAlpha) := by
      rw [Rat.smul_def, Rat.smul_def]; push_cast
      linear_combination (-wordBeta) * hrr
    rw [← e] at h2
    have h3 := (word_angles_int_indep _ _ h2).1
    have := r.den_pos
    omega
  · intro h
    obtain ⟨r, hr⟩ := Submodule.mem_span_singleton.1 h
    rw [← Submodule.Quotient.mk_smul, Submodule.Quotient.eq] at hr
    have hrr : (r : ℝ) * r.den = r.num := by exact_mod_cast Rat.mul_den_eq_num r
    have h2 := ratPi.smul_mem (r.den : ℚ) hr
    have e : (r.num : ℝ) * wordAlpha + ((-(r.den : ℤ) : ℤ) : ℝ) * wordBeta =
        (r.den : ℚ) • (r • wordAlpha - wordBeta) := by
      rw [Rat.smul_def, Rat.smul_def]; push_cast
      linear_combination (-wordAlpha) * hrr
    rw [← e] at h2
    have h3 := (word_angles_int_indep _ _ h2).2
    have := r.den_pos
    omega

namespace Unconditional

/-- No real multiple of the Dehn invariant of CLEO is the Dehn invariant of AXE. -/
theorem cleo_axe_not_proportional (t : ℝ) : t • dehnSet cleoSet ≠ dehnSet axeSet :=
  DehnCanon.Library.cleo_axe_not_proportional wordAnglesIndep t

/-- No real multiple of the Dehn invariant of CLEO is the Dehn invariant of FUJI. -/
theorem cleo_fuji_not_proportional (t : ℝ) : t • dehnSet cleoSet ≠ dehnSet fujiSet :=
  DehnCanon.Library.cleo_fuji_not_proportional wordAnglesIndep t

/-- No real multiple of the Dehn invariant of AXE is the Dehn invariant of FUJI. -/
theorem axe_fuji_not_proportional (t : ℝ) : t • dehnSet axeSet ≠ dehnSet fujiSet :=
  DehnCanon.Library.axe_fuji_not_proportional wordAnglesIndep t

/-- **No CLEO is scissors congruent to an AXE** (any sizes, any positions). -/
theorem cleo_axe_not_scissorsCongruent {C A : Set R3}
    (hC : IsSimilarCopy cleoSet C) (hA : IsSimilarCopy axeSet A) : ¬ ScissorsCongruent C A :=
  DehnCanon.Library.cleo_axe_not_scissorsCongruent wordAnglesIndep hC hA

/-- **No CLEO is scissors congruent to a FUJI** (any sizes, any positions). -/
theorem cleo_fuji_not_scissorsCongruent {C F : Set R3}
    (hC : IsSimilarCopy cleoSet C) (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent C F :=
  DehnCanon.Library.cleo_fuji_not_scissorsCongruent wordAnglesIndep hC hF

/-- **No AXE is scissors congruent to a FUJI** (any sizes, any positions). -/
theorem axe_fuji_not_scissorsCongruent {A F : Set R3}
    (hA : IsSimilarCopy axeSet A) (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent A F :=
  DehnCanon.Library.axe_fuji_not_scissorsCongruent wordAnglesIndep hA hF

end Unconditional

end DehnCanon.Library
