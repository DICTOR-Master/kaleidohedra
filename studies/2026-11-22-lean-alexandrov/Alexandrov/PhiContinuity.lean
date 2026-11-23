/-
Alexandrov's theorem on prescribed curvature, polyhedral case: continuity of Oliker's functional.
DICTO, with Claude (Anthropic).
-/
import Alexandrov.Functional

/-!
# Oliker's functional is continuous (M9b)

`continuousAt_Phi`: `Phi n κ` is continuous at every `r₀` with positive entries (dominated
convergence: near `r₀` the integrand is bounded by a constant, by `abs_log_ratio_le`).
-/

open MeasureTheory Set Metric Finset Filter Topology
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

variable {N : ℕ} [NeZero N]

lemma continuous_supp_left (n : Fin N → E3) (x : E3) : Continuous fun r : Fin N → ℝ => supp n r x :=
  Continuous.finset_sup'_apply univ_nonempty' fun k _ => (continuous_apply k).mul continuous_const

theorem continuousAt_Phi {n : Fin N → E3} (hspan : ∀ x : E3, x ≠ 0 → ∃ i, 0 < ⟪n i, x⟫)
    (κ : Fin N → ℝ) {r₀ : Fin N → ℝ} (hr₀ : ∀ i, 0 < r₀ i) : ContinuousAt (Phi n κ) r₀ := by
  have : IsFiniteMeasure (volume.restrict (ball (0 : E3) 1)) :=
    isFiniteMeasure_restrict.2 measure_ball_lt_top.ne
  have hone : ∀ i, 0 < (1 : Fin N → ℝ) i := fun _ => by simp
  unfold Phi gap
  refine ContinuousAt.sub ?_ (continuousAt_const.mul ?_)
  · refine tendsto_finsetSum _ fun j _ => ?_
    simp only [Pi.one_apply, div_one]
    exact continuousAt_const.mul ((continuous_apply j).continuousAt.log (hr₀ j).ne')
  · have hU : ∀ᶠ r in 𝓝 r₀, ∀ i, r₀ i / 2 < r i ∧ r i < 2 * r₀ i := eventually_all.2 fun i => by
      have ht : Tendsto (fun r : Fin N → ℝ => r i) (𝓝 r₀) (𝓝 (r₀ i)) :=
        (continuous_apply i).tendsto r₀
      exact (ht.eventually (lt_mem_nhds (by linarith [hr₀ i]))).and
        (ht.eventually (gt_mem_nhds (by linarith [hr₀ i])))
    set B : ℝ := ∑ i, (|Real.log (r₀ i / 2)| + |Real.log (2 * r₀ i)|) with hB
    refine continuousAt_of_dominated (bound := fun _ => B)
      (Eventually.of_forall fun r => (measurable_log_ratio n 1 r).aestronglyMeasurable) ?_
      (integrable_const B) (Eventually.of_forall fun x => ?_)
    · filter_upwards [hU] with r hr
      have hrpos : ∀ i, 0 < r i := fun i => lt_trans (by linarith [hr₀ i]) (hr i).1
      refine Eventually.of_forall fun x => ?_
      rw [Real.norm_eq_abs]
      refine (abs_log_ratio_le hspan hone hrpos x).trans (Finset.sum_le_sum fun i _ => ?_)
      simp only [Pi.one_apply, div_one]
      have h1 := Real.log_lt_log (by linarith [hr₀ i]) (hr i).1
      have h2 := Real.log_lt_log (hrpos i) (hr i).2
      rw [abs_le]
      constructor
      · linarith [neg_abs_le (Real.log (r₀ i / 2)), abs_nonneg (Real.log (2 * r₀ i))]
      · linarith [le_abs_self (Real.log (2 * r₀ i)), abs_nonneg (Real.log (r₀ i / 2))]
    · by_cases hx : x = 0
      · subst hx
        simp only [supp_zero, div_zero, Real.log_zero]
        exact continuousAt_const
      · exact ((continuous_supp_left n x).continuousAt.div_const _).log
          (div_pos (supp_pos hspan hr₀ hx) (supp_pos hspan hone hx)).ne'

end Alexandrov
