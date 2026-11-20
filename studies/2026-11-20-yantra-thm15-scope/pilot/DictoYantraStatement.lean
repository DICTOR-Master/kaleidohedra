import YantraCert.Main

/-!
# Pilot: Theorem 15 of #103 (the DICTO Yantra is the only one), stated against the existing definitions

Feasibility pilot only. The two theorems carry `sorry`; nothing here is a proof of Theorem 15.
The frame, `Yantra`, `Huet`, `OnCircle` and `Admissible` are the published entry's definitions, unchanged.
Only two new definitions are needed: Kulaichev's (b), (c), (d) without (a), and the Cleo-Antonius product.
-/

namespace DictoYantraPilot

open YantraCert.Y

/-- Kulaichev's (b), (c) and (d), word for word as in `Yantra.Kulaichev`, without (a) -/
def _root_.YantraCert.Y.Yantra.KulaichevBCD (y : Yantra) : Prop :=
  OnCircle (y.w 0) (y.b 0) ∧
  OnCircle (y.w 8) (y.b 8) ∧
  (y.b 4 < 1 / 2 ∧ 1 / 2 < y.a 0 ∧
    1 / 2 - y.b 4 = y.w 0 * (y.a 0 - 1 / 2) / Real.sqrt ((y.a 0 - y.b 0) ^ 2 + y.w 0 ^ 2))

/-- DICTO's Cleo-Antonius condition (#103 §9.1): the slope `u = w7/b7` of the upper great triangle t7 times the slope
`v = w3/(1 - b3)` of the lower great triangle t3 is `2/φ³ = 2√5 - 4` -/
def _root_.YantraCert.Y.Yantra.CleoAntonius (y : Yantra) : Prop :=
  (y.w 6 / y.b 6) * (y.w 2 / (1 - y.b 2)) = 2 * Real.sqrt 5 - 4

/-- the reuse is exact: Kulaichev's conditions are (a) together with the new `KulaichevBCD` -/
theorem kulaichev_eq_a_and_bcd (y : Yantra) :
    y.Kulaichev ↔ ((y.a 2 - y.b 2 = y.b 6 - y.a 6 ∧ y.w 2 = y.w 6) ∧ y.KulaichevBCD) := Iff.rfl

/-- `2/φ³ = 2√5 - 4`, with `φ = (1 + √5)/2` -/
theorem two_div_phi_cube : 2 / ((1 + Real.sqrt 5) / 2) ^ 3 = 2 * Real.sqrt 5 - 4 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < (1 + Real.sqrt 5) / 2 := by positivity
  rw [div_eq_iff (by positivity)]
  nlinarith [h5]

/-- **Theorem 15 (pilot statement).** The DICTO Yantra is the only one. -/
theorem dicto_unique : ∃! y : Yantra, y.Huet ∧ y.KulaichevBCD ∧ y.CleoAntonius ∧ y.Admissible := by
  sorry

/-- its slope `w7/b7` lies in an interval of width `2⁻²¹` around `0.6793185887067746…` (#103, Theorem 9) -/
theorem dicto_slope (y : Yantra) (h : y.Huet ∧ y.KulaichevBCD ∧ y.CleoAntonius ∧ y.Admissible) :
    (3059377869223857 : ℝ) / 4503599627370496 ≤ y.w 6 / y.b 6 ∧
      y.w 6 / y.b 6 ≤ (3059380016707505 : ℝ) / 4503599627370496 := by
  sorry

end DictoYantraPilot
