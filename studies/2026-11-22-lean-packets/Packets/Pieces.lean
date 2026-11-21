/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Part 6: angles of copies and of
solids given by their faces.

* `edgeAngle_image`, `edgeAngle_smul`, `SimilarCopy.edgeAngle_iff`: the dihedral angles of a solid, read from
  the set, do not change under rigid motions (rotations, reflections, translations) and positive scalings
  (from the Dehn Canon's `tcone_image`, `linSpace_image`, `wedgeAngleIn_image`, `tcone_smul_set`).
* `edgeAngle_edgeData`: for a solid `sol n b` with interior points and edge data (`IsEdgeData`, Dehn Canon
  study 5), the dihedral angles read from the set are exactly the values `π − ∠(n i, n j)` over the edges, `i`, `j`
  the two faces of the edge (from the Canon's `faceSet_edge`, `faceSet_subset_corners`, `exists_pair_cone`,
  `wedgeAngle_two_planes`).
* `pi_sub_angle_eq`, `cos_eq_neg_of_sq`: evaluating `π − ∠(u, v)` from Gram values.
No `sorry`.
-/
module

public import Packets.Lemma2

@[expose] public section

open Set MeasureTheory Module Filter Topology
open scoped RealInnerProductSpace Pointwise

namespace Packets

open DehnCanon.Library (tcone linSpace wedgeSet wedgeAngle sol act cone linCone faceSet IsEdgeData)

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

lemma edgeAngle_linear_image (L : E ≃ₗᵢ[ℝ] E) (T : Set E) :
    finrank ℝ (linSpace (L '' T)) = finrank ℝ (linSpace T) ∧
      wedgeAngle (L '' T) (linSpace (L '' T)) = wedgeAngle T (linSpace T) := by
  rw [DehnCanon.Library.linSpace_image]
  refine ⟨LinearEquiv.finrank_map_eq _ _, ?_⟩
  rw [DehnCanon.Library.wedgeAngle_eq_in, DehnCanon.Library.wedgeAngle_eq_in,
    ← Submodule.map_orthogonal_equiv, DehnCanon.Library.wedgeAngleIn_image]

/-- Rigid motions (reflections allowed) keep the dihedral angles. -/
theorem edgeAngle_image (g : E ≃ᵃⁱ[ℝ] E) (P : Set E) (θ : ℝ) : EdgeAngle (g '' P) θ ↔ EdgeAngle P θ := by
  constructor
  · rintro ⟨_, ⟨x, hx, rfl⟩, h1, h2⟩
    rw [DehnCanon.Library.tcone_image] at h1 h2
    obtain ⟨e1, e2⟩ := edgeAngle_linear_image g.linearIsometryEquiv (tcone P x)
    exact ⟨x, hx, e1.symm.trans h1, e2.symm.trans h2⟩
  · rintro ⟨x, hx, h1, h2⟩
    obtain ⟨e1, e2⟩ := edgeAngle_linear_image g.linearIsometryEquiv (tcone P x)
    refine ⟨g x, mem_image_of_mem g hx, ?_, ?_⟩ <;> rw [DehnCanon.Library.tcone_image]
    · exact e1.trans h1
    · exact e2.trans h2

/-- Positive scalings keep the dihedral angles. -/
theorem edgeAngle_smul {c : ℝ} (hc : 0 < c) (P : Set E) (θ : ℝ) : EdgeAngle (c • P) θ ↔ EdgeAngle P θ := by
  constructor
  · rintro ⟨_, ⟨x, hx, rfl⟩, h1, h2⟩
    rw [DehnCanon.Library.tcone_smul_set hc] at h1 h2
    exact ⟨x, hx, h1, h2⟩
  · rintro ⟨x, hx, h1, h2⟩
    refine ⟨c • x, Set.smul_mem_smul_set hx, ?_, ?_⟩ <;> rw [DehnCanon.Library.tcone_smul_set hc]
    · exact h1
    · exact h2

/-- `Q` is a similar copy of `S`: the image of a positive scaling of `S` under a rigid motion (reflections
allowed). -/
def SimilarCopy (Q S : Set E) : Prop := ∃ (g : E ≃ᵃⁱ[ℝ] E) (c : ℝ), 0 < c ∧ Q = g '' (c • S)

theorem SimilarCopy.edgeAngle_iff {Q S : Set E} (h : SimilarCopy Q S) (θ : ℝ) :
    EdgeAngle Q θ ↔ EdgeAngle S θ := by
  obtain ⟨g, c, hc, rfl⟩ := h
  rw [edgeAngle_image, edgeAngle_smul hc]

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
lemma linIndep_of_gram {u v : E} (h : ⟪u, v⟫ ^ 2 < ⟪u, u⟫ * ⟪v, v⟫) : LinearIndependent ℝ ![u, v] := by
  rw [LinearIndependent.pair_iff]
  intro s t hst
  have h1 : s * ⟪u, u⟫ + t * ⟪u, v⟫ = 0 := by
    have := congrArg (fun w => ⟪u, w⟫) hst
    simpa [inner_add_right, real_inner_smul_right] using this
  have h2 : s * ⟪u, v⟫ + t * ⟪v, v⟫ = 0 := by
    have := congrArg (fun w => ⟪v, w⟫) hst
    simp only [inner_add_right, real_inner_smul_right, inner_zero_right] at this
    rw [real_inner_comm u v] at this; exact this
  have hdet : ⟪u, u⟫ * ⟪v, v⟫ - ⟪u, v⟫ ^ 2 ≠ 0 := by linarith
  have hs : s * (⟪u, u⟫ * ⟪v, v⟫ - ⟪u, v⟫ ^ 2) = 0 := by linear_combination ⟪v, v⟫ * h1 - ⟪u, v⟫ * h2
  have ht : t * (⟪u, u⟫ * ⟪v, v⟫ - ⟪u, v⟫ ^ 2) = 0 := by linear_combination ⟪u, u⟫ * h2 - ⟪u, v⟫ * h1
  exact ⟨(mul_eq_zero.1 hs).resolve_right hdet, (mul_eq_zero.1 ht).resolve_right hdet⟩

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
lemma cone_pair {ι : Type} (n : ι → E) (p q : ι) : cone n {p, q} = cone ![n p, n q] Set.univ := by
  ext v; simp [DehnCanon.Library.cone]

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
lemma linCone_pair {ι : Type} (n : ι → E) (p q : ι) : linCone n {p, q} = linCone ![n p, n q] Set.univ := by
  ext v; simp [DehnCanon.Library.mem_linCone]

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
/-- Evaluating `π − ∠(u, v)` from the Gram values of `u`, `v`. -/
lemma pi_sub_angle_eq {u v : E} {g X Y θ : ℝ} (hg : ⟪u, v⟫ = g) (hX : ⟪u, u⟫ = X) (hY : ⟪v, v⟫ = Y)
    (h0 : 0 ≤ θ) (hπ : θ ≤ Real.pi) (hc : Real.cos θ = -(g / (√X * √Y))) :
    Real.pi - InnerProductGeometry.angle u v = θ := by
  have hu : ‖u‖ = √X := by rw [← hX, real_inner_self_eq_norm_sq, Real.sqrt_sq (norm_nonneg _)]
  have hv : ‖v‖ = √Y := by rw [← hY, real_inner_self_eq_norm_sq, Real.sqrt_sq (norm_nonneg _)]
  rw [InnerProductGeometry.angle, hg, hu, hv, ← Real.arccos_neg, ← hc, Real.arccos_cos h0 hπ]

lemma cos_eq_neg_of_sq {x c : ℝ} (hsign : x * c ≤ 0) (h : x ^ 2 = c ^ 2) : x = -c := by
  have h' : (x + c) * (x - c) = 0 := by linear_combination h
  rcases mul_eq_zero.1 h' with h1 | h1
  · linarith
  · have hx : x = c := by linarith
    rw [hx] at hsign ⊢
    nlinarith [sq_nonneg c]

variable [Fact (finrank ℝ E = 3)]

/-- **The dihedral angles of a solid with edge data**, read from the set, are the values `π − ∠(n i, n j)` over
its edges. -/
theorem edgeAngle_edgeData {ι κ ε : Type} [Fintype ι] [Nonempty ι] [Finite κ] {n : ι → E} {b : ι → ℝ}
    {p : κ → E} {fi fj : ε → ι} {vk vl : ε → κ} (h : IsEdgeData n b p fi fj vk vl)
    (hint : (interior (sol n b)).Nonempty) (hind : ∀ e, LinearIndependent ℝ ![n (fi e), n (fj e)])
    (θ : ℝ) :
    EdgeAngle (sol n b) θ ↔ ∃ e, θ = Real.pi - InnerProductGeometry.angle (n (fi e)) (n (fj e)) := by
  constructor
  · rintro ⟨x, hx, h1, rfl⟩
    rw [DehnCanon.Library.tcone_sol n b hx, DehnCanon.Library.linSpace_cone] at h1 ⊢
    have hfs : x ∈ faceSet n b (act n b x) := ⟨hx, rfl⟩
    obtain ⟨e, he⟩ : ∃ e, act n b x = {fi e, fj e} := by
      by_contra hno
      push Not at hno
      have hsub := h.faceSet_subset_corners h1 hno
      obtain ⟨d, hdA, hd0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot
        (show linCone n (act n b x) ≠ ⊥ from fun hb => by rw [hb, finrank_bot] at h1; exact zero_ne_one h1)
      obtain ⟨ε0, hε0, hsh⟩ := edge_shift hx hdA
      have hinj : Set.InjOn (fun s : ℝ => x + s • d) (Set.Ioo (-ε0) ε0) :=
        fun s _ t _ hst => smul_left_injective ℝ hd0 (add_left_cancel hst)
      have hinf := Set.Infinite.image hinj (Set.Ioo_infinite (by linarith : -ε0 < ε0))
      apply hinf ((Set.finite_range p).subset _)
      rintro _ ⟨s, hs, rfl⟩
      exact hsub ⟨(hsh s (abs_lt.2 hs)).1, (hsh s (abs_lt.2 hs)).2⟩
    obtain ⟨p', hp, q', hq, hpq, hcone⟩ := DehnCanon.Library.exists_pair_cone hint hfs h1
    have hlin : linCone n (act n b x) = linCone n {p', q'} := by
      rw [← DehnCanon.Library.linSpace_cone, hcone, DehnCanon.Library.linSpace_cone]
    rw [hcone, hlin, cone_pair, linCone_pair, DehnCanon.Library.wedgeAngle_two_planes _ _ hpq]
    have hne : p' ≠ q' := by
      rintro rfl
      have := LinearIndependent.pair_iff.1 hpq 1 (-1) (by simp)
      norm_num at this
    rw [he] at hp hq
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hp hq
    refine ⟨e, ?_⟩
    rcases hp with rfl | rfl <;> rcases hq with rfl | rfl
    · exact absurd rfl hne
    · rfl
    · rw [InnerProductGeometry.angle_comm]
    · exact absurd rfl hne
  · rintro ⟨e, rfl⟩
    have hmem : (1 / 2 : ℝ) • p (vk e) + (1 / 2 : ℝ) • p (vl e) ∈ faceSet n b {fi e, fj e} := by
      rw [h.faceSet_edge e]; exact ⟨1 / 2, 1 / 2, by norm_num, by norm_num, by norm_num, rfl⟩
    obtain ⟨hx, hact⟩ := hmem
    refine ⟨_, hx, ?_, ?_⟩
    · rw [DehnCanon.Library.tcone_sol n b hx, hact, DehnCanon.Library.linSpace_cone, linCone_pair]
      exact DehnCanon.Library.finrank_linCone_pair (hind e)
    · rw [DehnCanon.Library.tcone_sol n b hx, hact, DehnCanon.Library.linSpace_cone, cone_pair, linCone_pair]
      exact DehnCanon.Library.wedgeAngle_two_planes _ _ (hind e)

end Packets
