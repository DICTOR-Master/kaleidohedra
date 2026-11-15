module

public import Mathlib
public import LoopEquality.Explicit

@[expose] public section

/-!
# The aperiodic Fibonacci stacking (DICTO, Fibonacci stackings, 28 Oct 2026; #102 checks)

The layer types `c`/`h` follow the Fibonacci word (substitution `c ↦ ch`,
`h ↦ c`, from `c`): `c h c c h c h c c h …`. As a Sturmian word of slope
`α = 1/φ² = (3 − √5)/2` its letter at position `k` is `h` exactly when
`⌊(k+2)α⌋ ≠ ⌊(k+1)α⌋` (cut-and-project form; Morse–Hedlund 1940; Lothaire,
*Algebraic Combinatorics on Words*, 2002, Ch. 2). We take this form as the
definition, for all `k ∈ ℤ` (the two-sided Sturmian extension of DICTO's
one-sided word), and check it against the substitution for `k < 100`
(`isH_eq_word`).

Layers are stacked by Jagodzinski's rule, as in DICTO's study and #102's
checks: the step `σ(k+1) − σ(k) = ±1` keeps its direction at a `c` layer and
reverses at an `h` layer, with `σ 0 = A`, `σ 1 = B`. Hence the step is
`(−1)^⌊(k+2)α⌋` (`fibStep`).

Results:
* `fibonacci_isStacking`: it is a close-packed stacking;
* `fibonacci_layer_type`: layer `k` is hexagonal (`σ(k−1) = σ(k+1)`) exactly when
  the Fibonacci letter at `k` is `h`;
* `isH_not_periodic`, `fibonacci_not_periodic`: neither the type word nor the
  stacking is periodic (the frequency of `h` would be rational; `α` is irrational
  because `√5` is);
* `fibonacci_loop_equality`: at every site of the Fibonacci stacking the number
  of closed non-backtracking loops of length `m` is diamond's, and is `loopCount m`.
-/

namespace LoopEqualityProof

open Finset

/-- `α = 1/φ² = (3 − √5)/2`, the frequency of `h` in the Fibonacci word. -/
noncomputable def fibAlpha : ℝ := (3 - Real.sqrt 5) / 2

/-- `⌊(k+2)α⌋`: the number of `h` letters at positions `1, …, k` (for `k ≥ 0`). -/
noncomputable def fibFlip (k : ℤ) : ℤ := ⌊((k : ℝ) + 2) * fibAlpha⌋

/-- The Fibonacci letter at position `k` is `h`. -/
def IsH (k : ℤ) : Prop := fibFlip k ≠ fibFlip (k - 1)

/-- The step `σ(k+1) − σ(k)`: `+1` or `−1` (`(−1)^⌊(k+2)α⌋`). -/
noncomputable def fibStep (k : ℤ) : ZMod 3 := if Even (fibFlip k) then 1 else -1

/-- The Fibonacci stacking: `σ 0 = A` and the steps `fibStep`. -/
noncomputable def fibonacci (k : ℤ) : ZMod 3 :=
  if 0 ≤ k then ∑ n ∈ range k.toNat, fibStep n
  else -∑ n ∈ range (-k).toNat, fibStep (-1 - n)

/-! ## Basic facts about `α` -/

theorem sqrt5_irrational : Irrational (Real.sqrt 5) := by
  have := Nat.Prime.irrational_sqrt (p := 5) (by norm_num)
  simpa using this

theorem sqrt5_bounds : 2 < Real.sqrt 5 ∧ Real.sqrt 5 < 3 := by
  constructor
  · rw [show (2 : ℝ) = Real.sqrt 4 by rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  · rw [Real.sqrt_lt' (by norm_num)]; norm_num

theorem fibAlpha_pos : 0 < fibAlpha := by
  unfold fibAlpha; linarith [sqrt5_bounds.2]

theorem fibAlpha_lt_half : fibAlpha < 1 / 2 := by
  unfold fibAlpha; linarith [sqrt5_bounds.1]

theorem fibFlip_step (k : ℤ) : fibFlip k = fibFlip (k - 1) ∨ fibFlip k = fibFlip (k - 1) + 1 := by
  unfold fibFlip
  have ha := fibAlpha_pos
  have hb := fibAlpha_lt_half
  have e : (((k - 1 : ℤ) : ℝ) + 2) * fibAlpha = ((k : ℝ) + 2) * fibAlpha - fibAlpha := by
    push_cast; ring
  rw [e]
  set x := ((k : ℝ) + 2) * fibAlpha
  have h1 : ⌊x - fibAlpha⌋ ≤ ⌊x⌋ := Int.floor_mono (by linarith)
  have h2 : ⌊x⌋ ≤ ⌊x - fibAlpha⌋ + 1 := by
    rw [← Int.floor_add_one]; exact Int.floor_mono (by linarith)
  omega

theorem fibFlip_zero : fibFlip 0 = 0 := by
  unfold fibFlip
  rw [Int.floor_eq_iff]
  have ha := fibAlpha_pos
  have hb := fibAlpha_lt_half
  push_cast
  constructor <;> nlinarith

/-! ## A close-packed stacking -/

theorem fibStep_ne_zero (k : ℤ) : fibStep k ≠ 0 := by
  unfold fibStep; split_ifs <;> decide

theorem fibonacci_nonpos {k : ℤ} (hk : k ≤ 0) :
    fibonacci k = -∑ n ∈ range (-k).toNat, fibStep (-1 - n) := by
  unfold fibonacci
  split_ifs with h
  · have : k = 0 := by omega
    subst this
    simp only [Int.toNat_zero, range_zero, sum_empty]
    decide
  · rfl

theorem fibonacci_succ_sub (k : ℤ) : fibonacci (k + 1) - fibonacci k = fibStep k := by
  rcases le_or_gt 0 k with hk | hk
  · unfold fibonacci
    rw [if_pos (by omega), if_pos hk, show (k + 1).toNat = k.toNat + 1 by omega, sum_range_succ,
      Int.toNat_of_nonneg hk]
    abel
  · rw [fibonacci_nonpos (show k + 1 ≤ 0 by omega), fibonacci_nonpos (show k ≤ 0 by omega),
      show (-k).toNat = (-(k + 1)).toNat + 1 by omega, sum_range_succ]
    have : (-1 - ((-(k + 1)).toNat : ℕ) : ℤ) = k := by omega
    rw [this]
    abel

/-- **The Fibonacci stacking is a close-packed stacking.** -/
theorem fibonacci_isStacking : IsStacking fibonacci := by
  intro k h
  have := fibonacci_succ_sub k
  rw [h, sub_self] at this
  exact fibStep_ne_zero k this.symm

theorem fibonacci_zero : fibonacci 0 = 0 := by simp [fibonacci]

theorem fibonacci_one : fibonacci 1 = 1 := by
  unfold fibonacci
  rw [if_pos (by norm_num), show (1 : ℤ).toNat = 1 from rfl, sum_range_one, Nat.cast_zero, fibStep,
    fibFlip_zero, if_pos (by decide)]

/-- **Jagodzinski's rule.** Layer `k` is hexagonal (its two neighbours are in the
same position) exactly when the Fibonacci letter at `k` is `h`. -/
theorem fibonacci_layer_type (k : ℤ) : fibonacci (k - 1) = fibonacci (k + 1) ↔ IsH k := by
  have h1 := fibonacci_succ_sub k
  have h2 := fibonacci_succ_sub (k - 1)
  rw [sub_add_cancel] at h2
  have e : fibonacci (k + 1) - fibonacci (k - 1) = fibStep k + fibStep (k - 1) := by
    rw [← h1, ← h2]; ring
  rw [eq_comm, ← sub_eq_zero, e]
  unfold IsH fibStep
  rcases fibFlip_step k with h | h
  · rw [h]
    simp only [ne_eq, not_true_eq_false, iff_false]
    split_ifs <;> decide
  · rw [h]
    simp only [ne_eq, add_eq_left, one_ne_zero, not_false_eq_true, iff_true]
    by_cases he : Even (fibFlip (k - 1))
    · rw [if_neg (Int.even_add_one.not.2 (not_not.2 he)), if_pos he]; decide
    · rw [if_pos (Int.even_add_one.2 he), if_neg he]; decide

/-! ## The substitution word, for comparison -/

/-- One application of the Fibonacci substitution `c ↦ ch`, `h ↦ c`
(`false` = c, `true` = h). -/
def fibSubst (w : List Bool) : List Bool := w.flatMap fun b => if b then [false] else [false, true]

/-- The substitution applied `n` times to `c`. -/
def fibWord (n : ℕ) : List Bool := (fibSubst)^[n] [false]

/-- `⌊nα⌋` in integers, via `⌊n√5⌋ = Nat.sqrt (5n²)`. -/
def flipZ (n : ℕ) : ℤ := (3 * (n : ℤ) - (Nat.sqrt (5 * n ^ 2) : ℤ) - 1) / 2

theorem floor_eq_flipZ (n : ℕ) (hn : 1 ≤ n) : ⌊(n : ℝ) * fibAlpha⌋ = flipZ n := by
  set s := Nat.sqrt (5 * n ^ 2) with hs
  have hs1 := Nat.sqrt_le' (5 * n ^ 2)
  have hs2 := Nat.lt_succ_sqrt' (5 * n ^ 2)
  rw [← hs] at hs1 hs2
  have hsq : (n : ℝ) * Real.sqrt 5 = Real.sqrt (5 * (n : ℝ) ^ 2) := by
    rw [Real.sqrt_mul (by norm_num), Real.sqrt_sq (Nat.cast_nonneg n), mul_comm]
  have hlo : (s : ℝ) ≤ n * Real.sqrt 5 := by
    rw [hsq, Real.le_sqrt (Nat.cast_nonneg s) (by positivity)]
    exact_mod_cast hs1
  have hne : (s : ℝ) ≠ n * Real.sqrt 5 := by
    intro h
    apply sqrt5_irrational
    refine ⟨(s : ℚ) / n, ?_⟩
    have hn0 : (n : ℝ) ≠ 0 := by positivity
    push_cast
    rw [h]; field_simp
  have hlo' : (s : ℝ) < n * Real.sqrt 5 := lt_of_le_of_ne hlo hne
  have hhi : n * Real.sqrt 5 < (s : ℝ) + 1 := by
    rw [hsq, Real.sqrt_lt' (by positivity)]
    exact_mod_cast hs2
  rw [Int.floor_eq_iff]
  unfold flipZ fibAlpha
  set t : ℤ := 3 * (n : ℤ) - (s : ℤ) - 1 with ht
  have a1 : 2 * (t / 2) ≤ t := by omega
  have a2 : t ≤ 2 * (t / 2) + 1 := by omega
  have b1 : (2 : ℝ) * ((t / 2 : ℤ) : ℝ) ≤ (t : ℝ) := by exact_mod_cast a1
  have b2 : (t : ℝ) ≤ 2 * ((t / 2 : ℤ) : ℝ) + 1 := by exact_mod_cast a2
  have tt : (t : ℝ) = 3 * n - s - 1 := by rw [ht]; push_cast; ring
  constructor <;> nlinarith

theorem fibFlip_nat (k : ℕ) : fibFlip k = flipZ (k + 2) := by
  rw [← floor_eq_flipZ (k + 2) (by omega), fibFlip]; push_cast; ring_nf

theorem fibFlip_pred_nat (k : ℕ) : fibFlip ((k : ℤ) - 1) = flipZ (k + 1) := by
  rcases k with _ | k
  · rw [show flipZ (0 + 1) = 0 by decide +kernel]
    unfold fibFlip; rw [Int.floor_eq_iff]
    have := fibAlpha_pos; have := fibAlpha_lt_half
    push_cast; constructor <;> nlinarith
  · rw [show ((k + 1 : ℕ) : ℤ) - 1 = (k : ℤ) by push_cast; ring, fibFlip_nat]

/-- The cut-and-project letters agree with the substitution word `c ↦ ch, h ↦ c`
at positions `0, …, 99` (kernel computation). -/
theorem word_check : ∀ k < 100,
    (flipZ (k + 2) ≠ flipZ (k + 1) ↔ (fibWord 10).getD k false = true) := by
  decide +kernel

theorem isH_eq_word (k : ℕ) (hk : k < 100) : IsH k ↔ (fibWord 10).getD k false = true := by
  rw [← word_check k hk, IsH, fibFlip_nat, fibFlip_pred_nat]

/-! ## Aperiodicity -/

/-- **The Fibonacci type word is not periodic** (Morse–Hedlund 1940: a Sturmian
word of irrational slope is aperiodic; here directly from the irrationality
of `α`). -/
theorem isH_not_periodic (p : ℤ) (hp : p ≠ 0) : ¬ ∀ k, (IsH (k + p) ↔ IsH k) := by
  intro hper
  -- the jumps `fibFlip k - fibFlip (k-1) ∈ {0, 1}` are periodic, so `fibFlip (k + p) - fibFlip k` is constant
  have jump : ∀ k, fibFlip (k + p) - fibFlip (k + p - 1) = fibFlip k - fibFlip (k - 1) := by
    intro k
    have h := hper k
    unfold IsH at h
    rcases fibFlip_step (k + p) with h1 | h1 <;> rcases fibFlip_step k with h2 | h2 <;>
      simp only [h1, h2, ne_eq, not_true_eq_false, add_eq_left, one_ne_zero, not_false_eq_true,
        iff_true, iff_false] at h ⊢ <;> omega
  set c := fibFlip p - fibFlip 0 with hc
  have hconst : ∀ k, fibFlip (k + p) = fibFlip k + c := by
    intro k
    induction k using Int.induction_on with
    | zero => rw [zero_add, hc]; ring
    | succ k ih =>
      have := jump (k + 1)
      rw [show (k : ℤ) + 1 + p - 1 = k + p by ring, add_sub_cancel_right] at this
      omega
    | pred k ih =>
      have := jump (-k)
      rw [show -(k : ℤ) + p - 1 = -k - 1 + p by ring] at this
      omega
  have hmul : ∀ n : ℕ, fibFlip (n * p) = n * c := by
    intro n
    induction n with
    | zero => simp [fibFlip_zero]
    | succ n ih =>
      rw [show ((n + 1 : ℕ) : ℤ) * p = n * p + p by push_cast; ring, hconst, ih]; push_cast; ring
  -- so `|n (p α - c)| ≤ 2` for every `n`, hence `p α = c`
  have hbound : ∀ n : ℕ, |(n : ℝ) * (p * fibAlpha - c)| ≤ 2 := by
    intro n
    have h := hmul n
    unfold fibFlip at h
    have f1 := Int.floor_le ((((n * p : ℤ) : ℝ) + 2) * fibAlpha)
    have f2 := Int.lt_floor_add_one ((((n * p : ℤ) : ℝ) + 2) * fibAlpha)
    rw [h] at f1 f2
    push_cast at f1 f2
    have ha := fibAlpha_pos
    have hb := fibAlpha_lt_half
    rw [abs_le]
    constructor <;> nlinarith
  have heq : (p : ℝ) * fibAlpha = c := by
    by_contra hne
    have hpos : 0 < |(p : ℝ) * fibAlpha - c| := abs_pos.2 (sub_ne_zero.2 hne)
    obtain ⟨n, hn⟩ := exists_nat_gt (3 / |(p : ℝ) * fibAlpha - c|)
    have := hbound n
    rw [abs_mul, Nat.abs_cast] at this
    rw [div_lt_iff₀ hpos] at hn
    linarith
  apply sqrt5_irrational
  refine ⟨3 - 2 * (c : ℚ) / p, ?_⟩
  have hp' : (p : ℝ) ≠ 0 := by exact_mod_cast hp
  unfold fibAlpha at heq
  push_cast
  field_simp
  linarith

/-- **The Fibonacci stacking is not periodic.** -/
theorem fibonacci_not_periodic (p : ℤ) (hp : p ≠ 0) : ¬ ∀ k, fibonacci (k + p) = fibonacci k := by
  intro hper
  apply isH_not_periodic p hp
  intro k
  rw [← fibonacci_layer_type, ← fibonacci_layer_type, show k + p - 1 = (k - 1) + p by ring,
    show k + p + 1 = (k + 1) + p by ring, hper, hper]

/-! ## The Loop Equality on the Fibonacci stacking -/

/-- **Corollary (aperiodic case).** At every site of the aperiodic Fibonacci
stacking, the number of closed non-backtracking loops of length `m` equals
diamond's, and equals the explicit `loopCount m` (24, 48, 480, 3432, … for
`m = 6, 8, 10, 12, …`). -/
theorem fibonacci_loop_equality (v : Atom) (hv : IsSite fibonacci v) (m : ℕ) [NeZero m] :
    (nbLoops fibonacci v m).ncard = (nbLoops diamond (0, (0, 0), 0) m).ncard ∧
      ((nbLoops fibonacci v m).ncard : ℤ) = loopCount m :=
  ⟨loop_equality fibonacci fibonacci_isStacking v hv m,
    loop_count_eq fibonacci fibonacci_isStacking v hv m⟩

end LoopEqualityProof
