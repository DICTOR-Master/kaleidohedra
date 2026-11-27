module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1
public import LoopEquality.Locality

@[expose] public section

/-!
# Finitely many polygons (Lean paper, Milestone 2, finiteness)

* `must_cross_gen`: for any property `P` of atoms, a polygon with an edge at `v`, `¬ P v`, that reaches an
  atom with `P` has an edge with one end `P` and the other `¬ P` (minimality; generalises `must_cross`).
* `coord_bound`: if every bond changes a coordinate `f` by at most 2, every atom of a polygon through `v` with
  `l` edges has `f ≤ f v + 2l`.
* `polysA1_finite`: the polygons through `v` with `l` edges crossing every bilayer at most twice form a finite
  set (they all lie in a finite box around `v`).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem must_cross_gen {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) (P : Atom → Prop)
    {v x : Atom} (hv : 0 < degS E v) (hvP : ¬ P v) (hx : InE E x) (hxP : P x) :
    ∃ a b, s(a, b) ∈ E ∧ P a ∧ ¬ P b := by
  by_contra hno
  push Not at hno
  obtain ⟨-, -, hcl, hmin⟩ := hE
  set F := E.filter (fun e => ∀ y ∈ e, ¬ P y) with hF
  have hFcl : Closed F := by
    intro y
    by_cases hy : P y
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
          intro z hz hzP
          induction e using Sym2.ind with
          | _ a b =>
            rcases Sym2.mem_iff.mp hye with rfl | rfl <;> rcases Sym2.mem_iff.mp hz with rfl | rfl
            · exact hy hzP
            · exact hy (hno _ _ (by rw [Sym2.eq_swap]; exact he) hzP)
            · exact hy (hno _ _ he hzP)
            · exact hy hzP
      rw [this]; exact hcl y
  have hFne : F.Nonempty := by
    have : 0 < (E.filter (fun e => v ∈ e)).card := hv
    obtain ⟨e, he⟩ := Finset.card_pos.mp this
    refine ⟨e, Finset.mem_filter.mpr ⟨(Finset.mem_filter.mp he).1, ?_⟩⟩
    intro z hz hzP
    have hve := (Finset.mem_filter.mp he).2
    have heE := (Finset.mem_filter.mp he).1
    induction e using Sym2.ind with
    | _ a b =>
      rcases Sym2.mem_iff.mp hve with rfl | rfl <;> rcases Sym2.mem_iff.mp hz with rfl | rfl
      · exact hvP hzP
      · exact hvP (hno _ _ (by rw [Sym2.eq_swap]; exact heE) hzP)
      · exact hvP (hno _ _ heE hzP)
      · exact hvP hzP
  have hFE : F = E := hmin F (Finset.filter_subset _ _) hFne hFcl
  obtain ⟨e, he, hxe⟩ := hx
  rw [← hFE] at he
  exact (Finset.mem_filter.mp he).2 x hxe hxP

/-- If every edge of a polygon changes the coordinate `f` by at most 2, every atom of the polygon has
`f ≤ f v + 2 · (number of edges)`. -/
theorem coord_bound {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) (f : Atom → ℤ)
    (hf : ∀ a b, s(a, b) ∈ E → f a ≤ f b + 2 ∧ f b ≤ f a + 2) {v x : Atom} (hv : 0 < degS E v)
    (hx : InE E x) : f x ≤ f v + 2 * E.card := by
  by_contra hlt
  push Not at hlt
  set J := Finset.Ioc (f v) (f x) with hJ
  have hcross : ∀ t ∈ J, ∃ e ∈ E, ∃ a b, e = s(a, b) ∧ t ≤ f a ∧ f b < t := by
    intro t ht
    rw [Finset.mem_Ioc] at ht
    obtain ⟨a, b, hab, ha, hb⟩ := must_cross_gen hE (fun y => t ≤ f y) hv (by show ¬ t ≤ f v; omega) hx ht.2
    exact ⟨_, hab, a, b, rfl, ha, not_le.mp hb⟩
  choose! g hgE hgab using hcross
  -- each edge serves at most two values of t
  have hfib : ∀ e ∈ J.image g, (J.filter (fun t => g t = e)).card ≤ 2 := by
    intro e he
    obtain ⟨t0, ht0, rfl⟩ := Finset.mem_image.mp he
    obtain ⟨a, b, hab, ha, hb⟩ := hgab t0 ht0
    have hsub : J.filter (fun t => g t = g t0) ⊆ Finset.Ioc (f b) (f a) := by
      intro t ht
      obtain ⟨htJ, hgt⟩ := Finset.mem_filter.mp ht
      obtain ⟨a', b', hab', ha', hb'⟩ := hgab t htJ
      rw [hgt, hab] at hab'
      rw [Finset.mem_Ioc]
      rcases Sym2.eq_iff.mp hab' with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · omega
      · have := hf a b (hab ▸ hgE t0 ht0); omega
    have hab2 := hf a b (hab ▸ hgE t0 ht0)
    calc (J.filter (fun t => g t = g t0)).card ≤ (Finset.Ioc (f b) (f a)).card := Finset.card_le_card hsub
      _ ≤ 2 := by rw [Int.card_Ioc]; omega
  have hcard := Finset.card_le_mul_card_image J 2 hfib
  have himg : J.image g ⊆ E := by
    intro e he; obtain ⟨t, ht, rfl⟩ := Finset.mem_image.mp he; exact hgE t ht
  have := Finset.card_le_card himg
  have hJc : (J.card : ℤ) = f x - f v := by rw [hJ, Int.card_Ioc]; omega
  omega

theorem bond_steps {σ : ℤ → ZMod 3} {a b : Atom} (h : Bond σ a b) :
    (a.1 ≤ b.1 + 2 ∧ b.1 ≤ a.1 + 2) ∧ (a.2.1.1 ≤ b.2.1.1 + 2 ∧ b.2.1.1 ≤ a.2.1.1 + 2) ∧
      (a.2.1.2 ≤ b.2.1.2 + 2 ∧ b.2.1.2 ≤ a.2.1.2 + 2) := by
  obtain ⟨-, -, hb⟩ := h
  obtain ⟨j, ⟨p1, p2⟩, u⟩ := a
  obtain ⟨j', ⟨q1, q2⟩, u'⟩ := b
  simp only at hb ⊢
  have hs : ∀ x : ℤ × ℤ, x ∈ shortVecs → (-2 ≤ x.1 ∧ x.1 ≤ 2) ∧ (-2 ≤ x.2 ∧ x.2 ≤ 2) := by
    intro x hx
    simp only [shortVecs, Finset.mem_insert, Finset.mem_singleton] at hx
    rcases hx with rfl | rfl | rfl | rfl | rfl | rfl <;> simp
  rcases hb with ⟨h1, h2, -⟩ | ⟨h1, -, -, h4⟩ | ⟨h1, -, -, h4⟩
  · simp only [Prod.mk.injEq] at h2; omega
  · have := hs _ h4; simp only [Prod.fst_sub, Prod.snd_sub] at this; omega
  · have := hs _ h4; simp only [Prod.fst_sub, Prod.snd_sub] at this; omega

/-- The box of atoms within `r` of `v` in every coordinate. -/
noncomputable def box (v : Atom) (r : ℕ) : Finset Atom :=
  (Finset.Icc (v.1 - r) (v.1 + r)) ×ˢ ((Finset.Icc (v.2.1.1 - r) (v.2.1.1 + r)) ×ˢ
    (Finset.Icc (v.2.1.2 - r) (v.2.1.2 + r))) ×ˢ (Finset.univ : Finset (Fin 2))

theorem polygon_in_box {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) {v : Atom}
    (hv : 0 < degS E v) : E ⊆ (box v (2 * E.card)).sym2 := by
  intro e he
  have hb := hE.2.1 e he
  have hbound : ∀ x, InE E x → x ∈ box v (2 * E.card) := by
    intro x hx
    have step : ∀ (f : Atom → ℤ), (∀ a b, Bond σ a b → f a ≤ f b + 2 ∧ f b ≤ f a + 2) →
        f x ≤ f v + 2 * E.card ∧ f v ≤ f x + 2 * E.card := by
      intro f hfb
      have hE' : ∀ a b, s(a, b) ∈ E → f a ≤ f b + 2 ∧ f b ≤ f a + 2 := by
        intro a b hab; exact hfb a b (bondS_mk.mp (hE.2.1 _ hab))
      refine ⟨coord_bound hE f hE' hv hx, ?_⟩
      have := coord_bound hE (fun y => -f y) (fun a b hab => by have := hE' a b hab; omega) hv hx
      change -f x ≤ -f v + 2 * E.card at this; omega
    have h1 := step (fun y => y.1) (fun a b h => (bond_steps h).1)
    have h2 := step (fun y => y.2.1.1) (fun a b h => (bond_steps h).2.1)
    have h3 := step (fun y => y.2.1.2) (fun a b h => (bond_steps h).2.2)
    simp only [box, Finset.mem_product, Finset.mem_Icc, Finset.mem_univ, and_true]
    push_cast
    omega
  induction e using Sym2.ind with
  | _ a b =>
    rw [Finset.mk_mem_sym2_iff]
    exact ⟨hbound a ⟨_, he, Sym2.mem_mk_left a b⟩, hbound b ⟨_, he, Sym2.mem_mk_right a b⟩⟩

/-- **Finiteness.** The polygons through `v` with `l` edges crossing every bilayer at most twice form a
finite set. -/
theorem polysA1_finite (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) : (PolysA1 σ v l).Finite := by
  apply Set.Finite.subset (Finset.finite_toSet ((box v (2 * l)).sym2.powerset))
  rintro E ⟨hpoly, hv, hcard, -⟩
  rw [Finset.mem_coe, Finset.mem_powerset]
  have := polygon_in_box hpoly hv
  rwa [hcard] at this

end LoopEqualityProof
