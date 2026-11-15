import YantraCert.Defs
import YantraCert.Frac

/-!
# The construction is forced (the geometric half of step 2)

From Huet's conditions, Kulaichev's (a)–(d) and admissibility, every coordinate of the figure is determined by
`u = w7/b7`, `t = b1/w1` and `S = b9`, one relation at a time. This is the construction of studies/2026-11-15-yantra-uniqueness
(s1_system.py), with the leg slopes named: `k_i = w_i / |b_i - a_i|`. The quantities are numbered as in `Deriv.Data`:

`0 u, 1 t, 2 S, 3 R = b7, 4 P = b3, 5 w7, 6 b1, 7 w1, 8 k2, 9 k9, 10 w9, 11 k8, 12 Q = b6, 13 k1, 14 b8, 15 k4, 16 w6, 17 b2,
18 b4, 19 k6, 20 b5, 21 w5, 22 w2, 23 w4, 24 w8`.

`Facts.steps` gives, for each quantity, the relation `V i * d_i = n_i` and `d_i ≠ 0`, exactly in the form that
`Frac.step_inv` consumes. A triple point (leg `p`, base `q`, leg `r`) is used through `conc_eq`:
`w_p (b_q - a_p)(b_r - a_r) = w_r (b_q - a_r)(b_p - a_p)`, which says that the two legs cross the base line at the same point.
-/

namespace YantraCert.Y
open YantraCert

/-- a triple point as an equation: the two legs cross the base line of `q` at the same abscissa -/
lemma conc_eq (y : Yantra) (p q r : Fin 9) (h : Concurrent (y.leg p) (y.base q) (y.leg r)) (hq : y.w q ≠ 0) :
    y.w p * (y.b q - y.a p) * (y.b r - y.a r) = y.w r * (y.b q - y.a r) * (y.b p - y.a p) := by
  unfold Concurrent Yantra.leg Yantra.base lineThrough at h
  simp only at h
  have e : 2 * y.w q * (y.w p * (y.b q - y.a p) * (y.b r - y.a r) - y.w r * (y.b q - y.a r) * (y.b p - y.a p)) = 0 := by
    linear_combination h
  have h2 : (2 : ℝ) * y.w q ≠ 0 := mul_ne_zero two_ne_zero hq
  have := (mul_eq_zero.mp e).resolve_left h2
  linarith

/-- the conditions, unpacked -/
structure Facts (y : Yantra) : Prop where
  a3 : y.a 2 = 1
  a7 : y.a 6 = 0
  c3 : y.w 2 ^ 2 + y.b 2 ^ 2 - y.b 2 = 0
  c7 : y.w 6 ^ 2 + y.b 6 ^ 2 - y.b 6 = 0
  a8 : y.a 7 = y.b 0
  a6 : y.a 5 = y.b 1
  a9 : y.a 8 = y.b 2
  a1 : y.a 0 = y.b 5
  a5 : y.a 4 = y.b 6
  a4 : y.a 3 = y.b 7
  a2 : y.a 1 = y.b 8
  m127 : y.w 0 * (y.b 1 - y.a 0) * (y.b 6 - y.a 6) = y.w 6 * (y.b 1 - y.a 6) * (y.b 0 - y.a 0)
  m237 : y.w 1 * (y.b 2 - y.a 1) * (y.b 6 - y.a 6) = y.w 6 * (y.b 2 - y.a 6) * (y.b 1 - y.a 1)
  m138 : y.w 0 * (y.b 2 - y.a 0) * (y.b 7 - y.a 7) = y.w 7 * (y.b 2 - y.a 7) * (y.b 0 - y.a 0)
  m146 : y.w 0 * (y.b 3 - y.a 0) * (y.b 5 - y.a 5) = y.w 5 * (y.b 3 - y.a 5) * (y.b 0 - y.a 0)
  m159 : y.w 0 * (y.b 4 - y.a 0) * (y.b 8 - y.a 8) = y.w 8 * (y.b 4 - y.a 8) * (y.b 0 - y.a 0)
  m469 : y.w 3 * (y.b 5 - y.a 3) * (y.b 8 - y.a 8) = y.w 8 * (y.b 5 - y.a 8) * (y.b 3 - y.a 3)
  m279 : y.w 1 * (y.b 6 - y.a 1) * (y.b 8 - y.a 8) = y.w 8 * (y.b 6 - y.a 8) * (y.b 1 - y.a 1)
  m378 : y.w 2 * (y.b 6 - y.a 2) * (y.b 7 - y.a 7) = y.w 7 * (y.b 6 - y.a 7) * (y.b 2 - y.a 2)
  m389 : y.w 2 * (y.b 7 - y.a 2) * (y.b 8 - y.a 8) = y.w 8 * (y.b 7 - y.a 8) * (y.b 2 - y.a 2)
  t448 : y.w 3 * (y.b 3 - y.a 3) * (y.b 7 - y.a 7) = y.w 7 * (y.b 3 - y.a 7) * (y.b 3 - y.a 3)
  t556 : y.w 4 * (y.b 4 - y.a 4) * (y.b 5 - y.a 5) = y.w 5 * (y.b 4 - y.a 5) * (y.b 4 - y.a 4)
  t266 : y.w 1 * (y.b 5 - y.a 1) * (y.b 5 - y.a 5) = y.w 5 * (y.b 5 - y.a 5) * (y.b 1 - y.a 1)
  ka : y.a 2 - y.b 2 = y.b 6 - y.a 6
  kw : y.w 2 = y.w 6
  c1 : y.w 0 ^ 2 + y.b 0 ^ 2 - y.b 0 = 0
  c9 : y.w 8 ^ 2 + y.b 8 ^ 2 - y.b 8 = 0
  d5 : y.b 4 < 1 / 2
  d1 : 1 / 2 < y.a 0
  dd : 1 / 2 - y.b 4 = y.w 0 * (y.a 0 - 1 / 2) / Real.sqrt ((y.a 0 - y.b 0) ^ 2 + y.w 0 ^ 2)
  o01 : y.b 0 < y.b 1
  o12 : y.b 1 < y.b 2
  o23 : y.b 2 < y.b 3
  o34 : y.b 3 < y.b 4
  o45 : y.b 4 < y.b 5
  o56 : y.b 5 < y.b 6
  o67 : y.b 6 < y.b 7
  o78 : y.b 7 < y.b 8
  wp : ∀ i, 0 < y.w i
  ap : ∀ i : Fin 9, (i : ℕ) < 5 → y.b i < y.a i
  au : ∀ i : Fin 9, 5 ≤ (i : ℕ) → y.a i < y.b i
  disc : ∀ i, InDisc (y.w i) (y.b i)

theorem facts_of (y : Yantra) (hH : y.Huet) (hK : y.Kulaichev) (hA : y.Admissible) : Facts y := by
  obtain ⟨a3, a7, c3, c7, a8, a6, a9, a1, a5, a4, a2, m127, m237, m138, m146, m159, m469, m279, m378, m389, t448, t556,
    t266⟩ := hH
  obtain ⟨⟨ka, kw⟩, c1, c9, d5, d1, dd⟩ := hK
  obtain ⟨ord, wp, ap, au, disc⟩ := hA
  have W : ∀ i, y.w i ≠ 0 := fun i => (wp i).ne'
  exact ⟨a3, a7, by simpa [OnCircle] using c3, by simpa [OnCircle] using c7, a8, a6, a9, a1, a5, a4, a2,
    conc_eq y 0 1 6 m127 (W 1), conc_eq y 1 2 6 m237 (W 2), conc_eq y 0 2 7 m138 (W 2), conc_eq y 0 3 5 m146 (W 3),
    conc_eq y 0 4 8 m159 (W 4), conc_eq y 3 5 8 m469 (W 5), conc_eq y 1 6 8 m279 (W 6), conc_eq y 2 6 7 m378 (W 6),
    conc_eq y 2 7 8 m389 (W 7), conc_eq y 3 3 7 t448 (W 3), conc_eq y 4 4 5 t556 (W 4), conc_eq y 1 5 5 t266 (W 5),
    ka, kw, by simpa [OnCircle] using c1, by simpa [OnCircle] using c9, d5, d1, dd,
    ord 0, ord 1, ord 2, ord 3, ord 4, ord 5, ord 6, ord 7, wp, ap, au, disc⟩

/-- the named quantities of a figure -/
noncomputable def V (y : Yantra) : Nat → ℝ := fun i =>
  match i with
  | 0 => y.w 6 / y.b 6 | 1 => y.b 0 / y.w 0 | 2 => y.b 8 | 3 => y.b 6 | 4 => y.b 2 | 5 => y.w 6 | 6 => y.b 0
  | 7 => y.w 0 | 8 => y.w 1 / (y.b 8 - y.b 1) | 9 => y.w 8 / (y.b 8 - y.b 2) | 10 => y.w 8
  | 11 => y.w 7 / (y.b 7 - y.b 0) | 12 => y.b 5 | 13 => y.w 0 / (y.b 5 - y.b 0) | 14 => y.b 7
  | 15 => y.w 3 / (y.b 7 - y.b 3) | 16 => y.w 5 | 17 => y.b 1 | 18 => y.b 3 | 19 => y.w 5 / (y.b 5 - y.b 1)
  | 20 => y.b 4 | 21 => y.w 4 | 22 => y.w 1 | 23 => y.w 3 | 24 => y.w 7
  | 25 => (y.w 0 / (y.b 5 - y.b 0)) * (y.b 5 - y.b 3) | 26 => (y.w 5 / (y.b 5 - y.b 1)) * (y.b 3 - y.b 1) | _ => 0

section
variable {y : Yantra} (F : Facts y)
include F

lemma b0pos : 0 < y.b 0 := by
  have := F.c1; have := F.wp 0; nlinarith [sq_nonneg (y.b 0)]
lemma b6pos : 0 < y.b 6 := by linarith [b0pos F, F.o01, F.o12, F.o23, F.o34, F.o45, F.o56]
lemma b8lt1 : y.b 8 < 1 := by have := F.c9; have := F.wp 8; nlinarith [sq_nonneg (y.b 8), F.o78, b6pos F]

/-- `R (1 + u²) = 1` -/
lemma R_eq : y.b 6 * (1 + (y.w 6 / y.b 6) ^ 2) = 1 := by
  have h6 := b6pos F
  field_simp
  nlinarith [F.c7]

lemma P_eq : y.b 2 = 1 - y.b 6 := by have := F.ka; rw [F.a3, F.a7] at this; linarith
lemma upos : 0 < y.w 6 / y.b 6 := div_pos (F.wp 6) (b6pos F)
lemma w0_eq : y.w 0 * (1 + (y.b 0 / y.w 0) ^ 2) = y.b 0 / y.w 0 := by
  have := F.wp 0
  field_simp
  nlinarith [F.c1]

lemma nz_b6 : y.b 6 ≠ 0 := (b6pos F).ne'
lemma nz_w0 : y.w 0 ≠ 0 := (F.wp 0).ne'
lemma nz_b8_b1 : y.b 8 - y.b 1 ≠ 0 := by linarith [F.o12, F.o23, F.o34, F.o45, F.o56, F.o67, F.o78]
lemma nz_b8_b2 : y.b 8 - y.b 2 ≠ 0 := by linarith [F.o23, F.o34, F.o45, F.o56, F.o67, F.o78]
lemma nz_b7_b0 : y.b 7 - y.b 0 ≠ 0 := by linarith [F.o01, F.o12, F.o23, F.o34, F.o45, F.o56, F.o67]
lemma nz_b5_b0 : y.b 5 - y.b 0 ≠ 0 := by linarith [F.o01, F.o12, F.o23, F.o34, F.o45]
lemma nz_b7_b3 : y.b 7 - y.b 3 ≠ 0 := by linarith [F.o34, F.o45, F.o56, F.o67]
lemma nz_b5_b1 : y.b 5 - y.b 1 ≠ 0 := by linarith [F.o12, F.o23, F.o34, F.o45]
lemma nz_b6_b0 : y.b 6 - y.b 0 ≠ 0 := by linarith [F.o01, F.o12, F.o23, F.o34, F.o45, F.o56]
lemma nz_b4_b6 : y.b 4 - y.b 6 ≠ 0 := by linarith [F.o45, F.o56]
lemma nz_b3_b7 : y.b 3 - y.b 7 ≠ 0 := by linarith [F.o34, F.o45, F.o56, F.o67]
lemma nz_b5_b8 : y.b 5 - y.b 8 ≠ 0 := by linarith [F.o56, F.o67, F.o78]
lemma nz_b2_b0 : y.b 2 - y.b 0 ≠ 0 := by linarith [F.o01, F.o12]

/-- the hypotheses of the step certificates (`scripts/c6_geom_lean.py`), apexes substituted -/
lemma hyps_of :
    y.w 0 * (y.b 1 - y.b 5) * (y.b 6 - 0) = y.w 6 * (y.b 1 - 0) * (y.b 0 - y.b 5) ∧
    y.w 1 * (y.b 2 - y.b 8) * (y.b 6 - 0) = y.w 6 * (y.b 2 - 0) * (y.b 1 - y.b 8) ∧
    y.w 0 * (y.b 2 - y.b 5) * (y.b 7 - y.b 0) = y.w 7 * (y.b 2 - y.b 0) * (y.b 0 - y.b 5) ∧
    y.w 0 * (y.b 3 - y.b 5) * (y.b 5 - y.b 1) = y.w 5 * (y.b 3 - y.b 1) * (y.b 0 - y.b 5) ∧
    y.w 0 * (y.b 4 - y.b 5) * (y.b 8 - y.b 2) = y.w 8 * (y.b 4 - y.b 2) * (y.b 0 - y.b 5) ∧
    y.w 3 * (y.b 5 - y.b 7) * (y.b 8 - y.b 2) = y.w 8 * (y.b 5 - y.b 2) * (y.b 3 - y.b 7) ∧
    y.w 1 * (y.b 6 - y.b 8) * (y.b 8 - y.b 2) = y.w 8 * (y.b 6 - y.b 2) * (y.b 1 - y.b 8) ∧
    y.w 2 * (y.b 6 - 1) * (y.b 7 - y.b 0) = y.w 7 * (y.b 6 - y.b 0) * (y.b 2 - 1) ∧
    y.w 2 * (y.b 7 - 1) * (y.b 8 - y.b 2) = y.w 8 * (y.b 7 - y.b 2) * (y.b 2 - 1) ∧
    y.w 3 * (y.b 3 - y.b 7) * (y.b 7 - y.b 0) = y.w 7 * (y.b 3 - y.b 0) * (y.b 3 - y.b 7) ∧
    y.w 4 * (y.b 4 - y.b 6) * (y.b 5 - y.b 1) = y.w 5 * (y.b 4 - y.b 1) * (y.b 4 - y.b 6) ∧
    y.w 1 * (y.b 5 - y.b 8) * (y.b 5 - y.b 1) = y.w 5 * (y.b 5 - y.b 1) * (y.b 1 - y.b 8) ∧
    y.w 6 ^ 2 + y.b 6 ^ 2 - y.b 6 = 0 ∧ y.w 0 ^ 2 + y.b 0 ^ 2 - y.b 0 = 0 ∧ y.b 2 = 1 - y.b 6 ∧ y.w 2 = y.w 6 ∧
    y.w 6 / y.b 6 * y.b 6 = y.w 6 ∧ y.b 0 / y.w 0 * y.w 0 = y.b 0 ∧
    y.w 1 / (y.b 8 - y.b 1) * (y.b 8 - y.b 1) = y.w 1 ∧ y.w 8 / (y.b 8 - y.b 2) * (y.b 8 - y.b 2) = y.w 8 ∧
    y.w 7 / (y.b 7 - y.b 0) * (y.b 7 - y.b 0) = y.w 7 ∧ y.w 0 / (y.b 5 - y.b 0) * (y.b 5 - y.b 0) = y.w 0 ∧
    y.w 3 / (y.b 7 - y.b 3) * (y.b 7 - y.b 3) = y.w 3 ∧ y.w 5 / (y.b 5 - y.b 1) * (y.b 5 - y.b 1) = y.w 5 := by
  have m127 := F.m127; have m237 := F.m237; have m138 := F.m138; have m146 := F.m146; have m159 := F.m159
  have m469 := F.m469; have m279 := F.m279; have m378 := F.m378; have m389 := F.m389; have t448 := F.t448
  have t556 := F.t556; have t266 := F.t266
  simp only [F.a1, F.a2, F.a3, F.a4, F.a5, F.a6, F.a7, F.a8, F.a9] at m127 m237 m138 m146 m159 m469 m279 m378 m389 t448 t556 t266
  refine ⟨m127, m237, m138, m146, m159, m469, m279, m378, m389, t448, t556, t266, F.c7, F.c1, P_eq F, F.kw,
    div_mul_cancel₀ _ (nz_b6 F), div_mul_cancel₀ _ (nz_w0 F), div_mul_cancel₀ _ (nz_b8_b1 F), div_mul_cancel₀ _ (nz_b8_b2 F),
    div_mul_cancel₀ _ (nz_b7_b0 F), div_mul_cancel₀ _ (nz_b5_b0 F), div_mul_cancel₀ _ (nz_b7_b3 F),
    div_mul_cancel₀ _ (nz_b5_b1 F)⟩

end

end YantraCert.Y
