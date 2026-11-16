module

public import Mathlib
public import YantraCert.ZPoly
public import YantraCert.Sound

@[expose] public section

/-!
# Soundness of the polynomial normaliser and of fraction arithmetic

* `ZP.eval_add`, `ZP.eval_mul`, `ZP.eval_subst`, `ZP.eval_substH`: the operations commute with evaluation.
* `ZP.eq_of_eqv`: a kernel-checked identity `ZP.eqv p q = true` gives `p(x) = q(x)` everywhere.
* `Ex.frac_sound`: if every named quantity `V i` is `N_i / D_i` in the multiplicative sense `V i * D_i(x) = N_i(x)`, then so
  is every expression in them, with the numerator and denominator computed by the kernel.
-/

namespace YantraCert
open Finset

noncomputable def ZP.eval : ZP → ℝ → ℝ → ℝ → ℝ
  | .nil, _, _, _ => 0
  | .cons c a b e t, x, y, z => (c : ℝ) * x ^ a * y ^ b * z ^ e + t.eval x y z

@[simp] lemma ZP.eval_nil (x y z : ℝ) : ZP.nil.eval x y z = 0 := rfl
@[simp] lemma ZP.eval_cons (c : Int) (a b e : Nat) (t : ZP) (x y z : ℝ) :
    (ZP.cons c a b e t).eval x y z = (c : ℝ) * x ^ a * y ^ b * z ^ e + t.eval x y z := rfl

lemma ZP.eval_app (p q : ZP) (x y z : ℝ) : (ZP.app p q).eval x y z = p.eval x y z + q.eval x y z := by
  induction p with
  | nil => simp [ZP.app]
  | cons c a b e t ih =>
    show (ZP.cons c a b e (ZP.app t q)).eval x y z = _
    rw [ZP.eval_cons, ih, ZP.eval_cons]; ring

lemma mlt_meq {a b e a' b' e' : Nat} (h : meq a b e a' b' e' = true) : a = a' ∧ b = b' ∧ e = e' := by
  unfold meq at h; simp only [Bool.and_eq_true, Nat.beq_eq] at h; exact ⟨h.1.1, h.1.2, h.2⟩

lemma ZP.eval_ins (c : Int) (a b e : Nat) (f : ZP → ZP) (K : ℝ) (x y z : ℝ)
    (hf : ∀ q, (f q).eval x y z = K + q.eval x y z) :
    ∀ q, (ZP.ins c a b e f q).eval x y z = (c : ℝ) * x ^ a * y ^ b * z ^ e + K + q.eval x y z := by
  intro q
  induction q with
  | nil =>
    show (cond (c == 0) (f .nil) (.cons c a b e (f .nil))).eval x y z = _
    cases hc : (c == 0)
    · simp only [cond, ZP.eval_cons, hf, ZP.eval_nil]; ring
    · have : c = 0 := by simpa using hc
      simp only [cond, hf, this, ZP.eval_nil]; push_cast; ring
  | cons c' a' b' e' q' ih =>
    show (cond (mlt a' b' e' a b e) (.cons c' a' b' e' (ZP.ins c a b e f q'))
        (cond (meq a b e a' b' e')
          (cond (c + c' == 0) (f q') (.cons (c + c') a b e (f q')))
          (cond (c == 0) (f (.cons c' a' b' e' q')) (.cons c a b e (f (.cons c' a' b' e' q')))))).eval x y z = _
    cases h1 : mlt a' b' e' a b e
    · cases h2 : meq a b e a' b' e'
      · cases hc : (c == 0)
        · simp only [cond, ZP.eval_cons, hf]; ring
        · have : c = 0 := by simpa using hc
          simp only [cond, hf, ZP.eval_cons, this]; push_cast; ring
      · obtain ⟨ha, hb, he⟩ := mlt_meq h2
        subst ha hb he
        cases hc : (c + c' == 0)
        · simp only [cond, ZP.eval_cons, hf]; push_cast; ring
        · have : c + c' = 0 := by simpa using hc
          have : (c : ℝ) + c' = 0 := by exact_mod_cast this
          simp only [cond, hf, ZP.eval_cons]; linear_combination (-(x ^ a * y ^ b * z ^ e)) * this
    · simp only [cond, ZP.eval_cons, ih]; ring

lemma ZP.eval_add (p q : ZP) (x y z : ℝ) : (ZP.add p q).eval x y z = p.eval x y z + q.eval x y z := by
  induction p generalizing q with
  | nil => simp [ZP.add]
  | cons c a b e t ih =>
    show (ZP.ins c a b e (fun q => ZP.add t q) q).eval x y z = _
    rw [ZP.eval_ins c a b e _ (t.eval x y z) x y z (fun q => ih q), ZP.eval_cons]

lemma ZP.eval_neg (p : ZP) (x y z : ℝ) : (ZP.neg p).eval x y z = -p.eval x y z := by
  induction p with
  | nil => simp [ZP.neg]
  | cons c a b e t ih =>
    show (ZP.cons (-c) a b e (ZP.neg t)).eval x y z = _
    rw [ZP.eval_cons, ih, ZP.eval_cons]; push_cast; ring

lemma ZP.eval_sub (p q : ZP) (x y z : ℝ) : (ZP.sub p q).eval x y z = p.eval x y z - q.eval x y z := by
  unfold ZP.sub; rw [ZP.eval_add, ZP.eval_neg]; ring

lemma ZP.eval_scale (c : Int) (a b e : Nat) (q : ZP) (x y z : ℝ) :
    (ZP.scale c a b e q).eval x y z = (c : ℝ) * x ^ a * y ^ b * z ^ e * q.eval x y z := by
  induction q with
  | nil => simp [ZP.scale]
  | cons c' a' b' e' t ih =>
    show (ZP.cons (c * c') (a + a') (b + b') (e + e') (ZP.scale c a b e t)).eval x y z = _
    rw [ZP.eval_cons, ih, ZP.eval_cons]; push_cast; ring

lemma ZP.eval_mul (p q : ZP) (x y z : ℝ) : (ZP.mul p q).eval x y z = p.eval x y z * q.eval x y z := by
  induction p with
  | nil => simp [ZP.mul]
  | cons c a b e t ih =>
    show (ZP.add (ZP.scale c a b e q) (ZP.mul t q)).eval x y z = _
    rw [ZP.eval_add, ZP.eval_scale, ih, ZP.eval_cons]; ring

@[simp] lemma ZP.eval_one (x y z : ℝ) : ZP.one.eval x y z = 1 := by simp [ZP.one]
@[simp] lemma ZP.eval_const (c : Int) (x y z : ℝ) : (ZP.const c).eval x y z = c := by simp [ZP.const]

lemma ZP.eval_pow (p : ZP) (n : Nat) (x y z : ℝ) : (ZP.pow p n).eval x y z = p.eval x y z ^ n := by
  induction n with
  | zero => show ZP.one.eval x y z = _; simp
  | succ n ih => show (ZP.mul (ZP.pow p n) p).eval x y z = _; rw [ZP.eval_mul, ih, pow_succ]

lemma ZP.eval_subst (X Y Z p : ZP) (x y z : ℝ) :
    (ZP.subst X Y Z p).eval x y z = p.eval (X.eval x y z) (Y.eval x y z) (Z.eval x y z) := by
  induction p with
  | nil => simp [ZP.subst]
  | cons c a b e t ih =>
    show (ZP.add (ZP.mul (ZP.const c) (ZP.mul (ZP.mul (ZP.pow X a) (ZP.pow Y b)) (ZP.pow Z e))) (ZP.subst X Y Z t)).eval x y z = _
    rw [ZP.eval_add, ZP.eval_mul, ZP.eval_mul, ZP.eval_mul, ZP.eval_pow, ZP.eval_pow, ZP.eval_pow, ih, ZP.eval_const,
      ZP.eval_cons]; ring

lemma ZP.zdeg_cons {d c a b e} {t : ZP} : (ZP.cons c a b e t).zdeg d = true ↔ e ≤ d ∧ t.zdeg d = true := by
  show (Nat.ble e d && t.zdeg d) = true ↔ _
  simp [Bool.and_eq_true, Nat.ble_eq]

lemma ZP.eval_substH (X Y Zn Zd p : ZP) (d : Nat) (hd : p.zdeg d = true) (x y z : ℝ) (h0 : Zd.eval x y z ≠ 0) :
    (ZP.substH X Y Zn Zd d p).eval x y z =
      p.eval (X.eval x y z) (Y.eval x y z) (Zn.eval x y z / Zd.eval x y z) * Zd.eval x y z ^ d := by
  induction p with
  | nil => simp [ZP.substH]
  | cons c a b e t ih =>
    obtain ⟨he, ht⟩ := ZP.zdeg_cons.mp hd
    show (ZP.add (ZP.mul (ZP.const c)
      (ZP.mul (ZP.mul (ZP.mul (ZP.pow X a) (ZP.pow Y b)) (ZP.pow Zn e)) (ZP.pow Zd (d - e)))) (ZP.substH X Y Zn Zd d t)).eval x y z = _
    rw [ZP.eval_add, ZP.eval_mul, ZP.eval_mul, ZP.eval_mul, ZP.eval_mul, ZP.eval_pow, ZP.eval_pow, ZP.eval_pow, ZP.eval_pow,
      ih ht, ZP.eval_const, ZP.eval_cons]
    have : Zd.eval x y z ^ d = Zd.eval x y z ^ e * Zd.eval x y z ^ (d - e) := by rw [← pow_add, Nat.add_sub_cancel' he]
    rw [this, div_pow]; field_simp

lemma ZP.isNil_eval {p : ZP} (h : p.isNil = true) (x y z : ℝ) : p.eval x y z = 0 := by
  cases p with
  | nil => rfl
  | cons c a b e t => exact absurd h (by simp [ZP.isNil])

/-- **a kernel-checked identity holds everywhere** -/
theorem ZP.eq_of_eqv {p q : ZP} (h : ZP.eqv p q = true) (x y z : ℝ) : p.eval x y z = q.eval x y z := by
  have := ZP.isNil_eval h x y z
  rw [ZP.eval_sub] at this; linarith

lemma ZP.eval_prod (l : List ZP) (x y z : ℝ) : (ZP.prod l).eval x y z = (l.map fun p => p.eval x y z).prod := by
  induction l with
  | nil => show ZP.one.eval x y z = _; simp
  | cons p l ih => show (ZP.mul p (ZP.prod l)).eval x y z = _; rw [ZP.eval_mul, ih]; simp

lemma ZP.allPos_cons {c a b e} {t : ZP} : (ZP.cons c a b e t).allPos = true ↔ 0 < c ∧ t.allPos = true := by
  show (decide (0 < c) && t.allPos) = true ↔ _
  simp [Bool.and_eq_true]

/-- a polynomial with positive coefficients is nonnegative at a nonnegative point -/
lemma ZP.allPos_nonneg {p : ZP} (h : p.allPos = true) {x y z : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (hz : 0 ≤ z) :
    0 ≤ p.eval x y z := by
  induction p with
  | nil => simp
  | cons c a b e t ih =>
    obtain ⟨hc, ht⟩ := ZP.allPos_cons.mp h
    have hc' : (0 : ℝ) ≤ c := by exact_mod_cast hc.le
    rw [ZP.eval_cons]; have := ih ht; positivity

/-- ... and positive at a positive point, if it is not empty -/
lemma ZP.allPos_pos {c a b e} {t : ZP} (h : (ZP.cons c a b e t).allPos = true) {x y z : ℝ} (hx : 0 < x) (hy : 0 < y)
    (hz : 0 < z) : 0 < (ZP.cons c a b e t).eval x y z := by
  obtain ⟨hc, ht⟩ := ZP.allPos_cons.mp h
  have hc' : (0 : ℝ) < c := by exact_mod_cast hc
  rw [ZP.eval_cons]; have := ZP.allPos_nonneg ht hx.le hy.le hz.le; positivity

end YantraCert
