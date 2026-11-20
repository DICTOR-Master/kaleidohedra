/-
Dehn–Hadwiger study, part 8: the regular 120-cell has invariant zero (DICTO, 20 Nov 2026).

Coordinates in ℤ[φ] (φ the golden ratio, Mathlib `Real.goldenRatio`): the pair `(a, b)` stands for `a + b φ`
(`gval`). The 120 facet normals of the 120-cell are the 120 vertices of the 600-cell, doubled
(`cell120Z`): ±2eᵢ, (±1, ±1, ±1, ±1) and the even permutations of (±φ, ±1, ±φ⁻¹, 0), φ⁻¹ = φ − 1; the
120-cell is `sol` of these normals with offset 1 (the polar of the 600-cell is the 120-cell).
Any two normals have dot product 0, ±2, ±4, ±2φ or ±2(φ − 1) (`cell120_dot_table`, checked by
`decide +kernel` in ℤ[φ]), so their angles are multiples of 36° or 60°: cos 5θ = ±1 for cos θ = ±φ/2,
±(φ − 1)/2 (`cos_five_mul`, the fivefold-angle formula). By part 4 the invariant is zero.
No `sorry`.
-/
import DehnHadwiger.DH7Cell5

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

/-- The real number `a + b φ` coded by `(a, b)`. -/
noncomputable def gval (c : ℤ × ℤ) : ℝ := c.1 + c.2 * Real.goldenRatio

/-- Product in ℤ[φ], with φ² = φ + 1. -/
def gmul (c d : ℤ × ℤ) : ℤ × ℤ := (c.1 * d.1 + c.2 * d.2, c.1 * d.2 + c.2 * d.1 + c.2 * d.2)

lemma gval_mul (c d : ℤ × ℤ) : gval (gmul c d) = gval c * gval d := by
  have h := Real.goldenRatio_sq
  unfold gval gmul; push_cast; linear_combination (-(c.2 : ℝ) * d.2) * h

lemma gval_add (c d : ℤ × ℤ) : gval (c + d) = gval c + gval d := by
  unfold gval; simp only [Prod.fst_add, Prod.snd_add]; push_cast; ring

/-- The vector of `R4` with coordinates in ℤ[φ]. -/
noncomputable def gvec (z : Fin 4 → ℤ × ℤ) : R4 := !₂[gval (z 0), gval (z 1), gval (z 2), gval (z 3)]

/-- Dot product in ℤ[φ]. -/
def gdot (z w : Fin 4 → ℤ × ℤ) : ℤ × ℤ := gmul (z 0) (w 0) + gmul (z 1) (w 1) + gmul (z 2) (w 2) + gmul (z 3) (w 3)

lemma inner_gvec (z w : Fin 4 → ℤ × ℤ) : ⟪gvec z, gvec w⟫ = gval (gdot z w) := by
  unfold gvec gdot; rw [inner4]; simp only [gval_add, gval_mul]; rfl

/-- **The fivefold-angle formula.** -/
lemma cos_five_mul (x : ℝ) : Real.cos (5 * x) = 16 * Real.cos x ^ 5 - 20 * Real.cos x ^ 3 + 5 * Real.cos x := by
  have h5 : 5 * x = 3 * x + 2 * x := by ring
  have hs := Real.sin_sq_add_cos_sq x
  rw [h5, Real.cos_add, Real.cos_three_mul, Real.cos_two_mul, Real.sin_three_mul, Real.sin_two_mul]
  linear_combination (-2 * Real.cos x * (3 - 4 * (Real.sin x ^ 2 + 1 - Real.cos x ^ 2))) * hs

lemma mem_ratPi_of_cos_five {θ : ℝ} (h : Real.cos (5 * θ) = 1 ∨ Real.cos (5 * θ) = -1) : θ ∈ ratPi := by
  apply mem_ratPi_of_sin_nat_mul 5 (by norm_num)
  have hs := Real.sin_sq_add_cos_sq (5 * θ)
  have h0 : Real.sin (5 * θ) ^ 2 = 0 := by rcases h with e | e <;> rw [e] at hs <;> linarith
  push_cast
  exact pow_eq_zero_iff (two_ne_zero) |>.1 h0

/-- Angles whose cosine is ±φ/2 or ±(φ − 1)/2 (36°, 72°, 108°, 144°) are rational multiples of π. -/
lemma mem_ratPi_of_cos_gold {θ : ℝ} (h : Real.cos θ = Real.goldenRatio / 2 ∨ Real.cos θ = -(Real.goldenRatio / 2) ∨
    Real.cos θ = (Real.goldenRatio - 1) / 2 ∨ Real.cos θ = -((Real.goldenRatio - 1) / 2)) : θ ∈ ratPi := by
  have g := Real.goldenRatio_sq
  set p := Real.goldenRatio
  apply mem_ratPi_of_cos_five
  rw [cos_five_mul]
  rcases h with e | e | e | e <;> rw [e]
  · right; linear_combination (-1 - 3 / 2 * p + 1 / 2 * p ^ 2 + 1 / 2 * p ^ 3) * g
  · left; linear_combination (1 + 3 / 2 * p - 1 / 2 * p ^ 2 - 1 / 2 * p ^ 3) * g
  · left; linear_combination (3 / 2 + p - 2 * p ^ 2 + 1 / 2 * p ^ 3) * g
  · right; linear_combination (-3 / 2 - p + 2 * p ^ 2 - 1 / 2 * p ^ 3) * g

/-- The dot products allowed between the normals (of length 2). -/
def goldDots : List (ℤ × ℤ) := [(4, 0), (-4, 0), (2, 0), (-2, 0), (0, 0), (0, 2), (0, -2), (-2, 2), (2, -2)]

lemma angle_mem_ratPi_of_gdot {z w : Fin 4 → ℤ × ℤ} (hz : gdot z z = (4, 0)) (hw : gdot w w = (4, 0))
    (h : gdot z w ∈ goldDots) : InnerProductGeometry.angle (gvec z) (gvec w) ∈ ratPi := by
  have hn : ∀ v : Fin 4 → ℤ × ℤ, gdot v v = (4, 0) → ‖gvec v‖ = 2 := by
    intro v hv
    have h1 := inner_gvec v v
    rw [hv, real_inner_self_eq_norm_sq] at h1
    simp [gval] at h1
    nlinarith [norm_nonneg (gvec v)]
  have hc : Real.cos (InnerProductGeometry.angle (gvec z) (gvec w)) = gval (gdot z w) / 4 := by
    rw [InnerProductGeometry.cos_angle, inner_gvec, hn z hz, hn w hw]; ring
  simp only [goldDots, List.mem_cons, List.not_mem_nil, or_false] at h
  have g4 : ∀ k : ℕ, k ≤ 4 → 4 * Real.cos (InnerProductGeometry.angle (gvec z) (gvec w)) ^ 2 = k →
      InnerProductGeometry.angle (gvec z) (gvec w) ∈ ratPi := fun k hk e => mem_ratPi_of_four_cos_sq hk e
  rcases h with e | e | e | e | e | e | e | e | e <;> rw [e] at hc <;> simp [gval] at hc
  · exact g4 4 le_rfl (by rw [hc]; norm_num)
  · exact g4 4 le_rfl (by rw [hc]; norm_num)
  · exact g4 1 (by norm_num) (by rw [hc]; norm_num)
  · exact g4 1 (by norm_num) (by rw [hc]; norm_num)
  · exact g4 0 (by norm_num) (by rw [hc]; norm_num)
  · exact mem_ratPi_of_cos_gold (Or.inl (by rw [hc]; ring))
  · exact mem_ratPi_of_cos_gold (Or.inr (Or.inl (by rw [hc]; ring)))
  · exact mem_ratPi_of_cos_gold (Or.inr (Or.inr (Or.inl (by rw [hc]; ring))))
  · exact mem_ratPi_of_cos_gold (Or.inr (Or.inr (Or.inr (by rw [hc]; ring))))

/-- **Normals in ℤ[φ] with dot products in `goldDots` give invariant zero.** -/
theorem dehnHadwiger_gvec_eq_zero {n : ℕ} (z : Fin n → Fin 4 → ℤ × ℤ) (b : Fin n → ℝ)
    (hself : ∀ i, gdot (z i) (z i) = (4, 0)) (htab : ∀ i j, gdot (z i) (z j) ∈ goldDots) :
    dehnHadwiger (sol (fun i => gvec (z i)) b) = 0 := by
  have hne : ∀ i, gvec (z i) ≠ 0 := by
    intro i h0
    have h1 := inner_gvec (z i) (z i)
    rw [h0, inner_zero_left, hself] at h1
    simp [gval] at h1
  exact dehnHadwiger_sol_eq_zero_of_rational _ _ hne
    (fun i j => angle_mem_ratPi_of_gdot (hself i) (hself j) (htab i j))

/-- Facet normals of the regular 120-cell: the 120 vertices of the 600-cell, doubled, in ℤ[φ]. -/
def cell120Z : Fin 120 → Fin 4 → ℤ × ℤ :=
  ![![(2, 0), (0, 0), (0, 0), (0, 0)], ![(-2, 0), (0, 0), (0, 0), (0, 0)], ![(0, 0), (2, 0), (0, 0), (0, 0)], ![(0, 0), (-2, 0), (0, 0), (0, 0)], ![(0, 0), (0, 0), (2, 0), (0, 0)],
    ![(0, 0), (0, 0), (-2, 0), (0, 0)], ![(0, 0), (0, 0), (0, 0), (2, 0)], ![(0, 0), (0, 0), (0, 0), (-2, 0)], ![(1, 0), (1, 0), (1, 0), (1, 0)], ![(1, 0), (1, 0), (1, 0), (-1, 0)],
    ![(1, 0), (1, 0), (-1, 0), (1, 0)], ![(1, 0), (1, 0), (-1, 0), (-1, 0)], ![(1, 0), (-1, 0), (1, 0), (1, 0)], ![(1, 0), (-1, 0), (1, 0), (-1, 0)], ![(1, 0), (-1, 0), (-1, 0), (1, 0)],
    ![(1, 0), (-1, 0), (-1, 0), (-1, 0)], ![(-1, 0), (1, 0), (1, 0), (1, 0)], ![(-1, 0), (1, 0), (1, 0), (-1, 0)], ![(-1, 0), (1, 0), (-1, 0), (1, 0)], ![(-1, 0), (1, 0), (-1, 0), (-1, 0)],
    ![(-1, 0), (-1, 0), (1, 0), (1, 0)], ![(-1, 0), (-1, 0), (1, 0), (-1, 0)], ![(-1, 0), (-1, 0), (-1, 0), (1, 0)], ![(-1, 0), (-1, 0), (-1, 0), (-1, 0)], ![(0, 1), (1, 0), (-1, 1), (0, 0)],
    ![(0, 1), (1, 0), (1, -1), (0, 0)], ![(0, 1), (-1, 0), (-1, 1), (0, 0)], ![(0, 1), (-1, 0), (1, -1), (0, 0)], ![(0, -1), (1, 0), (-1, 1), (0, 0)], ![(0, -1), (1, 0), (1, -1), (0, 0)],
    ![(0, -1), (-1, 0), (-1, 1), (0, 0)], ![(0, -1), (-1, 0), (1, -1), (0, 0)], ![(0, 1), (-1, 1), (0, 0), (1, 0)], ![(0, 1), (-1, 1), (0, 0), (-1, 0)], ![(0, 1), (1, -1), (0, 0), (1, 0)],
    ![(0, 1), (1, -1), (0, 0), (-1, 0)], ![(0, -1), (-1, 1), (0, 0), (1, 0)], ![(0, -1), (-1, 1), (0, 0), (-1, 0)], ![(0, -1), (1, -1), (0, 0), (1, 0)], ![(0, -1), (1, -1), (0, 0), (-1, 0)],
    ![(0, 1), (0, 0), (1, 0), (-1, 1)], ![(0, 1), (0, 0), (1, 0), (1, -1)], ![(0, 1), (0, 0), (-1, 0), (-1, 1)], ![(0, 1), (0, 0), (-1, 0), (1, -1)], ![(0, -1), (0, 0), (1, 0), (-1, 1)],
    ![(0, -1), (0, 0), (1, 0), (1, -1)], ![(0, -1), (0, 0), (-1, 0), (-1, 1)], ![(0, -1), (0, 0), (-1, 0), (1, -1)], ![(1, 0), (0, 1), (0, 0), (-1, 1)], ![(1, 0), (0, 1), (0, 0), (1, -1)],
    ![(1, 0), (0, -1), (0, 0), (-1, 1)], ![(1, 0), (0, -1), (0, 0), (1, -1)], ![(-1, 0), (0, 1), (0, 0), (-1, 1)], ![(-1, 0), (0, 1), (0, 0), (1, -1)], ![(-1, 0), (0, -1), (0, 0), (-1, 1)],
    ![(-1, 0), (0, -1), (0, 0), (1, -1)], ![(1, 0), (-1, 1), (0, 1), (0, 0)], ![(1, 0), (-1, 1), (0, -1), (0, 0)], ![(1, 0), (1, -1), (0, 1), (0, 0)], ![(1, 0), (1, -1), (0, -1), (0, 0)],
    ![(-1, 0), (-1, 1), (0, 1), (0, 0)], ![(-1, 0), (-1, 1), (0, -1), (0, 0)], ![(-1, 0), (1, -1), (0, 1), (0, 0)], ![(-1, 0), (1, -1), (0, -1), (0, 0)], ![(1, 0), (0, 0), (-1, 1), (0, 1)],
    ![(1, 0), (0, 0), (-1, 1), (0, -1)], ![(1, 0), (0, 0), (1, -1), (0, 1)], ![(1, 0), (0, 0), (1, -1), (0, -1)], ![(-1, 0), (0, 0), (-1, 1), (0, 1)], ![(-1, 0), (0, 0), (-1, 1), (0, -1)],
    ![(-1, 0), (0, 0), (1, -1), (0, 1)], ![(-1, 0), (0, 0), (1, -1), (0, -1)], ![(-1, 1), (0, 1), (1, 0), (0, 0)], ![(-1, 1), (0, 1), (-1, 0), (0, 0)], ![(-1, 1), (0, -1), (1, 0), (0, 0)],
    ![(-1, 1), (0, -1), (-1, 0), (0, 0)], ![(1, -1), (0, 1), (1, 0), (0, 0)], ![(1, -1), (0, 1), (-1, 0), (0, 0)], ![(1, -1), (0, -1), (1, 0), (0, 0)], ![(1, -1), (0, -1), (-1, 0), (0, 0)],
    ![(-1, 1), (1, 0), (0, 0), (0, 1)], ![(-1, 1), (1, 0), (0, 0), (0, -1)], ![(-1, 1), (-1, 0), (0, 0), (0, 1)], ![(-1, 1), (-1, 0), (0, 0), (0, -1)], ![(1, -1), (1, 0), (0, 0), (0, 1)],
    ![(1, -1), (1, 0), (0, 0), (0, -1)], ![(1, -1), (-1, 0), (0, 0), (0, 1)], ![(1, -1), (-1, 0), (0, 0), (0, -1)], ![(-1, 1), (0, 0), (0, 1), (1, 0)], ![(-1, 1), (0, 0), (0, 1), (-1, 0)],
    ![(-1, 1), (0, 0), (0, -1), (1, 0)], ![(-1, 1), (0, 0), (0, -1), (-1, 0)], ![(1, -1), (0, 0), (0, 1), (1, 0)], ![(1, -1), (0, 0), (0, 1), (-1, 0)], ![(1, -1), (0, 0), (0, -1), (1, 0)],
    ![(1, -1), (0, 0), (0, -1), (-1, 0)], ![(0, 0), (0, 1), (-1, 1), (1, 0)], ![(0, 0), (0, 1), (-1, 1), (-1, 0)], ![(0, 0), (0, 1), (1, -1), (1, 0)], ![(0, 0), (0, 1), (1, -1), (-1, 0)],
    ![(0, 0), (0, -1), (-1, 1), (1, 0)], ![(0, 0), (0, -1), (-1, 1), (-1, 0)], ![(0, 0), (0, -1), (1, -1), (1, 0)], ![(0, 0), (0, -1), (1, -1), (-1, 0)], ![(0, 0), (1, 0), (0, 1), (-1, 1)],
    ![(0, 0), (1, 0), (0, 1), (1, -1)], ![(0, 0), (1, 0), (0, -1), (-1, 1)], ![(0, 0), (1, 0), (0, -1), (1, -1)], ![(0, 0), (-1, 0), (0, 1), (-1, 1)], ![(0, 0), (-1, 0), (0, 1), (1, -1)],
    ![(0, 0), (-1, 0), (0, -1), (-1, 1)], ![(0, 0), (-1, 0), (0, -1), (1, -1)], ![(0, 0), (-1, 1), (1, 0), (0, 1)], ![(0, 0), (-1, 1), (1, 0), (0, -1)], ![(0, 0), (-1, 1), (-1, 0), (0, 1)],
    ![(0, 0), (-1, 1), (-1, 0), (0, -1)], ![(0, 0), (1, -1), (1, 0), (0, 1)], ![(0, 0), (1, -1), (1, 0), (0, -1)], ![(0, 0), (1, -1), (-1, 0), (0, 1)], ![(0, 0), (1, -1), (-1, 0), (0, -1)]]

/-- The regular 120-cell: `⟪n, x⟫ ≤ 1` for its 120 facet normals `n`. -/
def cell120 : Set R4 := sol (fun i => gvec (cell120Z i)) (fun _ => 1)

lemma cell120_self : ∀ i, gdot (cell120Z i) (cell120Z i) = (4, 0) := by decide +kernel

lemma cell120_dot_table : ∀ i j, gdot (cell120Z i) (cell120Z j) ∈ goldDots := by decide +kernel

theorem dehnHadwiger_cell120 : dehnHadwiger cell120 = 0 :=
  dehnHadwiger_gvec_eq_zero _ _ cell120_self cell120_dot_table

theorem isPoly_cell120 : IsPoly cell120 := by
  refine ⟨bounded_of_coords4 1 ?_, Fin 120, inferInstance, _, _, rfl⟩
  intro x hx k
  have H : ∀ i, ⟪gvec (cell120Z i), x⟫ ≤ 1 := hx
  have e0 : cell120Z 0 = ![(2, 0), (0, 0), (0, 0), (0, 0)] := rfl
  have e1 : cell120Z 1 = ![(-2, 0), (0, 0), (0, 0), (0, 0)] := rfl
  have e2 : cell120Z 2 = ![(0, 0), (2, 0), (0, 0), (0, 0)] := rfl
  have e3 : cell120Z 3 = ![(0, 0), (-2, 0), (0, 0), (0, 0)] := rfl
  have e4 : cell120Z 4 = ![(0, 0), (0, 0), (2, 0), (0, 0)] := rfl
  have e5 : cell120Z 5 = ![(0, 0), (0, 0), (-2, 0), (0, 0)] := rfl
  have e6 : cell120Z 6 = ![(0, 0), (0, 0), (0, 0), (2, 0)] := rfl
  have e7 : cell120Z 7 = ![(0, 0), (0, 0), (0, 0), (-2, 0)] := rfl
  have h0 := H 0
  rw [e0] at h0
  have h1 := H 1
  rw [e1] at h1
  have h2 := H 2
  rw [e2] at h2
  have h3 := H 3
  rw [e3] at h3
  have h4 := H 4
  rw [e4] at h4
  have h5 := H 5
  rw [e5] at h5
  have h6 := H 6
  rw [e6] at h6
  have h7 := H 7
  rw [e7] at h7
  simp [gvec, gval, inner4] at h0 h1 h2 h3 h4 h5 h6 h7
  fin_cases k <;> exact abs_le.2 ⟨by simp; linarith, by simp; linarith⟩

end DehnHadwiger
