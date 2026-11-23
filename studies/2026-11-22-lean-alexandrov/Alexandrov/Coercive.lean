/-
Alexandrov's theorem on prescribed curvature, polyhedral case: coercivity of Oliker's functional.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Margin

/-!
# Coercivity (M9c, part 2)

On the slice `0 < r i ≤ 1` with some `r i = 1`, write `a j = -log r j ≥ 0` and `T = max_j a j`.

**Theorem** (`Phi_le_of_margin`). With `ε, η` as in `exists_margin`,
`Phi n κ r ≤ -4π log ε - η T`.

Proof. Let `mx x = max_j (if ⟪n j, x⟫ > ε ‖x‖ then -a j else -T)`. Pointwise
`log (supp r / supp 1) ≥ log ε + mx`. By the layer-cake formula,
`∫_{ball} (-mx) = ∫_0^∞ vol {x ∈ ball : -mx x > t} dt` and `Σ κ j a j = ∫_0^∞ κ {j : a j > t} dt`;
for `0 < t < T` the rays with `a j ≤ t` form a nonempty proper set `I`, the level set lies outside
`nbhd n ε I`, and the margin gives `3 vol {…} + η ≤ κ {j : a j > t}`. Integrating over `t`:
`3 ∫ (-mx) + η T ≤ Σ κ j a j`, and the bound follows.

**Corollary** (`exists_coercive`). Under Alexandrov's condition there is `δ > 0` with `Phi n κ r < 0 =
Phi n κ 1` whenever `r` is on the slice and some `r i < δ`.
-/

open MeasureTheory Set Metric Finset Filter Topology
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ} [NeZero N]

theorem Phi_le_of_margin {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {κ : Fin N → ℝ} (hκ : ∀ j, 0 ≤ κ j) (hsum : ∑ j, κ j = 4 * Real.pi)
    {ε η : ℝ} (hε : 0 < ε) (hη : 0 < η) (hcov : ∀ x : E3, x ≠ 0 → ∃ j, ε * ‖x‖ < ⟪n j, x⟫)
    (hmar : ∀ I : Finset (Fin N), I.Nonempty → I ≠ Finset.univ →
        ∑ i ∈ I, κ i + η ≤ 3 * (volume (nbhd n ε I ∩ ball (0 : E3) 1)).toReal)
    {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hr1 : ∀ i, r i ≤ 1) (hmax : ∃ i, r i = 1) :
    Phi n κ r ≤ -(4 * Real.pi * Real.log ε) -
      η * Finset.univ.sup' univ_nonempty' (fun j => -Real.log (r j)) := by
  classical
  set B : Set E3 := ball (0 : E3) 1 with hB
  have : IsFiniteMeasure (volume.restrict B) := isFiniteMeasure_restrict.2 measure_ball_lt_top.ne
  set a : Fin N → ℝ := fun j => -Real.log (r j) with hadef
  have ha0 : ∀ j, 0 ≤ a j := fun j => neg_nonneg.2 (Real.log_nonpos (hr j).le (hr1 j))
  set T := Finset.univ.sup' univ_nonempty' a with hTdef
  have haT : ∀ j, a j ≤ T := fun j => Finset.le_sup' a (Finset.mem_univ j)
  have hT0 : 0 ≤ T := (ha0 0).trans (haT 0)
  have hε1 : ε < 1 := by
    obtain ⟨x, hx⟩ := exists_ne (0 : E3)
    obtain ⟨j, hj⟩ := hcov x hx
    have h1 : ⟪n j, x⟫ ≤ 1 * ‖x‖ := by
      rw [one_mul]; exact (real_inner_le_norm _ _).trans (by rw [hn j, one_mul])
    exact lt_of_mul_lt_mul_right (hj.trans_le h1) (norm_nonneg x)
  have hlogε : Real.log ε < 0 := Real.log_neg hε hε1
  -- the step function mx
  set g : Fin N → E3 → ℝ := fun j x => if ε * ‖x‖ < ⟪n j, x⟫ then -a j else -T with hgdef
  set mx : E3 → ℝ := fun x => Finset.univ.sup' univ_nonempty' (fun j => g j x) with hmxdef
  have hgm : ∀ j, Measurable (g j) := fun j =>
    Measurable.ite (measurableSet_lt (continuous_const.mul continuous_norm).measurable
      (continuous_const.inner continuous_id).measurable) measurable_const measurable_const
  have hmxm : Measurable mx := by
    have := Finset.measurable_sup' univ_nonempty' (fun j _ => hgm j)
    convert this using 1
    funext x
    rw [Finset.sup'_apply]
  have hgT : ∀ j x, -T ≤ g j x := fun j x => by
    simp only [hgdef]; split_ifs <;> linarith [haT j]
  have hmx0 : ∀ x, mx x ≤ 0 := fun x => Finset.sup'_le _ _ fun j _ => by
    simp only [hgdef]; split_ifs <;> linarith [ha0 j]
  have hmxT : ∀ x, -T ≤ mx x := fun x =>
    (hgT 0 x).trans (Finset.le_sup' (fun j => g j x) (Finset.mem_univ 0))
  have hmxi : Integrable mx (volume.restrict B) :=
    Integrable.mono' (integrable_const T) hmxm.aestronglyMeasurable
      (Eventually.of_forall fun x => by
        rw [Real.norm_eq_abs, abs_le]; constructor <;> linarith [hmx0 x, hmxT x])
  -- pointwise lower bound
  have hone : ∀ i, 0 < (1 : Fin N → ℝ) i := fun _ => by simp
  have hlow : ∀ x, Real.log ε + mx x ≤ Real.log (supp n r x / supp n 1 x) := by
    intro x
    by_cases hx : x = 0
    · subst hx
      simp only [supp_zero, div_zero, Real.log_zero]
      linarith [hmx0 0]
    obtain ⟨j, -, hj⟩ := Finset.exists_mem_eq_sup' univ_nonempty' (fun j => g j x)
    have hmxj : mx x = g j x := hj
    obtain ⟨j', hJ, hle⟩ : ∃ j', ε * ‖x‖ < ⟪n j', x⟫ ∧ mx x ≤ -a j' := by
      by_cases hjJ : ε * ‖x‖ < ⟪n j, x⟫
      · exact ⟨j, hjJ, by rw [hmxj]; simp only [hgdef, hjJ, ite_true, le_refl]⟩
      · obtain ⟨j', hj'⟩ := hcov x hx
        exact ⟨j', hj', by rw [hmxj]; simp only [hgdef, hjJ, ite_false]; linarith [haT j']⟩
    have hs1 : supp n 1 x ≤ ‖x‖ := Finset.sup'_le _ _ fun i _ => by
      show (1 : Fin N → ℝ) i * ⟪n i, x⟫ ≤ ‖x‖
      rw [Pi.one_apply, one_mul]
      exact (real_inner_le_norm _ _).trans (by rw [hn i, one_mul])
    have hs1pos := supp_pos hspan hone hx
    have hsr : r j' * (ε * ‖x‖) ≤ supp n r x :=
      (mul_le_mul_of_nonneg_left hJ.le (hr j').le).trans (le_supp n r x j')
    have hratio : ε * r j' ≤ supp n r x / supp n 1 x := by
      rw [le_div_iff₀ hs1pos]
      nlinarith [mul_le_mul_of_nonneg_left hs1 (mul_pos hε (hr j')).le]
    have hl := Real.log_le_log (mul_pos hε (hr j')) hratio
    rw [Real.log_mul hε.ne' (hr j').ne'] at hl
    have haj : a j' = -Real.log (r j') := rfl
    linarith
  -- layer cake on the ball
  have hLC : ∫⁻ x in B, ENNReal.ofReal (-mx x) =
      ∫⁻ t in Ioi 0, (volume.restrict B) {x | t < -mx x} :=
    lintegral_eq_lintegral_meas_lt _
      (Eventually.of_forall fun x => by simp only [Pi.zero_apply]; linarith [hmx0 x])
      hmxm.neg.aemeasurable
  -- layer cake on the rays
  have hind : ∀ c : ℝ, 0 ≤ c → ∫⁻ t in Ioi 0, (Iio c).indicator 1 t = ENNReal.ofReal c := by
    intro c _
    rw [lintegral_indicator_one measurableSet_Iio, Measure.restrict_apply measurableSet_Iio,
      Iio_inter_Ioi, Real.volume_Ioo, sub_zero]
  have hindm : ∀ c : ℝ, Measurable ((Iio c).indicator (1 : ℝ → ℝ≥0∞)) := fun c =>
    measurable_one.indicator measurableSet_Iio
  have hK : ENNReal.ofReal (∑ j, κ j * a j) =
      ∫⁻ t in Ioi 0, ∑ j, ENNReal.ofReal (κ j) * (Iio (a j)).indicator 1 t := by
    rw [lintegral_finsetSum _ fun j _ => (hindm (a j)).const_mul _,
      ENNReal.ofReal_sum_of_nonneg fun j _ => mul_nonneg (hκ j) (ha0 j)]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [lintegral_const_mul _ (hindm (a j)), hind (a j) (ha0 j), ENNReal.ofReal_mul (hκ j)]
  -- comparison at each level t
  have hvolB : volume B = ENNReal.ofReal (4 * Real.pi / 3) := by
    rw [hB, EuclideanSpace.volume_ball_fin_three, ENNReal.ofReal_one, one_pow, one_mul]
    congr 1; ring
  have hlevel : ∀ t ∈ Ioi (0 : ℝ),
      3 * (volume.restrict B) {x | t < -mx x} + ENNReal.ofReal η * (Iio T).indicator 1 t ≤
        ∑ j, ENNReal.ofReal (κ j) * (Iio (a j)).indicator 1 t := by
    intro t ht
    have ht0 : 0 < t := ht
    set It := Finset.univ.filter (fun j => a j ≤ t) with hIt
    have hRHS : ∑ j, ENNReal.ofReal (κ j) * (Iio (a j)).indicator 1 t =
        ENNReal.ofReal (∑ j ∈ Finset.univ.filter (fun j => ¬ a j ≤ t), κ j) := by
      rw [ENNReal.ofReal_sum_of_nonneg (fun j _ => hκ j), Finset.sum_filter]
      refine Finset.sum_congr rfl fun j _ => ?_
      by_cases h : a j ≤ t
      · rw [ite_eq_right_of_eq_false _ _ (eq_false (not_not.2 h)), indicator_of_notMem (show t ∉ Iio (a j) from not_lt.2 h),
          mul_zero]
      · rw [ite_eq_left_of_eq_true _ _ (eq_true h), indicator_of_mem (show t ∈ Iio (a j) from not_le.1 h), Pi.one_apply,
          mul_one]
    have hsplit := Finset.sum_filter_add_sum_filter_not Finset.univ (fun j => a j ≤ t) κ
    rw [hsum] at hsplit
    have hSm : MeasurableSet {x : E3 | t < -mx x} := measurableSet_lt measurable_const hmxm.neg
    have h0null : (volume.restrict B) ({0} : Set E3) = 0 := by
      rw [Measure.restrict_apply (measurableSet_singleton 0)]
      exact measure_mono_null Set.inter_subset_left (measure_singleton 0)
    rw [hRHS]
    by_cases htT : t < T
    · -- the rays reached by level t form a nonempty proper set
      have hne : It.Nonempty := by
        obtain ⟨i, hi⟩ := hmax
        refine ⟨i, Finset.mem_filter.2 ⟨Finset.mem_univ i, ?_⟩⟩
        have : a i = 0 := by simp [hadef, hi]
        linarith
      have hneu : It ≠ Finset.univ := by
        intro h
        obtain ⟨j, -, hj⟩ := Finset.exists_mem_eq_sup' univ_nonempty' a
        have : j ∈ It := h ▸ Finset.mem_univ j
        have := (Finset.mem_filter.1 this).2
        have hTj : T = a j := hj
        linarith
      have hm := hmar It hne hneu
      set W := nbhd n ε It with hW
      have hWm : MeasurableSet W := (isOpen_nbhd n ε It).measurableSet
      have hsub : {x : E3 | t < -mx x} ∩ B ⊆ (B \ W) ∪ {0} := by
        rintro x ⟨hxS, hxB⟩
        by_cases hx0 : x = 0
        · exact Or.inr hx0
        refine Or.inl ⟨hxB, fun hxW => ?_⟩
        obtain ⟨i, hiI, hi⟩ := hxW
        have hai := (Finset.mem_filter.1 hiI).2
        have : g i x = -a i := by simp only [hgdef, hi, ite_true]
        have hle : g i x ≤ mx x := Finset.le_sup' (fun j => g j x) (Finset.mem_univ i)
        have : t < -mx x := hxS
        linarith
      have hμ : (volume.restrict B) {x | t < -mx x} ≤ volume (B \ W) := by
        rw [Measure.restrict_apply hSm]
        calc volume ({x : E3 | t < -mx x} ∩ B) ≤ volume ((B \ W) ∪ {0}) := measure_mono hsub
          _ ≤ volume (B \ W) + volume ({0} : Set E3) := measure_union_le _ _
          _ = volume (B \ W) := by rw [measure_singleton, add_zero]
      have hadd := measure_sdiff_add_inter (μ := volume) B hWm
      have hfinD : volume (B \ W) ≠ ∞ :=
        (measure_mono Set.sdiff_subset |>.trans_lt measure_ball_lt_top).ne
      have hfinI : volume (B ∩ W) ≠ ∞ :=
        (measure_mono Set.inter_subset_left |>.trans_lt measure_ball_lt_top).ne
      have hreal : (volume (B \ W)).toReal + (volume (W ∩ B)).toReal = 4 * Real.pi / 3 := by
        rw [Set.inter_comm, ← ENNReal.toReal_add hfinD hfinI, hadd, hvolB,
          ENNReal.toReal_ofReal (by positivity)]
      rw [indicator_of_mem (show t ∈ Iio T from htT), Pi.one_apply, mul_one]
      calc 3 * (volume.restrict B) {x | t < -mx x} + ENNReal.ofReal η
          ≤ 3 * volume (B \ W) + ENNReal.ofReal η := by gcongr
        _ = ENNReal.ofReal (3 * (volume (B \ W)).toReal + η) := by
            rw [ENNReal.ofReal_add (mul_nonneg (by norm_num) ENNReal.toReal_nonneg) hη.le,
              ENNReal.ofReal_mul (by norm_num), ENNReal.ofReal_toReal hfinD]
            norm_num
        _ ≤ ENNReal.ofReal (∑ j ∈ Finset.univ.filter (fun j => ¬ a j ≤ t), κ j) := by
            apply ENNReal.ofReal_le_ofReal
            linarith
    · -- above the top level nothing is left
      have hsub : {x : E3 | t < -mx x} ⊆ {0} := by
        intro x hxS
        by_contra hx0
        obtain ⟨j', hj'⟩ := hcov x hx0
        have : g j' x = -a j' := by simp only [hgdef, hj', ite_true]
        have hle : g j' x ≤ mx x := Finset.le_sup' (fun j => g j x) (Finset.mem_univ j')
        have : t < -mx x := hxS
        linarith [haT j', not_lt.1 htT]
      rw [measure_mono_null hsub h0null,
        indicator_of_notMem (show t ∉ Iio T from htT), mul_zero, mul_zero, add_zero]
      exact zero_le
  -- integrate over the levels
  have hint : 3 * (∫⁻ x in B, ENNReal.ofReal (-mx x)) + ENNReal.ofReal η * ENNReal.ofReal T ≤
      ENNReal.ofReal (∑ j, κ j * a j) := by
    rw [hLC, hK, ← hind T hT0, ← lintegral_const_mul _ (hindm T),
      ← lintegral_const_mul' _ _ (by norm_num : (3 : ℝ≥0∞) ≠ ∞),
      ← lintegral_add_right _ ((hindm T).const_mul _)]
    exact lintegral_mono_ae ((ae_restrict_iff' measurableSet_Ioi).2
      (Eventually.of_forall hlevel))
  have hI0 : 0 ≤ ∫ x in B, -mx x := integral_nonneg fun x => neg_nonneg.2 (hmx0 x)
  have hI : ∫⁻ x in B, ENNReal.ofReal (-mx x) = ENNReal.ofReal (∫ x in B, -mx x) :=
    (ofReal_integral_eq_lintegral_ofReal hmxi.neg
      (Eventually.of_forall fun x => by simp only [Pi.zero_apply, Pi.neg_apply]; linarith [hmx0 x])).symm
  have hcomb : (3 : ℝ≥0∞) * ENNReal.ofReal (∫ x in B, -mx x) + ENNReal.ofReal η * ENNReal.ofReal T =
      ENNReal.ofReal (3 * (∫ x in B, -mx x) + η * T) := by
    rw [ENNReal.ofReal_add (mul_nonneg (by norm_num) hI0) (mul_nonneg hη.le hT0),
      ENNReal.ofReal_mul (by norm_num), ENNReal.ofReal_mul hη.le]
    norm_num
  rw [hI, hcomb, ENNReal.ofReal_le_ofReal_iff
    (Finset.sum_nonneg fun j _ => mul_nonneg (hκ j) (ha0 j))] at hint
  have hL : ∫ x in B, (Real.log ε + mx x) ≤ ∫ x in B, Real.log (supp n r x / supp n 1 x) :=
    integral_mono ((integrable_const _).add hmxi) (integrable_log_ratio hspan hone hr) hlow
  have hL2 : ∫ x in B, (Real.log ε + mx x) = 4 * Real.pi / 3 * Real.log ε + ∫ x in B, mx x := by
    rw [integral_add (integrable_const _) hmxi, setIntegral_const, smul_eq_mul, measureReal_def,
      hvolB, ENNReal.toReal_ofReal (by positivity)]
  have hneg : ∫ x in B, -mx x = -∫ x in B, mx x := integral_neg _
  have hPhi : Phi n κ r = -(∑ j, κ j * a j) -
      3 * ∫ x in B, Real.log (supp n r x / supp n 1 x) := by
    unfold Phi gap
    simp only [Pi.one_apply, div_one, hadef, mul_neg, Finset.sum_neg_distrib, neg_neg]
    rfl
  rw [hPhi]
  linarith

/-- **Coercivity.** Under Alexandrov's condition, `Phi n κ r < 0 = Phi n κ 1` on the slice
`0 < r ≤ 1`, `max r = 1`, as soon as some `r i < δ`. -/
theorem exists_coercive {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {κ : Fin N → ℝ} (hκ : ∀ j, 0 ≤ κ j) (hsum : ∑ j, κ j = 4 * Real.pi)
    (hA : ∀ I : Finset (Fin N), I.Nonempty → I ≠ Finset.univ →
      ∑ i ∈ I, κ i < 3 * (volume (nbhd n 0 I ∩ ball (0 : E3) 1)).toReal) :
    ∃ δ > 0, ∀ r : Fin N → ℝ, (∀ i, 0 < r i) → (∀ i, r i ≤ 1) → (∃ i, r i = 1) →
      (∃ i, r i < δ) → Phi n κ r < 0 := by
  obtain ⟨ε, hε, η, hη, hcov, hmar⟩ := exists_margin hspan hA
  set C := -(4 * Real.pi * Real.log ε) with hC
  refine ⟨Real.exp (-(C / η + 1)), Real.exp_pos _, fun r hr hr1 hmax ⟨i, hi⟩ => ?_⟩
  have h := Phi_le_of_margin hn hspan hκ hsum hε hη hcov hmar hr hr1 hmax
  have hai : C / η + 1 < -Real.log (r i) := by
    have := Real.log_lt_log (hr i) hi
    rw [Real.log_exp] at this
    linarith
  have hT : -Real.log (r i) ≤ Finset.univ.sup' univ_nonempty' (fun j => -Real.log (r j)) :=
    Finset.le_sup' (fun j => -Real.log (r j)) (Finset.mem_univ i)
  have e : η * (C / η) = C := by field_simp
  have := mul_lt_mul_of_pos_left (hai.trans_le hT) hη
  rw [mul_add, e, mul_one] at this
  linarith

end Alexandrov
