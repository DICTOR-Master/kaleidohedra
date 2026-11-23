/-
Lean study 5 of the shape-language canon (DICTO, 19 Nov 2026), part Q: FUJI, the third nonzero word.

FUJI is the third of the pieces AXE, CLEO, FUJI of the study of 14 October 2026: 7 corners, 7 faces
(six triangles at one corner, the apex, and a hexagon), 12 edges; corners in ℚ(√5) (exact form of the corner
data of that study). This file proves, from the 7 corners and 7 face normals (`IsEdgeData`, part P):

* `dehnSet_fuji`: the Dehn invariant of FUJI as a set is study 1's value of its edge list: six edges of
  length 1 at α + β (the edges at the apex), three edges of length 1 at γ and three edges of length (√5 − 1)/2
  at ε (the hexagon, alternating);
* `dehn_fuji_alpha_beta`, `dehn_cleo_alpha_beta`, `dehn_axe_alpha_beta`: the three words over the two
  angles α, β (with g = (√5 − 1)/2):
  CLEO = 3 ⊗ α + 3g ⊗ β, AXE = (1 + g) ⊗ α + 6 ⊗ β, FUJI = (9 − 3g) ⊗ α + (12 − 3g) ⊗ β;
* `dehnSet_fuji_ne_zero`: FUJI is a nonzero word;
* `fuji_not_scissorsCongruent_cube`, `fuji_not_scissorsCongruent_cubeRD`: no similar copy of FUJI is scissors
  congruent to a cube or to a cube ∩ rhombic dodecahedron solid of any size, in any position.

Why "not zero" needs α only, as in study 4: 9 − 3g is not a rational multiple of 12 − 3g (√5 is irrational),
so a ℚ-linear map ℝ → ℚ that kills 12 − 3g leaves a nonzero multiple of α, and α is not a rational multiple
of π (Niven's theorem, study 4). No independence of α and β is used.

The numbers in the certificates (which third face fixes the position along an edge, the determinants of the
triples of normals, the relations `n c + μ n c' = a n i + a' n j` for the nine pairs of faces that share only
the apex, the combinations that bound the coordinates) were computed exactly in ℚ(√5) on the compute host and
are checked here by Lean: polynomial identities by the tactic `grind` from √5² = 5, signs by `linarith` from
1 < √5 < 3, finite tables by `decide`.

Credits: study 4's `tmul_add_tmul_ne_zero`, `wordAlpha_not_ratPi` (Niven's theorem `niven`, Mathlib),
`theta_pair_of_gram`, `dist3`; Mathlib `Nat.Prime.irrational_sqrt`, `Real.arccos_neg`, `List.sum_ofFn`,
`TensorProduct.smul_tmul'`, `convexHull_min`; the tactic `grind`.
No `sorry`.
-/
module

public import Packets.Canon.Dehn5Edges

@[expose] public section

open scoped RealInnerProductSpace Real
open Set MeasureTheory Measure Module TensorProduct

namespace DehnCanon.Library

/-! ### Small tools -/

/-- The inner product of ℝ³ in coordinates. -/
lemma inner3' (x v : R3) : ⟪x, v⟫ = x 0 * v 0 + x 1 * v 1 + x 2 * v 2 := by
  simp [EuclideanSpace.inner_eq_star_dotProduct, Fin.sum_univ_three, dotProduct]; ring

/-- Three vectors of ℝ³ with nonzero determinant `D` have no common perpendicular direction. -/
lemma ind3 {x y z : R3} {D : ℝ}
    (hD : x 0 * (y 1 * z 2 - y 2 * z 1) - x 1 * (y 0 * z 2 - y 2 * z 0) + x 2 * (y 0 * z 1 - y 1 * z 0) = D)
    (hD0 : D ≠ 0) (v : R3) (h1 : ⟪x, v⟫ = 0) (h2 : ⟪y, v⟫ = 0) (h3 : ⟪z, v⟫ = 0) : v = 0 := by
  rw [inner3'] at h1 h2 h3
  have e0 : D * v 0 = 0 := by
    rw [← hD]
    linear_combination (y 1 * z 2 - y 2 * z 1) * h1 - (x 1 * z 2 - x 2 * z 1) * h2 +
      (x 1 * y 2 - x 2 * y 1) * h3
  have e1 : D * v 1 = 0 := by
    rw [← hD]
    linear_combination -(y 0 * z 2 - y 2 * z 0) * h1 + (x 0 * z 2 - x 2 * z 0) * h2 -
      (x 0 * y 2 - x 2 * y 0) * h3
  have e2 : D * v 2 = 0 := by
    rw [← hD]
    linear_combination (y 0 * z 1 - y 1 * z 0) * h1 - (x 0 * z 1 - x 1 * z 0) * h2 +
      (x 0 * y 1 - x 1 * y 0) * h3
  ext k
  fin_cases k
  · exact (mul_eq_zero.1 e0).resolve_left hD0
  · exact (mul_eq_zero.1 e1).resolve_left hD0
  · exact (mul_eq_zero.1 e2).resolve_left hD0

/-- `u ≥ 0` from a combination with coefficients ≥ 0 of three numbers ≥ 0. -/
lemma nonneg_of_comb3 {u A B C a b c : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (hA : 0 ≤ A)
    (hB : 0 ≤ B) (hC : 0 ≤ C) (h : u = a * A + b * B + c * C) : 0 ≤ u := by
  rw [h]; exact add_nonneg (add_nonneg (mul_nonneg ha hA) (mul_nonneg hb hB)) (mul_nonneg hc hC)

/-- Signs of numbers a + b√5 from 1 < √5 < 3. -/
macro "sqrt5_pos" : tactic =>
  `(tactic| (have h1 := one_lt_sqrt5; have h3 := sqrt5_lt_three; linarith))

macro "sqrt5_ne" : tactic =>
  `(tactic| (have h1 := one_lt_sqrt5; have h3 := sqrt5_lt_three; intro h; linarith))

/-! ### FUJI: corners, faces, edges -/

/-- The seven corners of FUJI (exact form of the corner data of the study of 14 October 2026);
corner 0 is the apex, corners 1 to 6 are the corners of the hexagon. -/
noncomputable def fujiP : Fin 7 → R3 :=
  ![!₂[-(1 + √5) / 4, -(1 + √5) / 4, -(1 + √5) / 4], !₂[-(1 + √5) / 4, -(1 + √5) / 4, -(5 + √5) / 4],
    !₂[-(1 + √5) / 2, -1 / 2, -(3 + √5) / 4], !₂[-1 / 2, -(3 + √5) / 4, -(1 + √5) / 2],
    !₂[-(5 + √5) / 4, -(1 + √5) / 4, -(1 + √5) / 4], !₂[-(1 + √5) / 4, -(5 + √5) / 4, -(1 + √5) / 4],
    !₂[-(3 + √5) / 4, -(1 + √5) / 2, -1 / 2]]

/-- Outward normals of the seven faces of FUJI: faces 0 to 5 are the six triangles at the apex
(0, 3, 5 with sides 1, 1, 1 and 1, 2, 4 with sides 1, 1, (√5 − 1)/2), face 6 is the hexagon. -/
noncomputable def fujiN : Fin 7 → R3 :=
  ![!₂[√5 - 1, √5 + 1, 0], !₂[2, √5 - 1, 0], !₂[0, 2, √5 - 1], !₂[√5 + 1, 0, √5 - 1],
    !₂[√5 - 1, 0, 2], !₂[0, √5 - 1, √5 + 1], !₂[-1, -1, -1]]

noncomputable def fujiB : Fin 7 → ℝ :=
  ![-(5 + √5) / 2, -(3 + √5) / 2, -(3 + √5) / 2, -(5 + √5) / 2, -(3 + √5) / 2, -(5 + √5) / 2,
    (7 + 3 * √5) / 4]

/-- **FUJI**, as the intersection of its seven face half-spaces. -/
def fujiSet : Set R3 := sol fujiN fujiB

/-- The table "face `m` passes through corner `k`". -/
def fujiZ : Fin 7 → Fin 7 → Bool :=
  ![![true, true, true, false, false, false, false], ![true, true, false, true, false, false, false],
    ![true, false, true, false, true, false, false], ![true, false, false, true, false, true, false],
    ![true, false, false, false, false, true, true], ![true, false, false, false, true, false, true],
    ![false, true, true, true, true, true, true]]

/-- The table of the values `b m − ⟪n m, p k⟫` (how far the corner `k` is inside the face `m`). -/
noncomputable def fujiS : Fin 7 → Fin 7 → ℝ :=
  ![![0, 0, 0, √5 - 1, √5 - 1, √5 + 1, √5 + 1], ![0, 0, √5 - 1, 0, 2, √5 - 1, 2],
    ![0, √5 - 1, 0, 2, 0, 2, √5 - 1], ![0, √5 - 1, √5 + 1, 0, √5 + 1, 0, √5 - 1],
    ![0, 2, 2, √5 - 1, √5 - 1, 0, 0], ![0, √5 + 1, √5 - 1, √5 + 1, 0, √5 - 1, 0],
    ![1, 0, 0, 0, 0, 0, 0]]

/-- The twelve edges: the two faces of each edge … -/
def fujiFi : Fin 12 → Fin 7 := ![0, 0, 3, 5, 3, 5, 6, 6, 6, 1, 2, 4]
def fujiFj : Fin 12 → Fin 7 := ![1, 2, 1, 2, 4, 4, 0, 3, 5, 6, 6, 6]

/-- … and its two corners. Edges 0 to 5 start at the apex; edges 6 to 11 are the sides of the hexagon. -/
def fujiVk : Fin 12 → Fin 7 := ![0, 0, 0, 0, 0, 0, 1, 3, 4, 1, 2, 5]
def fujiVl : Fin 12 → Fin 7 := ![1, 2, 3, 4, 5, 6, 2, 5, 6, 3, 4, 6]

lemma fuji_slack (m k : Fin 7) : fujiB m - ⟪fujiN m, fujiP k⟫ = fujiS m k := by
  have ht := sqrt5_sq
  fin_cases m <;> fin_cases k <;> simp [fujiB, fujiN, fujiP, fujiS, inner3] <;> grind

lemma fujiS_spec (m k : Fin 7) :
    (fujiZ m k = true → fujiS m k = 0) ∧ (fujiZ m k = false → 0 < fujiS m k) := by
  have h1 := one_lt_sqrt5
  fin_cases m <;> fin_cases k <;> simp [fujiZ, fujiS] <;> linarith

lemma fuji_tight (m k : Fin 7) (h : fujiZ m k = true) : ⟪fujiN m, fujiP k⟫ = fujiB m := by
  have h1 := fuji_slack m k
  have h2 := (fujiS_spec m k).1 h
  linarith

lemma fuji_lt (m k : Fin 7) (h : fujiZ m k = false) : ⟪fujiN m, fujiP k⟫ < fujiB m := by
  have h1 := fuji_slack m k
  have h2 := (fujiS_spec m k).2 h
  linarith

lemma fuji_le (m k : Fin 7) : ⟪fujiN m, fujiP k⟫ ≤ fujiB m := by
  cases h : fujiZ m k
  · exact (fuji_lt m k h).le
  · exact (fuji_tight m k h).le

/-- The statement of `IsEdgeData.cover` for FUJI. -/
def FujiCover (x : R3) (i j : Fin 7) : Prop :=
  (∃ e, ({i, j} : Set (Fin 7)) = {fujiFi e, fujiFj e} ∧
    x ∈ segment ℝ (fujiP (fujiVk e)) (fujiP (fujiVl e))) ∨ ∃ k, x = fujiP k

/-! ### Independent triples of normals (determinants computed exactly in ℚ(√5)) -/

lemma fuji_ind_0_1_6 (v : R3) (h1 : ⟪fujiN 0, v⟫ = 0) (h2 : ⟪fujiN 1, v⟫ = 0)
    (h3 : ⟪fujiN 6, v⟫ = 0) : v = 0 :=
  ind3 (D := -4 + 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_0_2_6 (v : R3) (h1 : ⟪fujiN 0, v⟫ = 0) (h2 : ⟪fujiN 2, v⟫ = 0)
    (h3 : ⟪fujiN 6, v⟫ = 0) : v = 0 :=
  ind3 (D := 4 - 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_0_3_1 (v : R3) (h1 : ⟪fujiN 0, v⟫ = 0) (h2 : ⟪fujiN 3, v⟫ = 0)
    (h3 : ⟪fujiN 1, v⟫ = 0) : v = 0 :=
  ind3 (D := 24 - 8 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_0_4_1 (v : R3) (h1 : ⟪fujiN 0, v⟫ = 0) (h2 : ⟪fujiN 4, v⟫ = 0)
    (h3 : ⟪fujiN 1, v⟫ = 0) : v = 0 :=
  ind3 (D := -8 + 8 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_0_5_1 (v : R3) (h1 : ⟪fujiN 0, v⟫ = 0) (h2 : ⟪fujiN 5, v⟫ = 0)
    (h3 : ⟪fujiN 1, v⟫ = 0) : v = 0 :=
  ind3 (D := 16) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_0_6_2 (v : R3) (h1 : ⟪fujiN 0, v⟫ = 0) (h2 : ⟪fujiN 6, v⟫ = 0)
    (h3 : ⟪fujiN 2, v⟫ = 0) : v = 0 :=
  ind3 (D := -4 + 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_1_2_0 (v : R3) (h1 : ⟪fujiN 1, v⟫ = 0) (h2 : ⟪fujiN 2, v⟫ = 0)
    (h3 : ⟪fujiN 0, v⟫ = 0) : v = 0 :=
  ind3 (D := -24 + 8 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_1_3_6 (v : R3) (h1 : ⟪fujiN 1, v⟫ = 0) (h2 : ⟪fujiN 3, v⟫ = 0)
    (h3 : ⟪fujiN 6, v⟫ = 0) : v = 0 :=
  ind3 (D := -4 + 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_1_4_0 (v : R3) (h1 : ⟪fujiN 1, v⟫ = 0) (h2 : ⟪fujiN 4, v⟫ = 0)
    (h3 : ⟪fujiN 0, v⟫ = 0) : v = 0 :=
  ind3 (D := 8 - 8 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_1_5_0 (v : R3) (h1 : ⟪fujiN 1, v⟫ = 0) (h2 : ⟪fujiN 5, v⟫ = 0)
    (h3 : ⟪fujiN 0, v⟫ = 0) : v = 0 :=
  ind3 (D := -16) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_1_6_3 (v : R3) (h1 : ⟪fujiN 1, v⟫ = 0) (h2 : ⟪fujiN 6, v⟫ = 0)
    (h3 : ⟪fujiN 3, v⟫ = 0) : v = 0 :=
  ind3 (D := 4 - 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_2_3_0 (v : R3) (h1 : ⟪fujiN 2, v⟫ = 0) (h2 : ⟪fujiN 3, v⟫ = 0)
    (h3 : ⟪fujiN 0, v⟫ = 0) : v = 0 :=
  ind3 (D := 16) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_2_4_0 (v : R3) (h1 : ⟪fujiN 2, v⟫ = 0) (h2 : ⟪fujiN 4, v⟫ = 0)
    (h3 : ⟪fujiN 0, v⟫ = 0) : v = 0 :=
  ind3 (D := -8 + 8 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_2_5_6 (v : R3) (h1 : ⟪fujiN 2, v⟫ = 0) (h2 : ⟪fujiN 5, v⟫ = 0)
    (h3 : ⟪fujiN 6, v⟫ = 0) : v = 0 :=
  ind3 (D := 4 - 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_2_6_5 (v : R3) (h1 : ⟪fujiN 2, v⟫ = 0) (h2 : ⟪fujiN 6, v⟫ = 0)
    (h3 : ⟪fujiN 5, v⟫ = 0) : v = 0 :=
  ind3 (D := -4 + 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_3_4_6 (v : R3) (h1 : ⟪fujiN 3, v⟫ = 0) (h2 : ⟪fujiN 4, v⟫ = 0)
    (h3 : ⟪fujiN 6, v⟫ = 0) : v = 0 :=
  ind3 (D := -4 + 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_3_5_0 (v : R3) (h1 : ⟪fujiN 3, v⟫ = 0) (h2 : ⟪fujiN 5, v⟫ = 0)
    (h3 : ⟪fujiN 0, v⟫ = 0) : v = 0 :=
  ind3 (D := -(16 * √5)) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_3_6_4 (v : R3) (h1 : ⟪fujiN 3, v⟫ = 0) (h2 : ⟪fujiN 6, v⟫ = 0)
    (h3 : ⟪fujiN 4, v⟫ = 0) : v = 0 :=
  ind3 (D := 4 - 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_4_5_6 (v : R3) (h1 : ⟪fujiN 4, v⟫ = 0) (h2 : ⟪fujiN 5, v⟫ = 0)
    (h3 : ⟪fujiN 6, v⟫ = 0) : v = 0 :=
  ind3 (D := -4 + 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_4_6_5 (v : R3) (h1 : ⟪fujiN 4, v⟫ = 0) (h2 : ⟪fujiN 6, v⟫ = 0)
    (h3 : ⟪fujiN 5, v⟫ = 0) : v = 0 :=
  ind3 (D := 4 - 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

lemma fuji_ind_5_6_4 (v : R3) (h1 : ⟪fujiN 5, v⟫ = 0) (h2 : ⟪fujiN 6, v⟫ = 0)
    (h3 : ⟪fujiN 4, v⟫ = 0) : v = 0 :=
  ind3 (D := -4 + 4 * √5) (by have ht := sqrt5_sq; simp [fujiN]; grind) (by sqrt5_ne) v h1 h2 h3

/-! ### The cover: every pair of faces -/

lemma fuji_cover_0_1 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 0, x⟫ = fujiB 0)
    (hj : ⟪fujiN 1, x⟫ = fujiB 1) : FujiCover x 0 1 :=
  Or.inl ⟨0, rfl, mem_segment_of_tight fuji_ind_0_1_6
    (fuji_tight 0 0 (by decide)) (fuji_tight 0 1 (by decide)) (fuji_tight 1 0 (by decide))
    (fuji_tight 1 1 (by decide)) (fuji_tight 6 1 (by decide)) (fuji_lt 6 0 (by decide))
    (fuji_tight 2 0 (by decide)) (fuji_lt 2 1 (by decide)) hx hi hj⟩

lemma fuji_cover_0_2 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 0, x⟫ = fujiB 0)
    (hj : ⟪fujiN 2, x⟫ = fujiB 2) : FujiCover x 0 2 :=
  Or.inl ⟨1, rfl, mem_segment_of_tight fuji_ind_0_2_6
    (fuji_tight 0 0 (by decide)) (fuji_tight 0 2 (by decide)) (fuji_tight 2 0 (by decide))
    (fuji_tight 2 2 (by decide)) (fuji_tight 6 2 (by decide)) (fuji_lt 6 0 (by decide))
    (fuji_tight 1 0 (by decide)) (fuji_lt 1 2 (by decide)) hx hi hj⟩

lemma fuji_cover_0_3 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 0, x⟫ = fujiB 0)
    (hj : ⟪fujiN 3, x⟫ = fujiB 3) : FujiCover x 0 3 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_0_3_1
    (fuji_tight 1 0 (by decide)) (fuji_tight 2 0 (by decide)) (fuji_tight 0 0 (by decide))
    (fuji_tight 3 0 (by decide)) (μ := (3 - √5) / 2) (a := (√5 - 1) / 2) (a' := (3 - √5) / 2) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_0_4 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 0, x⟫ = fujiB 0)
    (hj : ⟪fujiN 4, x⟫ = fujiB 4) : FujiCover x 0 4 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_0_4_1
    (fuji_tight 1 0 (by decide)) (fuji_tight 2 0 (by decide)) (fuji_tight 0 0 (by decide))
    (fuji_tight 4 0 (by decide)) (μ := 1) (a := 1) (a' := (√5 - 1) / 2) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_0_5 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 0, x⟫ = fujiB 0)
    (hj : ⟪fujiN 5, x⟫ = fujiB 5) : FujiCover x 0 5 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_0_5_1
    (fuji_tight 1 0 (by decide)) (fuji_tight 2 0 (by decide)) (fuji_tight 0 0 (by decide))
    (fuji_tight 5 0 (by decide)) (μ := (3 + √5) / 2) (a := (1 + √5) / 2) (a' := 1) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_0_6 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 0, x⟫ = fujiB 0)
    (hj : ⟪fujiN 6, x⟫ = fujiB 6) : FujiCover x 0 6 :=
  Or.inl ⟨6, Set.pair_comm _ _, mem_segment_of_tight fuji_ind_0_6_2
    (fuji_tight 0 1 (by decide)) (fuji_tight 0 2 (by decide)) (fuji_tight 6 1 (by decide))
    (fuji_tight 6 2 (by decide)) (fuji_tight 2 2 (by decide)) (fuji_lt 2 1 (by decide))
    (fuji_tight 1 1 (by decide)) (fuji_lt 1 2 (by decide)) hx hi hj⟩

lemma fuji_cover_1_2 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 1, x⟫ = fujiB 1)
    (hj : ⟪fujiN 2, x⟫ = fujiB 2) : FujiCover x 1 2 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_1_2_0
    (fuji_tight 0 0 (by decide)) (fuji_tight 3 0 (by decide)) (fuji_tight 1 0 (by decide))
    (fuji_tight 2 0 (by decide)) (μ := (√5 - 1) / 2) (a := (1 + √5) / 2) (a' := (√5 - 1) / 2) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_1_3 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 1, x⟫ = fujiB 1)
    (hj : ⟪fujiN 3, x⟫ = fujiB 3) : FujiCover x 1 3 :=
  Or.inl ⟨2, Set.pair_comm _ _, mem_segment_of_tight fuji_ind_1_3_6
    (fuji_tight 1 0 (by decide)) (fuji_tight 1 3 (by decide)) (fuji_tight 3 0 (by decide))
    (fuji_tight 3 3 (by decide)) (fuji_tight 6 3 (by decide)) (fuji_lt 6 0 (by decide))
    (fuji_tight 0 0 (by decide)) (fuji_lt 0 3 (by decide)) hx hi hj⟩

lemma fuji_cover_1_4 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 1, x⟫ = fujiB 1)
    (hj : ⟪fujiN 4, x⟫ = fujiB 4) : FujiCover x 1 4 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_1_4_0
    (fuji_tight 0 0 (by decide)) (fuji_tight 3 0 (by decide)) (fuji_tight 1 0 (by decide))
    (fuji_tight 4 0 (by decide)) (μ := (1 + √5) / 2) (a := (3 + √5) / 2) (a' := 1) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_1_5 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 1, x⟫ = fujiB 1)
    (hj : ⟪fujiN 5, x⟫ = fujiB 5) : FujiCover x 1 5 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_1_5_0
    (fuji_tight 0 0 (by decide)) (fuji_tight 3 0 (by decide)) (fuji_tight 1 0 (by decide))
    (fuji_tight 5 0 (by decide)) (μ := 1) (a := √5) (a' := (3 - √5) / 2) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_1_6 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 1, x⟫ = fujiB 1)
    (hj : ⟪fujiN 6, x⟫ = fujiB 6) : FujiCover x 1 6 :=
  Or.inl ⟨9, rfl, mem_segment_of_tight fuji_ind_1_6_3
    (fuji_tight 1 1 (by decide)) (fuji_tight 1 3 (by decide)) (fuji_tight 6 1 (by decide))
    (fuji_tight 6 3 (by decide)) (fuji_tight 3 3 (by decide)) (fuji_lt 3 1 (by decide))
    (fuji_tight 0 1 (by decide)) (fuji_lt 0 3 (by decide)) hx hi hj⟩

lemma fuji_cover_2_3 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 2, x⟫ = fujiB 2)
    (hj : ⟪fujiN 3, x⟫ = fujiB 3) : FujiCover x 2 3 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_2_3_0
    (fuji_tight 0 0 (by decide)) (fuji_tight 4 0 (by decide)) (fuji_tight 2 0 (by decide))
    (fuji_tight 3 0 (by decide)) (μ := (1 + √5) / 2) (a := (1 + √5) / 2) (a' := 1) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_2_4 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 2, x⟫ = fujiB 2)
    (hj : ⟪fujiN 4, x⟫ = fujiB 4) : FujiCover x 2 4 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_2_4_0
    (fuji_tight 0 0 (by decide)) (fuji_tight 5 0 (by decide)) (fuji_tight 2 0 (by decide))
    (fuji_tight 4 0 (by decide)) (μ := (1 + √5) / 2) (a := (3 + √5) / 2) (a' := 1) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_2_5 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 2, x⟫ = fujiB 2)
    (hj : ⟪fujiN 5, x⟫ = fujiB 5) : FujiCover x 2 5 :=
  Or.inl ⟨3, Set.pair_comm _ _, mem_segment_of_tight fuji_ind_2_5_6
    (fuji_tight 2 0 (by decide)) (fuji_tight 2 4 (by decide)) (fuji_tight 5 0 (by decide))
    (fuji_tight 5 4 (by decide)) (fuji_tight 6 4 (by decide)) (fuji_lt 6 0 (by decide))
    (fuji_tight 0 0 (by decide)) (fuji_lt 0 4 (by decide)) hx hi hj⟩

lemma fuji_cover_2_6 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 2, x⟫ = fujiB 2)
    (hj : ⟪fujiN 6, x⟫ = fujiB 6) : FujiCover x 2 6 :=
  Or.inl ⟨10, rfl, mem_segment_of_tight fuji_ind_2_6_5
    (fuji_tight 2 2 (by decide)) (fuji_tight 2 4 (by decide)) (fuji_tight 6 2 (by decide))
    (fuji_tight 6 4 (by decide)) (fuji_tight 5 4 (by decide)) (fuji_lt 5 2 (by decide))
    (fuji_tight 0 2 (by decide)) (fuji_lt 0 4 (by decide)) hx hi hj⟩

lemma fuji_cover_3_4 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 3, x⟫ = fujiB 3)
    (hj : ⟪fujiN 4, x⟫ = fujiB 4) : FujiCover x 3 4 :=
  Or.inl ⟨4, rfl, mem_segment_of_tight fuji_ind_3_4_6
    (fuji_tight 3 0 (by decide)) (fuji_tight 3 5 (by decide)) (fuji_tight 4 0 (by decide))
    (fuji_tight 4 5 (by decide)) (fuji_tight 6 5 (by decide)) (fuji_lt 6 0 (by decide))
    (fuji_tight 0 0 (by decide)) (fuji_lt 0 5 (by decide)) hx hi hj⟩

lemma fuji_cover_3_5 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 3, x⟫ = fujiB 3)
    (hj : ⟪fujiN 5, x⟫ = fujiB 5) : FujiCover x 3 5 :=
  Or.inr ⟨0, eq_of_tight fuji_ind_3_5_0
    (fuji_tight 0 0 (by decide)) (fuji_tight 4 0 (by decide)) (fuji_tight 3 0 (by decide))
    (fuji_tight 5 0 (by decide)) (μ := (5 + 3 * √5) / 2) (a := (3 + √5) / 2) (a' := (3 + √5) / 2) (by sqrt5_pos)
    (by have ht := sqrt5_sq; ext t; fin_cases t <;> simp [fujiN] <;> grind) hx hi hj⟩

lemma fuji_cover_3_6 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 3, x⟫ = fujiB 3)
    (hj : ⟪fujiN 6, x⟫ = fujiB 6) : FujiCover x 3 6 :=
  Or.inl ⟨7, Set.pair_comm _ _, mem_segment_of_tight fuji_ind_3_6_4
    (fuji_tight 3 3 (by decide)) (fuji_tight 3 5 (by decide)) (fuji_tight 6 3 (by decide))
    (fuji_tight 6 5 (by decide)) (fuji_tight 4 5 (by decide)) (fuji_lt 4 3 (by decide))
    (fuji_tight 1 3 (by decide)) (fuji_lt 1 5 (by decide)) hx hi hj⟩

lemma fuji_cover_4_5 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 4, x⟫ = fujiB 4)
    (hj : ⟪fujiN 5, x⟫ = fujiB 5) : FujiCover x 4 5 :=
  Or.inl ⟨5, Set.pair_comm _ _, mem_segment_of_tight fuji_ind_4_5_6
    (fuji_tight 4 0 (by decide)) (fuji_tight 4 6 (by decide)) (fuji_tight 5 0 (by decide))
    (fuji_tight 5 6 (by decide)) (fuji_tight 6 6 (by decide)) (fuji_lt 6 0 (by decide))
    (fuji_tight 0 0 (by decide)) (fuji_lt 0 6 (by decide)) hx hi hj⟩

lemma fuji_cover_4_6 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 4, x⟫ = fujiB 4)
    (hj : ⟪fujiN 6, x⟫ = fujiB 6) : FujiCover x 4 6 :=
  Or.inl ⟨11, rfl, mem_segment_of_tight fuji_ind_4_6_5
    (fuji_tight 4 5 (by decide)) (fuji_tight 4 6 (by decide)) (fuji_tight 6 5 (by decide))
    (fuji_tight 6 6 (by decide)) (fuji_tight 5 6 (by decide)) (fuji_lt 5 5 (by decide))
    (fuji_tight 3 5 (by decide)) (fuji_lt 3 6 (by decide)) hx hi hj⟩

lemma fuji_cover_5_6 {x : R3} (hx : x ∈ sol fujiN fujiB) (hi : ⟪fujiN 5, x⟫ = fujiB 5)
    (hj : ⟪fujiN 6, x⟫ = fujiB 6) : FujiCover x 5 6 :=
  Or.inl ⟨8, Set.pair_comm _ _, mem_segment_of_tight fuji_ind_5_6_4
    (fuji_tight 5 4 (by decide)) (fuji_tight 5 6 (by decide)) (fuji_tight 6 4 (by decide))
    (fuji_tight 6 6 (by decide)) (fuji_tight 4 6 (by decide)) (fuji_lt 4 4 (by decide))
    (fuji_tight 2 4 (by decide)) (fuji_lt 2 6 (by decide)) hx hi hj⟩

lemma fuji_cover_lt {x : R3} (hx : x ∈ sol fujiN fujiB) : ∀ i j : Fin 7, i < j →
    ⟪fujiN i, x⟫ = fujiB i → ⟪fujiN j, x⟫ = fujiB j → FujiCover x i j := by
  intro i j hij hi hj
  fin_cases i <;> fin_cases j <;> first
    | exact absurd hij (by decide)
    | exact fuji_cover_0_1 hx hi hj
    | exact fuji_cover_0_2 hx hi hj
    | exact fuji_cover_0_3 hx hi hj
    | exact fuji_cover_0_4 hx hi hj
    | exact fuji_cover_0_5 hx hi hj
    | exact fuji_cover_0_6 hx hi hj
    | exact fuji_cover_1_2 hx hi hj
    | exact fuji_cover_1_3 hx hi hj
    | exact fuji_cover_1_4 hx hi hj
    | exact fuji_cover_1_5 hx hi hj
    | exact fuji_cover_1_6 hx hi hj
    | exact fuji_cover_2_3 hx hi hj
    | exact fuji_cover_2_4 hx hi hj
    | exact fuji_cover_2_5 hx hi hj
    | exact fuji_cover_2_6 hx hi hj
    | exact fuji_cover_3_4 hx hi hj
    | exact fuji_cover_3_5 hx hi hj
    | exact fuji_cover_3_6 hx hi hj
    | exact fuji_cover_4_5 hx hi hj
    | exact fuji_cover_4_6 hx hi hj
    | exact fuji_cover_5_6 hx hi hj
lemma fuji_cover {x : R3} (hx : x ∈ sol fujiN fujiB) (i j : Fin 7) (hij : i ≠ j)
    (hi : ⟪fujiN i, x⟫ = fujiB i) (hj : ⟪fujiN j, x⟫ = fujiB j) : FujiCover x i j := by
  rcases lt_or_gt_of_ne hij with h | h
  · exact fuji_cover_lt hx i j h hi hj
  · rcases fuji_cover_lt hx j i h hj hi with ⟨e, he, hseg⟩ | hk
    · exact Or.inl ⟨e, (Set.pair_comm i j).trans he, hseg⟩
    · exact Or.inr hk

/-! ### FUJI is bounded -/

theorem fuji_bounded : Bornology.IsBounded (sol fujiN fujiB) := by
  refine bounded_of_coords 3 (fun x hx i => ?_)
  have ht := sqrt5_sq
  have h1 := one_lt_sqrt5
  have h3 := sqrt5_lt_three
  have f0 : ⟪(!₂[√5 - 1, √5 + 1, 0] : R3), x⟫ ≤ -(5 + √5) / 2 := hx 0
  have f1 : ⟪(!₂[2, √5 - 1, 0] : R3), x⟫ ≤ -(3 + √5) / 2 := hx 1
  have f2 : ⟪(!₂[0, 2, √5 - 1] : R3), x⟫ ≤ -(3 + √5) / 2 := hx 2
  have f3 : ⟪(!₂[√5 + 1, 0, √5 - 1] : R3), x⟫ ≤ -(5 + √5) / 2 := hx 3
  have f4 : ⟪(!₂[√5 - 1, 0, 2] : R3), x⟫ ≤ -(3 + √5) / 2 := hx 4
  have f5 : ⟪(!₂[0, √5 - 1, √5 + 1] : R3), x⟫ ≤ -(5 + √5) / 2 := hx 5
  have f6 : ⟪(!₂[-1, -1, -1] : R3), x⟫ ≤ (7 + 3 * √5) / 4 := hx 6
  rw [inner3] at f0 f1 f2 f3 f4 f5 f6
  have u0 : 0 ≤ -1 / 2 - x 0 :=
    nonneg_of_comb3 (a := 1 / 4) (b := 1 / 4) (c := (√5 - 1) / 4) (by norm_num) (by norm_num)
      (by linarith) (sub_nonneg.2 f1) (sub_nonneg.2 f3) (sub_nonneg.2 f6) (by grind)
  have l0 : 0 ≤ 1 + √5 / 2 + x 0 :=
    nonneg_of_comb3 (a := 1 / 4) (b := (1 + √5) / 8) (c := (3 + √5) / 4) (by norm_num) (by linarith)
      (by linarith) (sub_nonneg.2 f0) (sub_nonneg.2 f5) (sub_nonneg.2 f6) (by grind)
  have u1 : 0 ≤ -1 / 2 - x 1 :=
    nonneg_of_comb3 (a := 1 / 4) (b := 1 / 4) (c := (√5 - 1) / 4) (by norm_num) (by norm_num)
      (by linarith) (sub_nonneg.2 f0) (sub_nonneg.2 f2) (sub_nonneg.2 f6) (by grind)
  have l1 : 0 ≤ 1 + √5 / 2 + x 1 :=
    nonneg_of_comb3 (a := (1 + √5) / 8) (b := 1 / 4) (c := (3 + √5) / 4) (by linarith) (by norm_num)
      (by linarith) (sub_nonneg.2 f3) (sub_nonneg.2 f5) (sub_nonneg.2 f6) (by grind)
  have u2 : 0 ≤ -1 / 2 - x 2 :=
    nonneg_of_comb3 (a := 1 / 4) (b := 1 / 4) (c := (√5 - 1) / 4) (by norm_num) (by norm_num)
      (by linarith) (sub_nonneg.2 f4) (sub_nonneg.2 f5) (sub_nonneg.2 f6) (by grind)
  have l2 : 0 ≤ 1 + √5 / 2 + x 2 :=
    nonneg_of_comb3 (a := (1 + √5) / 8) (b := 1 / 4) (c := (3 + √5) / 4) (by linarith) (by norm_num)
      (by linarith) (sub_nonneg.2 f0) (sub_nonneg.2 f3) (sub_nonneg.2 f6) (by grind)
  have key : |x 0| ≤ 3 ∧ |x 1| ≤ 3 ∧ |x 2| ≤ 3 :=
    ⟨abs_le.2 ⟨by linarith, by linarith⟩, abs_le.2 ⟨by linarith, by linarith⟩,
      abs_le.2 ⟨by linarith, by linarith⟩⟩
  fin_cases i
  exacts [key.1, key.2.1, key.2.2]

/-- FUJI is a convex polytope. -/
theorem isPoly_fuji : IsPoly fujiSet := ⟨fuji_bounded, Fin 7, inferInstance, fujiN, _, rfl⟩

/-! ### The edge data of FUJI -/

/-- Three faces through each corner. -/
def fujiT : Fin 7 → Fin 7 × Fin 7 × Fin 7 :=
  ![(0, 1, 2), (0, 1, 6), (0, 2, 6), (1, 3, 6), (2, 5, 6), (3, 4, 6), (4, 5, 6)]

lemma fujiT_spec : ∀ k, (fujiT k).1 ≠ (fujiT k).2.1 ∧ (fujiT k).1 ≠ (fujiT k).2.2 ∧
    (fujiT k).2.1 ≠ (fujiT k).2.2 ∧ fujiZ (fujiT k).1 k = true ∧ fujiZ (fujiT k).2.1 k = true ∧
    fujiZ (fujiT k).2.2 k = true := by decide

lemma fujiE_ne : ∀ e, fujiFi e ≠ fujiFj e := by decide

lemma fujiE_inj : ∀ e e', ({fujiFi e, fujiFj e} : Finset (Fin 7)) = {fujiFi e', fujiFj e'} → e = e' := by
  decide

lemma fujiE_tight : ∀ e, fujiZ (fujiFi e) (fujiVk e) = true ∧ fujiZ (fujiFi e) (fujiVl e) = true ∧
    fujiZ (fujiFj e) (fujiVk e) = true ∧ fujiZ (fujiFj e) (fujiVl e) = true := by decide

lemma fujiE_other : ∀ e m, m ≠ fujiFi e → m ≠ fujiFj e →
    fujiZ m (fujiVk e) = false ∨ fujiZ m (fujiVl e) = false := by decide

/-- **The corners, faces and edges of FUJI satisfy `IsEdgeData`.** -/
theorem fuji_isEdgeData : IsEdgeData fujiN fujiB fujiP fujiFi fujiFj fujiVk fujiVl where
  bounded := fuji_bounded
  corner_mem := fun k m => fuji_le m k
  corner_three := fun k => by
    obtain ⟨h1, h2, h3, t1, t2, t3⟩ := fujiT_spec k
    exact ⟨_, _, _, h1, h2, h3, fuji_tight _ _ t1, fuji_tight _ _ t2, fuji_tight _ _ t3⟩
  faces_ne := fujiE_ne
  faces_inj := fun e e' h => by
    apply fujiE_inj
    apply Finset.coe_injective
    rw [Finset.coe_pair, Finset.coe_pair]
    exact h
  tight := fun e => by
    obtain ⟨t1, t2, t3, t4⟩ := fujiE_tight e
    exact ⟨fuji_tight _ _ t1, fuji_tight _ _ t2, fuji_tight _ _ t3, fuji_tight _ _ t4⟩
  other := fun e m h1 h2 => by
    rcases fujiE_other e m h1 h2 with h | h
    · exact Or.inl (fuji_lt _ _ h)
    · exact Or.inr (fuji_lt _ _ h)
  cover := fun x hx i j hij hi hj => fuji_cover hx i j hij hi hj

/-- The convex hull of the seven corners lies in FUJI. (The other inclusion is not proved here.) -/
theorem convexHull_fujiP_subset : convexHull ℝ (Set.range fujiP) ⊆ fujiSet := by
  apply convexHull_min _ (convex_sol fujiN fujiB)
  rintro _ ⟨k, rfl⟩
  exact fuji_isEdgeData.corner_mem k

/-- The open edges of FUJI: the points where exactly the two faces of the edge `e` are tight. -/
theorem fuji_faceSet_edge (e : Fin 12) :
    faceSet fujiN fujiB {fujiFi e, fujiFj e} = openSegment ℝ (fujiP (fujiVk e)) (fujiP (fujiVl e)) :=
  fuji_isEdgeData.faceSet_edge e

/-! ### Lengths and angles of the twelve edges -/

lemma fuji_dist_one : ∀ e : Fin 12, e.val < 9 → dist (fujiP (fujiVk e)) (fujiP (fujiVl e)) = 1 := by
  have ht := sqrt5_sq
  intro e he
  apply dist3 _ _ zero_le_one
  fin_cases e <;> simp [fujiP, fujiVk, fujiVl] at he ⊢ <;> grind

lemma fuji_dist_gold : ∀ e : Fin 12, 9 ≤ e.val →
    dist (fujiP (fujiVk e)) (fujiP (fujiVl e)) = (√5 - 1) / 2 := by
  have ht := sqrt5_sq
  have h1 := one_lt_sqrt5
  intro e he
  apply dist3 _ _ (by linarith)
  fin_cases e <;> simp [fujiP, fujiVk, fujiVl] at he ⊢ <;> grind

/-- The Gram numbers of the normals: the three kinds of faces … -/
lemma fujiN_sq : ⟪fujiN 0, fujiN 0⟫ = 12 ∧ ⟪fujiN 3, fujiN 3⟫ = 12 ∧ ⟪fujiN 5, fujiN 5⟫ = 12 ∧
    ⟪fujiN 1, fujiN 1⟫ = 10 - 2 * √5 ∧ ⟪fujiN 2, fujiN 2⟫ = 10 - 2 * √5 ∧
    ⟪fujiN 4, fujiN 4⟫ = 10 - 2 * √5 ∧ ⟪fujiN 6, fujiN 6⟫ = 3 := by
  have ht := sqrt5_sq
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp [fujiN, norm3_sq] <;> grind

/-- … and the twelve pairs of faces that share an edge. -/
lemma fujiN_gram : ⟪fujiN 0, fujiN 1⟫ = -(-(2 * √5 + 2)) ∧ ⟪fujiN 0, fujiN 2⟫ = -(-(2 * √5 + 2)) ∧
    ⟪fujiN 3, fujiN 1⟫ = -(-(2 * √5 + 2)) ∧ ⟪fujiN 5, fujiN 2⟫ = -(-(2 * √5 + 2)) ∧
    ⟪fujiN 3, fujiN 4⟫ = -(-(2 * √5 + 2)) ∧ ⟪fujiN 5, fujiN 4⟫ = -(-(2 * √5 + 2)) ∧
    ⟪fujiN 6, fujiN 0⟫ = -(2 * √5) ∧ ⟪fujiN 6, fujiN 3⟫ = -(2 * √5) ∧ ⟪fujiN 6, fujiN 5⟫ = -(2 * √5) ∧
    ⟪fujiN 1, fujiN 6⟫ = -(√5 + 1) ∧ ⟪fujiN 2, fujiN 6⟫ = -(√5 + 1) ∧ ⟪fujiN 4, fujiN 6⟫ = -(√5 + 1) := by
  have ht := sqrt5_sq
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp [fujiN, inner3] <;> grind

lemma apex_gram_ne : (12 : ℝ) * (10 - 2 * √5) ≠ (-(2 * √5 + 2)) ^ 2 := by
  intro h
  have h3 : (√5 : ℝ) = 3 := by linear_combination (-1 / 32 : ℝ) * h - (1 / 8 : ℝ) * sqrt5_sq
  linarith [sqrt5_lt_three]

lemma eps_gram_ne : (10 - 2 * √5) * 3 ≠ (√5 + 1) ^ 2 := by
  intro h
  have h3 : (√5 : ℝ) = 3 := by linear_combination (-1 / 8 : ℝ) * h - (1 / 8 : ℝ) * sqrt5_sq
  linarith [sqrt5_lt_three]

/-- The angle value read off from the normals of two neighbouring triangles is π − ε = α + β. -/
lemma apex_form : Real.arccos (-(2 * √5 + 2) / √(12 * (10 - 2 * √5))) = wordAlpha + wordBeta := by
  rw [wordAlpha_add_wordBeta]
  unfold wordEps wordR
  rw [← Real.arccos_neg]
  congr 1
  rw [show (12 : ℝ) * (10 - 2 * √5) = 2 ^ 2 * (3 * (10 - 2 * √5)) by ring, Real.sqrt_mul (by norm_num),
    Real.sqrt_sq (by norm_num), show -(2 * √5 + 2) = 2 * -(√5 + 1) by ring,
    mul_div_mul_left _ _ two_ne_zero, neg_div]

lemma eps_form : Real.arccos ((√5 + 1) / √((10 - 2 * √5) * 3)) = wordEps := by
  unfold wordEps wordR; rw [mul_comm (10 - 2 * √5) 3]

/-- Two neighbouring triangles (one of each kind) meet at the angle α + β = π − ε. -/
lemma fuji_theta_apex {i j : Fin 7} (hii : ⟪fujiN i, fujiN i⟫ = 12)
    (hjj : ⟪fujiN j, fujiN j⟫ = 10 - 2 * √5) (hij : ⟪fujiN i, fujiN j⟫ = -(-(2 * √5 + 2))) :
    theta (cone fujiN ({i, j} : Set (Fin 7))) =
      (Submodule.Quotient.mk (wordAlpha + wordBeta) : Angle) := by
  rw [theta_pair_of_gram fujiN rfl (by norm_num) hii hjj hij apex_gram_ne, apex_form]

/-- The hexagon meets a triangle with sides 1, 1, 1 at the angle γ. -/
lemma fuji_theta_gamma {j : Fin 7} (hjj : ⟪fujiN j, fujiN j⟫ = 12)
    (hij : ⟪fujiN 6, fujiN j⟫ = -(2 * √5)) :
    theta (cone fujiN ({6, j} : Set (Fin 7))) = (Submodule.Quotient.mk wordGamma : Angle) := by
  rw [theta_pair_of_gram fujiN rfl (by norm_num) fujiN_sq.2.2.2.2.2.2 hjj hij gamma_gram_ne, gamma_form]

/-- The hexagon meets a triangle with sides 1, 1, (√5 − 1)/2 at the angle ε. -/
lemma fuji_theta_eps {i : Fin 7} (hii : ⟪fujiN i, fujiN i⟫ = 10 - 2 * √5)
    (hij : ⟪fujiN i, fujiN 6⟫ = -(√5 + 1)) :
    theta (cone fujiN ({i, 6} : Set (Fin 7))) = (Submodule.Quotient.mk wordEps : Angle) := by
  rw [theta_pair_of_gram fujiN rfl ten_sub_pos hii fujiN_sq.2.2.2.2.2.2 hij eps_gram_ne, eps_form]

/-- The lengths of the twelve edges … -/
noncomputable def fujiLen : Fin 12 → ℝ :=
  ![1, 1, 1, 1, 1, 1, 1, 1, 1, (√5 - 1) / 2, (√5 - 1) / 2, (√5 - 1) / 2]

/-- … and their interior angles. -/
noncomputable def fujiAng : Fin 12 → ℝ :=
  ![wordAlpha + wordBeta, wordAlpha + wordBeta, wordAlpha + wordBeta, wordAlpha + wordBeta,
    wordAlpha + wordBeta, wordAlpha + wordBeta, wordGamma, wordGamma, wordGamma, wordEps, wordEps, wordEps]

lemma fuji_term (e : Fin 12) :
    dist (fujiP (fujiVk e)) (fujiP (fujiVl e)) ⊗ₜ[ℚ] theta (cone fujiN ({fujiFi e, fujiFj e} : Set (Fin 7))) =
      edgeTerm (fujiLen e) (fujiAng e) := by
  obtain ⟨s0, s3, s5, s1, s2, s4, s6⟩ := fujiN_sq
  obtain ⟨g01, g02, g31, g52, g34, g54, g60, g63, g65, g16, g26, g46⟩ := fujiN_gram
  fin_cases e
  · exact congrArg₂ _ (fuji_dist_one 0 (by decide)) (fuji_theta_apex s0 s1 g01)
  · exact congrArg₂ _ (fuji_dist_one 1 (by decide)) (fuji_theta_apex s0 s2 g02)
  · exact congrArg₂ _ (fuji_dist_one 2 (by decide)) (fuji_theta_apex s3 s1 g31)
  · exact congrArg₂ _ (fuji_dist_one 3 (by decide)) (fuji_theta_apex s5 s2 g52)
  · exact congrArg₂ _ (fuji_dist_one 4 (by decide)) (fuji_theta_apex s3 s4 g34)
  · exact congrArg₂ _ (fuji_dist_one 5 (by decide)) (fuji_theta_apex s5 s4 g54)
  · exact congrArg₂ _ (fuji_dist_one 6 (by decide)) (fuji_theta_gamma s0 g60)
  · exact congrArg₂ _ (fuji_dist_one 7 (by decide)) (fuji_theta_gamma s3 g63)
  · exact congrArg₂ _ (fuji_dist_one 8 (by decide)) (fuji_theta_gamma s5 g65)
  · exact congrArg₂ _ (fuji_dist_gold 9 (by decide)) (fuji_theta_eps s1 g16)
  · exact congrArg₂ _ (fuji_dist_gold 10 (by decide)) (fuji_theta_eps s2 g26)
  · exact congrArg₂ _ (fuji_dist_gold 11 (by decide)) (fuji_theta_eps s4 g46)

/-- The edge list of FUJI (length, interior angle): six edges of length 1 at α + β, three of length 1 at γ,
three of length (√5 − 1)/2 at ε. -/
noncomputable def fujiEdges : List (ℝ × ℝ) := List.ofFn fun e : Fin 12 => (fujiLen e, fujiAng e)

/-- **The Dehn invariant of FUJI, as a set, is study 1's value of its edge list.** -/
theorem dehnSet_fuji : dehnSet fujiSet = dehn fujiEdges := by
  unfold fujiSet
  rw [fuji_isEdgeData.dehnSet_eq]
  unfold dehn fujiEdges
  rw [List.map_ofFn, List.sum_ofFn]
  exact Finset.sum_congr rfl (fun e _ => fuji_term e)

/-! ### The three words over the two angles α and β -/

lemma edgeTerm_angle_add (L θ₁ θ₂ : ℝ) : edgeTerm L (θ₁ + θ₂) = edgeTerm L θ₁ + edgeTerm L θ₂ := by
  unfold edgeTerm; rw [Submodule.Quotient.mk_add, TensorProduct.tmul_add]

lemma edgeTerm_pi (L : ℝ) : edgeTerm L π = 0 := by
  have h := edgeTerm_rat L 1
  rwa [Rat.cast_one, one_mul] at h

/-- Modulo π, γ = α + 2β. -/
lemma edgeTerm_gamma (L : ℝ) :
    edgeTerm L wordGamma = edgeTerm L wordAlpha + edgeTerm L wordBeta + edgeTerm L wordBeta := by
  have h : wordGamma + π = wordAlpha + wordBeta + wordBeta := by linarith [word_angle_relation]
  have h2 := edgeTerm_angle_add L wordGamma π
  rw [edgeTerm_pi, add_zero, h, edgeTerm_angle_add, edgeTerm_angle_add] at h2
  exact h2.symm

/-- Modulo π, ε = −α − β. -/
lemma edgeTerm_eps (L : ℝ) : edgeTerm L wordEps = -(edgeTerm L wordAlpha + edgeTerm L wordBeta) := by
  have h2 := edgeTerm_angle_add L (wordAlpha + wordBeta) wordEps
  rw [word_angle_sum, edgeTerm_pi, edgeTerm_angle_add] at h2
  exact eq_neg_of_add_eq_zero_right h2.symm

lemma edgeTerm_int (p q : ℤ) (L M θ : ℝ) :
    edgeTerm (p * L + q * M) θ = p • edgeTerm L θ + q • edgeTerm M θ := by
  unfold edgeTerm
  rw [TensorProduct.add_tmul, ← zsmul_eq_mul, ← zsmul_eq_mul, TensorProduct.smul_tmul',
    TensorProduct.smul_tmul']

lemma edgeTerm_int1 (p : ℤ) (L θ : ℝ) : edgeTerm (p * L) θ = p • edgeTerm L θ := by
  unfold edgeTerm
  rw [← zsmul_eq_mul, TensorProduct.smul_tmul']

/-- **CLEO over α, β**: 3 ⊗ α + 3g ⊗ β, g = (√5 − 1)/2. -/
theorem dehn_cleo_alpha_beta :
    dehn cleoEdges = edgeTerm 3 wordAlpha + edgeTerm (3 * ((√5 - 1) / 2)) wordBeta := by
  have h1 : edgeTerm 3 wordAlpha = (3 : ℤ) • edgeTerm 1 wordAlpha := by
    rw [← edgeTerm_int1]; congr 1; norm_num
  have h2 : edgeTerm (3 * ((√5 - 1) / 2)) wordBeta = (3 : ℤ) • edgeTerm ((√5 - 1) / 2) wordBeta := by
    rw [← edgeTerm_int1]; congr 1
  rw [h1, h2]
  simp only [dehn, cleoEdges, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
  abel

/-- **AXE over α, β**: (1 + g) ⊗ α + 6 ⊗ β. -/
theorem dehn_axe_alpha_beta :
    dehn axeEdges = edgeTerm (1 + (√5 - 1) / 2) wordAlpha + edgeTerm 6 wordBeta := by
  have h1 : edgeTerm 6 wordBeta = (6 : ℤ) • edgeTerm 1 wordBeta := by
    rw [← edgeTerm_int1]; congr 1; norm_num
  rw [h1, edgeTerm_add]
  simp only [dehn, axeEdges, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
  rw [edgeTerm_gamma]
  abel

/-- **FUJI over α, β**: (9 − 3g) ⊗ α + (12 − 3g) ⊗ β. -/
theorem dehn_fuji_alpha_beta :
    dehn fujiEdges =
      edgeTerm (9 - 3 * ((√5 - 1) / 2)) wordAlpha + edgeTerm (12 - 3 * ((√5 - 1) / 2)) wordBeta := by
  rw [show (9 : ℝ) - 3 * ((√5 - 1) / 2) = ((9 : ℤ) : ℝ) * 1 + ((-3 : ℤ) : ℝ) * ((√5 - 1) / 2) by
      push_cast; ring,
    show (12 : ℝ) - 3 * ((√5 - 1) / 2) = ((12 : ℤ) : ℝ) * 1 + ((-3 : ℤ) : ℝ) * ((√5 - 1) / 2) by
      push_cast; ring,
    edgeTerm_int, edgeTerm_int]
  unfold dehn fujiEdges
  rw [List.map_ofFn, List.sum_ofFn]
  simp only [Function.comp_apply, Fin.sum_univ_succ, Fin.sum_univ_zero, fujiLen, fujiAng,
    Matrix.cons_val_zero, Matrix.cons_val_succ, add_zero]
  simp only [edgeTerm_angle_add, edgeTerm_gamma, edgeTerm_eps]
  abel

/-! ### FUJI is a nonzero word -/

/-- 9 − 3g is not a rational multiple of 12 − 3g. -/
lemma fuji_lengths_indep :
    (9 - 3 * ((√5 - 1) / 2) : ℝ) ∉ Submodule.span ℚ {(12 - 3 * ((√5 - 1) / 2) : ℝ)} := by
  rw [Submodule.mem_span_singleton]
  rintro ⟨q, hq⟩
  rw [Rat.smul_def] at hq
  by_cases hq1 : (q : ℝ) = 1
  · rw [hq1] at hq; linarith
  · have hne : (q : ℝ) - 1 ≠ 0 := sub_ne_zero.2 hq1
    have h1 : (√5 - 1) * ((q : ℝ) - 1) = 8 * q - 6 := by linear_combination (-2 / 3 : ℝ) * hq
    have h2 := eq_div_of_mul_eq hne h1
    apply irrational_sqrt5
    refine ⟨1 + (8 * q - 6) / (q - 1), ?_⟩
    push_cast
    linarith

/-- **FUJI is a nonzero word**: its Dehn invariant is not zero. -/
theorem dehnSet_fuji_ne_zero : dehnSet fujiSet ≠ 0 := by
  rw [dehnSet_fuji, dehn_fuji_alpha_beta]
  exact tmul_add_tmul_ne_zero fuji_lengths_indep wordAlpha_class_ne_zero

/-- **No FUJI is scissors congruent to a cube**: any size, any position of both. -/
theorem fuji_not_scissorsCongruent_cube {C Q : Set R3} (hC : IsSimilarCopy fujiSet C)
    (hQ : IsSimilarCopy (cubeSet 1) Q) : ¬ ScissorsCongruent C Q :=
  not_scissorsCongruent_similarCopies isPoly_fuji (isPoly_cube 1) dehnSet_fuji_ne_zero
    (dehnSet_cube 1 one_pos) hC hQ

/-- No FUJI is scissors congruent to a cube ∩ rhombic dodecahedron solid (the fair 18-face die among them). -/
theorem fuji_not_scissorsCongruent_cubeRD (s c : ℝ) {C Q : Set R3} (hC : IsSimilarCopy fujiSet C)
    (hQ : IsSimilarCopy (cubeRDSet s c) Q) : ¬ ScissorsCongruent C Q :=
  not_scissorsCongruent_similarCopies isPoly_fuji (isPoly_cubeRD s c) dehnSet_fuji_ne_zero
    (dehnSet_cubeRD s c) hC hQ

end DehnCanon.Library
