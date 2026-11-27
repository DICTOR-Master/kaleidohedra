module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1
public import LoopEquality.Finiteness
public import LoopEquality.Parts
public import LoopEquality.Counting

@[expose] public section

/-!
# Theorem B: the flip formula (Lean paper, Milestone 3d)

Study 2026-11-15-polygon-bijection §3. For `v` on the root side of bilayer `k` and a good centre `c`:

* `ncard_polys_sum`: the polygons through `v` with `l` edges are the disjoint union, over the crossing sets
  `P` inside a finite window, of those crossing bilayer `k` exactly at `P`.
* `polysCross_empty_flip`: polygons through `v` that do not cross bilayer `k` are the same in both stackings.
* `theoremB`: the number of polygons through `v` with `l` edges in the flipped stacking equals the number in
  `G σ` plus, summed over the nonempty crossing sets `P` whose vertical bonds are bonds,
  `#(FlipParts σ v l k P c) − #(PartsCross σ v l k P)`: every term is counted in `G σ` alone.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- Polygons of `G σ` through `v` with `l` edges. -/
def Polys (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) : Set (Finset (Sym2 Atom)) :=
  {E | IsPolygon σ E ∧ 0 < degS E v ∧ E.card = l}

theorem polys_finite (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) : (Polys σ v l).Finite := by
  apply Set.Finite.subset (Finset.finite_toSet ((box v (2 * l)).sym2.powerset))
  rintro E ⟨hpoly, hv, hcard⟩
  rw [Finset.mem_coe, Finset.mem_powerset]
  have := polygon_in_box hpoly hv
  rwa [hcard] at this

/-- The window of positions for crossing points. -/
noncomputable def window (v : Atom) (l : ℕ) : Finset (ℤ × ℤ) := (box v (2 * l)).image (fun a => a.2.1)

theorem ncard_polys_sum (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) :
    (Polys σ v l).ncard = ∑ P ∈ (window v l).powerset, (PolysCross σ v l k P).ncard := by
  have hcover : Polys σ v l = ⋃ P ∈ ((window v l).powerset : Set (Finset (ℤ × ℤ))), PolysCross σ v l k P := by
    ext E
    simp only [Set.mem_iUnion, exists_prop]
    constructor
    · rintro ⟨hE, hv, hcard⟩
      refine ⟨(window v l).filter (fun p => vert k p ∈ E), ?_, hE, hv, hcard, ?_⟩
      · rw [Finset.coe_powerset, Set.mem_preimage, Set.mem_powerset_iff, Finset.coe_subset]
        exact Finset.filter_subset _ _
      · intro p
        rw [Finset.mem_filter]
        refine ⟨fun h => h.2, fun h => ⟨?_, h⟩⟩
        have hb := polygon_in_box hE hv h
        rw [hcard, vert, Finset.mk_mem_sym2_iff] at hb
        exact Finset.mem_image.mpr ⟨_, hb.1, rfl⟩
    · rintro ⟨P, -, hE, hv, hcard, -⟩; exact ⟨hE, hv, hcard⟩
  rw [hcover, Set.Finite.ncard_biUnion (Finset.finite_toSet _)]
  · exact finsum_mem_coe_finset _ _
  · intro P _
    exact (polys_finite σ v l).subset (fun E ⟨hE, hv, hcard, _⟩ => ⟨hE, hv, hcard⟩)
  · intro P _ P' _ hne
    rw [Function.onFun, Set.disjoint_left]
    rintro E ⟨-, -, -, h1⟩ ⟨-, -, -, h2⟩
    exact hne (Finset.ext fun p => (h1 p).trans (h2 p).symm)

/-- A polygon through a root-side atom with no vertical bond at bilayer `k` lies wholly on the root side. -/
theorem root_of_no_cross {σ : ℤ → ZMod 3} {k : ℤ} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) {v : Atom}
    (hv : 0 < degS E v) (hvr : ¬ IsFar k v) (hno : ∀ p, vert k p ∉ E) :
    ∀ e ∈ E, ∀ w ∈ e, ¬ IsFar k w := by
  intro e he w hw hfar
  obtain ⟨a, b, hab, ha, hb⟩ := must_cross_gen hE (IsFar k) hv hvr ⟨e, he, hw⟩ hfar
  have hc : IsCrossS k s(a, b) := by rw [isCrossS_mk]; exact Or.inl ⟨ha, hb⟩
  obtain ⟨p, hp, -⟩ := cross_eq_vert (hE.2.1 _ hab) hc
  exact hno p (hp ▸ hab)

theorem polysCross_empty_flip {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ}
    (hc : GoodCentre σ k c) (hv : ¬ IsFar k v) :
    PolysCross (flipAt σ k) v l k ∅ = PolysCross σ v l k ∅ := by
  have key : ∀ {τ τ' : ℤ → ZMod 3}, (∀ a b, ¬ IsFar k a → ¬ IsFar k b → (Bond τ a b → Bond τ' a b)) →
      ∀ E ∈ PolysCross τ v l k ∅, E ∈ PolysCross τ' v l k ∅ := by
    intro τ τ' hb E ⟨hE, hdv, hcard, hP⟩
    have hno : ∀ p, vert k p ∉ E := fun p h => by simpa using (hP p).mpr h
    have hroot := root_of_no_cross hE hdv hv hno
    refine ⟨⟨hE.1, fun e he => ?_, hE.2.2.1, hE.2.2.2⟩, hdv, hcard, hP⟩
    have h1 := hE.2.1 e he
    have hs := hroot e he
    induction e using Sym2.ind with
    | _ a b =>
      rw [bondS_mk] at h1 ⊢
      exact hb a b (hs a (Sym2.mem_mk_left a b)) (hs b (Sym2.mem_mk_right a b)) h1
  ext E
  constructor
  · exact key (fun a b ha hb => (bond_root_flip hc ha hb).mpr) E
  · exact key (fun a b ha hb => (bond_root_flip hc ha hb).mp) E

theorem polysCross_eq_empty_of_not_bond {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {P : Finset (ℤ × ℤ)}
    (h : ¬ ∀ p ∈ P, BondS σ (vert k p)) : PolysCross σ v l k P = ∅ := by
  push Not at h
  obtain ⟨p, hp, hnb⟩ := h
  ext E
  simp only [Set.mem_empty_iff_false, iff_false]
  rintro ⟨hE, -, -, hP⟩
  exact hnb (hE.2.1 _ ((hP p).mp hp))

/-- **Theorem B (the flip formula).** For a good centre `c` of `σ` at bilayer `k` and `v` on the root side of
`k`, the polygons through `v` with `l` edges in the flipped stacking `flipAt σ k` number
`#(polygons in G σ) + ∑_P (#FlipParts σ v l k P c − #PartsCross σ v l k P)`, the sum over the nonempty
crossing sets `P` in the window whose vertical bonds are bonds of `G σ`. Every term on the right is counted in
`G σ` alone. -/
theorem theoremB {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hv : ¬ IsFar k v) :
    ((Polys (flipAt σ k) v l).ncard : ℤ) = (Polys σ v l).ncard +
      ∑ P ∈ ((window v l).powerset.filter (fun P => P.Nonempty ∧ ∀ p ∈ P, BondS σ (vert k p))),
        (((FlipParts σ v l k P c).ncard : ℤ) - (PartsCross σ v l k P).ncard) := by
  rw [ncard_polys_sum _ v l k, ncard_polys_sum _ v l k]
  push_cast
  rw [← sub_eq_iff_eq_add', ← Finset.sum_sub_distrib]
  rw [← Finset.sum_filter_add_sum_filter_not _ (fun P => P.Nonempty ∧ ∀ p ∈ P, BondS σ (vert k p))]
  have hrest : ∑ P ∈ (window v l).powerset.filter (fun P => ¬ (P.Nonempty ∧ ∀ p ∈ P, BondS σ (vert k p))),
      (((PolysCross (flipAt σ k) v l k P).ncard : ℤ) - (PolysCross σ v l k P).ncard) = 0 := by
    apply Finset.sum_eq_zero
    intro P hP
    have hn := (Finset.mem_filter.mp hP).2
    by_cases he : P.Nonempty
    · have hnb : ¬ ∀ p ∈ P, BondS σ (vert k p) := fun h => hn ⟨he, h⟩
      have hnb' : ¬ ∀ p ∈ P, BondS (flipAt σ k) (vert k p) := fun h =>
        hnb (fun p hp => bondS_vert_flip.mpr (h p hp))
      rw [polysCross_eq_empty_of_not_bond hnb, polysCross_eq_empty_of_not_bond hnb']; simp
    · rw [Finset.not_nonempty_iff_eq_empty.mp he, polysCross_empty_flip hc hv]; simp
  rw [hrest, add_zero]
  apply Finset.sum_congr rfl
  intro P hP
  obtain ⟨hne, hV⟩ := (Finset.mem_filter.mp hP).2
  rw [theoremB_count hc hv hne hV, ncard_polysCross hv hne hV]

end LoopEqualityProof
