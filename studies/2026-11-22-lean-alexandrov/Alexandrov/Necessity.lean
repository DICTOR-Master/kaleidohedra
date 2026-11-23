/-
Alexandrov's theorem on prescribed curvature, polyhedral case: necessity of Alexandrov's condition.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Monotone
import Alexandrov.Total

/-!
# Alexandrov's condition is necessary

Let `C` be a set of directions containing a nonzero vector and lying in a closed hemisphere
(some `u ≠ 0` has `⟪v, u⟫ ≤ 0` for all `v ∈ C`). Write `C'` for the open cone of directions within an
angle `< π/2` of some direction in `C`. Then the curvature carried by the corners on rays in `C` is
strictly less than the area of `C'` (`curvature_lt_of_hemisphere`):

  `Σ_{n i ∈ C} κ i < 3 · volume (C' ∩ unit ball) = area (C' ∩ unit sphere)`.

Every nonempty spherically convex set other than the whole sphere lies in a closed hemisphere, so this
contains the necessity half of Alexandrov's condition `μ(ω) < σ(ω^{π/2})` (with the open
`π/2`-neighbourhood, which is the stronger form). Convexity is not needed.
-/

open MeasureTheory Set Metric Finset
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

/-- Cells are cones: scaling a point by a positive number keeps it in, or out of, a cell. -/
lemma smul_mem_cell_iff (n : Fin N → E3) (r : Fin N → ℝ) (k : Fin N) {c : ℝ} (hc : 0 < c)
    (x : E3) : c • x ∈ cell n r k ↔ x ∈ cell n r k := by
  simp only [cell, mem_ofPred_eq, real_inner_smul_right]
  refine forall_congr' fun j => ⟨fun h => ?_, fun h => ?_⟩ <;> nlinarith

open Classical in
/-- **Necessity of Alexandrov's condition** (for any set of directions in a closed hemisphere). -/
theorem curvature_lt_of_hemisphere {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) (C : Set E3) (hC : ∃ v ∈ C, v ≠ 0)
    (hhemi : ∃ u : E3, u ≠ 0 ∧ ∀ v ∈ C, ⟪v, u⟫ ≤ 0) :
    ∑ i ∈ univ.filter (fun i => n i ∈ C), curvature (rayPolytope n r) (corner n r i) <
      3 * volume ({x : E3 | ∃ v ∈ C, 0 < ⟪v, x⟫} ∩ ball (0 : E3) 1) := by
  set I := univ.filter (fun i => n i ∈ C) with hI
  set W : Set E3 := {x : E3 | ∃ v ∈ C, 0 < ⟪v, x⟫} with hW
  set U : Set E3 := ⋃ i ∈ I, cell n r i with hU
  have hWopen : IsOpen W := by
    have : W = ⋃ v ∈ C, {x : E3 | 0 < ⟪v, x⟫} := by ext x; simp [W]
    rw [this]
    exact isOpen_biUnion fun v _ => isOpen_lt continuous_const (continuous_const.inner continuous_id)
  have hUclosed : IsClosed U := isClosed_biUnion_finset fun i _ => isClosed_cell n r i
  -- the cells of the corners on rays in C lie in W (apart from the origin)
  have hUW : ∀ x ∈ U, x ≠ 0 → x ∈ W := by
    intro x hx h0
    obtain ⟨i, hi, hxi⟩ := mem_iUnion₂.1 hx
    exact ⟨n i, (Finset.mem_filter.1 hi).2,
      pos_of_mul_pos_right (pos_of_mem_cell hspan hr hxi h0) (hr i).le⟩
  -- some direction of W escapes these cells
  have hX : IsPreconnected ({0}ᶜ : Set E3) := by
    refine (isConnected_compl_singleton_of_one_lt_rank ?_ 0).isPreconnected
    rw [← Module.finrank_eq_rank, finrank_euclideanSpace_fin]
    exact_mod_cast (by norm_num : 1 < 3)
  obtain ⟨y, hyW, hyU⟩ : ∃ y, y ∈ W ∧ y ∉ U := by
    by_contra hne
    push Not at hne
    obtain ⟨v, hvC, hv0⟩ := hC
    obtain ⟨u, hu0, hu⟩ := hhemi
    have h1 : (({0}ᶜ : Set E3) ∩ W).Nonempty :=
      ⟨v, hv0, v, hvC, real_inner_self_pos.2 hv0⟩
    have h2 : ¬ ({0}ᶜ : Set E3) ⊆ W := fun h => by
      obtain ⟨w, hwC, hw⟩ := h hu0
      exact absurd (hu w hwC) (not_le.2 hw)
    obtain ⟨u0, hu0X, hu0W, hu0cl⟩ := exists_mem_closure_not_mem hX hWopen h1 h2
    exact hu0W (hUW u0 (closure_minimal (fun x hx => hne x hx) hUclosed hu0cl) hu0X)
  have hy0 : y ≠ 0 := by
    rintro rfl
    obtain ⟨v, -, hv⟩ := hyW
    simp at hv
  -- an open piece of W in the unit ball outside the cells
  set c : ℝ := (‖y‖ + 1)⁻¹ with hc
  have hc0 : 0 < c := by positivity
  set V : Set E3 := W ∩ ball (0 : E3) 1 ∩ Uᶜ with hV
  have hVopen : IsOpen V := (hWopen.inter isOpen_ball).inter hUclosed.isOpen_compl
  have hcy : c • y ∈ V := by
    refine ⟨⟨?_, ?_⟩, ?_⟩
    · obtain ⟨v, hvC, hv⟩ := hyW
      exact ⟨v, hvC, by rw [real_inner_smul_right]; exact mul_pos hc0 hv⟩
    · rw [mem_ball_zero_iff, norm_smul, Real.norm_of_nonneg hc0.le, hc,
        inv_mul_lt_iff₀ (by positivity)]
      linarith
    · intro hcU
      obtain ⟨i, hi, hxi⟩ := mem_iUnion₂.1 hcU
      exact hyU (mem_iUnion₂.2 ⟨i, hi, (smul_mem_cell_iff n r i hc0 y).1 hxi⟩)
  have hVpos : 0 < volume V := hVopen.measure_pos volume ⟨_, hcy⟩
  -- the sum is the volume of the union of the cells
  have hsum : ∑ i ∈ I, volume (cell n r i ∩ ball (0 : E3) 1) = volume (U ∩ ball (0 : E3) 1) := by
    rw [hU, iUnion₂_inter]
    refine (measure_biUnion_finset₀ ?_ fun i _ => ((isClosed_cell n r i).measurableSet.inter
      measurableSet_ball).nullMeasurableSet).symm
    intro i _ j _ hij
    exact measure_mono_null (inter_subset_inter Set.inter_subset_left Set.inter_subset_left)
      (volume_cell_inter hn hinj hr hij)
  have hfin : volume (U ∩ ball (0 : E3) 1) ≠ ∞ :=
    (measure_mono Set.inter_subset_right |>.trans_lt measure_ball_lt_top).ne
  have hdisj : Disjoint (U ∩ ball (0 : E3) 1) V :=
    Set.disjoint_left.2 fun x hx hxV => hxV.2 hx.1
  have hsub : (U ∩ ball (0 : E3) 1) ∪ V ⊆ (W ∩ ball (0 : E3) 1) ∪ {0} := by
    rintro x (⟨hxU, hxB⟩ | ⟨hxWB, -⟩)
    · by_cases h0 : x = 0
      · exact Or.inr h0
      · exact Or.inl ⟨hUW x hxU h0, hxB⟩
    · exact Or.inl hxWB
  simp only [curvature_rayPolytope]
  rw [← Finset.mul_sum, hsum]
  refine (ENNReal.mul_lt_mul_iff_right (by norm_num) (by norm_num)).2 ?_
  calc volume (U ∩ ball (0 : E3) 1)
      < volume (U ∩ ball (0 : E3) 1) + volume V := ENNReal.lt_add_right hfin hVpos.ne'
    _ = volume ((U ∩ ball (0 : E3) 1) ∪ V) := (measure_union hdisj hVopen.measurableSet).symm
    _ ≤ volume ((W ∩ ball (0 : E3) 1) ∪ {0}) := measure_mono hsub
    _ ≤ volume (W ∩ ball (0 : E3) 1) + volume ({0} : Set E3) := measure_union_le _ _
    _ = volume (W ∩ ball (0 : E3) 1) := by rw [measure_singleton, add_zero]

end Alexandrov
