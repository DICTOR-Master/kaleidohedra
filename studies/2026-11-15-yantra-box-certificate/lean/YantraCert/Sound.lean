import Mathlib
import YantraCert.Check

/-!
# Soundness of the box checks

* `SP.signMono_sound`: the monotone split (R. E. Moore, *Interval Analysis*, 1966, natural interval extension in the form
  `p = p⁺ - p⁻` on a box of nonnegative coordinates).
* `SP.signSlope_sound`: the slope form (R. Krawczyk and A. Neumaier, *SIAM J. Numer. Anal.* 22, 1985), through the identity
  `(Σ_{i<n} x^i m^(n-1-i)) (x - m) = x^n - m^n` (Mathlib `geom_sum₂_mul`).
* `go_sound`: a bisection tree whose leaves pass covers its cell.
-/

namespace YantraCert
open Finset

/-! ## Real semantics -/

/-- real value of a polynomial with natural coefficients -/
noncomputable def NP.eval : NP → ℝ → ℝ → ℝ → ℝ
  | .nil, _, _, _ => 0
  | .cons c a b e t, x, y, z => (c : ℝ) * x ^ a * y ^ b * z ^ e + t.eval x y z

/-- real value of a signed polynomial -/
noncomputable def SP.eval (p : SP) (x y z : ℝ) : ℝ := p.pp.eval x y z - p.pn.eval x y z

/-- the closed cell -/
def Cell.Mem (c : Cell) (x y z : ℝ) : Prop :=
  (c.ix : ℝ) / 2 ^ c.dx ≤ x ∧ x ≤ ((c.ix : ℝ) + 1) / 2 ^ c.dx ∧
  (c.iy : ℝ) / 2 ^ c.dy ≤ y ∧ y ≤ ((c.iy : ℝ) + 1) / 2 ^ c.dy ∧
  (c.iz : ℝ) / 2 ^ c.dz ≤ z ∧ z ≤ ((c.iz : ℝ) + 1) / 2 ^ c.dz

/-- the rational box of a hole (multiplied out, so that it is meaningful for every denominator) -/
def HB.Mem (h : HB) (x y z : ℝ) : Prop :=
  (h.xl : ℝ) ≤ x * h.xlq ∧ x * h.xhq ≤ h.xh ∧ (h.yl : ℝ) ≤ y * h.ylq ∧ y * h.yhq ≤ h.yh ∧
  (h.zl : ℝ) ≤ z * h.zlq ∧ z * h.zhq ≤ h.zh

/-- what a leaf certifies at a point -/
def Chart.Good (C : Chart) (x y z : ℝ) : Prop :=
  (∃ p ∈ C.F, p.eval x y z ≠ 0) ∨ (∃ q ∈ C.T, q.1.eval x y z * q.2.eval x y z < 0) ∨ (∃ h ∈ C.H, h.Mem x y z)

def Chart.Covered (C : Chart) (c : Cell) : Prop := ∀ x y z, c.Mem x y z → C.Good x y z

/-! ## Basic facts -/

lemma NP.ev_nil (fx fy fz : Nat → Nat) : NP.nil.ev fx fy fz = 0 := rfl
lemma NP.ev_cons (fx fy fz : Nat → Nat) (c a b e : Nat) (t : NP) :
    (NP.cons c a b e t).ev fx fy fz = c * (fx a * fy b * fz e) + t.ev fx fy fz := rfl
lemma NP.degLE_cons (Dx Dy Dz c a b e : Nat) (t : NP) :
    (NP.cons c a b e t).degLE Dx Dy Dz = (Nat.ble a Dx && Nat.ble b Dy && Nat.ble e Dz && t.degLE Dx Dy Dz) := rfl

lemma NP.degLE_cons_iff {Dx Dy Dz c a b e : Nat} {t : NP} :
    (NP.cons c a b e t).degLE Dx Dy Dz = true ↔ a ≤ Dx ∧ b ≤ Dy ∧ e ≤ Dz ∧ t.degLE Dx Dy Dz = true := by
  rw [NP.degLE_cons]; simp [Bool.and_eq_true, Nat.ble_eq, and_assoc]

lemma sp_cast (D d n a : Nat) (h : a ≤ D) : ((sp D d n a : Nat) : ℝ) = ((n : ℝ) / 2 ^ d) ^ a * 2 ^ (D * d) := by
  unfold sp
  rw [Nat.shiftLeft_eq]
  push_cast
  have h2 : (2 : ℝ) ^ (D * d) = 2 ^ (a * d) * 2 ^ ((D - a) * d) := by
    rw [← pow_add]; congr 1
    rw [← Nat.add_mul, Nat.add_sub_cancel' h]
  rw [h2, div_pow, ← pow_mul, mul_comm a d]
  field_simp

lemma sp_mono (D d a : Nat) {n n' : Nat} (h : n ≤ n') : sp D d n a ≤ sp D d n' a := by
  unfold sp; rw [Nat.shiftLeft_eq, Nat.shiftLeft_eq]
  exact Nat.mul_le_mul_right _ (Nat.pow_le_pow_left h a)

/-- the scaled evaluation at a grid point is the real value times the scale -/
lemma NP.ev_cast (Dx Dy Dz dx dy dz nx ny nz : Nat) (p : NP) (hd : p.degLE Dx Dy Dz = true) :
    ((p.ev (sp Dx dx nx) (sp Dy dy ny) (sp Dz dz nz) : Nat) : ℝ) =
      p.eval ((nx : ℝ) / 2 ^ dx) ((ny : ℝ) / 2 ^ dy) ((nz : ℝ) / 2 ^ dz) * 2 ^ (Dx * dx + Dy * dy + Dz * dz) := by
  induction p with
  | nil => simp [NP.ev_nil, NP.eval]
  | cons c a b e t ih =>
    obtain ⟨ha, hb, he, ht⟩ := NP.degLE_cons_iff.mp hd
    rw [NP.ev_cons]; push_cast
    rw [sp_cast _ _ _ _ ha, sp_cast _ _ _ _ hb, sp_cast _ _ _ _ he, ih ht, NP.eval, pow_add, pow_add]
    ring

lemma NP.eval_mono (p : NP) {x y z x' y' z' : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (hz : 0 ≤ z)
    (hxx : x ≤ x') (hyy : y ≤ y') (hzz : z ≤ z') : p.eval x y z ≤ p.eval x' y' z' := by
  induction p with
  | nil => simp [NP.eval]
  | cons c a b e t ih =>
    simp only [NP.eval]
    have h1 : x ^ a ≤ x' ^ a := pow_le_pow_left₀ hx hxx a
    have h2 : y ^ b ≤ y' ^ b := pow_le_pow_left₀ hy hyy b
    have h3 : z ^ e ≤ z' ^ e := pow_le_pow_left₀ hz hzz e
    have hc : (0 : ℝ) ≤ c := Nat.cast_nonneg c
    have : (c : ℝ) * x ^ a * y ^ b * z ^ e ≤ c * x' ^ a * y' ^ b * z' ^ e := by
      apply mul_le_mul _ h3 (pow_nonneg hz _)
        (mul_nonneg (mul_nonneg hc (pow_nonneg (hx.trans hxx) _)) (pow_nonneg (hy.trans hyy) _))
      apply mul_le_mul _ h2 (pow_nonneg hy _) (mul_nonneg hc (pow_nonneg (hx.trans hxx) _))
      exact mul_le_mul_of_nonneg_left h1 hc
    linarith

lemma cell_lo_nonneg (d i : Nat) : (0 : ℝ) ≤ (i : ℝ) / 2 ^ d := by positivity

/-! ## Monotone split -/

lemma SP.signMono_sound (p : SP) (hd : p.degOK = true) (c : Cell) (x y z : ℝ) (hc : c.Mem x y z) :
    (p.signMono c = 1 → 0 < p.eval x y z) ∧ (p.signMono c = 2 → p.eval x y z < 0) := by
  obtain ⟨hx1, hx2, hy1, hy2, hz1, hz2⟩ := hc
  have hdp : p.pp.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.1
  have hdn : p.pn.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.2
  have x0 := cell_lo_nonneg c.dx c.ix
  have y0 := cell_lo_nonneg c.dy c.iy
  have z0 := cell_lo_nonneg c.dz c.iz
  have hs : (0 : ℝ) < 2 ^ (p.Dx * c.dx + p.Dy * c.dy + p.Dz * c.dz) := by positivity
  -- the four corner values
  have eLp := NP.ev_cast p.Dx p.Dy p.Dz c.dx c.dy c.dz c.ix c.iy c.iz p.pp hdp
  have eLn := NP.ev_cast p.Dx p.Dy p.Dz c.dx c.dy c.dz c.ix c.iy c.iz p.pn hdn
  have eHp := NP.ev_cast p.Dx p.Dy p.Dz c.dx c.dy c.dz (c.ix + 1) (c.iy + 1) (c.iz + 1) p.pp hdp
  have eHn := NP.ev_cast p.Dx p.Dy p.Dz c.dx c.dy c.dz (c.ix + 1) (c.iy + 1) (c.iz + 1) p.pn hdn
  push_cast at eHp eHn
  have mLp := NP.eval_mono p.pp x0 y0 z0 hx1 hy1 hz1
  have mLn := NP.eval_mono p.pn x0 y0 z0 hx1 hy1 hz1
  have mHp := NP.eval_mono p.pp (x0.trans hx1) (y0.trans hy1) (z0.trans hz1) hx2 hy2 hz2
  have mHn := NP.eval_mono p.pn (x0.trans hx1) (y0.trans hy1) (z0.trans hz1) hx2 hy2 hz2
  unfold SP.signMono SP.eval
  constructor
  · intro h
    cases hb : Nat.blt (p.pn.ev (sp p.Dx c.dx (c.ix + 1)) (sp p.Dy c.dy (c.iy + 1)) (sp p.Dz c.dz (c.iz + 1)))
        (p.pp.ev (sp p.Dx c.dx c.ix) (sp p.Dy c.dy c.iy) (sp p.Dz c.dz c.iz))
    · rw [hb] at h
      cases hb2 : Nat.blt (p.pp.ev (sp p.Dx c.dx (c.ix + 1)) (sp p.Dy c.dy (c.iy + 1)) (sp p.Dz c.dz (c.iz + 1)))
          (p.pn.ev (sp p.Dx c.dx c.ix) (sp p.Dy c.dy c.iy) (sp p.Dz c.dz c.iz)) <;> rw [hb2] at h <;> simp at h
    · rw [Nat.blt_eq] at hb; have hlt := hb
      have hlt' : ((p.pn.ev (sp p.Dx c.dx (c.ix + 1)) (sp p.Dy c.dy (c.iy + 1)) (sp p.Dz c.dz (c.iz + 1)) : Nat) : ℝ) <
          ((p.pp.ev (sp p.Dx c.dx c.ix) (sp p.Dy c.dy c.iy) (sp p.Dz c.dz c.iz) : Nat) : ℝ) := by exact_mod_cast hlt
      rw [eHn, eLp] at hlt'
      have := lt_of_mul_lt_mul_right hlt' hs.le
      linarith
  · intro h
    cases hb : Nat.blt (p.pn.ev (sp p.Dx c.dx (c.ix + 1)) (sp p.Dy c.dy (c.iy + 1)) (sp p.Dz c.dz (c.iz + 1)))
        (p.pp.ev (sp p.Dx c.dx c.ix) (sp p.Dy c.dy c.iy) (sp p.Dz c.dz c.iz))
    · rw [hb] at h
      cases hb2 : Nat.blt (p.pp.ev (sp p.Dx c.dx (c.ix + 1)) (sp p.Dy c.dy (c.iy + 1)) (sp p.Dz c.dz (c.iz + 1)))
          (p.pn.ev (sp p.Dx c.dx c.ix) (sp p.Dy c.dy c.iy) (sp p.Dz c.dz c.iz))
      · rw [hb2] at h; simp at h
      · rw [Nat.blt_eq] at hb2; have hlt := hb2
        have hlt' : ((p.pp.ev (sp p.Dx c.dx (c.ix + 1)) (sp p.Dy c.dy (c.iy + 1)) (sp p.Dz c.dz (c.iz + 1)) : Nat) : ℝ) <
            ((p.pn.ev (sp p.Dx c.dx c.ix) (sp p.Dy c.dy c.iy) (sp p.Dz c.dz c.iz) : Nat) : ℝ) := by exact_mod_cast hlt
        rw [eHp, eLn] at hlt'
        have := lt_of_mul_lt_mul_right hlt' hs.le
        linarith
    · rw [hb] at h; simp at h

/-! ## Slope form -/

/-- `Σ_{i<n} x^i m^(n-1-i)`, so that `gs n x m * (x - m) = x^n - m^n` -/
noncomputable def gs (n : ℕ) (x m : ℝ) : ℝ := ∑ i ∈ range n, x ^ i * m ^ (n - 1 - i)

lemma gs_mul (n : ℕ) (x m : ℝ) : gs n x m * (x - m) = x ^ n - m ^ n := geom_sum₂_mul x m n

lemma gs_nonneg (n : ℕ) {x m : ℝ} (hx : 0 ≤ x) (hm : 0 ≤ m) : 0 ≤ gs n x m :=
  sum_nonneg fun _ _ => mul_nonneg (pow_nonneg hx _) (pow_nonneg hm _)

lemma gs_mono (n : ℕ) {x x' m : ℝ} (hx : 0 ≤ x) (hxx : x ≤ x') (hm : 0 ≤ m) : gs n x m ≤ gs n x' m :=
  sum_le_sum fun i _ => mul_le_mul_of_nonneg_right (pow_le_pow_left₀ hx hxx i) (pow_nonneg hm _)

/-- the three slope parts of a polynomial -/
noncomputable def NP.ax : NP → ℝ → ℝ → ℝ → ℝ → ℝ → ℝ → ℝ
  | .nil, _, _, _, _, _, _ => 0
  | .cons c a b e t, x, y, z, mx, my, mz => (c : ℝ) * gs a x mx * y ^ b * z ^ e + t.ax x y z mx my mz
noncomputable def NP.ay : NP → ℝ → ℝ → ℝ → ℝ → ℝ → ℝ → ℝ
  | .nil, _, _, _, _, _, _ => 0
  | .cons c a b e t, x, y, z, mx, my, mz => (c : ℝ) * mx ^ a * gs b y my * z ^ e + t.ay x y z mx my mz
noncomputable def NP.az : NP → ℝ → ℝ → ℝ → ℝ → ℝ → ℝ → ℝ
  | .nil, _, _, _, _, _, _ => 0
  | .cons c a b e t, x, y, z, mx, my, mz => (c : ℝ) * mx ^ a * my ^ b * gs e z mz + t.az x y z mx my mz

/-- the slope identity `p(y) - p(m) = Σ_j (y_j - m_j) A_j` -/
lemma NP.slope_id (p : NP) (x y z mx my mz : ℝ) :
    p.eval x y z - p.eval mx my mz = (x - mx) * p.ax x y z mx my mz + (y - my) * p.ay x y z mx my mz +
      (z - mz) * p.az x y z mx my mz := by
  induction p with
  | nil => simp [NP.eval, NP.ax, NP.ay, NP.az]
  | cons c a b e t ih =>
    simp only [NP.eval, NP.ax, NP.ay, NP.az]
    have h1 := gs_mul a x mx
    have h2 := gs_mul b y my
    have h3 := gs_mul e z mz
    linear_combination ih - ((c : ℝ) * y ^ b * z ^ e) * h1 - ((c : ℝ) * mx ^ a * z ^ e) * h2 -
      ((c : ℝ) * mx ^ a * my ^ b) * h3

lemma slopeAcc_nil (Dx Dy Dz Ex Ey Ez Lx Ly Lz : Nat) :
    slopeAcc Dx Dy Dz Ex Ey Ez Lx Ly Lz .nil = ⟨0, 0, 0, 0, 0, 0, 0⟩ := rfl
lemma slopeAcc_cons (Dx Dy Dz Ex Ey Ez Lx Ly Lz c a b g : Nat) (t : NP) :
    slopeAcc Dx Dy Dz Ex Ey Ez Lx Ly Lz (.cons c a b g t) =
      (slopeAcc Dx Dy Dz Ex Ey Ez Lx Ly Lz t).add c (sp Dx Ex Lx a) (sp Dx Ex (Lx + 1) a) (sp Dx Ex (Lx + 2) a)
        (sp Dy Ey Ly b) (sp Dy Ey (Ly + 1) b) (sp Dy Ey (Ly + 2) b)
        (sp Dz Ez Lz g) (sp Dz Ez (Lz + 1) g) (sp Dz Ez (Lz + 2) g) := rfl

/-- grid value `(L + k) / 2^E` -/
noncomputable def gv (L E k : Nat) : ℝ := ((L : ℝ) + k) / 2 ^ E

lemma gv_nonneg (L E k : Nat) : 0 ≤ gv L E k := by unfold gv; positivity

lemma sp_gv (D E L a k : Nat) (h : a ≤ D) : ((sp D E (L + k) a : Nat) : ℝ) = gv L E k ^ a * 2 ^ (D * E) := by
  rw [sp_cast D E (L + k) a h]; unfold gv; push_cast; ring

lemma sp_gv0 (D E L a : Nat) (h : a ≤ D) : ((sp D E L a : Nat) : ℝ) = gv L E 0 ^ a * 2 ^ (D * E) := by
  have := sp_gv D E L a 0 h; simpa using this

lemma gv_sub (L E : Nat) : gv L E 2 - gv L E 1 = 1 / 2 ^ E ∧ gv L E 1 - gv L E 0 = 1 / 2 ^ E := by
  unfold gv; constructor <;> (push_cast; field_simp; ring)

lemma sp_sub_hi (D E L a : Nat) (h : a ≤ D) :
    (((sp D E (L + 2) a - sp D E (L + 1) a : Nat)) : ℝ) = gs a (gv L E 2) (gv L E 1) * 2 ^ (D * E) / 2 ^ E := by
  rw [Nat.cast_sub (sp_mono D E a (by omega)), sp_gv D E L a 2 h, sp_gv D E L a 1 h, ← sub_mul,
    ← gs_mul a (gv L E 2) (gv L E 1), (gv_sub L E).1]
  field_simp

lemma sp_sub_lo (D E L a : Nat) (h : a ≤ D) :
    (((sp D E (L + 1) a - sp D E L a : Nat)) : ℝ) = gs a (gv L E 0) (gv L E 1) * 2 ^ (D * E) / 2 ^ E := by
  rw [Nat.cast_sub (sp_mono D E a (by omega)), sp_gv D E L a 1 h, sp_gv0 D E L a h]
  have h2 := gs_mul a (gv L E 0) (gv L E 1)
  have e : gv L E 1 ^ a * 2 ^ (D * E) - gv L E 0 ^ a * 2 ^ (D * E) = -((gv L E 0 ^ a - gv L E 1 ^ a) * 2 ^ (D * E)) := by ring
  have e2 : gv L E 0 - gv L E 1 = -(1 / 2 ^ E) := by linarith [(gv_sub L E).2]
  rw [e, ← h2, e2]
  field_simp

/-- the scale -/
noncomputable def sc (Dx Dy Dz Ex Ey Ez : Nat) : ℝ := 2 ^ (Dx * Ex) * 2 ^ (Dy * Ey) * 2 ^ (Dz * Ez)

/-- the slope sums are the real slope parts at the corners, times the scale -/
lemma NP.acc_eq (Dx Dy Dz Ex Ey Ez Lx Ly Lz : Nat) (p : NP) (hd : p.degLE Dx Dy Dz = true) :
    let A := slopeAcc Dx Dy Dz Ex Ey Ez Lx Ly Lz p
    let s := sc Dx Dy Dz Ex Ey Ez
    let X := gv Lx Ex; let Y := gv Ly Ey; let Z := gv Lz Ez
    (A.v : ℝ) = p.eval (X 1) (Y 1) (Z 1) * s ∧
    (A.ah : ℝ) * 2 ^ Ex = p.ax (X 2) (Y 2) (Z 2) (X 1) (Y 1) (Z 1) * s ∧
    (A.al : ℝ) * 2 ^ Ex = p.ax (X 0) (Y 0) (Z 0) (X 1) (Y 1) (Z 1) * s ∧
    (A.bh : ℝ) * 2 ^ Ey = p.ay (X 2) (Y 2) (Z 2) (X 1) (Y 1) (Z 1) * s ∧
    (A.bl : ℝ) * 2 ^ Ey = p.ay (X 0) (Y 0) (Z 0) (X 1) (Y 1) (Z 1) * s ∧
    (A.ch : ℝ) * 2 ^ Ez = p.az (X 2) (Y 2) (Z 2) (X 1) (Y 1) (Z 1) * s ∧
    (A.cl : ℝ) * 2 ^ Ez = p.az (X 0) (Y 0) (Z 0) (X 1) (Y 1) (Z 1) * s := by
  intro A s X Y Z
  simp only [A, s, X, Y, Z]
  induction p with
  | nil => simp [slopeAcc_nil, NP.eval, NP.ax, NP.ay, NP.az]
  | cons c a b g t ih =>
    obtain ⟨ha, hb, hg, ht⟩ := NP.degLE_cons_iff.mp hd
    obtain ⟨i0, i1, i2, i3, i4, i5, i6⟩ := ih ht
    rw [slopeAcc_cons]
    simp only [S7.add, NP.eval, NP.ax, NP.ay, NP.az]
    simp only [Nat.cast_add, Nat.cast_mul]
    rw [sp_sub_hi Dx Ex Lx a ha, sp_sub_lo Dx Ex Lx a ha, sp_sub_hi Dy Ey Ly b hb, sp_sub_lo Dy Ey Ly b hb,
      sp_sub_hi Dz Ez Lz g hg, sp_sub_lo Dz Ez Lz g hg]
    simp only [sp_gv Dx Ex Lx a 2 ha, sp_gv Dx Ex Lx a 1 ha, sp_gv0 Dx Ex Lx a ha,
      sp_gv Dy Ey Ly b 2 hb, sp_gv Dy Ey Ly b 1 hb, sp_gv0 Dy Ey Ly b hb,
      sp_gv Dz Ez Lz g 2 hg, sp_gv Dz Ez Lz g 1 hg, sp_gv0 Dz Ez Lz g hg]
    unfold sc at *
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · rw [i0]; ring
    · rw [add_mul, i1]; field_simp; ring
    · rw [add_mul, i2]; field_simp; ring
    · rw [add_mul, i3]; field_simp; ring
    · rw [add_mul, i4]; field_simp; ring
    · rw [add_mul, i5]; field_simp; ring
    · rw [add_mul, i6]; field_simp; ring

/-- monotonicity of a product of three nonnegative factors times a nonnegative constant -/
lemma mul4_le {c A B C A' B' C' : ℝ} (hc : 0 ≤ c) (hA : 0 ≤ A) (hB : 0 ≤ B) (hC : 0 ≤ C)
    (hAA : A ≤ A') (hBB : B ≤ B') (hCC : C ≤ C') : c * A * B * C ≤ c * A' * B' * C' := by
  apply mul_le_mul _ hCC hC (mul_nonneg (mul_nonneg hc (hA.trans hAA)) (hB.trans hBB))
  apply mul_le_mul _ hBB hB (mul_nonneg hc (hA.trans hAA))
  exact mul_le_mul_of_nonneg_left hAA hc

/-- the slope parts are monotone in the point (for a fixed centre `m ≥ 0`) -/
lemma NP.slope_mono (p : NP) {x y z x' y' z' mx my mz : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (hz : 0 ≤ z)
    (hxx : x ≤ x') (hyy : y ≤ y') (hzz : z ≤ z') (hmx : 0 ≤ mx) (hmy : 0 ≤ my) (hmz : 0 ≤ mz) :
    p.ax x y z mx my mz ≤ p.ax x' y' z' mx my mz ∧ p.ay x y z mx my mz ≤ p.ay x' y' z' mx my mz ∧
    p.az x y z mx my mz ≤ p.az x' y' z' mx my mz := by
  induction p with
  | nil => simp [NP.ax, NP.ay, NP.az]
  | cons c a b e t ih =>
    obtain ⟨i1, i2, i3⟩ := ih
    simp only [NP.ax, NP.ay, NP.az]
    have hc : (0 : ℝ) ≤ c := Nat.cast_nonneg c
    refine ⟨?_, ?_, ?_⟩
    · have := mul4_le hc (gs_nonneg a hx hmx) (pow_nonneg hy b) (pow_nonneg hz e) (gs_mono a hx hxx hmx)
        (pow_le_pow_left₀ hy hyy b) (pow_le_pow_left₀ hz hzz e)
      linarith
    · have := mul4_le hc (pow_nonneg hmx a) (gs_nonneg b hy hmy) (pow_nonneg hz e) le_rfl (gs_mono b hy hyy hmy)
        (pow_le_pow_left₀ hz hzz e)
      linarith
    · have := mul4_le hc (pow_nonneg hmx a) (pow_nonneg hmy b) (gs_nonneg e hz hmz) le_rfl le_rfl (gs_mono e hz hzz hmz)
      linarith

lemma abs_tA {t A lo hi w : ℝ} (hw : 0 < w) (ht : |t| ≤ 1 / w) (h1 : w * lo ≤ A) (h2 : A ≤ w * hi) :
    |t * A| ≤ max |hi| |lo| := by
  have hA : |A| ≤ w * max |hi| |lo| := by
    rw [abs_le]; constructor
    · have : -(w * max |hi| |lo|) ≤ w * lo := by
        have := neg_abs_le lo; have := le_max_right |hi| |lo|; nlinarith
      linarith
    · have : w * hi ≤ w * max |hi| |lo| := by
        have := le_abs_self hi; have := le_max_left |hi| |lo|; nlinarith
      linarith
  rw [abs_mul]
  calc |t| * |A| ≤ (1 / w) * (w * max |hi| |lo|) := mul_le_mul ht hA (abs_nonneg _) (by positivity)
    _ = max |hi| |lo| := by field_simp

lemma adist_cast (a b : Nat) : ((adist a b : Nat) : ℝ) = |(a : ℝ) - b| := by
  unfold adist
  rcases le_total a b with h | h
  · rw [Nat.sub_eq_zero_of_le h, zero_add, Nat.cast_sub h, abs_of_nonpos (by linarith [(Nat.cast_le (α := ℝ)).mpr h])]
    ring
  · rw [Nat.sub_eq_zero_of_le h, add_zero, Nat.cast_sub h, abs_of_nonneg (by linarith [(Nat.cast_le (α := ℝ)).mpr h])]

lemma gv_cell (d i : Nat) : gv (2 * i) (d + 1) 0 = (i : ℝ) / 2 ^ d ∧ gv (2 * i) (d + 1) 2 = ((i : ℝ) + 1) / 2 ^ d := by
  unfold gv; constructor <;> (push_cast; rw [pow_succ]; field_simp; try ring)

set_option maxHeartbeats 2000000 in
/-- the slope form encloses the polynomial on the cell -/
lemma SP.slope_enclosure (p : SP) (hd : p.degOK = true) (c : Cell) (x y z : ℝ) (hc : c.Mem x y z) :
    |p.eval x y z * sc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) - (((p.accP c).v : ℝ) - (p.accN c).v)| ≤
      (S7.rad (p.accP c) (p.accN c) : ℝ) := by
  obtain ⟨hx1, hx2, hy1, hy2, hz1, hz2⟩ := hc
  have hdp : p.pp.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.1
  have hdn : p.pn.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.2
  obtain ⟨gx0, gx2⟩ := gv_cell c.dx c.ix
  obtain ⟨gy0, gy2⟩ := gv_cell c.dy c.iy
  obtain ⟨gz0, gz2⟩ := gv_cell c.dz c.iz
  rw [← gx0] at hx1; rw [← gx2] at hx2; rw [← gy0] at hy1; rw [← gy2] at hy2; rw [← gz0] at hz1; rw [← gz2] at hz2
  set X := gv (2 * c.ix) (c.dx + 1) with hX
  set Y := gv (2 * c.iy) (c.dy + 1) with hY
  set Z := gv (2 * c.iz) (c.dz + 1) with hZ
  set s := sc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) with hs
  have hs0 : 0 ≤ s := by rw [hs]; unfold sc; positivity
  obtain ⟨P0, P1, P2, P3, P4, P5, P6⟩ := NP.acc_eq p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) (2 * c.ix) (2 * c.iy) (2 * c.iz) p.pp hdp
  obtain ⟨N0, N1, N2, N3, N4, N5, N6⟩ := NP.acc_eq p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) (2 * c.ix) (2 * c.iy) (2 * c.iz) p.pn hdn
  have x0 : 0 ≤ X 0 := gv_nonneg _ _ _
  have y0 : 0 ≤ Y 0 := gv_nonneg _ _ _
  have z0 : 0 ≤ Z 0 := gv_nonneg _ _ _
  have m0x : 0 ≤ X 1 := gv_nonneg _ _ _
  have m0y : 0 ≤ Y 1 := gv_nonneg _ _ _
  have m0z : 0 ≤ Z 1 := gv_nonneg _ _ _
  obtain ⟨pL1, pL2, pL3⟩ := NP.slope_mono p.pp x0 y0 z0 hx1 hy1 hz1 m0x m0y m0z
  obtain ⟨pH1, pH2, pH3⟩ := NP.slope_mono p.pp (x0.trans hx1) (y0.trans hy1) (z0.trans hz1) hx2 hy2 hz2 m0x m0y m0z
  obtain ⟨nL1, nL2, nL3⟩ := NP.slope_mono p.pn x0 y0 z0 hx1 hy1 hz1 m0x m0y m0z
  obtain ⟨nH1, nH2, nH3⟩ := NP.slope_mono p.pn (x0.trans hx1) (y0.trans hy1) (z0.trans hz1) hx2 hy2 hz2 m0x m0y m0z
  have ip := NP.slope_id p.pp x y z (X 1) (Y 1) (Z 1)
  have iN := NP.slope_id p.pn x y z (X 1) (Y 1) (Z 1)
  -- distances to the centre
  have dX := gv_sub (2 * c.ix) (c.dx + 1)
  have dY := gv_sub (2 * c.iy) (c.dy + 1)
  have dZ := gv_sub (2 * c.iz) (c.dz + 1)
  have tx : |x - X 1| ≤ 1 / 2 ^ (c.dx + 1) := by rw [abs_le]; constructor <;> linarith [dX.1, dX.2]
  have ty : |y - Y 1| ≤ 1 / 2 ^ (c.dy + 1) := by rw [abs_le]; constructor <;> linarith [dY.1, dY.2]
  have tz : |z - Z 1| ≤ 1 / 2 ^ (c.dz + 1) := by rw [abs_le]; constructor <;> linarith [dZ.1, dZ.2]
  have wx : (0 : ℝ) < 2 ^ (c.dx + 1) := by positivity
  have wy : (0 : ℝ) < 2 ^ (c.dy + 1) := by positivity
  have wz : (0 : ℝ) < 2 ^ (c.dz + 1) := by positivity
  unfold SP.accP SP.accN
  set P := slopeAcc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) (2 * c.ix) (2 * c.iy) (2 * c.iz) p.pp with hP
  set N := slopeAcc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) (2 * c.ix) (2 * c.iy) (2 * c.iz) p.pn with hN
  have bx := abs_tA (t := x - X 1) (A := (p.pp.ax x y z (X 1) (Y 1) (Z 1) - p.pn.ax x y z (X 1) (Y 1) (Z 1)) * s)
    (lo := (P.al : ℝ) - N.ah) (hi := (P.ah : ℝ) - N.al) wx tx
    (by have := mul_le_mul_of_nonneg_right pL1 hs0; have := mul_le_mul_of_nonneg_right nH1 hs0; linarith)
    (by have := mul_le_mul_of_nonneg_right pH1 hs0; have := mul_le_mul_of_nonneg_right nL1 hs0; linarith)
  have by' := abs_tA (t := y - Y 1) (A := (p.pp.ay x y z (X 1) (Y 1) (Z 1) - p.pn.ay x y z (X 1) (Y 1) (Z 1)) * s)
    (lo := (P.bl : ℝ) - N.bh) (hi := (P.bh : ℝ) - N.bl) wy ty
    (by have := mul_le_mul_of_nonneg_right pL2 hs0; have := mul_le_mul_of_nonneg_right nH2 hs0; linarith)
    (by have := mul_le_mul_of_nonneg_right pH2 hs0; have := mul_le_mul_of_nonneg_right nL2 hs0; linarith)
  have bz := abs_tA (t := z - Z 1) (A := (p.pp.az x y z (X 1) (Y 1) (Z 1) - p.pn.az x y z (X 1) (Y 1) (Z 1)) * s)
    (lo := (P.cl : ℝ) - N.ch) (hi := (P.ch : ℝ) - N.cl) wz tz
    (by have := mul_le_mul_of_nonneg_right pL3 hs0; have := mul_le_mul_of_nonneg_right nH3 hs0; linarith)
    (by have := mul_le_mul_of_nonneg_right pH3 hs0; have := mul_le_mul_of_nonneg_right nL3 hs0; linarith)
  have key : p.eval x y z * s - ((P.v : ℝ) - N.v) =
      (x - X 1) * ((p.pp.ax x y z (X 1) (Y 1) (Z 1) - p.pn.ax x y z (X 1) (Y 1) (Z 1)) * s) +
      (y - Y 1) * ((p.pp.ay x y z (X 1) (Y 1) (Z 1) - p.pn.ay x y z (X 1) (Y 1) (Z 1)) * s) +
      (z - Z 1) * ((p.pp.az x y z (X 1) (Y 1) (Z 1) - p.pn.az x y z (X 1) (Y 1) (Z 1)) * s) := by
    unfold SP.eval; rw [P0, N0]; linear_combination s * ip - s * iN
  rw [key]
  unfold S7.rad
  push_cast
  rw [adist_cast, adist_cast, adist_cast, adist_cast, adist_cast, adist_cast]
  calc _ ≤ |(x - X 1) * ((p.pp.ax x y z (X 1) (Y 1) (Z 1) - p.pn.ax x y z (X 1) (Y 1) (Z 1)) * s)| +
        |(y - Y 1) * ((p.pp.ay x y z (X 1) (Y 1) (Z 1) - p.pn.ay x y z (X 1) (Y 1) (Z 1)) * s)| +
        |(z - Z 1) * ((p.pp.az x y z (X 1) (Y 1) (Z 1) - p.pn.az x y z (X 1) (Y 1) (Z 1)) * s)| :=
        (abs_add_le _ _).trans (add_le_add (abs_add_le _ _) le_rfl)
    _ ≤ _ := add_le_add (add_le_add bx by') bz

lemma SP.signSlope_sound (p : SP) (hd : p.degOK = true) (c : Cell) (x y z : ℝ) (hc : c.Mem x y z) :
    (p.signSlope c = 1 → 0 < p.eval x y z) ∧ (p.signSlope c = 2 → p.eval x y z < 0) := by
  have he := p.slope_enclosure hd c x y z hc
  have hs : 0 < sc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) := by unfold sc; positivity
  rw [abs_le] at he
  unfold SP.signSlope signOf
  constructor
  · intro h
    cases hb : Nat.blt ((p.accN c).v + S7.rad (p.accP c) (p.accN c)) (p.accP c).v
    · rw [hb] at h
      cases hb2 : Nat.blt ((p.accP c).v + S7.rad (p.accP c) (p.accN c)) (p.accN c).v <;> rw [hb2] at h <;> simp at h
    · rw [Nat.blt_eq] at hb
      have hb' : ((p.accN c).v : ℝ) + (S7.rad (p.accP c) (p.accN c) : ℝ) < (p.accP c).v := by exact_mod_cast hb
      have : 0 < p.eval x y z * sc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) := by linarith
      exact pos_of_mul_pos_left this hs.le
  · intro h
    cases hb : Nat.blt ((p.accN c).v + S7.rad (p.accP c) (p.accN c)) (p.accP c).v
    · rw [hb] at h
      cases hb2 : Nat.blt ((p.accP c).v + S7.rad (p.accP c) (p.accN c)) (p.accN c).v
      · rw [hb2] at h; simp at h
      · rw [Nat.blt_eq] at hb2
        have hb' : ((p.accP c).v : ℝ) + (S7.rad (p.accP c) (p.accN c) : ℝ) < (p.accN c).v := by exact_mod_cast hb2
        have : p.eval x y z * sc p.Dx p.Dy p.Dz (c.dx + 1) (c.dy + 1) (c.dz + 1) < 0 := by linarith
        exact neg_of_mul_neg_left this hs.le
    · rw [hb] at h; simp at h

/-- either method -/
lemma SP.sign_sound (p : SP) (hd : p.degOK = true) (m : Nat) (c : Cell) (x y z : ℝ) (hc : c.Mem x y z) :
    (p.sign m c = 1 → 0 < p.eval x y z) ∧ (p.sign m c = 2 → p.eval x y z < 0) := by
  unfold SP.sign
  cases Nat.beq m 0
  · exact p.signSlope_sound hd c x y z hc
  · exact p.signMono_sound hd c x y z hc

end YantraCert
