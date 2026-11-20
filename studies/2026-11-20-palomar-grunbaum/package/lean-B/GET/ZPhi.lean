module

public import Mathlib

@[expose] public section

/-!
# Exact arithmetic in `ℤ[φ]`

`ZPhi` is the pair `(a, b)` standing for `a + b φ`, with `φ` Mathlib's `Real.goldenRatio`. The ring operations use
`φ² = φ + 1`. `toReal` is the evaluation into `ℝ`; it commutes with `+`, `-`, `*` (proved below). `pos` decides the
sign exactly by integer tests, and `pos_sound` proves that `pos x = true` gives `0 < toReal x`. Everything else in the
pilot is computed on `ZPhi` and checked by `decide +kernel`.
-/

namespace GET

/-- `a + b φ` -/
structure ZPhi where
  a : ℤ
  b : ℤ
deriving DecidableEq, Repr

namespace ZPhi

instance : Zero ZPhi := ⟨⟨0, 0⟩⟩
instance : One ZPhi := ⟨⟨1, 0⟩⟩
instance : Add ZPhi := ⟨fun x y => ⟨x.a + y.a, x.b + y.b⟩⟩
instance : Neg ZPhi := ⟨fun x => ⟨-x.a, -x.b⟩⟩
instance : Sub ZPhi := ⟨fun x y => ⟨x.a - y.a, x.b - y.b⟩⟩
/-- `(a + bφ)(c + dφ) = (ac + bd) + (ad + bc + bd)φ`, since `φ² = φ + 1` -/
instance : Mul ZPhi := ⟨fun x y => ⟨x.a * y.a + x.b * y.b, x.a * y.b + x.b * y.a + x.b * y.b⟩⟩

/-- the integer `n` -/
def ofInt (n : ℤ) : ZPhi := ⟨n, 0⟩

/-- the golden ratio itself -/
def phi : ZPhi := ⟨0, 1⟩

/-- evaluation in `ℝ` -/
noncomputable def toReal (x : ZPhi) : ℝ := x.a + x.b * Real.goldenRatio

/-- exact positivity: `a + bφ = (u + v√5)/2` with `u = 2a + b`, `v = b` -/
def pos (x : ZPhi) : Bool :=
  let u := 2 * x.a + x.b
  let v := x.b
  (decide (0 ≤ u) && decide (0 ≤ v) && !(decide (u = 0) && decide (v = 0))) ||
  (decide (0 < u) && decide (v < 0) && decide (5 * v * v < u * u)) ||
  (decide (u < 0) && decide (0 < v) && decide (u * u < 5 * v * v))

/-- exact non-negativity -/
def nonneg (x : ZPhi) : Bool := decide (x = 0) || pos x

@[simp] theorem add_a (x y : ZPhi) : (x + y).a = x.a + y.a := rfl
@[simp] theorem add_b (x y : ZPhi) : (x + y).b = x.b + y.b := rfl
@[simp] theorem neg_a (x : ZPhi) : (-x).a = -x.a := rfl
@[simp] theorem neg_b (x : ZPhi) : (-x).b = -x.b := rfl
@[simp] theorem sub_a (x y : ZPhi) : (x - y).a = x.a - y.a := rfl
@[simp] theorem sub_b (x y : ZPhi) : (x - y).b = x.b - y.b := rfl
@[simp] theorem mul_a (x y : ZPhi) : (x * y).a = x.a * y.a + x.b * y.b := rfl
@[simp] theorem mul_b (x y : ZPhi) : (x * y).b = x.a * y.b + x.b * y.a + x.b * y.b := rfl

theorem toReal_add (x y : ZPhi) : toReal (x + y) = toReal x + toReal y := by
  unfold toReal; rw [add_a, add_b]; push_cast; ring

theorem toReal_neg (x : ZPhi) : toReal (-x) = -toReal x := by
  unfold toReal; rw [neg_a, neg_b]; push_cast; ring

theorem toReal_sub (x y : ZPhi) : toReal (x - y) = toReal x - toReal y := by
  unfold toReal; rw [sub_a, sub_b]; push_cast; ring

theorem toReal_mul (x y : ZPhi) : toReal (x * y) = toReal x * toReal y := by
  have h := Real.goldenRatio_sq
  unfold toReal; rw [mul_a, mul_b]; push_cast
  linear_combination (-(x.b : ℝ) * y.b) * h

theorem toReal_zero : toReal 0 = 0 := by
  show ((0 : ℤ) : ℝ) + ((0 : ℤ) : ℝ) * Real.goldenRatio = 0; simp
theorem toReal_one : toReal 1 = 1 := by
  show ((1 : ℤ) : ℝ) + ((0 : ℤ) : ℝ) * Real.goldenRatio = 1; simp
theorem toReal_ofInt (n : ℤ) : toReal (ofInt n) = n := by
  show (n : ℝ) + ((0 : ℤ) : ℝ) * Real.goldenRatio = n; simp
theorem toReal_phi : toReal phi = Real.goldenRatio := by
  show ((0 : ℤ) : ℝ) + ((1 : ℤ) : ℝ) * Real.goldenRatio = Real.goldenRatio; simp

theorem toReal_eq (x : ZPhi) :
    toReal x = ((2 * x.a + x.b : ℤ) + (x.b : ℝ) * Real.sqrt 5) / 2 := by
  simp only [toReal, Real.goldenRatio]; push_cast; ring

/-- soundness of the sign test -/
theorem pos_sound {x : ZPhi} (h : pos x = true) : 0 < toReal x := by
  rw [toReal_eq]
  set u : ℤ := 2 * x.a + x.b with hu
  set v : ℤ := x.b with hv
  have s0 : (0 : ℝ) < Real.sqrt 5 := by positivity
  have s2 : Real.sqrt 5 * Real.sqrt 5 = 5 := Real.mul_self_sqrt (by norm_num)
  simp only [pos, Bool.or_eq_true, Bool.and_eq_true, Bool.not_eq_true', decide_eq_true_eq,
    Bool.and_eq_false_iff, decide_eq_false_iff_not] at h
  rw [← hu, ← hv] at h
  apply half_pos
  rcases h with (⟨⟨hu0, hv0⟩, hne⟩ | ⟨⟨hu0, hv0⟩, hq⟩) | ⟨⟨hu0, hv0⟩, hq⟩
  · have hu' : (0 : ℝ) ≤ u := by exact_mod_cast hu0
    have hv' : (0 : ℝ) ≤ v := by exact_mod_cast hv0
    rcases hne with h1 | h1
    · have : (0 : ℝ) < u := by exact_mod_cast lt_of_le_of_ne hu0 (Ne.symm h1)
      nlinarith
    · have : (0 : ℝ) < v := by exact_mod_cast lt_of_le_of_ne hv0 (Ne.symm h1)
      nlinarith
  · have hu' : (0 : ℝ) < u := by exact_mod_cast hu0
    have hv' : (v : ℝ) < 0 := by exact_mod_cast hv0
    have hq' : 5 * (v : ℝ) * v < u * u := by exact_mod_cast hq
    -- u > -v √5 > 0 since u² > 5 v² = (v √5)²
    nlinarith [mul_pos (neg_pos.mpr hv') s0]
  · have hu' : (u : ℝ) < 0 := by exact_mod_cast hu0
    have hv' : (0 : ℝ) < v := by exact_mod_cast hv0
    have hq' : (u : ℝ) * u < 5 * v * v := by exact_mod_cast hq
    nlinarith [mul_pos hv' s0]

theorem nonneg_sound {x : ZPhi} (h : nonneg x = true) : 0 ≤ toReal x := by
  simp only [nonneg, Bool.or_eq_true, decide_eq_true_eq] at h
  rcases h with h | h
  · subst h; rw [toReal_zero]
  · exact (pos_sound h).le

/-- `toReal` is injective (φ is irrational) -/
theorem toReal_injective : Function.Injective toReal := by
  intro x y h
  have hirr := Real.goldenRatio_irrational
  simp only [toReal] at h
  by_cases hb : x.b = y.b
  · have : (x.a : ℝ) = y.a := by rw [hb] at h; linarith
    cases x; cases y; simp_all
  · exfalso
    have hb' : ((x.b - y.b : ℤ) : ℝ) ≠ 0 := by exact_mod_cast sub_ne_zero.mpr hb
    have hm : ((x.b - y.b : ℤ) : ℝ) * Real.goldenRatio = ((y.a - x.a : ℤ) : ℝ) := by
      push_cast; linarith
    have : Real.goldenRatio = ((y.a - x.a : ℤ) : ℝ) / ((x.b - y.b : ℤ) : ℝ) := by
      rw [eq_div_iff hb', mul_comm]; exact hm
    exact hirr ⟨((y.a - x.a : ℤ) : ℚ) / ((x.b - y.b : ℤ) : ℚ), by rw [this]; push_cast; ring⟩

end ZPhi

end GET
