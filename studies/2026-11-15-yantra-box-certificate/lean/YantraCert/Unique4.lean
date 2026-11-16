module

public import YantraCert.Unique3
public import YantraCert.Deriv.KKBox

@[expose] public section

/-!
# Uniqueness

`unique`: two admissible figures that satisfy Huet's and Kulaichev's conditions are equal. Their main-chart points lie in
the Krawczyk box (`pt_in_X`) and are zeros of `G~, H~, D~` (`fm_*`), so they coincide (`KBox.unique_X`). The point fixes
`(u, t, S)`, and every coordinate is a named quantity, hence the stored fraction `N_i(u,t,S)/D_i(u,t,S)` (`invs`).
-/

namespace YantraCert.Y
open YantraCert YantraCert.Deriv

lemma inbox_of {x : Fin 3 → ℝ} (h : ∀ j, (KBox.LX j : ℝ) / KBox.QX ≤ x j ∧ x j ≤ (KBox.HX j : ℝ) / KBox.QX) :
    InBox KBox.cX KBox.rX x := by
  intro j; have := h j; rw [abs_le]; simp only [KBox.cX, KBox.rX]; constructor <;> linarith [this.1, this.2]

section
variable {y : Yantra} (F : Facts y)
include F

lemma kbox_zero : ∀ k, KBox.F k (pt y) = 0 := by
  intro k
  have e0 : (pt y) 0 = V y 0 := rfl
  have e1 : (pt y) 1 = tau y := rfl
  have e2 : (pt y) 2 = rho y := rfl
  fin_cases k
  · show KBox.P0.eval _ _ _ = 0
    rw [← ZP.eval_ofSP, ZP.eq_of_eqv KKBox.k0, e0, e1, e2]; exact fm_G F
  · show KBox.P1.eval _ _ _ = 0
    rw [← ZP.eval_ofSP, ZP.eq_of_eqv KKBox.k1, e0, e1, e2]; exact fm_H1 F
  · show KBox.P2.eval _ _ _ = 0
    rw [← ZP.eval_ofSP, ZP.eq_of_eqv KKBox.k2, e0, e1, e2]; exact fm_D F

/-- `S` from the main-chart point -/
lemma S_of : V y 2 = (1 + rho y * (1 - V y 0) * V y 0 ^ 2) / (1 + V y 0 ^ 2) := by
  have h3 := s3 F; have hu1 := u_lt1 F
  have hR : V y 3 < 1 := by rw [V3_eq]; linarith [b8lt1 F, F.o78, F.o67]
  have hden : (1 - V y 0) * (1 - V y 3) ≠ 0 := by apply mul_ne_zero <;> linarith
  have hr : rho y * ((1 - V y 0) * (1 - V y 3)) = V y 2 - V y 3 := div_mul_cancel₀ _ hden
  rw [eq_div_iff (by positivity)]
  linear_combination -(1 + V y 0 ^ 2) * hr - (rho y * (1 - V y 0) - 1) * h3

lemma t_of : V y 1 = V y 0 * tau y := by unfold tau; field_simp [(u_pos F).ne']

end

theorem V_eq_of_pt {y y' : Yantra} (F : Facts y) (F' : Facts y') (h : pt y = pt y') : ∀ i < 27, V y i = V y' i := by
  have e0 : V y 0 = V y' 0 := congrFun h 0
  have e1 : tau y = tau y' := congrFun h 1
  have e2 : rho y = rho y' := congrFun h 2
  have et : V y 1 = V y' 1 := by rw [t_of F, t_of F', e0, e1]
  have eS : V y 2 = V y' 2 := by rw [S_of F, S_of F', e0, e2]
  intro i hi
  obtain ⟨a1, a2⟩ := invs F i hi
  obtain ⟨b1, b2⟩ := invs F' i hi
  rw [e0, et, eS] at a1 a2
  rw [eq_div_of_mul_eq a2 a1, eq_div_of_mul_eq b2 b1]

theorem y_eq_of_V {y y' : Yantra} (F : Facts y) (F' : Facts y') (h : ∀ i < 27, V y i = V y' i) : y = y' := by
  have hb : y.b = y'.b := by
    funext i; fin_cases i
    · exact h 6 (by norm_num)
    · exact h 17 (by norm_num)
    · exact h 4 (by norm_num)
    · exact h 18 (by norm_num)
    · exact h 20 (by norm_num)
    · exact h 12 (by norm_num)
    · exact h 3 (by norm_num)
    · exact h 14 (by norm_num)
    · exact h 2 (by norm_num)
  have hw : y.w = y'.w := by
    funext i; fin_cases i
    · exact h 7 (by norm_num)
    · exact h 22 (by norm_num)
    · show y.w 2 = y'.w 2; rw [F.kw, F'.kw]; exact h 5 (by norm_num)
    · exact h 23 (by norm_num)
    · exact h 21 (by norm_num)
    · exact h 16 (by norm_num)
    · exact h 5 (by norm_num)
    · exact h 24 (by norm_num)
    · exact h 10 (by norm_num)
  have ha : y.a = y'.a := by
    funext i; fin_cases i
    · show y.a 0 = y'.a 0; rw [F.a1, F'.a1, hb]
    · show y.a 1 = y'.a 1; rw [F.a2, F'.a2, hb]
    · show y.a 2 = y'.a 2; rw [F.a3, F'.a3]
    · show y.a 3 = y'.a 3; rw [F.a4, F'.a4, hb]
    · show y.a 4 = y'.a 4; rw [F.a5, F'.a5, hb]
    · show y.a 5 = y'.a 5; rw [F.a6, F'.a6, hb]
    · show y.a 6 = y'.a 6; rw [F.a7, F'.a7]
    · show y.a 7 = y'.a 7; rw [F.a8, F'.a8, hb]
    · show y.a 8 = y'.a 8; rw [F.a9, F'.a9, hb]
  cases y; cases y'; simp_all

/-- **uniqueness** -/
theorem unique (y y' : Yantra) (h : y.Huet ∧ y.Kulaichev ∧ y.Admissible) (h' : y'.Huet ∧ y'.Kulaichev ∧ y'.Admissible) :
    y = y' := by
  have F := facts_of y h.1 h.2.1 h.2.2
  have F' := facts_of y' h'.1 h'.2.1 h'.2.2
  have hp := KBox.unique_X (pt y) (pt y') (inbox_of (pt_in_X F)) (inbox_of (pt_in_X F')) (kbox_zero F) (kbox_zero F')
  exact y_eq_of_V F F' (V_eq_of_pt F F' hp)

/-- **the slope** `w7/b7` of an admissible figure lies in the `u`-interval of the Krawczyk box -/
theorem slope (y : Yantra) (h : y.Huet ∧ y.Kulaichev ∧ y.Admissible) :
    (3379673547380287 : ℝ) / 4503599627370496 ≤ y.w 6 / y.b 6 ∧ y.w 6 / y.b 6 ≤ (3379675694863935 : ℝ) / 4503599627370496 := by
  have F := facts_of y h.1 h.2.1 h.2.2
  have := pt_in_X F 0
  simpa [pt, V, KBox.LX, KBox.HX, KBox.QX] using this

end YantraCert.Y
