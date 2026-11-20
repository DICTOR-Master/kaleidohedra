/-
Dehn–Hadwiger study, part 3: the bridge (DICTO, 20 Nov 2026).

* `dehnHadwiger_image`: every isometry of the space keeps the invariant.
* `dehnHadwiger_dissection`: the invariant is additive over dissections of a convex polytope into convex polytopes.
* `dehnHadwiger_eq_of_scissorsCongruent` (**the bridge**): scissors-congruent convex polytopes have the same
  Dehn–Hadwiger invariant, in every finite dimension (Hadwiger 1954 for the classical ridge-sum invariant).
* `dehnHadwigerSum_eq_of_scissors`: the same for finite unions of convex polytopes.

The dissection step is the Canon's `DehnCanon.dissection_additive` (common refinement by the facet hyperplanes),
applied to the cut identity of part 2; scissors congruence is the Canon's `DehnCanon.ScissorsCongruent`, which
does not depend on the dimension. The rigid-motion step reuses the Canon's `tcone_image`, `linSpace_image` and
`wedgeAngleIn_image`.
No `sorry`.
-/
import DehnHadwiger.DH2Cut
import DehnCanon.DehnCanon2

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

lemma thetaH_image (L : E ≃ₗᵢ[ℝ] E) (T : Set E) : thetaH (L '' T) = thetaH T := by
  unfold thetaH
  rw [linSpace_image, LinearEquiv.finrank_map_eq]
  by_cases h : finrank ℝ (linSpace T) + 2 = finrank ℝ E
  · simp only [h, ↓reduceIte]
    rw [wedgeAngle_eq_in, wedgeAngle_eq_in, ← Submodule.map_orthogonal_equiv, wedgeAngleIn_image]
  · simp only [h, ↓reduceIte]

lemma ridgeAngle_image (g : E ≃ᵃⁱ[ℝ] E) (P : Set E) (x : E) :
    ridgeAngle (g '' P) (g x) = ridgeAngle P x := by
  unfold ridgeAngle
  rw [tcone_image, thetaH_image]

/-- **Rigid motions keep the Dehn–Hadwiger invariant.** -/
theorem dehnHadwiger_image (g : E ≃ᵃⁱ[ℝ] E) (P : Set E) : dehnHadwiger (g '' P) = dehnHadwiger P := by
  unfold dehnHadwiger
  apply finsum_congr; intro θ
  have h : {y | ridgeAngle (g '' P) y = θ} = g '' {x | ridgeAngle P x = θ} := by
    ext y; constructor
    · intro hy
      refine ⟨g.symm y, ?_, g.apply_symm_apply y⟩
      show ridgeAngle P (g.symm y) = θ
      rw [← ridgeAngle_image g P (g.symm y), g.apply_symm_apply]; exact hy
    · rintro ⟨x, hx, rfl⟩
      show ridgeAngle (g '' P) (g x) = θ
      rw [ridgeAngle_image]; exact hx
  rw [h, g.isometry.hausdorffMeasure_image (Or.inl (Nat.cast_nonneg _))]

/-- In dimension below 2 there are no ridge points, and the invariant is zero. -/
lemma dehnHadwiger_eq_zero_of_lt (hE : finrank ℝ E < 2) (P : Set E) : dehnHadwiger P = 0 := by
  have h0 : ∀ x, ridgeAngle P x = 0 := by
    intro x
    unfold ridgeAngle thetaH
    rw [ite_eq_right]
    intro h; omega
  unfold dehnHadwiger
  apply finsum_eq_zero_of_forall_eq_zero
  intro θ
  by_cases hθ : θ = 0
  · rw [hθ, TensorProduct.tmul_zero]
  · have : {x | ridgeAngle P x = θ} = ∅ := by
      ext x; simp only [mem_ofPred_eq, h0, mem_empty_iff_false, iff_false]; exact fun h => hθ h.symm
    rw [this, measure_empty, ENNReal.toReal_zero, TensorProduct.zero_tmul]

/-- **The invariant is additive over dissections.** If a convex polytope `P` is the union of finitely many
convex polytopes `p k` with pairwise disjoint interiors, then `dehnHadwiger P = Σ k, dehnHadwiger (p k)`. -/
theorem dehnHadwiger_dissection {κ : Type} [Fintype κ] {P : Set E} {p : κ → Set E} (hP : IsPoly P)
    (hp : ∀ k, IsPoly (p k)) (hU : (⋃ k, p k) = P)
    (hdisj : Pairwise fun i j => Disjoint (interior (p i)) (interior (p j))) :
    dehnHadwiger P = ∑ k, dehnHadwiger (p k) := by
  by_cases hE : finrank ℝ E < 2
  · simp [dehnHadwiger_eq_zero_of_lt hE]
  · have : Nontrivial E := Module.nontrivial_of_finrank_pos (R := ℝ) (by omega)
    exact dissection_additive dehnHadwiger (fun Q hQ c d hc => dehnHadwiger_cut hQ c d hc) hP hp hU hdisj

/-- **The bridge.** Scissors-congruent convex polytopes have the same Dehn–Hadwiger invariant. -/
theorem dehnHadwiger_eq_of_scissorsCongruent {P Q : Set E} (hP : IsPoly P) (hQ : IsPoly Q)
    (h : ScissorsCongruent P Q) : dehnHadwiger P = dehnHadwiger Q := by
  obtain ⟨κ, _, p, g, hp, hUP, hdP, hUQ, hdQ⟩ := h
  rw [dehnHadwiger_dissection hP hp hUP hdP,
    dehnHadwiger_dissection hQ (fun k => (hp k).image (g k)) hUQ hdQ]
  exact Finset.sum_congr rfl fun k _ => (dehnHadwiger_image (g k) (p k)).symm

/-- Contrapositive: convex polytopes with different invariants are not scissors congruent. -/
theorem not_scissorsCongruent_of_dehnHadwiger_ne {P Q : Set E} (hP : IsPoly P) (hQ : IsPoly Q)
    (h : dehnHadwiger P ≠ dehnHadwiger Q) : ¬ ScissorsCongruent P Q :=
  fun hs => h (dehnHadwiger_eq_of_scissorsCongruent hP hQ hs)

/-- Two families of convex polytopes, each with pairwise disjoint interiors, that fill the same set have the
same total invariant. -/
theorem dehnHadwigerSum_eq_of_same_union {κ κ' : Type} [Fintype κ] [Fintype κ'] {p : κ → Set E}
    {q : κ' → Set E} (hp : ∀ k, IsPoly (p k)) (hq : ∀ l, IsPoly (q l))
    (hdp : Pairwise fun i j => Disjoint (interior (p i)) (interior (p j)))
    (hdq : Pairwise fun i j => Disjoint (interior (q i)) (interior (q j)))
    (hU : (⋃ k, p k) = ⋃ l, q l) :
    ∑ k, dehnHadwiger (p k) = ∑ l, dehnHadwiger (q l) := by
  have h1 : ∀ k, dehnHadwiger (p k) = ∑ l, dehnHadwiger (p k ∩ q l) := by
    intro k
    apply dehnHadwiger_dissection (hp k) (fun l => (hp k).inter (hq l))
    · rw [← inter_iUnion, ← hU]; exact inter_eq_left.2 (subset_iUnion p k)
    · intro i j hij
      exact (hdq hij).mono (interior_mono inter_subset_right) (interior_mono inter_subset_right)
  have h2 : ∀ l, dehnHadwiger (q l) = ∑ k, dehnHadwiger (p k ∩ q l) := by
    intro l
    apply dehnHadwiger_dissection (hq l) (fun k => (hp k).inter (hq l))
    · rw [← iUnion_inter, hU]; exact inter_eq_right.2 (subset_iUnion q l)
    · intro i j hij
      exact (hdp hij).mono (interior_mono inter_subset_left) (interior_mono inter_subset_left)
  rw [Finset.sum_congr rfl (fun k _ => h1 k), Finset.sum_congr rfl (fun l _ => h2 l)]
  exact Finset.sum_comm

/-- **The bridge for finite unions of convex polytopes.** Let the set `⋃ k, p k` be cut into the convex pieces
`p k`, and let the moved pieces `g k '' p k` fill a second set. Then every dissection `p₁` of the first set
into convex polytopes and every dissection `p₂` of the second have the same total invariant. -/
theorem dehnHadwigerSum_eq_of_scissors {κ κ₁ κ₂ : Type} [Fintype κ] [Fintype κ₁] [Fintype κ₂]
    {p : κ → Set E} {g : κ → E ≃ᵃⁱ[ℝ] E} {p₁ : κ₁ → Set E} {p₂ : κ₂ → Set E}
    (hp : ∀ k, IsPoly (p k))
    (hdp : Pairwise fun i j => Disjoint (interior (p i)) (interior (p j)))
    (hdg : Pairwise fun i j => Disjoint (interior (g i '' p i)) (interior (g j '' p j)))
    (hp₁ : ∀ k, IsPoly (p₁ k))
    (hd₁ : Pairwise fun i j => Disjoint (interior (p₁ i)) (interior (p₁ j)))
    (hU₁ : (⋃ k, p₁ k) = ⋃ k, p k)
    (hp₂ : ∀ k, IsPoly (p₂ k))
    (hd₂ : Pairwise fun i j => Disjoint (interior (p₂ i)) (interior (p₂ j)))
    (hU₂ : (⋃ k, p₂ k) = ⋃ k, g k '' p k) :
    ∑ k, dehnHadwiger (p₁ k) = ∑ k, dehnHadwiger (p₂ k) := by
  rw [dehnHadwigerSum_eq_of_same_union hp₁ hp hd₁ hdp hU₁,
    dehnHadwigerSum_eq_of_same_union hp₂ (fun k => (hp k).image (g k)) hd₂ hdg hU₂]
  exact Finset.sum_congr rfl fun k _ => (dehnHadwiger_image (g k) (p k)).symm

end DehnHadwiger
