/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Part 7: lead 1 with no hypothesis.

* `pyrDSet`: the dodecahedron centre pyramid (apex at the centre of the dodecahedron with corners (±2, ±2, ±2)
  and the cyclic permutations of (0, ±(1 + √5), ±(√5 − 1)); base the face with outward normal (0, 2, 1 + √5));
  `tiSet`: the truncated icosahedron with corners the cyclic permutations of (0, ±2, ±3(1 + √5)),
  (±2, ±(5 + √5), ±2(1 + √5)), (±(1 + √5), ±4, ±(4 + 2√5)) (edge 4). Both are given by their face inequalities
  (files GenPyrD, GenTI, generated with exact arithmetic in ℚ(√5) and checked by Lean).
* `pyrD_edgeAngle`, `ti_edgeAngle`: **Table 1, read from the sets**: the dihedral angles of the pyramid are
  exactly `α` and `2π/3`; those of the truncated icosahedron exactly `3π/2 − 2β` and `3π/4 − α + β`.
* `theorem4a_copies`: **Theorem 4 (a) for the pair, with rational helpers, no hypothesis.** In a tiling of space
  by convex polytopes each of which is a similar copy (rigid motion, reflection, positive scaling) of the
  dodecahedron centre pyramid or of the truncated icosahedron, or has only nonnegative rational multiples of π
  as dihedral angles, no tile is a copy of the pyramid or of the truncated icosahedron.
No `sorry`.
-/
module

public import Packets.Pieces
public import Packets.GenPyrD
public import Packets.GenTI

@[expose] public section

open Set Module
open scoped RealInnerProductSpace

namespace Packets

open DehnCanon.Library (sol R3 sqrt5_sq)
open PacketsGen

/-! ### Ranges of α and β -/

lemma α_nonneg : 0 ≤ α := Real.arctan_nonneg.2 (by positivity)

lemma α_le : α ≤ Real.pi / 2 := (Real.arctan_lt_pi_div_two _).le

lemma α_ge : Real.pi / 4 ≤ α := by
  rw [← Real.arctan_one]
  exact Real.arctan_strictMono.monotone (by
    have := Real.one_lt_sqrt_two; have h5 : (1 : ℝ) ≤ √5 := Real.one_le_sqrt.2 (by norm_num); linarith)

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

/-! ### The pyramid -/

def pyrDSet : Set R3 := sol pyrDN pyrDB

lemma fin2_cases : ∀ k : Fin 2, k = 0 ∨ k = 1 := by decide

lemma pyrD_ind (e : Fin 10) : LinearIndependent ℝ ![pyrDN (pyrDFi e), pyrDN (pyrDFj e)] := by
  obtain ⟨hg, hX, hY⟩ := pyrD_gram e
  apply linIndep_of_gram
  rw [hg, hX, hY]
  have h5 := sqrt5_sq
  rcases fin2_cases (pyrDKd e) with hk | hk <;> rw [hk] <;> simp [pyrDGg, pyrDGX, pyrDGY] <;>
    nlinarith [Real.sqrt_nonneg 5]

lemma pyrD_val (e : Fin 10) :
    Real.pi - InnerProductGeometry.angle (pyrDN (pyrDFi e)) (pyrDN (pyrDFj e)) =
      if pyrDKd e = 0 then α else 2 * Real.pi / 3 := by
  obtain ⟨hg, hX, hY⟩ := pyrD_gram e
  have h5 := sqrt5_sq
  have hpi := Real.pi_pos
  rcases fin2_cases (pyrDKd e) with hk | hk <;> rw [hk] at hg hX hY ⊢ <;>
    simp only [pyrDGg, pyrDGX, pyrDGY, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons] at hg hX hY <;>
    simp only [if_pos, if_neg, Fin.zero_eta, show (1 : Fin 2) ≠ 0 by decide, if_false, if_true]
  · refine pi_sub_angle_eq hg hX hY α_nonneg (by linarith [α_le]) ?_
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
  · refine pi_sub_angle_eq hg hX hY (by positivity) (by linarith) ?_
    have h64 : √(64 : ℝ) = 8 := by
      rw [show (64 : ℝ) = 8 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
    rw [show 2 * Real.pi / 3 = Real.pi - Real.pi / 3 by ring, Real.cos_pi_sub, Real.cos_pi_div_three, h64]
    norm_num

/-- **The dihedral angles of the dodecahedron centre pyramid, read from the set: exactly `α` and `2π/3`.** -/
theorem pyrD_edgeAngle (θ : ℝ) : EdgeAngle pyrDSet θ ↔ θ ∈ pyrD := by
  rw [pyrDSet, edgeAngle_edgeData pyrD_isEdgeData pyrD_interior pyrD_ind, pyrD_eq]
  constructor
  · rintro ⟨e, rfl⟩
    rw [pyrD_val]
    split_ifs <;> simp
  · intro h
    simp only [List.mem_cons, List.not_mem_nil, or_false] at h
    rcases h with rfl | rfl
    · exact ⟨0, by rw [pyrD_val]; rfl⟩
    · exact ⟨5, by rw [pyrD_val]; rfl⟩

/-! ### The truncated icosahedron -/

def tiSet : Set R3 := sol tiN tiB

lemma ti_ind (e : Fin 90) : LinearIndependent ℝ ![tiN (tiFi e), tiN (tiFj e)] := by
  obtain ⟨hg, hX, hY⟩ := ti_gram e
  apply linIndep_of_gram
  rw [hg, hX, hY]
  have h5 := sqrt5_sq
  rcases fin2_cases (tiKd e) with hk | hk <;> rw [hk] <;> simp [tiGg, tiGX, tiGY] <;>
    nlinarith [Real.sqrt_nonneg 5]

lemma ti_val (e : Fin 90) :
    Real.pi - InnerProductGeometry.angle (tiN (tiFi e)) (tiN (tiFj e)) =
      if tiKd e = 0 then 3 * Real.pi / 4 - α + β else 3 * Real.pi / 2 - 2 * β := by
  obtain ⟨hg, hX, hY⟩ := ti_gram e
  have h5 := sqrt5_sq
  have hpi := Real.pi_pos
  have ha1 := α_nonneg; have ha2 := α_le; have ha3 := α_ge
  have hb1 := β_le; have hb2 := β_ge
  rcases fin2_cases (tiKd e) with hk | hk <;> rw [hk] at hg hX hY ⊢ <;>
    simp only [tiGg, tiGX, tiGY, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons] at hg hX hY <;>
    simp only [if_pos, if_neg, Fin.zero_eta, show (1 : Fin 2) ≠ 0 by decide, if_false, if_true]
  · refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
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
  · refine pi_sub_angle_eq hg hX hY (by linarith) (by linarith) ?_
    rw [show 3 * Real.pi / 2 - 2 * β = (Real.pi / 2 - 2 * β) + Real.pi by ring, Real.cos_add_pi,
      Real.cos_pi_div_two_sub, sin_two_β, Real.mul_self_sqrt (by norm_num)]
    ring

/-- **The dihedral angles of the truncated icosahedron, read from the set: exactly `3π/2 − 2β` and
`3π/4 − α + β`.** -/
theorem ti_edgeAngle (θ : ℝ) : EdgeAngle tiSet θ ↔ θ ∈ ti := by
  rw [tiSet, edgeAngle_edgeData ti_isEdgeData ti_interior ti_ind, ti_eq]
  constructor
  · rintro ⟨e, rfl⟩
    rw [ti_val]
    split_ifs <;> simp
  · intro h
    simp only [List.mem_cons, List.not_mem_nil, or_false] at h
    rcases h with rfl | rfl
    · exact ⟨60, by rw [ti_val]; rfl⟩
    · exact ⟨0, by rw [ti_val]; rfl⟩

/-! ### Theorem 4 (a) for copies -/

/-- **Theorem 4 (a), lead 1, with no hypothesis**: copies of the dodecahedron centre pyramid and of the truncated
icosahedron, with any convex helpers whose dihedral angles are nonnegative rational multiples of π. -/
theorem theorem4a_copies {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) pyrDSet ∨ SimilarCopy (T.P i) tiSet ∨
      ∀ θ, EdgeAngle (T.P i) θ → ∃ q : ℚ, 0 ≤ q ∧ θ = q * Real.pi) (i : ι) :
    ¬ SimilarCopy (T.P i) pyrDSet ∧ ¬ SimilarCopy (T.P i) tiSet := by
  classical
  let ang : ι → List ℝ := fun j =>
    if SimilarCopy (T.P j) pyrDSet then pyrD else if SimilarCopy (T.P j) tiSet then ti else []
  have hang : ∀ j, ∀ θ ∈ ang j, EdgeAngle (T.P j) θ := by
    intro j θ hθ
    by_cases h1 : SimilarCopy (T.P j) pyrDSet
    · simp only [ang, if_pos h1] at hθ
      exact (h1.edgeAngle_iff θ).2 ((pyrD_edgeAngle θ).2 hθ)
    · by_cases h2 : SimilarCopy (T.P j) tiSet
      · simp only [ang, if_neg h1, if_pos h2] at hθ
        exact (h2.edgeAngle_iff θ).2 ((ti_edgeAngle θ).2 hθ)
      · simp [ang, h1, h2] at hθ
  have hk' : ∀ j, AllowedA (ang j) (EdgeAngle (T.P j)) := by
    intro j
    by_cases h1 : SimilarCopy (T.P j) pyrDSet
    · left
      refine ⟨Or.inl (by simp only [ang, if_pos h1]), fun θ hθ => ?_⟩
      simp only [ang, if_pos h1]
      exact (pyrD_edgeAngle θ).1 ((h1.edgeAngle_iff θ).1 hθ)
    · by_cases h2 : SimilarCopy (T.P j) tiSet
      · left
        refine ⟨Or.inr (Or.inl (by simp only [ang, if_neg h1, if_pos h2])), fun θ hθ => ?_⟩
        simp only [ang, if_neg h1, if_pos h2]
        exact (ti_edgeAngle θ).1 ((h2.edgeAngle_iff θ).1 hθ)
      · right
        rcases hk j with h | h | h
        · exact absurd h h1
        · exact absurd h h2
        · exact h
  obtain ⟨n1, n2, -⟩ := theorem4a_tiling T ang hang hk' i
  refine ⟨fun h => n1 (by simp only [ang, if_pos h]), fun h => ?_⟩
  by_cases h1 : SimilarCopy (T.P i) pyrDSet
  · exact n1 (by simp only [ang, if_pos h1])
  · exact n2 (by simp only [ang, if_neg h1, if_pos h])

end Packets
