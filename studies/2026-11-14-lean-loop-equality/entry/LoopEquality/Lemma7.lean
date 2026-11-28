module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Parts
public import LoopEquality.Counting
public import LoopEquality.Pairings
public import LoopEquality.BSym

@[expose] public section

/-!
# Toward Lemma 7 of #102: few crossings for short polygons

* `card_ends_le`: a linkage none of whose edges joins two of its ends has at least as many edges as ends.
* Root and far linkages ending at a crossing set `P` have at least `|P|` edges (two atoms of the cut on the same
  side are never bonded).
* `term_zero_of_large`: in Theorem B (`theoremB_symmetric`), every term with `3 |P| > l` is zero; so for
  `l ≤ 20` only crossing sets with at most 6 points contribute (#102, Lemma 7, first part).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem card_ends_le {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B)
    (hno : ∀ e ∈ L, ∀ a ∈ B, ∀ b ∈ B, a ∈ e → b ∈ e → a = b) : B.card ≤ L.card := by
  have hone : ∀ b ∈ B, ∃ e ∈ L, b ∈ e := fun b hb => by
    have := hL.1 b hb
    obtain ⟨e, he⟩ := Finset.card_pos.mp (by unfold degS at this; omega : 0 < (L.filter (fun e => b ∈ e)).card)
    exact ⟨e, (Finset.mem_filter.mp he).1, (Finset.mem_filter.mp he).2⟩
  choose! f hfL hfb using hone
  apply Finset.card_le_card_of_injOn f (fun b hb => hfL b hb)
  intro a ha b hb hab
  exact hno (f a) (hfL a ha) a ha b hb (hfb a ha) (hab ▸ hfb b hb)

theorem not_bond_loA {σ : ℤ → ZMod 3} {k : ℤ} {p q : ℤ × ℤ} : ¬ Bond σ (loA k p) (loA k q) := by
  rintro ⟨-, -, h⟩; unfold loA at h; simp at h

theorem not_bond_upA {σ : ℤ → ZMod 3} {k : ℤ} {p q : ℤ × ℤ} : ¬ Bond σ (upA k p) (upA k q) := by
  rintro ⟨-, -, h⟩; unfold upA at h; simp at h

theorem rootL_card {σ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} {R : Finset (Sym2 Atom)} (hR : RootL σ k P R) :
    P.card ≤ R.card := by
  have hc : (P.image (loA k)).card = P.card := Finset.card_image_of_injective _ (fun a b h => loA_inj h)
  rw [← hc]
  apply card_ends_le hR.1
  intro e he a ha b hb hae hbe
  obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp ha; obtain ⟨q, -, rfl⟩ := Finset.mem_image.mp hb
  by_contra hne
  have hbd := hR.2.2 e he
  induction e using Sym2.ind with
  | _ x y =>
    rw [bondS_mk] at hbd
    rcases Sym2.mem_iff.mp hae with rfl | rfl <;> rcases Sym2.mem_iff.mp hbe with h | h
    · exact hne h.symm
    · subst h; exact not_bond_loA hbd
    · subst h; exact not_bond_loA hbd
    · exact hne h.symm

theorem farL_card {σ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : FarL σ k P F) :
    P.card ≤ F.card := by
  have hc : (P.image (upA k)).card = P.card := Finset.card_image_of_injective _ (fun a b h => upA_inj h)
  rw [← hc]
  apply card_ends_le hF.1
  intro e he a ha b hb hae hbe
  obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp ha; obtain ⟨q, -, rfl⟩ := Finset.mem_image.mp hb
  by_contra hne
  have hbd := hF.2.2 e he
  induction e using Sym2.ind with
  | _ x y =>
    rw [bondS_mk] at hbd
    rcases Sym2.mem_iff.mp hae with rfl | rfl <;> rcases Sym2.mem_iff.mp hbe with h | h
    · exact hne h.symm
    · subst h; exact not_bond_upA hbd
    · subst h; exact not_bond_upA hbd
    · exact hne h.symm

theorem Wc_zero {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {P : Finset (ℤ × ℤ)} {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {r : ℕ}
    (h : r < P.card) : Wc σ v k P M r = 0 := by
  have e : RootSet σ v k P M r = ∅ := by
    ext R; simp only [RootSet, Set.mem_setOf_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨hR, -, hr, -⟩; have := rootL_card hR; omega
  unfold Wc; rw [e]; simp

theorem Fc_zero {σ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ}
    (h : s < P.card) : Fc σ k P N s = 0 := by
  have e : FarSet σ k P N s = ∅ := by
    ext F; simp only [FarSet, Set.mem_setOf_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨hF, hs, -⟩; have := farL_card hF; omega
  unfold Fc; rw [e]; simp

theorem Aw_zero {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)}
    {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {r : ℕ} (h : r < P.card) : Aw σ v k c P M r = 0 := by
  unfold Aw; rw [Wc_zero h, Wc_zero (by rw [card_gP]; exact h)]; simp

theorem Af_zero {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)}
    {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ} (h : s < P.card) : Af σ k c P N s = 0 := by
  unfold Af; rw [Fc_zero h, Fc_zero (by rw [card_gP]; exact h)]; simp

/-- **#102, Lemma 7, first part.** In Theorem B, a term whose crossing set has more than `l / 3` points is zero:
each side then has fewer edges than crossing points. So for `l ≤ 20` only crossing sets of at most 6 points count. -/
theorem term_zero_of_large {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} {l : ℕ} {P : Finset (ℤ × ℤ)} {x}
    (hx : x ∈ idxSet l P P (OneCycleRel P)) (hP : l < 3 * P.card) :
    Aw σ v k c P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 = 0 := by
  have hsum := (Finset.mem_filter.mp hx).2.1
  by_cases hr : x.2.1 < P.card
  · rw [Aw_zero hr, zero_mul]
  · rw [Af_zero (by omega), mul_zero]

end LoopEqualityProof
