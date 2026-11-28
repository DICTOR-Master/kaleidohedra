module

public import Mathlib
public import LoopEquality.Data16

@[expose] public section

/-!
# One flip keeps the polygons of length 16; Theorem 5 (a) for l ≤ 17

The (6, 6) sum is regrouped by shape classes (`sum16_regroup`), the shape list is complete (`G16_complete` with the
kernel check `hcheck16`), each class's terms over the translates of `v` are the computable `shapeVal4`
(`shape_sum`, `shapeVal_eq4`), which see only the letters of bilayers `-1, 0, 1` (`G16_congr`) and the kind of `v`; the
kernel check `sum16_kernel` gives zero for every pattern and kind.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- From a zero sum of root-count times far-asymmetry terms, one flip keeps the polygons. -/
theorem flip_of_sum (σ : ℤ → ZMod 3) (k : ℤ) {v : Atom} (hv : ¬ IsFar k v) (l : ℕ)
    (hK : ∑ P ∈ famP σ v l k (cDefault σ k), ∑ x ∈ idxSet l P P (OneCycleRel P),
      Wc σ v k P x.1.1 x.2.1 * Af σ k (cDefault σ k) P x.1.2 x.2.2 = 0) :
    (Polys (flipAt σ k) v l).ncard = (Polys σ v l).ncard := by
  set c := cDefault σ k
  have hc : GoodCentre σ k c := goodCentre_cDefault σ k
  have h := theoremB_sym (σ := σ) (v := v) (l := l) hc hv
  have hz : ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l P P (OneCycleRel P),
      Aw σ v k c P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 = 0 := by
    simp only [Aw, sub_mul, Finset.sum_sub_distrib]
    have h2 : ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l P P (OneCycleRel P),
        Wc σ v k (gP c P) (gM c x.1.1) x.2.1 * Af σ k c P x.1.2 x.2.2 = 0 := by
      have e : ∀ P, ∑ x ∈ idxSet l P P (OneCycleRel P), Wc σ v k (gP c P) (gM c x.1.1) x.2.1 * Af σ k c P x.1.2 x.2.2 =
          - ∑ x ∈ idxSet l (gP c P) (gP c P) (OneCycleRel (gP c P)),
            Wc σ v k (gP c P) x.1.1 x.2.1 * Af σ k c (gP c P) x.1.2 x.2.2 := fun P => by rw [sum_g]; ring
      rw [Finset.sum_congr rfl (fun P _ => e P), Finset.sum_neg_distrib, neg_eq_zero, ← hK]
      apply Finset.sum_nbij' (gP c) (gP c)
      · intro P hP; exact famP_g hc hP
      · intro P hP; exact famP_g hc hP
      · intro P _; exact gP_gP c P
      · intro P _; exact gP_gP c P
      · intro P _; rfl
    rw [hK, h2, sub_zero]
  rw [hz] at h; omega

theorem site_of_Wc {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {P : Finset (ℤ × ℤ)} {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))}
    {r : ℕ} (h : Wc σ v k P M r ≠ 0) : IsSite σ v := by
  obtain ⟨R, hR⟩ : (RootSet σ v k P M r).Nonempty := by
    rw [Set.nonempty_iff_ne_empty]; intro h0; apply h; unfold Wc; rw [h0]; simp
  obtain ⟨e, he, hve⟩ := exists_edge_of_degS hR.2.1
  have hb := hR.1.2.2 e he
  induction e using Sym2.ind with
  | _ x y =>
    rw [bondS_mk] at hb
    rcases Sym2.mem_iff.mp hve with rfl | rfl
    · exact hb.1
    · exact hb.2.1

theorem res_zero {p : ℤ} (h : p % 3 = 0) : (p : ZMod 3) = 0 :=
  (ZMod.intCast_zmod_eq_zero_iff_dvd p 3).mpr (Int.dvd_of_emod_eq_zero h)

/-- **The (6, 6) sum vanishes** (bilayer 0, letter 0). -/
theorem sumG16_zero (σ : ℤ → ZMod 3) (h0 : σ 0 = 0) {v : Atom} (hv : ¬ IsFar 0 v) :
    ∑ P ∈ famP σ v 16 0 (cDefault σ 0), G16 σ 0 (cDefault σ 0) v P = 0 := by
  have hc0 : cDefault σ 0 = (0, 0) := by unfold cDefault; rw [h0]; simp
  rw [hc0]
  have hc : GoodCentre σ 0 (0, 0) := by rw [← hc0]; exact goodCentre_cDefault σ 0
  by_cases hs : IsSite σ v
  swap
  · apply Finset.sum_eq_zero; intro P _
    unfold G16; apply Finset.sum_eq_zero; intro x _
    split_ifs
    · by_contra hne; exact hs (site_of_Wc (left_ne_zero_of_mul hne))
    · rfl
  set a := σ (-1); set b := σ 1
  have hagree : ∀ (w : Atom) (P : Finset (ℤ × ℤ)), G16 σ 0 (0, 0) w P = G16b (sigR a) (sigF b) 0 (0, 0) w P :=
    fun w P => G16_eq_b (by simp [sigR, a]) (by simp [sigR, h0]) (by simp [sigF, h0]) (by simp [sigF, b]) _ w P
  have hc' : GoodCentre (sigF b) 0 (0, 0) := by unfold GoodCentre sigF; simp
  have hk : sigR a 0 = sigF b 0 := by simp [sigR, sigF]
  set L := zqOf b
  have hprops := zq_props b
  unfold propsB at hprops
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at hprops
  obtain ⟨hnd, hq⟩ := hprops
  have hcheck : ∀ q ∈ candQuads (sigF b) 0 (0, 0), nrm (toSet q) ∈ Zf L ∧ nrm (gP (0, 0) (toSet q)) ∈ Zf L :=
    hcheckF b
  have hZ : ∀ P, G16 σ 0 (0, 0) v P ≠ 0 → nrm P ∈ Zf L := by
    intro P hP; rw [hagree] at hP
    exact G16b_complete hk hc' v (b₀ := (0, 0)) (by simp [sigF]) hcheck P hP
  have hZn : ∀ S ∈ Zf L, nrm S = S := by
    intro S hS
    obtain ⟨q, hqL, hSq⟩ := List.mem_map.mp (List.mem_toFinset.mp hS)
    rw [← hSq]; exact (hq q hqL).2
  rw [sum16_regroup hc hv (Zf L) hZ hZn]
  unfold Zf
  rw [List.sum_toFinset _ hnd, List.map_map]
  -- each class: the computable shape value
  have hterm : ∀ q ∈ L, ((fun S => ∑ f ∈ T16 v S, G16 σ 0 (0, 0) (posA (sc f) v) S) ∘ toSet) q =
      shapeVal4B (sigR a) (sigF b) 0 (0, 0) v q.1 q.2.1 q.2.2.1 q.2.2.2 := by
    intro q hqL
    have hd := (hq q hqL).1.1
    have hr := (hq q hqL).1.2
    simp only [dist4B, Bool.and_eq_true, bne_iff_ne, ne_eq] at hd
    obtain ⟨⟨⟨⟨⟨d12, d13⟩, d14⟩, d23⟩, d24⟩, d34⟩ := hd
    have hD : Dist4 q.1 q.2.1 q.2.2.1 q.2.2.2 := ⟨d12, d13, d14, d23, d24, d34⟩
    simp only [beq_iff_eq] at hr
    obtain ⟨⟨⟨⟨⟨⟨⟨r1, r2⟩, r3⟩, r4⟩, r5⟩, r6⟩, r7⟩, r8⟩ := hr
    have hV : ∀ p ∈ ({q.1, q.2.1, q.2.2.1, q.2.2.2} : Finset (ℤ × ℤ)),
        (p.1 : ZMod 3) = sigF b 0 ∧ (p.2 : ZMod 3) = sigF b 0 := by
      have s0 : sigF b 0 = 0 := by simp [sigF]
      intro p hp; rw [s0]
      simp only [Finset.mem_insert, Finset.mem_singleton] at hp
      rcases hp with rfl | rfl | rfl | rfl
      · exact ⟨res_zero r1, res_zero r2⟩
      · exact ⟨res_zero r3, res_zero r4⟩
      · exact ⟨res_zero r5, res_zero r6⟩
      · exact ⟨res_zero r7, res_zero r8⟩
    simp only [Function.comp_apply, toSet]
    simp only [hagree]
    rw [shape_sum2 hc' v hD hV, shapeValB_eq4 hD]
  rw [List.map_congr_left hterm]
  -- the kind of v
  have hv' : v.1 < 0 ∨ (v.1 = 0 ∧ v.2.2 = 0) := by
    unfold IsFar at hv; push Not at hv
    rcases lt_or_eq_of_le hv.1 with h | h
    · exact Or.inl h
    · right; refine ⟨h, ?_⟩
      have h2 := hv.2 h
      revert h2; generalize v.2.2 = u; intro h2
      fin_cases u
      · rfl
      · exact absurd rfl h2
  by_cases hv0 : v.1 = 0
  · have hu : v.2.2 = 0 := by
      rcases hv' with h | h
      · omega
      · exact h.2
    have hpos : (v.2.1.1 : ZMod 3) = 0 ∧ (v.2.1.2 : ZMod 3) = 0 := by
      have := hs; unfold IsSite at this; rw [hv0, h0] at this; exact this
    have e : ∀ q : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ),
        shapeVal4B (sigR a) (sigF b) 0 (0, 0) v q.1 q.2.1 q.2.2.1 q.2.2.2 =
        shapeVal4B (sigR a) (sigF b) 0 (0, 0) (0, (0, 0), 0) q.1 q.2.1 q.2.2.1 q.2.2.2 := fun q =>
      shapeVal4B_congr hv0 hu (by simpa using (ZMod.intCast_zmod_eq_zero_iff_dvd _ 3).mp hpos.1 |> Int.emod_eq_zero_of_dvd)
        (by simpa using (ZMod.intCast_zmod_eq_zero_iff_dvd _ 3).mp hpos.2 |> Int.emod_eq_zero_of_dvd) _ _ _ _
    simp only [e]
    have hk := (sum16B_kernel a b 0).1
    unfold S16B at hk; exact hk
  by_cases hvm : v.1 = -1
  · have hpos : (v.2.1.1 : ZMod 3) = a ∧ (v.2.1.2 : ZMod 3) = a := by
      have := hs; unfold IsSite at this; rw [hvm] at this; exact this
    have d1 : (v.2.1.1 - (a.val : ℤ)) % 3 = 0 := by
      apply Int.emod_eq_zero_of_dvd; apply (ZMod.intCast_zmod_eq_zero_iff_dvd _ 3).mp
      push_cast; rw [hpos.1]; simp
    have d2 : (v.2.1.2 - (a.val : ℤ)) % 3 = 0 := by
      apply Int.emod_eq_zero_of_dvd; apply (ZMod.intCast_zmod_eq_zero_iff_dvd _ 3).mp
      push_cast; rw [hpos.2]; simp
    have e : ∀ q : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ),
        shapeVal4B (sigR a) (sigF b) 0 (0, 0) v q.1 q.2.1 q.2.2.1 q.2.2.2 =
        shapeVal4B (sigR a) (sigF b) 0 (0, 0) (-1, ((a.val : ℤ), (a.val : ℤ)), v.2.2) q.1 q.2.1 q.2.2.1 q.2.2.2 := fun q =>
      shapeVal4B_congr (v' := (-1, ((a.val : ℤ), (a.val : ℤ)), v.2.2)) hvm rfl d1 d2 q.1 q.2.1 q.2.2.1 q.2.2.2
    simp only [e]
    have hk := (sum16B_kernel a b v.2.2).2
    unfold S16B at hk; exact hk
  · have hz : ∀ q : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ),
        shapeVal4B (sigR a) (sigF b) 0 (0, 0) v q.1 q.2.1 q.2.2.1 q.2.2.2 = 0 := by
      intro q; unfold shapeVal4B
      simp only [wR4_zero (σ := sigR a) (k := 0) (v := v) ⟨hv0, by omega⟩]; ring
    simp [hz]

/-- **One flip keeps the polygons of length 16** (bilayer 0, letter 0). -/
theorem flip_keeps_16_norm (σ : ℤ → ZMod 3) (h0 : σ 0 = 0) {v : Atom} (hv : ¬ IsFar 0 v) :
    (Polys (flipAt σ 0) v 16).ncard = (Polys σ v 16).ncard := by
  apply flip_of_sum σ 0 hv 16
  rw [sumWc_16_iff (goodCentre_cDefault σ 0) hv]
  exact sumG16_zero σ h0 hv

theorem flipAt_shift (τ : ℤ → ZMod 3) (k : ℤ) :
    (fun j => flipAt τ k (j - -k)) = flipAt (fun j => τ (j - -k)) 0 := by
  funext j; unfold flipAt; simp only [sub_neg_eq_add, zero_add]
  by_cases h : j ≤ 0
  · rw [if_pos (by omega), if_pos h]
  · rw [if_neg (by omega), if_neg h]

theorem flipAt_add (σ : ℤ → ZMod 3) (s : ZMod 3) :
    (fun j => flipAt σ 0 j + s) = flipAt (fun j => σ j + s) 0 := by
  funext j; unfold flipAt tog; split_ifs <;> ring

/-- **One flip keeps the polygons of length 16**, at any bilayer, for any letters. -/
theorem flipLaw_16 : FlipLaw (fun _ => True) 16 := by
  intro τ k w hw
  -- move bilayer k to 0
  rw [ncard_true_shift τ (-k) w 16, ncard_true_shift (flipAt τ k) (-k) w 16, flipAt_shift]
  set σ₁ : ℤ → ZMod 3 := fun j => τ (j - -k)
  set w₁ := shiftA (-k) w
  have hw₁ : ¬ IsFar 0 w₁ := by
    unfold IsFar at hw ⊢; simp only [w₁, shiftA]; omega
  -- make the letter of bilayer 0 zero
  set s : ZMod 3 := -σ₁ 0
  have hd : (((s.val : ℤ), (s.val : ℤ)).1 : ZMod 3) = s ∧ (((s.val : ℤ), (s.val : ℤ)).2 : ZMod 3) = s := by simp
  rw [ncard_true_pos σ₁ hd w₁ 16, ncard_true_pos (flipAt σ₁ 0) hd w₁ 16, flipAt_add]
  set σ₂ : ℤ → ZMod 3 := fun j => σ₁ j + s
  have h0 : σ₂ 0 = 0 := add_neg_cancel (σ₁ 0)
  have hw₂ : ¬ IsFar 0 (posA ((s.val : ℤ), (s.val : ℤ)) w₁) := by
    unfold IsFar at hw₁ ⊢; simp only [posA]; exact hw₁
  rw [polysQ_true, polysQ_true]
  exact (flip_keeps_16_norm σ₂ h0 hw₂).symm

/-- **Theorem 5 (a) of #102 at l = 16.** -/
theorem theorem5a_16 {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) :
    (Polys σ v 16).ncard = (Polys diamond (0, (0, 0), 0) 16).ncard := theorem5a_of_law flipLaw_16 hσ hv

/-- **Theorem 5 (a) of #102 for l ≤ 17.** -/
theorem theorem5a_upto17 {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) {l : ℕ} (hl : l ≤ 17) :
    (Polys σ v l).ncard = (Polys diamond (0, (0, 0), 0) l).ncard := by
  rcases (show l ≤ 15 ∨ l = 16 ∨ l = 17 by omega) with h | rfl | rfl
  · exact theorem5a_upto15 hσ hv h
  · exact theorem5a_16 hσ hv
  · exact theorem5a_odd σ diamond v _ (by decide)

end LoopEqualityProof
