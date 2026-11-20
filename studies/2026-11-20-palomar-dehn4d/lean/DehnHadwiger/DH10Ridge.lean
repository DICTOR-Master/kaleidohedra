/-
Dehn–Hadwiger study, part 10: tools for polytopes whose facets are not all pairwise adjacent (DICTO, 20 Nov 2026).

* `dehnHadwiger_sol_eq_single_ridge`: as part 4's `dehnHadwiger_sol_eq_single`, but the pair condition is only needed
  at ridge points: there every active normal lies in the plane of the two normals that give the angle.
* `eq_of_mem_span_pair`: three normals of the same length, all tight at one point and lying in one plane, are not
  three different vectors (a line meets a circle in at most two points).
* `facet_bary`: in four-space, a point of a facet whose four corners and four neighbouring facets are known is the
  barycentric combination of the corners, with weights read from the neighbouring facets.
No `sorry`.
-/
import DehnHadwiger.DH4Pair

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E] {ι : Type}

/-- **The pair condition at ridge points only.** If, at every point where two independent tight normals span all
the tight normals, the class `π − angle` of the two is `τ`, then the invariant is (measure of the class-`τ` points)
⊗ `τ`. -/
theorem dehnHadwiger_sol_eq_single_ridge [Finite ι] (a : ι → E) (b : ι → ℝ) (hne : ∀ i, a i ≠ 0) (τ : Angle)
    (hpair : ∀ x ∈ sol a b, ∀ p ∈ act a b x, ∀ q ∈ act a b x, LinearIndependent ℝ ![a p, a q] →
      (∀ r ∈ act a b x, a r ∈ Submodule.span ℝ (Set.range ![a p, a q])) →
      (Submodule.Quotient.mk (Real.pi - InnerProductGeometry.angle (a p) (a q)) : Angle) = τ) :
    dehnHadwiger (sol a b) =
      (μH[(finrank ℝ E - 2 : ℕ)] {x | ridgeAngle (sol a b) x = τ}).toReal ⊗ₜ[ℚ] τ := by
  apply dehnHadwiger_eq_single
  intro x
  by_cases hx : x ∈ sol a b
  · rw [ridgeAngle_sol a b hx]
    set A := act a b x
    by_cases hfin : finrank ℝ (linCone a A) + 2 = finrank ℝ E
    · rcases thetaH_cone_cases a A hne with h0 | ⟨p, hp, q, hq, hli, he⟩
      · right; exact h0
      · left
        rw [he]
        apply hpair x hx p hp q hq hli
        have hmem : ∀ i ∈ A, a i ∈ (linCone a A)ᗮ := by
          intro i hi
          rw [Submodule.mem_orthogonal']
          intro u hu
          exact hu i hi
        have hW : finrank ℝ (linCone a A)ᗮ = 2 := by
          have := Submodule.finrank_add_finrank_orthogonal (linCone a A)
          omega
        have hspan : Submodule.span ℝ (Set.range ![a p, a q]) = (linCone a A)ᗮ := by
          apply Submodule.eq_of_le_of_finrank_eq
          · rw [Submodule.span_le]
            rintro _ ⟨i, rfl⟩
            fin_cases i
            · exact hmem p hp
            · exact hmem q hq
          · rw [finrank_span_eq_card hli, hW]; simp
        intro r hr
        rw [hspan]
        exact hmem r hr
    · right; unfold thetaH; rw [linSpace_cone, ite_eq_right hfin]
  · right; exact ridgeAngle_of_notMem hx

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
/-- **Three tight normals of one length in one plane.** If `u`, `v` (independent) and `w` have the same length,
are all `1` at the point `x`, and `w` lies in the plane of `u` and `v`, then `w` is `u` or `v`. -/
lemma eq_of_mem_span_pair {u v w x : E} {N : ℝ} (hu : ⟪u, u⟫ = N) (hv : ⟪v, v⟫ = N) (hw : ⟪w, w⟫ = N)
    (hux : ⟪u, x⟫ = 1) (hvx : ⟪v, x⟫ = 1) (hwx : ⟪w, x⟫ = 1) (hli : LinearIndependent ℝ ![u, v])
    (hspan : w ∈ Submodule.span ℝ (Set.range ![u, v])) : w = u ∨ w = v := by
  obtain ⟨c, hc⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).1 hspan
  simp only [Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one] at hc
  set α := c 0
  set β := c 1
  have h1 : α + β = 1 := by
    rw [← hc, inner_add_left, inner_smul_left, inner_smul_left, hux, hvx] at hwx
    simpa using hwx
  have hd : ⟪u, v⟫ ≠ N := by
    intro h
    have : u - v = 0 := by
      rw [← inner_self_eq_zero (𝕜 := ℝ), inner_sub_left, inner_sub_right, inner_sub_right, hu, hv, h,
        real_inner_comm, h]
      ring
    have := LinearIndependent.pair_iff.1 hli 1 (-1) (by rw [sub_eq_zero] at this; rw [this]; simp)
    exact one_ne_zero this.1
  have h2 : α * β * (N - ⟪u, v⟫) = 0 := by
    have e := hw
    rw [← hc] at e
    simp only [inner_add_left, inner_add_right, inner_smul_left, inner_smul_right, hu, hv,
      real_inner_comm u v, RCLike.conj_to_real] at e
    have hb : β = 1 - α := by linarith
    rw [hb] at e ⊢
    linear_combination (-1 / 2 : ℝ) * e
  rcases mul_eq_zero.1 h2 with h | h
  · rcases mul_eq_zero.1 h with h | h
    · right; rw [← hc, h, zero_smul, zero_add, show β = 1 by linarith, one_smul]
    · left; rw [← hc, h, zero_smul, add_zero, show α = 1 by linarith, one_smul]
  · exact absurd (by linarith : ⟪u, v⟫ = N) hd

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
/-- Four vectors whose pairings with four others form the matrix `J − (1 − c) I` (`c ≠ 1`, `c ≠ −3`) are linearly
independent. -/
lemma linIndep_of_pairing {n v : Fin 4 → E} {c : ℝ} (hc1 : c ≠ 1) (hc3 : c ≠ -3)
    (hnv : ∀ i j, ⟪n i, v j⟫ = if i = j then c else 1) : LinearIndependent ℝ n := by
  rw [Fintype.linearIndependent_iff]
  intro β hβ k
  have key : ∀ j, (∑ i, β i) - (1 - c) * β j = 0 := by
    intro j
    have := congrArg (fun y => ⟪y, v j⟫) hβ
    simp only [sum_inner, inner_smul_left, hnv, inner_zero_left, RCLike.conj_to_real] at this
    rw [Fin.sum_univ_four] at this ⊢
    fin_cases j <;> simp at this ⊢ <;> linarith
  have hS : ∑ i, β i = 0 := by
    have k0 := key 0; have k1 := key 1; have k2 := key 2; have k3 := key 3
    rw [Fin.sum_univ_four] at k0 k1 k2 k3 ⊢
    have h4 : (3 + c) * (β 0 + β 1 + β 2 + β 3) = 0 := by linear_combination k0 + k1 + k2 + k3
    rcases mul_eq_zero.1 h4 with h | h
    · exact absurd (by linarith : c = -3) hc3
    · exact h
  have := key k
  rw [hS, zero_sub, neg_eq_zero] at this
  rcases mul_eq_zero.1 this with h | h
  · exact absurd (by linarith : c = 1) hc1
  · exact h

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
/-- In a four-dimensional space, a vector orthogonal to four independent vectors is zero. -/
lemma eq_zero_of_inner_four [FiniteDimensional ℝ E] (hE : finrank ℝ E = 4) {n : Fin 4 → E} (hn : LinearIndependent ℝ n) {z : E}
    (hz : ∀ j, ⟪n j, z⟫ = 0) : z = 0 := by
  have hb : Submodule.span ℝ (Set.range n) = ⊤ :=
    hn.span_eq_top_of_card_eq_finrank (by simp [hE])
  have hz' : z ∈ (Submodule.span ℝ (Set.range n))ᗮ := by
    rw [Submodule.mem_orthogonal']
    intro u hu
    refine Submodule.span_induction (fun y hy => ?_) ?_ (fun x y _ _ hx hy => ?_) (fun a x _ hx => ?_) hu
    · obtain ⟨j, rfl⟩ := hy; rw [real_inner_comm]; exact hz j
    · simp
    · rw [inner_add_right, hx, hy, add_zero]
    · rw [inner_smul_right, hx, mul_zero]
  rw [hb, Submodule.top_orthogonal_eq_bot, Submodule.mem_bot] at hz'
  exact hz'

omit [MeasurableSpace E] [BorelSpace E] in
/-- **A point of a facet in barycentric coordinates.** In four-space, let the facet `⟪ap, ·⟫ = 1` have corners
`v j` and neighbouring facet normals `n i` with `⟪n i, v j⟫ = c` for `i = j` and `1` otherwise, and
`∑ n i = (3 + c) ap`. Then every point `x` of the facet's hyperplane is `∑ μ j • v j` with
`μ j = (1 − ⟪n j, x⟫) / (1 − c)`. -/
lemma facet_bary (hE : finrank ℝ E = 4) {ap : E} {v n : Fin 4 → E} {c : ℝ} (hc1 : c ≠ 1) (hc3 : c ≠ -3)
    (hnv : ∀ i j, ⟪n i, v j⟫ = if i = j then c else 1) (hsum : ∑ i, n i = (3 + c) • ap)
    {x : E} (hx : ⟪ap, x⟫ = 1) :
    x = ∑ j, ((1 - ⟪n j, x⟫) / (1 - c)) • v j := by
  have h1c : (1 - c) ≠ 0 := sub_ne_zero.2 (Ne.symm hc1)
  have hsx : ∑ i, ⟪n i, x⟫ = 3 + c := by
    rw [← sum_inner, hsum, inner_smul_left, hx]; simp
  have hS : ∑ j, (1 - ⟪n j, x⟫) / (1 - c) = 1 := by
    rw [← Finset.sum_div, Finset.sum_sub_distrib, hsx]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    field_simp; ring
  rw [← sub_eq_zero]
  apply eq_zero_of_inner_four hE (linIndep_of_pairing hc1 hc3 hnv)
  intro i
  rw [inner_sub_right, inner_sum]
  simp only [inner_smul_right, hnv]
  have e : ∑ j, (1 - ⟪n j, x⟫) / (1 - c) * (if i = j then c else 1) =
      ∑ j, (1 - ⟪n j, x⟫) / (1 - c) - (1 - ⟪n i, x⟫) := by
    rw [Fin.sum_univ_four, Fin.sum_univ_four]
    fin_cases i <;> simp <;> field_simp <;> ring
  rw [e, hS]; ring

end DehnHadwiger
