/-
Dehn–Hadwiger study, part 7: the regular 5-cell has non-zero invariant (DICTO, 20 Nov 2026).

`cell5 = sol fiveN 1` with the five facet normals (√5 s, 1) (s = (1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1)) and
(0, 0, 0, −4): all of length 4, any two with dot product −4, so the polytope is a regular 5-cell (the polar of
the regular simplex with these corners). Any two facets meet at the dihedral angle π − arccos(−1/4) = arccos(1/4).

* `dehnHadwiger_cell5`: the invariant is A ⊗ arccos(1/4) with A the total area (2-dimensional Hausdorff measure)
  of the ridge points, `0 < A < ∞`.
* `arccos_quarter_not_ratPi`: arccos(1/4) is not a rational multiple of π (Niven's theorem, Mathlib
  `niven`, Meiburg–Broshi; the Canon's arccos(1/3) proof, unchanged).
* `dehnHadwiger_cell5_ne_zero`.

The area is positive because a small square of the ridge between the facets 3 and 4 is mapped onto a square of
the plane by a 1-Lipschitz map (`hausdorff_two_pos`, Mathlib `hausdorffMeasure_pi_real`), and finite by part 2.
No `sorry`.
-/
import DehnHadwiger.DH6Cells

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

/-- A set of `R4` that a 1-Lipschitz map sends onto a set containing a non-empty open set of the plane has
positive area. -/
lemma hausdorff_two_pos {S : Set R4} (f : R4 → (Fin 2 → ℝ)) (hf : LipschitzWith 1 f)
    {U : Set (Fin 2 → ℝ)} (hU : IsOpen U) (hne : U.Nonempty) (hsub : U ⊆ f '' S) : 0 < μH[2] S := by
  have h0 : (μH[(Fintype.card (Fin 2) : ℝ)] : Measure (Fin 2 → ℝ)) = volume := hausdorffMeasure_pi_real
  simp only [Fintype.card_fin, Nat.cast_ofNat] at h0
  have h1 : 0 < μH[2] U := by rw [h0]; exact hU.measure_pos volume hne
  have h2 := hf.hausdorffMeasure_image_le (d := 2) (by norm_num) S
  simp only [ENNReal.coe_one, ENNReal.one_rpow, one_mul] at h2
  exact h1.trans_le ((measure_mono hsub).trans h2)

lemma finrank_R4_sub : ((finrank ℝ R4 - 2 : ℕ) : ℝ) = 2 := by simp

/-- The five facet normals of the regular 5-cell. -/
noncomputable def fiveN : Fin 5 → R4 :=
  ![!₂[√5, √5, √5, 1], !₂[√5, -√5, -√5, 1], !₂[-√5, √5, -√5, 1], !₂[-√5, -√5, √5, 1], !₂[0, 0, 0, -4]]

/-- The regular 5-cell: the points with `⟪fiveN i, x⟫ ≤ 1` for the five facet normals. -/
def cell5 : Set R4 := sol fiveN (fun _ => 1)

lemma s5 : √5 * √5 = 5 := Real.mul_self_sqrt (by norm_num)

lemma two_le_s5 : 2 ≤ √5 := Real.le_sqrt_of_sq_le (by norm_num)

lemma s5_lt_three : √5 < 3 := (Real.sqrt_lt' (by norm_num)).2 (by norm_num)

lemma fiveN_inner (i j : Fin 5) : ⟪fiveN i, fiveN j⟫ = if i = j then 16 else -4 := by
  have h := s5
  fin_cases i <;> fin_cases j <;>
    simp [fiveN, inner4, -inner_self_eq_norm_sq_to_K] <;> nlinarith [h]

lemma fiveN_norm (i : Fin 5) : ‖fiveN i‖ = 4 := by
  have h := fiveN_inner i i
  rw [ite_eq_left rfl, real_inner_self_eq_norm_sq] at h
  nlinarith [norm_nonneg (fiveN i)]

lemma fiveN_ne_zero (i : Fin 5) : fiveN i ≠ 0 := by
  intro h; have := fiveN_norm i; rw [h, norm_zero] at this; norm_num at this

lemma fiveN_angle {i j : Fin 5} (h : i ≠ j) :
    InnerProductGeometry.angle (fiveN i) (fiveN j) = Real.arccos (-(1 / 4)) := by
  unfold InnerProductGeometry.angle
  rw [fiveN_inner, ite_eq_right h, fiveN_norm, fiveN_norm]; norm_num

lemma fiveN_indep {i j : Fin 5} (h : i ≠ j) : LinearIndependent ℝ ![fiveN i, fiveN j] := by
  apply linIndep_pair_of_gram
  rw [fiveN_inner, fiveN_inner, fiveN_inner, ite_eq_left rfl, ite_eq_left rfl, ite_eq_right h]; norm_num

/-- The dihedral angle of the regular 5-cell, as a class modulo ℚπ: arccos(1/4). -/
lemma fiveN_class {i j : Fin 5} (h : i ≠ j) :
    (Submodule.Quotient.mk (Real.pi - InnerProductGeometry.angle (fiveN i) (fiveN j)) : Angle) =
      Submodule.Quotient.mk (Real.arccos (1 / 4)) := by
  rw [fiveN_angle h, Real.arccos_neg, sub_sub_cancel]

/-- **arccos(1/4) is not a rational multiple of π** (Niven's theorem). -/
theorem arccos_quarter_not_ratPi : Real.arccos (1 / 4) ∉ ratPi := by
  rw [mem_ratPi_iff]
  rintro ⟨r, hr⟩
  have hcos : Real.cos (Real.arccos (1 / 4)) = 1 / 4 := by rw [Real.cos_arccos] <;> norm_num
  have hn := niven (θ := Real.arccos (1 / 4)) ⟨r, hr⟩ ⟨1 / 4, by rw [hcos]; norm_num⟩
  rw [hcos] at hn
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hn
  norm_num at hn

theorem isPoly_cell5 : IsPoly cell5 := by
  refine ⟨bounded_of_coords4 6 ?_, Fin 5, inferInstance, _, _, rfl⟩
  intro x hx k
  have H : ∀ i, ⟪fiveN i, x⟫ ≤ 1 := hx
  have h0 := H 0; have h1 := H 1; have h2 := H 2; have h3 := H 3; have h4 := H 4
  simp [fiveN, inner4] at h0 h1 h2 h3 h4
  have hs := two_le_s5
  fin_cases k <;> refine abs_le.2 ⟨?_, ?_⟩ <;> simp <;> nlinarith

/-- **The invariant of the 5-cell**: (area of its ridge points) ⊗ arccos(1/4). -/
theorem dehnHadwiger_cell5_eq : dehnHadwiger cell5 =
    (μH[(finrank ℝ R4 - 2 : ℕ)] {x | ridgeAngle cell5 x = Submodule.Quotient.mk (Real.arccos (1 / 4))}).toReal
      ⊗ₜ[ℚ] (Submodule.Quotient.mk (Real.arccos (1 / 4)) : Angle) := by
  apply dehnHadwiger_sol_eq_single fiveN _ fiveN_ne_zero
  intro x _ p _ q _ hli
  have hpq : p ≠ q := by
    rintro rfl
    have := LinearIndependent.pair_iff.1 hli 1 (-1) (by simp)
    exact one_ne_zero this.1
  exact fiveN_class hpq

/-- A point of the ridge between the facets 3 and 4. -/
noncomputable def ridgePt (s t : ℝ) : R4 := !₂[-√5 / 12 + s + t, -√5 / 12 - s + t, √5 / 12 + 2 * t, -1 / 4]

lemma ridgePt_inner (s t : ℝ) :
    ⟪fiveN 0, ridgePt s t⟫ = -2 / 3 + 4 * √5 * t ∧ ⟪fiveN 1, ridgePt s t⟫ = -2 / 3 + 2 * √5 * (s - t) ∧
    ⟪fiveN 2, ridgePt s t⟫ = -2 / 3 - 2 * √5 * (s + t) ∧ ⟪fiveN 3, ridgePt s t⟫ = 1 ∧
    ⟪fiveN 4, ridgePt s t⟫ = 1 := by
  have h := s5
  simp only [fiveN, ridgePt, Matrix.cons_val, inner4]
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> nlinarith [h]

lemma ridgePt_facts {s t : ℝ} (hs : |s| < 1 / 10) (ht : |t| < 1 / 10) :
    ridgePt s t ∈ cell5 ∧ act fiveN (fun _ => 1) (ridgePt s t) = {3, 4} := by
  obtain ⟨e0, e1, e2, e3, e4⟩ := ridgePt_inner s t
  obtain ⟨hs1, hs2⟩ := abs_lt.1 hs
  obtain ⟨ht1, ht2⟩ := abs_lt.1 ht
  have h3 := s5_lt_three
  have h2 := two_le_s5
  have l0 : ⟪fiveN 0, ridgePt s t⟫ < 1 := by rw [e0]; nlinarith
  have l1 : ⟪fiveN 1, ridgePt s t⟫ < 1 := by rw [e1]; nlinarith
  have l2 : ⟪fiveN 2, ridgePt s t⟫ < 1 := by rw [e2]; nlinarith
  refine ⟨?_, ?_⟩
  · intro i; fin_cases i
    · exact l0.le
    · exact l1.le
    · exact l2.le
    · exact e3.le
    · exact e4.le
  · ext i; fin_cases i
    · simp only [act, mem_ofPred_eq]; constructor
      · intro h; exact absurd h l0.ne
      · intro h; simp at h
    · simp only [act, mem_ofPred_eq]; constructor
      · intro h; exact absurd h l1.ne
      · intro h; simp at h
    · simp only [act, mem_ofPred_eq]; constructor
      · intro h; exact absurd h l2.ne
      · intro h; simp at h
    · simp only [act, mem_ofPred_eq]; exact ⟨fun _ => by simp, fun _ => e3⟩
    · simp only [act, mem_ofPred_eq]; exact ⟨fun _ => by simp, fun _ => e4⟩

lemma ridgeAngle_ridgePt {s t : ℝ} (hs : |s| < 1 / 10) (ht : |t| < 1 / 10) :
    ridgeAngle cell5 (ridgePt s t) = Submodule.Quotient.mk (Real.arccos (1 / 4)) := by
  obtain ⟨hmem, hact⟩ := ridgePt_facts hs ht
  unfold cell5 at hmem ⊢
  rw [ridgeAngle_sol _ _ hmem, hact, thetaH_pair fiveN rfl (fiveN_indep (by decide)),
    fiveN_class (by decide)]

/-- The area of the ridge points of the 5-cell is positive. -/
lemma cell5_area_pos :
    0 < μH[2] {x | ridgeAngle cell5 x = Submodule.Quotient.mk (Real.arccos (1 / 4))} := by
  let S : Set R4 := {y | ∃ s t : ℝ, |s| < 1 / 10 ∧ |t| < 1 / 10 ∧ y = ridgePt s t}
  have hS : S ⊆ {x | ridgeAngle cell5 x = Submodule.Quotient.mk (Real.arccos (1 / 4))} := by
    rintro y ⟨s, t, hs, ht, rfl⟩; exact ridgeAngle_ridgePt hs ht
  let f : R4 → (Fin 2 → ℝ) := fun y => ![(y 0 - y 1) / 2, (y 0 + y 1 + 2 * y 2) / 6]
  have hf : LipschitzWith 1 f := by
    apply LipschitzWith.of_dist_le_mul
    intro y z
    rw [NNReal.coe_one, one_mul, dist_pi_le_iff dist_nonneg, dist_eq_norm]
    have hk : ∀ k, |y k - z k| ≤ ‖y - z‖ := fun k => by
      have := PiLp.norm_apply_le (y - z) k
      rwa [PiLp.sub_apply, Real.norm_eq_abs] at this
    have a0 := hk 0; have a1 := hk 1; have a2 := hk 2
    intro i; fin_cases i
    · simp only [f, Real.dist_eq]
      rw [abs_le]; constructor <;> simp <;> nlinarith [abs_le.1 a0, abs_le.1 a1, norm_nonneg (y - z)]
    · simp only [f, Real.dist_eq]
      rw [abs_le]; constructor <;> simp <;>
        nlinarith [abs_le.1 a0, abs_le.1 a1, abs_le.1 a2, norm_nonneg (y - z)]
  let U : Set (Fin 2 → ℝ) := {w | |w 0| < 1 / 10 ∧ |w 1| < 1 / 10}
  have hU : IsOpen U := by
    show IsOpen ({w : Fin 2 → ℝ | |w 0| < 1 / 10} ∩ {w | |w 1| < 1 / 10})
    exact (isOpen_lt (by fun_prop) continuous_const).inter (isOpen_lt (by fun_prop) continuous_const)
  have hne : U.Nonempty := ⟨0, by simp [U]⟩
  have hsub : U ⊆ f '' S := by
    rintro w ⟨hw0, hw1⟩
    refine ⟨ridgePt (w 0) (w 1), ⟨w 0, w 1, hw0, hw1, rfl⟩, ?_⟩
    funext i; fin_cases i <;> simp [f, ridgePt]
    ring
  exact (hausdorff_two_pos f hf hU hne hsub).trans_le (measure_mono hS)

/-- **The regular 5-cell has non-zero Dehn–Hadwiger invariant.** -/
theorem dehnHadwiger_cell5_ne_zero : dehnHadwiger cell5 ≠ 0 := by
  rw [dehnHadwiger_cell5_eq]
  have hτ : (Submodule.Quotient.mk (Real.arccos (1 / 4)) : Angle) ≠ 0 := by
    rw [Ne, Submodule.Quotient.mk_eq_zero]; exact arccos_quarter_not_ratPi
  have hfin : μH[(finrank ℝ R4 - 2 : ℕ)]
      {x | ridgeAngle cell5 x = Submodule.Quotient.mk (Real.arccos (1 / 4))} ≠ ⊤ := by
    refine ne_top_of_le_ne_top (support_finite fiveN (fun _ => 1) isPoly_cell5.1) (measure_mono ?_)
    intro x hx; rw [mem_ofPred_eq] at hx ⊢; show ridgeAngle cell5 x ≠ 0; rw [hx]; exact hτ
  have hpos := cell5_area_pos
  rw [← finrank_R4_sub] at hpos
  exact edgeTerm_ne_zero (ENNReal.toReal_pos hpos.ne' hfin).ne' arccos_quarter_not_ratPi

end DehnHadwiger
