module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Parts
public import LoopEquality.Counting
public import LoopEquality.Finiteness
public import LoopEquality.TheoremB
public import LoopEquality.Transfer

@[expose] public section

/-!
# Pairings of linkages (Lean paper, Theorem B in #102's form, step 2a-2b)

* `pairR k R P`, `pairF k F P`: the pairs of crossing points joined by the root (far) linkage, as a finset of `P ×ˢ P`.
* `OneCycleRel P M M'`: no nonempty proper subset of `P` is closed under both relations; `singleCycle_iff`:
  `SingleCycle k P R F ↔ OneCycleRel P (pairR k R P) (pairF k F P)`.
* `linkage_near`: every atom of a linkage with ends `B` is joined to an end (so lies within reach of `B`).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

noncomputable def pairR (k : ℤ) (R : Finset (Sym2 Atom)) (P : Finset (ℤ × ℤ)) : Finset ((ℤ × ℤ) × (ℤ × ℤ)) :=
  (P ×ˢ P).filter (fun pq => Conn R (loA k pq.1) (loA k pq.2))

noncomputable def pairF (k : ℤ) (F : Finset (Sym2 Atom)) (P : Finset (ℤ × ℤ)) : Finset ((ℤ × ℤ) × (ℤ × ℤ)) :=
  (P ×ˢ P).filter (fun pq => Conn F (upA k pq.1) (upA k pq.2))

/-- No nonempty proper subset of `P` is closed under both relations. -/
def OneCycleRel (P : Finset (ℤ × ℤ)) (M M' : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : Prop :=
  ∀ Q ⊆ P, Q.Nonempty → (∀ p ∈ Q, ∀ q ∈ P, (p, q) ∈ M → q ∈ Q) → (∀ p ∈ Q, ∀ q ∈ P, (p, q) ∈ M' → q ∈ Q) → Q = P

theorem singleCycle_iff (k : ℤ) (P : Finset (ℤ × ℤ)) (R F : Finset (Sym2 Atom)) :
    SingleCycle k P R F ↔ OneCycleRel P (pairR k R P) (pairF k F P) := by
  unfold SingleCycle OneCycleRel pairR pairF
  constructor
  · intro h Q hQ hne h1 h2
    apply h Q hQ hne
    · intro p hp q hq hc; exact h1 p hp q hq (Finset.mem_filter.mpr ⟨Finset.mem_product.mpr ⟨hQ hp, hq⟩, hc⟩)
    · intro p hp q hq hc; exact h2 p hp q hq (Finset.mem_filter.mpr ⟨Finset.mem_product.mpr ⟨hQ hp, hq⟩, hc⟩)
  · intro h Q hQ hne h1 h2
    apply h Q hQ hne
    · intro p hp q hq hm; exact h1 p hp q hq (Finset.mem_filter.mp hm).2
    · intro p hp q hq hm; exact h2 p hp q hq (Finset.mem_filter.mp hm).2

/-! ## Step 2c: counting pairs of linkages by their pairings and sizes -/

/-- Root linkages of `G σ` through `v` ending at `P`, with `r` edges and pairing `M`. -/
def RootSet (σ : ℤ → ZMod 3) (v : Atom) (k : ℤ) (P : Finset (ℤ × ℤ)) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (r : ℕ) :
    Set (Finset (Sym2 Atom)) :=
  {R | RootL σ k P R ∧ 0 < degS R v ∧ R.card = r ∧ pairR k R P = M}

/-- Far linkages of `G σ` ending at `Q`, with `s` edges and pairing `N`. -/
def FarSet (σ : ℤ → ZMod 3) (k : ℤ) (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) :
    Set (Finset (Sym2 Atom)) :=
  {F | FarL σ k Q F ∧ F.card = s ∧ pairF k F Q = N}

/-- Pairs (root linkage through `v` ending at `P`, far linkage ending at `Q`) with `l` edges in all (counting
`|P|` vertical bonds) whose pairings satisfy `C`. -/
def GenParts (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (P Q : Finset (ℤ × ℤ))
    (C : Finset ((ℤ × ℤ) × (ℤ × ℤ)) → Finset ((ℤ × ℤ) × (ℤ × ℤ)) → Prop) :
    Set (Finset (Sym2 Atom) × Finset (Sym2 Atom)) :=
  {RF | RootL σ k P RF.1 ∧ FarL σ k Q RF.2 ∧ 0 < degS RF.1 v ∧ RF.1.card + P.card + RF.2.card = l ∧
    C (pairR k RF.1 P) (pairF k RF.2 Q)}

/-- The index set: pairings `M ⊆ P × P`, `N ⊆ Q × Q`, sizes `r`, `s` with `r + |P| + s = l`, and `C M N`. -/
noncomputable def idxSet (l : ℕ) (P Q : Finset (ℤ × ℤ))
    (C : Finset ((ℤ × ℤ) × (ℤ × ℤ)) → Finset ((ℤ × ℤ) × (ℤ × ℤ)) → Prop) :
    Finset ((Finset ((ℤ × ℤ) × (ℤ × ℤ)) × Finset ((ℤ × ℤ) × (ℤ × ℤ))) × (ℕ × ℕ)) :=
  (((P ×ˢ P).powerset ×ˢ (Q ×ˢ Q).powerset) ×ˢ (Finset.range (l + 1) ×ˢ Finset.range (l + 1))).filter
    (fun x => x.2.1 + P.card + x.2.2 = l ∧ C x.1.1 x.1.2)

theorem pairR_sub (k : ℤ) (R : Finset (Sym2 Atom)) (P : Finset (ℤ × ℤ)) : pairR k R P ⊆ P ×ˢ P :=
  Finset.filter_subset _ _
theorem pairF_sub (k : ℤ) (F : Finset (Sym2 Atom)) (P : Finset (ℤ × ℤ)) : pairF k F P ⊆ P ×ˢ P :=
  Finset.filter_subset _ _

theorem genParts_eq (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (P Q : Finset (ℤ × ℤ))
    (C : Finset ((ℤ × ℤ) × (ℤ × ℤ)) → Finset ((ℤ × ℤ) × (ℤ × ℤ)) → Prop) :
    GenParts σ v l k P Q C = ⋃ x ∈ (↑(idxSet l P Q C) : Set ((Finset ((ℤ × ℤ) × (ℤ × ℤ)) × Finset ((ℤ × ℤ) × (ℤ × ℤ))) × (ℕ × ℕ))),
      RootSet σ v k P x.1.1 x.2.1 ×ˢ FarSet σ k Q x.1.2 x.2.2 := by
  ext ⟨R, F⟩
  simp only [Set.mem_iUnion, Set.mem_prod, exists_prop, Finset.mem_coe]
  constructor
  · rintro ⟨hR, hF, hd, hc, hC⟩
    change R.card + P.card + F.card = l at hc
    refine ⟨((pairR k R P, pairF k F Q), (R.card, F.card)), ?_, ⟨hR, hd, rfl, rfl⟩, ⟨hF, rfl, rfl⟩⟩
    simp only [idxSet, Finset.mem_filter, Finset.mem_product, Finset.mem_powerset, Finset.mem_range]
    exact ⟨⟨⟨pairR_sub k R P, pairF_sub k F Q⟩, by omega, by omega⟩, hc, hC⟩
  · rintro ⟨x, hx, ⟨hR, hd, hr, hM⟩, ⟨hF, hs, hN⟩⟩
    simp only [idxSet, Finset.mem_filter] at hx
    refine ⟨hR, hF, hd, by rw [hr, hs]; exact hx.2.1, by rw [hM, hN]; exact hx.2.2⟩

/-- **Counting by pairings.** If the pairs are finitely many, their number is
`Σ_{(M, N, r, s)} #RootSet(P, M, r) · #FarSet(Q, N, s)` over the index set. -/
theorem ncard_genParts {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {P Q : Finset (ℤ × ℤ)}
    {C : Finset ((ℤ × ℤ) × (ℤ × ℤ)) → Finset ((ℤ × ℤ) × (ℤ × ℤ)) → Prop}
    (hfin : (GenParts σ v l k P Q C).Finite) :
    (GenParts σ v l k P Q C).ncard = ∑ x ∈ idxSet l P Q C,
      (RootSet σ v k P x.1.1 x.2.1).ncard * (FarSet σ k Q x.1.2 x.2.2).ncard := by
  have hE := genParts_eq σ v l k P Q C
  rw [hE, Set.Finite.ncard_biUnion (Finset.finite_toSet _)]
  · rw [finsum_mem_coe_finset]
    exact Finset.sum_congr rfl (fun x _ => Set.ncard_prod)
  · intro x hx
    apply hfin.subset
    rw [hE]; exact Set.subset_biUnion_of_mem (u := fun x => RootSet σ v k P x.1.1 x.2.1 ×ˢ FarSet σ k Q x.1.2 x.2.2) hx
  · intro x _ y _ hxy
    rw [Function.onFun, Set.disjoint_left]
    rintro ⟨R, F⟩ ⟨⟨-, -, hr, hM⟩, ⟨-, hs, hN⟩⟩ ⟨⟨-, -, hr', hM'⟩, ⟨-, hs', hN'⟩⟩
    apply hxy
    ext1
    · ext1
      · exact hM.symm.trans hM'
      · exact hN.symm.trans hN'
    · ext1
      · exact hr.symm.trans hr'
      · exact hs.symm.trans hs'

/-! ## The two counted sets of Theorem B in this form, and their finiteness -/

theorem partsCross_eq_gen (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (P : Finset (ℤ × ℤ)) :
    PartsCross σ v l k P = GenParts σ v l k P P (OneCycleRel P) := by
  ext RF
  simp only [PartsCross, GenParts, Set.mem_setOf_eq, singleCycle_iff]

/-- The half-turn on pairs of points. -/
def gg (c : ℤ × ℤ) (pq : (ℤ × ℤ) × (ℤ × ℤ)) : (ℤ × ℤ) × (ℤ × ℤ) := (c - pq.1, c - pq.2)

theorem pairF_image (c : ℤ × ℤ) (k : ℤ) (F : Finset (Sym2 Atom)) (P : Finset (ℤ × ℤ)) :
    pairF k (F.image (htS c)) P = (pairF k F (P.image (fun p => c - p))).image (gg c) := by
  ext ⟨p, q⟩
  simp only [pairF, Finset.mem_filter, Finset.mem_product, Finset.mem_image, gg, Prod.mk.injEq]
  have hconn : Conn F (upA k (c - p)) (upA k (c - q)) ↔ Conn (F.image (htS c)) (upA k p) (upA k q) := by
    have := conn_image (htA_invol c) F (upA k (c - p)) (upA k (c - q))
    rwa [htA_upA, htA_upA, sub_sub_cancel, sub_sub_cancel] at this
  constructor
  · rintro ⟨⟨hp, hq⟩, hc⟩
    refine ⟨(c - p, c - q), ⟨⟨⟨p, hp, rfl⟩, ⟨q, hq, rfl⟩⟩, hconn.mpr hc⟩, sub_sub_cancel c p, sub_sub_cancel c q⟩
  · rintro ⟨⟨a, b⟩, ⟨⟨⟨p', hp', rfl⟩, ⟨q', hq', rfl⟩⟩, hc⟩, h1, h2⟩
    simp only at h1 h2 hc
    rw [sub_sub_cancel] at h1 h2; subst h1; subst h2
    exact ⟨⟨hp', hq'⟩, hconn.mp hc⟩

theorem flipParts_eq_gen (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (P : Finset (ℤ × ℤ)) (c : ℤ × ℤ) :
    FlipParts σ v l k P c = GenParts σ v l k P (P.image (fun p => c - p)) (fun M N => OneCycleRel P M (N.image (gg c))) := by
  ext RF
  simp only [FlipParts, GenParts, Set.mem_setOf_eq, singleCycle_iff, pairF_image]

theorem partsCross_finite {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {P : Finset (ℤ × ℤ)}
    (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p)) : (PartsCross σ v l k P).Finite := by
  apply ((polys_finite σ v l).image (fun E => (E.filter (fun e => ∀ w ∈ e, ¬ IsFar k w),
    E.filter (fun e => ∀ w ∈ e, IsFar k w)))).subset
  rintro ⟨R, F⟩ ⟨⟨hRl, hRs, hRb⟩, ⟨hFl, hFs, hFb⟩, hdv, hcard, hsc⟩
  refine ⟨R ∪ P.image (vert k) ∪ F, ⟨?_, ?_, ?_⟩, ?_⟩
  · apply parts_to_polygon hP hRl hFl hRs hFs _ hsc
    intro e he
    rcases Finset.mem_union.mp he with h | h
    · rcases Finset.mem_union.mp h with h | h
      · exact hRb e h
      · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp h; exact hV p hp
    · exact hFb e h
  · exact (Finset.card_pos.mpr ⟨_, Finset.mem_filter.mpr ⟨Finset.mem_union_left _ (Finset.mem_union_left _
      (Finset.mem_filter.mp (Finset.card_pos.mp hdv).choose_spec).1), (Finset.mem_filter.mp (Finset.card_pos.mp hdv).choose_spec).2⟩⟩)
  · rw [card_three hRs hFs]; exact hcard
  · simp only [filter_root_three hRs hFs, filter_far_three hRs hFs]

theorem flipParts_finite {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p)) : (FlipParts σ v l k P c).Finite := by
  have hinv := htA_invol c
  have hS : htS c = Sym2.map (htA c) := rfl
  apply ((partsCross_finite (σ := flipAt σ k) (v := v) (l := l) hP (fun p hp => bondS_vert_flip.mp (hV p hp))).image
    (fun RF => (RF.1, RF.2.image (htS c)))).subset
  rintro ⟨R, F⟩ ⟨hR, ⟨hFl, hFs, hFb⟩, hdv, hcard, hsc⟩
  obtain ⟨t1, t2, t3, t4, -⟩ := flip_transfer hc hFl hFs hFb
  rw [image_sub_sub] at t1
  refine ⟨(R, F.image (htS c)), ⟨(rootL_flip hc).mp hR, ⟨t1, t2, t3⟩, hdv, by rw [t4]; exact hcard, hsc⟩, ?_⟩
  simp only [Prod.mk.injEq, true_and]
  rw [hS]; exact image_image_invol hinv F

end LoopEqualityProof
