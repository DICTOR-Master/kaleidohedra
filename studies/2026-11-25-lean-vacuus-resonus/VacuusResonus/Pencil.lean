/-
The pencil lemma and the polar link in any dimension (#120, Theorems 2 and 4 (b)).
DICTO, with Claude (Anthropic).
-/
import Mathlib

/-!
# The pencil lemma (M5)

A ridge `R = F₁ ∩ F₂` of a polytope `Q` with the centre `O = 0` inside lies in the two facet planes
`⟪u₁, y⟫ = h₁` and `⟪u₂, y⟫ = h₂` (`h₁, h₂ ≠ 0`, as `O` is interior; `u₁, u₂` independent, two different
facets). We state the ridge through its affine span: `ridgeFlat u₁ h₁ u₂ h₂`, the set of points on both planes.

* `span_ridgeFlat` (**#120 Theorem 2, the pencil lemma**): the plane through `O` and the ridge flat,
  `span ℝ (ridgeFlat …)`, is `{y | ⟪h₂ • u₁ - h₁ • u₂, y⟫ = 0}`, i.e. `(ℝ ∙ (h₂ • u₁ - h₁ • u₂))ᗮ`.
* `span_eq_of_affineSpan` : any set `R` whose affine span is the ridge flat spans the same plane (the Vacuus plate of `R`).
* `vacuusPlate_polar` (**#120 Theorem 4 (b), any dimension**): with `h₁ = h₂ = 1` (facet planes `⟪a, x⟫ = 1`,
  `⟪b, x⟫ = 1`, so `a, b` are corners of the polar), the plate is `(ℝ ∙ (a - b))ᗮ`, at right angles to the polar edge.
-/

open scoped RealInnerProductSpace

namespace VacuusResonus

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The points on both facet planes `⟪u₁, y⟫ = h₁` and `⟪u₂, y⟫ = h₂`: the flat carrying a ridge. -/
def ridgeFlat (u₁ : E) (h₁ : ℝ) (u₂ : E) (h₂ : ℝ) : Set E := {y | ⟪u₁, y⟫ = h₁ ∧ ⟪u₂, y⟫ = h₂}

/-- The pencil form `h₂ u₁ - h₁ u₂`. -/
def pencil (u₁ : E) (h₁ : ℝ) (u₂ : E) (h₂ : ℝ) : E := h₂ • u₁ - h₁ • u₂

lemma inner_pencil (u₁ : E) (h₁ : ℝ) (u₂ : E) (h₂ : ℝ) (y : E) :
    ⟪pencil u₁ h₁ u₂ h₂, y⟫ = h₂ * ⟪u₁, y⟫ - h₁ * ⟪u₂, y⟫ := by
  simp [pencil, inner_sub_left, inner_smul_left]

/-- Two independent vectors: the flat is not empty. -/
lemma ridgeFlat_nonempty {u₁ u₂ : E} (hli : LinearIndependent ℝ ![u₁, u₂]) (h₁ h₂ : ℝ) :
    (ridgeFlat u₁ h₁ u₂ h₂).Nonempty := by
  have hc : ⟪u₂, u₁⟫ = ⟪u₁, u₂⟫ := real_inner_comm u₁ u₂
  have hdet : ⟪u₁, u₁⟫ * ⟪u₂, u₂⟫ - ⟪u₁, u₂⟫ * ⟪u₁, u₂⟫ ≠ 0 := by
    intro h0
    have key : ⟪⟪u₂, u₂⟫ • u₁ - ⟪u₁, u₂⟫ • u₂, ⟪u₂, u₂⟫ • u₁ - ⟪u₁, u₂⟫ • u₂⟫ =
        ⟪u₂, u₂⟫ * (⟪u₁, u₁⟫ * ⟪u₂, u₂⟫ - ⟪u₁, u₂⟫ * ⟪u₁, u₂⟫) := by
      simp only [inner_sub_left, inner_sub_right, real_inner_smul_left, real_inner_smul_right, hc]; ring
    rw [h0, mul_zero] at key
    have hz : ⟪u₂, u₂⟫ • u₁ - ⟪u₁, u₂⟫ • u₂ = 0 := inner_self_eq_zero.1 key
    have hg22 : ⟪u₂, u₂⟫ ≠ 0 := inner_self_ne_zero.2 (hli.ne_zero 1)
    have := LinearIndependent.pair_iff.1 hli ⟪u₂, u₂⟫ (-⟪u₁, u₂⟫) (by rw [neg_smul, ← sub_eq_add_neg]; exact hz)
    exact hg22 this.1
  have hd2 : ⟪u₂, u₂⟫ * ⟪u₁, u₁⟫ - ⟪u₁, u₂⟫ ^ 2 ≠ 0 := by
    intro h; apply hdet; linear_combination h
  have hd3 : -⟪u₁, u₂⟫ ^ 2 + ⟪u₂, u₂⟫ * ⟪u₁, u₁⟫ ≠ 0 := by
    intro h; apply hdet; linear_combination h
  refine ⟨((h₁ * ⟪u₂, u₂⟫ - h₂ * ⟪u₁, u₂⟫) / (⟪u₁, u₁⟫ * ⟪u₂, u₂⟫ - ⟪u₁, u₂⟫ * ⟪u₁, u₂⟫)) • u₁ +
      ((h₂ * ⟪u₁, u₁⟫ - h₁ * ⟪u₁, u₂⟫) / (⟪u₁, u₁⟫ * ⟪u₂, u₂⟫ - ⟪u₁, u₂⟫ * ⟪u₁, u₂⟫)) • u₂, ?_, ?_⟩
  · simp only [inner_add_right, real_inner_smul_right]
    field_simp; ring
  · simp only [inner_add_right, real_inner_smul_right, hc]
    field_simp; ring

/-- **#120 Theorem 2 (the pencil lemma).** For independent `u₁, u₂` and `h₁, h₂ ≠ 0`, the plane through `O`
and the ridge flat is the zero set of the pencil form `h₂ u₁ - h₁ u₂`. -/
theorem span_ridgeFlat {u₁ u₂ : E} (hli : LinearIndependent ℝ ![u₁, u₂]) {h₁ h₂ : ℝ}
    (hh₁ : h₁ ≠ 0) (hh₂ : h₂ ≠ 0) :
    Submodule.span ℝ (ridgeFlat u₁ h₁ u₂ h₂) = (ℝ ∙ pencil u₁ h₁ u₂ h₂)ᗮ := by
  apply le_antisymm
  · rw [Submodule.span_le]
    intro y hy
    rw [SetLike.mem_coe, Submodule.mem_orthogonal_singleton_iff_inner_right, inner_pencil, hy.1, hy.2]
    ring
  · intro z hz
    rw [Submodule.mem_orthogonal_singleton_iff_inner_right, inner_pencil] at hz
    obtain ⟨p, hp⟩ := ridgeFlat_nonempty hli h₁ h₂
    by_cases hα : ⟪u₁, z⟫ = 0
    · -- then also ⟪u₂, z⟫ = 0: z = (p + z) - p with both in the flat
      have h2 : ⟪u₂, z⟫ = 0 := by
        have : h₁ * ⟪u₂, z⟫ = 0 := by linarith [hz, show h₂ * ⟪u₁, z⟫ = 0 by rw [hα, mul_zero]]
        exact (mul_eq_zero.1 this).resolve_left hh₁
      have hpz : p + z ∈ ridgeFlat u₁ h₁ u₂ h₂ := by
        refine ⟨?_, ?_⟩ <;> simp [inner_add_right, hp.1, hp.2, hα, h2]
      have := (Submodule.span ℝ (ridgeFlat u₁ h₁ u₂ h₂)).sub_mem (Submodule.subset_span hpz) (Submodule.subset_span hp)
      simpa using this
    · -- z is a nonzero multiple of a point of the flat
      set α := ⟪u₁, z⟫ / h₁ with hαdef
      have hα0 : α ≠ 0 := div_ne_zero hα hh₁
      have hq : α⁻¹ • z ∈ ridgeFlat u₁ h₁ u₂ h₂ := by
        refine ⟨?_, ?_⟩
        · simp only [inner_smul_right, hαdef]; field_simp
        · simp only [inner_smul_right, hαdef]
          have h2 : ⟪u₂, z⟫ = h₂ * ⟪u₁, z⟫ / h₁ := by field_simp; linarith
          rw [h2]; field_simp
      have := (Submodule.span ℝ (ridgeFlat u₁ h₁ u₂ h₂)).smul_mem α (Submodule.subset_span hq)
      simpa [smul_smul, hα0] using this

/-- Any set whose affine span is the ridge flat spans the same plane through `O`. -/
theorem span_eq_of_affineSpan {R : Set E} {u₁ u₂ : E} {h₁ h₂ : ℝ}
    (hR : (affineSpan ℝ R : Set E) = ridgeFlat u₁ h₁ u₂ h₂) :
    Submodule.span ℝ R = Submodule.span ℝ (ridgeFlat u₁ h₁ u₂ h₂) := by
  apply le_antisymm
  · exact Submodule.span_mono (hR ▸ subset_affineSpan ℝ R)
  · rw [Submodule.span_le, ← hR]
    intro y hy
    exact (affineSpan_le_toAffineSubspace_span (k := ℝ) (s := R)) hy

/-- **#120 Theorem 4 (b), any dimension.** A ridge whose affine span is the flat of the facet planes
`⟪a, x⟫ = 1` and `⟪b, x⟫ = 1` (independent `a, b`, the corners of the polar dual to the two facets) spans the
plane `(ℝ ∙ (a - b))ᗮ`: the Vacuus plate is at right angles to the polar edge `[a, b]`. -/
theorem vacuusPlate_polar {R : Set E} {a b : E} (hli : LinearIndependent ℝ ![a, b])
    (hR : (affineSpan ℝ R : Set E) = ridgeFlat a 1 b 1) :
    Submodule.span ℝ R = (ℝ ∙ (a - b))ᗮ := by
  rw [span_eq_of_affineSpan hR, span_ridgeFlat hli one_ne_zero one_ne_zero]
  simp [pencil]

end VacuusResonus
