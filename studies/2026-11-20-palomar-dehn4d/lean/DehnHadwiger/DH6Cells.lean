/-
Dehn–Hadwiger study, part 6: four-space and the regular polytopes with integer facet normals (DICTO, 20 Nov 2026).

`R4` is coordinate 4-space. A polytope is given by its outward facet normals (whole-number vectors, `zvec`) and
the half-spaces `⟪n, x⟫ ≤ 1`:
* `tesseract`: normals ±eᵢ (8 facets): the cube [-1, 1]⁴;
* `cell16`: normals (±1, ±1, ±1, ±1) (16 facets): the regular 16-cell |x₀| + |x₁| + |x₂| + |x₃| ≤ 1;
* `cell24`: normals ±eᵢ ± eⱼ (24 facets): a regular 24-cell (the polar of the 24-cell with corners ±eᵢ ± eⱼ,
  which is again a 24-cell).
Each is a convex polytope with interior points, and each has Dehn–Hadwiger invariant zero: any two of its
normals make an angle of 0°, 60°, 90°, 120° or 180° (`dehnHadwiger_zvec_eq_zero`, from part 4; the angle
table is checked by `decide +kernel` on whole numbers, as the Canon's `crDot_table`).
No `sorry`.
-/
import DehnHadwiger.DH5Scale

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

/-- Coordinate 4-space. -/
abbrev R4 := EuclideanSpace ℝ (Fin 4)

instance : Fact (finrank ℝ R4 = 4) := ⟨by simp⟩

lemma inner4 (p q r s : ℝ) (x : R4) :
    ⟪(!₂[p, q, r, s] : R4), x⟫ = p * x 0 + q * x 1 + r * x 2 + s * x 3 := by
  simp [EuclideanSpace.inner_eq_star_dotProduct, Fin.sum_univ_four, dotProduct]; ring

lemma bounded_of_coords4 {S : Set R4} (C : ℝ) (h : ∀ x ∈ S, ∀ i, |x i| ≤ C) :
    Bornology.IsBounded S := by
  rw [isBounded_iff_forall_norm_le]
  refine ⟨√(4 * C ^ 2), fun x hx => ?_⟩
  rw [EuclideanSpace.norm_eq]
  apply Real.sqrt_le_sqrt
  rw [Fin.sum_univ_four]
  have h1 : ∀ i, ‖x i‖ ^ 2 ≤ C ^ 2 := fun i => by
    rw [Real.norm_eq_abs, sq_abs]
    exact sq_le_sq' (abs_le.1 (h x hx i)).1 (abs_le.1 (h x hx i)).2
  have := h1 0; have := h1 1; have := h1 2; have := h1 3
  linarith

/-- The vector of `R4` with whole-number coordinates `z`. -/
noncomputable def zvec (z : Fin 4 → ℤ) : R4 := !₂[(z 0 : ℝ), (z 1 : ℝ), (z 2 : ℝ), (z 3 : ℝ)]

/-- Dot product of whole-number vectors. -/
def zdot (z w : Fin 4 → ℤ) : ℤ := z 0 * w 0 + z 1 * w 1 + z 2 * w 2 + z 3 * w 3

lemma inner_zvec_left (z : Fin 4 → ℤ) (x : R4) :
    ⟪zvec z, x⟫ = (z 0 : ℝ) * x 0 + (z 1 : ℝ) * x 1 + (z 2 : ℝ) * x 2 + (z 3 : ℝ) * x 3 := by
  unfold zvec; rw [inner4]

lemma inner_zvec (z w : Fin 4 → ℤ) : ⟪zvec z, zvec w⟫ = (zdot z w : ℝ) := by
  rw [inner_zvec_left]; unfold zvec zdot; simp

lemma zvec_ne_zero {z : Fin 4 → ℤ} (h : zdot z z ≠ 0) : zvec z ≠ 0 := by
  intro h0
  have h1 := inner_zvec z z
  rw [h0, inner_zero_left] at h1
  exact h (by exact_mod_cast h1.symm)

/-- **Whole-number normals with rational angles give invariant zero.** -/
theorem dehnHadwiger_zvec_eq_zero {n : ℕ} (z : Fin n → Fin 4 → ℤ) (b : Fin n → ℝ)
    (htab : ∀ i j, ∃ k : Fin 5, 4 * zdot (z i) (z j) ^ 2 = (k : ℤ) * (zdot (z i) (z i) * zdot (z j) (z j)))
    (hne : ∀ i, zdot (z i) (z i) ≠ 0) :
    dehnHadwiger (sol (fun i => zvec (z i)) b) = 0 := by
  apply dehnHadwiger_sol_eq_zero_of_rational _ _ (fun i => zvec_ne_zero (hne i))
  intro i j
  obtain ⟨k, hk⟩ := htab i j
  apply angle_mem_ratPi_of_gram (zvec_ne_zero (hne i)) (zvec_ne_zero (hne j)) (k := (k : ℕ)) (by omega)
  rw [inner_zvec, inner_zvec, inner_zvec]
  exact_mod_cast hk

lemma zero_mem_interior_sol {ι : Type} [Finite ι] (a : ι → R4) (b : ι → ℝ) (hb : ∀ i, 0 < b i) :
    (0 : R4) ∈ interior (sol a b) := by
  have hopen : IsOpen {x : R4 | ∀ i, ⟪a i, x⟫ < b i} := by
    simp only [ofPred_forall]
    exact isOpen_iInter_of_finite fun i => isOpen_lt (by fun_prop) continuous_const
  refine interior_maximal (fun x hx i => (hx i).le) hopen ?_
  intro i; rw [inner_zero_right]; exact hb i

/-- Facet normals of the tesseract [-1, 1]⁴: ±eᵢ. -/
def tessZ : Fin 8 → Fin 4 → ℤ :=
  ![![1, 0, 0, 0], ![-1, 0, 0, 0], ![0, 1, 0, 0], ![0, -1, 0, 0], ![0, 0, 1, 0], ![0, 0, -1, 0], ![0, 0, 0, 1], ![0, 0, 0, -1]]

/-- Facet normals of the regular 16-cell: the sixteen vectors (±1, ±1, ±1, ±1). -/
def cell16Z : Fin 16 → Fin 4 → ℤ :=
  ![![1, 1, 1, 1], ![1, 1, 1, -1], ![1, 1, -1, 1], ![1, 1, -1, -1], ![1, -1, 1, 1], ![1, -1, 1, -1], ![1, -1, -1, 1], ![1, -1, -1, -1],
    ![-1, 1, 1, 1], ![-1, 1, 1, -1], ![-1, 1, -1, 1], ![-1, 1, -1, -1], ![-1, -1, 1, 1], ![-1, -1, 1, -1], ![-1, -1, -1, 1], ![-1, -1, -1, -1]]

/-- Facet normals of a regular 24-cell: the twenty-four vectors ±eᵢ ± eⱼ (i < j). -/
def cell24Z : Fin 24 → Fin 4 → ℤ :=
  ![![1, 1, 0, 0], ![1, -1, 0, 0], ![-1, 1, 0, 0], ![-1, -1, 0, 0], ![1, 0, 1, 0], ![1, 0, -1, 0], ![-1, 0, 1, 0], ![-1, 0, -1, 0],
    ![1, 0, 0, 1], ![1, 0, 0, -1], ![-1, 0, 0, 1], ![-1, 0, 0, -1], ![0, 1, 1, 0], ![0, 1, -1, 0], ![0, -1, 1, 0], ![0, -1, -1, 0],
    ![0, 1, 0, 1], ![0, 1, 0, -1], ![0, -1, 0, 1], ![0, -1, 0, -1], ![0, 0, 1, 1], ![0, 0, 1, -1], ![0, 0, -1, 1], ![0, 0, -1, -1]]

/-- The tesseract (4-cube) [-1, 1]⁴. -/
def tesseract : Set R4 := sol (fun i => zvec (tessZ i)) (fun _ => 1)

/-- The regular 16-cell |x₀| + |x₁| + |x₂| + |x₃| ≤ 1. -/
def cell16 : Set R4 := sol (fun i => zvec (cell16Z i)) (fun _ => 1)

/-- A regular 24-cell: |xᵢ| + |xⱼ| ≤ 1 for all i < j. -/
def cell24 : Set R4 := sol (fun i => zvec (cell24Z i)) (fun _ => 1)

theorem isPoly_tesseract : IsPoly tesseract := by
  refine ⟨bounded_of_coords4 1 ?_, Fin 8, inferInstance, _, _, rfl⟩
  intro x hx k
  have H : ∀ i, ⟪zvec (tessZ i), x⟫ ≤ 1 := hx
  simp only [inner_zvec_left] at H
  have h0 := H 0
  have h1 := H 1
  have h2 := H 2
  have h3 := H 3
  have h4 := H 4
  have h5 := H 5
  have h6 := H 6
  have h7 := H 7
  norm_num [tessZ] at h0 h1 h2 h3 h4 h5 h6 h7
  fin_cases k <;> exact abs_le.2 ⟨by simp; linarith, by simp; linarith⟩

theorem isPoly_cell16 : IsPoly cell16 := by
  refine ⟨bounded_of_coords4 1 ?_, Fin 16, inferInstance, _, _, rfl⟩
  intro x hx k
  have H : ∀ i, ⟪zvec (cell16Z i), x⟫ ≤ 1 := hx
  simp only [inner_zvec_left] at H
  have h0 := H 0
  have h1 := H 1
  have h2 := H 2
  have h3 := H 3
  have h4 := H 4
  have h5 := H 5
  have h6 := H 6
  have h7 := H 7
  have h8 := H 8
  have h9 := H 9
  have h10 := H 10
  have h11 := H 11
  have h12 := H 12
  have h13 := H 13
  have h14 := H 14
  have h15 := H 15
  norm_num [cell16Z] at h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h12 h13 h14 h15
  fin_cases k <;> exact abs_le.2 ⟨by simp; linarith, by simp; linarith⟩

theorem isPoly_cell24 : IsPoly cell24 := by
  refine ⟨bounded_of_coords4 1 ?_, Fin 24, inferInstance, _, _, rfl⟩
  intro x hx k
  have H : ∀ i, ⟪zvec (cell24Z i), x⟫ ≤ 1 := hx
  simp only [inner_zvec_left] at H
  have h0 := H 0
  have h1 := H 1
  have h2 := H 2
  have h3 := H 3
  have h4 := H 4
  have h5 := H 5
  have h6 := H 6
  have h7 := H 7
  have h8 := H 8
  have h9 := H 9
  have h10 := H 10
  have h11 := H 11
  have h12 := H 12
  have h13 := H 13
  have h14 := H 14
  have h15 := H 15
  have h16 := H 16
  have h17 := H 17
  have h18 := H 18
  have h19 := H 19
  have h20 := H 20
  have h21 := H 21
  have h22 := H 22
  have h23 := H 23
  norm_num [cell24Z] at h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h12 h13 h14 h15 h16 h17 h18 h19 h20 h21 h22 h23
  fin_cases k <;> exact abs_le.2 ⟨by simp; linarith, by simp; linarith⟩

theorem dehnHadwiger_tesseract : dehnHadwiger tesseract = 0 :=
  dehnHadwiger_zvec_eq_zero _ _ (by decide +kernel) (by decide +kernel)

theorem dehnHadwiger_cell16 : dehnHadwiger cell16 = 0 :=
  dehnHadwiger_zvec_eq_zero _ _ (by decide +kernel) (by decide +kernel)

theorem dehnHadwiger_cell24 : dehnHadwiger cell24 = 0 :=
  dehnHadwiger_zvec_eq_zero _ _ (by decide +kernel) (by decide +kernel)

end DehnHadwiger
