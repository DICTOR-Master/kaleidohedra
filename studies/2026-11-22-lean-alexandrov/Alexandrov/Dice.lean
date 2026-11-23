/-
Alexandrov's theorem on prescribed curvature, polyhedral case: fair dice (#112, Theorem A (a)).
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Main

/-!
# Fair dice (M11)

A die with face normals `n j` (distinct unit vectors, not all in one closed hemisphere) and face
distances `d j > 0` is `die n d = {x | ∀ j, ⟪n j, x⟫ ≤ d j}`. The rays from `0` that leave the die
through face `k` form `faceCone n d k`; the solid angle of face `k` is the area of their directions,
`3 * volume (faceCone n d k ∩ unit ball)`. The die is fair about `0` when every face has solid
angle `4π / N`.

* `solidAngle_eq_curvature` (**#112 Lemma 1, the polar identity**): the solid angle of face `k` equals
  the curvature of the polar polytope (corners `n j / d j`) at its corner `n k / d k`.
* `fair_die_iff` (**#112 Theorem A (a), existence**): a fair die with these face normals exists if and
  only if Alexandrov's condition holds for the equal curvatures `4π / N`.
* `fair_die_unique` (**uniqueness**): two fair dice with the same face normals are equal up to scaling
  about `0`.
-/

open MeasureTheory Set Metric Finset
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

/-- The die with face normals `n j` at distances `d j` from the origin. -/
def die (n : Fin N → E3) (d : Fin N → ℝ) : Set E3 := {x | ∀ j, ⟪n j, x⟫ ≤ d j}

/-- Directions `x` whose ray from the origin leaves the die through face `k`. -/
def faceCone (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) : Set E3 :=
  {x | ∃ t : ℝ, 0 < t ∧ t • x ∈ die n d ∧ ⟪n k, t • x⟫ = d k}

/-- The solid angle of face `k` seen from the origin (area of the directions through it). -/
noncomputable def solidAngle (n : Fin N → E3) (d : Fin N → ℝ) (k : Fin N) : ℝ≥0∞ :=
  3 * volume (faceCone n d k ∩ ball (0 : E3) 1)

/-- A die is fair about the origin when all `N` faces have solid angle `4π / N`. -/
def IsFair (n : Fin N → E3) (d : Fin N → ℝ) : Prop :=
  ∀ k, solidAngle n d k = ENNReal.ofReal (4 * Real.pi / N)

/-- **#112 Lemma 1 (the polar identity).** -/
theorem solidAngle_eq_curvature {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d : Fin N → ℝ} (hd : ∀ j, 0 < d j) (k : Fin N) :
    solidAngle n d k =
      curvature (rayPolytope n fun j => (d j)⁻¹) (corner n (fun j => (d j)⁻¹) k) := by
  rw [curvature_rayPolytope, solidAngle]
  have hdk := (hd k).ne'
  have hsub : faceCone n d k ⊆ cell n (fun j => (d j)⁻¹) k := by
    rintro x ⟨t, ht, hdie, hface⟩ j
    have hdj := (hd j).ne'
    have h1 := hdie j
    rw [real_inner_smul_right] at h1 hface
    have key : t * (⟪n j, x⟫ * d k) ≤ t * (⟪n k, x⟫ * d j) := by
      have e : d j * d k = t * (⟪n k, x⟫ * d j) := by rw [← hface]; ring
      have := mul_le_mul_of_nonneg_right h1 (hd k).le
      linarith
    have key' := le_of_mul_le_mul_left key ht
    have e1 : (d j)⁻¹ * ⟪n j, x⟫ = (⟪n j, x⟫ * d k) * ((d j)⁻¹ * (d k)⁻¹) := by field_simp
    have e2 : (d k)⁻¹ * ⟪n k, x⟫ = (⟪n k, x⟫ * d j) * ((d j)⁻¹ * (d k)⁻¹) := by field_simp
    show (d j)⁻¹ * ⟪n j, x⟫ ≤ (d k)⁻¹ * ⟪n k, x⟫
    rw [e1, e2]
    exact mul_le_mul_of_nonneg_right key' (by have := hd j; have := hd k; positivity)
  have hsup : cell n (fun j => (d j)⁻¹) k ⊆ faceCone n d k ∪ {0} := by
    intro x hx
    by_cases hx0 : x = 0
    · exact Or.inr hx0
    left
    obtain ⟨m, hm⟩ := hspan x hx0
    have hcm := hx m
    have hb : 0 < ⟪n k, x⟫ := by
      have : 0 < (d m)⁻¹ * ⟪n m, x⟫ := mul_pos (inv_pos.2 (hd m)) hm
      have : 0 < (d k)⁻¹ * ⟪n k, x⟫ := lt_of_lt_of_le this hcm
      exact pos_of_mul_pos_right this (inv_pos.2 (hd k)).le
    refine ⟨d k / ⟪n k, x⟫, div_pos (hd k) hb, fun j => ?_, ?_⟩
    · rw [real_inner_smul_right, div_mul_eq_mul_div, div_le_iff₀ hb]
      have hc : (d j)⁻¹ * ⟪n j, x⟫ ≤ (d k)⁻¹ * ⟪n k, x⟫ := hx j
      have h' := (inv_mul_le_iff₀ (hd j)).1 hc
      calc d k * ⟪n j, x⟫ ≤ d k * (d j * ((d k)⁻¹ * ⟪n k, x⟫)) :=
            mul_le_mul_of_nonneg_left h' (hd k).le
        _ = d j * ⟪n k, x⟫ := by field_simp
    · rw [real_inner_smul_right, div_mul_cancel₀ _ hb.ne']
  congr 1
  refine le_antisymm (measure_mono (Set.inter_subset_inter_left _ hsub)) ?_
  calc volume (cell n (fun j => (d j)⁻¹) k ∩ ball (0 : E3) 1)
      ≤ volume ((faceCone n d k ∩ ball (0 : E3) 1) ∪ {0}) := by
        refine measure_mono fun x ⟨hx, hb⟩ => ?_
        rcases hsup hx with h | h
        · exact Or.inl ⟨h, hb⟩
        · exact Or.inr h
    _ ≤ volume (faceCone n d k ∩ ball (0 : E3) 1) + volume ({0} : Set E3) := measure_union_le _ _
    _ = volume (faceCone n d k ∩ ball (0 : E3) 1) := by rw [measure_singleton, add_zero]

/-- **#112 Theorem A (a), existence.** A fair die with face normals `n` exists if and only if
Alexandrov's condition holds for the equal curvatures `4π / N`. -/
theorem fair_die_iff [NeZero N] {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫) :
    (∃ d : Fin N → ℝ, (∀ j, 0 < d j) ∧ IsFair n d) ↔
      AlexandrovCondition n (fun _ => 4 * Real.pi / N) := by
  have hN : (0 : ℝ) < N := Nat.cast_pos.2 (Nat.pos_of_ne_zero (NeZero.ne N))
  have hκ : ∀ j : Fin N, 0 < (fun _ : Fin N => 4 * Real.pi / N) j := fun _ => by positivity
  have hsum : ∑ _j : Fin N, 4 * Real.pi / N = 4 * Real.pi := by
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    field_simp
  constructor
  · rintro ⟨d, hd, hfair⟩
    refine (alexandrov_necessary hn hinj hspan hκ (r := fun j => (d j)⁻¹)
      (fun j => inv_pos.2 (hd j)) fun j => ?_).2
    rw [← solidAngle_eq_curvature hspan hd, hfair j]
  · intro hA
    obtain ⟨r, hr, hcurv⟩ := (alexandrov_iff hn hinj hspan hκ).2 ⟨hsum, hA⟩
    refine ⟨fun j => (r j)⁻¹, fun j => inv_pos.2 (hr j), fun k => ?_⟩
    rw [solidAngle_eq_curvature hspan (fun j => inv_pos.2 (hr j))]
    simp only [inv_inv]
    exact hcurv k

/-- **Uniqueness of the fair die.** Two fair dice with the same face normals are equal up to
scaling about the origin. -/
theorem fair_die_unique [NeZero N] {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {d d' : Fin N → ℝ} (hd : ∀ j, 0 < d j) (hd' : ∀ j, 0 < d' j)
    (hf : IsFair n d) (hf' : IsFair n d') : ∃ c : ℝ, 0 < c ∧ d' = c • d := by
  have hN : (0 : ℝ) < N := Nat.cast_pos.2 (Nat.pos_of_ne_zero (NeZero.ne N))
  obtain ⟨c, hc, hrc⟩ := alexandrov_unique hn hinj hspan (κ := fun _ => 4 * Real.pi / N)
    (fun _ => by positivity) (r := fun j => (d j)⁻¹) (r' := fun j => (d' j)⁻¹)
    (fun j => inv_pos.2 (hd j)) (fun j => inv_pos.2 (hd' j))
    (fun j => by rw [← solidAngle_eq_curvature hspan hd, hf j])
    (fun j => by rw [← solidAngle_eq_curvature hspan hd', hf' j])
  refine ⟨c⁻¹, inv_pos.2 hc, funext fun j => ?_⟩
  have h := congrFun hrc j
  simp only [Pi.smul_apply, smul_eq_mul] at h ⊢
  have hdj := (hd j).ne'
  have hd'j := (hd' j).ne'
  field_simp at h ⊢
  linarith

end Alexandrov
