module

public import YantraCert.Sound

@[expose] public section

/-!
# Existence and uniqueness of a zero in a box (Krawczyk's test, slope form)

The test is R. Krawczyk's (*Computing* 4, 1969), in the uniqueness form of R. E. Moore (*SIAM J. Numer. Anal.* 14, 1977) and
A. Neumaier (*Interval Methods for Systems of Equations*, 1990, Thm 5.1.7), with slopes in place of derivatives (Krawczyk and
Neumaier 1985).  For a box `X = c ± r`, slopes `F x - F m = S(x, m) (x - m)` with `S` enclosed in `[ℓ, h]` on `X × X`, and any
matrix `Y`:
* if `‖I - Y S‖ < 1` in the norm weighted by `r` (`hK`), `F` has at most one zero in `X` (`krawczyk_unique`);
* if moreover `|Y F(c)| + M r ≤ r` (`hI`) and `Z Y = I`, the map `x ↦ x - Y F(x)` sends `X` into itself and is a contraction, so
  it has a fixed point by Banach's fixed-point theorem (Mathlib `ContractingWith.fixedPoint`), which is a zero of `F`
  (`krawczyk_exists`).

The second part (the polynomial instance) gives the slopes and their enclosures for polynomials with natural coefficients on a
box with nonnegative coordinates and a common denominator `Q`.
-/

namespace YantraCert
open Finset

section General

variable {ι : Type} [Fintype ι] [DecidableEq ι]

/-- the box `c ± r` -/
def InBox (c r : ι → ℝ) (x : ι → ℝ) : Prop := ∀ j, |x j - c j| ≤ r j

/-- one entry of `I - Y S` is bounded by the midpoint–radius bound -/
lemma entry_bound (δ : ℝ) (Y S ℓ h : ι → ℝ) (hS : ∀ k, ℓ k ≤ S k ∧ S k ≤ h k) :
    |δ - ∑ k, Y k * S k| ≤ |δ - ∑ k, Y k * ((ℓ k + h k) / 2)| + ∑ k, |Y k| * ((h k - ℓ k) / 2) := by
  have e : δ - ∑ k, Y k * S k = (δ - ∑ k, Y k * ((ℓ k + h k) / 2)) - ∑ k, Y k * (S k - (ℓ k + h k) / 2) := by
    rw [sub_sub, ← sum_add_distrib]; congr 1; apply sum_congr rfl; intro k _; ring
  rw [e]
  refine (abs_sub _ _).trans (add_le_add le_rfl ?_)
  refine (abs_sum_le_sum_abs _ _).trans (sum_le_sum fun k _ => ?_)
  rw [abs_mul]
  apply mul_le_mul_of_nonneg_left _ (abs_nonneg _)
  rw [abs_le]; constructor <;> linarith [(hS k).1, (hS k).2]

/-- the Krawczyk map -/
def kmap (F : ι → (ι → ℝ) → ℝ) (Y : ι → ι → ℝ) (x : ι → ℝ) : ι → ℝ := fun i => x i - ∑ k, Y i k * F k x

/-- the basic estimate: `|(T x - T m)_i| ≤ Σ_j M_ij |x_j - m_j|` -/
lemma kmap_diff (F : ι → (ι → ℝ) → ℝ) (S : ι → ι → (ι → ℝ) → (ι → ℝ) → ℝ) (c r : ι → ℝ) (ℓ h Y M : ι → ι → ℝ)
    (hS : ∀ x m, InBox c r x → InBox c r m → ∀ k, F k x - F k m = ∑ j, S k j x m * (x j - m j))
    (hSb : ∀ x m, InBox c r x → InBox c r m → ∀ k j, ℓ k j ≤ S k j x m ∧ S k j x m ≤ h k j)
    (hM : ∀ i j, |(if i = j then (1 : ℝ) else 0) - ∑ k, Y i k * ((ℓ k j + h k j) / 2)| +
      ∑ k, |Y i k| * ((h k j - ℓ k j) / 2) ≤ M i j)
    (x m : ι → ℝ) (hx : InBox c r x) (hm : InBox c r m) (i : ι) :
    |kmap F Y x i - kmap F Y m i| ≤ ∑ j, M i j * |x j - m j| := by
  have e : kmap F Y x i - kmap F Y m i =
      ∑ j, ((if i = j then (1 : ℝ) else 0) - ∑ k, Y i k * S k j x m) * (x j - m j) := by
    unfold kmap
    have e1 : x i - m i = ∑ j, (if i = j then (1 : ℝ) else 0) * (x j - m j) := by simp
    have e2 : ∑ k, Y i k * F k x - ∑ k, Y i k * F k m = ∑ j, (∑ k, Y i k * S k j x m) * (x j - m j) := by
      rw [← sum_sub_distrib]
      simp_rw [← mul_sub, hS x m hx hm, mul_sum, sum_mul]
      rw [sum_comm]; apply sum_congr rfl; intro j _; apply sum_congr rfl; intro k _; ring
    rw [show x i - ∑ k, Y i k * F k x - (m i - ∑ k, Y i k * F k m) =
      (x i - m i) - (∑ k, Y i k * F k x - ∑ k, Y i k * F k m) by ring, e1, e2, ← sum_sub_distrib]
    apply sum_congr rfl; intro j _; ring
  rw [e]
  refine (abs_sum_le_sum_abs _ _).trans (sum_le_sum fun j _ => ?_)
  rw [abs_mul]
  apply mul_le_mul_of_nonneg_right _ (abs_nonneg _)
  exact (entry_bound _ (Y i) (fun k => S k j x m) (fun k => ℓ k j) (fun k => h k j)
    (fun k => hSb x m hx hm k j)).trans (hM i j)

lemma M_nonneg {ℓ h Y M : ι → ι → ℝ}
    (hM : ∀ i j, |(if i = j then (1 : ℝ) else 0) - ∑ k, Y i k * ((ℓ k j + h k j) / 2)| +
      ∑ k, |Y i k| * ((h k j - ℓ k j) / 2) ≤ M i j)
    (hl : ∀ k j, ℓ k j ≤ h k j) (i j : ι) : 0 ≤ M i j := by
  refine le_trans ?_ (hM i j)
  exact add_nonneg (abs_nonneg _) (sum_nonneg fun k _ => mul_nonneg (abs_nonneg _) (by linarith [hl k j]))

/-- **at most one zero in the box** -/
theorem krawczyk_unique (F : ι → (ι → ℝ) → ℝ) (S : ι → ι → (ι → ℝ) → (ι → ℝ) → ℝ) (c r : ι → ℝ) (ℓ h Y M : ι → ι → ℝ)
    (hS : ∀ x m, InBox c r x → InBox c r m → ∀ k, F k x - F k m = ∑ j, S k j x m * (x j - m j))
    (hSb : ∀ x m, InBox c r x → InBox c r m → ∀ k j, ℓ k j ≤ S k j x m ∧ S k j x m ≤ h k j)
    (hl : ∀ k j, ℓ k j ≤ h k j)
    (hM : ∀ i j, |(if i = j then (1 : ℝ) else 0) - ∑ k, Y i k * ((ℓ k j + h k j) / 2)| +
      ∑ k, |Y i k| * ((h k j - ℓ k j) / 2) ≤ M i j)
    (hr : ∀ i, 0 < r i) (hC : ∀ i, ∑ j, M i j * r j < r i)
    (x x' : ι → ℝ) (hx : InBox c r x) (hx' : InBox c r x') (h0 : ∀ k, F k x = 0) (h0' : ∀ k, F k x' = 0) : x = x' := by
  by_contra hne
  have hne' : ∃ j, x j ≠ x' j := by
    by_contra hh; push Not at hh; exact hne (funext hh)
  obtain ⟨j1, hj1⟩ := hne'
  obtain ⟨j0, -, hj0⟩ := Finset.exists_max_image Finset.univ (fun j => |x j - x' j| / r j) ⟨j1, Finset.mem_univ _⟩
  set t := |x j0 - x' j0| / r j0 with ht
  have tpos : 0 < t := by
    have := hj0 j1 (Finset.mem_univ _)
    have : 0 < |x j1 - x' j1| / r j1 := div_pos (abs_pos.mpr (sub_ne_zero.mpr hj1)) (hr j1)
    linarith
  have fix : ∀ y, (∀ k, F k y = 0) → kmap F Y y = y := by
    intro y hy; funext i; simp [kmap, hy]
  have hd := kmap_diff F S c r ℓ h Y M hS hSb hM x x' hx hx' j0
  rw [fix x h0, fix x' h0'] at hd
  have hb : ∑ j, M j0 j * |x j - x' j| ≤ ∑ j, M j0 j * (r j * t) := by
    apply sum_le_sum; intro j _
    apply mul_le_mul_of_nonneg_left _ (M_nonneg hM hl j0 j)
    have := hj0 j (Finset.mem_univ _)
    rw [div_le_iff₀ (hr j)] at this; linarith
  have e : ∑ j, M j0 j * (r j * t) = (∑ j, M j0 j * r j) * t := by rw [sum_mul]; apply sum_congr rfl; intro j _; ring
  have : |x j0 - x' j0| < r j0 * t := by
    calc |x j0 - x' j0| ≤ (∑ j, M j0 j * r j) * t := by linarith
      _ < r j0 * t := mul_lt_mul_of_pos_right (hC j0) tpos
  rw [ht, mul_div_cancel₀ _ (hr j0).ne'] at this
  exact lt_irrefl _ this

/-- **a zero exists in the box** (Banach's fixed-point theorem, Mathlib `ContractingWith.fixedPoint`) -/
theorem krawczyk_exists (F : ι → (ι → ℝ) → ℝ) (S : ι → ι → (ι → ℝ) → (ι → ℝ) → ℝ) (c r : ι → ℝ) (ℓ h Y Z M : ι → ι → ℝ)
    (K : ℝ) (hS : ∀ x m, InBox c r x → InBox c r m → ∀ k, F k x - F k m = ∑ j, S k j x m * (x j - m j))
    (hSb : ∀ x m, InBox c r x → InBox c r m → ∀ k j, ℓ k j ≤ S k j x m ∧ S k j x m ≤ h k j)
    (hl : ∀ k j, ℓ k j ≤ h k j)
    (hM : ∀ i j, |(if i = j then (1 : ℝ) else 0) - ∑ k, Y i k * ((ℓ k j + h k j) / 2)| +
      ∑ k, |Y i k| * ((h k j - ℓ k j) / 2) ≤ M i j)
    (hr : ∀ i, 0 < r i) (hK0 : 0 ≤ K) (hK1 : K < 1) (hK : ∀ i, ∑ j, M i j * r j ≤ K * r i)
    (hI : ∀ i, |∑ k, Y i k * F k c| + ∑ j, M i j * r j ≤ r i)
    (hZ : ∀ i l, ∑ k, Z i k * Y k l = if i = l then 1 else 0) :
    ∃ x, InBox c r x ∧ ∀ k, F k x = 0 := by
  -- scaled coordinates: x = c + r w with w in the closed unit ball of the sup norm
  let emb : (ι → ℝ) → (ι → ℝ) := fun w j => c j + r j * w j
  have inb : ∀ w : ι → ℝ, (∀ j, |w j| ≤ 1) → InBox c r (emb w) := by
    intro w hw j
    simp only [emb, add_sub_cancel_left, abs_mul, abs_of_pos (hr j)]
    nlinarith [hw j, hr j, abs_nonneg (w j)]
  have cin : InBox c r c := fun j => by simp [(hr j).le]
  let Φ : (ι → ℝ) → (ι → ℝ) := fun w i => (kmap F Y (emb w) i - c i) / r i
  let B := Metric.closedBall (0 : ι → ℝ) 1
  have memB : ∀ w : ι → ℝ, w ∈ B ↔ ∀ j, |w j| ≤ 1 := by
    intro w
    simp only [B, Metric.mem_closedBall, dist_zero_right]
    rw [pi_norm_le_iff_of_nonneg zero_le_one]
    simp [Real.norm_eq_abs]
  have maps : ∀ w ∈ B, Φ w ∈ B := by
    intro w hw
    rw [memB] at hw ⊢
    intro i
    have h1 := kmap_diff F S c r ℓ h Y M hS hSb hM (emb w) c (inb w hw) cin i
    have h2 : ∑ j, M i j * |emb w j - c j| ≤ ∑ j, M i j * r j := by
      apply sum_le_sum; intro j _
      exact mul_le_mul_of_nonneg_left (inb w hw j) (M_nonneg hM hl i j)
    have h3 : kmap F Y c i - c i = -∑ k, Y i k * F k c := by simp [kmap]
    simp only [Φ]
    rw [abs_div, abs_of_pos (hr i), div_le_one (hr i)]
    calc |kmap F Y (emb w) i - c i| = |(kmap F Y (emb w) i - kmap F Y c i) + (kmap F Y c i - c i)| := by ring_nf
      _ ≤ |kmap F Y (emb w) i - kmap F Y c i| + |kmap F Y c i - c i| := abs_add_le _ _
      _ ≤ r i := by rw [h3, abs_neg]; linarith [hI i]
  have lip : ∀ w ∈ B, ∀ w' ∈ B, dist (Φ w) (Φ w') ≤ K * dist w w' := by
    intro w hw w' hw'
    have hw0 := (memB w).mp hw
    have hw0' := (memB w').mp hw'
    apply (dist_pi_le_iff (mul_nonneg hK0 dist_nonneg)).mpr
    intro i
    have h1 := kmap_diff F S c r ℓ h Y M hS hSb hM (emb w) (emb w') (inb w hw0) (inb w' hw0') i
    have h2 : ∑ j, M i j * |emb w j - emb w' j| ≤ (∑ j, M i j * r j) * dist w w' := by
      rw [sum_mul]; apply sum_le_sum; intro j _
      have : |emb w j - emb w' j| = r j * dist (w j) (w' j) := by
        simp only [emb, Real.dist_eq]; rw [show c j + r j * w j - (c j + r j * w' j) = r j * (w j - w' j) by ring,
          abs_mul, abs_of_pos (hr j)]
      rw [this, ← mul_assoc]
      exact mul_le_mul_of_nonneg_left (dist_le_pi_dist w w' j) (mul_nonneg (M_nonneg hM hl i j) (hr j).le)
    simp only [Φ, Real.dist_eq]
    rw [div_sub_div_same, show kmap F Y (emb w) i - c i - (kmap F Y (emb w') i - c i) =
      kmap F Y (emb w) i - kmap F Y (emb w') i by ring, abs_div, abs_of_pos (hr i), div_le_iff₀ (hr i)]
    have := hK i
    nlinarith [dist_nonneg (x := w) (y := w')]
  -- Banach on the closed ball
  have : CompleteSpace B := (Metric.isClosed_closedBall).completeSpace_coe
  have : Nonempty B := ⟨⟨0, by simp [B]⟩⟩
  let f : B → B := fun w => ⟨Φ w, maps w w.2⟩
  have hf : ContractingWith ⟨K, hK0⟩ f := by
    refine ⟨by exact_mod_cast hK1, LipschitzWith.of_dist_le_mul fun w w' => ?_⟩
    simp only [f, Subtype.dist_eq]
    exact lip w w.2 w' w'.2
  set w := ContractingWith.fixedPoint f hf with hwdef
  have hfix : f w = w := ContractingWith.fixedPoint_isFixedPt hf
  have hΦ : Φ w.1 = w.1 := congrArg Subtype.val hfix
  refine ⟨emb w.1, inb w.1 ((memB w.1).mp w.2), ?_⟩
  -- the fixed point gives Y F(x) = 0, and Z Y = I gives F(x) = 0
  have hYF : ∀ i, ∑ k, Y i k * F k (emb w.1) = 0 := by
    intro i
    have := congrFun hΦ i
    simp only [Φ, kmap, emb] at this
    rw [div_eq_iff (hr i).ne'] at this
    linarith
  intro l
  have : F l (emb w.1) = ∑ i, (if l = i then (1 : ℝ) else 0) * F i (emb w.1) := by simp
  rw [this]
  simp_rw [← hZ, sum_mul]
  rw [sum_comm]
  simp_rw [mul_assoc, ← mul_sum, hYF, mul_zero, sum_const_zero]

end General

/-! ## Polynomial slopes on a box with a common denominator -/

/-- homogenised power with denominator `Q`: `n^a Q^(D-a)` -/
def spq (D Q n a : Nat) : Nat := n ^ a * Q ^ (D - a)
/-- homogenised slope corner `gs a t t = a t^(a-1)` with `t = n/Q`: `a n^(a-1) Q^(D-a)` -/
def gsq (D Q n a : Nat) : Nat := a * n ^ (a - 1) * Q ^ (D - a)

noncomputable def NP.evalG (gx gy gz : Nat → ℝ) : NP → ℝ
  | .nil => 0
  | .cons c a b e t => (c : ℝ) * gx a * gy b * gz e + t.evalG gx gy gz

lemma NP.ev_cast_gen (Dx Dy Dz : Nat) (p : NP) (hd : p.degLE Dx Dy Dz = true) (fx fy fz : Nat → Nat)
    (gx gy gz : Nat → ℝ) (hx : ∀ a ≤ Dx, (fx a : ℝ) = gx a) (hy : ∀ b ≤ Dy, (fy b : ℝ) = gy b)
    (hz : ∀ e ≤ Dz, (fz e : ℝ) = gz e) : ((p.ev fx fy fz : Nat) : ℝ) = p.evalG gx gy gz := by
  induction p with
  | nil => simp [NP.ev_nil, NP.evalG]
  | cons c a b e t ih =>
    obtain ⟨ha, hb, he, ht⟩ := NP.degLE_cons_iff.mp hd
    rw [NP.ev_cons]; push_cast; rw [hx a ha, hy b hb, hz e he, ih ht, NP.evalG]; ring

lemma spq_cast (D Q n a : Nat) (h : a ≤ D) (hQ : 0 < Q) :
    ((spq D Q n a : Nat) : ℝ) = ((n : ℝ) / Q) ^ a * (Q : ℝ) ^ D := by
  unfold spq; push_cast
  have hQ' : (Q : ℝ) ≠ 0 := by exact_mod_cast hQ.ne'
  have : (Q : ℝ) ^ D = (Q : ℝ) ^ a * (Q : ℝ) ^ (D - a) := by rw [← pow_add, Nat.add_sub_cancel' h]
  rw [this, div_pow]; field_simp

lemma gs_self (n : Nat) (t : ℝ) : gs n t t = n * t ^ (n - 1) := by
  unfold gs
  rw [sum_congr rfl (g := fun _ => t ^ (n - 1))]
  · simp
  · intro i hi
    rw [mem_range] at hi
    rw [← pow_add]; congr 1; omega

lemma gsq_cast (D Q n a : Nat) (h : a ≤ D) (hQ : 0 < Q) :
    ((gsq D Q n a : Nat) : ℝ) = gs a ((n : ℝ) / Q) ((n : ℝ) / Q) * (Q : ℝ) ^ (D - 1) := by
  rw [gs_self]; unfold gsq
  have hQ' : (Q : ℝ) ≠ 0 := by exact_mod_cast hQ.ne'
  cases a with
  | zero => push_cast; ring
  | succ a =>
    push_cast
    have e : D - 1 = a + (D - (a + 1)) := by omega
    rw [e, pow_add, div_pow]; field_simp

lemma NP.evalG_eval (p : NP) (tx ty tz Kx Ky Kz : ℝ) :
    p.evalG (fun a => tx ^ a * Kx) (fun b => ty ^ b * Ky) (fun e => tz ^ e * Kz) = p.eval tx ty tz * (Kx * Ky * Kz) := by
  induction p with
  | nil => simp [NP.evalG, NP.eval]
  | cons c a b e t ih => simp only [NP.evalG, NP.eval, ih]; ring

lemma NP.evalG_ax (p : NP) (tx ty tz Kx Ky Kz : ℝ) :
    p.evalG (fun a => gs a tx tx * Kx) (fun b => ty ^ b * Ky) (fun e => tz ^ e * Kz) = p.ax tx ty tz tx ty tz * (Kx * Ky * Kz) := by
  induction p with
  | nil => simp [NP.evalG, NP.ax]
  | cons c a b e t ih => simp only [NP.evalG, NP.ax, ih]; ring
lemma NP.evalG_ay (p : NP) (tx ty tz Kx Ky Kz : ℝ) :
    p.evalG (fun a => tx ^ a * Kx) (fun b => gs b ty ty * Ky) (fun e => tz ^ e * Kz) = p.ay tx ty tz tx ty tz * (Kx * Ky * Kz) := by
  induction p with
  | nil => simp [NP.evalG, NP.ay]
  | cons c a b e t ih => simp only [NP.evalG, NP.ay, ih]; ring
lemma NP.evalG_az (p : NP) (tx ty tz Kx Ky Kz : ℝ) :
    p.evalG (fun a => tx ^ a * Kx) (fun b => ty ^ b * Ky) (fun e => gs e tz tz * Kz) = p.az tx ty tz tx ty tz * (Kx * Ky * Kz) := by
  induction p with
  | nil => simp [NP.evalG, NP.az]
  | cons c a b e t ih => simp only [NP.evalG, NP.az, ih]; ring

lemma gs_mono2 (n : ℕ) {x x' m m' : ℝ} (hx : 0 ≤ x) (hxx : x ≤ x') (hm : 0 ≤ m) (hmm : m ≤ m') :
    gs n x m ≤ gs n x' m' :=
  sum_le_sum fun i _ => mul_le_mul (pow_le_pow_left₀ hx hxx i) (pow_le_pow_left₀ hm hmm _) (pow_nonneg hm _)
    (pow_nonneg (hx.trans hxx) _)

/-- the slope parts are monotone in the point and in the centre -/
lemma NP.slope_mono2 (p : NP) {x y z mx my mz x' y' z' mx' my' mz' : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (hz : 0 ≤ z)
    (hmx : 0 ≤ mx) (hmy : 0 ≤ my) (hmz : 0 ≤ mz) (hxx : x ≤ x') (hyy : y ≤ y') (hzz : z ≤ z')
    (hmxx : mx ≤ mx') (hmyy : my ≤ my') (hmzz : mz ≤ mz') :
    p.ax x y z mx my mz ≤ p.ax x' y' z' mx' my' mz' ∧ p.ay x y z mx my mz ≤ p.ay x' y' z' mx' my' mz' ∧
    p.az x y z mx my mz ≤ p.az x' y' z' mx' my' mz' := by
  induction p with
  | nil => simp [NP.ax, NP.ay, NP.az]
  | cons c a b e t ih =>
    obtain ⟨i1, i2, i3⟩ := ih
    simp only [NP.ax, NP.ay, NP.az]
    have hc : (0 : ℝ) ≤ c := Nat.cast_nonneg c
    refine ⟨?_, ?_, ?_⟩
    · have := mul4_le hc (gs_nonneg a hx hmx) (pow_nonneg hy b) (pow_nonneg hz e) (gs_mono2 a hx hxx hmx hmxx)
        (pow_le_pow_left₀ hy hyy b) (pow_le_pow_left₀ hz hzz e)
      linarith
    · have := mul4_le hc (pow_nonneg hmx a) (gs_nonneg b hy hmy) (pow_nonneg hz e) (pow_le_pow_left₀ hmx hmxx a)
        (gs_mono2 b hy hyy hmy hmyy) (pow_le_pow_left₀ hz hzz e)
      linarith
    · have := mul4_le hc (pow_nonneg hmx a) (pow_nonneg hmy b) (gs_nonneg e hz hmz) (pow_le_pow_left₀ hmx hmxx a)
        (pow_le_pow_left₀ hmy hmyy b) (gs_mono2 e hz hzz hmz hmzz)
      linarith

/-- the slope corner sums of one polynomial with natural coefficients -/
noncomputable def NP.sx (Dx Dy Dz Q nx ny nz : Nat) (p : NP) : Nat := p.ev (gsq Dx Q nx) (spq Dy Q ny) (spq Dz Q nz)
noncomputable def NP.sy (Dx Dy Dz Q nx ny nz : Nat) (p : NP) : Nat := p.ev (spq Dx Q nx) (gsq Dy Q ny) (spq Dz Q nz)
noncomputable def NP.sz (Dx Dy Dz Q nx ny nz : Nat) (p : NP) : Nat := p.ev (spq Dx Q nx) (spq Dy Q ny) (gsq Dz Q nz)
/-- value at a grid point of denominator `Q` -/
noncomputable def NP.vq (Dx Dy Dz Q nx ny nz : Nat) (p : NP) : Nat := p.ev (spq Dx Q nx) (spq Dy Q ny) (spq Dz Q nz)

lemma NP.vq_cast (Dx Dy Dz Q nx ny nz : Nat) (p : NP) (hd : p.degLE Dx Dy Dz = true) (hQ : 0 < Q) :
    ((p.vq Dx Dy Dz Q nx ny nz : Nat) : ℝ) = p.eval ((nx : ℝ) / Q) ((ny : ℝ) / Q) ((nz : ℝ) / Q) * ((Q : ℝ) ^ Dx * (Q : ℝ) ^ Dy * (Q : ℝ) ^ Dz) := by
  unfold NP.vq
  rw [NP.ev_cast_gen Dx Dy Dz p hd _ _ _ (fun a => ((nx : ℝ) / Q) ^ a * (Q : ℝ) ^ Dx) (fun b => ((ny : ℝ) / Q) ^ b * (Q : ℝ) ^ Dy)
    (fun e => ((nz : ℝ) / Q) ^ e * (Q : ℝ) ^ Dz) (fun a ha => spq_cast _ _ _ _ ha hQ) (fun a ha => spq_cast _ _ _ _ ha hQ)
    (fun a ha => spq_cast _ _ _ _ ha hQ), NP.evalG_eval]

/-- slope corners: the three slope parts at `(t, t)` for `t = n / Q`, scaled -/
lemma NP.s_cast (Dx Dy Dz Q nx ny nz : Nat) (p : NP) (hd : p.degLE Dx Dy Dz = true) (hQ : 0 < Q) :
    let tx := (nx : ℝ) / Q; let ty := (ny : ℝ) / Q; let tz := (nz : ℝ) / Q
    ((p.sx Dx Dy Dz Q nx ny nz : Nat) : ℝ) = p.ax tx ty tz tx ty tz * ((Q : ℝ) ^ (Dx - 1) * (Q : ℝ) ^ Dy * (Q : ℝ) ^ Dz) ∧
    ((p.sy Dx Dy Dz Q nx ny nz : Nat) : ℝ) = p.ay tx ty tz tx ty tz * ((Q : ℝ) ^ Dx * (Q : ℝ) ^ (Dy - 1) * (Q : ℝ) ^ Dz) ∧
    ((p.sz Dx Dy Dz Q nx ny nz : Nat) : ℝ) = p.az tx ty tz tx ty tz * ((Q : ℝ) ^ Dx * (Q : ℝ) ^ Dy * (Q : ℝ) ^ (Dz - 1)) := by
  intro tx ty tz
  refine ⟨?_, ?_, ?_⟩
  · unfold NP.sx
    rw [NP.ev_cast_gen Dx Dy Dz p hd _ _ _ (fun a => gs a tx tx * (Q : ℝ) ^ (Dx - 1)) (fun b => ty ^ b * (Q : ℝ) ^ Dy)
      (fun e => tz ^ e * (Q : ℝ) ^ Dz) (fun a ha => gsq_cast _ _ _ _ ha hQ) (fun a ha => spq_cast _ _ _ _ ha hQ)
      (fun a ha => spq_cast _ _ _ _ ha hQ), NP.evalG_ax]
  · unfold NP.sy
    rw [NP.ev_cast_gen Dx Dy Dz p hd _ _ _ (fun a => tx ^ a * (Q : ℝ) ^ Dx) (fun b => gs b ty ty * (Q : ℝ) ^ (Dy - 1))
      (fun e => tz ^ e * (Q : ℝ) ^ Dz) (fun a ha => spq_cast _ _ _ _ ha hQ) (fun a ha => gsq_cast _ _ _ _ ha hQ)
      (fun a ha => spq_cast _ _ _ _ ha hQ), NP.evalG_ay]
  · unfold NP.sz
    rw [NP.ev_cast_gen Dx Dy Dz p hd _ _ _ (fun a => tx ^ a * (Q : ℝ) ^ Dx) (fun b => ty ^ b * (Q : ℝ) ^ Dy)
      (fun e => gs e tz tz * (Q : ℝ) ^ (Dz - 1)) (fun a ha => spq_cast _ _ _ _ ha hQ) (fun a ha => spq_cast _ _ _ _ ha hQ)
      (fun a ha => gsq_cast _ _ _ _ ha hQ), NP.evalG_az]

/-- the slope of a signed polynomial in direction `j` (0, 1, 2) -/
noncomputable def SP.slope (p : SP) (j : Fin 3) (x m : Fin 3 → ℝ) : ℝ :=
  match j with
  | 0 => p.pp.ax (x 0) (x 1) (x 2) (m 0) (m 1) (m 2) - p.pn.ax (x 0) (x 1) (x 2) (m 0) (m 1) (m 2)
  | 1 => p.pp.ay (x 0) (x 1) (x 2) (m 0) (m 1) (m 2) - p.pn.ay (x 0) (x 1) (x 2) (m 0) (m 1) (m 2)
  | 2 => p.pp.az (x 0) (x 1) (x 2) (m 0) (m 1) (m 2) - p.pn.az (x 0) (x 1) (x 2) (m 0) (m 1) (m 2)

lemma SP.slope_identity (p : SP) (x m : Fin 3 → ℝ) :
    p.eval (x 0) (x 1) (x 2) - p.eval (m 0) (m 1) (m 2) = ∑ j, p.slope j x m * (x j - m j) := by
  rw [Fin.sum_univ_three]
  simp only [SP.slope, SP.eval]
  have h1 := NP.slope_id p.pp (x 0) (x 1) (x 2) (m 0) (m 1) (m 2)
  have h2 := NP.slope_id p.pn (x 0) (x 1) (x 2) (m 0) (m 1) (m 2)
  linear_combination h1 - h2

/-- the corner value of a slope corner sum as a real -/
noncomputable def SP.sCorner (p : SP) (Q : Nat) (j : Fin 3) (pos : Bool) (n : Fin 3 → Nat) : ℝ :=
  let P := if pos then p.pp else p.pn
  match j with
  | 0 => (P.sx p.Dx p.Dy p.Dz Q (n 0) (n 1) (n 2) : ℝ) / ((Q : ℝ) ^ (p.Dx - 1) * (Q : ℝ) ^ p.Dy * (Q : ℝ) ^ p.Dz)
  | 1 => (P.sy p.Dx p.Dy p.Dz Q (n 0) (n 1) (n 2) : ℝ) / ((Q : ℝ) ^ p.Dx * (Q : ℝ) ^ (p.Dy - 1) * (Q : ℝ) ^ p.Dz)
  | 2 => (P.sz p.Dx p.Dy p.Dz Q (n 0) (n 1) (n 2) : ℝ) / ((Q : ℝ) ^ p.Dx * (Q : ℝ) ^ p.Dy * (Q : ℝ) ^ (p.Dz - 1))

/-- the slopes of a signed polynomial are enclosed by its corner sums on a box `[L/Q, H/Q]` (all coordinates `≥ 0`) -/
lemma SP.slope_bounds (p : SP) (hd : p.degOK = true) (Q : Nat) (hQ : 0 < Q) (L H : Fin 3 → Nat) (x m : Fin 3 → ℝ)
    (hx : ∀ j, (L j : ℝ) / Q ≤ x j ∧ x j ≤ (H j : ℝ) / Q) (hm : ∀ j, (L j : ℝ) / Q ≤ m j ∧ m j ≤ (H j : ℝ) / Q) (j : Fin 3) :
    p.sCorner Q j true L - p.sCorner Q j false H ≤ p.slope j x m ∧ p.slope j x m ≤ p.sCorner Q j true H - p.sCorner Q j false L := by
  have hdp : p.pp.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.1
  have hdn : p.pn.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.2
  have q0 : (0 : ℝ) < Q := by exact_mod_cast hQ
  have l0 : ∀ i, (0 : ℝ) ≤ (L i : ℝ) / Q := fun i => by positivity
  obtain ⟨pL1, pL2, pL3⟩ := NP.s_cast p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2) p.pp hdp hQ
  obtain ⟨pH1, pH2, pH3⟩ := NP.s_cast p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2) p.pp hdp hQ
  obtain ⟨nL1, nL2, nL3⟩ := NP.s_cast p.Dx p.Dy p.Dz Q (L 0) (L 1) (L 2) p.pn hdn hQ
  obtain ⟨nH1, nH2, nH3⟩ := NP.s_cast p.Dx p.Dy p.Dz Q (H 0) (H 1) (H 2) p.pn hdn hQ
  have mp := fun (P : NP) => NP.slope_mono2 P (l0 0) (l0 1) (l0 2) (l0 0) (l0 1) (l0 2)
    (hx 0).1 (hx 1).1 (hx 2).1 (hm 0).1 (hm 1).1 (hm 2).1
  have mq := fun (P : NP) => NP.slope_mono2 P ((l0 0).trans (hx 0).1) ((l0 1).trans (hx 1).1) ((l0 2).trans (hx 2).1)
    ((l0 0).trans (hm 0).1) ((l0 1).trans (hm 1).1) ((l0 2).trans (hm 2).1)
    (hx 0).2 (hx 1).2 (hx 2).2 (hm 0).2 (hm 1).2 (hm 2).2
  fin_cases j
  · simp only [SP.sCorner, SP.slope, ite_true, Bool.false_eq_true, ite_false]
    rw [pL1, pH1, nL1, nH1]
    have dpos : (0 : ℝ) < (Q : ℝ) ^ (p.Dx - 1) * (Q : ℝ) ^ p.Dy * (Q : ℝ) ^ p.Dz := by positivity
    rw [mul_div_cancel_right₀ _ dpos.ne', mul_div_cancel_right₀ _ dpos.ne', mul_div_cancel_right₀ _ dpos.ne',
      mul_div_cancel_right₀ _ dpos.ne']
    constructor <;> linarith [(mp p.pp).1, (mq p.pp).1, (mp p.pn).1, (mq p.pn).1]
  · simp only [SP.sCorner, SP.slope, ite_true, Bool.false_eq_true, ite_false]
    rw [pL2, pH2, nL2, nH2]
    have dpos : (0 : ℝ) < (Q : ℝ) ^ p.Dx * (Q : ℝ) ^ (p.Dy - 1) * (Q : ℝ) ^ p.Dz := by positivity
    rw [mul_div_cancel_right₀ _ dpos.ne', mul_div_cancel_right₀ _ dpos.ne', mul_div_cancel_right₀ _ dpos.ne',
      mul_div_cancel_right₀ _ dpos.ne']
    constructor <;> linarith [(mp p.pp).2.1, (mq p.pp).2.1, (mp p.pn).2.1, (mq p.pn).2.1]
  · simp only [SP.sCorner, SP.slope, ite_true, Bool.false_eq_true, ite_false]
    rw [pL3, pH3, nL3, nH3]
    have dpos : (0 : ℝ) < (Q : ℝ) ^ p.Dx * (Q : ℝ) ^ p.Dy * (Q : ℝ) ^ (p.Dz - 1) := by positivity
    rw [mul_div_cancel_right₀ _ dpos.ne', mul_div_cancel_right₀ _ dpos.ne', mul_div_cancel_right₀ _ dpos.ne',
      mul_div_cancel_right₀ _ dpos.ne']
    constructor <;> linarith [(mp p.pp).2.2, (mq p.pp).2.2, (mp p.pn).2.2, (mq p.pn).2.2]

/-- the value at a grid point as a real -/
lemma SP.vq_eval (p : SP) (hd : p.degOK = true) (Q : Nat) (hQ : 0 < Q) (n : Fin 3 → Nat) :
    p.eval ((n 0 : ℝ) / Q) ((n 1 : ℝ) / Q) ((n 2 : ℝ) / Q) =
      (((p.pp.vq p.Dx p.Dy p.Dz Q (n 0) (n 1) (n 2) : Nat) : ℝ) - (p.pn.vq p.Dx p.Dy p.Dz Q (n 0) (n 1) (n 2) : Nat)) /
        ((Q : ℝ) ^ p.Dx * (Q : ℝ) ^ p.Dy * (Q : ℝ) ^ p.Dz) := by
  have hdp : p.pp.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.1
  have hdn : p.pn.degLE p.Dx p.Dy p.Dz = true := by
    unfold SP.degOK at hd; simp only [Bool.and_eq_true] at hd; exact hd.2
  rw [NP.vq_cast _ _ _ _ _ _ _ _ hdp hQ, NP.vq_cast _ _ _ _ _ _ _ _ hdn hQ, ← sub_mul, SP.eval]
  have : (0 : ℝ) < (Q : ℝ) ^ p.Dx * (Q : ℝ) ^ p.Dy * (Q : ℝ) ^ p.Dz := by
    have : (0 : ℝ) < Q := by exact_mod_cast hQ
    positivity
  rw [mul_div_cancel_right₀ _ this.ne']

/-- the midpoint-radius bound from two one-sided bounds -/
lemma abs_bound_of {a s s' M : ℝ} (hs : s ≤ s') (h1 : a + s' ≤ M) (h2 : -a + s' ≤ M) : |a| + s ≤ M := by
  rcases abs_cases a with ⟨h, _⟩ | ⟨h, _⟩ <;> rw [h] <;> linarith

end YantraCert
