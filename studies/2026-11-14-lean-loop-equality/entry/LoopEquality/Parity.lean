module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.TheoremB

@[expose] public section

/-!
# Polygons have even length (the network is bipartite)

Every bond joins a lower atom (`u = 0`) to an upper atom (`u = 1`). In an edge set in which every atom has even degree,
the number of edges is the sum of the degrees of the lower atoms, so it is even: every polygon has an even number of
edges, and for odd `l` there are none (`polys_odd`).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem bond_lower_upper {σ : ℤ → ZMod 3} {a b : Atom} (h : Bond σ a b) : a.2.2 ≠ b.2.2 := by
  obtain ⟨-, -, hb⟩ := h
  rcases hb with ⟨-, -, h3⟩ | ⟨-, h2, h3, -⟩ | ⟨-, h2, h3, -⟩
  · exact h3
  · rw [h2, h3]; decide
  · rw [h2, h3]; decide

/-- The lower atom of an edge set's edge, as a set of atoms with `u = 0`. -/
theorem card_eq_sum_lower {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hb : ∀ e ∈ E, BondS σ e) :
    E.card = ∑ x ∈ (atomsOf E).filter (fun a => a.2.2 = 0), degS E x := by
  unfold degS
  rw [← Finset.card_biUnion]
  · congr 1
    ext e
    simp only [Finset.mem_biUnion, Finset.mem_filter]
    constructor
    · intro he
      have hbe := hb e he
      induction e using Sym2.ind with
      | _ a b =>
        rw [bondS_mk] at hbe
        have hne := bond_lower_upper hbe
        by_cases ha : a.2.2 = 0
        · exact ⟨a, ⟨mem_atomsOf.mpr ⟨_, he, Sym2.mem_mk_left a b⟩, ha⟩, he, Sym2.mem_mk_left a b⟩
        · have hb0 : b.2.2 = 0 := by
            have h1 : a.2.2 = 1 := by have := a.2.2.isLt; omega
            have := b.2.2.isLt; omega
          exact ⟨b, ⟨mem_atomsOf.mpr ⟨_, he, Sym2.mem_mk_right a b⟩, hb0⟩, he, Sym2.mem_mk_right a b⟩
    · rintro ⟨x, -, he, -⟩; exact he
  · intro x hx y hy hxy
    rw [Function.onFun, Finset.disjoint_left]
    intro e hex hey
    have he := (Finset.mem_filter.mp hex).1
    have hbe := hb e he
    have hx0 := (Finset.mem_filter.mp hx).2; have hy0 := (Finset.mem_filter.mp hy).2
    have hxe := (Finset.mem_filter.mp hex).2; have hye := (Finset.mem_filter.mp hey).2
    induction e using Sym2.ind with
    | _ a b =>
      rw [bondS_mk] at hbe
      have hne := bond_lower_upper hbe
      rcases Sym2.mem_iff.mp hxe with rfl | rfl <;> rcases Sym2.mem_iff.mp hye with rfl | rfl
      · exact hxy rfl
      · exact hne (hx0.trans hy0.symm)
      · exact hne (hy0.trans hx0.symm)
      · exact hxy rfl

theorem polygon_card_even {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) : Even E.card := by
  rw [card_eq_sum_lower hE.2.1]
  exact Finset.even_sum _ (fun x _ => hE.2.2.1 x)

theorem polys_odd (σ : ℤ → ZMod 3) (v : Atom) {l : ℕ} (hl : ¬ Even l) : Polys σ v l = ∅ := by
  ext E; simp only [Set.mem_empty_iff_false, iff_false]
  rintro ⟨hE, -, rfl⟩; exact hl (polygon_card_even hE)

/-- **Theorem 5 (a) of #102 for odd lengths.** There are no polygons of odd length, in any stacking. -/
theorem theorem5a_odd (σ τ : ℤ → ZMod 3) (v w : Atom) {l : ℕ} (hl : ¬ Even l) :
    (Polys σ v l).ncard = (Polys τ w l).ncard := by
  rw [polys_odd σ v hl, polys_odd τ w hl]

end LoopEqualityProof
