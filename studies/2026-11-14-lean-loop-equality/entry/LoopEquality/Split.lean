module

public import Mathlib
public import LoopEquality.Parts
public import LoopEquality.Pairings
public import LoopEquality.Finiteness

@[expose] public section

/-!
# A linkage is its components: splitting and joining

`compPart L x₀`: the edges of `L` in the component of `x₀`; `restPart L x₀`: the others. For a linkage on `B`, these
are linkages on the ends joined to `x₀` and on the other ends, with no atom in common. Conversely two linkages with
no atom in common join to a linkage on the union of their ends, and paths in the union stay in one part.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

noncomputable def compPart (L : Finset (Sym2 Atom)) (x₀ : Atom) : Finset (Sym2 Atom) :=
  L.filter (fun e => ∃ w ∈ e, Conn L x₀ w)

noncomputable def restPart (L : Finset (Sym2 Atom)) (x₀ : Atom) : Finset (Sym2 Atom) :=
  L.filter (fun e => ∃ w ∈ e, ¬ Conn L x₀ w)

theorem conn_class {L : Finset (Sym2 Atom)} {x₀ u w : Atom} {e : Sym2 Atom} (he : e ∈ L) (hu : u ∈ e) (hw : w ∈ e) :
    Conn L x₀ u ↔ Conn L x₀ w := by
  induction e using Sym2.ind with
  | _ a b =>
    have hab : s(a, b) ∈ L := he
    have hba : s(b, a) ∈ L := by rw [Sym2.eq_swap]; exact he
    rcases Sym2.mem_iff.mp hu with rfl | rfl <;> rcases Sym2.mem_iff.mp hw with rfl | rfl
    · exact Iff.rfl
    · exact ⟨fun h => conn_step h hab, fun h => conn_step h hba⟩
    · exact ⟨fun h => conn_step h hba, fun h => conn_step h hab⟩
    · exact Iff.rfl

theorem degS_compPart (L : Finset (Sym2 Atom)) (x₀ w : Atom) :
    degS (compPart L x₀) w = if Conn L x₀ w then degS L w else 0 :=
  degS_filter_closed (fun a => Conn L x₀ a) (fun a b h ha => conn_step ha h) w

theorem degS_restPart (L : Finset (Sym2 Atom)) (x₀ w : Atom) :
    degS (restPart L x₀) w = if Conn L x₀ w then 0 else degS L w := by
  have := degS_filter_closed (L := L) (fun a => ¬ Conn L x₀ a)
    (fun a b h ha hb => ha (conn_step hb (by rw [Sym2.eq_swap]; exact h))) w
  unfold restPart; rw [this]; by_cases h : Conn L x₀ w <;> simp [h]

theorem compPart_union_restPart (L : Finset (Sym2 Atom)) (x₀ : Atom) : compPart L x₀ ∪ restPart L x₀ = L := by
  ext e
  simp only [compPart, restPart, Finset.mem_union, Finset.mem_filter]
  constructor
  · rintro (⟨h, -⟩ | ⟨h, -⟩) <;> exact h
  · intro he
    by_cases h : ∃ w ∈ e, Conn L x₀ w
    · exact Or.inl ⟨he, h⟩
    · obtain ⟨w, hw⟩ := exists_mem_sym2 e
      exact Or.inr ⟨he, w, hw, fun hc => h ⟨w, hw, hc⟩⟩

theorem disjoint_compPart_restPart (L : Finset (Sym2 Atom)) (x₀ : Atom) : Disjoint (compPart L x₀) (restPart L x₀) := by
  rw [Finset.disjoint_left]
  intro e h1 h2
  obtain ⟨he, u, hu, hcu⟩ := Finset.mem_filter.mp h1
  obtain ⟨-, w, hw, hcw⟩ := Finset.mem_filter.mp h2
  exact hcw ((conn_class he hu hw).mp hcu)

theorem linkage_compPart {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B) (x₀ : Atom) :
    IsLinkageOn (compPart L x₀) (B.filter (Conn L x₀)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro w hw; obtain ⟨hwB, hc⟩ := Finset.mem_filter.mp hw
    rw [degS_compPart, if_pos hc]; exact hL.1 w hwB
  · intro w hw
    rw [degS_compPart]; split_ifs with hc
    · exact hL.2.1 w (fun hB => hw (Finset.mem_filter.mpr ⟨hB, hc⟩))
    · exact Or.inl rfl
  · intro G hG hne; exact hL.2.2.1 G (hG.trans (Finset.filter_subset _ _)) hne
  · intro e he; exact hL.2.2.2 e (Finset.filter_subset _ _ he)

theorem linkage_restPart {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B) (x₀ : Atom) :
    IsLinkageOn (restPart L x₀) (B.filter (fun w => ¬ Conn L x₀ w)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro w hw; obtain ⟨hwB, hc⟩ := Finset.mem_filter.mp hw
    rw [degS_restPart, if_neg hc]; exact hL.1 w hwB
  · intro w hw
    rw [degS_restPart]; split_ifs with hc
    · exact Or.inl rfl
    · exact hL.2.1 w (fun hB => hw (Finset.mem_filter.mpr ⟨hB, hc⟩))
  · intro G hG hne; exact hL.2.2.1 G (hG.trans (Finset.filter_subset _ _)) hne
  · intro e he; exact hL.2.2.2 e (Finset.filter_subset _ _ he)

/-- No atom in both parts. -/
theorem compPart_restPart_atoms (L : Finset (Sym2 Atom)) (x₀ w : Atom) :
    degS (compPart L x₀) w = 0 ∨ degS (restPart L x₀) w = 0 := by
  rw [degS_compPart, degS_restPart]
  by_cases h : Conn L x₀ w
  · right; rw [if_pos h]
  · left; rw [if_neg h]

/-- Paths from `x₀`'s component stay in `compPart`. -/
theorem conn_compPart {L : Finset (Sym2 Atom)} {x₀ x y : Atom} (hx : Conn L x₀ x) (h : Conn L x y) :
    Conn (compPart L x₀) x y := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail h' hbc ih =>
    refine ih.tail ⟨Finset.mem_filter.mpr ⟨hbc.1, _, Sym2.mem_mk_left _ _, hx.trans h'⟩, hbc.2⟩

theorem conn_restPart {L : Finset (Sym2 Atom)} {x₀ x y : Atom} (hx : ¬ Conn L x₀ x) (h : Conn L x y) :
    Conn (restPart L x₀) x y := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail h' hbc ih =>
    refine ih.tail ⟨Finset.mem_filter.mpr ⟨hbc.1, _, Sym2.mem_mk_left _ _, fun hb => hx (hb.trans (conn_symm h'))⟩, hbc.2⟩

/-! ## Joining two linkages with no atom in common -/

theorem degS_pos_of' {F : Finset (Sym2 Atom)} {e : Sym2 Atom} {w : Atom} (he : e ∈ F) (hw : w ∈ e) :
    0 < degS F w := Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨he, hw⟩⟩

def AtomDisj (L₁ L₂ : Finset (Sym2 Atom)) : Prop := ∀ w, degS L₁ w = 0 ∨ degS L₂ w = 0

theorem disjoint_of_atomDisj {L₁ L₂ : Finset (Sym2 Atom)} (h : AtomDisj L₁ L₂) : Disjoint L₁ L₂ := by
  rw [Finset.disjoint_left]; intro e h1 h2
  obtain ⟨w, hw⟩ := exists_mem_sym2 e
  rcases h w with h0 | h0
  · exact absurd h0 (Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨h1, hw⟩⟩).ne'
  · exact absurd h0 (Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨h2, hw⟩⟩).ne'

theorem linkage_union {L₁ L₂ : Finset (Sym2 Atom)} {B₁ B₂ : Finset Atom} (h1 : IsLinkageOn L₁ B₁)
    (h2 : IsLinkageOn L₂ B₂) (hd : AtomDisj L₁ L₂) : IsLinkageOn (L₁ ∪ L₂) (B₁ ∪ B₂) := by
  have hD := disjoint_of_atomDisj hd
  have hB1 : ∀ w ∈ B₁, degS L₂ w = 0 := fun w hw => (hd w).resolve_left (by rw [h1.1 w hw]; omega)
  have hB2 : ∀ w ∈ B₂, degS L₁ w = 0 := fun w hw => (hd w).resolve_right (by rw [h2.1 w hw]; omega)
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro w hw; rw [degS_union hD]
    rcases Finset.mem_union.mp hw with h | h
    · rw [h1.1 w h, hB1 w h]
    · rw [h2.1 w h, hB2 w h]
  · intro w hw; rw [degS_union hD]
    have a1 := h1.2.1 w (fun h => hw (Finset.mem_union_left _ h))
    have a2 := h2.2.1 w (fun h => hw (Finset.mem_union_right _ h))
    rcases hd w with z | z <;> rw [z] <;> omega
  · intro G hG hne hcl
    set G₁ := G.filter (· ∈ L₁)
    set G₂ := G.filter (· ∈ L₂)
    have cl : ∀ (L L' : Finset (Sym2 Atom)), (∀ w, degS L w = 0 ∨ degS L' w = 0) → G ⊆ L ∪ L' →
        Closed (G.filter (· ∈ L)) := by
      intro L L' hdd hGs w
      rcases hdd w with z | z
      · have : degS (G.filter (· ∈ L)) w = 0 := by
          have := degS_mono (show G.filter (· ∈ L) ⊆ L from fun e he => (Finset.mem_filter.mp he).2) w; omega
        rw [this]; exact Even.zero
      · have : degS (G.filter (· ∈ L)) w = degS G w := by
          unfold degS; congr 1; ext e; simp only [Finset.mem_filter]
          constructor
          · rintro ⟨⟨he, -⟩, hw⟩; exact ⟨he, hw⟩
          · rintro ⟨he, hw⟩
            refine ⟨⟨he, ?_⟩, hw⟩
            rcases Finset.mem_union.mp (hGs he) with h | h
            · exact h
            · exact absurd z (Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨h, hw⟩⟩).ne'
        rw [this]; exact hcl w
    have c1 := cl L₁ L₂ hd hG
    have c2 := cl L₂ L₁ (fun w => (hd w).symm) (by rw [Finset.union_comm]; exact hG)
    by_cases e1 : G₁.Nonempty
    · exact h1.2.2.1 G₁ (fun e he => (Finset.mem_filter.mp he).2) e1 c1
    by_cases e2 : G₂.Nonempty
    · exact h2.2.2.1 G₂ (fun e he => (Finset.mem_filter.mp he).2) e2 c2
    obtain ⟨e, he⟩ := hne
    rcases Finset.mem_union.mp (hG he) with h | h
    · exact e1 ⟨e, Finset.mem_filter.mpr ⟨he, h⟩⟩
    · exact e2 ⟨e, Finset.mem_filter.mpr ⟨he, h⟩⟩
  · intro e he
    rcases Finset.mem_union.mp he with h | h
    · exact h1.2.2.2 e h
    · exact h2.2.2.2 e h

/-- A path in the union, starting at an atom not on `L₂`, stays in `L₁`. -/
theorem conn_union_left {L₁ L₂ : Finset (Sym2 Atom)} (hd : AtomDisj L₁ L₂) {x y : Atom} (hx : degS L₂ x = 0)
    (h : Conn (L₁ ∪ L₂) x y) : Conn L₁ x y := by
  have key : Conn L₁ x y ∧ degS L₂ y = 0 := by
    induction h with
    | refl => exact ⟨Relation.ReflTransGen.refl, hx⟩
    | @tail b c _ hbc ih =>
      obtain ⟨ih1, ih2⟩ := ih
      have hin : s(b, c) ∈ L₁ := by
        rcases Finset.mem_union.mp hbc.1 with h | h
        · exact h
        · exact absurd ih2 (degS_pos_of' h (Sym2.mem_mk_left b c)).ne'
      refine ⟨ih1.tail ⟨hin, hbc.2⟩, ?_⟩
      exact (hd c).resolve_left (degS_pos_of' hin (Sym2.mem_mk_right b c)).ne'
  exact key.1

/-! ## Linkages are bounded: every atom lies within `2 |L|` of an end -/

theorem level_cross {L : Finset (Sym2 Atom)} (f : Atom → ℤ) {a b : Atom} (h : Conn L a b) {t : ℤ}
    (ha : f a ≤ t) (hb : t < f b) : ∃ u w, s(u, w) ∈ L ∧ f u ≤ t ∧ t < f w := by
  induction h with
  | refl => omega
  | @tail c d _ hcd ih =>
    by_cases hc : f c ≤ t
    · exact ⟨c, d, hcd.1, hc, hb⟩
    · exact ih (by omega)

theorem conn_level_bound {L : Finset (Sym2 Atom)} (f : Atom → ℤ)
    (hstep : ∀ u w, s(u, w) ∈ L → f w ≤ f u + 2 ∧ f u ≤ f w + 2) {a b : Atom} (h : Conn L a b) :
    f b ≤ f a + 2 * L.card := by
  by_contra hlt
  push Not at hlt
  -- each level t in [f a, f a + 2|L| + 1) is crossed by an edge; an edge crosses at most two levels
  set T := Finset.Ico (f a) (f a + 2 * L.card + 1)
  have hcross : ∀ t ∈ T, ∃ u w, s(u, w) ∈ L ∧ f u ≤ t ∧ t < f w := fun t ht => by
    obtain ⟨h1, h2⟩ := Finset.mem_Ico.mp ht
    exact level_cross f h h1 (by omega)
  choose! U W hUW hU hW using hcross
  have hmaps : ∀ t ∈ T, s(U t, W t) ∈ L := fun t ht => hUW t ht
  have hfib : ∀ e ∈ L, (T.filter (fun t => s(U t, W t) = e)).card ≤ 2 := by
    intro e he
    induction e using Sym2.ind with
    | _ x y =>
      have hxy := hstep x y he
      apply (Finset.card_le_card (t := Finset.Ico (min (f x) (f y)) (min (f x) (f y) + 2)) ?_).trans (by simp)
      intro t htf
      obtain ⟨htT, heq⟩ := Finset.mem_filter.mp htf
      have h1 := hU t htT; have h2 := hW t htT
      simp only [Finset.mem_Ico]
      rcases Sym2.eq_iff.mp heq with ⟨e1, e2⟩ | ⟨e1, e2⟩
      · rw [e1] at h1; rw [e2] at h2; constructor <;> omega
      · rw [e1] at h1; rw [e2] at h2; constructor <;> omega
  have hcard := Finset.card_le_mul_card_image_of_maps_to (f := fun t => s(U t, W t)) hmaps 2
    (fun e he => hfib e he)
  simp only [T, Int.card_Ico] at hcard
  have : (f a + 2 * L.card + 1 - f a).toNat = 2 * L.card + 1 := by omega
  rw [this] at hcard
  omega

/-- Every far linkage with `s` edges ending at `Q` lies in the boxes of radius `2 s` about its ends. -/
theorem farL_in_box {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : FarL τ k Q F) :
    F ⊆ (Q.biUnion (fun p => box (upA k p) (2 * F.card))).sym2 := by
  have hb : ∀ x, (∃ e ∈ F, x ∈ e) → x ∈ Q.biUnion (fun p => box (upA k p) (2 * F.card)) := by
    rintro x ⟨e, he, hx⟩
    obtain ⟨b, hbQ, hconn⟩ := reaches_end hF.1 he hx
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hbQ
    have st : ∀ (f : Atom → ℤ), (∀ a b, Bond τ a b → f a ≤ f b + 2 ∧ f b ≤ f a + 2) →
        f x ≤ f (upA k p) + 2 * F.card ∧ f (upA k p) ≤ f x + 2 * F.card := by
      intro f hfb
      have hs : ∀ u w, s(u, w) ∈ F → f w ≤ f u + 2 ∧ f u ≤ f w + 2 := fun u w h => by
        have := hfb u w (bondS_mk.mp (hF.2.2 _ h)); omega
      have hs' : ∀ u w, s(u, w) ∈ F → -f w ≤ -f u + 2 ∧ -f u ≤ -f w + 2 := fun u w h => by
        have := hs u w h; omega
      have c1 := conn_level_bound f hs (conn_symm hconn)
      have c2 := conn_level_bound (fun y => -f y) hs' (conn_symm hconn)
      omega
    have h1 := st (fun y => y.1) (fun a b h => (bond_steps h).1)
    have h2 := st (fun y => y.2.1.1) (fun a b h => (bond_steps h).2.1)
    have h3 := st (fun y => y.2.1.2) (fun a b h => (bond_steps h).2.2)
    refine Finset.mem_biUnion.mpr ⟨p, hp, ?_⟩
    simp only [box, Finset.mem_product, Finset.mem_Icc, Finset.mem_univ, and_true]
    push_cast
    omega
  intro e he
  induction e using Sym2.ind with
  | _ a b =>
    rw [Finset.mk_mem_sym2_iff]
    exact ⟨hb a ⟨_, he, Sym2.mem_mk_left a b⟩, hb b ⟨_, he, Sym2.mem_mk_right a b⟩⟩

theorem farSet_finite (τ : ℤ → ZMod 3) (k : ℤ) (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) :
    (FarSet τ k Q N s).Finite := by
  apply Set.Finite.subset (Finset.finite_toSet ((Q.biUnion (fun p => box (upA k p) (2 * s))).sym2.powerset))
  rintro F ⟨hF, hs, -⟩
  rw [Finset.mem_coe, Finset.mem_powerset]
  have := farL_in_box hF; rwa [hs] at this

end LoopEqualityProof
