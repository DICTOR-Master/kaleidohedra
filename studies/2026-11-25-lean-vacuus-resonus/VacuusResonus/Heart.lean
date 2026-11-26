/-
The heart kind (#120 Theorem 1), first half: a centrally symmetric convex set has its exposed faces in opposite pairs, of equal
dimension, so every ridge has its opposite ridge (in the same plate through O).
DICTO, with Claude (Anthropic).
-/
import Mathlib

/-!
# Theorem 1 (⇐): central symmetry gives the heart kind (M6a)

A ridge of a convex body `X` in a finite-dimensional real inner-product space `E` is an exposed face whose direction space has
dimension `finrank E - 2`. `X` is of the heart kind when the opposite `-R` of every ridge `R` is again a ridge (then `R` and `-R`
span the same plate through `O`, and the plate is a full sheet).

* `isExposed_neg`: `F` an exposed face of `X` ⇒ `-F` an exposed face of `-X`.
* `finrank_vectorSpan_neg`: `-F` has the same dimension as `F`.
* `heart_of_symm` (**#120 Theorem 1, ⇐**): `X = -X` ⇒ every ridge's opposite is a ridge.
* `span_neg`: `R` and `-R` span the same plane through `O`.
The converse (⇒) needs that every corner of a polytope lies on a ridge (M6b, next).
-/

open scoped RealInnerProductSpace Pointwise

namespace VacuusResonus

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- A ridge of `X`: an exposed face of dimension `finrank E - 2`. -/
def IsRidge (X R : Set E) : Prop :=
  R.Nonempty ∧ IsExposed ℝ X R ∧ Module.finrank ℝ (vectorSpan ℝ R) + 2 = Module.finrank ℝ E

/-- The heart kind: the opposite of every ridge is a ridge. -/
def IsHeart (X : Set E) : Prop := ∀ R, IsRidge X R → IsRidge X (-R)

theorem isExposed_neg {X F : Set E} (h : IsExposed ℝ X F) : IsExposed ℝ (-X) (-F) := by
  intro hne
  obtain ⟨l, hl⟩ := h (by simpa using hne.neg)
  refine ⟨l.comp (-ContinuousLinearMap.id ℝ E), ?_⟩
  ext x
  simp only [Set.mem_neg, hl, Set.mem_ofPred_eq, ContinuousLinearMap.comp_apply, neg_apply,
    ContinuousLinearMap.id_apply]
  constructor
  · rintro ⟨hx, hmax⟩
    exact ⟨by simpa using hx, fun y hy => by simpa using hmax (-y) (by simpa using hy)⟩
  · rintro ⟨hx, hmax⟩
    exact ⟨by simpa using hx, fun y hy => by simpa using hmax (-y) (by simpa using hy)⟩

theorem vectorSpan_neg (F : Set E) : vectorSpan ℝ (-F) = (vectorSpan ℝ F).map (-LinearMap.id) := by
  rw [vectorSpan_def, vectorSpan_def, Submodule.map_span]
  congr 1
  ext v
  simp only [Set.mem_vsub, Set.mem_neg, Set.mem_image, LinearMap.neg_apply, LinearMap.id_apply, vsub_eq_sub]
  constructor
  · rintro ⟨a, ha, b, hb, rfl⟩; exact ⟨-a - -b, ⟨-a, by simpa using ha, -b, by simpa using hb, rfl⟩, by abel⟩
  · rintro ⟨w, ⟨a, ha, b, hb, rfl⟩, rfl⟩; exact ⟨-a, by simpa using ha, -b, by simpa using hb, by abel⟩

theorem finrank_vectorSpan_neg (F : Set E) :
    Module.finrank ℝ (vectorSpan ℝ (-F)) = Module.finrank ℝ (vectorSpan ℝ F) := by
  rw [vectorSpan_neg]
  exact LinearEquiv.finrank_map_eq (LinearEquiv.neg ℝ) _

/-- **#120 Theorem 1 (⇐).** A centrally symmetric set is of the heart kind. -/
theorem heart_of_symm {X : Set E} (hs : -X = X) : IsHeart X := by
  rintro R ⟨hne, hexp, hdim⟩
  refine ⟨hne.neg, ?_, by rw [finrank_vectorSpan_neg]; exact hdim⟩
  simpa [hs] using isExposed_neg hexp

/-- A ridge and its opposite span the same plane through `O`. -/
theorem span_neg (R : Set E) : Submodule.span ℝ (-R) = Submodule.span ℝ R := by
  apply le_antisymm <;> rw [Submodule.span_le]
  · intro x hx; simpa using (Submodule.span ℝ R).neg_mem (Submodule.subset_span (show -x ∈ R from hx))
  · intro x hx; simpa using (Submodule.span ℝ (-R)).neg_mem (Submodule.subset_span (show -x ∈ -R by simpa using hx))

end VacuusResonus
