module

public import Mathlib
public import LoopEquality.Sixteen
public import LoopEquality.Counts

@[expose] public section

/-!
# The (6, 6) terms over the three matchings

For a crossing set `{p₁, p₂, p₃, p₄}`, the root and far pairings that carry linkages are among the three matchings,
so the sum over all pairing relations in `G16` is a sum over pairs of matchings.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

def Mt (p₁ p₂ p₃ p₄ : ℤ × ℤ) : Finset (Finset ((ℤ × ℤ) × (ℤ × ℤ))) :=
  {pr2 p₁ p₂ ∪ pr2 p₃ p₄, pr2 p₁ p₃ ∪ pr2 p₂ p₄, pr2 p₁ p₄ ∪ pr2 p₂ p₃}

def Dist4 (p₁ p₂ p₃ p₄ : ℤ × ℤ) : Prop :=
  p₁ ≠ p₂ ∧ p₁ ≠ p₃ ∧ p₁ ≠ p₄ ∧ p₂ ≠ p₃ ∧ p₂ ≠ p₄ ∧ p₃ ≠ p₄

theorem pr2_congr {a b c d : ℤ × ℤ} (h : ({a, b} : Finset (ℤ × ℤ)) = {c, d}) : pr2 a b = pr2 c d := by
  unfold pr2; rw [h]

theorem pr2_comm (a b : ℤ × ℤ) : pr2 a b = pr2 b a := pr2_congr (Finset.pair_comm a b)

/-- A split `{p₁, b} | {c, d}` of `{p₁, p₂, p₃, p₄}` is one of the three matchings. -/
theorem split_mem_Mt {p₁ p₂ p₃ p₄ b c d : ℤ × ℤ} (hD : Dist4 p₁ p₂ p₃ p₄)
    (hS : ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)) = {p₁, b, c, d})
    (hdis : ∀ p ∈ ({p₁, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c, d} : Finset (ℤ × ℤ)), p ≠ q) (hb : p₁ ≠ b) :
    pr2 p₁ b ∪ pr2 c d ∈ Mt p₁ p₂ p₃ p₄ := by
  obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
  have mS : ∀ x, x ∈ ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)) ↔ (x = p₁ ∨ x = b ∨ x = c ∨ x = d) := fun x => by
    rw [hS]; simp
  have hc1 : c ≠ p₁ := fun h => hdis p₁ (by simp) c (by simp) h.symm
  have hd1 : d ≠ p₁ := fun h => hdis p₁ (by simp) d (by simp) h.symm
  have hcb : c ≠ b := fun h => hdis b (by simp) c (by simp) h.symm
  have hdb : d ≠ b := fun h => hdis b (by simp) d (by simp) h.symm
  have rest : ∀ x, (x = c ∨ x = d) ↔ (x ∈ ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)) ∧ x ≠ p₁ ∧ x ≠ b) := fun x => by
    rw [mS]
    constructor
    · rintro (rfl | rfl)
      · exact ⟨by tauto, hc1, hcb⟩
      · exact ⟨by tauto, hd1, hdb⟩
    · rintro ⟨h, h1, h2⟩; tauto
  have hbS : b ∈ ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)) := (mS b).mpr (by tauto)
  simp only [Finset.mem_insert, Finset.mem_singleton] at hbS
  unfold Mt
  simp only [Finset.mem_insert, Finset.mem_singleton]
  rcases hbS with rfl | rfl | rfl | rfl
  · exact absurd rfl hb
  · left; congr 1; apply pr2_congr; ext x; simp only [Finset.mem_insert, Finset.mem_singleton]
    rw [rest]; simp only [Finset.mem_insert, Finset.mem_singleton]
    constructor
    · rintro ⟨h | h | h | h, h1, h2⟩ <;> first | exact absurd h h1 | exact absurd h h2 | tauto
    · rintro (rfl | rfl) <;> refine ⟨by tauto, ?_, ?_⟩ <;> intro h <;> simp_all
  · right; left; congr 1; apply pr2_congr; ext x; simp only [Finset.mem_insert, Finset.mem_singleton]
    rw [rest]; simp only [Finset.mem_insert, Finset.mem_singleton]
    constructor
    · rintro ⟨h | h | h | h, h1, h2⟩ <;> first | exact absurd h h1 | exact absurd h h2 | tauto
    · rintro (rfl | rfl) <;> refine ⟨by tauto, ?_, ?_⟩ <;> intro h <;> simp_all
  · right; right; congr 1; apply pr2_congr; ext x; simp only [Finset.mem_insert, Finset.mem_singleton]
    rw [rest]; simp only [Finset.mem_insert, Finset.mem_singleton]
    constructor
    · rintro ⟨h | h | h | h, h1, h2⟩ <;> first | exact absurd h h1 | exact absurd h h2 | tauto
    · rintro (rfl | rfl) <;> refine ⟨by tauto, ?_, ?_⟩ <;> intro h <;> simp_all

theorem card_four {p₁ p₂ p₃ p₄ : ℤ × ℤ} (hD : Dist4 p₁ p₂ p₃ p₄) : ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)).card = 4 := by
  obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
  rw [Finset.card_insert_of_notMem (by simp [h12, h13, h14]), Finset.card_insert_of_notMem (by simp [h23, h24]),
    Finset.card_insert_of_notMem (by simp [h34]), Finset.card_singleton]

/-- Far pairings carrying linkages are matchings. -/
theorem pairF_mem_Mt {τ : ℤ → ZMod 3} {k : ℤ} {p₁ p₂ p₃ p₄ : ℤ × ℤ} (hD : Dist4 p₁ p₂ p₃ p₄)
    {F : Finset (Sym2 Atom)} (hF : FarL τ k {p₁, p₂, p₃, p₄} F) : pairF k F {p₁, p₂, p₃, p₄} ∈ Mt p₁ p₂ p₃ p₄ := by
  obtain ⟨b, c, d, hS, hdis, hb, -, he⟩ := pairF_four hF (card_four hD) (by simp : p₁ ∈ ({p₁, p₂, p₃, p₄} : Finset _))
  rw [he]; exact split_mem_Mt hD hS hdis hb

theorem Fc_ne_zero_mem {τ : ℤ → ZMod 3} {k : ℤ} {p₁ p₂ p₃ p₄ : ℤ × ℤ} (hD : Dist4 p₁ p₂ p₃ p₄)
    {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ} (h : Fc τ k {p₁, p₂, p₃, p₄} N s ≠ 0) : N ∈ Mt p₁ p₂ p₃ p₄ := by
  obtain ⟨F, hF⟩ : (FarSet τ k {p₁, p₂, p₃, p₄} N s).Nonempty := by
    rw [Set.nonempty_iff_ne_empty]; intro h0; apply h; unfold Fc; rw [h0]; simp
  rw [← hF.2.2]; exact pairF_mem_Mt hD hF.1

theorem dist4_g {p₁ p₂ p₃ p₄ : ℤ × ℤ} (c : ℤ × ℤ) (hD : Dist4 p₁ p₂ p₃ p₄) :
    Dist4 (c - p₁) (c - p₂) (c - p₃) (c - p₄) := by
  obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> intro h <;> simp_all

theorem gM_Mt {p₁ p₂ p₃ p₄ : ℤ × ℤ} (c : ℤ × ℤ) {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))}
    (h : M ∈ Mt (c - p₁) (c - p₂) (c - p₃) (c - p₄)) : gM c M ∈ Mt p₁ p₂ p₃ p₄ := by
  unfold Mt at h ⊢
  simp only [Finset.mem_insert, Finset.mem_singleton] at h ⊢
  rcases h with rfl | rfl | rfl <;> simp [gM_union, gM_pr2, sub_sub_cancel]

theorem Af_ne_zero_mem {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {p₁ p₂ p₃ p₄ : ℤ × ℤ} (hD : Dist4 p₁ p₂ p₃ p₄)
    {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ} (h : Af σ k c {p₁, p₂, p₃, p₄} N s ≠ 0) : N ∈ Mt p₁ p₂ p₃ p₄ := by
  unfold Af at h
  by_cases h1 : Fc σ k {p₁, p₂, p₃, p₄} N s = 0
  · rw [h1, zero_sub, neg_ne_zero] at h
    rw [gP_quad] at h
    have := Fc_ne_zero_mem (dist4_g c hD) h
    have := gM_Mt c this
    rwa [gM_gM] at this
  · exact Fc_ne_zero_mem hD h1

theorem Wc_ne_zero_mem {σ : ℤ → ZMod 3} {a : Atom} {k : ℤ} {p₁ p₂ p₃ p₄ : ℤ × ℤ} (hD : Dist4 p₁ p₂ p₃ p₄)
    {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {r : ℕ} (h : Wc σ a k {p₁, p₂, p₃, p₄} M r ≠ 0) : M ∈ Mt p₁ p₂ p₃ p₄ := by
  obtain ⟨R, hR⟩ : (RootSet σ a k {p₁, p₂, p₃, p₄} M r).Nonempty := by
    rw [Set.nonempty_iff_ne_empty]; intro h0; apply h; unfold Wc; rw [h0]; simp
  obtain ⟨h1, h2⟩ := rootL_mir hR.1
  rw [← hR.2.2.2, ← h2]; exact pairF_mem_Mt hD h1

/-- **`G16` over pairs of matchings.** -/
theorem G16_mt {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (a : Atom) {p₁ p₂ p₃ p₄ : ℤ × ℤ} (hD : Dist4 p₁ p₂ p₃ p₄) :
    G16 σ k c a {p₁, p₂, p₃, p₄} =
      ∑ y ∈ Mt p₁ p₂ p₃ p₄ ×ˢ Mt p₁ p₂ p₃ p₄, if OneCycleRel {p₁, p₂, p₃, p₄} y.1 y.2 then
        Wc σ a k {p₁, p₂, p₃, p₄} y.1 6 * Af σ k c {p₁, p₂, p₃, p₄} y.2 6 else 0 := by
  set S : Finset (ℤ × ℤ) := {p₁, p₂, p₃, p₄}
  have hS4 : S.card = 4 := card_four hD
  have hsub : ∀ M ∈ Mt p₁ p₂ p₃ p₄, M ⊆ S ×ˢ S := by
    intro M hM
    unfold Mt at hM; simp only [Finset.mem_insert, Finset.mem_singleton] at hM
    intro x hx
    rcases hM with rfl | rfl | rfl <;>
    · simp only [pr2, Finset.mem_union, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton] at hx
      simp only [S, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton]; tauto
  unfold G16
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

end LoopEqualityProof
