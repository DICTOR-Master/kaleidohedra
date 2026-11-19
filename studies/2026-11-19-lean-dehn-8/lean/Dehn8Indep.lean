/-
Lean study 8 of the shape-language canon (DICTO, 19 Nov 2026), part AA: the angle θ = arccos(1/3) of the
tetrahedron and the octahedron is independent of the two angles α, β of the dodecahedron, the icosahedron and
the three words, modulo π.

* `tet_word_angles_indep`: for rationals p, q, r, if p θ + q α + r β is a rational multiple of π then
  p = q = r = 0 (`tet_word_angles_int_indep`: the same for integers).
* `tet_not_mem_span`: in the angle classes modulo ℚπ, θ is not a rational combination of α and β.

Method (two quadratic fields; no prime, no valuation): cos θ = 1/3 and sin θ = (2/3)√2, so by the addition
formulas cos(nθ) is rational and sin(nθ) is a rational multiple of √2 for every integer n. The cosines and sines
of 2α and 2β lie in ℚ(√5) (cos 2α = −3/5, sin 2α = 4/5, cos 2β = −(10 + 8√5)/30, sin 2β = (10 − 2√5)/15), so the
sine of every Q·2α + R·2β lies in ℚ(√5). A relation P θ + Q·2α + R·2β = m·2π gives sin(Pθ) = −sin(Q·2α + R·2β),
a rational multiple of √2 that lies in ℚ(√5); as √2 is not in ℚ(√5) (√10 is irrational), sin(Pθ) = 0, so Pθ is
a multiple of π, and P = 0 because θ is not a rational multiple of π (study 1, Niven's theorem). Then
q α + r β is a rational multiple of π, and q = r = 0 by study 6.
This is the field form of the classical argument: e^{iθ} lies in ℚ(√−2), e^{2iα} and e^{2iβ} in ℚ(√5, i), and
these two fields meet only in ℚ. The independence on paper is in Conway, Radin and Sadun (1999), for angles
with rational squared cosine such as arccos(1/3) and arccos(1/√5), and, for α and γ, in Ogievetsky and
Papadopolos (1999), Lemma 2; this file is a machine-checked version.

Credits: Mathlib `Real.cos_add`, `Real.sin_add`, `Real.sin_two_mul`, `Real.sin_arccos`, `Real.cos_arccos`,
`Real.sin_int_mul_two_pi_sub`, `Real.sin_eq_zero_iff`, `Real.sqrt_mul`, `irrational_sqrt_two`,
`irrational_sqrt_natCast_iff`, `Irrational.ne_rat`, `Int.eq_nat_or_neg`, `Rat.mul_den_eq_num`,
`Submodule.mem_span_pair`. Studies 1, 5 and 6 of this canon: `tetDihedral_not_ratPi`, `mem_ratPi_iff`,
`sqrt_one_sub_sq`, `sin_wordAlpha`, `cos_wordAlpha`, `sin_wordBeta`, `cos_wordBeta`, `wordR_sq`, `wordR_pos`,
`cos_two_wordAlpha`, `cos_two_wordBeta`, `word_angles_int_indep`; study 4: `sqrt5_sq`.
No `sorry`.
-/
import DehnCanon.Dehn6Indep

open scoped Real

namespace DehnCanon

/-! ### Multiples of θ = arccos(1/3): cosines in ℚ, sines in ℚ√2 -/

lemma sqrt2_sq : (√2 : ℝ) ^ 2 = 2 := Real.sq_sqrt (by norm_num)

lemma cos_tetDihedral : Real.cos tetDihedral = 1 / 3 := by
  unfold tetDihedral; rw [Real.cos_arccos] <;> norm_num

lemma sin_tetDihedral : Real.sin tetDihedral = 2 * √2 / 3 := by
  unfold tetDihedral
  rw [Real.sin_arccos]
  exact sqrt_one_sub_sq (by positivity) (by linear_combination (4 / 9 : ℝ) * sqrt2_sq)

/-- cos(nθ) is rational and sin(nθ) is a rational multiple of √2. -/
lemma tet_nat_mul (n : ℕ) :
    ∃ a b : ℚ, Real.cos (n * tetDihedral) = a ∧ Real.sin (n * tetDihedral) = b * √2 := by
  induction n with
  | zero => exact ⟨1, 0, by simp, by simp⟩
  | succ n ih =>
    obtain ⟨a, b, ha, hb⟩ := ih
    refine ⟨a / 3 - 4 * b / 3, b / 3 + 2 * a / 3, ?_, ?_⟩
    · rw [Nat.cast_succ, add_mul, one_mul, Real.cos_add, ha, hb, cos_tetDihedral, sin_tetDihedral]
      push_cast
      linear_combination (-(2 * (b : ℝ) / 3)) * sqrt2_sq
    · rw [Nat.cast_succ, add_mul, one_mul, Real.sin_add, ha, hb, cos_tetDihedral, sin_tetDihedral]
      push_cast
      ring

/-- sin(zθ) is a rational multiple of √2 for every integer z. -/
lemma tet_int_mul_sin (z : ℤ) : ∃ b : ℚ, Real.sin (z * tetDihedral) = b * √2 := by
  obtain ⟨n, rfl | rfl⟩ := Int.eq_nat_or_neg z
  · obtain ⟨-, b, -, hb⟩ := tet_nat_mul n
    exact ⟨b, by rw [Int.cast_natCast, hb]⟩
  · obtain ⟨-, b, -, hb⟩ := tet_nat_mul n
    exact ⟨-b, by rw [Int.cast_neg, Int.cast_natCast, neg_mul, Real.sin_neg, hb]; push_cast; ring⟩

/-! ### The field ℚ(√5) -/

/-- `x` lies in ℚ(√5). -/
def InQ5 (x : ℝ) : Prop := ∃ a b : ℚ, x = a + b * √5

lemma InQ5.add {x y : ℝ} (hx : InQ5 x) (hy : InQ5 y) : InQ5 (x + y) := by
  obtain ⟨a, b, rfl⟩ := hx; obtain ⟨c, d, rfl⟩ := hy
  exact ⟨a + c, b + d, by push_cast; ring⟩

lemma InQ5.neg {x : ℝ} (hx : InQ5 x) : InQ5 (-x) := by
  obtain ⟨a, b, rfl⟩ := hx
  exact ⟨-a, -b, by push_cast; ring⟩

lemma InQ5.sub {x y : ℝ} (hx : InQ5 x) (hy : InQ5 y) : InQ5 (x - y) := by
  rw [sub_eq_add_neg]; exact hx.add hy.neg

lemma InQ5.mul {x y : ℝ} (hx : InQ5 x) (hy : InQ5 y) : InQ5 (x * y) := by
  obtain ⟨a, b, rfl⟩ := hx; obtain ⟨c, d, rfl⟩ := hy
  exact ⟨a * c + 5 * b * d, a * d + b * c, by push_cast; linear_combination ((b : ℝ) * d) * sqrt5_sq⟩

/-- If cos u and sin u lie in ℚ(√5), so do cos(nu) and sin(nu). -/
lemma inQ5_nat_mul {u : ℝ} (hc : InQ5 (Real.cos u)) (hs : InQ5 (Real.sin u)) (n : ℕ) :
    InQ5 (Real.cos (n * u)) ∧ InQ5 (Real.sin (n * u)) := by
  induction n with
  | zero => exact ⟨⟨1, 0, by simp⟩, ⟨0, 0, by simp⟩⟩
  | succ n ih =>
    rw [Nat.cast_succ, add_mul, one_mul, Real.cos_add, Real.sin_add]
    exact ⟨(ih.1.mul hc).sub (ih.2.mul hs), (ih.2.mul hc).add (ih.1.mul hs)⟩

lemma inQ5_int_mul {u : ℝ} (hc : InQ5 (Real.cos u)) (hs : InQ5 (Real.sin u)) (z : ℤ) :
    InQ5 (Real.cos (z * u)) ∧ InQ5 (Real.sin (z * u)) := by
  obtain ⟨n, rfl | rfl⟩ := Int.eq_nat_or_neg z
  · rw [Int.cast_natCast]; exact inQ5_nat_mul hc hs n
  · rw [Int.cast_neg, Int.cast_natCast, neg_mul, Real.cos_neg, Real.sin_neg]
    exact ⟨(inQ5_nat_mul hc hs n).1, (inQ5_nat_mul hc hs n).2.neg⟩

lemma cos_two_wordAlpha_inQ5 : InQ5 (Real.cos (2 * wordAlpha)) :=
  ⟨-3 / 5, 0, by rw [cos_two_wordAlpha]; push_cast; ring⟩

lemma sin_two_wordAlpha_inQ5 : InQ5 (Real.sin (2 * wordAlpha)) :=
  ⟨4 / 5, 0, by
    rw [Real.sin_two_mul, sin_wordAlpha, cos_wordAlpha]; push_cast
    linear_combination (4 / 25 : ℝ) * sqrt5_sq⟩

lemma cos_two_wordBeta_inQ5 : InQ5 (Real.cos (2 * wordBeta)) :=
  ⟨-1 / 3, -4 / 15, by rw [cos_two_wordBeta]; push_cast; ring⟩

/-- sin 2β = (10 − 2√5)/15. -/
lemma sin_two_wordBeta : Real.sin (2 * wordBeta) = (10 - 2 * √5) / 15 := by
  have hR : wordR ^ 2 ≠ 0 := pow_ne_zero 2 wordR_pos.ne'
  rw [Real.sin_two_mul, sin_wordBeta, cos_wordBeta,
    show 2 * (4 / wordR) * ((3 - √5) / wordR) = 8 * (3 - √5) / wordR ^ 2 by field_simp; ring,
    div_eq_iff hR, wordR_sq]
  linear_combination (-4 / 5 : ℝ) * sqrt5_sq

lemma sin_two_wordBeta_inQ5 : InQ5 (Real.sin (2 * wordBeta)) :=
  ⟨2 / 3, -2 / 15, by rw [sin_two_wordBeta]; push_cast; ring⟩

/-- The sine of every Q·2α + R·2β lies in ℚ(√5). -/
lemma sin_word_comb_inQ5 (Q R : ℤ) : InQ5 (Real.sin (Q * (2 * wordAlpha) + R * (2 * wordBeta))) := by
  have hA := inQ5_int_mul cos_two_wordAlpha_inQ5 sin_two_wordAlpha_inQ5 Q
  have hB := inQ5_int_mul cos_two_wordBeta_inQ5 sin_two_wordBeta_inQ5 R
  rw [Real.sin_add]
  exact (hA.2.mul hB.1).add (hA.1.mul hB.2)

/-! ### √2 is not in ℚ(√5) -/

lemma irrational_sqrt10 : Irrational (√10 : ℝ) := by
  have h := (irrational_sqrt_natCast_iff (n := 10)).2 (by
    rintro ⟨r, hr⟩
    have : r ≤ 4 := by nlinarith
    interval_cases r <;> omega)
  simpa using h

/-- **A rational multiple of √2 that lies in ℚ(√5) is zero.** -/
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

/-- **The key step**: a relation P θ + Q·2α + R·2β = m·2π with integers P, Q, R, m has P = 0. -/
theorem tet_word_relation (P Q R m : ℤ)
    (h : (P : ℝ) * tetDihedral + Q * (2 * wordAlpha) + R * (2 * wordBeta) = m * (2 * π)) : P = 0 := by
  have hs : Real.sin (P * tetDihedral) = -Real.sin (Q * (2 * wordAlpha) + R * (2 * wordBeta)) := by
    rw [show (P : ℝ) * tetDihedral = m * (2 * π) - (Q * (2 * wordAlpha) + R * (2 * wordBeta)) by linarith,
      Real.sin_int_mul_two_pi_sub]
  obtain ⟨b, hb⟩ := tet_int_mul_sin P
  have hb0 : b = 0 := eq_zero_of_mul_sqrt2_inQ5 (by rw [← hb, hs]; exact (sin_word_comb_inQ5 Q R).neg)
  rw [hb0, Rat.cast_zero, zero_mul] at hb
  obtain ⟨n, hn⟩ := Real.sin_eq_zero_iff.1 hb
  by_contra hP
  have hP' : (P : ℝ) ≠ 0 := Int.cast_ne_zero.2 hP
  apply tetDihedral_not_ratPi
  rw [mem_ratPi_iff]
  refine ⟨n / P, ?_⟩
  push_cast
  rw [div_mul_eq_mul_div, eq_div_iff hP', hn, mul_comm]

/-- **θ, α, β are independent modulo π (integer form).** If p θ + q α + r β is a rational multiple of π, with
integers p, q, r, then p = q = r = 0. -/
theorem tet_word_angles_int_indep (p q r : ℤ)
    (h : (p : ℝ) * tetDihedral + q * wordAlpha + r * wordBeta ∈ ratPi) : p = 0 ∧ q = 0 ∧ r = 0 := by
  obtain ⟨s, hs⟩ := (mem_ratPi_iff _).1 h
  have hrr : (s : ℝ) * s.den = s.num := by exact_mod_cast Rat.mul_den_eq_num s
  have hp : p = 0 := by
    have h0 := tet_word_relation (2 * s.den * p) (s.den * q) (s.den * r) s.num (by
      push_cast
      linear_combination (2 * (s.den : ℝ)) * hs + (2 * π) * hrr)
    have hd : (2 * (s.den : ℤ)) ≠ 0 := by have := s.den_ne_zero; omega
    exact (mul_eq_zero.1 h0).resolve_left hd
  subst hp
  have h' : (q : ℝ) * wordAlpha + r * wordBeta ∈ ratPi := by
    rw [mem_ratPi_iff]; exact ⟨s, by rw [← hs]; push_cast; ring⟩
  exact ⟨rfl, word_angles_int_indep q r h'⟩

/-- **θ, α, β are independent modulo π.** If p θ + q α + r β is a rational multiple of π, with rationals
p, q, r, then p = q = r = 0. -/
theorem tet_word_angles_indep (p q r : ℚ)
    (h : (p : ℝ) * tetDihedral + q * wordAlpha + r * wordBeta ∈ ratPi) : p = 0 ∧ q = 0 ∧ r = 0 := by
  obtain ⟨s, hs⟩ := (mem_ratPi_iff _).1 h
  have hp : (p : ℝ) * p.den = p.num := by exact_mod_cast Rat.mul_den_eq_num p
  have hq : (q : ℝ) * q.den = q.num := by exact_mod_cast Rat.mul_den_eq_num q
  have hr : (r : ℝ) * r.den = r.num := by exact_mod_cast Rat.mul_den_eq_num r
  obtain ⟨h1, h2, h3⟩ := tet_word_angles_int_indep (p.num * q.den * r.den) (q.num * p.den * r.den)
    (r.num * p.den * q.den) ((mem_ratPi_iff _).2 ⟨s * p.den * q.den * r.den, by
      push_cast
      linear_combination ((p.den : ℝ) * q.den * r.den) * hs - ((q.den : ℝ) * r.den * tetDihedral) * hp -
        ((p.den : ℝ) * r.den * wordAlpha) * hq - ((p.den : ℝ) * q.den * wordBeta) * hr⟩)
  have hpd : (q.den : ℤ) * r.den ≠ 0 := mul_ne_zero (by exact_mod_cast q.den_ne_zero) (by exact_mod_cast r.den_ne_zero)
  have hqd : (p.den : ℤ) * r.den ≠ 0 := mul_ne_zero (by exact_mod_cast p.den_ne_zero) (by exact_mod_cast r.den_ne_zero)
  have hrd : (p.den : ℤ) * q.den ≠ 0 := mul_ne_zero (by exact_mod_cast p.den_ne_zero) (by exact_mod_cast q.den_ne_zero)
  rw [mul_assoc] at h1 h2 h3
  exact ⟨Rat.num_eq_zero.1 ((mul_eq_zero.1 h1).resolve_right hpd),
    Rat.num_eq_zero.1 ((mul_eq_zero.1 h2).resolve_right hqd),
    Rat.num_eq_zero.1 ((mul_eq_zero.1 h3).resolve_right hrd)⟩

/-- **In the angle classes modulo ℚπ, θ is not a rational combination of α and β.** -/
theorem tet_not_mem_span : (Submodule.Quotient.mk tetDihedral : Angle) ∉
    Submodule.span ℚ {(Submodule.Quotient.mk wordAlpha : Angle), Submodule.Quotient.mk wordBeta} := by
  intro hm
  obtain ⟨a, b, hab⟩ := Submodule.mem_span_pair.1 hm
  have hz : (Submodule.Quotient.mk (tetDihedral - a • wordAlpha - b • wordBeta) : Angle) = 0 := by
    rw [Submodule.Quotient.mk_sub, Submodule.Quotient.mk_sub, Submodule.Quotient.mk_smul,
      Submodule.Quotient.mk_smul, ← hab]
    abel
  rw [Submodule.Quotient.mk_eq_zero] at hz
  have := (tet_word_angles_indep 1 (-a) (-b) (by
    convert hz using 1
    simp only [Rat.smul_def]; push_cast; ring)).1
  exact one_ne_zero this

end DehnCanon
