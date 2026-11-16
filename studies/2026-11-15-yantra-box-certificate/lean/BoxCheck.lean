module

public import Mathlib

@[expose] public section

/-!
# Box certificate checker (pilot)

A polynomial in three variables is a list of terms `(c, a, b, e)` meaning `c * x^a * y^b * z^e`.
A leaf is a dyadic cell `[i/2^d, (i+1)/2^d]` in each coordinate (all coordinates in `[0, 1]`).
Because every coordinate is `≥ 0`, a term with `c ≥ 0` is smallest at the lower corner and largest at the upper
corner (and the other way round for `c < 0`): this is the monotone split `p = p⁺ - p⁻` of the natural interval
extension (R. E. Moore, *Interval Analysis*, 1966).  The bounds are computed exactly in `Int`, scaled by
`2^(Dx*dx + Dy*dy + Dz*dz)`, and checked by the kernel (`decide +kernel`, no `native_decide`).
-/

namespace BoxCheck

abbrev Term := Int × Nat × Nat × Nat
abbrev Poly := List Term

/-- real value of a polynomial -/
noncomputable def evalR (p : Poly) (x y z : ℝ) : ℝ :=
  (p.map fun t => (t.1 : ℝ) * x ^ t.2.1 * y ^ t.2.2.1 * z ^ t.2.2.2).sum

/-- a leaf: levels and indices in each coordinate -/
structure Leaf where
  dx : Nat
  ix : Nat
  dy : Nat
  iy : Nat
  dz : Nat
  iz : Nat
deriving Repr

/-- scaled corner value of one monomial: `n^a * 2^((D-a)*d)` per coordinate -/
def mono (D a d n : Nat) : Int := ((n ^ a * 2 ^ ((D - a) * d) : Nat) : Int)   -- Nat powers: GMP-accelerated in the kernel

/-- scaled lower bound of one term on the leaf -/
def lowT (Dx Dy Dz : Nat) (l : Leaf) (t : Term) : Int :=
  if 0 ≤ t.1 then t.1 * mono Dx t.2.1 l.dx l.ix * mono Dy t.2.2.1 l.dy l.iy * mono Dz t.2.2.2 l.dz l.iz
  else t.1 * mono Dx t.2.1 l.dx (l.ix + 1) * mono Dy t.2.2.1 l.dy (l.iy + 1) * mono Dz t.2.2.2 l.dz (l.iz + 1)

/-- scaled upper bound of one term on the leaf -/
def upT (Dx Dy Dz : Nat) (l : Leaf) (t : Term) : Int :=
  if 0 ≤ t.1 then t.1 * mono Dx t.2.1 l.dx (l.ix + 1) * mono Dy t.2.2.1 l.dy (l.iy + 1) * mono Dz t.2.2.2 l.dz (l.iz + 1)
  else t.1 * mono Dx t.2.1 l.dx l.ix * mono Dy t.2.2.1 l.dy l.iy * mono Dz t.2.2.2 l.dz l.iz

def low (Dx Dy Dz : Nat) (p : Poly) (l : Leaf) : Int := (p.map (lowT Dx Dy Dz l)).sum
def up (Dx Dy Dz : Nat) (p : Poly) (l : Leaf) : Int := (p.map (upT Dx Dy Dz l)).sum

/-- degree bounds hold for every term -/
def degOK (Dx Dy Dz : Nat) (p : Poly) : Bool := p.all fun t => t.2.1 ≤ Dx && t.2.2.1 ≤ Dy && t.2.2.2 ≤ Dz

/-- the leaf check for "p has a fixed sign on the leaf" -/
def signFixed (Dx Dy Dz : Nat) (p : Poly) (l : Leaf) : Bool := 0 < low Dx Dy Dz p l || up Dx Dy Dz p l < 0

/-- membership of a real point in a leaf -/
def InLeaf (l : Leaf) (x y z : ℝ) : Prop :=
  (l.ix : ℝ) / 2 ^ l.dx ≤ x ∧ x ≤ ((l.ix : ℝ) + 1) / 2 ^ l.dx ∧
  (l.iy : ℝ) / 2 ^ l.dy ≤ y ∧ y ≤ ((l.iy : ℝ) + 1) / 2 ^ l.dy ∧
  (l.iz : ℝ) / 2 ^ l.dz ≤ z ∧ z ≤ ((l.iz : ℝ) + 1) / 2 ^ l.dz

/-- the scale -/
noncomputable def scale (Dx Dy Dz : Nat) (l : Leaf) : ℝ := 2 ^ (Dx * l.dx + Dy * l.dy + Dz * l.dz)

lemma mono_cast (D a d n : Nat) (h : a ≤ D) :
    ((mono D a d n : Int) : ℝ) = ((n : ℝ) / 2 ^ d) ^ a * 2 ^ (D * d) := by
  unfold mono
  push_cast
  have h2 : (2 : ℝ) ^ (D * d) = 2 ^ (a * d) * 2 ^ ((D - a) * d) := by
    rw [← pow_add]; congr 1
    rw [← Nat.add_mul, Nat.add_sub_cancel' h]
  rw [h2, div_pow, ← pow_mul, mul_comm a d]
  field_simp

lemma pow_mono_between {lo x hi : ℝ} (a : Nat) (h0 : 0 ≤ lo) (h1 : lo ≤ x) (h2 : x ≤ hi) :
    lo ^ a ≤ x ^ a ∧ x ^ a ≤ hi ^ a :=
  ⟨pow_le_pow_left₀ h0 h1 a, pow_le_pow_left₀ (h0.trans h1) h2 a⟩

/-- one coordinate: corner powers bracket the point's power -/
lemma coord_bracket (D a d n : Nat) (x : ℝ) (ha : a ≤ D)
    (hl : (n : ℝ) / 2 ^ d ≤ x) (hu : x ≤ ((n : ℝ) + 1) / 2 ^ d) :
    ((mono D a d n : Int) : ℝ) ≤ x ^ a * 2 ^ (D * d) ∧
    x ^ a * 2 ^ (D * d) ≤ ((mono D a d (n + 1) : Int) : ℝ) := by
  rw [mono_cast D a d n ha, mono_cast D a d (n + 1) ha]
  have h0 : (0 : ℝ) ≤ (n : ℝ) / 2 ^ d := by positivity
  have hp : (0 : ℝ) < 2 ^ (D * d) := by positivity
  have hu' : x ≤ (((n + 1 : ℕ) : ℝ)) / 2 ^ d := by push_cast; exact hu
  obtain ⟨b1, b2⟩ := pow_mono_between a h0 hl hu'
  exact ⟨mul_le_mul_of_nonneg_right b1 hp.le, mul_le_mul_of_nonneg_right b2 hp.le⟩

lemma term_bounds (Dx Dy Dz : Nat) (l : Leaf) (t : Term) (x y z : ℝ)
    (hd : t.2.1 ≤ Dx ∧ t.2.2.1 ≤ Dy ∧ t.2.2.2 ≤ Dz) (hx : InLeaf l x y z) :
    ((lowT Dx Dy Dz l t : Int) : ℝ) ≤ (t.1 : ℝ) * x ^ t.2.1 * y ^ t.2.2.1 * z ^ t.2.2.2 * scale Dx Dy Dz l ∧
    (t.1 : ℝ) * x ^ t.2.1 * y ^ t.2.2.1 * z ^ t.2.2.2 * scale Dx Dy Dz l ≤ ((upT Dx Dy Dz l t : Int) : ℝ) := by
  obtain ⟨c, a, b, e⟩ := t
  obtain ⟨hxl, hxu, hyl, hyu, hzl, hzu⟩ := hx
  obtain ⟨X1, X2⟩ := coord_bracket Dx a l.dx l.ix x hd.1 hxl hxu
  obtain ⟨Y1, Y2⟩ := coord_bracket Dy b l.dy l.iy y hd.2.1 hyl hyu
  obtain ⟨Z1, Z2⟩ := coord_bracket Dz e l.dz l.iz z hd.2.2 hzl hzu
  have hsc : scale Dx Dy Dz l = 2 ^ (Dx * l.dx) * 2 ^ (Dy * l.dy) * 2 ^ (Dz * l.dz) := by
    unfold scale; rw [pow_add, pow_add]
  -- the product of the three scaled coordinate powers
  set PX := x ^ a * 2 ^ (Dx * l.dx)
  set PY := y ^ b * 2 ^ (Dy * l.dy)
  set PZ := z ^ e * 2 ^ (Dz * l.dz)
  have hval : (c : ℝ) * x ^ a * y ^ b * z ^ e * scale Dx Dy Dz l = (c : ℝ) * (PX * PY * PZ) := by
    rw [hsc]; ring
  have m0 : ∀ D k d n, (0 : ℝ) ≤ ((mono D k d n : Int) : ℝ) := by
    intro D k d n; unfold mono; push_cast; positivity
  have lowprod : ((mono Dx a l.dx l.ix : Int) : ℝ) * ((mono Dy b l.dy l.iy : Int) : ℝ) * ((mono Dz e l.dz l.iz : Int) : ℝ)
      ≤ PX * PY * PZ := by
    apply mul_le_mul (mul_le_mul X1 Y1 (m0 _ _ _ _) ((m0 _ _ _ _).trans X1)) Z1 (m0 _ _ _ _)
    exact mul_nonneg ((m0 _ _ _ _).trans X1) ((m0 _ _ _ _).trans Y1)
  have upprod : PX * PY * PZ ≤ ((mono Dx a l.dx (l.ix + 1) : Int) : ℝ) * ((mono Dy b l.dy (l.iy + 1) : Int) : ℝ) *
      ((mono Dz e l.dz (l.iz + 1) : Int) : ℝ) := by
    apply mul_le_mul (mul_le_mul X2 Y2 ((m0 _ _ _ _).trans Y1) (m0 _ _ _ _)) Z2 ((m0 _ _ _ _).trans Z1)
    exact mul_nonneg (m0 _ _ _ _) (m0 _ _ _ _)
  rw [hval]
  unfold lowT upT
  simp only
  split_ifs with hc
  · have hc' : (0 : ℝ) ≤ c := by exact_mod_cast hc
    push_cast
    constructor
    · have := mul_le_mul_of_nonneg_left lowprod hc'; linarith [this]
    · have := mul_le_mul_of_nonneg_left upprod hc'; linarith [this]
  · have hc' : (c : ℝ) ≤ 0 := by push Not at hc; exact_mod_cast hc.le
    push_cast
    constructor
    · have := mul_le_mul_of_nonpos_left upprod hc'; linarith [this]
    · have := mul_le_mul_of_nonpos_left lowprod hc'; linarith [this]

/-- soundness of the enclosure: `low ≤ p * scale ≤ up` on the leaf -/
theorem bounds (Dx Dy Dz : Nat) (p : Poly) (l : Leaf) (x y z : ℝ) (hdeg : degOK Dx Dy Dz p = true)
    (hx : InLeaf l x y z) :
    ((low Dx Dy Dz p l : Int) : ℝ) ≤ evalR p x y z * scale Dx Dy Dz l ∧
    evalR p x y z * scale Dx Dy Dz l ≤ ((up Dx Dy Dz p l : Int) : ℝ) := by
  induction p with
  | nil => simp [low, up, evalR]
  | cons t q ih =>
    simp only [degOK, List.all_cons, Bool.and_eq_true, decide_eq_true_eq] at hdeg
    obtain ⟨⟨⟨h1, h2⟩, h3⟩, hq⟩ := hdeg
    obtain ⟨i1, i2⟩ := ih (by simpa [degOK] using hq)
    obtain ⟨t1, t2⟩ := term_bounds Dx Dy Dz l t x y z ⟨h1, h2, h3⟩ hx
    have el : low Dx Dy Dz (t :: q) l = lowT Dx Dy Dz l t + low Dx Dy Dz q l := by simp [low]
    have eu : up Dx Dy Dz (t :: q) l = upT Dx Dy Dz l t + up Dx Dy Dz q l := by simp [up]
    have ev : evalR (t :: q) x y z = (t.1 : ℝ) * x ^ t.2.1 * y ^ t.2.2.1 * z ^ t.2.2.2 + evalR q x y z := by simp [evalR]
    rw [el, eu, ev, add_mul]
    push_cast
    constructor <;> linarith

/-- a leaf on which `signFixed` holds contains no zero of `p` -/
theorem no_zero (Dx Dy Dz : Nat) (p : Poly) (l : Leaf) (hdeg : degOK Dx Dy Dz p = true)
    (hs : signFixed Dx Dy Dz p l = true) (x y z : ℝ) (hx : InLeaf l x y z) : evalR p x y z ≠ 0 := by
  intro h0
  obtain ⟨b1, b2⟩ := bounds Dx Dy Dz p l x y z hdeg hx
  rw [h0, zero_mul] at b1 b2
  simp only [signFixed, Bool.or_eq_true, decide_eq_true_eq] at hs
  rcases hs with h | h
  · have : (0 : ℝ) < (low Dx Dy Dz p l : ℝ) := by exact_mod_cast h
    linarith
  · have : ((up Dx Dy Dz p l : Int) : ℝ) < 0 := by exact_mod_cast h
    linarith

/-- all leaves of a list pass -/
theorem no_zero_all (Dx Dy Dz : Nat) (p : Poly) (L : List Leaf) (hdeg : degOK Dx Dy Dz p = true)
    (hs : L.all (signFixed Dx Dy Dz p) = true) :
    ∀ l ∈ L, ∀ x y z, InLeaf l x y z → evalR p x y z ≠ 0 := by
  intro l hl x y z hx
  rw [List.all_eq_true] at hs
  exact no_zero Dx Dy Dz p l hdeg (hs l hl) x y z hx

end BoxCheck
