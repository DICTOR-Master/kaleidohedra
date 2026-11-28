module

public import Mathlib
public import LoopEquality.Pairing14
public import LoopEquality.Twelve
public import LoopEquality.Lemma7
public import LoopEquality.Theorem5

@[expose] public section

/-!
# One flip keeps the polygons of length 14

At `l = 14` only the terms with four crossing points and a root linkage of minimal size (4 edges) are left. They are
split by the centre of the arc at `v` (twice `v`'s own crossing point when `v` is an end, the sum of its two ends when
`v` is a middle). For each centre `c'`, the half-turn about `c'` followed by the middle swap (on the root side, read
through the mirror) keeps the count, and it turns the far asymmetry into its negative, so the terms cancel in pairs.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-! ## Support: a non-zero term lives in the window -/

theorem window_of_parts {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {P : Finset (ℤ × ℤ)}
    (hv : ¬ IsFar k v) (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p))
    {M N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {r s : ℕ} {R F : Finset (Sym2 Atom)}
    (hR : R ∈ RootSet σ v k P M r) (hF : F ∈ FarSet σ k P N s) (hOC : OneCycleRel P M N) :
    P ⊆ window v (r + P.card + s) := by
  obtain ⟨⟨hRl, hRs, hRb⟩, hdv, hr, hM⟩ := hR
  obtain ⟨⟨hFl, hFs, hFb⟩, hs, hN⟩ := hF
  have hsc : SingleCycle k P R F := by rw [singleCycle_iff, hM, hN]; exact hOC
  apply polysCross_window (σ := σ) (k := k) (E := R ∪ P.image (vert k) ∪ F)
  refine ⟨?_, ?_, ?_, ?_⟩
  · refine parts_to_polygon hP hRl hFl hRs hFs (fun e he => ?_) hsc
    rcases Finset.mem_union.mp he with h | h
    · rcases Finset.mem_union.mp h with h | h
      · exact hRb e h
      · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp h; exact hV p hp
    · exact hFb e h
  · rw [degS_pos_root hRl hRs hFs hv]; exact hdv
  · rw [card_three hRs hFs, hr, hs]
  · intro p
    constructor
    · intro hp; exact Finset.mem_union_left _ (Finset.mem_union_right _ (Finset.mem_image_of_mem _ hp))
    · intro h
      rcases Finset.mem_union.mp h with h | h
      · rcases Finset.mem_union.mp h with h | h
        · exact absurd (isFar_upA k p) (hRs _ h _ (by rw [vert_eq]; exact Sym2.mem_mk_right _ _))
        · obtain ⟨q, hq, hqp⟩ := Finset.mem_image.mp h; rw [← vert_inj hqp]; exact hq
      · exact absurd (hFs _ h _ (by rw [vert_eq]; exact Sym2.mem_mk_left _ _)) (not_isFar_loA k p)

theorem window_of_term {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    {P : Finset (ℤ × ℤ)} (hv : ¬ IsFar k v) (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p))
    {M N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {r s : ℕ} (hOC : OneCycleRel P M N)
    (hW : Wc σ v k P M r ≠ 0) (hA : Af σ k c P N s ≠ 0) : P ⊆ window v (r + P.card + s) := by
  obtain ⟨R, hR⟩ : (RootSet σ v k P M r).Nonempty := by
    rw [Set.nonempty_iff_ne_empty]; intro h; apply hW; unfold Wc; rw [h]; simp
  by_cases h1 : (FarSet σ k P N s).Nonempty
  · obtain ⟨F, hF⟩ := h1; exact window_of_parts hv hP hV hR hF hOC
  · have h2 : (FarSet σ k (gP c P) (gM c N) s).Nonempty := by
      rw [Set.nonempty_iff_ne_empty]; intro h; apply hA; unfold Af Fc
      rw [Set.not_nonempty_iff_eq_empty.mp h1, h]; simp
    obtain ⟨F', hF'⟩ := h2
    have hF := farSet_htS hc hF'
    rw [gP_gP, gM_gM] at hF
    have hR' : R ∈ RootSet (flipAt σ k) v k P M r := ⟨(rootL_flip hc).mp hR.1, hR.2⟩
    exact window_of_parts hv hP (fun p hp => bondS_vert_flip.mp (hV p hp)) hR' hF hOC

/-! ## Minimal far linkages: finitely many; the centre of the arc at an atom -/

theorem minFar_finite (τ : ℤ → ZMod 3) (k : ℤ) (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) :
    (FarSet τ k Q N Q.card).Finite := by
  apply (((Q ×ˢ shortVecs).image
    (fun x => s(upA k x.1, ((k + 1, x.1 + x.2, 0) : Atom)))).powerset.finite_toSet).subset
  intro F hF
  refine Finset.mem_coe.mpr (Finset.mem_powerset.mpr ?_)
  intro e he
  obtain ⟨p, hp, m, rfl, hm⟩ := minF_edge ⟨hF.1, hF.2.1⟩ he
  exact Finset.mem_image.mpr ⟨(p, m - p), Finset.mem_product.mpr ⟨hp, hm⟩, by simp⟩

theorem degS_pos_of {F : Finset (Sym2 Atom)} {e : Sym2 Atom} {w : Atom} (he : e ∈ F) (hw : w ∈ e) :
    0 < degS F w := Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨he, hw⟩⟩

theorem exists_edge_of_degS {F : Finset (Sym2 Atom)} {w : Atom} (h : 0 < degS F w) : ∃ e ∈ F, w ∈ e := by
  obtain ⟨e, he⟩ := Finset.card_pos.mp h
  exact ⟨e, (Finset.mem_filter.mp he).1, (Finset.mem_filter.mp he).2⟩

theorem mid_filter {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {p q m : ℤ × ℤ} (hpq : p ≠ q) (hpF : s(upA k p, ((k + 1, m, 0) : Atom)) ∈ F)
    (hqF : s(upA k q, ((k + 1, m, 0) : Atom)) ∈ F) :
    F.filter (fun e => ((k + 1, m, 0) : Atom) ∈ e) =
      {s(upA k p, (k + 1, m, 0)), s(upA k q, (k + 1, m, 0))} := by
  ext f
  simp only [Finset.mem_filter, Finset.mem_insert, Finset.mem_singleton]
  constructor
  · rintro ⟨hf, hmf⟩; exact mid_pair hF hpq hpF hqF hf hmf
  · rintro (rfl | rfl)
    · exact ⟨hpF, Sym2.mem_mk_right _ _⟩
    · exact ⟨hqF, Sym2.mem_mk_right _ _⟩

/-- The centre of the arc at `w`: twice `w`'s position if `w` is an end, else the sum of its two neighbours. -/
noncomputable def cenAt (k : ℤ) (w : Atom) (F : Finset (Sym2 Atom)) : ℤ × ℤ :=
  if w.1 = k ∧ w.2.2 = 1 then w.2.1 + w.2.1 else nbSum F w

/-- The possible centres at `w`. -/
def cenSet (w : Atom) : Finset (ℤ × ℤ) :=
  insert (w.2.1 + w.2.1) ((shortVecs ×ˢ shortVecs).image (fun d => (w.2.1 - d.1) + (w.2.1 - d.2)))

theorem cenAt_end (k : ℤ) (p : ℤ × ℤ) (F : Finset (Sym2 Atom)) : cenAt k (upA k p) F = p + p := by
  unfold cenAt upA; simp

theorem cenAt_mid (k : ℤ) (m : ℤ × ℤ) (F : Finset (Sym2 Atom)) :
    cenAt k ((k + 1, m, 0) : Atom) F = nbSum F (k + 1, m, 0) := by
  unfold cenAt; rw [if_neg (by simp)]

theorem cen_spec {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))}
    {F : Finset (Sym2 Atom)} {w : Atom} (hF : F ∈ FarSet τ k Q N Q.card) (hw : 0 < degS F w) :
    (∃ p ∈ Q, ∃ q ∈ Q, cenAt k w F = p + q) ∧ cenAt k w F ∈ cenSet w := by
  have hm : MinF τ k Q F := ⟨hF.1, hF.2.1⟩
  obtain ⟨e, he, hwe⟩ := exists_edge_of_degS hw
  obtain ⟨p, hp, q, hq, m, hpq, rfl, hqF, -, hmp, hmq⟩ := swap_edge hm he
  rcases Sym2.mem_iff.mp hwe with rfl | rfl
  · rw [cenAt_end]
    exact ⟨⟨p, hp, p, hp, rfl⟩, by unfold cenSet upA; simp⟩
  · rw [cenAt_mid, minF_nb hm hpq (mid_filter hm hpq he hqF)]
    refine ⟨⟨p, hp, q, hq, rfl⟩, ?_⟩
    unfold cenSet
    refine Finset.mem_insert_of_mem (Finset.mem_image.mpr ⟨(m - p, m - q), Finset.mem_product.mpr ⟨hmp, hmq⟩, ?_⟩)
    simp

/-- The pairing map about the centre keeps "`w` is on the linkage, with this centre". -/
theorem cond_cen {τ : ℤ → ZMod 3} {k : ℤ} {w : Atom} {c' : ℤ × ℤ} (hc : GoodCentre τ k c')
    (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (F : Finset (Sym2 Atom))
    (hF : F ∈ FarSet τ k Q N Q.card) (hC : 0 < degS F w ∧ cenAt k w F = c') :
    0 < degS (pairMap k c' F) w ∧ cenAt k w (pairMap k c' F) = c' := by
  have hm : MinF τ k Q F := ⟨hF.1, hF.2.1⟩
  have hF2 := pairMap_mem hc hF
  have hm2 : MinF τ k (gP c' Q) (pairMap k c' F) := ⟨hF2.1, by rw [hF2.2.1, card_gP]⟩
  obtain ⟨e, he, hwe⟩ := exists_edge_of_degS hC.1
  obtain ⟨p, hp, q, hq, m, hpq, rfl, hqF, -, -, -⟩ := swap_edge hm he
  rcases Sym2.mem_iff.mp hwe with rfl | rfl
  · rw [cenAt_end] at hC
    obtain ⟨-, rfl⟩ := hC
    obtain ⟨e', he', hpe'⟩ := cond_end Q N F hF ⟨_, he, Sym2.mem_mk_left _ _⟩
    exact ⟨degS_pos_of he' hpe', cenAt_end _ _ _⟩
  · rw [cenAt_mid, minF_nb hm hpq (mid_filter hm hpq he hqF)] at hC
    obtain ⟨-, rfl⟩ := hC
    obtain ⟨h1, h2⟩ := cond_mid hc hpq Q N F hF ⟨he, hqF⟩
    exact ⟨degS_pos_of h1 (Sym2.mem_mk_right _ _), by rw [cenAt_mid, minF_nb hm2 hpq (mid_filter hm2 hpq h1 h2)]⟩

/-- Minimal far linkages through `w` with centre `c'`. -/
noncomputable def Wcen (τ : ℤ → ZMod 3) (k : ℤ) (w : Atom) (c' : ℤ × ℤ) (Q : Finset (ℤ × ℤ))
    (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : ℤ :=
  ({F | F ∈ FarSet τ k Q N Q.card ∧ (0 < degS F w ∧ cenAt k w F = c')} : Set (Finset (Sym2 Atom))).ncard

theorem Wcen_g {τ : ℤ → ZMod 3} {k : ℤ} {w : Atom} {c' : ℤ × ℤ} (hc : GoodCentre τ k c')
    (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) :
    Wcen τ k w c' (gP c' Q) (gM c' N) = Wcen τ k w c' Q N := by
  unfold Wcen; rw [card_gP]
  have := count_sym hc (fun F => 0 < degS F w ∧ cenAt k w F = c') (fun Q N F hF hC => cond_cen hc Q N F hF hC) Q N
  exact_mod_cast this.symm

/-- **The root count at minimal size, split by the centre.** -/
theorem Wc_cen (σ : ℤ → ZMod 3) (v : Atom) (k : ℤ) (P : Finset (ℤ × ℤ)) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) :
    Wc σ v k P M P.card = ∑ c' ∈ cenSet (mirA v), Wcen (mirS σ) (-k) (mirA v) c' P M := by
  rw [Wc_mir]
  set S : Set (Finset (Sym2 Atom)) := {F | F ∈ FarSet (mirS σ) (-k) P M P.card ∧ 0 < degS F (mirA v)} with hSdef
  have hfin : S.Finite := (minFar_finite _ _ P M).subset (fun F hF => hF.1)
  rw [Set.ncard_eq_toFinset_card S hfin,
    Finset.card_eq_sum_card_fiberwise (f := cenAt (-k) (mirA v)) (t := cenSet (mirA v)) ?_]
  · push_cast
    apply Finset.sum_congr rfl; intro c' _
    unfold Wcen
    rw [← Set.ncard_coe_finset]
    congr 2; ext F
    simp [S, and_assoc]
  · intro F hF
    have hF' := (Set.Finite.mem_toFinset hfin).mp hF
    exact (cen_spec hF'.1 hF'.2).2

theorem good_mirS {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (h : GoodCentre σ k c) : GoodCentre (mirS σ) (-k) c := by
  unfold GoodCentre mirS at *; simpa using h

theorem Wcen_bad {σ : ℤ → ZMod 3} {k : ℤ} {v : Atom} {c' : ℤ × ℤ} {P : Finset (ℤ × ℤ)}
    {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))} (hV : ∀ p ∈ P, BondS σ (vert k p)) (hc : ¬ GoodCentre σ k c') :
    Wcen (mirS σ) (-k) (mirA v) c' P M = 0 := by
  unfold Wcen
  have : ({F | F ∈ FarSet (mirS σ) (-k) P M P.card ∧ (0 < degS F (mirA v) ∧ cenAt (-k) (mirA v) F = c')} :
      Set (Finset (Sym2 Atom))) = ∅ := by
    apply Set.eq_empty_of_forall_notMem
    rintro F ⟨hF, hw, he⟩
    obtain ⟨⟨p, hp, q, hq, hpq⟩, -⟩ := cen_spec hF hw
    apply hc; rw [← he, hpq]
    have h1 := bondS_vert_iff.mp (hV p hp); have h2 := bondS_vert_iff.mp (hV q hq)
    unfold GoodCentre
    simp only [Prod.fst_add, Prod.snd_add, Int.cast_add, h1.1, h1.2, h2.1, h2.2]
    constructor <;> ring
  rw [this]; simp

/-! ## The cancellation -/

/-- The surviving terms at one centre. -/
noncomputable def f14 (σ : ℤ → ZMod 3) (v : Atom) (k : ℤ) (c c' : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : ℤ :=
  ∑ x ∈ idxSet 14 P P (OneCycleRel P),
    if P.card = 4 ∧ x.2.1 = 4 then Wcen (mirS σ) (-k) (mirA v) c' P x.1.1 * Af σ k c P x.1.2 x.2.2 else 0

theorem f14_g {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c c' : ℤ × ℤ} (hc : GoodCentre σ k c) (hc' : GoodCentre σ k c')
    (P : Finset (ℤ × ℤ)) : f14 σ v k c c' (gP c' P) = - f14 σ v k c c' P := by
  unfold f14
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

theorem f14_support {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c c' : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hv : ¬ IsFar k v) {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p))
    (h : f14 σ v k c c' P ≠ 0) : P ⊆ window v 14 := by
  unfold f14 at h
  obtain ⟨x, hx, hne⟩ := Finset.exists_ne_zero_of_sum_ne_zero h
  split_ifs at hne with hcond
  · have hW := left_ne_zero_of_mul hne
    have hA := right_ne_zero_of_mul hne
    have hx' := Finset.mem_filter.mp hx
    have hWc : Wc σ v k P x.1.1 x.2.1 ≠ 0 := by
      unfold Wcen at hW
      obtain ⟨F, hF, hw, -⟩ := Set.nonempty_of_ncard_ne_zero (by exact_mod_cast hW)
      rw [show x.2.1 = P.card by omega, Wc_mir]
      have hfin : ({F | F ∈ FarSet (mirS σ) (-k) P x.1.1 P.card ∧ 0 < degS F (mirA v)} :
          Set (Finset (Sym2 Atom))).Finite := (minFar_finite _ _ P x.1.1).subset (fun F hF => hF.1)
      have := (Set.ncard_pos hfin).mpr ⟨F, hF, hw⟩
      exact_mod_cast this.ne'
    have := window_of_term hc hv hP hV hx'.2.2 hWc hA
    rwa [hx'.2.1] at this
  · exact absurd rfl hne

theorem f14_sum {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c c' : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hc' : GoodCentre σ k c') (hv : ¬ IsFar k v) : ∑ P ∈ famP σ v 14 k c, f14 σ v k c c' P = 0 := by
  rw [← Finset.sum_filter_ne_zero]
  apply Finset.sum_involution (fun P _ => gP c' P)
  · intro P _; rw [f14_g hc hc']; ring
  · intro P _ hne heq
    have := f14_g (v := v) hc hc' P; rw [heq] at this
    exact hne (by linarith)
  · intro P hP
    obtain ⟨hP1, hP2⟩ := Finset.mem_filter.mp hP
    simp only [famP, Finset.mem_filter, Finset.mem_powerset] at hP1
    obtain ⟨-, hne, hV⟩ := hP1
    have hV' : ∀ p ∈ gP c' P, BondS σ (vert k p) := fun p hp => by
      have := bondS_vert_g hc' (hV _ (mem_gP.mp hp)); rwa [sub_sub_cancel] at this
    have hne' : (gP c' P).Nonempty := by
      obtain ⟨q, hq⟩ := hne; exact ⟨c' - q, mem_gP.mpr (by rwa [sub_sub_cancel])⟩
    have hf : f14 σ v k c c' (gP c' P) ≠ 0 := by rw [f14_g hc hc']; exact neg_ne_zero.mpr hP2
    refine Finset.mem_filter.mpr ⟨?_, hf⟩
    simp only [famP, Finset.mem_filter, Finset.mem_powerset]
    exact ⟨(f14_support hc hv hne' hV' hf).trans Finset.subset_union_left, hne', hV'⟩
  · intro P _; exact gP_gP c' P

/-- At `l = 14` each term is its surviving part, split by the centre. -/
theorem term14 {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {P : Finset (ℤ × ℤ)}
    (hP : P ∈ famP σ v 14 k c) {x} (hx : x ∈ idxSet 14 P P (OneCycleRel P)) :
    Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 =
      ∑ c' ∈ cenSet (mirA v), (if P.card = 4 ∧ x.2.1 = 4 then
        Wcen (mirS σ) (-k) (mirA v) c' P x.1.1 * Af σ k c P x.1.2 x.2.2 else 0) := by
  have hsum := (Finset.mem_filter.mp hx).2.1
  simp only [famP, Finset.mem_filter] at hP
  obtain ⟨-, hne, hV⟩ := hP
  by_cases hcond : P.card = 4 ∧ x.2.1 = 4
  · simp only [if_pos hcond]
    rw [← Finset.sum_mul, ← Wc_cen]
    congr 2; omega
  · simp only [if_neg hcond, Finset.sum_const_zero]
    by_cases hr : x.2.1 < P.card
    · rw [Wc_zero hr, zero_mul]
    by_cases hs : x.2.2 < P.card
    · rw [Af_zero hs, mul_zero]
    by_cases hev : Even P.card
    swap
    · rw [Af_odd hev, mul_zero]
    have hpos : 0 < P.card := Finset.card_pos.mpr hne
    obtain ⟨t, ht⟩ := hev
    have h24 : P.card = 2 ∨ P.card = 4 := by omega
    rcases h24 with h2 | h4
    · obtain ⟨a, b, hab, rfl⟩ := Finset.card_eq_two.mp h2
      have ha := bondS_vert_iff.mp (hV a (by simp)); have hb := bondS_vert_iff.mp (hV b (by simp))
      have : Af σ k c {a, b} x.1.2 x.2.2 = 0 := by unfold Af; rw [Fc_two hc ha hb]; simp
      rw [this, mul_zero]
    · by_cases hodd : Even x.2.1
      swap
      · rw [Wc_odd_size hodd, zero_mul]
      obtain ⟨u, hu⟩ := hodd
      have : x.2.2 = P.card := by omega
      rw [this, Af_min hc, mul_zero]

theorem sumWc_14 {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) (hv : ¬ IsFar k v) :
    ∑ P ∈ famP σ v 14 k c, ∑ x ∈ idxSet 14 P P (OneCycleRel P), Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 = 0 := by
  have e1 : ∀ P ∈ famP σ v 14 k c,
      ∑ x ∈ idxSet 14 P P (OneCycleRel P), Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 =
      ∑ c' ∈ cenSet (mirA v), ∑ x ∈ idxSet 14 P P (OneCycleRel P), (if P.card = 4 ∧ x.2.1 = 4 then
        Wcen (mirS σ) (-k) (mirA v) c' P x.1.1 * Af σ k c P x.1.2 x.2.2 else 0) := fun P hP => by
    rw [Finset.sum_congr rfl (fun x hx => term14 hc hP hx)]; exact Finset.sum_comm
  rw [Finset.sum_congr rfl e1, Finset.sum_comm]
  apply Finset.sum_eq_zero; intro c' _
  by_cases hg : GoodCentre σ k c'
  · have := f14_sum (v := v) hc hg hv; unfold f14 at this; exact this
  · apply Finset.sum_eq_zero; intro P hP; apply Finset.sum_eq_zero; intro x _
    simp only [famP, Finset.mem_filter] at hP
    split_ifs
    · rw [Wcen_bad hP.2.2 hg, zero_mul]
    · rfl

/-- **One flip keeps the polygons of length 14** through any atom below the cut. -/
theorem flip_keeps_14 (σ : ℤ → ZMod 3) (k : ℤ) {v : Atom} (hv : ¬ IsFar k v) :
    (Polys (flipAt σ k) v 14).ncard = (Polys σ v 14).ncard := by
  set c := cDefault σ k
  have hc : GoodCentre σ k c := goodCentre_cDefault σ k
  have h := theoremB_sym (σ := σ) (v := v) (l := 14) hc hv
  have hK := sumWc_14 (v := v) hc hv
  have hz : ∑ P ∈ famP σ v 14 k c, ∑ x ∈ idxSet 14 P P (OneCycleRel P),
      Aw σ v k c P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 = 0 := by
    simp only [Aw, sub_mul, Finset.sum_sub_distrib]
    have h2 : ∑ P ∈ famP σ v 14 k c, ∑ x ∈ idxSet 14 P P (OneCycleRel P),
        Wc σ v k (gP c P) (gM c x.1.1) x.2.1 * Af σ k c P x.1.2 x.2.2 = 0 := by
      have e : ∀ P, ∑ x ∈ idxSet 14 P P (OneCycleRel P), Wc σ v k (gP c P) (gM c x.1.1) x.2.1 * Af σ k c P x.1.2 x.2.2 =
          - ∑ x ∈ idxSet 14 (gP c P) (gP c P) (OneCycleRel (gP c P)),
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

/-! ## Theorem 5 (a) at l = 14 -/

/-- From a one-flip law at `l`, Theorem 5 (a) at `l` (the assembly of `theorem5a_12`, for any `l`). -/
theorem theorem5a_of_law {l : ℕ} (hF : FlipLaw (fun _ => True) l) {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom}
    (hv : IsSite σ v) : (Polys σ v l).ncard = (Polys diamond (0, (0, 0), 0) l).ncard := by
  have hFm : FlipLaw (mirQ (fun _ => True)) l := by rw [mirQ_true]; exact hF
  rw [← polysQ_true, ← polysQ_true]
  obtain ⟨j, p, u⟩ := v
  set σ1 : ℤ → ZMod 3 := fun i => σ (i - -j) with hσ1
  have h1 := ncard_true_shift σ (-j) (j, p, u) l
  have hs1 : shiftA (-j) (j, p, u) = (0, p, u) := by simp [shiftA]
  rw [hs1] at h1
  have hσ1s : IsStacking σ1 := by
    intro i h
    apply hσ (i + j)
    have h' : σ (i + 1 - -j) = σ (i - -j) := h
    rwa [show i + 1 - -j = i + j + 1 by ring, show i - -j = i + j by ring] at h'
  have hv1 : IsSite σ1 (0, p, u) := by unfold IsSite at hv ⊢; simpa [hσ1] using hv
  obtain ⟨σ2, hσ2s, hv2, h2⟩ : ∃ σ2 : ℤ → ZMod 3, IsStacking σ2 ∧ IsSite σ2 (0, p, 0) ∧
      (PolysQ (fun _ => True) σ1 (0, p, u) l).ncard = (PolysQ (fun _ => True) σ2 (0, p, 0) l).ncard := by
    fin_cases u
    · exact ⟨σ1, hσ1s, hv1, rfl⟩
    · refine ⟨mirS σ1, mirS_isStacking hσ1s, ?_, ?_⟩
      · have := isSite_mirA hv1; simpa [mirA] using this
      · have := ncard_polysQ_mirror (fun _ => True) σ1 (0, p, 1) l
        rw [mirQ_true] at this; simpa [mirA] using this
  have hd : ((-p).1 : ZMod 3) = -σ2 0 ∧ ((-p).2 : ZMod 3) = -σ2 0 := by
    unfold IsSite at hv2; simp only at hv2
    refine ⟨?_, ?_⟩ <;> simp only [Prod.fst_neg, Prod.snd_neg, Int.cast_neg, hv2.1, hv2.2] <;> rfl
  have h3 := ncard_true_pos σ2 hd (0, p, 0) l
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

theorem flipLaw_14 : FlipLaw (fun _ => True) 14 := by
  intro τ k w hw; rw [polysQ_true, polysQ_true]; exact (flip_keeps_14 τ k hw).symm

/-- **Theorem 5 (a) of #102 at l = 14.** -/
theorem theorem5a_14 {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) :
    (Polys σ v 14).ncard = (Polys diamond (0, (0, 0), 0) 14).ncard := theorem5a_of_law flipLaw_14 hσ hv

/-- **Theorem 5 (a) of #102 for l ≤ 15.** -/
theorem theorem5a_upto15 {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) {l : ℕ} (hl : l ≤ 15) :
    (Polys σ v l).ncard = (Polys diamond (0, (0, 0), 0) l).ncard := by
  rcases (show l ≤ 13 ∨ l = 14 ∨ l = 15 by omega) with h | rfl | rfl
  · exact theorem5a_upto13 hσ hv h
  · exact theorem5a_14 hσ hv
  · exact theorem5a_odd σ diamond v _ (by decide)

end LoopEqualityProof
