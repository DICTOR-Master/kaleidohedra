/-
Dehn–Hadwiger study, part 14: the 600-cell has non-zero invariant (DICTO, 20 Nov 2026).

* `area_pos_of_patch`: a set containing a small square `g + s e₁ + t e₂` (`e₁ ⊥ e₂`, lengths at most 1) has
  positive area (2-dimensional Hausdorff measure); from part 7's `hausdorff_two_pos`.
* `cell600_area_pos`: the ridge points of the 600-cell have positive area: a small square around the centre of the
  triangle shared by the facets `(0, 0, 2, 2)` and `(−φ⁻¹, 0, √5, φ)`, on which only these two facets are tight
  (checked by `decide +kernel` against all 600 normals, `chk_patch`).
* `isPoly_cell600`, `dehnHadwiger_cell600_ne_zero`.
No `sorry`.
-/
import DehnHadwiger.DH13Cell600

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

/-- **A small square has positive area.** -/
lemma area_pos_of_patch {g e₁ e₂ : R4} (h12 : ⟪e₁, e₂⟫ = 0) (h1 : 0 < ⟪e₁, e₁⟫) (h2 : 0 < ⟪e₂, e₂⟫)
    (n1 : ‖e₁‖ ≤ 1) (n2 : ‖e₂‖ ≤ 1) {ε : ℝ} (hε : 0 < ε) {S : Set R4}
    (hS : ∀ s t : ℝ, |s| < ε → |t| < ε → g + s • e₁ + t • e₂ ∈ S) : 0 < μH[2] S := by
  let f : R4 → (Fin 2 → ℝ) := fun y => ![⟪e₁, y⟫, ⟪e₂, y⟫]
  have hf : LipschitzWith 1 f := by
    apply LipschitzWith.of_dist_le_mul
    intro y z
    rw [NNReal.coe_one, one_mul, dist_pi_le_iff dist_nonneg]
    have key : ∀ e : R4, ‖e‖ ≤ 1 → dist ⟪e, y⟫ ⟪e, z⟫ ≤ dist y z := by
      intro e he
      rw [Real.dist_eq, ← inner_sub_right, dist_eq_norm]
      calc |⟪e, y - z⟫| ≤ ‖e‖ * ‖y - z‖ := abs_real_inner_le_norm _ _
        _ ≤ 1 * ‖y - z‖ := by gcongr
        _ = ‖y - z‖ := one_mul _
    intro i; fin_cases i
    · exact key e₁ n1
    · exact key e₂ n2
  let U : Set (Fin 2 → ℝ) := {w | |w 0 - ⟪e₁, g⟫| < ε * ⟪e₁, e₁⟫ ∧ |w 1 - ⟪e₂, g⟫| < ε * ⟪e₂, e₂⟫}
  have hU : IsOpen U := by
    show IsOpen ({w : Fin 2 → ℝ | |w 0 - ⟪e₁, g⟫| < ε * ⟪e₁, e₁⟫} ∩ {w | |w 1 - ⟪e₂, g⟫| < ε * ⟪e₂, e₂⟫})
    exact (isOpen_lt (by fun_prop) continuous_const).inter (isOpen_lt (by fun_prop) continuous_const)
  have hne : U.Nonempty :=
    ⟨![⟪e₁, g⟫, ⟪e₂, g⟫], ⟨by simpa using mul_pos hε h1, by simpa using mul_pos hε h2⟩⟩
  have hsub : U ⊆ f '' S := by
    rintro w ⟨hw0, hw1⟩
    set s := (w 0 - ⟪e₁, g⟫) / ⟪e₁, e₁⟫
    set t := (w 1 - ⟪e₂, g⟫) / ⟪e₂, e₂⟫
    have hs : |s| < ε := by
      rw [abs_div, abs_of_pos h1, div_lt_iff₀ h1]; exact hw0
    have ht : |t| < ε := by
      rw [abs_div, abs_of_pos h2, div_lt_iff₀ h2]; exact hw1
    refine ⟨g + s • e₁ + t • e₂, hS s t hs ht, ?_⟩
    have h21 : ⟪e₂, e₁⟫ = 0 := by rw [real_inner_comm]; exact h12
    funext i; fin_cases i
    · show ⟪e₁, g + s • e₁ + t • e₂⟫ = w 0
      rw [inner_add_right, inner_add_right, inner_smul_right, inner_smul_right, h12]
      simp only [s]; field_simp; ring
    · show ⟪e₂, g + s • e₁ + t • e₂⟫ = w 1
      rw [inner_add_right, inner_add_right, inner_smul_right, inner_smul_right, h21]
      simp only [t]; field_simp; ring
  exact hausdorff_two_pos f hf hU hne hsub

/-! ### The square on a ridge of the 600-cell -/

/-- The facets `(0, 0, 2, 2)` and `(−φ⁻¹, 0, √5, φ)` of the 600-cell; their common triangle has centre
`g6 / 6`, and `e1 / 2`, `e2 / 2` are two perpendicular directions in its plane. -/
def P0 : Fin 4 → ℤ × ℤ := ![(0, 0), (0, 0), (2, 0), (2, 0)]
def Q0 : Fin 4 → ℤ × ℤ := ![(1, -1), (0, 0), (-1, 2), (0, 1)]
def g6Z : Fin 4 → ℤ × ℤ := ![(3, -2), (0, 0), (0, 1), (3, -1)]
def e1Z : Fin 4 → ℤ × ℤ := ![(0, 0), (6, -4), (0, 0), (0, 0)]
def e2Z : Fin 4 → ℤ × ℤ := ![(6, -4), (0, 0), (6, -4), (-6, 4)]

/-- At the centre of the triangle only `P0` and `Q0` are tight (and they are constant along the plane); every
other facet gives at most `(−4 + 6φ)/6 < 1`. -/
def patchOK (z : Fin 4 → ℤ × ℤ) : Bool :=
  if gdot z g6Z == (6, 0) then (veq z P0 || veq z Q0) && gdot z e1Z == (0, 0) && gdot z e2Z == (0, 0)
  else gnonneg ((-4, 6) - gdot z g6Z)

theorem chk_patch : ((List.range 600).all fun k => patchOK (L8get k).toZ) = true := by decide +kernel

theorem chk_patch_facts : gdot P0 g6Z = (6, 0) ∧ gdot Q0 g6Z = (6, 0) ∧ gdot P0 Q0 = (-2, 6) ∧
    gdot e1Z e2Z = (0, 0) ∧ gdot e1Z e1Z = (52, -32) ∧ gdot e2Z e2Z = (156, -96) := by decide +kernel

theorem P0_mem : P0 ∈ cell600Z := vmem_sound (by decide +kernel)

theorem Q0_mem : Q0 ∈ cell600Z := vmem_sound (by decide +kernel)

attribute [local irreducible] L8get

/-- A point of the square. -/
noncomputable def sqPt (s t : ℝ) : R4 :=
  (1 / 6 : ℝ) • gvec g6Z + s • ((1 / 2 : ℝ) • gvec e1Z) + t • ((1 / 2 : ℝ) • gvec e2Z)

lemma inner_sqPt (z : Fin 4 → ℤ × ℤ) (s t : ℝ) : ⟪gvec z, sqPt s t⟫ =
    gval (gdot z g6Z) / 6 + s * ⟪gvec z, (1 / 2 : ℝ) • gvec e1Z⟫ + t * ⟪gvec z, (1 / 2 : ℝ) • gvec e2Z⟫ := by
  simp only [sqPt, inner_add_right, inner_smul_right, inner_gvec]
  ring

lemma s5_bounds : 2.236 < √5 ∧ √5 < 2.2362 :=
  ⟨(Real.lt_sqrt (by norm_num)).2 (by norm_num), (Real.sqrt_lt' (by norm_num)).2 (by norm_num)⟩

lemma half_e_norm {z : Fin 4 → ℤ × ℤ} {c : ℤ × ℤ} (hz : gdot z z = c) (h0 : 0 < gval c) (h1 : gval c ≤ 1) :
    ‖(1 / 2 : ℝ) • gvec z‖ ≤ 1 / 2 ∧ 0 < ⟪(1 / 2 : ℝ) • gvec z, (1 / 2 : ℝ) • gvec z⟫ := by
  have e : ⟪(1 / 2 : ℝ) • gvec z, (1 / 2 : ℝ) • gvec z⟫ = gval c / 4 := by
    rw [inner_smul_left, inner_smul_right, inner_gvec, hz]; simp; ring
  refine ⟨?_, by rw [e]; positivity⟩
  have hsq : ‖(1 / 2 : ℝ) • gvec z‖ ^ 2 ≤ (1 / 2) ^ 2 := by
    rw [← real_inner_self_eq_norm_sq, e]; linarith
  exact (pow_le_pow_iff_left₀ (norm_nonneg _) (by norm_num) (by norm_num)).1 hsq

lemma e_facts : ‖(1 / 2 : ℝ) • gvec e1Z‖ ≤ 1 / 2 ∧ 0 < ⟪(1 / 2 : ℝ) • gvec e1Z, (1 / 2 : ℝ) • gvec e1Z⟫ ∧
    ‖(1 / 2 : ℝ) • gvec e2Z‖ ≤ 1 / 2 ∧ 0 < ⟪(1 / 2 : ℝ) • gvec e2Z, (1 / 2 : ℝ) • gvec e2Z⟫ := by
  obtain ⟨-, -, -, -, h11, h22⟩ := chk_patch_facts
  obtain ⟨b1, b2⟩ := s5_bounds
  have g1 : 0 < gval (52, -32) ∧ gval (52, -32) ≤ 1 := by rw [gval_eq]; push_cast; constructor <;> linarith
  have g2 : 0 < gval (156, -96) ∧ gval (156, -96) ≤ 1 := by rw [gval_eq]; push_cast; constructor <;> linarith
  obtain ⟨a1, a2⟩ := half_e_norm h11 g1.1 g1.2
  obtain ⟨c1, c2⟩ := half_e_norm h22 g2.1 g2.2
  exact ⟨a1, a2, c1, c2⟩

lemma norm_L600_le {z : Fin 4 → ℤ × ℤ} (hz : NZ z) : ‖gvec z‖ ≤ 3 := by
  have h := inner_self_L600 hz
  rw [real_inner_self_eq_norm_sq] at h
  nlinarith [norm_nonneg (gvec z)]

/-- On the square only `P0` and `Q0` are tight. -/
lemma sqPt_facts {s t : ℝ} (hs : |s| < 1 / 100) (ht : |t| < 1 / 100) :
    sqPt s t ∈ cell600 ∧ act (fun z : {z // z ∈ cell600Z} => gvec z.1) (fun _ => 1) (sqPt s t) =
      {⟨P0, P0_mem⟩, ⟨Q0, Q0_mem⟩} := by
  obtain ⟨n1, -, n2, -⟩ := e_facts
  obtain ⟨hP6, hQ6, -, -, -, -⟩ := chk_patch_facts
  obtain ⟨b1, b2⟩ := s5_bounds
  have key : ∀ z, NZ z → (⟪gvec z, sqPt s t⟫ = 1 ∧ (z = P0 ∨ z = Q0)) ∨ (⟪gvec z, sqPt s t⟫ < 1 ∧
      gdot z g6Z ≠ (6, 0)) := by
    intro z hz
    have hc : patchOK z = true := by
      obtain ⟨k, hk, rfl⟩ := hz
      exact List.all_eq_true.1 chk_patch k (List.mem_range.2 hk)
    unfold patchOK at hc
    by_cases h6 : gdot z g6Z = (6, 0)
    · left
      rw [ite_eq_left (by rw [h6]; rfl)] at hc
      simp only [Bool.and_eq_true, Bool.or_eq_true, beq_iff_eq] at hc
      obtain ⟨⟨hpq, he1⟩, he2⟩ := hc
      refine ⟨?_, hpq.imp veq_sound veq_sound⟩
      rw [inner_sqPt, h6, inner_half_gvec, inner_half_gvec, he1, he2]; simp [gval]
    · right
      refine ⟨?_, h6⟩
      rw [ite_eq_right (by simpa using h6)] at hc
      have hg := gnonneg_sound hc
      rw [gval_sub] at hg
      have hb : gval (-4, 6) / 6 < 0.9515 := by rw [gval_eq]; push_cast; linarith
      have hz3 := norm_L600_le hz
      have i1 : |⟪gvec z, (1 / 2 : ℝ) • gvec e1Z⟫| ≤ 3 / 2 :=
        (abs_real_inner_le_norm _ _).trans (by nlinarith [norm_nonneg (gvec z), norm_nonneg ((1 / 2 : ℝ) • gvec e1Z)])
      have i2 : |⟪gvec z, (1 / 2 : ℝ) • gvec e2Z⟫| ≤ 3 / 2 :=
        (abs_real_inner_le_norm _ _).trans (by nlinarith [norm_nonneg (gvec z), norm_nonneg ((1 / 2 : ℝ) • gvec e2Z)])
      have m1 : s * ⟪gvec z, (1 / 2 : ℝ) • gvec e1Z⟫ ≤ 3 / 200 := by
        calc s * _ ≤ |s * ⟪gvec z, (1 / 2 : ℝ) • gvec e1Z⟫| := le_abs_self _
          _ = |s| * |⟪gvec z, (1 / 2 : ℝ) • gvec e1Z⟫| := abs_mul _ _
          _ ≤ 1 / 100 * (3 / 2) := by gcongr
          _ = 3 / 200 := by norm_num
      have m2 : t * ⟪gvec z, (1 / 2 : ℝ) • gvec e2Z⟫ ≤ 3 / 200 := by
        calc t * _ ≤ |t * ⟪gvec z, (1 / 2 : ℝ) • gvec e2Z⟫| := le_abs_self _
          _ = |t| * |⟪gvec z, (1 / 2 : ℝ) • gvec e2Z⟫| := abs_mul _ _
          _ ≤ 1 / 100 * (3 / 2) := by gcongr
          _ = 3 / 200 := by norm_num
      rw [inner_sqPt]
      have : gval (gdot z g6Z) / 6 ≤ gval (-4, 6) / 6 := by
        have h2 : gval ((-4 : ℤ), (6 : ℤ)) - gval (gdot z g6Z) ≥ 0 := hg
        linarith
      linarith
  refine ⟨fun r => ?_, ?_⟩
  · rcases key r.1 (mem_L600 r.2) with h | h
    · exact h.1.le
    · exact h.1.le
  · ext r
    simp only [act, Set.mem_ofPred_eq, Set.mem_insert_iff, Set.mem_singleton_iff]
    rcases key r.1 (mem_L600 r.2) with h | h
    · refine ⟨fun _ => ?_, fun _ => h.1⟩
      rcases h.2 with e | e
      · left; exact Subtype.ext e
      · right; exact Subtype.ext e
    · refine ⟨fun e => absurd e h.1.ne, ?_⟩
      rintro (e | e)
      · exact absurd (by rw [e]; exact hP6) h.2
      · exact absurd (by rw [e]; exact hQ6) h.2

lemma P0_Q0_indep : LinearIndependent ℝ ![gvec P0, gvec Q0] := by
  obtain ⟨-, -, hpq, -, -, -⟩ := chk_patch_facts
  obtain ⟨b1, b2⟩ := s5_bounds
  apply linIndep_pair_of_gram
  rw [inner_self_L600 (mem_L600 P0_mem), inner_self_L600 (mem_L600 Q0_mem), inner_gvec, hpq, gval_eq]
  push_cast
  nlinarith

lemma ridgeAngle_sqPt {s t : ℝ} (hs : |s| < 1 / 100) (ht : |t| < 1 / 100) :
    ridgeAngle cell600 (sqPt s t) = Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4)) := by
  obtain ⟨hmem, hact⟩ := sqPt_facts hs ht
  obtain ⟨-, -, hpq, -, -, -⟩ := chk_patch_facts
  unfold cell600 at hmem ⊢
  rw [ridgeAngle_sol _ _ hmem, hact, thetaH_pair (fun z : {z // z ∈ cell600Z} => gvec z.1)
    (i := ⟨P0, P0_mem⟩) (j := ⟨Q0, Q0_mem⟩) rfl P0_Q0_indep]
  exact adj_class (inner_self_L600 (mem_L600 P0_mem)) (inner_self_L600 (mem_L600 Q0_mem)) hpq

/-- The area of the ridge points of the 600-cell is positive. -/
lemma cell600_area_pos :
    0 < μH[2] {x | ridgeAngle cell600 x = Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4))} := by
  obtain ⟨n1, p1, n2, p2⟩ := e_facts
  obtain ⟨-, -, -, h12, -, -⟩ := chk_patch_facts
  have h12' : ⟪(1 / 2 : ℝ) • gvec e1Z, (1 / 2 : ℝ) • gvec e2Z⟫ = 0 := by
    rw [inner_smul_left, inner_smul_right, inner_gvec, h12]; simp [gval]
  apply area_pos_of_patch h12' p1 p2 (n1.trans (by norm_num)) (n2.trans (by norm_num))
    (by norm_num : (0 : ℝ) < 1 / 100)
  intro s t hs ht
  exact ridgeAngle_sqPt hs ht

theorem isPoly_cell600 : IsPoly cell600 := by
  have hv : ∀ z : Fin 4 → ℤ × ℤ, cell600Z.any (veq z) = true → ∀ x ∈ cell600, ⟪gvec z, x⟫ ≤ 1 :=
    fun z hz x hx => hx ⟨z, vmem_sound hz⟩
  refine ⟨bounded_of_coords4 1 ?_, {z // z ∈ cell600Z}, Fintype.ofFinite _, _, _, rfl⟩
  intro x hx k
  have a1 := hv ![(2, 0), (2, 0), (0, 0), (0, 0)] (by decide +kernel) x hx
  have a2 := hv ![(2, 0), (-2, 0), (0, 0), (0, 0)] (by decide +kernel) x hx
  have a3 := hv ![(-2, 0), (2, 0), (0, 0), (0, 0)] (by decide +kernel) x hx
  have a4 := hv ![(-2, 0), (-2, 0), (0, 0), (0, 0)] (by decide +kernel) x hx
  have a5 := hv ![(0, 0), (0, 0), (2, 0), (2, 0)] (by decide +kernel) x hx
  have a6 := hv ![(0, 0), (0, 0), (2, 0), (-2, 0)] (by decide +kernel) x hx
  have a7 := hv ![(0, 0), (0, 0), (-2, 0), (2, 0)] (by decide +kernel) x hx
  have a8 := hv ![(0, 0), (0, 0), (-2, 0), (-2, 0)] (by decide +kernel) x hx
  simp [gvec, gval, inner4] at a1 a2 a3 a4 a5 a6 a7 a8
  fin_cases k <;> refine abs_le.2 ⟨?_, ?_⟩ <;> simp <;> linarith

/-- **The regular 600-cell has non-zero Dehn–Hadwiger invariant.** -/
theorem dehnHadwiger_cell600_ne_zero : dehnHadwiger cell600 ≠ 0 := by
  rw [dehnHadwiger_cell600_eq]
  have hτ : (Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4)) : Angle) ≠ 0 := by
    rw [Ne, Submodule.Quotient.mk_eq_zero]; exact angle600_not_ratPi
  have hfin : μH[(finrank ℝ R4 - 2 : ℕ)]
      {x | ridgeAngle cell600 x = Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4))} ≠ ⊤ := by
    refine ne_top_of_le_ne_top (support_finite (fun z : {z // z ∈ cell600Z} => gvec z.1) (fun _ => 1)
      isPoly_cell600.1) (measure_mono ?_)
    intro x hx; rw [mem_ofPred_eq] at hx ⊢; show ridgeAngle cell600 x ≠ 0; rw [hx]; exact hτ
  have hpos := cell600_area_pos
  rw [← finrank_R4_sub] at hpos
  exact edgeTerm_ne_zero (ENNReal.toReal_pos hpos.ne' hfin).ne' angle600_not_ratPi

end DehnHadwiger
