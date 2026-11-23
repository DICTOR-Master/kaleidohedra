/-
Alexandrov's theorem on prescribed curvature, polyhedral case: the variational characterization.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Continuity
import Alexandrov.Monotone
import Alexandrov.Total

/-!
# A maximizer has the prescribed curvature

`supp n r x = max_j r j * ⟪n j, x⟫` is the support function of the ray polytope. For prescribed
`κ j ≥ 0` the gain of passing from `r` to `r'` is

  `gap n κ r r' = Σ_j κ j * log (r' j / r j) - 3 * ∫_{unit ball} log (supp n r' x / supp n r x) dx`,

the change of Oliker's functional `Φ(r) = Σ κ j log r j - ∫_{S²} log h_r` (the factor 3 turns the
ball integral of a function constant along rays into the sphere integral).

**Theorem** (`curvature_eq_of_maximizer`). If `Σ κ j = 4π` and no `r'` gains (`gap n κ r r' ≤ 0` for
all `r' > 0`), then the curvature at every corner of the polytope of `r` is `κ j`.

Proof: push corner `j` out by a factor `s > 1`. The integrand lies in `[0, log s]` and vanishes off the
new cell of `j`, so `κ j ≤ κ_j(r'_s)`; let `s → 1` (continuity, M5) to get `κ j ≤ κ_j(r)`; the totals
are both `4π` (M4), so equality holds at every corner.
-/

open MeasureTheory Set Metric Finset Filter Topology
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ} [NeZero N]

lemma univ_nonempty' : (univ : Finset (Fin N)).Nonempty := ⟨0, mem_univ _⟩

/-- The support function of the ray polytope. -/
noncomputable def supp (n : Fin N → E3) (r : Fin N → ℝ) (x : E3) : ℝ :=
  univ.sup' univ_nonempty' (fun j => r j * ⟪n j, x⟫)

/-- The gain of Oliker's functional from `r` to `r'`. -/
noncomputable def gap (n : Fin N → E3) (κ r r' : Fin N → ℝ) : ℝ :=
  ∑ j, κ j * Real.log (r' j / r j) -
    3 * ∫ x in ball (0 : E3) 1, Real.log (supp n r' x / supp n r x)

lemma le_supp (n : Fin N → E3) (r : Fin N → ℝ) (x : E3) (j : Fin N) :
    r j * ⟪n j, x⟫ ≤ supp n r x :=
  le_sup' (fun j => r j * ⟪n j, x⟫) (mem_univ j)

lemma exists_supp_eq (n : Fin N → E3) (r : Fin N → ℝ) (x : E3) :
    ∃ i, supp n r x = r i * ⟪n i, x⟫ := by
  obtain ⟨i, -, hi⟩ := exists_mem_eq_sup' univ_nonempty' (fun j => r j * ⟪n j, x⟫)
  exact ⟨i, hi⟩

lemma supp_zero (n : Fin N → E3) (r : Fin N → ℝ) : supp n r 0 = 0 := by
  simp [supp]

lemma continuous_supp (n : Fin N → E3) (r : Fin N → ℝ) : Continuous (supp n r) :=
  continuous_sup' univ univ_nonempty' r n

lemma supp_pos {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) {x : E3} (hx : x ≠ 0) : 0 < supp n r x := by
  obtain ⟨m, hm⟩ := hspan x hx
  exact (mul_pos (hr m) hm).trans_le (le_supp n r x m)

omit [NeZero N] in
lemma raise_pos {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) {s : ℝ} (hs : 1 ≤ s) (j : Fin N) :
    ∀ i, 0 < Function.update r j (s * r j) i := by
  intro i
  rw [Function.update_apply]
  split_ifs with h
  · subst h; exact mul_pos (by linarith) (hr i)
  · exact hr i

section raise

variable {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
  {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) {s : ℝ} (hs : 1 ≤ s) (j : Fin N)

include hspan hr hs in
lemma supp_le_supp_raise {x : E3} (hx : x ≠ 0) :
    supp n r x ≤ supp n (Function.update r j (s * r j)) x := by
  have hpos := supp_pos hspan (raise_pos hr hs j) hx
  refine Finset.sup'_le _ _ fun i _ => ?_
  have hle := le_supp n (Function.update r j (s * r j)) x i
  rw [Function.update_apply] at hle
  split_ifs at hle with h
  · subst h
    rcases le_or_gt 0 ⟪n i, x⟫ with ht | ht
    · nlinarith [mul_nonneg (sub_nonneg.2 hs) (mul_nonneg (hr i).le ht)]
    · have := mul_neg_of_pos_of_neg (hr i) ht
      linarith
  · exact hle

include hspan hr hs in
lemma supp_raise_le {x : E3} (hx : x ≠ 0) :
    supp n (Function.update r j (s * r j)) x ≤ s * supp n r x := by
  have hpos := supp_pos hspan hr hx
  refine Finset.sup'_le _ _ fun i _ => ?_
  have hle := le_supp n r x i
  show Function.update r j (s * r j) i * ⟪n i, x⟫ ≤ s * supp n r x
  rw [Function.update_apply]
  split_ifs with h
  · subst h; rw [mul_assoc]; exact mul_le_mul_of_nonneg_left hle (by linarith)
  · nlinarith

include hspan hr hs in
lemma supp_raise_eq {x : E3} (hx : x ≠ 0) (hcell : x ∉ cell n (Function.update r j (s * r j)) j) :
    supp n (Function.update r j (s * r j)) x = supp n r x := by
  refine le_antisymm ?_ (supp_le_supp_raise hspan hr hs j hx)
  obtain ⟨i, hi⟩ := exists_supp_eq n (Function.update r j (s * r j)) x
  by_cases h : i = j
  · subst h
    exfalso
    apply hcell
    intro k
    rw [← hi]
    exact le_supp _ _ _ k
  · rw [hi, Function.update_of_ne h]
    exact le_supp n r x i

include hspan hr hs in
/-- The integrand lies between `0` and `log s` on the new cell of `j`, and `0` off it. -/
lemma log_ratio_bounds (x : E3) :
    0 ≤ Real.log (supp n (Function.update r j (s * r j)) x / supp n r x) ∧
      Real.log (supp n (Function.update r j (s * r j)) x / supp n r x) ≤
        (cell n (Function.update r j (s * r j)) j).indicator (fun _ => Real.log s) x := by
  have hlogs : 0 ≤ Real.log s := Real.log_nonneg hs
  by_cases hx : x = 0
  · subst hx
    simp only [supp_zero, div_zero, Real.log_zero, le_refl, true_and]
    exact indicator_nonneg (fun _ _ => hlogs) _
  have hpos := supp_pos hspan hr hx
  have h1 := supp_le_supp_raise hspan hr hs j hx
  have h2 := supp_raise_le hspan hr hs j hx
  have hq1 : 1 ≤ supp n (Function.update r j (s * r j)) x / supp n r x := by
    rw [le_div_iff₀ hpos]; linarith
  refine ⟨Real.log_nonneg hq1, ?_⟩
  by_cases hc : x ∈ cell n (Function.update r j (s * r j)) j
  · rw [indicator_of_mem hc]
    exact Real.log_le_log (by linarith) ((div_le_iff₀ hpos).2 h2)
  · rw [indicator_of_notMem hc, supp_raise_eq hspan hr hs j hx hc, div_self hpos.ne',
      Real.log_one]

end raise

/-- **The variational characterization.** If `Σ κ j = 4π` and no `r' > 0` gains over `r`, the
polytope of `r` has curvature `κ j` at every corner. -/
theorem curvature_eq_of_maximizer {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1)
    (hinj : Function.Injective n) (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) (κ : Fin N → ℝ)
    (hsum : ∑ j, κ j = 4 * Real.pi)
    (hmax : ∀ r' : Fin N → ℝ, (∀ i, 0 < r' i) → gap n κ r r' ≤ 0) :
    ∀ j, curvature (rayPolytope n r) (corner n r j) = ENNReal.ofReal (κ j) := by
  have : IsFiniteMeasure (volume.restrict (ball (0 : E3) 1)) :=
    isFiniteMeasure_restrict.2 measure_ball_lt_top.ne
  have hfin : ∀ (q : Fin N → ℝ) (k : Fin N), volume (cell n q k ∩ ball (0 : E3) 1) ≠ ∞ :=
    fun q k => (measure_mono Set.inter_subset_right |>.trans_lt measure_ball_lt_top).ne
  -- Step 1: pushing corner j out by s > 1 shows κ j ≤ its new curvature
  have step1 : ∀ j, ∀ s : ℝ, 1 < s →
      κ j ≤ 3 * (volume (cell n (Function.update r j (s * r j)) j ∩ ball (0 : E3) 1)).toReal := by
    intro j s hs1
    set r' := Function.update r j (s * r j) with hr'
    have hs := hs1.le
    have hlogpos : 0 < Real.log s := Real.log_pos hs1
    set g : E3 → ℝ := fun x => Real.log (supp n r' x / supp n r x) with hg
    have hcellm : MeasurableSet (cell n r' j) := (isClosed_cell n r' j).measurableSet
    have hgm : Measurable g :=
      ((continuous_supp n r').measurable.div (continuous_supp n r).measurable).log
    have hgb : ∀ x, ‖g x‖ ≤ Real.log s := fun x => by
      obtain ⟨b0, b1⟩ := log_ratio_bounds hspan hr hs j x
      rw [Real.norm_of_nonneg b0]
      refine b1.trans (indicator_apply_le' (fun _ => le_rfl) (fun _ => hlogpos.le))
    have hgi : Integrable g (volume.restrict (ball (0 : E3) 1)) :=
      Integrable.mono' (integrable_const (Real.log s)) hgm.aestronglyMeasurable
        (Eventually.of_forall hgb)
    have hint : ∫ x in ball (0 : E3) 1, g x ≤
        (volume (cell n r' j ∩ ball (0 : E3) 1)).toReal * Real.log s := by
      calc ∫ x in ball (0 : E3) 1, g x
          ≤ ∫ x in ball (0 : E3) 1, (cell n r' j).indicator (fun _ => Real.log s) x :=
            integral_mono hgi ((integrable_const _).indicator hcellm)
              fun x => (log_ratio_bounds hspan hr hs j x).2
        _ = (volume (cell n r' j ∩ ball (0 : E3) 1)).toReal * Real.log s := by
            rw [integral_indicator_const _ hcellm, smul_eq_mul, Measure.real,
              Measure.restrict_apply hcellm]
    have hgap : gap n κ r r' = κ j * Real.log s - 3 * ∫ x in ball (0 : E3) 1, g x := by
      simp only [gap]
      congr 1
      rw [Finset.sum_eq_single j]
      · rw [hr', Function.update_self, mul_div_assoc, div_self (hr j).ne', mul_one]
      · intro i _ hij
        rw [hr', Function.update_of_ne hij, div_self (hr i).ne', Real.log_one, mul_zero]
      · intro h; exact absurd (Finset.mem_univ j) h
    have hle := hmax r' (raise_pos hr hs j)
    rw [hgap] at hle
    refine le_of_mul_le_mul_right ?_ hlogpos
    nlinarith
  -- Step 2: let s → 1
  have step2 : ∀ j, κ j ≤ 3 * (volume (cell n r j ∩ ball (0 : E3) 1)).toReal := by
    intro j
    have hcont : Continuous fun s : ℝ => Function.update r j (s * r j) :=
      continuous_const.update j (continuous_id.mul continuous_const)
    have hpath := hcont.tendsto 1
    simp only [one_mul, Function.update_eq_self] at hpath
    have hlim : Tendsto (fun s : ℝ =>
        3 * (volume (cell n (Function.update r j (s * r j)) j ∩ ball (0 : E3) 1)).toReal)
        (𝓝[>] 1) (𝓝 (3 * (volume (cell n r j ∩ ball (0 : E3) 1)).toReal)) := by
      refine (Tendsto.const_mul 3 ?_).mono_left nhdsWithin_le_nhds
      exact (ENNReal.tendsto_toReal (hfin r j)).comp
        ((continuousAt_volume_cell hn hinj hr j).tendsto.comp hpath)
    exact ge_of_tendsto hlim (eventually_nhdsWithin_of_forall fun s hs => step1 j s hs)
  -- Step 3: the totals agree, so every inequality is an equality
  set c : Fin N → ℝ := fun j => (curvature (rayPolytope n r) (corner n r j)).toReal with hc
  have hcj : ∀ j, c j = 3 * (volume (cell n r j ∩ ball (0 : E3) 1)).toReal := fun j => by
    simp only [c, curvature_rayPolytope, ENNReal.toReal_mul]
    norm_num
  have hcne : ∀ j, curvature (rayPolytope n r) (corner n r j) ≠ ∞ := fun j => by
    rw [curvature_rayPolytope]; exact ENNReal.mul_ne_top (by norm_num) (hfin r j)
  have hcsum : ∑ j, c j = 4 * Real.pi := by
    simp only [c]
    rw [← ENNReal.toReal_sum (fun j _ => hcne j), sum_curvature hn hinj hspan hr,
      ENNReal.toReal_ofReal (by positivity)]
  have heq : ∀ j ∈ (Finset.univ : Finset (Fin N)), κ j = c j :=
    (Finset.sum_eq_sum_iff_of_le fun j _ => (step2 j).trans_eq (hcj j).symm).1
      (hsum.trans hcsum.symm)
  intro j
  rw [heq j (Finset.mem_univ j), hc, ENNReal.ofReal_toReal (hcne j)]

end Alexandrov
