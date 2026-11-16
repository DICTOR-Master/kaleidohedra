module

public import YantraCert.ZPoly2
public import YantraCert.ZPolySound
public import YantraCert.Frac

@[expose] public section

namespace YantraCert

lemma ZP.eval_ofNP (neg : Bool) (p : NP) (x y z : ℝ) :
    (ZP.ofNP neg p).eval x y z = cond neg (-p.eval x y z) (p.eval x y z) := by
  induction p with
  | nil => cases neg <;> simp [ZP.ofNP, NP.eval]
  | cons c a b e t ih =>
    show (ZP.cons (cond neg (-(c : Int)) (c : Int)) a b e (ZP.ofNP neg t)).eval x y z = _
    rw [ZP.eval_cons, ih]; cases neg <;> simp [NP.eval] <;> ring

lemma ZP.eval_norm (p : ZP) (x y z : ℝ) : (ZP.norm p).eval x y z = p.eval x y z := by
  induction p with
  | nil => rfl
  | cons c a b e t ih =>
    show (ZP.add (.cons c a b e .nil) (ZP.norm t)).eval x y z = _
    rw [ZP.eval_add, ih]; simp

lemma ZP.eval_ofSP (p : SP) (x y z : ℝ) : (ZP.ofSP p).eval x y z = p.eval x y z := by
  unfold ZP.ofSP SP.eval
  rw [ZP.eval_add, ZP.eval_norm, ZP.eval_norm, ZP.eval_ofNP, ZP.eval_ofNP]; simp; ring

lemma ZP.degLE_cons {D0 D1 D2 c a b e} {t : ZP} :
    (ZP.cons c a b e t).degLE D0 D1 D2 = true ↔ a ≤ D0 ∧ b ≤ D1 ∧ e ≤ D2 ∧ t.degLE D0 D1 D2 = true := by
  show (Nat.ble a D0 && Nat.ble b D1 && Nat.ble e D2 && t.degLE D0 D1 D2) = true ↔ _
  simp [Bool.and_eq_true, Nat.ble_eq, and_assoc]

lemma pow_scale (n d D a : Nat) (h : a ≤ D) (hd : 0 < d) (x : ℝ) :
    ((n ^ a * d ^ (D - a) : Nat) : ℝ) * x ^ a = (d : ℝ) ^ D * ((n : ℝ) * x / d) ^ a := by
  have hd' : (d : ℝ) ≠ 0 := by exact_mod_cast hd.ne'
  push_cast
  have : (d : ℝ) ^ D = (d : ℝ) ^ a * (d : ℝ) ^ (D - a) := by rw [← pow_add, Nat.add_sub_cancel' h]
  rw [this, div_pow, mul_pow]; field_simp

lemma ZP.eval_scaleW (n0 d0 D0 n1 d1 D1 n2 d2 D2 : Nat) (h0 : 0 < d0) (h1 : 0 < d1) (h2 : 0 < d2) (p : ZP)
    (hp : p.degLE D0 D1 D2 = true) (x y z : ℝ) :
    (ZP.scaleW n0 d0 D0 n1 d1 D1 n2 d2 D2 p).eval x y z =
      (d0 : ℝ) ^ D0 * (d1 : ℝ) ^ D1 * (d2 : ℝ) ^ D2 * p.eval (n0 * x / d0) (n1 * y / d1) (n2 * z / d2) := by
  induction p with
  | nil => simp [ZP.scaleW]
  | cons c a b e t ih =>
    obtain ⟨ha, hb, he, ht⟩ := ZP.degLE_cons.mp hp
    show (ZP.cons (c * ((n0 ^ a * d0 ^ (D0 - a) * (n1 ^ b * d1 ^ (D1 - b)) * (n2 ^ e * d2 ^ (D2 - e)) : Nat) : Int)) a b e
      (ZP.scaleW n0 d0 D0 n1 d1 D1 n2 d2 D2 t)).eval x y z = _
    rw [ZP.eval_cons, ih ht, ZP.eval_cons]
    have e1 := pow_scale n0 d0 D0 a ha h0 x
    have e2 := pow_scale n1 d1 D1 b hb h1 y
    have e3 := pow_scale n2 d2 D2 e he h2 z
    push_cast at e1 e2 e3 ⊢
    linear_combination (c : ℝ) * (y ^ b * z ^ e * ((n1 : ℝ) ^ b * (d1 : ℝ) ^ (D1 - b)) * ((n2 : ℝ) ^ e * (d2 : ℝ) ^ (D2 - e))) * e1 +
      (c : ℝ) * ((d0 : ℝ) ^ D0 * ((n0 : ℝ) * x / d0) ^ a) * z ^ e * ((n2 : ℝ) ^ e * (d2 : ℝ) ^ (D2 - e)) * e2 +
      (c : ℝ) * ((d0 : ℝ) ^ D0 * ((n0 : ℝ) * x / d0) ^ a) * ((d1 : ℝ) ^ D1 * ((n1 : ℝ) * y / d1) ^ b) * e3

end YantraCert
