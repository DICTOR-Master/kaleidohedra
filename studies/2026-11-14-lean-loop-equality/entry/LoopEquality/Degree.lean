module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Locality

@[expose] public section

/-!
# A polygon is a single cycle: every degree is at most 2 (Lean paper, Milestone 3b, degree lemma)

A polygon is a minimal nonempty edge set in which every atom has even degree. Here: every atom of a polygon
has degree 0 or 2 (`polygon_deg_le_two`).

Route. Take an edge `e = s(x, y)` and `E' = E \ {e}`.
* `joined_after_erase`: `x` and `y` are joined in `E'` (parity in the component of `x`).
* `erase_connected`: every atom of `E` is joined to `x` in `E'` (else the edges of `E'` at the component of
  `x`, with `e`, would be a smaller even set).
* `erase_acyclic`: the graph of `E'` on the atoms of `E` has no cycle (a cycle's edges would be a smaller
  even set).
* So it is a tree: `|E'| = |atoms| − 1`, `|E| = |atoms|`, and the handshake count forces every degree to 2.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem polygon_nodiag {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) :
    ∀ e ∈ E, ¬ e.IsDiag := by
  intro e he hd
  have hb := hE.2.1 e he
  induction e using Sym2.ind with
  | _ a b => rw [bondS_mk] at hb; exact bond_ne hb (Sym2.mk_isDiag_iff.mp hd)

theorem degS_erase (E : Finset (Sym2 Atom)) {e : Sym2 Atom} (he : e ∈ E) (z : Atom) :
    degS (E.erase e) z + (if z ∈ e then 1 else 0) = degS E z := by
  unfold degS
  rw [Finset.filter_erase]
  by_cases hz : z ∈ e
  · simp only [hz, ↓reduceIte]
    rw [Finset.card_erase_of_mem (Finset.mem_filter.mpr ⟨he, hz⟩)]
    have : 0 < (E.filter (fun e => z ∈ e)).card := Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨he, hz⟩⟩
    omega
  · simp only [hz, ↓reduceIte, add_zero]
    congr 1
    exact Finset.erase_eq_of_notMem (fun h => hz (Finset.mem_filter.mp h).2)

/-- `x` and `y` stay joined after removing the edge `s(x, y)` of a closed loopless set. -/
theorem joined_after_erase {E : Finset (Sym2 Atom)} (hcl : Closed E) (hnd : ∀ e ∈ E, ¬ e.IsDiag)
    {x y : Atom} (he : s(x, y) ∈ E) : Conn (E.erase s(x, y)) x y := by
  set E' := E.erase s(x, y) with hE'
  have hxy : x ≠ y := fun h => hnd _ he (by rw [h]; exact Sym2.mk_isDiag_iff.mpr rfl)
  have hnd' : ∀ f ∈ E', ¬ f.IsDiag := fun f hf => hnd f (Finset.mem_of_mem_erase hf)
  by_contra hno
  set C := compSet E' x
  have hsum := handshake E' C hnd' (compSet_closed E' x)
  -- degrees in E': odd only at x and y; y ∉ C
  have hyC : y ∉ C := fun h => hno (Finset.mem_filter.mp h).2
  have hodd : Odd (∑ z ∈ C, degS E' z) := by
    rw [← Finset.add_sum_erase C _ (mem_compSet_self E' x)]
    have hx := degS_erase E he x
    simp only [Sym2.mem_mk_left, ↓reduceIte] at hx
    rw [← hE'] at hx
    have hxe := hcl x
    have hev : Even (∑ z ∈ C.erase x, degS E' z) := by
      apply Finset.even_sum
      intro z hz
      obtain ⟨hzx, hzC⟩ := Finset.mem_erase.mp hz
      have hzy : z ≠ y := fun h => hyC (h ▸ hzC)
      have hzn : z ∉ s(x, y) := by rw [Sym2.mem_iff]; tauto
      have := degS_erase E he z
      simp only [hzn, ↓reduceIte, add_zero] at this
      rw [this]; exact hcl z
    have hpos : 0 < degS E x :=
      Finset.card_pos.mpr ⟨_, Finset.mem_filter.mpr ⟨he, Sym2.mem_mk_left x y⟩⟩
    rcases hxe with ⟨m, hm⟩
    rcases hev with ⟨k, hk⟩
    exact ⟨m + k - 1, by omega⟩
  rw [hsum] at hodd
  exact (Nat.not_even_iff_odd.mpr hodd) (even_two_mul _)

theorem conn_mem_compSet {L : Finset (Sym2 Atom)} {x z : Atom} (h : Conn L x z) : z ∈ compSet L x := by
  refine Finset.mem_filter.mpr ⟨?_, h⟩
  rcases Relation.ReflTransGen.cases_tail h with rfl | ⟨b, -, hbz⟩
  · exact Finset.mem_insert_self _ _
  · exact Finset.mem_insert_of_mem (mem_atomsOf.mpr ⟨_, hbz.1, Sym2.mem_mk_right b z⟩)

theorem degS_insert (S : Finset (Sym2 Atom)) {e : Sym2 Atom} (he : e ∉ S) (z : Atom) :
    degS (insert e S) z = degS S z + (if z ∈ e then 1 else 0) := by
  unfold degS
  rw [Finset.filter_insert]
  by_cases hz : z ∈ e
  · simp only [hz, ↓reduceIte]
    rw [Finset.card_insert_of_notMem (fun h => he (Finset.mem_filter.mp h).1)]
  · simp only [hz, ↓reduceIte, add_zero]

/-- After removing an edge `s(x, y)` of a polygon, every atom of the polygon is still joined to `x`. -/
theorem erase_connected {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) {x y : Atom}
    (he : s(x, y) ∈ E) {z : Atom} (hz : InE E z) : Conn (E.erase s(x, y)) x z := by
  have hnd := polygon_nodiag hE
  obtain ⟨-, -, hcl, hmin⟩ := hE
  set E' := E.erase s(x, y) with hE'
  set C := compSet E' x with hC
  have hxC : x ∈ C := mem_compSet_self E' x
  have hyC : y ∈ C := conn_mem_compSet (joined_after_erase hcl hnd he)
  have heE' : s(x, y) ∉ E' := Finset.notMem_erase _ _
  set M := E'.filter (fun f => ∃ w ∈ f, w ∈ C) with hM
  have heM : s(x, y) ∉ M := fun h => heE' (Finset.mem_filter.mp h).1
  have hMclosed : ∀ f ∈ M, ∀ w ∈ f, w ∈ C := by
    intro f hf w hw
    obtain ⟨hfE', u, hu, huC⟩ := Finset.mem_filter.mp hf
    exact compSet_closed E' x f hfE' u hu huC w hw
  set K := insert s(x, y) M with hK
  have hKcl : Closed K := by
    intro w
    rw [hK, degS_insert M heM]
    by_cases hw : w ∈ C
    · -- every edge of E' at w meets C
      have hdeg : degS M w = degS E' w := by
        unfold degS; congr 1
        ext f; simp only [Finset.mem_filter, hM]
        constructor
        · rintro ⟨⟨hf, -⟩, hwf⟩; exact ⟨hf, hwf⟩
        · rintro ⟨hf, hwf⟩; exact ⟨⟨hf, w, hwf, hw⟩, hwf⟩
      rw [hdeg, hE', degS_erase E he w]; exact hcl w
    · have hdeg : degS M w = 0 := by
        unfold degS
        rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
        intro f hf hwf
        exact hw (hMclosed f hf w hwf)
      have hwe : w ∉ s(x, y) := by
        rw [Sym2.mem_iff]; rintro (rfl | rfl)
        · exact hw hxC
        · exact hw hyC
      rw [hdeg]; simp only [hwe, ↓reduceIte, add_zero]; exact Even.zero
  have hKE : K ⊆ E := by
    intro f hf
    rcases Finset.mem_insert.mp hf with rfl | hfM
    · exact he
    · exact Finset.mem_of_mem_erase (Finset.mem_filter.mp hfM).1
  have hKeq := hmin K hKE ⟨_, Finset.mem_insert_self _ _⟩ hKcl
  -- z lies on an edge of E = K
  obtain ⟨f, hf, hzf⟩ := hz
  rw [← hKeq] at hf
  have hzC : z ∈ C := by
    rcases Finset.mem_insert.mp hf with rfl | hfM
    · rcases Sym2.mem_iff.mp hzf with rfl | rfl
      · exact hxC
      · exact hyC
    · exact hMclosed f hfM z hzf
  exact (Finset.mem_filter.mp hzC).2

end LoopEqualityProof
