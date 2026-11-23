/-
Lean study 7 of the shape-language canon (DICTO, 19 Nov 2026), part U: the zero words whose face normals make
rational angles.

* `cos_five_mul`, `mem_ratPi_of_cos_gold`: an angle whose cosine is (±1 ± √5)/4 is a multiple of 36°.
* `rtN`: the 30 two-fold directions of the icosahedral group, with coordinates in ℤ[√5]
  (± 4 e_i, and the cyclic permutations of (±(√5 − 1), ±(√5 + 1), ±2)); `rtN_angle`: any two of them make an
  angle that is a rational multiple of π (0°, 36°, 60°, 72°, 90°, … , 180°).
* `dehnSet_rtFamily`: **every solid cut out by planes perpendicular to two-fold directions of the icosahedral
  group has Dehn invariant zero**, whatever the choice of directions and offsets.
* `dehnSet_rt`: the rhombic triacontahedron (its 30 faces at one distance) is a zero word.
* `goldProlateSet_eq`, `goldOblateSet_eq`: the two golden rhombohedra, as six half-spaces from the 30 directions,
  are the parallelepipeds spanned by three five-fold axes (edge vectors of length √((5 + √5)/2)): pairwise at
  arccos(1/√5) for the prolate, and with one pair at π − arccos(1/√5) for the oblate.
  `dehnSet_goldProlate`, `dehnSet_goldOblate`: both are zero words.
* `dehnSet_crFamily`, `dehnSet_rd`: the same for the 18 directions of the cube ∩ rhombic dodecahedron line
  (study 4); the rhombic dodecahedron alone (its 12 faces) is a zero word.

Answer to the question of the brief ("the dihedral angles of the golden rhombohedra and of the rhombic
triacontahedron are not all in ℚπ"): they are. All face normals of these solids are two-fold directions, so all
their dihedral angles are multiples of 36° (72° and 108° for the prolate rhombohedron, 36° and 144° for the
oblate one, 144° for the triacontahedron). The cheapest Lean route is therefore study 4's
`dehnSet_sol_eq_zero_of_rational`, with a Gram table over ℤ[√5] checked by `decide`, and no edge list.

Credits: Mathlib `Real.cos_add`, `Real.cos_three_mul`, `Real.sin_three_mul`, `Real.cos_two_mul`,
`Real.sin_two_mul`, `InnerProductGeometry.cos_angle`, `norm_eq_sqrt_real_inner`; study 4's
`dehnSet_sol_eq_zero_of_rational`, `angle_mem_ratPi_of_gram`, `mem_ratPi_of_sin_nat_mul`, `crN_angle`;
study 5's `ind3`, `inner3'`.
No `sorry`.
-/
module

public import Packets.Canon.Dehn6Pairs

@[expose] public section

open scoped RealInnerProductSpace Real
open Set Module TensorProduct

namespace DehnCanon.Library

/-! ### Multiples of 36° -/

lemma cos_five_mul (x : ℝ) :
    Real.cos (5 * x) = 16 * Real.cos x ^ 5 - 20 * Real.cos x ^ 3 + 5 * Real.cos x := by
  have h := Real.sin_sq_add_cos_sq x
  rw [show 5 * x = 3 * x + 2 * x by ring, Real.cos_add, Real.cos_three_mul, Real.sin_three_mul,
    Real.cos_two_mul, Real.sin_two_mul]
  linear_combination (-2 * Real.cos x * (-4 * Real.sin x ^ 2 + 4 * Real.cos x ^ 2 - 1)) * h

/-- **An angle whose cosine c satisfies 4c² − 2sc − 1 = 0, s = ±1, is a rational multiple of π.** These are
c = (±1 ± √5)/4, the cosines of 36°, 72°, 108°, 144°; then cos 5θ = ±1. -/
lemma mem_ratPi_of_cos_gold {θ s : ℝ} (hs : s = 1 ∨ s = -1)
    (h : 4 * Real.cos θ ^ 2 - 2 * s * Real.cos θ - 1 = 0) : θ ∈ ratPi := by
  apply mem_ratPi_of_sin_nat_mul 5 (by norm_num)
  have h5 := cos_five_mul θ
  have hc : Real.cos (5 * θ) ^ 2 = 1 := by
    rcases hs with rfl | rfl
    · have e : Real.cos (5 * θ) = -1 := by
        rw [h5]
        linear_combination (Real.cos θ + 1) * (4 * Real.cos θ ^ 2 - 2 * Real.cos θ - 1) * h
      rw [e]; norm_num
    · have e : Real.cos (5 * θ) = 1 := by
        rw [h5]
        linear_combination (Real.cos θ - 1) * (4 * Real.cos θ ^ 2 + 2 * Real.cos θ - 1) * h
      rw [e]; norm_num
  have hs5 := Real.sin_sq_add_cos_sq (5 * θ)
  have h0 : Real.sin (5 * θ) ^ 2 = 0 := by linarith
  rw [show ((5 : ℕ) : ℝ) * θ = 5 * θ by push_cast; ring]
  exact pow_eq_zero_iff (two_ne_zero) |>.1 h0

section gram

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Two vectors of squared length 16 whose inner product is A + B√5 with A, B = ±4 make an angle that is a
rational multiple of π. -/
lemma angle_mem_ratPi_of_gram_gold {x y : E} (hx : ⟪x, x⟫ = 16) (hy : ⟪y, y⟫ = 16) {A B : ℤ}
    (hA : A = 4 ∨ A = -4) (hB : B = 4 ∨ B = -4) (h : ⟪x, y⟫ = A + B * √5) :
    InnerProductGeometry.angle x y ∈ ratPi := by
  have hnx : ‖x‖ = 4 := by
    rw [norm_eq_sqrt_real_inner, hx, show (16 : ℝ) = 4 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have hny : ‖y‖ = 4 := by
    rw [norm_eq_sqrt_real_inner, hy, show (16 : ℝ) = 4 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have hc : Real.cos (InnerProductGeometry.angle x y) = (A + B * √5) / 16 := by
    rw [InnerProductGeometry.cos_angle, h, hnx, hny]; norm_num
  have h5 := sqrt5_sq
  rcases hA with rfl | rfl
  · apply mem_ratPi_of_cos_gold (s := 1) (Or.inl rfl)
    rw [hc]
    rcases hB with rfl | rfl <;> push_cast <;> linear_combination (1 / 4 : ℝ) * h5
  · apply mem_ratPi_of_cos_gold (s := -1) (Or.inr rfl)
    rw [hc]
    rcases hB with rfl | rfl <;> push_cast <;> linear_combination (1 / 4 : ℝ) * h5

end gram

/-! ### The 30 two-fold directions of the icosahedral group -/

/-- A number a + b√5 with integers a, b. -/
noncomputable def q5 (z : ℤ × ℤ) : ℝ := z.1 + z.2 * √5

/-- Product in ℤ[√5]. -/
def mul5 (z w : ℤ × ℤ) : ℤ × ℤ := (z.1 * w.1 + 5 * z.2 * w.2, z.1 * w.2 + z.2 * w.1)

lemma q5_mul (z w : ℤ × ℤ) : q5 z * q5 w = q5 (mul5 z w) := by
  unfold q5 mul5; push_cast; linear_combination ((z.2 : ℝ) * w.2) * sqrt5_sq

lemma q5_add (z w : ℤ × ℤ) : q5 z + q5 w = q5 (z + w) := by
  unfold q5; rw [Prod.fst_add, Prod.snd_add]; push_cast; ring

/-- The 30 two-fold directions, coordinates as pairs (a, b) for a + b√5: first ± 4 e_i, then the cyclic
permutations of (±(√5 − 1), ±(√5 + 1), ±2). Each has squared length 16 (exact list: `checks/gold_check.out`). -/
def rtZ : Fin 30 → Fin 3 → ℤ × ℤ :=
  ![![(4, 0), (0, 0), (0, 0)], ![(-4, 0), (0, 0), (0, 0)], ![(0, 0), (4, 0), (0, 0)],
    ![(0, 0), (-4, 0), (0, 0)], ![(0, 0), (0, 0), (4, 0)], ![(0, 0), (0, 0), (-4, 0)],
    ![(-1, 1), (1, 1), (2, 0)], ![(-1, 1), (1, 1), (-2, 0)], ![(-1, 1), (-1, -1), (2, 0)],
    ![(-1, 1), (-1, -1), (-2, 0)], ![(1, -1), (1, 1), (2, 0)], ![(1, -1), (1, 1), (-2, 0)],
    ![(1, -1), (-1, -1), (2, 0)], ![(1, -1), (-1, -1), (-2, 0)], ![(2, 0), (-1, 1), (1, 1)],
    ![(2, 0), (-1, 1), (-1, -1)], ![(2, 0), (1, -1), (1, 1)], ![(2, 0), (1, -1), (-1, -1)],
    ![(-2, 0), (-1, 1), (1, 1)], ![(-2, 0), (-1, 1), (-1, -1)], ![(-2, 0), (1, -1), (1, 1)],
    ![(-2, 0), (1, -1), (-1, -1)], ![(1, 1), (2, 0), (-1, 1)], ![(1, 1), (2, 0), (1, -1)],
    ![(1, 1), (-2, 0), (-1, 1)], ![(1, 1), (-2, 0), (1, -1)], ![(-1, -1), (2, 0), (-1, 1)],
    ![(-1, -1), (2, 0), (1, -1)], ![(-1, -1), (-2, 0), (-1, 1)], ![(-1, -1), (-2, 0), (1, -1)]]

/-- The 30 directions as vectors of ℝ³. -/
noncomputable def rtN (i : Fin 30) : R3 := !₂[q5 (rtZ i 0), q5 (rtZ i 1), q5 (rtZ i 2)]

/-- Inner products in ℤ[√5]. -/
def rtDot (i j : Fin 30) : ℤ × ℤ :=
  mul5 (rtZ i 0) (rtZ j 0) + mul5 (rtZ i 1) (rtZ j 1) + mul5 (rtZ i 2) (rtZ j 2)

lemma rtN_inner (i j : Fin 30) : ⟪rtN i, rtN j⟫ = q5 (rtDot i j) := by
  unfold rtDot
  rw [← q5_add, ← q5_add, ← q5_mul, ← q5_mul, ← q5_mul]
  unfold rtN
  rw [inner3]
  rfl

lemma rtN_inner_x (i : Fin 30) (x : R3) :
    ⟪rtN i, x⟫ = q5 (rtZ i 0) * x 0 + q5 (rtZ i 1) * x 1 + q5 (rtZ i 2) * x 2 := by
  unfold rtN; rw [inner3]

/-- The allowed inner products: 0, ±8, ±16 (90°, 60° or 120°, 0° or 180°) and ±4 ± 4√5
(36°, 72°, 108°, 144°). -/
def goodDot (z : ℤ × ℤ) : Bool :=
  (z.2 == 0 && (z.1 == 0 || z.1 == 8 || z.1 == -8 || z.1 == 16 || z.1 == -16)) ||
    ((z.1 == 4 || z.1 == -4) && (z.2 == 4 || z.2 == -4))

lemma rtDot_table : ∀ i j : Fin 30, goodDot (rtDot i j) = true := by decide +kernel

lemma rtDot_self : ∀ i : Fin 30, rtDot i i = (16, 0) := by decide +kernel

lemma rtN_sq (i : Fin 30) : ⟪rtN i, rtN i⟫ = 16 := by
  rw [rtN_inner, rtDot_self]; unfold q5; norm_num

lemma rtN_ne_zero (i : Fin 30) : rtN i ≠ 0 := by
  intro h
  have h1 := rtN_sq i
  rw [h, inner_zero_left] at h1
  norm_num at h1

/-- **Any two of the 30 two-fold directions make an angle that is a rational multiple of π.** -/
theorem rtN_angle (i j : Fin 30) : InnerProductGeometry.angle (rtN i) (rtN j) ∈ ratPi := by
  have ht := rtDot_table i j
  have hin := rtN_inner i j
  generalize rtDot i j = z at ht hin
  obtain ⟨A, B⟩ := z
  unfold q5 at hin
  simp only [goodDot, Bool.or_eq_true, Bool.and_eq_true, beq_iff_eq] at ht
  rcases ht with ⟨rfl, hA⟩ | ⟨hA, hB⟩
  · have key : ∃ k : ℕ, k ≤ 4 ∧ 4 * (A : ℝ) ^ 2 = k * (16 * 16) := by
      rcases hA with (((rfl | rfl) | rfl) | rfl) | rfl
      · exact ⟨0, by norm_num, by norm_num⟩
      · exact ⟨1, by norm_num, by norm_num⟩
      · exact ⟨1, by norm_num, by norm_num⟩
      · exact ⟨4, by norm_num, by norm_num⟩
      · exact ⟨4, by norm_num, by norm_num⟩
    obtain ⟨k, hk, hk'⟩ := key
    apply angle_mem_ratPi_of_gram (rtN_ne_zero i) (rtN_ne_zero j) hk
    rw [hin, rtN_sq, rtN_sq]
    push_cast at hk' ⊢
    linarith
  · exact angle_mem_ratPi_of_gram_gold (rtN_sq i) (rtN_sq j) hA hB (by rw [hin])

/-- **Two-fold directions, zero invariant.** Every solid cut out by half-spaces whose normals are two-fold
directions of the icosahedral group has Dehn invariant zero, for every choice of the directions `f` and of the
offsets `b`. -/
theorem dehnSet_rtFamily {ι : Type} [Finite ι] (f : ι → Fin 30) (b : ι → ℝ) :
    dehnSet (sol (fun i => rtN (f i)) b) = 0 :=
  dehnSet_sol_eq_zero_of_rational _ b (fun i => rtN_ne_zero (f i)) (fun i j => rtN_angle (f i) (f j))

/-! ### The rhombic triacontahedron -/

/-- **The rhombic triacontahedron**: its 30 faces are perpendicular to the 30 two-fold directions, all at one
distance `r / 4` from the centre. -/
def rtSet (r : ℝ) : Set R3 := sol rtN (fun _ => r)

theorem isPoly_rt (r : ℝ) : IsPoly (rtSet r) := by
  refine ⟨bounded_of_coords (r / 4) (fun x hx i => ?_), Fin 30, inferInstance, rtN, _, rfl⟩
  have e : ∀ m : Fin 30, ⟪rtN m, x⟫ ≤ r := fun m => hx m
  have h0 := e 0; have h1 := e 1; have h2 := e 2; have h3 := e 3; have h4 := e 4; have h5 := e 5
  simp only [rtN_inner_x, rtZ, q5] at h0 h1 h2 h3 h4 h5
  norm_num at h0 h1 h2 h3 h4 h5
  fin_cases i <;> simp only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk] <;> rw [abs_le] <;>
    constructor <;> linarith

/-- **The rhombic triacontahedron is a zero word.** -/
theorem dehnSet_rt (r : ℝ) : dehnSet (rtSet r) = 0 := dehnSet_rtFamily id _

/-! ### A parallelepiped as six half-spaces -/

section para

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- With normals `n₁, n₂, n₃` dual to the edge vectors `u, v, w` (`⟪nᵢ, ·⟫` is `dᵢ > 0` on one edge vector and
zero on the other two) and no common perpendicular direction, the six inequalities `0 ≤ ⟪nᵢ, x⟫ ≤ dᵢ` cut out
exactly the parallelepiped `{a u + b v + c w : a, b, c ∈ [0, 1]}`. -/
lemma mem_parallelepiped_iff {u v w n1 n2 n3 : E} {d1 d2 d3 : ℝ} (hd1 : 0 < d1) (hd2 : 0 < d2)
    (hd3 : 0 < d3) (h1u : ⟪n1, u⟫ = d1) (h1v : ⟪n1, v⟫ = 0) (h1w : ⟪n1, w⟫ = 0)
    (h2u : ⟪n2, u⟫ = 0) (h2v : ⟪n2, v⟫ = d2) (h2w : ⟪n2, w⟫ = 0)
    (h3u : ⟪n3, u⟫ = 0) (h3v : ⟪n3, v⟫ = 0) (h3w : ⟪n3, w⟫ = d3)
    (hind : ∀ y : E, ⟪n1, y⟫ = 0 → ⟪n2, y⟫ = 0 → ⟪n3, y⟫ = 0 → y = 0) (x : E) :
    (0 ≤ ⟪n1, x⟫ ∧ ⟪n1, x⟫ ≤ d1 ∧ 0 ≤ ⟪n2, x⟫ ∧ ⟪n2, x⟫ ≤ d2 ∧ 0 ≤ ⟪n3, x⟫ ∧ ⟪n3, x⟫ ≤ d3) ↔
      ∃ a b c : ℝ, a ∈ Icc (0 : ℝ) 1 ∧ b ∈ Icc (0 : ℝ) 1 ∧ c ∈ Icc (0 : ℝ) 1 ∧
        x = a • u + b • v + c • w := by
  have ev : ∀ (n : E) (a b c : ℝ), ⟪n, a • u + b • v + c • w⟫ = a * ⟪n, u⟫ + b * ⟪n, v⟫ + c * ⟪n, w⟫ :=
    fun n a b c => by rw [inner_add_right, inner_add_right, inner_smul_right, inner_smul_right,
      inner_smul_right]
  constructor
  · rintro ⟨a0, a1, b0, b1, c0, c1⟩
    refine ⟨⟪n1, x⟫ / d1, ⟪n2, x⟫ / d2, ⟪n3, x⟫ / d3, ⟨div_nonneg a0 hd1.le, (div_le_one hd1).2 a1⟩,
      ⟨div_nonneg b0 hd2.le, (div_le_one hd2).2 b1⟩, ⟨div_nonneg c0 hd3.le, (div_le_one hd3).2 c1⟩, ?_⟩
    rw [← sub_eq_zero]
    apply hind <;> rw [inner_sub_right, ev] <;> field_simp <;>
      simp only [h1u, h1v, h1w, h2u, h2v, h2w, h3u, h3v, h3w] <;> field_simp <;> ring
  · rintro ⟨a, b, c, ⟨a0, a1⟩, ⟨b0, b1⟩, ⟨c0, c1⟩, rfl⟩
    rw [ev, ev, ev, h1u, h1v, h1w, h2u, h2v, h2w, h3u, h3v, h3w]
    refine ⟨by nlinarith, by nlinarith, by nlinarith, by nlinarith, by nlinarith, by nlinarith⟩

end para

lemma inner_neg_eq {x y v : R3} (h : x = -y) : ⟪x, v⟫ = -⟪y, v⟫ := by rw [h, inner_neg_left]

/-- `φ = (1 + √5)/2`. -/
noncomputable abbrev phi : ℝ := (1 + √5) / 2

/-! ### The prolate golden rhombohedron -/

/-- Edge vectors of the prolate golden rhombohedron: three five-fold axes (icosahedron corners) pairwise at
arccos(1/√5) = 63.43…°. -/
noncomputable def gpU : R3 := !₂[0, 1, phi]
noncomputable def gpV : R3 := !₂[0, -1, phi]
noncomputable def gpW : R3 := !₂[phi, 0, 1]

/-- Its six faces: two-fold directions 10, 9 (= −10), 12, 7 (= −12), 0, 1 (= −0). -/
def gpF : Fin 6 → Fin 30 := ![10, 9, 12, 7, 0, 1]

noncomputable def gpB : Fin 6 → ℝ := ![2 + 2 * √5, 0, 2 + 2 * √5, 0, 2 + 2 * √5, 0]

/-- **The prolate golden rhombohedron**, as six half-spaces. -/
def goldProlateSet : Set R3 := sol (fun i => rtN (gpF i)) gpB

macro "q5_simp" : tactic =>
  `(tactic| ((simp only [rtN_inner_x, rtZ, q5, gpU, gpV, gpW, phi]) <;> (try simp) <;> grind))

lemma gp_neg : rtN 9 = -rtN 10 ∧ rtN 7 = -rtN 12 ∧ rtN 1 = -rtN 0 := by
  refine ⟨?_, ?_, ?_⟩ <;> ext k <;> fin_cases k <;> simp [rtN, rtZ, q5] <;> ring

/-- **The prolate golden rhombohedron is the parallelepiped on its three edge vectors.** -/
theorem goldProlateSet_eq : goldProlateSet = {x | ∃ a b c : ℝ, a ∈ Icc (0 : ℝ) 1 ∧ b ∈ Icc (0 : ℝ) 1 ∧
    c ∈ Icc (0 : ℝ) 1 ∧ x = a • gpU + b • gpV + c • gpW} := by
  have ht := sqrt5_sq
  have hd : (0 : ℝ) < 2 + 2 * √5 := by positivity
  obtain ⟨n9, n7, n1⟩ := gp_neg
  ext x
  rw [Set.mem_ofPred_eq, ← mem_parallelepiped_iff (n1 := rtN 10) (n2 := rtN 12) (n3 := rtN 0) hd hd hd
    (by q5_simp) (by q5_simp) (by q5_simp) (by q5_simp) (by q5_simp) (by q5_simp) (by q5_simp)
    (by q5_simp) (by q5_simp)
    (fun y h1 h2 h3 => ind3 (x := rtN 10) (y := rtN 12) (z := rtN 0) (D := 16 + 16 * √5)
      (by simp [rtN, rtZ, q5]; grind) (by positivity) y h1 h2 h3)]
  constructor
  · intro hx
    have e := fun i => (hx i : ⟪rtN (gpF i), x⟫ ≤ gpB i)
    have e0 := e 0; have e1 := e 1; have e2 := e 2; have e3 := e 3; have e4 := e 4; have e5 := e 5
    simp only [gpF, gpB, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val] at e0 e1 e2 e3 e4 e5
    rw [inner_neg_eq n9] at e1; rw [inner_neg_eq n7] at e3; rw [inner_neg_eq n1] at e5
    exact ⟨by linarith, e0, by linarith, e2, by linarith, e4⟩
  · rintro ⟨a0, a1, b0, b1, c0, c1⟩ i
    show ⟪rtN (gpF i), x⟫ ≤ gpB i
    fin_cases i <;> simp only [gpF, gpB, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val,
      Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk]
    · exact a1
    · rw [inner_neg_eq n9]; linarith
    · exact b1
    · rw [inner_neg_eq n7]; linarith
    · exact c1
    · rw [inner_neg_eq n1]; linarith

/-- **The prolate golden rhombohedron is a zero word.** -/
theorem dehnSet_goldProlate : dehnSet goldProlateSet = 0 := dehnSet_rtFamily gpF gpB

/-! ### The oblate golden rhombohedron -/

/-- Edge vectors of the oblate golden rhombohedron: three five-fold axes, two pairs at arccos(1/√5) and one
pair at π − arccos(1/√5) (the product of the three inner products is negative). -/
noncomputable def goU : R3 := !₂[0, 1, phi]
noncomputable def goV : R3 := !₂[0, -1, phi]
noncomputable def goW : R3 := !₂[1, phi, 0]

/-- Its six faces: two-fold directions 26, 25 (= −26), 24, 27 (= −24), 0, 1 (= −0). -/
def goF : Fin 6 → Fin 30 := ![26, 25, 24, 27, 0, 1]

noncomputable def goB : Fin 6 → ℝ := ![4, 0, 4, 0, 4, 0]

/-- **The oblate golden rhombohedron**, as six half-spaces. -/
def goldOblateSet : Set R3 := sol (fun i => rtN (goF i)) goB

macro "q5_simp'" : tactic =>
  `(tactic| ((simp only [rtN_inner_x, rtZ, q5, goU, goV, goW, phi]) <;> (try simp) <;> grind))

lemma go_neg : rtN 25 = -rtN 26 ∧ rtN 27 = -rtN 24 ∧ rtN 1 = -rtN 0 := by
  refine ⟨?_, ?_, ?_⟩ <;> ext k <;> fin_cases k <;> simp [rtN, rtZ, q5] <;> ring

/-- **The oblate golden rhombohedron is the parallelepiped on its three edge vectors.** -/
theorem goldOblateSet_eq : goldOblateSet = {x | ∃ a b c : ℝ, a ∈ Icc (0 : ℝ) 1 ∧ b ∈ Icc (0 : ℝ) 1 ∧
    c ∈ Icc (0 : ℝ) 1 ∧ x = a • goU + b • goV + c • goW} := by
  have ht := sqrt5_sq
  have h1 := one_lt_sqrt5
  have hd : (0 : ℝ) < 4 := by norm_num
  obtain ⟨n25, n27, n1⟩ := go_neg
  ext x
  rw [Set.mem_ofPred_eq, ← mem_parallelepiped_iff (n1 := rtN 26) (n2 := rtN 24) (n3 := rtN 0) hd hd hd
    (by q5_simp') (by q5_simp') (by q5_simp') (by q5_simp') (by q5_simp') (by q5_simp') (by q5_simp')
    (by q5_simp') (by q5_simp')
    (fun y h1 h2 h3 => ind3 (x := rtN 26) (y := rtN 24) (z := rtN 0) (D := -16 + 16 * √5)
      (by simp [rtN, rtZ, q5]; grind) (by intro h; linarith) y h1 h2 h3)]
  constructor
  · intro hx
    have e := fun i => (hx i : ⟪rtN (goF i), x⟫ ≤ goB i)
    have e0 := e 0; have e1 := e 1; have e2 := e 2; have e3 := e 3; have e4 := e 4; have e5 := e 5
    simp only [goF, goB, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val] at e0 e1 e2 e3 e4 e5
    rw [inner_neg_eq n25] at e1; rw [inner_neg_eq n27] at e3; rw [inner_neg_eq n1] at e5
    exact ⟨by linarith, e0, by linarith, e2, by linarith, e4⟩
  · rintro ⟨a0, a1, b0, b1, c0, c1⟩ i
    show ⟪rtN (goF i), x⟫ ≤ goB i
    fin_cases i <;> simp only [goF, goB, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val,
      Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk]
    · exact a1
    · rw [inner_neg_eq n25]; linarith
    · exact b1
    · rw [inner_neg_eq n27]; linarith
    · exact c1
    · rw [inner_neg_eq n1]; linarith

/-- **The oblate golden rhombohedron is a zero word.** -/
theorem dehnSet_goldOblate : dehnSet goldOblateSet = 0 := dehnSet_rtFamily goF goB

/-- The three edge vectors of each rhombohedron have one length, √((5 + √5)/2), and are five-fold axes:
the prolate ones pairwise at arccos(1/√5) (inner product φ = (1 + √5)/2 = (squared length)/√5), the oblate ones
with inner products φ, −φ, φ. -/
theorem gold_edge_vectors :
    ⟪gpU, gpU⟫ = (5 + √5) / 2 ∧ ⟪gpV, gpV⟫ = (5 + √5) / 2 ∧ ⟪gpW, gpW⟫ = (5 + √5) / 2 ∧
    ⟪gpU, gpV⟫ = phi ∧ ⟪gpV, gpW⟫ = phi ∧ ⟪gpW, gpU⟫ = phi ∧
    ⟪goW, goW⟫ = (5 + √5) / 2 ∧ ⟪goU, goV⟫ = phi ∧ ⟪goV, goW⟫ = -phi ∧ ⟪goW, goU⟫ = phi := by
  have ht := sqrt5_sq
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    simp only [gpU, gpV, gpW, goU, goV, goW, phi, inner3] <;> simp <;> grind

/-! ### The cube ∩ rhombic dodecahedron directions, and the rhombic dodecahedron -/

/-- Every solid cut out by half-spaces whose normals are among the 18 directions of study 4 (± e_i, ± e_i ± e_j)
has Dehn invariant zero. -/
theorem dehnSet_crFamily {ι : Type} [Finite ι] (f : ι → Fin 18) (b : ι → ℝ) :
    dehnSet (sol (fun i => crN (f i)) b) = 0 :=
  dehnSet_sol_eq_zero_of_rational _ b (fun i => crN_ne_zero (f i)) (fun i j => crN_angle (f i) (f j))

/-- **The rhombic dodecahedron** `|x i ± x j| ≤ c`: its 12 faces, the directions ± e_i ± e_j. -/
def rdSet (c : ℝ) : Set R3 := sol (fun i : Fin 12 => crN (Fin.natAdd 6 i)) (fun _ => c)

/-- **The rhombic dodecahedron is a zero word** (the cube is study 3's `dehnSet_cube`). -/
theorem dehnSet_rd (c : ℝ) : dehnSet (rdSet c) = 0 := dehnSet_crFamily _ _

end DehnCanon.Library
