import YantraCert.ZPolySound
import YantraCert.Krawczyk

/-!
# Named quantities as fractions of polynomials (the divisor lemma, mechanised)

A construction defines real quantities `V i` one after another, each by a relation `V i * d = n` with `d ≠ 0`, where `d` and
`n` are expressions in earlier quantities. `Inv T V x i` says that `V i = N_i(x) / D_i(x)` with `D_i(x) ≠ 0`, for the stored
pair `(N_i, D_i) = T[i]` of polynomials in the base point `x = (x₀, x₁, x₂)`.

* `frac_sound`: an expression in quantities that satisfy `Inv` equals the kernel-computed fraction.
* `step_inv`: a new quantity satisfies `Inv` once two kernel-checked identities hold: `D_i K = A` and `N_i K = B`, where
  `A / B` is the unreduced fraction of `n / d` and `K` is the cancelled common factor. `K(x) ≠ 0` is not assumed: it follows
  from `A(x) ≠ 0`, which holds because `d ≠ 0` and every earlier denominator is nonzero. This is the divisor lemma of
  studies/2026-11-15-yantra-uniqueness (s1_system.py), made mechanical.
* `num_zero`: an expression that vanishes has a vanishing numerator.
-/

namespace YantraCert
open Finset

/-- real value of an expression -/
noncomputable def Ex.ev (V : Nat → ℝ) : Ex → ℝ
  | .v i => V i
  | .c z => (z : ℝ)
  | .add a b => a.ev V + b.ev V
  | .sub a b => a.ev V - b.ev V
  | .mul a b => a.ev V * b.ev V

/-- `V i` is the stored fraction at the point, with nonzero denominator -/
def Inv (T : List (ZP × ZP)) (V : Nat → ℝ) (x y z : ℝ) (i : Nat) : Prop :=
  V i * (nth (ZP.nil, ZP.one) T i).2.eval x y z = (nth (ZP.nil, ZP.one) T i).1.eval x y z ∧
    (nth (ZP.nil, ZP.one) T i).2.eval x y z ≠ 0

lemma Ex.within_add {n a b} : (Ex.add a b).within n = true ↔ a.within n = true ∧ b.within n = true := by
  show (a.within n && b.within n) = true ↔ _; simp
lemma Ex.within_sub {n a b} : (Ex.sub a b).within n = true ↔ a.within n = true ∧ b.within n = true := by
  show (a.within n && b.within n) = true ↔ _; simp
lemma Ex.within_mul {n a b} : (Ex.mul a b).within n = true ↔ a.within n = true ∧ b.within n = true := by
  show (a.within n && b.within n) = true ↔ _; simp

/-- **fractions of expressions are sound** -/
theorem frac_sound (T : List (ZP × ZP)) (V : Nat → ℝ) (x y z : ℝ) (n : Nat) (hI : ∀ i < n, Inv T V x y z i) :
    ∀ e : Ex, e.within n = true →
      e.ev V * (Ex.frac T e).2.eval x y z = (Ex.frac T e).1.eval x y z ∧ (Ex.frac T e).2.eval x y z ≠ 0 := by
  intro e
  induction e with
  | v i =>
    intro h
    have hi : i < n := by simpa [Ex.within] using h
    exact hI i hi
  | c z => intro _; simp [Ex.frac, Ex.ev]
  | add a b iha ihb =>
    intro h
    obtain ⟨ha, hb⟩ := Ex.within_add.mp h
    obtain ⟨a1, a2⟩ := iha ha
    obtain ⟨b1, b2⟩ := ihb hb
    show (a.ev V + b.ev V) * (cond (ZP.eqv (Ex.frac T a).2 (Ex.frac T b).2) (ZP.add (Ex.frac T a).1 (Ex.frac T b).1, (Ex.frac T a).2)
        (ZP.add (ZP.mul (Ex.frac T a).1 (Ex.frac T b).2) (ZP.mul (Ex.frac T b).1 (Ex.frac T a).2),
          ZP.mul (Ex.frac T a).2 (Ex.frac T b).2)).2.eval x y z =
      (cond (ZP.eqv (Ex.frac T a).2 (Ex.frac T b).2) (ZP.add (Ex.frac T a).1 (Ex.frac T b).1, (Ex.frac T a).2)
        (ZP.add (ZP.mul (Ex.frac T a).1 (Ex.frac T b).2) (ZP.mul (Ex.frac T b).1 (Ex.frac T a).2),
          ZP.mul (Ex.frac T a).2 (Ex.frac T b).2)).1.eval x y z ∧
      (cond (ZP.eqv (Ex.frac T a).2 (Ex.frac T b).2) (ZP.add (Ex.frac T a).1 (Ex.frac T b).1, (Ex.frac T a).2)
        (ZP.add (ZP.mul (Ex.frac T a).1 (Ex.frac T b).2) (ZP.mul (Ex.frac T b).1 (Ex.frac T a).2),
          ZP.mul (Ex.frac T a).2 (Ex.frac T b).2)).2.eval x y z ≠ 0
    cases he : ZP.eqv (Ex.frac T a).2 (Ex.frac T b).2
    · simp only [cond]
      rw [ZP.eval_add, ZP.eval_mul, ZP.eval_mul, ZP.eval_mul, ← a1, ← b1]
      exact ⟨by ring, mul_ne_zero a2 b2⟩
    · simp only [cond]
      have hd := ZP.eq_of_eqv he x y z
      rw [ZP.eval_add, ← a1, ← b1, hd]
      exact ⟨by ring, by rw [← hd]; exact a2⟩
  | sub a b iha ihb =>
    intro h
    obtain ⟨ha, hb⟩ := Ex.within_sub.mp h
    obtain ⟨a1, a2⟩ := iha ha
    obtain ⟨b1, b2⟩ := ihb hb
    show (a.ev V - b.ev V) * (cond (ZP.eqv (Ex.frac T a).2 (Ex.frac T b).2) (ZP.sub (Ex.frac T a).1 (Ex.frac T b).1, (Ex.frac T a).2)
        (ZP.sub (ZP.mul (Ex.frac T a).1 (Ex.frac T b).2) (ZP.mul (Ex.frac T b).1 (Ex.frac T a).2),
          ZP.mul (Ex.frac T a).2 (Ex.frac T b).2)).2.eval x y z =
      (cond (ZP.eqv (Ex.frac T a).2 (Ex.frac T b).2) (ZP.sub (Ex.frac T a).1 (Ex.frac T b).1, (Ex.frac T a).2)
        (ZP.sub (ZP.mul (Ex.frac T a).1 (Ex.frac T b).2) (ZP.mul (Ex.frac T b).1 (Ex.frac T a).2),
          ZP.mul (Ex.frac T a).2 (Ex.frac T b).2)).1.eval x y z ∧
      (cond (ZP.eqv (Ex.frac T a).2 (Ex.frac T b).2) (ZP.sub (Ex.frac T a).1 (Ex.frac T b).1, (Ex.frac T a).2)
        (ZP.sub (ZP.mul (Ex.frac T a).1 (Ex.frac T b).2) (ZP.mul (Ex.frac T b).1 (Ex.frac T a).2),
          ZP.mul (Ex.frac T a).2 (Ex.frac T b).2)).2.eval x y z ≠ 0
    cases he : ZP.eqv (Ex.frac T a).2 (Ex.frac T b).2
    · simp only [cond]
      rw [ZP.eval_sub, ZP.eval_mul, ZP.eval_mul, ZP.eval_mul, ← a1, ← b1]
      exact ⟨by ring, mul_ne_zero a2 b2⟩
    · simp only [cond]
      have hd := ZP.eq_of_eqv he x y z
      rw [ZP.eval_sub, ← a1, ← b1, hd]
      exact ⟨by ring, by rw [← hd]; exact a2⟩
  | mul a b iha ihb =>
    intro h
    obtain ⟨ha, hb⟩ := Ex.within_mul.mp h
    obtain ⟨a1, a2⟩ := iha ha
    obtain ⟨b1, b2⟩ := ihb hb
    show (a.ev V * b.ev V) * (ZP.mul (Ex.frac T a).2 (Ex.frac T b).2).eval x y z =
        (ZP.mul (Ex.frac T a).1 (Ex.frac T b).1).eval x y z ∧ (ZP.mul (Ex.frac T a).2 (Ex.frac T b).2).eval x y z ≠ 0
    rw [ZP.eval_mul, ZP.eval_mul, ← a1, ← b1]
    exact ⟨by ring, mul_ne_zero a2 b2⟩

/-- **one step of the construction** -/
theorem step_inv (T : List (ZP × ZP)) (V : Nat → ℝ) (x y z : ℝ) (i : Nat) (d n : Ex) (K : ZP)
    (hok : stepOK T i d n K = true) (hI : ∀ j < i, Inv T V x y z j)
    (hq : V i * d.ev V = n.ev V) (hd : d.ev V ≠ 0) : Inv T V x y z i := by
  unfold stepOK at hok
  simp only [Bool.and_eq_true] at hok
  obtain ⟨⟨⟨hbd, hbn⟩, h1⟩, h2⟩ := hok
  obtain ⟨d1, d2⟩ := frac_sound T V x y z i hI d hbd
  obtain ⟨n1, n2⟩ := frac_sound T V x y z i hI n hbn
  have e1 := ZP.eq_of_eqv h1 x y z
  have e2 := ZP.eq_of_eqv h2 x y z
  rw [ZP.eval_mul, ZP.eval_mul] at e1 e2
  set Dq := (nth (ZP.nil, ZP.one) T i).2.eval x y z
  set Nq := (nth (ZP.nil, ZP.one) T i).1.eval x y z
  set k := K.eval x y z
  have hA : (Ex.frac T d).1.eval x y z * (Ex.frac T n).2.eval x y z ≠ 0 := by
    rw [← d1]; exact mul_ne_zero (mul_ne_zero hd d2) n2
  have hk : k ≠ 0 := by intro h0; rw [h0, mul_zero] at e1; exact hA e1.symm
  have hD : Dq ≠ 0 := by intro h0; rw [h0, zero_mul] at e1; exact hA e1.symm
  refine ⟨?_, hD⟩
  -- V i * A = B, then cancel k
  have hB : V i * ((Ex.frac T d).1.eval x y z * (Ex.frac T n).2.eval x y z) =
      (Ex.frac T n).1.eval x y z * (Ex.frac T d).2.eval x y z := by
    rw [← d1, ← n1, ← hq]; ring
  rw [← e1, ← e2] at hB
  have : (V i * Dq - Nq) * k = 0 := by linear_combination hB
  rcases mul_eq_zero.mp this with h | h
  · linarith
  · exact absurd h hk

/-- **a vanishing expression has a vanishing numerator** -/
theorem num_zero (T : List (ZP × ZP)) (V : Nat → ℝ) (x y z : ℝ) (n : Nat) (hI : ∀ i < n, Inv T V x y z i) (e : Ex)
    (hb : e.within n = true) (h0 : e.ev V = 0) : (Ex.frac T e).1.eval x y z = 0 := by
  obtain ⟨h1, _⟩ := frac_sound T V x y z n hI e hb
  rw [← h1, h0, zero_mul]

/-- **and conversely**, a vanishing numerator makes the expression vanish -/
theorem zero_of_num (T : List (ZP × ZP)) (V : Nat → ℝ) (x y z : ℝ) (n : Nat) (hI : ∀ i < n, Inv T V x y z i) (e : Ex)
    (hb : e.within n = true) (h0 : (Ex.frac T e).1.eval x y z = 0) : e.ev V = 0 := by
  obtain ⟨h1, h2⟩ := frac_sound T V x y z n hI e hb
  rw [h0] at h1
  rcases mul_eq_zero.mp h1 with h | h
  · exact h
  · exact absurd h h2

/-- the base quantities `x, y, z` themselves -/
lemma inv_base (T : List (ZP × ZP)) (V : Nat → ℝ) (x y z : ℝ) (i : Nat) (N : ZP) (hT : nth (ZP.nil, ZP.one) T i = (N, ZP.one))
    (hV : V i = N.eval x y z) : Inv T V x y z i := by
  unfold Inv; rw [hT]; simp [hV]

/-! ## Signed polynomials from integer polynomials, and signs on a box -/

lemma ZP.posNP_negNP_eval (p : ZP) (x y z : ℝ) : p.eval x y z = p.posNP.eval x y z - p.negNP.eval x y z := by
  induction p with
  | nil => simp [ZP.posNP, ZP.negNP, NP.eval]
  | cons c a b e t ih =>
    show _ = (cond (decide (0 < c)) (NP.cons c.toNat a b e t.posNP) t.posNP).eval x y z -
      (cond (decide (c < 0)) (NP.cons (-c).toNat a b e t.negNP) t.negNP).eval x y z
    rcases lt_trichotomy c 0 with h | h | h
    · have h1 : decide (0 < c) = false := by simp; omega
      have h2 : decide (c < 0) = true := by simp; omega
      rw [h1, h2]; simp only [cond, NP.eval, ZP.eval_cons, ih]
      have : ((-c).toNat : ℝ) = -(c : ℝ) := by
        have : ((-c).toNat : Int) = -c := Int.toNat_of_nonneg (by omega)
        exact_mod_cast this
      rw [this]; ring
    · subst h; simp [cond, ZP.eval_cons, ih]
    · have h1 : decide (0 < c) = true := by simp; omega
      have h2 : decide (c < 0) = false := by simp; omega
      rw [h1, h2]; simp only [cond, NP.eval, ZP.eval_cons, ih]
      have : (c.toNat : ℝ) = (c : ℝ) := by
        have : (c.toNat : Int) = c := Int.toNat_of_nonneg (by omega)
        exact_mod_cast this
      rw [this]; ring

lemma ZP.toSP_eval (Dx Dy Dz : Nat) (p : ZP) (x y z : ℝ) : (p.toSP Dx Dy Dz).eval x y z = p.eval x y z := by
  rw [ZP.posNP_negNP_eval]; rfl

/-- sign code of a signed polynomial on the box `[L/Q, H/Q]` (nonnegative coordinates) by the monotone split -/
noncomputable def SP.boxSign (p : SP) (Q : Nat) (L H : Fin 3 → Nat) : Nat :=
  cond (Nat.blt (p.pn.vq p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2)) (p.pp.vq p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2))) 1
    (cond (Nat.blt (p.pp.vq p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2)) (p.pn.vq p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2))) 2 0)

theorem SP.boxSign_sound (p : SP) (hd : p.degOK = true) (Q : Nat) (hQ : 0 < Q) (L H : Fin 3 → Nat) (x : Fin 3 → ℝ)
    (hx : ∀ j, (L j : ℝ) / Q ≤ x j ∧ x j ≤ (H j : ℝ) / Q) :
    (p.boxSign Q L H = 1 → 0 < p.eval (x 0) (x 1) (x 2)) ∧ (p.boxSign Q L H = 2 → p.eval (x 0) (x 1) (x 2) < 0) := by
  have hdp : p.pp.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.1
  have hdn : p.pn.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.2
  have q0 : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hs : (0 : ℝ) < (Q : ℝ) ^ p.Dx * (Q : ℝ) ^ p.Dy * (Q : ℝ) ^ p.Dz := by positivity
  have l0 : ∀ j, (0 : ℝ) ≤ (L j : ℝ) / Q := fun j => by positivity
  have mLp := NP.eval_mono p.pp (l0 0) (l0 1) (l0 2) (hx 0).1 (hx 1).1 (hx 2).1
  have mLn := NP.eval_mono p.pn (l0 0) (l0 1) (l0 2) (hx 0).1 (hx 1).1 (hx 2).1
  have mHp := NP.eval_mono p.pp ((l0 0).trans (hx 0).1) ((l0 1).trans (hx 1).1) ((l0 2).trans (hx 2).1) (hx 0).2 (hx 1).2 (hx 2).2
  have mHn := NP.eval_mono p.pn ((l0 0).trans (hx 0).1) ((l0 1).trans (hx 1).1) ((l0 2).trans (hx 2).1) (hx 0).2 (hx 1).2 (hx 2).2
  have cLp := NP.vq_cast p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2) p.pp hdp hQ
  have cLn := NP.vq_cast p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2) p.pn hdn hQ
  have cHp := NP.vq_cast p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2) p.pp hdp hQ
  have cHn := NP.vq_cast p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2) p.pn hdn hQ
  unfold SP.boxSign SP.eval
  constructor
  · intro h
    cases hb : Nat.blt (p.pn.vq p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2)) (p.pp.vq p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2))
    · rw [hb] at h
      cases hb2 : Nat.blt (p.pp.vq p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2)) (p.pn.vq p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2)) <;>
        rw [hb2] at h <;> simp at h
    · rw [Nat.blt_eq] at hb
      have hb' : ((p.pn.vq p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2) : Nat) : ℝ) < (p.pp.vq p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2) : Nat) := by
        exact_mod_cast hb
      rw [cHn, cLp] at hb'
      have := lt_of_mul_lt_mul_right hb' hs.le
      linarith
  · intro h
    cases hb : Nat.blt (p.pn.vq p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2)) (p.pp.vq p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2))
    · rw [hb] at h
      cases hb2 : Nat.blt (p.pp.vq p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2)) (p.pn.vq p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2))
      · rw [hb2] at h; simp at h
      · rw [Nat.blt_eq] at hb2
        have hb' : ((p.pp.vq p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2) : Nat) : ℝ) < (p.pn.vq p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2) : Nat) := by
          exact_mod_cast hb2
        rw [cHp, cLn] at hb'
        have := lt_of_mul_lt_mul_right hb' hs.le
        linarith
    · rw [hb] at h; simp at h

end YantraCert
