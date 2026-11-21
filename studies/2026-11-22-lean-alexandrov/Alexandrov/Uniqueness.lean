/-
Alexandrov's theorem on prescribed curvature, polyhedral case: uniqueness.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Comparison

/-!
# Uniqueness up to scale

**Theorem** (`alexandrov_uniqueness`). Let `n 0, …, n (N-1)` be distinct unit vectors in `E3`, not all
in one closed hemisphere. If two polytopes with corners `r i • n i` and `r' i • n i` (all `r i, r' i > 0`)
have the same curvature at every corner, and these curvatures are positive, then `r' = c • r` for some
`c > 0`: the polytopes are homothetic about the origin.

This is the uniqueness half of Alexandrov's theorem in the form used by #112 (Aequi), Theorem A (a):
the polar of a fair die has curvature `4π/N` at every corner.
-/

open MeasureTheory Set Metric Finset
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

/-- Uniqueness, stated with cell volumes. -/
theorem cell_volume_uniqueness {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hr' : ∀ i, 0 < r' i)
    (hpos : ∀ i, volume (cell n r i ∩ ball (0 : E3) 1) ≠ 0)
    (heq : ∀ i, volume (cell n r' i ∩ ball (0 : E3) 1) = volume (cell n r i ∩ ball (0 : E3) 1)) :
    ∃ c : ℝ, 0 < c ∧ r' = c • r := by
  classical
  obtain ⟨x, hx⟩ := exists_ne (0 : E3)
  obtain ⟨i0, -⟩ := hspan x hx
  have hU : (univ : Finset (Fin N)).Nonempty := ⟨i0, mem_univ _⟩
  set L : ℝ := univ.sup' hU (fun i => r' i / r i) with hL
  have hLpos : 0 < L :=
    lt_of_lt_of_le (div_pos (hr' i0) (hr i0)) (Finset.le_sup' (fun i => r' i / r i) (mem_univ i0))
  have hLge : ∀ i, r' i ≤ L * r i := fun i =>
    (div_le_iff₀ (hr i)).1 (Finset.le_sup' (fun i => r' i / r i) (mem_univ i))
  set ρ : Fin N → ℝ := L⁻¹ • r' with hρdef
  have hρ : ∀ i, ρ i = L⁻¹ * r' i := fun i => rfl
  have hρ0 : ∀ i, 0 ≤ ρ i := fun i => by rw [hρ]; exact mul_nonneg (inv_pos.2 hLpos).le (hr' i).le
  have hle : ∀ i, ρ i ≤ r i := fun i => by
    rw [hρ, inv_mul_le_iff₀ hLpos]; exact hLge i
  have hcell : ∀ k, cell n ρ k = cell n r' k := fun k => cell_smul n r' (inv_pos.2 hLpos) k
  have hI : ∃ k, ρ k = r k := by
    obtain ⟨k, -, hk⟩ := Finset.exists_mem_eq_sup' hU (fun i => r' i / r i)
    refine ⟨k, ?_⟩
    have : r' k = L * r k := by rw [hL, hk]; field_simp [(hr k).ne']
    rw [hρ, this, ← mul_assoc, inv_mul_cancel₀ hLpos.ne', one_mul]
  by_cases hJ : ∃ j, ρ j < r j
  · exfalso
    obtain ⟨k, -, hk⟩ := exists_cell_volume_lt hn hinj hspan hr hρ0 hle hI hJ hpos
    rw [hcell, heq] at hk
    exact lt_irrefl _ hk
  · push Not at hJ
    refine ⟨L, hLpos, funext fun i => ?_⟩
    have h := le_antisymm (hle i) (hJ i)
    rw [hρ] at h
    rw [Pi.smul_apply, smul_eq_mul, ← h, ← mul_assoc, mul_inv_cancel₀ hLpos.ne', one_mul]

/-- **Alexandrov's uniqueness theorem, polyhedral case.** Two polytopes with corners on the same
rays (distinct unit vectors not all in one closed hemisphere) and the same positive curvature at
every corner are homothetic about the origin. -/
theorem alexandrov_uniqueness {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hr' : ∀ i, 0 < r' i)
    (hpos : ∀ i, curvature (rayPolytope n r) (corner n r i) ≠ 0)
    (heq : ∀ i, curvature (rayPolytope n r') (corner n r' i) =
      curvature (rayPolytope n r) (corner n r i)) :
    ∃ c : ℝ, 0 < c ∧ r' = c • r := by
  simp only [curvature_rayPolytope] at hpos heq
  refine cell_volume_uniqueness hn hinj hspan hr hr' (fun i => right_ne_zero_of_mul (hpos i))
    fun i => ?_
  exact (ENNReal.mul_right_inj (by norm_num) (by norm_num)).1 (heq i)

end Alexandrov
