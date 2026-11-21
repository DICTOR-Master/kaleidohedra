/-
Alexandrov's theorem on prescribed curvature, polyhedral case: the comparison lemma.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Basic

/-!
# The comparison lemma

If `ρ ≤ r` on every ray, with equality on a nonempty set `I` of rays and strict inequality on a
nonempty set `J`, and every cell of `r` has positive volume, then some corner in `I` has a strictly
larger cell for `ρ` than for `r` (`exists_cell_volume_lt`).
This is the maximum principle behind uniqueness.
-/

open MeasureTheory Set Metric Finset
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ}

/-- A connected set that meets an open set `A` without lying inside it has a point of the
closure of `A` outside `A`. -/
lemma exists_mem_closure_not_mem {X A : Set E3} (hX : IsPreconnected X) (hA : IsOpen A)
    (h1 : (X ∩ A).Nonempty) (h2 : ¬ X ⊆ A) : ∃ u ∈ X, u ∉ A ∧ u ∈ closure A := by
  by_contra hcon
  push Not at hcon
  have hsub : X ⊆ A ∪ (closure A)ᶜ := fun u hu => by
    by_cases h : u ∈ A
    · exact Or.inl h
    · exact Or.inr (hcon u hu h)
  rcases hX.subset_or_subset hA isClosed_closure.isOpen_compl
      (disjoint_compl_right.mono_left subset_closure) hsub with h | h
  · exact h2 h
  · obtain ⟨u, huX, huA⟩ := h1
    exact h huX (subset_closure huA)

/-- The largest of finitely many `a k * ⟪n k, x⟫` is positively homogeneous in `x`. -/
lemma sup'_smul (s : Finset (Fin N)) (H : s.Nonempty) (a : Fin N → ℝ) (n : Fin N → E3)
    {c : ℝ} (hc : 0 ≤ c) (x : E3) :
    s.sup' H (fun k => a k * ⟪n k, c • x⟫) = c * s.sup' H (fun k => a k * ⟪n k, x⟫) := by
  apply le_antisymm
  · refine (Finset.sup'_le_iff H _).2 fun k hk => ?_
    have := Finset.le_sup' (fun k => a k * ⟪n k, x⟫) hk
    calc a k * ⟪n k, c • x⟫ = c * (a k * ⟪n k, x⟫) := by rw [real_inner_smul_right]; ring
      _ ≤ _ := mul_le_mul_of_nonneg_left this hc
  · obtain ⟨k, hk, he⟩ := Finset.exists_mem_eq_sup' H (fun k => a k * ⟪n k, x⟫)
    rw [he]
    calc c * (a k * ⟪n k, x⟫) = a k * ⟪n k, c • x⟫ := by rw [real_inner_smul_right]; ring
      _ ≤ _ := Finset.le_sup' (fun k => a k * ⟪n k, c • x⟫) hk

lemma continuous_sup' (s : Finset (Fin N)) (H : s.Nonempty) (a : Fin N → ℝ) (n : Fin N → E3) :
    Continuous fun x : E3 => s.sup' H (fun k => a k * ⟪n k, x⟫) :=
  Continuous.finset_sup'_apply H fun _ _ =>
    continuous_const.mul (continuous_const.inner continuous_id)

/-- A plane through the origin has volume zero. -/
lemma volume_plane {w : E3} (hw : w ≠ 0) : volume {x : E3 | ⟪w, x⟫ = 0} = 0 := by
  have hs : (LinearMap.ker (innerₛₗ ℝ w)) ≠ ⊤ := by
    intro h
    have : w ∈ LinearMap.ker (innerₛₗ ℝ w) := h ▸ Submodule.mem_top
    rw [LinearMap.mem_ker] at this
    have hww : ⟪w, w⟫ = 0 := this
    exact hw (inner_self_eq_zero.1 hww)
  have := Measure.addHaar_submodule volume _ hs
  convert this using 2
  ext x
  exact Iff.rfl

/-- With the rays not in one closed hemisphere, shrinking the other corners only enlarges the cell
of a corner that stays put. -/
lemma cell_subset_cell {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r ρ : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hρ : ∀ i, 0 ≤ ρ i) (hle : ∀ i, ρ i ≤ r i)
    {k : Fin N} (hk : ρ k = r k) : cell n r k ⊆ cell n ρ k := by
  intro x hx j
  have hpos : 0 ≤ r k * ⟪n k, x⟫ := by
    by_cases h0 : x = 0
    · simp [h0]
    obtain ⟨m, hm⟩ := hspan x h0
    have := hx m
    have := mul_pos (hr m) hm
    linarith
  have hj := hx j
  rw [hk]
  rcases le_or_gt 0 ⟪n j, x⟫ with ht | ht
  · nlinarith [hle j]
  · nlinarith [hρ j]

/-- The comparison lemma (maximum principle). -/
theorem exists_cell_volume_lt {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r ρ : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hρ : ∀ i, 0 ≤ ρ i) (hle : ∀ i, ρ i ≤ r i)
    (hI : ∃ k, ρ k = r k) (hJ : ∃ j, ρ j < r j)
    (hpos : ∀ i, volume (cell n r i ∩ ball (0 : E3) 1) ≠ 0) :
    ∃ k, ρ k = r k ∧
      volume (cell n r k ∩ ball (0 : E3) 1) < volume (cell n ρ k ∩ ball (0 : E3) 1) := by
  classical
  set I : Finset (Fin N) := univ.filter fun i => ρ i = r i with hIdef
  set J : Finset (Fin N) := univ.filter fun i => ρ i < r i with hJdef
  have hIne : I.Nonempty := by
    obtain ⟨k, hk⟩ := hI; exact ⟨k, by simp [I, hk]⟩
  have hJne : J.Nonempty := by
    obtain ⟨j, hj⟩ := hJ; exact ⟨j, by simp [J, hj]⟩
  have memI : ∀ {i}, i ∈ I ↔ ρ i = r i := by intro i; simp [I]
  have memJ : ∀ {i}, i ∈ J ↔ ρ i < r i := by intro i; simp [J]
  set f : E3 → ℝ := fun x => I.sup' hIne (fun k => r k * ⟪n k, x⟫) with hf
  set g : E3 → ℝ := fun x => J.sup' hJne (fun k => r k * ⟪n k, x⟫) with hg
  set g' : E3 → ℝ := fun x => J.sup' hJne (fun k => ρ k * ⟪n k, x⟫) with hg'
  have fc : Continuous f := continuous_sup' I hIne r n
  have gc : Continuous g := continuous_sup' J hJne r n
  have g'c : Continuous g' := continuous_sup' J hJne ρ n
  have hcorner := corner_injective hn hinj hr
  -- every ray is in I or J
  have hIJ : ∀ i, i ∈ I ∨ i ∈ J := fun i => by
    rcases (hle i).lt_or_eq with h | h
    · exact Or.inr (memJ.2 h)
    · exact Or.inl (memI.2 h)
  -- the farthest corner reaches beyond the origin
  have hmax : ∀ x : E3, x ≠ 0 → 0 < f x ∨ 0 < g x := by
    intro x hx
    obtain ⟨m, hm⟩ := hspan x hx
    have := mul_pos (hr m) hm
    rcases hIJ m with h | h
    · exact Or.inl (lt_of_lt_of_le this (Finset.le_sup' (fun k => r k * ⟪n k, x⟫) h))
    · exact Or.inr (lt_of_lt_of_le this (Finset.le_sup' (fun k => r k * ⟪n k, x⟫) h))
  set A : Set E3 := {x | f x < g x} with hA
  have hAopen : IsOpen A := isOpen_lt fc gc
  -- the J-corners win somewhere
  have h1 : (({0}ᶜ : Set E3) ∩ A).Nonempty := by
    by_contra hne
    rw [Set.not_nonempty_iff_eq_empty] at hne
    have hgf : ∀ x : E3, g x ≤ f x := by
      intro x
      by_cases hx : x = 0
      · subst hx; simp [f, g]
      · by_contra hlt
        have : x ∈ ({0}ᶜ : Set E3) ∩ A := ⟨hx, lt_of_not_ge hlt⟩
        rw [hne] at this; exact this
    obtain ⟨j, hj⟩ := hJne
    apply hpos j
    apply measure_mono_null (t := ⋃ k ∈ (I : Set (Fin N)),
      {x : E3 | ⟪corner n r k - corner n r j, x⟫ = 0})
    · rintro x ⟨hx, -⟩
      obtain ⟨k, hkI, hk⟩ := Finset.exists_mem_eq_sup' hIne (fun k => r k * ⟪n k, x⟫)
      have e1 : r j * ⟪n j, x⟫ ≤ g x := Finset.le_sup' (fun k => r k * ⟪n k, x⟫) hj
      have e2 := hgf x
      have e3 := hx k
      have hfx : f x = r k * ⟪n k, x⟫ := hk
      simp only [mem_iUnion, mem_ofPred_eq]
      refine ⟨k, hkI, ?_⟩
      rw [inner_sub_left, inner_corner, inner_corner]
      linarith
    · refine (measure_biUnion_null_iff (Set.to_countable _)).2 fun k hk => volume_plane ?_
      intro h0
      have := hcorner (sub_eq_zero.1 h0)
      subst this
      have a := memI.1 hk
      have b := memJ.1 hj
      linarith
  -- the I-corners win somewhere
  have h2 : ¬ ({0}ᶜ : Set E3) ⊆ A := by
    intro hsub
    obtain ⟨k, hk⟩ := hIne
    apply hpos k
    apply measure_mono_null (t := ({0} : Set E3)) _ (measure_singleton 0)
    rintro x ⟨hx, -⟩
    by_contra hx0
    have hlt : f x < g x := hsub hx0
    obtain ⟨j, hjJ, hj⟩ := Finset.exists_mem_eq_sup' hJne (fun k => r k * ⟪n k, x⟫)
    have e1 : r k * ⟪n k, x⟫ ≤ f x := Finset.le_sup' (fun k => r k * ⟪n k, x⟫) hk
    have e2 := hx j
    have hgx : g x = r j * ⟪n j, x⟫ := hj
    linarith
  have hX : IsPreconnected ({0}ᶜ : Set E3) := by
    refine (isConnected_compl_singleton_of_one_lt_rank ?_ 0).isPreconnected
    rw [← Module.finrank_eq_rank, finrank_euclideanSpace_fin]
    exact_mod_cast (by norm_num : 1 < 3)
  -- a boundary point between the two
  obtain ⟨u, hu0, huA, hucl⟩ := exists_mem_closure_not_mem hX hAopen h1 h2
  have hfu : f u = g u := le_antisymm (closure_lt_subset_le fc gc hucl) (not_lt.1 huA)
  have hgpos : 0 < g u := by
    rcases hmax u hu0 with h | h
    · rwa [← hfu]
    · exact h
  have hg'u : g' u < f u := by
    rw [hfu]
    refine (Finset.sup'_lt_iff hJne).2 fun j hj => ?_
    have hjlt := memJ.1 hj
    have e1 : r j * ⟪n j, u⟫ ≤ g u := Finset.le_sup' (fun k => r k * ⟪n k, u⟫) hj
    rcases lt_or_ge 0 ⟪n j, u⟫ with ht | ht
    · nlinarith
    · nlinarith [hρ j]
  set W : Set E3 := {x | g' x < f x} with hW
  have hWopen : IsOpen W := isOpen_lt g'c fc
  obtain ⟨y, hyW, hyA⟩ := mem_closure_iff.1 hucl W hWopen hg'u
  -- move it into the unit ball
  set c : ℝ := (‖y‖ + 1)⁻¹ with hc
  have hc0 : 0 < c := by positivity
  have hsc : ∀ (s : Finset (Fin N)) (H : s.Nonempty) (a : Fin N → ℝ),
      s.sup' H (fun k => a k * ⟪n k, c • y⟫) = c * s.sup' H (fun k => a k * ⟪n k, y⟫) :=
    fun s H a => sup'_smul s H a n hc0.le y
  set V : Set E3 := ball 0 1 ∩ W ∩ A with hV
  have hVopen : IsOpen V := (isOpen_ball.inter hWopen).inter hAopen
  have hzV : c • y ∈ V := by
    refine ⟨⟨?_, ?_⟩, ?_⟩
    · rw [mem_ball_zero_iff, norm_smul, Real.norm_of_nonneg hc0.le, hc,
        inv_mul_lt_iff₀ (by positivity)]
      linarith
    · show g' (c • y) < f (c • y)
      simp only [g', f, hsc]
      exact mul_lt_mul_of_pos_left hyW hc0
    · show f (c • y) < g (c • y)
      simp only [g, f, hsc]
      exact mul_lt_mul_of_pos_left hyA hc0
  have hVpos : 0 < volume V := hVopen.measure_pos volume ⟨_, hzV⟩
  -- V is covered by the ρ-cells of the I-corners
  have hVcov : V ⊆ ⋃ k ∈ (I : Set (Fin N)), V ∩ cell n ρ k := by
    intro x hx
    obtain ⟨⟨-, hxW⟩, -⟩ := id hx
    obtain ⟨k, hkI, hk⟩ := Finset.exists_mem_eq_sup' hIne (fun k => r k * ⟪n k, x⟫)
    have hfx : f x = r k * ⟪n k, x⟫ := hk
    simp only [mem_iUnion]
    refine ⟨k, hkI, hx, fun j => ?_⟩
    rw [memI.1 hkI, ← hfx]
    rcases hIJ j with hj | hj
    · rw [memI.1 hj]; exact Finset.le_sup' (fun k => r k * ⟪n k, x⟫) hj
    · have : ρ j * ⟪n j, x⟫ ≤ g' x := Finset.le_sup' (fun k => ρ k * ⟪n k, x⟫) hj
      exact this.trans hxW.le
  obtain ⟨k, hkI, hkpos⟩ : ∃ k ∈ I, 0 < volume (V ∩ cell n ρ k) := by
    by_contra hne
    push Not at hne
    have : volume (⋃ k ∈ (I : Set (Fin N)), V ∩ cell n ρ k) = 0 :=
      (measure_biUnion_null_iff (Set.to_countable _)).2 fun k hk => nonpos_iff_eq_zero.1 (hne k hk)
    exact hVpos.ne' (measure_mono_null hVcov this)
  refine ⟨k, memI.1 hkI, ?_⟩
  have hdisj : Disjoint (cell n r k ∩ ball (0 : E3) 1) (V ∩ cell n ρ k) := by
    rw [Set.disjoint_left]
    rintro x ⟨hx, -⟩ ⟨⟨-, hxA⟩, -⟩
    have e1 : r k * ⟪n k, x⟫ ≤ f x := Finset.le_sup' (fun k => r k * ⟪n k, x⟫) hkI
    have e2 : g x ≤ r k * ⟪n k, x⟫ := (Finset.sup'_le_iff hJne _).2 fun j _ => hx j
    exact absurd hxA (not_lt.2 (e2.trans e1))
  have hsub : (cell n r k ∩ ball (0 : E3) 1) ∪ (V ∩ cell n ρ k) ⊆ cell n ρ k ∩ ball (0 : E3) 1 := by
    rintro x (⟨hx, hb⟩ | ⟨⟨⟨hb, -⟩, -⟩, hx⟩)
    · exact ⟨cell_subset_cell hspan hr hρ hle (memI.1 hkI) hx, hb⟩
    · exact ⟨hx, hb⟩
  have hfin : volume (cell n r k ∩ ball (0 : E3) 1) ≠ ∞ :=
    (measure_mono Set.inter_subset_right |>.trans_lt measure_ball_lt_top).ne
  calc volume (cell n r k ∩ ball (0 : E3) 1)
      < volume (cell n r k ∩ ball (0 : E3) 1) + volume (V ∩ cell n ρ k) :=
        ENNReal.lt_add_right hfin hkpos.ne'
    _ = volume ((cell n r k ∩ ball (0 : E3) 1) ∪ (V ∩ cell n ρ k)) :=
        (measure_union hdisj (hVopen.measurableSet.inter (isClosed_cell n ρ k).measurableSet)).symm
    _ ≤ volume (cell n ρ k ∩ ball (0 : E3) 1) := measure_mono hsub

end Alexandrov
