module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.CorollaryA1
public import LoopEquality.Relabel

@[expose] public section

/-!
# Runs of flips (Lean paper, Milestone 2f-2)

`flipFor v σ k` flips the c/h letter of bilayer `k`: by swapping the letters above `k` when `v` is in the
root half of `k` (`flipAt`), and the letters below `k` otherwise (`flipBelow`). Either way the positions on
`v`'s side are kept.

* `flipBelow_hex`, `flipFor_hex`: the c/h letter changes at bilayer `k` and nowhere else.
* `flipFor_isStacking`: the result is a stacking.
* `ncard_polysA1_flipFor`: one such flip keeps the counts at `v`.
* `ncard_polysA1_flipRun`: so does any finite run of them (`flipRun v σ ks`), and the c/h letter of the
  result at bilayer `j` is that of `σ` flipped once for each occurrence of `j` in `ks` (`flipRun_hex`).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem flipBelow_of_le {σ : ℤ → ZMod 3} {k j : ℤ} (h : k ≤ j) : flipBelow σ k j = σ j := by
  simp only [flipBelow, h, ↓reduceIte]

theorem flipBelow_of_lt {σ : ℤ → ZMod 3} {k j : ℤ} (h : j < k) : flipBelow σ k j = tog (σ k) (σ j) := by
  simp only [flipBelow, show ¬ k ≤ j by omega, ↓reduceIte]

theorem mirS_hex {σ : ℤ → ZMod 3} {j : ℤ} : IsHex (mirS σ) (-j) ↔ IsHex σ j := by
  unfold IsHex mirS
  rw [show -(-j - 1) = j + 1 by ring, show -(-j + 1) = j - 1 by ring]
  exact eq_comm

theorem flipBelow_hex {σ : ℤ → ZMod 3} (hσ : IsStacking σ) (k j : ℤ) :
    IsHex (flipBelow σ k) j ↔ (if j = k then ¬ IsHex σ j else IsHex σ j) := by
  rw [← mirS_hex, mirS_flipBelow, flipAt_hex (mirS_isStacking hσ), mirS_hex]
  by_cases h : j = k
  · subst h; simp
  · simp [h, show ¬ (-j = -k) by omega]

theorem flipBelow_isStacking {σ : ℤ → ZMod 3} (hσ : IsStacking σ) (k : ℤ) : IsStacking (flipBelow σ k) := by
  have h := flipAt_isStacking (mirS_isStacking hσ) (-k)
  rw [← mirS_flipBelow] at h
  have h2 := mirS_isStacking h
  rwa [mirS_mirS] at h2

/-- Flip the c/h letter of bilayer `k`, keeping the positions on `v`'s side. -/
noncomputable def flipFor (v : Atom) (σ : ℤ → ZMod 3) (k : ℤ) : ℤ → ZMod 3 :=
  if IsFar k v then flipBelow σ k else flipAt σ k

theorem flipFor_isStacking {v : Atom} {σ : ℤ → ZMod 3} (hσ : IsStacking σ) (k : ℤ) :
    IsStacking (flipFor v σ k) := by
  unfold flipFor; split
  · exact flipBelow_isStacking hσ k
  · exact flipAt_isStacking hσ k

theorem flipFor_hex {v : Atom} {σ : ℤ → ZMod 3} (hσ : IsStacking σ) (k j : ℤ) :
    IsHex (flipFor v σ k) j ↔ (if j = k then ¬ IsHex σ j else IsHex σ j) := by
  unfold flipFor; split
  · exact flipBelow_hex hσ k j
  · exact flipAt_hex hσ k j

theorem ncard_polysA1_flipFor (v : Atom) (σ : ℤ → ZMod 3) (k : ℤ) (l : ℕ) :
    (PolysA1 (flipFor v σ k) v l).ncard = (PolysA1 σ v l).ncard := by
  unfold flipFor; split
  · next h => exact ncard_polysA1_flipBelow h l
  · next h => exact (ncard_polysA1_flip h l).symm

/-- A run of flips, applied from the head of the list. -/
noncomputable def flipRun (v : Atom) : (ℤ → ZMod 3) → List ℤ → ℤ → ZMod 3
  | σ, [] => σ
  | σ, k :: ks => flipRun v (flipFor v σ k) ks

theorem flipRun_isStacking {v : Atom} : ∀ (ks : List ℤ) {σ : ℤ → ZMod 3}, IsStacking σ →
    IsStacking (flipRun v σ ks)
  | [], _, h => h
  | k :: ks, _, h => flipRun_isStacking ks (flipFor_isStacking h k)

/-- **Runs of flips keep the counts.** -/
theorem ncard_polysA1_flipRun (v : Atom) (l : ℕ) : ∀ (ks : List ℤ) (σ : ℤ → ZMod 3),
    (PolysA1 (flipRun v σ ks) v l).ncard = (PolysA1 σ v l).ncard
  | [], _ => rfl
  | k :: ks, σ => by
    show (PolysA1 (flipRun v (flipFor v σ k) ks) v l).ncard = _
    rw [ncard_polysA1_flipRun v l ks, ncard_polysA1_flipFor]

/-- The c/h letter after a run: flipped once for each occurrence of `j` in `ks`. -/
theorem flipRun_hex {v : Atom} : ∀ (ks : List ℤ) {σ : ℤ → ZMod 3}, IsStacking σ → ∀ j : ℤ,
    (IsHex (flipRun v σ ks) j ↔ (IsHex σ j ↔ Even (ks.count j)))
  | [], σ, _, j => by simp [flipRun]
  | k :: ks, σ, hσ, j => by
    show IsHex (flipRun v (flipFor v σ k) ks) j ↔ _
    rw [flipRun_hex ks (flipFor_isStacking hσ k) j, flipFor_hex hσ k j, List.count_cons]
    by_cases h : j = k
    · subst h
      simp only [↓reduceIte, beq_self_eq_true, Nat.even_add_one]
      tauto
    · have h' : (k == j) = false := by simpa [beq_iff_eq] using fun h' : k = j => h h'.symm
      simp only [h, h', ↓reduceIte, Bool.false_eq_true, add_zero]

end LoopEqualityProof
