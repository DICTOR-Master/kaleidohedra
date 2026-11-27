module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Surgery
public import LoopEquality.Polygons
public import LoopEquality.TheoremA

@[expose] public section

/-!
# Linkages: every end has a partner (Lean paper, Milestone 3a, part 1)

Study 2026-11-15-polygon-bijection §3 (linkages and their pairings).

`LAdj L a b` says that `s(a, b)` is an edge of `L` with `a ≠ b`; `Conn L` is its reflexive–transitive
closure (joined by a path of edges of `L`).

* `handshake`: in a loopless edge set, the degrees over any finite set of atoms that contains both ends of
  every edge meeting it add up to twice the number of those edges.
* `partner_exists`: in a loopless edge set with every degree at most 2, an atom of degree 1 is joined to a
  second atom of degree 1.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- `s(a, b)` is an edge of `L` and `a ≠ b`. -/
def LAdj (L : Finset (Sym2 Atom)) (a b : Atom) : Prop := s(a, b) ∈ L ∧ a ≠ b

/-- Joined by a path of edges of `L`. -/
def Conn (L : Finset (Sym2 Atom)) : Atom → Atom → Prop := Relation.ReflTransGen (LAdj L)

theorem lAdj_symm {L : Finset (Sym2 Atom)} {a b : Atom} (h : LAdj L a b) : LAdj L b a :=
  ⟨by rw [Sym2.eq_swap]; exact h.1, fun e => h.2 e.symm⟩

theorem conn_symm {L : Finset (Sym2 Atom)} {a b : Atom} (h : Conn L a b) : Conn L b a := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hbc ih => exact Relation.ReflTransGen.head (lAdj_symm hbc) ih

/-- The atoms of `L`. -/
noncomputable def atomsOf (L : Finset (Sym2 Atom)) : Finset Atom := L.biUnion endsF

theorem mem_atomsOf {L : Finset (Sym2 Atom)} {x : Atom} : x ∈ atomsOf L ↔ ∃ e ∈ L, x ∈ e := by
  simp only [atomsOf, Finset.mem_biUnion, mem_endsF]

/-- **Handshake.** Let `C` be a finite set of atoms such that every edge of `L` meeting `C` has both ends in
`C`, and let `L` have no loops. Then the degrees over `C` add up to twice the number of edges meeting `C`. -/
theorem handshake (L : Finset (Sym2 Atom)) (C : Finset Atom) (hnd : ∀ e ∈ L, ¬ e.IsDiag)
    (hcl : ∀ e ∈ L, ∀ y ∈ e, y ∈ C → ∀ z ∈ e, z ∈ C) :
    ∑ y ∈ C, degS L y = 2 * (L.filter (fun e => ∃ y ∈ C, y ∈ e)).card := by
  unfold degS
  simp only [Finset.card_eq_sum_ones, Finset.sum_filter]
  rw [Finset.sum_comm]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro e he
  induction e using Sym2.ind with
  | _ a b =>
    have hab : a ≠ b := fun h => hnd _ he (by rw [h]; exact Sym2.mk_isDiag_iff.mpr rfl)
    by_cases hm : ∃ y ∈ C, y ∈ s(a, b)
    · obtain ⟨y, hyC, hy⟩ := hm
      have haC : a ∈ C := hcl _ he y hy hyC a (Sym2.mem_mk_left a b)
      have hbC : b ∈ C := hcl _ he y hy hyC b (Sym2.mem_mk_right a b)
      simp only [show (∃ y ∈ C, y ∈ s(a, b)) from ⟨y, hyC, hy⟩, ↓reduceIte]
      have : (∑ x ∈ C, if x ∈ s(a, b) then 1 else 0) = ∑ x ∈ ({a, b} : Finset Atom), 1 := by
        rw [← Finset.sum_filter]
        congr 1
        ext x; simp only [Finset.mem_filter, Finset.mem_insert, Finset.mem_singleton, Sym2.mem_iff]
        constructor
        · exact fun h => h.2
        · rintro (rfl | rfl)
          · exact ⟨haC, Or.inl rfl⟩
          · exact ⟨hbC, Or.inr rfl⟩
      rw [this, Finset.sum_const, Finset.card_pair hab]; rfl
    · simp only [hm, ↓reduceIte]
      apply Finset.sum_eq_zero
      intro x hx
      simp only [show x ∉ s(a, b) from fun h => hm ⟨x, hx, h⟩, ↓reduceIte]

/-- **Every end has a partner.** In a loopless edge set with every degree at most 2, an atom `x` of degree
1 is joined by a path of edges to another atom of degree 1. -/
theorem partner_exists (L : Finset (Sym2 Atom)) (hnd : ∀ e ∈ L, ¬ e.IsDiag) (hle : ∀ y, degS L y ≤ 2)
    {x : Atom} (hx : degS L x = 1) : ∃ y, y ≠ x ∧ degS L y = 1 ∧ Conn L x y := by
  by_contra hno
  push Not at hno
  -- the atoms joined to x
  set C := (insert x (atomsOf L)).filter (Conn L x) with hC
  have hxC : x ∈ C := Finset.mem_filter.mpr ⟨Finset.mem_insert_self _ _, Relation.ReflTransGen.refl⟩
  have hcl : ∀ e ∈ L, ∀ y ∈ e, y ∈ C → ∀ z ∈ e, z ∈ C := by
    intro e he y hy hyC z hz
    have hxy : Conn L x y := (Finset.mem_filter.mp hyC).2
    refine Finset.mem_filter.mpr ⟨Finset.mem_insert_of_mem (mem_atomsOf.mpr ⟨e, he, hz⟩), ?_⟩
    by_cases hyz : y = z
    · rw [← hyz]; exact hxy
    · refine Relation.ReflTransGen.tail hxy ⟨?_, hyz⟩
      induction e using Sym2.ind with
      | _ a b =>
        rcases Sym2.mem_iff.mp hy with rfl | rfl <;> rcases Sym2.mem_iff.mp hz with rfl | rfl
        · exact absurd rfl hyz
        · exact he
        · rw [Sym2.eq_swap]; exact he
        · exact absurd rfl hyz
  have hsum := handshake L C hnd hcl
  -- every atom of C other than x has even degree (0 or 2), x has degree 1: the sum is odd
  have hodd : Odd (∑ y ∈ C, degS L y) := by
    rw [← Finset.add_sum_erase C _ hxC, hx]
    have hev : Even (∑ y ∈ C.erase x, degS L y) := by
      apply Finset.even_sum
      intro y hy
      obtain ⟨hyx, hyC⟩ := Finset.mem_erase.mp hy
      have hconn : Conn L x y := (Finset.mem_filter.mp hyC).2
      have h1 : degS L y ≠ 1 := fun h => hno y hyx h hconn
      have h2 := hle y
      rcases (show degS L y = 0 ∨ degS L y = 2 by omega) with h | h
      · rw [h]; exact Even.zero
      · rw [h]; exact even_two
    rcases hev with ⟨m, hm⟩
    exact ⟨m, by rw [hm]; ring⟩
  rw [hsum] at hodd
  exact (Nat.not_even_iff_odd.mpr hodd) (even_two_mul _)

end LoopEqualityProof
