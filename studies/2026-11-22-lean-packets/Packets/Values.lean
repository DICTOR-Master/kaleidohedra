/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Part 7: the values of Table 1 from
Gram values of face normals.

Each lemma evaluates `π − ∠(u, v)`, the dihedral angle at an edge whose two faces have outward normals `u`, `v`,
from `⟪u, v⟫`, `⟪u, u⟫`, `⟪v, v⟫` (in the coordinates of the generated solids) as a value of Table 1:
`α`, `2α`, `2π/3`, `2π/5`, `3π/4 − β`, `3π/2 − 2β`, `3π/4 − α + β`, `π/2 + γ`, `π − 2γ`.
No `sorry`.
-/
module

public import Packets.Pieces

@[expose] public section

open Set Module
open scoped RealInnerProductSpace

namespace Packets

open DehnCanon.Library (R3 sqrt5_sq)

/-! ### Ranges of α, β -/

lemma α_nonneg : 0 ≤ α := Real.arctan_nonneg.2 (by positivity)

lemma α_le : α ≤ Real.pi / 2 := (Real.arctan_lt_pi_div_two _).le

lemma α_ge : Real.pi / 4 ≤ α := by
  rw [← Real.arctan_one]
  exact Real.arctan_strictMono.monotone (by
    have h5 : (1 : ℝ) ≤ √5 := Real.one_le_sqrt.2 (by norm_num); linarith)

lemma β_ge : Real.pi / 4 ≤ β := by
  by_contra hβ
  push Not at hβ
  have h := Real.cos_lt_cos_of_nonneg_of_le_pi_div_two β_nonneg (by linarith [Real.pi_pos]) hβ
  rw [Real.cos_pi_div_four, cos_β] at h
  have h6 : (1 : ℝ) / √6 = √6 / 6 := by
    rw [div_eq_div_iff (by positivity) (by norm_num), one_mul, Real.mul_self_sqrt (by norm_num)]
  rw [h6] at h
  nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num), Real.sq_sqrt (show (0 : ℝ) ≤ 6 by norm_num),
    Real.sqrt_nonneg 2, Real.sqrt_nonneg 6]

lemma sqrt_sq_num {a : ℝ} (ha : 0 ≤ a) : √(a ^ 2) = a := Real.sqrt_sq ha

variable {u v : R3}

/-- Pentagon–hexagon of the truncated icosahedron, triangle–decagon of the truncated dodecahedron. -/
lemma val_pentHex (hg : ⟪u, v⟫ = (6 + 2 * √5)) (hX : ⟪u, u⟫ = (10 + 2 * √5)) (hY : ⟪v, v⟫ = 12) :
    Real.pi - InnerProductGeometry.angle u v = 3 * Real.pi / 4 - α + β := by
  have h5 := sqrt5_sq
  have hpi := Real.pi_pos
  have ha2 := α_le; have ha3 := α_ge; have hb1 := β_le; have hb2 := β_ge
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  apply cos_eq_neg_of_sq
  · have hc : Real.cos (3 * Real.pi / 4 - α + β) ≤ 0 :=
      Real.cos_nonpos_of_pi_div_two_le_of_le (by linarith) (by linarith)
    have hd : 0 ≤ (6 + 2 * √5) / (√(10 + 2 * √5) * √12) := by positivity
    nlinarith
  · rw [Real.cos_sq, show 2 * (3 * Real.pi / 4 - α + β) = (Real.pi / 2 - (2 * α - 2 * β)) + Real.pi by ring,
      Real.cos_add_pi, Real.cos_pi_div_two_sub, Real.sin_sub, sin_two_α, cos_two_α, sin_two_β, cos_two_β,
      div_pow, mul_pow, Real.sq_sqrt (by positivity), Real.sq_sqrt (by norm_num)]
    rw [eq_div_iff (by positivity)]
    linear_combination (-(1 : ℝ) / 30 * ((10 + 2 * √5) * 12) - 4 / 5) * h5

/-- Hexagon–hexagon of the truncated icosahedron; the icosahedron. -/
lemma val_hexHex (hg : ⟪u, v⟫ = 4 * √5) (hX : ⟪u, u⟫ = 12) (hY : ⟪v, v⟫ = 12) :
    Real.pi - InnerProductGeometry.angle u v = 3 * Real.pi / 2 - 2 * β := by
  have hpi := Real.pi_pos
  have hb1 := β_le; have hb2 := β_ge
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  rw [show 3 * Real.pi / 2 - 2 * β = (Real.pi / 2 - 2 * β) + Real.pi by ring, Real.cos_add_pi,
    Real.cos_pi_div_two_sub, sin_two_β, Real.mul_self_sqrt (by norm_num)]
  ring

/-- Decagon–decagon of the truncated dodecahedron; the dodecahedron. -/
lemma val_decDec (hg : ⟪u, v⟫ = (2 + 2 * √5)) (hX : ⟪u, u⟫ = (10 + 2 * √5)) (hY : ⟪v, v⟫ = (10 + 2 * √5)) :
    Real.pi - InnerProductGeometry.angle u v = 2 * α := by
  have h5 := sqrt5_sq
  have ha1 := α_nonneg; have ha2 := α_le
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  have hr : (2 + 2 * √5) / (10 + 2 * √5) = √5 / 5 := by
    rw [div_eq_div_iff (by positivity) (by norm_num)]; linear_combination (-2 : ℝ) * h5
  rw [cos_two_α, Real.mul_self_sqrt (by positivity), hr]
  ring

/-- Base–side of the dodecahedron centre pyramid. -/
lemma val_pyrDBase (hg : ⟪u, v⟫ = (-16)) (hX : ⟪u, u⟫ = (10 + 2 * √5)) (hY : ⟪v, v⟫ = 64) :
    Real.pi - InnerProductGeometry.angle u v = α := by
  have h5 := sqrt5_sq
  refine pi_sub_angle_eq hg hX hY α_nonneg (by linarith [α_le, Real.pi_pos]) ?_
  set t : ℝ := 1 + ((1 + √5) / 2) ^ 2 with htdef
  have ht0 : 0 < t := by positivity
  have hX4 : (10 + 2 * √5 : ℝ) = 4 * t := by rw [htdef]; linear_combination (-1 : ℝ) * h5
  have h64 : √(64 : ℝ) = 8 := by
    rw [show (64 : ℝ) = 8 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have hs : √(4 * t) = 2 * √t := by
    rw [Real.sqrt_mul (by norm_num), show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have hst : 0 < √t := Real.sqrt_pos.2 ht0
  rw [hX4, hs, h64, α, Real.cos_arctan, ← htdef]
  field_simp
  ring

/-- Side–side of the dodecahedron centre pyramid. -/
lemma val_pyrDSide (hg : ⟪u, v⟫ = 32) (hX : ⟪u, u⟫ = 64) (hY : ⟪v, v⟫ = 64) :
    Real.pi - InnerProductGeometry.angle u v = 2 * Real.pi / 3 := by
  have hpi := Real.pi_pos
  refine pi_sub_angle_eq hg hX hY (by positivity) (by linarith) ?_
  rw [show 2 * Real.pi / 3 = Real.pi - Real.pi / 3 by ring, Real.cos_pi_sub, Real.cos_pi_div_three,
    Real.mul_self_sqrt (by norm_num)]
  norm_num

/-- Base–side of the icosahedron centre pyramid. -/
lemma val_pyrIBase (hg : ⟪u, v⟫ = (-16)) (hX : ⟪u, u⟫ = 12) (hY : ⟪v, v⟫ = (96 + 32 * √5)) :
    Real.pi - InnerProductGeometry.angle u v = 3 * Real.pi / 4 - β := by
  have h5 := sqrt5_sq
  have hpi := Real.pi_pos
  have hb1 := β_le; have hb2 := β_ge
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  apply cos_eq_neg_of_sq
  · have hc : 0 ≤ Real.cos (3 * Real.pi / 4 - β) :=
      Real.cos_nonneg_of_neg_pi_div_two_le_of_le (by linarith) (by linarith)
    have hd : (-16) / (√12 * √(96 + 32 * √5)) ≤ 0 := div_nonpos_of_nonpos_of_nonneg (by norm_num) (by positivity)
    exact mul_nonpos_of_nonneg_of_nonpos hc hd
  · rw [Real.cos_sq, show 2 * (3 * Real.pi / 4 - β) = (Real.pi / 2 - 2 * β) + Real.pi by ring,
      Real.cos_add_pi, Real.cos_pi_div_two_sub, sin_two_β,
      div_pow, mul_pow, Real.sq_sqrt (by norm_num), Real.sq_sqrt (by positivity)]
    rw [eq_div_iff (by positivity)]
    linear_combination (-64 : ℝ) * h5

/-- Side–side of the icosahedron centre pyramid. -/
lemma val_pyrISide (hg : ⟪u, v⟫ = (-16 - 16 * √5)) (hX : ⟪u, u⟫ = (96 + 32 * √5))
    (hY : ⟪v, v⟫ = (96 + 32 * √5)) :
    Real.pi - InnerProductGeometry.angle u v = 2 * Real.pi / 5 := by
  have h5 := sqrt5_sq
  have hpi := Real.pi_pos
  refine pi_sub_angle_eq hg hX hY (by positivity) (by linarith) ?_
  have hr : (-16 - 16 * √5) / (96 + 32 * √5) = (1 - √5) / 4 := by
    rw [div_eq_div_iff (by positivity) (by norm_num)]; linear_combination (32 : ℝ) * h5
  rw [show 2 * Real.pi / 5 = 2 * (Real.pi / 5) by ring, Real.cos_two_mul, Real.cos_pi_div_five,
    Real.mul_self_sqrt (by positivity), hr]
  linear_combination (1 / 8 : ℝ) * h5

/-- Square–hexagon of the truncated octahedron. -/
lemma val_toSqHex (hg : ⟪u, v⟫ = 1) (hX : ⟪u, u⟫ = 1) (hY : ⟪v, v⟫ = 3) :
    Real.pi - InnerProductGeometry.angle u v = Real.pi / 2 + γ := by
  have hpi := Real.pi_pos
  have hg1 := γ_nonneg; have hg2 := γ_le
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  rw [show Real.pi / 2 + γ = γ + Real.pi / 2 by ring, Real.cos_add_pi_div_two, γ, Real.sin_arccos,
    Real.sq_sqrt (by norm_num), Real.sqrt_one, one_mul, show (1 : ℝ) - 2 / 3 = 3⁻¹ by norm_num,
    Real.sqrt_inv, one_div]

/-- Hexagon–hexagon of the truncated octahedron. -/
lemma val_toHexHex (hg : ⟪u, v⟫ = 1) (hX : ⟪u, u⟫ = 3) (hY : ⟪v, v⟫ = 3) :
    Real.pi - InnerProductGeometry.angle u v = Real.pi - 2 * γ := by
  have hpi := Real.pi_pos
  have hg1 := γ_nonneg; have hg2 := γ_le
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  rw [Real.cos_pi_sub, cos_two_γ, Real.mul_self_sqrt (by norm_num)]

/-- Square–hexagon of the truncated cuboctahedron. -/
lemma val_tcoSqHex (hg : ⟪u, v⟫ = 2) (hX : ⟪u, u⟫ = 2) (hY : ⟪v, v⟫ = 3) :
    Real.pi - InnerProductGeometry.angle u v = Real.pi - γ := by
  have hpi := Real.pi_pos
  have hg1 := γ_nonneg; have hg2 := γ_le
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  rw [Real.cos_pi_sub, cos_γ, Real.sqrt_div (by norm_num : (0 : ℝ) ≤ 2), neg_inj,
    div_eq_div_iff (by positivity) (by positivity), ← mul_assoc, Real.mul_self_sqrt (by norm_num)]

/-- Square–octagon of the truncated cuboctahedron. -/
lemma val_tcoSqOct (hg : ⟪u, v⟫ = 1) (hX : ⟪u, u⟫ = 2) (hY : ⟪v, v⟫ = 1) :
    Real.pi - InnerProductGeometry.angle u v = 3 * Real.pi / 4 := by
  have hpi := Real.pi_pos
  refine pi_sub_angle_eq hg hX hY (by positivity) (by linarith) ?_
  rw [show 3 * Real.pi / 4 = Real.pi - Real.pi / 4 by ring, Real.cos_pi_sub, Real.cos_pi_div_four,
    Real.sqrt_one, mul_one, neg_inj, div_eq_div_iff (by norm_num) (by positivity), one_mul,
    Real.mul_self_sqrt (by norm_num)]

/-- Hexagon–octagon of the truncated cuboctahedron. -/
lemma val_tcoHexOct (hg : ⟪u, v⟫ = 1) (hX : ⟪u, u⟫ = 3) (hY : ⟪v, v⟫ = 1) :
    Real.pi - InnerProductGeometry.angle u v = Real.pi / 2 + γ := by
  have hpi := Real.pi_pos
  have hg1 := γ_nonneg; have hg2 := γ_le
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  rw [show Real.pi / 2 + γ = γ + Real.pi / 2 by ring, Real.cos_add_pi_div_two, γ, Real.sin_arccos,
    Real.sq_sqrt (by norm_num), Real.sqrt_one, mul_one, show (1 : ℝ) - 2 / 3 = 3⁻¹ by norm_num,
    Real.sqrt_inv, one_div]

lemma val_sqAlpha {g X Y : ℝ} (hg : ⟪u, v⟫ = g) (hX : ⟪u, u⟫ = X) (hY : ⟪v, v⟫ = Y) (hg0 : 0 ≤ g)
    (hX0 : 0 < X) (hY0 : 0 < Y) (hsq : (1 / 2 + √5 / 10) * (X * Y) = g ^ 2) :
    Real.pi - InnerProductGeometry.angle u v = Real.pi / 2 + α := by
  have hpi := Real.pi_pos
  have ha1 := α_nonneg; have ha2 := α_le
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  apply cos_eq_neg_of_sq
  · have hc : Real.cos (Real.pi / 2 + α) ≤ 0 := Real.cos_nonpos_of_pi_div_two_le_of_le (by linarith) (by linarith)
    have hd : 0 ≤ g / (√X * √Y) := by positivity
    nlinarith
  · rw [Real.cos_sq, show 2 * (Real.pi / 2 + α) = 2 * α + Real.pi by ring, Real.cos_add_pi, cos_two_α,
      div_pow, mul_pow, Real.sq_sqrt hX0.le, Real.sq_sqrt hY0.le, eq_div_iff (by positivity)]
    linarith

lemma val_sqBeta {g X Y : ℝ} (hg : ⟪u, v⟫ = g) (hX : ⟪u, u⟫ = X) (hY : ⟪v, v⟫ = Y) (hg0 : 0 ≤ g)
    (hX0 : 0 < X) (hY0 : 0 < Y) (hsq : (1 / 2 + √5 / 6) * (X * Y) = g ^ 2) :
    Real.pi - InnerProductGeometry.angle u v = 5 * Real.pi / 4 - β := by
  have hpi := Real.pi_pos
  have hb1 := β_le; have hb2 := β_ge
  refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
  apply cos_eq_neg_of_sq
  · have hc : Real.cos (5 * Real.pi / 4 - β) ≤ 0 :=
      Real.cos_nonpos_of_pi_div_two_le_of_le (by linarith) (by linarith)
    have hd : 0 ≤ g / (√X * √Y) := by positivity
    nlinarith
  · rw [Real.cos_sq, show 2 * (5 * Real.pi / 4 - β) = (Real.pi / 2 - 2 * β) + 2 * Real.pi by ring,
      Real.cos_add_two_pi, Real.cos_pi_div_two_sub, sin_two_β,
      div_pow, mul_pow, Real.sq_sqrt hX0.le, Real.sq_sqrt hY0.le, eq_div_iff (by positivity)]
    linarith

/-- Decagon–square of the truncated icosidodecahedron (two normal lengths). -/
lemma val_decSqA (hg : ⟪u, v⟫ = (2 + 2 * √5)) (hX : ⟪u, u⟫ = (10 + 2 * √5)) (hY : ⟪v, v⟫ = 4) :
    Real.pi - InnerProductGeometry.angle u v = Real.pi / 2 + α :=
  val_sqAlpha hg hX hY (by positivity) (by positivity) (by norm_num)
    (by linear_combination (-16 / 5 : ℝ) * sqrt5_sq)

lemma val_decSqB (hg : ⟪u, v⟫ = (6 + 2 * √5)) (hX : ⟪u, u⟫ = (10 + 2 * √5)) (hY : ⟪v, v⟫ = (6 + 2 * √5)) :
    Real.pi - InnerProductGeometry.angle u v = Real.pi / 2 + α :=
  val_sqAlpha hg hX hY (by positivity) (by positivity) (by positivity)
    (by linear_combination (6 / 5 + 2 / 5 * √5 : ℝ) * sqrt5_sq)

/-- Hexagon–square of the truncated icosidodecahedron (two normal lengths). -/
lemma val_hexSqA (hg : ⟪u, v⟫ = (6 + 2 * √5)) (hX : ⟪u, u⟫ = 12) (hY : ⟪v, v⟫ = (6 + 2 * √5)) :
    Real.pi - InnerProductGeometry.angle u v = 5 * Real.pi / 4 - β :=
  val_sqBeta hg hX hY (by positivity) (by norm_num) (by positivity) (by ring)

lemma val_hexSqB (hg : ⟪u, v⟫ = (2 + 2 * √5)) (hX : ⟪u, u⟫ = 12) (hY : ⟪v, v⟫ = 4) :
    Real.pi - InnerProductGeometry.angle u v = 5 * Real.pi / 4 - β :=
  val_sqBeta hg hX hY (by positivity) (by norm_num) (by norm_num)
    (by linear_combination (-4 : ℝ) * sqrt5_sq)

end Packets
