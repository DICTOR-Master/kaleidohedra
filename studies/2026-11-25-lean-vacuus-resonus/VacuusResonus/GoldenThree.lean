/-
The factor 3 is not a φ-step (study 2026-11-25-stellation-cycle, gap (b)).
DICTO, with Claude (Anthropic).
-/
import Mathlib

/-!
# The factor 3 and the φ ladder (M3)

The φ ladder scales by `φ ^ k`, `k : ℤ`. Gap (b) of the stellation-cycle study needs: the depth ratio
`r` of the station dice, with `φ² r² = 3`, is not reached by φ-steps.

* `goldenRatio_zpow_irrational` : `φ ^ k` is irrational for every integer `k ≠ 0`.
* `goldenRatio_zpow_ne_three` : `φ ^ k ≠ 3` for every integer `k`.
* `three_eq_rat_mul_zpow_iff` : `3 = q · φ ^ k` with `q` rational only for `k = 0`, `q = 3`.
* `ratio_ne_rat_mul_zpow` (**gap (b)**): if `φ² r² = 3` then `r ≠ q · φ ^ k` for every rational `q`
  and integer `k`; in particular `r ≠ φ ^ k` and `r² ≠ φ ^ k`.
-/

open Real
open scoped goldenRatio

namespace VacuusResonus

/-- `φ ^ (n + 1) = φ · F(n+1) + F(n)` is irrational. -/
theorem goldenRatio_pow_succ_irrational (n : ℕ) : Irrational (φ ^ (n + 1)) := by
  rw [← goldenRatio_mul_fib_succ_add_fib]
  have hf : Nat.fib (n + 1) ≠ 0 := (Nat.fib_pos.2 (Nat.succ_pos n)).ne'
  exact (goldenRatio_irrational.mul_natCast hf).add_natCast _

/-- `φ ^ k` is irrational for every integer `k ≠ 0`. -/
theorem goldenRatio_zpow_irrational {k : ℤ} (hk : k ≠ 0) : Irrational (φ ^ k) := by
  obtain ⟨m, rfl | rfl⟩ := Int.eq_nat_or_neg k
  · obtain ⟨n, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by exact_mod_cast hk)
    rw [zpow_natCast]
    exact goldenRatio_pow_succ_irrational n
  · obtain ⟨n, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by simpa using hk)
    rw [zpow_neg, zpow_natCast]
    exact (goldenRatio_pow_succ_irrational n).inv

/-- **3 is not a power of φ.** -/
theorem goldenRatio_zpow_ne_three (k : ℤ) : φ ^ k ≠ 3 := by
  by_cases hk : k = 0
  · subst hk; norm_num
  · simpa using (goldenRatio_zpow_irrational hk).ne_rat 3

/-- `3 = q · φ ^ k` with `q` rational only when `k = 0` and `q = 3`. -/
theorem three_eq_rat_mul_zpow_iff (q : ℚ) (k : ℤ) : (3 : ℝ) = q * φ ^ k ↔ k = 0 ∧ q = 3 := by
  constructor
  · intro h
    by_cases hk : k = 0
    · subst hk
      refine ⟨rfl, ?_⟩
      exact_mod_cast (by simpa using h.symm : (q : ℝ) = 3)
    · exfalso
      have hq : (q : ℝ) ≠ 0 := by rintro hq; rw [hq, zero_mul] at h; norm_num at h
      have : φ ^ k = ((3 / q : ℚ) : ℝ) := by
        rw [Rat.cast_div, Rat.cast_ofNat, h]; field_simp
      exact (goldenRatio_zpow_irrational hk).ne_rat _ this
  · rintro ⟨rfl, rfl⟩
    norm_num

/-- **Gap (b).** The depth ratio `r` of the station dice, `φ² r² = 3`, is not a rational multiple of
any φ-step: `r ≠ q · φ ^ k`. -/
theorem ratio_ne_rat_mul_zpow {r : ℝ} (hr : φ ^ 2 * r ^ 2 = 3) (q : ℚ) (k : ℤ) :
    r ≠ q * φ ^ k := by
  intro h
  have h3 : (3 : ℝ) = ((q ^ 2 : ℚ) : ℝ) * φ ^ (2 * k + 2) := by
    rw [← hr, h, Rat.cast_pow, zpow_add₀ goldenRatio_ne_zero, mul_comm 2 k, zpow_mul]
    simp only [zpow_ofNat]
    ring
  obtain ⟨-, hq⟩ := (three_eq_rat_mul_zpow_iff _ _).1 h3
  have hirr : Irrational (√(3 : ℕ)) := Nat.Prime.irrational_sqrt (show Nat.Prime 3 by norm_num)
  apply hirr.ne_rat |q|
  have : ((q ^ 2 : ℚ) : ℝ) = 3 := by exact_mod_cast hq
  rw [Rat.cast_pow] at this
  rw [Nat.cast_ofNat, ← this, Real.sqrt_sq_eq_abs, Rat.cast_abs]

/-- In particular `r` is not a power of φ. -/
theorem ratio_ne_zpow {r : ℝ} (hr : φ ^ 2 * r ^ 2 = 3) (k : ℤ) : r ≠ φ ^ k := by
  simpa using ratio_ne_rat_mul_zpow hr 1 k

/-- In particular `r²` is not a power of φ (the form tested by the study's `factor3.py`). -/
theorem ratio_sq_ne_zpow {r : ℝ} (hr : φ ^ 2 * r ^ 2 = 3) (k : ℤ) : r ^ 2 ≠ φ ^ k := by
  intro h
  apply goldenRatio_zpow_ne_three (k + 2)
  rw [zpow_add₀ goldenRatio_ne_zero, ← h, ← hr]
  simp only [zpow_ofNat]
  ring

end VacuusResonus
