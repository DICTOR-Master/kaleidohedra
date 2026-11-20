module

public import GET.SphereData

@[expose] public section

/-!
# The frontier of GET B is homeomorphic to the sphere

`sphere_of_radial`: if a compact set `K` contains a point `c` not on its frontier, and two frontier points on the same
ray from `c` are equal, then radial projection from `c` is a homeomorphism from the frontier onto the unit sphere.
For GET B, `c` is the centre `c₀ = (0, φ, 1 + φ)`; the injectivity on rays comes from the face planes (one face) and
from the cone-separation certificates `SPB` (two faces).
-/

namespace GET

open ZPhi GrunbaumK10 Set MeasureTheory
open scoped Pointwise

/-! ## Radial projection -/

theorem sphere_of_radial {K : Set Space} (hK : IsCompact K) {c : Space} (hc : c ∈ K) (hcf : c ∉ frontier K)
    (hinj : ∀ z₁ ∈ frontier K, ∀ z₂ ∈ frontier K, ∀ l : ℝ, 0 < l → z₂ - c = l • (z₁ - c) → z₁ = z₂) :
    Nonempty (frontier K ≃ₜ Metric.sphere (0 : Space) 1) := by
  have hne : ∀ z : frontier K, (z : Space) - c ≠ 0 := by
    intro z h
    rw [sub_eq_zero] at h
    exact hcf (h ▸ z.2)
  have hnorm : ∀ z : frontier K, ‖(z : Space) - c‖ ≠ 0 := fun z => norm_ne_zero_iff.mpr (hne z)
  let f : frontier K → Metric.sphere (0 : Space) 1 := fun z =>
    ⟨‖(z : Space) - c‖⁻¹ • ((z : Space) - c), by
      rw [mem_sphere_zero_iff_norm, norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ (hnorm z)]⟩
  have hcont : Continuous f := by
    apply Continuous.subtype_mk
    exact (((continuous_subtype_val.sub continuous_const).norm).inv₀ hnorm).smul
      (continuous_subtype_val.sub continuous_const)
  have hinj' : Function.Injective f := by
    intro z₁ z₂ h
    have h' := congrArg Subtype.val h
    simp only [f] at h'
    apply Subtype.ext
    apply hinj z₁ z₁.2 z₂ z₂.2 (‖(z₂ : Space) - c‖ / ‖(z₁ : Space) - c‖)
    · exact div_pos (norm_pos_iff.mpr (hne z₂)) (norm_pos_iff.mpr (hne z₁))
    · have := congrArg (fun x => ‖(z₂ : Space) - c‖ • x) h'
      simp only [smul_smul, mul_inv_cancel₀ (hnorm z₂), one_smul] at this
      rw [div_eq_mul_inv]; exact this.symm
  have hsurj : Function.Surjective f := by
    intro θ
    have hθ : ‖(θ : Space)‖ = 1 := mem_sphere_zero_iff_norm.mp θ.2
    set T := {s : ℝ | 0 ≤ s ∧ c + s • (θ : Space) ∈ K}
    have hTc : IsClosed T :=
      isClosed_Ici.inter (hK.isClosed.preimage (continuous_const.add (continuous_id.smul continuous_const)))
    obtain ⟨R, hR⟩ := hK.isBounded.exists_norm_le
    have hbound : ∀ s ∈ T, s ≤ R + ‖c‖ := by
      intro s hs
      have h1 := hR _ hs.2
      have h2 : ‖s • (θ : Space)‖ = s := by rw [norm_smul, hθ, mul_one, Real.norm_of_nonneg hs.1]
      have h3 : ‖s • (θ : Space)‖ ≤ ‖c + s • (θ : Space)‖ + ‖c‖ := by
        calc ‖s • (θ : Space)‖ = ‖(c + s • (θ : Space)) - c‖ := by rw [add_sub_cancel_left]
          _ ≤ _ := norm_sub_le _ _
      linarith
    have hTb : BddAbove T := ⟨R + ‖c‖, hbound⟩
    have hT0 : (0 : ℝ) ∈ T := ⟨le_refl _, by simpa using hc⟩
    have hTcpt : IsCompact T := by
      apply Metric.isCompact_of_isClosed_isBounded hTc
      rw [Metric.isBounded_iff_subset_closedBall 0]
      refine ⟨R + ‖c‖, fun s hs => ?_⟩
      rw [Metric.mem_closedBall, dist_zero_right, Real.norm_of_nonneg hs.1]
      exact hbound s hs
    set s₀ := sSup T
    have hs₀ : s₀ ∈ T := hTcpt.sSup_mem ⟨0, hT0⟩
    have hy : c + s₀ • (θ : Space) ∈ frontier K := by
      rw [frontier, hK.isClosed.closure_eq]
      refine ⟨hs₀.2, fun hint => ?_⟩
      obtain ⟨ε, hε, hball⟩ := Metric.isOpen_iff.mp isOpen_interior _ hint
      have hmem : s₀ + ε / 2 ∈ T := by
        refine ⟨by linarith [hs₀.1], interior_subset (hball ?_)⟩
        rw [Metric.mem_ball, dist_eq_norm, add_smul, ← add_assoc, add_sub_cancel_left, norm_smul, hθ, mul_one,
          Real.norm_of_nonneg (by linarith)]
        linarith
      have := le_csSup hTb hmem
      linarith
    have hpos : 0 < s₀ := by
      rcases lt_or_eq_of_le hs₀.1 with h | h
      · exact h
      · exfalso; apply hcf; rw [← h, zero_smul, add_zero] at hy; exact hy
    refine ⟨⟨_, hy⟩, Subtype.ext ?_⟩
    simp only [f, add_sub_cancel_left, norm_smul, hθ, mul_one, Real.norm_of_nonneg hpos.le, smul_smul,
      inv_mul_cancel₀ hpos.ne', one_smul]
  have : CompactSpace (frontier K) :=
    isCompact_iff_compactSpace.mp (hK.of_isClosed_subset isClosed_frontier
      (frontier_subset_closure.trans hK.isClosed.closure_eq.subset))
  exact ⟨hcont.homeoOfEquivCompactToT2 (f := Equiv.ofBijective f ⟨hinj', hsurj⟩)⟩

end GET
