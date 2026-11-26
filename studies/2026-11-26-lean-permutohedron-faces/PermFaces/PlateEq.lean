/-
When do two plates of the form {Σ y = 0, Σ w y = 0} coincide? Layer 1 of #120 Theorem 3 (ii).
DICTO, with Claude (Anthropic).
-/
import Mathlib

/-!
# Layer 1 (M8a): plates in `V₀` and affine relations of their weight vectors

For a weight vector `w : Fin n → ℝ` let `plateOf w = {y | ∑ yᵢ = 0 ∧ ∑ wᵢ yᵢ = 0}`.
* `affine_of_plateOf_le`: if `plateOf u ≤ plateOf v` then `v = λ u + μ` for some reals `λ, μ` (entrywise).
* `plateOf_le_of_affine`: conversely `v = λ u + μ` gives `plateOf u ≤ plateOf v`.
The block patterns of the permutohedron (layer 2) then decide which ridges share a plate.
-/

namespace VacuusResonus

open Finset

variable {n : ℕ}

/-- The functional `y ↦ ∑ wᵢ yᵢ`. -/
def dotL (w : Fin n → ℝ) : (Fin n → ℝ) →ₗ[ℝ] ℝ where
  toFun y := ∑ i, w i * y i
  map_add' x y := by simp [mul_add, sum_add_distrib]
  map_smul' t y := by simp [mul_sum, mul_left_comm]

/-- The plate `{y | ∑ yᵢ = 0 ∧ ∑ wᵢ yᵢ = 0}`. -/
def plateOf (w : Fin n → ℝ) : Submodule ℝ (Fin n → ℝ) :=
  LinearMap.ker (dotL (fun _ => 1)) ⊓ LinearMap.ker (dotL w)

lemma dotL_single (w : Fin n → ℝ) (i : Fin n) : dotL w (Pi.single i 1) = w i := by
  simp [dotL, Pi.single_apply]

theorem affine_of_plateOf_le {u v : Fin n → ℝ} (h : plateOf u ≤ plateOf v) :
    ∃ l m : ℝ, ∀ i, v i = l * u i + m := by
  have hk : (⨅ j : Fin 2, LinearMap.ker (![dotL (fun _ => 1), dotL u] j)) ≤ LinearMap.ker (dotL v) := by
    intro y hy
    have hy' : y ∈ plateOf u := by
      simp only [Submodule.mem_iInf] at hy
      exact ⟨hy 0, hy 1⟩
    exact (h hy').2
  obtain ⟨c, hc⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).1 (mem_span_of_iInf_ker_le_ker hk)
  refine ⟨c 1, c 0, fun i => ?_⟩
  have := congrArg (fun f : (Fin n → ℝ) →ₗ[ℝ] ℝ => f (Pi.single i 1)) hc
  simp only [Fin.sum_univ_two, LinearMap.add_apply, LinearMap.smul_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one, smul_eq_mul, dotL_single] at this
  linarith

theorem plateOf_le_of_affine {u v : Fin n → ℝ} {l m : ℝ} (hv : ∀ i, v i = l * u i + m) :
    plateOf u ≤ plateOf v := by
  rintro y ⟨h1, h2⟩
  refine ⟨h1, ?_⟩
  have e1 : ∑ i, y i = 0 := by simpa [dotL] using h1
  have e2 : ∑ i, u i * y i = 0 := by simpa [dotL] using h2
  show dotL v y = 0
  simp only [dotL, LinearMap.coe_mk, AddHom.coe_mk, hv, add_mul, sum_add_distrib, mul_assoc, ← mul_sum, e1, e2]
  ring

end VacuusResonus
