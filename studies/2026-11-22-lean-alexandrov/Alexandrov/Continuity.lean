/-
Alexandrov's theorem on prescribed curvature, polyhedral case: continuity of curvature.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Comparison

/-!
# Curvature depends continuously on the corners

At any `r₀` with all `r₀ i > 0`, the volume of each cell inside the unit ball, and so the curvature at
each corner, is continuous in `r` (`continuousAt_volume_cell`, `continuousAt_curvature`).
Proof: dominated convergence. Off the planes where two corners tie for `r₀`
(a set of volume zero), whether a point lies in the cell is decided by strict inequalities, which
persist for `r` near `r₀`.
-/

open MeasureTheory Set Metric Filter Topology
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

/-- Away from ties, membership in the cell is locally constant in `r`. -/
lemma eventually_mem_cell_iff (n : Fin N → E3) (r₀ : Fin N → ℝ) (k : Fin N) {x : E3}
    (hx : ∀ j, j ≠ k → r₀ j * ⟪n j, x⟫ ≠ r₀ k * ⟪n k, x⟫) :
    ∀ᶠ r in 𝓝 r₀, (x ∈ cell n r k ∩ ball (0 : E3) 1 ↔ x ∈ cell n r₀ k ∩ ball (0 : E3) 1) := by
  have hc : ∀ j, Tendsto (fun r : Fin N → ℝ => r j * ⟪n j, x⟫) (𝓝 r₀)
      (𝓝 (r₀ j * ⟪n j, x⟫)) := fun j =>
    ((continuous_apply j).mul continuous_const).tendsto r₀
  by_cases hin : x ∈ cell n r₀ k ∩ ball (0 : E3) 1
  · have hstrict : ∀ j, ∀ᶠ r in 𝓝 r₀, r j * ⟪n j, x⟫ ≤ r k * ⟪n k, x⟫ := by
      intro j
      by_cases hjk : j = k
      · subst hjk; exact Eventually.of_forall fun r => le_rfl
      · exact ((hc j).eventually_lt (hc k)
          (lt_of_le_of_ne (hin.1 j) (hx j hjk))).mono fun r hr => hr.le
    filter_upwards [eventually_all.2 hstrict] with r hr
    exact iff_of_true ⟨hr, hin.2⟩ hin
  · rw [mem_inter_iff, not_and_or] at hin
    rcases hin with hcell | hball
    · simp only [cell, mem_ofPred_eq, not_forall, not_le] at hcell
      obtain ⟨j, hj⟩ := hcell
      filter_upwards [(hc k).eventually_lt (hc j) hj] with r hr
      refine iff_of_false (fun h => absurd (h.1 j) (not_le.2 hr)) ?_
      rintro ⟨h, -⟩
      exact absurd (h j) (not_le.2 hj)
    · exact Eventually.of_forall fun r =>
        iff_of_false (fun h => hball h.2) (fun h => hball h.2)

/-- **Continuity.** The volume of a cell inside the unit ball is continuous in `r` at every `r₀`
with positive entries. -/
theorem continuousAt_volume_cell {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) {r₀ : Fin N → ℝ} (hr₀ : ∀ i, 0 < r₀ i) (k : Fin N) :
    ContinuousAt (fun r => volume (cell n r k ∩ ball (0 : E3) 1)) r₀ := by
  have hmeas : ∀ r, MeasurableSet (cell n r k ∩ ball (0 : E3) 1) := fun r =>
    (isClosed_cell n r k).measurableSet.inter measurableSet_ball
  simp only [ContinuousAt, ← lintegral_indicator_one (hmeas _)]
  refine tendsto_lintegral_filter_of_dominated_convergence ((ball (0 : E3) 1).indicator 1)
    (Eventually.of_forall fun r => measurable_one.indicator (hmeas r))
    (Eventually.of_forall fun r => Eventually.of_forall fun x =>
      indicator_le_indicator_of_subset Set.inter_subset_right (fun _ => by simp) x) ?_ ?_
  · rw [lintegral_indicator_one measurableSet_ball]
    exact measure_ball_lt_top.ne
  · -- the exceptional set: ties for r₀
    set Z : Set E3 := (⋃ j ∈ ({k}ᶜ : Set (Fin N)),
      {x : E3 | ⟪corner n r₀ j - corner n r₀ k, x⟫ = 0}) with hZ
    have hZ0 : volume Z = 0 := by
      refine (measure_biUnion_null_iff (Set.to_countable _)).2 fun j hj => volume_plane ?_
      intro h0
      exact hj (corner_injective hn hinj hr₀ (sub_eq_zero.1 h0))
    filter_upwards [measure_eq_zero_iff_ae_notMem.1 hZ0] with x hx
    have htie : ∀ j, j ≠ k → r₀ j * ⟪n j, x⟫ ≠ r₀ k * ⟪n k, x⟫ := by
      intro j hj h
      apply hx
      refine mem_iUnion₂.2 ⟨j, hj, ?_⟩
      simp only [mem_ofPred_eq, inner_sub_left, inner_corner, h, sub_self]
    refine tendsto_const_nhds.congr' ?_
    filter_upwards [eventually_mem_cell_iff n r₀ k htie] with r hr
    by_cases h : x ∈ cell n r₀ k ∩ ball (0 : E3) 1
    · simp only [Set.indicator_of_mem h, Set.indicator_of_mem (hr.2 h)]
    · simp only [Set.indicator_of_notMem h, Set.indicator_of_notMem (mt hr.1 h)]

/-- The curvature at each corner is continuous in `r` at every `r₀` with positive entries. -/
theorem continuousAt_curvature {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) {r₀ : Fin N → ℝ} (hr₀ : ∀ i, 0 < r₀ i) (k : Fin N) :
    ContinuousAt (fun r => curvature (rayPolytope n r) (corner n r k)) r₀ := by
  simp only [curvature_rayPolytope]
  exact ENNReal.Tendsto.const_mul (continuousAt_volume_cell hn hinj hr₀ k) (Or.inr (by norm_num))

end Alexandrov
