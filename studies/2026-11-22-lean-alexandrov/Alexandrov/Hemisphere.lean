/-
Alexandrov's theorem on prescribed curvature, polyhedral case: the textbook form of the necessity.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Necessity

/-!
# Spherically convex sets lie in a closed hemisphere (M6b)

* `exists_halfspace_of_convex`: a convex set `K ≠ E3` that is closed under positive scaling lies in a
  closed half-space through the origin (finite-dimensional separation; a convex set with empty interior
  lies in a proper affine subspace).
* `curvature_lt_of_sphericallyConvex`: **necessity of Alexandrov's condition, textbook form.** For a
  nonempty `ω` on the unit sphere whose cone `{t • v | t > 0, v ∈ ω}` is convex (`ω` spherically convex;
  such an `ω` is never the whole sphere), `Σ_{n i ∈ ω} κ i < area (ω^{π/2})`, with `ω^{π/2}` the open
  `π/2`-neighbourhood of `ω`.
-/

open MeasureTheory Set Metric Finset
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

theorem exists_halfspace_of_convex {K : Set E3} (hK : Convex ℝ K)
    (hcone : ∀ x ∈ K, ∀ t : ℝ, 0 < t → t • x ∈ K) (hne : K.Nonempty) (htop : K ≠ univ) :
    ∃ u : E3, u ≠ 0 ∧ ∀ v ∈ K, ⟪v, u⟫ ≤ 0 := by
  have hcl : closure K ≠ univ := by
    intro h
    by_cases hint : (interior K).Nonempty
    · have := hK.interior_closure_eq_interior_of_nonempty_interior hint
      rw [h, interior_univ] at this
      exact htop (eq_univ_of_univ_subset (this ▸ interior_subset))
    · have hspan : affineSpan ℝ K ≠ ⊤ := fun h' =>
        hint (hK.interior_nonempty_iff_affineSpan_eq_top.2 h')
      have hcl' : closure K ⊆ affineSpan ℝ K :=
        closure_minimal (subset_affineSpan ℝ K) (AffineSubspace.closed_of_finiteDimensional _)
      rw [h] at hcl'
      exact hspan (AffineSubspace.coe_eq_univ_iff _ |>.1 (eq_univ_of_univ_subset hcl'))
  obtain ⟨p, hp⟩ := (Set.ne_univ_iff_exists_notMem _).1 hcl
  obtain ⟨f, c, hfc, hcp⟩ := geometric_hahn_banach_closed_point hK.closure isClosed_closure hp
  have hf0 : ∀ v ∈ K, f v ≤ 0 := by
    intro v hv
    by_contra hpos
    push Not at hpos
    set t := (|c| + 1) / f v with ht
    have htpos : 0 < t := div_pos (by positivity) hpos
    have := hfc _ (subset_closure (hcone v hv t htpos))
    rw [map_smul, smul_eq_mul, ht, div_mul_cancel₀ _ hpos.ne'] at this
    linarith [le_abs_self c]
  set w := (InnerProductSpace.toDual ℝ E3).symm f with hw
  have hwf : ∀ v, ⟪v, w⟫ = f v := fun v => by
    rw [real_inner_comm, hw, InnerProductSpace.toDual_symm_apply]
  refine ⟨w, fun h0 => ?_, fun v hv => (hwf v).trans_le (hf0 v hv)⟩
  obtain ⟨a, ha⟩ := hne
  have h1 := hfc a (subset_closure ha)
  rw [← hwf, h0, inner_zero_right] at h1 hcp
  linarith

/-- **Necessity of Alexandrov's condition, textbook form.** -/
theorem curvature_lt_of_sphericallyConvex {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) (ω : Set E3) (hω : ω ⊆ sphere (0 : E3) 1)
    (hωne : ω.Nonempty) (hconv : Convex ℝ {x : E3 | ∃ t : ℝ, 0 < t ∧ ∃ v ∈ ω, x = t • v}) :
    haveI := Classical.decPred (fun i => n i ∈ ω)
    ∑ i ∈ univ.filter (fun i => n i ∈ ω), curvature (rayPolytope n r) (corner n r i) <
      3 * volume ({x : E3 | ∃ v ∈ ω, 0 < ⟪v, x⟫} ∩ ball (0 : E3) 1) := by
  classical
  set K := {x : E3 | ∃ t : ℝ, 0 < t ∧ ∃ v ∈ ω, x = t • v} with hKdef
  have hωK : ω ⊆ K := fun v hv => ⟨1, one_pos, v, hv, (one_smul ℝ v).symm⟩
  have hcone : ∀ x ∈ K, ∀ t : ℝ, 0 < t → t • x ∈ K := by
    rintro x ⟨s, hs, v, hv, rfl⟩ t ht
    exact ⟨t * s, mul_pos ht hs, v, hv, by rw [smul_smul]⟩
  have h0 : (0 : E3) ∉ K := by
    rintro ⟨t, ht, v, hv, h⟩
    have hv1 : ‖v‖ = 1 := mem_sphere_zero_iff_norm.1 (hω hv)
    have := congrArg norm h
    rw [norm_zero, norm_smul, hv1, mul_one, Real.norm_of_nonneg ht.le] at this
    linarith
  obtain ⟨u, hu0, hu⟩ := exists_halfspace_of_convex hconv hcone
    (hωne.mono hωK) (fun h => h0 (h ▸ mem_univ _))
  obtain ⟨v, hv⟩ := hωne
  have hv0 : v ≠ 0 := fun h => by
    have := mem_sphere_zero_iff_norm.1 (hω hv); rw [h, norm_zero] at this; norm_num at this
  convert curvature_lt_of_hemisphere hn hinj hspan hr ω ⟨v, hv, hv0⟩
    ⟨u, hu0, fun w hw => hu w (hωK hw)⟩

end Alexandrov
