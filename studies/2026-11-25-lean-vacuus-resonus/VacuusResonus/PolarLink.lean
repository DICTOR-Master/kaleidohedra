/-
The polar link of the Resonus and the Vacuus (study 2026-11-24-resonus, Theorem 1).
DICTO, with Claude (Anthropic).
-/
import Mathlib

/-!
# The polar link (M1)

A facet `F` of a convex polytope `P` with the centre `O = 0` inside lies on the plane `⟪a, x⟫ = 1`;
the vector `a` is the corner of the polar `P*` dual to `F` (standard face duality, Ziegler,
*Lectures on Polytopes*, Thm 2.11; not formalised here).

* `resonusPlane_eq_orthogonal` (**Theorem 1 (a)**): the plane through `O` parallel to the facet plane
  `⟪a, x⟫ = 1` is `{x | ⟪a, x⟫ = 0}`, the orthogonal complement of the line `ℝ ∙ a` from `O` to the
  polar corner `a`.
* `vacuusPlate_eq` (**Theorem 1 (b)**, in 3-space): if the edge `[u, v]` (`u ≠ v`) lies on the two facet
  planes `⟪a, x⟫ = 1` and `⟪b, x⟫ = 1` (`a ≠ b`), the plane through `O` and the edge, `span {u, v}`,
  is the orthogonal complement of `ℝ ∙ (a - b)`, the direction of the polar edge `[a, b]`.
-/

open scoped RealInnerProductSpace

namespace VacuusResonus

section General

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The facet plane `⟪a, x⟫ = 1`. -/
def facetPlane (a : E) : Set E := {x | ⟪a, x⟫ = 1}

/-- The polar of a set `P`. -/
def polar (P : Set E) : Set E := {y | ∀ x ∈ P, ⟪y, x⟫ ≤ 1}

/-- The vector `a` of a supporting plane `⟪a, x⟫ = 1` of `P` lies in the polar of `P`. -/
theorem mem_polar {P : Set E} {a : E} (h : ∀ x ∈ P, ⟪a, x⟫ ≤ 1) : a ∈ polar P := h

/-- The Resonus plane of the facet plane `⟪a, x⟫ = 1`: the plane through `O` parallel to it, i.e.
the translations that carry the facet plane into itself. -/
def resonusPlane (a : E) : Set E := {v | ∀ p ∈ facetPlane a, p + v ∈ facetPlane a}

/-- **Theorem 1 (a), first form.** The Resonus plane of `⟪a, x⟫ = 1` is `⟪a, x⟫ = 0`. -/
theorem resonusPlane_eq {a : E} (ha : a ≠ 0) : resonusPlane a = {x | ⟪a, x⟫ = 0} := by
  ext v
  simp only [resonusPlane, facetPlane, Set.mem_ofPred_eq]
  constructor
  · intro h
    have hp : ⟪a, (‖a‖ ^ 2)⁻¹ • a⟫ = 1 := by
      rw [real_inner_smul_right, real_inner_self_eq_norm_sq]
      have : ‖a‖ ≠ 0 := norm_ne_zero_iff.2 ha
      field_simp
    have h2 := h _ hp
    rw [inner_add_right, hp] at h2
    linarith
  · intro hv p hp
    rw [inner_add_right, hp, hv, add_zero]

/-- **Theorem 1 (a).** The Resonus plane of the facet `⟪a, x⟫ = 1` is the plane through `O` at right
angles to the vector from `O` to the polar corner `a`. -/
theorem resonusPlane_eq_orthogonal {a : E} (ha : a ≠ 0) :
    resonusPlane a = ((ℝ ∙ a)ᗮ : Submodule ℝ E) := by
  rw [resonusPlane_eq ha]
  ext v
  simp [Submodule.mem_orthogonal_singleton_iff_inner_right]

end General

/-- Euclidean 3-space. -/
abbrev E3 := EuclideanSpace ℝ (Fin 3)

/-- The Vacuus plate of the edge `[u, v]`: the plane through `O` and the edge. -/
def vacuusPlate (u v : E3) : Submodule ℝ E3 := Submodule.span ℝ {u, v}

/-- The plate contains the whole edge. -/
theorem segment_subset_vacuusPlate (u v : E3) :
    segment ℝ u v ⊆ (vacuusPlate u v : Set E3) :=
  (Submodule.convex _).segment_subset (Submodule.subset_span (by simp))
    (Submodule.subset_span (by simp))

/-- **Theorem 1 (b).** If the edge `[u, v]` lies on the facet planes `⟪a, x⟫ = 1` and `⟪b, x⟫ = 1`
of two distinct facets, its Vacuus plate is the plane through `O` at right angles to the polar edge
`[a, b]`. -/
theorem vacuusPlate_eq {a b u v : E3} (hab : a ≠ b) (huv : u ≠ v)
    (hua : ⟪a, u⟫ = 1) (hva : ⟪a, v⟫ = 1) (hub : ⟪b, u⟫ = 1) (hvb : ⟪b, v⟫ = 1) :
    vacuusPlate u v = (ℝ ∙ (a - b))ᗮ := by
  have hle : vacuusPlate u v ≤ (ℝ ∙ (a - b))ᗮ := by
    rw [vacuusPlate, Submodule.span_le]
    rintro x (rfl | rfl)
    · simp [Submodule.mem_orthogonal_singleton_iff_inner_right, inner_sub_left, hua, hub]
    · simp [Submodule.mem_orthogonal_singleton_iff_inner_right, inner_sub_left, hva, hvb]
  have hli : LinearIndependent ℝ ![u, v] := by
    rw [LinearIndependent.pair_iff]
    intro s t hst
    have h1 : s + t = 0 := by
      have := congrArg (fun x => ⟪a, x⟫) hst
      simp only [inner_add_right, real_inner_smul_right, hua, hva, inner_zero_right] at this
      linarith
    have ht : t = -s := by linarith
    subst ht
    have h2 : s • (u - v) = 0 := by
      rw [smul_sub, sub_eq_add_neg, ← neg_smul]
      exact hst
    rcases smul_eq_zero.1 h2 with h | h
    · simp [h]
    · exact absurd (sub_eq_zero.1 h) huv
  have hrange : Set.range ![u, v] = {u, v} := by
    ext x
    simp only [Set.mem_range, Fin.exists_fin_two, Matrix.cons_val_zero, Matrix.cons_val_one,
      Set.mem_insert_iff, Set.mem_singleton_iff]
    tauto
  have hrank : Module.finrank ℝ (vacuusPlate u v) = 2 := by
    rw [vacuusPlate, ← hrange, finrank_span_eq_card hli, Fintype.card_fin]
  have : Fact (Module.finrank ℝ E3 = 2 + 1) := ⟨by simp⟩
  have hab' : a - b ≠ 0 := sub_ne_zero.2 hab
  exact Submodule.eq_of_le_of_finrank_eq hle
    (by rw [hrank, Submodule.finrank_orthogonal_span_singleton (n := 2) hab'])

end VacuusResonus
