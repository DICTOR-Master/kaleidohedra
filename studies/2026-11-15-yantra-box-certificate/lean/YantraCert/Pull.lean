import YantraCert.BoxBounds
import YantraCert.ZPoly2Sound

/-!
# The equations at an admissible figure, and the pull-back to the main chart

* `eG`, `eH1`, `eD`: Kulaichev (c), the triple point (1,4,6) and Kulaichev (d) (squared) as vanishing expressions in the named
  quantities.
* `subst_pt`: the homogenised substitution `t = u τ`, `S = (1 + ρ (1 - u) u²) / (1 + u²)` evaluated at the main-chart point of
  a figure is the polynomial at `(u, t, S)` times `(1 + u²)^d`.
-/

namespace YantraCert.Y
open YantraCert YantraCert.Deriv

section
variable {y : Yantra} (F : Facts y)
include F

lemma eG : Ex.ev (V y) E_G = 0 := by
  show V y 10 * V y 10 + V y 2 * V y 2 - V y 2 = 0
  rw [V10_eq, V2_eq]; linear_combination F.c9

lemma eH1 : Ex.ev (V y) E_H1 = 0 := by
  show (y.w 0 / (y.b 5 - y.b 0)) * (y.b 5 - y.b 3) - (y.w 5 / (y.b 5 - y.b 1)) * (y.b 3 - y.b 1) = 0
  obtain ⟨-, -, -, m146, -, -, -, -, -, -, -, -, -, -, -, -, -, -, -, -, -, hk1, -, hk6⟩ := hyps_of F
  generalize y.w 0 / (y.b 5 - y.b 0) = k1 at *
  generalize y.w 5 / (y.b 5 - y.b 1) = k6 at *
  have h0 : (y.b 5 - y.b 0) * (y.b 5 - y.b 1) * (k1 * (y.b 5 - y.b 3) - k6 * (y.b 3 - y.b 1)) = 0 := by
    linear_combination -m146 + (y.b 5 - y.b 1) * (y.b 5 - y.b 3) * hk1 - (y.b 5 - y.b 0) * (y.b 3 - y.b 1) * hk6
  have hc : (y.b 5 - y.b 0) * (y.b 5 - y.b 1) ≠ 0 := mul_ne_zero (nz_b5_b0 F) (nz_b5_b1 F)
  have := (mul_eq_zero.mp h0).resolve_left hc
  linarith

lemma eD : Ex.ev (V y) E_D = 0 := by
  show (((1 : ℤ) : ℝ) - ((2 : ℤ) : ℝ) * y.b 4) * (((1 : ℤ) : ℝ) - ((2 : ℤ) : ℝ) * y.b 4) *
      ((y.b 5 - y.b 0) * (y.b 5 - y.b 0) + y.w 0 * y.w 0) -
      y.w 0 * y.w 0 * (((2 : ℤ) : ℝ) * y.b 5 - ((1 : ℤ) : ℝ)) * (((2 : ℤ) : ℝ) * y.b 5 - ((1 : ℤ) : ℝ)) = 0
  push_cast
  have dd := F.dd
  rw [F.a1] at dd
  set L := (y.b 5 - y.b 0) ^ 2 + y.w 0 ^ 2 with hL
  have hL0 : 0 < L := by have := F.wp 0; positivity
  have hs : Real.sqrt L ^ 2 = L := Real.sq_sqrt hL0.le
  have hs0 : 0 < Real.sqrt L := Real.sqrt_pos.mpr hL0
  have e : (1 / 2 - y.b 4) * Real.sqrt L = y.w 0 * (y.b 5 - 1 / 2) := by rw [dd]; field_simp
  have e2 : (1 / 2 - y.b 4) ^ 2 * L = y.w 0 ^ 2 * (y.b 5 - 1 / 2) ^ 2 := by
    rw [← hs]; linear_combination (((1 / 2 - y.b 4) * Real.sqrt L) + y.w 0 * (y.b 5 - 1 / 2)) * e
  rw [hL] at e2
  linear_combination 4 * e2

/-- the substitution at the main-chart point -/
lemma subst_pt (P : ZP) (d : Nat) (hd : P.zdeg d = true) :
    (ZP.substH PX PY PZn PZd d P).eval (V y 0) (tau y) (rho y) = P.eval (V y 0) (V y 1) (V y 2) * (1 + V y 0 ^ 2) ^ d := by
  have hu := u_pos F
  have hd0 : PZd.eval (V y 0) (tau y) (rho y) ≠ 0 := by simp [PZd, ZP.eval]; positivity
  rw [ZP.eval_substH PX PY PZn PZd P d hd _ _ _ hd0]
  have ex : PX.eval (V y 0) (tau y) (rho y) = V y 0 := by simp [PX, ZP.eval]
  have ey : PY.eval (V y 0) (tau y) (rho y) = V y 1 := by simp [PY, ZP.eval, tau]; field_simp
  have ez : PZn.eval (V y 0) (tau y) (rho y) / PZd.eval (V y 0) (tau y) (rho y) = V y 2 := by
    have h3 := s3 F
    have hR : V y 3 < 1 := by rw [V3_eq]; linarith [b8lt1 F, F.o78, F.o67]
    have hu1 := u_lt1 F
    have hden : (1 - V y 0) * (1 - V y 3) ≠ 0 := by apply mul_ne_zero <;> linarith
    have hr : rho y * ((1 - V y 0) * (1 - V y 3)) = V y 2 - V y 3 := div_mul_cancel₀ _ hden
    simp [PZn, PZd, ZP.eval]
    rw [div_eq_iff (by positivity)]
    linear_combination (1 + V y 0 ^ 2) * hr + (rho y * (1 - V y 0) - 1) * h3
  have ezd : PZd.eval (V y 0) (tau y) (rho y) = 1 + V y 0 ^ 2 := by simp [PZd, ZP.eval]
  rw [ex, ey, ez, ezd]

end

end YantraCert.Y
