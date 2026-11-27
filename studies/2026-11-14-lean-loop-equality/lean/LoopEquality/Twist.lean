module

public import Mathlib
public import LoopEquality.Defs

@[expose] public section

/-!
# One flip is one twist (Lean paper, Milestone 1)

#102, Theorem 5, and study 2026-11-15-polygon-bijection, Lemmas 1 and 2, in the coordinates of `Defs.lean`.

* `tog a` fixes the letter `a` and exchanges the other two (`b ↦ 2a − b`).
* `flipAt σ k` is the stacking with the letters above bilayer `k` swapped by `tog (σ k)`. It is again a
  stacking (`flipAt_isStacking`), and its hexagonal/cubic letter changes at bilayer `k` and nowhere else
  (`flipAt_hex`).
* `twist c k` moves the far half (the upper atom of bilayer `k` and everything above) by the half-turn
  `p ↦ c − p`, with `c ≡ 2·σ k` in both coordinates mod 3, and leaves the root half alone.
* Lemma 1 (`flip_is_twist`): the twist carries the sites of `G σ` onto the sites of `G (flipAt σ k)`, and
  within each half it carries bonds to bonds and non-bonds to non-bonds. The root half is unchanged.
* Lemma 2 (`halfturn_two_points`): two points of one position are exchanged by such a half-turn.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

/-- The letter swap at `a`: fixes `a`, exchanges the other two letters. -/
def tog (a b : ZMod 3) : ZMod 3 := 2 * a - b

theorem tog_self (a : ZMod 3) : tog a a = a := by unfold tog; ring

theorem tog_tog (a b : ZMod 3) : tog a (tog a b) = b := by unfold tog; ring

theorem tog_injective (a : ZMod 3) : Function.Injective (tog a) := by
  intro x y h
  have h' := congrArg (tog a) h
  rwa [tog_tog, tog_tog] at h'

theorem tog_ne_self {a b : ZMod 3} (h : b ≠ a) : tog a b ≠ a := by
  intro h'
  apply h
  have := congrArg (tog a) h'
  rwa [tog_tog, tog_self] at this

/-- With `x, y ≠ a`: `x = tog a y` exactly when `x ≠ y` (three letters). -/
theorem eq_tog_iff_ne : ∀ a x y : ZMod 3, x ≠ a → y ≠ a → (x = tog a y ↔ x ≠ y) := by
  unfold tog; decide

/-- The stacking with bilayer `k`'s letter flipped: the letters above `k` swapped by `tog (σ k)`. -/
def flipAt (σ : ℤ → ZMod 3) (k : ℤ) (j : ℤ) : ZMod 3 := if j ≤ k then σ j else tog (σ k) (σ j)

theorem flipAt_of_le {σ : ℤ → ZMod 3} {k j : ℤ} (h : j ≤ k) : flipAt σ k j = σ j := by
  simp only [flipAt, h, ↓reduceIte]

theorem flipAt_of_lt {σ : ℤ → ZMod 3} {k j : ℤ} (h : k < j) : flipAt σ k j = tog (σ k) (σ j) := by
  simp only [flipAt, show ¬ j ≤ k by omega, ↓reduceIte]

theorem flipAt_isStacking {σ : ℤ → ZMod 3} (hσ : IsStacking σ) (k : ℤ) : IsStacking (flipAt σ k) := by
  intro j
  by_cases h1 : j + 1 ≤ k
  · rw [flipAt_of_le h1, flipAt_of_le (by omega)]; exact hσ j
  · by_cases h0 : j ≤ k
    · have hj : j = k := by omega
      subst hj
      rw [flipAt_of_lt (by omega), flipAt_of_le le_rfl]
      exact tog_ne_self (hσ j)
    · rw [flipAt_of_lt (by omega), flipAt_of_lt (by omega)]
      intro h
      exact hσ j (tog_injective _ h)

/-- Bilayer `j` is hexagonal (h) when its two neighbours are in the same position; otherwise cubic (c). -/
def IsHex (σ : ℤ → ZMod 3) (j : ℤ) : Prop := σ (j - 1) = σ (j + 1)

/-- Flipping at `k` changes the c/h letter at bilayer `k` and nowhere else. -/
theorem flipAt_hex {σ : ℤ → ZMod 3} (hσ : IsStacking σ) (k j : ℤ) :
    IsHex (flipAt σ k) j ↔ (if j = k then ¬ IsHex σ j else IsHex σ j) := by
  unfold IsHex
  have hdown : ∀ i, σ (i - 1) ≠ σ i := fun i => by
    have := hσ (i - 1); rw [sub_add_cancel] at this; exact fun h => this h.symm
  by_cases hjk : j = k
  · subst hjk
    simp only [↓reduceIte]
    rw [flipAt_of_le (by omega), flipAt_of_lt (by omega)]
    exact eq_tog_iff_ne _ _ _ (hdown j) (hσ j)
  · simp only [hjk, ↓reduceIte]
    by_cases hlt : j < k
    · rw [flipAt_of_le (by omega), flipAt_of_le (by omega)]
    · by_cases hj1 : j - 1 = k
      · have hj : j = k + 1 := by omega
        subst hj
        rw [flipAt_of_le (by omega), flipAt_of_lt (by omega), hj1]
        constructor
        · intro h
          have h' := congrArg (tog (σ k)) h
          rw [tog_tog, tog_self] at h'
          exact h'
        · intro h
          rw [← h, tog_self]
      · rw [flipAt_of_lt (by omega), flipAt_of_lt (by omega)]
        exact (tog_injective _).eq_iff

/-- The far half above the cut at bilayer `k`: the upper atom of bilayer `k` and everything above it. -/
def IsFar (k : ℤ) (v : Atom) : Prop := k < v.1 ∨ (v.1 = k ∧ v.2.2 = 1)

open Classical in
/-- The half-turn `p ↦ c − p` applied to the far half; the root half stays where it is. -/
noncomputable def twist (c : ℤ × ℤ) (k : ℤ) (v : Atom) : Atom :=
  if IsFar k v then (v.1, c - v.2.1, v.2.2) else v

theorem twist_far {c : ℤ × ℤ} {k : ℤ} {v : Atom} (h : IsFar k v) : twist c k v = (v.1, c - v.2.1, v.2.2) := by
  simp only [twist, h, ↓reduceIte]

theorem twist_root {c : ℤ × ℤ} {k : ℤ} {v : Atom} (h : ¬ IsFar k v) : twist c k v = v := by
  simp only [twist, h, ↓reduceIte]

theorem isFar_twist {c : ℤ × ℤ} {k : ℤ} {v : Atom} : IsFar k (twist c k v) ↔ IsFar k v := by
  by_cases h : IsFar k v
  · rw [twist_far h]; exact Iff.rfl
  · rw [twist_root h]

theorem twist_twist {c : ℤ × ℤ} {k : ℤ} (v : Atom) : twist c k (twist c k v) = v := by
  by_cases h : IsFar k v
  · rw [twist_far h, twist_far (by exact h)]
    obtain ⟨j, p, u⟩ := v
    simp
  · rw [twist_root h, twist_root h]

/-- The centre condition: `c ≡ 2·σ k` in both coordinates, mod 3. -/
def GoodCentre (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) : Prop :=
  ((c.1 : ZMod 3) = 2 * σ k) ∧ ((c.2 : ZMod 3) = 2 * σ k)

theorem twist_isSite {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {v : Atom}
    (hv : IsSite σ v) : IsSite (flipAt σ k) (twist c k v) := by
  obtain ⟨j, ⟨p1, p2⟩, u⟩ := v
  unfold IsSite at hv ⊢
  by_cases hf : IsFar k (j, (p1, p2), u)
  · rw [twist_far hf]
    have hkj : k ≤ j := by unfold IsFar at hf; simp only at hf; omega
    simp only [Prod.fst_sub, Prod.snd_sub, Int.cast_sub, hc.1, hc.2, hv.1, hv.2]
    rcases lt_or_eq_of_le hkj with hlt | heq
    · rw [flipAt_of_lt hlt]; unfold tog; exact ⟨rfl, rfl⟩
    · subst heq; rw [flipAt_of_le le_rfl]; constructor <;> ring
  · rw [twist_root hf]
    have hjk : j ≤ k := by unfold IsFar at hf; simp only at hf; omega
    simp only [flipAt_of_le hjk]; exact hv

theorem neg_mem_shortVecs {x : ℤ × ℤ} (h : x ∈ shortVecs) : -x ∈ shortVecs := by
  simp only [shortVecs, Finset.mem_insert, Finset.mem_singleton] at h ⊢
  rcases h with h | h | h | h | h | h <;> subst h <;> simp

/-- Lemma 1, one direction: within one half, bonds of `G σ` go to bonds of `G (flipAt σ k)`. -/
theorem twist_bond {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {v w : Atom}
    (hs : IsFar k v ↔ IsFar k w) (hvw : Bond σ v w) : Bond (flipAt σ k) (twist c k v) (twist c k w) := by
  obtain ⟨hv, hw, hb⟩ := hvw
  refine ⟨twist_isSite hc hv, twist_isSite hc hw, ?_⟩
  by_cases hf : IsFar k v
  · have hf' : IsFar k w := hs.mp hf
    rw [twist_far hf, twist_far hf']
    obtain ⟨j, p, u⟩ := v
    obtain ⟨j', q, u'⟩ := w
    simp only at hb ⊢
    rcases hb with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩
    · exact Or.inl ⟨h1, by rw [h2], h3⟩
    · refine Or.inr (Or.inl ⟨h1, h2, h3, ?_⟩)
      have : c - q - (c - p) = -(q - p) := by abel
      rw [this]; exact neg_mem_shortVecs h4
    · refine Or.inr (Or.inr ⟨h1, h2, h3, ?_⟩)
      have : c - p - (c - q) = -(p - q) := by abel
      rw [this]; exact neg_mem_shortVecs h4
  · have hf' : ¬ IsFar k w := fun h => hf (hs.mpr h)
    rw [twist_root hf, twist_root hf']
    exact hb

theorem flipAt_flipAt {σ : ℤ → ZMod 3} (k : ℤ) : flipAt (flipAt σ k) k = σ := by
  funext j
  by_cases h : j ≤ k
  · rw [flipAt_of_le h, flipAt_of_le h]
  · rw [not_le] at h
    rw [flipAt_of_lt h, flipAt_of_lt h, flipAt_of_le le_rfl, tog_tog]

theorem goodCentre_flipAt {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) :
    GoodCentre (flipAt σ k) k c := by
  unfold GoodCentre at *; rw [flipAt_of_le le_rfl]; exact hc

/-- **Lemma 1 (one flip is one twist).** Moving the far half by the half-turn `p ↦ c − p`
(`c ≡ 2·σ k`) turns `G σ` into `G (flipAt σ k)`: sites go to sites, the root half is unchanged, and
within each half two atoms are bonded before exactly when their images are bonded after. -/
theorem flip_is_twist {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) :
    (∀ v, IsSite σ v → IsSite (flipAt σ k) (twist c k v)) ∧
    (∀ v, ¬ IsFar k v → twist c k v = v) ∧
    (∀ v w, (IsFar k v ↔ IsFar k w) → (Bond σ v w ↔ Bond (flipAt σ k) (twist c k v) (twist c k w))) := by
  refine ⟨fun v hv => twist_isSite hc hv, fun v hv => twist_root hv, fun v w hs => ⟨twist_bond hc hs, ?_⟩⟩
  intro h
  have hs' : IsFar k (twist c k v) ↔ IsFar k (twist c k w) := by rw [isFar_twist, isFar_twist]; exact hs
  have := twist_bond (goodCentre_flipAt hc) hs' h
  rwa [flipAt_flipAt, twist_twist, twist_twist] at this

/-- **Lemma 2 (two points).** Two points `p, q` of one position `a` are exchanged by the half-turn
`x ↦ (p + q) − x`, whose centre `p + q` satisfies the centre condition for the letter `a`. -/
theorem halfturn_two_points {a : ZMod 3} {p q : ℤ × ℤ}
    (hp : (p.1 : ZMod 3) = a ∧ (p.2 : ZMod 3) = a) (hq : (q.1 : ZMod 3) = a ∧ (q.2 : ZMod 3) = a) :
    (((p + q).1 : ZMod 3) = 2 * a ∧ ((p + q).2 : ZMod 3) = 2 * a) ∧ (p + q) - p = q ∧ (p + q) - q = p := by
  refine ⟨⟨?_, ?_⟩, by abel, by abel⟩
  · simp only [Prod.fst_add, Int.cast_add, hp.1, hq.1]; ring
  · simp only [Prod.snd_add, Int.cast_add, hp.2, hq.2]; ring

end LoopEqualityProof
