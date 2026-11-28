module

public import Mathlib
public import LoopEquality.Regroup
public import LoopEquality.MinRoot

@[expose] public section

/-!
# Toward one flip keeping the polygons of length 16

The surviving terms at `l = 16`: four crossing points, six edges on each side.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- The surviving terms of Theorem B at `l = 16` for the atom `a` and the crossing set `P`. -/
noncomputable def G16 (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (a : Atom) (P : Finset (ℤ × ℤ)) : ℤ :=
  ∑ x ∈ idxSet 16 P P (OneCycleRel P),
    if P.card = 4 ∧ x.2.1 = 6 ∧ x.2.2 = 6 then Wc σ a k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 else 0

theorem trP_as_g (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : trP d P = gP d (gP 0 P) := by
  rw [gP_gP']; simp

theorem trM_as_g (d : ℤ × ℤ) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : trM d M = gM d (gM 0 M) := by
  rw [gM_gM']; simp

theorem idx_tr_mem {l : ℕ} {d : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {x} (hx : x ∈ idxSet l P P (OneCycleRel P)) :
    ((trM d x.1.1, trM d x.1.2), x.2) ∈ idxSet l (trP d P) (trP d P) (OneCycleRel (trP d P)) := by
  rw [trP_as_g, trM_as_g, trM_as_g]
  exact idx_g_mem (c := d) (idx_g_mem (c := 0) hx)

theorem trM_trM_neg (d : ℤ × ℤ) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : trM (-d) (trM d M) = M := trM_neg d M

theorem trP_trP_neg (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : trP (-d) (trP d P) = P := trP_neg d P

theorem card_trP (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : (trP d P).card = P.card := by
  unfold trP; exact Finset.card_image_of_injective _ (fun p q h => by simpa using h)

/-- **The surviving terms are invariant under joint lattice translations.** -/
theorem G16_translate (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) {d : ℤ × ℤ} (hd : GoodVec d) (a : Atom)
    (P : Finset (ℤ × ℤ)) : G16 σ k c (posA d a) (trP d P) = G16 σ k c a P := by
  unfold G16
  symm
  apply Finset.sum_nbij' (fun x => ((trM d x.1.1, trM d x.1.2), x.2)) (fun x => ((trM (-d) x.1.1, trM (-d) x.1.2), x.2))
  · intro x hx; exact idx_tr_mem hx
  · intro x hx; have := idx_tr_mem (d := -d) hx; rwa [trP_trP_neg] at this
  · intro x _; simp [trM_trM_neg]
  · intro x _
    have : ∀ M, trM d (trM (-d) M) = M := fun M => by have := trM_neg (-d) M; rwa [neg_neg] at this
    simp [this]
  · intro x _
    simp only [card_trP]
    split_ifs
    · rw [Wc_translate hd, Af_translate hd]
    · rfl

theorem goodVec_sc (f : ℤ × ℤ) : GoodVec (sc f) := by
  unfold GoodVec sc; push_cast
  constructor <;> rw [show (3 : ZMod 3) = 0 from rfl, zero_mul]

end LoopEqualityProof
