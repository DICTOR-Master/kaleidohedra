/-
# Exact numbers a + b√5

`Q5` is the ring ℤ[√5] (pairs of integers), with its value in ℝ (`toReal`),
and a decision procedure for `≤` (`Q5.le`) proved correct (`Q5.le_iff`).
The coordinates of all three dice lie in this ring (after scaling).
-/
import Mathlib

namespace RollingLaw

/-- The number `a + b √5`. -/
structure Q5 where
  a : ℤ
  b : ℤ
deriving DecidableEq

namespace Q5

/-- Sum. -/
def add (p q : Q5) : Q5 := ⟨p.a + q.a, p.b + q.b⟩
/-- Difference. -/
def sub (p q : Q5) : Q5 := ⟨p.a - q.a, p.b - q.b⟩
/-- Product, using `√5 · √5 = 5`. -/
def mul (p q : Q5) : Q5 := ⟨p.a * q.a + 5 * p.b * q.b, p.a * q.b + p.b * q.a⟩

/-- The real number `a + b √5`. -/
noncomputable def toReal (p : Q5) : ℝ := p.a + p.b * Real.sqrt 5

/-- Decides `0 ≤ a + b √5` by comparing squares. -/
def nonneg (p : Q5) : Bool :=
  if 0 ≤ p.a then (if 0 ≤ p.b then true else decide (5 * p.b * p.b ≤ p.a * p.a))
  else (if 0 ≤ p.b then decide (p.a * p.a ≤ 5 * p.b * p.b) else false)

/-- Decides `p ≤ q`. -/
def le (p q : Q5) : Bool := (sub q p).nonneg

theorem toReal_add (p q : Q5) : (add p q).toReal = p.toReal + q.toReal := by
  simp [add, toReal]; ring
theorem toReal_sub (p q : Q5) : (sub p q).toReal = p.toReal - q.toReal := by
  simp [sub, toReal]; ring
theorem toReal_mul (p q : Q5) : (mul p q).toReal = p.toReal * q.toReal := by
  have h5 : Real.sqrt 5 * Real.sqrt 5 = 5 := Real.mul_self_sqrt (by norm_num)
  simp only [mul, toReal]; push_cast; linear_combination (-(↑p.b * ↑q.b : ℝ)) * h5

theorem le_mul_sqrt {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (h : x * x ≤ y * y * 5) :
    x ≤ y * Real.sqrt 5 := by
  calc x = Real.sqrt (x * x) := (Real.sqrt_mul_self hx).symm
    _ ≤ Real.sqrt (y * y * 5) := Real.sqrt_le_sqrt h
    _ = y * Real.sqrt 5 := by rw [Real.sqrt_mul (mul_self_nonneg y), Real.sqrt_mul_self hy]

theorem nonneg_iff (p : Q5) : p.nonneg = true ↔ 0 ≤ p.toReal := by
  obtain ⟨a, b⟩ := p
  have s0 : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have h5 : Real.sqrt 5 * Real.sqrt 5 = 5 := Real.mul_self_sqrt (by norm_num)
  simp only [nonneg, toReal]
  by_cases ha : 0 ≤ a <;> by_cases hb : 0 ≤ b <;> simp only [ha, hb, ite_true, ite_false,
    decide_eq_true_eq, reduceCtorEq, false_iff, true_iff, not_le]
  · have : (0 : ℝ) ≤ a := by exact_mod_cast ha
    have : (0 : ℝ) ≤ b := by exact_mod_cast hb
    positivity
  · have ha' : (0 : ℝ) ≤ a := by exact_mod_cast ha
    have hb' : (b : ℝ) < 0 := by exact_mod_cast (not_le.mp hb)
    have e : (-(b : ℝ) * Real.sqrt 5) * (-(b : ℝ) * Real.sqrt 5) = 5 * b * b := by
      linear_combination ((b : ℝ) * b) * h5
    have x0 : 0 ≤ -(b : ℝ) * Real.sqrt 5 := by nlinarith
    constructor
    · intro h
      have h' : (5 : ℝ) * b * b ≤ a * a := by exact_mod_cast h
      have := (mul_self_le_mul_self_iff x0 ha').mpr (by linarith)
      linarith
    · intro h
      have := mul_self_le_mul_self x0 (by linarith : -(b : ℝ) * Real.sqrt 5 ≤ a)
      have : (5 : ℝ) * b * b ≤ a * a := by linarith
      exact_mod_cast this
  · have ha' : (a : ℝ) < 0 := by exact_mod_cast (not_le.mp ha)
    have hb' : (0 : ℝ) ≤ b := by exact_mod_cast hb
    constructor
    · intro h
      have h' : (a : ℝ) * a ≤ 5 * b * b := by exact_mod_cast h
      have := le_mul_sqrt (x := -(a : ℝ)) (y := b) (by linarith) hb' (by nlinarith)
      linarith
    · intro h
      have : (a : ℝ) * a ≤ 5 * b * b := by nlinarith
      exact_mod_cast this
  · have ha' : (a : ℝ) < 0 := by exact_mod_cast (not_le.mp ha)
    have hb' : (b : ℝ) < 0 := by exact_mod_cast (not_le.mp hb)
    nlinarith

theorem le_iff (p q : Q5) : le p q = true ↔ p.toReal ≤ q.toReal := by
  rw [le, nonneg_iff, toReal_sub, sub_nonneg]

theorem lt_of_le_false {p q : Q5} (h : le q p = false) : p.toReal < q.toReal := by
  have : ¬ q.toReal ≤ p.toReal := by rw [← le_iff, h]; decide
  exact not_le.mp this

/-- The zero vector entry. -/
def zero : Q5 := ⟨0, 0⟩

/-- Dot product of two 3-vectors (lists of length 3). -/
def dot (u v : List Q5) : Q5 :=
  add (mul (u.getD 0 zero) (v.getD 0 zero))
    (add (mul (u.getD 1 zero) (v.getD 1 zero)) (mul (u.getD 2 zero) (v.getD 2 zero)))

/-- The real dot product of two 3-vectors. -/
noncomputable def rdot (u v : List Q5) : ℝ :=
  ∑ k : Fin 3, (u.getD k zero).toReal * (v.getD k zero).toReal

theorem toReal_dot (u v : List Q5) : (dot u v).toReal = rdot u v := by
  simp [dot, rdot, toReal_add, toReal_mul, Fin.sum_univ_three]; ring

end Q5

end RollingLaw
