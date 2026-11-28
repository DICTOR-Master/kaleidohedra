module

public import Mathlib
public import LoopEquality.Weighted

@[expose] public section

/-!
# One cycle from two matchings

Two different matchings of four points close into one cycle; a matching with itself does not.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

theorem oneCycle_two {a b c d : ℤ × ℤ} :
    OneCycleRel {a, b, c, d} (pr2 a b ∪ pr2 c d) (pr2 a c ∪ pr2 b d) := by
  intro Q hQ hne hM hN
  obtain ⟨x, hx⟩ := hne
  have mem : ∀ y ∈ ({a, b, c, d} : Finset (ℤ × ℤ)), y ∈ Q → ∀ z ∈ ({a, b, c, d} : Finset (ℤ × ℤ)),
      ((y, z) ∈ pr2 a b ∪ pr2 c d ∨ (y, z) ∈ pr2 a c ∪ pr2 b d) → z ∈ Q := by
    rintro y - hy z hz (h | h)
    · exact hM y hy z hz h
    · exact hN y hy z hz h
  have P : ∀ y z, y ∈ Q → ((y, z) ∈ pr2 a b ∪ pr2 c d ∨ (y, z) ∈ pr2 a c ∪ pr2 b d) → z ∈ Q := by
    intro y z hy h
    have hyS := hQ hy
    have hzS : z ∈ ({a, b, c, d} : Finset (ℤ × ℤ)) := by
      rcases h with h | h <;> simp only [pr2, Finset.mem_union, Finset.mem_product, Finset.mem_insert,
        Finset.mem_singleton] at h <;> simp only [Finset.mem_insert, Finset.mem_singleton] <;> tauto
    exact mem y hyS hy z hzS h
  have step : ∀ y z, y ∈ Q → (y, z) ∈ pr2 a b ∪ pr2 c d ∨ (y, z) ∈ pr2 a c ∪ pr2 b d → z ∈ Q := P
  have hS := hQ hx
  apply Finset.Subset.antisymm hQ
  -- from any point reach a, then everything
  have ha : a ∈ Q := by
    simp only [Finset.mem_insert, Finset.mem_singleton] at hS
    rcases hS with rfl | rfl | rfl | rfl
    · exact hx
    · exact step _ _ hx (Or.inl (by simp [pr2]))
    · exact step _ _ hx (Or.inr (by simp [pr2]))
    · have hb : b ∈ Q := step _ _ hx (Or.inr (by simp [pr2]))
      exact step _ _ hb (Or.inl (by simp [pr2]))
  have hb : b ∈ Q := step _ _ ha (Or.inl (by simp [pr2]))
  have hc : c ∈ Q := step _ _ ha (Or.inr (by simp [pr2]))
  have hd : d ∈ Q := step _ _ hb (Or.inr (by simp [pr2]))
  intro y hy
  simp only [Finset.mem_insert, Finset.mem_singleton] at hy
  rcases hy with rfl | rfl | rfl | rfl <;> assumption

theorem oneCycle_symm {P : Finset (ℤ × ℤ)} {M N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} (h : OneCycleRel P M N) :
    OneCycleRel P N M := fun Q hQ hne h1 h2 => h Q hQ hne h2 h1

theorem not_oneCycle_self {a b c d : ℤ × ℤ} (hD : Dist4 a b c d) :
    ¬ OneCycleRel {a, b, c, d} (pr2 a b ∪ pr2 c d) (pr2 a b ∪ pr2 c d) := by
  obtain ⟨hab, hac, had, hbc, hbd, hcd⟩ := hD
  intro h
  have := h {a, b} (by intro x hx; simp only [Finset.mem_insert, Finset.mem_singleton] at hx ⊢; tauto) ⟨a, by simp⟩
    (by intro p hp q _ hpq
        simp only [pr2, Finset.mem_union, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton] at hp hpq ⊢
        rcases hpq with ⟨-, h⟩ | ⟨h1, -⟩
        · exact h
        · rcases h1 with rfl | rfl <;> rcases hp with h | h <;> simp_all)
    (by intro p hp q _ hpq
        simp only [pr2, Finset.mem_union, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton] at hp hpq ⊢
        rcases hpq with ⟨-, h⟩ | ⟨h1, -⟩
        · exact h
        · rcases h1 with rfl | rfl <;> rcases hp with h | h <;> simp_all)
  have hc : c ∈ ({a, b} : Finset (ℤ × ℤ)) := this ▸ (by simp : c ∈ ({a, b, c, d} : Finset (ℤ × ℤ)))
  simp only [Finset.mem_insert, Finset.mem_singleton] at hc
  rcases hc with h | h
  · exact hac h.symm
  · exact hbc h.symm

/-! ## The value of one shape -/

/-- Weighted root count and far asymmetry of one matching `x y | z t`, from the enumeration. -/
def wR (σ : ℤ → ZMod 3) (k : ℤ) (v : Atom) (m : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) : ℤ :=
  wRootL (mirS σ) (-k) m.1 m.2.1 m.2.2.1 m.2.2.2 6 (mirA v)

def aF (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (m : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) : ℤ :=
  meetCountL σ k (c - m.1) (c - m.2.1) (c - m.2.2.1) (c - m.2.2.2) 6 - meetCountL σ k m.1 m.2.1 m.2.2.1 m.2.2.2 6

/-- The value of the shape `{p₁, p₂, p₃, p₄}`: over ordered pairs of different matchings. -/
def shapeVal (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (v : Atom) (p₁ p₂ p₃ p₄ : ℤ × ℤ) : ℤ :=
  let m₁ := (p₁, p₂, p₃, p₄); let m₂ := (p₁, p₃, p₂, p₄); let m₃ := (p₁, p₄, p₂, p₃)
  wR σ k v m₁ * (aF σ k c m₂ + aF σ k c m₃) + wR σ k v m₂ * (aF σ k c m₁ + aF σ k c m₃) +
    wR σ k v m₃ * (aF σ k c m₁ + aF σ k c m₂)

section
open Classical

theorem wsum {σ : ℤ → ZMod 3} {k : ℤ} (v : Atom) {x y z t : ℤ × ℤ} (hD : Dist4 x y z t) :
    ∑ f ∈ T16 v {x, y, z, t}, Wc σ (posA (sc f) v) k {x, y, z, t} (pr2 x y ∪ pr2 z t) 6 = wR σ k v (x, y, z, t) := by
  obtain ⟨hxy, hxz, hxt, hyz, hyt, hzt⟩ := hD
  have hdis : ∀ p ∈ ({x, y} : Finset (ℤ × ℤ)), ∀ q ∈ ({z, t} : Finset (ℤ × ℤ)), p ≠ q := by
    intro p hp q hq; simp only [Finset.mem_insert, Finset.mem_singleton] at hp hq
    rcases hp with rfl | rfl <;> rcases hq with rfl | rfl <;> assumption
  simp only [Wc_four hdis hxy hzt]
  exact sum_through_eq_weighted _ _ v _ (by simp) (by simp)

theorem asum {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {x y z t : ℤ × ℤ} (hD : Dist4 x y z t)
    (hV : ∀ p ∈ ({x, y, z, t} : Finset (ℤ × ℤ)), (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k) :
    Af σ k c {x, y, z, t} (pr2 x y ∪ pr2 z t) 6 = aF σ k c (x, y, z, t) := by
  obtain ⟨hxy, hxz, hxt, hyz, hyt, hzt⟩ := hD
  have hdis : ∀ p ∈ ({x, y} : Finset (ℤ × ℤ)), ∀ q ∈ ({z, t} : Finset (ℤ × ℤ)), p ≠ q := by
    intro p hp q hq; simp only [Finset.mem_insert, Finset.mem_singleton] at hp hq
    rcases hp with rfl | rfl <;> rcases hq with rfl | rfl <;> assumption
  exact Af_four_enum hc hV hdis hxy hzt 6

end

section
open Classical

/-- **The (6, 6) terms of one shape, summed over the translates of `v`, from the enumeration.** -/
theorem shape_sum {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) (v : Atom) {p₁ p₂ p₃ p₄ : ℤ × ℤ}
    (hD : Dist4 p₁ p₂ p₃ p₄)
    (hV : ∀ p ∈ ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)), (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k) :
    ∑ f ∈ T16 v {p₁, p₂, p₃, p₄}, G16 σ k c (posA (sc f) v) {p₁, p₂, p₃, p₄} = shapeVal σ k c v p₁ p₂ p₃ p₄ := by
  obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
  set S : Finset (ℤ × ℤ) := {p₁, p₂, p₃, p₄} with hSdef
  have hS2 : S = {p₁, p₃, p₂, p₄} := by ext x; simp only [S, Finset.mem_insert, Finset.mem_singleton]; tauto
  have hS3 : S = {p₁, p₄, p₂, p₃} := by ext x; simp only [S, Finset.mem_insert, Finset.mem_singleton]; tauto
  have hS4 : S = {p₁, p₂, p₄, p₃} := by ext x; simp only [S, Finset.mem_insert, Finset.mem_singleton]; tauto
  have hS5 : S = {p₁, p₃, p₄, p₂} := by ext x; simp only [S, Finset.mem_insert, Finset.mem_singleton]; tauto
  have hD1 : Dist4 p₁ p₂ p₃ p₄ := ⟨h12, h13, h14, h23, h24, h34⟩
  have hD2 : Dist4 p₁ p₃ p₂ p₄ := ⟨h13, h12, h14, h23.symm, h34, h24⟩
  have hD3 : Dist4 p₁ p₄ p₂ p₃ := ⟨h14, h12, h13, h24.symm, h34.symm, h23⟩
  set m₁ := pr2 p₁ p₂ ∪ pr2 p₃ p₄
  set m₂ := pr2 p₁ p₃ ∪ pr2 p₂ p₄
  set m₃ := pr2 p₁ p₄ ∪ pr2 p₂ p₃
  -- weighted root counts and asymmetries of the three matchings
  have W1 : ∑ f ∈ T16 v S, Wc σ (posA (sc f) v) k S m₁ 6 = wR σ k v (p₁, p₂, p₃, p₄) := wsum v hD1
  have W2 : ∑ f ∈ T16 v S, Wc σ (posA (sc f) v) k S m₂ 6 = wR σ k v (p₁, p₃, p₂, p₄) := by
    rw [hS2]; exact wsum v hD2
  have W3 : ∑ f ∈ T16 v S, Wc σ (posA (sc f) v) k S m₃ 6 = wR σ k v (p₁, p₄, p₂, p₃) := by
    rw [hS3]; exact wsum v hD3
  have A1 : Af σ k c S m₁ 6 = aF σ k c (p₁, p₂, p₃, p₄) := asum hc hD1 hV
  have A2 : Af σ k c S m₂ 6 = aF σ k c (p₁, p₃, p₂, p₄) := by
    rw [hS2]; exact asum hc hD2 (by rw [← hS2]; exact hV)
  have A3 : Af σ k c S m₃ 6 = aF σ k c (p₁, p₄, p₂, p₃) := by
    rw [hS3]; exact asum hc hD3 (by rw [← hS3]; exact hV)
  -- which pairs close into one cycle
  have o12 : OneCycleRel S m₁ m₂ := oneCycle_two
  have o13 : OneCycleRel S m₁ m₃ := by
    have := oneCycle_two (a := p₁) (b := p₂) (c := p₄) (d := p₃)
    rwa [← hS4, pr2_comm p₄ p₃] at this
  have o23 : OneCycleRel S m₂ m₃ := by
    have := oneCycle_two (a := p₁) (b := p₃) (c := p₄) (d := p₂)
    rwa [← hS5, pr2_comm p₄ p₂, pr2_comm p₃ p₂] at this
  have n11 : ¬ OneCycleRel S m₁ m₁ := not_oneCycle_self hD1
  have n22 : ¬ OneCycleRel S m₂ m₂ := by rw [hS2]; exact not_oneCycle_self hD2
  have n33 : ¬ OneCycleRel S m₃ m₃ := by rw [hS3]; exact not_oneCycle_self hD3
  -- the three matchings are different
  have memc : ∀ {a b x y z w : ℤ × ℤ}, (a, b) ∈ pr2 x y ∪ pr2 z w ↔
      ((a = x ∨ a = y) ∧ (b = x ∨ b = y)) ∨ ((a = z ∨ a = w) ∧ (b = z ∨ b = w)) := by
    intros; simp only [pr2, Finset.mem_union, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton]
  have d12 : m₁ ≠ m₂ := by
    intro h
    have hm : (p₁, p₂) ∈ m₁ := memc.mpr (Or.inl ⟨Or.inl rfl, Or.inr rfl⟩)
    rw [h, memc] at hm
    rcases hm with ⟨-, h1 | h1⟩ | ⟨h1 | h1, -⟩
    · exact h12 h1.symm
    · exact h23 h1
    · exact h12 h1
    · exact h14 h1
  have d13 : m₁ ≠ m₃ := by
    intro h
    have hm : (p₁, p₂) ∈ m₁ := memc.mpr (Or.inl ⟨Or.inl rfl, Or.inr rfl⟩)
    rw [h, memc] at hm
    rcases hm with ⟨-, h1 | h1⟩ | ⟨h1 | h1, -⟩
    · exact h12 h1.symm
    · exact h24 h1
    · exact h12 h1
    · exact h13 h1
  have d23 : m₂ ≠ m₃ := by
    intro h
    have hm : (p₁, p₃) ∈ m₂ := memc.mpr (Or.inl ⟨Or.inl rfl, Or.inr rfl⟩)
    rw [h, memc] at hm
    rcases hm with ⟨-, h1 | h1⟩ | ⟨h1 | h1, -⟩
    · exact h13 h1.symm
    · exact h34 h1
    · exact h12 h1
    · exact h13 h1
  -- assemble
  have hG : ∀ f, G16 σ k c (posA (sc f) v) S = ∑ y ∈ Mt p₁ p₂ p₃ p₄ ×ˢ Mt p₁ p₂ p₃ p₄,
      (if OneCycleRel S y.1 y.2 then Wc σ (posA (sc f) v) k S y.1 6 * Af σ k c S y.2 6 else 0) :=
    fun f => G16_mt _ hD1
  rw [Finset.sum_congr rfl (fun f _ => hG f), Finset.sum_comm]
  have hpull : ∀ y ∈ Mt p₁ p₂ p₃ p₄ ×ˢ Mt p₁ p₂ p₃ p₄,
      ∑ f ∈ T16 v S, (if OneCycleRel S y.1 y.2 then Wc σ (posA (sc f) v) k S y.1 6 * Af σ k c S y.2 6 else 0) =
      if OneCycleRel S y.1 y.2 then (∑ f ∈ T16 v S, Wc σ (posA (sc f) v) k S y.1 6) * Af σ k c S y.2 6 else 0 := by
    intro y _; split_ifs
    · rw [Finset.sum_mul]
    · simp
  rw [Finset.sum_congr rfl hpull, Finset.sum_product]
  have hMt : Mt p₁ p₂ p₃ p₄ = {m₁, m₂, m₃} := rfl
  rw [hMt]
  have nm1 : m₁ ∉ ({m₂, m₃} : Finset _) := by simp [d12, d13]
  have nm2 : m₂ ∉ ({m₃} : Finset _) := by simp [d23]
  simp only [Finset.sum_insert nm1, Finset.sum_insert nm2, Finset.sum_singleton]
  rw [if_neg n11, if_pos o12, if_pos o13, if_pos (oneCycle_symm o12), if_neg n22, if_pos o23,
    if_pos (oneCycle_symm o13), if_pos (oneCycle_symm o23), if_neg n33, W1, W2, W3, A1, A2, A3]
  unfold shapeVal; ring

end

end LoopEqualityProof
