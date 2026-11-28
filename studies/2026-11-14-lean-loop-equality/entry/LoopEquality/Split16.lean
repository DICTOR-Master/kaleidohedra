module

public import Mathlib
public import LoopEquality.LetterLocal
public import LoopEquality.Final16
public import LoopEquality.Complete16

@[expose] public section

/-!
# l = 16 with the root side and the far side read in two stackings

`G16 σ` is `G16b σR σF` for any `σR` agreeing with `σ` on bilayers `k - 1, k` and `σF` agreeing on `k, k + 1`
(`G16_eq_b`); the shape values are then products of a root weight computed in `σR` and a far asymmetry computed in
`σF`, so each is evaluated once.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

noncomputable def G16b (σR σF : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (a : Atom) (P : Finset (ℤ × ℤ)) : ℤ :=
  ∑ x ∈ idxSet 16 P P (OneCycleRel P),
    if P.card = 4 ∧ x.2.1 = 6 ∧ x.2.2 = 6 then Wc σR a k P x.1.1 x.2.1 * Af σF k c P x.1.2 x.2.2 else 0

theorem G16_eq_b {σ σR σF : ℤ → ZMod 3} {k : ℤ} (hm : σ (k - 1) = σR (k - 1)) (h0 : σ k = σR k)
    (h0' : σ k = σF k) (h1 : σ (k + 1) = σF (k + 1)) (c : ℤ × ℤ) (a : Atom) (P : Finset (ℤ × ℤ)) :
    G16 σ k c a P = G16b σR σF k c a P := by
  unfold G16 G16b
  apply Finset.sum_congr rfl; intro x _
  split_ifs with hcond
  · rw [hcond.2.1, hcond.2.2, Wc6_congr h0 hm a hcond.1, Af6_congr h0' h1 c hcond.1]
  · rfl

def shapeValB (σR σF : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (v : Atom) (p₁ p₂ p₃ p₄ : ℤ × ℤ) : ℤ :=
  let m₁ := (p₁, p₂, p₃, p₄); let m₂ := (p₁, p₃, p₂, p₄); let m₃ := (p₁, p₄, p₂, p₃)
  wR σR k v m₁ * (aF σF k c m₂ + aF σF k c m₃) + wR σR k v m₂ * (aF σF k c m₁ + aF σF k c m₃) +
    wR σR k v m₃ * (aF σF k c m₁ + aF σF k c m₂)

def shapeVal4B (σR σF : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (v : Atom) (p₁ p₂ p₃ p₄ : ℤ × ℤ) : ℤ :=
  let m₁ := (p₁, p₂, p₃, p₄); let m₂ := (p₁, p₃, p₂, p₄); let m₃ := (p₁, p₄, p₂, p₃)
  wR4 σR k v m₁ * (aF4 σF k c m₂ + aF4 σF k c m₃) + wR4 σR k v m₂ * (aF4 σF k c m₁ + aF4 σF k c m₃) +
    wR4 σR k v m₃ * (aF4 σF k c m₁ + aF4 σF k c m₂)

theorem shapeValB_eq4 {σR σF : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {v : Atom} {p₁ p₂ p₃ p₄ : ℤ × ℤ}
    (hD : Dist4 p₁ p₂ p₃ p₄) : shapeValB σR σF k c v p₁ p₂ p₃ p₄ = shapeVal4B σR σF k c v p₁ p₂ p₃ p₄ := by
  obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
  unfold shapeValB shapeVal4B wR aF wR4 aF4
  dsimp only
  rw [wRootL_eq h12 h34, wRootL_eq h13 h24, wRootL_eq h14 h23,
    meetCountL_eq h12 h34, meetCountL_eq h13 h24, meetCountL_eq h14 h23,
    meetCountL_eq (sub_ne_sub h12) (sub_ne_sub h34), meetCountL_eq (sub_ne_sub h13) (sub_ne_sub h24),
    meetCountL_eq (sub_ne_sub h14) (sub_ne_sub h23)]

theorem shapeVal4B_congr {σR σF : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {v v' : Atom} (h1 : v.1 = v'.1)
    (h2 : v.2.2 = v'.2.2) (h3 : (v.2.1.1 - v'.2.1.1) % 3 = 0) (h4 : (v.2.1.2 - v'.2.1.2) % 3 = 0)
    (p₁ p₂ p₃ p₄ : ℤ × ℤ) : shapeVal4B σR σF k c v p₁ p₂ p₃ p₄ = shapeVal4B σR σF k c v' p₁ p₂ p₃ p₄ := by
  unfold shapeVal4B; simp only [wR4_congr (σ := σR) (k := k) h1 h2 h3 h4]

/-- **`G16b` over pairs of matchings.** -/
theorem G16b_mt {σR σF : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (a : Atom) {p₁ p₂ p₃ p₄ : ℤ × ℤ} (hD : Dist4 p₁ p₂ p₃ p₄) :
    G16b σR σF k c a {p₁, p₂, p₃, p₄} =
      ∑ y ∈ Mt p₁ p₂ p₃ p₄ ×ˢ Mt p₁ p₂ p₃ p₄, if OneCycleRel {p₁, p₂, p₃, p₄} y.1 y.2 then
        Wc σR a k {p₁, p₂, p₃, p₄} y.1 6 * Af σF k c {p₁, p₂, p₃, p₄} y.2 6 else 0 := by
  set S : Finset (ℤ × ℤ) := {p₁, p₂, p₃, p₄}
  have hS4 : S.card = 4 := card_four hD
  have hsub : ∀ M ∈ Mt p₁ p₂ p₃ p₄, M ⊆ S ×ˢ S := by
    intro M hM
    unfold Mt at hM; simp only [Finset.mem_insert, Finset.mem_singleton] at hM
    intro x hx
    rcases hM with rfl | rfl | rfl <;>
    · simp only [pr2, Finset.mem_union, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton] at hx
      simp only [S, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton]; tauto
  unfold G16b
  apply Finset.sum_bij_ne_zero (fun x _ _ => (x.1.1, x.1.2))
  · intro x hx hne
    rw [hS4] at hne
    split_ifs at hne with hcond
    · have hW := left_ne_zero_of_mul hne
      have hA := right_ne_zero_of_mul hne
      exact Finset.mem_product.mpr ⟨Wc_ne_zero_mem hD hW, Af_ne_zero_mem hD hA⟩
    · exact absurd rfl hne
  · intro x hx hne y hy hne' hxy
    rw [hS4] at hne hne'
    split_ifs at hne hne' with h1 h2 h2
    · simp only [Prod.mk.injEq] at hxy
      obtain ⟨⟨M, N⟩, r, s⟩ := x; obtain ⟨⟨M', N'⟩, r', s'⟩ := y
      simp only at h1 h2 hxy ⊢
      rw [hxy.1, hxy.2, h1.2.1, h1.2.2, h2.2.1, h2.2.2]
    all_goals exact absurd rfl (by assumption)
  · intro y hy hne
    split_ifs at hne with hoc
    · refine ⟨((y.1, y.2), (6, 6)), ?_, ?_, rfl⟩
      · simp only [idxSet, Finset.mem_filter, Finset.mem_product, Finset.mem_powerset, Finset.mem_range]
        obtain ⟨h1, h2⟩ := Finset.mem_product.mp hy
        exact ⟨⟨⟨hsub _ h1, hsub _ h2⟩, by omega, by omega⟩, by rw [hS4], hoc⟩
      · simp only [hS4, and_self, if_true, ne_eq]; exact hne
    · exact absurd rfl hne
  · intro x hx hne
    rw [hS4] at hne ⊢
    split_ifs at hne ⊢ with hcond hoc
    · rw [hcond.2.1, hcond.2.2]
    all_goals first | rfl | exact absurd (Finset.mem_filter.mp hx).2.2 ‹_› | exact absurd rfl hne

section
open Classical

/-- **The same with the root side read in `σR` and the far side in `σF`.** -/
theorem shape_sum2 {σR σF : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σF k c) (v : Atom) {p₁ p₂ p₃ p₄ : ℤ × ℤ}
    (hD : Dist4 p₁ p₂ p₃ p₄)
    (hV : ∀ p ∈ ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)), (p.1 : ZMod 3) = σF k ∧ (p.2 : ZMod 3) = σF k) :
    ∑ f ∈ T16 v {p₁, p₂, p₃, p₄}, G16b σR σF k c (posA (sc f) v) {p₁, p₂, p₃, p₄} = shapeValB σR σF k c v p₁ p₂ p₃ p₄ := by
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
  have W1 : ∑ f ∈ T16 v S, Wc σR (posA (sc f) v) k S m₁ 6 = wR σR k v (p₁, p₂, p₃, p₄) := wsum v hD1
  have W2 : ∑ f ∈ T16 v S, Wc σR (posA (sc f) v) k S m₂ 6 = wR σR k v (p₁, p₃, p₂, p₄) := by
    rw [hS2]; exact wsum v hD2
  have W3 : ∑ f ∈ T16 v S, Wc σR (posA (sc f) v) k S m₃ 6 = wR σR k v (p₁, p₄, p₂, p₃) := by
    rw [hS3]; exact wsum v hD3
  have A1 : Af σF k c S m₁ 6 = aF σF k c (p₁, p₂, p₃, p₄) := asum hc hD1 hV
  have A2 : Af σF k c S m₂ 6 = aF σF k c (p₁, p₃, p₂, p₄) := by
    rw [hS2]; exact asum hc hD2 (by rw [← hS2]; exact hV)
  have A3 : Af σF k c S m₃ 6 = aF σF k c (p₁, p₄, p₂, p₃) := by
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
  have hG : ∀ f, G16b σR σF k c (posA (sc f) v) S = ∑ y ∈ Mt p₁ p₂ p₃ p₄ ×ˢ Mt p₁ p₂ p₃ p₄,
      (if OneCycleRel S y.1 y.2 then Wc σR (posA (sc f) v) k S y.1 6 * Af σF k c S y.2 6 else 0) :=
    fun f => G16b_mt _ hD1
  rw [Finset.sum_congr rfl (fun f _ => hG f), Finset.sum_comm]
  have hpull : ∀ y ∈ Mt p₁ p₂ p₃ p₄ ×ˢ Mt p₁ p₂ p₃ p₄,
      ∑ f ∈ T16 v S, (if OneCycleRel S y.1 y.2 then Wc σR (posA (sc f) v) k S y.1 6 * Af σF k c S y.2 6 else 0) =
      if OneCycleRel S y.1 y.2 then (∑ f ∈ T16 v S, Wc σR (posA (sc f) v) k S y.1 6) * Af σF k c S y.2 6 else 0 := by
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
  unfold shapeValB; ring

/-- **Completeness, with the root side in `σR` and the far side in `σF`.** -/
theorem G16b_complete {σR σF : ℤ → ZMod 3} {k : ℤ} (hk : σR k = σF k) {c : ℤ × ℤ} (hc : GoodCentre σF k c)
    (v : Atom) {b₀ : ℤ × ℤ} (hb₀ : (b₀.1 : ZMod 3) = σF k ∧ (b₀.2 : ZMod 3) = σF k) {Z : Finset (Finset (ℤ × ℤ))}
    (hcheck : ∀ q ∈ candQuads σF k b₀, nrm (toSet q) ∈ Z ∧ nrm (gP c (toSet q)) ∈ Z) :
    ∀ P, G16b σR σF k c v P ≠ 0 → nrm P ∈ Z := by
  intro P h
  unfold G16b at h
  obtain ⟨x, -, hne⟩ := Finset.exists_ne_zero_of_sum_ne_zero h
  split_ifs at hne with hcond
  swap
  · exact absurd rfl hne
  have hW := left_ne_zero_of_mul hne
  have hA := right_ne_zero_of_mul hne
  rw [hcond.2.2] at hA
  obtain ⟨p₁, p₂, p₃, p₄, hD, rfl⟩ := exists_four hcond.1
  have hV : ∀ p ∈ ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)), (p.1 : ZMod 3) = σF k ∧ (p.2 : ZMod 3) = σF k :=
    fun p hp => by rw [← hk]; exact bondS_vert_iff.mp (bonds_of_Wc hW p hp)
  have hN := Af_ne_zero_mem hD hA
  obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
  unfold Mt at hN
  simp only [Finset.mem_insert, Finset.mem_singleton] at hN
  rcases hN with e | e | e <;> rw [e] at hA
  · exact class_in_Z hc hb₀ hcheck ⟨h12, h13, h14, h23, h24, h34⟩ hV hA
  · rw [quad_perm2] at hA hV ⊢
    exact class_in_Z hc hb₀ hcheck ⟨h13, h12, h14, h23.symm, h34, h24⟩ hV hA
  · rw [quad_perm3] at hA hV ⊢
    exact class_in_Z hc hb₀ hcheck ⟨h14, h12, h13, h24.symm, h34.symm, h23⟩ hV hA

end

end LoopEqualityProof
