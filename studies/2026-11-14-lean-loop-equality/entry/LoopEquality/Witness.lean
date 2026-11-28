module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1
public import LoopEquality.Linkage
public import LoopEquality.Product
public import LoopEquality.Finiteness
public import LoopEquality.Parts

@[expose] public section

/-!
# A witness: the counts are not empty (Lean paper, countdown item 7)

The hexagon of diamond through the site `(0, (0, 0), 0)` in the puckered layer between bilayers `-1` and `0`:
lower atoms of bilayer `0` at `(0,0), (-3,0), (-3,3)`, upper atoms of bilayer `-1` at `(-1,-1), (-4,2), (-1,2)`.
It is a polygon with 6 edges crossing no bilayer, so the set counted by Corollary A at `l = 6` is nonempty.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

def hx0 : Atom := (0, (0, 0), 0)
def hx1 : Atom := (-1, (-1, -1), 1)
def hx2 : Atom := (0, (-3, 0), 0)
def hx3 : Atom := (-1, (-4, 2), 1)
def hx4 : Atom := (0, (-3, 3), 0)
def hx5 : Atom := (-1, (-1, 2), 1)

/-- The hexagon. -/
def hexE : Finset (Sym2 Atom) := {s(hx0, hx1), s(hx1, hx2), s(hx2, hx3), s(hx3, hx4), s(hx4, hx5), s(hx5, hx0)}

theorem hexE_card : hexE.card = 6 := by decide

theorem hexE_bonds : ∀ e ∈ hexE, BondS diamond e := by
  intro e he
  simp only [hexE, Finset.mem_insert, Finset.mem_singleton] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl <;>
    (rw [bondS_mk]; unfold Bond IsSite diamond shortVecs; simp only [hx0, hx1, hx2, hx3, hx4, hx5]; decide)

theorem degS_hexE (x : Atom) : degS hexE x = if x ∈ ({hx0, hx1, hx2, hx3, hx4, hx5} : Finset Atom) then 2 else 0 := by
  unfold degS hexE
  by_cases h0 : x = hx0
  · subst h0; decide
  by_cases h1 : x = hx1
  · subst h1; decide
  by_cases h2 : x = hx2
  · subst h2; decide
  by_cases h3 : x = hx3
  · subst h3; decide
  by_cases h4 : x = hx4
  · subst h4; decide
  by_cases h5 : x = hx5
  · subst h5; decide
  simp only [Finset.mem_insert, Finset.mem_singleton, h0, h1, h2, h3, h4, h5, or_self, ↓reduceIte]
  rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro e he hxe
  simp only [Finset.mem_insert, Finset.mem_singleton] at he
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl <;> rw [Sym2.mem_iff] at hxe <;> tauto

theorem hexE_closed : Closed hexE := fun x => by
  rw [degS_hexE]; split
  · exact even_two
  · exact Even.zero

/-- Around the hexagon every atom is joined to `hx0`. -/
theorem hexE_conn : ∀ x ∈ ({hx0, hx1, hx2, hx3, hx4, hx5} : Finset Atom), Conn hexE hx0 x := by
  have st : ∀ a b, s(a, b) ∈ hexE → a ≠ b → ∀ y, Conn hexE y a → Conn hexE y b :=
    fun a b h hne y hy => hy.tail ⟨h, hne⟩
  have m : ∀ {a b}, s(a, b) ∈ ({s(hx0, hx1), s(hx1, hx2), s(hx2, hx3), s(hx3, hx4), s(hx4, hx5), s(hx5, hx0)} :
      Finset (Sym2 Atom)) → s(a, b) ∈ hexE := fun h => h
  have c1 : Conn hexE hx0 hx1 := st _ _ (m (by simp)) (by decide) _ Relation.ReflTransGen.refl
  have c2 : Conn hexE hx0 hx2 := st _ _ (m (by simp)) (by decide) _ c1
  have c3 : Conn hexE hx0 hx3 := st _ _ (m (by simp)) (by decide) _ c2
  have c4 : Conn hexE hx0 hx4 := st _ _ (m (by simp)) (by decide) _ c3
  have c5 : Conn hexE hx0 hx5 := st _ _ (m (by simp)) (by decide) _ c4
  intro x hx
  simp only [Finset.mem_insert, Finset.mem_singleton] at hx
  rcases hx with rfl | rfl | rfl | rfl | rfl | rfl
  exacts [Relation.ReflTransGen.refl, c1, c2, c3, c4, c5]

theorem hexE_polygon : IsPolygon diamond hexE := by
  refine ⟨⟨_, Finset.mem_insert_self _ _⟩, hexE_bonds, hexE_closed, ?_⟩
  intro F hF hFne hFcl
  have hle : ∀ y, degS hexE y ≤ 2 := fun y => by rw [degS_hexE]; split <;> omega
  have hev : ∀ y, degS hexE y = 2 → Even (degS F y) := fun y _ => hFcl y
  obtain ⟨e, he⟩ := hFne
  obtain ⟨a, ha⟩ := exists_mem_sym2 e
  have hall : ∀ x ∈ ({hx0, hx1, hx2, hx3, hx4, hx5} : Finset Atom), AllAt hexE F x := by
    -- from the touched atom `a`, go to `hx0`, then around
    have haV : a ∈ ({hx0, hx1, hx2, hx3, hx4, hx5} : Finset Atom) := by
      by_contra hn
      have := degS_hexE a
      rw [if_neg hn] at this
      have : 0 < degS hexE a := Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨hF he, ha⟩⟩
      omega
    have h0 : AllAt hexE F hx0 := propagate hF hle hev ⟨e, he, ha⟩ (conn_symm (hexE_conn a haV))
    intro x hx
    exact propagate hF hle hev ⟨s(hx0, hx1), h0 _ (Finset.mem_insert_self _ _) (Sym2.mem_mk_left _ _),
      Sym2.mem_mk_left _ _⟩ (hexE_conn x hx)
  apply Finset.Subset.antisymm hF
  intro f hf
  have hfx := hf
  simp only [hexE, Finset.mem_insert, Finset.mem_singleton] at hfx
  rcases hfx with rfl | rfl | rfl | rfl | rfl | rfl <;>
    exact hall _ (by simp) _ hf (Sym2.mem_mk_left _ _)

theorem crossN_hexE (j : ℤ) : crossN hexE j = 0 := by
  unfold crossN
  rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro e he hc
  obtain ⟨p, hp, -⟩ := cross_eq_vert (hexE_bonds e he) hc
  subst hp
  simp only [hexE, Finset.mem_insert, Finset.mem_singleton, vert, hx0, hx1, hx2, hx3, hx4, hx5,
    Sym2.eq_iff, Prod.mk.injEq] at he
  omega

/-- **The count is not empty.** The hexagon is a polygon of diamond through `(0, (0, 0), 0)` with 6 edges
crossing every bilayer at most twice. -/
theorem hexE_mem : hexE ∈ PolysA1 diamond (0, (0, 0), 0) 6 := by
  refine ⟨hexE_polygon, ?_, hexE_card, fun j => by rw [crossN_hexE]; omega⟩
  rw [degS_hexE]; simp [hx0]

theorem polysA1_diamond_six_pos : 0 < (PolysA1 diamond (0, (0, 0), 0) 6).ncard :=
  (Set.ncard_pos (polysA1_finite _ _ _)).mpr ⟨_, hexE_mem⟩

end LoopEqualityProof
