module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist

@[expose] public section

/-!
# The cut and the surgery on edges (Lean paper, Milestone 2a)

Study 2026-11-15-polygon-bijection §1–2.

* `bond_symm`: bonds are symmetric.
* `cut` (the cut lemma): a bond between the far half and the root half at bilayer `k` is the vertical
  bond of bilayer `k`: lower atom `(k, p, 0)` to upper atom `(k, p, 1)`, same planar point `p`.
* `crossing_bond_flip`: such a crossing bond is also a bond of the flipped network.
* `surg c k`: the surgery on one edge (an ordered pair of atoms). A far–far edge is moved by the half-turn;
  root–root edges and crossing bonds stay. `surg_bond`: every bond of `G σ` goes to a bond of
  `G (flipAt σ k)`; `surg_surg`: the surgery undoes itself; `surg_bond_iff`: bonds before exactly when
  bonds after.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

theorem bond_symm {σ : ℤ → ZMod 3} {v w : Atom} (h : Bond σ v w) : Bond σ w v := by
  obtain ⟨hv, hw, hb⟩ := h
  refine ⟨hw, hv, ?_⟩
  rcases hb with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩
  · exact Or.inl ⟨h1.symm, h2.symm, h3.symm⟩
  · exact Or.inr (Or.inr ⟨h1, h2, h3, h4⟩)
  · exact Or.inr (Or.inl ⟨h1, h2, h3, h4⟩)

/-- **The cut lemma.** A bond from the far half to the root half at bilayer `k` is the vertical bond of
bilayer `k`: `v = (k, p, 1)` and `w = (k, p, 0)`. -/
theorem cut {σ : ℤ → ZMod 3} {k : ℤ} {v w : Atom} (h : Bond σ v w) (hv : IsFar k v) (hw : ¬ IsFar k w) :
    v.1 = k ∧ w.1 = k ∧ v.2.1 = w.2.1 ∧ v.2.2 = 1 ∧ w.2.2 = 0 := by
  obtain ⟨-, -, hb⟩ := h
  obtain ⟨j, p, u⟩ := v
  obtain ⟨j', q, u'⟩ := w
  unfold IsFar at hv hw
  simp only at hv hw hb ⊢
  push Not at hw
  rcases hb with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩
  · subst h1; subst h2
    rcases hv with hv | ⟨hv1, hv2⟩
    · omega
    · subst hv1; subst hv2
      refine ⟨rfl, rfl, rfl, rfl, ?_⟩
      fin_cases u' <;> simp_all
  · subst h2
    rcases hv with hv | ⟨hv1, -⟩ <;> omega
  · subst h3
    rcases hv with hv | ⟨-, hv2⟩
    · by_cases hj' : k < j'
      · omega
      · have : j' = k := by omega
        exact absurd (hw.2 ‹_›) (by rw [h2]; decide)
    · exact absurd hv2 (by decide)

/-- A crossing bond is a bond of the flipped network too (it sits at bilayer `k`, whose letter is kept). -/
theorem crossing_bond_flip {σ : ℤ → ZMod 3} {k : ℤ} {v w : Atom} (h : Bond σ v w) (hv : IsFar k v)
    (hw : ¬ IsFar k w) : Bond (flipAt σ k) v w := by
  obtain ⟨h1, h2, h3, h4, h5⟩ := cut h hv hw
  obtain ⟨hsv, hsw, hb⟩ := h
  refine ⟨?_, ?_, hb⟩
  · unfold IsSite at hsv ⊢; rw [h1, flipAt_of_le le_rfl]; rw [h1] at hsv; exact hsv
  · unfold IsSite at hsw ⊢; rw [h2, flipAt_of_le le_rfl]; rw [h2] at hsw; exact hsw

open Classical in
/-- The surgery on one edge: a far–far edge is moved by the half-turn; every other edge stays. -/
noncomputable def surg (c : ℤ × ℤ) (k : ℤ) (e : Atom × Atom) : Atom × Atom :=
  if IsFar k e.1 ∧ IsFar k e.2 then (twist c k e.1, twist c k e.2) else e

theorem surg_far {c : ℤ × ℤ} {k : ℤ} {e : Atom × Atom} (h : IsFar k e.1 ∧ IsFar k e.2) :
    surg c k e = (twist c k e.1, twist c k e.2) := by
  simp only [surg, h, and_self, ↓reduceIte]

theorem surg_other {c : ℤ × ℤ} {k : ℤ} {e : Atom × Atom} (h : ¬ (IsFar k e.1 ∧ IsFar k e.2)) :
    surg c k e = e := by
  simp only [surg, h, ↓reduceIte]

theorem surg_surg {c : ℤ × ℤ} {k : ℤ} (e : Atom × Atom) : surg c k (surg c k e) = e := by
  by_cases h : IsFar k e.1 ∧ IsFar k e.2
  · rw [surg_far h, surg_far ⟨isFar_twist.mpr h.1, isFar_twist.mpr h.2⟩]
    simp only [twist_twist]
  · rw [surg_other h, surg_other h]

theorem surg_injective (c : ℤ × ℤ) (k : ℤ) : Function.Injective (surg c k) := by
  intro x y hxy
  have := congrArg (surg c k) hxy
  rwa [surg_surg, surg_surg] at this

/-- Every bond of `G σ` goes to a bond of `G (flipAt σ k)` under the surgery. -/
theorem surg_bond {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {e : Atom × Atom}
    (h : Bond σ e.1 e.2) : Bond (flipAt σ k) (surg c k e).1 (surg c k e).2 := by
  by_cases hff : IsFar k e.1 ∧ IsFar k e.2
  · rw [surg_far hff]
    exact twist_bond hc ⟨fun _ => hff.2, fun _ => hff.1⟩ h
  · rw [surg_other hff]
    by_cases h1 : IsFar k e.1
    · have h2 : ¬ IsFar k e.2 := fun h2 => hff ⟨h1, h2⟩
      exact crossing_bond_flip h h1 h2
    · by_cases h2 : IsFar k e.2
      · exact bond_symm (crossing_bond_flip (bond_symm h) h2 h1)
      · have := twist_bond (c := c) hc ⟨fun h => absurd h h1, fun h => absurd h h2⟩ h
        rwa [twist_root h1, twist_root h2] at this

/-- Bonds before exactly when bonds after. -/
theorem surg_bond_iff {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) (e : Atom × Atom) :
    Bond σ e.1 e.2 ↔ Bond (flipAt σ k) (surg c k e).1 (surg c k e).2 := by
  refine ⟨surg_bond hc, fun h => ?_⟩
  have := surg_bond (goodCentre_flipAt hc) h
  rwa [flipAt_flipAt, surg_surg] at this

end LoopEqualityProof
