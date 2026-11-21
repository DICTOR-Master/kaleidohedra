/-
Lean formalization of DICTO's paper #117, "From Dehn Packets to Scutoids: How the Fullerene Star Fills Space"
(Zenodo 10.5281/zenodo.24411660). Part 1: the four angles and Lemma 3.

* `α = arctan φ`, `β = arccos (1/√6)`, `γ = arccos √(2/3)`, with exact cosines and sines of `2α, 4α, 2β, 2γ`.
* `lemma3`: **π, α, β, γ are linearly independent over ℚ.**

Method (two quadratic fields, as in study 8 of the Dehn Canon): cos 4α = −3/5 and sin 4α = −4/5 are rational;
cos 2β = −2/3 is rational and sin 2β = √5/3; cos 2γ = 1/3 is rational and sin 2γ = 2√2/3. So for every integer n
the cosines of n·4α, n·2β, n·2γ are rational and their sines lie in ℚ, ℚ√5, ℚ√2. A relation
P·4α + Q·2β + R·2γ = m·2π gives sin(R·2γ) = −sin(P·4α + Q·2β) ∈ ℚ(√5); as √2 ∉ ℚ(√5), sin(R·2γ) = 0. Then
sin(P·4α) = −sin(Q·2β) is rational and a rational multiple of √5, so both vanish. Each angle 4α, 2β, 2γ has a
rational cosine outside {0, ±1/2, ±1}, so it is not a rational multiple of π (Niven), and P = Q = R = 0.

Credits: Niven's theorem `niven` (Mathlib, `NumberTheory/Niven.lean`); the field argument and the lemmas
`irrational_sqrt10`, `eq_zero_of_mul_sqrt2_inQ5` are taken from study 8 (`Dehn8Indep`) of DICTO's Dehn Canon
(Palomar entry palomar-dehn), whose independence of arccos(1/3) from two Q(√5) angles is the model here.
No `sorry`.
-/
module

public import Mathlib

@[expose] public section

open Real

namespace Packets

lemma sqrt5_sq : (√5 : ℝ) ^ 2 = 5 := Real.sq_sqrt (by norm_num)

lemma sqrt2_sq : (√2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)

lemma irrational_sqrt5 : Irrational (√5 : ℝ) := by
  simpa using Nat.Prime.irrational_sqrt (show Nat.Prime 5 by norm_num)

/-! ### The angles -/

/-- `α = arctan φ` (58.28°), half the dihedral angle of the regular dodecahedron. -/
noncomputable def α : ℝ := Real.arctan ((1 + √5) / 2)

/-- `β = arccos (1/√6)` (65.91°); `3π/4 − β` is half the dihedral angle of the regular icosahedron. -/
noncomputable def β : ℝ := Real.arccos (1 / √6)

/-- `γ = arccos √(2/3)` (35.26°); `2γ = arccos (1/3)` is the dihedral angle of the regular tetrahedron. -/
noncomputable def γ : ℝ := Real.arccos (√(2 / 3))

lemma gold_t_inv : (1 + ((1 + √5) / 2) ^ 2)⁻¹ = (5 - √5) / 10 := by
  have h5 := sqrt5_sq
  have ht : (1 + ((1 + √5) / 2) ^ 2) = (5 + √5) / 2 := by linear_combination (1 / 4) * h5
  rw [ht]; apply inv_eq_of_mul_eq_one_right; linear_combination (-1 / 20) * h5

lemma cos_two_α : Real.cos (2 * α) = -√5 / 5 := by
  rw [Real.cos_two_mul, α, Real.cos_arctan, div_pow, one_pow, Real.sq_sqrt (by positivity), one_div,
    gold_t_inv]
  ring

lemma sin_two_α : Real.sin (2 * α) = 2 * √5 / 5 := by
  have hpos : (0 : ℝ) ≤ 1 + ((1 + √5) / 2) ^ 2 := by positivity
  rw [Real.sin_two_mul, α, Real.sin_arctan, Real.cos_arctan]
  have hs := Real.mul_self_sqrt hpos
  calc 2 * ((1 + √5) / 2 / √(1 + ((1 + √5) / 2) ^ 2)) * (1 / √(1 + ((1 + √5) / 2) ^ 2))
      = (1 + √5) * (√(1 + ((1 + √5) / 2) ^ 2) * √(1 + ((1 + √5) / 2) ^ 2))⁻¹ := by ring
    _ = 2 * √5 / 5 := by rw [hs, gold_t_inv]; linear_combination (-1 / 10) * sqrt5_sq

lemma cos_four_α : Real.cos (4 * α) = -3 / 5 := by
  rw [show 4 * α = 2 * (2 * α) by ring, Real.cos_two_mul, cos_two_α]
  linear_combination (2 / 25) * sqrt5_sq

lemma sin_four_α : Real.sin (4 * α) = -4 / 5 := by
  rw [show 4 * α = 2 * (2 * α) by ring, Real.sin_two_mul, cos_two_α, sin_two_α]
  linear_combination (-4 / 25) * sqrt5_sq

lemma one_lt_sqrt6 : (1 : ℝ) < √6 := (Real.lt_sqrt (by norm_num)).2 (by norm_num)

lemma cos_β : Real.cos β = 1 / √6 := by
  have h := one_lt_sqrt6
  have h0 : 0 ≤ 1 / √6 := by positivity
  unfold β
  rw [Real.cos_arccos (by linarith) ((div_le_one (by positivity)).2 h.le)]

lemma β_nonneg : 0 ≤ β := Real.arccos_nonneg _

lemma β_le : β ≤ π / 2 := Real.arccos_le_pi_div_two.2 (by positivity)

lemma cos_two_β : Real.cos (2 * β) = -2 / 3 := by
  rw [Real.cos_two_mul, cos_β, div_pow, one_pow, Real.sq_sqrt (by norm_num)]
  norm_num

lemma sin_two_β : Real.sin (2 * β) = √5 / 3 := by
  rw [Real.sin_eq_sqrt_one_sub_cos_sq (by linarith [β_nonneg]) (by linarith [β_le]), cos_two_β,
    show (1 : ℝ) - (-2 / 3) ^ 2 = (√5 / 3) ^ 2 by linear_combination (-1 / 9) * sqrt5_sq]
  exact Real.sqrt_sq (by positivity)

lemma sqrt_two_thirds_le_one : √(2 / 3 : ℝ) ≤ 1 := by
  rw [show (1 : ℝ) = √1 from Real.sqrt_one.symm]
  exact Real.sqrt_le_sqrt (by norm_num)

lemma cos_γ : Real.cos γ = √(2 / 3) := by
  have h0 : 0 ≤ √(2 / 3 : ℝ) := Real.sqrt_nonneg _
  unfold γ
  rw [Real.cos_arccos (by linarith) sqrt_two_thirds_le_one]

lemma γ_nonneg : 0 ≤ γ := Real.arccos_nonneg _

lemma γ_le : γ ≤ π / 2 := Real.arccos_le_pi_div_two.2 (Real.sqrt_nonneg _)

lemma cos_two_γ : Real.cos (2 * γ) = 1 / 3 := by
  rw [Real.cos_two_mul, cos_γ, Real.sq_sqrt (by norm_num)]
  norm_num

lemma sin_two_γ : Real.sin (2 * γ) = 2 * √2 / 3 := by
  rw [Real.sin_eq_sqrt_one_sub_cos_sq (by linarith [γ_nonneg]) (by linarith [γ_le]), cos_two_γ,
    show (1 : ℝ) - (1 / 3) ^ 2 = (2 * √2 / 3) ^ 2 by linear_combination (-4 / 9) * sqrt2_sq]
  exact Real.sqrt_sq (by positivity)

/-- `2γ = arccos (1/3)`, the dihedral angle of the regular tetrahedron. -/
lemma two_γ_eq : 2 * γ = Real.arccos (1 / 3) := by
  rw [← cos_two_γ, Real.arccos_cos (by linarith [γ_nonneg]) (by linarith [γ_le])]

/-! ### None of 4α, 2β, 2γ is a rational multiple of π (Niven) -/

lemma four_α_not_rat (r : ℚ) : 4 * α ≠ r * π := by
  intro hr
  have hn := niven (θ := 4 * α) ⟨r, hr⟩ ⟨-3 / 5, by rw [cos_four_α]; norm_num⟩
  rw [cos_four_α] at hn
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hn
  norm_num at hn

lemma two_β_not_rat (r : ℚ) : 2 * β ≠ r * π := by
  intro hr
  have hn := niven (θ := 2 * β) ⟨r, hr⟩ ⟨-2 / 3, by rw [cos_two_β]; norm_num⟩
  rw [cos_two_β] at hn
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hn
  norm_num at hn

lemma two_γ_not_rat (r : ℚ) : 2 * γ ≠ r * π := by
  intro hr
  have hn := niven (θ := 2 * γ) ⟨r, hr⟩ ⟨1 / 3, by rw [cos_two_γ]; norm_num⟩
  rw [cos_two_γ] at hn
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hn
  norm_num at hn

lemma int_eq_zero_of_sin {θ : ℝ} (hθ : ∀ r : ℚ, θ ≠ r * π) {R : ℤ} (h : Real.sin (R * θ) = 0) : R = 0 := by
  obtain ⟨n, hn⟩ := Real.sin_eq_zero_iff.1 h
  by_contra hR
  have hR' : (R : ℝ) ≠ 0 := Int.cast_ne_zero.2 hR
  apply hθ (n / R)
  push_cast
  rw [div_mul_eq_mul_div, eq_div_iff hR']
  linear_combination -hn

/-! ### Multiples: cosines rational, sines in ℚ√d -/

lemma nat_mul_form {u : ℝ} {d : ℕ} {c s : ℚ} (hc : Real.cos u = c) (hs : Real.sin u = s * √(d : ℝ))
    (n : ℕ) : ∃ a b : ℚ, Real.cos (n * u) = a ∧ Real.sin (n * u) = b * √(d : ℝ) := by
  have hd : (√(d : ℝ)) ^ 2 = d := Real.sq_sqrt (Nat.cast_nonneg d)
  induction n with
  | zero => exact ⟨1, 0, by simp, by simp⟩
  | succ n ih =>
    obtain ⟨a, b, ha, hb⟩ := ih
    refine ⟨a * c - b * s * d, b * c + a * s, ?_, ?_⟩
    · rw [Nat.cast_succ, add_mul, one_mul, Real.cos_add, ha, hb, hc, hs]
      push_cast
      linear_combination (-(b : ℝ) * s) * hd
    · rw [Nat.cast_succ, add_mul, one_mul, Real.sin_add, ha, hb, hc, hs]
      push_cast
      ring

lemma int_mul_form {u : ℝ} {d : ℕ} {c s : ℚ} (hc : Real.cos u = c) (hs : Real.sin u = s * √(d : ℝ))
    (z : ℤ) : ∃ a b : ℚ, Real.cos (z * u) = a ∧ Real.sin (z * u) = b * √(d : ℝ) := by
  obtain ⟨n, rfl | rfl⟩ := Int.eq_nat_or_neg z
  · obtain ⟨a, b, ha, hb⟩ := nat_mul_form hc hs n
    exact ⟨a, b, by rw [Int.cast_natCast, ha], by rw [Int.cast_natCast, hb]⟩
  · obtain ⟨a, b, ha, hb⟩ := nat_mul_form hc hs n
    refine ⟨a, -b, ?_, ?_⟩
    · rw [Int.cast_neg, Int.cast_natCast, neg_mul, Real.cos_neg, ha]
    · rw [Int.cast_neg, Int.cast_natCast, neg_mul, Real.sin_neg, hb]; push_cast; ring

/-! ### √2 is not in ℚ(√5) (from study 8 of the Dehn Canon) -/

/-- `x` lies in ℚ(√5). -/
def InQ5 (x : ℝ) : Prop := ∃ a b : ℚ, x = a + b * √5

lemma irrational_sqrt10 : Irrational (√10 : ℝ) := by
  have h := (irrational_sqrt_natCast_iff (n := 10)).2 (by
    rintro ⟨r, hr⟩
    have : r ≤ 4 := by nlinarith
    interval_cases r <;> omega)
  simpa using h

/-- A rational multiple of √2 that lies in ℚ(√5) is zero. -/
lemma eq_zero_of_mul_sqrt2_inQ5 {b : ℚ} (h : InQ5 (b * √2)) : b = 0 := by
  obtain ⟨c, d, h⟩ := h
  have h25 : √2 * √5 = √10 := by rw [← Real.sqrt_mul (by norm_num)]; norm_num
  have key : ((2 * b * d : ℚ) : ℝ) * √10 = ((2 * b ^ 2 + 5 * d ^ 2 - c ^ 2 : ℚ) : ℝ) := by
    rw [← h25]; push_cast
    linear_combination (-((b : ℝ) * √2 - d * √5 + c)) * h + (b : ℝ) ^ 2 * sqrt2_sq + (d : ℝ) ^ 2 * sqrt5_sq
  have hbd : b * d = 0 := by
    by_contra hbd
    have h0 : ((2 * b * d : ℚ) : ℝ) ≠ 0 := by
      rw [Rat.cast_ne_zero]; intro e; apply hbd; linarith
    apply irrational_sqrt10.ne_rat ((2 * b ^ 2 + 5 * d ^ 2 - c ^ 2) / (2 * b * d))
    rw [Rat.cast_div, eq_div_iff h0, ← key, mul_comm]
  rcases mul_eq_zero.1 hbd with hb | hd
  · exact hb
  · by_contra hb
    have hb' : (b : ℝ) ≠ 0 := Rat.cast_ne_zero.2 hb
    apply irrational_sqrt_two.ne_rat (c / b)
    rw [Rat.cast_div, eq_div_iff hb', mul_comm, h, hd]
    push_cast; ring

/-! ### The independence -/

lemma cos_four_α' : Real.cos (4 * α) = ((-3 / 5 : ℚ) : ℝ) := by rw [cos_four_α]; push_cast; ring
lemma sin_four_α' : Real.sin (4 * α) = ((-4 / 5 : ℚ) : ℝ) * √((1 : ℕ) : ℝ) := by
  rw [sin_four_α]; push_cast; simp
lemma cos_two_β' : Real.cos (2 * β) = ((-2 / 3 : ℚ) : ℝ) := by rw [cos_two_β]; push_cast; ring
lemma sin_two_β' : Real.sin (2 * β) = ((1 / 3 : ℚ) : ℝ) * √((5 : ℕ) : ℝ) := by
  rw [sin_two_β]; push_cast; ring
lemma cos_two_γ' : Real.cos (2 * γ) = ((1 / 3 : ℚ) : ℝ) := by rw [cos_two_γ]; push_cast; ring
lemma sin_two_γ' : Real.sin (2 * γ) = ((2 / 3 : ℚ) : ℝ) * √((2 : ℕ) : ℝ) := by
  rw [sin_two_γ]; push_cast; ring

/-- **The integer relation.** If P·4α + Q·2β + R·2γ = m·2π with integers P, Q, R, m, then P = Q = R = 0. -/
theorem int_relation (P Q R m : ℤ)
    (h : (P : ℝ) * (4 * α) + Q * (2 * β) + R * (2 * γ) = m * (2 * π)) : P = 0 ∧ Q = 0 ∧ R = 0 := by
  obtain ⟨cA, sA, hcA, hsA⟩ := int_mul_form cos_four_α' sin_four_α' P
  obtain ⟨cB, sB, hcB, hsB⟩ := int_mul_form cos_two_β' sin_two_β' Q
  obtain ⟨cC, sC, hcC, hsC⟩ := int_mul_form cos_two_γ' sin_two_γ' R
  simp only [Nat.cast_one, Real.sqrt_one, mul_one] at hsA
  push_cast at hsB hsC
  -- the √2 part
  have hR : R = 0 := by
    have hs : Real.sin (R * (2 * γ)) = -Real.sin (P * (4 * α) + Q * (2 * β)) := by
      rw [show (R : ℝ) * (2 * γ) = m * (2 * π) - (P * (4 * α) + Q * (2 * β)) by linarith,
        Real.sin_int_mul_two_pi_sub]
    rw [Real.sin_add, hsA, hcA, hsB, hcB, hsC] at hs
    have hC0 : sC = 0 := eq_zero_of_mul_sqrt2_inQ5 ⟨-(sA * cB), -(cA * sB), by rw [hs]; push_cast; ring⟩
    apply int_eq_zero_of_sin two_γ_not_rat
    rw [hsC, hC0]; simp
  subst hR
  have h2 : (P : ℝ) * (4 * α) + Q * (2 * β) = m * (2 * π) := by simpa using h
  have hs : Real.sin (P * (4 * α)) = -Real.sin (Q * (2 * β)) := by
    rw [show (P : ℝ) * (4 * α) = m * (2 * π) - Q * (2 * β) by linarith, Real.sin_int_mul_two_pi_sub]
  rw [hsA, hsB] at hs
  have hB0 : sB = 0 := by
    by_contra hB
    have hB' : (sB : ℝ) ≠ 0 := Rat.cast_ne_zero.2 hB
    apply irrational_sqrt5.ne_rat (-sA / sB)
    rw [Rat.cast_div, eq_div_iff hB', Rat.cast_neg, hs]; ring
  have hQ : Q = 0 := int_eq_zero_of_sin two_β_not_rat (by rw [hsB, hB0]; simp)
  refine ⟨int_eq_zero_of_sin four_α_not_rat ?_, hQ, rfl⟩
  rw [hsA]; rw [hB0] at hs; simpa using hs

lemma exists_int_of_den_dvd (x : ℚ) {n : ℕ} (h : x.den ∣ n) : ∃ z : ℤ, (n : ℝ) * x = z := by
  obtain ⟨k, rfl⟩ := h
  refine ⟨x.num * k, ?_⟩
  have hx : (x : ℝ) * x.den = x.num := by exact_mod_cast Rat.mul_den_eq_num x
  push_cast
  linear_combination (k : ℝ) * hx

/-- **Lemma 3 of the paper: π, α, β and γ are linearly independent over ℚ.** -/
theorem lemma3 (q a b c : ℚ) (h : (q : ℝ) * π + a * α + b * β + c * γ = 0) :
    q = 0 ∧ a = 0 ∧ b = 0 ∧ c = 0 := by
  set D : ℕ := q.den * a.den * b.den * c.den with hD
  have hD0 : (D : ℝ) ≠ 0 := by
    have : D ≠ 0 := by
      rw [hD]; exact Nat.mul_ne_zero (Nat.mul_ne_zero (Nat.mul_ne_zero q.den_ne_zero a.den_ne_zero)
        b.den_ne_zero) c.den_ne_zero
    exact_mod_cast this
  obtain ⟨zq, hzq⟩ := exists_int_of_den_dvd q (n := D)
    (Dvd.dvd.mul_right (Dvd.dvd.mul_right (dvd_mul_right _ _) _) _)
  obtain ⟨za, hza⟩ := exists_int_of_den_dvd a (n := D)
    (Dvd.dvd.mul_right (Dvd.dvd.mul_right (dvd_mul_left _ _) _) _)
  obtain ⟨zb, hzb⟩ := exists_int_of_den_dvd b (n := D) (Dvd.dvd.mul_right (dvd_mul_left _ _) _)
  obtain ⟨zc, hzc⟩ := exists_int_of_den_dvd c (n := D) (dvd_mul_left _ _)
  obtain ⟨hP, hQ, hR⟩ := int_relation (2 * za) (4 * zb) (4 * zc) (-4 * zq) (by
    push_cast
    linear_combination (8 * (D : ℝ)) * h - 8 * α * hza - 8 * β * hzb - 8 * γ * hzc - 8 * π * hzq)
  have ha : za = 0 := by omega
  have hb : zb = 0 := by omega
  have hc : zc = 0 := by omega
  have e : ∀ x : ℚ, ∀ z : ℤ, (D : ℝ) * x = z → z = 0 → x = 0 := by
    intro x z hx hz
    rw [hz, Int.cast_zero] at hx
    exact_mod_cast (mul_eq_zero.1 hx).resolve_left hD0
  have ha' := e a za hza ha
  have hb' := e b zb hzb hb
  have hc' := e c zc hzc hc
  subst ha' hb' hc'
  refine ⟨?_, rfl, rfl, rfl⟩
  have : (q : ℝ) * π = 0 := by simpa using h
  exact_mod_cast (mul_eq_zero.1 this).resolve_right Real.pi_ne_zero

end Packets
