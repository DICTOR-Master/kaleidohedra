/-
Dehn–Hadwiger study, part 4: reading the angle class from the facet normals (DICTO, 20 Nov 2026).

* `wedgeAngle_two_planes'`: the wedge between two half-spaces with independent normals has angle π minus the
  angle between the normals, in every finite dimension (the Canon's `wedgeAngle_two_planes` of study 3, whose
  proof only needs the 2-dimensional complement, here spanned by the two normals).
* `thetaH_cone_cases`: at a point of `sol a b` the angle class is 0 or π minus the angle between two tight
  normals `a p`, `a q` (any number of tight constraints; the Canon's `two_extreme` of study 4).
* `dehnHadwiger_sol_eq_zero_of_rational`: if any two normals make an angle in ℚπ, the invariant is zero.
* `dehnHadwiger_sol_eq_single`: if every two tight independent normals give the class `τ`, the invariant is
  (measure of the ridge points of class `τ`) ⊗ `τ`.
No `sorry`.
-/
import DehnHadwiger.DH3Bridge
import DehnCanon.Dehn4Rational

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E] {ι : Type}

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
lemma linCone_pair_eq (a₁ a₂ : E) :
    linCone ![a₁, a₂] Set.univ = (Submodule.span ℝ (Set.range ![a₁, a₂]))ᗮ := by
  set S : Submodule ℝ E := Submodule.span ℝ (Set.range ![a₁, a₂]) with hS
  ext v
  rw [mem_linCone_pair, Submodule.mem_orthogonal']
  constructor
  · rintro ⟨h1, h2⟩ u hu
    have hle : S ≤ (ℝ ∙ v)ᗮ := by
      rw [hS, Submodule.span_le]
      rintro _ ⟨i, rfl⟩
      refine Submodule.mem_orthogonal_singleton_iff_inner_right.2 ?_
      fin_cases i
      · simpa [real_inner_comm] using h1
      · simpa [real_inner_comm] using h2
    exact Submodule.mem_orthogonal_singleton_iff_inner_right.1 (hle hu)
  · intro hv
    have m1 : a₁ ∈ S := Submodule.subset_span ⟨0, rfl⟩
    have m2 : a₂ ∈ S := Submodule.subset_span ⟨1, rfl⟩
    exact ⟨by rw [real_inner_comm]; exact hv _ m1, by rw [real_inner_comm]; exact hv _ m2⟩

omit [MeasurableSpace E] [BorelSpace E] in
lemma finrank_orth_linCone_pair {a₁ a₂ : E} (h : LinearIndependent ℝ ![a₁, a₂]) :
    finrank ℝ (linCone ![a₁, a₂] Set.univ)ᗮ = 2 := by
  rw [linCone_pair_eq, Submodule.orthogonal_orthogonal, finrank_span_eq_card h]; simp

/-- Two half-spaces, unit normals: the wedge angle is π minus the angle between the normals. -/
theorem wedgeAngle_two_planes_unit' (u₁ u₂ : E) (hu₁ : ‖u₁‖ = 1) (hu₂ : ‖u₂‖ = 1)
    (h : LinearIndependent ℝ ![u₁, u₂]) :
    wedgeAngle (cone ![u₁, u₂] Set.univ) (linCone ![u₁, u₂] Set.univ) =
      Real.pi - InnerProductGeometry.angle u₁ u₂ := by
  have hpi := Real.pi_pos
  set K : Submodule ℝ E := linCone ![u₁, u₂] Set.univ with hKdef
  have hV : finrank ℝ Kᗮ = 2 := finrank_orth_linCone_pair h
  have hpair := LinearIndependent.pair_iff.1 h
  -- inner products of the unit normals
  set g : ℝ := ⟪u₁, u₂⟫ with hg
  have i11 : ⟪u₁, u₁⟫ = 1 := by rw [real_inner_self_eq_norm_sq, hu₁]; norm_num
  have i22 : ⟪u₂, u₂⟫ = 1 := by rw [real_inner_self_eq_norm_sq, hu₂]; norm_num
  have i21 : ⟪u₂, u₁⟫ = g := real_inner_comm _ _
  -- the bisector and the difference
  set d₁ : E := u₁ + u₂ with hd₁
  set d₂ : E := u₁ - u₂ with hd₂
  have hd₁0 : d₁ ≠ 0 := by
    intro h0
    have := hpair 1 1 (by rw [one_smul, one_smul]; exact h0)
    exact one_ne_zero this.1
  have hd₂0 : d₂ ≠ 0 := by
    intro h0
    have := hpair 1 (-1) (by rw [one_smul, neg_one_smul, ← sub_eq_add_neg]; exact h0)
    exact one_ne_zero this.1
  set m : ℝ := ‖d₁‖ with hm
  set n : ℝ := ‖d₂‖ with hn
  have hm0 : 0 < m := norm_pos_iff.2 hd₁0
  have hn0 : 0 < n := norm_pos_iff.2 hd₂0
  have j11 : ⟪d₁, d₁⟫ = 2 + 2 * g := by
    rw [hd₁, inner_add_left, inner_add_right, inner_add_right, i11, i22, i21]; ring
  have j22 : ⟪d₂, d₂⟫ = 2 - 2 * g := by
    rw [hd₂, inner_sub_left, inner_sub_right, inner_sub_right, i11, i22, i21]; ring
  have j12 : ⟪d₁, d₂⟫ = 0 := by
    rw [hd₁, hd₂, inner_add_left, inner_sub_right, inner_sub_right, i11, i22, i21]; ring
  have hm2 : m ^ 2 = 2 + 2 * g := by rw [hm, ← real_inner_self_eq_norm_sq, j11]
  have hn2 : n ^ 2 = 2 - 2 * g := by rw [hn, ← real_inner_self_eq_norm_sq, j22]
  have k11 : ⟪u₁, d₁⟫ = m ^ 2 / 2 := by rw [hd₁, inner_add_right, i11, hm2]; ring
  have k12 : ⟪u₁, d₂⟫ = n ^ 2 / 2 := by rw [hd₂, inner_sub_right, i11, hn2]; ring
  have k21 : ⟪u₂, d₁⟫ = m ^ 2 / 2 := by rw [hd₁, inner_add_right, i22, i21, hm2]; ring
  have k22 : ⟪u₂, d₂⟫ = -(n ^ 2 / 2) := by rw [hd₂, inner_sub_right, i22, i21, hn2]; ring
  -- the orthonormal pair in the plane perpendicular to the edge
  have hu₁K : u₁ ∈ Kᗮ := by
    rw [Submodule.mem_orthogonal']; intro u hu; exact (mem_linCone_pair.1 hu).1
  have hu₂K : u₂ ∈ Kᗮ := by
    rw [Submodule.mem_orthogonal']; intro u hu; exact (mem_linCone_pair.1 hu).2
  set e₁ : E := (-m⁻¹) • d₁ with he₁
  set e₂ : E := n⁻¹ • d₂ with he₂
  have he₁K : e₁ ∈ Kᗮ := Kᗮ.smul_mem _ (Kᗮ.add_mem hu₁K hu₂K)
  have he₂K : e₂ ∈ Kᗮ := Kᗮ.smul_mem _ (Kᗮ.sub_mem hu₁K hu₂K)
  have o11 : ⟪e₁, e₁⟫ = 1 := by
    rw [he₁, inner_smul_left, inner_smul_right, j11, ← hm2]; simp only [conj_trivial]; field_simp
  have o22 : ⟪e₂, e₂⟫ = 1 := by
    rw [he₂, inner_smul_left, inner_smul_right, j22, ← hn2]; simp only [conj_trivial]; field_simp
  have o12 : ⟪e₁, e₂⟫ = 0 := by
    rw [he₁, he₂, inner_smul_left, inner_smul_right, j12]; simp
  let w : Fin 2 → Kᗮ := ![⟨e₁, he₁K⟩, ⟨e₂, he₂K⟩]
  have hw : Orthonormal ℝ w := by
    rw [orthonormal_iff_ite]
    intro i j
    fin_cases i <;> fin_cases j
    · exact o11
    · exact o12
    · show ⟪e₂, e₁⟫ = 0
      rw [real_inner_comm]; exact o12
    · exact o22
  let B : OrthonormalBasis (Fin 2) ℝ Kᗮ :=
    (basisOfOrthonormalOfCardEqFinrank hw (by rw [hV]; simp)).toOrthonormalBasis
      (by rw [coe_basisOfOrthonormalOfCardEqFinrank]; exact hw)
  have hB : ∀ i, B i = w i := by
    intro i
    show ((basisOfOrthonormalOfCardEqFinrank hw _).toOrthonormalBasis _) i = w i
    rw [Basis.coe_toOrthonormalBasis, coe_basisOfOrthonormalOfCardEqFinrank]
  let ψ : ℂ ≃ₗᵢ[ℝ] Kᗮ := Complex.isometryOfOrthonormal B
  have hψ : ∀ z : ℂ, ((ψ z : Kᗮ) : E) = z.re • e₁ + z.im • e₂ := by
    intro z
    show ((Complex.isometryOfOrthonormal B z : Kᗮ) : E) = _
    rw [Complex.isometryOfOrthonormal_apply, hB, hB]
    rfl
  -- the angle β
  have hmn : m ^ 2 + n ^ 2 = 4 := by rw [hm2, hn2]; ring
  have hm_lt : m / 2 < 1 := by nlinarith
  set β : ℝ := Real.arcsin (m / 2) with hβdef
  have hβ0 : 0 < β := Real.arcsin_pos.2 (by positivity)
  have hβ1 : β < Real.pi / 2 := Real.arcsin_lt_pi_div_two.2 hm_lt
  have hsin : Real.sin β = m / 2 := Real.sin_arcsin (by linarith) hm_lt.le
  have hcos : Real.cos β = n / 2 := by
    have hc0 : 0 ≤ Real.cos β := Real.cos_arcsin_nonneg _
    have hsq : Real.cos β ^ 2 = (n / 2) ^ 2 := by
      have := Real.sin_sq_add_cos_sq β
      rw [hsin] at this; nlinarith
    exact (sq_eq_sq₀ hc0 (by positivity)).1 hsq
  -- the wedge is carried to the sector
  have a1 : ∀ z : ℂ, ⟪u₁, z.re • e₁ + z.im • e₂⟫ = -(Real.sin β) * z.re + Real.cos β * z.im := by
    intro z
    rw [inner_add_right, he₁, he₂]
    simp only [inner_smul_right]
    rw [k11, k12, hsin, hcos]
    field_simp
  have a2 : ∀ z : ℂ, ⟪u₂, z.re • e₁ + z.im • e₂⟫ = -(Real.sin β) * z.re - Real.cos β * z.im := by
    intro z
    rw [inner_add_right, he₁, he₂]
    simp only [inner_smul_right]
    rw [k21, k22, hsin, hcos]
    field_simp
    ring
  let me : ℂ ≃ᵐ Kᗮ := ψ.toHomeomorph.toMeasurableEquiv
  have hmp : MeasurePreserving me volume volume := ψ.measurePreserving
  have hpre : me ⁻¹' wedgeSet (cone ![u₁, u₂] Set.univ) K = sector β := by
    ext z
    show ((ψ z : Kᗮ) : E) ∈ cone ![u₁, u₂] Set.univ ∧ ‖ψ z‖ < 1 ↔ z ∈ sector β
    rw [hψ, mem_cone_pair, a1, a2, ψ.norm_map]
    rfl
  have hball : me ⁻¹' Metric.ball (0 : Kᗮ) 1 = Metric.ball (0 : ℂ) 1 := by
    ext z
    show ψ z ∈ Metric.ball (0 : Kᗮ) 1 ↔ z ∈ Metric.ball (0 : ℂ) 1
    rw [Metric.mem_ball, Metric.mem_ball, dist_zero_right, dist_zero_right, ψ.norm_map]
  have hvol1 : volume (wedgeSet (cone ![u₁, u₂] Set.univ) K) = ENNReal.ofReal β := by
    rw [← hmp.measure_preimage_equiv, hpre, volume_sector hβ0 hβ1]
  have hvol2 : (volume (Metric.ball (0 : Kᗮ) 1)).toReal = Real.pi := by
    rw [← hmp.measure_preimage_equiv, hball, Complex.volume_ball]
    simp
  -- the angle between the normals
  have hang : InnerProductGeometry.angle u₁ u₂ = Real.pi - 2 * β := by
    unfold InnerProductGeometry.angle
    rw [hu₁, hu₂, mul_one, div_one, ← hg]
    have hgc : g = Real.cos (Real.pi - 2 * β) := by
      rw [Real.cos_pi_sub, Real.cos_two_mul, hcos]
      linarith [hn2]
    rw [hgc, Real.arccos_cos (by linarith) (by linarith)]
  unfold wedgeAngle
  rw [hvol1, hvol2, hang, ENNReal.toReal_ofReal hβ0.le]
  field_simp
  ring


/-- Two half-spaces with independent normals: the wedge angle is π minus the angle between the normals. -/
theorem wedgeAngle_two_planes' (a₁ a₂ : E) (h : LinearIndependent ℝ ![a₁, a₂]) :
    wedgeAngle (cone ![a₁, a₂] Set.univ) (linCone ![a₁, a₂] Set.univ) =
      Real.pi - InnerProductGeometry.angle a₁ a₂ := by
  have hpair := LinearIndependent.pair_iff.1 h
  have ha₁ : a₁ ≠ 0 := by
    intro h0
    have := hpair 1 0 (by rw [h0, smul_zero, zero_smul, add_zero])
    exact one_ne_zero this.1
  have ha₂ : a₂ ≠ 0 := by
    intro h0
    have := hpair 0 1 (by rw [h0, smul_zero, zero_smul, add_zero])
    exact one_ne_zero this.2
  have n₁ : 0 < ‖a₁‖ := norm_pos_iff.2 ha₁
  have n₂ : 0 < ‖a₂‖ := norm_pos_iff.2 ha₂
  have c₁ : 0 < ‖a₁‖⁻¹ := inv_pos.2 n₁
  have c₂ : 0 < ‖a₂‖⁻¹ := inv_pos.2 n₂
  have hu : LinearIndependent ℝ ![‖a₁‖⁻¹ • a₁, ‖a₂‖⁻¹ • a₂] := by
    rw [LinearIndependent.pair_iff]
    intro s t hst
    rw [smul_smul, smul_smul] at hst
    have := hpair _ _ hst
    exact ⟨(mul_eq_zero.1 this.1).resolve_right c₁.ne', (mul_eq_zero.1 this.2).resolve_right c₂.ne'⟩
  have key := wedgeAngle_two_planes_unit' (‖a₁‖⁻¹ • a₁) (‖a₂‖⁻¹ • a₂)
    (by rw [norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ n₁.ne'])
    (by rw [norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ n₂.ne']) hu
  rw [cone_pair_smul c₁ c₂, linCone_pair_smul c₁ c₂,
    InnerProductGeometry.angle_smul_left_of_pos _ _ c₁,
    InnerProductGeometry.angle_smul_right_of_pos _ _ c₂] at key
  exact key


/-- **The angle class where exactly two facets meet**: π minus the angle between the two normals. -/
theorem thetaH_pair (a : ι → E) {A : Set ι} {i j : ι} (hA : A = {i, j})
    (h : LinearIndependent ℝ ![a i, a j]) :
    thetaH (cone a A) =
      Submodule.Quotient.mk (Real.pi - InnerProductGeometry.angle (a i) (a j)) := by
  have hc : cone a A = cone ![a i, a j] Set.univ := by
    ext v; rw [mem_cone_pair, hA]; simp [cone]
  have hl : linCone a A = linCone ![a i, a j] Set.univ := by
    ext v; rw [mem_linCone_pair, mem_linCone, hA]; simp
  have hf : finrank ℝ (linCone ![a i, a j] Set.univ) + 2 = finrank ℝ E := by
    have := Submodule.finrank_add_finrank_orthogonal (linCone ![a i, a j] Set.univ)
    rw [finrank_orth_linCone_pair h] at this; omega
  unfold thetaH
  rw [linSpace_cone, hl]
  simp only [hf, ↓reduceIte]
  rw [hc, wedgeAngle_two_planes' _ _ h]

omit [MeasurableSpace E] [BorelSpace E] in
/-- A direction space that contains a hyperplane does not have codimension 2. -/
lemma finrank_linCone_ne_of_perp (a : ι → E) {A : Set ι} {u : E}
    (hle : (ℝ ∙ u)ᗮ ≤ linCone a A) : finrank ℝ (linCone a A) + 2 ≠ finrank ℝ E := by
  have h1 := Submodule.finrank_add_finrank_orthogonal (ℝ ∙ u)
  have h2 : finrank ℝ (ℝ ∙ u) ≤ 1 := (finrank_span_le_card ({u} : Set E)).trans (by simp)
  have h3 := Submodule.finrank_mono hle
  omega

/-- **The angle class of a cone of constraints**: 0, or π minus the angle between two of its normals
(independent), whatever the number of constraints. -/
theorem thetaH_cone_cases [Finite ι] (a : ι → E) (A : Set ι) (hne : ∀ i, a i ≠ 0) :
    thetaH (cone a A) = 0 ∨ ∃ p ∈ A, ∃ q ∈ A, LinearIndependent ℝ ![a p, a q] ∧
      thetaH (cone a A) = Submodule.Quotient.mk (Real.pi - InnerProductGeometry.angle (a p) (a q)) := by
  classical
  by_cases hfin : finrank ℝ (linCone a A) + 2 = finrank ℝ E
  swap
  · left; unfold thetaH; rw [linSpace_cone, ite_eq_right hfin]
  have hW : finrank ℝ (linCone a A)ᗮ = 2 := by
    have := Submodule.finrank_add_finrank_orthogonal (linCone a A)
    omega
  have hmem : ∀ i ∈ A, a i ∈ (linCone a A)ᗮ := by
    intro i hi
    rw [Submodule.mem_orthogonal']
    intro u hu
    exact hu i hi
  by_cases hv0 : ∃ v0, ∀ i ∈ A, ⟪a i, v0⟫ < 0
  · obtain ⟨v0, hv0⟩ := hv0
    have hAne : A.Nonempty := by
      by_contra hno
      rw [Set.not_nonempty_iff_eq_empty] at hno
      have htop : linCone a A = ⊤ := by
        rw [eq_top_iff]; intro v _
        rw [mem_linCone, hno]; intro i hi; exact absurd hi (Set.notMem_empty i)
      rw [htop, finrank_top] at hfin
      omega
    have hAfin : A.Finite := Set.toFinite A
    obtain ⟨p, hp, q, hq, hpq⟩ := two_extreme hW a v0 hAfin.toFinset
      ((Set.Finite.toFinset_nonempty hAfin).2 hAne)
      (fun i hi => hmem i ((Set.Finite.mem_toFinset hAfin).1 hi))
      (fun i hi => hv0 i ((Set.Finite.mem_toFinset hAfin).1 hi))
    have hpA : p ∈ A := (Set.Finite.mem_toFinset hAfin).1 hp
    have hqA : q ∈ A := (Set.Finite.mem_toFinset hAfin).1 hq
    have hcone : cone a A = cone a {p, q} := by
      ext v; constructor
      · intro h i hi
        rcases hi with rfl | rfl
        · exact h _ hpA
        · exact h _ hqA
      · intro h i hi
        exact hpq v (h p (mem_insert _ _)) (h q (mem_insert_of_mem _ rfl)) i
          ((Set.Finite.mem_toFinset hAfin).2 hi)
    by_cases hli : LinearIndependent ℝ ![a p, a q]
    · right
      refine ⟨p, hpA, q, hqA, hli, ?_⟩
      rw [hcone]; exact thetaH_pair a rfl hli
    · left
      rw [hcone]
      rw [LinearIndependent.pair_iff' (hne p)] at hli
      push Not at hli
      obtain ⟨c, hc⟩ := hli
      have hle : (ℝ ∙ a p)ᗮ ≤ linCone a {p, q} := by
        intro v hv
        have h0 : ⟪a p, v⟫ = 0 := Submodule.mem_orthogonal_singleton_iff_inner_right.1 hv
        rw [mem_linCone]
        intro i hi
        rcases hi with rfl | rfl
        · exact h0
        · rw [← hc, inner_smul_left, h0, mul_zero]
      unfold thetaH
      rw [linSpace_cone, ite_eq_right (finrank_linCone_ne_of_perp a hle)]
  · left
    push Not at hv0
    unfold thetaH
    rw [linSpace_cone]
    simp only [hfin, ↓reduceIte]
    rw [Submodule.Quotient.mk_eq_zero]
    have hnull : volume (wedgeSet (cone a A) (linCone a A)) = 0 := by
      have hsub : wedgeSet (cone a A) (linCone a A) ⊆
          ⋃ i ∈ A, {w : (linCone a A)ᗮ | ⟪a i, (w : E)⟫ = 0} := by
        intro w hw
        obtain ⟨i, hi, h0⟩ := hv0 (w : E)
        exact mem_iUnion₂.2 ⟨i, hi, le_antisymm (hw.1 i hi) h0⟩
      apply measure_mono_null hsub
      rw [measure_biUnion_null_iff (Set.to_countable A)]
      intro i hi
      let N : Submodule ℝ (linCone a A)ᗮ := (ℝ ∙ (⟨a i, hmem i hi⟩ : (linCone a A)ᗮ))ᗮ
      have hN : N ≠ ⊤ := by
        intro h
        have h1 : (⟨a i, hmem i hi⟩ : (linCone a A)ᗮ) ∈ N := by rw [h]; trivial
        have h2 : ⟪(⟨a i, hmem i hi⟩ : (linCone a A)ᗮ), (⟨a i, hmem i hi⟩ : (linCone a A)ᗮ)⟫ = 0 :=
          Submodule.mem_orthogonal_singleton_iff_inner_right.1 h1
        have h3 : (⟨a i, hmem i hi⟩ : (linCone a A)ᗮ) = 0 := inner_self_eq_zero.1 h2
        exact hne i (congrArg Subtype.val h3)
      have hset : {w : (linCone a A)ᗮ | ⟪a i, (w : E)⟫ = 0} = (N : Set (linCone a A)ᗮ) := by
        ext w
        exact (Submodule.mem_orthogonal_singleton_iff_inner_right
          (u := (⟨a i, hmem i hi⟩ : (linCone a A)ᗮ)) (v := w)).symm
      rw [hset]
      exact Measure.addHaar_submodule volume N hN
    unfold wedgeAngle
    rw [hnull]
    simp

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
/-- If the angle class takes only one value `τ` besides 0, the invariant is (measure where it is `τ`) ⊗ `τ`. -/
lemma dehnHadwiger_eq_single [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] (P : Set E)
    (τ : Angle) (h : ∀ x, ridgeAngle P x = τ ∨ ridgeAngle P x = 0) :
    dehnHadwiger P = (μH[(finrank ℝ E - 2 : ℕ)] {x | ridgeAngle P x = τ}).toReal ⊗ₜ[ℚ] τ := by
  unfold dehnHadwiger
  apply finsum_eq_single _ τ
  intro θ hθ
  by_cases h0 : θ = 0
  · rw [h0, TensorProduct.tmul_zero]
  · have he : {x | ridgeAngle P x = θ} = ∅ := by
      rw [Set.eq_empty_iff_forall_notMem]
      intro x hx
      have hx' : ridgeAngle P x = θ := hx
      rcases h x with h1 | h1
      · exact hθ (hx'.symm.trans h1)
      · exact h0 (hx'.symm.trans h1)
    rw [he, measure_empty, ENNReal.toReal_zero, TensorProduct.zero_tmul]

/-- **Every tight pair gives the class `τ`**: then the invariant is (measure of the class-`τ` points) ⊗ `τ`. -/
theorem dehnHadwiger_sol_eq_single [Finite ι] (a : ι → E) (b : ι → ℝ) (hne : ∀ i, a i ≠ 0) (τ : Angle)
    (hpair : ∀ x ∈ sol a b, ∀ p ∈ act a b x, ∀ q ∈ act a b x, LinearIndependent ℝ ![a p, a q] →
      (Submodule.Quotient.mk (Real.pi - InnerProductGeometry.angle (a p) (a q)) : Angle) = τ) :
    dehnHadwiger (sol a b) =
      (μH[(finrank ℝ E - 2 : ℕ)] {x | ridgeAngle (sol a b) x = τ}).toReal ⊗ₜ[ℚ] τ := by
  apply dehnHadwiger_eq_single
  intro x
  by_cases hx : x ∈ sol a b
  · rw [ridgeAngle_sol a b hx]
    rcases thetaH_cone_cases a (act a b x) hne with h0 | ⟨p, hp, q, hq, hli, he⟩
    · right; exact h0
    · left; rw [he]; exact hpair x hx p hp q hq hli
  · right; exact ridgeAngle_of_notMem hx

/-- **Rational normals, zero invariant**, in every dimension: a solid cut out by finitely many half-spaces
whose normals make, two by two, angles in ℚπ has Dehn–Hadwiger invariant zero, for all offsets `b`. -/
theorem dehnHadwiger_sol_eq_zero_of_rational [Finite ι] (a : ι → E) (b : ι → ℝ) (hne : ∀ i, a i ≠ 0)
    (hang : ∀ i j, InnerProductGeometry.angle (a i) (a j) ∈ ratPi) : dehnHadwiger (sol a b) = 0 := by
  rw [dehnHadwiger_sol_eq_single a b hne 0, TensorProduct.tmul_zero]
  intro x _ p _ q _ _
  rw [Submodule.Quotient.mk_eq_zero]
  exact ratPi.sub_mem pi_mem_ratPi (hang p q)

end DehnHadwiger
