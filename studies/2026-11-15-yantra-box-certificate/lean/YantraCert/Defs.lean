module

public import Mathlib

@[expose] public section

/-!
# The definitions of the Challenge, copied word for word into the library namespace `YantraCert.Y`

**Informal statement.** Take a circle of diameter 1 and nine isosceles triangles `t1, …, t9` with a common vertical axis,
`t1–t5` pointing down and `t6–t9` pointing up. Suppose they meet Huet's conditions, in the form given by Chiodo:

* the two great triangles `t3` and `t7` are inscribed;
* seven apexes lie on bases;
* the 18 marmas (nine mirror pairs of triple points: a leg, a base and a leg pass through one point) and the 6 corner
  touches (three mirror pairs) hold.

Add Kulaichev's four conditions:

* (a) the two great triangles are congruent;
* (b) the corners of `t1` lie on the circle;
* (c) the corners of `t9` lie on the circle;
* (d) the centre of the circle is the incentre of the innermost triangle, the one bounded by the legs of `t1` and the base
  of `t5`.

Finally, ask for admissibility as in DICTO's #103, Theorem 1: the bases are strictly ordered, every half-width is positive,
every apex lies on the correct side of its base, and every corner lies in the closed disc. Then exactly one such figure
exists. A. P. Kulaichev asked this question in 1984 (*IJHS* 19.3, p. 285). Chiodo (*C. R. Math.* 359, 2021) called it still
open.

**Frame.** The axis is the line `x = 0`, and the depth `d` is measured downwards from the top point of the circle, so the
circle is `x² + d² - d = 0`. Triangle `t(i+1)` has base depth `b i`, base half-width `w i` and apex `(0, a i)`, for
`i : Fin 9`. By the mirror symmetry, each condition is stated on the right half. The labels, the orientation and the scale are
fixed by this frame, so "exactly one" means exactly one 27-tuple `(b, w, a)`.

**Sources.** E. Huet (2002) gave the conditions, and A. Chiodo (2021) the form used here. A. P. Kulaichev (1984) added (a)–(d).
DICTO, #103 (*The DICTO Yantra*), Theorem 1, gives admissibility.
-/

namespace YantraCert.Y

/-- nine isosceles triangles with a common vertical axis: `t(i+1)` has base depth `b i`, base half-width `w i` and apex
depth `a i` -/
structure Yantra where
  b : Fin 9 → ℝ
  w : Fin 9 → ℝ
  a : Fin 9 → ℝ

/-- the line through two points `(x₁, d₁)` and `(x₂, d₂)`, as coefficients `(A, B, C)` of `A x + B d + C = 0` -/
def lineThrough (x₁ d₁ x₂ d₂ : ℝ) : ℝ × ℝ × ℝ := (d₁ - d₂, x₂ - x₁, x₁ * d₂ - x₂ * d₁)

/-- three lines pass through one point (or are parallel): their coefficient determinant vanishes -/
def Concurrent (l₁ l₂ l₃ : ℝ × ℝ × ℝ) : Prop :=
  l₁.1 * (l₂.2.1 * l₃.2.2 - l₂.2.2 * l₃.2.1) - l₁.2.1 * (l₂.1 * l₃.2.2 - l₂.2.2 * l₃.1) +
    l₁.2.2 * (l₂.1 * l₃.2.1 - l₂.2.1 * l₃.1) = 0

/-- the right leg of `t(i+1)`: from its right corner `(w i, b i)` to its apex `(0, a i)` -/
def Yantra.leg (y : Yantra) (i : Fin 9) : ℝ × ℝ × ℝ := lineThrough (y.w i) (y.b i) 0 (y.a i)

/-- the base line of `t(i+1)` -/
def Yantra.base (y : Yantra) (i : Fin 9) : ℝ × ℝ × ℝ := lineThrough (-y.w i) (y.b i) (y.w i) (y.b i)

/-- a point lies on the circle of diameter 1 through the top point `(0, 0)` -/
def OnCircle (x d : ℝ) : Prop := x ^ 2 + d ^ 2 - d = 0

/-- a point lies in the closed disc -/
def InDisc (x d : ℝ) : Prop := x ^ 2 + d ^ 2 - d ≤ 0

/-- **Huet's conditions** in Chiodo's form (indices are `i - 1` for `ti`) -/
def Yantra.Huet (y : Yantra) : Prop :=
  -- (i) the great triangles t3 and t7 are inscribed: apexes at the bottom and top points, corners on the circle
  y.a 2 = 1 ∧ y.a 6 = 0 ∧ OnCircle (y.w 2) (y.b 2) ∧ OnCircle (y.w 6) (y.b 6) ∧
  -- (ii) seven apexes on bases: a8 = b1, a6 = b2, a9 = b3, a1 = b6, a5 = b7, a4 = b8, a2 = b9
  y.a 7 = y.b 0 ∧ y.a 5 = y.b 1 ∧ y.a 8 = y.b 2 ∧ y.a 0 = y.b 5 ∧ y.a 4 = y.b 6 ∧ y.a 3 = y.b 7 ∧ y.a 1 = y.b 8 ∧
  -- (iii) the nine marma pairs (leg of p, base of q, leg of r concur):
  --       (1,2,7) (2,3,7) (1,3,8) (1,4,6) (1,5,9) (4,6,9) (2,7,9) (3,7,8) (3,8,9)
  Concurrent (y.leg 0) (y.base 1) (y.leg 6) ∧ Concurrent (y.leg 1) (y.base 2) (y.leg 6) ∧
  Concurrent (y.leg 0) (y.base 2) (y.leg 7) ∧ Concurrent (y.leg 0) (y.base 3) (y.leg 5) ∧
  Concurrent (y.leg 0) (y.base 4) (y.leg 8) ∧ Concurrent (y.leg 3) (y.base 5) (y.leg 8) ∧
  Concurrent (y.leg 1) (y.base 6) (y.leg 8) ∧ Concurrent (y.leg 2) (y.base 6) (y.leg 7) ∧
  Concurrent (y.leg 2) (y.base 7) (y.leg 8) ∧
  --       and the three corner touches (4,4,8) (5,5,6) (2,6,6)
  Concurrent (y.leg 3) (y.base 3) (y.leg 7) ∧ Concurrent (y.leg 4) (y.base 4) (y.leg 5) ∧
  Concurrent (y.leg 1) (y.base 5) (y.leg 5)

/-- **Kulaichev's conditions** (a)–(d) -/
def Yantra.Kulaichev (y : Yantra) : Prop :=
  -- (a) t3 and t7 are congruent: equal heights and equal base half-widths
  (y.a 2 - y.b 2 = y.b 6 - y.a 6 ∧ y.w 2 = y.w 6) ∧
  -- (b) the corners of t1 lie on the circle
  OnCircle (y.w 0) (y.b 0) ∧
  -- (c) the corners of t9 lie on the circle
  OnCircle (y.w 8) (y.b 8) ∧
  -- (d) the centre (0, 1/2) is the incentre of the triangle bounded by the legs of t1 and the base of t5: it lies strictly
  --     between that base and the apex of t1, and its distance to the base equals its distance to the leg of t1
  (y.b 4 < 1 / 2 ∧ 1 / 2 < y.a 0 ∧
    1 / 2 - y.b 4 = y.w 0 * (y.a 0 - 1 / 2) / Real.sqrt ((y.a 0 - y.b 0) ^ 2 + y.w 0 ^ 2))

/-- **admissibility** (#103, Theorem 1): bases strictly ordered, half-widths positive, apexes on the correct side
(t1–t5 point down, so their apexes lie below their bases), corners in the closed disc -/
def Yantra.Admissible (y : Yantra) : Prop :=
  (∀ i : Fin 8, y.b i.castSucc < y.b i.succ) ∧ (∀ i, 0 < y.w i) ∧
  (∀ i : Fin 9, (i : ℕ) < 5 → y.b i < y.a i) ∧ (∀ i : Fin 9, 5 ≤ (i : ℕ) → y.a i < y.b i) ∧
  (∀ i, InDisc (y.w i) (y.b i))

end YantraCert.Y
