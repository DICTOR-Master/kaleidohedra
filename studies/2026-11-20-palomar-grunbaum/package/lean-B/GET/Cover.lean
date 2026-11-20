module

public import GET.Tiling

@[expose] public section

/-!
# The translates of GET B cover space

The volume of `PB` equals the covolume of the lattice (`20 + 32 φ`), and distinct translates meet in null sets. By
Mathlib's fundamental domain of the lattice, the union `U` of the translates meets the fundamental domain in a set of
full measure, so the complement of `U`, which is invariant under the lattice, is null. Only finitely many translates
meet a ball, so `U` is closed; an open null set is empty, hence `U` is all of space.
-/

namespace GET

open ZPhi GrunbaumK10 Set MeasureTheory
open scoped Pointwise

/-! ## Volumes -/

theorem B_cell_dets : ∀ i : Fin 16,
    pos (D (CB i).i (CB i).j (CB i).k) = true ∨ pos (-(D (CB i).i (CB i).j (CB i).k)) = true := by
  decide +kernel

theorem B_cell_sum : lsum ((List.finRange 16).map fun i => cellVol (CB i)) = δB := by decide +kernel

theorem volume_cellSet (c : Cell) : volume (cellSet c) = ENNReal.ofReal |toReal (D c.i c.j c.k)| :=
  volume_cell _ _ _ _

theorem measurableSet_PB : MeasurableSet PB :=
  MeasurableSet.iUnion fun i => (isCompact_cellSet _).isClosed.measurableSet

theorem volume_PB : volume PB = ENNReal.ofReal (toReal δB) := by
  rw [PB, measure_iUnion₀ (fun i j hij => PB_cells_null hij)
    (fun i => (isCompact_cellSet _).isClosed.measurableSet.nullMeasurableSet), tsum_fintype]
  simp_rw [volume_cellSet]
  rw [← ENNReal.ofReal_sum_of_nonneg (fun _ _ => abs_nonneg _), ← B_cell_sum, toReal_lsum, List.map_map,
    Fin.sum_univ_def]
  congr 2
  apply List.map_congr_left
  intro i _
  simp only [Function.comp_apply, cellVol]
  rw [toReal_zabs (B_cell_dets i)]

/-! ## The lattice as a `ℤ`-span -/

theorem bB_eq : bB = ![ev (posn (BB 0)), ev (posn (BB 1)), ev (posn (BB 2))] := by
  funext r; fin_cases r <;> rfl

theorem det_BB : det3 (posn (BB 0)) (posn (BB 1)) (posn (BB 2)) ≠ 0 ∧
    zabs (det3 (posn (BB 0)) (posn (BB 1)) (posn (BB 2))) = δB ∧
    (pos (det3 (posn (BB 0)) (posn (BB 1)) (posn (BB 2))) = true ∨
      pos (-(det3 (posn (BB 0)) (posn (BB 1)) (posn (BB 2)))) = true) := by decide +kernel

theorem bB_li : LinearIndependent ℝ bB := by
  rw [bB_eq]; exact linearIndependent_ev3 det_BB.1

/-- the lattice basis as a `Basis` -/
noncomputable def bbB : Module.Basis (Fin 3) ℝ Space :=
  basisOfLinearIndependentOfCardEqFinrank bB_li (by simp)

theorem bbB_coe : ⇑bbB = bB := coe_basisOfLinearIndependentOfCardEqFinrank _ _

/-- the lattice as an additive subgroup -/
noncomputable abbrev GB : AddSubgroup Space := (Submodule.span ℤ (range bbB)).toAddSubgroup

theorem lattice_eq : lattice bB = (GB : Set Space) := by
  unfold lattice
  rw [GB, bbB_coe, Submodule.span_int_eq_addSubgroupClosure]

theorem volume_F0 : volume (ZSpan.fundamentalDomain bbB) = ENNReal.ofReal (toReal δB) := by
  rw [measure_congr (ZSpan.fundamentalDomain_ae_parallelepiped bbB volume), bbB_coe]
  have h := volume_vadd_parallelepiped 0 bB
  rw [zero_vadd] at h
  rw [h]
  congr 1
  have e : (Matrix.of fun i j => bB j i) = (rmat (posn (BB 0)) (posn (BB 1)) (posn (BB 2))).transpose := by
    ext i j; fin_cases j <;> rfl
  rw [e, Matrix.det_transpose, toReal_det3, ← toReal_zabs det_BB.2.2, det_BB.2.1]

/-! ## Translates meet in null sets -/

theorem translates_null {s t : Space} (hs : s ∈ lattice bB) (ht : t ∈ lattice bB) (hst : s ≠ t) :
    volume ((s +ᵥ PB) ∩ (t +ᵥ PB)) = 0 := by
  obtain ⟨xs, rfl⟩ := mem_lattice.mp hs
  obtain ⟨xt, rfl⟩ := mem_lattice.mp ht
  have e : (lat xs +ᵥ PB) ∩ (lat xt +ᵥ PB) = lat xs +ᵥ (PB ∩ (lat (xt - xs) +ᵥ PB)) := by
    rw [Set.vadd_set_inter, vadd_vadd, lat_sub, add_sub_cancel]
  rw [e, measure_vadd]
  apply PB_inter_null
  intro h0
  apply hst
  rw [show xt = xs by rw [← sub_eq_zero]; exact h0]

/-! ## Local finiteness -/

theorem isCompact_PB : IsCompact PB := isCompact_iUnion fun i => isCompact_cellSet _

theorem PB_bounded : ∃ R, ∀ w ∈ PB, ‖w‖ ≤ R := isCompact_PB.isBounded.exists_norm_le

instance : Countable GB := by
  have : Function.Surjective (fun x : Fin 3 → ℤ =>
      (⟨lat x, by rw [← SetLike.mem_coe, ← lattice_eq]; exact lat_mem x⟩ : GB)) := by
    rintro ⟨g, hg⟩
    obtain ⟨x, hx⟩ := mem_lattice.mp (by rw [lattice_eq]; exact hg)
    exact ⟨x, Subtype.ext hx.symm⟩
  exact this.countable

theorem coeff_le_of_norm {x : Fin 3 → ℤ} {K : ℝ} (h : ‖lat x‖ ≤ K) (r : Fin 3) :
    |(x r : ℝ)| * toReal δB ≤ ‖ev (mB r)‖ * K := by
  have := abs_real_inner_le_norm (ev (mB r)) (lat x)
  rw [inner_mB_lat, abs_mul, abs_of_pos δB_pos] at this
  calc |(x r : ℝ)| * toReal δB ≤ ‖ev (mB r)‖ * ‖lat x‖ := this
    _ ≤ ‖ev (mB r)‖ * K := by gcongr

theorem translates_locallyFinite : LocallyFinite fun g : GB => (g : Space) +ᵥ PB := by
  intro y
  obtain ⟨R, hR⟩ := PB_bounded
  refine ⟨Metric.ball y 1, Metric.ball_mem_nhds y one_pos, ?_⟩
  set K := ‖y‖ + 1 + R
  set M := (‖ev (mB 0)‖ + ‖ev (mB 1)‖ + ‖ev (mB 2)‖) * K / toReal δB
  set N : ℤ := ⌈M⌉
  apply Set.Finite.of_finite_image (f := Subtype.val) _ Subtype.val_injective.injOn
  apply ((Set.finite_Icc (-fun _ => N) (fun _ => N)).image lat).subset
  rintro _ ⟨g, ⟨z, hz1, hz2⟩, rfl⟩
  obtain ⟨w, hw, rfl⟩ := Set.mem_vadd_set.mp hz1
  have hg : (g : Space) ∈ lattice bB := by rw [lattice_eq]; exact g.2
  obtain ⟨x, hx⟩ := mem_lattice.mp hg
  refine ⟨x, ?_, hx.symm⟩
  have hgK : ‖lat x‖ ≤ K := by
    rw [← hx]
    have h1 : ‖((g : Space) +ᵥ w) - y‖ < 1 := by
      have := Metric.mem_ball.mp hz2; rwa [dist_eq_norm] at this
    have h2 := hR w hw
    have : (g : Space) = (((g : Space) +ᵥ w) - y) + y - w := by rw [vadd_eq_add]; abel
    rw [this]
    calc ‖(((g : Space) +ᵥ w) - y) + y - w‖ ≤ ‖(((g : Space) +ᵥ w) - y) + y‖ + ‖w‖ := norm_sub_le _ _
      _ ≤ ‖((g : Space) +ᵥ w) - y‖ + ‖y‖ + ‖w‖ := by gcongr; exact norm_add_le _ _
      _ ≤ K := by simp only [K]; linarith
  have hK : 0 ≤ K := le_trans (norm_nonneg _) hgK
  have hM : ∀ r, |(x r : ℝ)| ≤ M := by
    intro r
    have := coeff_le_of_norm hgK r
    have hδ := δB_pos
    rw [le_div_iff₀ hδ]
    have hs : ‖ev (mB r)‖ ≤ ‖ev (mB 0)‖ + ‖ev (mB 1)‖ + ‖ev (mB 2)‖ := by
      fin_cases r <;> simp <;> linarith [norm_nonneg (ev (mB 0)), norm_nonneg (ev (mB 1)),
        norm_nonneg (ev (mB 2))]
    nlinarith
  constructor
  · intro r
    have h1 := (abs_le.mp (hM r)).1
    have h2 : -(N : ℝ) ≤ (x r : ℝ) := by linarith [Int.le_ceil M]
    show -N ≤ x r
    exact_mod_cast h2
  · intro r
    have h1 := (abs_le.mp (hM r)).2
    have h2 : (x r : ℝ) ≤ N := by linarith [Int.le_ceil M]
    show x r ≤ N
    exact_mod_cast h2

theorem isClosed_union_translates : IsClosed (⋃ g : GB, (g : Space) +ᵥ PB) :=
  translates_locallyFinite.isClosed_iUnion fun g => by
    rw [← Set.image_vadd]; exact (isCompact_PB.image (continuous_const.add continuous_id)).isClosed

/-! ## Covering -/

/-- **the lattice translates of GET B cover space** -/
theorem PB_cover : (⋃ t ∈ lattice bB, t +ᵥ PB) = univ := by
  have hF : IsAddFundamentalDomain GB (ZSpan.fundamentalDomain bbB) volume :=
    ZSpan.isAddFundamentalDomain' bbB volume
  set F0 := ZSpan.fundamentalDomain bbB
  set U := ⋃ g : GB, (g : Space) +ᵥ PB with hUdef
  have hUm : MeasurableSet U := isClosed_union_translates.measurableSet
  -- the pieces of the translates in `F0` are a.e. disjoint, and their measures add up to `vol PB`
  have hpieces : volume (⋃ g : GB, (g +ᵥ PB) ∩ F0) = volume PB := by
    rw [measure_iUnion₀, ← hF.measure_eq_tsum PB]
    · intro g g' hgg'
      apply measure_mono_null (t := ((g : Space) +ᵥ PB) ∩ ((g' : Space) +ᵥ PB))
      · intro z hz; exact ⟨hz.1.1, hz.2.1⟩
      · apply translates_null
        · rw [lattice_eq]; exact g.2
        · rw [lattice_eq]; exact g'.2
        · intro h; exact hgg' (Subtype.ext h)
    · intro g
      exact (measurableSet_PB.const_vadd _).nullMeasurableSet.inter hF.nullMeasurableSet
  have hF0fin : volume F0 ≠ ⊤ := by rw [volume_F0]; exact ENNReal.ofReal_ne_top
  have hsub : (⋃ g : GB, (g +ᵥ PB) ∩ F0) ⊆ F0 ∩ U := by
    intro z hz
    obtain ⟨g, hg1, hg2⟩ := mem_iUnion.mp hz
    exact ⟨hg2, mem_iUnion.mpr ⟨g, hg1⟩⟩
  have hge : volume F0 ≤ volume (F0 ∩ U) := by
    calc volume F0 = volume PB := by rw [volume_F0, volume_PB]
      _ = _ := hpieces.symm
      _ ≤ _ := measure_mono hsub
  have hdiff : volume (F0 \ U) = 0 := by
    have h := measure_inter_add_sdiff (μ := volume) F0 hUm
    have heq : volume (F0 ∩ U) = volume F0 := le_antisymm (measure_mono inter_subset_left) hge
    rw [heq] at h
    exact (ENNReal.add_right_inj hF0fin).mp (h.trans (add_zero _).symm)
  have hinv : ∀ g : GB, g +ᵥ Uᶜ = Uᶜ := by
    intro g
    have hgU : (g : Space) +ᵥ U = U := by
      rw [hUdef, Set.vadd_set_iUnion]
      ext z
      simp only [mem_iUnion, vadd_vadd]
      constructor
      · rintro ⟨h, hz⟩; exact ⟨g + h, by simpa using hz⟩
      · rintro ⟨h, hz⟩; exact ⟨-g + h, by simpa using hz⟩
    show (g : Space) +ᵥ Uᶜ = Uᶜ
    rw [Set.vadd_set_compl, hgU]
  have hV0 : volume Uᶜ = 0 :=
    hF.measure_zero_of_invariant Uᶜ hinv (by rw [inter_comm, ← Set.sdiff_eq]; exact hdiff)
  have hVe : Uᶜ = ∅ := (isClosed_union_translates.isOpen_compl.measure_eq_zero_iff volume).mp hV0
  have hU : U = univ := compl_empty_iff.mp hVe
  ext z
  simp only [mem_univ, iff_true, mem_iUnion]
  have : z ∈ U := hU ▸ mem_univ z
  obtain ⟨g, hg⟩ := mem_iUnion.mp this
  exact ⟨g, by rw [lattice_eq]; exact g.2, hg⟩

end GET
