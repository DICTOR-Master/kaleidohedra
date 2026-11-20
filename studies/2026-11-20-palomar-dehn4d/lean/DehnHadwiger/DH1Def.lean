/-
Dehn–Hadwiger study, part 1: the invariant of a set in codimension 2 (DICTO, 20 Nov 2026).

The Dehn Canon (studies 2026-11-19-lean-dehn-1 to -10, namespace `DehnCanon`) read the 3D Dehn invariant from
the set: at each point the cone of directions `tcone`, its lineality space `linSpace`, and where that space is a
line, the wedge angle around it. Here the same construction is made in any finite dimension `n`: a point is a
*ridge point* when the lineality space has dimension `n - 2` (codimension 2); the wedge angle is then measured in
the 2-dimensional orthogonal complement, exactly as before (`DehnCanon.wedgeAngle`, unchanged); and the invariant
adds `(n-2)`-dimensional Hausdorff measure ⊗ angle class. In dimension 4 the ridge points are the relative
interior points of the 2-faces, and the invariant is Σ area ⊗ dihedral angle (Hadwiger 1954).

Proved here: the cone-cut rule for the angle class in any dimension (`thetaH_cut`), from the Canon's
`wedgeAngle_split`; the 2D fact that a cone containing a full line of the complement has angle 0, π or 2π
(`wedgeAngle_mem_ratPi_of_perp`, the Canon's `wedgeAngle_mem_ratPi_of_line` with the dimension hypothesis put
on the complement); and two Hausdorff-measure facts on affine pieces (`hausdorff_affine_ne_top`,
`hausdorff_affine_null`). Credits: Mathlib's `isAddHaarMeasure_hausdorffMeasure`, `Isometry.hausdorffMeasure_image`,
`hausdorffMeasure_of_dimH_lt`, `Real.dimH_univ_eq_finrank`.
No `sorry`.
-/
import DehnCanon.Dehn2Local

open scoped RealInnerProductSpace
open Set MeasureTheory Module TensorProduct DehnCanon

namespace DehnHadwiger

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- The angle class in ℝ/ℚπ of a cone: its wedge angle around `linSpace` when that space has codimension 2,
else 0. -/
noncomputable def thetaH (T : Set E) : Angle :=
  if finrank ℝ (linSpace T) + 2 = finrank ℝ E then Submodule.Quotient.mk (wedgeAngle T (linSpace T)) else 0

/-- The dihedral angle class of the set `P` at the point `x` (0 unless `x` is a ridge point). -/
noncomputable def ridgeAngle (P : Set E) (x : E) : Angle := thetaH (tcone P x)

/-- **The Dehn–Hadwiger invariant of a set**, in ℝ ⊗[ℚ] (ℝ/ℚπ): Σ over angle classes θ of
((n−2)-dimensional measure of the ridge points with class θ) ⊗ θ, `n` the dimension of the space. -/
noncomputable def dehnHadwiger (P : Set E) : DehnSpace :=
  ∑ᶠ θ : Angle, (μH[(finrank ℝ E - 2 : ℕ)] {x | ridgeAngle P x = θ}).toReal ⊗ₜ[ℚ] θ

lemma thetaH_empty : thetaH (∅ : Set E) = 0 := by
  have hw : wedgeSet (∅ : Set E) (linSpace ∅) = ∅ := by ext w; simp [wedgeSet]
  unfold thetaH wedgeAngle
  rw [hw]; split_ifs <;> simp

lemma ridgeAngle_of_notMem {P : Set E} {x : E} (hx : x ∉ P) : ridgeAngle P x = 0 := by
  have h : tcone P x = ∅ := by
    rw [Set.eq_empty_iff_forall_notMem]; intro v hv; exact hx hv.1
  unfold ridgeAngle; rw [h, thetaH_empty]

/-- **A cone that contains a whole line of the 2-dimensional complement has angle 0, π or 2π.** -/
lemma wedgeAngle_mem_ratPi_of_perp {T : Set E} {K : Submodule ℝ E}
    (hV : finrank ℝ Kᗮ = 1 + 1)
    (hadd : ∀ v ∈ T, ∀ w ∈ T, v + w ∈ T) (hsmul : ∀ v ∈ T, ∀ s : ℝ, 0 < s → s • v ∈ T)
    {w0 : E} (hw0 : w0 ≠ 0) (hw0K : w0 ∈ Kᗮ) (hw0T : w0 ∈ T) (hw0T' : -w0 ∈ T) :
    wedgeAngle T K ∈ ratPi := by
  classical
  rw [mem_ratPi_iff]
  unfold wedgeAngle
  have : Fact (finrank ℝ Kᗮ = 1 + 1) := ⟨hV⟩
  set W0 : Kᗮ := ⟨w0, hw0K⟩ with hW0def
  have hW0 : W0 ≠ 0 := fun h => hw0 (congrArg Subtype.val h)
  have hf1 : finrank ℝ (ℝ ∙ W0)ᗮ = 1 := Submodule.finrank_orthogonal_span_singleton hW0
  obtain ⟨n, hnmem, hn0⟩ : ∃ n ∈ (ℝ ∙ W0)ᗮ, n ≠ 0 := by
    apply (Submodule.ne_bot_iff _).1
    intro h
    rw [h] at hf1
    simp at hf1
  have hnW : ⟪W0, n⟫ = 0 := Submodule.mem_orthogonal_singleton_iff_inner_right.1 hnmem
  have hf2 : finrank ℝ (ℝ ∙ n)ᗮ = 1 := Submodule.finrank_orthogonal_span_singleton hn0
  have hW0n : W0 ∈ (ℝ ∙ n)ᗮ :=
    Submodule.mem_orthogonal_singleton_iff_inner_right.2 (by rw [real_inner_comm]; exact hnW)
  have hline : ∀ v : Kᗮ, ⟪n, v⟫ = 0 → ∃ t : ℝ, t • W0 = v := by
    intro v hv
    have hv' : v ∈ (ℝ ∙ n)ᗮ := Submodule.mem_orthogonal_singleton_iff_inner_right.2 hv
    have hne : (⟨W0, hW0n⟩ : (ℝ ∙ n)ᗮ) ≠ 0 := fun h => hW0 (congrArg Subtype.val h)
    obtain ⟨t, ht⟩ := (finrank_eq_one_iff_of_nonzero' _ hne).1 hf2 ⟨v, hv'⟩
    exact ⟨t, congrArg Subtype.val ht⟩
  have h0T : (0 : E) ∈ T := by
    have := hadd _ hw0T _ hw0T'
    rwa [add_neg_cancel] at this
  have hlineT : ∀ t : ℝ, t • w0 ∈ T := by
    intro t
    rcases lt_trichotomy t 0 with ht | ht | ht
    · have := hsmul _ hw0T' (-t) (by linarith)
      rwa [smul_neg, neg_smul, neg_neg] at this
    · rw [ht, zero_smul]; exact h0T
    · exact hsmul _ hw0T t ht
  have claimA : ∀ v0 : Kᗮ, (v0 : E) ∈ T → ∀ v : Kᗮ, 0 < ⟪n, v⟫ / ⟪n, v0⟫ → (v : E) ∈ T := by
    intro v0 hv0 v hpos
    have hne : ⟪n, v0⟫ ≠ 0 := by
      intro h; rw [h, div_zero] at hpos; exact lt_irrefl _ hpos
    obtain ⟨t, ht⟩ := hline (v - (⟪n, v⟫ / ⟪n, v0⟫) • v0) (by
      rw [inner_sub_right, inner_smul_right, div_mul_cancel₀ _ hne, sub_self])
    have h1 : v = (⟪n, v⟫ / ⟪n, v0⟫) • v0 + t • W0 := by rw [ht]; abel
    have hv : (v : E) = (⟪n, v⟫ / ⟪n, v0⟫) • (v0 : E) + t • w0 := by
      calc (v : E) = (((⟪n, v⟫ / ⟪n, v0⟫) • v0 + t • W0 : Kᗮ) : E) := congrArg Subtype.val h1
        _ = (⟪n, v⟫ / ⟪n, v0⟫) • (v0 : E) + t • w0 := rfl
    rw [hv]
    exact hadd _ (hsmul _ hv0 _ hpos) _ (hlineT t)
  set S := wedgeSet T K with hS
  set B : Set Kᗮ := Metric.ball (0 : Kᗮ) 1 with hB
  let Hp : Set Kᗮ := {v | 0 < ⟪n, v⟫}
  let Hn : Set Kᗮ := {v | ⟪n, v⟫ < 0}
  have hHp : MeasurableSet Hp := (isOpen_lt continuous_const (by fun_prop)).measurableSet
  have hHn : MeasurableSet Hn := (isOpen_lt (by fun_prop) continuous_const).measurableSet
  let N : Submodule ℝ Kᗮ := (ℝ ∙ n)ᗮ
  have hN : volume (N : Set Kᗮ) = 0 := by
    apply Measure.addHaar_submodule
    intro h
    have h1 : n ∈ N := by rw [h]; trivial
    have h2 : ⟪n, n⟫ = 0 := Submodule.mem_orthogonal_singleton_iff_inner_right.1 h1
    exact hn0 (inner_self_eq_zero.1 h2)
  have hsplit : ∀ X : Set Kᗮ, volume X = volume (X ∩ Hp) + volume (X ∩ Hn) := by
    intro X
    have h1 := measure_inter_add_sdiff (μ := volume) X hHp
    have h2 := measure_inter_add_sdiff (μ := volume) (X \ Hp) hHn
    have h3 : volume ((X \ Hp) \ Hn) = 0 := by
      apply measure_mono_null _ hN
      intro v hv
      have a1 : ¬ 0 < ⟪n, v⟫ := hv.1.2
      have a2 : ¬ ⟪n, v⟫ < 0 := hv.2
      exact Submodule.mem_orthogonal_singleton_iff_inner_right.2
        (le_antisymm (not_lt.1 a1) (not_lt.1 a2))
    have h4 : (X \ Hp) ∩ Hn = X ∩ Hn := by
      ext v; constructor
      · rintro ⟨⟨hx, -⟩, hn⟩; exact ⟨hx, hn⟩
      · rintro ⟨hx, hn⟩; exact ⟨⟨hx, fun hp => lt_asymm (show 0 < ⟪n, v⟫ from hp) (show ⟪n, v⟫ < 0 from hn)⟩, hn⟩
    rw [← h1, ← h2, h3, add_zero, h4]
  have hBm : MeasurableSet B := Metric.isOpen_ball.measurableSet
  have hsym : volume (B ∩ Hn) = volume (B ∩ Hp) := by
    have hmp := (LinearIsometryEquiv.neg ℝ (E := Kᗮ)).measurePreserving
    have h1 := hmp.measure_preimage (hBm.inter hHp).nullMeasurableSet
    rw [← h1]
    congr 1
    ext v
    have hb : (-v ∈ B) ↔ v ∈ B := by
      rw [hB, Metric.mem_ball, Metric.mem_ball, dist_zero_right, dist_zero_right, norm_neg]
    constructor
    · rintro ⟨h2, h3⟩
      refine ⟨hb.2 h2, ?_⟩
      show 0 < ⟪n, -v⟫
      rw [inner_neg_right]; have h3' : ⟪n, v⟫ < 0 := h3; linarith
    · rintro ⟨h2, h3⟩
      have h3' : 0 < ⟪n, -v⟫ := h3
      rw [inner_neg_right] at h3'
      exact ⟨hb.1 h2, show ⟪n, v⟫ < 0 by linarith⟩
  have hSB : S ⊆ B := wedgeSet_subset_ball T K
  have dp : S ∩ Hp = B ∩ Hp ∨ S ∩ Hp = ∅ := by
    by_cases h : ∃ v0 : Kᗮ, (v0 : E) ∈ T ∧ 0 < ⟪n, v0⟫
    · obtain ⟨v0, hv0, hpos⟩ := h
      left
      ext v; constructor
      · rintro ⟨hs, hp⟩; exact ⟨hSB hs, hp⟩
      · rintro ⟨hb, hp⟩
        refine ⟨⟨claimA v0 hv0 v (div_pos hp hpos), ?_⟩, hp⟩
        rw [hB, Metric.mem_ball, dist_zero_right] at hb; exact hb
    · right
      rw [Set.eq_empty_iff_forall_notMem]
      rintro v ⟨hs, hp⟩
      exact h ⟨v, hs.1, hp⟩
  have dn : S ∩ Hn = B ∩ Hn ∨ S ∩ Hn = ∅ := by
    by_cases h : ∃ v0 : Kᗮ, (v0 : E) ∈ T ∧ ⟪n, v0⟫ < 0
    · obtain ⟨v0, hv0, hneg⟩ := h
      left
      ext v; constructor
      · rintro ⟨hs, hp⟩; exact ⟨hSB hs, hp⟩
      · rintro ⟨hb, hp⟩
        refine ⟨⟨claimA v0 hv0 v (div_pos_of_neg_of_neg hp hneg), ?_⟩, hp⟩
        rw [hB, Metric.mem_ball, dist_zero_right] at hb; exact hb
    · right
      rw [Set.eq_empty_iff_forall_notMem]
      rintro v ⟨hs, hp⟩
      exact h ⟨v, hs.1, hp⟩
  have hBpos : 0 < volume B := Metric.measure_ball_pos volume _ one_pos
  have hBfin : volume B ≠ ⊤ := measure_ball_lt_top.ne
  have hBsplit := hsplit B
  rw [hsym] at hBsplit
  have hSsplit := hsplit S
  have hfin : volume (B ∩ Hp) ≠ ⊤ := ((measure_mono inter_subset_left).trans_lt hBfin.lt_top).ne
  have hfinn : volume (B ∩ Hn) ≠ ⊤ := ((measure_mono inter_subset_left).trans_lt hBfin.lt_top).ne
  have hm : (volume B).toReal = (volume (B ∩ Hp)).toReal + (volume (B ∩ Hp)).toReal := by
    rw [← ENNReal.toReal_add hfin hfin, ← hBsplit]
  have hmpos : 0 < (volume B).toReal := ENNReal.toReal_pos hBpos.ne' hBfin
  have hSr : (volume S).toReal = (volume (S ∩ Hp)).toReal + (volume (S ∩ Hn)).toReal := by
    rw [← ENNReal.toReal_add, ← hSsplit]
    · exact ((measure_mono (inter_subset_left.trans hSB)).trans_lt hBfin.lt_top).ne
    · exact ((measure_mono (inter_subset_left.trans hSB)).trans_lt hBfin.lt_top).ne
  have hx : (volume (S ∩ Hp)).toReal = (volume (B ∩ Hp)).toReal ∨ (volume (S ∩ Hp)).toReal = 0 := by
    rcases dp with e | e
    · left; rw [e]
    · right; rw [e]; simp
  have hy : (volume (S ∩ Hn)).toReal = (volume (B ∩ Hp)).toReal ∨ (volume (S ∩ Hn)).toReal = 0 := by
    rcases dn with e | e
    · left; rw [e, hsym]
    · right; rw [e]; simp
  rw [hSr, hm]
  rw [hm] at hmpos
  generalize (volume (B ∩ Hp)).toReal = h at *
  have hh : 0 < h := by linarith
  rcases hx with ex | ex <;> rcases hy with ey | ey <;> rw [ex, ey]
  · refine ⟨2, ?_⟩
    rw [div_self (by positivity)]; push_cast; ring
  · refine ⟨1, ?_⟩
    have : (h + 0) / (h + h) = 1 / 2 := by
      rw [div_eq_div_iff (by positivity) (by norm_num)]; ring
    rw [this]; push_cast; ring
  · refine ⟨1, ?_⟩
    have : (0 + h) / (h + h) = 1 / 2 := by
      rw [div_eq_div_iff (by positivity) (by norm_num)]; ring
    rw [this]; push_cast; ring
  · refine ⟨0, ?_⟩
    simp

omit [MeasurableSpace E] [BorelSpace E] in
/-- **The angle class under a cut through the point**, any dimension. `T` is the cone at a point, `L` its
lineality space; cut the cone by the hyperplane with normal `c` through the point. Unless the point is a ridge
point whose ridge crosses the hyperplane (`L` of codimension 2 and not inside it), the angle class is the sum of
the angle classes of the two parts. -/
lemma thetaH_cut [MeasurableSpace E] [BorelSpace E] {T : Set E} {L : Submodule ℝ E}
    (hL : ∀ v, (v ∈ T ∧ -v ∈ T) ↔ v ∈ L)
    (hadd : ∀ v ∈ T, ∀ w ∈ T, v + w ∈ T) (hsmul : ∀ v ∈ T, ∀ s : ℝ, 0 < s → s • v ∈ T)
    {c : E} (hc : c ≠ 0) (hexc : ¬ (finrank ℝ L + 2 = finrank ℝ E ∧ ¬ L ≤ (ℝ ∙ c)ᗮ)) :
    thetaH T = thetaH (T ∩ {v | ⟪c, v⟫ ≤ 0}) + thetaH (T ∩ {v | ⟪-c, v⟫ ≤ 0}) := by
  have hLT : linSpace T = L := linSpace_eq_of hL
  have hLp : linSpace (T ∩ {v | ⟪c, v⟫ ≤ 0}) = L ⊓ (ℝ ∙ c)ᗮ := by
    apply linSpace_eq_of
    intro v
    rw [Submodule.mem_inf, Submodule.mem_orthogonal_singleton_iff_inner_right, ← hL v]
    constructor
    · rintro ⟨⟨h1, h2⟩, ⟨h3, h4⟩⟩
      have h2' : ⟪c, v⟫ ≤ 0 := h2
      have h4' : ⟪c, -v⟫ ≤ 0 := h4
      rw [inner_neg_right] at h4'
      exact ⟨⟨h1, h3⟩, by linarith⟩
    · rintro ⟨⟨h1, h3⟩, h0⟩
      refine ⟨⟨h1, ?_⟩, ⟨h3, ?_⟩⟩
      · show ⟪c, v⟫ ≤ 0
        rw [h0]
      · show ⟪c, -v⟫ ≤ 0
        rw [inner_neg_right, h0, neg_zero]
  have hLm : linSpace (T ∩ {v | ⟪-c, v⟫ ≤ 0}) = L ⊓ (ℝ ∙ c)ᗮ := by
    apply linSpace_eq_of
    intro v
    rw [Submodule.mem_inf, Submodule.mem_orthogonal_singleton_iff_inner_right, ← hL v]
    constructor
    · rintro ⟨⟨h1, h2⟩, ⟨h3, h4⟩⟩
      have h2' : ⟪-c, v⟫ ≤ 0 := h2
      have h4' : ⟪-c, -v⟫ ≤ 0 := h4
      rw [inner_neg_left] at h2'
      rw [inner_neg_left, inner_neg_right, neg_neg] at h4'
      exact ⟨⟨h1, h3⟩, by linarith⟩
    · rintro ⟨⟨h1, h3⟩, h0⟩
      refine ⟨⟨h1, ?_⟩, ⟨h3, ?_⟩⟩
      · show ⟪-c, v⟫ ≤ 0
        rw [inner_neg_left, h0, neg_zero]
      · show ⟪-c, -v⟫ ≤ 0
        rw [inner_neg_left, inner_neg_right, neg_neg, h0]
  unfold thetaH
  rw [hLT, hLp, hLm]
  by_cases hsub : L ≤ (ℝ ∙ c)ᗮ
  · rw [inf_eq_left.2 hsub]
    by_cases h1 : finrank ℝ L + 2 = finrank ℝ E
    · simp only [h1, ↓reduceIte]
      rw [← Submodule.Quotient.mk_add]
      have hcL : c ∈ Lᗮ := by
        rw [Submodule.mem_orthogonal']
        intro u hu
        exact Submodule.mem_orthogonal_singleton_iff_inner_right.1 (hsub hu)
      rw [wedgeAngle_split T L hc hcL]
    · simp only [h1, ↓reduceIte, add_zero]
  · have h1 : ¬ finrank ℝ L + 2 = finrank ℝ E := fun h => hexc ⟨h, hsub⟩
    simp only [h1, ↓reduceIte]
    by_cases h2 : finrank ℝ ↥(L ⊓ (ℝ ∙ c)ᗮ) + 2 = finrank ℝ E
    · simp only [h2, ↓reduceIte]
      rw [← Submodule.Quotient.mk_add]
      symm
      rw [Submodule.Quotient.mk_eq_zero]
      have hcL : c ∈ (L ⊓ (ℝ ∙ c)ᗮ)ᗮ := by
        rw [Submodule.mem_orthogonal']
        intro u hu
        exact Submodule.mem_orthogonal_singleton_iff_inner_right.1 hu.2
      rw [← wedgeAngle_split T _ hc hcL]
      obtain ⟨v1, hv1L, hv1c⟩ : ∃ v1 ∈ L, ⟪c, v1⟫ ≠ 0 := by
        by_contra hno
        push Not at hno
        exact hsub fun v hv => Submodule.mem_orthogonal_singleton_iff_inner_right.2 (hno v hv)
      set M : Submodule ℝ E := L ⊓ (ℝ ∙ c)ᗮ with hM
      have hpM : M.starProjection v1 ∈ M := Submodule.starProjection_apply_mem M v1
      set w0 : E := v1 - M.starProjection v1 with hw0def
      have hw0L : w0 ∈ L := L.sub_mem hv1L (Submodule.mem_inf.1 hpM).1
      have hw0c : ⟪c, w0⟫ = ⟪c, v1⟫ := by
        rw [hw0def, inner_sub_right,
          Submodule.mem_orthogonal_singleton_iff_inner_right.1 (Submodule.mem_inf.1 hpM).2, sub_zero]
      have hw0 : w0 ≠ 0 := by
        intro h; rw [h, inner_zero_right] at hw0c; exact hv1c hw0c.symm
      have hw0K : w0 ∈ Mᗮ := Submodule.sub_starProjection_mem_orthogonal v1
      have hV : finrank ℝ Mᗮ = 1 + 1 := by
        have := Submodule.finrank_add_finrank_orthogonal M; omega
      have hw0T := (hL w0).2 hw0L
      exact wedgeAngle_mem_ratPi_of_perp hV hadd hsmul hw0 hw0K hw0T.1 hw0T.2
    · simp only [h2, ↓reduceIte, add_zero]

/-! ### Hausdorff measure of pieces of affine subspaces -/

omit [FiniteDimensional ℝ E] in
/-- A bounded set inside a translate of a subspace `W` has finite `dim W`-dimensional Hausdorff measure. -/
lemma hausdorff_affine_ne_top [FiniteDimensional ℝ E] (W : Submodule ℝ E) (x0 : E) {S : Set E}
    (hS : Bornology.IsBounded S) (hsub : ∀ x ∈ S, x - x0 ∈ W) :
    μH[(finrank ℝ W : ℝ)] S ≠ ⊤ := by
  let f : W → E := fun w => (w : E) + x0
  have hf : Isometry f := (isometry_add_right x0).comp isometry_subtype_coe
  let T : Set W := {w | f w ∈ S}
  have hST : S = f '' T := by
    ext x; constructor
    · intro hx
      refine ⟨⟨x - x0, hsub x hx⟩, ?_, ?_⟩
      · show (x - x0) + x0 ∈ S
        rw [sub_add_cancel]; exact hx
      · show (x - x0) + x0 = x
        rw [sub_add_cancel]
    · rintro ⟨w, hw, rfl⟩; exact hw
  have hT : Bornology.IsBounded T := by
    obtain ⟨M, hM⟩ := isBounded_iff_forall_norm_le.1 hS
    refine isBounded_iff_forall_norm_le.2 ⟨M + ‖x0‖, fun w hw => ?_⟩
    have h1 := hM _ hw
    have h2 : ‖(w : E)‖ ≤ ‖(w : E) + x0‖ + ‖x0‖ := by
      calc ‖(w : E)‖ = ‖((w : E) + x0) - x0‖ := by rw [add_sub_cancel_right]
        _ ≤ ‖(w : E) + x0‖ + ‖x0‖ := norm_sub_le _ _
    rw [Submodule.norm_coe] at *
    linarith
  rw [hST, hf.hausdorffMeasure_image (Or.inl (Nat.cast_nonneg _))]
  have hc : IsCompact (closure T) := hT.isCompact_closure
  exact ((measure_mono subset_closure).trans_lt hc.measure_lt_top).ne

omit [FiniteDimensional ℝ E] in
/-- A set inside a translate of a subspace `W` has zero `d`-dimensional Hausdorff measure when `dim W < d`. -/
lemma hausdorff_affine_null [FiniteDimensional ℝ E] (W : Submodule ℝ E) (x0 : E) {S : Set E}
    (hsub : ∀ x ∈ S, x - x0 ∈ W) {d : ℕ} (hd : finrank ℝ W < d) :
    μH[(d : ℝ)] S = 0 := by
  let f : W → E := fun w => (w : E) + x0
  have hf : Isometry f := (isometry_add_right x0).comp isometry_subtype_coe
  have hS : S ⊆ f '' univ := by
    intro x hx
    refine ⟨⟨x - x0, hsub x hx⟩, mem_univ _, ?_⟩
    show (x - x0) + x0 = x
    rw [sub_add_cancel]
  have hdim : dimH S < (d : NNReal) := by
    calc dimH S ≤ dimH (f '' univ) := dimH_mono hS
      _ ≤ dimH (univ : Set W) := hf.lipschitzWith.dimH_image_le _
      _ = finrank ℝ W := Real.dimH_univ_eq_finrank W
      _ < (d : NNReal) := by exact_mod_cast hd
  have := hausdorffMeasure_of_dimH_lt hdim
  simpa using this

end DehnHadwiger
