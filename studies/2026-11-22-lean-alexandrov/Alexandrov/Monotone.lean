/-
Alexandrov's theorem on prescribed curvature, polyhedral case: moving one corner outward.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Comparison

/-!
# Moving one corner outward

If only corner `k` moves outward along its ray (`r k ≤ r' k`, all other `r' j = r j`), its cell can
only grow and every other cell can only shrink (`cell_subset_cell_of_raise`,
`cell_subset_cell_of_raise_other`); so its curvature does not decrease and every other curvature does not
increase (`curvature_le_of_raise`, `curvature_le_of_raise_other`).
-/

open MeasureTheory Set Metric
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

/-- In the cell of corner `j`, corner `j` reaches beyond the origin. -/
lemma pos_of_mem_cell {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) {j : Fin N} {x : E3} (hx : x ∈ cell n r j) (h0 : x ≠ 0) :
    0 < r j * ⟪n j, x⟫ := by
  obtain ⟨m, hm⟩ := hspan x h0
  exact lt_of_lt_of_le (mul_pos (hr m) hm) (hx m)

theorem cell_subset_cell_of_raise {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) {k : Fin N} (hk : r k ≤ r' k)
    (hother : ∀ j, j ≠ k → r' j = r j) : cell n r k ⊆ cell n r' k := by
  intro x hx j
  by_cases h0 : x = 0
  · simp [h0]
  have hp := pos_of_mem_cell hspan hr hx h0
  have hnk : 0 < ⟪n k, x⟫ := pos_of_mul_pos_right hp (hr k).le
  have hkk : r k * ⟪n k, x⟫ ≤ r' k * ⟪n k, x⟫ := mul_le_mul_of_nonneg_right hk hnk.le
  by_cases hjk : j = k
  · subst hjk; exact le_rfl
  · rw [hother j hjk]; exact (hx j).trans hkk

theorem cell_subset_cell_of_raise_other {n : Fin N → E3}
    (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) {k : Fin N} (hk : r k ≤ r' k)
    (hother : ∀ j, j ≠ k → r' j = r j) {j : Fin N} (hjk : j ≠ k) : cell n r' j ⊆ cell n r j := by
  have hr' : ∀ i, 0 < r' i := fun i => by
    by_cases h : i = k
    · subst h; exact (hr i).trans_le hk
    · rw [hother i h]; exact hr i
  intro x hx i
  by_cases h0 : x = 0
  · simp [h0]
  have hp := pos_of_mem_cell hspan hr' hx h0
  have hxi := hx i
  have hxk := hx k
  rw [hother j hjk] at hp hxi hxk
  by_cases hik : i = k
  · subst hik
    rcases le_or_gt 0 ⟪n i, x⟫ with ht | ht
    · exact (mul_le_mul_of_nonneg_right hk ht).trans hxk
    · exact (mul_neg_of_pos_of_neg (hr i) ht).le.trans hp.le
  · rwa [hother i hik] at hxi

theorem curvature_le_of_raise {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) {k : Fin N} (hk : r k ≤ r' k)
    (hother : ∀ j, j ≠ k → r' j = r j) :
    curvature (rayPolytope n r) (corner n r k) ≤ curvature (rayPolytope n r') (corner n r' k) := by
  simp only [curvature_rayPolytope]
  gcongr
  exact cell_subset_cell_of_raise hspan hr hk hother

theorem curvature_le_of_raise_other {n : Fin N → E3}
    (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) {k : Fin N} (hk : r k ≤ r' k)
    (hother : ∀ j, j ≠ k → r' j = r j) {j : Fin N} (hjk : j ≠ k) :
    curvature (rayPolytope n r') (corner n r' j) ≤ curvature (rayPolytope n r) (corner n r j) := by
  simp only [curvature_rayPolytope]
  gcongr
  exact cell_subset_cell_of_raise_other hspan hr hk hother hjk

end Alexandrov
