module

public import Mathlib
public import LoopEquality.Mt

@[expose] public section

/-!
# The weighted root count: summing over the lattice translates of `v`

For a crossing set `S`, summing the root count through `v + 3 f` over all shifts `f` counts each root linkage at `S`
once for every atom of it of `v`'s kind (same bilayer and sublayer). So the (6, 6) sum depends on `v` only through
its kind.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

/-- Atoms of the kind of `w` (the mirrored `v`): same layer and sublayer, position differing by a lattice vector. -/
def typB (w : Atom) (y : Atom) : Bool :=
  y.1 == w.1 && y.2.2 == w.2.2 && ((y.2.1.1 - w.2.1.1) % 3 == 0) && ((y.2.1.2 - w.2.1.2) % 3 == 0)

/-- The weighted root count: pairs of disjoint arcs, each weighted by its atoms of `w`'s kind. -/
def wRootL (τ : ℤ → ZMod 3) (k : ℤ) (a b c d : ℤ × ℤ) (s : ℕ) (w : Atom) : ℤ :=
  ∑ i ∈ Finset.range (s + 1), ((((arcList τ k a b i) ×ˢ (arcList τ k c d (s - i))).filter
    (fun x => disjB x.1 x.2)).map (fun x => ((x.1 ++ x.2).countP (typB w) : ℤ))).sum

theorem bondChain_cons {σ : ℤ → ZMod 3} {x : Atom} {l : List Atom} (h : BondChain σ (x :: l)) : BondChain σ l := by
  cases l with
  | nil => trivial
  | cons y t => exact h.2

/-- Along a chain of bonds, every atom is within `2 n` of the last one (`n` bonds). -/
theorem chain_bound {σ : ℤ → ZMod 3} : ∀ (l : List Atom) (hne : l ≠ []), BondChain σ l → ∀ y ∈ l,
    |y.2.1.1 - (l.getLast hne).2.1.1| ≤ 2 * (l.length - 1 : ℤ) ∧ |y.2.1.2 - (l.getLast hne).2.1.2| ≤ 2 * (l.length - 1 : ℤ)
  | [x], _, _, y, hy => by rw [List.mem_singleton.mp hy]; simp
  | x :: z :: t, _, hc, y, hy => by
    have ih := chain_bound (z :: t) (List.cons_ne_nil _ _) hc.2
    have hlast : (x :: z :: t).getLast (List.cons_ne_nil _ _) = (z :: t).getLast (List.cons_ne_nil _ _) :=
      List.getLast_cons _
    rw [hlast]
    simp only [List.length_cons, Nat.cast_add, Nat.cast_one] at ih ⊢
    rcases List.mem_cons.mp hy with rfl | hy
    · obtain ⟨h1, h2⟩ := ih z List.mem_cons_self
      have hb := bond_steps hc.1
      constructor <;> rw [abs_le] at * <;> constructor <;> omega
    · obtain ⟨h1, h2⟩ := ih y hy
      constructor <;> rw [abs_le] at * <;> constructor <;> omega

theorem farPath_bound {τ : ℤ → ZMod 3} {k : ℤ} {p q : ℤ × ℤ} {i : ℕ} {l : List Atom} (hl : l ∈ arcList τ k p q i)
    {y : Atom} (hy : y ∈ l) : |y.2.1.1 - q.1| ≤ 2 * i ∧ |y.2.1.2 - q.2| ≤ 2 * i := by
  rw [mem_arcList] at hl
  obtain ⟨hh, hlast, hnd, hlen, hb, hf⟩ := hl
  have hne : l ≠ [] := by rintro rfl; simp at hh
  have hc : BondChain τ l := (bondChain_iff_edges l).mpr hb
  have hL : l.getLast hne = upA k q := by
    rw [List.getLast?_eq_getLast hne] at hlast; exact Option.some.inj hlast
  have := chain_bound l hne hc y hy
  rw [hL, hlen] at this
  simp only [upA, Nat.cast_add, Nat.cast_one, add_sub_cancel_right] at this
  exact this

theorem sum_list_map_comm {α : Type*} (T : Finset (ℤ × ℤ)) (g : (ℤ × ℤ) → α → ℤ) :
    ∀ L : List α, ∑ f ∈ T, (L.map (g f)).sum = (L.map (fun x => ∑ f ∈ T, g f x)).sum
  | [] => by simp
  | x :: L => by simp [Finset.sum_add_distrib, sum_list_map_comm T g L]

theorem len_filter_eq_sum {α : Type*} (P : α → Bool) : ∀ L : List α,
    ((L.filter P).length : ℤ) = (L.map (fun x => if P x then (1 : ℤ) else 0)).sum
  | [] => by simp
  | x :: L => by
    rw [List.filter_cons]; split <;> simp_all [len_filter_eq_sum P L] <;> ring

theorem filter_map_sum {α : Type*} (P : α → Bool) (g : α → ℤ) : ∀ L : List α,
    ((L.filter P).map g).sum = (L.map (fun x => if P x then g x else 0)).sum
  | [] => by simp
  | x :: L => by rw [List.filter_cons]; split <;> simp_all [filter_map_sum P g L]

theorem countP_eq_card {l : List Atom} (hnd : l.Nodup) (P : Atom → Bool) :
    (l.countP P : ℤ) = ((l.toFinset.filter (fun y => P y = true)).card : ℤ) := by
  rw [List.countP_eq_length_filter, ← List.toFinset_card_of_nodup (hnd.filter _)]
  congr 2; ext y; simp

/-- **Summing the root count through the translates of `v` gives the weighted root count.** -/
theorem sum_through_eq_weighted (τ : ℤ → ZMod 3) (k : ℤ) (v : Atom) {p q r t : ℤ × ℤ} (S : Finset (ℤ × ℤ))
    (hq : q ∈ S) (ht : t ∈ S) :
    ∑ f ∈ T16 v S, throughCountL τ k p q r t 6 (mirA (posA (sc f) v)) = wRootL τ k p q r t 6 (mirA v) := by
  classical
  unfold throughCountL wRootL
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl; intro i hi
  have hi6 : i ≤ 6 := by simpa [Nat.lt_succ_iff] using hi
  set L := (arcList τ k p q i) ×ˢ (arcList τ k r t (6 - i))
  simp only [len_filter_eq_sum]
  rw [sum_list_map_comm, filter_map_sum]
  apply congrArg List.sum
  apply List.map_congr_left
  rintro ⟨x₁, x₂⟩ hx
  obtain ⟨h1, h2⟩ := List.mem_product.mp hx
  simp only
  by_cases hd : disjB x₁ x₂ = true
  swap
  · simp [hd]
  simp only [hd, Bool.true_and, if_true]
  have hn1 : x₁.Nodup := (mem_arcList.mp h1).2.2.1
  have hn2 : x₂.Nodup := (mem_arcList.mp h2).2.2.1
  have hnd : (x₁ ++ x₂).Nodup := List.nodup_append.mpr ⟨hn1, hn2, fun a ha b hb hab => (disjB_iff.mp hd) a ha (hab ▸ hb)⟩
  rw [countP_eq_card hnd, Finset.sum_boole]
  have hb : ∀ f, ((x₁.contains (mirA (posA (sc f) v)) || x₂.contains (mirA (posA (sc f) v))) = true) ↔
      mirA (posA (sc f) v) ∈ x₁ ++ x₂ := by intro f; simp [List.contains_iff_mem]
  rw [Finset.filter_congr (fun f _ => hb f)]
  congr 1
  apply Finset.card_bij (fun f _ => mirA (posA (sc f) v))
  · intro f hf
    obtain ⟨-, hmem⟩ := Finset.mem_filter.mp hf
    refine Finset.mem_filter.mpr ⟨List.mem_toFinset.mpr hmem, ?_⟩
    simp [typB, mirA, posA, sc]
  · intro f _ g _ hfg
    have h := congrArg (fun a : Atom => a.2.1) hfg
    simp only [mirA, posA, sc] at h
    have h1 := congrArg Prod.fst h; have h2 := congrArg Prod.snd h
    simp only [Prod.fst_add, Prod.snd_add] at h1 h2
    ext <;> omega
  · intro y hy
    obtain ⟨hy, htyp⟩ := Finset.mem_filter.mp hy
    have hyl := List.mem_toFinset.mp hy
    simp only [typB, mirA, Bool.and_eq_true, beq_iff_eq] at htyp
    obtain ⟨⟨⟨e1, e2⟩, e3⟩, e4⟩ := htyp
    refine ⟨((y.2.1.1 - v.2.1.1) / 3, (y.2.1.2 - v.2.1.2) / 3), ?_, ?_⟩
    · refine Finset.mem_filter.mpr ⟨?_, ?_⟩
      · -- the bound
        have hbnd : ∃ z ∈ S, |y.2.1.1 - z.1| ≤ 12 ∧ |y.2.1.2 - z.2| ≤ 12 := by
          rcases List.mem_append.mp hyl with hy1 | hy2
          · obtain ⟨b1, b2⟩ := farPath_bound h1 hy1
            exact ⟨q, hq, by push_cast at b1; omega, by push_cast at b2; omega⟩
          · obtain ⟨b1, b2⟩ := farPath_bound h2 hy2
            exact ⟨t, ht, by push_cast at b1; omega, by push_cast at b2; omega⟩
        obtain ⟨z, hz, b1, b2⟩ := hbnd
        rw [abs_le] at b1 b2
        refine Finset.mem_biUnion.mpr ⟨z, hz, Finset.mem_product.mpr ⟨Finset.mem_Icc.mpr ⟨?_, ?_⟩,
          Finset.mem_Icc.mpr ⟨?_, ?_⟩⟩⟩ <;> simp only <;> omega
      · have : mirA (posA (sc ((y.2.1.1 - v.2.1.1) / 3, (y.2.1.2 - v.2.1.2) / 3)) v) = y := by
          obtain ⟨y0, ⟨y1, y2⟩, y3⟩ := y
          simp only at e1 e2 e3 e4 ⊢
          simp only [mirA, posA, sc]
          refine Prod.ext (by simp; omega) (Prod.ext (Prod.ext (by simp; omega) (by simp; omega)) ?_)
          simp only; rw [e2]
        rw [this]; exact hyl
    · obtain ⟨y0, ⟨y1, y2⟩, y3⟩ := y
      simp only at e1 e2 e3 e4 ⊢
      simp only [mirA, posA, sc]
      refine Prod.ext (by simp; omega) (Prod.ext (Prod.ext (by simp; omega) (by simp; omega)) ?_)
      simp only; rw [e2]

end LoopEqualityProof
