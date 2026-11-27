module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage

@[expose] public section

/-!
# Propagation along paths (Lean paper, Milestone 3b, part 1)

Study 2026-11-15-polygon-bijection §3 (product structure).

Let `K` be an edge set with every degree at most 2 and `H ⊆ K` with even degree at every atom where `K`
has degree 2. If `H` contains an edge at an atom, it contains every edge of `K` at that atom
(`all_edges_of_touched`), and then every edge of `K` at every atom joined to it in `K`
(`propagate`). On a path of a linkage, `H` is therefore all or nothing.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- Every edge of `K` at `z` lies in `H`. -/
def AllAt (K H : Finset (Sym2 Atom)) (z : Atom) : Prop := ∀ e ∈ K, z ∈ e → e ∈ H

theorem all_edges_of_touched {K H : Finset (Sym2 Atom)} (hHK : H ⊆ K) (hle : ∀ y, degS K y ≤ 2)
    (hev : ∀ y, degS K y = 2 → Even (degS H y)) {z : Atom} (hz : ∃ e ∈ H, z ∈ e) : AllAt K H z := by
  intro e he hze
  have hsub : H.filter (fun e => z ∈ e) ⊆ K.filter (fun e => z ∈ e) :=
    Finset.filter_subset_filter _ hHK
  have hpos : 0 < degS H z := by
    obtain ⟨e', he', hz'⟩ := hz
    exact Finset.card_pos.mpr ⟨e', Finset.mem_filter.mpr ⟨he', hz'⟩⟩
  have hle' : degS H z ≤ degS K z := Finset.card_le_card hsub
  have heq : H.filter (fun e => z ∈ e) = K.filter (fun e => z ∈ e) := by
    apply Finset.eq_of_subset_of_card_le hsub
    change degS K z ≤ degS H z
    have h2 := hle z
    rcases (show degS K z = 1 ∨ degS K z = 2 by omega) with h | h
    · omega
    · have hevz := hev z h
      rcases hevz with ⟨m, hm⟩
      omega
  have : e ∈ K.filter (fun e => z ∈ e) := Finset.mem_filter.mpr ⟨he, hze⟩
  rw [← heq] at this
  exact (Finset.mem_filter.mp this).1

/-- **Propagation.** From an atom touched by `H`, every atom joined to it in `K` has all its `K`-edges in `H`. -/
theorem propagate {K H : Finset (Sym2 Atom)} (hHK : H ⊆ K) (hle : ∀ y, degS K y ≤ 2)
    (hev : ∀ y, degS K y = 2 → Even (degS H y)) {y z : Atom} (hy : ∃ e ∈ H, y ∈ e) (hyz : Conn K y z) :
    AllAt K H z := by
  induction hyz with
  | refl => exact all_edges_of_touched hHK hle hev hy
  | @tail b c _ hbc ih =>
    apply all_edges_of_touched hHK hle hev
    exact ⟨s(b, c), ih _ hbc.1 (Sym2.mem_mk_left b c), Sym2.mem_mk_right b c⟩

end LoopEqualityProof
