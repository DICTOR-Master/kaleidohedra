module

public import YantraCert.ZPoly2Sound

@[expose] public section

/-!
# Small lemmas for the assembly: signs through identities
-/

namespace YantraCert

/-- a polynomial with positive coefficients and a positive constant term is positive at a nonnegative point -/
lemma ZP.allPos_const_pos {c : Int} {t : ZP} (h : (ZP.cons c 0 0 0 t).allPos = true) {x y z : ℝ} (hx : 0 ≤ x)
    (hy : 0 ≤ y) (hz : 0 ≤ z) : 0 < (ZP.cons c 0 0 0 t).eval x y z := by
  obtain ⟨hc, ht⟩ := ZP.allPos_cons.mp h
  have hc' : (0 : ℝ) < c := by exact_mod_cast hc
  rw [ZP.eval_cons]; have := ZP.allPos_nonneg ht hx hy hz; simp; linarith

/-- the sign of a stored test pair, carried from the sign of the test quantity `q` through the identities
`q TD E2 c1 = TN E1 c4` (main chart), `TN c5 = Nc EN c2` and `TD c6 = Dc ED c3` (chart and rescaling) -/
lemma sign_transfer {q TD E2 TN E1 Nc Dc EN ED c1 c4 c5 c6 c2 c3 : ℝ} (h1 : q * TD * E2 * c1 = TN * E1 * c4)
    (h2 : TN * c5 = Nc * EN * c2) (h3 : TD * c6 = Dc * ED * c3) (hTD : TD ≠ 0) (hE2 : 0 < E2) (hc1 : 0 < c1)
    (hc4 : 0 < c4) (hc5 : 0 < c5) (hc6 : 0 < c6) (hc23 : 0 < c2 * c3) (hq : 0 ≤ q) (hE : 0 ≤ EN * ED * E1)
    (hstrict : 0 < EN * ED * E1 ∨ 0 < q) : 0 ≤ Nc * Dc := by
  have key : Nc * Dc * (EN * ED * E1) * (c2 * c3 * c4) = q * c1 * TD ^ 2 * E2 * (c5 * c6) := by
    linear_combination (-(c5 * c6 * TD)) * h1 - (E1 * c4 * TD * c6) * h2 - (E1 * c4 * Nc * EN * c2) * h3
  have rhs : 0 ≤ q * c1 * TD ^ 2 * E2 * (c5 * c6) := by positivity
  have hc : 0 < c2 * c3 * c4 := mul_pos hc23 hc4
  rcases eq_or_lt_of_le hE with h0 | h0
  · rcases hstrict with h | h
    · linarith
    · rw [← h0, mul_zero, zero_mul] at key
      have : 0 < q * c1 * TD ^ 2 * E2 * (c5 * c6) := by
        have := pow_pos (abs_pos.mpr hTD) 2; rw [sq_abs] at this; positivity
      linarith
  · by_contra hneg; push Not at hneg
    have : Nc * Dc * (EN * ED * E1) * (c2 * c3 * c4) < 0 := mul_neg_of_neg_of_pos (mul_neg_of_neg_of_pos hneg h0) hc
    linarith

/-- the evaluation of a product of powers -/
lemma ZP.eval_prod_pow (l : List (ZP × Nat)) (x y z : ℝ) :
    (ZP.prod (l.map fun fm => ZP.pow fm.1 fm.2)).eval x y z = (l.map fun fm => fm.1.eval x y z ^ fm.2).prod := by
  rw [ZP.eval_prod]; simp [List.map_map, Function.comp_def, ZP.eval_pow]

end YantraCert
