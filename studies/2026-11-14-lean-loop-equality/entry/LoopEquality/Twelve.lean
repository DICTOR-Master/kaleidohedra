module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Parts
public import LoopEquality.Counting
public import LoopEquality.Pairings
public import LoopEquality.BSym
public import LoopEquality.Lemma7
public import LoopEquality.SingleArc
public import LoopEquality.Minimal
public import LoopEquality.Parity

@[expose] public section

/-!
# One flip does not change the polygons of length 12 (toward Theorem 5 (a) at l = 12)

In Theorem B (`theoremB_sym`) at `l = 12` every term vanishes: five or more crossing points leave too few edges
(`term_zero_of_large`); an odd number is impossible (`linkage_even`); two points give no far asymmetry (`Fc_two`); with
four points the far side has its minimal size 4 (`Af_min`).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- A linkage has an even number of ends. -/
theorem linkage_even {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B) : Even B.card := by
  have hcl : ∀ e ∈ L, ∀ y ∈ e, y ∈ atomsOf L → ∀ z ∈ e, z ∈ atomsOf L :=
    fun e he _ _ _ z hz => mem_atomsOf.mpr ⟨e, he, hz⟩
  have hs := handshake L (atomsOf L) hL.2.2.2 hcl
  have hB : B ⊆ atomsOf L := by
    intro b hb
    have h1 := hL.1 b hb
    obtain ⟨e, he⟩ := Finset.card_pos.mp (by unfold degS at h1; omega : 0 < (L.filter (fun e => b ∈ e)).card)
    exact mem_atomsOf.mpr ⟨e, (Finset.mem_filter.mp he).1, (Finset.mem_filter.mp he).2⟩
  rw [← Finset.sum_sdiff hB] at hs
  have h1 : ∑ y ∈ B, degS L y = B.card := by
    rw [Finset.card_eq_sum_ones]; exact Finset.sum_congr rfl (fun y hy => hL.1 y hy)
  have h2 : Even (∑ y ∈ atomsOf L \ B, degS L y) := by
    apply Finset.even_sum; intro y hy
    rcases hL.2.1 y (Finset.mem_sdiff.mp hy).2 with h | h <;> rw [h]
    · exact Even.zero
    · exact even_two
  rw [h1] at hs
  obtain ⟨t, ht⟩ := h2
  exact ⟨(L.filter (fun e => ∃ y ∈ atomsOf L, y ∈ e)).card - t, by omega⟩

theorem Fc_odd {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ}
    (h : ¬ Even Q.card) : Fc τ k Q N s = 0 := by
  have e : FarSet τ k Q N s = ∅ := by
    ext F; simp only [FarSet, Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨hF, -, -⟩
    have := linkage_even hF.1
    rw [Finset.card_image_of_injective _ (fun a b h => upA_inj h)] at this
    exact h this
  unfold Fc; rw [e]; simp

theorem Af_odd {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ}
    (h : ¬ Even P.card) : Af σ k c P N s = 0 := by
  unfold Af; rw [Fc_odd h, Fc_odd (by rwa [card_gP])]; simp

theorem term_zero_12 {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    {P : Finset (ℤ × ℤ)} (hP : P ∈ famP σ v 12 k c) {x} (hx : x ∈ idxSet 12 P P (OneCycleRel P)) :
    Aw σ v k c P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 = 0 := by
  have hsum := (Finset.mem_filter.mp hx).2.1
  simp only [famP, Finset.mem_filter] at hP
  obtain ⟨-, hne, hV⟩ := hP
  by_cases hbig : 12 < 3 * P.card
  · exact term_zero_of_large hx hbig
  by_cases hev : Even P.card
  swap
  · rw [Af_odd hev, mul_zero]
  have hpos : 0 < P.card := Finset.card_pos.mpr hne
  obtain ⟨t, ht⟩ := hev
  have h24 : P.card = 2 ∨ P.card = 4 := by omega
  rcases h24 with h2 | h4
  · obtain ⟨a, b, hab, rfl⟩ := Finset.card_eq_two.mp h2
    have ha := bondS_vert_iff.mp (hV a (by simp)); have hb := bondS_vert_iff.mp (hV b (by simp))
    have : Af σ k c {a, b} x.1.2 x.2.2 = 0 := by
      unfold Af; rw [Fc_two hc ha hb]; simp
    rw [this, mul_zero]
  · by_cases hr : x.2.1 < P.card
    · rw [Aw_zero hr, zero_mul]
    by_cases hs : x.2.2 < P.card
    · rw [Af_zero hs, mul_zero]
    have : x.2.2 = P.card := by omega
    rw [this, Af_min hc, mul_zero]

/-- **One flip keeps the polygons of length 12** through any atom below the cut. -/
theorem flip_keeps_12 (σ : ℤ → ZMod 3) (k : ℤ) {v : Atom} (hv : ¬ IsFar k v) :
    (Polys (flipAt σ k) v 12).ncard = (Polys σ v 12).ncard := by
  have h := theoremB_sym (σ := σ) (v := v) (l := 12) (goodCentre_cDefault σ k) hv
  have hz : ∑ P ∈ famP σ v 12 k (cDefault σ k), ∑ x ∈ idxSet 12 P P (OneCycleRel P),
      Aw σ v k (cDefault σ k) P x.1.1 x.2.1 * Af σ k (cDefault σ k) P x.1.2 x.2.2 = 0 :=
    Finset.sum_eq_zero (fun P hP => Finset.sum_eq_zero (fun x hx => term_zero_12 (goodCentre_cDefault σ k) hP hx))
  rw [hz] at h
  omega

/-- Every far linkage has an even number of edges: its lower atoms are not ends, so each has even degree. -/
theorem farL_card_even {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : FarL τ k Q F) :
    Even F.card := by
  rw [card_eq_sum_lower hF.2.2]
  apply Finset.even_sum
  intro x hx
  have hx0 := (Finset.mem_filter.mp hx).2
  have hnot : x ∉ Q.image (upA k) := by
    intro h; obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp h; simp [upA] at hx0
  rcases hF.1.2.1 x hnot with h | h <;> rw [h]
  · exact Even.zero
  · exact even_two

/-- Every root linkage has an even number of edges: its lower atoms are its ends (degree 1, evenly many) and
others of even degree. -/
theorem rootL_card_even {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {R : Finset (Sym2 Atom)} (hR : RootL τ k Q R) :
    Even R.card := by
  rw [card_eq_sum_lower hR.2.2]
  set A := (atomsOf R).filter (fun a => a.2.2 = 0)
  have hB : Q.image (loA k) ⊆ A := by
    intro b hb
    have h1 := hR.1.1 b hb
    obtain ⟨e, he⟩ := Finset.card_pos.mp (by unfold degS at h1; omega : 0 < (R.filter (fun e => b ∈ e)).card)
    obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp hb
    exact Finset.mem_filter.mpr ⟨mem_atomsOf.mpr ⟨e, (Finset.mem_filter.mp he).1, (Finset.mem_filter.mp he).2⟩, rfl⟩
  rw [← Finset.sum_sdiff hB]
  have h1 : ∑ y ∈ Q.image (loA k), degS R y = (Q.image (loA k)).card := by
    rw [Finset.card_eq_sum_ones]; exact Finset.sum_congr rfl (fun y hy => hR.1.1 y hy)
  rw [h1]
  apply Even.add
  · apply Finset.even_sum; intro y hy
    rcases hR.1.2.1 y (Finset.mem_sdiff.mp hy).2 with h | h <;> rw [h]
    · exact Even.zero
    · exact even_two
  · exact linkage_even hR.1

theorem Wc_odd_size {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {P : Finset (ℤ × ℤ)} {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {r : ℕ}
    (h : ¬ Even r) : Wc σ v k P M r = 0 := by
  have e : RootSet σ v k P M r = ∅ := by
    ext R; simp only [RootSet, Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨hR, -, rfl, -⟩; exact h (rootL_card_even hR)
  unfold Wc; rw [e]; simp

theorem Fc_odd_size {σ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ}
    (h : ¬ Even s) : Fc σ k P N s = 0 := by
  have e : FarSet σ k P N s = ∅ := by
    ext F; simp only [FarSet, Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨hF, rfl, -⟩; exact h (farL_card_even hF)
  unfold Fc; rw [e]; simp

theorem Aw_odd_size {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)}
    {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {r : ℕ} (h : ¬ Even r) : Aw σ v k c P M r = 0 := by
  unfold Aw; rw [Wc_odd_size h, Wc_odd_size h]; simp

theorem Af_odd_size {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)}
    {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ} (h : ¬ Even s) : Af σ k c P N s = 0 := by
  unfold Af; rw [Fc_odd_size h, Fc_odd_size h]; simp

end LoopEqualityProof
