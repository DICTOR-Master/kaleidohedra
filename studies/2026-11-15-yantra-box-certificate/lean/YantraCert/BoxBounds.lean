module

public import YantraCert.GeomSteps

@[expose] public section

/-!
# The main box coordinates of an admissible figure (step 3b)

`u = w7/b7`, `τ = t/u` with `t = b1/w1`, and `ρ = (S - R)/((1 - u)(1 - R))` with `S = b9`, `R = b7`. At an admissible figure,
`0 < u < 1`, `0 < τ < 1` and `0 < ρ ≤ 6` (README §1): `u < 1` because `b3 < b7`; `τ < 1` because `b1 < b3`; `ρ > 0` because
`b7 < b9`; and `ρ ≤ 6` because `b9 < 1` when `u ≤ 5/6`, and because `w9 ≤ 1/2` (t9's corner on the circle) when `u > 5/6`.
-/

namespace YantraCert.Y
open YantraCert YantraCert.Deriv

noncomputable def tau (y : Yantra) : ℝ := V y 1 / V y 0
noncomputable def rho (y : Yantra) : ℝ := (V y 2 - V y 3) / ((1 - V y 0) * (1 - V y 3))
/-- the point of the main chart -/
noncomputable def pt (y : Yantra) : Fin 3 → ℝ := ![V y 0, tau y, rho y]

lemma V3_eq {y : Yantra} : V y 3 = y.b 6 := rfl
lemma V4_eq {y : Yantra} : V y 4 = y.b 2 := rfl
lemma V2_eq {y : Yantra} : V y 2 = y.b 8 := rfl
lemma V10_eq {y : Yantra} : V y 10 = y.w 8 := rfl

section
variable {y : Yantra} (F : Facts y)
include F

lemma s3 : V y 3 * (1 + V y 0 * V y 0) = 1 := by
  have h := gstep3 F; change V y 3 * (((1 : ℤ) : ℝ) + V y 0 * V y 0) = ((1 : ℤ) : ℝ) at h; push_cast at h; exact h
lemma s4 : V y 4 * (1 + V y 0 * V y 0) = V y 0 * V y 0 := by
  have h := gstep4 F; change V y 4 * (((1 : ℤ) : ℝ) + V y 0 * V y 0) = V y 0 * V y 0 at h; push_cast at h; exact h
lemma s8 : V y 8 * (V y 2 - V y 4) = V y 0 * V y 4 := gstep8 F
lemma s9 : V y 9 * (V y 3 - V y 4) = V y 8 * (V y 2 - V y 3) := gstep9 F
lemma s10 : V y 10 * 1 = V y 9 * (V y 2 - V y 4) := by
  have h := gstep10 F; change V y 10 * ((1 : ℤ) : ℝ) = V y 9 * (V y 2 - V y 4) at h; push_cast at h; exact h

lemma u_pos : 0 < V y 0 := upos F

lemma u_lt1 : V y 0 < 1 := by
  have h3 := s3 F; have h4 := s4 F; have hu := u_pos F
  have hPR : V y 4 < V y 3 := by rw [V4_eq, V3_eq]; linarith [F.o23, F.o34, F.o45, F.o56]
  -- (R - P)(1 + u²) = 1 - u² > 0
  have : (V y 3 - V y 4) * (1 + V y 0 * V y 0) = 1 - V y 0 * V y 0 := by linear_combination h3 - h4
  have : 0 < 1 - V y 0 * V y 0 := by rw [← this]; positivity
  nlinarith

lemma t_pos : 0 < V y 1 := div_pos (b0pos F) (F.wp 0)

lemma tau_pos : 0 < tau y := div_pos (t_pos F) (u_pos F)

lemma tau_lt1 : tau y < 1 := by
  have hu := u_pos F; have ht := t_pos F
  have h6 := gstep6 F; change V y 6 * (((1 : ℤ) : ℝ) + V y 1 * V y 1) = V y 1 * V y 1 at h6; push_cast at h6
  have h4 := s4 F
  have hb : V y 6 < V y 4 := by show y.b 0 < y.b 2; linarith [F.o01, F.o12]
  -- b1 < b3:  t²/(1+t²) < u²/(1+u²)  gives  t² < u²
  have : V y 1 * V y 1 < V y 0 * V y 0 := by
    by_contra hh; push Not at hh
    have e1 : V y 6 = V y 1 * V y 1 / (1 + V y 1 * V y 1) := by field_simp; linarith
    have e2 : V y 4 = V y 0 * V y 0 / (1 + V y 0 * V y 0) := by field_simp; linarith
    rw [e1, e2, div_lt_div_iff₀ (by positivity) (by positivity)] at hb
    nlinarith
  unfold tau; rw [div_lt_one hu]; nlinarith

lemma rho_pos : 0 < rho y := by
  have h1 := u_lt1 F
  have hR : V y 3 < 1 := by rw [V3_eq]; linarith [b8lt1 F, F.o78, F.o67]
  have hS : V y 3 < V y 2 := by rw [V3_eq, V2_eq]; linarith [F.o78, F.o67]
  unfold rho; apply div_pos (by linarith); apply mul_pos <;> linarith

/-- `ρ u⁵ R = w9 (1 + u)` -/
lemma rho_w9 : rho y * V y 0 ^ 5 * V y 3 = V y 10 * (1 + V y 0) := by
  have h3 := s3 F; have h4 := s4 F; have h8 := s8 F; have h9 := s9 F; have h10 := s10 F
  have hu := u_pos F; have hu1 := u_lt1 F
  have hR : V y 3 < 1 := by rw [V3_eq]; linarith [b8lt1 F, F.o78, F.o67]
  have hRP : V y 4 < V y 3 := by rw [V4_eq, V3_eq]; linarith [F.o23, F.o34, F.o45, F.o56]
  have hP : V y 4 = 1 - V y 3 := by rw [V4_eq, V3_eq]; exact P_eq F
  -- w9 (R - P) = u P (S - R)
  have hw : V y 10 * (V y 3 - V y 4) = V y 0 * V y 4 * (V y 2 - V y 3) := by
    have : V y 10 * (V y 3 - V y 4) = V y 9 * (V y 3 - V y 4) * (V y 2 - V y 4) := by
      rw [show V y 10 = V y 9 * (V y 2 - V y 4) by linarith]; ring
    rw [this, h9]; linear_combination (V y 2 - V y 3) * h8
  have hden : (1 - V y 0) * (1 - V y 3) ≠ 0 := by apply mul_ne_zero <;> linarith
  have hr : rho y * ((1 - V y 0) * (1 - V y 3)) = V y 2 - V y 3 := div_mul_cancel₀ _ hden
  have hR0 : 0 < V y 3 := by rw [V3_eq]; exact b6pos F
  have hw2 : V y 10 * (V y 3 * (1 - V y 0 ^ 2)) = V y 0 * (V y 0 ^ 2 * V y 3) * (V y 2 - V y 3) := by
    rw [hP] at hw; linear_combination hw - (V y 10 + V y 0 * (V y 2 - V y 3)) * h3
  have hw3 : V y 10 * (1 - V y 0 ^ 2) = V y 0 ^ 3 * (V y 2 - V y 3) := by
    have : V y 3 * (V y 10 * (1 - V y 0 ^ 2) - V y 0 ^ 3 * (V y 2 - V y 3)) = 0 := by linear_combination hw2
    rcases mul_eq_zero.mp this with h | h
    · linarith
    · linarith
  have : (rho y * V y 0 ^ 5 * V y 3 - V y 10 * (1 + V y 0)) * ((1 - V y 0) * (1 - V y 3)) = 0 := by
    linear_combination (V y 0 ^ 5 * V y 3) * hr - (1 - V y 3) * hw3 + V y 0 ^ 3 * (V y 2 - V y 3) * h3
  rcases mul_eq_zero.mp this with h | h
  · linarith
  · exact absurd h hden

lemma rho_le6 : rho y ≤ 6 := by
  have hu := u_pos F; have hu1 := u_lt1 F; have h3 := s3 F
  have hR : V y 3 < 1 := by rw [V3_eq]; linarith [b8lt1 F, F.o78, F.o67]
  have hR0 : 0 < V y 3 := by rw [V3_eq]; exact b6pos F
  have hS1 : V y 2 < 1 := by rw [V2_eq]; exact b8lt1 F
  have hden : (1 - V y 0) * (1 - V y 3) ≠ 0 := by apply mul_ne_zero <;> linarith
  have hr : rho y * ((1 - V y 0) * (1 - V y 3)) = V y 2 - V y 3 := div_mul_cancel₀ _ hden
  have hrp := rho_pos F
  rcases le_or_gt (V y 0) (5 / 6) with hc | hc
  · -- rho (1 - u)(1 - R) = S - R < 1 - R
    have : rho y * (1 - V y 0) < 1 := by
      have h1 : 0 < 1 - V y 3 := by linarith
      nlinarith
    nlinarith
  · -- rho u⁵ R = w9 (1 + u) ≤ 1, R ≥ 1/2
    have hw := rho_w9 F
    have hw9 : V y 10 ≤ 1 / 2 := by
      have := F.c9; rw [V10_eq]; nlinarith [sq_nonneg (y.w 8 - 1 / 2), sq_nonneg (y.b 8 - 1 / 2), F.wp 8]
    have hRh : 1 / 2 ≤ V y 3 := by nlinarith
    have hu5 : (5 / 6 : ℝ) ^ 5 ≤ V y 0 ^ 5 := pow_le_pow_left₀ (by norm_num) hc.le 5
    have h1 : rho y * V y 0 ^ 5 * V y 3 ≤ 1 := by rw [hw]; nlinarith [F.wp 8]
    have h2 : rho y * ((5 / 6 : ℝ) ^ 5 * (1 / 2)) ≤ rho y * (V y 0 ^ 5 * V y 3) := by
      apply mul_le_mul_of_nonneg_left _ hrp.le
      exact mul_le_mul hu5 hRh (by norm_num) (by positivity)
    nlinarith

end

end YantraCert.Y
