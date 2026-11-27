module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Surgery
public import LoopEquality.Polygons

@[expose] public section

/-!
# Theorem A for polygons crossing a bilayer at most twice (Lean paper, Milestone 2c, part 2)

Study 2026-11-15-polygon-bijection, Theorem A and Corollary A1.

A **polygon** of `G σ` is a nonempty finite set of bonds in which every atom has even degree and no
nonempty proper subset has that property (a minimal nonempty even edge set, that is, a cycle).

* `even_card_cross` (parity): a closed edge set without loops crosses the cut at bilayer `k` an even number
  of times.
* `surgery_polygon` (Theorem A, at most two crossings): if a polygon `E` of `G σ` crosses bilayer `k` at
  most twice and the half-turn `p ↦ c − p` (`c ≡ 2·σ k`) carries its crossing edges onto themselves, the
  surgered set is a polygon of `G (flipAt σ k)` with the same number of edges and the same crossing edges.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

/-- Bonds as a predicate on unordered edges. -/
def BondS (σ : ℤ → ZMod 3) : Sym2 Atom → Prop :=
  Sym2.lift ⟨Bond σ, fun _ _ => propext ⟨bond_symm, bond_symm⟩⟩

theorem bondS_mk {σ : ℤ → ZMod 3} {a b : Atom} : BondS σ s(a, b) ↔ Bond σ a b := by
  simp only [BondS, Sym2.lift_mk]

theorem bond_ne {σ : ℤ → ZMod 3} {a b : Atom} (h : Bond σ a b) : a ≠ b := by
  intro hab; subst hab
  obtain ⟨-, -, hb⟩ := h
  rcases hb with ⟨-, -, h3⟩ | ⟨h1, -⟩ | ⟨h1, -⟩
  · exact h3 rfl
  · omega
  · omega

theorem bondS_surgS {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {e : Sym2 Atom}
    (h : BondS σ e) : BondS (flipAt σ k) (surgS c k e) := by
  induction e using Sym2.ind with
  | _ a b =>
    rw [bondS_mk] at h
    have := surg_bond hc (e := (a, b)) h
    by_cases hff : IsFar k a ∧ IsFar k b
    · rw [surgS_far hff, bondS_mk]
      rw [surg_far (e := (a, b)) hff] at this
      simpa only [twist_eq_htA hff.1, twist_eq_htA hff.2] using this
    · rw [surgS_other hff, bondS_mk]
      rw [surg_other (e := (a, b)) hff] at this
      exact this

theorem isCrossS_surgS {c : ℤ × ℤ} {k : ℤ} {e : Sym2 Atom} : IsCrossS k (surgS c k e) ↔ IsCrossS k e := by
  induction e using Sym2.ind with
  | _ a b =>
    by_cases hff : IsFar k a ∧ IsFar k b
    · rw [surgS_far hff, isCrossS_mk, isCrossS_mk, isFar_htA, isFar_htA]
    · rw [surgS_other hff]

theorem surgS_cross {c : ℤ × ℤ} {k : ℤ} {e : Sym2 Atom} (h : IsCrossS k e) : surgS c k e = e := by
  induction e using Sym2.ind with
  | _ a b =>
    apply surgS_other
    rw [isCrossS_mk] at h
    tauto

/-- Every atom has even degree. -/
def Closed (E : Finset (Sym2 Atom)) : Prop := ∀ x, Even (degS E x)

/-- A polygon of `G σ`: a nonempty set of bonds, closed, and minimal with these properties. -/
def IsPolygon (σ : ℤ → ZMod 3) (E : Finset (Sym2 Atom)) : Prop :=
  E.Nonempty ∧ (∀ e ∈ E, BondS σ e) ∧ Closed E ∧ ∀ F ⊆ E, F.Nonempty → Closed F → F = E

/-- The ends of an edge, as a finset. -/
def endsF (e : Sym2 Atom) : Finset Atom :=
  Sym2.lift ⟨fun a b => ({a, b} : Finset Atom), fun a b => Finset.pair_comm a b⟩ e

theorem mem_endsF {x : Atom} {e : Sym2 Atom} : x ∈ endsF e ↔ x ∈ e := by
  induction e using Sym2.ind with
  | _ a b => simp [endsF, Sym2.mem_iff]

open Classical in
/-- **Parity.** A closed edge set without loops crosses the cut an even number of times. -/
theorem even_card_cross (k : ℤ) (F : Finset (Sym2 Atom)) (hF : Closed F) (hnd : ∀ e ∈ F, ¬ e.IsDiag) :
    Even (F.filter (IsCrossS k)).card := by
  -- the far ends of the edges of F
  set V : Finset Atom := (F.biUnion endsF).filter (IsFar k) with hV
  -- count the pairs (far atom, edge at it) two ways
  have hsum : ∑ x ∈ V, degS F x = ∑ e ∈ F, (V.filter (fun x => x ∈ e)).card := by
    unfold degS
    simp only [Finset.card_eq_sum_ones, Finset.sum_filter]
    exact Finset.sum_comm
  have hedge : ∀ e ∈ F, (V.filter (fun x => x ∈ e)).card =
      (if IsCrossS k e then 1 else 0) + 2 * (if ¬ IsCrossS k e ∧ (∃ x ∈ e, IsFar k x) then 1 else 0) := by
    intro e he
    induction e using Sym2.ind with
    | _ a b =>
      have hab : a ≠ b := fun h => hnd _ he (by rw [h]; exact Sym2.mk_isDiag_iff.mpr rfl)
      have haV : IsFar k a → a ∈ V := fun h => by
        rw [hV, Finset.mem_filter, Finset.mem_biUnion]
        exact ⟨⟨s(a, b), he, mem_endsF.mpr (Sym2.mem_mk_left a b)⟩, h⟩
      have hbV : IsFar k b → b ∈ V := fun h => by
        rw [hV, Finset.mem_filter, Finset.mem_biUnion]
        exact ⟨⟨s(a, b), he, mem_endsF.mpr (Sym2.mem_mk_right a b)⟩, h⟩
      have hfilt : V.filter (fun x => x ∈ s(a, b)) = V.filter (fun x => x = a ∨ x = b) := by
        apply Finset.filter_congr; intro x _; exact Sym2.mem_iff
      rw [hfilt, isCrossS_mk]
      by_cases ha : IsFar k a <;> by_cases hb : IsFar k b
      · have : V.filter (fun x => x = a ∨ x = b) = {a, b} := by
          ext x; simp only [Finset.mem_filter, Finset.mem_insert, Finset.mem_singleton]
          constructor
          · exact fun h => h.2
          · rintro (h | h)
            · subst h; exact ⟨haV ha, Or.inl rfl⟩
            · subst h; exact ⟨hbV hb, Or.inr rfl⟩
        rw [this, Finset.card_pair hab]
        simp [ha, hb]
      · have : V.filter (fun x => x = a ∨ x = b) = {a} := by
          ext x; simp only [Finset.mem_filter, Finset.mem_singleton]
          constructor
          · rintro ⟨hx, h | h⟩
            · exact h
            · subst h; exact absurd ((Finset.mem_filter.mp hx).2) hb
          · rintro h; subst h; exact ⟨haV ha, Or.inl rfl⟩
        rw [this, Finset.card_singleton]
        simp [ha, hb]
      · have : V.filter (fun x => x = a ∨ x = b) = {b} := by
          ext x; simp only [Finset.mem_filter, Finset.mem_singleton]
          constructor
          · rintro ⟨hx, h | h⟩
            · subst h; exact absurd ((Finset.mem_filter.mp hx).2) ha
            · exact h
          · rintro h; subst h; exact ⟨hbV hb, Or.inr rfl⟩
        rw [this, Finset.card_singleton]
        simp [ha, hb]
      · have : V.filter (fun x => x = a ∨ x = b) = ∅ := by
          ext x; simp only [Finset.mem_filter, Finset.notMem_empty, iff_false, not_and]
          intro hx h
          rcases h with h | h
          · subst h; exact ha ((Finset.mem_filter.mp hx).2)
          · subst h; exact hb ((Finset.mem_filter.mp hx).2)
        rw [this, Finset.card_empty]
        simp [ha, hb]
  have hleft : Even (∑ x ∈ V, degS F x) := Finset.even_sum _ (fun x _ => hF x)
  rw [hsum, Finset.sum_congr rfl hedge] at hleft
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum] at hleft
  have h2 : Even (2 * ∑ e ∈ F, if ¬ IsCrossS k e ∧ (∃ x ∈ e, IsFar k x) then 1 else 0) := even_two_mul _
  have hcross : ∑ e ∈ F, (if IsCrossS k e then 1 else 0) = (F.filter (IsCrossS k)).card := by
    rw [Finset.card_eq_sum_ones, Finset.sum_filter]
  rw [← hcross]
  exact (Nat.even_add.mp hleft).mpr h2

theorem closed_surgS {c : ℤ × ℤ} {k : ℤ} {F : Finset (Sym2 Atom)} (hF : Closed F)
    (hP : ∀ e ∈ F, IsCrossS k e → htS c e ∈ F) : Closed (F.image (surgS c k)) := by
  intro x
  by_cases hx : IsFar k x
  · rw [degS_surg_far c k F hP hx]; exact hF _
  · rw [degS_surg_root c k F hx]; exact hF _

theorem surgS_mem_image {c : ℤ × ℤ} {k : ℤ} {E F : Finset (Sym2 Atom)} (h : F ⊆ E.image (surgS c k)) :
    F.image (surgS c k) ⊆ E := by
  intro f hf
  obtain ⟨f', hf', rfl⟩ := Finset.mem_image.mp hf
  obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp (h hf')
  rw [surgS_surgS]; exact he

open Classical in
theorem cross_image_surgS {c : ℤ × ℤ} {k : ℤ} (E : Finset (Sym2 Atom)) :
    (E.image (surgS c k)).filter (IsCrossS k) = E.filter (IsCrossS k) := by
  ext f
  simp only [Finset.mem_filter, Finset.mem_image]
  constructor
  · rintro ⟨⟨e, he, rfl⟩, hcr⟩
    have hcr' : IsCrossS k e := isCrossS_surgS.mp hcr
    rw [surgS_cross hcr']; exact ⟨he, hcr'⟩
  · rintro ⟨he, hcr⟩
    exact ⟨⟨f, he, surgS_cross hcr⟩, hcr⟩

open Classical in
/-- **Theorem A (at most two crossings).** Let `E` be a polygon of `G σ` crossing bilayer `k` at most
twice, and let the half-turn `p ↦ c − p` (`c ≡ 2·σ k`) carry its crossing edges onto crossing edges of `E`.
Then the surgered set is a polygon of the flipped network `G (flipAt σ k)`, with the same number of edges
and the same crossing edges. -/
theorem surgery_polygon {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) (hle : (E.filter (IsCrossS k)).card ≤ 2)
    (hP : ∀ e ∈ E, IsCrossS k e → htS c e ∈ E) :
    IsPolygon (flipAt σ k) (E.image (surgS c k)) ∧ (E.image (surgS c k)).card = E.card ∧
      (E.image (surgS c k)).filter (IsCrossS k) = E.filter (IsCrossS k) := by
  obtain ⟨hne, hbond, hcl, hmin⟩ := hE
  refine ⟨⟨hne.image _, ?_, closed_surgS hcl hP, ?_⟩,
    Finset.card_image_of_injective _ (surgS_injective c k), cross_image_surgS E⟩
  · intro f hf
    obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp hf
    exact bondS_surgS hc (hbond e he)
  · intro F' hF' hF'ne hF'cl
    -- the crossing edges of F' are among those of E, and there are 0 or 2 of them
    have hnd : ∀ e ∈ F', ¬ e.IsDiag := by
      intro e he hd
      obtain ⟨e0, he0, rfl⟩ := Finset.mem_image.mp (hF' he)
      have hb := bondS_surgS hc (hbond e0 he0)
      induction e0 using Sym2.ind with
      | _ a b =>
        by_cases hff : IsFar k a ∧ IsFar k b
        · rw [surgS_far hff] at hd hb
          rw [bondS_mk] at hb
          exact bond_ne hb (Sym2.mk_isDiag_iff.mp hd)
        · rw [surgS_other hff] at hd hb
          rw [bondS_mk] at hb
          exact bond_ne hb (Sym2.mk_isDiag_iff.mp hd)
    have hsub : F'.filter (IsCrossS k) ⊆ E.filter (IsCrossS k) := by
      intro f hf
      rw [← cross_image_surgS (c := c) E]
      simp only [Finset.mem_filter] at hf ⊢
      exact ⟨hF' hf.1, hf.2⟩
    have hev := even_card_cross k F' hF'cl hnd
    have hcardle := Finset.card_le_card hsub
    have hPF : ∀ e ∈ F', IsCrossS k e → htS c e ∈ F' := by
      intro e he hcr
      have h2 : (F'.filter (IsCrossS k)).card = 2 := by
        have h1 : 0 < (F'.filter (IsCrossS k)).card :=
          Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨he, hcr⟩⟩
        rcases hev with ⟨m, hm⟩
        omega
      have heq : F'.filter (IsCrossS k) = E.filter (IsCrossS k) :=
        Finset.eq_of_subset_of_card_le hsub (by omega)
      have heE : e ∈ E.filter (IsCrossS k) := hsub (Finset.mem_filter.mpr ⟨he, hcr⟩)
      have hhtE : htS c e ∈ E.filter (IsCrossS k) :=
        Finset.mem_filter.mpr ⟨hP e (Finset.mem_filter.mp heE).1 hcr, isCrossS_htS.mpr hcr⟩
      rw [← heq] at hhtE
      exact (Finset.mem_filter.mp hhtE).1
    -- pull F' back: a closed nonempty subset of E, hence all of E
    have hFE : F'.image (surgS c k) ⊆ E := surgS_mem_image hF'
    have hFeq := hmin _ hFE (hF'ne.image _) (closed_surgS hF'cl hPF)
    rw [← hFeq, Finset.image_image]
    have : surgS c k ∘ surgS c k = id := funext (surgS_surgS c k)
    rw [this, Finset.image_id]

/-- The vertical bond of bilayer `k` at the planar point `p`. -/
def vert (k : ℤ) (p : ℤ × ℤ) : Sym2 Atom := s((k, p, 0), (k, p, 1))

theorem htS_vert (c : ℤ × ℤ) (k : ℤ) (p : ℤ × ℤ) : htS c (vert k p) = vert k (c - p) := rfl

theorem isCrossS_vert (k : ℤ) (p : ℤ × ℤ) : IsCrossS k (vert k p) := by
  rw [vert, isCrossS_mk]; right; unfold IsFar; simp

open Classical in
/-- Polygons of `G σ` through the atom `v` whose crossing edges at bilayer `k` are exactly `S`. -/
def PolysThrough (σ : ℤ → ZMod 3) (k : ℤ) (v : Atom) (S : Finset (Sym2 Atom)) : Set (Finset (Sym2 Atom)) :=
  {E | IsPolygon σ E ∧ 0 < degS E v ∧ E.filter (IsCrossS k) = S}

open Classical in
theorem mapsTo_surgery {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {v : Atom}
    (hv : ¬ IsFar k v) {S : Finset (Sym2 Atom)} (hS : S.card ≤ 2) (hSc : ∀ e ∈ S, htS c e ∈ S) :
    Set.MapsTo (fun (E : Finset (Sym2 Atom)) => E.image (surgS c k)) (PolysThrough σ k v S) (PolysThrough (flipAt σ k) k v S) := by
  intro E ⟨hE, hvE, hcross⟩
  have hP : ∀ e ∈ E, IsCrossS k e → htS c e ∈ E := by
    intro e he hcr
    have heS : e ∈ S := by rw [← hcross]; exact Finset.mem_filter.mpr ⟨he, hcr⟩
    have := hSc e heS
    rw [← hcross] at this
    exact (Finset.mem_filter.mp this).1
  obtain ⟨hpoly, -, hcr⟩ := surgery_polygon hc hE (by rw [hcross]; exact hS) hP
  exact ⟨hpoly, by rw [degS_surg_root c k E hv]; exact hvE, by rw [hcr, hcross]⟩

open Classical in
/-- **Corollary A1 at one flip.** For a set `S` of at most two crossing edges kept by the half-turn about
`c` (`c ≡ 2·σ k`), and an atom `v` of the root half, the surgery is a bijection between the polygons through
`v` with crossing edges `S` in `G σ` and those in the flipped network; it keeps the number of edges. -/
theorem bijOn_surgery {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {v : Atom}
    (hv : ¬ IsFar k v) {S : Finset (Sym2 Atom)} (hS : S.card ≤ 2) (hSc : ∀ e ∈ S, htS c e ∈ S) :
    Set.BijOn (fun (E : Finset (Sym2 Atom)) => E.image (surgS c k)) (PolysThrough σ k v S) (PolysThrough (flipAt σ k) k v S) ∧
      ∀ E : Finset (Sym2 Atom), (E.image (surgS c k)).card = E.card := by
  refine ⟨⟨mapsTo_surgery hc hv hS hSc, ?_, ?_⟩, fun E => Finset.card_image_of_injective _ (surgS_injective c k)⟩
  · intro E₁ _ E₂ _ h
    exact Finset.image_injective (surgS_injective c k) h
  · intro E' hE'
    have hback := mapsTo_surgery (goodCentre_flipAt hc) hv hS hSc hE'
    rw [flipAt_flipAt] at hback
    refine ⟨E'.image (surgS c k), hback, ?_⟩
    simp only [Finset.image_image]
    have : surgS c k ∘ surgS c k = id := funext (surgS_surgS c k)
    rw [this, Finset.image_id]

open Classical in
/-- The two-crossing case: the crossing edges are the vertical bonds at two points `p ≠ q` of the
position of bilayer `k`, and the centre is `c = p + q` (Lemma 2). -/
theorem bijOn_two_crossings {σ : ℤ → ZMod 3} {k : ℤ} {v : Atom} (hv : ¬ IsFar k v) {p q : ℤ × ℤ}
    (hp : (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k) (hq : (q.1 : ZMod 3) = σ k ∧ (q.2 : ZMod 3) = σ k) :
    Set.BijOn (fun (E : Finset (Sym2 Atom)) => E.image (surgS (p + q) k)) (PolysThrough σ k v {vert k p, vert k q})
      (PolysThrough (flipAt σ k) k v {vert k p, vert k q}) := by
  obtain ⟨hcentre, hp', hq'⟩ := halfturn_two_points hp hq
  refine (bijOn_surgery hcentre hv (Finset.card_le_two) ?_).1
  intro e he
  simp only [Finset.mem_insert, Finset.mem_singleton] at he ⊢
  rcases he with rfl | rfl
  · right; rw [htS_vert, hp']
  · left; rw [htS_vert, hq']

end LoopEqualityProof
