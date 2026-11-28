module

public import Mathlib
public import LoopEquality.Fourteen

@[expose] public section

/-!
# Terms with a minimal root side cancel, at every length

The argument of `Fourteen.lean` for any `l`: over the crossing sets of Theorem B, the terms whose root linkage has as
many edges as there are crossing points sum to zero (split by the centre of the arc at `v`; for each centre, the
half-turn about it followed by the middle swap reverses the sign).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- The minimal-root terms at one centre. -/
noncomputable def fmin (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (c c' : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : ℤ :=
  ∑ x ∈ idxSet l P P (OneCycleRel P),
    if x.2.1 = P.card then Wcen (mirS σ) (-k) (mirA v) c' P x.1.1 * Af σ k c P x.1.2 x.2.2 else 0

theorem fmin_g {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c c' : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hc' : GoodCentre σ k c') (P : Finset (ℤ × ℤ)) : fmin σ v l k c c' (gP c' P) = - fmin σ v l k c c' P := by
  unfold fmin
  rw [← Finset.sum_neg_distrib]
  symm
  apply Finset.sum_nbij' (fun x => ((gM c' x.1.1, gM c' x.1.2), x.2)) (fun x => ((gM c' x.1.1, gM c' x.1.2), x.2))
  · intro x hx; exact idx_g_mem hx
  · intro x hx; have := idx_g_mem (c := c') hx; rwa [gP_gP] at this
  · intro x _; simp [gM_gM]
  · intro x _; simp [gM_gM]
  · intro x _
    simp only [card_gP]
    split_ifs
    · rw [Wcen_g (good_mirS hc'), Af_any_centre hc hc']; ring
    · simp

theorem fmin_support {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c c' : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hv : ¬ IsFar k v) {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p))
    (h : fmin σ v l k c c' P ≠ 0) : P ⊆ window v l := by
  unfold fmin at h
  obtain ⟨x, hx, hne⟩ := Finset.exists_ne_zero_of_sum_ne_zero h
  split_ifs at hne with hcond
  · have hW := left_ne_zero_of_mul hne
    have hA := right_ne_zero_of_mul hne
    have hx' := Finset.mem_filter.mp hx
    have hWc : Wc σ v k P x.1.1 x.2.1 ≠ 0 := by
      unfold Wcen at hW
      obtain ⟨F, hF, hw, -⟩ := Set.nonempty_of_ncard_ne_zero (by exact_mod_cast hW)
      rw [hcond, Wc_mir]
      have hfin : ({F | F ∈ FarSet (mirS σ) (-k) P x.1.1 P.card ∧ 0 < degS F (mirA v)} :
          Set (Finset (Sym2 Atom))).Finite := (minFar_finite _ _ P x.1.1).subset (fun F hF => hF.1)
      have := (Set.ncard_pos hfin).mpr ⟨F, hF, hw⟩
      exact_mod_cast this.ne'
    have := window_of_term hc hv hP hV hx'.2.2 hWc hA
    rwa [hx'.2.1] at this
  · exact absurd rfl hne

theorem fmin_sum {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c c' : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hc' : GoodCentre σ k c') (hv : ¬ IsFar k v) : ∑ P ∈ famP σ v l k c, fmin σ v l k c c' P = 0 := by
  rw [← Finset.sum_filter_ne_zero]
  apply Finset.sum_involution (fun P _ => gP c' P)
  · intro P _; rw [fmin_g hc hc']; ring
  · intro P _ hne heq
    have := fmin_g (v := v) (l := l) hc hc' P; rw [heq] at this
    exact hne (by linarith)
  · intro P hP
    obtain ⟨hP1, hP2⟩ := Finset.mem_filter.mp hP
    simp only [famP, Finset.mem_filter, Finset.mem_powerset] at hP1
    obtain ⟨-, hne, hV⟩ := hP1
    have hV' : ∀ p ∈ gP c' P, BondS σ (vert k p) := fun p hp => by
      have := bondS_vert_g hc' (hV _ (mem_gP.mp hp)); rwa [sub_sub_cancel] at this
    have hne' : (gP c' P).Nonempty := by
      obtain ⟨q, hq⟩ := hne; exact ⟨c' - q, mem_gP.mpr (by rwa [sub_sub_cancel])⟩
    have hf : fmin σ v l k c c' (gP c' P) ≠ 0 := by rw [fmin_g hc hc']; exact neg_ne_zero.mpr hP2
    refine Finset.mem_filter.mpr ⟨?_, hf⟩
    simp only [famP, Finset.mem_filter, Finset.mem_powerset]
    exact ⟨(fmin_support hc hv hne' hV' hf).trans Finset.subset_union_left, hne', hV'⟩
  · intro P _; exact gP_gP c' P

/-- **The minimal-root terms of Theorem B sum to zero, at every length.** -/
theorem minRoot_zero {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hv : ¬ IsFar k v) :
    ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l P P (OneCycleRel P),
      (if x.2.1 = P.card then Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 else 0) = 0 := by
  have e1 : ∀ P ∈ famP σ v l k c,
      ∑ x ∈ idxSet l P P (OneCycleRel P), (if x.2.1 = P.card then Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 else 0) =
      ∑ c' ∈ cenSet (mirA v), ∑ x ∈ idxSet l P P (OneCycleRel P), (if x.2.1 = P.card then
        Wcen (mirS σ) (-k) (mirA v) c' P x.1.1 * Af σ k c P x.1.2 x.2.2 else 0) := fun P _ => by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl; intro x _
    split_ifs with h
    · rw [h, Wc_cen, Finset.sum_mul]
    · simp
  rw [Finset.sum_congr rfl e1, Finset.sum_comm]
  apply Finset.sum_eq_zero; intro c' _
  by_cases hg : GoodCentre σ k c'
  · have := fmin_sum (v := v) (l := l) hc hg hv; unfold fmin at this; exact this
  · apply Finset.sum_eq_zero; intro P hP; apply Finset.sum_eq_zero; intro x _
    simp only [famP, Finset.mem_filter] at hP
    split_ifs
    · rw [Wcen_bad hP.2.2 hg, zero_mul]
    · rfl

end LoopEqualityProof
