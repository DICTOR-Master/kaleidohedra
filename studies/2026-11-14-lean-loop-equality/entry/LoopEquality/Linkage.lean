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
* `ends_le_two`, `partner_unique`: and to exactly one (the component of an end, as a connected Mathlib graph,
  has at least as many edges as atoms minus one, which leaves room for two ends).

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

/-- The atoms joined to `x` by paths of edges of `L`. -/
noncomputable def compSet (L : Finset (Sym2 Atom)) (x : Atom) : Finset Atom := (insert x (atomsOf L)).filter (Conn L x)

theorem mem_compSet_self (L : Finset (Sym2 Atom)) (x : Atom) : x ∈ compSet L x :=
  Finset.mem_filter.mpr ⟨Finset.mem_insert_self _ _, Relation.ReflTransGen.refl⟩

theorem compSet_closed (L : Finset (Sym2 Atom)) (x : Atom) :
    ∀ e ∈ L, ∀ y ∈ e, y ∈ compSet L x → ∀ z ∈ e, z ∈ compSet L x := by
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

/-- The component of `x` as a finite simple graph. -/
def compGraph (L : Finset (Sym2 Atom)) (x : Atom) : SimpleGraph {y // y ∈ compSet L x} where
  Adj a b := s(a.1, b.1) ∈ L ∧ a.1 ≠ b.1
  symm := ⟨fun a b h => ⟨by rw [Sym2.eq_swap]; exact h.1, fun e => h.2 e.symm⟩⟩
  loopless := ⟨fun a h => h.2 rfl⟩

theorem compGraph_adj {L : Finset (Sym2 Atom)} {x : Atom} {a b : {y // y ∈ compSet L x}} :
    (compGraph L x).Adj a b ↔ s(a.1, b.1) ∈ L ∧ a.1 ≠ b.1 := Iff.rfl

theorem compGraph_connected (L : Finset (Sym2 Atom)) (x : Atom) : (compGraph L x).Connected := by
  have base : ∀ y, Conn L x y → ∀ hy : y ∈ compSet L x,
      (compGraph L x).Reachable ⟨x, mem_compSet_self L x⟩ ⟨y, hy⟩ := by
    intro y h
    induction h with
    | refl => intro _; exact SimpleGraph.Reachable.refl _
    | @tail b c hxb hbc ih =>
      intro hc
      have hb : b ∈ compSet L x :=
        Finset.mem_filter.mpr ⟨Finset.mem_insert_of_mem (mem_atomsOf.mpr ⟨_, hbc.1, Sym2.mem_mk_left b c⟩), hxb⟩
      exact (ih hb).trans (SimpleGraph.Adj.reachable (G := compGraph L x) (compGraph_adj.mpr ⟨hbc.1, hbc.2⟩))
  have : Nonempty {y // y ∈ compSet L x} := ⟨⟨x, mem_compSet_self L x⟩⟩
  refine ⟨fun u v => ?_⟩
  have hu := base u.1 (Finset.mem_filter.mp u.2).2 u.2
  have hv := base v.1 (Finset.mem_filter.mp v.2).2 v.2
  exact hu.symm.trans hv

theorem degree_compGraph (L : Finset (Sym2 Atom)) (x : Atom) (hnd : ∀ e ∈ L, ¬ e.IsDiag)
    (y : {y // y ∈ compSet L x}) : (compGraph L x).degree y = degS L y.1 := by
  rw [← SimpleGraph.card_neighborFinset_eq_degree]
  unfold degS
  apply Finset.card_bij (fun z _ => s(y.1, z.1))
  · intro z hz
    rw [SimpleGraph.mem_neighborFinset] at hz
    exact Finset.mem_filter.mpr ⟨(compGraph_adj.mp hz).1, Sym2.mem_mk_left _ _⟩
  · intro z₁ hz₁ z₂ hz₂ h
    rw [SimpleGraph.mem_neighborFinset] at hz₁ hz₂
    rcases Sym2.eq_iff.mp h with ⟨-, h2⟩ | ⟨h1, h2⟩
    · exact Subtype.ext h2
    · exact absurd h2.symm (compGraph_adj.mp hz₁).2
  · intro e he
    obtain ⟨heL, hye⟩ := Finset.mem_filter.mp he
    have hw : Sym2.Mem.other hye ∈ compSet L x :=
      compSet_closed L x e heL y.1 hye y.2 _ (Sym2.other_mem hye)
    refine ⟨⟨_, hw⟩, ?_, Sym2.other_spec hye⟩
    rw [SimpleGraph.mem_neighborFinset]
    refine compGraph_adj.mpr ⟨by rw [Sym2.other_spec hye]; exact heL, fun h => ?_⟩
    apply hnd e heL
    rw [← Sym2.other_spec hye]
    exact Sym2.mk_isDiag_iff.mpr h

/-- **At most two ends in a component.** In a loopless edge set with every degree at most 2, the atoms of
degree 1 joined to `x` are at most two. -/
theorem ends_le_two (L : Finset (Sym2 Atom)) (hnd : ∀ e ∈ L, ¬ e.IsDiag) (hle : ∀ y, degS L y ≤ 2)
    (x : Atom) (hx : 0 < degS L x) : ((compSet L x).filter (fun y => degS L y = 1)).card ≤ 2 := by
  have hpos : ∀ y ∈ compSet L x, 0 < degS L y := by
    intro y hy
    rcases Finset.mem_insert.mp (Finset.mem_filter.mp hy).1 with rfl | hy'
    · exact hx
    · obtain ⟨e, he, hye⟩ := mem_atomsOf.mp hy'
      exact Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨he, hye⟩⟩
  have hsum : ∑ y ∈ compSet L x, degS L y = 2 * (compGraph L x).edgeFinset.card := by
    rw [← SimpleGraph.sum_degrees_eq_twice_card_edges, ← Finset.sum_coe_sort (compSet L x)]
    exact Finset.sum_congr rfl (fun y _ => (degree_compGraph L x hnd y).symm)
  have hconn := (compGraph_connected L x).card_vert_le_card_edgeSet_add_one
  rw [Nat.card_eq_fintype_card, Fintype.card_coe, Nat.card_eq_fintype_card,
    ← SimpleGraph.edgeFinset_card] at hconn
  have hsplit : ∑ y ∈ compSet L x, degS L y + ((compSet L x).filter (fun y => degS L y = 1)).card = 2 * (compSet L x).card := by
    rw [Finset.card_eq_sum_ones ((compSet L x).filter _), Finset.sum_filter, ← Finset.sum_add_distrib, Finset.card_eq_sum_ones,
      Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro y hy
    have h1 := hpos y hy
    have h2 := hle y
    by_cases h : degS L y = 1
    · simp [h]
    · simp only [h, ↓reduceIte, add_zero, mul_one]; omega
  omega

/-- **Exactly one partner.** In a loopless edge set with every degree at most 2, an atom of degree 1 is
joined to exactly one other atom of degree 1. -/
theorem partner_unique (L : Finset (Sym2 Atom)) (hnd : ∀ e ∈ L, ¬ e.IsDiag) (hle : ∀ y, degS L y ≤ 2)
    {x y z : Atom} (hx : degS L x = 1) (hy : degS L y = 1) (hz : degS L z = 1) (hyx : y ≠ x) (hzx : z ≠ x)
    (hxy : Conn L x y) (hxz : Conn L x z) : y = z := by
  by_contra hyz
  have hmem : ∀ w, degS L w = 1 → Conn L x w → w ∈ (compSet L x).filter (fun y => degS L y = 1) := by
    intro w hw hc
    refine Finset.mem_filter.mpr ⟨Finset.mem_filter.mpr ⟨?_, hc⟩, hw⟩
    by_cases hwx : w = x
    · rw [hwx]; exact Finset.mem_insert_self _ _
    · apply Finset.mem_insert_of_mem
      have : 0 < degS L w := by omega
      obtain ⟨e, he⟩ := Finset.card_pos.mp this
      exact mem_atomsOf.mpr ⟨e, (Finset.mem_filter.mp he).1, (Finset.mem_filter.mp he).2⟩
  have h3 : ({x, y, z} : Finset Atom) ⊆ (compSet L x).filter (fun y => degS L y = 1) := by
    intro w hw
    simp only [Finset.mem_insert, Finset.mem_singleton] at hw
    rcases hw with rfl | rfl | rfl
    · exact hmem w hx Relation.ReflTransGen.refl
    · exact hmem w hy hxy
    · exact hmem w hz hxz
  have hcard := Finset.card_le_card h3
  rw [Finset.card_insert_of_notMem (by simp [Ne.symm hyx, Ne.symm hzx]),
    Finset.card_pair hyz] at hcard
  have := ends_le_two L hnd hle x (by omega)
  omega

end LoopEqualityProof
