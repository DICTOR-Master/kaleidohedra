module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1
public import LoopEquality.Relabel
public import LoopEquality.FlipRuns
public import LoopEquality.Locality
public import LoopEquality.Assembly
public import LoopEquality.EverySite
public import LoopEquality.TheoremB
public import LoopEquality.Twelve
public import LoopEquality.Short
public import LoopEquality.Parity

@[expose] public section

/-!
# From one flip to every stacking, for any count that one flip keeps (Theorem 5 (a) at l = 12)

`FlipLaw Q l`: one flip (`flipAt`, atom below the cut) keeps the polygons with crossing condition `Q` and `l` edges.
`corollaryFL` is Corollary A's assembly with this as the only input. With `Q` = no condition and `l = 12`
(`flip_keeps_12`): `theorem5a_12`.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

def FlipLaw (Q : (ℤ → ℕ) → Prop) (l : ℕ) : Prop :=
  ∀ (τ : ℤ → ZMod 3) (k : ℤ) (w : Atom), ¬ IsFar k w → (PolysQ Q τ w l).ncard = (PolysQ Q (flipAt τ k) w l).ncard

theorem ncard_polysQ_flipBelow' {Q : (ℤ → ℕ) → Prop} {l : ℕ} (hFm : FlipLaw (mirQ Q) l) {σ : ℤ → ZMod 3} {k : ℤ}
    {v : Atom} (hv : IsFar k v) : (PolysQ Q (flipBelow σ k) v l).ncard = (PolysQ Q σ v l).ncard := by
  rw [ncard_polysQ_mirror Q (flipBelow σ k) v l, mirS_flipBelow, ncard_polysQ_mirror Q σ v l]
  have hroot : ¬ IsFar (-k) (mirA v) := fun h => (isFar_mirA.mp h) hv
  exact (hFm _ _ _ hroot).symm

theorem ncard_polysQ_flipFor' {Q : (ℤ → ℕ) → Prop} {l : ℕ} (hF : FlipLaw Q l) (hFm : FlipLaw (mirQ Q) l)
    (v : Atom) (σ : ℤ → ZMod 3) (k : ℤ) : (PolysQ Q (flipFor v σ k) v l).ncard = (PolysQ Q σ v l).ncard := by
  unfold flipFor; split
  · next h => exact ncard_polysQ_flipBelow' hFm h
  · next h => exact (hF _ _ _ h).symm

theorem ncard_polysQ_flipRun' {Q : (ℤ → ℕ) → Prop} {l : ℕ} (hF : FlipLaw Q l) (hFm : FlipLaw (mirQ Q) l) (v : Atom) :
    ∀ (ks : List ℤ) (σ : ℤ → ZMod 3), (PolysQ Q (flipRun v σ ks) v l).ncard = (PolysQ Q σ v l).ncard
  | [], _ => rfl
  | k :: ks, σ => by
    show (PolysQ Q (flipRun v (flipFor v σ k) ks) v l).ncard = _
    rw [ncard_polysQ_flipRun' hF hFm v ks, ncard_polysQ_flipFor' hF hFm]

theorem corollaryFL {Q : (ℤ → ℕ) → Prop} {l0 : ℕ} (hF : FlipLaw Q l0) (hFm : FlipLaw (mirQ Q) l0) {σ τ : ℤ → ZMod 3} (hσ : IsStacking σ) (hτ : IsStacking τ) {v : Atom}
    (hvσ : IsSite σ v) (hvτ : IsSite τ v) :
    (PolysQ Q σ v l0).ncard = (PolysQ Q τ v l0).ncard := by
  set l := l0
  -- 1. flip the c/h letters that differ on the window
  set W := Finset.Icc (v.1 - (l + 1 : ℕ) + 1) (v.1 + (l + 1 : ℕ)) with hW
  set D := W.filter (fun j => ¬ (IsHex σ j ↔ IsHex τ j)) with hD
  set σ1 := flipRun v σ D.toList with hσ1
  have hσ1s : IsStacking σ1 := flipRun_isStacking _ hσ
  have hcount1 : (PolysQ Q σ1 v l).ncard = (PolysQ Q σ v l).ncard := ncard_polysQ_flipRun' hF hFm v _ σ
  have hhex1 : ∀ j, v.1 - (l + 1 : ℕ) + 1 ≤ j → j ≤ v.1 + (l + 1 : ℕ) → (IsHex σ1 j ↔ IsHex τ j) := by
    intro j h1 h2
    rw [hσ1, flipRun_hex _ hσ j]
    have hjW : j ∈ W := Finset.mem_Icc.mpr ⟨h1, h2⟩
    by_cases hdiff : IsHex σ j ↔ IsHex τ j
    · have : j ∉ D := fun h => (Finset.mem_filter.mp h).2 hdiff
      rw [List.count_eq_zero_of_not_mem (by rwa [Finset.mem_toList])]
      simp only [Nat.even_iff, Nat.zero_mod, iff_true]; exact hdiff
    · have hjD : j ∈ D := Finset.mem_filter.mpr ⟨hjW, hdiff⟩
      rw [List.count_eq_one_of_mem (Finset.nodup_toList D) (by rwa [Finset.mem_toList])]
      simp only [Nat.even_iff, Nat.one_mod]
      tauto
  -- 2. the letter of v's bilayer agrees
  have hv1 : σ1 v.1 = τ v.1 := by rw [hσ1, flipRun_at_v]; exact hvσ.1.symm.trans hvτ.1
  -- 3. locality once the window agrees
  have hloc : ∀ ρ : ℤ → ZMod 3, IsStacking ρ → ρ v.1 = τ v.1 → ρ (v.1 + 1) = τ (v.1 + 1) →
      (∀ j, v.1 - (l + 1 : ℕ) + 1 ≤ j → j ≤ v.1 + (l + 1 : ℕ) → (IsHex ρ j ↔ IsHex τ j)) →
      PolysQ Q ρ v l = PolysQ Q τ v l := by
    intro ρ hρ h0 h1 hh
    apply polysQ_local
    intro j hj1 hj2
    exact eq_window hρ hτ (l + 1) h0 h1 hh j (by push_cast; omega) (by push_cast; omega)
  by_cases hnext : σ1 (v.1 + 1) = τ (v.1 + 1)
  · rw [← hcount1, hloc σ1 hσ1s hv1 hnext hhex1]
  · -- 4. relabel by tog a (a = the letter of v's bilayer), then translate back to v
    obtain ⟨a, ha⟩ : ∃ a, a = σ1 v.1 := ⟨_, rfl⟩
    obtain ⟨ρ, hρ⟩ : ∃ ρ : ℤ → ZMod 3, ρ = fun j => tog a (σ1 j) := ⟨_, rfl⟩
    have hρs : IsStacking ρ := by rw [hρ]; exact isStacking_tog hσ1s a
    have hρ0 : ρ v.1 = τ v.1 := by
      rw [hρ]; show tog a (σ1 v.1) = τ v.1; rw [← ha, tog_self, ha, hv1]
    have hρ1 : ρ (v.1 + 1) = τ (v.1 + 1) := by
      rw [hρ]; show tog a (σ1 (v.1 + 1)) = τ (v.1 + 1)
      have hx : τ (v.1 + 1) ≠ a := by rw [ha, hv1]; exact hτ v.1
      have hy : σ1 (v.1 + 1) ≠ a := by rw [ha]; exact hσ1s v.1
      exact ((eq_tog_iff_ne a _ _ hx hy).mpr (fun h => hnext h.symm)).symm
    have hρhex : ∀ j, v.1 - (l + 1 : ℕ) + 1 ≤ j → j ≤ v.1 + (l + 1 : ℕ) → (IsHex ρ j ↔ IsHex τ j) := by
      intro j h1 h2; rw [hρ, hex_tog]; exact hhex1 j h1 h2
    set c : ℤ × ℤ := (((2 * a).val : ℤ), ((2 * a).val : ℤ)) with hc
    have hcg : (c.1 : ZMod 3) = 2 * a ∧ (c.2 : ZMod 3) = 2 * a := by simp [hc]
    have hrel := ncard_polysQ_relabel Q (σ := σ1) hcg v l
    set d : ℤ × ℤ := v.2.1 + v.2.1 - c with hd
    have hvpos : (v.2.1.1 : ZMod 3) = a ∧ (v.2.1.2 : ZMod 3) = a := by
      rw [ha, hσ1, flipRun_at_v]; exact hvσ
    have hd0 : (d.1 : ZMod 3) = 0 ∧ (d.2 : ZMod 3) = 0 := by
      simp only [hd, Prod.fst_sub, Prod.snd_sub, Prod.fst_add, Prod.snd_add, Int.cast_sub, Int.cast_add,
        hvpos.1, hvpos.2, hcg.1, hcg.2]
      constructor <;> ring
    have htr := ncard_polysQ_translate (Q := Q) (σ := ρ) hd0 (htA c v) l
    have hback : trA d (htA c v) = v := by
      obtain ⟨j, p, u⟩ := v
      simp only [trA, htA, hd]
      congr 1; congr 1; abel
    rw [hback] at htr
    rw [← hcount1, hrel, ← hρ, htr, hloc ρ hρs hρ0 hρ1 hρhex]


theorem polysQ_true (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) : PolysQ (fun _ => True) σ v l = Polys σ v l := by
  ext E; simp [PolysQ, Polys]

theorem mirQ_true : mirQ (fun _ : ℤ → ℕ => True) = fun _ => True := by funext f; rfl

theorem flipLaw_12 : FlipLaw (fun _ => True) 12 := by
  intro τ k w hw; rw [polysQ_true, polysQ_true]; exact (flip_keeps_12 τ k hw).symm

theorem ncard_true_shift (σ : ℤ → ZMod 3) (m : ℤ) (v : Atom) (l : ℕ) :
    (PolysQ (fun _ => True) σ v l).ncard = (PolysQ (fun _ => True) (fun j => σ (j - m)) (shiftA m v) l).ncard := by
  apply ncard_polysQ_iso (shiftA m) (shiftA (-m)) (shiftA_shiftA m)
    (fun a => by have := shiftA_shiftA (-m) a; rwa [neg_neg] at this)
    (fun a b h => bond_shiftA m h)
  · intro a b h
    have := bond_shiftA (-m) h
    simpa using this
  · intro E _; trivial
  · intro E _; trivial

theorem ncard_true_pos (σ : ℤ → ZMod 3) {d : ℤ × ℤ} {s : ZMod 3}
    (hd : (d.1 : ZMod 3) = s ∧ (d.2 : ZMod 3) = s) (v : Atom) (l : ℕ) :
    (PolysQ (fun _ => True) σ v l).ncard = (PolysQ (fun _ => True) (fun j => σ j + s) (posA d v) l).ncard := by
  have hd' : ((-d).1 : ZMod 3) = -s ∧ ((-d).2 : ZMod 3) = -s := by
    refine ⟨?_, ?_⟩ <;> simp only [Prod.fst_neg, Prod.snd_neg, Int.cast_neg, hd.1, hd.2] <;> rfl
  apply ncard_polysQ_iso (posA d) (posA (-d)) (posA_posA d)
    (fun a => by have := posA_posA (-d) a; rwa [neg_neg] at this) (fun a b h => bond_posA hd h)
  · intro a b h
    have := bond_posA hd' h
    have e : (fun j => σ j + s + -s) = σ := by funext j; exact add_neg_cancel_right (σ j) s
    rwa [e] at this
  · intro E _; trivial
  · intro E _; trivial

/-- **Theorem 5 (a) of #102 at l = 12.** For every stacking and every site `v` of it, the polygons through `v` with
12 edges are as many as at diamond's site `(0, (0, 0), 0)`. -/
theorem theorem5a_12 {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) :
    (Polys σ v 12).ncard = (Polys diamond (0, (0, 0), 0) 12).ncard := by
  have hF := flipLaw_12
  have hFm : FlipLaw (mirQ (fun _ => True)) 12 := by rw [mirQ_true]; exact hF
  rw [← polysQ_true, ← polysQ_true]
  obtain ⟨j, p, u⟩ := v
  set σ1 : ℤ → ZMod 3 := fun i => σ (i - -j) with hσ1
  have h1 := ncard_true_shift σ (-j) (j, p, u) 12
  have hs1 : shiftA (-j) (j, p, u) = (0, p, u) := by simp [shiftA]
  rw [hs1] at h1
  have hσ1s : IsStacking σ1 := by
    intro i h
    apply hσ (i + j)
    have h' : σ (i + 1 - -j) = σ (i - -j) := h
    rwa [show i + 1 - -j = i + j + 1 by ring, show i - -j = i + j by ring] at h'
  have hv1 : IsSite σ1 (0, p, u) := by unfold IsSite at hv ⊢; simpa [hσ1] using hv
  obtain ⟨σ2, hσ2s, hv2, h2⟩ : ∃ σ2 : ℤ → ZMod 3, IsStacking σ2 ∧ IsSite σ2 (0, p, 0) ∧
      (PolysQ (fun _ => True) σ1 (0, p, u) 12).ncard = (PolysQ (fun _ => True) σ2 (0, p, 0) 12).ncard := by
    fin_cases u
    · exact ⟨σ1, hσ1s, hv1, rfl⟩
    · refine ⟨mirS σ1, mirS_isStacking hσ1s, ?_, ?_⟩
      · have := isSite_mirA hv1; simpa [mirA] using this
      · have := ncard_polysQ_mirror (fun _ => True) σ1 (0, p, 1) 12
        rw [mirQ_true] at this; simpa [mirA] using this
  have hd : ((-p).1 : ZMod 3) = -σ2 0 ∧ ((-p).2 : ZMod 3) = -σ2 0 := by
    unfold IsSite at hv2; simp only at hv2
    refine ⟨?_, ?_⟩ <;> simp only [Prod.fst_neg, Prod.snd_neg, Int.cast_neg, hv2.1, hv2.2] <;> rfl
  have h3 := ncard_true_pos σ2 hd (0, p, 0) 12
  have hp : posA (-p) (0, p, 0) = (0, (0, 0), 0) := by simp [posA]; rfl
  rw [hp] at h3
  set σ3 : ℤ → ZMod 3 := fun i => σ2 i + -σ2 0 with hσ3
  have hσ3s : IsStacking σ3 := fun i h => hσ2s i (add_right_cancel h)
  have hv3 : IsSite σ3 (0, (0, 0), 0) := by
    unfold IsSite
    refine ⟨?_, ?_⟩ <;> simp only [hσ3, Int.cast_zero] <;> exact (add_neg_cancel _).symm
  have hvd : IsSite diamond (0, (0, 0), 0) := by unfold IsSite diamond; simp
  have h4 := corollaryFL hF hFm hσ3s diamond_isStacking hv3 hvd
  rw [h1, h2, h3, h4]

/-- **Theorem 5 (a) of #102 for l ≤ 13.** -/
theorem theorem5a_upto13 {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) {l : ℕ} (hl : l ≤ 13) :
    (Polys σ v l).ncard = (Polys diamond (0, (0, 0), 0) l).ncard := by
  rcases (show l < 12 ∨ l = 12 ∨ l = 13 by omega) with h | rfl | rfl
  · exact theorem5a_short hσ hv h
  · exact theorem5a_12 hσ hv
  · exact theorem5a_odd σ diamond v _ (by decide)

end LoopEqualityProof
