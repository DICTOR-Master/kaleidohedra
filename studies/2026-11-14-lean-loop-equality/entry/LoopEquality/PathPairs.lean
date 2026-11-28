module

public import Mathlib
public import LoopEquality.Enum
public import LoopEquality.Meet

@[expose] public section

/-!
# Counting pairs of arcs by pairs of enumerated paths

Arcs from `a` to `b` with `i` edges are the paths in `arcList`; pairs of arcs with a condition read on their atoms are
counted by filtering the product of two such lists.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

/-- The far paths from `upA a` to `upA b` with `i` edges, enumerated. -/
def arcList (τ : ℤ → ZMod 3) (k : ℤ) (a b : ℤ × ℤ) (i : ℕ) : List (List Atom) :=
  (ext τ k i [upA k b]).filter (fun l => l.head? == some (upA k a))

theorem mem_arcList {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} {i : ℕ} {l : List Atom} :
    l ∈ arcList τ k a b i ↔ l ∈ FarPaths τ k a b i := by
  simp only [arcList, FarPaths, Set.mem_setOf_eq, List.mem_filter, beq_iff_eq]
  rw [mem_ext i [upA k b] (List.cons_ne_nil _ _) (List.nodup_singleton _) trivial]
  constructor
  · rintro ⟨⟨q, rfl, hq, hnd', hfar, hc⟩, hh⟩
    refine ⟨hh, by simp, hnd', by simp [hq], (bondChain_iff_edges _).mp hc, ?_⟩
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hfar x hx
    · rw [List.mem_singleton.mp hx]; exact isFar_upA k b
  · rintro ⟨hh, hl, hnd', hlen, hbond, hfar⟩
    obtain ⟨q, rfl⟩ : ∃ q, l = q ++ [upA k b] := by
      rcases List.eq_nil_or_concat l with h0 | ⟨q, x, h0⟩
      · rw [h0] at hh; simp at hh
      · refine ⟨q, ?_⟩; rw [h0] at hl ⊢; simp at hl; rw [List.concat_eq_append, hl]
    exact ⟨⟨q, rfl, by simpa using hlen, hnd', fun x hx => hfar x (by simp [hx]), (bondChain_iff_edges _).mpr hbond⟩, hh⟩

theorem arcList_nodup (τ : ℤ → ZMod 3) (k : ℤ) (a b : ℤ × ℤ) (i : ℕ) : (arcList τ k a b i).Nodup :=
  (ext_nodup (σ := τ) (k := k) i [upA k b] (List.cons_ne_nil _ _) (List.nodup_singleton _) trivial).filter _

section
variable {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} {i : ℕ}

theorem farPaths_len (hab : a ≠ b) {l : List Atom} (hl : l ∈ FarPaths τ k a b i) : 2 ≤ l.length := by
  obtain ⟨hh, hl', -⟩ := hl
  rcases l with _ | ⟨x, _ | ⟨y, t⟩⟩
  · simp at hh
  · simp at hh hl'; exact absurd (hh.symm.trans hl') (upA_ne hab)
  · simp

theorem path_to_arc (hab : a ≠ b) {l : List Atom} (hl : l ∈ FarPaths τ k a b i) :
    pathEdges l ∈ FarSet τ k {a, b} (pr2 a b) i := by
  have h2 := farPaths_len hab hl
  obtain ⟨hh, hl', hnd, hlen, hb, hf⟩ := hl
  obtain ⟨hL, hc, hconn⟩ := path_linkage' h2 hnd hh hl'
  exact ⟨⟨by rw [image_pair]; exact hL, fun e he w hw => hf w (atom_of_pathEdges he w hw), hb⟩, by omega,
    pairF_full hconn⟩

theorem arc_to_farPath (hab : a ≠ b) {F : Finset (Sym2 Atom)} (hF : F ∈ FarSet τ k {a, b} (pr2 a b) i) :
    ∃ l ∈ FarPaths τ k a b i, pathEdges l = F := by
  obtain ⟨⟨hL, hfar, hb⟩, hs, -⟩ := hF
  rw [image_pair] at hL
  obtain ⟨l, hh, hl, hnd, hlen, hE⟩ := arc_to_path F.card F _ _ rfl hL (upA_ne hab)
  obtain ⟨-, hc, -⟩ := path_linkage' hlen hnd hh hl
  refine ⟨l, ⟨hh, hl, hnd, by rw [hE] at hc; omega, by rw [hE]; exact hb, ?_⟩, hE⟩
  intro w hw
  have := mem_path_deg hlen hw
  rw [hE] at this
  obtain ⟨e, he, hwe⟩ := exists_edge_of_degS' this
  exact hfar e he w hwe

theorem farPath_inj (hab : a ≠ b) {l₁ l₂ : List Atom} (h1 : l₁ ∈ FarPaths τ k a b i) (h2 : l₂ ∈ FarPaths τ k a b i)
    (h : pathEdges l₁ = pathEdges l₂) : l₁ = l₂ :=
  path_unique l₁ l₂ _ h1.1 h2.1 h1.2.2.1 h2.2.2.1 (farPaths_len hab h1) (farPaths_len hab h2) h

theorem deg_path {l : List Atom} (h2 : 2 ≤ l.length) (w : Atom) : 0 < degS (pathEdges l) w ↔ w ∈ l :=
  ⟨fun h => by by_contra hw; rw [degS_pathEdges_out hw] at h; omega, fun h => mem_path_deg h2 h⟩

end

/-- **Pairs of arcs with a condition, counted by enumerated paths.** -/
theorem ncard_arcPairs_cond {τ : ℤ → ZMod 3} {k : ℤ} {a b c d : ℤ × ℤ} (hab : a ≠ b) (hcd : c ≠ d) (s : ℕ)
    (R : Finset (Sym2 Atom) × Finset (Sym2 Atom) → Prop) (r : List Atom × List Atom → Bool)
    (hRr : ∀ i l₁ l₂, l₁ ∈ FarPaths τ k a b i → l₂ ∈ FarPaths τ k c d (s - i) →
      (R (pathEdges l₁, pathEdges l₂) ↔ r (l₁, l₂) = true)) :
    (({x | x ∈ ArcPairs τ k a b c d s ∧ R x} : Set _).ncard : ℤ) =
      ∑ i ∈ Finset.range (s + 1), (((arcList τ k a b i) ×ˢ (arcList τ k c d (s - i))).filter r).length := by
  classical
  have hE : {x | x ∈ ArcPairs τ k a b c d s ∧ R x} = ⋃ i ∈ ((Finset.range (s + 1) : Finset ℕ) : Set ℕ),
      {x | x ∈ FarSet τ k {a, b} (pr2 a b) i ×ˢ FarSet τ k {c, d} (pr2 c d) (s - i) ∧ R x} := by
    rw [arcPairs_eq]; ext x; simp only [Set.mem_setOf_eq, Set.mem_iUnion, exists_prop]
    constructor
    · rintro ⟨⟨i, hi, hx⟩, hR⟩; exact ⟨i, hi, hx, hR⟩
    · rintro ⟨i, hi, hx, hR⟩; exact ⟨⟨i, hi, hx⟩, hR⟩
  rw [hE, Set.Finite.ncard_biUnion (Finset.finite_toSet _)]
  · rw [finsum_mem_coe_finset]; push_cast
    apply Finset.sum_congr rfl; intro i _
    have hnd : (((arcList τ k a b i) ×ˢ (arcList τ k c d (s - i))).filter r).Nodup :=
      ((arcList_nodup τ k a b i).product (arcList_nodup τ k c d (s - i))).filter _
    rw [← List.toFinset_card_of_nodup hnd, ← Set.ncard_coe_finset]
    congr 1
    symm
    apply Set.ncard_congr (fun y _ => (pathEdges y.1, pathEdges y.2))
    · rintro ⟨y1, y2⟩ hy
      simp only [List.coe_toFinset, Set.mem_setOf_eq, List.mem_filter] at hy
      obtain ⟨hp, hr⟩ := hy
      obtain ⟨h1, h2⟩ := List.mem_product.mp hp
      rw [mem_arcList] at h1 h2
      exact ⟨⟨path_to_arc hab h1, path_to_arc hcd h2⟩, (hRr i _ _ h1 h2).mpr hr⟩
    · rintro ⟨y1, y2⟩ ⟨z1, z2⟩ hy hz hyz
      simp only [List.coe_toFinset, Set.mem_setOf_eq, List.mem_filter] at hy hz
      obtain ⟨hy1, hy2⟩ := List.mem_product.mp hy.1
      obtain ⟨hz1, hz2⟩ := List.mem_product.mp hz.1
      rw [mem_arcList] at hy1 hy2 hz1 hz2
      simp only [Prod.mk.injEq] at hyz
      exact Prod.ext (farPath_inj hab hy1 hz1 hyz.1) (farPath_inj hcd hy2 hz2 hyz.2)
    · rintro ⟨F₁, F₂⟩ ⟨⟨h1, h2⟩, hR⟩
      obtain ⟨l₁, hl₁, e1⟩ := arc_to_farPath hab h1
      obtain ⟨l₂, hl₂, e2⟩ := arc_to_farPath hcd h2
      refine ⟨(l₁, l₂), ?_, by simp [e1, e2]⟩
      simp only [List.coe_toFinset, Set.mem_setOf_eq, List.mem_filter]
      refine ⟨List.mem_product.mpr ⟨mem_arcList.mpr hl₁, mem_arcList.mpr hl₂⟩, (hRr i _ _ hl₁ hl₂).mp ?_⟩
      rw [e1, e2]; exact hR
  · intro i _
    exact ((farSet_finite τ k _ _ _).prod (farSet_finite τ k _ _ _)).subset (fun x hx => hx.1)
  · intro i _ j _ hij
    rw [Function.onFun, Set.disjoint_left]
    rintro x ⟨⟨⟨-, e1, -⟩, -⟩, -⟩ ⟨⟨⟨-, e1', -⟩, -⟩, -⟩
    exact hij (e1.symm.trans e1')

end LoopEqualityProof
