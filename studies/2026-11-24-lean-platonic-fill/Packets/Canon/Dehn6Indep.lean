/-
Lean study 6 of the shape-language canon (DICTO, 19 Nov 2026), part S: the two angles α, β of the three words
AXE, CLEO, FUJI are independent modulo π.

* `word_angles_int_indep`: for integers p, q, if p α + q β is a rational multiple of π then p = 0 and q = 0.

Method (classical: a relation between angles makes a product of the numbers e^{2iα}, e^{2iβ} a root of unity,
and a root of unity has valuation 0 at every prime; here the valuation at 3 is read from real parts only, so
that no number field, no ideal and no complex number is needed):
cos 2α = −3/5 and cos 2β = −(10 + 8√5)/30. By the recurrence cos((n+2)x) = 2 cos x cos((n+1)x) − cos(n x),
2·5ⁿ cos(2nα) is an integer d_n and 2·15ⁿ cos(2nβ) = a_n + b_n √5 with integers a_n, b_n, where
(a, b) ↦ (−10a − 40b, −8a − 10b) is multiplication by −(10 + 8√5), of norm −220. Hence
a_{n+1}² − 5 b_{n+1}² = −220 (a_n² − 5 b_n²) modulo 225, and 3 never divides a_n² − 5 b_n² for n ≥ 1.
A relation P·2α + Q·2β = m·2π gives cos(2|Q|β) = cos(2|P|α), so 5^|P| (a + b√5) = 15^|Q| d; as √5 is
irrational, b = 0 and 3 divides a when |Q| ≥ 1, so 3 divides a² − 5b²: impossible. So Q = 0, and then P = 0
because α is not a rational multiple of π (study 4, Niven's theorem).

Credits: Mathlib `Real.cos_add`, `Real.cos_sub`, `Real.cos_two_mul`, `Real.cos_int_mul_two_pi_sub`,
`Nat.twoStepInduction`, `Irrational.ne_rat`, `Int.prime_three`, `Rat.mul_den_eq_num`; the tactic `omega`.
Studies 4 and 5 of this canon: `irrational_sqrt5`, `wordAlpha_not_ratPi` (Niven's theorem `niven`),
`cos_wordAlpha`, `cos_wordBeta`, `wordR_sq`.
No `sorry`.
-/
module

public import Packets.Canon.Dehn5Angles

@[expose] public section

open scoped Real

namespace DehnCanon.Library

/-! ### The cosines of the doubled angles -/

/-- cos(y + x) = 2 cos x cos y − cos(y − x). -/
lemma cos_step (x y : ℝ) : Real.cos (y + x) = 2 * Real.cos x * Real.cos y - Real.cos (y - x) := by
  rw [Real.cos_add, Real.cos_sub]; ring

lemma cos_two_wordAlpha : Real.cos (2 * wordAlpha) = -3 / 5 := by
  rw [Real.cos_two_mul, cos_wordAlpha]
  linear_combination (2 / 25 : ℝ) * sqrt5_sq

lemma cos_two_wordBeta : Real.cos (2 * wordBeta) = -(10 + 8 * √5) / 30 := by
  have hR : (3 * (10 - 2 * √5) : ℝ) ≠ 0 := by
    rw [← wordR_sq]; exact pow_ne_zero 2 wordR_pos.ne'
  have h : Real.cos wordBeta ^ 2 = (5 - 2 * √5) / 15 := by
    rw [cos_wordBeta, div_pow, wordR_sq, div_eq_iff hR]
    linear_combination (1 / 5 : ℝ) * sqrt5_sq
  rw [Real.cos_two_mul, h]; ring

/-! ### Two integer sequences -/

/-- d_n = 2·5ⁿ cos(2nα): d₀ = 2, d₁ = −6, d_{n+2} = −6 d_{n+1} − 25 d_n. -/
def wordSeqA : ℕ → ℤ
  | 0 => 2
  | 1 => -6
  | n + 2 => -6 * wordSeqA (n + 1) - 25 * wordSeqA n

/-- (a_n, b_n) with a_n + b_n √5 = 2·15ⁿ cos(2nβ): (2, 0), (−10, −8), and
x_{n+2} = −(10 + 8√5) x_{n+1} − 225 x_n written in the two coordinates. -/
def wordSeqB : ℕ → ℤ × ℤ
  | 0 => (2, 0)
  | 1 => (-10, -8)
  | n + 2 => (-10 * (wordSeqB (n + 1)).1 - 40 * (wordSeqB (n + 1)).2 - 225 * (wordSeqB n).1,
      -8 * (wordSeqB (n + 1)).1 - 10 * (wordSeqB (n + 1)).2 - 225 * (wordSeqB n).2)

lemma wordSeqA_succ_succ (n : ℕ) :
    wordSeqA (n + 2) = -6 * wordSeqA (n + 1) - 25 * wordSeqA n := by
  rw [wordSeqA]

lemma wordSeqB_succ_succ (n : ℕ) :
    wordSeqB (n + 2) = (-10 * (wordSeqB (n + 1)).1 - 40 * (wordSeqB (n + 1)).2 - 225 * (wordSeqB n).1,
      -8 * (wordSeqB (n + 1)).1 - 10 * (wordSeqB (n + 1)).2 - 225 * (wordSeqB n).2) := by
  rw [wordSeqB]

/-- 2·5ⁿ cos(2nα) is the integer d_n. -/
lemma wordSeqA_cos (n : ℕ) : 2 * (5 : ℝ) ^ n * Real.cos (n * (2 * wordAlpha)) = wordSeqA n := by
  induction n using Nat.twoStepInduction with
  | zero => simp [wordSeqA]
  | one =>
    have e : wordSeqA 1 = -6 := rfl
    rw [Nat.cast_one, one_mul, cos_two_wordAlpha, e]; norm_num
  | more n h0 h1 =>
    have e : ((n + 2 : ℕ) : ℝ) * (2 * wordAlpha) = ((n + 1 : ℕ) : ℝ) * (2 * wordAlpha) + 2 * wordAlpha := by
      push_cast; ring
    have e' : ((n + 1 : ℕ) : ℝ) * (2 * wordAlpha) - 2 * wordAlpha = (n : ℝ) * (2 * wordAlpha) := by
      push_cast; ring
    rw [e, cos_step, e', cos_two_wordAlpha, wordSeqA_succ_succ]
    push_cast at h1 ⊢
    linear_combination (-6 : ℝ) * h1 - 25 * h0

/-- 2·15ⁿ cos(2nβ) = a_n + b_n √5. -/
lemma wordSeqB_cos (n : ℕ) :
    2 * (15 : ℝ) ^ n * Real.cos (n * (2 * wordBeta)) = (wordSeqB n).1 + (wordSeqB n).2 * √5 := by
  induction n using Nat.twoStepInduction with
  | zero => simp [wordSeqB]
  | one =>
    have e : wordSeqB 1 = (-10, -8) := rfl
    rw [Nat.cast_one, one_mul, cos_two_wordBeta, e]; push_cast; ring
  | more n h0 h1 =>
    have e : ((n + 2 : ℕ) : ℝ) * (2 * wordBeta) = ((n + 1 : ℕ) : ℝ) * (2 * wordBeta) + 2 * wordBeta := by
      push_cast; ring
    have e' : ((n + 1 : ℕ) : ℝ) * (2 * wordBeta) - 2 * wordBeta = (n : ℝ) * (2 * wordBeta) := by
      push_cast; ring
    rw [e, cos_step, e', cos_two_wordBeta, wordSeqB_succ_succ]
    push_cast at h1 ⊢
    linear_combination (-(10 + 8 * √5)) * h1 - 225 * h0 - 8 * ((wordSeqB (n + 1)).2 : ℝ) * sqrt5_sq

/-! ### The invariant at 3 -/

lemma not_three_dvd_step (N K X : ℤ) (h : X = -220 * N + 3 * K) (hN : ¬ (3 : ℤ) ∣ N) : ¬ (3 : ℤ) ∣ X := by
  omega

/-- One step of the recurrence multiplies the norm a² − 5b² by −220, up to a multiple of 225. -/
lemma wordSeqB_norm_step (a b a0 b0 : ℤ) :
    (-10 * a - 40 * b - 225 * a0) ^ 2 - 5 * (-8 * a - 10 * b - 225 * b0) ^ 2 =
      -220 * (a ^ 2 - 5 * b ^ 2) + 3 * (75 * (-2 * (-10 * a - 40 * b) * a0 + 225 * a0 ^ 2 +
        10 * (-8 * a - 10 * b) * b0 - 1125 * b0 ^ 2)) := by
  ring

/-- **3 does not divide a_n² − 5 b_n² for n ≥ 1.** -/
lemma wordSeqB_norm (n : ℕ) :
    ¬ (3 : ℤ) ∣ (wordSeqB (n + 1)).1 ^ 2 - 5 * (wordSeqB (n + 1)).2 ^ 2 := by
  induction n with
  | zero => decide
  | succ n ih =>
    rw [wordSeqB_succ_succ]
    exact not_three_dvd_step _ _ _ (wordSeqB_norm_step _ _ _ _) ih

/-! ### The relation -/

/-- If x + y√5 = 0 with integers x, y then x = 0 and y = 0. -/
lemma int_add_mul_sqrt5 {x y : ℤ} (h : (x : ℝ) + y * √5 = 0) : x = 0 ∧ y = 0 := by
  have hy : y = 0 := by
    by_contra hy
    have hy' : (y : ℝ) ≠ 0 := Int.cast_ne_zero.2 hy
    apply irrational_sqrt5.ne_rat (-x / y : ℚ)
    push_cast
    rw [eq_div_iff hy']
    linarith
  refine ⟨?_, hy⟩
  rw [hy] at h
  simpa using h

lemma cos_int_mul_natAbs (Q : ℤ) (x : ℝ) : Real.cos (Q * x) = Real.cos ((Q.natAbs : ℝ) * x) := by
  rcases Int.natAbs_eq Q with e | e
  · have h := congrArg (Int.cast (R := ℝ)) e
    rw [Int.cast_natCast] at h
    rw [h]
  · have h := congrArg (Int.cast (R := ℝ)) e
    rw [Int.cast_neg, Int.cast_natCast] at h
    rw [h, neg_mul, Real.cos_neg]

/-- **The key step**: a relation P·2α + Q·2β = m·2π with integers P, Q, m has Q = 0. -/
theorem word_double_angles (P Q m : ℤ)
    (h : (P : ℝ) * (2 * wordAlpha) + Q * (2 * wordBeta) = m * (2 * π)) : Q = 0 := by
  by_contra hQ
  have hc : Real.cos (Q * (2 * wordBeta)) = Real.cos (P * (2 * wordAlpha)) := by
    rw [show (Q : ℝ) * (2 * wordBeta) = m * (2 * π) - P * (2 * wordAlpha) by linarith,
      Real.cos_int_mul_two_pi_sub]
  rw [cos_int_mul_natAbs Q, cos_int_mul_natAbs P] at hc
  obtain ⟨j, hj⟩ : ∃ j, Q.natAbs = j + 1 := Nat.exists_eq_succ_of_ne_zero (Int.natAbs_ne_zero.2 hQ)
  rw [hj] at hc
  have hB := wordSeqB_cos (j + 1)
  have hA := wordSeqA_cos P.natAbs
  have hn := wordSeqB_norm j
  generalize P.natAbs = k at hc hA
  generalize wordSeqA k = d at hA
  generalize wordSeqB (j + 1) = ab at hB hn
  obtain ⟨a, b⟩ := ab
  simp only at hB hn
  have e : (((5 : ℤ) ^ k * a - 15 ^ (j + 1) * d : ℤ) : ℝ) + (((5 : ℤ) ^ k * b : ℤ) : ℝ) * √5 = 0 := by
    push_cast
    linear_combination (-(5 : ℝ) ^ k) * hB + (15 : ℝ) ^ (j + 1) * hA + 2 * 5 ^ k * 15 ^ (j + 1) * hc
  obtain ⟨h1, h2⟩ := int_add_mul_sqrt5 e
  have hb : b = 0 := (mul_eq_zero.1 h2).resolve_left (pow_ne_zero _ (by norm_num))
  have hdvd : (3 : ℤ) ∣ 5 ^ k * a := ⟨5 * 15 ^ j * d, by linear_combination h1⟩
  have ha : (3 : ℤ) ∣ a := by
    refine (Int.prime_three.dvd_or_dvd hdvd).resolve_left fun h5 => ?_
    have h5' := Int.prime_three.dvd_of_dvd_pow h5
    omega
  apply hn
  obtain ⟨c, hc'⟩ := ha
  exact ⟨3 * c ^ 2, by rw [hb, hc']; ring⟩

/-- **α and β are independent modulo π**: if p α + q β is a rational multiple of π, with integers p, q,
then p = 0 and q = 0. -/
theorem word_angles_int_indep (p q : ℤ) (h : (p : ℝ) * wordAlpha + q * wordBeta ∈ ratPi) :
    p = 0 ∧ q = 0 := by
  rw [mem_ratPi_iff] at h
  obtain ⟨r, hr⟩ := h
  have hrr : (r : ℝ) * r.den = r.num := by exact_mod_cast Rat.mul_den_eq_num r
  have hq : q = 0 := by
    have h0 := word_double_angles (r.den * p) (r.den * q) r.num (by
      push_cast
      linear_combination (2 * (r.den : ℝ)) * hr + (2 * π) * hrr)
    rcases mul_eq_zero.1 h0 with h' | h'
    · exact absurd h' (by exact_mod_cast r.den_ne_zero)
    · exact h'
  subst hq
  refine ⟨?_, rfl⟩
  by_contra hp
  have hp' : (p : ℝ) ≠ 0 := Int.cast_ne_zero.2 hp
  have hr' : (p : ℝ) * wordAlpha = r * π := by simpa using hr
  apply wordAlpha_not_ratPi
  rw [mem_ratPi_iff]
  refine ⟨r / p, ?_⟩
  push_cast
  rw [div_mul_eq_mul_div, eq_div_iff hp', ← hr', mul_comm]

end DehnCanon.Library
