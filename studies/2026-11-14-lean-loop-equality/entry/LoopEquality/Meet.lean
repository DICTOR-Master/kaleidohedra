module

public import Mathlib
public import LoopEquality.FourPoint
public import LoopEquality.SingleArc

@[expose] public section

/-!
# Locality for four crossing points: the far asymmetry counts meeting arcs

`Fc(P, a b | c d, s) = Σ_i Fc({a,b}, i) · Fc({c,d}, s - i) − #(pairs of such arcs with a common atom)`; the products are
unchanged by a good half-turn (single arcs, `Fc_two`), so the far asymmetry is the change in the number of meeting pairs.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

section M

variable {τ : ℤ → ZMod 3} {k : ℤ}

/-- All pairs (arc `a`–`b`, arc `c`–`d`) with `s` edges in all. -/
def ArcPairs (τ : ℤ → ZMod 3) (k : ℤ) (a b c d : ℤ × ℤ) (s : ℕ) : Set (Finset (Sym2 Atom) × Finset (Sym2 Atom)) :=
  {x | FarL τ k {a, b} x.1 ∧ pairF k x.1 {a, b} = pr2 a b ∧ FarL τ k {c, d} x.2 ∧ pairF k x.2 {c, d} = pr2 c d ∧
    x.1.card + x.2.card = s}

/-- Those that share an atom. -/
def MeetPairs (τ : ℤ → ZMod 3) (k : ℤ) (a b c d : ℤ × ℤ) (s : ℕ) : Set (Finset (Sym2 Atom) × Finset (Sym2 Atom)) :=
  {x | x ∈ ArcPairs τ k a b c d s ∧ ¬ AtomDisj x.1 x.2}

theorem arcPairs_eq (a b c d : ℤ × ℤ) (s : ℕ) :
    ArcPairs τ k a b c d s = ⋃ i ∈ ((Finset.range (s + 1) : Finset ℕ) : Set ℕ),
      FarSet τ k {a, b} (pr2 a b) i ×ˢ FarSet τ k {c, d} (pr2 c d) (s - i) := by
  ext x
  simp only [ArcPairs, FarSet, Set.mem_setOf_eq, Set.mem_iUnion, Set.mem_prod, Finset.coe_range, Set.mem_Iio,
    exists_prop]
  constructor
  · rintro ⟨h1, h2, h3, h4, h5⟩
    exact ⟨x.1.card, by omega, ⟨h1, rfl, h2⟩, ⟨h3, by omega, h4⟩⟩
  · rintro ⟨i, hi, ⟨h1, e1, h2⟩, ⟨h3, e2, h4⟩⟩
    exact ⟨h1, h2, h3, h4, by omega⟩

theorem arcPairs_finite (a b c d : ℤ × ℤ) (s : ℕ) : (ArcPairs τ k a b c d s).Finite := by
  rw [arcPairs_eq]
  exact Set.Finite.biUnion (Finset.finite_toSet _) (fun i _ =>
    (farSet_finite τ k _ _ _).prod (farSet_finite τ k _ _ _))

theorem ncard_arcPairs (a b c d : ℤ × ℤ) (s : ℕ) :
    ((ArcPairs τ k a b c d s).ncard : ℤ) =
      ∑ i ∈ Finset.range (s + 1), Fc τ k {a, b} (pr2 a b) i * Fc τ k {c, d} (pr2 c d) (s - i) := by
  rw [arcPairs_eq, Set.Finite.ncard_biUnion (Finset.finite_toSet _)]
  · rw [finsum_mem_coe_finset]; push_cast
    exact Finset.sum_congr rfl (fun i _ => by rw [Set.ncard_prod]; unfold Fc; push_cast; ring)
  · intro i _; exact (farSet_finite τ k _ _ _).prod (farSet_finite τ k _ _ _)
  · intro i _ j _ hij
    rw [Function.onFun, Set.disjoint_left]
    rintro x ⟨⟨-, e1, -⟩, ⟨-, e2, -⟩⟩ ⟨⟨-, e1', -⟩, ⟨-, e2', -⟩⟩
    apply hij; omega

theorem fc_four_meet (hdis : ∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c, d} : Finset (ℤ × ℤ)), p ≠ q) (s : ℕ) :
    Fc τ k {a, b, c, d} (pr2 a b ∪ pr2 c d) s =
      ∑ i ∈ Finset.range (s + 1), Fc τ k {a, b} (pr2 a b) i * Fc τ k {c, d} (pr2 c d) (s - i) -
        (MeetPairs τ k a b c d s).ncard := by
  rw [fc_four hdis, ← ncard_arcPairs]
  have hsplit : ArcPairs τ k a b c d s = TwoArcs τ k a b c d s ∪ MeetPairs τ k a b c d s := by
    ext x; simp only [ArcPairs, TwoArcs, MeetPairs, Set.mem_union, Set.mem_setOf_eq]
    constructor
    · rintro ⟨h1, h2, h3, h4, h5⟩
      by_cases hd : AtomDisj x.1 x.2
      · exact Or.inl ⟨h1, h2, h3, h4, h5, hd⟩
      · exact Or.inr ⟨⟨h1, h2, h3, h4, h5⟩, hd⟩
    · rintro (⟨h1, h2, h3, h4, h5, -⟩ | ⟨h, -⟩)
      · exact ⟨h1, h2, h3, h4, h5⟩
      · exact h
  have hdisj : Disjoint (TwoArcs τ k a b c d s) (MeetPairs τ k a b c d s) := by
    rw [Set.disjoint_left]; rintro x ⟨-, -, -, -, -, hd⟩ ⟨-, hnd⟩; exact hnd hd
  have hfin := arcPairs_finite (τ := τ) (k := k) a b c d s
  rw [hsplit] at hfin ⊢
  rw [Set.ncard_union_eq hdisj (hfin.subset Set.subset_union_left) (hfin.subset Set.subset_union_right)]
  push_cast; ring

end M

theorem gP_pair (c a b : ℤ × ℤ) : gP c {a, b} = {c - a, c - b} := by
  unfold gP; simp [Finset.image_insert]

theorem gP_quad (c a b e f : ℤ × ℤ) : gP c {a, b, e, f} = {c - a, c - b, c - e, c - f} := by
  unfold gP; simp [Finset.image_insert]

theorem gM_pr2 (c a b : ℤ × ℤ) : gM c (pr2 a b) = pr2 (c - a) (c - b) := by
  unfold gM pr2
  ext ⟨x, y⟩
  simp only [Finset.mem_image, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton, gg, Prod.mk.injEq]
  constructor
  · rintro ⟨⟨p, q⟩, ⟨hp, hq⟩, rfl, rfl⟩
    simp only at hp hq
    rcases hp with rfl | rfl <;> rcases hq with rfl | rfl <;> simp
  · rintro ⟨hx, hy⟩
    refine ⟨⟨c - x, c - y⟩, ⟨?_, ?_⟩, by simp, by simp⟩
    · rcases hx with rfl | rfl <;> simp
    · rcases hy with rfl | rfl <;> simp

theorem gM_union (c : ℤ × ℤ) (M N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : gM c (M ∪ N) = gM c M ∪ gM c N := by
  unfold gM; exact Finset.image_union _ _

/-- **Locality.** For four crossing points paired `a b | e f`, the far asymmetry is the change in the number of
pairs of arcs that meet. -/
theorem Af_four {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {a b e f : ℤ × ℤ}
    (hV : ∀ p ∈ ({a, b, e, f} : Finset (ℤ × ℤ)), (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k)
    (hdis : ∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({e, f} : Finset (ℤ × ℤ)), p ≠ q) (s : ℕ) :
    Af σ k c {a, b, e, f} (pr2 a b ∪ pr2 e f) s =
      ((MeetPairs σ k (c - a) (c - b) (c - e) (c - f) s).ncard : ℤ) - (MeetPairs σ k a b e f s).ncard := by
  have hdis' : ∀ p ∈ ({c - a, c - b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c - e, c - f} : Finset (ℤ × ℤ)), p ≠ q := by
    intro p hp q hq hpq
    simp only [Finset.mem_insert, Finset.mem_singleton] at hp hq
    have : ∀ x ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ y ∈ ({e, f} : Finset (ℤ × ℤ)), c - x ≠ c - y :=
      fun x hx y hy h => hdis x hx y hy (by simpa using h)
    rcases hp with rfl | rfl <;> rcases hq with rfl | rfl <;> exact this _ (by simp) _ (by simp) hpq
  unfold Af
  rw [gP_quad, gM_union, gM_pr2, gM_pr2, fc_four_meet hdis, fc_four_meet hdis']
  have hprod : ∀ i ∈ Finset.range (s + 1),
      Fc σ k {a, b} (pr2 a b) i * Fc σ k {e, f} (pr2 e f) (s - i) =
      Fc σ k {c - a, c - b} (pr2 (c - a) (c - b)) i * Fc σ k {c - e, c - f} (pr2 (c - e) (c - f)) (s - i) := by
    intro i _
    rw [Fc_two hc (hV a (by simp)) (hV b (by simp)) (pr2 a b) i, Fc_two hc (hV e (by simp)) (hV f (by simp)) (pr2 e f) (s - i),
      gP_pair, gP_pair, gM_pr2, gM_pr2]
  rw [Finset.sum_congr rfl hprod]
  ring

end LoopEqualityProof
