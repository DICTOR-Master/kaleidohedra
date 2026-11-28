module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Parts
public import LoopEquality.Counting
public import LoopEquality.Transfer
public import LoopEquality.Pairings
public import LoopEquality.BSym
public import LoopEquality.SingleArc
public import LoopEquality.Minimal
public import LoopEquality.Translate
public import LoopEquality.Relabel

@[expose] public section

/-!
# The sign-reversing pairing for minimal linkages through a site (toward l = 14)

On the far side (the root side is reached by the mirror):
* `farSet_htS`: the half-turn about a good centre carries a far linkage to one of the flipped stacking.
* `swapF_htS`: the middle swap commutes with the half-turn.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem farSet_htS {τ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre τ k c) {P : Finset (ℤ × ℤ)}
    {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ} {F : Finset (Sym2 Atom)} (hF : F ∈ FarSet τ k P N s) :
    F.image (htS c) ∈ FarSet (flipAt τ k) k (gP c P) (gM c N) s := by
  obtain ⟨⟨hFl, hFs, hFb⟩, hs, hN⟩ := hF
  obtain ⟨t1, t2, t3, t4, -⟩ := flip_transfer hc hFl hFs hFb
  refine ⟨⟨t1, t2, t3⟩, by rw [t4, hs], ?_⟩
  have := pairF_image c k F (gP c P)
  rw [show (gP c P).image (fun p => c - p) = P from gP_gP c P] at this
  show pairF k (F.image (htS c)) (gP c P) = gM c N
  rw [this, hN]; rfl

theorem minF_htS {τ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre τ k c) {Q : Finset (ℤ × ℤ)}
    {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F) : MinF (flipAt τ k) k (gP c Q) (F.image (htS c)) := by
  have h := farSet_htS hc (show F ∈ FarSet τ k Q (pairF k F Q) Q.card from ⟨hF.1, hF.2, rfl⟩)
  exact ⟨h.1, by rw [h.2.1, card_gP]⟩

theorem htS_mk (c : ℤ × ℤ) (a b : Atom) : htS c s(a, b) = s(htA c a, htA c b) := rfl
theorem htA_mid (c : ℤ × ℤ) (k : ℤ) (m : ℤ × ℤ) : htA c ((k + 1, m, 0) : Atom) = (k + 1, c - m, 0) := rfl

/-- The middle swap commutes with the half-turn. -/
theorem swapF_htS {τ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre τ k c) {Q : Finset (ℤ × ℤ)}
    {G : Finset (Sym2 Atom)} (hG : MinF τ k Q G) :
    (swapF k G).image (htS c) = swapF k (G.image (htS c)) := by
  have hG' := minF_htS hc hG
  ext e'
  rw [Finset.mem_image]
  constructor
  · rintro ⟨f, hf, rfl⟩
    obtain ⟨e, he, rfl⟩ := swapF_mem.mp hf
    obtain ⟨p, hp, q, hq, m, hpq, rfl, hqG, himg, -, -⟩ := swap_edge hG he
    have hpe : s(upA k (c - p), ((k + 1, c - m, 0) : Atom)) ∈ G.image (htS c) := Finset.mem_image.mpr ⟨_, he, rfl⟩
    have hqe : s(upA k (c - q), ((k + 1, c - m, 0) : Atom)) ∈ G.image (htS c) := Finset.mem_image.mpr ⟨_, hqG, rfl⟩
    have hd := mid_deg hG' (mem_gP.mpr (by rwa [sub_sub_cancel])) (mem_gP.mpr (by rwa [sub_sub_cancel]))
      (fun h => hpq (by simpa using h)) hpe hqe
    have hin : s(upA k (c - p), ((k + 1, (c - p) + (c - q) - (c - m), 0) : Atom)) ∈ swapF k (G.image (htS c)) := by
      have : s(upA k (c - p), ((k + 1, (c - p) + (c - q) - (c - m), 0) : Atom)) ∈
          (swapF k (G.image (htS c))).filter (fun e => ((k + 1, (c - p) + (c - q) - (c - m), 0) : Atom) ∈ e) := by
        rw [hd]; simp
      exact (Finset.mem_filter.mp this).1
    have heq : htS c (Sym2.map (swapAt k G) s(upA k p, ((k + 1, m, 0) : Atom))) =
        s(upA k (c - p), ((k + 1, (c - p) + (c - q) - (c - m), 0) : Atom)) := by
      rw [himg, htS_mk]
      show s(upA k (c - p), ((k + 1, c - (p + q - m), 0) : Atom)) = _
      congr 2; congr 1; abel
    rw [heq]; exact hin
  · intro he'
    obtain ⟨g, hg, rfl⟩ := swapF_mem.mp he'
    obtain ⟨p', hp', q', hq', m', hpq', rfl, hqG', himg', -, -⟩ := swap_edge hG' hg
    obtain ⟨f, hf, hfe⟩ := Finset.mem_image.mp hg
    obtain ⟨p, hp, q, hq, m, hpq, rfl, hqG, himg, -, -⟩ := swap_edge hG hf
    rw [htS_mk] at hfe
    have e1 : c - p = p' ∧ c - m = m' := by
      rcases Sym2.eq_iff.mp hfe with ⟨h1, h2⟩ | ⟨h1, -⟩
      · exact ⟨upA_inj h1, by have := congrArg (fun a : Atom => a.2.1) h2; simpa [htA] using this⟩
      · exact absurd h1 upA_ne_mid
    obtain ⟨rfl, rfl⟩ := e1
    have hqe : s(upA k (c - q), ((k + 1, c - m, 0) : Atom)) ∈ G.image (htS c) := Finset.mem_image.mpr ⟨_, hqG, rfl⟩
    have hq'q : q' = c - q := by
      rcases mid_pair hG' hpq' hg hqG' hqe (Sym2.mem_mk_right _ _) with h | h
      · exfalso
        rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
        · exact hpq (by have h2 := upA_inj h1; simpa using h2.symm)
        · exact absurd h1 upA_ne_mid
      · rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
        · exact (upA_inj h1).symm
        · exact absurd h1 upA_ne_mid
    subst hq'q
    refine ⟨_, swapF_mem.mpr ⟨_, hf, himg⟩, ?_⟩
    rw [himg', htS_mk]
    show s(upA k (c - p), ((k + 1, c - (p + q - m), 0) : Atom)) = s(upA k (c - p), (k + 1, (c - p) + (c - q) - (c - m), 0))
    congr 2; congr 1; abel

/-! ## The pairing map: half-turn, then middle swap -/

noncomputable def pairMap (k : ℤ) (c : ℤ × ℤ) (F : Finset (Sym2 Atom)) : Finset (Sym2 Atom) :=
  swapF k (F.image (htS c))

theorem pairMap_mem {τ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre τ k c) {P : Finset (ℤ × ℤ)}
    {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {F : Finset (Sym2 Atom)} (hF : F ∈ FarSet τ k P N P.card) :
    pairMap k c F ∈ FarSet τ k (gP c P) (gM c N) P.card := by
  have h1 := farSet_htS hc hF
  have hG : MinF (flipAt τ k) k (gP c P) (F.image (htS c)) := ⟨h1.1, by rw [h1.2.1, card_gP]⟩
  obtain ⟨h2, h3⟩ := swapF_minF hG
  rw [flipAt_flipAt] at h2
  exact ⟨h2, by unfold pairMap; rw [h3, card_gP], by unfold pairMap; rw [swapF_pair hG, h1.2.2]⟩

theorem pairMap_pairMap {τ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre τ k c) {P : Finset (ℤ × ℤ)}
    {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {F : Finset (Sym2 Atom)} (hF : F ∈ FarSet τ k P N P.card) :
    pairMap k c (pairMap k c F) = F := by
  have hinv := htA_invol c
  have hS : htS c = Sym2.map (htA c) := rfl
  have h1 := farSet_htS hc hF
  have hG : MinF (flipAt τ k) k (gP c P) (F.image (htS c)) := ⟨h1.1, by rw [h1.2.1, card_gP]⟩
  unfold pairMap
  rw [swapF_htS (goodCentre_flipAt hc) hG]
  rw [show (F.image (htS c)).image (htS c) = F by rw [hS]; exact image_image_invol hinv F]
  exact swapF_swapF ⟨hF.1, hF.2.1⟩

/-- **Counts with a condition kept by the pairing map are the same at `P` and at its half-turn.** -/
theorem count_sym {τ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre τ k c) (Cond : Finset (Sym2 Atom) → Prop)
    (hCond : ∀ (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (F : Finset (Sym2 Atom)),
      F ∈ FarSet τ k Q N Q.card → Cond F → Cond (pairMap k c F))
    (P : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) :
    ({F | F ∈ FarSet τ k P N P.card ∧ Cond F} : Set (Finset (Sym2 Atom))).ncard =
      ({F | F ∈ FarSet τ k (gP c P) (gM c N) P.card ∧ Cond F} : Set (Finset (Sym2 Atom))).ncard := by
  apply Set.ncard_congr (fun F _ => pairMap k c F)
  · rintro F ⟨hF, hC⟩; exact ⟨pairMap_mem hc hF, hCond _ _ _ hF hC⟩
  · rintro F₁ F₂ ⟨h1, -⟩ ⟨h2, -⟩ h
    have := congrArg (pairMap k c) h
    rwa [pairMap_pairMap hc h1, pairMap_pairMap hc h2] at this
  · rintro G ⟨hG, hC⟩
    have hG' : G ∈ FarSet τ k (gP c P) (gM c N) (gP c P).card := by rw [card_gP]; exact hG
    have hm := pairMap_mem hc hG'
    rw [gP_gP, gM_gM, card_gP] at hm
    exact ⟨pairMap k c G, ⟨hm, hCond _ _ _ hG' hC⟩, pairMap_pairMap hc hG'⟩

/-! ## The two conditions the pairing map keeps -/

theorem htA_upA_self (k : ℤ) (p : ℤ × ℤ) : htA (p + p) (upA k p) = upA k p := by
  unfold htA upA; simp

/-- `v` is a crossing point: the half-turn about it keeps it in the linkage. -/
theorem cond_end {τ : ℤ → ZMod 3} {k : ℤ} {p0 : ℤ × ℤ} (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ)))
    (F : Finset (Sym2 Atom)) (_hF : F ∈ FarSet τ k Q N Q.card) (hC : ∃ e ∈ F, upA k p0 ∈ e) :
    ∃ e ∈ pairMap k (p0 + p0) F, upA k p0 ∈ e := by
  obtain ⟨e, he, hpe⟩ := hC
  refine ⟨Sym2.map (swapAt k (F.image (htS (p0 + p0)))) (htS (p0 + p0) e),
    swapF_mem.mpr ⟨_, Finset.mem_image_of_mem _ he, rfl⟩, ?_⟩
  rw [← swapAt_upA k (F.image (htS (p0 + p0))) p0]
  refine Sym2.mem_map.mpr ⟨upA k p0, ?_, rfl⟩
  rw [← htA_upA_self k p0]
  exact Sym2.mem_map.mpr ⟨upA k p0, hpe, rfl⟩

/-- `v` is the middle `(k + 1, m0, 0)` of the arc `p, q`: the half-turn about the arc's midpoint keeps that arc's
middle at `v`. -/
theorem cond_mid {τ : ℤ → ZMod 3} {k : ℤ} {p q m0 : ℤ × ℤ} (hc : GoodCentre τ k (p + q)) (hpq : p ≠ q)
    (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (F : Finset (Sym2 Atom)) (hF : F ∈ FarSet τ k Q N Q.card)
    (hC : s(upA k p, ((k + 1, m0, 0) : Atom)) ∈ F ∧ s(upA k q, ((k + 1, m0, 0) : Atom)) ∈ F) :
    s(upA k p, ((k + 1, m0, 0) : Atom)) ∈ pairMap k (p + q) F ∧ s(upA k q, ((k + 1, m0, 0) : Atom)) ∈ pairMap k (p + q) F := by
  set c := p + q
  have h1 := farSet_htS hc hF
  have hG : MinF (flipAt τ k) k (gP c Q) (F.image (htS c)) := ⟨h1.1, by rw [h1.2.1, card_gP]⟩
  have hpQ : p ∈ Q := by
    have hm := (minF_edge ⟨hF.1, hF.2.1⟩ hC.1)
    obtain ⟨p', hp', m', he, -⟩ := hm
    rcases Sym2.eq_iff.mp he with ⟨h, -⟩ | ⟨h, -⟩
    · rw [upA_inj h]; exact hp'
    · exact absurd h upA_ne_mid
  have hqQ : q ∈ Q := by
    obtain ⟨q', hq', m', he, -⟩ := minF_edge ⟨hF.1, hF.2.1⟩ hC.2
    rcases Sym2.eq_iff.mp he with ⟨h, -⟩ | ⟨h, -⟩
    · rw [upA_inj h]; exact hq'
    · exact absurd h upA_ne_mid
  -- the two edges after the half-turn: q and p at the middle c - m0
  have eq1 : htS c s(upA k p, ((k + 1, m0, 0) : Atom)) = s(upA k q, ((k + 1, c - m0, 0) : Atom)) := by
    rw [htS_mk]; show s(upA k (c - p), _) = _; congr 2; show p + q - p = q; abel
  have eq2 : htS c s(upA k q, ((k + 1, m0, 0) : Atom)) = s(upA k p, ((k + 1, c - m0, 0) : Atom)) := by
    rw [htS_mk]; show s(upA k (c - q), _) = _; congr 2; show p + q - q = p; abel
  have hq' : s(upA k q, ((k + 1, c - m0, 0) : Atom)) ∈ F.image (htS c) := Finset.mem_image.mpr ⟨_, hC.1, eq1⟩
  have hp' : s(upA k p, ((k + 1, c - m0, 0) : Atom)) ∈ F.image (htS c) := Finset.mem_image.mpr ⟨_, hC.2, eq2⟩
  have hqg : q ∈ gP c Q := mem_gP.mpr (by show p + q - q ∈ Q; rw [add_sub_cancel_right]; exact hpQ)
  have hpg : p ∈ gP c Q := mem_gP.mpr (by show p + q - p ∈ Q; rw [add_sub_cancel_left]; exact hqQ)
  have hd := mid_deg hG hqg hpg (fun h => hpq h.symm) hq' hp'
  have hm : q + p - (c - m0) = m0 := by show q + p - (p + q - m0) = m0; abel
  rw [hm] at hd
  have a1 : s(upA k q, ((k + 1, m0, 0) : Atom)) ∈ (swapF k (F.image (htS c))).filter (fun e => ((k + 1, m0, 0) : Atom) ∈ e) := by
    rw [hd]; simp
  have a2 : s(upA k p, ((k + 1, m0, 0) : Atom)) ∈ (swapF k (F.image (htS c))).filter (fun e => ((k + 1, m0, 0) : Atom) ∈ e) := by
    rw [hd]; simp
  exact ⟨(Finset.mem_filter.mp a2).1, (Finset.mem_filter.mp a1).1⟩

/-! ## The root side by the mirror -/

theorem mirA_loA (k : ℤ) (p : ℤ × ℤ) : mirA (loA k p) = upA (-k) p := by
  unfold mirA loA upA; simp

theorem mirS_mirS' (σ : ℤ → ZMod 3) : mirS (mirS σ) = σ := by funext i; simp [mirS]

/-- A root linkage, mirrored, is a far linkage of the mirrored stacking with the same ends, pairing and size. -/
theorem rootL_mir {σ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} {R : Finset (Sym2 Atom)} (hR : RootL σ k P R) :
    FarL (mirS σ) (-k) P (R.image mirE) ∧ pairF (-k) (R.image mirE) P = pairR k R P := by
  have hinv : ∀ a, mirA (mirA a) = a := mirA_mirA
  have hends : (P.image (loA k)).image mirA = P.image (upA (-k)) := by
    rw [Finset.image_image]; exact Finset.image_congr (fun p _ => mirA_loA k p)
  refine ⟨⟨?_, ?_, ?_⟩, ?_⟩
  · rw [← hends]; exact linkage_image hinv hR.1
  · intro e he w hw
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    obtain ⟨a, ha, rfl⟩ := Sym2.mem_map.mp hw
    exact isFar_mirA.mpr (hR.2.1 f hf a ha)
  · intro e he
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    have hb := hR.2.2 f hf
    induction f using Sym2.ind with
    | _ a b => rw [bondS_mk] at hb; show BondS _ s(mirA a, mirA b); rw [bondS_mk]; exact bond_mirA hb
  · ext ⟨p, q⟩
    simp only [pairF, pairR, Finset.mem_filter, Finset.mem_product]
    rw [← mirA_loA, ← mirA_loA]
    exact and_congr_right (fun _ => (conn_image hinv R (loA k p) (loA k q)).symm)

theorem farL_mir {σ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)}
    (hF : FarL (mirS σ) (-k) P F) : RootL σ k P (F.image mirE) := by
  have hinv : ∀ a, mirA (mirA a) = a := mirA_mirA
  have hends : (P.image (upA (-k))).image mirA = P.image (loA k) := by
    rw [Finset.image_image]; apply Finset.image_congr; intro p _
    show mirA (upA (-k) p) = loA k p
    have := mirA_loA k p; rw [← this, mirA_mirA]
  refine ⟨?_, ?_, ?_⟩
  · rw [← hends]; exact linkage_image hinv hF.1
  · intro e he w hw
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    obtain ⟨a, ha, rfl⟩ := Sym2.mem_map.mp hw
    intro h
    have : IsFar (-k) (mirA (mirA a)) := by rw [mirA_mirA]; exact hF.2.1 f hf a ha
    exact (isFar_mirA.mp this) h
  · intro e he
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    have hb := hF.2.2 f hf
    induction f using Sym2.ind with
    | _ a b =>
      rw [bondS_mk] at hb; show BondS _ s(mirA a, mirA b); rw [bondS_mk]
      have := bond_mirA hb; rwa [mirS_mirS'] at this

/-- **Root counts through `v` are far counts through the mirrored `v`.** -/
theorem Wc_mir (σ : ℤ → ZMod 3) (v : Atom) (k : ℤ) (P : Finset (ℤ × ℤ)) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (r : ℕ) :
    Wc σ v k P M r = ({F | F ∈ FarSet (mirS σ) (-k) P M r ∧ 0 < degS F (mirA v)} : Set (Finset (Sym2 Atom))).ncard := by
  unfold Wc; congr 1
  apply Set.ncard_congr (fun R _ => R.image mirE)
  · rintro R ⟨hR, hv, hr, hM⟩
    obtain ⟨h1, h2⟩ := rootL_mir hR
    exact ⟨⟨h1, by rw [Finset.card_image_of_injective _ mirE_injective, hr], by rw [h2, hM]⟩, by rw [degS_mirE]; exact hv⟩
  · intro R₁ R₂ _ _ h; exact Finset.image_injective mirE_injective h
  · rintro F ⟨⟨hF, hs, hN⟩, hv⟩
    have hR := farL_mir hF
    refine ⟨F.image mirE, ⟨hR, ?_, ?_, ?_⟩, image_mirE_mirE F⟩
    · have h := degS_mirE F (mirA v)
      rw [mirA_mirA] at h; rw [h]; exact hv
    · rw [Finset.card_image_of_injective _ mirE_injective, hs]
    · have := (rootL_mir hR).2
      rw [image_mirE_mirE] at this; rw [← this, hN]

end LoopEqualityProof
