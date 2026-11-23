/-
Alexandrov's theorem on prescribed curvature, polyhedral case: Oliker's functional.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Variational

/-!
# Oliker's functional: well defined, additive, scale invariant (M9a)

* `abs_log_ratio_le`: the integrand `log (supp n r' x / supp n r x)` is bounded by
  `Σ_i |log (r' i / r i)|`, so it is integrable on the unit ball.
* `gap_add`: `gap r r'' = gap r r' + gap r' r''` (the gains add up along a path).
* `gap_smul`: `gap r (c • r) = (Σ κ - 4π) log c`, which is `0` when `Σ κ = 4π`.
* `Phi n κ r = gap n κ 1 r` is Oliker's functional (up to a constant); `gap r r' = Phi r' - Phi r`,
  `Phi 1 = 0`, and `Phi (c • r) = Phi r` when `Σ κ = 4π`.
-/

open MeasureTheory Set Metric Finset Filter Topology
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ} [NeZero N]

/-- Comparing two support functions by the largest ratio of their corners. -/
lemma supp_le_mul_supp {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hr' : ∀ i, 0 ≤ r' i) {M : ℝ} (hM : 0 ≤ M)
    (hle : ∀ i, r' i ≤ M * r i) {x : E3} (hx : x ≠ 0) : supp n r' x ≤ M * supp n r x := by
  have hpos := supp_pos hspan hr hx
  refine Finset.sup'_le _ _ fun i _ => ?_
  have hs := le_supp n r x i
  rcases le_or_gt 0 ⟪n i, x⟫ with ht | ht
  · calc r' i * ⟪n i, x⟫ ≤ (M * r i) * ⟪n i, x⟫ := mul_le_mul_of_nonneg_right (hle i) ht
      _ = M * (r i * ⟪n i, x⟫) := by ring
      _ ≤ M * supp n r x := mul_le_mul_of_nonneg_left hs hM
  · have : r' i * ⟪n i, x⟫ ≤ 0 := mul_nonpos_of_nonneg_of_nonpos (hr' i) ht.le
    nlinarith

/-- The integrand of `gap` is bounded by `Σ_i |log (r' i / r i)|`. -/
lemma abs_log_ratio_le {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hr' : ∀ i, 0 < r' i) (x : E3) :
    |Real.log (supp n r' x / supp n r x)| ≤ ∑ i, |Real.log (r' i / r i)| := by
  set B := ∑ i, |Real.log (r' i / r i)| with hB
  have hB0 : 0 ≤ B := Finset.sum_nonneg fun i _ => abs_nonneg _
  by_cases hx : x = 0
  · subst hx; simp [supp_zero, hB0]
  have hi : ∀ i, |Real.log (r' i / r i)| ≤ B := fun i =>
    Finset.single_le_sum (f := fun i => |Real.log (r' i / r i)|) (fun i _ => abs_nonneg _)
      (Finset.mem_univ i)
  have h1 : ∀ i, r' i ≤ Real.exp B * r i := fun i => by
    have : r' i / r i ≤ Real.exp B := by
      rw [← Real.exp_log (div_pos (hr' i) (hr i))]
      exact Real.exp_le_exp.2 ((le_abs_self _).trans (hi i))
    rwa [div_le_iff₀ (hr i)] at this
  have h2 : ∀ i, r i ≤ Real.exp B * r' i := fun i => by
    have : r i / r' i ≤ Real.exp B := by
      rw [← Real.exp_log (div_pos (hr i) (hr' i))]
      refine Real.exp_le_exp.2 ((le_abs_self _).trans ?_)
      rw [Real.log_div (hr i).ne' (hr' i).ne', ← neg_sub, abs_neg,
        ← Real.log_div (hr' i).ne' (hr i).ne']
      exact hi i
    rwa [div_le_iff₀ (hr' i)] at this
  have hp := supp_pos hspan hr hx
  have hp' := supp_pos hspan hr' hx
  have u1 := supp_le_mul_supp hspan hr (fun i => (hr' i).le) (Real.exp_pos B).le h1 hx
  have u2 := supp_le_mul_supp hspan hr' (fun i => (hr i).le) (Real.exp_pos B).le h2 hx
  have hq : 0 < supp n r' x / supp n r x := div_pos hp' hp
  rw [abs_le]
  constructor
  · have : Real.exp (-B) ≤ supp n r' x / supp n r x := by
      rw [le_div_iff₀ hp, Real.exp_neg, inv_mul_le_iff₀ (Real.exp_pos B)]
      exact u2
    have := Real.log_le_log (Real.exp_pos _) this
    rwa [Real.log_exp] at this
  · have : supp n r' x / supp n r x ≤ Real.exp B := by
      rw [div_le_iff₀ hp]; exact u1
    have := Real.log_le_log hq this
    rwa [Real.log_exp] at this

lemma measurable_log_ratio (n : Fin N → E3) (r r' : Fin N → ℝ) :
    Measurable fun x : E3 => Real.log (supp n r' x / supp n r x) :=
  ((continuous_supp n r').measurable.div (continuous_supp n r).measurable).log

lemma integrable_log_ratio {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hr' : ∀ i, 0 < r' i) :
    Integrable (fun x : E3 => Real.log (supp n r' x / supp n r x))
      (volume.restrict (ball (0 : E3) 1)) := by
  have : IsFiniteMeasure (volume.restrict (ball (0 : E3) 1)) :=
    isFiniteMeasure_restrict.2 measure_ball_lt_top.ne
  exact Integrable.mono' (integrable_const (∑ i, |Real.log (r' i / r i)|))
    (measurable_log_ratio n r r').aestronglyMeasurable
    (Eventually.of_forall fun x => by
      rw [Real.norm_eq_abs]; exact abs_log_ratio_le hspan hr hr' x)

/-- **Additivity.** The gains add up along a path. -/
theorem gap_add {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    (κ : Fin N → ℝ) {r r' r'' : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hr' : ∀ i, 0 < r' i)
    (hr'' : ∀ i, 0 < r'' i) : gap n κ r r'' = gap n κ r r' + gap n κ r' r'' := by
  have hpt : ∀ x : E3, Real.log (supp n r'' x / supp n r x) =
      Real.log (supp n r' x / supp n r x) + Real.log (supp n r'' x / supp n r' x) := by
    intro x
    by_cases hx : x = 0
    · subst hx; simp [supp_zero]
    rw [Real.log_div (supp_pos hspan hr'' hx).ne' (supp_pos hspan hr hx).ne',
      Real.log_div (supp_pos hspan hr' hx).ne' (supp_pos hspan hr hx).ne',
      Real.log_div (supp_pos hspan hr'' hx).ne' (supp_pos hspan hr' hx).ne']
    ring
  have hint : ∫ x in ball (0 : E3) 1, Real.log (supp n r'' x / supp n r x) =
      (∫ x in ball (0 : E3) 1, Real.log (supp n r' x / supp n r x)) +
        ∫ x in ball (0 : E3) 1, Real.log (supp n r'' x / supp n r' x) := by
    rw [← integral_add (integrable_log_ratio hspan hr hr') (integrable_log_ratio hspan hr' hr'')]
    exact integral_congr_ae (Eventually.of_forall hpt)
  have hsum : ∑ j, κ j * Real.log (r'' j / r j) =
      ∑ j, κ j * Real.log (r' j / r j) + ∑ j, κ j * Real.log (r'' j / r' j) := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Real.log_div (hr'' j).ne' (hr j).ne', Real.log_div (hr' j).ne' (hr j).ne',
      Real.log_div (hr'' j).ne' (hr' j).ne']
    ring
  simp only [gap]
  rw [hint, hsum]
  ring

/-- Scaling the support function. -/
lemma supp_smul (n : Fin N → E3) (r : Fin N → ℝ) {c : ℝ} (hc : 0 ≤ c) (x : E3) :
    supp n (c • r) x = c * supp n r x := by
  unfold supp
  rw [← sup'_smul univ univ_nonempty' r n hc x]
  refine Finset.sup'_congr _ rfl fun k _ => ?_
  simp only [Pi.smul_apply, smul_eq_mul, real_inner_smul_right]
  ring

/-- **Scaling.** The gain of a homothety is `(Σ κ - 4π) log c`. -/
theorem gap_smul {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    (κ : Fin N → ℝ) {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) {c : ℝ} (hc : 0 < c) :
    gap n κ r (c • r) = (∑ j, κ j - 4 * Real.pi) * Real.log c := by
  have hae : (fun x : E3 => Real.log (supp n (c • r) x / supp n r x)) =ᵐ[volume.restrict
      (ball (0 : E3) 1)] fun _ => Real.log c := by
    refine ae_restrict_of_ae ?_
    filter_upwards [measure_eq_zero_iff_ae_notMem.1 (measure_singleton (0 : E3))] with x hx
    have hx0 : x ≠ 0 := fun h => hx (by simp [h])
    rw [supp_smul n r hc.le, mul_div_assoc, div_self (supp_pos hspan hr hx0).ne', mul_one]
  simp only [gap]
  rw [integral_congr_ae hae, setIntegral_const, smul_eq_mul, measureReal_def,
    EuclideanSpace.volume_ball_fin_three]
  have hsum : ∑ j, κ j * Real.log ((c • r) j / r j) = (∑ j, κ j) * Real.log c := by
    rw [Finset.sum_mul]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Pi.smul_apply, smul_eq_mul, mul_div_assoc, div_self (hr j).ne', mul_one]
  rw [hsum, ENNReal.ofReal_one, one_pow, one_mul,
    ENNReal.toReal_ofReal (by positivity)]
  ring

/-- Oliker's functional (normalized so that `Phi 1 = 0`). -/
noncomputable def Phi (n : Fin N → E3) (κ r : Fin N → ℝ) : ℝ := gap n κ 1 r

theorem gap_eq_Phi_sub {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    (κ : Fin N → ℝ) {r r' : Fin N → ℝ} (hr : ∀ i, 0 < r i) (hr' : ∀ i, 0 < r' i) :
    gap n κ r r' = Phi n κ r' - Phi n κ r := by
  simp only [Phi]
  rw [gap_add hspan κ (r := 1) (fun _ => by simp) hr hr']
  ring

theorem Phi_one (n : Fin N → E3) (κ : Fin N → ℝ) : Phi n κ 1 = 0 := by
  have h : ∀ a : ℝ, Real.log (a / a) = 0 := fun a => by
    by_cases ha : a = 0
    · simp [ha]
    · rw [div_self ha, Real.log_one]
  simp [Phi, gap, h]

theorem Phi_smul {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    {κ : Fin N → ℝ} (hsum : ∑ j, κ j = 4 * Real.pi) {r : Fin N → ℝ} (hr : ∀ i, 0 < r i)
    {c : ℝ} (hc : 0 < c) : Phi n κ (c • r) = Phi n κ r := by
  have hcr : ∀ i, 0 < (c • r) i := fun i => by
    rw [Pi.smul_apply, smul_eq_mul]; exact mul_pos hc (hr i)
  have := gap_eq_Phi_sub hspan κ hr hcr
  rw [gap_smul hspan κ hr hc, hsum, sub_self, zero_mul] at this
  linarith

end Alexandrov
