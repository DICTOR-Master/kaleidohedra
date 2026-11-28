module

public import Mathlib
public import LoopEquality.Complete16

@[expose] public section

/-!
# l = 16: the fast form of the shape values and the kind of `v`

With Claude (Anthropic).
-/

namespace LoopEqualityProof

def wR4 (σ : ℤ → ZMod 3) (k : ℤ) (v : Atom) (m : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) : ℤ :=
  wRoot4 (mirS σ) (-k) m.1 m.2.1 m.2.2.1 m.2.2.2 (mirA v)

def aF4 (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (m : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) : ℤ :=
  meet4 σ k (c - m.1) (c - m.2.1) (c - m.2.2.1) (c - m.2.2.2) - meet4 σ k m.1 m.2.1 m.2.2.1 m.2.2.2

def shapeVal4 (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (v : Atom) (p₁ p₂ p₃ p₄ : ℤ × ℤ) : ℤ :=
  let m₁ := (p₁, p₂, p₃, p₄); let m₂ := (p₁, p₃, p₂, p₄); let m₃ := (p₁, p₄, p₂, p₃)
  wR4 σ k v m₁ * (aF4 σ k c m₂ + aF4 σ k c m₃) + wR4 σ k v m₂ * (aF4 σ k c m₁ + aF4 σ k c m₃) +
    wR4 σ k v m₃ * (aF4 σ k c m₁ + aF4 σ k c m₂)

theorem sub_ne_sub {c a b : ℤ × ℤ} (h : a ≠ b) : c - a ≠ c - b := fun e => h (by simpa using e)

theorem shapeVal_eq4 {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {v : Atom} {p₁ p₂ p₃ p₄ : ℤ × ℤ}
    (hD : Dist4 p₁ p₂ p₃ p₄) : shapeVal σ k c v p₁ p₂ p₃ p₄ = shapeVal4 σ k c v p₁ p₂ p₃ p₄ := by
  obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
  unfold shapeVal shapeVal4 wR aF wR4 aF4
  dsimp only
  rw [wRootL_eq h12 h34, wRootL_eq h13 h24, wRootL_eq h14 h23,
    meetCountL_eq h12 h34, meetCountL_eq h13 h24, meetCountL_eq h14 h23,
    meetCountL_eq (sub_ne_sub h12) (sub_ne_sub h34), meetCountL_eq (sub_ne_sub h13) (sub_ne_sub h24),
    meetCountL_eq (sub_ne_sub h14) (sub_ne_sub h23)]

/-! ## The kind of `v` -/

theorem typB_congr {w w' : Atom} (h1 : w.1 = w'.1) (h2 : w.2.2 = w'.2.2) (h3 : (w.2.1.1 - w'.2.1.1) % 3 = 0)
    (h4 : (w.2.1.2 - w'.2.1.2) % 3 = 0) (y : Atom) : typB w y = typB w' y := by
  have e1 : ((y.2.1.1 - w.2.1.1) % 3 == 0) = ((y.2.1.1 - w'.2.1.1) % 3 == 0) := by
    rw [Bool.eq_iff_iff]; simp only [beq_iff_eq]; omega
  have e2 : ((y.2.1.2 - w.2.1.2) % 3 == 0) = ((y.2.1.2 - w'.2.1.2) % 3 == 0) := by
    rw [Bool.eq_iff_iff]; simp only [beq_iff_eq]; omega
  unfold typB; rw [h1, h2, e1, e2]

theorem wR4_congr {σ : ℤ → ZMod 3} {k : ℤ} {v v' : Atom} (h1 : v.1 = v'.1) (h2 : v.2.2 = v'.2.2)
    (h3 : (v.2.1.1 - v'.2.1.1) % 3 = 0) (h4 : (v.2.1.2 - v'.2.1.2) % 3 = 0) (m) : wR4 σ k v m = wR4 σ k v' m := by
  unfold wR4 wRoot4
  have : typB (mirA v) = typB (mirA v') := funext (typB_congr (by simp [mirA, h1]) (by simp [mirA, h2]) h3 h4)
  rw [this]

theorem shapeVal4_congr {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {v v' : Atom} (h1 : v.1 = v'.1) (h2 : v.2.2 = v'.2.2)
    (h3 : (v.2.1.1 - v'.2.1.1) % 3 = 0) (h4 : (v.2.1.2 - v'.2.1.2) % 3 = 0) (p₁ p₂ p₃ p₄ : ℤ × ℤ) :
    shapeVal4 σ k c v p₁ p₂ p₃ p₄ = shapeVal4 σ k c v' p₁ p₂ p₃ p₄ := by
  unfold shapeVal4; simp only [wR4_congr (σ := σ) (k := k) h1 h2 h3 h4]

/-- Root arcs of at most four edges meet only bilayers `k - 1` and `k`: for `v` elsewhere the weight is 0. -/
theorem wR4_zero {σ : ℤ → ZMod 3} {k : ℤ} {v : Atom} (hv : v.1 ≠ k ∧ v.1 ≠ k - 1) (m) : wR4 σ k v m = 0 := by
  unfold wR4 wRoot4
  simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
  have hz : ∀ i, 2 ≤ i → i ≤ 4 → ∀ x ∈ ((arcList (mirS σ) (-k) m.1 m.2.1 i) ×ˢ (arcList (mirS σ) (-k) m.2.2.1 m.2.2.2 (6 - i))).filter
      (fun x => disjB x.1 x.2), ((x.1 ++ x.2).countP (typB (mirA v)) : ℤ) = 0 := by
    intro i hi2 hi x hx
    obtain ⟨hp, -⟩ := List.mem_filter.mp hx
    obtain ⟨h1, h2⟩ := List.mem_product.mp hp
    rw [Nat.cast_eq_zero, List.countP_eq_zero]
    intro y hy hty
    simp only [typB, mirA, Bool.and_eq_true, beq_iff_eq] at hty
    have hl : -k ≤ y.1 ∧ y.1 ≤ -k + 1 := by
      rcases List.mem_append.mp hy with hy | hy
      · exact arc_layer hi (mem_arcList.mp h1) hy
      · exact arc_layer (show 6 - i ≤ 4 by omega) (mem_arcList.mp h2) hy
    have := hty.1.1.1
    omega
  rw [List.map_congr_left (hz 2 (by omega) (by omega)), List.map_congr_left (hz 4 (by omega) (by omega))]
  simp

end LoopEqualityProof
