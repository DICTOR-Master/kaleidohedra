module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Surgery
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1
public import LoopEquality.Relabel

@[expose] public section

/-!
# Locality (Lean paper, Milestone 2f-3)

* `must_cross`: if a polygon has an edge at `v`, `v` is in the root half of bilayer `j`, and the polygon
  reaches the far half of `j`, then it has an edge crossing `j` (otherwise its root–root edges would form a
  smaller closed set).
* `reach_bound`: every atom of a polygon through `v` with `l` edges lies at bilayer at most `v.1 + l + 1`
  (crossing edges at different bilayers are different edges); `reach_bound_below` by the mirror.
* `polysA1_local`: two stackings that agree on the bilayers within `l + 1` of `v` have exactly the same
  polygons through `v` with `l` edges crossing every bilayer at most twice.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- `x` is an end of some edge of `E`. -/
def InE (E : Finset (Sym2 Atom)) (x : Atom) : Prop := ∃ e ∈ E, x ∈ e

theorem must_cross {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) {v x : Atom} {j : ℤ}
    (hv : 0 < degS E v) (hvr : ¬ IsFar j v) (hx : InE E x) (hxf : IsFar j x) :
    ∃ e ∈ E, IsCrossS j e := by
  by_contra hno
  push Not at hno
  obtain ⟨-, -, hcl, hmin⟩ := hE
  set F := E.filter (fun e => ∀ y ∈ e, ¬ IsFar j y) with hF
  -- F is closed: at a root atom all edges of E are root–root; at a far atom F has no edge
  have hFcl : Closed F := by
    intro y
    by_cases hy : IsFar j y
    · have : degS F y = 0 := by
        unfold degS
        rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
        intro e he hye
        exact ((Finset.mem_filter.mp he).2 y hye) hy
      rw [this]; exact Even.zero
    · have : degS F y = degS E y := by
        unfold degS
        congr 1
        ext e
        simp only [Finset.mem_filter, hF]
        constructor
        · rintro ⟨⟨he, -⟩, hye⟩; exact ⟨he, hye⟩
        · rintro ⟨he, hye⟩
          refine ⟨⟨he, ?_⟩, hye⟩
          intro z hz hzf
          induction e using Sym2.ind with
          | _ a b =>
            have hc := hno _ he
            rw [isCrossS_mk] at hc
            rcases Sym2.mem_iff.mp hye with rfl | rfl <;> rcases Sym2.mem_iff.mp hz with rfl | rfl <;> tauto
      rw [this]; exact hcl y
  -- F is nonempty: an edge of E at v is root–root
  have hFne : F.Nonempty := by
    have : 0 < (E.filter (fun e => v ∈ e)).card := hv
    obtain ⟨e, he⟩ := Finset.card_pos.mp this
    refine ⟨e, Finset.mem_filter.mpr ⟨(Finset.mem_filter.mp he).1, ?_⟩⟩
    intro z hz hzf
    have hve := (Finset.mem_filter.mp he).2
    induction e using Sym2.ind with
    | _ a b =>
      have hc := hno _ (Finset.mem_filter.mp he).1
      rw [isCrossS_mk] at hc
      rcases Sym2.mem_iff.mp hve with rfl | rfl <;> rcases Sym2.mem_iff.mp hz with rfl | rfl <;> tauto
  have hFE : F = E := hmin F (Finset.filter_subset _ _) hFne hFcl
  obtain ⟨e, he, hxe⟩ := hx
  rw [← hFE] at he
  exact (Finset.mem_filter.mp he).2 x hxe hxf

/-- Every atom of a polygon through `v` with `l` edges lies at bilayer at most `v.1 + l + 1`. -/
theorem reach_bound {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) {v x : Atom}
    (hv : 0 < degS E v) (hx : InE E x) : x.1 ≤ v.1 + E.card + 1 := by
  by_contra hlt
  push Not at hlt
  -- for every bilayer j with v.1 < j < x.1, E has a crossing edge at j; they are different edges
  set J := Finset.Ioo v.1 x.1 with hJ
  have hcross : ∀ j ∈ J, ∃ e ∈ E, IsCrossS j e := by
    intro j hj
    rw [Finset.mem_Ioo] at hj
    refine must_cross hE hv ?_ hx (Or.inl hj.2)
    unfold IsFar; omega
  choose! f hfE hfc using hcross
  have hinj : Set.InjOn f J := by
    intro j₁ hj₁ j₂ hj₂ h
    -- a crossing edge at j is a vertical bond of bilayer j
    obtain ⟨p, hp, -⟩ := cross_eq_vert (hE.2.1 _ (hfE j₁ hj₁)) (hfc j₁ hj₁)
    obtain ⟨q, hq, -⟩ := cross_eq_vert (hE.2.1 _ (hfE j₂ hj₂)) (hfc j₂ hj₂)
    rw [h, hq] at hp
    unfold vert at hp
    rcases Sym2.eq_iff.mp hp with h' | h'
    · exact (congrArg Prod.fst h'.1).symm
    · exact (congrArg Prod.fst h'.1).symm
  have hcard := Finset.card_le_card_of_injOn f (fun j hj => hfE j hj) hinj
  rw [hJ, Int.card_Ioo] at hcard
  omega

theorem isPolygon_mirror {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) :
    IsPolygon (mirS σ) (E.image mirE) := by
  obtain ⟨hne, hbond, hcl, hmin⟩ := hE
  refine ⟨hne.image _, ?_, closed_mirE hcl, ?_⟩
  · intro f hf
    obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp hf
    have hb := hbond e he
    induction e using Sym2.ind with
    | _ x y =>
      rw [bondS_mk] at hb
      show BondS _ s(mirA x, mirA y)
      rw [bondS_mk]; exact bond_mirA hb
  · intro F hF hFne hFcl
    have hsub : F.image mirE ⊆ E := by
      intro f hf
      obtain ⟨f', hf', rfl⟩ := Finset.mem_image.mp hf
      obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp (hF hf')
      rw [mirE_mirE]; exact he
    have := hmin _ hsub (hFne.image _) (closed_mirE hFcl)
    rw [← this]; exact (image_mirE_mirE F).symm

theorem inE_mirror {E : Finset (Sym2 Atom)} {x : Atom} (hx : InE E x) : InE (E.image mirE) (mirA x) := by
  obtain ⟨e, he, hxe⟩ := hx
  refine ⟨mirE e, Finset.mem_image_of_mem _ he, ?_⟩
  unfold mirE; exact Sym2.mem_map.mpr ⟨x, hxe, rfl⟩

/-- Every atom of a polygon through `v` with `l` edges lies at bilayer at least `v.1 − l − 1`. -/
theorem reach_bound_below {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) {v x : Atom}
    (hv : 0 < degS E v) (hx : InE E x) : v.1 - E.card - 1 ≤ x.1 := by
  have h := reach_bound (isPolygon_mirror hE) (v := mirA v) (x := mirA x)
    (by rw [degS_mirE]; exact hv) (inE_mirror hx)
  rw [Finset.card_image_of_injective _ mirE_injective] at h
  simp only [mirA] at h
  omega

theorem isSite_congr {σ τ : ℤ → ZMod 3} {a : Atom} (h : σ a.1 = τ a.1) : IsSite σ a ↔ IsSite τ a := by
  unfold IsSite; rw [h]

theorem bond_congr {σ τ : ℤ → ZMod 3} {a b : Atom} (ha : σ a.1 = τ a.1) (hb : σ b.1 = τ b.1) :
    Bond σ a b ↔ Bond τ a b := by
  unfold Bond; rw [isSite_congr ha, isSite_congr hb]

theorem polysA1_local_sub {σ τ : ℤ → ZMod 3} {v : Atom} {l : ℕ}
    (h : ∀ j, v.1 - l - 1 ≤ j → j ≤ v.1 + l + 1 → σ j = τ j) : PolysA1 σ v l ⊆ PolysA1 τ v l := by
  intro E ⟨⟨hne, hbond, hcl, hmin⟩, hv, hcard, hprof⟩
  have hpoly : IsPolygon σ E := ⟨hne, hbond, hcl, hmin⟩
  refine ⟨⟨hne, ?_, hcl, hmin⟩, hv, hcard, hprof⟩
  intro e he
  have hb := hbond e he
  induction e using Sym2.ind with
  | _ a b =>
    have ha : InE E a := ⟨_, he, Sym2.mem_mk_left a b⟩
    have hb' : InE E b := ⟨_, he, Sym2.mem_mk_right a b⟩
    have h1 := reach_bound hpoly hv ha
    have h2 := reach_bound_below hpoly hv ha
    have h3 := reach_bound hpoly hv hb'
    have h4 := reach_bound_below hpoly hv hb'
    rw [hcard] at h1 h2 h3 h4
    rw [bondS_mk] at hb ⊢
    exact (bond_congr (h a.1 (by omega) (by omega)) (h b.1 (by omega) (by omega))).mp hb

/-- **Locality.** Two stackings that agree on the bilayers within `l + 1` of `v` have exactly the same
polygons through `v` with `l` edges crossing every bilayer at most twice. -/
theorem polysA1_local {σ τ : ℤ → ZMod 3} {v : Atom} {l : ℕ}
    (h : ∀ j, v.1 - l - 1 ≤ j → j ≤ v.1 + l + 1 → σ j = τ j) : PolysA1 σ v l = PolysA1 τ v l :=
  Set.Subset.antisymm (polysA1_local_sub h) (polysA1_local_sub (fun j h1 h2 => (h j h1 h2).symm))

end LoopEqualityProof
