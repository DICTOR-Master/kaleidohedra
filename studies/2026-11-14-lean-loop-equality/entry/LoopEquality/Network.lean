module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Graph

@[expose] public section

/-!
# The neighbours of an atom in the tetrahedral network of a stacking

`triD` is the triangle `D = {t, t - a₁, t - a₂}` of #102 (here `(1,1)`,
`(-2,1)`, `(1,-2)`), and `sd σ k d` is `d` or `-d` according as
`σ (k+1) - σ k` is `1` or `2` (the sign `ε_k` of #102). `nbr σ v` lists the
four neighbours of `v`; the formula is used at every atom (sites and
non-sites alike), which makes the neighbour graph 4-regular everywhere.

* `regular`: the graph `nbr σ` is symmetric, loopless and 4-regular.
* `bond_iff`: at a site of a stacking, `Bond σ v w ↔ w ∈ nbr σ v`.
-/

namespace LoopEqualityProof

open Finset

/-- The triangle `D` of the three shortest vectors of `Λ + t`. -/
def triD : Finset (ℤ × ℤ) := {(1, 1), (-2, 1), (1, -2)}

/-- `d` if `σ (k+1) - σ k = 1`, and `-d` otherwise. -/
def sd (σ : ℤ → ZMod 3) (k : ℤ) (d : ℤ × ℤ) : ℤ × ℤ :=
  if σ (k + 1) - σ k = 1 then d else -d

theorem sd_injective (σ : ℤ → ZMod 3) (k : ℤ) : Function.Injective (sd σ k) := by
  intro d d' h
  unfold sd at h
  split_ifs at h
  · exact h
  · exact neg_injective h

/-- The four neighbours of an atom. -/
def nbr (σ : ℤ → ZMod 3) (v : Atom) : Finset Atom :=
  if v.2.2 = 0 then
    insert (v.1, v.2.1, 1) (triD.image fun d => (v.1 - 1, v.2.1 - sd σ (v.1 - 1) d, 1))
  else
    insert (v.1, v.2.1, 0) (triD.image fun d => (v.1 + 1, v.2.1 + sd σ v.1 d, 0))

theorem nbr_lower (σ : ℤ → ZMod 3) (k : ℤ) (p : ℤ × ℤ) :
    nbr σ (k, p, 0) = insert (k, p, 1) (triD.image fun d => (k - 1, p - sd σ (k - 1) d, 1)) := by
  simp [nbr]

theorem nbr_upper (σ : ℤ → ZMod 3) (k : ℤ) (p : ℤ × ℤ) :
    nbr σ (k, p, 1) = insert (k, p, 0) (triD.image fun d => (k + 1, p + sd σ k d, 0)) := by
  simp [nbr]

theorem fin2_cases (u : Fin 2) : u = 0 ∨ u = 1 := by fin_cases u <;> simp

theorem triD_card : triD.card = 3 := by decide

theorem regular (σ : ℤ → ZMod 3) : Graph.IsRegular (nbr σ) 3 where
  symm := by
    rintro ⟨k, p, u⟩ ⟨k', q, u'⟩ h
    rcases fin2_cases u with rfl | rfl
    · rw [nbr_lower] at h
      simp only [mem_insert, mem_image, Prod.mk.injEq] at h
      rcases h with ⟨rfl, rfl, rfl⟩ | ⟨d, hd, rfl, rfl, rfl⟩
      · rw [nbr_upper]; exact mem_insert_self _ _
      · rw [nbr_upper]; exact mem_insert_of_mem (mem_image.2 ⟨d, hd, by simp⟩)
    · rw [nbr_upper] at h
      simp only [mem_insert, mem_image, Prod.mk.injEq] at h
      rcases h with ⟨rfl, rfl, rfl⟩ | ⟨d, hd, rfl, rfl, rfl⟩
      · rw [nbr_lower]; exact mem_insert_self _ _
      · rw [nbr_lower]; exact mem_insert_of_mem (mem_image.2 ⟨d, hd, by simp⟩)
  irrefl := by
    rintro ⟨k, p, u⟩
    rcases fin2_cases u with rfl | rfl
    · rw [nbr_lower]; simp
    · rw [nbr_upper]; simp
  card := by
    rintro ⟨k, p, u⟩
    rcases fin2_cases u with rfl | rfl
    · rw [nbr_lower, card_insert_of_notMem (by simp), card_image_of_injective, triD_card]
      intro d d' h
      simp only [Prod.mk.injEq, sub_right_inj, true_and, and_true] at h
      exact sd_injective σ _ h
    · rw [nbr_upper, card_insert_of_notMem (by simp), card_image_of_injective, triD_card]
      intro d d' h
      simp only [Prod.mk.injEq, add_right_inj, true_and, and_true] at h
      exact sd_injective σ _ h

/-! ## Residues mod 3 -/

theorem triD_mod {d : ℤ × ℤ} (hd : d ∈ triD) : (d.1 : ZMod 3) = 1 ∧ (d.2 : ZMod 3) = 1 := by
  simp only [triD, mem_insert, mem_singleton] at hd
  rcases hd with rfl | rfl | rfl <;> decide

theorem stack_diff (a b : ZMod 3) (h : b ≠ a) (h1 : ¬ b - a = 1) : b - a = -1 := by
  revert a b; decide

theorem sd_mod {σ : ℤ → ZMod 3} (hσ : IsStacking σ) (k : ℤ) {d : ℤ × ℤ} (hd : d ∈ triD) :
    ((sd σ k d).1 : ZMod 3) = σ (k + 1) - σ k ∧ ((sd σ k d).2 : ZMod 3) = σ (k + 1) - σ k := by
  obtain ⟨h1, h2⟩ := triD_mod hd
  unfold sd
  split_ifs with h
  · rw [h1, h2, h]; simp
  · have := stack_diff _ _ (hσ k) h
    rw [this]
    constructor
    · show ((-d.1 : ℤ) : ZMod 3) = -1
      rw [Int.cast_neg, h1]; rfl
    · show ((-d.2 : ℤ) : ZMod 3) = -1
      rw [Int.cast_neg, h2]; rfl

theorem sd_short (σ : ℤ → ZMod 3) (k : ℤ) {d : ℤ × ℤ} (hd : d ∈ triD) : sd σ k d ∈ shortVecs := by
  simp only [triD, mem_insert, mem_singleton] at hd
  unfold sd
  split_ifs <;> rcases hd with rfl | rfl | rfl <;> decide

theorem exists_sd {σ : ℤ → ZMod 3} (hσ : IsStacking σ) (k : ℤ) {δ : ℤ × ℤ} (hδ : δ ∈ shortVecs)
    (hm : (δ.1 : ZMod 3) = σ (k + 1) - σ k) : ∃ d ∈ triD, sd σ k d = δ := by
  have hs := hσ k
  unfold sd
  generalize σ (k + 1) = b at hm hs
  generalize σ k = a at hm hs
  simp only [shortVecs, mem_insert, mem_singleton] at hδ
  revert a b
  rcases hδ with rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-! ## Bonds are the neighbours -/

theorem isSite_iff (σ : ℤ → ZMod 3) (k : ℤ) (p : ℤ × ℤ) (u : Fin 2) :
    IsSite σ (k, p, u) ↔ (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k := Iff.rfl

theorem bond_iff {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v w : Atom} (hv : IsSite σ v) :
    Bond σ v w ↔ w ∈ nbr σ v := by
  obtain ⟨k, p, u⟩ := v
  obtain ⟨k', q, u'⟩ := w
  rw [isSite_iff] at hv
  unfold Bond
  rw [isSite_iff, isSite_iff]
  rcases fin2_cases u with rfl | rfl
  · rw [nbr_lower]
    simp only [mem_insert, mem_image, Prod.mk.injEq]
    constructor
    · rintro ⟨-, hw, h⟩
      rcases h with ⟨rfl, rfl, hu⟩ | ⟨-, h01, -⟩ | ⟨rfl, rfl, -, hs⟩
      · left
        rcases fin2_cases u' with rfl | rfl
        · exact absurd rfl hu
        · exact ⟨rfl, rfl, rfl⟩
      · exact absurd h01 (by decide)
      · right
        obtain ⟨d, hd, he⟩ := exists_sd hσ k' hs (by
          simp only [Prod.fst_sub, Int.cast_sub, hv.1, hw.1])
        refine ⟨d, hd, by ring, ?_, rfl⟩
        rw [add_sub_cancel_right, he]; abel
    · rintro (⟨rfl, rfl, rfl⟩ | ⟨d, hd, rfl, rfl, rfl⟩)
      · exact ⟨hv, hv, Or.inl ⟨rfl, rfl, by decide⟩⟩
      · obtain ⟨m1, m2⟩ := sd_mod hσ (k - 1) hd
        rw [sub_add_cancel] at m1 m2
        refine ⟨hv, ⟨?_, ?_⟩, Or.inr (Or.inr ⟨by ring, by simp, by simp, ?_⟩)⟩
        · simp only [Prod.fst_sub, Int.cast_sub, hv.1, m1]; ring
        · simp only [Prod.snd_sub, Int.cast_sub, hv.2, m2]; ring
        · simp only [sub_sub_cancel]; exact sd_short σ _ hd
  · rw [nbr_upper]
    simp only [mem_insert, mem_image, Prod.mk.injEq]
    constructor
    · rintro ⟨-, hw, h⟩
      rcases h with ⟨rfl, rfl, hu⟩ | ⟨rfl, -, rfl, hs⟩ | ⟨-, -, h10, -⟩
      · left
        rcases fin2_cases u' with rfl | rfl
        · exact ⟨rfl, rfl, rfl⟩
        · exact absurd rfl hu
      · right
        obtain ⟨d, hd, he⟩ := exists_sd hσ k hs (by
          simp only [Prod.fst_sub, Int.cast_sub, hv.1, hw.1])
        refine ⟨d, hd, rfl, ?_, rfl⟩
        rw [he]; abel
      · exact absurd h10 (by decide)
    · rintro (⟨rfl, rfl, rfl⟩ | ⟨d, hd, rfl, rfl, rfl⟩)
      · exact ⟨hv, hv, Or.inl ⟨rfl, rfl, by decide⟩⟩
      · obtain ⟨m1, m2⟩ := sd_mod hσ k hd
        refine ⟨hv, ⟨?_, ?_⟩, Or.inr (Or.inl ⟨by simp, by simp, by simp, ?_⟩)⟩
        · simp only [Prod.fst_add, Int.cast_add, hv.1, m1]; ring
        · simp only [Prod.snd_add, Int.cast_add, hv.2, m2]; ring
        · simp only [add_sub_cancel_left]; exact sd_short σ _ hd

theorem site_of_mem_nbr {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v w : Atom} (hv : IsSite σ v)
    (hw : w ∈ nbr σ v) : IsSite σ w :=
  ((bond_iff hσ hv).2 hw).2.1

end LoopEqualityProof
