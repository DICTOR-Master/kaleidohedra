/-
Alexandrov's theorem on prescribed curvature, polyhedral case: the whole theorem.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Existence
import Alexandrov.Uniqueness
import Alexandrov.Hemisphere

/-!
# Alexandrov's theorem, polyhedral case (M10)

Let `n 0, …, n (N-1)` be distinct unit vectors not all in one closed hemisphere, and `κ j > 0`.

**Theorem** (`alexandrov_iff`). There is a polytope with corners `r i • n i` (`r i > 0`) whose
curvature at corner `j` is `κ j` for every `j` **if and only if** `Σ κ j = 4π` and Alexandrov's
condition holds: `Σ_{i ∈ I} κ i < area (nbhd n 0 I)` for every nonempty proper set `I` of rays.

**Theorem** (`alexandrov_unique`). Such a polytope is unique up to scaling about the origin.
-/

open MeasureTheory Set Metric Finset
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

/-- Alexandrov's condition for prescribed curvatures `κ` at the corners on the rays `n`. -/
def AlexandrovCondition (n : Fin N → E3) (κ : Fin N → ℝ) : Prop :=
  ∀ I : Finset (Fin N), I.Nonempty → I ≠ Finset.univ →
    ∑ i ∈ I, κ i < 3 * (volume (nbhd n 0 I ∩ ball (0 : E3) 1)).toReal

/-- Necessity: the curvatures of any such polytope add up to `4π` and satisfy Alexandrov's
condition. -/
theorem alexandrov_necessary {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {κ : Fin N → ℝ} (hκ : ∀ j, 0 < κ j) {r : Fin N → ℝ} (hr : ∀ i, 0 < r i)
    (hcurv : ∀ j, curvature (rayPolytope n r) (corner n r j) = ENNReal.ofReal (κ j)) :
    ∑ j, κ j = 4 * Real.pi ∧ AlexandrovCondition n κ := by
  classical
  refine ⟨?_, fun I hIne hIu => ?_⟩
  · have h := sum_curvature hn hinj hspan hr
    simp only [hcurv] at h
    rw [← ENNReal.ofReal_sum_of_nonneg fun j _ => (hκ j).le] at h
    exact (ENNReal.ofReal_eq_ofReal_iff (Finset.sum_nonneg fun j _ => (hκ j).le)
      (by positivity)).1 h
  by_cases hhemi : ∃ u : E3, u ≠ 0 ∧ ∀ i ∈ I, ⟪n i, u⟫ ≤ 0
  · set C : Set E3 := n '' (I : Set (Fin N)) with hC
    obtain ⟨i0, hi0⟩ := hIne
    have hn0 : n i0 ≠ 0 := fun h => by have := hn i0; rw [h, norm_zero] at this; norm_num at this
    obtain ⟨u, hu0, hu⟩ := hhemi
    have key := curvature_lt_of_hemisphere hn hinj hspan hr C ⟨n i0, ⟨i0, hi0, rfl⟩, hn0⟩
      ⟨u, hu0, by rintro _ ⟨i, hi, rfl⟩; exact hu i hi⟩
    have hfilter : (Finset.univ.filter fun i => n i ∈ C) = I := by
      ext i; simp [hC, hinj.mem_set_image]
    have hset : {x : E3 | ∃ v ∈ C, 0 < ⟪v, x⟫} = nbhd n 0 I := by
      ext x; simp [hC, nbhd]
    rw [hfilter, hset] at key
    simp only [hcurv] at key
    rw [← ENNReal.ofReal_sum_of_nonneg fun j _ => (hκ j).le,
      ENNReal.ofReal_lt_iff_lt_toReal (Finset.sum_nonneg fun j _ => (hκ j).le)
        (ENNReal.mul_ne_top (by norm_num)
          (measure_mono Set.inter_subset_right |>.trans_lt measure_ball_lt_top).ne),
      ENNReal.toReal_mul] at key
    simpa using key
  · push Not at hhemi
    have hall : volume (nbhd n 0 I ∩ ball (0 : E3) 1) = volume (ball (0 : E3) 1) := by
      refine le_antisymm (measure_mono Set.inter_subset_right) ?_
      calc volume (ball (0 : E3) 1) ≤ volume ((nbhd n 0 I ∩ ball (0 : E3) 1) ∪ {0}) := by
            refine measure_mono fun x hx => ?_
            by_cases hx0 : x = 0
            · exact Or.inr hx0
            · obtain ⟨i, hi, hpos⟩ := hhemi x hx0
              exact Or.inl ⟨⟨i, hi, by simpa using hpos⟩, hx⟩
        _ ≤ volume (nbhd n 0 I ∩ ball (0 : E3) 1) + volume ({0} : Set E3) := measure_union_le _ _
        _ = volume (nbhd n 0 I ∩ ball (0 : E3) 1) := by rw [measure_singleton, add_zero]
    have hB : 3 * (volume (ball (0 : E3) 1)).toReal = 4 * Real.pi := by
      rw [EuclideanSpace.volume_ball_fin_three, ENNReal.ofReal_one, one_pow, one_mul,
        ENNReal.toReal_ofReal (by positivity)]
      ring
    obtain ⟨j, hj⟩ : ∃ j, j ∉ I := by
      by_contra h
      push Not at h
      exact hIu (Finset.eq_univ_of_forall h)
    have hlt : ∑ i ∈ I, κ i < ∑ i, κ i :=
      Finset.sum_lt_sum_of_subset (Finset.subset_univ I) (Finset.mem_univ j) hj (hκ j)
        fun i _ _ => (hκ i).le
    have hsum := sum_curvature hn hinj hspan hr
    simp only [hcurv] at hsum
    rw [← ENNReal.ofReal_sum_of_nonneg fun j _ => (hκ j).le,
      ENNReal.ofReal_eq_ofReal_iff (Finset.sum_nonneg fun j _ => (hκ j).le)
        (by positivity)] at hsum
    rw [hall, hB]
    linarith

/-- **Alexandrov's theorem, polyhedral case: existence.** -/
theorem alexandrov_iff [NeZero N] {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {κ : Fin N → ℝ} (hκ : ∀ j, 0 < κ j) :
    (∃ r : Fin N → ℝ, (∀ i, 0 < r i) ∧
      ∀ j, curvature (rayPolytope n r) (corner n r j) = ENNReal.ofReal (κ j)) ↔
    (∑ j, κ j = 4 * Real.pi ∧ AlexandrovCondition n κ) := by
  constructor
  · rintro ⟨r, hr, hcurv⟩
    exact alexandrov_necessary hn hinj hspan hκ hr hcurv
  · rintro ⟨hsum, hA⟩
    exact alexandrov_existence hn hinj hspan (fun j => (hκ j).le) hsum hA

/-- **Alexandrov's theorem, polyhedral case: uniqueness up to scaling.** -/
theorem alexandrov_unique {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {κ : Fin N → ℝ} (hκ : ∀ j, 0 < κ j) {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i)
    (hr' : ∀ i, 0 < r' i)
    (hc : ∀ j, curvature (rayPolytope n r) (corner n r j) = ENNReal.ofReal (κ j))
    (hc' : ∀ j, curvature (rayPolytope n r') (corner n r' j) = ENNReal.ofReal (κ j)) :
    ∃ c : ℝ, 0 < c ∧ r' = c • r :=
  alexandrov_uniqueness hn hinj hspan hr hr'
    (fun j => by rw [hc j]; exact (ENNReal.ofReal_pos.2 (hκ j)).ne')
    (fun j => by rw [hc j, hc' j])

end Alexandrov
