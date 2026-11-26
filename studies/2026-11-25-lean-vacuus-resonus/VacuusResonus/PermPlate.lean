/-
The Vacuus plates of the permutohedron in every dimension (#120 Theorem 3 (i)).
DICTO, with Claude (Anthropic).
-/
import Mathlib

/-!
# Theorem 3 (i): the plate of a permutohedron ridge (M7)

The permutohedron `Π_n` (corners: the permutations of `(1, …, n)`, centred) lies in `V₀ = {y | ∑ y = 0}`. Its facet for a set
`S` (`∅ ≠ S ≠ [n]`, `m = |S|`) lies on `∑_{i ∈ S} yᵢ = m (n - m) / 2`. A ridge is given by an ordered split `(B₁, B₂, B₃)` of `[n]`
into nonempty blocks (sizes `a, b, c`): it lies on the facets `S₁ = B₁` and `S₂ = B₁ ∪ B₂`, at heights `a (b + c) / 2` and
`(a + b) c / 2`. We take the ridge through the flat of these two planes inside `V₀` (`permFlat`).

* `span_permFlat` (**#120 Theorem 3 (i)**): the plane through `O` and the ridge flat is
  `{y ∈ V₀ | c (a + b) ∑_{B₁} y + a (b + c) ∑_{B₃} y = 0}`.
-/

namespace VacuusResonus

open Finset

variable {n : ℕ}

/-- The flat of the ridge `(B₁, B₂, B₃)` inside `V₀`. -/
def permFlat (B₁ B₂ B₃ : Finset (Fin n)) : Set (Fin n → ℝ) :=
  {y | ∑ i ∈ B₁, y i = (B₁.card : ℝ) * ((B₂.card : ℝ) + B₃.card) / 2 ∧
       ∑ i ∈ B₁ ∪ B₂, y i = ((B₁.card : ℝ) + B₂.card) * B₃.card / 2 ∧ ∑ i, y i = 0}

/-- The plate predicted by #120 Theorem 3 (i), as a submodule of `Fin n → ℝ`. -/
def permPlate (B₁ B₂ B₃ : Finset (Fin n)) : Submodule ℝ (Fin n → ℝ) where
  carrier := {y | ∑ i, y i = 0 ∧
    (B₃.card : ℝ) * ((B₁.card : ℝ) + B₂.card) * ∑ i ∈ B₁, y i +
      (B₁.card : ℝ) * ((B₂.card : ℝ) + B₃.card) * ∑ i ∈ B₃, y i = 0}
  add_mem' := by
    rintro x y ⟨hx1, hx2⟩ ⟨hy1, hy2⟩
    refine ⟨?_, ?_⟩
    · simp [Finset.sum_add_distrib, hx1, hy1]
    · simp only [Pi.add_apply, Finset.sum_add_distrib]; linear_combination hx2 + hy2
  zero_mem' := by simp
  smul_mem' := by
    rintro t y ⟨h1, h2⟩
    refine ⟨?_, ?_⟩
    · simp [← Finset.mul_sum, h1]
    · simp only [Pi.smul_apply, smul_eq_mul, ← Finset.mul_sum]; linear_combination t * h2

variable {B₁ B₂ B₃ : Finset (Fin n)}

/-- For a split of `[n]`, the three block sums add up to the total. -/
lemma sum_split (h12 : Disjoint B₁ B₂) (h13 : Disjoint B₁ B₃) (h23 : Disjoint B₂ B₃)
    (hu : B₁ ∪ B₂ ∪ B₃ = univ) (y : Fin n → ℝ) :
    ∑ i, y i = ∑ i ∈ B₁, y i + ∑ i ∈ B₂, y i + ∑ i ∈ B₃, y i := by
  rw [← hu, sum_union (disjoint_union_left.2 ⟨h13, h23⟩), sum_union h12]

/-- The block-constant point of the flat (so the flat is not empty). -/
lemma permFlat_nonempty (h12 : Disjoint B₁ B₂) (h13 : Disjoint B₁ B₃) (h23 : Disjoint B₂ B₃)
    (hu : B₁ ∪ B₂ ∪ B₃ = univ) :
    (permFlat B₁ B₂ B₃).Nonempty := by
  let x₁ : ℝ := ((B₂.card : ℝ) + B₃.card) / 2
  let x₂ : ℝ := ((B₃.card : ℝ) - B₁.card) / 2
  let x₃ : ℝ := -((B₁.card : ℝ) + B₂.card) / 2
  let f : Fin n → ℝ := fun i => if i ∈ B₁ then x₁ else if i ∈ B₂ then x₂ else x₃
  have s1 : ∑ i ∈ B₁, f i = B₁.card * x₁ := by
    rw [sum_congr rfl (g := fun _ => x₁) (fun i hi => by simp [f, hi])]; simp
  have s2 : ∑ i ∈ B₂, f i = B₂.card * x₂ := by
    rw [sum_congr rfl (g := fun _ => x₂) (fun i hi => by simp [f, hi, disjoint_right.1 h12 hi])]; simp
  have s3 : ∑ i ∈ B₃, f i = B₃.card * x₃ := by
    rw [sum_congr rfl (g := fun _ => x₃) (fun i hi => by simp [f, disjoint_right.1 h13 hi, disjoint_right.1 h23 hi])]; simp
  refine ⟨f, ?_, ?_, ?_⟩
  · rw [s1]; simp only [x₁]; ring
  · rw [sum_union h12, s1, s2]; simp only [x₁, x₂]; ring
  · rw [sum_split h12 h13 h23 hu, s1, s2, s3]; simp only [x₁, x₂, x₃]; ring

/-- **#120 Theorem 3 (i).** The Vacuus plate of the permutohedron ridge `(B₁, B₂, B₃)`. -/
theorem span_permFlat (h12 : Disjoint B₁ B₂) (h13 : Disjoint B₁ B₃) (h23 : Disjoint B₂ B₃)
    (hu : B₁ ∪ B₂ ∪ B₃ = univ) (ha : B₁.Nonempty) (hb : B₂.Nonempty) (hc : B₃.Nonempty) :
    Submodule.span ℝ (permFlat B₁ B₂ B₃) = permPlate B₁ B₂ B₃ := by
  set a : ℝ := (B₁.card : ℝ); set b : ℝ := (B₂.card : ℝ); set c : ℝ := (B₃.card : ℝ)
  have ha0 : a ≠ 0 := by simp [a, ha.ne_empty]
  have hb0 : b ≠ 0 := by simp [b, hb.ne_empty]
  have hc0 : c ≠ 0 := by simp [c, hc.ne_empty]
  have hsplit := sum_split h12 h13 h23 hu
  apply le_antisymm
  · rw [Submodule.span_le]
    rintro y ⟨h1, h2, h0⟩
    refine ⟨h0, ?_⟩
    have h2' : ∑ i ∈ B₁, y i + ∑ i ∈ B₂, y i = (a + b) * c / 2 := by rw [← sum_union h12]; exact h2
    have h3 : ∑ i ∈ B₃, y i = -(∑ i ∈ B₁, y i + ∑ i ∈ B₂, y i) := by linarith [hsplit y]
    rw [h3, h1]; rw [show ∑ i ∈ B₂, y i = (a + b) * c / 2 - a * (b + c) / 2 by linarith]; ring
  · rintro z ⟨hz0, hz⟩
    obtain ⟨p, hp1, hp2, hp0⟩ := permFlat_nonempty h12 h13 h23 hu
    by_cases hα : ∑ i ∈ B₁, z i = 0
    · have h3 : ∑ i ∈ B₃, z i = 0 := by
        have : a * (b + c) * ∑ i ∈ B₃, z i = 0 := by rw [hα, mul_zero] at hz; linarith
        rcases mul_eq_zero.1 this with h | h
        · exfalso; rcases mul_eq_zero.1 h with h | h
          · exact ha0 h
          · have : (0 : ℝ) < b + c := by positivity
            linarith
        · exact h
      have h2 : ∑ i ∈ B₂, z i = 0 := by linarith [hsplit z]
      have hpz : p + z ∈ permFlat B₁ B₂ B₃ := by
        refine ⟨?_, ?_, ?_⟩
        · simp [sum_add_distrib, hp1, hα]
        · have hz12 : ∑ i ∈ B₁ ∪ B₂, z i = 0 := by rw [sum_union h12, hα, h2, add_zero]
          simp only [Pi.add_apply, sum_add_distrib, hp2, hz12, add_zero]
        · simp [sum_add_distrib, hp0, hz0]
      have := (Submodule.span ℝ (permFlat B₁ B₂ B₃)).sub_mem (Submodule.subset_span hpz) (Submodule.subset_span ⟨hp1, hp2, hp0⟩)
      simpa using this
    · set α : ℝ := (∑ i ∈ B₁, z i) / (a * (b + c) / 2) with hαd
      have hbc : b + c ≠ 0 := by have : (0 : ℝ) < b + c := by positivity
                                 linarith
      have hα0 : α ≠ 0 := div_ne_zero hα (by positivity)
      have hq : α⁻¹ • z ∈ permFlat B₁ B₂ B₃ := by
        have hB3 : ∑ i ∈ B₃, z i = -(c * (a + b)) * (∑ i ∈ B₁, z i) / (a * (b + c)) := by
          field_simp; linarith [hz]
        refine ⟨?_, ?_, ?_⟩
        · simp only [Pi.smul_apply, smul_eq_mul, ← mul_sum, hαd]; field_simp; simp [a, b, c]
        · simp only [Pi.smul_apply, smul_eq_mul, ← mul_sum, sum_union h12, hαd]
          have h2 : ∑ i ∈ B₂, z i = -(∑ i ∈ B₁, z i) - ∑ i ∈ B₃, z i := by linarith [hsplit z]
          rw [h2, hB3]; field_simp; ring
        · simp [← mul_sum, hz0]
      have := (Submodule.span ℝ (permFlat B₁ B₂ B₃)).smul_mem α (Submodule.subset_span hq)
      simpa [smul_smul, hα0] using this

end VacuusResonus
