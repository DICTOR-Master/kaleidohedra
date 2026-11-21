/-
Alexandrov's theorem on prescribed curvature, polyhedral case: total curvature.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Comparison

/-!
# Total curvature is 4π

The first step toward existence: for any polytope with corners on the rays (distinct unit vectors,
not all in one closed hemisphere, positive `r i`), the curvatures at the corners add up to `4π`
(`sum_curvature`). So `Σ κ i = 4π` is necessary for a prescribed curvature `κ`; for the fair dice,
`κ i = 4π / N`.
-/

open MeasureTheory Set Metric Finset
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

/-- Every direction has a farthest corner: the cells cover space. -/
lemma iUnion_cell (n : Fin N → E3) (r : Fin N → ℝ) (hN : (univ : Finset (Fin N)).Nonempty) :
    (⋃ i, cell n r i) = univ := by
  refine eq_univ_of_forall fun x => ?_
  obtain ⟨k, -, hk⟩ := Finset.exists_mem_eq_sup' hN (fun i => r i * ⟪n i, x⟫)
  refine mem_iUnion.2 ⟨k, fun j => ?_⟩
  rw [← hk]
  exact Finset.le_sup' (fun i => r i * ⟪n i, x⟫) (mem_univ j)

/-- Two different cells meet in a set of volume zero. -/
lemma volume_cell_inter {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1) (hinj : Function.Injective n)
    {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) {i j : Fin N} (hij : i ≠ j) :
    volume (cell n r i ∩ cell n r j) = 0 := by
  refine measure_mono_null (t := {x : E3 | ⟪corner n r i - corner n r j, x⟫ = 0}) ?_
    (volume_plane fun h0 => hij (corner_injective hn hinj hr (sub_eq_zero.1 h0)))
  rintro x ⟨hi, hj⟩
  have a := hi j
  have b := hj i
  simp only [mem_ofPred_eq, inner_sub_left, inner_corner]
  linarith

/-- **Total curvature.** The curvatures at the corners add up to `4π`. -/
theorem sum_curvature {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1) (hinj : Function.Injective n)
    (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫) {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) :
    ∑ i, curvature (rayPolytope n r) (corner n r i) = ENNReal.ofReal (4 * Real.pi) := by
  obtain ⟨x, hx⟩ := exists_ne (0 : E3)
  obtain ⟨i0, -⟩ := hspan x hx
  have hN : (univ : Finset (Fin N)).Nonempty := ⟨i0, mem_univ _⟩
  simp only [curvature_rayPolytope]
  rw [← Finset.mul_sum]
  have hU : volume (⋃ i, cell n r i ∩ ball (0 : E3) 1) = ∑ i, volume (cell n r i ∩ ball (0 : E3) 1) := by
    rw [measure_iUnion₀ _ fun i => ((isClosed_cell n r i).measurableSet.inter
      measurableSet_ball).nullMeasurableSet, tsum_fintype]
    intro i j hij
    exact measure_mono_null (inter_subset_inter Set.inter_subset_left Set.inter_subset_left)
      (volume_cell_inter hn hinj hr hij)
  rw [← hU, ← iUnion_inter, iUnion_cell n r hN, univ_inter, EuclideanSpace.volume_ball_fin_three]
  rw [ENNReal.ofReal_one, one_pow, one_mul,
    show (3 : ℝ≥0∞) = ENNReal.ofReal 3 by norm_num, ← ENNReal.ofReal_mul (by norm_num)]
  congr 1
  ring

end Alexandrov
